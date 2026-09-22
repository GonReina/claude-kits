---
name: paper
description: Work through a scientific article actively — map its prerequisites, reconstruct its key derivations, audit its claims, and mine it for new ideas and experiments. Use whenever Gonzalo shares or names a paper (arXiv link, DOI, PDF in Library/, "this PRL on…"), says "let's read/go through this paper", "help me understand this article", "journal club", or "what could we do with this?". Especially relevant for quantum technologies, AMO and NV-centre / magnetometry work.
---

# Paper

Follow the shared conventions in `CLAUDE.md`. The goal isn't a summary. The goal is that Gonzalo could **reproduce the paper's core argument, judge its claims as a referee would, and propose the next experiment.** He does the reading and deriving; you steer, probe and audit.

Notes go in `Learning/Papers/<FirstAuthor Year>.md`.

## 1. Get it and triage (first pass)
- Get the PDF: from `Library/`, from arXiv, or via WebFetch of a DOI or link. Extract the text with `pdftotext` (with `-layout` for equations). If the text is garbled, ask him to put the PDF in `Library/`. Don't reconstruct a paper's content from memory.
- He reads the title, abstract, figures and conclusions, then states **in his own words**: the claim, the method, and why it matters. This is recall, so don't summarise it for him first. Then correct and sharpen his version.
- Classify the paper: new effect, new method or technique, better number, or theory proposal. The kind decides where the value lies and what to audit.

## 2. Prerequisite map
- List the concepts and techniques the paper relies on, and sort them into three groups: solid for him, rusty, and new. Use a quick probe in the style of the `teach` skill if unsure, and check `Learning/Topics/` for existing edge maps.
- Draw a small ```mermaid``` map: prerequisites → the paper's key steps → its main result.
- For a rusty or new prerequisite that the main result depends on, offer a short `teach` detour now, or add it as a known gap and continue. He decides.

## 3. Reconstruct the core (second pass: active)
- Identify the 1–3 **load-bearing** results: the central derivation, model or equation that everything else rests on.
- For each one, **predict before reading**: "Given their setup, what scaling do you expect for the sensitivity? What should limit it?" Then have him **derive it himself** from the paper's stated starting point, using the `problems` skill (hint ladder, line-by-line marking). Verify the paper's equations with sympy or numerics while he works. Papers contain typos and errors too. If you find one, say so and show the check.
- For each figure that carries the claim, have him say what the axes are, what the curve would look like if the claim were false, and whether the error bars support the conclusion.

## 4. Audit (referee mode)
Work through these with him; he answers first, then you add:
- **Assumptions ledger**: every assumption, approximation and regime, stated or unstated. For example: Markovian bath, RWA, low excitation, a particular temperature, shot-noise limit, ideal readout contrast. Note which ones are tested and which are just asserted.
- **Numbers**: re-derive the headline figure of merit from the paper's own parameters (sensitivity, fidelity, coherence time, SNR). Check orders of magnitude and units, and compare against known limits (standard quantum limit, spin-projection noise, photon shot noise) and against competing work. Find and verify competing figures; never recall them from memory.
- **Controls and alternatives**: what else could produce the same data? What control would rule it out?
- **What's missing**: the obvious experiment or parameter sweep they didn't show.

## 5. Ideas (third pass: the point of the exercise)
Push him to generate ideas first, then add your own, then stress-test all of them bluntly:
- **Relax an assumption** from the ledger. What happens, and is that regime interesting or accessible?
- **Change the platform**: port the method to NV centres or ODMR in his confocal setup, or port an NV technique into this system. What changes (contrast, $T_2$ vs $T_2^*$, readout, temperature, field range)?
- **Combine**: pair this with another technique he knows (for example, from his OPM or MEG background).
- **Push a limit**: what currently limits the headline number, and what would beat it?

For each idea that survives, write a short **feasibility sketch** in the notes: the key measurement, the expected signal against the noise floor (an order-of-magnitude estimate, verified with code), the hardware needed versus what he has, the main risk, and the first cheap test. Check for prior art with WebSearch before calling anything new, and report what you found honestly.

## 6. Close
- Notes file: his summary, prerequisite map, reconstructed derivations, assumptions ledger, audit findings, and idea log with feasibility sketches.
- Cards via `recall`: the load-bearing derivations, any prerequisite he fumbled, and one `concept` card per paper ("What is the key idea of [paper], and what limits it?").
- Link the paper note from the relevant `Learning/Topics/` files.
