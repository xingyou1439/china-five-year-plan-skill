#!/usr/bin/env python3
"""Search bundled official passages. Ranking is lexical relevance, not confidence."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def normalize(value):
    return re.sub(r"\s+", "", value).casefold()


def load_data():
    corpus = json.loads((ROOT / "references/official-corpus.json").read_text(encoding="utf-8"))
    cards = json.loads((ROOT / "references/policy-cards.json").read_text(encoding="utf-8"))["cards"]
    return corpus, cards


def search(query, plan=None, limit=5, as_of=None):
    if not query.strip():
        raise ValueError("query must contain non-whitespace text")
    if not 1 <= limit <= 20:
        raise ValueError("limit must be between 1 and 20")
    if plan not in (None, 13, 14, 15):
        raise ValueError("plan must be 13, 14 or 15")
    cutoff = dt.date.fromisoformat(as_of) if as_of else None
    corpus, cards = load_data()
    query_norm = normalize(query)
    terms = {normalize(t) for t in re.findall(r"[a-zA-Z0-9]+|[\u4e00-\u9fff]{2,}", query)}
    # Phrase aliases support Chinese/English discovery. They do not prove entailment.
    matched_cards = []
    for card in cards:
        aliases = [normalize(k) for k in card["keywords"]]
        if any((re.search(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])", query.casefold())
                if k.isascii() else k in query_norm) for k in aliases):
            matched_cards.append(card)
    ref_hits = {}
    for card in matched_cards:
        terms.add(normalize(card["title_zh"]))
        terms.update(normalize(k) for k in card["keywords"] if not k.isascii())
        for ref in card["source_refs"]:
            ref_hits.setdefault((ref["source_id"], ref["pdf_page"]), []).append(card["id"])
    hits, excluded = [], []
    for source in corpus["sources"]:
        if plan and source["plan"] != plan:
            continue
        published = source.get("publication_date")
        if cutoff and (not published or dt.date.fromisoformat(published) > cutoff):
            excluded.append({"source_id": source["source_id"], "reason": "publication date unknown" if not published else "published after cutoff"})
            continue
        for page in source["pages"]:
            text = page["text"]
            ocr_text = page.get("ocr_text_unverified", "")
            if ocr_text:
                text += "\n[Unverified OCR; visually check numerical and tabular claims]\n" + ocr_text
            norm = normalize(text)
            matches = [t for t in terms if t and t in norm]
            ids = ref_hits.get((source["source_id"], page["page"]), [])
            if not matches and not ids:
                continue
            score = len(matches) + 6 * len(ids)
            # Return a window around a match rather than an unrelated page beginning.
            clean = re.sub(r"\s+", "", text)
            starts = [clean.casefold().find(t) for t in matches if clean.casefold().find(t) >= 0]
            pos = min(starts) if starts else 0
            snippet = clean[max(0, pos - 160):pos + 1350]
            hits.append({"source_id": source["source_id"], "source_kind": "official_outline", "plan": source["plan"],
                         "source_title": source["title"], "publication_date": published,
                         "pdf_page": page["page"], "page_numbering": source["page_numbering"],
                         "official_url": source.get("official_url"), "matched_cards": ids,
                         "extraction_method": "pdf_text_layer_plus_unverified_ocr" if ocr_text else "pdf_text_layer",
                         "excerpt_zh": snippet, "lexical_rank_score": score})
    hits.sort(key=lambda h: (-h["lexical_rank_score"], -h["plan"], h["pdf_page"]))
    return {"snapshot_date": corpus["snapshot_date"], "query": query, "as_of": as_of,
            "warning": "Lexical retrieval only. Read context; ranking is not confidence. OCR numbers need visual verification. No result does not prove absence from all policies.",
            "excluded_sources": excluded, "results": hits[:limit]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--plan", type=int, choices=(13, 14, 15))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--as-of", help="ISO date; sources with unknown or later publication dates are excluded")
    args = parser.parse_args()
    try:
        result = search(args.query, args.plan, args.limit, args.as_of)
    except ValueError as error:
        parser.error(str(error))
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
