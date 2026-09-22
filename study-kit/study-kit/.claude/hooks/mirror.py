#!/usr/bin/env python3
"""Mirror the Claude Code conversation into the current Obsidian session note.

Called by hooks in .claude/settings.json:
  UserPromptSubmit -> mirror.py user       (appends Gonzalo's message)
  Stop             -> mirror.py assistant  (appends Claude's reply text)

Target note: path stored in Learning/.current-session (written by Claude at
session start). If that pointer is missing or not from today, falls back to
Learning/Sessions/YYYY-MM-DD session.md.

Never prints to stdout (UserPromptSubmit stdout would be injected into context)
and never fails loudly: mirroring is best-effort and must not block the session.
"""
import datetime as dt
import json
import os
import sys
import time


def project_dir():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def note_path(root):
    today = dt.date.today()
    ptr = os.path.join(root, "Learning", ".current-session")
    try:
        if dt.date.fromtimestamp(os.path.getmtime(ptr)) == today:
            rel = open(ptr, encoding="utf-8").read().strip()
            if rel:
                return rel if os.path.isabs(rel) else os.path.join(root, rel)
    except OSError:
        pass
    return os.path.join(root, "Learning", "Sessions", f"{today.isoformat()} session.md")


def append(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if new:
            f.write(f"# Session {dt.date.today().isoformat()}\n\n")
        f.write(text)


def is_real_user_entry(entry):
    """A user turn typed by Gonzalo (not a tool result / meta message)."""
    if entry.get("type") != "user" or entry.get("isMeta"):
        return False
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, str):
        return True
    if isinstance(content, list):
        return any(isinstance(b, dict) and b.get("type") == "text" for b in content) and not any(
            isinstance(b, dict) and b.get("type") == "tool_result" for b in content)
    return False


def last_assistant_text(transcript):
    try:
        with open(transcript, encoding="utf-8") as f:
            entries = []
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except OSError:
        return ""
    # walk back to the last real user prompt, collect assistant text after it
    start = 0
    for i in range(len(entries) - 1, -1, -1):
        if is_real_user_entry(entries[i]):
            start = i + 1
            break
    parts = []
    for e in entries[start:]:
        if e.get("type") != "assistant":
            continue
        content = (e.get("message") or {}).get("content")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            parts += [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
    return "\n\n".join(p.strip() for p in parts if p and p.strip())


def main():
    role = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    root = project_dir()
    stamp = dt.datetime.now().strftime("%H:%M")
    if role == "user":
        prompt = (data.get("prompt") or "").strip()
        if prompt:
            append(note_path(root), f"\n---\n#### 🧑 Gonzalo · {stamp}\n\n{prompt}\n\n")
    elif role == "assistant":
        tp = data.get("transcript_path")
        text = ""
        for _ in range(6):  # transcript may lag the Stop event slightly
            text = last_assistant_text(tp) if tp else ""
            if text:
                break
            time.sleep(0.5)
        if text:
            append(note_path(root), f"#### 🤖 Claude · {stamp}\n\n{text}\n\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
