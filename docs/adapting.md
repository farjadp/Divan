# Adapting Divan to an existing repository

A new project can take the kit almost as it is. An existing project cannot: it already has rules,
some written down and some only visible in its scripts. Pasting a generic kit over them breaks things.

**Rule: the repo always wins.**

## The short version

1. Install: `./install.sh /path/to/your/repo` (it never overwrites a file).
2. Open the repo in Claude Code and say: **"adapt Divan to this repo"**.
   That runs the `divan-adapt` skill, which does the steps below and opens a pull request.
3. Review the pull request — especially the **conflict table** and the decisions it asks you to make.

## What the adaptation does

| Step | What happens | Why it matters |
|---|---|---|
| 1. Read first | Existing `AGENTS.md` / `CONTRIBUTING.md`, `.gitignore`, commands, CI, deploy config, PR template, privacy statements, recent history | Agents must know the repo's law before acting |
| 2. Baseline | Run tests, type-check, lint before any change; record the numbers | You cannot prove you broke nothing on a red or unknown baseline |
| 3. Conflict table | Every generic rule checked against the repo | The single most useful output — it shows the repo's hidden rules |
| 4. Adapt | Thin `CLAUDE.md` that imports existing rules; agents rewritten to cite real commands and promises; agents that do not apply removed | Copies of rules drift; references do not |
| 5. Verify | Same test numbers; hook proven to pass, block and respect its loop guard; ignore rules checked | Trust comes from evidence |
| 6. Hand over | Branch, pull request with the repo's template, owner decisions listed | The owner merges; agents never do |

## Conflicts you will probably meet

| The kit assumes | Your repo may say | Resolution |
|---|---|---|
| Agents may push | Push to `main` deploys | No agent pushes or tags |
| Success = analytics event | No tracking, by promise | Signal from feedback, issues, reviews, server logs |
| Generic security checklist | Specific public promises | The security agent checks them by name |
| ML agent included | No model | Remove it and say why |
| One design proposal | Owner picks among options | Architect prepares three variants |
| Changelog for everything | Changelog is user-facing | No entry for internal work |
| Feature cards in `docs/` | Roadmap lives in Notion / Linear | Cards as local notes in `.claude/work/` |
| `.claude/` committed | `.claude/` git-ignored | Narrow the ignore rule — **owner's decision** |

## About `.gitignore` and public repositories

Many repos ignore `.claude/` entirely. To share the team, the rule becomes:

```gitignore
.claude/*
!.claude/agents/
!.claude/skills/
!.claude/hooks/
!.claude/settings.json
```

Personal files (`settings.local.json`, working notes) stay ignored. On a **public** repository,
consider whether you want your agent setup visible. Keeping it local is a legitimate choice.

## A real example

[`case-studies/taghvim.md`](case-studies/taghvim.md) — the first adaptation, on a live product
with a 135-line `AGENTS.md`, where push means deploy and the product promises zero tracking.
Several of the kit's current rules exist because of what that adaptation found.
