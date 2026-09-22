---
name: recall
description: Run active-recall review sessions (also invocable as /recall) with spaced repetition, and add or manage recall cards. Use whenever Gonzalo says "review", "recall", "quiz me", "what's due", "drill me on X", "flashcards", or at the start of a study session. Also use (silently, via the script) whenever another skill needs to add a card. All cards are free-response — he states, derives, computes or solves; Claude grades strictly and reschedules.
---

# Recall

Follow the shared conventions in `CLAUDE.md`. The deck lives in `Learning/Recall/deck.json` and is managed **only** through the script:

```
python .claude/skills/recall/scripts/srs.py <command> ...
```
Commands: `add`, `due`, `grade ID again|hard|good|easy [--note]`, `show ID`, `list`, `stats`, `edit`, `suspend`/`unsuspend`. Run `--help` for the options.

## Card kinds — what a good card asks

Cards ask him to **produce**, never to recognise. Each card tests one node or one skill, and the prompt must be answerable without its original context:

| kind | Prompt shape | Example |
|---|---|---|
| `definition` | State the precise definition | "Define a completely positive map." |
| `statement` | State a theorem or law *with its conditions* | "State the adiabatic theorem and its validity condition." |
| `derivation` | Derive a result from named starting points | "From $H = \frac{\hbar\Omega}{2}\sigma_x + \frac{\hbar\Delta}{2}\sigma_z$, derive the generalised Rabi frequency." |
| `problem` | A full problem (from a book, paper or exam) to redo | "Griffiths 4.xx — (full statement)". Always include the full statement. |
| `redo` | A problem he saw the solution to; redo it cold | Scheduled with `--delay 3` |
| `misconception` | A question that his specific wrong belief would get wrong | "Does a $\pi$ pulse on an ensemble with inhomogeneous detuning give full inversion? Why?" |
| `concept` | A why or when question | "Why does the RWA fail in the ultrastrong-coupling regime? What's the first observable correction?" |

The `--answer` field holds a concise model answer, or a pointer to where the verified full answer lives (for example, a session note heading). Write the prompt in LaTeX. Keep `--topic` hierarchical and consistent, such as `QM/angular-momentum` or `AMO/two-level`. Use `list` to reuse existing topic names.

Before adding any card, make sure the answer is verified (see `CLAUDE.md`). A wrong card rehearses an error.

## Running a review session

1. **Warm-up.** Run `stats` and `due`. Tell him how many cards are due and the topics with the most lapses. If more than about 25 are due, prioritise the most overdue, then the `misconception` and `redo` kinds, and ask whether he wants the full queue.
2. **One card at a time.** Show the prompt only, in your reply. He answers in LaTeX. **Don't show the answer field first**, and don't hint during a recall attempt. If he's blank, that's `again`.
3. **Mark strictly.** Use the `problems` skill's Stage 2 line-by-line rules for derivations and problems. Recall is a test, so skip Stage 1, but give him one chance to spot his own error before you reveal it. For statements and definitions, missing conditions or quantifiers count as errors. Check against the answer field *and* your own verified knowledge. If the stored answer turns out to be wrong or sloppy, fix the card with `edit` and tell him.
4. **Grade and reschedule.** You propose the grade and he can overrule it:
   - `again`: wrong, blank, or right only after a hint
   - `hard`: right, but slow, or with a notation or hand-wave issue you had to flag
   - `good`: right and clean
   - `easy`: right, clean, fast, and he could explain the "why"

   Run `grade ID <grade> --note "<what went wrong, if anything>"`.
5. **Vary, don't repeat.** An identical question served many times turns recall into recognition. For `problem`, `redo` and `derivation` cards whose reps are 2 or more, serve a **variant**: changed parameters, a changed geometry, the inverse question, or the same idea in another system. Verify each variant before serving it. Grade the card on the variant.
6. **Interleave.** Don't serve ten cards from one topic in a row if you can avoid it. Mixing topics makes retrieval harder, and harder retrieval makes memory stronger.
   When physics cards rest on maths that has been failing (linear algebra, ODEs, Fourier methods, complex analysis, probability, vector calculus), mix in a relevant maths card. Treat the maths as a live prerequisite, not a separate subject. Don't add random review for its own sake.
7. **Keep going until he stops.** When he's invoked `/recall`, drop new material and keep serving cards until he says "stop", "end recall", or the queue is empty.
8. **Close.** Give a tally by grade. For any card at 4 or more lapses (a *leech*), stop drilling it. The underlying node isn't understood, so offer to go through it with `teach` and suspend the card until then. Include the summary in your reply.

## Other recall modes
- **"Quiz me on X"** (not from the deck): generate 5–10 fresh free-response prompts on X, escalating in difficulty like the `teach` probe. Mix in the check types (state, predict, derive, compute, explain, sanity). Anything he misses becomes a card.
- **Blank-page recall**: "Write everything you know about $X$ without looking: definitions, key results, how they connect." Then compare it with the topic's dependency map in `Learning/Topics/`. Missing nodes and missing edges become cards.
- **Rapid-fire**: short questions with 30-second answers (orders of magnitude, constants, selection rules, standard commutators). The goal is fluency. Only misses become cards.
