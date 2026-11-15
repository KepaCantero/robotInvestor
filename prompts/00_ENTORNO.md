# PROMPT 00 — Entorno: verificación e instalación

> Ejecutar en la primera sesión. Todo punto se VERIFICA con un comando real; nada se da
> por supuesto. Si un paso falla, diagnostica y repórtalo — no cambies código del corpus
> para arreglarlo.

---

ENTORNO — deja el repo listo para implementar y verifica cada punto con un comando real antes de darlo por bueno.

1. Python y venv:
   - `~/.local/bin/python3.12 --version` debe existir. Si no existe: PARA y díselo al propietario; no instales Python por tu cuenta.
   - El venv del repo es `.venv/`. Créalo e instálalo SOLO con `.docs/scripts/preparar_entorno.sh` (T-96): usa las versiones
     fijadas de `tools/requisitos_entorno.txt`, instala los tres ejecutores, los opcionales de tests y las herramientas de
     calidad, y comprueba lo instalado. Nunca `pip install` sin versión: así es como `arch` 9.0.0 rompió las cuotas de mypy.
     Si el script dice que el `.venv` está a medias o es de otro Python, bórralo (`rm -rf .venv`) y vuelve a ejecutarlo.
     `.docs/scripts/preparar_entorno.sh --comprobar` solo compara lo instalado con el fichero.
   - El pre-commit es opcional y va fuera del entorno fijado (no lo usa el gate): `pipx install pre-commit` y `pre-commit install`.
   - El gate del repo es `./tools/check_all.sh`: debe terminar **12/12 en verde**. Anota los números REALES obtenidos.
   - Nota conocida: sin `python-docx`, bloque_b falla 3 tests (el .docx del mapa de eslabones degrada con elegancia) — es la incidencia INC-003, no un bug tuyo.

2. MCPs (con `claude mcp list`):
   - **context7** (documentación de librerías al día — anthropic SDK, pandas, arch, jsonschema). Es el MCP anti-alucinación de APIs de este proyecto: CONSÚLTOLO antes de escribir contra cualquier librería. Instalación:
     `claude mcp add --transport http context7 https://mcp.context7.com/mcp`
     Si el endpoint cambió o pide clave, busca la instrucción vigente en context7.com y úsala (la clave gratuita se crea allí). Verifica tras añadirla que responde.
   - **github** (opcional, solo si el propietario quiere PRs/issues desde la sesión): sigue la instrucción oficial del GitHub MCP server con un PAT del propietario. Para commits directos NO hace falta: git ya funciona con la credencial del llavero.
   - NO instales ningún otro MCP: cada uno extra es ruido. Claude Code ya trae bash, lectura de archivos y WebSearch/WebFetch.

3. Sanity de git: `git status` limpio, rama `develop`, remoto `origin` → github.com/KepaCantero/robotInvestor, push funciona (`git push` → everything up-to-date o sube lo que falte).

4. Registra en `docs/AVANCE.md` una línea «entorno verificado» con fecha y los números de tests reales obtenidos. Si cambiaste algo, commit con prefijo `infra:`.

Criterio de éxito: las tres suites en verde con los números anotados, `claude mcp list` muestra context7 operativo, y push OK.
