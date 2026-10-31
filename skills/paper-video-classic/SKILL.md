---
name: paper-video-classic
description: Use when creating evidence-first classic paper videos.
metadata:
  version: "0.1.0"
---

# Paper Video Classic

Create a paper explainer with the real PDF as the main evidence surface. The classic visual language uses flat paper, progressive underlines/rings and source-linked teaching cards. It is not the brush/notebook workflow.

## Scope

Use for a selected paper or a requested subsection. A request for a pilot is not a full-film request; a full-film request is not satisfied by a short technical test. A discussion or script revision does not start paid generation. Publishing and account actions require separate authorization.

## Explain before animating

For deep paper reading, five-step cognitive path organization, benchmark walkthroughs, and visual storytelling scripts, pair this skill with [`limu-paper`](https://github.com/litaohz/limu-paper) (located at `skills/limu-paper/SKILL.md` when cloned with `--recurse-submodules`, or installed side-by-side in your agent's skill directory). When `limu-paper` is available, load it first to complete source verification and script structuring before scene authoring.

1. Confirm the paper's identity, version, authors and permitted source use. Read the relevant full sections, figures, experiment setup, metrics and limitations; abstracts alone are insufficient.
2. Plan a cognitive path: research problem, related approaches and gap, design rationale, mechanism, experiment and conclusion. Define important terms before using them. Examples should solve local difficulties, not replace the paper's argument.
3. Write a compact claim/evidence record. Distinguish author findings, reported experiments, teaching illustrations and editorial interpretation. Calculate differences with code. Never invent measurements or provenance.
4. Draft narration with meaningful transitions. If using two voices, give the questioner a real understanding gap to resolve; avoid mechanical alternation, praise and repeated answers.
5. Review factual support and cognitive continuity separately before speech synthesis. Keep production checks and 'we did not run this' comments in internal records, not in audience narration.

## Ground the scene

- Keep the source readable, in its original colors and aspect ratio, with enough context to identify the passage.
- Use `paper-video quote` to locate each unique phrase. Missing or ambiguous quotes must fail. Scanned pages need an actual OCR stage, not guessed coordinates.
- Bind annotations to the words being explained. Cross-line phrases receive per-line marks. Use a closed ring for a numerical cell or localized object when implemented in the authored scene.
- Let a teaching panel grow from the relevant source region; retain the source highlight while explaining. Clear the panel's text before collapsing it, to avoid residual labels over the PDF.
- Preserve parallel branches, feedback and training/inference boundaries. Optional externally authored mechanism clips must be genuinely rendered and clearly identified as teaching illustrations, never passed off as original figures.
- Keep one subtitle channel. Do not duplicate whole narration sentences as large explanation banners.

## Time and render

Use a real audio file and its provider-native word timestamps for narrated projects. Verify normalized text coverage, monotonic finite bounds, decoded PCM length and audio hash. Do not estimate speech timing from text length. The bundled silent fixture uses explicitly authored timings only because it has no narration.

Use deterministic `frame(t)` composition and freeze source, script, coordinate, timing and asset inputs. A changed voice or script invalidates dependent timings; a visual-only revision should preserve unchanged valid audio. Refuse output overwrite; use a new revision directory.

The runnable CLI in this repository is a small one-region classic compositor, not a finished automatic full-paper director. For a full video, author each section and concatenate verified clips. The optional Azure adapter is one supported provider example, not a mandatory cloud service.

## Verify and return

Check exact source matches, visibility and reading holds, native audio/caption/cue consistency, seek-order determinism, final dimensions/frame count and complete media decode. Inspect intermediate annotation/panel states in the encoded output. Report factual review, technical checks, listening and aesthetics with their actual scope; unperformed checks are NOT_CHECKED, never inferred PASS.

Return the video, editable inputs/code, captions where present, provenance and checks. Do not include credentials, personal schedules, private delivery targets, logs containing account data or unlicensed fonts/papers. Do not publish or send externally without current authorization.
