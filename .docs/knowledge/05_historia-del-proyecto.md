# 05 · Historia del proyecto (del 3 al 11 de noviembre de 2026)

Todo lo hecho hasta el 11-11-2026, en orden, para que un chat nuevo o un compañero entienda de dónde viene cada cosa sin el historial de las conversaciones. El estado actual y lo pendiente están en el relevo más reciente (`.docs/tickets/_relevo/2026-11-11_relevo_nuevo_chat.md`). El detalle de cada paso está en su ticket (`.docs/tickets/T-NN/`), en su fila de la deuda técnica (`sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`), en el diario (`.docs/diario/`) o en `git log`.

## 1. El punto de partida (3-11-2026)

- El repositorio nace como monorepo con tres entregas anteriores, cada una con su propio corpus de documentos (gobernanza, prompts, catálogo, esquemas, pruebas y ejecutor):
  - **Bloque A V5.1**: buscador de oportunidades, doce tipos de activo, unos 25 agentes;
  - **Bloque A Forex V1.1**;
  - **Bloque B V2.1**: selección de activos por mercado, unos 24 agentes con un Director.
- El corpus se congela por huella (gate `corpus-integridad`) y se renormalizan a NFC los nombres de 191 ficheros que venían en NFD de macOS.
- Se trasladan los gates de calidad de robotTrading: `./tools/check_all.sh`, 12/12, con cuotas de ruff y mypy que solo pueden bajar y líneas base de pruebas.
- Se preparan los prompts por fases (`prompts/`) y un kit para un dashboard multiagente (`dashboard/prompts/`), que nunca se construyó y quedó superado por el rediseño.

## 2. La Constitución y el marco común de C (5 a 8-11-2026)

**Constitución global** (`sistema_global/constitucion/Constitucion_Global.md`): V0.1 y V0.3 el 5-11; cada versión trae su tabla «Qué cambia» en el §0.

**Marco común de C** (`sistema_global/marco_comun_c/`): el código de referencia de la Fase 1, en Python, todo en simulado. Cada versión lleva su Documento 0 en `sistema_global/documentos_0/` y sus baterías de pruebas.

| Versiones | Fecha | Qué se construyó |
| --- | --- | --- |
| V0.1 a V0.12 | 5-11 | Sobre CT-G-02 y encargo CT-G-01; K con sello de corte y calendario; Orquestador; Contradictor CT-G-03; consola N mínima; F (control de riesgo); G (ejecución con conciliación); H (vigilancia y cierre); E (dimensionado); D (comparador); prueba de extremo a extremo |
| V0.13 a V0.27 | 5-11 | Pasada de coherencia con la Constitución; niveles de autonomía; registro manual CT-G-14; propuesta ligada al sobre; D con referencia y abstención; orden de entrada viva; aprobación con importe tecleado y kill-switch; cartera real y euros; reducción parcial; vía de acceso; candidatos apartados; degradación por cartera; reapertura vigilada; contratos como esquemas; envoltura común |
| V0.28 a V0.36 | 5 y 6-11 | Deuda técnica: sobres más estrictos (T-27); Contradictor exigido (T-48); señales de H (T-49); controles sobre el operador (T-50); encargo con el mandato de SC-1 (T-51); Motor SC-3 y procedencia, licencia y calendario de K (T-26, T-42); confianza y costes en D (T-17); controles de F (T-22) |
| V0.37 a V0.41 | 6-11 | Hechas por GLM, otro modelo, con directrices de Claude (kit 1). Integradas en la V0.53 |
| V0.42 a V0.52 | 6 y 7-11 | Persistencia (T-03): estado guardado, diario de operaciones, jornada con reinicios, firma con clave, migraciones entre versiones, reloj del sistema y rotación de la clave. Nivel L3 y cambio de nivel por el operador (T-18). Reducción ajustada al lote (T-43) |
| V0.53 | 8-11 | Integración de las piezas de GLM |

Cada pieza pasó por una revisión independiente antes de cerrarse. Lo que quedaba abierto se apuntó en la deuda técnica, con su fase de destino.

## 3. Las enmiendas de la Constitución (7 a 9-11-2026)

- **Enmienda 1 → V0.4** (7-11, T-55):
  - A Forex y B Forex quedan fuera del Robot Investor (D-20); la Fase 1 se hace en divisas con los A y B generales;
  - radar tecnológico, small caps, startups y spin-offs, seguimiento de grandes inversores;
  - números ratificados (D-27). Las respuestas del operador sobre intermediario, presupuesto, capital y avisos están en T-56.
- **Decisiones aplazadas** (8-11, T-57): las decisiones técnicas y de perfil del operador se aplazan a una sesión única al completar la arquitectura. Mientras, se trabaja con valores por defecto `[PROPUESTO]` en simulado.
- **Reglas de diseño del operador** (8-11): A y B analizan todo tipo de activo; todo bloque es núcleo más perfiles; se diseña con el operador antes de construir; al dinero solo se llega por F y G.
- **Enmienda 2 → V0.5** (9-11, T-58, 27 puntos):
  - proyecciones y rentabilidad mínima exigida, y vigía de régimen;
  - Motor de cálculo compartido y parámetros con asesor de configuración;
  - análisis independientes con peso por historial, probabilidades verificables y torneo;
  - aprendizaje automático en J, escalera de verificación e incentivos de los agentes;
  - entrada por cualquier bloque, enchufabilidad (estado por bloque, adaptadores, manifiesto y registro de bloques) y J como laboratorio.
  Tuvo una revisión independiente con 19 hallazgos corregidos. Quedó toda ratificada (D-28 a D-43); los valores numéricos P-25 a P-35 siguen aplazados.
- **Enmienda 3 → V0.6** (9-11, T-59): cuestionario guiado para las decisiones, valores por defecto válidos para cualquier usuario, cambios a través del Broker y **una copia por usuario con su propio dinero** (D-47). De ahí que el repositorio no tenga nada personal.

## 4. La forma de trabajar entre agentes (9-11-2026)

- Entra **Astra** (OpenAI) como segundo agente, con las mismas reglas (`AGENTS.md`).
- Se fija el flujo planificar → implementar → probar → QA, con una skill por fase (`.agents/skills/`, enlazada como `.claude/skills`) y QA cruzada: la hace el agente que no implementó.
- Se crea la **memoria indexada** (`.docs/memoria/`) y, a propuesta de un compañero del operador, el espacio **`.docs/`** (T-60): tickets T-NN, diario mensual, scripts sobre `common.sh` (secretos solo en `.env`) y documentos de incorporación.
- El 10-11 se añade un flujo de GitHub Actions al repositorio.

## 5. El Bloque B (9 a 11-11-2026)

- **Astra** adapta B en ramas propias, y Claude hace la QA y las fusiona:
  - T-61: integración en el flujo, ficheros de precios vacíos y comparación con el azar;
  - T-62: objeciones por eslabón;
  - T-63: cita verificable obligatoria para cerrar una objeción fuerte;
  - T-64: fechas de las fuentes al cerrar objeciones.
  La línea base de B sube de 141 a 174 pruebas.
- **T-90** (10-11): una nota con fuentes posteriores al corte se excluye y se declara. B pasa a 176 pruebas.
- **T-68, evaluación de precisión frente a consumo** (11-11, `.docs/tickets/T-68/evaluacion_claude.md`):
  - un análisis N2 simulado lee unos 990.000 tokens en 27 a 29 llamadas, el 96 % releyendo prompts de sistema, y el Director se lleva cerca de la mitad;
  - mejoras propuestas: banco de medida, prompts por módulos y caché solo en lo que se repite.
- Desde el 11-11, **B está congelado** hasta cerrar su arquitectura; el rediseño propuesto pasa de 24 agentes a 5 papeles de IA, sin Director.

## 6. El Bloque A (9 a 11-11-2026)

- **T-53** (9-11): revisión con el operador. Se corrigen 19 defectos verificados (continuidad, datos inválidos, entregables bloqueados, pausas…). QA r01 NO APTO y r02 APTO. Quedan 21 propuestas, PA-01 a PA-21.
- **T-66** (10-11): se aplican las propuestas aceptadas:
  - solo el perfil de divisas activo por defecto (PA-01);
  - Contradictor con contrarréplica y veredicto por regla (PA-05);
  - muestra efectiva para certificar;
  - aprendizaje que solo endurece.
  Tras tres NO APTO, la QA r04 dio APTO y el bloque se dio por terminado en revisión. Lo aplazado está en T-67, con PA-06 y PA-07, que retoma el rediseño.
- **T-65** (10-11): hallazgos bajos de T-53 y resto técnico, en cinco rondas de QA hasta el APTO. A queda en 326 pruebas; los bajos restantes pasan a T-91.
- **T-92** (11-11): la auditoría de Astra al Bloque A, hecha en su rama, se integra tras cuatro rondas. A pasa a **439 pruebas**; los pendientes van a T-93.
- **Consumo medido** (11-11, `.docs/scripts/medir_consumo_a.py`): un ciclo simulado con los doce perfiles hace 77 llamadas y lee 1,66 M tokens; solo con divisas, 8 llamadas y 184.000 tokens. El rediseño propuesto pasa de 25 agentes a 6 papeles de IA, con un primer filtro por código.

## 7. El marco común de C, segunda parte (10-11-2026)

| Versión | Ticket | Qué |
| --- | --- | --- |
| V0.60 a V0.66 → V0.67 | T-79 | Kit 2 de GLM integrado con QA de Claude: panel de la consola, semana simulada, robustez de la persistencia, pasada de coherencia de 185 filas y pruebas doradas. Su deuda se renumeró T-69 a T-78 para no chocar |
| V0.68 | T-80 | Vía de entrada DIRECTA y modo CONSULTA (D-28). Cinco rondas de QA hasta el APTO |
| V0.69 | T-72, T-85 | Estado público del diario y reloj a prueba de NaN |
| V0.70 | T-75 | Embudo visible y alarma de sequía. **Detenido** tras la QA r02 NO APTO |
| V0.71 | T-76 | Cartera sombra pasiva desde el primer día. **Detenido** tras la QA r02 NO APTO |
| V0.72 | T-83 | Valores por defecto documentados como datos, con su justificación (D-45). Ronda r02 sin QA |
| V0.73 | T-75, T-76 | Rondas r02, reabiertas por el operador. Es la versión actual: 61 baterías |

En paralelo, la revisión independiente de la V0.63 (T-84) dio NO APTO; sus correcciones c1 esperan QA. El 10-11, el operador pidió que Astra trabajara hasta que todo pasara su QA, y se le dejó un relevo con el orden y las reglas (`.docs/tickets/_relevo/2026-11-10_pendientes_para_astra.md`).

## 8. El diseño de toda la arquitectura (11-11-2026)

El operador decidió discutir la arquitectura completa antes de construir más. Claude propuso cada pieza con el mismo patrón:
- el código conduce y la IA conversa, con pocos papeles de IA;
- la brújula es batir a la cartera sombra pasiva, en neto y por euro;
- cada cambio se adopta solo si gana en el banco de medida, como aspirante frente al titular;
- las cifras van con rango («todavía no se sabe» si el rango incluye el cero);
- ante la duda, falla cerrado.

Son **22 propuestas**, cada una con un documento para el operador, una copia en `.docs/diseno/` y un encargo de revisión para Astra: D, E, F, G, H, el rediseño de A y B, C, la enmienda 4, I, J, K, M, N, Broker Personal, SC-9 (fiscalidad), SC-3 (Motor de cálculo), SC-10 (intermediario), SC-7 (seguridad), la entrada del dinero existente, la pasada de coherencia y la enmienda 5, parte 1. Lo esencial de cada una está en la fila de `.docs/diseno/README.md` y en el diario del 11-11.

- La **pasada de coherencia** halló doce incoherencias, propuso servicios pequeños, fases, dieciséis contratos nuevos y cinco tandas de decisiones.
- El operador **aceptó la tanda 1** con sus valores por defecto (`.docs/diseno/decisiones_operador.md`).
- Con eso se adelantó lo que no depende de Astra:
  - el **banco de medida** (T-94);
  - las **plantillas del operador** en blanco (`.docs/plantillas_operador/`);
  - el **borrador de la enmienda 5, parte 1**;
  - el **prototipo navegable de la consola N** (T-95, `dashboard/consola_n/`), con el stack web que propuso el equipo del operador.
- Al final del día se escribió el relevo para chats nuevos y esta historia.

## 9. Lecciones que se han repetido

- **Medir antes de recortar:** B y A gastaban casi todo en releer instrucciones. El banco de medida existe para que ningún recorte se adopte por intuición.
- **Al integrar trabajo de otro agente o modelo**, renumerar su deuda contra la del repositorio: chocó con GLM (T-60 a T-69) y con Astra (su T-87).
- **Las QA encuentran cosas:** casi todo lo importante necesitó dos o más rondas. Un revisor nuevo, sin contexto, en cada ronda funciona mejor.
- **Los ZIP de otras entregas** traen permisos 755 y nombres NFD; hay que normalizarlos.
- **Un filtro de secretos** debe reconocer la forma del texto, no la de la clave (T-92).
- **Las cifras con cliente simulado y datos sintéticos** solo prueban la tubería; los informes lo dicen en su primera línea.

## 10. Documentos fuera del repositorio

El operador tiene en Claude documentos de trabajo privados: las 22 propuestas, la evaluación de B, «Cómo decide el Robot Investor y cómo lo entrenaríamos», los Documentos 0 de cada versión del marco, las directrices para GLM, las plantillas con sus datos y el prototipo publicado. El repositorio tiene una copia de todo lo que no es personal; si hace falta un documento privado, el operador da el enlace.
