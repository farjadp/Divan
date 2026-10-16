<p align="center">
  <img src="assets/banner.svg" alt="Divan — a product team of AI agents, built around one human who decides" width="100%">
</p>

<p align="center">
  <b>English</b> · <a href="README.fa.md">فارسی</a> · <a href="README.ar.md">العربية</a> · <a href="README.zh-CN.md">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-3B82F6" alt="version 0.1.0">
  <img src="https://img.shields.io/badge/status-early-EAB308" alt="status: early">
  <img src="https://img.shields.io/badge/licence-MIT-22C55E" alt="MIT licence">
  <img src="https://img.shields.io/badge/for-Claude%20Code-6366F1" alt="for Claude Code">
</p>

<p align="center">
  <a href="docs/method.md">The method</a> ·
  <a href="docs/adapting.md">Adapting to an existing repo</a> ·
  <a href="docs/case-studies/taghvim.md">Case study</a> ·
  <a href="#about-the-author">About the author</a>
</p>

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

## The team

<p align="center">
  <img src="assets/team.svg" alt="The owner above seven specialised agents" width="100%">
</p>

| | Agent | Human equivalent | Edits code? |
|:-:|---|---|---|
| <img src="assets/icons/spec-writer.svg" width="28" alt=""> | `spec-writer` | Product manager — Feature Definition | No |
| <img src="assets/icons/architect.svg" width="28" alt=""> | `architect` | Tech lead — design, three variants, task breakdown | No |
| <img src="assets/icons/builder.svg" width="28" alt=""> | `builder` | Full-stack and mobile developer, one task at a time | Yes |
| <img src="assets/icons/reviewer.svg" width="28" alt=""> | `reviewer` | Senior engineer and QA — **independent** of the builder | No |
| <img src="assets/icons/security-checker.svg" width="28" alt=""> | `security-checker` | Security and privacy — checks your public promises | No |
| <img src="assets/icons/feature-engineer.svg" width="28" alt=""> | `feature-engineer` | ML engineer — model input features, **only if you have a model** | ML folder only |
| <img src="assets/icons/release-docs.svg" width="28" alt=""> | `release-docs` | DevOps and technical writer — prepares, never deploys | Docs only |

Plus:
- **`feature-loop`** — the process that connects them, with **three gates** where you decide.
- **`feature-definition`** — turning requests into small, testable features with a success signal.
- **`divan-adapt`** — adapting the kit to a mature repo **without breaking its rules**.
- **A quality-gate hook** that stops an agent from finishing while tests or type-check fail.
- **Deny rules**: no push, no tag, no release, no reading `.env` or signing keys.

## The loop

<p align="center">
  <img src="assets/loop.svg" alt="The feature loop: spec-writer, gate A, architect, gate B, builder, reviewer, security-checker, release-docs, gate C, released, signal versus target" width="100%">
</p>

- **Gate A — scope.** You approve the feature card, including what was cut.
- **Gate B — design.** You approve the approach and pick one of three variants.
- **Gate C — release.** You merge, deploy and publish. Agents never do.

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
docs/                       method, adapting guide, case study
assets/                     logo, banner, diagrams, agent icons
scripts/make_assets.py      rebuilds every image in assets/
```

## Contributing

Real-world reports are the most valuable contribution: you installed Divan on a real project —
what conflicted, what broke, what you changed. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## About the author

<img src="assets/logo.svg" width="72" align="left" alt="" style="margin-right:16px">

**Farjad Pourmohammad** is an AI strategist, startup mentor and builder based in Toronto, Canada.
He has spent more than twenty years building technology companies in Iran and Canada — founding and
running a software company, leading engineering teams as a CTO, and building products of his own,
including [Taghvim](https://taghv.im), an open-source Persian calendar for the web, browsers and phones.
Today he mentors early-stage founders and helps businesses decide where AI actually earns its place.
Divan comes from that work: the discipline he asks of founders — define the problem, cut the scope,
measure the result — applied to a team of AI agents.

*From complexity, to clarity, to action.*

### Services

| | Service | What it is |
|:-:|---|---|
| 🧭 | **AI strategy** | Where AI earns its place in your business — then designing, building and securing it. |
| 🚀 | **Startup mentorship — The Founder Lab** | A free 8-week programme for five teams: customer discovery and lean validation, before you build. |
| 🤝 | **Founder advisory & coaching** | One-to-one sessions: a sparring partner for the decisions only you can make. |
| 🛠️ | **Web, app & AI product development** | Through AshaVid: websites, browser extensions, Android and iPhone apps, widgets and automation. |
| 🔤 | **Persian & right-to-left products** | Correct RTL layout, fonts, Persian digits and Solar Hijri dates, for products with Persian-speaking users. |

**Start small:** a free diagnostic call or a ten-minute self-assessment on the website.

🌐 **[farjadp.info](https://farjadp.info)** ·
💼 [LinkedIn](https://www.linkedin.com/in/farjadpourmohammad) ·
▶️ [YouTube @FarjadTalks](https://www.youtube.com/@FarjadTalks) ·
🐙 [GitHub @farjadp](https://github.com/farjadp)

---

## Licence

MIT — see [LICENSE](LICENSE). Agent glyphs are from [Lucide](https://lucide.dev) (ISC) — see
[assets/NOTICE-lucide.txt](assets/NOTICE-lucide.txt).

Divan is an independent project. It is not affiliated with or endorsed by Anthropic.
"Claude" and "Claude Code" are trademarks of Anthropic.
