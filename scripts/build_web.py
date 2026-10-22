# -*- coding: utf-8 -*-
"""Genera docs/index.html (GitHub Pages) bilingüe ES/EN desde data/cv.es.json y data/cv.en.json.
Diseño de dos columnas (igual que los PDF): barra lateral verde petróleo con toques ámbar + columna principal.
Privacidad: sin correo, teléfono, ciudad, foto, referencias ni PDF. Único contacto: LinkedIn (publico: si).
Uso: python -I scripts/build_web.py"""
import json, io, html, re, os
ROOT = r"C:\Users\Usuario\Documents\CV"
e = html.escape

T = {
    "es": {"interes": "Líneas de interés", "proy": "Proyectos destacados", "otros": "Otros proyectos",
           "elec": "Electivas y materias clave", "cursos": "Cursos y certificaciones",
           "sem": "Semilleros", "exp": "Experiencia", "form": "Formación", "hab": "Habilidades técnicas",
           "sw": "Software", "bl": "Habilidades blandas", "idi": "Idiomas", "asoc": "Proyecto asociado",
           "li": "Perfil en LinkedIn", "done": "(finalizado)", "perfil": "Perfil", "nav": "Contenido",
           "intereses": ["Gestión de tecnología biomédica, normativa sanitaria y tecnovigilancia",
                         "Fabricación de dispositivos médicos personalizados y su preparación técnica"],
           "desc": "CV en línea de Melissa Cadavid Varela, bioingeniera de la Universidad de Antioquia."},
    "en": {"interes": "Areas of interest", "proy": "Featured projects", "otros": "Other projects",
           "elec": "Electives and key courses", "cursos": "Courses and certifications",
           "sem": "Research groups", "exp": "Experience", "form": "Education", "hab": "Technical skills",
           "sw": "Software", "bl": "Soft skills", "idi": "Languages", "asoc": "Related project",
           "li": "LinkedIn profile", "done": "(completed)", "perfil": "Profile", "nav": "Contents",
           "intereses": ["Biomedical technology management, health regulations and technovigilance",
                         "Manufacture of custom medical devices and their technical preparation"],
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
    n = iter(range(1, 20))
    secs = []

    def sec(sid, title, body):
        secs.append((sid, title))
        return f'<section id="{sid}-{lang}"><h2><i>{next(n):02d}</i>{title}</h2>{body}</section>'

    def cards(ps, star=False):
        return "".join(
            f'<article class="card{" star" if star else ""}"><h3>{e(p["titulo"])}</h3><div class="ctx">{e(p["contexto"])}</div>'
            f'<p>{e(p["que_hice"])}.' + (f' <span class="muted">{e(p["problema"])}.</span>' if p.get("problema") else "")
            + "</p></article>" for p in ps)

    pr = d["Proyectos destacados"]
    destac = cards([p for p in pr if p.get("destacado") == "si"], star=True)
    otros = cards([p for p in pr if p.get("destacado") != "si"])
    elec = "".join(
        f'<article class="card"><h3>{e(m["titulo"])}</h3><p>'
        + (f'{e(m["que_aprendi"])}.' if m.get("que_aprendi") else "")
        + (f' <span class="muted">{t["asoc"]}: {e(m["proyecto_asociado"])}.</span>' if m.get("proyecto_asociado") else "")
        + "</p></article>" for m in d["Materias y cursos clave"])
    cur = "".join(
        f'<li><b>{e(r["campos"][0])}</b>' + (f' <span class="muted">— {e(" · ".join(x for x in r["campos"][1:] if x))}</span>'
                                             if any(r["campos"][1:]) else "") + "</li>"
        for r in d["Cursos complementarios y certificaciones"])

    def item(title, org, per, extra=""):
        return (f'<div class="item"><div class="head"><h3>{e(title)}</h3><span class="per">{e(per)}</span></div>'
                f'<div class="org">{e(org)}</div>{extra}</div>')

    sem = "".join(item(s["titulo"].split(" — ")[0], f'{s["titulo"].split(" — ")[1]} · {s["rol"]}', s["periodo"],
                       f'<ul><li>{e(s["que_hice"])}.</li></ul>') for s in d["Semilleros y grupos de investigación"])
    exp = "".join(item(x["titulo"].split(" — ")[0], x["titulo"].split(" — ")[1], x["periodo"].replace(" " + t["done"], ""),
                       "<ul>" + "".join(f"<li>{e(l)}</li>" for l in x["logros"]) + "</ul>")
                  for x in d["Experiencia"])
    form = "".join(f'<li><b>{e(f["titulo"].split(" — ")[0])}</b>{e(f["titulo"].split(" — ")[1])}'
                   f'<span class="per">{e(f["periodo"])}</span></li>' for f in d["Formación"])
    H = d["Habilidades"]
    chips = lambda items: "".join(f"<span>{e(cap(s))}</span>" for s in items)
    idi = "".join(f'<li><b>{e(r["campos"][0])}</b>{e(r["campos"][1])}</li>' for r in d["Idiomas"])
    lnk = f'<a class="lnk" href="{e(li)}" target="_blank" rel="noopener">{t["li"]} ↗</a>' if li else ""

    main = (sec("perfil", t["perfil"], f'<p class="lead">{e(d["Perfil"]["larga"])}</p><h4>{t["interes"]}</h4><ul>'
               + "".join(f"<li>{e(i)}</li>" for i in t["intereses"]) + "</ul>")
            + sec("proyectos", t["proy"], destac + f'<h4>{t["otros"]}</h4>' + otros)
            + sec("electivas", t["elec"], f'<div class="grid2">{elec}</div>')
            + sec("cursos", t["cursos"], f'<ul class="sq">{cur}</ul><h4>{t["sem"]}</h4>{sem}')
            + sec("experiencia", t["exp"], exp))
    nav = "".join(f'<a href="#{sid}-{lang}">{title}</a>' for sid, title in secs)
    side = (f'<aside><p class="kick">Curriculum vitae</p><h1>{e(d["meta"]["nombre"])}</h1>'
            f'<p class="role">{e(d["meta"]["titulo_corto"])}</p>{lnk}'
            f'<h5 class="navh">{t["nav"]}</h5><nav>{nav}</nav>'
            f'<h5>{t["form"]}</h5><ul class="edu">{form}</ul>'
            f'<h5>{t["sw"]}</h5><div class="chips">{chips(H["software"].split(","))}</div>'
            f'<h5>{t["hab"]}</h5><ul>{"".join(f"<li>{e(cap(s))}</li>" for s in H["tecnicas"].split(";"))}</ul>'
            f'<h5>{t["bl"]}</h5><div class="chips">{chips(H["blandas"].split(","))}</div>'
            f'<h5>{t["idi"]}</h5><ul class="edu">{idi}</ul></aside>')
    return f'<div class="lang" lang="{lang}" data-l="{lang}"><div class="layout">{side}<main>{main}</main></div></div>'


CSS = """
:root{--deep:#1d4a4f;--deeper:#153a3e;--amber:#e2b35e;--amber-d:#a9741a;--teal:#2f6f73;--soft:#f3f7f6;--bg:#fff;--ink:#1b2528;--muted:#5d6b70;--line:#cfdcdb;
--serif:'Fraunces',Georgia,serif;--sans:'Inter','Segoe UI',system-ui,Arial,sans-serif;--mono:'IBM Plex Mono',Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1719;--ink:#e6eef0;--muted:#9fb2b7;--line:#27393d;--soft:#16262a;--deeper:#d5e6e6;--teal:#7fc1c6;--amber-d:#e2b35e}}
:root[data-theme=dark]{--bg:#0f1719;--ink:#e6eef0;--muted:#9fb2b7;--line:#27393d;--soft:#16262a;--deeper:#d5e6e6;--teal:#7fc1c6;--amber-d:#e2b35e}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{font-family:var(--sans);background:var(--bg);color:var(--ink);line-height:1.6;font-size:16px}
.top{position:fixed;top:10px;right:14px;z-index:10;display:flex;gap:6px}
.top button{font-family:var(--mono);font-size:12px;letter-spacing:.08em;border:1px solid var(--line);background:var(--bg);color:var(--muted);padding:3px 12px;cursor:pointer;border-radius:2px}
.top button[aria-pressed=true]{border-color:var(--amber);color:var(--ink)}
.layout{display:grid;grid-template-columns:320px 1fr;min-height:100vh}
aside{background:var(--deep);color:#eef5f5;padding:44px 28px;position:sticky;top:0;height:100vh;overflow:auto}
.kick{font-family:var(--mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--amber);margin-bottom:10px}
aside h1{font-family:var(--serif);font-weight:600;font-size:34px;line-height:1.06}
.role{font-family:var(--serif);font-style:italic;color:#cfe3e3;margin:10px 0 16px}
.lnk{font-family:var(--mono);font-size:12.5px;color:var(--amber);text-decoration:none;border-bottom:1px solid var(--amber)}
aside h5{font-family:var(--mono);font-weight:500;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--amber);border-bottom:1px solid rgba(255,255,255,.2);padding-bottom:5px;margin:26px 0 10px}
aside nav{display:flex;flex-direction:column;gap:5px}aside nav a{color:#eef5f5;text-decoration:none;font-size:14.5px}aside nav a:hover{color:var(--amber)}
aside ul{list-style:none;font-size:14.5px}aside li{margin-bottom:6px}aside li b{display:block;font-weight:600}
.edu .per{display:block;font-family:var(--mono);font-size:12px;color:#cfe3e3}
.chips span{display:inline-block;border:1px solid rgba(255,255,255,.4);border-radius:3px;padding:2px 8px;margin:0 4px 6px 0;font-family:var(--mono);font-size:12px}
main{padding:56px clamp(20px,5vw,64px) 40px;max-width:900px}
section{margin-bottom:44px}
h2{display:flex;align-items:baseline;gap:12px;font-family:var(--serif);font-weight:600;font-size:26px;color:var(--teal);margin-bottom:16px}
h2 i{font-family:var(--mono);font-style:normal;font-weight:500;font-size:12px;color:var(--amber-d);letter-spacing:.08em}
h2::after{content:'';flex:1;height:1px;background:var(--line)}
h3{font-size:16px;font-weight:600}h4{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--amber-d);font-weight:500;margin:26px 0 12px}
.lead{font-size:17px}
.card{background:var(--soft);border-left:4px solid var(--line);border-radius:0 6px 6px 0;padding:12px 16px;margin-bottom:12px}
.card.star{border-left-color:var(--amber)}.card h3{margin-bottom:1px}
.ctx{font-family:var(--mono);font-size:12px;color:var(--teal);margin-bottom:4px}
.muted{color:var(--muted)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.grid2 .card{margin:0}
.sq{list-style:none;margin:0}.sq li{position:relative;padding-left:18px;margin-bottom:6px}.sq li::before{content:'';position:absolute;left:0;top:.62em;width:8px;height:8px;background:var(--amber)}
.item{margin-bottom:18px}.head{display:flex;justify-content:space-between;gap:14px;align-items:baseline;flex-wrap:wrap}
.per{font-family:var(--mono);font-size:12.5px;color:var(--teal);white-space:nowrap}.org{color:var(--muted);font-size:14.5px}
main ul{margin:4px 0 0 20px}main li{margin-bottom:3px}
.lang{display:none}.lang.on{display:block}
footer{padding:26px 20px;text-align:center;font-family:var(--mono);font-size:12px;letter-spacing:.08em;color:var(--muted)}
@media(max-width:860px){.layout{grid-template-columns:1fr}aside{position:static;height:auto;padding:56px 22px 30px}.grid2{grid-template-columns:1fr}aside nav,.navh{display:none}}
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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="top"><button data-l="es" aria-pressed="true">ES</button><button data-l="en" aria-pressed="false">EN</button></div>
{block("es")}
{block("en")}
<footer>MELISSA CADAVID VARELA</footer>
<script>{JS}</script>
</body>
</html>
"""
os.makedirs(ROOT + r"\docs", exist_ok=True)
io.open(ROOT + r"\docs\index.html", "w", encoding="utf-8").write(page)
print("docs/index.html", len(page), "bytes")
