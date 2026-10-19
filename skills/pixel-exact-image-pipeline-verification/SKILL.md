---
name: pixel-exact-image-pipeline-verification
description: Verify a C/C++ JPEG/color pipeline (3D LUT, tone map, resample) is mathematically correct down to single-LSB level, and prove where old-vs-new differences really come from. Use when a rewritten image-processing binary must be validated, when old-vs-new or Pillow-based diffs look suspicious, or when a reference implementation must be trusted.
whenToUse: Rewriting or optimizing an image-processing binary (LUT/color/geometry) and needing exact, defensible verification numbers before deploying; especially when a Python-based comparison gives unexpectedly large differences.
metadata:
  authoredBy: dsh-self-evolve
  updatedAt: 2026-10-15T14:37:13.757Z
  version: 1
  createdAt: 2026-10-15T14:37:13.757Z
---

Goal: prove the pixel math of a compiled image pipeline exactly, and separate "our bug" from "decoder/encoder noise".

STEP 0 — build a baseline of the OLD source, not just the new one.
  `cp src/tool.c src/tool.c.bak-pre`  then
  `cc -x c -O2 -o /tmp/old src/tool.c.bak-pre -I<inc> -L<lib> -ljpeg -lm`
  PITFALL: `cc file.c.bak` fails with "unknown file type" — the `-x c` flag is required for non-.c extensions.

STEP 1 — cheap structural checks (pure Python, no libs):
  - JPEG marker walker: list (marker, offset, length) of every segment before SOS; confirm APP1/APP2/APP13/COM survive and APP0 policy.
  - Parse SOF0 component sampling factors to prove 4:4:4 vs 4:2:0 took effect: `hv = d[10+k*3+1]; h=hv>>4; v=hv&15`.
  - File sizes in/out per encoder setting.

STEP 2 — end-to-end diff old vs new (this is the number users ask for, but it is NOT a correctness proof):
  mean|d|, max|d|, p99, % pixels differing, per-channel means, luma-histogram correlation.
  Report mean LSB as the headline; a mean well under 1-2 LSB is consistent with "same intent, better precision".

STEP 3 — the real proof: feed *identical raw pixels* to the compiled code and to an independent reference.
  a) Python dumps raw RGB: `np.ascontiguousarray(img[y0:y1,x0:x1]).tofile('tc.rgb')` (use a COLORFUL crop).
  b) Build a harness that reaches file-static functions directly:
       #define main tool_main
       #include "path/to/tool.c"
       #undef main
     then call the static per-pixel function in a loop reading/writing raw .rgb. No source changes to the deliverable.
  c) Write a vectorized numpy reference (float64/float32) from the format spec.
  d) Compare byte-exactly. Target: 0 to a few differing bytes out of millions (max |d| = 1). Anything above ~1e-4 fraction means a real bug in one of the two.

STEP 4 — if discrepancies remain, decide WHO is right by hand-computing a single offending pixel:
  print the input, the grid indices, the fractional weights, the 8 (or 4) corner values, and the expected value for each candidate branch, then see which implementation matches.

PITFALLS (all observed in practice):
  * Pillow is NOT a pixel-exact reference for a libjpeg-based tool. `Image.open(p).convert('RGB')` decodes as YCbCr and converts with Pillow's own coefficients; libjpeg's `out_color_space=JCS_RGB` differs by up to ~66 LSB (mean ~0.28) on the same file. Steep LUTs amplify that to 100+ LSB, looking like a bug in your code. Never blame your interpolation before checking this. Verify by decoding the same file twice: once with a 20-line libjpeg program, once with Pillow, and diff.
  * Reference-implementation bug pattern: vectorized boolean branch masks MUST mirror the C's exact comparison operators and be mutually exclusive. A wrong mask (e.g. using `fg>=fb` where the branch needs `fb>=fg`) silently leaves `out` uninitialized (`np.empty`) for the uncovered pixels — the result looks plausible and only ~3% of pixels are wrong. Always `assert sum(masks)==1` per pixel, and make the masks structurally parallel to the `if/else` chain.
  * Tetrahedral interpolation accumulation must use CONSECUTIVE vertices:
      out = c000 + f1*(v1-c000) + (f2-f1)*(v2-v1) + (f3-f2)*(v3-v2)
    A common wrong version reuses `c000` for every term: `+ (f2-f1)*(v2-c000)`.
  * Test images may be secretly monochrome. Check `(max(px)-min(px)).mean()` before trusting a color test: a gray source exercises none of the chroma/axis-order paths (R/B swaps are invisible). Also remember identity/grayscale LUTs cannot expose channel swaps — only a saturated color LUT can.
  * `.cube` line order is R fastest: `idx = r + N*g + N^2*b`; parse with `v.reshape(N,N,N,3).transpose(3,2,1,0)` to get `T[comp, r, g, b]`.
