# -*- coding: utf-8 -*-
"""Genera el HTML del CV desde data/cv.<lang>.json y la plantilla de la versión.
Uso: python -I scripts/build_cv.py <es|en> <corta|larga> <salida.html>
La versión corta usa templates/cv.html (1 página, con QR a la web);
la larga usa templates/cv-largo.html (hasta 2 páginas)."""
import json, io, re, html, sys
ROOT = r"C:\Users\Usuario\Documents\CV"
LANG, V, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(io.open(ROOT + rf"\data\cv.{LANG}.json", encoding="utf-8"))
e = html.escape
inV = lambda it: V in it.get("versiones", [])
c = d["Contacto"]
FILE = "file:///" + ROOT.replace("\\", "/") + "/"

LBL = {
    "es": {"CONTACTO": "Contacto", "FORMACION": "Formación", "SOFTWARE": "Software", "TECNICAS": "Habilidades técnicas",
           "BLANDAS": "Habilidades blandas", "IDIOMAS": "Idiomas", "PERFIL": "Perfil", "PROYECTOS": "Proyectos destacados",
           "PROYECTOS_L": "Proyectos", "MATERIAS": "Electivas clave", "MATERIAS_L": "Electivas y materias clave",
           "CURSOS": "Cursos y certificaciones", "EXPERIENCIA": "Experiencia", "SEMILLEROS": "Semilleros",
           "ASOC": "Proyecto asociado", "QR": "Versión completa en línea", "QR2": "Escanea el código", "DONE": "(finalizado)"},
    "en": {"CONTACTO": "Contact", "FORMACION": "Education", "SOFTWARE": "Software", "TECNICAS": "Technical skills",
           "BLANDAS": "Soft skills", "IDIOMAS": "Languages", "PERFIL": "Profile", "PROYECTOS": "Featured projects",
           "PROYECTOS_L": "Projects", "MATERIAS": "Key electives", "MATERIAS_L": "Key electives and courses",
           "CURSOS": "Courses and certifications", "EXPERIENCIA": "Experience", "SEMILLEROS": "Research groups",
           "ASOC": "Related project", "QR": "Full version online", "QR2": "Scan the code", "DONE": "(completed)"},
}[LANG]


def cap(s):
    s = s.strip()
    return s[:1].upper() + s[1:]


def link_text(u):
    return re.sub(r"^https?://(www\.)?", "", u).rstrip("/")


contacto = ""
for ic, k in (("@", "email"), ("T", "telefono"), ("L", "ciudad")):
    v = c[k]["valor"]
    if v:
        contacto += f'<li><span class="ic">{ic}</span>{e(v)}</li>'
if c["linkedin"]["valor"]:
    contacto += (f'<li><span class="ic">in</span><a href="{e(c["linkedin"]["valor"])}">'
                 f'{e(link_text(c["linkedin"]["valor"]))}</a></li>')

form = ""
for f in d["Formación"]:
    if not inV(f):
        continue
    a, b = f["titulo"].split(" — ")
    form += f'<li><b>{e(a)}</b>{e(b)}<br>{e(f["periodo"])}</li>'

H = d["Habilidades"]
sw = "".join(f"<span>{e(s.strip())}</span>" for s in H["software"].split(","))
tec = "".join(f"<li>{e(cap(s))}</li>" for s in H["tecnicas"].split(";"))
bl = "".join(f"<span>{e(cap(s))}</span>" for s in H["blandas"].split(","))
idi = "".join(f'<li><b>{e(r["campos"][0])}</b>{e(r["campos"][1])}</li>' for r in d["Idiomas"])

proy = ""
for p in d["Proyectos destacados"]:
    if not inV(p):
        continue
    # Los proyectos se muestran tal como los especificó Melissa: sin herramientas añadidas.
    extra = f' <span class="prob">{e(p["problema"])}.</span>' if V == "larga" and p.get("problema") else ""
    star = " star" if p.get("destacado") == "si" and V == "larga" else ""
    proy += (f'<div class="card{star}"><h3>{e(p["titulo"])}</h3><div class="ctx">{e(p["contexto"])}</div>'
             f'<p>{e(p["que_hice"])}.{extra}</p></div>')

mat = ""
for m in d["Materias y cursos clave"]:
    if not inV(m):
        continue
    if V == "corta":
        if m.get("que_aprendi"):
            mat += f'<div class="card"><h3>{e(m["titulo"])}</h3><p>{e(m["que_aprendi"])}.</p></div>'
    else:
        body = f'{e(m["que_aprendi"])}.' if m.get("que_aprendi") else ""
        asoc = f' <i>{LBL["ASOC"]}: {e(m["proyecto_asociado"])}.</i>' if m.get("proyecto_asociado") else ""
        mat += f'<div class="card"><h3>{e(m["titulo"])}</h3><p>{body}{asoc}</p></div>'

cur = ""
for r in d["Cursos complementarios y certificaciones"]:
    if not inV(r):
        continue
    extra = " · ".join(x for x in r["campos"][1:] if x)
    cur += f'<li><b>{e(r["campos"][0])}</b>' + (f' <span>— {e(extra)}</span>' if extra else "") + "</li>"

sem = ""
for s in d.get("Semilleros y grupos de investigación", []):
    if not inV(s):
        continue
    t, org = s["titulo"].split(" — ")
    sem += (f'<div class="item"><div class="head"><h3>{e(t)}</h3><span class="per">{e(s["periodo"])}</span></div>'
            f'<div class="org">{e(org)} · {e(s["rol"])}</div><ul><li>{e(s["que_hice"])}.</li></ul></div>')

exp = ""
for x in d["Experiencia"]:
    if not inV(x):
        continue
    t, org = x["titulo"].split(" — ")
    per = x["periodo"].replace(" " + LBL["DONE"], "")
    lis = "".join(f"<li>{e(l)}</li>" for l in x["logros"])
    exp += (f'<div class="item"><div class="head"><h3>{e(t)}</h3><span class="per">{e(per)}</span></div>'
            f'<div class="org">{e(org)} · {e(x["ciudad"])}</div><ul>{lis}</ul></div>')

qr = (f'<div class="qr"><img src="{FILE}output/qr-cv.png" alt="QR">'
      f'<p><b>{LBL["QR"]}</b><br>{LBL["QR2"]}</p></div>') if V == "corta" else ""

plain = {"LANG": LANG, "NOMBRE": d["meta"]["nombre"], "TITULO": d["meta"]["titulo_corto"]}
plain.update({"L_" + k: v for k, v in LBL.items() if k.isupper() and k not in ("DONE",)})
raw = {"FOTO": FILE + c["foto"]["valor"], "FOTO_DIV": '<div class="foto"></div>', "CONTACTO": contacto,
       "FORMACION": form, "SOFTWARE": sw, "TECNICAS": tec, "BLANDAS": bl, "IDIOMAS": idi,
       "PERFIL": e(d["Perfil"]["corta" if V == "corta" else "larga"]), "PROYECTOS": proy, "MATERIAS": mat,
       "CURSOS": cur, "SEMILLEROS": sem, "EXPERIENCIA": exp, "QR_BLOCK": qr}
tpl = "cv.html" if V == "corta" else "cv-largo.html"
t = io.open(ROOT + rf"\templates\{tpl}", encoding="utf-8").read()
for k, v in {**{k: e(v) for k, v in plain.items()}, **raw}.items():
    t = t.replace("{{" + k + "}}", v)
io.open(OUT, "w", encoding="utf-8").write(t)
