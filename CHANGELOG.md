# Changelog

## 0.1.1 — 2026-10-15

- README in four languages: English, Persian (فارسی), Arabic (العربية) and Simplified Chinese (中文).
- Visual identity: logo, banner, team chart, feature-loop diagram and an icon for each agent
  (`assets/`), rebuilt by `scripts/make_assets.py`. Agent glyphs from Lucide (ISC), credited in
  `assets/NOTICE-lucide.txt`.
- About the author and services, in every language.

## 0.1.0 — 2026-10-15

First public version.

- Seven agents: `spec-writer`, `architect`, `builder`, `reviewer`, `security-checker`,
  `feature-engineer` (ML only), `release-docs`.
- Three skills: `feature-loop` (with three owner gates), `feature-definition`, `divan-adapt`.
- Quality-gate Stop hook (skips documentation-only changes; loop guard) and deny rules.
- `install.sh`: never overwrites, `--dry-run`, warns about an ignored `.claude/` and existing
  agent instructions; works with macOS bash 3.2.
- `CLAUDE.md` template with the **three facts** section: deploy trigger, tracking policy, public promises.
- Docs: the method, adapting to an existing repo, and the Taghvim case study.

Lessons from the first real adaptation (Taghvim) built into this version: success *signal* within
the tracking policy, decision-log check before proposing, public-promise checks, three design
variants, user-facing changelog only.

**Not yet validated:** a full feature loop, idea to release, on a real product.
