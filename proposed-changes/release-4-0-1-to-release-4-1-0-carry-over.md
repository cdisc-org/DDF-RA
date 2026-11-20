# Carry-over review: what `release-4-0-1` has that `release-4-1-0` needs

Date: 2026-11-20

This report compares `release-4-0-1` with `release-4-1-0` and lists what should be brought across, in what form, and
what shouldn't. It is a report only: **no branch, file or deliverable was changed** to produce it.

## Scope and method

| Branch | Head (checked on GitHub with `git ls-remote`) |
| -- | -- |
| `main` | `aa303cb` (2025-06-03, "Final v4.0 for Publication") |
| `release-4-0-1` | `a5049a1` (2025-06-19) |
| `release-4-1-0` | `c69fd36` (2026-11-10) |

- Both release branches start from `main` at `aa303cb`; that is the merge base.
- `release-4-0-1` has 5 commits not on `release-4-1-0`, and `release-4-1-0` has 8 commits not on `release-4-0-1`.
- The checks used:
  - `git log`, `git diff --stat --find-renames` (three-dot, so only `release-4-0-1`'s own changes are shown), and a
    trial merge with `git merge-tree --write-tree`, which changes no branch;
  - the EA files (SQLite) compared class by class, attribute by attribute and association by association, with the
    same reader the `usdm-release-check` skill uses;
  - the M11 workbook read cell by cell, and the class-map PDF read directly.

The earlier `DDF-RA_branch_comparison_main_vs_release-4-0-1.html` in this directory describes `release-4-0-1` in
detail. This report answers the narrower question of what `release-4-1-0` needs from it.

## Summary

`release-4-0-1` contains **no normative changes**: no UML classes or attributes, no API, CT, rules or IG changes, and
`info.version` is still `4.0.0`. Its net effect is 6 files, all under `Documents/`. `release-4-1-0` hasn't touched
`Documents/` at all. **The trial merge completes without conflicts**, and none of the files are in the CI workflow's
trigger paths.

| File on `release-4-0-1` | Verdict | Why |
| -- | -- | -- |
| `Documents/README.md` (+3 / −2) | ✅ **Bring over as is** | Still accurate for 4.1. The M11 line only makes sense if the `Documents/M11/` folder comes over too |
| `Documents/M11/m11_mapping_review.xlsx` | ⚠️ **Bring over, then update** (if the M11 review is still wanted) | Copy of the published mapping plus empty review columns. Labelled USDM v4.0.0, and 4 rows are superseded by the 4.1 model |
| `Documents/M11/usdm_m11_classes.graffle` / `.pdf` | ⚠️ **Bring over, then update** | Labelled "USDM: V3.13"; needs relabelling, plus the new 4.1 class |
| `Documents/M11/M11.png` | ⚠️ **Bring over, then re-export** | Export of the "M11" diagram; it must be regenerated from the canonical model once the diagram lives there |
| `Documents/M11/USDM_UML.qea` | ❌ **Don't bring over as a file** | A second copy of the EA model, identical to the **4.0** model plus one diagram. It already lacks the 4.1 changes. Move its "M11" diagram into `Deliverables/UML/USDM_UML.qea` instead |

## 1. What `release-4-0-1` contains

| Commit | Date | Author | Change |
| -- | -- | -- | -- |
| `92eca00` | 2025-06-13 | Dave Iberson-Hurst | Adds `Documents/Mappings/m11_mapping_review.xlsx` |
| `2e99606` | 2025-06-13 | Dave Iberson-Hurst | Moves it to `Documents/M11/m11_mapping_review.xlsx` (net: nothing changes in `Documents/Mappings/`) |
| `4e40875` | 2025-06-13 | Dave Iberson-Hurst | Adds `Documents/M11/usdm_m11_classes.graffle` and `.pdf` |
| `d80ff97` | 2025-06-13 | Dave Iberson-Hurst | Updates `Documents/README.md` |
| `a5049a1` | 2025-06-19 | Dave IH | Adds `Documents/M11/M11.png` and `Documents/M11/USDM_UML.qea` ("a copy f the main for the moment") |

Files changed by `release-4-1-0` since the merge base, none of which overlap:

- `CLAUDE.md`
- the three CORE rules workbooks
- `Deliverables/UML/USDM_UML.qea`, `USDM_UML.png` and `UML_Views/StudyDesign.png`

## 2. Item by item

### 2.1 `Documents/README.md`: bring over as is

```diff
-- The changes made across the release from USDM v3.0 to v3.11 shown using the informational model diagram.
-- Mappings. A set of provisional mappings from M11 and CTIS to USDM. These are currently "work in progress" …
+- The changes made across the release from USDM v3.0 to v4 shown using the informational model diagram.
+- Mappings. A set of mappings for USDM to M11, EMA's CTIS, CPT, ClinicalTrials.gov and SDTM T Domains.
 - CORE Test Data Template. …
+- M11. A directory containing USDM M11 review related information
```

- Both corrected statements are accurate on `release-4-1-0`:
  - `Documents/Changes/` holds snapshots 3-0 to 3-13, the last version before 4.0;
  - `Documents/Mappings/` holds exactly those five mapping workbooks.

  The `release-4-1-0` README still has the out-of-date "v3.11 / work in progress" text, so this is an improvement
  regardless.
- Bring over the `M11.` line only if the folder comes over (section 2.2). If 4.1 adds a 4-x informative-diagram
  snapshot to `Documents/Changes/`, extend the first line from "v4" to "v4.1" at that time.

### 2.2 `Documents/M11/m11_mapping_review.xlsx`: bring over and update, if the review is still wanted

What it is:
- A copy of the published `Documents/Mappings/m11_mapping.xlsx`. Columns A–R are identical cell for cell (325 rows),
  and the published file is the same on `main` and `release-4-1-0`.
- It adds a "Review Comments" group: columns S–U repeat the element/class/attribute by formula, and V is a free-text
  Comment.
- **The Comment column is empty in all 323 data rows.** No review feedback was ever recorded in it.

**Decision first:** is the external M11 mapping review still planned? The workbook was prepared in June 2025 for that
purpose. If the review won't happen, leave this file behind, and leave out the README's `M11.` line unless the folder
comes over for its diagrams.

If it comes over, update it, because it would otherwise contradict the 4.1 model:

1. **Version labels** (Readme sheet): `USDM Version` is `v4.0.0`, so change it to `v4.1.0`. Confirm that `M11 Version`
   ("Updated Step 2 Draft, 14th March 2025") is still the version to review against.
2. **Four rows that 4.1 now models directly.** They are the same rows as in the published mapping, so update the
   published `m11_mapping.xlsx` first and then refresh columns A–R of this copy from it, so the two stay identical:

   | Row | M11 element | Mapped today to | 4.1 target |
   | -- | -- | -- | -- |
   | 73 | 1.1.2 Control type | `StudyArm.type` | `InterventionalStudyDesign.controlType` |
   | 87 | 1.1.2 Intervention assignment method | `StudyDesign.characteristics` | `InterventionAssignment.assignmentMethod` (and `otherMethod`) |
   | 97 | 1.1.2 randomly assigned to trial intervention/enrolled | `StudyDesign.characteristics` | `InterventionAssignment.assignmentMethod` / `randomizationType` |
   | 157 | 4.1 Method of Assignment to Trial Intervention | `StudyDesign.characteristics` | `InterventionAssignment.assignmentMethod` |

   Rows 87, 97 and 157 select on C46079 / C25689 / C147145, which are codelist C207416 values that overlap with
   `InterventionAssignment`. The final targets depend on the CT decision recorded in
   `release-4-1-0-vs-main-review.md` (sections 2.4 and 2.6).

Edit the workbook in Excel, not with a script, to keep its formatting and formulas.

### 2.3 `Documents/M11/usdm_m11_classes.graffle` / `.pdf`: bring over and update

- An OmniGraffle class map: green for classes that store M11 content, blue for classes needed for model integrity.
- The PDF is headed **"USDM: V3.13"**, "M11 Template Specification Dated: 13th March 2025", "13th May 2025", "For
  Information Only". Its labels don't match those of the review workbook (USDM v4.0.0, M11 draft of 14 March 2025).
- For 4.1:
  - relabel it to USDM 4.1 and the M11 version agreed in 2.2;
  - add `InterventionAssignment`, which stores M11 content (rows 87, 97 and 157 above), and its link from
    `InterventionalStudyDesign`;
  - show `controlType` on `InterventionalStudyDesign`.

  Then re-export the PDF.

### 2.4 `Documents/M11/USDM_UML.qea`: don't bring over; move its diagram into the canonical model

What it is:
- A full copy of the EA project. Its model content (88 objects, 390 attributes, 161 connectors, 3 packages) is
  **identical to the published 4.0 model**.
- The only difference is a new Logical diagram, **"M11"** (version 1.0, created 2025-06-17), placing 63 existing
  classes (see the appendix) and their links.

Why it shouldn't come over as a file:
- **It's already out of date.** The canonical model on `release-4-1-0` has the UGG-57/61 change (PR #719): the new
  `InterventionAssignment` class, and `controlType` and `interventionAssignment` on `InterventionalStudyDesign`. The
  copy has none of these.
- **It affects the diagram directly.** `InterventionalStudyDesign` is one of the 63 classes on the "M11" diagram, so
  the diagram would show it without its new properties.
- **It would ship two different EA models** in one release. The commit message itself calls the copy temporary.

What to do instead:
1. In `Deliverables/UML/USDM_UML.qea` on `release-4-1-0`, create an "M11" diagram with the same 63 classes. All 63 still
   exist in the 4.1 model, so this only adds a diagram, no model elements. Add `InterventionAssignment` too.
   - EA doesn't merge two projects automatically. Either recreate the diagram by placing the existing classes, or
     transfer it with EA's diagram export/import. If you transfer it, check that it doesn't create duplicate classes.
     Use whichever the UML maintainers prefer.
2. **Do it in the same EA session as the 4.1 XMI export**, together with the `USDM` diagram version fix (3.13 → 4.1.0)
   and UGG-11 if approved. The XMI includes diagrams, so the new diagram appears in `USDM_UML.xmi`. That's harmless to
   CI: the version check reads only the diagram named `USDM`, and DDF-RA-Tools reads only classes.
3. Afterwards, run `usdm-release-check`. Its UML export check (check 2) compares classes, attributes and associations,
   so a diagram-only change should leave it clean.

### 2.5 `Documents/M11/M11.png`: bring over after re-exporting

A 2404 × 3049 export of the "M11" diagram. Re-export it from the canonical model after 2.4, so it shows the 4.1
classes.

## 3. Recommended approach

On a topic branch from `release-4-1-0`, with a PR against `release-4-1-0` (the repository convention):

**Option A: take the files without the EA copy (recommended).**

```bash
git switch -c m11-docs-for-4-1-0 origin/release-4-1-0
git checkout origin/release-4-0-1 -- Documents/README.md \
  Documents/M11/m11_mapping_review.xlsx \
  Documents/M11/usdm_m11_classes.graffle Documents/M11/usdm_m11_classes.pdf \
  Documents/M11/M11.png
# then apply the updates in sections 2.2–2.5 and commit; the M11 diagram goes into Deliverables/UML/USDM_UML.qea
```

This gives one reviewable commit and never adds the 2.3 MB EA copy to the 4.1 history. The commit message should credit
the original commits (`92eca00`, `2e99606`, `4e40875`, `d80ff97`, `a5049a1`).

**Option B: merge, then remove the copy.** Merge `release-4-0-1` into the topic branch, which completes without
conflicts, then `git rm Documents/M11/USDM_UML.qea` and apply the updates. This keeps the original commits and their
authorship, but adds the EA copy to 4.1's history.

Either way:
- The changes touch only `Documents/` and the `.qea`, so they **don't trigger** the "Generate Diff and Data Dict"
  workflow. Only the later XMI export does, as part of the planned 4.1 export.
- Once the material is on `release-4-1-0`, **retire `release-4-0-1`** rather than publishing a 4.0.1. It has no
  normative content, so nothing would be lost.

## 4. Not to carry over

- `Documents/M11/USDM_UML.qea` as a file (section 2.4).
- Nothing else on `release-4-0-1` is unsuitable. The only other commit effect, the move of the review workbook out of
  `Documents/Mappings/`, nets to no change there.

## 5. Checklist

- [ ] Decide whether the external M11 mapping review is still wanted (2.2)
- [ ] Update the published `m11_mapping.xlsx` rows 73, 87, 97 and 157 for 4.1, after the C207416 decision
- [ ] Bring over the README change, and the `Documents/M11/` files except the `.qea`
- [ ] Review workbook: refresh columns A–R from the published mapping; update the version labels
- [ ] Class map: relabel to 4.1; add `InterventionAssignment` and `controlType`; re-export the PDF
- [ ] Recreate the "M11" diagram in `Deliverables/UML/USDM_UML.qea` (with `InterventionAssignment`), in the same EA
      session as the 4.1 export; re-export `M11.png`
- [ ] Run `usdm-release-check`, then open the PR against `release-4-1-0`
- [ ] Retire `release-4-0-1`

## Appendix: the 63 classes on the "M11" diagram

Abbreviation, Address, AdministrableProduct, AdministrableProductIdentifier, AdministrableProductProperty,
Administration, AliasCode, AnalysisPopulation, AssignedPerson, BiospecimenRetention, Characteristic, Code,
CommentAnnotation, DocumentContentReference, Duration, EligibilityCriterion, EligibilityCriterionItem, Endpoint,
Estimand, GeographicScope, GovernanceDate, Identifier, Indication, Ingredient, IntercurrentEvent,
**InterventionalStudyDesign** (changed in 4.1), Masking, MedicalDevice, MedicalDeviceIdentifier, NarrativeContent,
NarrativeContentItem, Objective, Organization, ParameterMap, PersonName, PopulationDefinition, ProductOrganizationRole,
Quantity, QuantityRange, Range, ReferenceIdentifier, Strength, Study, StudyAmendment, StudyAmendmentImpact,
StudyAmendmentReason, StudyArm, StudyChange, StudyCohort, StudyDefinitionDocument, StudyDefinitionDocumentVersion,
StudyDesign, StudyDesignPopulation, StudyIdentifier, StudyIntervention, StudyRole, StudySite, StudyTitle, StudyVersion,
SubjectEnrollment, Substance, SyntaxTemplate, SyntaxTemplateDictionary.

Add for 4.1: **InterventionAssignment**.
