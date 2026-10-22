---
name: cv-render
description: Genera los PDF del CV (corto de 1 página y largo, en español e inglés) con diseño moderno de dos columnas. Úsala cuando pida el PDF del CV genérico o de una variante.
---

# cv-render

## Pasos
1. Pregunta (si no se dijo): versión **corta**, **larga** o ambas; idioma **ES**, **EN** o ambos; fuente: master o `variants/<empresa>/`.
2. Ejecuta `cv-parse`; no sigas si hay bloqueantes. Si el inglés se pide y está desactualizado, tradúcelo primero a `data/cv-master.en.md` (o a la variante) y muéstraselo.
3. Filtra por `versiones:` según corta/larga. **Incluye teléfono y correo** en el PDF (el PDF es para enviar); `publico:` aplica solo a la web.
4. Genera los PDF con `powershell -NoProfile -File scripts/render.ps1 [-Langs es,en] [-Versions corta,larga]`. Usa `scripts/build_cv.py <es|en> <corta|larga> <html>` con `templates/cv.html` (corta, 1 página, con QR a la web) o `templates/cv-largo.html` (larga, 2 páginas) y convierte con Edge headless. Edge necesita un `--user-data-dir` distinto por PDF y los argumentos en una sola cadena; si no, falla con "Multiple targets". El script ya lo resuelve y cuenta las páginas.
   Los datos salen de `data/cv.<lang>.json` (se regenera con `python -I scripts/parse_master.py es|en`).
5. Verifica: la corta ocupa exactamente 1 página; la larga 2 como máximo. Si se desborda, recorta por prioridad (sin cambiar redacción sin avisar) y reporta qué sacó.
6. Nombres: `output/CV-Melissa-Cadavid-{corta|larga}-{es|en}.pdf`; variantes en `variants/<empresa>/`.

## Diseño
Dos columnas (ver `CLAUDE.md`): barra lateral verde petróleo con toques ámbar, foto circular (`assets/foto-estudio.jpg`) y QR (solo corta) abajo; columna principal con secciones numeradas y tarjetas suaves. Orden de la corta: Perfil → Proyectos → Electivas → Cursos → Experiencia (Formación y habilidades van en la barra lateral).
