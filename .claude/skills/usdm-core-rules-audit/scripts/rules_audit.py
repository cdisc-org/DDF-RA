#!/usr/bin/env python3
"""Audit Deliverables/RULES/USDM_CORE_Rules.xlsx against the USDM model, CT and changelog.

Checks:
  1. Workbook structure   duplicate Check_ID / DDF rule ID / CORE-ID, severity values,
                          version flags, active rules without a CORE-ID
  2. Model references     entities and attributes named by active rules exist in the UML
                          (inherited properties included)
  3. Codelist references  '(Cnnnnnn) DDF codelist' cited by a rule exists in the CT, and matches
                          the codelist the CT gives that entity/attribute
  4. Changelog            the chosen sheet of USDM_CORE_Rules_Changes.xlsx agrees with the rules
                          workbook (DELETED rules not active, NEW rules present, new text applied)
  5. New model content    with --base: properties added since that ref, and whether any active
                          rule covers them (coded attributes need a codelist rule)

Usage:
  python3 rules_audit.py [--repo .] [--ref REF] [--model qea|xmi] [--version-col "Version 4.0"]
                         [--changes-sheet NAME] [--base main] [--out FILE]

Exit status: 1 if any check FAILs. Standard library only.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usdm_lib as U  # noqa: E402

CODED = {"Code", "AliasCode"}
CT_SHEET = "DDF Entities&Attributes"
VVS_SHEET = "DDF valid value sets"


def materialize(repo: Path, ref: str | None, rel: str, tmp: Path) -> Path | None:
    if ref is None:
        p = repo / rel
        return p if p.exists() else None
    data = U.git_show(repo, ref, rel)
    if data is None:
        return None
    p = tmp / (ref.replace("/", "_") + "_" + Path(rel).name)
    p.write_bytes(data)
    return p


def find_col(h: dict[str, int], *needles: str, exact: str | None = None) -> int | None:
    if exact and exact in h:
        return h[exact]
    for name, i in h.items():
        low = name.lower()
        if all(n.lower() in low for n in needles):
            return i
    return None


def split_list(v: str) -> list[str]:
    return [x.strip() for x in re.split(r"[,;\n]", v or "") if x.strip()]


def load_rules(path: Path, version_col: str | None):
    wb = U.read_xlsx(path)
    sheet = next(iter(wb))
    rows = wb[sheet]
    h = U.header_index(rows[0])
    cols = {
        "text": find_col(h, "textual statement"),
        "sev": find_col(h, "warning", "error"),
        "ent": find_col(h, "entit"),
        "attr": find_col(h, "attribute"),
        "ddf": find_col(h, "final core rule id") if find_col(h, "final core rule id") is not None
        else find_col(h, "rule id"),
        "chk": find_col(h, "check_id") if find_col(h, "check_id") is not None else find_col(h, "check"),
        "core": find_col(h, "core-id"),
    }
    vcols = {n: i for n, i in h.items() if n.lower().startswith("version")}
    vc = version_col or (sorted(vcols, key=lambda s: [int(x) for x in re.findall(r"\d+", s)] or [0])[-1]
                         if vcols else None)
    cols["ver"] = vcols.get(vc) if vc else None
    rules = []
    for i, row in enumerate(rows[1:], start=2):
        if not any(row):
            continue
        g = lambda k: U.cell(row, cols[k]) if cols[k] is not None else ""
        rules.append({"row": i, "text": g("text"), "sev": g("sev"), "ent": g("ent"), "attr": g("attr"),
                      "ddf": g("ddf"), "chk": g("chk"), "core": g("core"), "ver": g("ver"),
                      "all_versions": {n: U.cell(row, j) for n, j in vcols.items()}})
    return sheet, vc, cols, rules


def check_structure(r: U.Report, rules, vc, cols):
    S = "1. Workbook structure"
    missing = [k for k, v in cols.items() if v is None]
    if missing:
        r.fail(S, f"could not find column(s) {missing} by header name")
    from collections import Counter
    bad = False
    for key, label in (("chk", "Check_ID"), ("ddf", "DDF rule ID"), ("core", "CORE-ID")):
        dup = [k for k, n in Counter(x[key] for x in rules if x[key] and x[key] != "None").items() if n > 1]
        if dup:
            r.fail(S, f"duplicate {label}: {dup}"); bad = True
    for x in rules:
        if x["sev"].upper() not in ("ERROR", "WARNING"):
            r.warn(S, f"row {x['row']} {x['chk']}: severity `{x['sev']}`"); bad = True
        for n, v in x["all_versions"].items():
            if v.upper() not in ("Y", "N", ""):
                r.warn(S, f"row {x['row']} {x['chk']}: `{n}` = `{v}` (expected Y/N)"); bad = True
    active = [x for x in rules if x["ver"].upper() == "Y"]
    no_core = [x["chk"] for x in active if not x["core"] or x["core"] == "None"]
    if no_core:
        r.warn(S, f"{len(no_core)} rule(s) active for `{vc}` have no CORE-ID: {no_core}"); bad = True
    r.info(S, f"{len(rules)} rules; {len(active)} active for `{vc}`")
    if not bad:
        r.ok(S, "no duplicate IDs; severities and version flags valid")
    return active


def check_model_refs(r: U.Report, active, m: U.Model):
    S = "2. Model references"
    bad = 0
    for x in active:
        ents = split_list(x["ent"])
        if not ents or ents == ["All"]:
            continue
        unknown = [e for e in ents if e not in m.classes]
        for e in unknown:
            r.fail(S, f"{x['chk']} ({x['ddf']}): entity `{e}` is not a UML class"); bad += 1
        known = [e for e in ents if e in m.classes]
        if not known:
            continue
        props: set[str] = set()
        for e in known:
            props |= set(m.all_props(e))
            for sub in m.subclasses(e):
                props |= set(m.all_props(sub))
        for a in split_list(x["attr"]):
            base = a.split(".")[0]
            alt = re.sub(r"Ids?$", "", base)
            if base not in props and alt not in props and base.lower() not in ("all", "n/a"):
                hint = [p for p in props if p.lower() == base.lower() or p.lower().startswith(base.lower()[:6])]
                owners = sorted(c for c, k in m.classes.items() if base in k.props)
                msg = f"{x['chk']} ({x['ddf']}): attribute `{a}` is not on {', '.join(known)}"
                if hint:
                    msg += f" (did you mean {sorted(hint)}?)"
                if owners:
                    msg += f"; `{base}` is defined on {owners}"
                r.fail(S, msg); bad += 1
    if not bad:
        r.ok(S, "every entity and attribute named by an active rule exists in the UML")


def check_codelists(r: U.Report, active, ct_path: Path):
    S = "3. Codelist references"
    wb = U.read_xlsx(ct_path, [CT_SHEET, VVS_SHEET])
    ent_rows = wb[CT_SHEET]
    h = U.header_index(ent_rows[0])
    hvl: dict[tuple[str, str], str] = {}
    all_cl: set[str] = set()
    for row in ent_rows[1:]:
        v = U.cell(row, h.get("Has Value List", -1))
        mm = re.search(r"(C\d{4,})\)", v)
        if mm:
            hvl[(U.cell(row, h["Entity Name"]), U.cell(row, h["Logical Data Model Name"]))] = mm.group(1)
            all_cl.add(mm.group(1))
    vrows = wb.get(VVS_SHEET, [])
    hi = next((i for i, row in enumerate(vrows) if "Codelist C-code" in row), None)
    if hi is not None:
        ci = vrows[hi].index("Codelist C-code")
        all_cl |= {U.cell(row, ci) for row in vrows[hi + 1:] if U.cell(row, ci)}
    bad = 0
    for x in active:
        for code in re.findall(r"\((C\d{4,})\)\s+DDF codelist", x["text"]):
            if code not in all_cl:
                r.fail(S, f"{x['chk']} ({x['ddf']}): cites DDF codelist {code}, which is not in the CT"); bad += 1
                continue
            ents, attrs = split_list(x["ent"]), split_list(x["attr"])
            pairs = [(e, a) for e in ents for a in attrs if (e, a) in hvl]
            mismatched = [(e, a, hvl[(e, a)]) for e, a in pairs if hvl[(e, a)] != code]
            if pairs and len(mismatched) == len(pairs):
                r.warn(S, f"{x['chk']} ({x['ddf']}): cites {code} but the CT gives " +
                          ", ".join(f"`{e}.{a}` {c}" for e, a, c in mismatched)); bad += 1
    if not bad:
        r.ok(S, "every cited DDF codelist exists and matches the CT")


def latest_sheet(names: list[str]) -> str:
    """Sheet for the most recent release, from the version numbers in its name:
    highest target version first, then highest starting version ('4.0 (errata)' > '3.13 -> 4.0')."""
    def key(n: str):
        vers = [tuple(int(p) for p in v.split(".")) for v in re.findall(r"\d+(?:\.\d+)+", n)]
        return (max(vers), vers[0]) if vers else ((0,), (0,))
    return max(names, key=key)


def check_changelog(r: U.Report, rules, vc, ch_path: Path | None, sheet: str | None):
    S = "4. Changelog"
    if ch_path is None:
        r.warn(S, "USDM_CORE_Rules_Changes.xlsx not found")
        return
    wb = U.read_xlsx(ch_path)
    name = sheet or latest_sheet(list(wb))
    if name not in wb:
        r.fail(S, f"sheet `{name}` not found; sheets: {list(wb)}")
        return
    rows = wb[name]
    hrow = next((i for i, row in enumerate(rows) if any("textual statement" in c.lower() for c in row)), 0)
    h = U.header_index(rows[hrow])
    c_change = find_col(h, "change?") if find_col(h, "change?") is not None else find_col(h, "change")
    c_new = find_col(h, "textual statement", "new")
    r.info(S, f"compared sheet `{name}` ({len(rows) - hrow - 1} rows); choose another with --changes-sheet: "
              + ", ".join(f"`{s}`" for s in wb if s != name))
    by_chk = {x["chk"]: x for x in rules}
    bad = 0
    for row in rows[hrow + 1:]:
        if not any(row):
            continue
        chk = next((m.group(0) for c in row for m in [re.search(r"CHK\d{4}", c)] if m), None)
        change = U.cell(row, c_change).upper() if c_change is not None else ""
        if not chk:
            continue
        x = by_chk.get(chk)
        if "DELET" in change:
            if x and x["ver"].upper() == "Y":
                r.fail(S, f"{chk}: marked {change} in the changelog but still active (`{vc}` = Y) in the rules "
                          "workbook"); bad += 1
        elif x is None:
            r.fail(S, f"{chk}: in the changelog ({change or 'no change flag'}) but not in the rules workbook"); bad += 1
        elif c_new is not None:
            new = re.sub(r"\s+", " ", U.cell(row, c_new)).strip()
            cur = re.sub(r"\s+", " ", x["text"]).strip()
            if new and new != cur:
                r.warn(S, f"{chk}: changelog new text differs from the rules workbook\n"
                          f"    changelog: {new[:200]}\n    workbook:  {cur[:200]}"); bad += 1
    if not bad:
        r.ok(S, "changelog sheet agrees with the rules workbook")


def check_new_content(r: U.Report, active, m: U.Model, base_m: U.Model, base: str):
    S = f"5. New model content since `{base}`"
    covered: set[tuple[str, str]] = set()
    for x in active:
        for e in split_list(x["ent"]):
            for a in split_list(x["attr"]):
                covered.add((e, a.split(".")[0]))
    found = False
    for cname, c in sorted(m.classes.items()):
        bc = base_m.classes.get(cname)
        if bc is None:
            r.info(S, f"new class `{cname}`" + (" (abstract)" if c.abstract else ""))
            found = True
        for p in c.props.values():
            if bc is not None and p.name in bc.props:
                continue
            found = True
            targets = [cname] + m.subclasses(cname)
            hit = any((t, p.name) in covered for t in targets)
            desc = f"`{cname}.{p.name}` ({p.type} {p.card})"
            if hit:
                r.ok(S, f"{desc} is referenced by an active rule")
            elif p.type in CODED:
                r.warn(S, f"{desc} is coded but no active rule checks its codelist")
            else:
                r.info(S, f"{desc} is not referenced by any rule (consider conditional/consistency rules)")
    if not found:
        r.ok(S, "no model changes")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--ref", help="audit this git ref instead of the working tree")
    ap.add_argument("--model", choices=["qea", "xmi"], default="qea")
    ap.add_argument("--version-col", help='rules column for the target version (default: highest "Version …")')
    ap.add_argument("--changes-sheet", help="changelog sheet to compare (default: last sheet)")
    ap.add_argument("--base", help="ref to diff the model against for check 5 (e.g. main)")
    ap.add_argument("--out")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    tmp = Path(tempfile.mkdtemp(prefix="usdm-rules-"))
    try:
        get = lambda rel, ref=args.ref: materialize(repo, ref, rel, tmp)
        rules_p = get(U.RULES)
        if rules_p is None:
            sys.exit(f"{U.RULES} not found")
        uml_p = get(U.QEA if args.model == "qea" else U.XMI)
        m = U.load_qea(uml_p) if args.model == "qea" else U.load_xmi(uml_p)
        sheet, vc, cols, rules = load_rules(rules_p, args.version_col)
        r = U.Report(f"CORE rules audit: {'`' + args.ref + '`' if args.ref else 'working tree'} "
                     f"(`{vc}`, UML from `.{args.model}`)")
        active = check_structure(r, rules, vc, cols)
        check_model_refs(r, active, m)
        ct_p = get(U.CT)
        if ct_p:
            check_codelists(r, active, ct_p)
        check_changelog(r, rules, vc, get(U.RULES_CHANGES), args.changes_sheet)
        if args.base:
            base_p = get(U.QEA if args.model == "qea" else U.XMI, args.base)
            base_m = U.load_qea(base_p) if args.model == "qea" else U.load_xmi(base_p)
            check_new_content(r, active, m, base_m, args.base)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    text = r.render()
    print(text)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    sys.exit(1 if r.failed else 0)


if __name__ == "__main__":
    main()
