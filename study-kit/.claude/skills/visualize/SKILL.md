---
name: visualize
description: Add one correct, minimal figure to a study session — either a concept dependency map (Mermaid, rendered natively by Obsidian) or a physical diagram/plot (level schemes, Bloch-sphere trajectories, field lines, vectors, pulse sequences, energy curves, experimental layouts, function plots) made and visually verified by the `diagram-maker` subagent. Use when an idea is genuinely clearer as a picture, when `teach`/`paper` needs a dependency map, or when Gonzalo asks to "draw", "sketch", "plot" or "show" something.
---

# Visualize

A figure earns its place only when it shows something words can't: structure, direction, geometry, scale, or time ordering. **A wrong figure is worse than no figure**, because pictures get memorised uncritically. When in doubt, don't draw.

You are the creative director. You decide the single idea and cut it down to the fewest elements that carry it. The picture is made in one of two ways.

## Route A — Dependency maps and concept structure → inline Mermaid

Obsidian renders ```mermaid``` blocks natively, so put them directly in your reply (the hook mirrors it to the note) or in the topic file. No subagent is needed.
- **Direction**: use `graph TD` or `graph BT`. Roots are the unconditional truths (postulates, definitions); arrows point from what a node depends on to what it enables; the goal is the sink.
- **Node types**: mark them with shapes, used consistently:
  - `([...])` for a postulate or definition
  - `[...]` for an exact result
  - `{{...}}` for an approximation. Put its regime in the label, for example `{{"RWA: Ω,|Δ| ≪ ω₀"}}`.
  - `((...))` for the goal
- **Colour nodes by mastery** (from the topic file) so the map doubles as a progress view. Paste this at the end of the block:
  ```
  classDef solid fill:#c8e6c9,stroke:#2e7d32;
  classDef shaky fill:#fff3c4,stroke:#b8860b;
  classDef gap fill:#ffcdd2,stroke:#c62828;
  classDef unseen fill:#eeeeee,stroke:#9e9e9e;
  ```
  Then assign nodes with `class A,B solid;`:
  - `solid` = retrieves unaided or better
  - `shaky` = studied, or explains with support
  - `gap` = a known gap or misconception
  - `unseen` = not met yet
- **Don't restructure for looks.** The dependency structure comes from the `teach` plan or the paper's prerequisite map. The picture must show that structure, not a prettier one.
- Keep labels short and use at most about 12 nodes. Mermaid labels don't render LaTeX reliably, so use Unicode (Ω, Δ, ħ, ≪, ⟨ψ|) and quote any label containing special characters.
- **Validate the syntax** before writing it into the note, if mermaid-cli is available: `npx -y @mermaid-js/mermaid-cli -i map.mmd -o /tmp/map.png`, then view the PNG. If it isn't available, re-read the source carefully: balanced brackets, quoted labels, no stray parentheses inside unquoted labels.
- Other structural visuals also go this route: flowcharts of a procedure (for example, a Ramsey or Hahn-echo sequence as steps), state machines, timelines, and trees.

## Route B — Physical diagrams and plots → `diagram-maker` subagent

Anything with positions, shapes, scales or data: level schemes with couplings and detunings, Bloch-sphere rotations, pulse-sequence timing diagrams, field lines, vector geometry, potential curves, dispersion or resonance lineshapes, ODMR spectra vs field, confocal or optical layouts, and plots of any function.

**Write a tight brief**: one idea, fewest elements, concrete. The maker needs the physics pinned down, because it will draw exactly what you say.
- BAD: "draw a Λ system"
- GOOD: "Level scheme, three levels: $|g_1\rangle$ and $|g_2\rangle$ at the bottom, split by $\omega_{12}$ with $|g_2\rangle$ higher; $|e\rangle$ at the top. Two upward arrows: $\Omega_p$ from $|g_1\rangle$ and $\Omega_c$ from $|g_2\rangle$, both ending at a dashed virtual level $\Delta$ below $|e\rangle$ (convention $\Delta = \omega_L - \omega_0 < 0$ drawn as red-detuned). Label $\Delta$ with a double arrow. Not to scale; say so in a corner note. No title."

**One idea per figure.** If two learning points would compete, make two figures.

**Always put in the brief**: the model (point particle vs extended body, and therefore where forces attach), the sign conventions, the units and axis labels, whether it's to scale, the parameter values for any plot, and what the figure must make obvious. For plots of equations, give the exact expression and parameter values you've verified. The maker plots what it's given; it doesn't derive the physics.

Dispatch it:
```
Task(subagent_type="diagram-maker", prompt="<brief>")
```
It returns:
```
RESULT:
filename: viz-<slug>-<timestamp>.png
path: viz/viz-<slug>-<timestamp>.png
```
or `RESULT: NONE` with a reason. In that case simplify the brief, or decide the figure isn't worth it. Never hand-draw a figure yourself that skips the maker's render-and-inspect loop.

## Embedding

Put the figure in your reply with Obsidian's embed syntax, using the filename only and a display width:
```
![[viz-<slug>-<timestamp>.png|500]]
```
Use a larger width for dense figures. Introduce the figure in one sentence, then let it carry the idea.

**Use figures for active recall too.** Figures are for prediction, not redrawing (he types in a terminal). Follow **structure → predict → reveal**:
- Ask before showing: "As $B_z$ increases from zero, how do the $m_s=\pm1$ lines move in the ODMR spectrum? Linear or not? What happens near 102 mT?" He answers in words or LaTeX. Then show the verified plot.
- Or show the structure and ask: show a level scheme and ask which transitions are allowed; show a potential and ask where the particle speeds up.
