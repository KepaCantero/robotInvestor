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

## Ronda r02 (hallazgos de la QA r01)

| Hallazgo | Corrección |
| --- | --- |
| H-01 | La cobertura tiene fila para cada ámbito que recibe el Analista y no propone (fase ANALISTA, con su motivo si lo declara), para cada vigente mantenida en el top-3 (SELECCION_FINAL, `vigente`) y para cada vigente cerrada (CIERRE). La muestra de descartes sale de las filas con símbolo |
| H-02 | CA-8 se reformula en el README del ticket, con la reformulación registrada: menos llamadas y menos tokens de entrada, con caché y sin ella |
| H-03 | Lo que el Contradictor no devuelve en dos intentos queda en `sin_respuesta`. Se declara en las limitaciones y en la cobertura (fase CRITICA, «no la devolvió») y deja el run PARCIAL. También lo deja PARCIAL lo que queda sin crítica o sin pronóstico |
| H-04 | El reintento de Prospectiva y del Contradictor lleva `reintento_de_cobertura` con las refs que faltan. Así es otro encargo y no sale de la caché HT-06 con la misma respuesta incompleta |
| H-05 | Con GC1 por código, la instrucción del Analista explica las marcas (`NOTA_GC1`): EXPLORACION y SIN_SENAL_MEDIBLE no se descartan por la señal, y `paso_gc1` es el juicio del Analista |
| H-06 | Una señal NaN o infinita cuenta como no medible: pasa marcada y no ordena ni descarta |
| H-07 | `diseno_v6.validar` comprueba la sección `v6` al crear el Bloque: enteros y sus mínimos, la fracción del Auditor, los enumerados, el horizonte, el catálogo de señales y los límites del Sintetizador. El `presupuesto_override` se aplica antes de repartir la bolsa del ciclo |
| H-08 | Las longitudes de los textos del Sintetizador salen de `v6.sintetizador_limites`. El presupuesto del mensaje CT-15 es el de la bolsa común. `tope_tokens_system` y `horizonte_contrafactual` quedan marcados `[PROPUESTO]` y en T-57 |
| H-09 | Un texto del Sintetizador con una probabilidad numérica (R13) o con la compra de un instrumento (R21, más `sintesis._UNITARIA`) no se toma y se declara. En los textos llanos, se usan los textos por defecto. En la V5, la integración de AG-02 sigue sin ese filtro, y queda en la deuda |
| H-10 | Si al vencer no hay ningún precio de lo que se podía medir, el contrafactual espera al ciclo siguiente. Con datos parciales se resuelve y cuenta `sin_precio`. La documentación dice que lo escribe el ciclo V6 en HA |
| H-11 | 23 pruebas nuevas contra los mutantes vivos: sin rondas de sustitución (M08, M09, M18 y M27), el Contradictor sin respuesta y su reintento (M06 y H-03), la caché en el reintento (H-04), refs no pedidas (M25), OPP- estables (M14), GC1 con más de `max_candidatas` y con NaN (M01 y H-06), falsos negativos (M23), el Evaluador con resueltos (M24), el Auditor en vivo (M26) y el contrafactual la víspera y sin precios (M12 y H-10) |

## Ronda r03 (hallazgos de la QA r02)

| Hallazgo | Corrección |
| --- | --- |
| H-12 | El filtro R13/R21 se rehace por patrones. R13: un porcentaje «de probabilidad/posibilidad/opciones», o una de esas palabras seguida de una cifra en la misma frase, salvo «de las veces». R21: un ISIN, un sufijo societario, un bono con año de vencimiento, `sintesis._UNITARIA`, un verbo de compra o venta junto a un código en mayúsculas o un código entre paréntesis que no está en `v6.filtro_r21_codigos` ni en el universo. Lo que no tiene patrón (un nombre propio suelto) queda como límite declarado en el README |
| H-13 | Los ciclos N1 guardan su rotación exploratoria (`rotacion`), y la cobertura tiene filas ROTACION y EXPLORATORIA_F3 (la que queda en F3 como CANDIDATA) |
| H-14 | No hay fila ANALISTA para lo que está en el top-3 ni para las vigentes, y la muestra de descartes no incluye nada del top-3 |
| H-15 | `elegidas` sale de los candidatos del top-3, también las vigentes arrastradas, con su símbolo y su precio |
| H-16 | Con GC1 por código, el embudo del paquete (`cribadas`, `pasan_gc1`) y las decisiones GC1 de F5 son las del código (`gc1_decisiones`) |
| H-17 | Con GC1 por código, una finalista cuyo indicador no estaba en el universo enviado al Analista se descarta (PS3) |
| H-18 | Un `presupuesto_override` de `V6_GLOBAL` se respeta tal cual. Una prueba vigila el cierre PARCIAL con la bolsa vacía |
| H-19 | `senal_por_perfil` solo admite tipos de activo conocidos y señales del Motor (`SENALES_GC1`); `gc1: null` no rompe |
| H-20 | Sin precios al vencer, el contrafactual espera como mucho `v6.cobertura.dias_max_espera_precio` días y después se cierra como NO_RESOLUBLE. Cada tipo lleva su estado (RESUELTO, SIN_DATOS o SIN_MUESTRA) |
| H-21 | `pruebas.md` cita la prueba de CA-8 con su nombre. Los literales que quedaban (régimen, evidencias del Contradictor, motivo de la contrarréplica y longitud de una limitación) salen de la configuración |
| H-22 | Regresiones para N06 (reintento del Contradictor fuera de la caché), N13 (fila de la vigente cerrada), N18 (tope de preguntas) y N22 (presupuesto del mensaje CT-15) |
