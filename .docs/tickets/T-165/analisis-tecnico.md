# T-165 · Análisis técnico

## Causa raíz o motivo

El catálogo de G3 (prompt del Orquestador técnico V5.0, §6.2) define G3-MET-13 «Madurez declarada» (clase B): «Método citado sin
`estado_madurez` o presentado como validado cuando RC lo registra como documentado o implementado». PB-47 la usa para que «nada se
presente como validado sin estarlo» (R22). La referencia de HT-09 (`bloque_a/10_Herramientas/ht09_validador_g3.py`, C01–C19,
corpus congelado) no la implementa, y el ejecutor tampoco: `sintesis.ht09_validar` solo añadía a la referencia la selección
unitaria (C15) y el método explícito de R13 (C07). Así, un informe de clase que llama «validado» a un método en DOCUMENTADO
pasaba G3 APTO y llegaba al técnico y al JSON.

Al probar la comprobación apareció una segunda causa, del propio ejecutor: el rótulo del técnico «N efectivo ML-CLUS-001: …»
(`redaccion.py`) y la limitación de «sin historia» (`orquestacion.py`) citan ML-CLUS-001 aunque el Motor lo haya rechazado. Con
ML-CLUS-001 en DOCUMENTADO, esa cita es justo lo que G3-MET-13 tiene que bloquear; sin corregirla, ningún ciclo con el método en
DOCUMENTADO podría entregarse nunca (y la prueba de T-159 de PB-47 caería).

## Evidencia

- HEAD (`189ee55`), sonda de la QA de T-159: `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s
  ../../.docs/tickets/T-159/revisores/r01_02_sondas.py -k pb47` → «dictámenes G3: ['APTO', 'APTO'] · entregables con «validado»:
  ['informe_tecnico', 'paquete_json']» y falla.
- Con T-165: «dictámenes G3: ['BLOQUEADO', 'APTO_CON_ADVERTENCIAS', 'APTO_CON_ADVERTENCIAS'] · entregables con «validado»: []» y
  pasa. El primer G3V- de F6 queda BLOQUEADO con G3-MET-13 (««validado» para ML-CLUS-001, «DOCUMENTADO» en el Catálogo: «Los
  clústeres…»»), el CT-14 llega al Orquestador, las seis opciones de RV y RF (todas lo afirmaban) se retiran y el segundo G3V-
  queda con la advertencia de los informes de clase que ya no llegan a la entrega.
- Lo que el texto del ejecutor cita de los métodos en un ciclo normal (sondeo de 2 ciclos con los 12 tipos): el técnico nombra
  ST-DESC-001 (valoración, lo escribe el Analista), RISK-DD-001 (riesgo sintético) y ML-CLUS-001 (N efectivo); el JSON, ST-DESC-001.
  Ninguna palabra de madurez aparece en ningún entregable del ciclo simulado («arrastre verificado» es la única palabra parecida).
- Los prompts de los Analistas declaran la madurez en `estado_madurez_metodos` con frases como «DER-OPT-001 documentado;
  VOL-GARCH-001 implementado», «FON-DISC-001: documentado, no validado» o «FX-PPA-001, FX-COINT-001: implementados, validación
  pendiente»: las pruebas las usan como casos que no deben saltar.

## Implementación

- **Archivos cambiados y por qué.**
  - `bloque_a/11_Ejecutor/bloque_a/herramientas/ht09.py`: sigue reexportando la referencia; añade `comprobar_madurez` (función pura:
    textos con ruta y severidad, la madurez del Catálogo, la función «se sirve» y el índice de fichas → una comprobación con el
    formato de HT-09), `textos_de` (aplana un JSON con rutas; el OPP- va en la ruta de cada elemento con `opp_id`; un campo
    `…madurez…` se lee con sus hermanos de método), `texto_html` y `nivel_catalogo`. Se quitan tres avisos de ruff que ya tenía
    (dos `noqa` sin uso y el orden de imports, con `noqa: I001` porque `DIR_REFERENCIA` tiene que ir antes).
  - `bloque_a/11_Ejecutor/bloque_a/sintesis.py`: `ht09_validar` suma `g3_met13` (paquete de síntesis, informe visual e informes
    de clase de `extras["seleccion"]` y `extras["analisis"]`) y recalcula dictamen, motivo y resumen con `_recalcular` (la regla de
    la referencia; antes solo se recalculaba con bloqueos). `g3_met13_tecnico` comprueba el técnico ya escrito y suma sus
    incidencias a la misma comprobación. `extras["clusteres_calc_id"]` dice si el Motor sirvió los clústeres.
  - `bloque_a/11_Ejecutor/bloque_a/redaccion.py`: tras escribir el técnico, `g3_met13_tecnico`; si bloquea, `G3-MET-13` entra en
    los bloqueos de F7 (la entrega va a `_bloqueados`, como con `COHERENCIA_ENTREGABLES`). `_rotulo_n_efectivo`: «N efectivo
    ML-CLUS-001» solo si hubo cálculo; si no, «N efectivo sin clústeres del Motor, cada serie cuenta aparte».
  - `bloque_a/11_Ejecutor/bloque_a/orquestacion.py` (lo justo, una expresión): la limitación de «sin historia» dice «el resto
    tampoco se agrupa (ML-CLUS-001 rechazado)» cuando el Motor lo rechazó.
  - `bloque_a/11_Ejecutor/tests/test_t165_g3_met13.py` (47 pruebas), `tests/mapa_plan_pruebas.json` (PB-47 → AUTOMATICA),
    `docs/evidencias_pruebas_bloque_a.md` (regenerado), `docs/incidencias.md` (INC-T165-01; nota «aplicada» en INC-T159-01),
    `bloque_a/11_Ejecutor/README.md` (§10).
- **Decisión tomada (no propuesta):** `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` §1, fila «G3-MET-13» (Agente, por delegación del operador, 16-11-2026): G3-MET-13 se queda como comprobación complementaria del ejecutor y el HT-09 de referencia del corpus no se toca. El registro de decisiones no lo toca este ticket.
- **Decisiones tomadas `[PROPUESTO]`** (detalle en INC-T165-01): id `G3-MET-13` y no C20; madurez y servicio desde el Motor; las
  reglas A (sobredeclaración) y B (ficha no servida sin declarar); una ficha servida citada sin madurez no salta (la primera mitad
  literal de G3-MET-13 exigiría cambiar el esquema del JSON, corpus); infradeclarar no salta; lectura frase a frase con atribución
  a la ficha más cercana o a todas en plural, negación con auxiliares de lista cerrada, «validado por» una persona o un dato
  (lista cerrada) no es madurez; los informes de clase de candidatas que no
  llegan a la entrega dan advertencia; fallo localizado en una opción → F6 la retira (no está entre los sistémicos de §6.3).
- **Desviaciones del plan:** ninguna de alcance. Las etiquetas HTML de formato en línea (`<b>`, `<span>`…) no cortan la frase: lo
  encontró una prueba del ticket (`test_texto_html_separa_frases_por_etiquetas`) antes de cerrar.
  Y la excepción «validado por el operador» dentro de una frase con ficha: la medí con frases de redacción realista («umbral validado
  por el operador», «tesis validada por el dato de empleo») y bloqueaban; ahora no, con la lista cerrada de INC-T165-01.
- **Límites conocidos.**
  - Es lectura de texto libre por patrones (lección `claude/2026-11-12_filtros-por-patron-en-texto-libre`): medida con las frases
    de los prompts, el ciclo simulado y un backtest de 13 ciclos, no con la redacción de un modelo real. Con dos fichas en una frase
    y la palabra en singular, solo cuenta para la más cercana: «ML-CLUS-001 y ST-DESC-001 implementado» no atribuye «implementado» a
    ML-CLUS-001, pero si este no se sirve la regla B lo bloquea igual (no está declarado); y «validado» bloquea a cualquiera porque
    ninguna ficha está VALIDADO. Una frase que el corte separa mal (abreviaturas con punto y espacio) puede perder la atribución.
  - El rótulo «(RISK-DD-001)» del riesgo sintético se escribe aunque RISK-DD-001 no se sirva: si dejara de servirse, G3-MET-13
    bloquearía la entrega (falla cerrado).
  - El informe de seguimiento C6 no se comprueba (lo escribe el ejecutor sin modelo).
  - En F7 no hay retirada: un bloqueo del visual o del técnico bloquea toda la entrega.
- **Comandos exactos para probarlo** (desde `bloque_a/11_Ejecutor`, con el Python del `.venv`; el ejecutable `bloque-a` del `.venv`
  enlazado importa el paquete de otra copia, así que el backtest se lanza con `python -m bloque_a.cli` desde esta carpeta):

```bash
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t165_g3_met13.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py -k pb47
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t159_extremo_a_extremo.py tests/test_fase4_mapa.py
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m bloque_a.cli --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv \
  --salida /tmp/salida_mock backtest --desde 2024-01-05 --hasta 2024-03-29
```
