---
name: live-photo-pairs-to-photos
description: Verify JPG+MOV pairs are real Live Photos via ContentIdentifier and batch-import them into macOS Photos for AirDrop, avoiding the common extraction/AppleScript pitfalls.
whenToUse: When you have a folder/zip of matching IMG_xxxx.JPG + IMG_xxxx.MOV files (e.g. an iPhone backup) and need them to become Live Photos in macOS Photos so they can be AirDropped to an iPhone.
metadata:
  authoredBy: dsh-self-evolve
  updatedAt: 2026-10-07T11:25:17.880Z
  version: 2
  createdAt: 2026-10-07T10:52:31.273Z
---

# Live Photo pairs -> Photos.app -> AirDrop

## Key insight
iPhone Live Photos are NOT a single container: they are a JPG + MOV pair linked by a shared
**ContentIdentifier** (a UUID). If the pair was copied off the phone intact, the link already
exists and **no conversion tool is needed at all** — `makelive` and friends are only for
building pairs from *unrelated* files.

Where the identifier lives:
- JPG: Apple MakerNote -> `exiftool -a -G1 -ContentIdentifier x.JPG` shows `[Apple] Content Identifier`
- MOV: QuickTime `mdta` keys -> shows `[Keys] Content Identifier`

## Procedure
1. **Check for an existing link before installing anything:**
   `exiftool -a -G1 -ContentIdentifier IMG_1234.JPG IMG_1234.MOV`
   If both print the same UUID -> already a valid Live Photo.
2. **Extract with the right tool** (see pitfalls). Verify the file count matches the archive.
3. **Validate every pair in bulk** with one `exiftool` call per chunk:
   `exiftool -q -ContentIdentifier -p '$filepath|$ContentIdentifier' <files...>`
   Group by `(dir, stem)`; compare the two UUIDs case-insensitively. Also check for
   duplicate CIDs shared across different pairs (confuses Photos).
4. **Import into the library Photos currently has open.** Hand both files of a pair in the
   *same* `import` call — Photos then merges 2 files into 1 Live Photo asset. The return
   value is the asset count, so `import` of 6 files returning `3` proves the merge worked.
5. **AirDrop from Photos.app** (Share -> AirDrop). AirDropping the raw JPG+MOV from Finder
   does **not** reassemble into a Live Photo. Do it in batches (a few hundred) so a failure
   does not lose the whole transfer.

## Pitfalls (all hit in practice)
- `unzip` **garbles** Chinese/CJK names when the archive stores them in the Info-ZIP
  `up` (0x7075 unicode-path) extra field with the UTF-8 general-purpose flag *clear*.
  Python's `zipfile` honours the `up` field; `unzip` does not.
- macOS `ditto -x -k` can silently stop early on a large archive (it printed
  `Couldn't read pkzip signature` and produced only ~half the files, yet exited 0).
  **Always compare extracted count vs archive count.** Finish the remainder with Python.
- Reading `Photos.sqlite` with `immutable=1` **ignores the WAL**, so counts look stale.
  Use `mode=ro` (no `immutable`) to see live data.
- `open -a Photos --args -library <path>` is **ignored** by current Photos; it silently
  keeps the default library. The Option-launch library chooser also does not trigger under
  System Events automation, and there is no "Open Library" menu item.
  -> Creating a separate library requires a **manual** Option-launch by the user.
- Photos AppleScript `delete` fails with `-10000` (AppleEvent handler failed) — deleting
  imported items must be done in the GUI.
- AppleScript reserved words to avoid as variable names: `log` (use `msg`).
- `library folder` is not a real Photos AppleScript property.
- `timeout` is not available on macOS; wrap with `subprocess.run(..., timeout=)` in Python.
- `import ... into album "X"` fails with `-1728` — the `into` parameter takes an **album object**,
  not a string. `make new album named "X"` first, then `import <files> into <albumVar>`.
- **Photos silently stops importing after a few thousand assets.** `import` returns
  `OK count=0` immediately — no error, no dialog. Even a freshly renamed copy returns 0.
  The fix is a **full relaunch** of Photos (`pkill -x Photos` then `open -a Photos`).
  Note `tell application "Photos" to quit` often does NOT actually quit it (it lags while
  flushing), so verify with `pgrep -x Photos` and escalate to `pkill -9`.
  -> Always drive bulk imports as: import batch -> if returned count < expected, relaunch
  Photos and retry -> and re-verify the whole set by CID at the end, looping until 0 missing.
- Photos renames everything in `originals/` to `<UUID>.jpeg` / `<UUID>_3.mov`, so you
  **cannot** audit an import by filename. Audit by ContentIdentifier instead: read the CID
  out of every file under `originals/` and diff against the expected CID set.
- A healthy Live Photo asset shows **3 rows in `ZINTERNALRESOURCE`** (2 originals + 1
  live sidecar), i.e. `select count(*) group by ZASSET` should be uniformly 3.

## Verifying iCloud upload risk
`ZCLOUDMASTER` count in `Photos.sqlite` == 0 while `ZASSET` > 0 means iCloud Photos sync
is OFF, so importing will not trigger an upload.

## Useful queries
```sql
select count(*) from ZASSET;            -- assets (1 per Live Photo, not 2)
select count(*) from ZINTERNALRESOURCE; -- resources (2 per Live Photo)
select count(*) from ZCLOUDMASTER;      -- 0 => iCloud sync off
```
