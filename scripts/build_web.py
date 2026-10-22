# -*- coding: utf-8 -*-
"""Genera docs/index.html (GitHub Pages) bilingüe ES/EN desde data/cv.es.json y data/cv.en.json.
Privacidad: sin correo, teléfono, ciudad, foto, referencias ni PDF. Único contacto: LinkedIn (publico: si).
Uso: python -I scripts/build_web.py"""
import json, io, html, re
ROOT = r"C:\Users\Usuario\Documents\CV"
e = html.escape
SITE = "https://melissa-cv.github.io/CV-/"

T = {
    "es": {"lang": "es", "interes": "Líneas de interés", "proy": "Proyectos destacados", "otros": "Otros proyectos",
           "elec": "Electivas de profundización y materias clave", "cursos": "Cursos y certificaciones",
           "sem": "Semilleros", "exp": "Experiencia", "form": "Formación", "hab": "Habilidades",
           "sw": "Software", "tec": "Técnicas", "bl": "Blandas", "idi": "Idiomas", "asoc": "Proyecto asociado",
           "li": "Ver LinkedIn", "done": "(finalizado)",
           "intereses": ["Gestión de tecnología biomédica, normativa sanitaria y tecnovigilancia",
                         "Fabricación de dispositivos médicos personalizados y su preparación técnica"],
           "nav": [("proyectos", "Proyectos"), ("electivas", "Electivas"), ("cursos", "Cursos"),
                   ("experiencia", "Experiencia"), ("formacion", "Formación"), ("habilidades", "Habilidades")],
           "desc": "CV en línea de Melissa Cadavid Varela, bioingeniera de la Universidad de Antioquia."},
    "en": {"lang": "en", "interes": "Areas of interest", "proy": "Featured projects", "otros": "Other projects",
           "elec": "In-depth electives and key courses", "cursos": "Courses and certifications",
           "sem": "Research groups", "exp": "Experience", "form": "Education", "hab": "Skills",
           "sw": "Software", "tec": "Technical", "bl": "Soft", "idi": "Languages", "asoc": "Related project",
           "li": "View LinkedIn", "done": "(completed)",
           "intereses": ["Biomedical technology management, health regulations and technovigilance",
                         "Manufacture of custom medical devices and their technical preparation"],
           "nav": [("proyectos", "Projects"), ("electivas", "Electives"), ("cursos", "Courses"),
                   ("experiencia", "Experience"), ("formacion", "Education"), ("habilidades", "Skills")],
           "desc": "Online CV of Melissa Cadavid Varela, bioengineer from the Universidad de Antioquia."},
}


def cap(s):
    s = s.strip()
    return s[:1].upper() + s[1:]


def block(lang):
    d = json.load(io.open(ROOT + rf"\data\cv.{lang}.json", encoding="utf-8"))
    t = T[lang]
    c = d["Contacto"]
    li = c["linkedin"]["valor"] if c["linkedin"]["publico"] else ""
    # destacados primero, luego el resto (todos son de la versión larga)
    cards = lambda ps: "".join(
        f'<article class="card{" star" if p.get("destacado") == "si" else ""}"><h3>{e(p["titulo"])}</h3>'
        f'<p class="ctx">{e(p["contexto"])}</p><p>{e(p["que_hice"])}.'
        + (f' <span class="muted">{e(p["problema"])}.</span>' if p.get("problema") else "") + "</p></article>"
        for p in ps)
    pr = d["Proyectos destacados"]
    destac = cards([p for p in pr if p.get("destacado") == "si"])
    otros = cards([p for p in pr if p.get("destacado") != "si"])
    elec = "".join(
        f'<article class="card"><h3>{e(m["titulo"])}</h3><p>'
        + (f'{e(m["que_aprendi"])}.' if m.get("que_aprendi") else "")
        + (f' <span class="muted">{t["asoc"]}: {e(m["proyecto_asociado"])}.</span>' if m.get("proyecto_asociado") else "")
        + "</p></article>" for m in d["Materias y cursos clave"])
    cur = "".join(
        '<span class="chip">' + e(r["campos"][0]) + (" · " + e(" · ".join(x for x in r["campos"][1:] if x))
                                                      if any(r["campos"][1:]) else "") + "</span>"
        for r in d["Cursos complementarios y certificaciones"])
    sem = "".join(
        f'<div class="row"><div class="when">{e(s["periodo"])}</div><div><h3>{e(s["titulo"].split(" — ")[0])}</h3>'
        f'<p class="muted">{e(s["titulo"].split(" — ")[1])} · {e(s["rol"])}</p><p>{e(s["que_hice"])}.</p></div></div>'
        for s in d["Semilleros y grupos de investigación"])
    exp = "".join(
        f'<div class="row"><div class="when">{e(x["periodo"].replace(" " + t["done"], ""))}</div><div>'
        f'<h3>{e(x["titulo"].split(" — ")[0])}</h3><p class="muted">{e(x["titulo"].split(" — ")[1])}</p>'
        f'<ul>{"".join(f"<li>{e(l)}</li>" for l in x["logros"])}</ul></div></div>'
        for x in d["Experiencia"])
    form = "".join(
        f'<div class="row"><div class="when">{e(f["periodo"])}</div><div><h3>{e(f["titulo"].split(" — ")[0])}</h3>'
        f'<p class="muted">{e(f["titulo"].split(" — ")[1])}</p></div></div>' for f in d["Formación"])
    H = d["Habilidades"]
    idi = "".join(f'<li><b>{e(r["campos"][0])}</b> — {e(r["campos"][1])}</li>' for r in d["Idiomas"])
    chips =lambda items: "".join(f'<span class="chip">{e(cap(s))}</span>' for s in items)
    hab = (f'<h3>{t["sw"]}</h3><div class="chips">{chips(H["software"].split(","))}</div>'
           f'<h3>{t["tec"]}</h3><ul>{"".join(f"<li>{e(cap(s))}</li>" for s in H["tecnicas"].split(";"))}</ul>'
           f'<h3>{t["bl"]}</h3><div class="chips">{chips(H["blandas"].split(","))}</div>'
           f'<h3>{t["idi"]}</h3><ul>{idi}</ul>')
    nav = "".join(f'<a href="#{i}">{n}</a>' for i, n in t["nav"])
    lnk = f'<a class="btn" href="{e(li)}" target="_blank" rel="noopener">{t["li"]}</a>' if li else ""
    return f"""<div class="lang" lang="{lang}" data-l="{lang}">
<header class="hero"><div class="wrap"><p class="eyebrow">{e(d["meta"]["titulo_corto"])}</p><h1>{e(d["meta"]["nombre"])}</h1>
<p class="lead">{e(d["Perfil"]["larga"])}</p>
<p class="eyebrow small">{t["interes"]}</p><ul class="interes">{"".join(f"<li>{e(i)}</li>" for i in t["intereses"])}</ul>{lnk}</div></header>
<nav class="wrap">{nav}</nav>
<main class="wrap">
<section id="proyectos"><h2>{t["proy"]}</h2><div class="grid">{destac}</div>
<h3 class="sub">{t["otros"]}</h3><div class="grid">{otros}</div></section>
<section id="electivas"><h2>{t["elec"]}</h2><div class="grid">{elec}</div></section>
<section id="cursos"><h2>{t["cursos"]}</h2><div class="chips">{cur}</div><h3 class="sub">{t["sem"]}</h3>{sem}</section>
<section id="experiencia"><h2>{t["exp"]}</h2>{exp}</section>
<section id="formacion"><h2>{t["form"]}</h2>{form}</section>
<section id="habilidades"><h2>{t["hab"]}</h2>{hab}</section>
</main></div>"""


CSS = """
:root{--brand:#1FC1C9;--dark:#0f6f75;--soft:#e8f9fa;--bg:#fff;--fg:#26323a;--muted:#5b6b74;--card:#e8f9fa;--line:#d6eef0}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0e1a1d;--fg:#e3eef0;--muted:#9fb4ba;--card:#14272b;--line:#1f3a3f;--soft:#14272b;--dark:#5fdce2}}
:root[data-theme=dark]{--bg:#0e1a1d;--fg:#e3eef0;--muted:#9fb4ba;--card:#14272b;--line:#1f3a3f;--soft:#14272b;--dark:#5fdce2}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:'Montserrat','Segoe UI',system-ui,Arial,sans-serif;background:var(--bg);color:var(--fg);line-height:1.55;font-size:16px}
.wrap{max-width:980px;margin:0 auto;padding:0 16px}
.top{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);display:flex;justify-content:flex-end;gap:8px;padding:8px 16px}
.top button{font:inherit;font-size:13px;font-weight:600;border:1px solid var(--brand);background:transparent;color:var(--dark);border-radius:999px;padding:4px 14px;cursor:pointer}
.top button[aria-pressed=true]{background:var(--brand);color:#fff}
.hero{background:linear-gradient(135deg,var(--brand),#0f8f96);color:#fff;padding:56px 0 44px}
.hero h1{font-size:clamp(30px,6vw,48px);font-weight:800;line-height:1.1;margin:6px 0 16px}
.eyebrow{font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:13px;opacity:.95}.eyebrow.small{margin-top:22px;font-size:12px}
.lead{max-width:760px;font-size:17px}
.interes{margin:8px 0 0 20px}.interes li{margin-bottom:4px}
.btn{display:inline-block;margin-top:22px;background:#fff;color:#0f6f75;font-weight:700;text-decoration:none;border-radius:999px;padding:9px 20px}
nav.wrap{display:flex;flex-wrap:wrap;gap:6px 18px;padding-top:14px;padding-bottom:14px}
nav a{color:var(--dark);font-weight:600;text-decoration:none;font-size:14px}
section{padding:30px 0 6px}
h2{color:var(--dark);text-transform:uppercase;letter-spacing:.1em;font-size:18px;font-weight:800;display:flex;align-items:center;gap:12px;margin-bottom:16px}
h2::after{content:'';flex:1;height:2px;background:var(--brand)}
h3{font-size:16px;font-weight:700}.sub{margin:24px 0 12px;color:var(--dark)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}
.card{background:var(--card);border-left:5px solid var(--brand);border-radius:0 10px 10px 0;padding:14px 16px}
.card.star{border-left-color:var(--dark)}.card h3{margin-bottom:2px}
.ctx{color:var(--dark);font-weight:600;font-size:13.5px;margin-bottom:4px}.muted{color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.chip{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:5px 14px;font-size:14px}
.row{display:grid;grid-template-columns:170px 1fr;gap:6px 18px;margin-bottom:18px}
.when{color:var(--dark);font-weight:700;font-size:14px}
.row ul,section ul{margin:4px 0 8px 20px}
.lang{display:none}.lang.on{display:block}
footer{padding:36px 16px;text-align:center;color:var(--muted);font-size:13px}
@media(max-width:600px){.row{grid-template-columns:1fr}}
"""

JS = """
(function(){
  var KEY='cv-lang', ls=function(){try{return window.localStorage}catch(e){return null}}();
  function set(l){
    document.querySelectorAll('.lang').forEach(function(n){n.classList.toggle('on',n.dataset.l===l)});
    document.querySelectorAll('.top button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.l===l)});
    document.documentElement.lang=l;
    try{ls&&ls.setItem(KEY,l)}catch(e){}
  }
  var saved=null;try{saved=ls&&ls.getItem(KEY)}catch(e){}
  var start=saved||((navigator.language||'es').slice(0,2)==='en'?'en':'es');
  document.querySelectorAll('.top button').forEach(function(b){b.addEventListener('click',function(){set(b.dataset.l)})});
  set(start);
})();
"""

page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Melissa Cadavid Varela · CV</title>
<meta name="description" content="{e(T['es']['desc'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="top"><button data-l="es" aria-pressed="true">ES</button><button data-l="en" aria-pressed="false">EN</button></div>
{block("es")}
{block("en")}
<footer>Melissa Cadavid Varela</footer>
<script>{JS}</script>
</body>
</html>
"""
import os
os.makedirs(ROOT + r"\docs", exist_ok=True)
io.open(ROOT + r"\docs\index.html", "w", encoding="utf-8").write(page)
print("docs/index.html", len(page), "bytes")
