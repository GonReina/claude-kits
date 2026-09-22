# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of portable Claude Code configurations ("kits"), published for others to use. There is no shared build, no package manager, and no test runner at the repo root — each kit is a self-contained bundle of `.claude/` config (agents, hooks, skills, settings) plus a `CLAUDE.md`, meant to be copied into the root of a target project.

## Repo structure

- One top-level folder per kit (e.g. `study-kit/`).
- Inside a kit folder, `.claude/` and `CLAUDE.md` sit at that folder's top level — this is the exact layout a user copies into their own project root. Do not nest a kit's `.claude/` any deeper than that, and do not repeat the kit's name as a subfolder inside itself.
- A kit's own `CLAUDE.md` is the authority for that kit's conventions once it's deployed into a project; this root `CLAUDE.md` only covers the meta-repo.

## Working on a kit

- Treat each kit as an isolated unit: skills/agents/hooks in one kit should not reference or depend on another kit.
- Kits commonly include small Python utilities invoked by skills or hooks (e.g. `study-kit/.claude/skills/recall/scripts/srs.py`, `study-kit/.claude/hooks/mirror.py`). There's no test suite for these — verify changes by running the script directly with `python3 <path> <args>` (check the script's own `--help` or docstring for its CLI).
- `settings.json` inside a kit wires up its hooks (see `study-kit/.claude/settings.json` for the pattern: `UserPromptSubmit`/`Stop` hooks calling a Python script with `$CLAUDE_PROJECT_DIR`). Hook scripts should stay best-effort and never fail loudly or block the session, since a hook error affects every Claude Code session run against that kit.
- Skill files (`.claude/skills/<name>/SKILL.md`) carry the trigger conditions in their frontmatter `description` — keep those precise, since that's how Claude decides when to invoke the skill.
- Agent files (`.claude/agents/<name>.md`) declare their own `tools:` allowlist in frontmatter; keep it minimal to what the agent actually needs.

## Adding a new kit

1. Create `<kit-name>/` at the repo root with `.claude/` and `CLAUDE.md` directly inside it (no extra nesting).
2. Write the kit's `CLAUDE.md` as the onboarding doc for whoever drops it into their project — conventions, folder layout it expects/creates, and how its skills/agents/hooks fit together.
3. Add a row for it to the table in the root `README.md`.
