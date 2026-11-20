---
name: usdm-model-propagation
description: >
  Carries a USDM UML model change through to the other DDF-RA deliverables. Diffs the UML
  (USDM_UML.qea, or the XMI) against the previous release and drafts the matching changes:
  -Input/-Output schemas and property/required edits for USDM_API.json and USDM_API.yaml (and
  can apply them), Controlled Terminology rows for the 'DDF Entities&Attributes' sheet of
  USDM_CT.xlsx, UML convention problems (missing id, lowercase types, breaking required
  attributes), and a checklist of affected examples, mappings, rules and docs. It follows the
  spec's UGG-9 schema constraints (additionalProperties: false, minItems: 1) once the spec uses
  them. Use in the DDF-RA
  repository when a class, attribute or association has been added, removed or changed in the
  UML; when asked what API or CT changes a model change needs; to "propagate", "carry through"
  or "sync" a model change; or to prepare the API/CT side of a release ticket.
---

# USDM model propagation

A model change in USDM has to be applied consistently to three hand-maintained artifacts: the
UML, the API spec (JSON and YAML) and the CT workbook. `scripts/propose_changes.py` works out
what the other two need from the UML change and drafts it.

## Workflow

1. **Generate the change pack** (read-only), from the DDF-RA repository root:

   ```bash
   python3 -I .claude/skills/usdm-model-propagation/scripts/propose_changes.py --base main \
     --out "$TMPDIR/change-pack.md" --csv "$TMPDIR/ct-rows.csv"
   ```

   `--base` is the previous release (default `main`). Add `--ref <branch>` to inspect a branch
   without checking it out. `--model xmi` diffs the exported XMI instead of the `.qea`.

   `--constraints auto|on|off` controls the UGG-9 schema constraints in the drafts:
   `additionalProperties: false` on new schemas, and `minItems: 1` on required (1..*) arrays.
   - `auto` (default) includes them only if the spec at `--ref` already uses them. Constraining only
     the new schemas in an otherwise open spec would make the release check's `auto` mode fail every
     other schema.
   - `on` forces them, e.g. when propagating together with UGG-9.
   - `off` leaves them out.

   Section 3 of the change pack says which mode applied and why.

2. **Review it with the user.** Read section 2 (UML hygiene) first: problems there are best fixed
   in the UML before anything is propagated. In particular:
   - A new concrete class without `id`: every concrete class has one (own or inherited) and every
     API schema requires it.
   - Lowercase `string`/`boolean`: the convention is `String`/`Boolean`.
   - A new **required** attribute on an existing class breaks every existing instance, including
     the examples. Confirm it is intended or make it optional.
   - The **Value vs Ref** assumption for each new association (owned nested object vs `<role>Id(s)`
     reference). The UML does not record this; the script infers it from `dataStructure.yml`.
     Confirm each one.

3. **Apply the API edits** once the user agrees (working tree only):

   ```bash
   python3 -I .claude/skills/usdm-model-propagation/scripts/propose_changes.py --base main --apply --set-version 4.1.0
   ```

   - JSON is edited by load and dump with 2-space indentation, which reproduces the file's format
     exactly. New schemas go in sorted position; new properties and `required` entries go just
     before `instanceType`, as in every existing schema.
   - YAML is edited by inserting text at the same positions, in the file's style.
   - Running it again is safe: existing schemas are left alone and properties are replaced, not
     duplicated.
   - Show the user `git diff --stat` and the key hunks afterwards.

4. **CT rows.** Don't write the CT workbook from a script; it is curated and openpyxl loses
   formatting. Give the user the section 4 table or the CSV to paste in Excel. Each row must go
   after its entity's `Entity` row. Every `TBD` needs a C-code, preferred name and definition, and
   every coded attribute needs a codelist (`Y (<C-code>)`). Offer the `ncit-concept-resolver`
   agent for candidate C-codes and definitions, and say that the final terminology needs the CT
   team's review.

5. **Verify.** Run the `usdm-release-check` skill. After the API is applied, its checks 3 (JSON vs
   YAML) and 4 (UML vs API) should pass, and so should check 7 (UGG-9 constraints) when the spec
   uses them. Checks 2 (XMI export) and 6 (CT) pass only after the XMI
   is exported in Enterprise Architect and the CT rows are added. Then work through section 5 of the
   change pack, using the `usdm-core-rules-audit` skill (with `--base`) for the rules.

## What the drafts follow

These conventions are taken from the 4.0.0 spec:

| UML | API property |
| -- | -- |
| `String` 1 | `{"type": "string", "title": …}`; `id`/`name` also get `"minLength": 1` |
| `String` 0..1 | `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": …}` |
| `String` 0..* | `{"items": {"type": "string"}, "type": "array", "title": …, "default": []}` |
| `Boolean` / `Integer` / `Float` / `Date` | `boolean` / `integer` / `number` / `string` + `"format": "date"` |
| Class type (Code, Quantity, …) 1 | `{"$ref": "#/components/schemas/<T>-Input"}` (no title) |
| Class type 0..1 | `{"anyOf": [{"$ref": …}, {"type": "null"}]}` |
| Class type 0..* / 1..* | array of `$ref`, with `"default": []` only when optional |
| Abstract type (e.g. QuantityRange) | `anyOf` of its concrete subclasses |
| Ref association | `<singular role>Id` (string) or `<singular role>Ids` (array of string) |
| Any 1..*, **with UGG-9 constraints** | `"minItems": 1` right after `"type": "array"` (not on optional arrays) |

- **Schemas:** `id`, then `extensionAttributes`, then the model's properties (inherited first), then
  `instanceType` (`const` = class name). `required` lists the required properties in that order,
  ending with `instanceType`. `title` is the name with only its first letter capitalized
  (`isStratified` → `Isstratified`). Abstract classes have no schema; their properties are added to
  every concrete subclass. With UGG-9 constraints, new schemas also get `"additionalProperties":
  false` right after `"type": "object"`. Edited existing schemas keep whatever
  `additionalProperties` they already have.
- **CT rows:** no row for `id`. Primitives are `Attribute`; class-typed attributes (Code, Quantity,
  CommentAnnotation, …) are `Complex Datatype Relationship`; associations are `Relationship`, with no
  C-code, `Has Value List` = `N/A` and the definition "A USDM relationship between the X and Y
  classes which identifies …". Subclasses repeat inherited rows with `Inherited From` set.

## Limits

- The script diffs names, types and cardinalities only. Renames show up as remove + add.
- Value vs Ref is a heuristic (see step 2).
- It never edits the UML, CT, rules, examples or docs. Section 5 lists what to update by hand.
- `scripts/usdm_lib.py` is shared with the `usdm-release-check` and `usdm-core-rules-audit` skills.
  Keep the copies identical.
