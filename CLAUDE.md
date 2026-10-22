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
- **Diseño:** moderno y llamativo, sin restricciones ATS (dos columnas, barra lateral de color, iconos, bloques destacados). Color de marca actual: turquesa `#1FC1C9`.
- **Versiones:** cada elemento lleva `versiones: corta, larga`. La corta cabe en 1 página.
- Los PDF originales de referencia están en `originales/` y no se modifican.
- Se escribe en español; ortografía y tildes revisadas siempre.
