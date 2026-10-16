#!/usr/bin/env bash
# ============================================================================
# Divan installer
# Copies the Divan agent team (kit/) into a target repository.
# Never overwrites an existing file. Works with macOS bash 3.2 and Linux bash.
#
# Usage:
#   ./install.sh [TARGET_DIR] [--dry-run]
#
#   TARGET_DIR  repository to install into (default: current directory)
#   --dry-run   show what would happen, change nothing
# ============================================================================
set -eu

DRY_RUN=0
TARGET="."
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    -h|--help)
      sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    -*) echo "Unknown option: $arg" >&2; exit 1 ;;
    *) TARGET="$arg" ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KIT="$SCRIPT_DIR/kit"

if [ ! -d "$KIT" ]; then
  echo "Error: kit/ not found next to install.sh ($KIT)." >&2
  exit 1
fi
if [ ! -d "$TARGET" ]; then
  echo "Error: target directory does not exist: $TARGET" >&2
  exit 1
fi
TARGET="$(cd "$TARGET" && pwd)"
if [ "$TARGET" = "$SCRIPT_DIR" ]; then
  echo "Error: run this against your project, not the Divan repo itself." >&2
  exit 1
fi

[ "$DRY_RUN" = 1 ] && echo "DRY RUN — nothing will be changed."
echo "Installing Divan into: $TARGET"
echo

ADDED=0
SKIPPED=0
SKIPPED_LIST=""

copy_file() { # copy_file <relative path> <destination relative path>
  src="$KIT/$1"
  dst="$TARGET/$2"
  if [ -e "$dst" ]; then
    echo "  skip    $2  (already exists)"
    SKIPPED=$((SKIPPED + 1))
    SKIPPED_LIST="$SKIPPED_LIST $2"
    return
  fi
  echo "  add     $2"
  ADDED=$((ADDED + 1))
  if [ "$DRY_RUN" = 0 ]; then
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
  fi
}

# CLAUDE.md: if the project already has one, install ours beside it to merge by hand.
if [ -e "$TARGET/CLAUDE.md" ] && grep -q "Project Brain (Divan)" "$TARGET/CLAUDE.md"; then
  copy_file "CLAUDE.md" "CLAUDE.md"   # Divan's own template from an earlier run: plain skip
elif [ -e "$TARGET/CLAUDE.md" ]; then
  echo "  note    CLAUDE.md exists — installing the Divan template as CLAUDE.divan.md"
  copy_file "CLAUDE.md" "CLAUDE.divan.md"
else
  copy_file "CLAUDE.md" "CLAUDE.md"
fi

# Everything else in kit/, file by file.
( cd "$KIT" && find . -type f ! -name 'CLAUDE.md' ! -name '.DS_Store' | sed 's|^\./||' | sort ) > "${TMPDIR:-/tmp}/divan-files.$$"
while IFS= read -r rel; do
  copy_file "$rel" "$rel"
done < "${TMPDIR:-/tmp}/divan-files.$$"
rm -f "${TMPDIR:-/tmp}/divan-files.$$"

if [ "$DRY_RUN" = 0 ] && [ -f "$TARGET/.claude/hooks/quality-gate.sh" ]; then
  chmod +x "$TARGET/.claude/hooks/quality-gate.sh"
fi

echo
echo "Added $ADDED file(s), skipped $SKIPPED."

# ---------------------------------------------------------------- warnings
WARN=0
if [ -f "$TARGET/.gitignore" ] && grep -Eq '^[[:space:]]*/?\.claude/?[[:space:]]*$' "$TARGET/.gitignore"; then
  WARN=1
  cat <<'EOF'

! .gitignore ignores the whole .claude/ folder, so the team will not be committed.
  To share it, replace that line with:
      .claude/*
      !.claude/agents/
      !.claude/skills/
      !.claude/hooks/
      !.claude/settings.json
  (Personal files such as settings.local.json stay ignored.) On a public repo,
  keeping the team private may be the better choice — your call.
EOF
fi
for f in AGENTS.md CONTRIBUTING.md .cursorrules; do
  if [ -f "$TARGET/$f" ]; then
    WARN=1
    echo
    echo "! This repo already has $f. Do not let Divan duplicate it:"
    echo "  run the divan-adapt skill (\"adapt Divan to this repo\") in Claude Code."
  fi
done
if [ -e "$TARGET/CLAUDE.divan.md" ]; then
  WARN=1
  echo
  echo "! Merge CLAUDE.divan.md into your existing CLAUDE.md, then delete it."
fi

cat <<EOF

Next steps
  1. Fill every <…> in CLAUDE.md — especially section 2 (deploy trigger,
     tracking policy, public promises) and section 4 (commands).
  2. Open the repo in Claude Code and run /agents to check the team is loaded.
  3. Existing project? Say: "adapt Divan to this repo".
  4. Then: "run the feature loop for: <one small, real feature>".
EOF
[ "$WARN" = 1 ] && echo && echo "Read the warnings above first."
exit 0
