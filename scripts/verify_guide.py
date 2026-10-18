#!/usr/bin/env python3
"""Check public guide provenance, generated content and local navigation."""
import importlib.util
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {'href', 'src'} and value:
                self.links.append(value)


def validate():
    errors = []
    d = json.loads((ROOT / 'guide/cards.json').read_text(encoding='utf-8'))
    policy = {c['id']: c for c in json.loads((ROOT / 'references/policy-cards.json').read_text(encoding='utf-8'))['cards']}
    updates = {s['id']: s for s in d['updates']}
    if len(updates) != len(d['updates']): errors.append('duplicate implementation-source ID')
    for s in updates.values():
        for field in ['title', 'issuer', 'document_date', 'retrieved', 'url', 'locator', 'quote', 'summary', 'scope']:
            if not s.get(field): errors.append(f'{s["id"]}: missing {field}')
        if not urlsplit(s['url']).hostname.endswith('.gov.cn'): errors.append(f'{s["id"]}: not a government domain')
        if s['document_date'] > d['reviewed'] or s['retrieved'] > d['reviewed']: errors.append(f'{s["id"]}: future evidence')
    if len({c['id'] for c in d['cards']}) != len(d['cards']): errors.append('duplicate decision-card ID')
    for c in d['cards']:
        for field in ['situation', 'judgment', 'interpretation', 'payer', 'capability', 'gap', 'success', 'stop', 'boundary']:
            if not c.get(field): errors.append(f'{c["id"]}: missing {field}')
        if '假设' not in c['situation']: errors.append(f'{c["id"]}: constructed scenario not labelled')
        if len(c.get('steps', [])) != 3: errors.append(f'{c["id"]}: incomplete experiment')
        for pid in c['policy_ids']:
            if pid not in policy: errors.append(f'{c["id"]}: unknown policy source')
        for uid in c['update_ids']:
            if uid not in updates: errors.append(f'{c["id"]}: unknown implementation source')
    # All local resources must stay inside the published static directory.
    for file in (ROOT / 'site').rglob('*.html'):
        parser = Links(); parser.feed(file.read_text(encoding='utf-8'))
        for value in parser.links:
            dest = urlsplit(value)
            if dest.scheme or dest.netloc or not dest.path: continue
            path = (file.parent / unquote(dest.path)).resolve()
            if not path.is_relative_to((ROOT / 'site').resolve()) or not path.is_file():
                errors.append(f'{file.relative_to(ROOT)}: missing local resource {value}')
    spec = importlib.util.spec_from_file_location('reader', ROOT / 'scripts/build_reader.py')
    builder = importlib.util.module_from_spec(spec); spec.loader.exec_module(builder)
    for c in d['cards']:
        for path, expected in [(ROOT/'site/cards'/f'{c["slug"]}.html', builder.detail(c)),
                               (ROOT/'site/cards'/f'share-{c["id"]}.html', builder.share(c)),
                               (ROOT/'guide'/f'card-{c["id"]}.md', builder.markdown(c))]:
            if path.read_text(encoding='utf-8') != expected: errors.append(f'{path.relative_to(ROOT)}: stale generated content')
    return errors


if __name__ == '__main__':
    errors = validate()
    print(json.dumps({'ok': not errors, 'decision_cards': 5, 'implementation_sources': 4, 'errors': errors}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))
