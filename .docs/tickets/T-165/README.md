# T-165 · Bloque A: comprobación G3-MET-13 de PB-47 (madurez declarada)

| Campo | Valor |
| --- | --- |
| Estado | EN QA (pendiente de un revisor nuevo sin contexto) |
| Pieza | bloque_a (ejecutor: validación G3 complementaria de HT-09) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (regla del 12-11-2026, `compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: completa una comprobación que el diseño ya define (G3-MET-13, clase B, en §6.2 del prompt del Orquestador técnico) y solo endurece G3. No toca el corpus, los contratos CT, los esquemas ni el Documento 0. Lo que el diseño no dice se decide por defecto (`compartida/2026-11-13_decide-el-agente-por-defecto`) y queda `[PROPUESTO]` en INC-T165-01. Dónde vive está decidido: `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` §1, fila «G3-MET-13» (Agente, por delegación del operador, 16-11-2026): G3-MET-13 se queda como comprobación complementaria del ejecutor y el HT-09 de referencia del corpus no se toca |
| Deuda técnica | T-165 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la lleva la sesión coordinadora; este ticket no la toca) |

## Objetivo

Que G3 bloquee una entrega que presenta un método con una madurez que el Catálogo no le da (PB-47: «validado» para un método en
DOCUMENTADO), o que nombra por su ficha un método que el Motor no sirve sin declararlo. Hoy pasa APTO y llega al entregable
(QA r01 de T-159, H-01; INC-T159-01).

## Qué dice el diseño

- **R22** (Documento 0, §1): «Todo componente declara si está documentado, implementado o validado. Presentar como validado lo que
  no lo está es un hallazgo».
- **G3-MET-13** (prompt del Orquestador técnico V5.0, §6.2, grupo G3-MET): «Madurez declarada · Método citado sin `estado_madurez`
  o presentado como validado cuando RC lo registra como documentado o implementado · **B**». No está entre los fallos sistémicos
  de la tabla de dictamen (§6.3): un fallo localizado en una opción la bloquea a ella («APTO para el resto si el Analizador la
  aísla y HT-09 pasa»).
- **PB-47**: método de MC-09 en DOCUMENTADO; informe de clase que lo describe como «validado»; HT-09 (G3-MET-13) → BLOQUEADO hasta
  corregir la declaración; criterio: el entregable final declara «documentado» o no usa el método.
- **La madurez la da el Motor** con la tabla del índice del Catálogo (`servicio.madurez_catalogo`, §4) y `servicio.servible`
  (código + IMPLEMENTADO o VALIDADO en el Catálogo); AUD-REX-001 es CT-10 (`servicio.SERVICIOS_CT10`).
- **Los informes de clase** declaran la madurez en `estado_madurez_metodos` («DER-OPT-001 documentado; VOL-GARCH-001
  implementado», «FON-DISC-001: documentado, no validado»; prompts de los Analistas, §esquema de salida).
- HT-09 de referencia (`10_Herramientas/ht09_validador_g3.py`, C01–C19) no tiene G3-MET-13, y es corpus congelado.

## Alcance

- Entra:
  - Función pura nueva `comprobar_madurez` en el envoltorio `bloque_a/11_Ejecutor/bloque_a/herramientas/ht09.py` (la referencia
    se sigue reexportando igual): recibe textos con su ruta, la madurez del Catálogo y la función «se sirve», y devuelve una
    comprobación con el formato de HT-09 (`id`, `nombre`, `resultado`, `incidencias` con `severidad`, `ruta`, `detalle`).
  - `bloque_a/11_Ejecutor/bloque_a/sintesis.py` (`ht09_validar`): añade la comprobación `G3-MET-13` sobre el paquete de síntesis
    (superconjunto del JSON), el informe visual si lo hay y los informes de clase del run; recalcula el dictamen como ya hace con
    C07.
  - `bloque_a/11_Ejecutor/bloque_a/redaccion.py` (`generar`): el informe técnico se escribe después de HT-09; se comprueba
    también y sus incidencias se suman a la misma comprobación (como `coherencia`). El rótulo «N efectivo ML-CLUS-001» solo cita
    la ficha si el Motor la sirvió.
  - `bloque_a/11_Ejecutor/bloque_a/orquestacion.py`, solo lo justo: la limitación de «sin historia» dice «con ML-CLUS-001» solo si
    el Motor lo sirvió (hoy lo dice también cuando lo rechaza).
  - Pruebas nuevas `bloque_a/11_Ejecutor/tests/test_t165_g3_met13.py`; `tests/mapa_plan_pruebas.json` (PB-47);
    `docs/evidencias_pruebas_bloque_a.md` regenerado; `docs/incidencias.md` (INC-T165-01 y nota en INC-T159-01);
    `bloque_a/11_Ejecutor/README.md`. El registro de decisiones no se toca: la fila «G3-MET-13» del §1 la mantiene la sesión coordinadora.
- No entra: el corpus (HT-09 de referencia, su copia en `herramientas/referencia/` y sus pruebas), el Documento 0, los goldens,
  `contratos.py`, `guias.py`, `evaluador.py`, `motor/`, `herramientas/verificador_ids.py`, otros bloques; el informe de
  seguimiento C6 (`validar_seguimiento`: lo escribe el ejecutor sin modelo); el rótulo «(RISK-DD-001)» del riesgo sintético
  (si RISK-DD-001 no se sirviera, la comprobación bloquearía: falla cerrado, límite declarado).

## Diseño

- **Menciones de método.** Un identificador con la forma de ficha del Catálogo (`[A-Z]+(-[A-Z][A-Z0-9]*)+-\d{3}`, el mismo que
  la tabla §4 con los segmentos intermedios empezando por letra) que esté en `FICHAS_CATALOGO`, en la tabla del Catálogo o tenga
  el prefijo de una de sus fichas (una ficha inventada, «ML-SUPER-001», cuenta: falla cerrado). `CALC-…`, `OPP-…`, `G3-MET-13`
  y los años no lo son.
- **Palabras de madurez.** validado/a/os/as, implementado/a/os/as, documentado/a/os/as (y validated, implemented, documented),
  con límites de palabra: `METODO_NO_IMPLEMENTADO` no cuenta como palabra. Precedida de una negación («no», «sin», «nunca»,
  «aún no», con hasta tres auxiliares de una lista cerrada: «no está validado», «no ha sido implementado») no es una afirmación
  de esa madurez.
- **Frase a frase.** El texto se parte en frases por `. `, `;`, `!`, `?`, saltos de línea, celdas de tabla `|` y etiquetas HTML
  (no por `:` ni `,`: «FX-PPA-001, FX-COINT-001: implementados» es una sola declaración). Una palabra de madurez se atribuye a la
  mención de ficha más cercana de su frase; en plural, a todas las de la frase. Sin ficha en la frase, no se atribuye a ningún
  método («validado por el operador» no salta).
- **Campos estructurados.** En un diccionario con una clave que contiene `madurez` (p. ej. `estado_madurez_metodo`), su valor se
  lee junto con los campos hermanos `metodo`, `method_id`, `ficha`, `operacion` y `metodos`, como una sola frase.
- **Regla A (sobredeclaración, B).** Una madurez afirmada por encima de la del Catálogo (orden DOCUMENTADO < IMPLEMENTADO <
  VALIDADO; una ficha sin fila en el Catálogo no tiene ninguna): «validado» de cualquier ficha que el Catálogo no da por VALIDADO
  (hoy ninguna), «implementado» de una en DOCUMENTADO, «documentado» de una que no existe.
- **Regla B (método nombrado que no se sirve, B).** Una mención de una ficha que el Motor no sirve (`servible`, o CT-10 con
  madurez citable para AUD-REX-001) necesita en su frase una declaración de que no se usa: «documentado», «rechazado/a/os/as»,
  «no implementado», «no servido», «no se sirve(n)» o los códigos `METODO_NO_IMPLEMENTADO` / `OPERACION_SIN_FICHA`. Si no, bloquea.
  Es la lectura del «método citado sin `estado_madurez`» que se puede comprobar hoy (el JSON no tiene ese campo).
- **Una ficha servida citada sin madurez** no salta `[PROPUESTO]`: su madurez es la del Catálogo, que el Motor publica, y
  exigir el campo en el JSON cambiaría su esquema (corpus), que no se toca (decisión del §1 del registro de decisiones).
- **Infradeclarar no salta** («documentado» de una ficha IMPLEMENTADO): R22 persigue presentar como más maduro lo que no lo es.
- **Qué se lee y dónde se localiza.**
  - Paquete de síntesis (todo el JSON y los `x_` del técnico): una incidencia dentro de `clases.X.opciones[i]` o de
    `paquete_para_bloque_B[i]` lleva el OPP- en la ruta, así que F6 retira esa opción y revalida (como C08 en PB-30); fuera de una
    opción (régimen, limitaciones…) bloquea el run.
  - Informes de clase (`extras["seleccion"][c]["candidatos"]`, lo que dijo el Analista de cada candidata): si la candidata es
    una opción del paquete, la incidencia lleva su OPP- (BLOQUEO localizado); si no llega a la entrega (no seleccionada o ya
    retirada), ADVERTENCIA: es un hallazgo R22, pero no se presenta al Broker `[PROPUESTO]`.
  - Informe visual (F7) e informe técnico (F7, después de escribirlo): BLOQUEO; en F7 no hay retirada, el entregable va a
    `_bloqueados`.
- **Formato.** Una comprobación más en `comprobaciones` con `id` «G3-MET-13» (el del catálogo de G3; no un C20 que podría chocar
  con una versión futura de la referencia) `[PROPUESTO]`, nombre «Madurez declarada de los métodos (R22)», y `datos` con las
  fichas citadas. El dictamen y el `motivo` se recalculan como con C07.
- **Números.** Ninguno nuevo: la madurez sale del Catálogo vía el Motor; los «hasta tres auxiliares» de la negación son una regla
  de lectura del texto, no un umbral del sistema.
- **Falla cerrado.** Sin Catálogo legible, ninguna ficha se sirve: toda mención no declarada bloquea. Si la comprobación lanza una
  excepción, se propaga (como cualquier fallo de HT-09: no hay APTO por defecto).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Falsos positivos en texto libre (lección `claude/2026-11-12_filtros-por-patron-en-texto-libre`) | Una opción retirada o un run bloqueado sin motivo | Frase a frase; solo con una ficha en la frase; negación; pruebas con frases que no deben saltar y el ciclo simulado normal (12 tipos, dos semanas) en APTO |
| Texto que genera el propio código y nombra una ficha no servida | Bloqueo permanente cuando el Catálogo baja una ficha | Corregidos el rótulo de ML-CLUS-001 y la limitación «sin historia»; RISK-DD-001 queda como límite (bloquearía) |
| Cambiar el dictamen de ciclos que hoy pasan | Pruebas vecinas en rojo | Suite completa de A; las vecinas de HT-09 y G3; goldens |

## Criterios de aceptación (binarios)

1. CA-1: con ML-CLUS-001 en DOCUMENTADO y un informe de clase que lo llama «validado» (la sonda de T-159), el primer G3V- de F6 es
   BLOQUEADO con G3-MET-13 y ningún entregable dice «validado».
2. CA-2: con ML-CLUS-001 en DOCUMENTADO y sin la siembra, el ciclo entrega (G3 APTO o APTO_CON_ADVERTENCIAS sin G3-MET-13) y la
   prueba de T-159 de PB-47 sigue pasando sin cambios.
3. CA-3: el ciclo simulado normal (12 tipos) da G3 APTO en F6 y F7, con G3-MET-13 OK.
4. CA-4: `comprobar_madurez` bloquea «validado» de una ficha IMPLEMENTADO, «implementado» de una DOCUMENTADO, una ficha inventada
   y una ficha no servida sin declarar; no salta con «validado por el operador», «documentado, no validado», «no implementado»,
   una ficha servida sin madurez, ni con `METODO_NO_IMPLEMENTADO`.
5. CA-5: el formato de la comprobación es el de HT-09 y el dictamen se recalcula (BLOQUEADO con su `motivo`).
6. CA-6: el informe técnico se comprueba en F7 y su bloqueo lleva la entrega a `_bloqueados`.
7. CA-7: PB-47 en el mapa como AUTOMATICA y «Superada» en las evidencias regeneradas.
8. CA-8: suite de A ≥ 607 y sin fallos; goldens; gates ligeros; ruff ≤ 2821; mypy A ≤ 109.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Unitarias de `comprobar_madurez` (positivos y frases que no deben saltar) | nominal, límite, fallo cerrado | CA-4, CA-5 |
| `ht09_validar` con una opción que dice «validado»: BLOQUEO localizado con su OPP- | contrato | CA-5 |
| PB-47 de extremo a extremo (siembra del Analista simulado) | integración, regresión (falla sin la corrección) | CA-1 |
| Ciclo con ML-CLUS-001 en DOCUMENTADO sin siembra | integración, regresión del rótulo | CA-2 |
| Técnico con un método no servido (solo en el técnico) | integración | CA-6 |
| Ciclo normal en APTO con G3-MET-13 OK | integración (falsos positivos) | CA-3 |
| Sonda `r01_02_sondas.py -k pb47` de la QA de T-159 | regresión | CA-1 |
| Suite completa de A, goldens, gates, cuotas, evidencias | regresión | CA-7, CA-8 |

## Scripts

`.docs/scripts/nuevo_ticket.sh`, `.docs/scripts/evidencias_plan_a.py --ejecutar`, `tests/goldens_ct.py`.

## Registro

- 2026-11-16 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-16 · PLANIFICADO · claude · plan y criterios
- 2026-11-16 · EN CURSO · claude · implementación (`ht09.py`, `sintesis.py`, `redaccion.py`, una expresión de `orquestacion.py`) y pruebas
- 2026-11-16 · EN QA · claude · `analisis-tecnico.md` y `pruebas.md`; commit local «wip local: T-165»
