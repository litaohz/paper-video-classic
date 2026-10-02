# Pipeline and input contract

## Files

A section's `config.json` contains `pdf` (relative path), one-based `page`, top-left PDF-point `crop`, `title`, `source_label`, and `marks`. Each mark has a unique `id`, an exact `quote`, `cue_phrase`, `caption`, `note_title`, `note` and three compact teaching `nodes`.

The source image is rendered from the actual PDF region. Quote matching supplies rectangles; no default rectangle is used on failure. Search must match exactly one location and the crop must contain all lines. PDFium calls are serial: its APIs are not thread-safe. Use separate processes rather than concurrent threads if extending source preprocessing.

## Silent preview versus speech

The bundled fixture has `timing_source: authored_silent_demo` with explicit `duration` and `cue` values. This is an editorial animation preview with no speech. Do not relabel such numbers as native speech alignment.

A real narration requires a native manifest:

```json
{
  "provider": "your-provider",
  "text": "exact spoken script",
  "audio": "speech.wav",
  "audio_sha256": "actual sha256",
  "words": [{"word": "exact token", "startTime": 0.0, "endTime": 0.2}]
}
```

The example above documents a schema, not observed service output. Offsets are in seconds, relative to the actual audio. Use mono 16-bit PCM WAV. The renderer checks the hash, normalized transcript coverage, finite monotonic bounds and exact cue phrases, then rebuilds captions and highlight times. It uses the entire native span for a multi-character token, not made-up per-character timing.

## Azure adapter (optional paid call)

Install dependencies in `adapters/azure` with `npm ci`. Set `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` in your shell or secret manager. Optionally set `AZURE_SPEECH_VOICE` and `AZURE_SPEECH_LANGUAGE`; defaults are en-US-JennyNeural and en-US. Never put real credentials in a public config or commit a .env.

```bash
node adapters/azure/synthesize.cjs out/demo/input/config.json out/speech
python -m paper_video.cli render --config out/demo/input/config.json --native out/speech/speech.json --out out/narrated
```

This adapter calls the provider once when explicitly invoked, writes genuine WordBoundary events and the returned WAV, and refuses to overwrite an existing directory. It has no automatic retries or hidden synthesis in `demo`.

## Capabilities and limits

The executable reference compositor covers a readable PDF region, per-line underlines, source-connected teaching cards, one subtitle channel, deterministic CPU rendering, optional native-timed speech, and basic media verification. It deliberately does not provide automated full-paper reasoning, OCR, generalized table extraction, Manim scene generation, platform publishing or cloud scheduling.

The classic agent skill describes how to author richer scenes, figures/rings and mechanism clips. Those require actual per-paper authoring; they are not claimed as hidden CLI features. Preserve conditionals, parallelism and evidence limits when implementing them.

## Revisions and checks

Create a new output directory for every render. Validate source identity, licensing, claim support and cognitive flow before synthesis. Changing text or voice requires fresh boundaries; changing visuals does not require resynthesizing unchanged speech.

Every successful render produces `grounding.json`, `timeline.json`, `verification.json`, complete decode logs and annotation frames extracted from the encoded video. The report states technical scope only. Seek-order stability is tested within the same dependency/font/codec environment; it is not a promise of byte-identical MP4s across all operating systems or FFmpeg builds.

The exported viewer-facing material should not include internal QA/provider/version labels, private paths or unperformed-test narration. Keep exact provenance and honest NOT_CHECKED fields in the editable evidence record.
