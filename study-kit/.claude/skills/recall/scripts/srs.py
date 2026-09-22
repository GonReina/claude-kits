#!/usr/bin/env python3
"""Minimal spaced-repetition deck for free-response maths/physics recall.

Deck lives in Learning/Recall/deck.json (override with --deck).
Scheduling is a simplified SM-2: grades again/hard/good/easy.

Usage:
  srs.py add --topic T --kind K --prompt P --answer A [--source S] [--delay DAYS]
  srs.py due [--topic T] [--limit N] [--date YYYY-MM-DD]
  srs.py grade ID {again,hard,good,easy} [--note TEXT]
  srs.py show ID
  srs.py list [--topic T] [--kind K]
  srs.py stats
  srs.py edit ID [--prompt P] [--answer A] [--topic T] [--kind K] [--source S]
  srs.py suspend ID | unsuspend ID

kind: definition | statement | derivation | problem | misconception | redo | concept
"""
import argparse
import datetime as dt
import json
import os
import sys
import tempfile

DEFAULT_DECK = os.path.join("Learning", "Recall", "deck.json")
KINDS = ["definition", "statement", "derivation", "problem", "misconception", "redo", "concept"]
GRADES = ["again", "hard", "good", "easy"]


def today():
    return dt.date.today()


def load(path):
    if not os.path.exists(path):
        return {"next_id": 1, "cards": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, deck):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def find(deck, cid):
    for c in deck["cards"]:
        if c["id"] == cid:
            return c
    sys.exit(f"No card with id {cid}")


def schedule(card, grade, on):
    ease = card["ease"]
    interval = card["interval"]
    reps = card["reps"]
    if grade == "again":
        card["lapses"] += 1
        reps = 0
        interval = 1
        ease = max(1.3, ease - 0.2)
    elif grade == "hard":
        interval = max(1.0, interval * 1.2) if reps > 0 else 1
        ease = max(1.3, ease - 0.15)
        reps += 1
    elif grade == "good":
        interval = 1 if reps == 0 else (3 if reps == 1 else interval * ease)
        reps += 1
    elif grade == "easy":
        interval = 3 if reps == 0 else max(4.0, interval * ease * 1.3)
        ease += 0.15
        reps += 1
    card["ease"] = round(ease, 3)
    card["interval"] = round(float(interval), 2)
    card["reps"] = reps
    card["due"] = (on + dt.timedelta(days=max(1, round(interval)))).isoformat()


def fmt(c, full=False):
    head = f"[#{c['id']}] ({c['kind']}, {c['topic']}) due {c['due']}"
    if c.get("suspended"):
        head += " SUSPENDED"
    lines = [head, f"  Prompt: {c['prompt']}"]
    if full:
        lines.append(f"  Answer/ref: {c['answer']}")
        if c.get("source"):
            lines.append(f"  Source: {c['source']}")
        lines.append(f"  reps={c['reps']} lapses={c['lapses']} interval={c['interval']}d ease={c['ease']}")
        for h in c.get("history", [])[-5:]:
            lines.append(f"    {h['date']}: {h['grade']}" + (f" — {h['note']}" if h.get("note") else ""))
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--deck", default=DEFAULT_DECK)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--topic", required=True)
    a.add_argument("--kind", required=True, choices=KINDS)
    a.add_argument("--prompt", required=True)
    a.add_argument("--answer", required=True, help="model answer or reference to where it lives")
    a.add_argument("--source", default="")
    a.add_argument("--delay", type=int, default=1, help="days until first review")

    d = sub.add_parser("due")
    d.add_argument("--topic")
    d.add_argument("--limit", type=int, default=20)
    d.add_argument("--date")

    g = sub.add_parser("grade")
    g.add_argument("id", type=int)
    g.add_argument("grade", choices=GRADES)
    g.add_argument("--note", default="")

    s = sub.add_parser("show")
    s.add_argument("id", type=int)

    l = sub.add_parser("list")
    l.add_argument("--topic")
    l.add_argument("--kind", choices=KINDS)

    sub.add_parser("stats")

    e = sub.add_parser("edit")
    e.add_argument("id", type=int)
    for f in ["prompt", "answer", "topic", "source"]:
        e.add_argument(f"--{f}")
    e.add_argument("--kind", choices=KINDS)

    for name in ["suspend", "unsuspend"]:
        x = sub.add_parser(name)
        x.add_argument("id", type=int)

    args = p.parse_args()
    deck = load(args.deck)

    if args.cmd == "add":
        cid = deck["next_id"]
        card = {
            "id": cid, "topic": args.topic, "kind": args.kind, "prompt": args.prompt,
            "answer": args.answer, "source": args.source, "created": today().isoformat(),
            "due": (today() + dt.timedelta(days=max(0, args.delay))).isoformat(),
            "interval": 0, "ease": 2.5, "reps": 0, "lapses": 0, "history": [], "suspended": False,
        }
        deck["cards"].append(card)
        deck["next_id"] = cid + 1
        save(args.deck, deck)
        print(f"Added card #{cid}, first review {card['due']}")

    elif args.cmd == "due":
        on = dt.date.fromisoformat(args.date) if args.date else today()
        cards = [c for c in deck["cards"] if not c.get("suspended")
                 and dt.date.fromisoformat(c["due"]) <= on
                 and (not args.topic or c["topic"] == args.topic)]
        # most overdue first, then most lapses
        cards.sort(key=lambda c: (c["due"], -c["lapses"]))
        print(f"{len(cards)} card(s) due on {on.isoformat()}" + (f" (showing {args.limit})" if len(cards) > args.limit else ""))
        for c in cards[: args.limit]:
            print(fmt(c))

    elif args.cmd == "grade":
        c = find(deck, args.id)
        schedule(c, args.grade, today())
        c.setdefault("history", []).append({"date": today().isoformat(), "grade": args.grade, "note": args.note})
        save(args.deck, deck)
        print(f"#{c['id']} graded {args.grade}; next due {c['due']} (interval {c['interval']}d)")

    elif args.cmd == "show":
        print(fmt(find(deck, args.id), full=True))

    elif args.cmd == "list":
        for c in deck["cards"]:
            if (not args.topic or c["topic"] == args.topic) and (not args.kind or c["kind"] == args.kind):
                print(fmt(c))

    elif args.cmd == "stats":
        cards = deck["cards"]
        on = today()
        due = sum(1 for c in cards if not c.get("suspended") and dt.date.fromisoformat(c["due"]) <= on)
        print(f"Cards: {len(cards)}  due today: {due}")
        topics = {}
        for c in cards:
            t = topics.setdefault(c["topic"], {"n": 0, "lapses": 0})
            t["n"] += 1
            t["lapses"] += c["lapses"]
        for t, v in sorted(topics.items(), key=lambda kv: -kv[1]["lapses"]):
            print(f"  {t}: {v['n']} cards, {v['lapses']} lapses")
        leeches = [c for c in cards if c["lapses"] >= 4]
        if leeches:
            print("Leeches (>=4 lapses) — reteach the underlying node:")
            for c in leeches:
                print("  " + fmt(c).splitlines()[0])

    elif args.cmd == "edit":
        c = find(deck, args.id)
        for f in ["prompt", "answer", "topic", "source", "kind"]:
            v = getattr(args, f)
            if v is not None:
                c[f] = v
        save(args.deck, deck)
        print(fmt(c, full=True))

    elif args.cmd in ("suspend", "unsuspend"):
        c = find(deck, args.id)
        c["suspended"] = args.cmd == "suspend"
        save(args.deck, deck)
        print(f"#{c['id']} {'suspended' if c['suspended'] else 'unsuspended'}")


if __name__ == "__main__":
    main()
