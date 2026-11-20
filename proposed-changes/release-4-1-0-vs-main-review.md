# Review: `release-4-1-0` vs `main`

Date: 2026-11-19

## Scope and method

- Compared local `release-4-1-0` (HEAD `c69fd36`) with local `main` (`aa303cb`, "Final v4.0 for Publication").
  A refresh from GitHub timed out, so this reflects the remote state as of the last successful fetch.
- 8 commits, 7 files changed:

| File | Change |
| -- | -- |
| `Deliverables/UML/USDM_UML.qea` | Model changes (PR #719, tickets UGG-57 / UGG-61) |
| `Deliverables/UML/UML_Views/StudyDesign.png`, `Deliverables/UML/USDM_UML.png` | Re-exported diagrams |
| `Deliverables/RULES/USDM_CORE_Rules.xlsx` | CORE rules errata |
| `Deliverables/RULES/USDM_CORE_Rules_Changes.xlsx` | New "Changes release 4.0 (errata)" sheet |
| `Deliverables/RULES/USDM_V3.0/USDM_CORE_Rules_v3.0_Final.xlsx` | v3.0 rules errata |
| `CLAUDE.md` | Added |

- The UML was compared by querying the `.qea` (a SQLite database) on both branches: `t_object` (classes),
  `t_attribute` (attributes), `t_connector` (associations and generalizations).
- The rules workbooks were compared with `openpyxl`, matching rows by `Check_ID`.

**Not changed on the branch:** `USDM_UML.xmi`, `USDM_API.json`, `USDM_API.yaml`, `USDM_CT.xlsx`, examples, the IG, and all
generated files (`dataDictionary.MD`, `dataStructure.yml`, `alignment.csv`, `*_DELTA_*.csv`).

## 1. What changed

### 1.1 UML model (`.qea` only)

New class `InterventionAssignment` (commit `a391061`, "Added new class: InterventionAssignment"):

| Attribute | Type | Cardinality |
| -- | -- | -- |
| `assignmentMethod` | Code | 1 |
| `isStratified` | boolean | 1 |
| `otherMethod` | string | 0..1 |
| `randomizationType` | string | 0..1 |

Changes to `InterventionalStudyDesign` (commit `e049c78`):

| Change | Detail |
| -- | -- |
| New attribute `controlType` | Code, 1 |
| New association `interventionAssignment` | `InterventionalStudyDesign` (1) → `InterventionAssignment` (1), directed source → destination |

`randomizationType` was changed from Code to string in `e049c78`. Nothing else in the model changed: no other classes,
attributes or associations were added, removed or modified.

### 1.2 CORE rules (`USDM_CORE_Rules.xlsx`)

- 235 rules gained a CORE-ID (new `CORE-ID` column values only).
- 1 new rule: **CHK0320 / DDF00263 / CORE-001076**, "An activity is expected to refer to at least one procedure,
  biomedical concept, biomedical concept category, biomedical concept surrogate, child activity, or timeline."
  (WARNING, v4.0 only). It replaces CHK0057 for v4.0.
- Substantive changes:

| Check_ID | Change |
| -- | -- |
| CHK0009 | "child instances of the same parent class" → "all instances of the same class" (names must be unique) |
| CHK0028 | Attribute name corrected: `reasonOther` → `otherReason` |
| CHK0035 | "must be" → "is expected to be"; **ERROR → WARNING** |
| CHK0057 | Version 4.0 **Y → N** (replaced by CHK0320) |
| CHK0110 | Codelist C201265 labelled DDF instead of SDTM |
| CHK0123 | **ERROR → WARNING** (planned age unit) |
| CHK0137 | Codelist named "extensible Study Design Characteristics Value Set Terminology (C207416)" |
| CHK0140 | Restricted to scheduled activity instances "in the main timeline" |
| CHK0165 | Mode of Subject Contact codelist marked extensible |
| CHK0183, CHK0184 | "and vice versa" removed (display section number / title) |
| CHK0188 | Scope widened from "the study version as the narrative content" to "the study" |
| CHK0204 | Codelist name corrected ("administrable product property type") |
| CHK0207, CHK0208 | "study protocol document version" → "study definition document version" |
| CHK0212 | Rule now names "a quantity's unit"; entity `Range, Quantity` → `Quantity` |
| CHK0232 | Typo "ether" → "either" |
| CHK0240 | Scope: "within any study definition document affected by a study amendment" |
| CHK0241 | **WARNING → ERROR** (document version referenced more than once) |
| CHK0243 | "An study impact type" → "A study amendment impact type" |
| CHK0257 | Rewritten: cross-over, parallel or factorial models expect more than 1 intervention |
| CHK0270 | Codelist name "observational study design subtype" |
| CHK0276 | Now conditional: "If a study phase is specified …" with value "Not Applicable" |
| CHK0295 | Whitespace fix |
| CHK0302 | "section numbers" → "displayed section numbers" |
| CHK0314 | Codelist named "extensible study role code (C215480)" |

`USDM_CORE_Rules_Changes.xlsx` has a new sheet, "Changes release 4.0 (errata)", with 30 entries that record the edits above.
The other sheets are unchanged. `USDM_CORE_Rules_v3.0_Final.xlsx` has the same edits where they apply to v3.0
(CHK0009, 0035, 0110, 0123, 0137, 0140, 0165, 0212).

## 2. Changes required as a result of this branch

The model change exists only in the Enterprise Architect project. None of the other deliverables have been updated, so
UML, API and CT are now out of step.

### 2.1 UML export (blocking)

- Re-export `Deliverables/UML/USDM_UML.xmi` from the `.qea`. The XMI is what DDF-RA-Tools reads, and it is unchanged
  from `main`. Until it is re-exported, CI produces no data dictionary, data structure, delta or alignment output for
  the new class.
- Set the `USDM` diagram version in the XMI to `4.1.0`. It is currently `4.0.0`. The CI workflow requires the branch
  version (`4-1-0`) to start with the UML version.

### 2.2 UML fixes suggested before export

- Add `id` (String, 1) to `InterventionAssignment`. Every other concrete class in the `main` model has an `id`, either
  directly (e.g. `Masking`, `GeographicScope`) or inherited (e.g. `Range` inherits it from `QuantityRange`), and every
  API schema for them requires `id`.
- Capitalize the types to `Boolean` and `String` to match the model's convention (259 `String`, 15 `Boolean`).
  The lowercase types are also used on `ConditionAssignment.id` and `ParameterMap.id` (already on `main`).
- Decide whether `randomizationType` should be a coded value. Commit `e049c78` changed it to string, but a Code would
  allow CT validation.

### 2.3 API (`USDM_API.json` and `USDM_API.yaml`)

The two files must stay in sync.

1. Bump `info.version` from `4.0.0` to `4.1.0`. Without this, the CI workflow fails on `release-4-1-0`, because the
   API version must equal the branch version and differ from the previous release.
2. Add `InterventionAssignment-Input` and `InterventionAssignment-Output`, modelled on `Masking-Input` and
   `Masking-Output`:

   ```json
   "InterventionAssignment-Input": {
     "title": "InterventionAssignment",
     "type": "object",
     "properties": {
       "id": {"type": "string", "minLength": 1, "title": "Id"},
       "extensionAttributes": {"type": "array", "items": {"$ref": "#/components/schemas/ExtensionAttribute-Input"}, "default": [], "title": "Extensionattributes"},
       "assignmentMethod": {"$ref": "#/components/schemas/Code-Input"},
       "isStratified": {"type": "boolean", "title": "Isstratified"},
       "otherMethod": {"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Othermethod"},
       "randomizationType": {"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Randomizationtype"},
       "instanceType": {"type": "string", "enum": ["InterventionAssignment"], "const": "InterventionAssignment", "title": "Instancetype"}
     },
     "required": ["id", "assignmentMethod", "isStratified", "instanceType"]
   }
   ```

   The `-Output` variant is the same but references `ExtensionAttribute-Output` and `Code-Output`.
3. Add these to both `InterventionalStudyDesign-Input` and `InterventionalStudyDesign-Output`:
   - `controlType` → `Code-Input` / `Code-Output`
   - `interventionAssignment` → `InterventionAssignment-Input` / `InterventionAssignment-Output`
   - Add both to `required` (the UML cardinality is 1 for each).
4. **Breaking change:** both new properties are required, so every existing v4.0 `InterventionalStudyDesign` instance
   is invalid under 4.1.0. Either accept this, and say so in the release notes, or make both 0..1 in the UML for a
   minor release.

### 2.4 Controlled Terminology (`USDM_CT.xlsx`, sheet `DDF Entities&Attributes`)

- Add these rows, each with a C-code, preferred name and definition:
  - Entity `InterventionAssignment`
  - Attributes `assignmentMethod`, `isStratified`, `otherMethod`, `randomizationType` (and `id` if added)
  - Relationship `InterventionalStudyDesign.interventionAssignment`
  - Attribute `InterventionalStudyDesign.controlType`
- Set `Has Value List` and the codelist for `assignmentMethod` and `controlType`, adding entries to
  `DDF valid value sets` if they are new DDF codelists.
- **Semantic overlap to resolve:** codelist C207416, used by `StudyDesign.characteristics`, already contains
  `C46079 Randomized`, `C25689 Stratification` and `C147145 Stratified Randomisation`. These now overlap with
  `InterventionAssignment.isStratified` and `assignmentMethod`. Decide which is authoritative, and either deprecate the
  overlapping characteristic values or add a consistency rule (see 2.5).

### 2.5 CORE rules to add for the new model content

| Proposed rule | Entity | Attributes |
| -- | -- | -- |
| An intervention assignment method must be specified according to the (new) assignment method codelist | InterventionAssignment | assignmentMethod |
| A control type must be specified according to the (new) control type codelist | InterventionalStudyDesign | controlType |
| If the assignment method is 'Other' then `otherMethod` must be specified, and vice versa | InterventionAssignment | assignmentMethod, otherMethod |
| A randomization type is only expected when the assignment method indicates randomization | InterventionAssignment | assignmentMethod, randomizationType |
| `isStratified` is expected to be consistent with the study design characteristics (C207416 stratification values) | InterventionAssignment, InterventionalStudyDesign | isStratified, characteristics |

Record the new rules in `USDM_CORE_Rules_Changes.xlsx` under a 4.1 sheet.

### 2.6 Downstream deliverables

- **Examples** (`Documents/Examples/*/*.json`): every interventional example needs `controlType` and
  `interventionAssignment`, and `usdmVersion` set to 4.1.0.
- **Implementation Guide** (`Deliverables/IG/USDM-IG.pdf`): add guidance for intervention assignment and control type,
  and how they relate to `characteristics`.
- **Mappings** (`Documents/Mappings/*.xlsx`): map M11 and ClinicalTrials.gov allocation, masking and control fields to
  the new attributes. For M11 (`m11_mapping.xlsx`, sheet `Mapping`), four rows map content that 4.1 now models
  directly, and need re-pointing:

  | Row | M11 element | Mapped today to | Proposed 4.1 target |
  | -- | -- | -- | -- |
  | 73 | 1.1.2 Control type | `StudyArm.type` (codes C174267, …) | `InterventionalStudyDesign.controlType` |
  | 87 | 1.1.2 Intervention assignment method | `StudyDesign.characteristics` (C46079, C25689, …) | `InterventionAssignment.assignmentMethod` (and `otherMethod`) |
  | 97 | 1.1.2 randomly assigned to trial intervention/enrolled | `StudyDesign.characteristics` (C46079, C147145) | `InterventionAssignment.assignmentMethod` / `randomizationType` |
  | 157 | 4.1 Method of Assignment to Trial Intervention | `StudyDesign.characteristics` (C46079, C25689, …) | `InterventionAssignment.assignmentMethod` |

  These rows select on C46079 (Randomized), C25689 (Stratification) and C147145 (Stratified Randomisation). Those are
  the C207416 values that overlap with `InterventionAssignment` (section 2.4), so the targets should follow whichever
  representation the CT decision makes authoritative.

  Also, the M11 review material on `release-4-0-1` isn't on this branch: the `Documents/M11/` folder (review
  workbook, M11 class diagrams, and a copy of the EA model with an "M11" diagram) and an updated `Documents/README.md`.
  It merges into `release-4-1-0` without conflicts. But its copy of the EA model predates the UGG-57/61 change, and its
  review workbook has the same four rows. See `DDF-RA_branch_comparison_main_vs_release-4-0-1.html` in this directory.
- **Generated by CI once the XMI, CT and API are updated:** `dataDictionary.MD`, `dataStructure.yml`, `alignment.csv`,
  `*_DELTA_4-0-0_4-1-0.csv`, and `CORE Test Data Template.xlsx`. Check that `alignment.csv` is header-only afterwards.
- **Informative diagram** (`Documents/DDF USDM Model Informative.*`) and `Documents/Changes/`: add the new class.

## 3. Issues found in the rules workbooks

Introduced or left unresolved on this branch:

- **CHK0181, CHK0219, CHK0294** are marked `DELETED` in the "Changes release 4.0 (errata)" sheet, but still appear in
  `USDM_CORE_Rules.xlsx` with Version 4.0 = `Y` and no CORE-ID. Either remove them or set Version 4.0 to `N`.
- **CHK0320**: the statement mentions "timeline", but the attributes column
  (`definedProcedures, biomedicalConcepts, bcCategories, bcSurrogates, children`) omits `timeline`.

Already on `main` (found by checking every v4.0 rule's entities and attributes against the model):

| Check_ID | Problem | Suggested fix |
| -- | -- | -- |
| CHK0053 | Entity `StudyProtocolDocumentVersion` does not exist in v4 | `StudyDefinitionDocumentVersion` |
| CHK0173, CHK0174 | Attribute `criteria` on `ObservationalStudyDesign` / `InterventionalStudyDesign`; the design classes use `eligibilityCriteria` (`criteria` belongs to `PopulationDefinition`) | `eligibilityCriteria` |
| CHK0254 | `productDesignation` listed on `StudyIntervention`; it belongs to `AdministrableProduct` | Entity `AdministrableProduct` |
| CHK0033 | `relativeFromScheduleInstance` | `relativeFromScheduledInstance` |

## Appendix: reproducing the analysis

```bash
# Changed files and commits
git log --oneline main..release-4-1-0
git diff --stat main...release-4-1-0

# Extract both EA projects (SQLite)
git show main:Deliverables/UML/USDM_UML.qea > main.qea
git show release-4-1-0:Deliverables/UML/USDM_UML.qea > br.qea

# Attributes per class (run for each file, then diff)
sqlite3 -readonly br.qea "select o.Name, a.Name, a.Type, a.LowerBound, a.UpperBound
  from t_attribute a join t_object o on o.Object_ID=a.Object_ID
  where o.Object_Type='Class' order by 1,2"

# Associations
sqlite3 -readonly br.qea "select c.Connector_Type, s.Name, c.SourceCard, d.Name, c.DestCard, c.Name
  from t_connector c join t_object s on s.Object_ID=c.Start_Object_ID
  join t_object d on d.Object_ID=c.End_Object_ID
  where c.Connector_Type in ('Association','Aggregation','Generalization') order by 2,4"

# Versions checked by CI
jq -r .info.version Deliverables/API/USDM_API.json
grep -o 'project[^>]*version="[^"]*"' Deliverables/UML/USDM_UML.xmi | head -1
```
