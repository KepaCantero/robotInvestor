# PROMPT 00 — Entorno: verificación e instalación

> Ejecutar en la primera sesión. Todo punto se VERIFICA con un comando real; nada se da
> por supuesto. Si un paso falla, diagnostica y repórtalo — no cambies código del corpus
> para arreglarlo.

---

ENTORNO — deja el repo listo para implementar y verifica cada punto con un comando real antes de darlo por bueno.

1. Python y venv:
   - `~/.local/bin/python3.12 --version` debe existir. Si no existe: PARA y díselo al propietario; no instales Python por tu cuenta.
   - El venv del repo es `.venv/`. Si no existe, créalo con ese intérprete exacto.
   - Instala los tres ejecutores y los opcionales de tests:
     `pip install -e bloque_a/11_Ejecutor -e bloque_a_forex/11_Ejecutor -e bloque_b/11_Ejecutor`
     `pip install arch openpyxl python-docx pytest`
   - Verifica las tres líneas base y anota los números REALES obtenidos:
     `pytest -q bloque_a/11_Ejecutor` → 58 · `pytest -q bloque_a_forex/11_Ejecutor` → 68 · `pytest -q bloque_b/11_Ejecutor` → 118
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
