---
name: feature-definition
description: Turn requirements into small, testable, valuable product features with traceability, acceptance criteria and a success signal. Use when defining, prioritizing or refining features or the backlog. This is product Feature Definition, not ML Feature Engineering.
---

# Feature Definition

## Name first
This activity is often wrongly called "Feature Engineering". In software and AI,
**Feature Engineering** means creating input variables for a machine-learning model
(see the `feature-engineer` agent). What this skill covers is **Feature Definition**,
part of **Requirements Engineering**. Use the correct words in specs, PRs and talks.

## Why it matters
Bad feature definition is the cheapest mistake to make and the most expensive to fix.
Done well, it:
1. Makes sure every feature fully implements the requirements it was approved for.
2. Keeps the product consistent with its strategy and principles.
3. Cuts wasted development effort and speeds up delivery.
4. Gives product, design and engineering one shared understanding.
5. Makes testing, release and adding future features easier.

## The full chain (the screenshot version stops at step 3 — that is the trap)
```
1 Business goal → 2 User problem → 3 Requirement → 4 Feature → 5 Acceptance criteria → 6 Success signal
```
- Steps 1–4 tell you **what** to build and **why**.
- Step 5 answers: *Is it built correctly?*
- Step 6 answers: *Was it worth building?*
A team that implements 100% of requirements but never checks step 6 becomes a **feature factory**.

## Procedure

### Step A — Collect and write requirements
- Write each requirement as a need, not a solution:
  ✅ "Users need to know when gold drops below their target price."
  ❌ "Add a push notification button."
- Give each an ID (`R-001`) and a source (interview #, support ticket, data, owner decision).
  A requirement with no source is an assumption — label it `ASSUMPTION`.

### Step A2 — Check what was already decided
Search the repo's decision log (`AGENTS.md`, `docs/adr/`, the changelog). If an earlier decision covers
this, quote it and explain what is different now — or stop. Re-debating settled questions is waste.

### Step B — Evaluate before you commit (this is where you say NO)
For each requirement, decide: **Do now · Later · Won't do**.
Score candidates with RICE = (Reach × Impact × Confidence) ÷ Effort.
- Low confidence → run a cheap test first (prototype, fake-door button, 5 user interviews).
- Expect to drop 30–50% of raw requirements. That is healthy, not a failure.
- Record every "Won't do" with its reason, so it is not re-debated every month.

### Step C — Turn approved requirements into features
- Every feature links to **at least one** requirement (traceability). No requirement → no feature.
- Keep features **small and independent** (INVEST). If a feature needs more than ~1–2 weeks
  of team work, split it by user value, not by technical layer:
  ✅ "Set one price alert" then "Edit/delete alerts"
  ❌ "Alert backend" then "Alert frontend"
- Involve design and engineering **at this step**, not after. A 15-minute check
  ("Is this feasible? Is there a simpler version?") saves weeks.

### Step D — Write acceptance criteria
Given / When / Then. Each criterion must be checkable in under 5 minutes.
```
Given I am a signed-in user with no alerts
When I set an alert for 18K gold at 3,500,000
Then I see it in "My alerts" and receive a push within 60 seconds of the price crossing it
```
Always add criteria for: empty state, error state, offline (mobile), and permission denied.

### Step E — Define one success signal (within the tracking policy)
Format: **signal · target · window · how gathered**. Read the tracking policy in `CLAUDE.md` §2 first.
- **Analytics allowed:** "≥ 25% of new users create an alert within 7 days · event `alert_created`."
- **No tracking (privacy-first product):** use what already exists — feedback mail, issue reports,
  replies on social media, app-store reviews, aggregate server request counts.
  "The question 'how do I get alerts?' stops appearing in replies within two weeks."
Never add tracking to measure a feature in a product that promises none.
No signal → the feature is not ready.

### Step F — Keep the backlog healthy
- Refine weekly: re-rank, split large items, delete stale items (> 90 days untouched = delete or re-justify).
- After launch, compare the success signal to its target. Missed it? Decide: iterate, or remove the feature.
  Removing a feature that does not work is a product win.

## Worked example
| Link | Content |
|---|---|
| Business goal | Grow daily active users of a price app |
| User problem | Users check prices 10 times a day and still miss good buying moments |
| Requirement R-004 | Users need to know when a price crosses their target |
| Feature F-012 | Price alerts (create, list, delete) with push notification |
| Acceptance criteria | (as in Step D) |
| Success signal | ≥ 25% of new users create an alert in 7 days (analytics allowed); in a no-tracking product: alert questions stop appearing in feedback within 2 weeks |
| Out of scope | Smart/predictive alerts (needs ML → `feature-engineer`, later) |

## Further reading
Phillip A. Laplante & Mohamad Kassab, *Requirements Engineering for Software and Systems*, 4th ed.
