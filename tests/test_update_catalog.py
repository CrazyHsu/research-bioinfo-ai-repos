from __future__ import annotations

import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError, URLError

from _load import load_script

uc = load_script("update_catalog")
ROOT = Path(__file__).resolve().parents[1]


def meta(full_name: str, stars: int = 10, **extra) -> dict:
    base = {
        "full_name": full_name, "html_url": f"https://github.com/{full_name}", "stargazers_count": stars,
        "forks_count": 2, "open_issues_count": 1, "created_at": "2025-01-02T00:00:00Z",
        "pushed_at": "2026-09-30T12:00:00Z", "updated_at": "2026-10-12T00:00:00Z", "archived": False,
        "license": {"spdx_id": "MIT"}, "language": "Python", "topics": ["mcp", "bio"],
        "homepage": "", "description": "GitHub description | with pipe",
    }
    base.update(extra)
    return base


def seed(repo: str, **extra) -> dict:
    row = {
        "repo": repo, "category": "Literature Search / Scholarly Search MCP", "type": "mcp-server",
        "type_detail": "", "interfaces": "mcp", "hosts": "", "domain": "research", "pinned": "",
        "notes": "English note", "notes_zh": "中文备注", "include": "yes",
    }
    row.update(extra)
    return row


def http_error(code: int, headers: dict | None = None) -> HTTPError:
    from email.message import Message
    msg = Message()
    for key, value in (headers or {}).items():
        msg[key] = value
    return HTTPError("https://api.github.com/repos/x/y", code, "err", msg, io.BytesIO(b""))


class RowFromMetaTests(unittest.TestCase):
    def test_fields_are_extracted(self):
        row = uc.row_from_meta(seed("a/b"), meta("a/b", stars=42), "2026-10-13")
        self.assertEqual(row["stars"], "42")
        self.assertEqual(row["pushed_at"], "2026-09-30")
        self.assertEqual(row["created_at"], "2025-01-02")
        self.assertEqual(row["license"], "MIT")
        self.assertEqual(row["topics"], "mcp,bio")
        self.assertEqual(row["archived"], "no")
        self.assertEqual(row["status"], "ok")
        self.assertEqual(row["fetched_at"], "2026-10-13")
        self.assertEqual(row["description"], "GitHub description / with pipe")
        self.assertEqual(row["notes"], "English note")

    def test_rename_is_recorded_without_changing_seed_key(self):
        row = uc.row_from_meta(seed("old/name"), meta("new/name"), "2026-10-13")
        self.assertEqual(row["repo"], "old/name")
        self.assertEqual(row["renamed_to"], "new/name")
        self.assertEqual(row["url"], "https://github.com/new/name")

    def test_noassertion_license_becomes_other(self):
        row = uc.row_from_meta(seed("a/b"), meta("a/b", license={"spdx_id": "NOASSERTION"}), "2026-10-13")
        self.assertEqual(row["license"], "other")


class RefreshTests(unittest.TestCase):
    def test_404_keeps_cached_row_and_marks_missing(self):
        old = uc.row_from_meta(seed("a/b"), meta("a/b", stars=5), "2026-10-05")
        existing = {"a/b": old}

        def fetcher(repo, token):
            raise http_error(404)

        rows, report = uc.refresh_from_github([seed("a/b")], existing, None, fetcher=fetcher)
        self.assertEqual(rows[0]["status"], "missing")
        self.assertEqual(rows[0]["stars"], "5")
        self.assertEqual(rows[0]["missing_since"], uc.today_utc())
        self.assertEqual(report["missing"], 1)
        self.assertEqual(rows[0]["fetched_at"], "2026-10-05")

    def test_404_without_cache_has_no_fetched_at(self):
        def fetcher(repo, token):
            raise http_error(404)

        rows, _ = uc.refresh_from_github([seed("typo/repo")], {}, None, fetcher=fetcher)
        self.assertEqual(rows[0]["status"], "missing")
        self.assertEqual(rows[0]["fetched_at"], "")

    def test_rate_limit_stops_fetching_and_uses_cache(self):
        calls = []
        old = uc.row_from_meta(seed("a/b"), meta("a/b"), "2026-10-05")

        def fetcher(repo, token):
            calls.append(repo)
            raise http_error(403, {"x-ratelimit-remaining": "0"})

        rows, report = uc.refresh_from_github([seed("a/b"), seed("c/d")], {"a/b": old}, None, fetcher=fetcher)
        self.assertEqual(calls, ["a/b"])
        self.assertTrue(report["rate_limited"])
        statuses = {row["repo"]: row["status"] for row in rows}
        self.assertEqual(statuses, {"a/b": "cached", "c/d": "pending"})

    def test_network_error_uses_cache(self):
        old = uc.row_from_meta(seed("a/b"), meta("a/b"), "2026-10-05")

        def fetcher(repo, token):
            raise URLError("boom")

        rows, report = uc.refresh_from_github([seed("a/b")], {"a/b": old}, None, fetcher=fetcher)
        self.assertEqual(rows[0]["status"], "cached")
        self.assertEqual(report["cached"], 1)

    def test_only_subset_leaves_others_cached_or_pending(self):
        old = uc.row_from_meta(seed("a/b"), meta("a/b", stars=1), "2026-10-05")
        fetched = []

        def fetcher(repo, token):
            fetched.append(repo)
            return meta(repo, stars=99)

        rows, _ = uc.refresh_from_github([seed("a/b"), seed("c/d")], {"a/b": old}, None, only={"c/d"}, fetcher=fetcher)
        self.assertEqual(fetched, ["c/d"])
        by_repo = {row["repo"]: row for row in rows}
        self.assertEqual(by_repo["a/b"]["stars"], "1")
        self.assertEqual(by_repo["c/d"]["stars"], "99")

    def test_rows_are_sorted_by_repo_name(self):
        def fetcher(repo, token):
            return meta(repo, stars={"b/x": 1, "A/y": 500}[repo])

        rows, _ = uc.refresh_from_github([seed("b/x"), seed("A/y")], {}, None, fetcher=fetcher)
        self.assertEqual([row["repo"] for row in rows], ["A/y", "b/x"])

    def test_archived_and_renamed_are_reported(self):
        def fetcher(repo, token):
            return meta("new/name", archived=True)

        _, report = uc.refresh_from_github([seed("old/name")], {}, None, fetcher=fetcher)
        self.assertEqual(report["archived"], ["old/name"])
        self.assertEqual(report["renamed"], ["old/name -> new/name"])


class ChangesTests(unittest.TestCase):
    def test_added_removed_and_gains(self):
        history = {
            "2026-10-05": {"a/b": {"stars": "10"}, "c/d": {"stars": "5"}},
            "2026-10-12": {"a/b": {"stars": "30"}, "e/f": {"stars": "1"}},
        }
        curated = [
            {"repo": "a/b", "archived": "yes", "status": "ok", "renamed_to": ""},
            {"repo": "e/f", "archived": "no", "status": "missing", "renamed_to": "g/h"},
        ]
        entries = uc.compute_changes(history, curated)
        latest = entries[0]
        self.assertEqual(latest["date"], "2026-10-12")
        self.assertEqual(latest["added"], ["e/f"])
        self.assertEqual(latest["removed"], ["c/d"])
        self.assertEqual(latest["gains"], [(20, "a/b", 10, 30)])
        self.assertEqual(latest["archived"], ["a/b"])
        self.assertEqual(latest["renamed"], ["e/f -> g/h"])
        self.assertEqual(latest["missing"], ["e/f"])
        self.assertIsNone(entries[1]["prev"])
        changelog = uc.render_changelog(entries)
        self.assertIn("## 2026-10-12 (vs 2026-10-05)", changelog)
        self.assertIn("`a/b` +20 (10 -> 30)", changelog)


class RenderTests(unittest.TestCase):
    def test_inject_preserves_prose_and_check_detects_markers(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "README.md"
            path.write_text(f"# Title\n\nprose\n\n{uc.MARK_START}\nold\n{uc.MARK_END}\n\ntail\n", encoding="utf-8")
            uc.inject(path, "NEW BODY")
            text = path.read_text(encoding="utf-8")
            self.assertIn("# Title\n\nprose\n\n", text)
            self.assertIn(f"{uc.MARK_START}\nNEW BODY\n{uc.MARK_END}\n\ntail\n", text)
            _, body, _ = uc.extract_body(text, path)
            self.assertEqual(body, "NEW BODY")
            path.write_text("no markers", encoding="utf-8")
            with self.assertRaises(SystemExit):
                uc.inject(path, "x")

    def test_table_marks_archived_and_pending(self):
        rows = [
            {"repo": "a/b", "url": "https://github.com/a/b", "type": "mcp-server", "stars": "3", "pushed_at": "2026-01-01", "notes": "n", "archived": "yes", "status": "ok"},
            {"repo": "c/d", "url": "https://github.com/c/d", "type": "skill", "stars": "", "pushed_at": "", "notes": "m", "status": "pending"},
        ]
        lines = uc.render_table(rows, "en")
        self.assertIn("| [a/b](https://github.com/a/b) (archived) | mcp-server | 3 | 2026-01-01 | n |", lines)
        self.assertIn("| [c/d](https://github.com/c/d) | skill | pending |  | m |", lines)
        zh = uc.render_table(rows, "zh")
        self.assertTrue(any("待抓取" in line for line in zh))


class CheckTests(unittest.TestCase):
    """End-to-end check on a temporary copy of the repository data."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for name in ("data", "skills", "README.md", "README-zh.md", "catalog.md"):
            src = ROOT / name
            if src.is_dir():
                shutil.copytree(src, self.tmp / name)
            else:
                shutil.copy(src, self.tmp / name)
        self.patches = [
            mock.patch.object(uc, "DATA", self.tmp / "data"),
            mock.patch.object(uc, "CONFIG_PATH", self.tmp / "data" / "catalog_config.json"),
            mock.patch.object(uc, "SEED_PATH", self.tmp / "data" / "repos.seed.tsv"),
            mock.patch.object(uc, "CURATED_PATH", self.tmp / "data" / "repos.curated.tsv"),
            mock.patch.object(uc, "HISTORY_PATH", self.tmp / "data" / "star_history.tsv"),
            mock.patch.object(uc, "LAST_REFRESH_PATH", self.tmp / "data" / "last_refresh.json"),
            mock.patch.object(uc, "REPORT_PATH", self.tmp / "data" / "refresh_report.md"),
            mock.patch.object(uc, "AWESOME_REFS_PATH", self.tmp / "data" / "awesome_refs.tsv"),
            mock.patch.object(uc, "POLICY_DOC_PATH", self.tmp / "skills" / "research-repo-catalog" / "references" / "catalog-policy.md"),
            mock.patch.object(uc, "README_PATH", self.tmp / "README.md"),
            mock.patch.object(uc, "README_ZH_PATH", self.tmp / "README-zh.md"),
            mock.patch.object(uc, "CATALOG_PATH", self.tmp / "catalog.md"),
            mock.patch.object(uc, "JSON_PATH", self.tmp / "catalog.json"),
            mock.patch.object(uc, "CHANGELOG_PATH", self.tmp / "CHANGELOG.md"),
        ]
        for patch in self.patches:
            patch.start()

    def tearDown(self):
        for patch in self.patches:
            patch.stop()
        shutil.rmtree(self.tmp)

    def run_main(self, *argv) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = uc.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_from_curated_then_check_passes_and_is_idempotent(self):
        code, out, err = self.run_main("--from-curated")
        self.assertEqual(code, 0, err)
        before = {p.name: p.read_text(encoding="utf-8") for p in (self.tmp / "README.md", self.tmp / "catalog.json", self.tmp / "CHANGELOG.md")}
        code, _, err = self.run_main("--from-curated")
        self.assertEqual(code, 0, err)
        after = {p.name: p.read_text(encoding="utf-8") for p in (self.tmp / "README.md", self.tmp / "catalog.json", self.tmp / "CHANGELOG.md")}
        self.assertEqual(before, after)
        code, out, _ = self.run_main("--check")
        self.assertEqual(code, 0)
        self.assertIn("ok:", out)
        payload = json.loads((self.tmp / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], 2)
        self.assertTrue(payload["repos"])

    def test_stale_output_fails_check(self):
        self.run_main("--from-curated")
        seed_path = self.tmp / "data" / "repos.seed.tsv"
        text = seed_path.read_text(encoding="utf-8").replace("\tyes\n", "\tyes\n", 1)
        lines = text.splitlines()
        cols = lines[1].split("\t")
        cols[8] = cols[8] + " (edited)"
        lines[1] = "\t".join(cols)
        seed_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        code, _, err = self.run_main("--check")
        self.assertEqual(code, 1)
        self.assertIn("differs from seed", err)

    def test_unknown_type_fails_check(self):
        self.run_main("--from-curated")
        seed_path = self.tmp / "data" / "repos.seed.tsv"
        lines = seed_path.read_text(encoding="utf-8").splitlines()
        cols = lines[1].split("\t")
        cols[2] = "Skill suite"
        lines[1] = "\t".join(cols)
        seed_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        code, _, err = self.run_main("--check")
        self.assertEqual(code, 1)
        self.assertIn("unknown type", err)

    def test_new_seed_row_is_pending_and_strict_fails(self):
        seed_path = self.tmp / "data" / "repos.seed.tsv"
        with seed_path.open("a", encoding="utf-8") as fh:
            fh.write("new/repo\tLiterature Search / Scholarly Search MCP\tmcp-server\t\tmcp\t\tresearch\t\tNew note\t新的备注\tyes\n")
        code, _, err = self.run_main("--from-curated")
        self.assertEqual(code, 0, err)
        self.assertIn("pending", err)
        self.assertIn("| [new/repo](https://github.com/new/repo) | mcp-server | pending |", (self.tmp / "README.md").read_text(encoding="utf-8"))
        code, _, err = self.run_main("--check", "--strict")
        self.assertEqual(code, 1)
        self.assertIn("pending its first GitHub refresh", err)

    def test_pinned_repo_missing_fails_check(self):
        seed_path = self.tmp / "data" / "repos.seed.tsv"
        lines = [line for line in seed_path.read_text(encoding="utf-8").splitlines() if not line.startswith("WUBING2023/PaperSpine\t")]
        seed_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        code, _, err = self.run_main("--from-curated")
        self.assertEqual(code, 1)
        self.assertIn("pinned repo missing from seed: WUBING2023/PaperSpine", err)


class SummaryTests(unittest.TestCase):
    def test_summary_line(self):
        info = {"date": "2026-10-12", "repos": 134, "added": 1, "removed": 0, "renamed": 2, "archived": 0, "missing": 1, "cached": 3}
        self.assertEqual(
            uc.summary_line(info),
            "Weekly refresh 2026-10-12: 134 repos (+1/-0), 2 renamed, 0 archived, 1 missing, 3 cached",
        )


if __name__ == "__main__":
    unittest.main()
