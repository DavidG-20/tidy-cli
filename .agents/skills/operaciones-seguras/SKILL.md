---
name: operaciones-seguras
description: Reglas obligatorias de seguridad al leer, mover o renombrar archivos en Linux.
---

# Reglas de Seguridad de Archivos

- **NUNCA** elimines archivos ni carpetas del usuario; esta herramienta solo mueve o renombra archivos.
- Ignora siempre archivos y carpetas ocultas (los que empiezan con `.` en Linux) y enlaces simbólicos (`is_symlink()`).
- Antes de mover un archivo, verifica si ya existe en el destino. Si existe, renómbralo con un sufijo numérico incremental (ej. `tarea (1).pdf`, `tarea (2).pdf`) en lugar de sobrescribirlo.
- Toda función que mueva archivos debe aceptar `dry_run: bool = False`. Si es `True`, solo devuelve el plan de movimientos sin tocar el disco.
- Guarda el historial de movimientos en un archivo JSON dentro de la carpeta organizada (`.tidy_history.json`) para soportar `--undo` de forma segura.
- En las pruebas con `pytest`, usa siempre el fixture `tmp_path` para crear archivos temporales aislados; nunca ejecutes pruebas sobre carpetas reales del usuario.
