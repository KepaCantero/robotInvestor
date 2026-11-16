# T-157 · Fase 0: verificador de consistencia de IDs del Bloque A

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (ejecutor: `bloque_a/11_Ejecutor/bloque_a/herramientas/verificador_ids.py`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (regla del 12-11-2026, `compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: herramienta de medida, sin cambio de contrato, de corpus ni de controles (tipo «corrección, pruebas, documentación» de `ri-planificar`) |
| Deuda técnica | T-157 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la reserva la sesión coordinadora; este ticket no la toca) |

## Objetivo

Medir con un comando qué identificadores están desincronizados entre el corpus vigente del Bloque A y el código del ejecutor
(contratos CT, reglas R, archivos F, fichas del Catálogo, referencias de los archivos operativos y puertas PS), con un informe
JSON y Markdown en el que cada dato sale del corpus y del código escaneados. Es la Fase 0 de `CLAUDE.md`; el prompt de la fase,
tal cual, es `prompts/FASE0_VERIFICADOR_IDS.md`; las notas de la sesión coordinadora que lo actualizan (línea base, desfase V4.0↔V5.0 ya resuelto, Documento 0 por patrón) están en el encargo.

## Alcance

- Entra:
  - `bloque_a/11_Ejecutor/bloque_a/herramientas/verificador_ids.py` (nuevo): escáner, informe JSON validado contra su esquema y
    Markdown; orden `python -m bloque_a.herramientas.verificador_ids`.
  - `bloque_a/11_Ejecutor/tests/test_t157_verificador_ids.py` (nuevo): un corpus de juguete con al menos un fallo de cada clase
    y pruebas contra el corpus y el código reales.
  - `docs/auditoria_ids_bloque_a.md` (nuevo): el informe generado más una tabla de decisiones PROPUESTAS (no se aplican).
  - `docs/auditoria_ids_bloque_a.json` (nuevo): el mismo informe en JSON.
  - `docs/incidencias.md`: una entrada INC-T157-xx por decisión propuesta, con su porqué.
  - `docs/AVANCE.md`: la entrada de la Fase 0.
  - `tools/refs_allowlist.txt`: quitar las dos líneas de la Fase 0 cuando existan los entregables.
  - `bloque_a/11_Ejecutor/README.md`: la orden del verificador en la estructura.
  - En el ticket, `mutantes_t157.py` (mutantes de las protecciones) y `handoff.md`; una lección en `.docs/memoria/claude/`.
- No entra:
  - Ningún `.md` ni `.docx` del corpus (canónicos); ni `99_Historico*` (no se lee ni se escanea).
  - Resolver ningún desfase: las decisiones solo se proponen.
  - `bloque_a_forex/`, `bloque_b/`, la deuda técnica, el Documento 0, los goldens, `tests/test_fase3_goldens.py`, `llm.py`,
    `consumo.py`, `orquestacion.py`, `cadena_b.py` y `motor/frontera_b.py` (otras tareas).

## Diseño

- **Entradas, sin nombres fijos.** El Documento 0 se busca por patrón (`Documento 0*.md`) en `bloque_a/01_Gobernanza/`: si hay
  cero o más de uno, el verificador falla cerrado (salida 2) sin informe. Igual el Catálogo (`Catálogo de cálculos del Motor*.md`
  en `04_Motor_conocimiento_y_catalogo/`). Los nombres se comparan en NFC. El informe dice qué versión leyó (nombre y H2) y la
  huella SHA-256 de cada entrada.
- **Secciones del Documento 0.** Solo §1 (tabla R), §5.1 (inventario), §6.1 (tabla CT), §9.3 (tabla PS) y el título de §7.3 (la
  lista de fases F0–F10, para no confundir «fase F3» con «archivo F3»). Si falta una sección o su tabla, falla cerrado. El rango
  del título (R1–R27, CT-01 a CT-25) se contrasta con las filas de la tabla: ningún número está escrito en el código.
- **Corpus escaneado.** Todos los `.md` de `bloque_a/` salvo `11_Ejecutor/` (código) y `99_Historico*`. Para (e), solo
  `02_System_prompts/` y `03_Funciones/` citan; las definiciones se indexan de `05_Archivos_operativos/` por identificador
  (encabezados `#### ID ·`, filas `| TA-01 |`, títulos `## TA-01`) y el «Registro de bajas»; F7, F8 y F9 no se cargan en
  contexto (regla 6): el verificador solo extrae sus identificadores.
- **Código.** Se importa el paquete (`motor/servicio.py`, `contratos.py`), no se interpreta su texto: `CATALOG_VERSION`,
  `FICHAS_CATALOGO`, `IMPLEMENTADAS`, `SERVICIOS_CT10`, `DOCUMENTADAS_CON_CODIGO`, `RUTA_CATALOGO`, `madurez_catalogo()`,
  `servible()`, `CANALES`, `CANALES_V6`, `CAMPOS_MINIMOS` y `canal_permitido`. Las pruebas pasan un `Codigo` de juguete.
- **Clases del informe.** (a) CT, (b) R, (c) F con el mapa código → archivo real por su H1, (d) fichas (IMPLEMENTADO,
  SOLO_CATALOGO, SOLO_CODIGO, ID_DISTINTO), madurez del índice §4 frente a manejadores, versión del Catálogo y menciones de otra
  versión, (e) referencias RF/TA/TM/TF/ANA-DOC/DOC-MOT, y (f) puertas PS1–PS8 (§9 está en el kit de la fase). Cada hallazgo
  lleva nivel (`ERROR`, `AVISO`, `INFO`), motivo y ubicaciones (archivo y línea).
- **Contratos.** No cambia ningún contrato CT ni esquema del corpus. El informe JSON tiene esquema propio en el módulo
  (`ESQUEMA_INFORME`, JSON Schema 2020-12) y se valida antes de escribirlo; si no valida, no se escribe.
- **Estado persistido:** no cambia.
- **Números:** ninguno a mano. Rangos y conteos salen del corpus; la tolerancia de «ID parecido» (distancia de edición ≤ 2 o mismo
  tallo con otro número) es un criterio técnico del verificador, declarado en el informe `[PROPUESTO INC-T157-…, técnico]`.
- **Falla cerrado:** entrada ausente, ambigua o ilegible → salida 2 y mensaje; nunca un informe parcial.
- **Salidas:** 0 sin errores, 1 con errores, 2 fallo cerrado. Determinista: sin hora ni rutas absolutas en el informe.
- **Decisiones del operador usadas como `[PROPUESTO]`:** las decisiones de resolución del informe, solo propuestas (INC-T157-xx).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Falsos positivos de los patrones (p. ej. «F1» como fase, «R2» en otro sentido) | Errores que no lo son | Fases de §7.3 separadas de archivos; los patrones exigen frontera de palabra; prueba con el corpus real |
| T-143 cambia el Documento 0 a V5.2 | Un nombre fijo dejaría el verificador roto | Búsqueda por patrón y fallo cerrado si no hay exactamente uno; prueba de 0 y de 2 Documentos 0 |
| Leer F7/F8/F9 enteros en contexto | Viola la regla 6 | Solo el verificador los recorre y extrae identificadores |
| La suite de A es lenta (≈6 600 pruebas) | Tiempo | Una pasada en segundo plano; el módulo nuevo se prueba aparte |

## Criterios de aceptación (binarios)

1. CA-1: `python -m bloque_a.herramientas.verificador_ids` (desde `bloque_a/11_Ejecutor`) escribe el informe JSON y Markdown y
   sale 0 sin errores o 1 con errores.
2. CA-2: con el corpus de juguete, el informe da al menos un ERROR de cada clase (a) a (e): CT inexistente, R inexistente, F
   inexistente, ficha SOLO_CATALOGO, SOLO_CODIGO e ID_DISTINTO, y referencia inexistente; y una mención «Catálogo V4.0».
3. CA-3: (c) da el mapa código → archivo por el H1, y señala un archivo cuyo H1 no coincide con §5.1.
4. CA-4: con cero o dos Documentos 0, o sin Catálogo, falla cerrado (salida 2, sin informe).
5. CA-5: el informe dice la versión del Documento 0 leída y la huella de cada entrada; dos ejecuciones dan el mismo JSON.
6. CA-6: el JSON valida contra `ESQUEMA_INFORME`; un informe que no valida no se escribe.
7. CA-7: no lee `99_Historico*` (una cita rota dentro de una carpeta así no aparece).
8. CA-8: con el corpus y el código reales, las cifras del informe coinciden con lo que se cuenta por separado (81 fichas en el
   Catálogo, `CATALOG_VERSION` igual a la del Catálogo, 25 CT en §6.1 y en `CANALES`) — la prueba las cuenta con su propio
   código, no con el del verificador.
9. CA-9: `docs/auditoria_ids_bloque_a.md` contiene el informe generado y la tabla de decisiones propuestas; cada decisión tiene
   su INC-T157-xx en `docs/incidencias.md`.
10. CA-10: la suite de A sigue entera en verde (ninguna falla), ruff ≤ 2831, mypy A ≤ 109, y los gates ligeros en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Corpus de juguete con un fallo de cada clase | nominal / fallo | CA-2, CA-3 |
| Sin Documento 0, con dos, sin Catálogo, sin sección §6.1 | fallo cerrado | CA-4 |
| Dos ejecuciones, mismo JSON; versión y huellas | determinismo | CA-5 |
| Informe alterado que no valida | contrato | CA-6 |
| Cita rota en `99_Historico_X/` | límite | CA-7 |
| Corpus y código reales contados aparte | integración | CA-8 |
| La orden de consola escribe JSON y Markdown y su salida | integración | CA-1 |
| Suite de A, ruff, mypy, gates ligeros | regresión | CA-10 |

## Scripts

Ninguno nuevo en `.docs/scripts/`: la orden repetible es el propio módulo (`python -m bloque_a.herramientas.verificador_ids`),
que además regenera el bloque del informe dentro de `docs/auditoria_ids_bloque_a.md` con `--auditoria`.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · PLANIFICADO · claude · plan y criterios escritos
- 2026-11-15 · EN CURSO · claude · implementación y pruebas
- 2026-11-15 · EN QA · claude · implementado y probado; commit local «wip local: T-157»; el commit definitivo lo hace la sesión coordinadora
