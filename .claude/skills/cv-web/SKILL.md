---
name: cv-web
description: Genera la versión online del CV (docs/index.html para GitHub Pages) y el código QR que enlaza a ella. Úsala para crear o actualizar la web del CV.
---

# cv-web

## Pasos
1. Ejecuta `cv-parse`. Repositorio ya definido: usuario `Melissa-cv`, repo `CV-` (`https://melissa-cv.github.io/CV-/`). Sin foto y sin correo público.
2. Genera `docs/index.html`: una sola página responsive, bilingüe (botón ES/EN), sin dependencias que requieran build, con secciones: Hero (nombre, título, líneas de interés), Proyectos destacados (tarjetas), Semilleros/electivas, Cursos y certificaciones (chips), Experiencia, Formación, Habilidades. **Sin botón de descargar PDF** (el PDF lleva datos de contacto y se envía aparte). Sin correo, ciudad ni foto; el único contacto es el enlace a LinkedIn.
3. **Privacidad:** incluye solo campos con `publico: si`. Nunca teléfono, dirección ni referencias. Si hay duda, no lo muestres.
4. No copies PDF ni foto a `docs/`.
5. Genera el QR a `https://<usuario>.github.io/<repo>/` en `output/qr-cv.png` (y SVG). Si falta la librería: `pip install qrcode[pil]`.
6. Indica los pasos para publicar: repo en GitHub → Settings → Pages → rama `main`, carpeta `/docs`. **No hagas push ni publiques sin confirmación.**
7. Revisa la página en el navegador integrado (escritorio y móvil) antes de dar por terminado.

## Diseño
Mismo lenguaje visual que el PDF (dos columnas: barra lateral verde petróleo con toques ámbar, tarjetas suaves, serif + mono), con modo claro/oscuro. Se genera con `python -I scripts/build_web.py`. Los proyectos y cursos universitarios van arriba del todo, antes que la experiencia.
