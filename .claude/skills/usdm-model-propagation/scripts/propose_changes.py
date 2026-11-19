#!/usr/bin/env python3
"""Draft the API, CT and downstream changes that follow from a USDM UML change.

Compares the UML (USDM package of the .qea by default) at --ref (default: working tree) with
--base (default: main), then writes a Markdown "change pack":

  1. UML changes            classes and properties added, removed or changed
  2. UML hygiene            conventions the new content breaks (missing id, lowercase types, …)
  3. API drafts             -Input/-Output schemas for new classes; property and required-list
                            edits for changed classes, in JSON and in the YAML file's style
  4. CT row drafts          'DDF Entities&Attributes' rows (also written as CSV with --csv)
  5. Downstream checklist   examples, mappings, rules, IG, versions affected by the change

Read-only unless --apply is given; --apply writes the section 3 API edits into the working-tree
USDM_API.json (load + dump, byte-identical formatting) and USDM_API.yaml (text insertion), and
--set-version also sets info.version in both. CT and other files are never written.

Usage:
  python3 propose_changes.py [--repo .] [--ref REF] [--base main] [--model qea|xmi]
                             [--out FILE.md] [--csv FILE.csv] [--apply [--set-version X.Y.Z]]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import usdm_lib as U  # noqa: E402

PRIM_JSON = {"string": {"type": "string"}, "boolean": {"type": "boolean"}, "integer": {"type": "integer"},
             "float": {"type": "number"}, "number": {"type": "number"},
             "date": {"type": "string", "format": "date"}, "datetime": {"type": "string", "format": "date-time"}}
CT_SHEET = "DDF Entities&Attributes"
IRREGULAR = {"children": "child", "criteria": "criterion"}


def singular(w: str) -> str:
    if w in IRREGULAR:
        return IRREGULAR[w]
    if w.endswith("ies"):
        return w[:-3] + "y"
    if w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def title(name: str) -> str:
    return name[:1].upper() + name[1:].lower()


def is_prim(t: str) -> bool:
    return t.lower() in PRIM_JSON


# --------------------------------------------------------------------------- inputs
class Src:
    def __init__(self, repo: Path):
        self.repo = repo
        self.tmp = Path(tempfile.mkdtemp(prefix="usdm-prop-"))

    def path(self, ref: str | None, rel: str) -> Path | None:
        if ref is None:
            p = self.repo / rel
            return p if p.exists() else None
        data = U.git_show(self.repo, ref, rel)
        if data is None:
            return None
        p = self.tmp / f"{ref.replace('/', '_')}_{Path(rel).name}"
        p.write_bytes(data)
        return p

    def model(self, ref: str | None, kind: str) -> U.Model:
        p = self.path(ref, U.QEA if kind == "qea" else U.XMI)
        return U.load_qea(p) if kind == "qea" else U.load_xmi(p)


def relationship_types(ds_path: Path | None) -> dict[tuple[str, str], tuple[str, str]]:
    """(class, role) -> (target, 'Value'|'Ref') from dataStructure.yml (line-based read)."""
    out: dict[tuple[str, str], tuple[str, str]] = {}
    if not ds_path:
        return out
    cls = attr = target = None
    for line in ds_path.read_text(encoding="utf-8").splitlines():
        m0 = re.match(r"^(\w+):\s*$", line)
        if m0:
            cls, attr, target = m0.group(1), None, None
            continue
        m4 = re.match(r"^    (\w+):\s*$", line)
        if m4:
            attr, target = m4.group(1), None
            continue
        mt = re.match(r"^      - \$ref: '#/(\w+)'", line)
        if mt and attr:
            target = mt.group(1)
            continue
        mr = re.match(r"^      Relationship Type: (\w+)", line)
        if mr and cls and attr:
            out[(cls, attr)] = (target or "", mr.group(1))
    return out


# --------------------------------------------------------------------------- diff
def diff_models(cur: U.Model, base: U.Model):
    added_cls = sorted(set(cur.classes) - set(base.classes))
    removed_cls = sorted(set(base.classes) - set(cur.classes))
    changes = []  # (class, prop, kind, old Prop|None, new Prop|None)
    for c in sorted(set(cur.classes) & set(base.classes)):
        a, b = base.classes[c], cur.classes[c]
        for p in sorted(set(a.props) | set(b.props)):
            pa, pb = a.props.get(p), b.props.get(p)
            if pa is None:
                changes.append((c, p, "added", None, pb))
            elif pb is None:
                changes.append((c, p, "removed", pa, None))
            elif (pa.type, pa.lower, pa.upper) != (pb.type, pb.lower, pb.upper):
                changes.append((c, p, "changed", pa, pb))
    cls_changes = []
    for c in sorted(set(cur.classes) & set(base.classes)):
        a, b = base.classes[c], cur.classes[c]
        if a.abstract != b.abstract or sorted(a.supers) != sorted(b.supers):
            cls_changes.append((c, a, b))
    return added_cls, removed_cls, changes, cls_changes


# --------------------------------------------------------------------------- API drafts
def rel_kind(m: U.Model, owner: str, p: U.Prop, rels, new_classes: set[str]) -> tuple[str, str]:
    """('Value'|'Ref', reason) for an association."""
    for c in [owner] + m.subclasses(owner):
        if (c, p.name) in rels:
            return rels[(c, p.name)][1], "as already published in dataStructure.yml"
    targets = p.type.split("|")
    if all(t in new_classes for t in targets):
        return "Value", "target class is new, so this association is assumed to own it"
    owned_elsewhere = {t for (c, r), (t, k) in rels.items() if k == "Value"}
    if any(t in owned_elsewhere for t in targets):
        return "Ref", "target is already owned (Value) by another class, so this is assumed to be an id reference"
    return "Value", "target is not owned elsewhere, so this association is assumed to own it"


def ref_schema(m: U.Model, t: str, io: str) -> dict:
    c = m.classes.get(t)
    if c and c.abstract:
        subs = [s for s in m.subclasses(t) if not m.classes[s].abstract]
        return {"anyOf": [{"$ref": f"#/components/schemas/{s}-{io}"} for s in subs]}
    return {"$ref": f"#/components/schemas/{t}-{io}"}


def prop_schema(m: U.Model, owner: str, p: U.Prop, io: str, kind: str) -> tuple[str, dict, bool]:
    """(api property name, JSON schema, required?) for a UML property."""
    name, req = p.name, p.required
    if p.kind == "association" and kind == "Ref":
        name = singular(p.name) + ("Ids" if p.many else "Id")
        base = {"type": "string"}
    elif is_prim(p.type):
        base = dict(PRIM_JSON[p.type.lower()])
        if p.name in ("id", "name") and p.required and not p.many:
            base["minLength"] = 1
    else:
        types = p.type.split("|")
        if len(types) > 1:
            base = {"anyOf": [ref_schema(m, t, io) for t in types]}
        else:
            base = ref_schema(m, types[0], io)
    is_ref_obj = "$ref" in base or ("anyOf" in base and "type" not in base)
    if p.many:
        s = {"items": base, "type": "array", "title": title(name)}
        if not p.required:
            s["default"] = []
        return name, s, p.required
    if not p.required:
        if "anyOf" in base:
            s = {"anyOf": base["anyOf"] + [{"type": "null"}]}
        else:
            s = {"anyOf": [base, {"type": "null"}]}
        if not is_ref_obj:
            s["title"] = title(name)
        return name, s, False
    s = dict(base)
    if not is_ref_obj:
        s["title"] = title(name)
    return name, s, req


def class_schema(m: U.Model, cname: str, io: str, rels, new_classes) -> dict:
    props, required = {}, []
    allp = m.all_props(cname)
    if "id" in allp:
        props["id"] = {"type": "string", "minLength": 1, "title": "Id"}
        required.append("id")
    props["extensionAttributes"] = {"items": {"$ref": f"#/components/schemas/ExtensionAttribute-{io}"},
                                    "type": "array", "title": "Extensionattributes", "default": []}
    for p in allp.values():
        if p.name == "id":
            continue
        kind = rel_kind(m, cname, p, rels, new_classes)[0] if p.kind == "association" else ""
        n, s, req = prop_schema(m, cname, p, io, kind)
        props[n] = s
        if req:
            required.append(n)
    props["instanceType"] = {"type": "string", "enum": [cname], "const": cname, "title": "Instancetype"}
    required.append("instanceType")
    return {"properties": props, "type": "object", "required": required, "title": cname}


# --------------------------------------------------------------------------- YAML emitter
_PLAIN = re.compile(r"^[A-Za-z_][\w .\-/()]*$")


def y_scalar(v) -> str:
    if v is True:
        return "true"
    if v is False:
        return "false"
    if v is None:
        return "null"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if _PLAIN.match(s) and s.lower() not in ("true", "false", "null", "yes", "no", "on", "off"):
        return s
    return "'" + s.replace("'", "''") + "'"


def to_yaml(obj, indent: int = 0) -> list[str]:
    """YAML in the style of USDM_API.yaml: 2-space indent, list items at the key's indent."""
    pad = " " * indent
    out = []
    for k, v in obj.items():
        key = y_scalar(k) if not re.match(r"^\$?[\w\-]+$", str(k)) else str(k)
        if isinstance(v, dict):
            out.append(f"{pad}{key}:")
            out += to_yaml(v, indent + 2)
        elif isinstance(v, list):
            if not v:
                out.append(f"{pad}{key}: []")
                continue
            out.append(f"{pad}{key}:")
            for item in v:
                if isinstance(item, dict):
                    sub = to_yaml(item, indent + 2)
                    sub[0] = pad + "- " + sub[0].lstrip()
                    out += sub
                else:
                    out.append(f"{pad}- {y_scalar(item)}")
        else:
            out.append(f"{pad}{key}: {y_scalar(v)}")
    return out


# --------------------------------------------------------------------------- CT drafts
def ct_role(p: U.Prop) -> str:
    if p.kind == "association":
        return "Relationship"
    return "Attribute" if is_prim(p.type) else "Complex Datatype Relationship"


def ct_rows_for(m: U.Model, entity: str, props: list[tuple[U.Prop, str | None]], with_entity: bool):
    rows = []
    if with_entity:
        c = m.classes[entity]
        rows.append({"Entity Name": entity, "Role": "Entity",
                     "Inherited From": c.supers[0] if c.supers else "",
                     "Logical Data Model Name": entity, "NCI C-code": "TBD", "CT Item Preferred Name": "TBD",
                     "Synonym(s)": "", "Definition": "TBD", "Has Value List": "N/A", "Codelist URL": ""})
    for p, inherited in props:
        if p.name == "id":
            continue
        role = ct_role(p)
        if role == "Relationship":
            tgt = " and ".join(p.type.split("|"))
            rows.append({"Entity Name": entity, "Role": role, "Inherited From": inherited or "",
                         "Logical Data Model Name": p.name, "NCI C-code": "", "CT Item Preferred Name": "",
                         "Synonym(s)": "",
                         "Definition": f"A USDM relationship between the {entity} and {tgt} classes which "
                                       f"identifies the {'set of ' if p.many else ''}<describe> associated with "
                                       f"the <{entity} in words>.",
                         "Has Value List": "N/A", "Codelist URL": ""})
        else:
            coded = p.type in ("Code", "AliasCode")
            rows.append({"Entity Name": entity, "Role": role, "Inherited From": inherited or "",
                         "Logical Data Model Name": p.name, "NCI C-code": "TBD", "CT Item Preferred Name": "TBD",
                         "Synonym(s)": "", "Definition": "TBD",
                         "Has Value List": "Y (<codelist C-code>)" if coded else "N",
                         "Codelist URL": "TBD" if coded else ""})
    return rows


def ct_last_row(ct_path: Path | None) -> dict[str, int]:
    """Entity -> the last 'Row #' (or sheet row) of its block, to say where new rows go."""
    if not ct_path:
        return {}
    rows = U.read_xlsx(ct_path, [CT_SHEET])[CT_SHEET]
    h = U.header_index(rows[0])
    last: dict[str, int] = {}
    for i, row in enumerate(rows[1:], start=2):
        e = U.cell(row, h.get("Entity Name", 1))
        if e:
            last[e] = i
    return last


# --------------------------------------------------------------------------- downstream
def example_usage(repo: Path, ref: str | None, classes: set[str]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    if ref is None:
        files = sorted((repo / "Documents/Examples").rglob("*.json"))
        items = [(str(f.relative_to(repo)), f.read_text(encoding="utf-8", errors="ignore")) for f in files]
    else:
        names = U.git(repo, "ls-tree", "-r", "--name-only", ref, "Documents/Examples").splitlines()
        items = [(n, (U.git_show(repo, ref, n) or b"").decode("utf-8", "ignore")) for n in names if n.endswith(".json")]
    for name, text in items:
        for c in classes:
            n = len(re.findall(rf'"instanceType"\s*:\s*"{re.escape(c)}"', text))
            if n:
                out.setdefault(name, {})[c] = n
    return out


# --------------------------------------------------------------------------- apply
def api_edits(cur: U.Model, added, changes, rels):
    """Edits as data: (schema, op, name, schema-json, required?) with op in
    new_schema / set_prop / del_prop."""
    new_set = set(added)
    edits = []
    for c in added:
        if cur.classes[c].abstract:
            continue
        for io in ("Input", "Output"):
            edits.append((f"{c}-{io}", "new_schema", None, class_schema(cur, c, io, rels, new_set), None))
    for c, prop, kind, old, new in changes:
        for t in cur.concrete_for(c):
            for io in ("Input", "Output"):
                if kind == "removed":
                    edits.append((f"{t}-{io}", "del_prop", prop, None, None))
                    continue
                k = rel_kind(cur, c, new, rels, new_set)[0] if new.kind == "association" else ""
                n, s, req = prop_schema(cur, c, new, io, k)
                edits.append((f"{t}-{io}", "set_prop", n, s, req))
    return edits


def apply_json(path: Path, edits, version: str | None) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    d = json.loads(raw)
    S = d["components"]["schemas"]
    log = []
    for sch, op, name, body, req in edits:
        if op == "new_schema":
            if sch in S:
                log.append(f"JSON: `{sch}` already exists; left unchanged")
                continue
            S[sch] = body
            log.append(f"JSON: added schema `{sch}`")
            continue
        if sch not in S:
            log.append(f"JSON: schema `{sch}` not found; skipped `{name}`")
            continue
        props, required = S[sch]["properties"], S[sch].setdefault("required", [])
        if op == "del_prop":
            props.pop(name, None)
            if name in required:
                required.remove(name)
            log.append(f"JSON: removed `{sch}.{name}`")
            continue
        items = [(k, v) for k, v in props.items() if k != name]
        pos = next((i for i, (k, _) in enumerate(items) if k == "instanceType"), len(items))
        items.insert(pos, (name, body))
        S[sch]["properties"] = dict(items)
        if req and name not in required:
            rpos = required.index("instanceType") if "instanceType" in required else len(required)
            required.insert(rpos, name)
        if not req and name in required:
            required.remove(name)
        log.append(f"JSON: set `{sch}.{name}`" + (" (required)" if req else ""))
    d["components"]["schemas"] = dict(sorted(S.items()))
    if version:
        d["info"]["version"] = version
        log.append(f"JSON: info.version = {version}")
    out = json.dumps(d, indent=2)
    path.write_text(out + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
    return log


def _block(lines: list[str], start: int, indent: int) -> int:
    """Index after the YAML block that starts at `start` (a key at `indent`)."""
    i = start + 1
    while i < len(lines):
        ln = lines[i]
        if ln.strip() and (len(ln) - len(ln.lstrip(" "))) <= indent and not ln.lstrip().startswith("- ") \
                or (ln.strip() and (len(ln) - len(ln.lstrip(" "))) < indent):
            break
        i += 1
    return i


def apply_yaml(path: Path, edits, version: str | None) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    log = []
    sch_start = next(i for i, ln in enumerate(lines) if ln == "  schemas:")
    sch_end = _block(lines, sch_start, 2)

    def find_schema(name):
        for i in range(sch_start + 1, sch_end):
            if re.match(rf"^    '?{re.escape(name)}'?:\s*$", lines[i]):
                return i
        return None

    for sch, op, name, body, req in edits:
        if op == "new_schema":
            if find_schema(sch) is not None:
                log.append(f"YAML: `{sch}` already exists; left unchanged")
                continue
            names = [(i, re.match(r"^    '?([^':]+)'?:\s*$", lines[i]).group(1)) for i in range(sch_start + 1, sch_end)
                     if re.match(r"^    \S[^:]*:\s*$", lines[i])]
            at = next((i for i, n in names if n > sch), sch_end)
            new = to_yaml({sch: body}, 4)
            lines[at:at] = new
            sch_end += len(new)
            log.append(f"YAML: added schema `{sch}`")
            continue
        s = find_schema(sch)
        if s is None:
            log.append(f"YAML: schema `{sch}` not found; skipped `{name}`")
            continue
        e = _block(lines, s, 4)
        p = next((i for i in range(s, e) if lines[i] == "      properties:"), None)
        pe = _block(lines, p, 6)
        cur_i = next((i for i in range(p + 1, pe) if re.match(rf"^        {re.escape(name)}:", lines[i])), None)
        if cur_i is not None:
            ce = _block(lines, cur_i, 8)
            del lines[cur_i:ce]
            delta = -(ce - cur_i)
            sch_end += delta
            pe += delta
            e += delta
        if op == "set_prop":
            it = next((i for i in range(p + 1, pe) if lines[i] == "        instanceType:"), pe)
            new = to_yaml({name: body}, 8)
            lines[it:it] = new
            sch_end += len(new)
            e += len(new)
        rq = next((i for i in range(s, e) if lines[i] == "      required:"), None)
        if rq is not None:
            re_ = _block(lines, rq, 6)
            entry = next((i for i in range(rq + 1, re_) if lines[i].strip() in (f"- {name}", f"- '{name}'")), None)
            if entry is not None and not (op == "set_prop" and req):
                del lines[entry]
                sch_end -= 1
            elif entry is None and op == "set_prop" and req:
                it = next((i for i in range(rq + 1, re_) if lines[i].strip() == "- instanceType"), re_)
                lines.insert(it, f"      - {name}")
                sch_end += 1
        log.append(f"YAML: {'removed' if op == 'del_prop' else 'set'} `{sch}.{name}`" +
                   (" (required)" if req else ""))
    if version:
        for i, ln in enumerate(lines):
            if ln == "info:":
                for j in range(i + 1, len(lines)):
                    if re.match(r"^  version:", lines[j]):
                        lines[j] = f"  version: {version}"
                        log.append(f"YAML: info.version = {version}")
                        break
                    if lines[j] and not lines[j].startswith(" "):
                        break
                break
    path.write_text("\n".join(lines), encoding="utf-8")
    return log


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--ref", help="model to propose changes for (default: working tree)")
    ap.add_argument("--base", default="main", help="previous release to diff against (default: main)")
    ap.add_argument("--model", choices=["qea", "xmi"], default="qea")
    ap.add_argument("--out", help="write the Markdown change pack here (default: stdout)")
    ap.add_argument("--csv", help="also write the CT row drafts as CSV (columns of 'DDF Entities&Attributes')")
    ap.add_argument("--apply", action="store_true",
                    help="write the section 3 API edits into the working-tree USDM_API.json and USDM_API.yaml")
    ap.add_argument("--set-version", help="with --apply, also set info.version in both API files (e.g. 4.1.0)")
    args = ap.parse_args()
    if args.apply and args.ref:
        sys.exit("--apply edits the working tree; run it without --ref")

    repo = Path(args.repo).resolve()
    src = Src(repo)
    try:
        cur, base = src.model(args.ref, args.model), src.model(args.base, args.model)
        rels = relationship_types(src.path(args.ref, U.DATA_STRUCTURE))
        ct_last = ct_last_row(src.path(args.ref, U.CT))
        added, removed, changes, cls_changes = diff_models(cur, base)
        new_set = set(added)
        L: list[str] = []
        w = L.append
        label = args.ref or "working tree"
        w(f"# USDM change pack: `{label}` vs `{args.base}`\n")
        w(f"UML source: `.{args.model}`. Generated drafts: every `TBD` and `<…>` needs a person (C-codes, "
          "definitions, codelists, wording). Nothing in the repository was changed.\n")

        # 1 ------------------------------------------------------------------
        w("## 1. UML changes\n")
        if not (added or removed or changes or cls_changes):
            w("No differences in the USDM package.\n")
        for c in added:
            k = cur.classes[c]
            w(f"- **New class `{c}`**" + (" (abstract)" if k.abstract else "") +
              (f", specialises {k.supers}" if k.supers else ""))
            for p in k.props.values():
                w(f"  - `{p.name}`: {p.type} {p.card} ({p.kind})")
        for c in removed:
            w(f"- **Removed class `{c}`**")
        for c, prop, kind, old, new in changes:
            if kind == "added":
                w(f"- `{c}.{prop}` added: {new.type} {new.card} ({new.kind})")
            elif kind == "removed":
                w(f"- `{c}.{prop}` removed (was {old.type} {old.card})")
            else:
                w(f"- `{c}.{prop}` changed: {old.type} {old.card} → {new.type} {new.card}")
        for c, a, b in cls_changes:
            w(f"- `{c}` class change: abstract {a.abstract}→{b.abstract}, supers {a.supers}→{b.supers}")
        w("")

        # 2 ------------------------------------------------------------------
        w("## 2. UML hygiene\n")
        hyg = 0
        no_id = sorted(n for n, c in base.classes.items() if not c.abstract and "id" not in base.all_props(n))
        for c in added:
            k = cur.classes[c]
            if not k.abstract and "id" not in cur.all_props(c):
                w(f"- `{c}` has no `id`. " + (f"Every concrete class in `{args.base}` has `id` (own or inherited) "
                  "and every API schema requires it." if not no_id else
                  f"Concrete classes without one in `{args.base}`: {', '.join(no_id)}; confirm which pattern applies."))
                hyg += 1
        touched = [(c, p) for c in added for p in cur.classes[c].props.values()] + \
                  [(c, new) for c, _, kind, _, new in changes if new is not None]
        for c, p in touched:
            if p.kind == "attribute" and is_prim(p.type) and p.type != p.type[:1].upper() + p.type[1:]:
                w(f"- `{c}.{p.name}` uses type `{p.type}`; the model convention is `{p.type[:1].upper() + p.type[1:]}`.")
                hyg += 1
        for c, prop, kind, old, new in changes:
            if kind == "added" and new.required:
                concrete = cur.concrete_for(c)
                w(f"- `{c}.{prop}` is required ({new.card}). Every existing `{', '.join(concrete)}` instance "
                  f"(including the examples) becomes invalid: a breaking change unless it is made optional.")
                hyg += 1
            if kind == "changed" and old.type != new.type and old.type in ("Code", "AliasCode"):
                w(f"- `{c}.{prop}` changed from {old.type} to {new.type}: it can no longer be validated against "
                  "a codelist. Confirm that is intended.")
                hyg += 1
        if not hyg:
            w("No issues found.")
        w("")

        # 3 ------------------------------------------------------------------
        w("## 3. API drafts (`USDM_API.json` and `USDM_API.yaml`)\n")
        w("Make every edit in both files. Each class has an `-Input` and an `-Output` schema; they differ only "
          "in the `-Input`/`-Output` suffix of `$ref`s.\n")
        assoc_notes = []
        for c in added:
            if cur.classes[c].abstract:
                w(f"### `{c}` (abstract): no schema; its properties go on each concrete subclass\n")
                continue
            for io in ("Input", "Output"):
                sch = class_schema(cur, c, io, rels, new_set)
                w(f"### New schema `{c}-{io}`\n")
                w("```json")
                w(f'"{c}-{io}": ' + json.dumps(sch, indent=2))
                w("```\n")
                w("YAML (under `components: schemas:`, alphabetical position):\n")
                w("```yaml")
                L.extend(to_yaml({f"{c}-{io}": sch}, 4))
                w("```\n")
            for p in cur.all_props(c).values():
                if p.kind == "association":
                    k, why = rel_kind(cur, c, p, rels, new_set)
                    assoc_notes.append(f"`{c}.{p.name}` → **{k}** ({why})")
        by_class: dict[str, list] = {}
        for c, prop, kind, old, new in changes:
            by_class.setdefault(c, []).append((prop, kind, old, new))
        for c, items in by_class.items():
            targets = cur.concrete_for(c)
            w(f"### Changes to `{c}`" + (f" (apply to {', '.join(f'`{t}`' for t in targets)})"
                                         if targets != [c] else "") + "\n")
            for prop, kind, old, new in items:
                if kind == "removed":
                    w(f"- Remove property `{prop}` (and from `required`) in every `-Input`/`-Output` schema above.")
                    continue
                k = rel_kind(cur, c, new, rels, new_set) if new.kind == "association" else ("", "")
                if new.kind == "association":
                    assoc_notes.append(f"`{c}.{prop}` → **{k[0]}** ({k[1]})")
                for io in ("Input", "Output"):
                    n, s, req = prop_schema(cur, c, new, io, k[0])
                    w(f"- `-{io}`: {'set' if kind == 'changed' else 'add'} property `{n}`"
                      + ("; add to `required`" if req else "; not required") + ":")
                    w("  ```json")
                    w("  " + json.dumps({n: s}))
                    w("  ```")
                    w("  ```yaml")
                    L.extend("  " + line for line in to_yaml({n: s}, 0))
                    w("  ```")
            w("")
        if assoc_notes:
            w("### Association form: confirm each\n")
            w("The UML does not say whether an association is an owned object (**Value**: nested schema) or an "
              "id reference (**Ref**: `<role>Id` / `<role>Ids` string). The drafts above assume:\n")
            for n in assoc_notes:
                w(f"- {n}")
            w("")
        w("Also bump `info.version` in both API files to the release version.\n")

        # 4 ------------------------------------------------------------------
        w("## 4. CT row drafts (`USDM_CT.xlsx`, sheet `DDF Entities&Attributes`)\n")
        w("Conventions: no row for `id`; primitives are `Attribute`; Code/Quantity/… typed attributes are "
          "`Complex Datatype Relationship`; class associations are `Relationship` (no C-code, templated "
          "definition, `N/A`). Subclasses repeat inherited rows with `Inherited From` set. Every row must come "
          "after its entity's `Entity` row, or DDF-RA-Tools stops with KeyError.\n")
        all_rows = []
        for c in added:
            k = cur.classes[c]
            if k.abstract:
                continue
            props = []
            for p in cur.all_props(c).values():
                owner = next((s for s in k.supers if p.name in cur.all_props(s)), None)
                props.append((p, owner))
            all_rows += ct_rows_for(cur, c, props, True)
        for c, items in by_class.items():
            for t in cur.concrete_for(c):
                props = [(new, c if t != c else None) for _, kind, _, new in items if kind in ("added",)]
                rows = ct_rows_for(cur, t, props, False)
                if rows:
                    where = f"after sheet row {ct_last[t]}" if t in ct_last else "after its Entity row"
                    w(f"- `{t}`: add {len(rows)} row(s) {where} (end of the `{t}` block)")
                all_rows += rows
            for prop, kind, old, new in items:
                if kind == "removed":
                    w(f"- Remove the `{prop}` rows for {', '.join(cur.concrete_for(c)) or c}")
                elif kind == "changed":
                    w(f"- Review the `{prop}` rows for {', '.join(cur.concrete_for(c)) or c} "
                      f"(Role / Has Value List may change: {old.type} {old.card} → {new.type} {new.card})")
        cols = ["Entity Name", "Role", "Inherited From", "Logical Data Model Name", "NCI C-code",
                "CT Item Preferred Name", "Synonym(s)", "Definition", "Has Value List", "Codelist URL"]
        if all_rows:
            w("")
            w("| " + " | ".join(cols) + " |")
            w("|" + " -- |" * len(cols))
            for row in all_rows:
                w("| " + " | ".join(str(row[c]).replace("|", "\\|") for c in cols) + " |")
            w("")
            w("For each coded attribute, add the codelist to `DDF valid value sets` if it is a new DDF "
              "codelist, and record the change in `USDM_CT_Changes.xlsx`. The `ncit-concept-resolver` agent can "
              "look up candidate C-codes and definitions.\n")
        if args.csv and all_rows:
            with open(args.csv, "w", newline="", encoding="utf-8") as f:
                wr = csv.DictWriter(f, fieldnames=cols)
                wr.writeheader()
                wr.writerows(all_rows)
            w(f"CT drafts also written to `{args.csv}`.\n")

        # 5 ------------------------------------------------------------------
        w("## 5. Downstream checklist\n")
        affected = set(added) | set(by_class)
        concrete_aff = set()
        for c in affected:
            concrete_aff |= set(cur.concrete_for(c)) | {c}
        owners = {c for c, k in cur.classes.items() for p in k.props.values()
                  if p.kind == "association" and set(p.type.split("|")) & set(added)}
        concrete_aff |= {s for o in owners for s in cur.concrete_for(o)}
        usage = example_usage(repo, args.ref, concrete_aff)
        w("- [ ] Export `USDM_UML.xmi` (and PNG views) from EA; set the `USDM` diagram version")
        w("- [ ] Apply section 3 to `USDM_API.json` and `USDM_API.yaml`; bump `info.version`")
        w("- [ ] Apply section 4 to `USDM_CT.xlsx`; log in `USDM_CT_Changes.xlsx`")
        w("- [ ] Run the `usdm-release-check` skill, push, let CI regenerate, pull, confirm `alignment.csv` is header-only")
        w("- [ ] CORE rules: run the `usdm-core-rules-audit` skill with `--base " + args.base +
          "`; add codelist rules for new coded attributes; record in `USDM_CORE_Rules_Changes.xlsx`")
        if usage:
            w("- [ ] Example files that contain affected classes (update them and `usdmVersion`):")
            for f, cs in sorted(usage.items()):
                w(f"  - `{f}`: " + ", ".join(f"{c} ×{n}" for c, n in sorted(cs.items())))
        else:
            w("- [ ] Example files: none contain the affected classes; update `usdmVersion` only")
        w("- [ ] `Documents/Mappings/*.xlsx`: map M11 / ClinicalTrials.gov / CTIS / SDTM fields to the new content")
        w("- [ ] Informative model diagram (`Documents/DDF USDM Model Informative.*`)")
        w("- [ ] Implementation Guide (`Deliverables/IG/USDM-IG.pdf`)")
        if args.apply:
            edits = api_edits(cur, added, changes, rels)
            log = apply_json(repo / U.API_JSON, edits, args.set_version)
            log += apply_yaml(repo / U.API_YAML, edits, args.set_version)
            w("\n## Applied to the working tree\n")
            L.extend(f"- {x}" for x in log)
        text = "\n".join(L) + "\n"
    finally:
        shutil.rmtree(src.tmp, ignore_errors=True)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
