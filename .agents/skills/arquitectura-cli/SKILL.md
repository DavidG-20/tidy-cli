---
name: arquitectura-cli
description: Reglas de diseño, tipado y separación de capas para la herramienta CLI tidy-cli en Python.
---

# Arquitectura CLI en Python

- Usa siempre `pathlib.Path` para manipular rutas; nunca uses `os.path` ni concatenación de strings.
- Separa estrictamente la capa de presentación (`main.py` con Typer y Rich) de la lógica de negocio (`scanner.py`, `mover.py`).
- Los módulos de lógica NO deben llamar a `print()` ni usar Rich directamente; deben devolver objetos tipados (`dataclasses` definidos en `models.py`) para que `main.py` decida cómo mostrarlos.
- Incluye type hints en todas las funciones y parámetros (Python 3.10+).
- Mantén el mapa de extensiones y categorías centralizado en `config.py`.
- Evita funciones monolíticas: mantén cada función enfocada en una sola responsabilidad.
