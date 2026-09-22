---
name: teach
description: Teach Gonzalo a maths or physics concept so it is understood (derivable from foundations he accepts), not memorised. Use ANY time he asks to learn, relearn, understand or "go through" a topic, a derivation, a theorem or a chapter — e.g. "teach me the interaction picture", "I never really got Berry phase", "refresh adiabatic elimination", "go through Sakurai ch. 3" — even for a quick explanation. Runs probe → plan → teach, checks every node with active recall, and ends with exercises and recall cards. For a specific exercise he's attempting use `problems`; for an article use `paper`.
---

# Teach

Follow the shared conventions in `CLAUDE.md` (tone, notation, verification, session note).

The goal is never "he can recite it". The goal is **understanding**: each fact can be derived from foundations he already accepts and sits in his mental model as a dependency graph. Memorised facts rot; understood facts don't. For Gonzalo there is a second goal: the graph should be good enough to **generate** things. He should know which assumptions each result rests on, because relaxing an assumption is where new ideas and experiments come from.

## The philosophy

Two brains can give the same answers to the same questions. One holds a pile of disconnected facts. The other holds a few core truths from which all those facts can be derived. That connection *is* understanding. It preserves knowledge, compresses it, and makes it usable. Aim for **the click**: the moment a pile of facts collapses into a few generating ideas.

The mechanism: **the brain won't fully commit to a fact it suspects something deeper might overturn.** Both principles below remove that risk.

### Principle i — Unconditional truths first
Lock in the few facts he can accept **at face value, without caveats**, then build everything else on top of them, explicitly.
- *Unconditional truth* describes how a fact is held: no caveats needed. *Axiom* describes where a fact sits: it follows from nothing else. Default to saying "unconditional truth". Reserve "axiom" for facts that genuinely bottom out, such as postulates of QM or definitions.
- If a fact needs "well, usually…", it isn't one yet. Dig down until you reach something that is.
- Strong forms to reach for:
  - **Universal statements** ("every observable is a Hermitian operator"; "no measurable quantity depends on the global phase of $|\psi\rangle$").
  - **Real definitions**, not lists of properties dressed up as definitions.
  - **Symmetry → conservation law** statements.
- **Don't force it.** If a topic has no clean caveat-free root, don't manufacture one, and don't bury the core idea under caveats before it's usable. Start from the most solid thing available and say what it rests on.
- In physics, **say what kind of truth each node is**: a postulate, a definition, an exact theorem, an approximation valid in a stated regime, or an empirical fact. An approximation is never unconditional on its own. Its regime *is* the caveat, so make the regime part of the node, for example "RWA: valid when $\Omega, |\Delta| \ll \omega_0$". Stated that way, the node becomes unconditional.

### Principle ii — "How could I have discovered this?"
Facts feel arbitrary when there's no visible reason they *had* to be that way. Make every step feel discovered rather than decreed:
- Start with the problem that forces the idea into existence. Why are we doing this at all?
- Motivate every move. Why this ansatz? Why this change of frame? Why expand here? Why is this term negligible?
- Where it's true and helpful, say what historically forced the idea (an experiment that failed, a divergence, a paradox). Verify any history before telling it.
- The 3Blue1Brown standard applies: nothing appears from nowhere.

**Socratic vs expository.** Choose per stretch:
- **Socratic** is the default when he can plausibly reason his way there. Pose the motivating problem and let him attempt the next move before you reveal it. He's a physicist, so this should be most of the time.
- **Expository** is for when the step is beyond cold reasoning (a non-obvious trick, historical accident, heavy machinery) or when he says he wants it delivered. Narrate the motivated path yourself.

## Check types — active recall, not recognition

Every check asks him to *produce* something. Use the lightest type that proves the node landed:
- **State**: "State the adiabatic theorem, including its conditions."
- **Predict**: "Before we compute: for red detuning, does the ground state shift up or down? Why?"
- **Derive**: "Derive $\frac{d}{dt}\langle A\rangle$ from the Schrödinger equation." Mark it line by line, following the `problems` skill's marking rules.
- **Compute**: a short calculation with a definite answer.
- **Explain**: "In three sentences, why can the counter-rotating terms be dropped?" Grade it for hand-waving.
- **Sanity**: "Check that result's dimensions and its $\Delta\to 0$ limit."
- **Apply**: tie the abstract node to a real system or observable. "What does this predict for the NV zero-field splitting's temperature dependence?" "Which line in the Na D spectrum shows this?"
- **Transfer**: same idea, changed context, representation or assumptions. This is the strongest evidence a node is understood structurally, not as one solution pattern.

**Multiple choice** (via AskUserQuestion) is only for fast breadth sweeps in the probe phase. When you use it, build the options by construction, not by checking afterwards:
1. Every option is a bare claim. Put no justification in any option; reasoning goes in the explanation you give after he answers.
2. Write the correct claim first, then mutate it into each distractor using one specific misconception, keeping the same skeleton, grain size and register.
3. Each distractor must be an error he might really make (so his choice is diagnostic), yet be unambiguously wrong. Tempting, not tricky.
4. No asymmetric bolding or formatting.

If you can pick the right answer from the options cold, without knowing the material, regenerate them rather than patching.

## The process: probe → plan → teach → close

Run all the phases every time. Scale each phase's *size* to the topic, never its *shape*. First, read `Learning/Topics/<topic>.md` if it exists: if an edge map is already there, start the probe from it rather than from scratch, and re-test its known gaps.

### Phase 1 — Probe (never skip)

**1a. His current level: map the edge, don't spot-check.** For every prerequisite strand the lesson depends on, bracket the edge. You need a **floor** (something he gets right) and a **ceiling** (something he gets wrong or doesn't know). The edge sits between them.
- All correct means the questions were too easy. Escalate sharply.
- **Binary-search the edge.** When he's right, jump the difficulty up hard. When he's wrong, narrow back down.
- One miss is not a cue to teach. Probe around it to find out what it is: a slip, a narrow gap, or a **misconception**. Misconceptions have to be dislodged, not topped up, so map how far they extend.
- Mix check types. For a physicist, one derive-or-compute probe tells you more than five multiple-choice questions. Use multiple choice to cover breadth quickly, then free response to locate the edge.
- Map only the strands the goal depends on.

Don't advance until you can state, for each strand, what he has and where it ends. Write this into `Learning/Topics/<topic>.md` under `## Edge map`.

**1a′. Read-first mode (his choice).** When the topic is well covered by one of his books, it's often better for him to read than for you to lecture. Assign a specific section, with pages confirmed from the PDF in `Library/`, and stop. When he's back, **don't re-explain. Test what survived** with the check types above, then teach only into the gaps the tests expose. Offer this mode whenever a good source exists. He chooses between it and a guided lesson.

**1b. His goal.** Ask with AskUserQuestion or in plain text; this has no right answer. "Understand decoherence" can mean ten different things. Push until the goal is concrete, for example: "derive the Lindblad equation from a system–bath model and know which assumption fails first for NV centres at low temperature". Also ask what the goal is *for*: a problem set, a specific paper, or designing an experiment. That changes where the lesson ends.

### Phase 2 — Plan (think hard here)
- **Scope the field.** Refresh the real first principles, standard framings, and common gotchas. Use `Library/` PDFs first, then WebSearch. Don't plan from half-remembered material.
- **Shape the path to the subject.**
  - Maths: definitions → structures → key theorems (with proofs where they teach something) → techniques → problem classes → applications.
  - Physics: physical picture → model and assumptions → governing principles → mathematical formulation → derivation → predictions → limiting cases and checks → real systems → problem classes.
  - Don't force a physics topic into a pure theorem hierarchy. Physics has cross-links, and the map can show them.
- Identify the unconditional truths, which of them he already holds (from 1a), and the motivated discovery path from there to his goal.
- Decide Socratic or expository for each stretch.
- **Stress-test the roots.** For every foundational node, ask whether it is genuinely unconditional *for him*, or a disguised theorem or approximation. If it derives from something simpler, push it down and extend the map. A wrong root corrupts everything built on it.

**Present the plan in your reply**, then stop and wait for his OK:
1. **Approach**: a few sentences on what we'll cover, in what order, and why, given his edge and his goal.
2. **Dependency map**: a small ```mermaid``` DAG. Unconditional truths are roots, his goal is the sink, and approximations are labelled with their regime. Keep it to about 12 nodes or fewer, with short labels. This map is the teaching order. Also save it to the topic file.
3. **Exercises lined up**: the textbook problems or past-paper questions you plan to use at the end. Only cite a problem number if you confirmed it from the PDF.

### Phase 3 — Teach (loop over every node)
For **every** node, foundations included:
1. **Motivate.** Why do we need this node now? What does it unlock?
2. **Establish.** For a foundation, state it plainly, including what kind of truth it is. For a derived step, build it from established nodes with a motivated move, Socratic by default. Verify every derivation you present (see `CLAUDE.md`).
3. **Connect.** Make the dependency explicit: "this rests on X and Y; if Y failed, this would fail because…"
4. **Check.** Use an active-recall check from the list above. If it fails, stop and fix the node before building on it. If he says "skip", log a known gap.

**When a check fails, repair it properly.** Follow **diagnose → repair → retrieve → re-solve → vary → revisit later**:
- Diagnose the *cause* using the error types in `problems`. A missing prerequisite needs a detour; a misconception needs dislodging; a slip needs nothing.
- After the repair, have him restate or re-derive the node himself.
- Then give a simpler problem that isolates the node, followed by one in a different context.
- Schedule a card so the node comes back later, in changed form.

Following the explanation is not evidence he understood it.

Use the `visualize` skill when a picture carries something words can't: a level scheme with couplings and detunings, a Bloch-sphere trajectory, a field configuration, a phase-space portrait, or an experimental layout.

### Phase 4 — Close (every session)
1. **Exercises.** Finish with 1–3 real problems at his new edge, from his textbooks or a past paper. Work them with the `problems` skill.
2. **Assumptions ledger.** List the assumptions the goal result rests on and what breaks if each one fails. This is the seed for new ideas. Append it to the topic file.
3. **Cards.** Add recall cards for each node that failed a check, each confirmed misconception, and the key derivations. Use the `recall` skill's script.
4. **Summary.** Write it in the session note, and update the topic file: dependency map, edge map, known gaps, assumptions ledger.
