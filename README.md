# Divan

**A product team of AI agents for software projects — built around one human who decides.**

[فارسی](README.fa.md) · [The method](docs/method.md) · [Adapting to an existing repo](docs/adapting.md) · [Case study](docs/case-studies/taghvim.md)

> **Status: early (v0.1).** Divan has been installed and adapted on one live product
> ([case study](docs/case-studies/taghvim.md)). A full feature loop — idea to release — has **not** yet
> been run end to end. Results, including failures, will be published here when it has.

---

## The problem

AI coding agents are fast. Speed is not the problem. The problem is that a single agent asked to
"build the feature" acts as product manager, architect, developer and reviewer at once — and grades
its own work. You get a lot of code quickly, and some of it solves the wrong problem, breaks a rule
nobody told it about, or pushes straight to production.

Human teams solved this long ago with **separate roles and approval points**. Divan brings that
structure to agents.

## What Divan is

A drop-in kit for [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) that turns a
repository into an organisation:

| Agent | Human equivalent | Edits code? |
|---|---|---|
| `spec-writer` | Product manager — Feature Definition | No |
| `architect` | Tech lead — design, three variants, task breakdown | No |
| `builder` | Full-stack and mobile developer, one task at a time | Yes |
| `reviewer` | Senior engineer and QA — **independent** of the builder | No |
| `security-checker` | Security and privacy — checks your public promises | No |
| `feature-engineer` | ML engineer — model input features, **only if you have a model** | ML folder only |
| `release-docs` | DevOps and technical writer — prepares, never deploys | Docs only |

Plus:
- **`feature-loop`** — the process that connects them, with **three gates** where you decide.
- **`feature-definition`** — turning requests into small, testable features with a success signal.
- **`divan-adapt`** — adapting the kit to a mature repo **without breaking its rules**.
- **A quality-gate hook** that stops an agent from finishing while tests or type-check fail.
- **Deny rules**: no push, no tag, no release, no reading `.env` or signing keys.

## The loop

```
Idea ─► spec-writer ─► GATE A (you approve scope)
     ─► architect   ─► GATE B (you approve design, pick a variant)
     ─► builder × tasks ─► reviewer ⟲ (max 3 rounds) ─► security-checker
     ─► release-docs ─► GATE C (you merge, deploy, publish)
     ─► after release: success signal vs target → keep / iterate / remove
```

Agents execute. **You** decide what to build, what to cut, and when it is good enough.

## Install

```bash
git clone --depth 1 https://github.com/farjadp/divan.git
./divan/install.sh /path/to/your/project
```

The installer **never overwrites a file**. If your project already has a `CLAUDE.md`, Divan's template
is written beside it as `CLAUDE.divan.md` for you to merge. It warns you if `.gitignore` hides `.claude/`
or if the repo already has agent instructions (`AGENTS.md`, `CONTRIBUTING.md`).
Use `--dry-run` to see what it would do.

Then:

1. Fill in `CLAUDE.md` — above all **section 2**, the three facts below, and **section 4**, your real commands.
2. Open the project in Claude Code and run `/agents` to see the team.
3. **Existing project?** Say: *"adapt Divan to this repo."*
4. Say: *"run the feature loop for: <one small, real feature>."*

## Three facts every agent must know

Most agent-team failures are not coding mistakes. They are an agent breaking one of these,
because nobody wrote it down:

1. **What triggers a production deploy?** If pushing to `main` deploys, an agent pushing is a release.
2. **What is the tracking policy?** It decides how success can be measured. Divan never adds tracking
   to a product that promises none.
3. **What does the product publicly promise?** ("No third-party requests", "works offline".)
   The security agent checks every change against each one by name.

## Feature Definition is not Feature Engineering

**Feature Engineering** is a machine-learning term: building the input variables a model learns from.
Turning user needs into product features is **Feature Definition**, part of Requirements Engineering.
Divan keeps the two apart — different agents, different words. [More in the method.](docs/method.md#3-feature-definition-not-feature-engineering)

## Why "Divan"?

In historical Persian government, the *divan* was the administration: specialised departments —
correspondence, finance, the army register — each doing one job well, all answering to one
decision-maker. That is the shape of this team.

## Honest limits

- **Discovery is yours.** Agents cannot interview users. Give them evidence or mark claims as assumptions.
- **Taste is yours.** Agents produce acceptable design, rarely great design.
- **Accounts are yours.** Stores, payments, signing keys, legal — human only.
- **Speed hides debt.** If you cannot explain a module in two minutes, stop and review.
- **Cost.** Long agent runs use many tokens. Small tasks are cheaper and better.
- **Tools change.** Agent, skill and hook formats evolve; check them against the current
  [Claude Code documentation](https://docs.claude.com/en/docs/claude-code/overview).

## Repository layout

```
install.sh                  installer (never overwrites)
kit/                        what gets copied into your project
  CLAUDE.md                 project brain template
  .claude/agents/           the seven agents
  .claude/skills/           feature-loop, feature-definition, divan-adapt
  .claude/hooks/            quality gate
  .claude/settings.json     hook + deny rules
  docs/templates/           feature card, review, decision record
  docs/product/             requirements traceability table
docs/
  method.md                 why the team is shaped this way
  adapting.md               bringing Divan into an existing repo
  case-studies/taghvim.md   the first real adaptation
```

## Contributing

Real-world reports are the most valuable contribution: you installed Divan on a real project —
what conflicted, what broke, what you changed. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Author and licence

Made by [Farjad Pourmohammad](https://github.com/farjadp). MIT licence — see [LICENSE](LICENSE).

Divan is an independent project. It is not affiliated with or endorsed by Anthropic.
"Claude" and "Claude Code" are trademarks of Anthropic.
