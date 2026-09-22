---
name: exam
description: Run a timed, exam-conditions attempt at a past paper (or a single past-paper question, or a mock paper) and then mark it. Use whenever Gonzalo says "exam mode", "timed", "mock exam", "past paper", "let's do the 2019 QM paper", or gives a link or PDF of a university exam. Fetches the paper, enforces the time limit and silence, then marks against the official scheme or a verified one, line by line.
---

# Exam

Follow the shared conventions in `CLAUDE.md`. The point of exam mode is **retrieval under pressure with no help**. So during the attempt, Claude says nothing useful.

## 1. Get the paper
- Look for it in `Library/` first. If he gives a URL, fetch it with WebFetch or `curl`, and save it to `Library/Exams/` (PDF plus a `pdftotext` copy). If there's no URL, search university sites with WebSearch. Only use papers that are publicly posted, and ask before downloading.
- Look for an official **mark scheme or solutions** too. If none exists, you'll build a scheme yourself (see step 3). Tell him which case applies before he starts.
- Check the paper covers what he wants. If it's a whole paper, ask which questions and the time limit. Otherwise, derive the limit from the paper's rubric, or scale it: minutes per mark, from the rubric.

## 2. The attempt
- Put the questions (verbatim, in LaTeX) into `Learning/Exams/<institution> <course> <year>.md`. **Start the clock**: record `date -Iseconds` via Bash and write the start time and deadline into the note.
- Then tell him: "Clock started. Deadline HH:MM. Write your answers under each question in the note, or paste them here. Say `done` when finished."
- **During the attempt, give no hints, no marking, and no confirmation.** If he asks a question, answer only clarifications of the question wording, as an invigilator would. Everything else gets: "Exam conditions. Noted for after." Log what he asked; it's diagnostic.
- If he asks for the time, run `date` and report how much is left.
- When he says `done`, or on his first message after the deadline, record the finish time. **Answers written after the deadline are marked separately**, as "overtime": they show knowledge, but not exam performance.

## 3. Marking
- **Build or confirm the scheme first.** With an official scheme, use it. Without one, solve each question, verify with sympy or numerics, and get an independent blind solve from the `verifier` subagent. Then write a scheme in the style of the paper, with method marks and answer marks.
- **Optional correction pass first.** Before revealing marks, offer Stage 1 of the `problems` marking: flag the locations of errors only, and let him fix them untimed. This doesn't change the exam score, but it separates what he can self-correct from what he genuinely doesn't know. Record both.
- Mark each question line by line using the Stage 2 rules in the `problems` skill (✓ / ✗[type] / ⚠[notation] / ⚠[hand-wave]), then award marks against the scheme. Be as strict as a real examiner. No partial credit for a right answer from wrong working.
- **Report**:
  - A table of each question's marks, total, and percentage, with in-time and overtime shown separately.
  - Time spent per question if he noted it, and where time was wasted.
  - Error-type tally, compared with the history in `Learning/Mistakes.md`.
  - The 2–3 highest-leverage fixes, whether topic gaps or habits (for example, "you lose most marks by skipping the limiting-case check, not on physics").
- Then offer, for each dropped question: re-attempt it cold now (hints allowed via `problems`), or schedule it.

## 4. Afterwards
- Every question with less than full marks becomes a recall card whose prompt is the full question. Every ✗ `concept` error becomes a card on the underlying node.
- Append the result line to `Learning/Exams/_log.md` (date, paper, score, time, main weaknesses) so progress is visible over time.
