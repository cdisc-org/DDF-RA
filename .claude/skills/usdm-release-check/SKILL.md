---
name: usdm-release-check
description: >
  Pre-push consistency check for DDF-RA (USDM) release branches. Runs one script that
  verifies the version numbers the "Generate Diff and Data Dict" CI workflow compares,
  detects UML changes saved in USDM_UML.qea but not exported to USDM_UML.xmi, checks
  USDM_API.json and USDM_API.yaml are in sync, and checks every UML class/property has a
  matching API schema property and Controlled Terminology (USDM_CT.xlsx) row. Optionally
  runs DDF-RA-Tools and reports alignment.csv. Use in the DDF-RA repository before pushing
  model, API or CT changes; when asked to check, validate or review a release branch; when CI
  "Generate Diff and Data Dict" fails or did not run; when alignment.csv has rows; or when
  asked whether UML, API and CT are aligned or a release is ready.
---

# USDM release check

One read-only script, `scripts/release_check.py`, checks a DDF-RA release branch the way CI
and DDF-RA-Tools will see it. It uses only the Python standard library, so it runs without
openpyxl, PyYAML or xmlstarlet.

## Run it

From the DDF-RA repository root:

```bash
# working tree of the current branch, compared with main (as CI does)
python3 -I .claude/skills/usdm-release-check/scripts/release_check.py

# any branch or tag, without checking it out
python3 -I .claude/skills/usdm-release-check/scripts/release_check.py --ref release-4-1-0

# save the report
python3 -I .claude/skills/usdm-release-check/scripts/release_check.py --out "$TMPDIR/release-check.md"
```

| Option | Use |
| -- | -- |
| `--ref REF` | Check a git ref instead of the working tree |
| `--prev-ref REF` | Previous release, as CI's `prev-branch` input (default `main`) |
| `--branch NAME` | Override the branch name used for `CURRENT_VERSION` |
| `--model qea\|xmi` | UML used for checks 4 and 6. Default `qea` (the model being edited); use `xmi` to see exactly what CI will see |
| `--tools PATH` | Path to a DDF-RA-Tools checkout. Runs `main.py` on copies of the inputs and reports `alignment.csv` |
| `--tools-python PY` | Python with DDF-RA-Tools' `requirements.txt` installed (default: the interpreter running the script) |

Exit status is 1 if any check fails. Present the report to the user grouped by check, and lead
with the failures that block CI (checks 1 and 2).

`--tools` copies the tools checkout to a temporary folder and never writes to the DDF-RA
repository. If its requirements are not installed, one way to run it is
`uv run --no-project --with-requirements <tools>/requirements.txt python -I release_check.py --tools <tools>`.
In the Claude Code sandbox, set `UV_CACHE_DIR="$TMPDIR/uvcache"` first.

## What each check means and how to fix it

1. **Versions (CI gate).** Recomputes the four values the workflow compares (dots become
   hyphens). The branch must be `release-<version>`; `info.version` in USDM_API.json must equal
   it and differ from the previous release; the XMI `USDM` diagram version must be a prefix of
   it. It also checks the YAML `info.version`, and warns when the `.qea` diagram version differs
   from the XMI. That has happened: for 4.0.0 the XMI was set to `4.0.0` while the `.qea` still
   says `3.13`, so a fresh export from EA would undo it.
   *Fix:* bump `info.version` in both API files; set the `USDM` diagram version in EA, then export.
2. **UML export.** Compares the `USDM` package of the `.qea` (SQLite) with the committed `.xmi`.
   Any difference means the XMI was not re-exported, so CI and DDF-RA-Tools cannot see the change.
   The `Extensions` package is not exported and is reported for information only.
   *Fix:* export the XMI from Enterprise Architect and commit it with the `.qea` and PNGs.
3. **API JSON vs YAML.** Schema names, property names and `required` lists must match. Nothing
   else in the project checks the YAML.
4. **UML vs API.** Every concrete class needs a `<Class>-Input` schema (the `-Output` schema
   mirrors it). Abstract classes have no schema; their properties are checked on each concrete
   subclass. An association can appear as a nested object (`definedProcedures`) or as an id
   reference (`biomedicalConceptIds`, `timelineId`); both forms are accepted.
   *Known exception:* `Study.id` is 1 in the UML but optional in the API. This is the one row of
   the published 4.0.0 `alignment.csv`; treat it as expected unless the team changes it.
5. **CT structure.** DDF-RA-Tools reads `DDF Entities&Attributes` by header name and attaches
   each non-Entity row to an Entity row it has already read. A row before its Entity row
   stops the generator with `KeyError`. `Has Value List` values starting with `Y` must be
   `Y (<codelist>)`.
6. **UML vs CT.** Every concrete class needs an `Entity` row, and every property (own and
   inherited, except `id`) needs a row under that entity. Rows for names not in the UML are
   warnings (stale or misspelt).
7. **DDF-RA-Tools alignment** (only with `--tools`). Runs the real generator and lists
   `alignment.csv` rows. This is authoritative; checks 4 and 6 are a faster approximation.

## Limits

- The YAML is read by indentation (2 spaces, as the project's file is written). Unusual
  formatting may need `--model`/manual review.
- Id-reference names are matched with simple English singular rules plus the irregulars
  `children → child` and `criteria → criterion`. Add others to `IRREGULAR` in the script if a
  false "no API property" appears.
- The script checks presence and required-ness, not data types or definitions.
- `scripts/usdm_lib.py` is shared with the `usdm-model-propagation` and `usdm-core-rules-audit`
  skills. Keep the copies identical.
