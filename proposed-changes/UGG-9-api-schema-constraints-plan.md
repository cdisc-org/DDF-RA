# Implementation plan: UGG-9, additional constraints for the API

Date: 2026-11-20

| | |
| -- | -- |
| Ticket | [UGG-9](https://jira.cdisc.org/browse/UGG-9): "Additional constraints for API" (originally GitHub issue [#701](https://github.com/cdisc-org/DDF-RA/issues/701), Nov 2025) |
| Status | Approval Needed (moved back by Darren Moreland on 16 Nov 2026); fix version **USDM v4.1** |
| Component | API |
| Sub-task | UGG-147 "API Development – Additional constraints…" (Backlog) |
| Attachment | `USDM_CORE_Schema_Constraints_Change_Request` (25 Aug 2026), referred to below as "the change request" |
| Target branch | `release-4-1-0` |

## 1. Context

CORE's JSON Schema validation uses schemas derived from the USDM v3 and v4 API specifications. CORE added two
constraints to its own copies that the published spec doesn't have:

1. **`additionalProperties: false` on every model class.** The extension mechanism (`extensionAttributes`,
   `ExtensionAttribute`, `ExtensionClass`) is now the sanctioned way to add data, so free-form extra keys aren't needed.
   Closing them makes misspelled attribute names fail validation instead of passing silently. The `Wrapper` class is
   excluded, because systems may need to add their own information at the top level (#701 comment).
2. **`minItems: 1` on required array properties.** JSON Schema `required` only means the key is present, so `[]`
   passes today. This is the same gap that `minLength: 1` already closes for required strings.

The request is to add both to `USDM_API.json` and `.yaml`, so CORE's schemas and the published spec don't diverge.

Status of the discussion:

- 16 Oct 2026: UGG leads agreed to move ahead.
- 16 Nov 2026: moved back to "Approval Needed". Implementers should be asked whether stricter validation breaks their
  workflows, and `Estimand.intercurrentEvents` raises an ICH E9(R1) question.

**This change touches only the API.** It has no UML or CT change, and no new model content.

## 2. Verification of the change request

Each factual claim was checked against `release-4-1-0` (`c69fd36`).

| Claim | Verified result |
| -- | -- |
| "164 schemas (82 model classes × Input/Output)" | ❌ **164 schemas = 80 model classes × 2 + `Wrapper` × 2 + 2 FastAPI error schemas** (`HTTPValidationError`, `ValidationError`). `additionalProperties: false` therefore applies to **160** schemas. |
| No schema sets `additionalProperties` today | ✅ None do. It's new everywhere. |
| `extensionAttributes` is on every model class | ✅ All 80 model classes have it (optional, `default: []`). |
| No construct conflicts with closing properties | ✅ No `allOf`, `oneOf`, `patternProperties` or `unevaluatedProperties` anywhere. (`additionalProperties: false` combined with `allOf` composition would have broken subclassing.) |
| "21 required array properties across 15 classes" | ⚠️ **21 properties is correct, but they span 12 classes**, not 15. The same 21 exist in both `-Input` and `-Output`, so **42** schema properties get `minItems`. |
| None currently specify `minItems` | ✅ None do. Arrays have only 4 `maxItems: 2`, on `plannedSex` in `StudyCohort` and `StudyDesignPopulation` (Input and Output). |
| The 21 match the model's "one or more" cardinality | ✅ **All 21 are 1..* in the UML**, and no other 1..* array is missing from the list. So `minItems: 1` adds no new rule; it makes the schema enforce cardinality the model already declares. |

The 21 properties (all UML 1..*, all `required` in the API):

| Class | Properties |
| -- | -- |
| `Estimand` | `interventionIds`, `intercurrentEvents` ⚠️ |
| `ExtensionClass` | `extensionAttributes` |
| `GovernanceDate` | `geographicScopes` |
| `InterventionalStudyDesign` | `arms`, `studyCells`, `epochs`, `eligibilityCriteria` |
| `ObservationalStudyDesign` | `arms`, `studyCells`, `epochs`, `eligibilityCriteria` |
| `ScheduledDecisionInstance` | `conditionAssignments` |
| `StudyAmendment` | `changes`, `geographicScopes` |
| `StudyCell` | `elementIds` |
| `StudyChange` | `changedSections` |
| `StudyVersion` | `studyIdentifiers`, `titles` |
| `Substance` | `strengths` |
| `SyntaxTemplateDictionary` | `parameterMaps` |

## 3. Evidence: the published examples against the constrained schema

The change request recommends "a validation pass against representative instance data". All five example files on
`release-4-1-0` were validated against `Wrapper-Input` with the Python `jsonschema` library (Draft 2020-12), with and
without the constraints:

| Example | Current schema | With UGG-9 constraints | Errors |
| -- | -- | -- | -- |
| CDISC Pilot (LZZT) | ✅ valid | ✅ valid | n/a |
| Alexion (NCT04573309) | ✅ valid | ❌ 2 errors | `StudyChange.changedSections` is `[]` in `StudyChange_8` (amendment `AMEND_1`) and `StudyChange_16` (`AMEND_2`) |
| Eli Lilly (NCT03421379) | ✅ valid | ❌ 1 error | `StudyAmendment.changes` is `[]` in `StudyAmendment_1` |
| Devices | ✅ valid | ❌ 1 error | `StudyAmendment.changes` is `[]` in `StudyAmendment_1` |
| Observational | ✅ valid | ❌ 4 errors | `StudyAmendment.changes` is `[]` in `StudyAmendment_1` to `_4` |

What this shows:

- **`additionalProperties: false` breaks nothing.** None of the examples has a stray or misspelled property.
- **`minItems: 1` fails 4 of the 5 published examples (8 errors).** All are on two properties, `StudyAmendment.changes`
  and `StudyChange.changedSections`. These files already break the model's 1..* cardinality; the current schema just
  doesn't catch it, and no active v4 CORE rule does either.
- **The implementer concern is real.** The tool that generated these examples writes empty required arrays. Other
  implementers' generators may do the same, especially for amendments.
- **CORE likely already reports these.** The ticket says CORE's schemas already contain both constraints, so CORE
  schema validation should report the same 8 errors on these examples today.

## 4. Decisions needed

1. **Adopt in 4.1? Recommended: yes, both constraints.**
   - Both constraints only reject data the model already declares invalid: unknown properties, and empty arrays for
     1..* properties.
   - The spec and CORE are diverging today.
   - Publish it with the release notes saying plainly that validation becomes stricter, and with the examples fixed
     first (decision 3).
2. **`Estimand.intercurrentEvents`: treat it as a model question, not a schema exception.**
   - The UML already says 1..*. Leaving out `minItems` for this one property would make the schema contradict the model.
   - If the estimand owners confirm that zero intercurrent events is valid (ICH E9(R1), early drafts), the correct
     change is to make it **0..* in the UML**, optional in the API (not `required`, `default: []`) and updated in CT.
     That's a separate ticket, and `minItems` is then not added.
   - Recommendation: apply `minItems` consistently in UGG-9, and raise the cardinality question with the estimand owners
     in parallel. If it changes before 4.1 is released, take this property off the list.
3. **Example files: fix them before the schema is tightened.**
   - The 4 failing examples are part of the deliverable and must validate.
   - Each empty `changes` / `changedSections` needs real content from the protocol amendment, or the empty
     `StudyAmendment`/`StudyChange` instance removed if it carries no information. This is a decision for the example
     owners; the data must not be invented.
   - Fix the source `.xlsx` and regenerate, rather than hand-editing the JSON.
4. **Where is the spec actually produced? (Needs confirming.)**
   - The spec's shape points to a generated origin: `-Input`/`-Output` pairs, FastAPI's `HTTPValidationError`, and
     titles like `Extensionattributes`. It looks like Pydantic models served by FastAPI.
   - If the JSON is regenerated from those models, hand edits will be lost. The constraints should then be made in the
     models: `model_config = ConfigDict(extra="forbid")` for `additionalProperties: false` (but not on `Wrapper`), and
     `Field(min_length=1)` on 1..* lists for `minItems: 1`.
   - Recent history (e.g. `4f73979` "Update API version and endpoints to v4") shows the JSON and YAML being edited
     directly in this repository. Confirm which applies before starting.

## 5. Changes

### 5.1 API (`Deliverables/API/USDM_API.json` and `.yaml`)

| Constraint | Where | Count |
| -- | -- | -- |
| `"additionalProperties": false` | Every `<Class>-Input` and `<Class>-Output` schema, **except** `Wrapper-Input`, `Wrapper-Output`, `HTTPValidationError` and `ValidationError` | 160 schemas |
| `"minItems": 1` | The 21 properties in section 2, in both `-Input` and `-Output` | 42 properties |

Placement convention:

- Put `additionalProperties` right after `"type": "object"`.
- Put `minItems` right after `"type": "array"`, matching how the existing `maxItems` is placed.

```json
"StudyCell-Input": {
  "properties": {
    "elementIds": { "items": { "type": "string" }, "type": "array", "minItems": 1, "title": "Elementids" },
    …
  },
  "type": "object",
  "additionalProperties": false,
  "required": [ … ],
  "title": "StudyCell"
}
```

```yaml
        elementIds:
          items:
            type: string
          type: array
          minItems: 1
          title: Elementids
      …
      type: object
      additionalProperties: false
      required:
```

**Applying it mechanically:** if the files are maintained in this repository (decision 4), a small script applies both
constraints exactly. It was tested on copies of the `release-4-1-0` files:

- It adds **202 lines to each file and removes none**. The JSON keeps its exact formatting via a load and dump with
  `indent=2`, which reproduces the file byte for byte. The YAML gets inserted lines in the file's own style.
- Afterwards the constrained JSON and YAML were compared in full (`components.schemas`, parsed with PyYAML) and are
  **identical**.

The script picks schemas by the `-Input`/`-Output` suffix, skips `Wrapper-*`, and adds `minItems` only to properties
that are both `required` and `type: array`. That selection gives exactly the 21 properties in section 2, so they don't
need to be listed by hand. Keep the script with the change (for example in the PR description) so it can be run again.

`info.version` → `4.1.0` in both files, if not already done for the release.

### 5.2 Example files (`Documents/Examples/`)

Fix the 8 empty arrays listed in section 3 (decision 3), and set `usdmVersion` to `4.1.0` as part of the release.
Afterwards, all five examples must validate against the constrained schema.

### 5.3 CORE rules (`Deliverables/RULES/`)

**No changes needed.** No active v4 rule duplicates either constraint. Related rules:

- **CHK0180 (DDF00067), "A study cell must refer to at least one element":** active for v3 only (`Version 4.0` = N).
  For v4, `minItems: 1` on `StudyCell.elementIds` now covers it at schema level.
- **CHK0128 (DDF00115)** requires an "Official Study Title". That implies `StudyVersion.titles` is non-empty, which
  `minItems` now enforces structurally. The rule is still needed for the title type.
- No rule checks `StudyAmendment.changes` or `StudyChange.changedSections`. That's why the 8 example errors are invisible
  to CORE's model rules today, although they're likely caught by CORE's schema validation (section 3).

### 5.4 UML, CT, mappings

No changes. The constraints express cardinalities the UML already has, and CT has nothing to describe.

### 5.5 IG, release notes and implementer communication

- **Release notes / "What's new in 4.1":** state that the 4.1 schema rejects unknown properties on model classes
  (use `extensionAttributes` instead) and empty arrays for required 1..* properties, and that `Wrapper` stays open for
  system-specific data.
- **IG section on the API / schema validation:** explain `required` + `minItems` vs `minLength`, and that extensions
  belong in `extensionAttributes`.
- **Before approval:** ask implementers (per the 16 Nov comment) whether their generators write empty required arrays
  or extra keys. The example files show at least one generator does.

### 5.6 Repository tooling (the `.claude/skills` added in PR #723)

- **`usdm-release-check`: done** (added after this plan was first written). When the plan was written, its JSON-vs-YAML
  check compared property names and `required` lists only, and its report was identical with and without the
  constraints. It now has:
  - **Check 3:** compares each schema's `additionalProperties` and each property's `minItems`/`maxItems` between JSON
    and YAML, so a one-sided edit fails.
  - **New check 7:** verifies `additionalProperties: false` on every model schema except `Wrapper-*`, and `minItems: 1`
    on every array that is required in the API or 1..* in the UML (42 on the 4.1 spec). It warns if `Wrapper` is closed
    or if a 0..* array has `minItems`.
  - **`--constraints auto|require|off`:** with the default `auto`, check 7 reports coverage only until the spec uses
    either constraint, then enforces it everywhere. Use `require` while implementing this plan.
- **`usdm-model-propagation`** should, once UGG-9 is adopted, emit `additionalProperties: false` in new class schemas
  and `minItems: 1` for 1..* arrays, so that future model changes (e.g. `InterventionAssignment` from UGG-57/61) follow
  the new convention. The drafts it produces today don't.

## 6. Implementation sequence

| # | Step | Owner area | Depends on |
| -- | -- | -- | -- |
| 0 | Implementer consultation and UGG approval (4.1) | UGG | n/a |
| 0a | `Estimand.intercurrentEvents` cardinality question to the estimand owners (separate ticket if 0..*) | Model | n/a |
| 0b | Confirm where the spec is maintained (decision 4) | API | n/a |
| 1 | Fix the 4 example files (via their source `.xlsx`) | Examples | 0 |
| 2 | Apply both constraints to JSON and YAML (UGG-147) | API | 0, 0b |
| 3 | Validate all examples against the constrained schema; push; let CI regenerate (the push changes `USDM_API.json`, which triggers it) | API | 1, 2 |
| 4 | Release notes and IG text | IG | 2 |
| 5 | Skill updates (section 5.6) | Tooling | 2 |
| 6 | Tell the CORE team the spec now carries the constraints, so CORE can derive its schemas without local additions | CORE | 3 |

**Coordination with the rest of 4.1:** if UGG-11 and UGG-57/61 are also in 4.1, apply UGG-9 *after* their API edits.
Then their new schemas and properties are constrained by the same script run. `StudyElement.plannedDuration` is optional,
so it gets no `minItems`. `InterventionAssignment-*` would get `additionalProperties: false`.

## 7. Verification

1. **Schema validity:** the constrained `USDM_API.json` is still a valid OpenAPI 3.1 document. Load it with the
   project's usual tooling or an OpenAPI validator.
2. **Counts:** 160 schemas with `additionalProperties: false` (none on `Wrapper-*`, `HTTPValidationError`,
   `ValidationError`); 42 properties with `minItems: 1`; 202 lines added to each of JSON and YAML; no lines removed.
3. **JSON = YAML, and coverage:** run `release_check.py --constraints require`. Check 3 must pass (constraints
   identical in JSON and YAML), and check 7 must report 160/160 and 42/42 with no failures. Optionally also compare
   `components.schemas` in full with PyYAML.
4. **Examples:** all five validate against `Wrapper-Input` with Draft 2020-12, after step 1.
5. **Negative tests:** a misspelled property (e.g. `"labell"` on a `StudyArm`) and an empty `arms` array each produce
   exactly one validation error. The `Wrapper` still accepts an extra top-level key.
6. **CI:** the "Generate Diff and Data Dict" run succeeds. `API_DELTA_4-0-0_4-1-0.csv` is regenerated; whether
   DDF-RA-Tools records the new constraints in it is unconfirmed, and it doesn't affect validity. `alignment.csv` is
   unaffected, since the constraints don't change cardinality as DDF-RA-Tools reads it.

## 8. Risks

- **Breaking for producers:** the risk is real for anyone writing empty required arrays (4 of our own 5 examples) or
  extra keys. It's mitigated by communicating ahead of time, and by the fact that such data already contradicts the
  model.
- **Lost edits:** if the spec is regenerated from code (decision 4), hand edits will be lost unless the change is made
  at the source.
- **`Estimand.intercurrentEvents`:** if the owners later decide on 0..*, it needs a model change, not just removing
  `minItems`.

## Sources

- UGG-9 Jira export (description and comments of 14 Apr, 25 Aug, 12 Oct, 16 Oct, 27 Oct and 16 Nov 2026), and GitHub
  issue #701 with its comments
- `USDM_CORE_Schema_Constraints_Change_Request.pdf` (25 Aug 2026)
- `release-4-1-0` at `c69fd36`: `USDM_API.json` and `.yaml`, the `USDM_UML.qea` UML (both packages),
  `USDM_CORE_Rules.xlsx`, and `Documents/Examples/*.json`
- Validation: Python `jsonschema` (Draft 2020-12) against `Wrapper-Input`; the constraints were applied to temporary
  copies only
