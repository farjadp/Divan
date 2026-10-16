#!/usr/bin/env bash
# Divan quality gate — a Claude Code Stop hook.
# Runs when Claude is about to finish a turn.
# If code changed and lint/type-check/tests fail, it blocks the stop (exit 2)
# and sends the failure back to Claude so it must fix it.
# Edit the COMMANDS section for your stack (or keep auto-detect).

INPUT="$(cat)"
# Avoid infinite loops: if this stop was already triggered by this hook, let it finish.
if echo "$INPUT" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0

# Only code changes need the gate: notes, docs and agent files do not.
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  CHANGED="$(git status --porcelain -- . ':(exclude).claude' ':(exclude)docs' ':(exclude)*.md' 2>/dev/null)"
  [ -z "$CHANGED" ] && exit 0
fi

FAILED=""
run() { # run "label" command...
  local label="$1"; shift
  OUT="$("$@" 2>&1)"; local code=$?
  if [ $code -ne 0 ]; then FAILED="${FAILED}\n--- ${label} FAILED ---\n$(echo "$OUT" | tail -n 40)"; fi
}

# ---------- COMMANDS (auto-detect; replace with your own if needed) ----------
if [ -f package.json ]; then
  PM="npm"; [ -f pnpm-lock.yaml ] && PM="pnpm"; [ -f yarn.lock ] && PM="yarn"
  grep -q '"lint"'      package.json && run "lint"       $PM run lint
  grep -q '"typecheck"' package.json && run "type-check" $PM run typecheck
  grep -q '"test"'      package.json && run "tests"      $PM test --silent
fi
if [ -f pyproject.toml ] || [ -f requirements.txt ]; then
  command -v ruff   >/dev/null 2>&1 && run "lint (ruff)" ruff check .
  command -v pytest >/dev/null 2>&1 && run "tests (pytest)" pytest -q
fi
# -----------------------------------------------------------------------------

if [ -n "$FAILED" ]; then
  echo -e "Quality gate failed. Fix these before finishing:${FAILED}" >&2
  exit 2
fi
exit 0
