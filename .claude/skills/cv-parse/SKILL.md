---
name: cv-parse
description: Valida y estructura data/cv-master.es.md. Úsala al iniciar cualquier flujo del CV, o cuando se edite el master, para detectar campos vacíos, marcas REVISAR, inconsistencias y generar data/cv.es.json.
---

# cv-parse

Lee `data/cv-master.es.md` (front-matter YAML + secciones `##` con elementos `###` y líneas `- clave: valor`).

## Pasos
1. Lee el archivo completo. Conoce las secciones esperadas: Contacto, Perfil, Formación, Semilleros y grupos, Proyectos destacados, Materias y cursos clave, Cursos y certificaciones, Experiencia, Habilidades, Idiomas, Referencias.
2. Detecta y lista:
   - Campos vacíos (valor en blanco) y marcas `<!-- REVISAR: ... -->`.
   - Elementos sin `versiones:` (propón cuáles van en corta/larga).
   - Fechas incoherentes o solapadas (ej. un cargo "Presente" y otro posterior), y diferencias de ortografía o nombres entre secciones.
   - Datos con `publico: no` que aparezcan fuera de Contacto o Referencias.
3. Convierte a `data/cv.es.json` con la misma jerarquía (sección → elementos → campos), conservando `versiones` y `publico` como listas/booleanos.
4. Entrega un reporte corto: ✅ completo / ⚠️ por revisar / ❌ bloqueante, y el conteo por sección.

## Reglas
- No modifiques el `.md`; solo reporta.
- No inventes valores faltantes.
