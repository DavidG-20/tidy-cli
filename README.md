# tidy-cli

Herramienta de línea de comandos (CLI) en Python para organizar automáticamente los archivos de cualquier carpeta en subcarpetas por categoría, con **modo simulación (`--dry-run`)**, **protección contra duplicados** y **deshacer en un comando (`--undo`)**.

## Características principales

- **Clasificación automática**: agrupa archivos en `Documents`, `Images`, `Videos`, `Audio`, `Archives`, `Code`, `Installers` y `Others` según las reglas centralizadas en `src/tidy_cli/config.py`.
- **Modo simulación (`--dry-run` / `-n`)**: muestra una tabla previa con los cambios que se harían **sin mover ningún archivo**.
- **Protección contra duplicados**: nunca sobrescribe archivos existentes; si ya hay un archivo con el mismo nombre, lo renombra automáticamente con sufijo numérico (ej. `tarea.pdf` → `tarea (1).pdf`).
- **Seguro por diseño**: nunca elimina archivos ni carpetas del usuario, e ignora automáticamente archivos ocultos (`.env`, `.git`), subcarpetas y enlaces simbólicos.
- **Historial y deshacer (`--undo`)**: guarda un registro en `.tidy_history.json` para devolver todos los archivos a su ubicación original (incluso admite `--undo --dry-run`).

## Tecnologías y arquitectura

- **Python 3.10+** gestionado con [`uv`](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`)
- **Typer** para comandos y validación de argumentos en terminal
- **Rich** para tablas y salida con colores
- **pytest** para pruebas automatizadas aisladas (`tmp_path`)

```text
tidy-cli/
├── .agents/skills/          # Skills de arquitectura y seguridad de archivos
├── AGENTS.md                # Reglas generales del proyecto
├── src/tidy_cli/
│   ├── main.py              # Capa de presentación (solo Typer + Rich)
│   ├── config.py            # Mapa de extensiones → categorías
│   ├── models.py            # Dataclasses tipados (MoveAction, OrganizePlan, ExecutionResult)
│   ├── scanner.py           # Lógica pura de escaneo y clasificación
│   └── mover.py             # Movimiento seguro e historial JSON para --undo
├── tests/
│   ├── test_scanner.py      # Pruebas de escaneo y resolución de duplicados
│   └── test_mover.py        # Pruebas de dry-run, movimiento y deshacer
└── pyproject.toml
```

## Instalación

Asegúrate de tener [`uv`](https://docs.astral.sh/uv/) instalado, luego clona el repositorio y sincroniza dependencias:

```bash
git clone https://github.com/DavidG-20/tidy-cli.git
cd tidy-cli
uv sync
```

## Uso

Previsualizar cambios sin mover archivos:

```bash
uv run tidy ~/Downloads --dry-run
```

Organizar una carpeta:

```bash
uv run tidy ~/Downloads
```

Deshacer el último ordenamiento en esa carpeta:

```bash
uv run tidy ~/Downloads --undo
```

Ver la ayuda completa:

```bash
uv run tidy --help
```

## Ejecutar pruebas

Todas las pruebas corren sobre carpetas temporales aisladas (`tmp_path` de `pytest`):

```bash
uv run pytest -v
```

## Licencia

MIT
