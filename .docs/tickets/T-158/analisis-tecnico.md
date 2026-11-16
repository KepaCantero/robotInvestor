# T-158 · Análisis técnico

## Causa raíz o motivo

El ejecutor tenía el canal CT-18 (AG-18 → cualquier agente) en `contratos.CANALES`, pero nada lo usaba: el Orquestador no emitía guías y ningún agente las cargaba. Por eso PB-48 («Conflicto de normas: la más restrictiva») solo podía probar R23 por construcción (HT-03 exige la segunda pasada) y no su criterio de aprobación: «Segunda pasada registrada; COR- y P3- en HA» (INC-T126-01).

## Evidencia

- Plan de pruebas V3.0, PB-48: preparación «Guía de tipo 2 vigente que sugiere omitir la segunda pasada en banda marginal»; resultado «el Analizador aplica la segunda pasada (regla más restrictiva), registra el conflicto y lo escala; el Orquestador reclasifica el ítem como tipo 3 y lo retira de la guía».
- Documento 0 V5.1: 0.2 (las guías de tipos 1 y 2 están por debajo del Documento 0 y del prompt), R23, 18.3 («el conflicto se registra en HA, se aplica la regla más restrictiva de forma provisional y se escala»); el Anexo B remite los campos de CT-18 al prompt del Orquestador.
- Prompt del Orquestador V5.0: 4.5 (forma del CT-18 de guía), 6.8 (reclasificación obligatoria; «el agente receptor repite la verificación: el control es doble y registrado»), 6.9 (límites absolutos, 8 ítems y 10 hallazgos por versión, caducidad de 2 trimestres, versionado y acuse).
- Esquema de HA V2.0: GUI- (4.4), P3- y COR- (4.8), estados (5).
- Antes de T-158: `grep -rn "CT-18" bloque_a/11_Ejecutor/bloque_a` solo daba la tabla de canales y la exención de `run_id`.

## Implementación

- **Archivos cambiados y por qué.**
  - `bloque_a/11_Ejecutor/bloque_a/guias.py` (nuevo): `ESQUEMA_CT18_GUIA` (primero el esquema) y `validar_cuerpo`; `conflicto_del_item` (control doble del receptor); `Guias` con `emitir` (Orquestador: numera, valida, envía por la mensajería, registra GUI- ISSUED con acuse y pasa la anterior a SUPERSEDED), `cargar` (F0: revisa todas las guías ISSUED una vez por run; conflicto → COR- y P3- y retirada), `para` (ítems aplicables del agente, para su contexto) y `aplicadas` (para F5).
  - `bloque_a/11_Ejecutor/bloque_a/orquestacion.py`: `self.guias = Guias(self)`; `ciclo` llama a `guias.cargar` justo después de numerar el run (antes del C5); `_invocar` añade `contexto["guias"]` solo si el agente tiene ítems aplicables; `_registrar_run` añade `guias_aplicadas` al RUN de F5 solo si hubo alguna. Además se quitan tres importaciones sin uso (`ESQUEMAS`, `contiene_credenciales`, `fecha_resolucion`), que bajan ruff de 2831 a 2828.
  - `bloque_a/11_Ejecutor/bloque_a/cli.py`: subcomando `guia emitir|listar`.
  - `bloque_a/11_Ejecutor/config/por_defecto.yaml`: sección `guias_orquestador` (8, 10, 6) con su origen.
  - `bloque_a/11_Ejecutor/ejemplos/guias/guia_pb48.json`: la guía de PB-48 con un ítem en conflicto y otro válido, para la CLI.
  - `bloque_a/11_Ejecutor/tests/test_t158_guias.py` (nuevo, 55 pruebas).
  - `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`: PB-48 pasa a AUTOMATICA con las pruebas nuevas.
  - `bloque_a/11_Ejecutor/README.md`, `docs/incidencias.md` (INC-T126-01, viñeta T-158), `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (fila de la sección 6), `docs/evidencias_pruebas_bloque_a.md` (regenerado).
- **No se toca:** `contratos.py`, los goldens, `llm.py`, `mock_respuestas.py`, `consumo.py`, `cadena_b.py`, `motor/frontera_b.py`, el Documento 0, `tests/test_t154.py`, otros bloques ni el corpus.

### Decisiones (`[PROPUESTO]`, decididas por Claude por defecto; en INC-T126-01 y en el registro de decisiones)

1. **El esquema del cuerpo vive en `guias.py`, no en la mensajería.** La mensajería valida el sobre (canal R2, datos protegidos R8, versión), como para todos los contratos; el cuerpo de tipo GUIA lo validan el emisor (`emitir`) y el receptor (`cargar`). Así no cambia ninguna tabla de `contratos.py` (`CAMPOS_MINIMOS`, `ESQUEMAS`), ni la batería (los casos `CT-18/*` de `bateria_mensajes.json`, con cuerpo `{"guia": "…"}`, siguen ADMITIDOS por la mensajería, como hoy) ni los flujos simulados (ningún flujo congelado emite guías). **Los goldens no cambian** (`tests/goldens_ct.py`: «goldens de contratos: coinciden»).
2. **`tipo_ct18: "GUIA"`** en lugar del `tipo_mensaje: "GUIA"` del prompt (4.5): el sobre del ejecutor ya usa `tipo_mensaje` para ENCARGO/RETORNO y `Mensajeria.crear` no deja cambiarlo desde el cuerpo. Se admiten campos adicionales (6.2.3).
3. **Identificadores:** `guia_id` `GUI-AGnn-NNNN` con NNNN igual a la versión (como en el ejemplo del prompt), `item_id` `<guia_id>-nn`; `sustituye` es la guía ISSUED del agente (o null si no hay ninguna).
4. **Revisión en el receptor al empezar cada run**, no al emitir. El Orquestador (modelo) filtra al redactar (6.8); el código hace el control doble del receptor antes de aplicar nada, y así el caso del plan (una guía vigente con el ítem) se puede ejercer. Ninguna guía se aplica sin revisar.
5. **Detector:** solo `que_cambia`, tres familias (tipo 3 por la reclasificación obligatoria; un control o regla junto a una acción que lo quita o rebaja; credenciales o cambiar un prompt o un contrato). Ante la duda, conflicto.
6. **COR- y P3-** según HA 4.8; el P3- es del Orquestador (`P3-ORQ-`, origen ORQ, `detectado_por` el receptor), en PENDING_OPERATOR; `pruebas_regresion` = batería del §6 del plan + PB-48; `npr` nulo; sin `antiguedad_dias` (se calcula al informar).
7. **Retirada:** versión nueva con los ítems válidos (enviada por CT-18) o RETIRADA si no queda ninguno. El HAL- de origen no se marca RECLASIFICADO.
8. **Aplicación:** contexto del agente receptor (`contexto["guias"]`) y `guias_aplicadas` en F5; no se pide al modelo que repita la `guia_id` (cambiaría los esquemas de respuesta, congelados).
9. **Fallo cerrado:** cuerpo inválido → `MensajeInvalido` sin escribir nada; guía de HA inválida → RETIRADA + incidencia HERRAMIENTA; revisión que falla → ninguna guía en ese run + incidencia; caducidad: se aplica hasta su fecha incluida; si caducan todos los ítems, RETIRADA.

- **Desviaciones del plan:** ninguna de alcance. Se añadió la CLI (`guia emitir|listar`) y el ejemplo, para que el caso funcione con `--cliente mock` desde la línea de órdenes.
- **Límites conocidos:**
  - El detector lee texto libre: una paráfrasis o un ítem en otro idioma no se reconoce y llega como contexto al modelo receptor; no llega a HT-03, a las puertas ni a G3 (código). Un ítem válido que nombra un control y una acción de las de la lista por motivos distintos se retira y se escala (falso positivo prudente). Lección conocida: `claude/2026-11-12_filtros-por-patron-en-texto-libre`; aquí el fallo del filtro no rompe ningún control, solo deja de registrar el conflicto.
  - El ejecutor no redacta guías: las emite quien llama a `emitir` (la CLI, una prueba o, en la Fase 5, el Orquestador con el modelo real).
  - No se mide la eficacia (10.6) ni se hace el mantenimiento mensual (caducidades, cola de tipo 3); los otros dos usos de CT-18 (instancias, presupuesto) siguen sin mensaje.
  - El `.venv` está enlazado al repositorio principal: el `bloque-a` instalado apunta a la copia principal; en esta copia la CLI se prueba con `python -m bloque_a.cli` desde `bloque_a/11_Ejecutor`.
- **Comandos exactos para probarlo** (desde `bloque_a/11_Ejecutor`):
  - `../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t158_guias.py`
  - `../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t126_pb26_pb48.py tests/test_t126_r02.py tests/test_fase3_goldens.py tests/test_fase4_mapa.py`
  - `../../.venv/bin/python tests/goldens_ct.py`
  - CLI con el simulado: `../../.venv/bin/python -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos --estado /tmp/e --salida /tmp/s --as-of 2026-06-05 guia emitir --receptor AG-02 --json ejemplos/guias/guia_pb48.json`, después `… ciclo` y `… guia listar` (GUI-AG02-0001 SUPERSEDED, GUI-AG02-0002 ISSUED con el ítem válido; COR-2026-0001 y P3-ORQ-2026-0001 en `HA_historial_auditorias.jsonl`).
  - Desde la raíz: `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-48`.
