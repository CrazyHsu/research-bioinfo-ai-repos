from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from _load import load_script

dc = load_script("discover_candidates")


def item(full_name: str, stars: int = 10, **extra) -> dict:
    base = {
        "full_name": full_name, "html_url": f"https://github.com/{full_name}", "stargazers_count": stars,
        "pushed_at": "2026-10-01T00:00:00Z", "language": "Python", "description": "PubMed MCP server for agents",
        "archived": False, "disabled": False, "fork": False,
    }
    base.update(extra)
    return base


class ExtractTests(unittest.TestCase):
    def test_extracts_and_normalizes_links(self):
        text = (
            "see https://github.com/scmcphub/scmcp.git and (github.com/vrtejus/pymol-mcp) plus "
            "https://github.com/features/copilot and https://github.com/topics/mcp and github.com/a/b/blob/main/x"
        )
        self.assertEqual(dc.extract_github_repos(text), {"scmcphub/scmcp", "vrtejus/pymol-mcp", "a/b"})


class RelevanceTests(unittest.TestCase):
    def test_relevance_filter(self):
        self.assertTrue(dc.is_relevant_candidate("x/arxiv-mcp", ""))
        self.assertTrue(dc.is_relevant_candidate("x/tool", "Zotero plugin with LLM chat"))
        self.assertTrue(dc.is_relevant_candidate("x/awesome-bio-skills", ""))
        self.assertFalse(dc.is_relevant_candidate("x/todo-app", "simple todo list"))
        self.assertFalse(dc.is_relevant_candidate("x/genome-browser", "a genome browser"))

    def test_suggestions(self):
        self.assertEqual(dc.suggest_category("x/zotero-mcp", ""), "Zotero / CNKI / Google Scholar / Reference Management")
        self.assertEqual(dc.suggest_category("x/scanpy-mcp", "single-cell"), "Bioinformatics / Omics / Single-Cell Skills")
        self.assertEqual(dc.suggest_type("x/awesome-y", ""), "directory")
        self.assertEqual(dc.suggest_type("x/pubmed-mcp", ""), "mcp-server")
        self.assertEqual(dc.suggest_type("x/paper-skills", ""), "skill-suite")


class SearchTests(unittest.TestCase):
    def test_filters_and_dedupes(self):
        queries = [
            {"query": "pubmed mcp", "target_category": "Literature Search / Scholarly Search MCP", "sort": "stars"},
            {"query": "pubmed mcp", "target_category": "Literature Search / Scholarly Search MCP", "sort": "updated"},
        ]
        results = {
            ("pubmed mcp", "stars"): [item("a/pubmed-mcp"), item("b/fork", fork=True), item("c/archived", archived=True),
                                      item("d/lowstar", stars=0), item("e/todo", description="todo list app")],
            ("pubmed mcp", "updated"): [item("a/pubmed-mcp", stars=11)],
        }

        def searcher(query, limit, sort, token):
            return results[(query, sort)]

        found, warnings, hits = dc.run_searches(queries, 30, 1, False, False, 0.0, None, searcher=searcher)
        self.assertEqual(warnings, [])
        self.assertEqual(set(found), {"a/pubmed-mcp"})
        self.assertEqual(found["a/pubmed-mcp"]["sources"], ["search:pubmed mcp"])
        self.assertEqual(found["a/pubmed-mcp"]["suggested_category"], "Literature Search / Scholarly Search MCP")
        self.assertEqual(hits, 2)

    def test_search_error_is_a_warning(self):
        from urllib.error import URLError

        def searcher(query, limit, sort, token):
            raise URLError("down")

        found, warnings, _ = dc.run_searches([{"query": "x", "target_category": "", "sort": "stars"}], 30, 1, False, False, 0.0, None, searcher=searcher)
        self.assertEqual(found, {})
        self.assertEqual(len(warnings), 1)


class AwesomeTests(unittest.TestCase):
    def test_crossref_collects_lists_per_reference(self):
        seed_rows = [
            {"repo": "L1/list", "type": "directory", "include": "yes"},
            {"repo": "L2/list", "type": "registry", "include": "yes"},
            {"repo": "x/skill", "type": "skill", "include": "yes"},
        ]
        readmes = {
            "L1/list": "https://github.com/x/skill https://github.com/fresh/pubmed-mcp https://github.com/other/random-thing",
            "L2/list": "github.com/fresh/pubmed-mcp github.com/other/random-thing https://github.com/L2/list",
        }
        refs, warnings = dc.run_awesome_crossref(seed_rows, None, 0.0, reader=lambda repo, token: readmes[repo])
        self.assertEqual(warnings, [])
        self.assertEqual(refs["x/skill"], {"L1/list"})
        self.assertEqual(refs["fresh/pubmed-mcp"], {"L1/list", "L2/list"})
        self.assertNotIn("l2/list", refs)

    def test_enrichment_uses_descriptions_cache_and_budget(self):
        refs = {
            "fresh/pubmed-mcp": {"L1/list", "L2/list"},
            "other/random-thing": {"L1/list"},
            "scmcphub/scmcp": {"L1/list"},
            "x/skill": {"L1/list"},
            "gone/repo": {"L1/list"},
        }
        metas = {
            "fresh/pubmed-mcp": {"full_name": "fresh/pubmed-mcp", "stargazers_count": 12, "description": "PubMed MCP", "pushed_at": "2026-10-01T00:00:00Z", "language": "Python"},
            "other/random-thing": {"full_name": "other/random-thing", "stargazers_count": 3, "description": "a todo list"},
            "scmcphub/scmcp": {"full_name": "scmcphub/scmcp", "stargazers_count": 16, "description": "MCP server for scRNA-seq analysis"},
        }
        calls = []

        def fetcher(repo, token):
            calls.append(repo)
            if repo == "gone/repo":
                import io as _io
                from email.message import Message
                from urllib.error import HTTPError
                raise HTTPError("u", 404, "gone", Message(), _io.BytesIO(b""))
            return metas[repo]

        cache: dict = {}
        found = dc.enrich_awesome_refs(refs, {"x/skill"}, cache, "2026-10-13", None, fetch_limit=10, fetcher=fetcher)
        self.assertNotIn("x/skill", calls)
        self.assertIn("fresh/pubmed-mcp", found)
        self.assertEqual(found["fresh/pubmed-mcp"]["stars"], "12")
        self.assertIn("scmcphub/scmcp", found)  # neutral name, relevant description
        self.assertNotIn("other/random-thing", found)  # single list, irrelevant description
        self.assertNotIn("gone/repo", found)
        self.assertEqual(cache["gone/repo"]["relevant"], "no")
        self.assertEqual(cache["scmcphub/scmcp"]["relevant"], "yes")
        # second run within the cache window makes no network calls
        calls.clear()
        found2 = dc.enrich_awesome_refs(refs, {"x/skill"}, cache, "2026-10-20", None, fetch_limit=10, fetcher=fetcher)
        self.assertEqual(calls, [])
        self.assertEqual(set(found2), {"fresh/pubmed-mcp", "scmcphub/scmcp"})
        # with no budget and no cache, only multi-listed or name-relevant references survive
        found3 = dc.enrich_awesome_refs({"a/b": {"L1/list", "L2/list"}, "c/zotero-mcp": {"L1/list"}, "d/e": {"L1/list"}}, set(), {}, "2026-10-13", None, fetch_limit=0, fetcher=fetcher)
        self.assertEqual(set(found3), {"a/b", "c/zotero-mcp"})
        self.assertEqual(found3["a/b"]["stars"], "")

    def test_redirected_references_are_keyed_by_resolved_name(self):
        refs = {"old-org/skills": {"L1/list"}, "a/old-name": {"L1/list"}, "a/new-name": {"L2/list"}}
        metas = {
            "old-org/skills": {"full_name": "K-Dense-AI/scientific-agent-skills", "stargazers_count": 1, "description": "agent skills for science"},
            "a/old-name": {"full_name": "a/new-name", "stargazers_count": 7, "description": "arxiv mcp server"},
            "a/new-name": {"full_name": "a/new-name", "stargazers_count": 7, "description": "arxiv mcp server"},
        }
        found = dc.enrich_awesome_refs(refs, {"k-dense-ai/scientific-agent-skills"}, {}, "2026-10-13", None, fetch_limit=10, fetcher=lambda repo, token: metas[repo])
        self.assertEqual(set(found), {"a/new-name"})
        self.assertEqual(found["a/new-name"]["sources"], ["awesome:L1/list", "awesome:L2/list"])
        seen: dict = {}
        dc.update_seen(seen, {"weird-key": {"repo": "A/New-Name", "url": "u", "stars": 1, "sources": ["search:q"]}}, "2026-10-13")
        self.assertEqual(list(seen), ["a/new-name"])

    def test_merge_candidates_combines_sources(self):
        found = {"a/b": {"repo": "a/b", "stars": 5, "sources": ["search:q"], "description": "d"}}
        dc.merge_candidates(found, {"a/b": {"repo": "a/b", "stars": "", "sources": ["awesome:L"], "description": ""}, "c/d": {"repo": "c/d", "sources": ["awesome:L"]}})
        self.assertEqual(found["a/b"]["sources"], ["search:q", "awesome:L"])
        self.assertEqual(found["a/b"]["stars"], 5)
        self.assertIn("c/d", found)


class SeenTests(unittest.TestCase):
    def test_times_seen_grows_once_per_run_date(self):
        seen: dict = {}
        found = {"a/b": {"repo": "a/b", "url": "https://github.com/a/b", "stars": 5, "pushed_at": "2026-10-01", "language": "Python",
                         "suggested_category": "C", "suggested_type": "mcp-server", "sources": ["search:q1"], "description": "d"}}
        dc.update_seen(seen, found, "2026-10-13")
        self.assertEqual(seen["a/b"]["first_seen"], "2026-10-13")
        self.assertEqual(seen["a/b"]["times_seen"], "1")
        found["a/b"]["stars"] = 9
        found["a/b"]["sources"] = ["search:q2"]
        dc.update_seen(seen, found, "2026-10-13")
        self.assertEqual(seen["a/b"]["times_seen"], "1")
        dc.update_seen(seen, found, "2026-10-20")
        self.assertEqual(seen["a/b"]["times_seen"], "2")
        self.assertEqual(seen["a/b"]["last_seen"], "2026-10-20")
        self.assertEqual(seen["a/b"]["max_stars"], "9")
        self.assertEqual(seen["a/b"]["sources"], "search:q1; search:q2")


class RenderAndCheckTests(unittest.TestCase):
    def test_render_respects_triage_and_check_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "candidates.md"
            seen = {
                "new/one": {"repo": "new/one", "url": "https://github.com/new/one", "first_seen": "2026-10-13", "last_seen": "2026-10-13", "times_seen": "1", "last_stars": "3", "sources": "search:q", "suggested_category": "C", "suggested_type": "skill", "description": "x"},
                "old/two": {"repo": "old/two", "url": "https://github.com/old/two", "first_seen": "2026-07-13", "last_seen": "2026-10-13", "times_seen": "14", "last_stars": "30", "sources": "search:q", "suggested_category": "C", "suggested_type": "skill", "description": "y"},
                "bad/three": {"repo": "bad/three", "url": "https://github.com/bad/three", "first_seen": "2026-07-13", "last_seen": "2026-10-13", "times_seen": "14", "last_stars": "1", "sources": "search:q", "suggested_category": "C", "suggested_type": "skill", "description": "z"},
                "later/four": {"repo": "later/four", "url": "https://github.com/later/four", "first_seen": "2026-08-01", "last_seen": "2026-10-13", "times_seen": "5", "last_stars": "7", "sources": "search:q", "suggested_category": "C", "suggested_type": "skill", "description": "w"},
                "mirror/five": {"repo": "mirror/five", "url": "https://github.com/mirror/five", "first_seen": "2026-10-13", "last_seen": "2026-10-13", "times_seen": "1", "last_stars": "2", "sources": "search:q", "suggested_category": "C", "suggested_type": "skill", "description": "[x/skill](https://github.com/x/skill) mirror of [mirror/five](https://github.com/mirror/five)"},
            }
            triage = {
                "bad/three": {"repo": "bad/three", "decision": "reject", "reason": "paper list", "date": "2026-10-13"},
                "later/four": {"repo": "later/four", "decision": "defer", "reason": "no README", "date": "2026-10-13"},
            }
            queries = [{"query": "q", "target_category": "C", "sort": "stars"}]
            dc.render_candidates(seen, triage, set(), queries, ["q: boom"], "2026-10-13", {"queries": 1, "hits": 2}, output)
            text = output.read_text(encoding="utf-8")
            self.assertIn("## New this run (2)", text)
            self.assertIn("## Seen before, not yet triaged (1)", text)
            self.assertIn("## Deferred (1)", text)
            self.assertNotIn("bad/three", text)
            self.assertIn("[later/four]", text)
            self.assertIn("## Search Warnings", text)
            self.assertIn("x/skill (https://github.com/x/skill) mirror of mirror/five (https://github.com/mirror/five)", text)
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = dc.check_candidates(output, [{"repo": "x/skill"}], triage)
            self.assertEqual(code, 0, err.getvalue())
            bad_triage = dict(triage)
            bad_triage["new/one"] = {"repo": "new/one", "decision": "accept", "reason": "good", "date": "2026-10-13"}
            with redirect_stdout(out), redirect_stderr(err):
                code = dc.check_candidates(output, [{"repo": "x/skill"}], bad_triage)
            self.assertEqual(code, 1)
            self.assertIn("accepted but not in the seed", err.getvalue())


if __name__ == "__main__":
    unittest.main()
