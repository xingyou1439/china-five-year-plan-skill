# coding: utf-8
"""Protect entry links and the evidence boundary of the worked walkthrough."""
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('onboarding_reader', ROOT/'scripts/build_reader.py')
reader = importlib.util.module_from_spec(spec); spec.loader.exec_module(reader)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.links=[]
    def handle_starttag(self, tag, attrs):
        self.ids.update(v for k,v in attrs if k == 'id')
        self.links.extend(v for k,v in attrs if tag == 'a' and k == 'href')

class OnboardingTests(unittest.TestCase):
    def test_walkthrough_is_regenerated_from_the_reviewed_example(self):
        self.assertEqual((ROOT/'site/first-session.html').read_text(), reader.walkthrough())
        page=Page();page.feed(reader.walkthrough())
        self.assertTrue({'step-1','step-2','step-3','step-4','step-5','step-6','step-7','step-8'} <= page.ids)
        self.assertIn(reader.DATA['source_url'], page.links)
        self.assertIn(reader.REPO+'/blob/codex/initial-release/references/decision-note.md',page.links)
        self.assertNotIn('../references/decision-note.md',page.links)

    def test_walkthrough_keeps_demo_and_freshness_limitations(self):
        text=reader.walkthrough()
        for phrase in ['构造的编辑示范','没有进行客户访谈','不能据此断言10月当地实施情况','还没有预算承诺','本段仍是构造示范']:
            self.assertIn(phrase,text)
        self.assertNotIn('source_id',text.split('<script')[0])

    def test_new_page_is_discoverable_and_google_verification_is_preserved(self):
        tree=ET.fromstring(reader.sitemap())
        locations=[node.text for node in tree.iter() if node.tag.endswith('}loc')]
        self.assertEqual(len(locations),7)
        self.assertIn(reader.BASE+'first-session.html',locations)
        self.assertEqual((ROOT/'site/googlee7f968b7a3579e7a.html').read_text().strip(),
                         'google-site-verification: googlee7f968b7a3579e7a.html')
        index=(ROOT/'site/index.html').read_text()
        self.assertIn('href="first-session.html"',index)
        self.assertIn('href="first-session.html#step-3"',index)

if __name__ == '__main__':unittest.main()
