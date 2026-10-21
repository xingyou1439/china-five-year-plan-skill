"""Regression checks for language, SEO, source reuse and published navigation."""
from html.parser import HTMLParser
from pathlib import Path
import importlib.util
import unittest
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reader', ROOT/'scripts/build_reader.py')
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if 'id' in attrs:
            self.ids.add(attrs['id'])


class EnglishReaderTests(unittest.TestCase):
    def test_reciprocal_homepage_alternates(self):
        for filename, language, canonical in [('index.html', 'zh-CN', reader.BASE),
                                             ('en/index.html', 'en', reader.BASE+'en/')]:
            page = Page((ROOT/'site'/filename).read_text())
            self.assertIn(('html', {'lang': language}), page.tags)
            links = [a for t, a in page.tags if t == 'link']
            self.assertEqual([a['href'] for a in links if a.get('rel') == 'canonical'], [canonical])
            self.assertEqual({a['hreflang']: a['href'] for a in links if a.get('rel') == 'alternate'},
                             {'en': reader.BASE+'en/', 'zh-CN': reader.BASE, 'x-default': reader.BASE+'en/'})
            self.assertTrue(any(t == 'meta' and a.get('name') == 'description' and a.get('content') for t,a in page.tags))

    def test_english_content_and_anchors(self):
        text = reader.english()
        page = Page(text)
        for value in ['WorkBuddy', 'Codex', 'Claude Code', 'Who it serves', 'Provenance and limitations',
                      'not official translations', 'Chinese only', reader.DATA['source_url']]:
            self.assertIn(value, text)
        for tag, attrs in page.tags:
            href = attrs.get('href', '')
            if href.startswith('#'):
                self.assertIn(href[1:], page.ids)
        self.assertNotIn('<script', text)
        self.assertEqual(text.count('— Chinese only</a>'), 5)

    def test_only_real_translation_pairs_and_sitemap(self):
        doc = ET.fromstring(reader.sitemap())
        urls = [n.text for n in doc.findall('{*}url/{*}loc')]
        self.assertEqual(len(urls), 7)
        self.assertEqual(len(set(urls)), 7)
        self.assertIn(reader.BASE+'en/', urls)
        for card in reader.DATA['cards']:
            self.assertNotIn('hreflang=', reader.shell('Card', 'Description', 'Content', canonical=reader.BASE+'cards/'+card['slug']+'.html'))

    def test_markdown_is_escaped_and_relative_links_resolve(self):
        rendered = reader.english_markdown('<script>alert(1)</script>\n\n[Sources](SOURCE_NOTICE.md)')
        self.assertNotIn('<script>', rendered)
        self.assertIn(reader.REPO+'/blob/codex/initial-release/SOURCE_NOTICE.md', rendered)


if __name__ == '__main__':
    unittest.main()
