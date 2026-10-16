---
name: feature-loop
description: Orchestrate the agent team to take one feature from idea to release-ready - spec-writer, architect, builder, reviewer, security-checker, feature-engineer (if ML), release-docs - with human approval gates. Use when the owner says "run the loop", "build feature X", or gives a new feature idea.
---

# Feature Loop — how the agent team works together

You (the main session) are the **orchestrator**. You assign work to subagents, pass their
outputs forward, and stop at every gate for the human owner. You do not do the specialists' work yourself.

```
Idea ─► [1 spec-writer] ─► GATE A ─► [2 architect] ─► GATE B ─► [3 builder ×N tasks]
     ─► [4 reviewer] ─┬─ changes ─► back to 3 (max 3 rounds, then escalate)
                      └─ approve ─► [5 security-checker] ─► [6 release-docs] ─► GATE C (owner merges/deploys)
              (if the feature needs a model: [ML feature-engineer] runs between 2 and 3)
```

## Step by step

**0. Intake** — Restate the idea in one sentence. Create a task list with the stages below.

**1. Definition** — Call `spec-writer` with the idea and any evidence.
→ **GATE A (owner):** show the feature card(s), the RICE scores and what was cut.
Ask: "Approve, change, or cut?" Do not continue without a clear approval.

**2. Design** — Call `architect` with the approved card IDs.
→ **GATE B (owner):** show the impact map, risks, any PROPOSED ADR, and the task list.
For a visible change, show the three variants and ask the owner to pick one.
An ADR must be ACCEPTED by the owner before building.

**2b. ML (only if the design says the feature depends on a model)** — Call `feature-engineer`.
If its report says the model does not beat the baseline, bring that to the owner before building.

**3. Build** — For each task in dependency order, call `builder` with ONE task.
Independent tasks may run in parallel. If a builder reports BLOCKED, resolve or escalate — never guess.

**4. Review** — Call `reviewer` with the card and the diff. Do **not** pass the builder's report to the reviewer.
- CHANGES REQUESTED → send blockers/majors back to `builder` as new tasks. Max 3 rounds; then stop and
  tell the owner the task is stuck and why.

**5. Security** — Call `security-checker` when the change touches auth, data, payments, uploads,
external APIs, AI prompts or infra — and always before a release. Any CRITICAL/HIGH → back to step 3.

**6. Release prep** — Call `release-docs`.
→ **GATE C (owner):** present the release package. The owner merges, deploys and publishes. Agents never do —
check `CLAUDE.md` §2: if a push deploys, even "just pushing the branch to main" is a release.

**7. After launch (owner + spec-writer, ~1–2 weeks later)** — Compare the success signal to its target.
Decide: keep, iterate, or remove. Write the result into the feature card.

## Orchestrator rules
- One feature per loop. Do not start feature #2 until #1 reaches Gate C, unless the owner says so.
- Keep the owner's view short: at each gate, ≤ 10 lines + links to files.
- Never mark a stage complete because an agent *said* it is done — check the file or the test output.
- Cost control: if a single task takes more than ~3 builder attempts, stop and ask the architect to split it.
