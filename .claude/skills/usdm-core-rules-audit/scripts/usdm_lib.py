"""Shared, dependency-free readers for the DDF-RA (USDM) deliverables.

Standard library only (sqlite3, zipfile, xml.etree, json), so the scripts run without
openpyxl, PyYAML or xmlstarlet. The same file is shipped in each usdm-* skill's
scripts/ folder; keep the copies identical.

Readers:
    load_qea(path)          Enterprise Architect project (SQLite)  -> Model
    load_xmi(path)          EA XMI 2.5 export                      -> Model
    xmi_diagram_version()   version of the 'USDM' Logical diagram in an XMI
    qea_diagram_version()   same, from the .qea
    load_api_json(path)     OpenAPI JSON                           -> dict of schemas
    yaml_schemas(path)      schema -> property names/required, from USDM_API.yaml
    read_xlsx(path)         {sheet: [[cell str, ...], ...]}
    git_show(repo, ref, p)  file bytes at a git ref
"""
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

# Repository-relative paths of the canonical artifacts.
QEA = "Deliverables/UML/USDM_UML.qea"
XMI = "Deliverables/UML/USDM_UML.xmi"
API_JSON = "Deliverables/API/USDM_API.json"
API_YAML = "Deliverables/API/USDM_API.yaml"
CT = "Deliverables/CT/USDM_CT.xlsx"
RULES = "Deliverables/RULES/USDM_CORE_Rules.xlsx"
RULES_CHANGES = "Deliverables/RULES/USDM_CORE_Rules_Changes.xlsx"
DATA_STRUCTURE = "Deliverables/UML/dataStructure.yml"

PRIMITIVES = {"string", "boolean", "integer", "float", "date", "datetime", "number"}


# --------------------------------------------------------------------------- model
@dataclass
class Prop:
    name: str
    type: str
    lower: str
    upper: str
    kind: str  # "attribute" or "association"

    @property
    def card(self) -> str:
        if self.lower == self.upper:
            return self.lower
        return f"{self.lower}..{self.upper}"

    @property
    def many(self) -> bool:
        return self.upper not in ("0", "1")

    @property
    def required(self) -> bool:
        return self.lower not in ("0", "")


@dataclass
class Cls:
    name: str
    abstract: bool = False
    supers: list[str] = field(default_factory=list)
    props: dict[str, Prop] = field(default_factory=dict)


@dataclass
class Model:
    source: str
    classes: dict[str, Cls] = field(default_factory=dict)

    def all_props(self, cname: str) -> dict[str, Prop]:
        """Own plus inherited properties (inherited first, own override)."""
        out: dict[str, Prop] = {}
        c = self.classes.get(cname)
        if not c:
            return out
        for s in c.supers:
            out.update(self.all_props(s))
        out.update(c.props)
        return out

    def subclasses(self, cname: str) -> list[str]:
        direct = [n for n, c in self.classes.items() if cname in c.supers]
        out = list(direct)
        for d in direct:
            out += self.subclasses(d)
        return out

    def concrete_for(self, cname: str) -> list[str]:
        """The concrete classes that carry cname's properties in the API."""
        c = self.classes.get(cname)
        if c and not c.abstract:
            return [cname] + [s for s in self.subclasses(cname) if not self.classes[s].abstract]
        return [s for s in self.subclasses(cname) if not self.classes[s].abstract]


def _card(lo, hi):
    lo = "" if lo is None else str(lo).strip()
    hi = "" if hi is None else str(hi).strip()
    if hi in ("-1",):
        hi = "*"
    return lo, hi


def _add_assoc(c: Cls, role: str, target: str, lo: str, hi: str):
    """Add an association end; a role reused for several targets (e.g. Condition.appliesTo)
    becomes one property whose type lists every target ('A|B') with the widest cardinality."""
    p = c.props.get(role)
    if p is None or p.kind != "association":
        c.props[role] = Prop(role, target, lo, hi, "association")
        return
    types = sorted(set(p.type.split("|")) | {target})
    lo2 = min([x for x in (p.lower, lo) if x != ""], default="", key=lambda v: int(v) if v.isdigit() else 0)
    hi2 = "*" if "*" in (p.upper, hi) else max(p.upper, hi)
    c.props[role] = Prop(role, "|".join(types), lo2, hi2, "association")


def _split_card(card: str | None):
    card = (card or "").strip()
    if ".." in card:
        lo, hi = card.split("..", 1)
        return lo.strip(), hi.strip()
    return (card, card) if card else ("", "")


def qea_packages(path: str | Path) -> dict[str, list[str]]:
    """Package name -> class names, for every package holding classes."""
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    out: dict[str, list[str]] = {}
    for pkg, cls in db.execute(
        "select p.Name, o.Name from t_object o join t_package p on p.Package_ID=o.Package_ID "
        "where o.Object_Type='Class' order by 1, 2"
    ):
        out.setdefault(pkg, []).append(cls)
    db.close()
    return out


def load_qea(path: str | Path, package: str | None = "USDM") -> Model:
    """Classes, attributes, associations and generalizations from an EA .qea (SQLite).

    Only classes in `package` are loaded (default 'USDM', the package exported to the XMI);
    pass None for every package."""
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    m = Model(source=str(path))
    pkg_filter = ""
    params: tuple = ()
    if package:
        pkg_filter = " and o.Package_ID in (select Package_ID from t_package where Name=?)"
        params = (package,)
    for oid, name, abstract in db.execute(
        "select o.Object_ID, o.Name, o.Abstract from t_object o where o.Object_Type='Class'" + pkg_filter,
        params,
    ):
        m.classes[name] = Cls(name=name, abstract=str(abstract) == "1")
    for cname, aname, atype, lo, hi in db.execute(
        "select o.Name, a.Name, a.Type, a.LowerBound, a.UpperBound from t_attribute a "
        "join t_object o on o.Object_ID=a.Object_ID where o.Object_Type='Class'" + pkg_filter,
        params,
    ):
        lo, hi = _card(lo, hi)
        m.classes[cname].props[aname] = Prop(aname, atype or "", lo, hi, "attribute")
    for ctype, src, dst, cname, dcard, drole in db.execute(
        "select c.Connector_Type, s.Name, d.Name, c.Name, c.DestCard, c.DestRole from t_connector c "
        "join t_object s on s.Object_ID=c.Start_Object_ID join t_object d on d.Object_ID=c.End_Object_ID "
        "where s.Object_Type='Class' and d.Object_Type='Class' "
        "and c.Connector_Type in ('Association','Aggregation','Generalization')"
    ):
        if src not in m.classes or dst not in m.classes:
            continue
        if ctype == "Generalization":
            if dst not in m.classes[src].supers:
                m.classes[src].supers.append(dst)
            continue
        role = (drole or cname or "").strip()
        if not role:
            continue
        lo, hi = _split_card(dcard)
        _add_assoc(m.classes[src], role, dst, lo, hi)
    db.close()
    return m


def qea_diagram_version(path: str | Path, diagram: str = "USDM") -> str | None:
    db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    row = db.execute(
        "select Version from t_diagram where Name=? and Diagram_Type='Logical'", (diagram,)
    ).fetchone()
    db.close()
    return row[0] if row else None


_XMI_NS = "{http://www.omg.org/spec/XMI/20131001}"


def _xmi_root(path_or_bytes):
    data = path_or_bytes if isinstance(path_or_bytes, bytes) else Path(path_or_bytes).read_bytes()
    return ET.fromstring(data)


def load_xmi(path_or_bytes, source: str | None = None) -> Model:
    """Classes, attributes, associations and generalizations from an EA XMI export."""
    root = _xmi_root(path_or_bytes)
    m = Model(source=source or str(path_or_bytes if not isinstance(path_or_bytes, bytes) else "<bytes>"))
    xid = f"{_XMI_NS}id"
    xtype = f"{_XMI_NS}type"
    xidref = f"{_XMI_NS}idref"
    ids: dict[str, str] = {}
    assoc_names: dict[str, str] = {}
    class_elems = []
    for el in root.iter("packagedElement"):
        t = el.get(xtype)
        if t == "uml:Class":
            ids[el.get(xid)] = el.get("name")
            class_elems.append(el)
        elif t == "uml:Association":
            assoc_names[el.get(xid)] = el.get("name") or ""
    for el in class_elems:
        c = Cls(name=el.get("name"), abstract=el.get("isAbstract") == "true")
        m.classes[c.name] = c
    for el in class_elems:
        c = m.classes[el.get("name")]
        for g in el.findall("generalization"):
            sup = ids.get(g.get("general"))
            if sup and sup not in c.supers:
                c.supers.append(sup)
        for a in el.findall("ownedAttribute"):
            t_el = a.find("type")
            tref = (t_el.get(xidref) or "") if t_el is not None else ""
            href = (t_el.get("href") or "") if t_el is not None else ""
            typ = ids.get(tref) or tref.replace("EAJava_", "") or href.rsplit("#", 1)[-1]
            lo_el, hi_el = a.find("lowerValue"), a.find("upperValue")
            lo, hi = _card(
                lo_el.get("value") if lo_el is not None else "",
                hi_el.get("value") if hi_el is not None else "",
            )
            if a.get("association"):
                role = a.get("name") or assoc_names.get(a.get("association"), "")
                if role:
                    _add_assoc(c, role, typ, lo, hi)
            else:
                c.props[a.get("name")] = Prop(a.get("name"), typ, lo, hi, "attribute")
    return m


def xmi_diagram_version(path_or_bytes, diagram: str = "USDM") -> str | None:
    """project/@version of the diagram whose properties are name=<diagram>, type=Logical
    (the same value the CI workflow reads with xmlstarlet)."""
    root = _xmi_root(path_or_bytes)
    for d in root.iter("diagram"):
        p = d.find("properties")
        if p is not None and p.get("name") == diagram and p.get("type") == "Logical":
            proj = d.find("project")
            return proj.get("version") if proj is not None else None
    return None


# --------------------------------------------------------------------------- API
def load_api_json(path_or_bytes) -> dict:
    data = path_or_bytes if isinstance(path_or_bytes, bytes) else Path(path_or_bytes).read_bytes()
    return json.loads(data)


ITEM_BOUNDS = ("minItems", "maxItems")


def api_schema_props(api: dict) -> dict[str, dict]:
    """schema name -> {'props': set, 'required': set,
                       'additionalProperties': value or None if absent,
                       'bounds': {prop: {'minItems': n, 'maxItems': n}} (only props that set one)}"""
    out = {}
    for name, s in api.get("components", {}).get("schemas", {}).items():
        props = s.get("properties", {})
        bounds = {}
        for p, v in props.items():
            b = {k: v[k] for k in ITEM_BOUNDS if isinstance(v, dict) and k in v}
            if b:
                bounds[p] = b
        out[name] = {"props": set(props), "required": set(s.get("required", [])),
                     "additionalProperties": s.get("additionalProperties"), "bounds": bounds}
    return out


def _yaml_scalar(v: str):
    v = v.strip().strip("'\"")
    if v in ("true", "false"):
        return v == "true"
    return int(v) if re.fullmatch(r"-?\d+", v) else v


def yaml_info_version(path: str | Path) -> str | None:
    in_info = False
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if re.match(r"^info:\s*$", line):
            in_info = True
            continue
        if in_info:
            if line and not line.startswith(" "):
                break
            mm = re.match(r"^  version:\s*['\"]?([^'\"\s]+)", line)
            if mm:
                return mm.group(1)
    return None


def yaml_schemas(path: str | Path) -> dict[str, dict]:
    """Indentation-based read of components/schemas in USDM_API.yaml (2-space indent, as
    produced by the project's tooling). Returns the same shape as api_schema_props():
    schema -> {'props', 'required', 'additionalProperties', 'bounds'}."""
    out: dict[str, dict] = {}
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    in_schemas = False
    cur = None
    section = None
    prop = None
    for line in lines:
        if re.match(r"^  schemas:\s*$", line):
            in_schemas = True
            continue
        if not in_schemas:
            continue
        if line and not line.startswith("  "):
            break  # left components
        m4 = re.match(r"^    ([^\s:][^:]*):\s*$", line)
        if m4:
            cur = m4.group(1).strip("'\"")
            out[cur] = {"props": set(), "required": set(), "additionalProperties": None, "bounds": {}}
            section = prop = None
            continue
        if cur is None:
            continue
        m6 = re.match(r"^      (\w+):\s*(.*)$", line)
        if m6:
            section, prop = m6.group(1), None
            if section == "additionalProperties" and m6.group(2).strip():
                out[cur]["additionalProperties"] = _yaml_scalar(m6.group(2))
            continue
        if section == "properties":
            m8 = re.match(r"^        ([^\s:][^:]*):", line)
            if m8:
                prop = m8.group(1).strip("'\"")
                out[cur]["props"].add(prop)
                continue
            mb = re.match(r"^          (minItems|maxItems):\s*(\S+)\s*$", line)
            if mb and prop:
                out[cur]["bounds"].setdefault(prop, {})[mb.group(1)] = _yaml_scalar(mb.group(2))
        elif section == "required":
            mr = re.match(r"^      - (.+?)\s*$", line)
            if mr:
                out[cur]["required"].add(mr.group(1).strip("'\""))
    return out


# --------------------------------------------------------------------------- xlsx
_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def _col_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_xlsx(path_or_bytes, sheets: list[str] | None = None) -> dict[str, list[list[str]]]:
    """Cell values as strings ('' for empty), using cached values for formulas."""
    import io

    src = io.BytesIO(path_or_bytes) if isinstance(path_or_bytes, bytes) else path_or_bytes
    out: dict[str, list[list[str]]] = {}
    with zipfile.ZipFile(src) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            sroot = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in sroot.findall("m:si", _NS):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{_NS['m']}}}t")))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = {r.get("Id"): r.get("Target") for r in rels}
        for sh in wb.find("m:sheets", _NS):
            name = sh.get("name")
            if sheets and name not in sheets:
                continue
            t = target[sh.get(_REL)].lstrip("/")
            t = t if t.startswith("xl/") else "xl/" + t
            root = ET.fromstring(z.read(t))
            rows: list[list[str]] = []
            for r in root.iter(f"{{{_NS['m']}}}row"):
                idx = int(r.get("r")) - 1
                while len(rows) < idx:
                    rows.append([])
                vals: list[str] = []
                for c in r.findall("m:c", _NS):
                    ci = _col_index(c.get("r"))
                    while len(vals) < ci:
                        vals.append("")
                    t_ = c.get("t")
                    v = c.find("m:v", _NS)
                    if t_ == "s" and v is not None:
                        val = shared[int(v.text)]
                    elif t_ == "inlineStr":
                        val = "".join(x.text or "" for x in c.iter(f"{{{_NS['m']}}}t"))
                    elif t_ == "b" and v is not None:
                        val = "TRUE" if v.text == "1" else "FALSE"
                    else:
                        val = v.text if v is not None and v.text is not None else ""
                    vals.append(val.strip())
                rows.append(vals)
            out[name] = rows
    return out


def cell(row: list[str], i: int) -> str:
    return row[i] if 0 <= i < len(row) else ""


def header_index(row: list[str]) -> dict[str, int]:
    return {h.strip(): i for i, h in enumerate(row) if h and h.strip()}


# --------------------------------------------------------------------------- git
def git(repo: str | Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def git_show(repo: str | Path, ref: str, relpath: str) -> bytes | None:
    r = subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{relpath}"], capture_output=True
    )
    return r.stdout if r.returncode == 0 else None


def hyphen(v: str | None) -> str:
    """CI normalisation: first space-separated token, dots -> hyphens."""
    return (v or "").split(" ")[0].replace(".", "-")


# --------------------------------------------------------------------------- report
class Report:
    def __init__(self, title: str):
        self.title = title
        self.items: list[tuple[str, str, str]] = []  # (status, section, message)

    def add(self, status: str, section: str, msg: str):
        self.items.append((status, section, msg))

    def ok(self, s, m):
        self.add("PASS", s, m)

    def warn(self, s, m):
        self.add("WARN", s, m)

    def fail(self, s, m):
        self.add("FAIL", s, m)

    def info(self, s, m):
        self.add("INFO", s, m)

    @property
    def failed(self) -> bool:
        return any(st == "FAIL" for st, _, _ in self.items)

    def render(self) -> str:
        icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌", "INFO": "ℹ️"}
        out = [f"# {self.title}", ""]
        counts = {k: sum(1 for s, _, _ in self.items if s == k) for k in icon}
        out.append(" · ".join(f"{icon[k]} {k} {v}" for k, v in counts.items() if v))
        sections: dict[str, list] = {}
        for st, sec, msg in self.items:
            sections.setdefault(sec, []).append((st, msg))
        for sec, items in sections.items():
            out += ["", f"## {sec}", ""]
            out += [f"- {icon[st]} {msg}" for st, msg in items]
        return "\n".join(out) + "\n"
