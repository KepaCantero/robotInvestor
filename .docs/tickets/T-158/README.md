# T-158 · Guías de mejora del Orquestador (CT-18) en el ejecutor del Bloque A

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (ejecutor, `11_Ejecutor`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (regla del 12-11-2026, `compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: corrección de una función que deja PB-48 a medias; lo que el diseño no dice se decide por defecto (regla del 13-11-2026) y va al registro de decisiones |
| Deuda técnica | T-158 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que el ejecutor emita y aplique las guías de mejora CT-18 del Orquestador y que, ante un ítem que contradice una regla, mande la norma más restrictiva (R23), el conflicto quede en HA (COR-), se escale (P3-, cola de tipo 3) y el Orquestador retire el ítem de la guía. Cierra la cláusula pendiente de PB-48 (INC-T126-01).

## Kit de contexto leído (regla 1)

- Documento 0 V5.1: 0.2 (jerarquía de prevalencia), R23, 5.1 (HA: «guías»), 6.1 (CT-18), 6.2, 12.1 (nivel A), 18.1 y 18.3 (tipos de cambio y conflictos), Anexo B («CT-16 a CT-22: campos en los prompts del Orquestador…»).
- Plan de pruebas V3.0: PB-48 y la batería de regresión (§6).
- Prompt del Orquestador V5.0 (dato en runtime, no se edita): 4.5 (forma del CT-18), 6.8 (tipos y reclasificación obligatoria), 6.9 (guías: contenido, límites absolutos, versionado, transmisión), 10.8.
- Prompt del Analizador V5.0, línea de CT-18: «aplicas las de tipo 1 y 2 si no contradicen el Documento 0; … la registras y no la aplicas».
- Esquema de HA V2.0 (`05_Archivos_operativos`): 4.4 (GUI-), 4.8 (P3- y COR-), 5 (estados).
- Código: `contratos.py` (CT-18, `Mensajeria`), `orquestacion.py` (ciclo, `_invocar`, `_registrar_run`), `almacen.py` (HA), `mock_respuestas.py` y `MockClient` (no hace falta tocarlos).

## Alcance

- Entra: módulo nuevo `bloque_a/guias.py` con el esquema del cuerpo CT-18 de tipo GUIA, la emisión por la mensajería, la revisión del receptor (control doble, R23), el registro COR- y P3- en HA, la retirada del ítem (versión nueva o RETIRADA) y las guías aplicables por agente; su enganche en el ciclo y en `_invocar`; F5 anota las guías aplicadas; CLI `bloque-a guia emitir|listar`; sección `guias_orquestador` de `por_defecto.yaml`; pruebas; mapa del plan de pruebas (PB-48); incidencia y registro de decisiones.
- No entra: que el Orquestador (modelo) redacte guías a partir de hallazgos y lecciones (Fase 5, con el modelo real); los otros dos usos de CT-18 (orden de instancias y autorización de presupuesto, que hoy van a HA como ORD- y AUT- sin mensaje); la medición de eficacia de las guías (10.6); la revisión mensual de caducidades; `contratos.py`, los goldens, el Documento 0 y el corpus.

## Diseño

- **Contratos.** CT-18 ya existe en `CANALES` (AG-18 → cualquier agente) y está exento de `run_id`. No se toca `contratos.py`: la mensajería sigue validando el sobre (canal, R8, versión) y el **cuerpo** de tipo GUIA se valida contra `guias.ESQUEMA_CT18_GUIA` (jsonschema, Draft 2020-12) al emitir y otra vez al aplicar. Así no cambia ninguna tabla, esquema de respuesta ni mensaje de los flujos congelados (los goldens coinciden sin re-congelar). Los casos CT-18 de la batería (`{"guia": "…"}`) los sigue admitiendo la mensajería, como hoy; el receptor no los aplicaría (no cumplen el esquema del cuerpo).
- **Esquema derivado** (prompt del Orquestador 4.5 y 6.9, HA 4.4): `tipo_ct18` = `GUIA` (el sobre ya usa `tipo_mensaje` para ENCARGO/RETORNO), `guia_id` `GUI-AGnn-NNNN`, `version` ≥ 1, `sustituye` (id o null), `fecha_aplicacion`, `acuse_requerido` = true e `items` (≥ 1) con `item_id` `GUI-AGnn-NNNN-nn`, `tipo` 1 o 2, `origen` (HAL- o LEC-, al menos uno), `que_cambia`, `donde_se_comprueba`, `como_se_sabe` y `caducidad`. Se admiten campos adicionales (6.2.3: el esquema del operador puede ampliarlos).
- **Estado persistido.** HA gana tres tipos de entrada ya definidos en su esquema V2.0: GUI- (alta ISSUED con acuse; cambios a SUPERSEDED o RETIRADA, entradas nuevas con el mismo `id`), COR- y P3- (origen ORQ, PENDING_OPERATOR). F5 lleva `guias_aplicadas` en el RUN solo si se aplicó alguna. No hay migración: son entradas nuevas en ficheros append-only.
- **Flujo.** `Guias.emitir(receptor, items)` (el Orquestador) numera la versión, valida el cuerpo, crea el CT-18 y registra la guía en HA; la anterior del mismo agente pasa a SUPERSEDED. Al empezar cada ciclo (F0) y en la primera llamada a un modelo de una consulta o seguimiento, `Guias.cargar` revisa todas las guías ISSUED: el receptor repite la verificación de 6.8 y 6.9 (control doble) con `conflicto_del_item`; cada ítem en conflicto deja un COR- y un P3- y el Orquestador emite la versión siguiente sin él (o la guía pasa a RETIRADA si no queda ninguno). Los ítems válidos, vigentes y sin caducar llegan al contexto del agente receptor (`contexto["guias"]`), nunca a HT-03 ni a las puertas: la regla de código manda siempre.
- **Números.** `guias_orquestador.max_items_por_version: 8`, `max_hallazgos_por_version: 10` y `caducidad_por_defecto_meses: 6` (prompt del Orquestador 6.9: «Máximo 10 hallazgos y 8 ítems por versión de guía»; «caducidad por defecto, 2 trimestres»).
- **Cómo falla cerrado.** Un cuerpo que no cumple el esquema o los límites no se emite (excepción, sin escribir nada); una guía de HA que no cumple el esquema no se aplica (pasa a RETIRADA con su incidencia); si la revisión no se puede hacer, no se aplica ninguna guía en ese run y queda una incidencia HERRAMIENTA. Un ítem dudoso para el detector se trata como conflicto (se retira y se escala), nunca al revés.
- **Decisiones `[PROPUESTO]`** (decididas por Claude por defecto; INC-T126-01 y registro de decisiones): ver `analisis-tecnico.md`, sección «Decisiones».

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| El detector de conflictos lee texto libre | Falsos negativos (una paráfrasis pasa) o positivos (un ítem válido se retira) | El falso positivo solo retira y escala (prudente). El negativo solo llega como contexto al modelo: HT-03, PS1–PS8 y G3 son código y no leen guías (R23 por construcción). Límites en la incidencia |
| Cambiar la forma de un mensaje congelado | Re-congelar goldens que lleva otra tarea (T-143) | No se toca `contratos.py`; los campos nuevos solo aparecen con guías, que ningún flujo congelado emite; se ejecuta `goldens_ct.py` |
| Leer HA en cada llamada | Coste en un ciclo con muchas llamadas | Una revisión por run, en caché por `run_id` |
| Hilos de los Analistas | Carreras al anotar las guías aplicadas | Cerrojo en `Guias` |

## Criterios de aceptación (binarios)

1. CA-1: un cuerpo CT-18 de tipo GUIA que cumple el esquema se emite por la mensajería (AG-18 → receptor) y queda en HA como GUI- ISSUED con su acuse; el anterior del agente pasa a SUPERSEDED.
2. CA-2: un cuerpo que no cumple el esquema o los límites de la configuración no se emite y HA no cambia; una guía de HA que no cumple el esquema no se aplica.
3. CA-3: un ítem válido y vigente llega al contexto del agente receptor (no al de otros) y el RUN de F5 anota la guía aplicada; uno caducado o con fecha de aplicación futura no llega.
4. CA-4 (PB-48): con una guía de tipo 2 vigente para AG-02 que sugiere omitir la segunda pasada en banda marginal, en un ciclo con `--cliente mock` la segunda pasada queda registrada en F3, hay un COR- y un P3- (PENDING_OPERATOR) en HA, el ítem se retira de la guía y su texto no llega a ningún agente ni a HT-03.
5. CA-5: con un ítem en conflicto y otro válido, la versión siguiente conserva solo el válido (sustituye a la anterior) y se envía por CT-18.
6. CA-6: sin guías, el ciclo no cambia: los goldens de contratos coinciden y la suite de A no baja.
7. CA-7: determinista (misma entrada, mismos identificadores y entradas) y sin red; números de `por_defecto.yaml`.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t158_guias.py` (emisión, versión, esquema, límites, aplicables, contexto, F5) | Nominal, límite, fallo cerrado, contrato | CA-1, CA-2, CA-3, CA-5, CA-7 |
| `test_pb48_*` de extremo a extremo con el cliente simulado | Integración | CA-4 |
| Detector: ítems del prompt (ejemplo de 4.5) y variantes que relajan | Nominal, fallo cerrado | CA-4 |
| `tests/test_t126_pb26_pb48.py`, `tests/test_t126_r02.py`, `tests/test_fase4_mapa.py` | Regresión | CA-6 |
| `tests/goldens_ct.py` y `tests/test_fase3_goldens.py` | Contrato | CA-6 |
| Suite completa de A | Regresión | CA-6 |

## Scripts

- `.docs/scripts/nuevo_ticket.sh` (abre el ticket).
- `.docs/scripts/evidencias_plan_a.py` (mapa y documento de evidencias).
- `bloque_a/11_Ejecutor/tests/goldens_ct.py` (comprobación de goldens, sin re-congelar).

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · PLANIFICADO · claude · plan y criterios escritos
- 2026-11-15 · EN CURSO · claude · implementación
- 2026-11-15 · EN QA · claude · implementado y probado; QA con un revisor nuevo
