# China's 15th Five-Year Plan (2026–2030): Policy Analysis and Decision Reference

**Understand China's priorities and decide what to investigate next.**

A free, bilingual AI skill for exploring careers, learning, ventures, projects and China market entry. Install it in a compatible AI assistant, describe your situation, and ask a question. It draws on China's 13th, 14th and 15th Five-Year Plans, with traceable sources and practical next steps.

[Get started](#use) · [中文](README.md) · [Read before installing](https://xingyou1439.github.io/china-five-year-plan-skill/)

## What can you ask?

- How have China's eldercare priorities changed from the 14th to the 15th Five-Year Plan? Explain the changes in plain English and link to the original text.
- I have five years of marketing experience and want to learn AI. Which adjacent directions should I investigate, and what skills would I need?
- We supply eldercare technology overseas. What policy priorities and current market-entry conditions should we verify before considering China?

Start with “I currently do ____, and I want to understand ____.” Choose to understand a direction, compare options or plan a next step. No complete intake form is required; only add location, alternatives, time and budget when they could change the answer. Answers explain the judgment, cite document titles and sections, identify missing evidence and suggest a next step. Policy direction, demand, capability and operating eligibility are assessed separately; insufficient evidence is a valid result.

The first answer aims for one screen: a provisional judgment, relevant sources, the biggest unknown and a useful action. Ask for a private decision note to save your alternatives, evidence and review conditions. Paste it back with new findings to continue; the Skill does not promise memory across chats. Request and review a redacted shareable version separately. The website builds prompts locally; it does not run a model. See the [complete constructed walkthrough](examples/first-session.md) and [decision-note template](references/decision-note.md).

Optional [Chinese examples and short PDF](https://xingyou1439.github.io/china-five-year-plan-skill/#downloads) demonstrate the method through hypothetical scenarios. They are supporting reading; use the installed Skill to analyze your own situation. English explanations are not official translations.

## Use

[Download v0.3.0](https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.3.0/china-five-year-plan-skill-v0.3.0.zip) · [Releases](https://github.com/xingyou1439/china-five-year-plan-skill/releases)

### WorkBuddy

Paste into the WorkBuddy chat to download the package:

```text
Download this Skill ZIP to my computer and tell me where it was saved. Keep it zipped:
https://github.com/xingyou1439/china-five-year-plan-skill/releases/download/v0.3.0/china-five-year-plan-skill-v0.3.0.zip
```

Then open **Experts · Skills · Connectors → Skills → Add Skill → Upload Skill** and select the ZIP. Search for `china-five-year-plan-skill` under Installed, confirm it is enabled, and start a new conversation. You can also use the download link above. [WorkBuddy's official guide](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) requires custom packages to be imported through Upload Skill; chat installation currently covers marketplace skills only.

### Codex

Paste into your local Codex chat:

```text
$skill-installer Install https://github.com/xingyou1439/china-five-year-plan-skill
Ref: v0.3.0; path within the repository: .; install name: china-five-year-plan-skill.
Install the complete folder and check that SKILL.md and references/ are present. Inspect any existing installation before proceeding; do not overwrite it.
```

Start a new conversation after installation; restart Codex if the Skill is not detected. See the [official Codex guide](https://learn.chatgpt.com/docs/build-skills).

### Claude Code

Paste into your local Claude Code chat:

```text
Install the complete v0.3.0 version of https://github.com/xingyou1439/china-five-year-plan-skill
into ~/.claude/skills/china-five-year-plan-skill, preserving relative file paths.
Inspect an existing destination before proceeding; do not overwrite it. Check that SKILL.md and references/ are present.
```

Invoke it with `/china-five-year-plan-skill`. See [Claude Code's official personal skill locations](https://code.claude.com/docs/en/skills#choose-where-skills-load).

Codex is the recommended starting host. Earlier v0.1.0 testing covered official-installer installation and evidence retrieval. For v0.3.0, see [the exact validation scope](tests/v0.3-validation.md): package integrity, a fresh local copy and evidence retrieval. New-session discovery and independent model behavior were not tested in this release; WorkBuddy import and Claude Code invocation also remain untested. Keep the complete folder, including references and scripts.

### After installation

Paste a question like these, replacing the scenario with your own. In Claude Code, you can start with `/china-five-year-plan-skill` instead.

```text
Use china-five-year-plan-skill to explain investment in people in China,
quoting Chinese policy text you actually read, with sources and a plain-English explanation.
If the Skill is not installed, say so directly.
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

**Version:** v0.3.0. This independent reference tool does not claim official endorsement, marketplace listing, validation on every host or demonstrated commercial outcomes.
