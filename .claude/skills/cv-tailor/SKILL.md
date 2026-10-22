---
name: cv-tailor
description: Personaliza el CV de Melissa para una empresa u oferta concreta. Úsala cuando indique una vacante, empresa o práctica; guarda la variante en variants/<empresa>/ sin tocar el master.
---

# cv-tailor

## Pasos
1. Pide la oferta (texto o enlace; si es enlace, usa WebFetch) y el nombre de la empresa. Si no hay oferta, pregunta el cargo y el área.
2. Extrae: palabras clave, requisitos obligatorios vs. deseables, tipo de cargo (práctica, auxiliar, ingeniería de calidad, etc.).
3. Cruza con `data/cv-master.es.md`: qué proyectos, cursos y experiencias respaldan cada requisito. Identifica a qué línea corresponde: **tecnovigilancia/gestión de equipos/normativa** o **fabricación/verificación de dispositivos**.
4. Propón (Antes → Después, numerado): perfil reescrito para la oferta, reorden de secciones, qué proyectos/cursos destacar u ocultar, versión (corta/larga) recomendada. Marca los requisitos que **no** cumple, sin maquillarlos.
5. Con su aprobación, crea `variants/<empresa>/cv.es.md` (copia del master con los cambios aprobados) y `variants/<empresa>/notas.md` (oferta, palabras clave, brechas, fecha).
6. Ofrece generar PDF con `cv-render` apuntando a esa variante.

## Reglas
- No modificar `data/cv-master.es.md`.
- No añadir habilidades ni experiencias que no estén en el master; si la oferta pide algo que Melissa sí sabe pero no está registrado, pregúntale y propón agregarlo al master.
- Carta de presentación solo si la pide.
