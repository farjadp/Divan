---
name: divan-adapt
description: Adapt the Divan agent team to an existing repository that already has its own rules (AGENTS.md, CONTRIBUTING, CI, release process). Use right after installing Divan into a real project, or when the owner says "adapt Divan to this repo". Finds every conflict between the generic kit and the repo, resolves each in the repo's favour, verifies, and opens a pull request.
---

# Adapt Divan to an existing repo

The generic kit is a starting point, not a rulebook. A mature repo already encodes decisions —
some written down, some only visible in its scripts and history. Pasting the kit over them breaks things.
**The repo always wins.** Your job is to bend Divan to fit it.

Work on a branch. Change nothing in the product code.

## Step 1 — Read before writing (no edits yet)
Read, in this order, and take notes:
1. Existing agent or contributor instructions: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `.cursorrules`,
   `.github/copilot-instructions.md`. These are the repo's law.
2. `.gitignore` — is `.claude/` ignored? (Common. It decides whether the team can be committed.)
3. `package.json` / `pyproject.toml` / `Makefile` — the real commands.
4. CI and release: `.github/workflows/`, release scripts, deploy config (Railway, Vercel, Fly…).
   Answer: **what exactly triggers a production deploy?**
5. PR template and branch-naming rules.
6. Privacy statements, `SECURITY.md`, store listings — **the public promises**.
7. Recent history: `git log --oneline -30` — how the owner actually works.

## Step 2 — Baseline
Install dependencies and run the tests, type-check and lint **before** changing anything.
Write down the numbers (e.g. "559 tests pass, typecheck clean"). If the baseline is already red,
stop and tell the owner — you cannot prove you broke nothing on a red baseline.

## Step 3 — Build the conflict table
For every generic rule in the kit, ask: *does this repo contradict it?* Typical conflicts:

| Generic kit assumes | What the repo may say instead | Resolution |
|---|---|---|
| Agents may push a branch to `main` | Push to `main` deploys production | Agents never push or tag |
| Measure success with an analytics event | The product promises no tracking | Success signal from feedback, issues, reviews, server logs |
| Generic security checklist | Specific public promises (zero requests, offline, no account) | Security agent checks those promises by name |
| ML `feature-engineer` agent | No model in the product | Remove the agent, say why in `CLAUDE.md` |
| One design proposal | Owner picks from several variants | Architect prepares A/B/C |
| `CHANGELOG.md` for everything | Changelog is user-facing only | Release agent writes no entry for internal work |
| `docs/product/` for feature cards | Roadmap lives elsewhere (Notion, Linear) | Cards as local notes in `.claude/work/` |
| Generic file style | File headers, colour tokens, i18n rules | Builder and reviewer cite the repo's style section |

Show this table to the owner. It is the most useful artefact of the whole adaptation.

## Step 4 — Adapt
- **`CLAUDE.md`:** if the repo has `AGENTS.md` (or similar), import it with `@AGENTS.md` and keep `CLAUDE.md`
  thin: the team table, the binding rules summarised **with a pointer to the full text**, and where agent work goes.
  Never copy the repo's rules into agent files — copies drift.
- **Agents:** edit each one to cite the repo's real commands, folders, invariants and promises by name.
  Rename where it helps (e.g. `security-checker` → `privacy-guard` for a privacy-first product).
- **Remove what does not apply** and say why (e.g. no ML agent).
- **`.gitignore`:** if `.claude/` is ignored, propose narrowing it to `.claude/*` with the shared folders
  un-ignored (`agents/`, `skills/`, `hooks/`, `templates/`, `settings.json`) and personal files kept local.
  This is the **owner's decision** — flag it clearly; on a public repo they may prefer to keep the team private.
- **Hook:** point the quality gate at the repo's real test and type-check commands; keep it fast
  (unit tests + types; leave builds and e2e to the reviewer).
- **Deny rules:** add the repo's dangerous commands (release tags, signing scripts, store uploads, key paths).

## Step 5 — Verify
1. Re-run the baseline: the numbers must be identical.
2. Prove the hook works: it exits 0 with only docs changed; exits 2 with a deliberate type error
   (then revert it); exits 0 when `stop_hook_active` is true.
3. `git check-ignore` confirms personal files stay ignored and shared files are tracked.
4. Validate `settings.json` as JSON and every agent/skill frontmatter.

## Step 6 — Hand over
Commit on a branch named the repo's way, push **the branch only** (confirm first that only the default
branch deploys), and open a pull request using the repo's PR template. The PR description includes:
the conflict table, every owner decision needed (especially `.gitignore`), the verification results,
and "no changelog entry — internal tooling" where that rule applies.

Never merge it yourself.

## Worked example
See `docs/case-studies/taghvim.md` in the Divan repository: a live Persian calendar (web, browser
extension, Android and iPhone apps) with a 135-line `AGENTS.md`, where push means deploy and the product
promises zero tracking.
