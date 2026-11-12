# T-101 · Análisis técnico

## Motivo

- Con los doce perfiles, un ciclo C1 del Bloque A hace 77 llamadas a 20 agentes y lee unos 1,66 millones de tokens de entrada; el 90 % son prompts de sistema (`.docs/diseno/bloque_a/propuesta_claude.md`).
- La revisión C-01 de Astra acepta el rumbo con cambios, y la decisión de Claude los recoge (`decision_claude_c01.md`).
- El operador pidió implementarlo el 12-11-2026.

## Implementación

| Pieza | Fichero | Qué hace |
| --- | --- | --- |
| Selección del diseño | `config/por_defecto.yaml` (`diseno`, sección `v6`) y `diseno_v6.validar` | `v5` por defecto; un valor desconocido falla al crear el Bloque |
| Núcleo y kits | `prompts.py` (`nucleo_comun`, `kit`, `secciones`, `identidad`) | Deriva del marco común V5.0 un núcleo sin marcadores, igual para los doce, y de cada prompt V5.0 un kit: identidad, §6, cada sección que difiere del marco (el ejemplo de la §11; en ALT, IDX, FON y DER también la §2 o la §12) y, si se pide, la §10. El system de un analista V6 tiene dos puntos de caché: núcleo con interfaz, y kit |
| Caché del simulador | `llm.MockClient.generar` | Por prefijo y por modelo, como la API: lee el prefijo guardado más largo y escribe el resto hasta el último punto |
| GC1 por código | `diseno_v6.gc1` | Hasta `max_candidatas` con señal ≥ `umbral_senal_gc1`. Exploración sembrada por fecha, tipo y símbolo. Lo que no tiene señal pasa marcado, y lo vigente siempre pasa. Un ámbito de exploración que acaba de finalista es un falso negativo |
| Prospectiva por ciclo | `diseno_v6.prospectiva_global` | Lotes de `max_encargos_por_lote` (o por tipo) con referencias `tipo:símbolo`. Lo que falta se pide una vez más; si sigue faltando, queda `_prospectiva_omitida` |
| Contradictor de la selección | `diseno_v6.seleccion_con_critica` y `refutacion_global` | Las finalistas nuevas N2/N3 llegan con `_critica_pendiente` (PS5 provisional en `_puertas`). Se critica lo que queda en un top-3, se vuelve a seleccionar y se critican las sustitutas, hasta `max_rondas_sustitucion` rondas. El protocolo PA-05 es el mismo de la V5, pero con una llamada por lote para todos los tipos. Lo que queda sin crítica deja de ser elegible. `_seleccionar` conserva el identificador OPP- entre rondas (`_opp_fijado`) |
| Presupuesto | `diseno_v6.repartir_presupuesto` | La parte de prospectiva y refutación de cada tipo pasa a la bolsa `V6_GLOBAL`; el total no cambia |
| Integración y Sintetizador | `diseno_v6.integracion_determinista` y `sintetizar` | Antes de G3, el régimen por tipo y los cambios frente al run anterior. Después de G3, una llamada a AG-26: de su respuesta solo se toman textos (régimen, factor de cada clúster existente, preguntas, lectura, limitaciones y los del Redactor). Después, la generación de los entregables con la segunda pasada de HT-09 |
| Papeles nuevos | `prompts_v6/` y `contratos.CANALES_V6` | AG-26, AG-27 y AG-28, con canales que solo se abren con la V6 (R2) |
| A código | `orquestacion.py` | Curación sin AG-12, dictamen G3 sin AG-18, sin informe AG-20 y Auditor por muestreo (`auditar_este_run`) |
| Cobertura y contrafactual | `diseno_v6.registrar_cobertura` y `resolver_contrafactual` | `COB-` en HA por run: filas por candidata, GC1, muestra de descartes con precio y elegidas. `CTF-` una sola vez cuando vence el horizonte, con las rentabilidades de los descartes frente a las elegidas |
| Coste completo | `agentes.py`, `consumo.py` y `backtest.py` | `intento` y `latencia_s` por llamada; `reintentos` y `latencia_s` por run, también en `consumo.csv` |
| Segundo proveedor | `Agentes.clientes` y `Bloque(cliente_contradictor=…)` | Cliente propio para AG-11. Si falta, la limitación se declara en el informe |

## Decisiones

- **La V5 sigue por defecto** (decisión 1 de la tanda 1). Cada pieza de la V6 tiene su interruptor, salvo que con la Prospectiva global la crítica es siempre de la selección. Combinar la Prospectiva global con la crítica de todas las finalistas no tiene sentido y falla.
- **Las referencias de los lotes son `tipo:símbolo`** porque un mismo símbolo podría estar en dos tipos. Los identificadores de las objeciones siguen siendo `OBJ-<símbolo>-nn`, como en la V5.
- **Los canales nuevos solo se abren con la V6** (`Mensajeria(v6=…)`), para no ampliar los canales de la V5.
- **El simulador pasa a cachear por prefijo.** No cambia ninguna de las 476 pruebas de la V5 y es más fiel a la API.

## Límites

- **GC1 con la señal compuesta y el umbral 0,75** apenas deja pasar ámbitos de renta fija, liquidez y tipos, porque su señal compuesta es baja por construcción. El Analista simulado de la V5 usa 0,55 y deja pasar más. La exploración de la V6 detecta los falsos negativos (EMB y ^VIX el 2026-06-05). Falta el catálogo de señales por perfil (`v6.gc1.senal_por_perfil`, `[PROPUESTO]`, va con K).
- **El Lector de evidencia** sigue haciendo una llamada por petición dentro de cada tipo; no hay lote por ciclo.
- **Con el simulador** solo se miden el flujo y el consumo; la calidad se medirá con la API real (Fase 5).
