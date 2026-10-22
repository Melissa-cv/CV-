# Proyecto CV — Melissa Cadavid Varela

Bioingeniera (Universidad de Antioquia), recién graduada / en espera de grado.
Poca experiencia laboral: el CV debe hacer brillar **proyectos de materias, electivas, cursos y voluntariado**.

## Flujo
Todo lo orquesta el subagente `cv-manager` (`.claude/agents/cv-manager.md`), que usa estas skills:

| Skill | Qué hace |
|---|---|
| `cv-parse` | Valida `data/cv-master.es.md`, detecta vacíos, conflictos y `REVISAR`, y genera `data/cv.es.json` |
| `cv-improve` | Propone mejoras al CV genérico; Melissa aprueba cada cambio |
| `cv-tailor` | Adapta el CV a una oferta concreta y lo guarda en `variants/<empresa>/` |
| `cv-render` | Genera los PDF (corto y largo, ES y EN) en `output/` |
| `cv-web` | Genera `docs/index.html` (GitHub Pages) y el QR |

## Reglas
- **Fuente de verdad:** `data/cv-master.es.md`. El inglés (`data/cv-master.en.md`) se deriva de él; si el español cambia, avisar de que el inglés está desactualizado.
- **Nunca inventar** datos, fechas, cifras ni resultados. Si falta algo, preguntar o marcar `<!-- REVISAR: ... -->`.
- **Privacidad:** solo los campos con `publico: si` aparecen en la web. Teléfono, dirección y referencias **nunca** van en `docs/`. Además, la web **no lleva datos personales** (correo, ciudad, foto); el único dato de contacto público es **LinkedIn**. Correo y teléfono van solo en el PDF corto, que incluye el QR hacia la web. La web **no tiene botón de descargar PDF**: Melissa envía el PDF y de ahí lleva a la web.
- **Web (repo):** `https://github.com/Melissa-cv/CV-` → `https://melissa-cv.github.io/CV-/`.
- **QR:** el PDF corto (1 página) lleva un QR que apunta a la web, que es la versión larga del CV (`output/qr-cv.png`). Debe caber en la misma hoja.
- **Proyectos:** no añadir programas/herramientas a los proyectos; se dejan exactamente como los especificó Melissa.
- **Electivas:** las materias tipo Metrología, Normas técnicas, Nanotecnología, Ensayos biológicos y Gestión de equipos son *electivas de profundización* de la UdeA.
- **Diseño (dos columnas, decisión final de Melissa):** barra lateral verde petróleo `#1D4A4F` con toques ámbar `#E2B35E` (foto circular con aro ámbar, títulos de sección en mono ámbar, chips solo con borde) y columna principal blanca con títulos numerados en serif (Fraunces), tarjetas suaves `#F3F7F6` con borde ámbar, texto Inter y fechas en mono (IBM Plex Mono). Sobrio, no chillón y no la plantilla común de Canva. Se aplica igual a los PDF y a la web. En el PDF corto el QR va abajo de la barra lateral. Plantillas: `templates/cv.html` (corta) y `templates/cv-largo.html` (larga). Foto con fondo blanco de estudio: `assets/foto-estudio.jpg` (el original se conserva en `assets/foto-original.jpg`).
- **Corta:** debe incluir los cursos Tecnovigilancia, Neurología y neurorrehabilitación y el Semillero de áreas básicas de la salud.
- **Versiones:** cada elemento lleva `versiones: corta, larga`. La corta cabe en 1 página.
- Los PDF originales de referencia están en `originales/` y no se modifican.
- Se escribe en español; ortografía y tildes revisadas siempre.
