"""Check the public citation boundary without weakening source traceability."""
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('guide_reader', ROOT/'scripts/build_reader.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class VisiblePage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}:
            self.hidden += 1
        if tag == 'a':
            self.links.extend(v for k,v in attrs if k == 'href')

    def handle_endtag(self, tag):
        if tag in {'script', 'style'}:
            self.hidden -= 1

    def handle_data(self, value):
        if not self.hidden:
            self.parts.append(value)


class PublicCitationTests(unittest.TestCase):
    def check_public_text(self, text):
        # Hidden JSON and original evidence files deliberately retain these fields.
        self.assertNotRegex(text, r'SRC-[A-Z0-9]+|\b(?:P\d{2}|U\d{2})\b')
        self.assertNotRegex(text, r'物理页|物理第|所用\s*PDF|pdf_page|source_id|page_numbering')

    def test_every_public_format_keeps_evidence_without_retrieval_labels(self):
        for card in reader.DATA['cards']:
            with self.subTest(card=card['id']):
                md = reader.markdown(card)
                self.check_public_text(md)
                for render in [reader.detail, reader.share]:
                    page = VisiblePage()
                    page.feed(render(card))
                    visible = ''.join(page.parts)
                    self.check_public_text(visible)
                    self.assertIn(reader.DATA['source_url'], page.links)
                    if render is reader.share:
                        self.assertIn(card['chapter'], visible)
                    for pid in card['policy_ids']:
                        for ref in reader.POLICY[pid]['source_refs']:
                            self.assertIn(ref['quote_zh'], visible)
                            if render is reader.detail:
                                self.assertIn(reader.CHAPTERS[pid], visible)
                            self.assertIn(ref['quote_zh'], md)

    def test_detail_keeps_followup_sources_and_material_conditions(self):
        for card in reader.DATA['cards']:
            page = VisiblePage()
            page.feed(reader.detail(card))
            visible = ''.join(page.parts)
            for uid in card['update_ids']:
                source = reader.UPDATES[uid]
                self.assertIn(source['url'], page.links)
                self.assertIn(source['document_date'], visible)
                self.assertIn(source['scope'], visible)
            self.assertIn(card['boundary'], visible)

    def test_original_evidence_remains_available_for_requested_audits(self):
        for policy in reader.POLICY.values():
            for ref in policy['source_refs']:
                self.assertTrue(ref['source_id'])
                self.assertGreater(ref['pdf_page'], 0)


if __name__ == '__main__':
    unittest.main()
