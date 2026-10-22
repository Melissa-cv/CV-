# -*- coding: utf-8 -*-
"""Convierte data/cv-master.<lang>.md a data/cv.<lang>.json (sin inventar valores).
Uso: python -I scripts/parse_master.py [es|en]   (por defecto es)"""
import re, json, sys, io
ROOT = r"C:\Users\Usuario\Documents\CV"
LANG = sys.argv[1] if len(sys.argv) > 1 else "es"
src = io.open(ROOT + rf"\data\cv-master.{LANG}.md", encoding="utf-8").read()
fm = re.match(r"---\n(.*?)\n---", src, re.S)
data = {"meta": {}}
for l in fm.group(1).splitlines():
    k, v = l.split(":", 1); data["meta"][k.strip()] = v.strip()
body = src[fm.end():]
revisar = re.findall(r"<!--\s*REVISAR:(.*?)-->", body)
body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
def val(v):
    v = v.strip()
    return v
def parse_kv(line):
    m = re.match(r"-\s+([a-z_]+):\s*(.*)$", line)
    return (m.group(1), m.group(2).strip()) if m else None
secs = {}
for sblock in re.split(r"\n## ", "\n" + body)[1:]:
    title, _, rest = sblock.partition("\n")
    title = title.strip()
    if "### " in rest:
        items = []
        for iblock in re.split(r"\n### ", "\n" + rest)[1:]:
            t, _, r = iblock.partition("\n")
            it = {"titulo": t.strip()}
            cur = None
            for line in r.splitlines():
                if re.match(r"\s{2,}-\s", line) and cur:
                    it[cur].append(line.strip()[2:].strip()); continue
                kv = parse_kv(line)
                if kv:
                    k, v = kv
                    if k == "logros": it[k] = []; cur = k
                    else:
                        cur = None
                        if k == "versiones": v = [x.strip() for x in v.split(",") if x.strip()]
                        it[k] = v
            items.append(it)
        secs[title] = items
    else:
        lines = [l for l in rest.splitlines() if l.strip().startswith("-")]
        if title in ("Contacto", "Perfil", "Habilidades"):
            d = {}
            for l in lines:
                kv = parse_kv(l)
                if kv:
                    k, v = kv
                    if "| publico:" in v:
                        v, p = v.split("| publico:"); d[k] = {"valor": v.strip(), "publico": p.strip() == "si"}
                    else: d[k] = v
            secs[title] = d
        else:
            out = []
            for l in lines:
                parts = [p.strip() for p in l.lstrip("- ").split("|")]
                row = {"campos": []}
                for p in parts:
                    m = re.match(r"(versiones|publico|horas|año|institución|nombre|profesion|telefono):\s*(.*)$", p)
                    if m:
                        k, v = m.groups()
                        row[k] = [x.strip() for x in v.split(",") if x.strip()] if k == "versiones" else (v == "si" if k == "publico" else v)
                    else: row["campos"].append(p)
                out.append(row)
            secs[title] = out
data.update(secs)
data["_revisar"] = [r.strip() for r in revisar]
io.open(ROOT + rf"\data\cv.{LANG}.json", "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2))
for k, v in secs.items(): print(k, len(v))
print("REVISAR:", len(revisar))
