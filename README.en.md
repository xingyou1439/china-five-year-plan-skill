# China Five-Year Plan Decision Reference Skill

[中文](README.md)

An open-source, bilingual AI skill for understanding China and making informed decisions about careers, ventures, projects and China market entry. It connects China's 13th, 14th and 15th Five-Year Plans (2026–2030) with traceable policy evidence, cross-plan comparisons and practical validation steps.

Its workflow follows policy direction → implementation instruments → customers and payers → accessible roles → validation, while separating official facts, research opinions and business assumptions.

## Who it serves

- People in China evaluating careers, learning, ventures and projects.
- Overseas researchers seeking context on China's priorities and institutions.
- Overseas businesses researching China market entry, partnerships and implementation conditions.

The Skill separates policy alignment, demand, capability, timing and current access eligibility. It can conclude that evidence is insufficient or a question is not meaningfully related to the plans.

## Use

[Download v0.1.0](https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.1.0/china-five-year-plan-skill-v0.1.0.zip) · [Releases](https://github.com/xingyou1439/china-five-year-plan-skill/releases)

Install the complete `china-five-year-plan-skill` folder in an Agent Skills-compatible host, preserving relative file paths. For Codex, consult the [official Skills documentation](https://learn.chatgpt.com/docs/build-skills); local skills can be placed under `~/.agents/skills/`. This package does not claim to have been tested on every host.

```text
Use $china-five-year-plan-skill to explain investment in people in China,
with Chinese source evidence and a plain-English explanation.
```

```text
Use $china-five-year-plan-skill to assess our proposed eldercare technology
entry into China. Separate policy direction, customer demand and current eligibility.
```

English translations produced by the Skill are explanatory, not official translations.

## Information security

Publication includes only reviewed Skill files, policy knowledge and methods, public bibliographic metadata, hypothetical examples and validation code. Internal personnel details, contact information, participant lists, personal assignments, internal source files, local machine paths and credentials are excluded. Git commits use the public account and a GitHub no-reply address.

A fixed file allowlist, content checks and release-archive verification are required before publication; the same checks run on subsequent changes. See [publication security](PUBLICATION_SECURITY.md) for scope and limitations.

## Evidence and workflow

[SKILL.md](SKILL.md) routes understanding, domestic decisions and market entry. The package includes 28 quote-checked cards, the text layer of three official outlines with PDF-page locations, a cross-plan comparison, secondary-research synthesis, corrections, a source catalogue and usage examples.

Policy objective → instrument → actor/project → payer/procurement → accessible role → validation. A policy priority is not an order, an entitlement, a market-size estimate, a guarantee of returns or proof of operating permission.

Optional standard-library helpers require Python 3.9+:

```sh
python3 scripts/search_evidence.py --query "market entry hospital" --plan 15
python3 scripts/verify_bundle.py
python3 -m unittest discover -s tests -v
```

## Provenance and limitations

Reviewed on **2026-10-17**, the supplied directory contains 133 PDFs (126 distinct files, 2,590 pages), two images and two video/download files skipped as requested. Extraction/indexing is not page-by-page critical or visual verification. See [coverage](references/coverage.md) and the [catalogue](references/source-catalogue.json).

The documents mainly date through March 2026. Current implementation, access, licensing and other regulated questions require fresh primary-source verification for the actual activity, entity and geography. Archived forecasts are not current data. Raw broker reports and course PDFs are not distributed. Source-page numbers refer to the supplied editions and may differ from online copies. See [source notice](SOURCE_NOTICE.md).

**Version:** v0.1.0. This independent reference tool does not claim official endorsement, marketplace listing, validation on every host or demonstrated commercial outcomes.
