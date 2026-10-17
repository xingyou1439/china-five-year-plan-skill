#!/usr/bin/env python3
"""Validate bundled citations and portable file references; no network required."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    corpus = json.loads((root / "references/official-corpus.json").read_text(encoding="utf-8"))
    cards = json.loads((root / "references/policy-cards.json").read_text(encoding="utf-8"))["cards"]
    catalogue = json.loads((root / "references/source-catalogue.json").read_text(encoding="utf-8"))
    sources = {s["source_id"]: s for s in corpus["sources"]}
    known_ids = {s["source_id"] for s in catalogue["unique_sources"]}
    normalize = lambda s: re.sub(r"\s+", "", s)
    if len({c["id"] for c in cards}) != len(cards):
        errors.append("duplicate card IDs")
    count = 0
    for card in cards:
        for ref in card["source_refs"]:
            source = sources.get(ref["source_id"])
            if source is None:
                errors.append(f"{card['id']}: missing source")
                continue
            page = next((p for p in source["pages"] if p["page"] == ref["pdf_page"]), None)
            if page is None or normalize(ref["quote_zh"]) not in normalize(page["text"]):
                errors.append(f"{card['id']}: quote not present at specified page")
            count += 1
    for file in root.rglob("*.md"):
        text = file.read_text(encoding="utf-8")
        for dest in re.findall(r"\]\(([^\s)]+)\)", text):
            if "://" in dest or dest.startswith("#"):
                continue
            path = (file.parent / dest.split("#")[0]).resolve()
            if not path.is_relative_to(root.resolve()):
                errors.append(f"{file.name}: nonportable link {dest}")
            elif not path.exists():
                errors.append(f"{file.name}: broken link {dest}")
        for sid in re.findall(r"SRC-[A-F0-9]{10}", text):
            if sid not in known_ids:
                errors.append(f"{file.name}: unknown source {sid}")
    return errors, {"cards": len(cards), "verified_quote_locations": count, "catalogue_sources": len(known_ids)}


if __name__ == "__main__":
    errors, stats = validate()
    print(json.dumps({"ok": not errors, **stats, "errors": errors}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))
