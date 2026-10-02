# Release checklist

## Verified locally

- [x] Editable Python install.
- [x] Credential-free 24-second, 1920x1080/24fps silent demo: 576 real encoded frames and complete decode.
- [x] Actual Azure optional-adapter call: 50 native word boundaries; 23.5-second narrated render, 564 frames, complete decode. The generated audio is not included in the source release.
- [x] Nine regression tests: exact and ambiguous PDF searches, out-of-crop failures, seek-order consistency, visible annotation pixels, overwrite protection, audio-hash mismatch and portable config.
- [x] Portable original demo PDF instead of a redistributed third-party research paper.
- [x] No PyMuPDF dependency and no copied Windows font/cursor files.

## Release scope

- [x] Owner and repository confirmed: `litaohz/paper-video-classic`.
- [x] MIT licensing and public author display name confirmed: Thomas Li.
- [x] Original candidate archive passed source/privacy/dependency checks and a clean unpacked-example test; only README publication links and this checklist were then updated. Runtime code and demonstration media are unchanged.
- [x] Publication scope is the standalone Classic files only, with fresh Git history. Private production files, memories and the newer brush/notebook implementation are excluded.
- [ ] Independent aesthetic review of the demo: not claimed by the automated checks.

Validated on Windows with Python 3.12. The clean virtual environment had no system site packages and reproduced the same silent-demo video hash. Local technical tests do not imply cross-platform acceptance, full-paper factual review, or user aesthetic approval. The repository's commit and release records are the authority for publication state.

## Deliberate limits

One PDF region per reference render; no bundled OCR, automatic paper comprehension, full Manim scene generator, publishing bot or scheduling service. The general workflow supports authoring multiple clips, but that is separate from the included small runnable compositor.
