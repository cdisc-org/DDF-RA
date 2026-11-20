#!/usr/bin/env python3
"""Pre-push consistency check for a DDF-RA (USDM) release branch.

Checks, in order:
  1. Versions      the four values the "Generate Diff and Data Dict" CI workflow compares,
                   plus the YAML version and the .qea diagram version
  2. UML export    .qea (USDM package) vs the committed .xmi
  3. API sync      USDM_API.json vs USDM_API.yaml (schemas, properties, required lists,
                   additionalProperties, minItems/maxItems)
  4. UML -> API    every concrete class and property has an API schema/property,
                   with matching required-ness
  5. CT structure  row order and 'Has Value List' format that DDF-RA-Tools depends on
  6. UML -> CT     every concrete class/property has a row in 'DDF Entities&Attributes'
  7. Constraints   UGG-9 schema constraints: additionalProperties=false on every model
                   schema (not Wrapper), minItems=1 on every 1..* / required array
  8. (optional)    run DDF-RA-Tools and report alignment.csv

Usage:
  python3 release_check.py [--repo .] [--ref REF] [--prev-ref main] [--branch NAME]
                           [--model qea|xmi] [--constraints auto|require|off]
                           [--tools PATH_TO_DDF-RA-Tools] [--out FILE]

Exit status: 1 if any check FAILs, else 0. Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usdm_lib as U  # noqa: E402

IGNORE_API_EXTRA = {"extensionAttributes", "instanceType"}
CT_SHEET = "DDF Entities&Attributes"
CT_ROLES = {"Entity", "Attribute", "Relationship", "Complex Datatype Relationship"}


class Artifacts:
    """Reads repository files from the working tree, or from a git ref when given."""

    def __init__(self, repo: Path, ref: str | None):
        self.repo, self.ref = repo, ref
        self.tmp = Path(tempfile.mkdtemp(prefix="usdm-check-"))

    def path(self, rel: str) -> Path | None:
        if self.ref is None:
            p = self.repo / rel
            return p if p.exists() else None
        data = U.git_show(self.repo, self.ref, rel)
        if data is None:
            return None
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def cleanup(self):
        shutil.rmtree(self.tmp, ignore_errors=True)


IRREGULAR = {"children": "child", "criteria": "criterion"}


def singular(word: str) -> str:
    if word in IRREGULAR:
        return IRREGULAR[word]
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith("sses") or word.endswith("xes"):
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def api_name_for(prop: U.Prop, props: set[str]) -> str | None:
    """The API property that represents a UML property (value or id-reference form)."""
    cands = [prop.name]
    if prop.kind == "association":
        s = singular(prop.name)
        cands += [f"{prop.name}Id", f"{prop.name}Ids", f"{s}Id", f"{s}Ids"]
    return next((c for c in cands if c in props), None)


# --------------------------------------------------------------------------- checks
def check_versions(r: U.Report, a: Artifacts, repo: Path, prev_ref: str, branch: str):
    S = "1. Versions (CI gate)"
    api_p, yaml_p, xmi_p, qea_p = (a.path(x) for x in (U.API_JSON, U.API_YAML, U.XMI, U.QEA))
    api_v = U.load_api_json(api_p).get("info", {}).get("version") if api_p else None
    yaml_v = U.yaml_info_version(yaml_p) if yaml_p else None
    xmi_v = U.xmi_diagram_version(xmi_p) if xmi_p else None
    qea_v = U.qea_diagram_version(qea_p) if qea_p else None
    prev_raw = U.git_show(repo, prev_ref, U.API_JSON)
    prev_v = U.load_api_json(prev_raw).get("info", {}).get("version") if prev_raw else None
    cur = branch.replace("release-", "", 1) if branch.startswith("release-") else ""

    PV, CV, AV, UV = U.hyphen(prev_v), cur, U.hyphen(api_v), U.hyphen(xmi_v)
    r.info(S, f"PREVIOUS_VERSION `{PV or '?'}` (API info.version on `{prev_ref}`) · CURRENT_VERSION "
              f"`{CV or '?'}` (branch `{branch}`) · CURRENT_API_VERSION `{AV or '?'}` · CURRENT_UML_VERSION `{UV or '?'}`")
    if not branch.startswith("release-"):
        r.warn(S, f"Branch `{branch}` is not named `release-<version>`; CI derives CURRENT_VERSION from the "
                  "branch name, so the workflow would fail here. Checks below assume the API version is the target.")
        CV = AV
    for label, v in (("PREVIOUS_VERSION", PV), ("CURRENT_VERSION", CV), ("CURRENT_API_VERSION", AV),
                     ("CURRENT_UML_VERSION", UV)):
        if "-" not in v:
            r.fail(S, f"{label} is missing or has no '.'/'-' separator (`{v or 'empty'}`)")
    if PV and CV and PV == CV:
        r.fail(S, f"Previous release `{prev_ref}` already has version `{PV}`; bump info.version on this branch")
    if AV != CV:
        r.fail(S, f"USDM_API.json info.version `{api_v}` does not match the branch version `{CV}`")
    else:
        r.ok(S, f"USDM_API.json info.version `{api_v}` matches the branch")
    if UV and CV and not CV.startswith(UV):
        r.fail(S, f"XMI `USDM` diagram version `{xmi_v}` is not a prefix of `{CV}`; set it in EA and re-export")
    elif UV:
        r.ok(S, f"XMI `USDM` diagram version `{xmi_v}` is compatible")
    if yaml_v != api_v:
        r.fail(S, f"USDM_API.yaml info.version `{yaml_v}` differs from USDM_API.json `{api_v}`")
    else:
        r.ok(S, "USDM_API.yaml info.version matches the JSON")
    if qea_v != xmi_v:
        r.warn(S, f"`.qea` `USDM` diagram version is `{qea_v}` but the XMI says `{xmi_v}`. A fresh EA export "
                  f"will write `{qea_v}`, so set the diagram version in EA before exporting.")


def compare_models(q: U.Model, x: U.Model):
    diffs = []
    for c in sorted(set(q.classes) | set(x.classes)):
        a, b = q.classes.get(c), x.classes.get(c)
        if not a or not b:
            diffs.append(f"class `{c}` only in {'.qea' if a else '.xmi'}")
            continue
        if sorted(a.supers) != sorted(b.supers):
            diffs.append(f"`{c}` superclasses .qea {a.supers} vs .xmi {b.supers}")
        if a.abstract != b.abstract:
            diffs.append(f"`{c}` abstract .qea {a.abstract} vs .xmi {b.abstract}")
        for p in sorted(set(a.props) | set(b.props)):
            pa, pb = a.props.get(p), b.props.get(p)
            if pa is None or pb is None:
                diffs.append(f"`{c}.{p}` only in {'.qea' if pa else '.xmi'}")
            elif (pa.type.lower(), pa.lower, pa.upper) != (pb.type.lower(), pb.lower, pb.upper):
                diffs.append(f"`{c}.{p}` .qea {pa.type} {pa.card} vs .xmi {pb.type} {pb.card}")
    return diffs


def check_export(r: U.Report, a: Artifacts):
    S = "2. UML export (.qea vs .xmi)"
    qp, xp = a.path(U.QEA), a.path(U.XMI)
    if not qp or not xp:
        r.fail(S, "`.qea` or `.xmi` not found")
        return None, None
    q, x = U.load_qea(qp), U.load_xmi(xp)
    others = {k: v for k, v in U.qea_packages(qp).items() if k != "USDM"}
    if others:
        r.info(S, "Not compared (outside the exported USDM package): " +
               "; ".join(f"{k}: {', '.join(v)}" for k, v in others.items()))
    diffs = compare_models(q, x)
    if diffs:
        r.fail(S, f"The XMI is out of date with the `.qea` ({len(diffs)} differences). CI and DDF-RA-Tools read "
                  "only the XMI, so re-export it from Enterprise Architect:")
        for d in diffs:
            r.fail(S, "  " + d)
    else:
        r.ok(S, f"XMI matches the `.qea` ({len(q.classes)} classes)")
    return q, x


def check_api_sync(r: U.Report, a: Artifacts):
    S = "3. API JSON vs YAML"
    jp, yp = a.path(U.API_JSON), a.path(U.API_YAML)
    j, y = U.api_schema_props(U.load_api_json(jp)), U.yaml_schemas(yp)
    bad = False
    for s in sorted(set(j) - set(y)):
        r.fail(S, f"schema `{s}` only in JSON"); bad = True
    for s in sorted(set(y) - set(j)):
        r.fail(S, f"schema `{s}` only in YAML"); bad = True
    for s in sorted(set(j) & set(y)):
        if j[s]["props"] != y[s]["props"]:
            r.fail(S, f"`{s}` properties differ: JSON-only {sorted(j[s]['props'] - y[s]['props'])}, "
                      f"YAML-only {sorted(y[s]['props'] - j[s]['props'])}"); bad = True
        if j[s]["required"] != y[s]["required"]:
            r.fail(S, f"`{s}` required differs: JSON-only {sorted(j[s]['required'] - y[s]['required'])}, "
                      f"YAML-only {sorted(y[s]['required'] - j[s]['required'])}"); bad = True
        if j[s]["additionalProperties"] != y[s]["additionalProperties"]:
            r.fail(S, f"`{s}` additionalProperties differs: JSON {_ap(j[s]['additionalProperties'])}, "
                      f"YAML {_ap(y[s]['additionalProperties'])}"); bad = True
        for p in sorted(set(j[s]["bounds"]) | set(y[s]["bounds"])):
            jb, yb = j[s]["bounds"].get(p, {}), y[s]["bounds"].get(p, {})
            if jb != yb:
                r.fail(S, f"`{s}.{p}` item bounds differ: JSON {jb or 'none'}, YAML {yb or 'none'}"); bad = True
    if not bad:
        n_ap = sum(1 for v in j.values() if v["additionalProperties"] is not None)
        n_b = sum(len(v["bounds"]) for v in j.values())
        r.ok(S, f"{len(j)} schemas: properties, required lists and constraints match "
                f"({n_ap} with additionalProperties, {n_b} properties with minItems/maxItems)")


def _ap(v) -> str:
    return "absent" if v is None else f"`{str(v).lower() if isinstance(v, bool) else v}`"


def is_model_schema(name: str) -> bool:
    """`<Class>-Input`/`-Output` schemas except Wrapper (which stays open, per DDF-RA #701)."""
    return bool(re.search(r"-(Input|Output)$", name)) and not name.startswith("Wrapper-")


def _report_list(r: U.Report, status: str, S: str, head: str, items: list[str], limit: int = 25):
    r.add(status, S, f"{head} ({len(items)}):")
    for it in items[:limit]:
        r.add(status, S, "  " + it)
    if len(items) > limit:
        r.add(status, S, f"  … {len(items) - limit} more")


def check_constraints(r: U.Report, a: Artifacts, m: U.Model, mode: str):
    """UGG-9: additionalProperties=false on model schemas, minItems=1 on 1..*/required arrays."""
    S = "7. API schema constraints (UGG-9)"
    if mode == "off":
        r.info(S, "skipped (--constraints off)")
        return
    schemas = U.load_api_json(a.path(U.API_JSON)).get("components", {}).get("schemas", {})
    model = sorted(n for n in schemas if is_model_schema(n))

    # minItems targets: required arrays in the API, plus UML 1..* arrays (both Input/Output)
    targets: dict[str, set[str]] = {n: set() for n in model}
    optional_with_min: list[str] = []
    for n in model:
        s = schemas[n]
        props, req = s.get("properties", {}), set(s.get("required", []))
        for p, v in props.items():
            if v.get("type") == "array" and p in req:
                targets[n].add(p)
        cname = re.sub(r"-(Input|Output)$", "", n)
        if cname in m.classes:
            for up in m.all_props(cname).values():
                name = api_name_for(up, set(props))
                if not name or props[name].get("type") != "array":
                    continue
                if up.many and up.required:
                    targets[n].add(name)
                elif props[name].get("minItems", 0) >= 1:
                    optional_with_min.append(f"`{n}.{name}` (UML {up.card})")
    n_targets = sum(len(v) for v in targets.values())

    missing_ap = [n for n in model if schemas[n].get("additionalProperties") is not False]
    bad_ap = [f"`{n}` = {_ap(schemas[n]['additionalProperties'])}" for n in model
              if "additionalProperties" in schemas[n] and schemas[n]["additionalProperties"] is not False]
    missing_min = [f"`{n}.{p}`" for n in model for p in sorted(targets[n])
                   if schemas[n]["properties"][p].get("minItems", 0) < 1]
    has_ap, has_min = len(model) - len(missing_ap), n_targets - len(missing_min)
    adopted = has_ap > 0 or has_min > 0

    summary = (f"additionalProperties: false on {has_ap}/{len(model)} model schemas; "
               f"minItems ≥ 1 on {has_min}/{n_targets} required (1..*) array properties")
    if mode == "auto" and not adopted:
        r.info(S, f"Not adopted yet: {summary}. Use `--constraints require` to enforce them before adoption.")
    else:
        r.info(S, summary + ("" if mode == "require" else " (enforced: the spec has started using them)"))
        if bad_ap:
            _report_list(r, "FAIL", S, "additionalProperties set to something other than false", bad_ap)
        missing_only = [f"`{n}`" for n in missing_ap if "additionalProperties" not in schemas[n]]
        if missing_only:
            _report_list(r, "FAIL", S, "model schemas without `additionalProperties: false`", missing_only)
        if missing_min:
            _report_list(r, "FAIL", S, "required/1..* array properties without `minItems: 1`", missing_min)
        if not (bad_ap or missing_only or missing_min):
            r.ok(S, "every model schema is closed and every required array has minItems: 1")

    # checked in every mode except off
    for w in sorted(n for n in schemas if n.startswith("Wrapper-") and schemas[n].get("additionalProperties") is False):
        r.warn(S, f"`{w}` has `additionalProperties: false`; the Wrapper should stay open for "
                  "system-specific data (DDF-RA #701)")
    if optional_with_min:
        _report_list(r, "WARN", S, "minItems on arrays that are optional (0..*) in the UML", optional_with_min)


def check_uml_api(r: U.Report, a: Artifacts, m: U.Model):
    S = "4. UML vs API"
    schemas = U.load_api_json(a.path(U.API_JSON)).get("components", {}).get("schemas", {})
    problems = 0
    for cname in sorted(m.classes):
        c = m.classes[cname]
        if c.abstract:
            continue
        s = schemas.get(f"{cname}-Input") or schemas.get(cname)
        if s is None:
            r.fail(S, f"no API schema for class `{cname}` (expected `{cname}-Input`/`{cname}-Output`)")
            problems += 1
            continue
        props, req = set(s.get("properties", {})), set(s.get("required", []))
        for p in m.all_props(cname).values():
            name = api_name_for(p, props)
            if name is None:
                r.fail(S, f"`{cname}.{p.name}` ({p.type} {p.card}) has no API property")
                problems += 1
                continue
            if p.required != (name in req) and not p.many:
                r.warn(S, f"`{cname}.{p.name}` is {p.card} in UML but API `{name}` is "
                          f"{'required' if name in req else 'optional'}")
                problems += 1
    if not problems:
        r.ok(S, "every concrete class and property is in the API with matching required-ness")


def ct_rows(path: Path):
    rows = U.read_xlsx(path, [CT_SHEET])[CT_SHEET]
    h = U.header_index(rows[0])
    need = ["Entity Name", "Role", "Logical Data Model Name", "Has Value List"]
    missing = [n for n in need if n not in h]
    return rows, h, missing


def check_ct(r: U.Report, a: Artifacts, m: U.Model):
    S_STRUCT, S_COV = "5. CT structure (DDF-RA-Tools input)", "6. UML vs CT"
    cp = a.path(U.CT)
    rows, h, missing = ct_rows(cp)
    if missing:
        r.fail(S_STRUCT, f"`{CT_SHEET}` is missing header(s) {missing}; DDF-RA-Tools reads columns by header name")
        return
    ent_seen: set[str] = set()
    ct: dict[str, set[str]] = {}
    order_bad = 0
    for i, row in enumerate(rows[1:], start=2):
        ent, role = U.cell(row, h["Entity Name"]), U.cell(row, h["Role"])
        name, hvl = U.cell(row, h["Logical Data Model Name"]), U.cell(row, h["Has Value List"])
        if not any(row):
            continue
        if role not in CT_ROLES:
            r.warn(S_STRUCT, f"row {i}: unexpected Role `{role}`")
        if role == "Entity":
            ent_seen.add(ent)
            ct.setdefault(ent, set())
            if name != ent:
                r.warn(S_STRUCT, f"row {i}: Entity Name `{ent}` differs from Logical Data Model Name `{name}`")
        else:
            if ent not in ent_seen:
                r.fail(S_STRUCT, f"row {i}: `{ent}.{name}` comes before any `{ent}` Entity row; DDF-RA-Tools "
                           "will stop with KeyError")
                order_bad += 1
            ct.setdefault(ent, set()).add(name)
        if hvl.startswith("Y") and not re.match(r"^Y \((.+?)\)$", hvl):
            r.warn(S_STRUCT, f"row {i}: Has Value List `{hvl}` is not in the form `Y (<codelist>)`")
    if not order_bad:
        r.ok(S_STRUCT, "every attribute/relationship row follows its Entity row")

    problems = 0
    for cname in sorted(m.classes):
        c = m.classes[cname]
        if c.abstract:
            continue
        if cname not in ct:
            r.fail(S_COV, f"class `{cname}` has no Entity row in `{CT_SHEET}`")
            problems += 1
            continue
        for p in m.all_props(cname).values():
            if p.name == "id":
                continue  # id has no CT row by convention
            if p.name not in ct[cname]:
                r.fail(S_COV, f"`{cname}.{p.name}` ({p.type} {p.card}) has no CT row")
                problems += 1
        extra = sorted(ct[cname] - set(m.all_props(cname)))
        if extra:
            r.warn(S_COV, f"`{cname}` CT rows not in the UML: {extra}")
            problems += 1
    stale = sorted(e for e in ct if e not in m.classes)
    if stale:
        r.warn(S_COV, f"CT entities not in the UML: {stale}")
        problems += 1
    if not problems:
        r.ok(S_COV, "every concrete class and property has a CT row")


def run_tools(r: U.Report, a: Artifacts, repo: Path, prev_ref: str, tools: Path, python: str):
    S = "8. DDF-RA-Tools alignment"
    work = Path(tempfile.mkdtemp(prefix="ddf-ra-tools-"))
    try:
        shutil.copytree(tools, work / "tools", ignore=shutil.ignore_patterns(".git"))
        t = work / "tools"
        for sub in ("prevRelease", "currRelease"):
            (t / "resources" / sub).mkdir(parents=True, exist_ok=True)
        for rel in (U.XMI, U.CT, U.API_JSON):
            fname = Path(rel).name
            prev = U.git_show(repo, prev_ref, rel)
            if prev is None:
                r.fail(S, f"`{rel}` not found on `{prev_ref}`")
                return
            (t / "resources/prevRelease" / fname).write_bytes(prev)
            shutil.copy(a.path(rel), t / "resources/currRelease" / fname)
        res = subprocess.run([python, "main.py"], cwd=t, capture_output=True, text=True)
        if res.returncode != 0:
            r.fail(S, f"DDF-RA-Tools failed (exit {res.returncode}): {(res.stderr or res.stdout)[-800:]}")
            return
        for line in (res.stdout or "").splitlines():
            if line.strip():
                r.warn(S, f"generator: {line.strip()}")
        with open(t / "alignment.csv", newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        if len(rows) <= 1:
            r.ok(S, "alignment.csv is header-only")
        else:
            r.fail(S, f"alignment.csv has {len(rows) - 1} mismatch row(s) (columns: {', '.join(rows[0])}):")
            for row in rows[1:51]:
                r.fail(S, "  " + " | ".join(row))
            if len(rows) > 51:
                r.fail(S, f"  … {len(rows) - 51} more")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".", help="DDF-RA checkout (default: .)")
    ap.add_argument("--ref", help="check this git ref instead of the working tree")
    ap.add_argument("--prev-ref", default="main", help="previous release ref, as CI's prev-branch (default: main)")
    ap.add_argument("--branch", help="branch name used for CURRENT_VERSION (default: current branch, or --ref)")
    ap.add_argument("--model", choices=["qea", "xmi"], default="qea",
                    help="UML source for checks 4, 6 and 7 (default: qea, the model being edited)")
    ap.add_argument("--constraints", choices=["auto", "require", "off"], default="auto",
                    help="check 7 (UGG-9 schema constraints): auto = enforce once the spec uses any of them, "
                         "otherwise report coverage only; require = always enforce; off = skip (default: auto)")
    ap.add_argument("--tools", help="path to a DDF-RA-Tools checkout; runs the generator and reports alignment.csv")
    ap.add_argument("--tools-python", default=sys.executable,
                    help="python with DDF-RA-Tools requirements installed (default: this python)")
    ap.add_argument("--out", help="also write the report to this file")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    branch = args.branch or (args.ref if args.ref else U.git(repo, "rev-parse", "--abbrev-ref", "HEAD"))
    a = Artifacts(repo, args.ref)
    r = U.Report(f"USDM release check: `{branch}`" + (f" @ `{args.ref}`" if args.ref else " (working tree)"))
    try:
        check_versions(r, a, repo, args.prev_ref, branch)
        q, x = check_export(r, a)
        check_api_sync(r, a)
        m = q if args.model == "qea" else x
        if m is not None:
            r.info("4. UML vs API", f"UML source: `.{args.model}`")
            check_uml_api(r, a, m)
            check_ct(r, a, m)
            check_constraints(r, a, m, args.constraints)
        if args.tools:
            run_tools(r, a, repo, args.prev_ref, Path(args.tools).resolve(), args.tools_python)
    finally:
        a.cleanup()
    text = r.render()
    print(text)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    sys.exit(1 if r.failed else 0)


if __name__ == "__main__":
    main()
