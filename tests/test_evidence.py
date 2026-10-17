import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


searcher = module("search_evidence")
verifier = module("verify_bundle")


class EvidenceTests(unittest.TestCase):
    def test_english_ai_query_retrieves_actual_chinese_passage(self):
        result = searcher.search("AI services for Chinese SMEs", plan=15)
        self.assertTrue(any(r["pdf_page"] == 26 and "中小企业" in r["excerpt_zh"] for r in result["results"]))

    def test_inbound_query_retrieves_pilot_conditions(self):
        result = searcher.search("market entry hospital", plan=15)
        self.assertTrue(any("试点" in r["excerpt_zh"] for r in result["results"]))

    def test_historical_cutoff_excludes_future_outline(self):
        result = searcher.search("AI", as_of="2024-12-31", limit=20)
        self.assertTrue(result["results"])
        self.assertTrue(all(r["plan"] == 14 for r in result["results"]))
        self.assertTrue(any(e["reason"] == "published after cutoff" for e in result["excluded_sources"]))

    def test_unknown_publication_date_is_not_silently_assumed(self):
        result = searcher.search("改革", plan=13, as_of="2024-12-31")
        self.assertEqual(result["results"], [])
        self.assertEqual(result["excluded_sources"][0]["reason"], "publication date unknown")

    def test_no_hit_does_not_invent_evidence(self):
        self.assertEqual(searcher.search("zzq_nonexistent_xyz_987")['results'], [])

    def test_alias_does_not_match_ai_inside_unrelated_word(self):
        self.assertEqual(searcher.search("Thailand")['results'], [])

    def test_specific_plan_filter(self):
        result = searcher.search("改革", plan=14)
        self.assertTrue(result['results'])
        self.assertTrue(all(r['plan'] == 14 for r in result['results']))

    def test_invalid_input(self):
        for kwargs in ({"query": " "}, {"query": "AI", "limit": 0}, {"query": "AI", "limit": 21},
                       {"query": "AI", "plan": 12}, {"query": "AI", "as_of": "yesterday"}):
            with self.assertRaises(ValueError):
                searcher.search(**kwargs)

    def test_all_quotes_resolve(self):
        errors, stats = verifier.validate()
        self.assertEqual(errors, [])
        self.assertEqual(stats['verified_quote_locations'], stats['cards'])

    def test_corrupted_quote_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(ROOT / 'references', root / 'references')
            cards_file = root / 'references/policy-cards.json'
            data = json.loads(cards_file.read_text())
            data['cards'][0]['source_refs'][0]['quote_zh'] = '此处不存在的预算承诺'
            cards_file.write_text(json.dumps(data, ensure_ascii=False))
            errors, _ = verifier.validate(root)
            self.assertTrue(any('quote not present' in error for error in errors))

    def test_wrong_page_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(ROOT / 'references', root / 'references')
            cards_file = root / 'references/policy-cards.json'
            data = json.loads(cards_file.read_text())
            data['cards'][0]['source_refs'][0]['pdf_page'] = 999
            cards_file.write_text(json.dumps(data, ensure_ascii=False))
            self.assertTrue(verifier.validate(root)[0])


if __name__ == '__main__':
    unittest.main()
