# The Divan method

Divan is named after the *divan* of historical Persian government: an administration made of
specialised departments — correspondence, finance, the army register — each doing one job well,
all answering to one decision-maker. A Divan agent team is the same shape: specialised agents,
one human owner.

## 1. Start from the organisation, not from the tools

A software product needs the same functions whether people or agents do the work:

| Human unit | What it owns | Divan agent |
|---|---|---|
| Product management | *What* to build and *why*; saying no | `spec-writer` |
| Engineering leadership | *How* to build it; architecture; splitting work | `architect` |
| Engineering | Building it, with tests | `builder` |
| Quality assurance | Finding what is wrong before users do | `reviewer` |
| Security & privacy | Keeping data safe and promises true | `security-checker` |
| Data science / ML (only if there is a model) | The model's input features | `feature-engineer` |
| DevOps & technical writing | Release preparation and documentation | `release-docs` |
| **Leadership** | **Decisions, priorities, taste, accountability** | **You. Not an agent.** |

The last row is the point. Agents multiply a good decision-maker; they do not replace one.

## 2. Where agents are strong, and where they are not

| Stage | Agent fit | Why |
|---|---|---|
| Discovery (talking to users) | Weak | Agents cannot feel a user's pain. They can only summarise evidence you bring. |
| Definition (specs, criteria) | Good | Fast, structured drafts. You still cut the scope. |
| Design | Medium | Solid options; real taste is yours. |
| Architecture | Medium | Good proposals; bad choices here are expensive, so you approve. |
| Build | Very good | The biggest return. |
| Review & QA | Good — **only if independent** | A builder grading its own work is not a review. |
| Launch (accounts, stores, legal) | Human | Accounts, signing keys and agreements are yours. |
| Measure | Medium | Good at analysing; you decide what matters. |

## 3. Feature Definition, not "Feature Engineering"

These two terms are often confused:

- **Feature Definition** — part of Requirements Engineering. Turning user needs into product features
  with acceptance criteria and a success signal. A product activity. Owned by `spec-writer`.
- **Feature Engineering** — a machine-learning activity. Creating, transforming and selecting the
  input variables a model learns from, with leakage checks. Owned by `feature-engineer`, and only
  present when the product actually has a model.

Using the ML term for product work costs credibility with engineers and invites confusion with AI teams.

The Feature Definition chain:

```
Business goal → User problem → Requirement → Feature → Acceptance criteria → Success signal
```

- **Acceptance criteria** answer: *is it built correctly?*
- **The success signal** answers: *was it worth building?*

A team that checks only the first becomes a feature factory: everything shipped to spec,
nothing anyone needed.

### The success signal respects the product's promises
If the product allows analytics, the signal can be an event metric. If the product promises
no tracking, the signal comes from what already exists — feedback mail, issue reports, social replies,
store reviews, aggregate server logs. **Never add tracking to measure a feature in a product that
promises none.** This rule came directly from the first real adaptation (see the Taghvim case study).

## 4. The loop and its three gates

```
Idea ─► spec-writer ─► GATE A ─► architect ─► GATE B ─► builder × tasks
     ─► reviewer ⟲ (max 3 rounds) ─► security-checker ─► release-docs ─► GATE C
     ─► 1–2 weeks after release: success signal vs target → keep / iterate / remove
```

- **Gate A — scope.** You approve the feature card, including what was cut.
- **Gate B — design.** You approve the approach; for visible changes you pick one of three variants.
- **Gate C — release.** You merge, deploy and publish. Agents never do.

Rules the orchestrator keeps:
- One feature per loop.
- The reviewer never sees the builder's self-report — it judges the result, not the story.
- A task that fails three builder attempts goes back to the architect to be split.
- Nothing is "done" because an agent said so; the orchestrator checks the file or runs the command.

## 5. Three facts that change everything

Before any agent works on a repository, three facts must be written in `CLAUDE.md`:

1. **What triggers a production deploy?** If a push to `main` deploys, an agent pushing is a release.
2. **What is the tracking policy?** It decides how success can be measured.
3. **What does the product publicly promise?** ("No third-party requests", "works offline",
   "no account needed".) The security agent checks every change against these by name.

Most agent-team mistakes are not coding mistakes. They are violations of one of these three facts
by an agent that was never told them.

## 6. The repo always wins

A mature repository already encodes decisions in its instructions, scripts and history.
Divan adapts to it, never the reverse: import the existing rules, do not copy them; resolve every
conflict in the repo's favour; remove agents that do not apply. The `divan-adapt` skill is the procedure,
and `docs/adapting.md` explains it.

## 7. Honest limits

- **Discovery is yours.** Feed agents real evidence or label claims as assumptions.
- **Taste is yours.** Agents produce acceptable UX, rarely great UX.
- **Speed hides debt.** If you cannot explain a module in two minutes, stop building and review.
- **Cost.** Long agent runs use many tokens. Small tasks are cheaper *and* better.
- **Formats change.** Agent and skill formats in coding tools evolve; check them against the
  current documentation of the tool you use.
