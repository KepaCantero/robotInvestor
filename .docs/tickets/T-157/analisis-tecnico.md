# T-157 · Análisis técnico

## Causa raíz o motivo

La Fase 0 de `CLAUDE.md` pide medir con un comando qué identificadores están desincronizados entre el corpus del Bloque A y el
código, antes de seguir con el Motor. Hasta ahora eso se sabía por auditorías a mano (T-92, T-106) y por notas como la de
`docs/AVANCE.md` («`servicio.py` = 60 de V4.0»), que ya no eran ciertas. El verificador lo hace repetible y con evidencia: cada
dato del informe sale del corpus o del código escaneados, con archivo y línea, y el informe lleva la huella SHA-256 de lo leído.

## Evidencia

El informe vigente está en `docs/auditoria_ids_bloque_a.md` (y en JSON, `docs/auditoria_ids_bloque_a.json`), generado con:

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids \
  --json ../../docs/auditoria_ids_bloque_a.json --auditoria ../../docs/auditoria_ids_bloque_a.md
# verificador_ids: 3 errores, 3 avisos (01_Gobernanza/Documento 0 - … V5.1.md, Catálogo V5.0)   → salida 1
```

Resumen por clase, con el corpus de `4f7ea73`:

| Clase | Errores | Avisos | Info | Qué dice |
| --- | --- | --- | --- | --- |
| (a) CT | 0 | 0 | 0 | 25 en §6.1, las 25 en `CANALES` con algún par que `canal_permitido` admite; ninguna CT citada que no exista |
| (b) R | 0 | 0 | 1 | R1–R27; «R30» es un código JEL |
| (c) F | 0 | 0 | 9 | F1–F11 con su archivo por H1 (más FM, HA y RC); CC y ENT no son archivos de 05; F02, F05, F12 y F31 son funciones locales, una fórmula o JEL |
| (d) fichas | 2 | 2 | 3 | 81 IMPLEMENTADO (80 por CT-09, AUD-REX-001 por CT-10); `catalog_version` 4.0 escrito en `evaluador.py`; la ficha FX-MC10-003 del ejemplo de RC; 8 menciones al «Catálogo V4.0» en el corpus y una en `motor/operaciones.py` |
| (e) referencias | 1 | 1 | 0 | TA 23, TM 18, TF 19 y DOC-MOT 4 citadas, todas existen; RF-0123 no existe; «RF-1» es otra cosa |
| (f) PS | 0 | 0 | 0 | PS1–PS8 |

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/herramientas/verificador_ids.py` (nuevo): el verificador. `verificar(raiz, codigo=None)`
    devuelve el informe; `Codigo.desde_paquete(raiz)` lee el código importándolo (`servicio`: `CATALOG_VERSION`,
    `FICHAS_CATALOGO`, `IMPLEMENTADAS`, `SERVICIOS_CT10`, `DOCUMENTADAS_CON_CODIGO`, `ALTERNATIVAS`, `RUTA_CATALOGO`,
    `madurez_catalogo()`, `servible()`; `contratos`: `CANALES`, `CANALES_V6`, `CAMPOS_MINIMOS`, `canal_permitido`) y busca en los
    `.py` del paquete versiones del Catálogo escritas a mano; `ESQUEMA_INFORME` y `validar_informe` (el resumen tiene que cuadrar
    con los hallazgos); `a_json`, `a_markdown`, `actualizar_auditoria` (solo entre marcas) y `main`.
  - `bloque_a/11_Ejecutor/tests/test_t157_verificador_ids.py` (nuevo, 34 pruebas): corpus de juguete con fallos de cada clase y
    pruebas del corpus real contadas con código propio.
  - `bloque_a/11_Ejecutor/README.md`: la orden y la estructura.
  - `docs/auditoria_ids_bloque_a.md` y `.json` (nuevos), `docs/incidencias.md` (INC-T157-01 a 05), `docs/AVANCE.md` (entrada y
    pendiente de la Fase 0, que decía «`servicio.py` = 60 de V4.0»), `tools/refs_allowlist.txt` (sin las dos líneas de la Fase 0).
- **Decisiones tomadas y desviaciones del plan:**
  - Ubicación: `herramientas/`, como pide el prompt y como esperaba `tools/refs_allowlist.txt`, aunque no es una herramienta HT
    del Documento 0 (lo dice su docstring). Se lanza con `python -m`; no se añade un `project.scripts` porque el `.venv`
    instala el paquete del repositorio principal en modo editable y una orden nueva exigiría reinstalarlo.
  - El código se lee importándolo, no interpretando su texto: `IMPLEMENTADAS` se construye en tiempo de importación con los
    módulos de fichas, y lo que cuenta es lo que el Motor sirve de verdad. Las pruebas pasan un `Codigo` de juguete.
  - Contextos que no son citas (INC-T157-01): sin ellos, la primera pasada daba 10 errores, de los que 7 eran falsos (JEL, la
    pendiente `(F1 − F12) / F12`, `PROS-F02…F12` abreviadas, un número de documento de trabajo de la NYU en F8, el símbolo de una
    serie ficticia `IDX-FICT-001`). Cada contexto se deduce del propio texto y se informa como INFO con su ubicación: no se
    esconde nada. La forma de los ID de ficha (segmentos intermedios que empiezan por letra) sale de los ID del Catálogo.
  - Añadidos al prompt: la clase (f), porque §9 está en el kit de la fase; la comparación de la madurez del índice §4 con los
    manejadores y con lo que lee `madurez_catalogo()`; y el escaneo de los `.py` del paquete, que encontró el único desajuste real
    del código (`evaluador.py`, `catalog_version` 4.0).
  - `docs/AVANCE.md`: la nota pendiente de la Fase 0 ya no era cierta (el verificador mide 81 en `FICHAS_CATALOGO`); se
    sustituye por las decisiones que quedan.
- **Límites conocidos:**
  - Los emisores y receptores de §6.1 están en prosa («Broker → Coordinador»); compararlos con `CANALES` exigiría el inventario
    de agentes de §4.2, fuera del kit. El verificador compara la existencia de cada CT y que su canal admita algún par.
  - Los `ESQUEMAS` de `contratos.py` son de respuestas de agentes, no de contratos CT: no entran en (a).
  - (e) mira solo las citas de `02_System_prompts/` y `03_Funciones/`, como pide el prompt. Las definiciones son los
    encabezados de `05_Archivos_operativos` (`#### RF-0001 ·`, `## TA-01 …`) y las filas de los Registros de bajas.
  - Una cita F1–F10 puede ser archivo o fase: solo se señala la que no es ninguna de las dos.
  - Los contextos ajenos son heurísticos y están a la vista; un caso nuevo se añade como regla con su prueba.
  - El informe del documento de auditoría lleva las huellas de `servicio.py` y `contratos.py`: queda desfasado en cuanto otra tarea
    los cambie; se regenera con `--auditoria`. Ninguna prueba compara el documento con el código, para no romper las suites de
    otras tareas.
  - `detect-secrets` (pre-commit) no está instalado en este `.venv`; si se instala, las huellas SHA-256 del informe pueden salir
    como «Hex High Entropy String» (falsos positivos, como las huellas hex ya auditadas en `.secrets.baseline`).
- **Comandos exactos para probarlo:**

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t157_verificador_ids.py
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids | head -40          # informe por la salida estándar
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids --raiz /ruta/sin/catalogo; echo $?   # 2, fallo cerrado
```
