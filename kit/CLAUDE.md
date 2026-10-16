# CLAUDE.md — Project Brain (Divan)

> Fill every `<…>` field. Every agent reads this file first; if it is wrong or empty, every agent is wrong.
>
> **Does this repo already have agent instructions** (`AGENTS.md`, `CONTRIBUTING.md`, an existing `CLAUDE.md`)?
> Then do not duplicate them. Import the existing file on its own line (for example `@AGENTS.md`),
> keep this file thin, and state that the existing file wins on any conflict.
> The `divan-adapt` skill walks through this.

## 1. Product
- **Name:** <product name>
- **One-line purpose:** <who it is for> + <what problem it solves>
- **Platforms:** Web (<framework>) · Mobile (<React Native / Flutter / Capacitor / native>) · Other (<extension, desktop…>)
- **Stage:** <Discovery / MVP / PMF / Scale>
- **North-star:** <the one outcome that means the product is working>

## 2. Three facts that change how agents must behave
- **What triggers a deploy?** <e.g. "every push to main deploys to production" / "manual release only">
  → If a push deploys, no agent may push. Ever.
- **Tracking policy:** <"analytics allowed: PostHog" / "no tracking at all — privacy promise">
  → This decides how success is measured (see the `feature-definition` skill).
- **Public promises the code must keep:** <e.g. "no third-party requests", "works offline", "no account needed">
  → The `security-checker` checks every change against these.

## 3. Stack (change only through a recorded decision)
- Frontend web: <…>
- Mobile: <…>
- Backend: <… or "none">
- Database: <… or "none">
- Hosting: <…>
- Auth: <… or "none">
- Analytics: <… or "none, by design">
- ML / AI (if any): <models, providers — or "none">

## 4. Commands
- Install: `<cmd>`
- Dev: `<cmd>` (port: <n>; never stop processes on other ports)
- Lint: `<cmd>`
- Type-check: `<cmd>`
- Test: `<cmd>`
- Build: `<cmd>`
- E2E: `<cmd or "none">`

## 5. The team (Divan)
The **owner** decides what to build, what to cut, and when it is good enough. Agents execute.
No agent merges, pushes to a deploying branch, tags a release, changes pricing, touches signing keys,
or touches real user data without the owner's explicit approval in chat.

| Agent | Role (human equivalent) | Writes code? |
|---|---|---|
| `spec-writer` | Product Manager — Feature Definition | No |
| `architect` | CTO / Tech Lead — design, variants, task breakdown | No (decision records only) |
| `builder` | Full-stack + mobile developer | Yes |
| `reviewer` | Senior engineer + QA — independent review | No (reports only) |
| `security-checker` | Security & privacy engineer | No (reports only) |
| `feature-engineer` | ML engineer — model input features (**only if the product has a model**) | Yes, in the ML folder only |
| `release-docs` | DevOps + tech writer | Docs and changelog only |

The process that connects them is the `feature-loop` skill.

## 6. Vocabulary (use these words exactly)
- **Requirement** — a need in user or business terms. "Users need to know when a price crosses their target."
- **Feature** — a product capability that satisfies one or more requirements. "Price alerts."
- **Feature Definition** — turning requirements into features with acceptance criteria and a success signal.
  A *product* activity, part of Requirements Engineering. It is **not** called Feature Engineering.
- **Feature Engineering** — an *ML* activity: creating, transforming and selecting input variables for a model.
  Only `feature-engineer` does this.
- **Acceptance criteria** — "Is it built correctly?" (testable, Given/When/Then).
- **Success signal** — "Was it worth building?" (a measurable or observable change, gathered within the tracking policy).

## 7. Rules for every agent
1. Read this file (and any file it imports) and the relevant feature card before starting.
2. One feature card = one branch = one pull request.
3. Every code change ships with tests. No tests → not done.
4. No new dependency without a one-line reason.
5. Never put secrets, keys or real user data in code, logs, tests or prompts.
6. If the spec is unclear, stop and ask. Do not guess and build.
7. A task bigger than about one day of human work goes back to `architect` to split.

## 8. Where agent work goes
- Feature cards: `docs/product/F-<n>-<slug>.md` · Reviews: `docs/reviews/` · Decisions: `docs/adr/`
  (or `.claude/work/` if the owner prefers working notes kept out of git).
- Templates: `docs/templates/`.

## 9. Definition of Done
- [ ] Acceptance criteria all pass (automated where possible)
- [ ] Lint, type-check, tests green
- [ ] `reviewer` verdict = APPROVE
- [ ] `security-checker` has no CRITICAL/HIGH open
- [ ] Success signal defined (and instrumented only if the tracking policy allows)
- [ ] Changelog entry written for user-visible changes
- [ ] Owner approved the merge
