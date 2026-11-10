# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

DDF-RA is the CDISC/TransCelerate **Digital Data Flow Reference Architecture**: the Unified Study Definitions
Model (USDM) logical model, its API specification, Implementation Guide (IG), Controlled Terminology (CT), and
CORE conformance rules. It contains almost no application code. The content is standards deliverables (Enterprise
Architect UML, OpenAPI spec, Excel workbooks, PDFs) plus generated artifacts and example study files. There is no
build, lint, or test suite. The only automation is one GitHub Actions workflow.

Licensing: code/scripts are MIT, content is CC-BY-4.0. Don't commit files that are under other licenses; link to
them instead (see `CONTRIBUTING.md`).

## Source-of-truth vs. generated files

The three canonical, hand-maintained artifacts drive everything else:

| Artifact | Path | Notes |
| -- | -- | -- |
| UML model | `Deliverables/UML/USDM_UML.qea` (Enterprise Architect project) exported to `USDM_UML.xmi` | The `.xmi` is what tooling reads. The UML version is the `version` of the diagram named `USDM` |
| API spec | `Deliverables/API/USDM_API.json` (OpenAPI 3.1, `/v4/...` paths) | `info.version` is the release version. `USDM_API.yaml` is the YAML form of the same spec, so keep the two in sync |
| Controlled Terminology | `Deliverables/CT/USDM_CT.xlsx` | The `DDF Entities&Attributes` sheet defines classes/attributes with NCIt C-codes |

These are **generated** from the three artifacts above by the external
[`cdisc-org/DDF-RA-Tools`](https://github.com/cdisc-org/DDF-RA-Tools) generator (run by CI). Don't hand-edit them:

- `Deliverables/UML/dataDictionary.MD`
- `Deliverables/UML/dataStructure.yml` (per-class NCIt code, definition, attributes, cardinality, relationship type)
- `Deliverables/UML/alignment.csv` (cardinality/characteristic mismatches between API, CT, and UML; ideally header-only)
- `Deliverables/{UML,CT,API}/{UML,CT,API}_DELTA_<prev>_<curr>.csv` (version-to-version diffs; column meanings are in each folder's `*_DELTA_README.md`)
- `Documents/CORE Test Data Template/CORE Test Data Template.xlsx`

Any `.xlsx` versions of the delta files (e.g. `CT_DELTA_3-0-0_4-0-0.xlsx`) and the `*_Changes.xlsx` workbooks are
hand-curated companions to that output.

A model change normally has to be applied consistently across UML, API, and CT. `alignment.csv` is how
inconsistencies between them surface.

## CI: "Generate Diff and Data Dict" workflow

`.github/workflows/diff-and-data-dict.yml` runs on pushes to any branch **except `main`** when `USDM_UML.xmi`,
`USDM_CT.xlsx`, or `USDM_API.json` change. It can also be run manually (`workflow_dispatch`, with input `prev-branch`,
default `main`). It checks out the previous release and DDF-RA-Tools, generates the files listed above, and
**commits them back to the branch** as `github-actions` with the message "Generate Diff and Data Dict". Pull
before you continue working on a release branch after pushing model changes.

The workflow fails unless the version numbers line up (dots become hyphens, e.g. `4.0.0` → `4-0-0`):

- The branch must be named `release-<version>` (e.g. `release-4-0-1`). The version taken from the branch name must equal `info.version` in `USDM_API.json`.
- The UML `USDM` diagram version must be a prefix of that version.
- `info.version` in the previous branch's `USDM_API.json` must differ from the current version.

To run it locally (from the workflow file's own comment):
`gh act workflow_dispatch -P ubuntu-latest=catthehacker/ubuntu:act-latest --secret-file ../DDF-RA-Actions/my.secrets`

## Other content

- `Deliverables/RULES/USDM_CORE_Rules.xlsx`: USDM CORE conformance rules, with a change log in `USDM_CORE_Rules_Changes.xlsx`. Earlier versions are archived in subfolders such as `USDM_V3.0/`.
- `Deliverables/IG/USDM-IG.pdf`: the Implementation Guide.
- `Deliverables/UML/UML_Views/*.png`: per-area diagrams exported from the UML.
- `Documents/Examples/<study>/`: each example has a source `.xlsx`, often the protocol `.pdf`, and the resulting USDM API `.json` (top-level keys `study`, `usdmVersion`, `systemName`, `systemVersion`). Update these when the model version changes.
- `Documents/Mappings/*.xlsx`: mappings to USDM from M11, CTIS, ClinicalTrials.gov, CPT, and SDTM.
- `Documents/DDF USDM Model Informative.*`: an informative model diagram maintained in OmniGraffle. `Documents/Changes/` holds per-version snapshots of it.
- `HowTos/`: generic GitHub template instructions, not specific to USDM.

## Working conventions

- Release work happens on `release-X-Y-Z` branches, and `main` holds the published release. Recent history shows commits that touch multiple deliverables for a single release step (e.g. "Updated CORE rules with last changes for v4").
- Use Python (`openpyxl`/`pandas`) for read-only inspection of `.xlsx`. Don't rewrite curated workbooks programmatically unless asked, because that can lose formatting.
- `Deliverables/UML/USDM_UML.xmi` (~1.8 MB) and `USDM_API.json` are large. Query them (`jq`, `xmlstarlet`, Python) rather than reading them whole.
