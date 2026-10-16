# Case study: adapting Divan to Taghvim

**Date:** 15 October 2026 · **Pull request:** [farjadp/taghvim#3](https://github.com/farjadp/taghvim/pull/3)
**Status:** adaptation complete and verified; the pull request is open for the owner's review.
**Not yet done:** a full feature loop (idea → release) has not been run with this team. When it has,
the results will be added here — including where it broke.

## The product

[Taghvim](https://taghv.im) is a Persian (Solar Hijri) calendar: a Next.js website, a browser
extension for Chrome and Firefox, an Android app and an iPhone app (Capacitor), and native home-screen
widgets in Kotlin and Swift. It is open source, built by one person, and used by real readers.

## Why it was a hard first test

- **A 135-line `AGENTS.md`** recording every product decision with its reason, date and who decided —
  including decisions that were reversed and must not come back.
- **Push means deploy.** Every push to `main` is built and published by the hosting platform.
- **No tracking, by public promise.** No accounts, no ads, no database, no analytics; a privacy statement
  that a browser-store listing links to.
- **Zero network requests** in the extension and the Android app, enforced by build checks and by
  having no `INTERNET` permission.
- **Release artefacts are built in CI with provenance, and signed only on the owner's machine.**
- **`.claude/` was git-ignored.**

## Baseline

Before any change: **28 test files, 559 unit tests passing; type-check clean.**

## The conflict table

| Generic kit said | Taghvim says | Resolution |
|---|---|---|
| Agents may push a branch | Push to `main` deploys production | Deny rules for `git push`, `git tag`, `gh release` and both signing scripts; agents commit on a branch at most |
| Instrument an analytics event for the success metric | No tracking, ever | Success signal from feedback mail, GitHub issues, replies on X, store reviews, aggregate server counts |
| Generic `security-checker` | Specific promises: zero requests, privacy statement must stay true, keys never touched | Renamed **`privacy-guard`**; checks each promise by name |
| ML `feature-engineer` included | No model | Removed, with the reason written in `CLAUDE.md` |
| Architect proposes one design | Every visible design was picked by the owner from three variants | Architect prepares A/B/C with measured heights |
| Changelog entry for every change | The changelog is written for visitors; internal work gets none | `release-prep` writes no entry for internal work and bumps no version |
| Feature cards in `docs/product/` | The roadmap lives in Notion | Cards as local notes in `.claude/work/` (git-ignored) |
| Copy the rules into `CLAUDE.md` | `AGENTS.md` is the single source of truth | `CLAUDE.md` imports `@AGENTS.md`; agents point to it, never copy it |
| Builder runs tests | Also: read the framework's bundled docs first; never stop the server on port 3000; regenerate widget data when events change; file headers on every code file | All written into `builder` and checked by `reviewer` |
| `.claude/` committed | `.claude/` ignored | Narrowed to `.claude/*` with shared folders un-ignored — **flagged as the owner's decision** |

## Verification

- Unit tests and type-check after the change: **identical to the baseline** (559 passing).
- Quality-gate hook, tested by hand:
  - only documentation and agent files changed → exit 0 (lets the session finish);
  - a deliberate type error added to a source file → exit 2, with the exact compiler error handed back
    (the error was then reverted);
  - `stop_hook_active: true` → exit 0 (no infinite loop).
- `git check-ignore` confirmed personal settings and working notes stay ignored.

## What it taught the generic kit

Every row in that table that was not Taghvim-specific went back into Divan:

1. `CLAUDE.md` now has a section for **three facts**: what triggers a deploy, the tracking policy, and the public promises.
2. "Success metric" became **success signal**, gathered *within the tracking policy*.
3. `spec-writer` reads the repo's **decision log** before proposing anything.
4. `security-checker` checks the product's **public promises** by name.
5. `architect` prepares **three variants** for visible changes.
6. `release-docs` writes a **user-facing** changelog and nothing for internal work.
7. The quality gate ignores documentation-only changes.
8. A new skill, **`divan-adapt`**, turns this whole process into a procedure.

## One honest note

The adaptation took one session. The hard part was not writing agent files — it was **reading**:
135 lines of decisions, the scripts, the CI, the history. A generic kit installed without that reading
would have told agents to push (a production deploy) and to add analytics (breaking a public promise).
That is the case for `divan-adapt`.
