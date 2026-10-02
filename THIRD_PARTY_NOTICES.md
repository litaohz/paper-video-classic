# Third-party notices and publication boundaries

The MIT license covers this repository's original code, documentation and authored demo fixture. It does not relicense third-party dependencies, voices, papers, fonts, screenshots or FFmpeg distributions.

- **Pillow 11.3.0**: the HPND/PIL software license and its bundled font notices apply. Dependencies are installed separately; their package notices remain with them.
- **pypdfium2 5.5.0**: its metadata identifies BSD-3-Clause, Apache-2.0 and dependency licenses; PDFium and its binary builds carry additional notices. Refer to the installed package's `licenses/` and upstream [licensing documentation](https://github.com/pypdfium2-team/pypdfium2). Do not strip these notices when redistributing binaries.
- **FFmpeg**: separately installed, not bundled. Licensing depends on the selected build and codecs. The tested command uses a system FFmpeg with libx264; do not describe every FFmpeg distribution as permissively licensed.
- **Microsoft Cognitive Services Speech SDK**: optional adapter dependency, installed separately under its upstream license. Azure services and generated audio remain subject to their service terms; the MIT code license does not grant subscription access or any voice-cloning rights.

The private classic production setup used PyMuPDF and Windows fonts/cursor assets. This public adaptation does **not** import or bundle PyMuPDF, Windows fonts or native cursor files. PDF extraction/rendering uses PDFium; the English demo uses Pillow's bundled default font and an original point marker. Supply a properly licensed font to render other scripts.

No third-party research paper is included. The generated sample PDF is explicitly labelled a demonstration fixture and makes no scientific claims. When using actual papers, retain their original identity and observe their redistribution license. Public availability is not itself a redistribution license.

This is a release candidate, not a legal opinion or certification. Before publishing, confirm the author/repository identity and any additional assets you choose to add. Do not place credentials, internal recipient IDs, historical account screenshots or private project paths in the public repository.
