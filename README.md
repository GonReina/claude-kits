# claude-kits

A collection of [Claude Code](https://claude.com/claude-code) configurations I use day to day — skills, subagents, hooks and settings, bundled per project type into self-contained "kits".

Each top-level folder is one kit. Drop its contents into a project (or point Claude Code at it directly) and its `.claude/` config and `CLAUDE.md` take over from there.

## Kits

| Kit | What it's for |
|---|---|
| [`study-kit`](study-kit/CLAUDE.md) | Turns a folder (e.g. an Obsidian vault) into a maths/physics study environment: guided teaching, problem coaching, timed exam practice, paper reading, spaced-repetition recall, and verified figures. |

## Using a kit

1. Copy the kit folder's contents into the root of the project you want it in (so `.claude/` and `CLAUDE.md` sit at that project's top level).
2. Read the kit's `CLAUDE.md` — it documents the conventions and any one-time setup.
3. Run `claude` from that project root.

## Contributing

These are personal, opinionated configs, shared as-is in case they're useful to others. Feel free to fork and adapt.
