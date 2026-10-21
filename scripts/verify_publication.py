#!/usr/bin/env python3
"""Check the fixed publication allowlist, sensitive-data patterns and file hashes."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "publication-manifest.json"
PUBLIC_FILES = frozenset({
    ".gitignore", ".github/workflows/validate.yml", "LICENSE", "README.md", "README.en.md",
    "SKILL.md", "SOURCE_NOTICE.md", "PUBLICATION_SECURITY.md", MANIFEST,
    "agents/openai.yaml", "examples/domestic.md", "examples/market-entry.md",
    "examples/understand-china.md", "references/china-context.md", "references/corrections.md",
    "references/coverage.md", "references/cross-plan-comparison.md", "references/decision-method.md",
    "references/industry-entry-map.md", "references/official-corpus.json",
    "references/policy-cards.json", "references/research-synthesis.md",
    "references/source-catalogue.json", "scripts/search_evidence.py", "scripts/verify_bundle.py",
    "scripts/verify_publication.py", "tests/behavioral-cases.md", "tests/test_evidence.py",
    "tests/test_publication_security.py",
    "references/decision-note.md", "examples/first-session.md",
    "site/first-session.html", "tests/test_onboarding.py", "tests/v0.3-validation.md",
    "launch/v0.3-launch.md",
    '.github/ISSUE_TEMPLATE/guide-feedback.yml',
    '.github/workflows/pages.yml',
    'guide/README.md',
    'guide/CONTRIBUTING.md',
    'guide/cards.json',
    'launch/launch-kit.md',
    'launch/question-backlog.md',
    'launch/reader-test-template.csv',
    'scripts/build_reader.py',
    'scripts/build_pdf.py',
    'scripts/verify_guide.py',
    'tests/test_reader_citations.py',
    'site/index.html',
    'site/style.css',
    'site/app.js',
    'site/.nojekyll',
    'site/sitemap.xml',
    'site/googlee7f968b7a3579e7a.html',
    'scripts/build_qr.py',
    'site/cards/qr-01.svg',
    'site/cards/qr-02.svg',
    'site/cards/qr-03.svg',
    'site/cards/qr-04.svg',
    'site/cards/qr-05.svg',
    'guide/card-01.md',
    'guide/card-02.md',
    'guide/card-03.md',
    'guide/card-04.md',
    'guide/card-05.md',
    'site/cards/manufacturing-ai.html',
    'site/cards/robotics-services.html',
    'site/cards/eldercare-payer.html',
    'site/cards/policy-to-order.html',
    'site/cards/skills-transfer.html',
    'site/cards/share-01.html',
    'site/cards/share-02.html',
    'site/cards/share-03.html',
    'site/cards/share-04.html',
    'site/cards/share-05.html',
})
PATTERNS = {
    "email_address": re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"),
    "phone_number": re.compile(r"(?<!\d)(?:\+?86[ -]?)?1[3-9]\d{9}(?!\d)|(?<!\d)0\d{2,3}[-－ ]?\d{7,8}(?!\d)"),
    "identity_number": re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"),
    "machine_path": re.compile(r"/(?:Users|home|private)/|[A-Za-z]:\\(?:Users|Documents)\\|file:/{3}"),
    "access_token": re.compile(r"(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}|\bAKIA[A-Z0-9]{16}\b|\bsk-[A-Za-z0-9_-]{24,}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def text_issues(text, private_markers=()):
    categories = [name for name, pattern in PATTERNS.items() if pattern.search(text)]
    if any(marker.casefold() in text.casefold() for marker in private_markers):
        categories.append("private_marker")
    return categories


def json_issues(value, private_markers=(), path="$"):
    findings = []
    if isinstance(value, dict):
        for key, child in value.items():
            # A validated whole-field content fingerprint is not a phone number.
            if key == "sha256" and isinstance(child, str) and re.fullmatch(r"[a-fA-F0-9]{64}", child):
                continue
            if key in {"relative_source_file", "absolute_path", "local_path"}:
                findings.append((path, "local_source_location"))
            findings.extend(json_issues(child, private_markers, path + "." + key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(json_issues(child, private_markers, path + f"[{index}]"))
    elif isinstance(value, str):
        findings.extend((path, category) for category in text_issues(value, private_markers))
    return findings


def file_manifest(root):
    entries = []
    for name in sorted(PUBLIC_FILES - {MANIFEST}):
        data = (root / name).read_bytes()
        entries.append({"path": name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    return {"version": "0.3.0", "files": entries}


def audit(root=ROOT, private_markers=(), write_manifest=False):
    root = Path(root)
    issues, found = [], set()
    for file in root.rglob("*"):
        relative = file.relative_to(root)
        if any(p in {".git", "__pycache__"} for p in relative.parts):
            continue
        name = relative.as_posix()
        if file.is_symlink():
            issues.append({"file": name, "category": "symbolic_link"})
            continue
        if not file.is_file():
            continue
        found.add(name)
        if name not in PUBLIC_FILES:
            issues.append({"file": name, "category": "not_allowlisted"})
            continue
        try:
            text = file.read_text(encoding="utf-8")
            findings = json_issues(json.loads(text), private_markers) if file.suffix == ".json" else [
                ("text", category) for category in text_issues(text, private_markers)]
            issues.extend({"file": name, "category": category, "location": location} for location, category in findings)
        except (UnicodeError, json.JSONDecodeError):
            issues.append({"file": name, "category": "not_valid_text_or_json"})
    required = PUBLIC_FILES - ({MANIFEST} if write_manifest else set())
    for name in sorted(required - found):
        issues.append({"file": name, "category": "missing_public_file"})
    if not issues:
        expected = file_manifest(root)
        if write_manifest:
            (root / MANIFEST).write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
        elif json.loads((root / MANIFEST).read_text(encoding="utf-8")) != expected:
            issues.append({"file": MANIFEST, "category": "content_hash_mismatch"})
    return {"ok": not issues, "allowlisted_files": len(PUBLIC_FILES), "issues": issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--private-denylist", type=Path,
                        help="Optional local-only markers; their values are never printed")
    args = parser.parse_args()
    markers = ()
    if args.private_denylist:
        markers = tuple(line.strip() for line in args.private_denylist.read_text(encoding="utf-8").splitlines() if line.strip())
        if any(len(marker) < 2 for marker in markers):
            parser.error("private markers must contain at least two characters")
    result = audit(private_markers=markers, write_manifest=args.write_manifest)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(not result["ok"])


if __name__ == "__main__":
    main()
