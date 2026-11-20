# Implementation plan: UGG-11, planned duration of a study element

Date: 2026-11-20

| | |
| -- | -- |
| Ticket | [UGG-11](https://jira.cdisc.org/browse/UGG-11): "Information about planned duration of an element is missing from USDM" |
| Status | UGG Review (unresolved); fix version **USDM v4.1** |
| Components | USDM Model, API, Controlled Terminology, USDM Implementation Guide, USDM IG Mappings, USDM Education/Training Material |
| Sub-tasks | UGG-148 to UGG-154 (titles not available when this plan was written) |
| Target branch | `release-4-1-0` |

## 1. Context

The SDTM Trial Elements (TE) domain needs three things per element:

- `TESTRL` (start rule), which comes from `StudyElement.transitionStartRule`
- `TEENRL` (end rule), which comes from `StudyElement.transitionEndRule`
- `TEDUR`, the planned duration of the element in ISO 8601 format

USDM 4.0 has no source for `TEDUR`. The current SDTM mapping (`Documents/Mappings/sdtm_mapping.xlsx`, sheet `TE`, row 9)
maps it to `Timing.value`, with the note "The element length can be calculated based on timing values … select the
last timing value of epoch related to the element and subtract the timing value of the last scheduledInstance
referencing to the previous epoch."

That derivation is unreliable, for these reasons:

- Epochs are shared by all arms, but the element in an epoch can differ by arm, and so can its length. For example, a
  2-week placebo run-in in one arm and a 4-week active run-in in another can share the same "Run-in" epoch.
- A cell can hold several elements in sequence, for example during a titration epoch.
- The timeline records when scheduled activity instances happen, not where elements start and end.

The ticket proposes one optional attribute, **`StudyElement.plannedDuration`**, using the existing `Duration` complex
datatype. This mirrors `ScheduleTimeline.plannedDuration`, which was added in 4.0. `TEDUR` then becomes a direct copy
rather than a derivation.

## 2. Decision needed first

The 10 November 2026 GGG discussion records agreement on the design, as a complex-datatype relationship with minimal
model impact (Edwin and Darren, 2 November). It also records that UGG had not yet been asked whether this goes in
**4.1 or 5.0**. Earlier Jira comments leaned towards 5.0 (20 July) and asked whether to prioritise M11 alignment
(12 October). The Jira fix version is already set to v4.1.

**Recommendation: include it in 4.1, subject to UGG approval.** Reasons:

- **It is additive and backwards compatible.** The attribute is optional (0..1), so every existing v4.0 file stays
  valid. The 4.1 change already on the branch from UGG-57/61 is different: it adds two *required* properties to
  `InterventionalStudyDesign` and breaks existing instances.
- **It reuses an existing class and pattern.** It needs one new UML attribute, one API property in two schemas, one CT
  row and one NCIt code.
- **It unblocks the SDTM trial design handbook now** rather than at the next major version.

If UGG chooses 5.0, keep this plan and change only the target branch.

## 3. The change

| Aspect | Value |
| -- | -- |
| Class | `StudyElement` (concrete, no superclass or subclasses) |
| New attribute | `plannedDuration` |
| Type | `Duration` (existing class: `text` 0..1, `quantity` QuantityRange 0..1, `durationWillVary` Boolean 1, `reasonDurationWillVary` 0..1, `id` 1) |
| Cardinality | 0..1 |
| Modelled as | An attribute typed by `Duration`, exactly like `ScheduleTimeline.plannedDuration`, so a Value (nested object) in the API, not an id reference |
| Precedent | `ScheduleTimeline.plannedDuration` (`Duration` 0..1, C217012); `Administration.duration` (`Duration` 1, C69282) |

> One Jira comment cites `AgentAdministration.duration` as another use of `Duration`. That class doesn't exist in the
> current model; the class is `Administration` (property `duration`, `Duration` 1).

The current `StudyElement` in `release-4-1-0`, before the change:

| Property | Type | Cardinality |
| -- | -- | -- |
| `id` | String | 1 |
| `name` | String | 1 |
| `label` | String | 0..1 |
| `description` | String | 0..1 |
| `notes` | CommentAnnotation | 0..* |
| `transitionStartRule` | TransitionRule | 0..1 |
| `transitionEndRule` | TransitionRule | 0..1 |
| `studyInterventions` | StudyIntervention (Ref: `studyInterventionIds`) | 0..* |

## 4. Changes by deliverable

The drafts below were produced with the `usdm-model-propagation` skill's own functions, applied to an in-memory copy of
the `release-4-1-0` model with `StudyElement.plannedDuration` added. They match the existing
`ScheduleTimeline.plannedDuration` property exactly.

### 4.1 UML (`Deliverables/UML/USDM_UML.qea` → `.xmi`), component: USDM Model

- In Enterprise Architect, add attribute `plannedDuration` to `StudyElement`: type `Duration`, multiplicity 0..1.
  Use the same type reference as `ScheduleTimeline.plannedDuration`.
- Re-export `USDM_UML.png` and `UML_Views/Arms_Epochs.png`. In the `.qea`, `StudyElement` appears on only two
  diagrams: "USDM" and "Arms and Epochs".
- **In the same EA session, set the `USDM` diagram version to 4.1.0 before exporting the XMI.** The `.qea` currently
  says 3.13; the 4.0.0 bump was made only in the XMI. Exporting without fixing it writes 3.13, and the CI version check
  fails.
- Export `USDM_UML.xmi` and commit it together with the `.qea` and the PNGs.

### 4.2 API (`Deliverables/API/USDM_API.json` and `.yaml`), component: API

Add one optional property, not in `required`, to both `StudyElement-Input` and `StudyElement-Output`, just before
`instanceType`:

```json
"plannedDuration": {
  "anyOf": [
    { "$ref": "#/components/schemas/Duration-Input" },
    { "type": "null" }
  ]
}
```

In `StudyElement-Output` the reference is `Duration-Output`. The YAML, in the file's own style:

```yaml
        plannedDuration:
          anyOf:
          - $ref: '#/components/schemas/Duration-Input'
          - type: 'null'
```

- No path, `required` list or other schema changes are needed. `Duration-Input` and `Duration-Output` already exist.
- `info.version` → `4.1.0` in both files, if not already done for the release.
- Once the UML is exported, this can be applied mechanically:
  `python3 -I .claude/skills/usdm-model-propagation/scripts/propose_changes.py --base main --apply --set-version 4.1.0`.
  On `release-4-1-0` that also applies the UGG-57/61 API changes, so review the report before using `--apply`.

### 4.3 Controlled Terminology (`Deliverables/CT/USDM_CT.xlsx`), component: Controlled Terminology

Add one row to `DDF Entities&Attributes`, at the end of the `StudyElement` block (after sheet row 109, `Row #` 108):

| Entity Name | Role | Inherited From | Logical Data Model Name | NCI C-code | CT Item Preferred Name | Definition | Has Value List |
| -- | -- | -- | -- | -- | -- | -- | -- |
| StudyElement | Complex Datatype Relationship | | plannedDuration | *new code (request from NCI EVS)* | Study Design Element Planned Duration | The period of time over which the study design element is intended to take place. | N |

- The preferred name follows the entity's naming (`Study Design Element Name`, `… Description`, `… Label`). The
  definition follows `Schedule Timeline Planned Duration` (C217012): "The period of time over which the scheduled
  timeline is intended to take place." Both are proposals for the CT team.
- No codelist is needed, because `Duration` is not a coded type.
- Log the change in `Deliverables/CT/USDM_CT_Changes.xlsx`.

### 4.4 CORE rules (`Deliverables/RULES/`)

**No new rule is required.** The existing `Duration` rules apply to every `Duration` instance, so they cover the new
attribute automatically:

| Rule | DDF ID | Severity | Statement |
| -- | -- | -- | -- |
| CHK0307 | DDF00033 | ERROR | At least the text or the quantity must be specified for a duration. |
| CHK0308 | DDF00034 | ERROR | If duration will vary then a reason must be given and vice versa. |
| CHK0309 | DDF00039 | WARNING | If the duration will vary, a quantity is not expected for the duration and vice versa. |

Two options for the team to consider (not part of the ticket):

- A WARNING like CHK0310 ("A planned duration is expected for the main timeline"). **Not recommended:** SDTM `TEDUR`
  is Permissible, and many elements are open-ended (e.g. follow-up until an event).
- A general rule that a duration's quantity unit must be a unit of time. No such rule exists today for any `Duration`.
  If added, it would cover all three uses.

If neither is adopted, the rules workbooks need no changes. The `usdm-core-rules-audit` skill will list the new
property in its "new model content" check as "not referenced by any rule". That is expected, because it isn't a coded
attribute.

### 4.5 SDTM mapping (`Documents/Mappings/sdtm_mapping.xlsx`, sheet `TE`), component: USDM IG Mappings

Replace the derivation in row 9 (`TEDUR`):

| Column | Current | Proposed |
| -- | -- | -- |
| Class / Attribute | `Timing` / `value` | `Duration` / `quantity` |
| Target Path | `…/ScheduleTimeline/@timings/Timing/@value` | `StudyVersion/@studyDesigns/StudyDesign/@elements/StudyElement/@plannedDuration/Duration/@quantity/Quantity/@value + @unit/AliasCode/@standardCode/Code/@code` |
| Target Notes | "The element length can be calculated …" | Convert value and unit to ISO 8601 (see below). Leave `TEDUR` null when `plannedDuration` is absent, when `durationWillVary` is true, or when the quantity is a `Range`. |
| Condition Path | cell/epoch/timeline join | *(none needed)* |
| Mapping Category | Study Timeline | Study Design |
| v4.0 Change | | Use the column's existing convention for a change in this release (the TS `LENGTH` row uses `NEW`) |

This follows the existing TS Parameters `LENGTH` row (row 27), which maps `ScheduleTimeline.plannedDuration` the same
way.

ISO 8601 conversion of `Quantity.value` + unit:

| Unit (C71620 UNIT codelist) | ISO 8601 | Example |
| -- | -- | -- |
| Year (C29848) | `P<n>Y` | 1 year → `P1Y` |
| Month (C29846) | `P<n>M` | 6 months → `P6M` |
| Week (C29844) | `P<n>W` | 24 weeks → `P24W` |
| Day (C25301) | `P<n>D` | 14 days → `P14D` |
| Hour (C25529) | `PT<n>H` | 12 hours → `PT12H` |

Year (C29848) is confirmed from the example files. Confirm the other C-codes against current SDTM CT before
publishing.

Also update the `Readme` sheet's `USDM Version` (currently `v4.0.0`) when the mappings are revised for 4.1.

### 4.6 Example files (`Documents/Examples/`)

- **No change is required for validity.** The attribute is optional, so all 5 examples remain valid. Together they
  contain 28 `StudyElement` instances: Alexion 4, CDISC Pilot 7, Devices 7, Eli Lilly 5, Observational 5.
- **Recommended:** populate `plannedDuration` in at least one example, such as the CDISC Pilot, so implementers see it.
  Take the durations from the protocol. No current example populates *any* `plannedDuration`, so there is no in-repo
  template; this one uses the examples' `Quantity` structure:

  ```json
  "plannedDuration": {
    "id": "Duration_1",
    "extensionAttributes": [],
    "text": "24 weeks",
    "quantity": {
      "id": "Quantity_1",
      "extensionAttributes": [],
      "value": 24.0,
      "unit": {
        "id": "AliasCode_1",
        "extensionAttributes": [],
        "standardCode": {
          "id": "Code_1", "extensionAttributes": [], "code": "C29844",
          "codeSystem": "http://www.cdisc.org", "codeSystemVersion": "<current>",
          "decode": "Week", "instanceType": "Code"
        },
        "standardCodeAliases": [],
        "instanceType": "AliasCode"
      },
      "instanceType": "Quantity"
    },
    "durationWillVary": false,
    "reasonDurationWillVary": null,
    "instanceType": "Duration"
  }
  ```

  Ids must be unique within the file. The source `.xlsx` for each example must be updated the same way.
- Set `usdmVersion` to `4.1.0` in all examples as part of the release, as for 4.0.0.

### 4.7 Implementation Guide (`Deliverables/IG/USDM-IG.pdf`), component: USDM Implementation Guide

- In the study design / study element section, describe `plannedDuration`: when to populate it (fixed-length elements),
  how to represent a variable length (`durationWillVary` = true with a reason, and no quantity), and how it relates to
  the transition rules. The rules say *how* an element starts and ends; `plannedDuration` says *how long* it is planned
  to last.
- In the SDTM trial design guidance, state that `TEDUR` comes from `StudyElement.plannedDuration`, replacing any
  description of deriving it from the timeline.

### 4.8 Education/training material and other documents

- Update the SDTM trial design handbook section on generating TE (the use case that raised the ticket).
- Informative model diagram (`Documents/DDF USDM Model Informative.graffle`, `.png`, `.pdf`): add `plannedDuration` to
  `StudyElement`.

### 4.9 Generated by CI (don't edit by hand)

The push that changes the XMI, CT and API triggers "Generate Diff and Data Dict". It regenerates `dataDictionary.MD`,
`dataStructure.yml`, `alignment.csv`, `*_DELTA_4-0-0_4-1-0.csv` and the CORE Test Data Template (a new
`plannedDuration` column on the `StudyElement` sheet).

## 5. Implementation sequence

| # | Step | Component | Depends on |
| -- | -- | -- | -- |
| 0 | UGG decision: 4.1 or 5.0 | n/a | n/a |
| 1 | Request an NCIt C-code and confirm the preferred name and definition with the CT team | Controlled Terminology | 0 |
| 2 | UML change in EA, version set to 4.1.0, XMI and PNG export | USDM Model | 0 |
| 3 | API JSON and YAML change | API | 2 |
| 4 | CT row and changelog entry | Controlled Terminology | 1 |
| 5 | Run `usdm-release-check`, push steps 2–4 together, let CI regenerate, pull | n/a | 2, 3, 4 |
| 6 | SDTM mapping `TE`/`TEDUR` row | USDM IG Mappings | 2 |
| 7 | Example update (at least one) | n/a | 3 |
| 8 | IG text | USDM Implementation Guide | 2 |
| 9 | Handbook and informative diagram | Education/Training Material | 2 |

The sub-tasks UGG-148 to UGG-154 (7 of them) probably split this work by component, but their titles weren't
available when this plan was written. Map steps 1–9 onto them in Jira.

**Coordination with the rest of 4.1:** `release-4-1-0` already carries the UGG-57/61 model change (PR #719), which
hasn't been exported or propagated yet (see `release-4-1-0-vs-main-review.md`). Do the UGG-11 UML edit in the same EA
session as that export and the version fix, so there is one XMI export, one API pass and one CI cycle.

## 6. Verification

1. **Before pushing:** `python3 -I .claude/skills/usdm-release-check/scripts/release_check.py`.
   - Check 2 (UML export) shows no differences between `.qea` and `.xmi`.
   - Check 4 (UML vs API) has no failures for `StudyElement.plannedDuration`.
   - Check 6 (UML vs CT) has no failures for `StudyElement.plannedDuration`.
   - The only expected warning is the known `Study.id` exception.
2. **After CI:**
   - `UML_DELTA_4-0-0_4-1-0.csv` and `API_DELTA_4-0-0_4-1-0.csv` each show `StudyElement.plannedDuration` as added.
   - `CT_DELTA_4-0-0_4-1-0.csv` shows the new CT row.
   - `dataStructure.yml` lists `plannedDuration` under `StudyElement` with Relationship Type `Value` and the new C-code.
   - `alignment.csv` has no row for `StudyElement` (apart from the known `Study.id` row it should be header-only).
3. **Rules:** `python3 -I .claude/skills/usdm-core-rules-audit/scripts/rules_audit.py --base main` lists
   `StudyElement.plannedDuration` as new content with no rule (expected) and no other new findings.
4. **Mapping check:** for the example that was populated, produce `TEDUR` from the new path and confirm it matches the
   protocol (e.g. `P24W`).
5. **Compatibility:** all five v4.0 example files still validate against the 4.1 API schema without `plannedDuration`.

## 7. Risks and open questions

- **Timing:** the 4.1 vs 5.0 decision (section 2). Everything else is small.
- **NCIt code lead time:** the CT row can't be finalised without a new C-code, so request it early.
- **Range durations:** `Duration.quantity` can be a `Range` (e.g. 2–4 weeks), which has no single ISO 8601 value.
  The proposed mapping leaves `TEDUR` null and relies on `text`. The IG should say so explicitly.
- **Not in scope:** an element-level start or end *offset* (when the element starts relative to the study). That would
  be a larger change and isn't requested.

## Sources

- UGG-11 Jira export (description and comments of 14 April, 20 July, 25 August, 12 October and 10 November 2026)
- `release-4-1-0` at `c69fd36`: UML `.qea` (`StudyElement`, `Duration`, `ScheduleTimeline`, `Administration`),
  `USDM_API.json` (`StudyElement-*`, `ScheduleTimeline-*`, `Duration-*`), `USDM_CT.xlsx` (rows 102–109, 255, 372,
  641–645), `USDM_CORE_Rules.xlsx`, `Documents/Mappings/sdtm_mapping.xlsx` (`TE` row 9, `TS Parameters` row 27) and
  `Documents/Examples/*.json`
