---
name: usdm-core-rules-audit
description: >
  Audits the USDM CORE conformance rules workbook (Deliverables/RULES/USDM_CORE_Rules.xlsx)
  in the DDF-RA repository against the UML model, the Controlled Terminology and the rules
  changelog (USDM_CORE_Rules_Changes.xlsx). Finds rules that name classes or attributes that
  do not exist, cite DDF codelists that are missing or attached to a different attribute in the
  CT, are marked DELETED/NEW in the changelog but not applied in the rules workbook, have
  duplicate IDs or no CORE-ID, and lists new model attributes that have no rule yet. Use in
  DDF-RA when CORE rules or the changelog are edited, after model changes, before a release,
  or when asked to check, review, audit or QC the CORE rules or DDF rule IDs (DDF00xxx/CHKxxxx).
  For authoring or testing rule YAML in the core-contributor project, use the
  core-conformance-rule-authoring skill instead.
---

# USDM CORE rules audit

`scripts/rules_audit.py` is a read-only audit of the rules workbook. It uses only the Python
standard library.

## Run it

From the DDF-RA repository root:

```bash
# working tree; add --base to see which new model content has no rule yet
python3 -I .claude/skills/usdm-core-rules-audit/scripts/rules_audit.py --base main

# a branch or tag without checking it out
python3 -I .claude/skills/usdm-core-rules-audit/scripts/rules_audit.py --ref release-4-1-0 --base main
```

| Option | Use |
| -- | -- |
| `--ref REF` | Audit a git ref instead of the working tree |
| `--base REF` | Enables check 5: model properties added since REF, and whether a rule covers them |
| `--model qea\|xmi` | UML source (default `qea`, the model being edited) |
| `--version-col NAME` | Rules column for the target version (default: highest `Version …` column, e.g. `Version 4.0`) |
| `--changes-sheet NAME` | Changelog sheet to compare (default: the sheet with the highest version in its name) |
| `--out FILE` | Also write the report to a file |

Exit status is 1 if any check fails.

## Checks

1. **Workbook structure.** Duplicate Check_ID, DDF rule ID or CORE-ID; severities other than
   ERROR/WARNING; version flags other than Y/N; rules active for the target version without a
   CORE-ID (often rules that should have been retired).
2. **Model references.** For rules active in the target version, every entity must be a UML
   class and every attribute must exist on it (own or inherited, or on a subclass). The report
   names the class that does define a misplaced attribute, and suggests near spellings.
3. **Codelist references.** A codelist cited as `(Cnnnnnn) DDF codelist` must exist in the CT
   (`DDF valid value sets` or a `Has Value List` entry). If the CT gives that entity/attribute a
   different codelist, it is a warning. SDTM codelists are not checked (they are not in the CT
   workbook).
4. **Changelog.** On the chosen changelog sheet: rules marked DELETED must not still be active;
   other listed rules must exist in the rules workbook; the "new" rule text must match the rules
   workbook. Comparing an older sheet will show text differences that later releases changed on
   purpose, so normally compare the latest sheet.
5. **New model content** (with `--base`). Lists classes and properties added since the base.
   Coded attributes (Code/AliasCode) with no rule are warnings, because USDM checks every coded
   attribute against a codelist. Other new properties are listed for consideration
   (conditional rules such as "if method is Other then otherMethod must be given").

## Reporting and fixing

- Group findings by check and give the Check_ID, DDF rule ID and a suggested correction.
- **Don't edit the workbooks with a script.** They are curated, and rewriting them with openpyxl
  loses formatting. Propose the edits for a person to make in Excel, and record each change on the
  release's sheet in `USDM_CORE_Rules_Changes.xlsx`.
- When proposing a new codelist rule, follow the wording of existing ones, e.g. "A study design's
  characteristics must be specified according to the extensible Study Design Characteristics Value
  Set Terminology (C207416) DDF codelist (e.g. an entry with a code or decode used from the
  codelist should be consistent with the full entry in the codelist)."

## Also review by hand

The script compares names, not meaning. When rules change, also read each changed rule and check:

- the attribute column lists everything the text mentions (e.g. CHK0320's text mentions
  "timeline", but `timeline` is not in its attribute list)
- severity matches the wording ("must" is usually ERROR, "is expected to" is usually WARNING)
- the version columns are right for rules that apply to only one model version

`scripts/usdm_lib.py` is shared with the `usdm-release-check` and `usdm-model-propagation`
skills. Keep the copies identical.
