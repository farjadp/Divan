# Contributing to Divan

## The most valuable contribution: a field report

You installed Divan on a real project. Open an issue with the **field report** template and tell us:

- the project type (web, mobile, extension, backend; stack; size),
- what the `divan-adapt` conflict table found,
- what broke during a feature loop, and at which gate,
- what you changed in the agents and why.

Reports of failures are as welcome as successes. They are how the kit improves —
most of v0.1's rules came from one real adaptation.

## Changing the kit

- Keep agents **role-pure**: a reviewer that fixes code is no longer independent.
- Every rule needs a reason. If you add one, say in the pull request what went wrong without it.
- Test `install.sh` against an empty repo and a repo that already has `CLAUDE.md`,
  `AGENTS.md` and an ignored `.claude/`. It must never overwrite a file, and a second run must add nothing.
- Validate `kit/.claude/settings.json` as JSON and every agent and skill frontmatter.
- Write in plain English. Persian translations of user-facing docs are welcome.

## Scope

Divan is about **structure and judgement**: roles, gates, definitions, guardrails.
Stack-specific agents (a "Next.js expert", a "Flutter expert") belong in your own fork or project,
adapted with `divan-adapt` — not in the generic kit.
