# T-53 · QA independiente

## Ronda r01 · NO APTO (9-11-2026)

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente Claude). Formé opinión con el plan, los hallazgos y el diff antes de leer `analisis-tecnico.md` y `pruebas.md`. · **Ronda:** r01
- **Scripts de ataque:** `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/qa_t53/` (`r01_…` a `r12_…`). Copiados a `revisores/scripts_qa/`. Las salidas de los scripts originales están en `run_old/` y `run_new/` de esa carpeta.
- **Cómo se ejecutan:** con el código actual (`8562d1e`, instalado en modo editable), desde la carpeta de scratch: `/home/claude/repo/.venv/bin/python r0X_….py`. `r04_backtest_largo.sh` y `r08_mutaciones.sh` apuntan al worktree `wt_new`, ya borrado: para repetirlos hay que recrearlo con `git worktree add --detach <scratch>/wt_new 8562d1e`.

### Reproducción desde limpio

- **Suite de A.** Worktree limpio en `8562d1e` y `PYTHONPATH` hacia él: `pytest -q` en `bloque_a/11_Ejecutor` da **103 passed** (82 s).
- **Gate completo** (`./tools/check_all.sh` en el worktree): **12/12**.
  - ruff 3120/3120;
  - mypy A 135, FX 174, B 159;
  - pytest A 103, FX 68, B 141.
  - El `--core` también sale en verde.
- **Copias de HT-03 y HT-09:** `cmp` da idénticas las de `10_Herramientas/` y `11_Ejecutor/bloque_a/herramientas/referencia/`.
- **Scripts de reproducción originales** (`scripts_codigo/`), ejecutados contra `63a376d` y contra `8562d1e`. Ya no reproducen:
  - CA-01, CA-02 (cierre y resolver), CA-03, CA-04, CA-05, CA-06 (caso original), CA-07, CA-08, CA-09, CA-10, CA-11 (copias) y CA-14/PS2.
  - Siguen igual, como declara el análisis: CA-12 (INC-T53-01) y CA-15 (orden de `participantes` y `msg_id`; F1–F4 idénticos).
  - `ca_ece_cero.py` solo evalúa la expresión antigua.
- **Backtest largo (r04):** 65 ciclos semanales, del 2025-03-07 al 2026-05-29, 12 tipos, mock; 1106 s, rc 0.
  - F4: 1915 altas (576 hitos) y 1176 resoluciones.
  - **Ninguna** incidencia R11 ni `PronosticoCongelado`.
  - 65/65 runs ENTREGADA y COMPLETO, sin `_borradores` ni `_bloqueados` residuales.
- **Muestra de mutaciones (r08).** Revertí una corrección cada vez en una copia y ejecuté su prueba.
  - Fallan, como deben: Holm, filtro `es_hito`, ECE = 0, exclusión sin historia, PS1 y F4 con segunda RESOLUCION.
  - **Pasan las 103** al revertir la corrección del semáforo o la del horizonte principal del Analista (ver H-03).
- **Pruebas nuevas contra el código anterior:** `test_t53_seleccion_y_entrega.py` en `63a376d` da 14 fallos y 4 pasan (controles), como dice `pruebas.md`.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · cada defecto corregido tiene una prueba que falla sin la corrección | **no (parcial)** | En la mayoría sí (r08 y la ejecución contra `63a376d`). Pero CS-01 solo tiene una prueba que comprueba que el esquema `FINALISTA` tiene dos claves, y el cambio del semáforo de CS-17 no tiene ninguna. Al revertir cualquiera de los dos en `sintesis.py`, las 103 pasan (H-03) |
| CA-2 · suites en verde, línea base subida y gate 12/12 | sí | 103 / 68 / 141; `cuotas.txt` en `pytest_bloque_a=103`; gate completo 12/12; ruff baja de 3487 a 3120 y mypy no sube |
| CA-3 · cada hallazgo no corregido, con su motivo | sí (con matices) | `analisis-tecnico.md` cubre CA-12, CA-14 (resto), CA-15 y los 28 CS. No menciona las tres «sospechas no confirmadas» de `codigo.md` ni la decisión de CA-11 sobre si el espaciado de hitos bloquea o advierte |
| CA-4 · propuestas priorizadas, con beneficio, coste y riesgo | sí | `propuestas.md` (orden y beneficio) y `revisores/arquitectura.md` (beneficio y «coste y riesgo» de cada PA-xx). Que se presentaran en la conversación no lo puedo verificar |

**Invariantes:**
- Falla cerrado: sí en general; ver H-01, H-02 y H-04.
- Valida antes de mutar: bóveda (r07) y F4 (r06), correctos. F4 solo admite ALTA a AG-10 y RESOLUCION a AG-20, y el índice se reconstruye al recargar el almacén.
- Números escritos a mano: H-08.
- Secretos: ninguno; el gate `secrets` está en verde.
- Determinismo: igual que antes (CA-15, declarado).
- Cuotas: no suben.
- Decisiones del operador sin `[PROPUESTO]`: H-09.

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_sin_historia_variantes.py`, caso (b): un par DIV con datos solo de 2020 a 2021, ciclo a 2026-06-05 | **Esperado** (CA-06, R14, R16): el símbolo se excluye y se declara, y el tipo sigue analizándose. **Obtenido:** las 6 fichas del Motor salen REJECTED y DIV queda con 0 opciones, estado COMPLETO y sin limitación, igual que en el defecto original. La exclusión solo mira si hay algún dato ≤ as_of (`valor_en`). El lote pide datos de [as_of − 3 años − 30 días, as_of], y el `continue` de `senales_clase` sigue descartando la ficha en silencio | Excluir con la condición del lote (algún dato en [ini, as_of]) o pedir las fichas por símbolo. Si una ficha se rechaza, añadir la laguna y dejar el tipo en PARCIAL | abierto |
| H-02 | media | `r03_horizonte_principal.py`, caso (b): el Analista declara `horizonte_principal: H5` (ofrecido) sin `naturaleza_inversion` | **Esperado:** el ejecutor no inventa un dato que haga fallar el control. **Obtenido:** el ejecutor pone la naturaleza por defecto del tipo (CICLICA, de H2 a H4) y C17 bloquea por «H5 fuera del rango de CICLICA», una naturaleza que nadie declaró. RV pasa de 3 opciones a 0 con el run COMPLETO y sin limitación; antes de T-53 se publicaban. Caso (c): un `horizonte_principal` no ofrecido se sustituye en silencio y sin limitación (CS-01 pedía declararlo) | Si falta la naturaleza y hay horizonte declarado: o se propone `naturaleza_para(hp)`, declarada como propuesta del ejecutor, o se bloquea con el motivo «naturaleza ausente». Declarar en `limitaciones` cuando se sustituye el horizonte del Analista | abierto |
| H-03 | media | `r08_mutaciones.sh`: mutaciones `semaforo` (vuelve a `VERDE si n ≥ 2`) y `hp_analista` (`hp_ag = None`) | **Esperado** (CA-1): al revertir la corrección falla una prueba. **Obtenido:** 103 passed en los dos casos. La única prueba de CS-01 (`test_esquema_finalista_admite_horizonte_principal_y_justificacion`) comprueba la implementación (claves del esquema), no la regla de 8.3. El semáforo (prompt AG-02, 6.15.5) no tiene prueba | Añadir pruebas de comportamiento: un ciclo o `construir` que use el horizonte y la justificación del Analista, con C17 bloqueando un caso incoherente y no bloqueando uno coherente (incluido el de H-02); y casos VERDE, ÁMBAR y GRIS del semáforo | abierto |
| H-04 | media | `r11_ps2_festivos.py` | **Esperado** (INC-T53-02: «el dato del viernes vale el lunes», sin relajar): el dato de la última sesión real supera PS2 en H1. **Obtenido:** `np.busday_count` no tiene festivos. Sábado 2026-04-04 con dato del jueves (Viernes Santo) da 2 sesiones y PS2 = False. Sábado 2025-12-27 con dato del 24 da 3 sesiones y False. Antes de T-53, los dos casos daban True. Como PS2 exige todos los horizontes de la opción, la opción entera deja de ser elegible en esas semanas | Contar las sesiones con el calendario de la propia serie (sesiones que tienen el indicador o su tipo entre `fecha_dato` y as_of) o con un calendario de festivos por mercado. Marcar la interpretación como `[PROPUESTO]` (PS2 es de régimen Operador) | abierto |
| H-05 | media | `r05_degradacion_h5_efecto.py`: 20 hitos RV×H5 resueltos con el 25 % cumplidos y dos ciclos | **Esperado** (D0 12.2: «se aplica en F10»): el ciclo siguiente usa «Limitado». **Obtenido:** F10 P-31 RV×H5 = LIMITADO y el AJU dice `aplicado_en_produccion: True`, pero `aplicabilidad(cfg)` sigue en «SI» y el ciclo siguiente ofrece H5 en las 3 opciones. El análisis lo declara pendiente («falta que cambie la tabla»), pero el registro afirma que ya se aplicó, y la prueba solo comprueba F6 y F10 | Que `aplicabilidad` y la tabla de los mensajes CT-06 lean P-31 de F10. Mientras tanto, registrar `aplicado_en_produccion: false` (o no escribir el CFG) y dejar el pendiente en la deuda con su ID | abierto |
| H-06 | baja | `r02_pausa_total.py`: BLOQUEANTE sobre CRI y ciclo con alcance `["CRI"]` | CA-04 queda corregido: no se analiza nada y el run queda PARCIAL con la limitación. Pero el run sigue integrando y redactando con el paquete vacío y acaba con `entrega: BLOQUEADA` por `ESQUEMA_JSON` («clases: {} should be non-empty»). Es un falso error de esquema, y el Broker no recibe la limitación | Si todo queda pausado, cortar antes de F5 y devolver un CT-02 PARCIAL o SIN_RESULTADO con las limitaciones, sin pasar por la redacción | abierto |
| H-07 | baja | `r10_bandas.py` | Las cinco bandas coinciden con el Anexo A y con el `enum` del esquema; los huecos van a la banda más cercana a 50 %. Respecto de la tabla antigua de F4 solo cambia 0,21–0,24 (pasa a POCO_PROBABLE, más prudente), y `PROB_DE_BANDA` no cambia. **Pero** `fijar_bandas` escribe en una variable global del módulo: crear un segundo `Evaluador` con otra `bandas_verbales` cambia `banda_de(0,58)` de INCIERTO a MAS_PROBABLE_QUE_NO en todo el proceso | Guardar la tabla en la instancia (Evaluador o Bloque) y pasarla a `banda_de` y `banda_publicable` | abierto |
| H-08 | baja | Lectura del diff y del prompt del Analizador (l. 443) | `seleccion.siguiente_paso.A_profundizar: 65` se atribuye al prompt 6.16, que no da ningún número (solo «atractiva pero con incertidumbre reducible»): es un umbral inventado. Además, los valores por defecto del YAML se repiten en el código (`_umbrales_presentacion`, `.get("alfa_holm", 0.10)`, `.get("degradacion_h5_tasa_min", 0.50)`…) | Quitar el número o marcarlo `[PROPUESTO]` con su pregunta. Hacer que falte la clave del YAML falle en lugar de usar un literal | abierto |
| H-09 | baja | `docs/incidencias.md`: INC-T53-02, -04 y -05 | Tres «Decisión» tomadas por quien implementó sobre parámetros de régimen Operador (PS2) o del corpus: PS2 en sesiones, «Limitado → No» como tipo 3, y semáforo y siguiente paso. Están documentadas, pero sin `[PROPUESTO]` y sin entrada propia en la deuda técnica | Marcarlas `[PROPUESTO]` y añadirlas a la deuda o a la lista de la reunión con el operador | abierto |
| H-10 | baja | `ca_entregable_bloqueado.py` (nuevo), `r12_datos_invalidos_laguna.py` y lectura de `seguimiento.py` | Restos de declaración: (a) el paquete en memoria conserva `estado_g3 = APTO` o `APTO_CON_ADVERTENCIAS` cuando la entrega se bloquea (`redaccion.py` todavía fuerza `APTO_CON_ADVERTENCIAS`); (b) en backtest, el C6 bloqueado va a `<entregables>/_bloqueados/` y no a `<fecha>/_bloqueados/`, como en la redacción; (c) un CSV con un solo `n.d.` se declara «sin datos HT-01 hasta as_of», sin incidencia en HA | No escribir un `estado_g3` favorable en el objeto bloqueado; unificar la ruta; usar un motivo y una incidencia propios para `DatosInvalidos` | abierto |
| H-11 | baja | `git diff 63a376d 8562d1e -- tools/refs_vivas.py` | El gate `refs-vivas` deja de revisar todas las carpetas `revisores/` de todos los tickets, presentes y futuros. Es una relajación general de un control, y solo hay un comentario en el código | Limitarlo a los informes que citan rutas de scratch, o documentar la excepción en `CLAUDE.md` y en la tabla de gates | abierto |

**Sin hallazgo en lo comprobado:**
- **Rechazo de F4 (r04, r06):** no lo dispara ninguna ruta legítima, ni en el backtest de 65 ciclos con arrastres y resoluciones, ni al recargar el almacén.
- **Bóveda (r07):** el flujo CT-25 completo en backtest con as_of pasado funciona; también la caducidad como `date`. Un índice heredado ilegible pasa a CADUCADA y `listar` no falla. Si `chmod` falla, el archivo anterior queda intacto; el modo final es 0600 y no quedan temporales.
- **Reescritura de AG-17 (r09), en backtest y en vivo:** lo bueno llega a la entrega, el primer intento queda en `_bloqueados` y no queda nada en `_borradores`.
- **Fuga de información en la exclusión:** no la hay, porque se usa `valor_en` con datos hasta as_of.
- **Siguiente paso:** cumple el prompt 6.16; las objeciones usan el campo `estado`, como en el ejemplo del esquema.
- **PS1:** solo la pieza de momentum lleva `origen: AG-13`, así que las piezas del Analista y de AG-14/16 siguen contando. Su dirección en F2 sigue sin depender de la tesis, aunque ya no afecta a PS1.

### Veredicto

**NO APTO** · No hay hallazgos críticos ni altos, pero CA-1 no se cumple: las correcciones de CS-01 y del semáforo de CS-17 no tienen ninguna prueba que falle sin ellas (H-03). Además quedan abiertas correcciones incompletas o con regresión:
- CA-06 sigue reproducible con un símbolo deslistado (H-01);
- el horizonte declarado sin naturaleza vacía un tipo con el run COMPLETO (H-02);
- PS2 en sesiones excluye opciones válidas tras festivos (H-04);
- la degradación de H5 queda registrada como aplicada sin estarlo (H-05).

Hay que corregir de H-01 a H-05 con su prueba de regresión y volver a ejecutar r01, r03, r05, r08 y r11. Los bajos (H-06 a H-11) pueden pasar a la deuda técnica con su ID.


## Correcciones tras la r01 (implementación, Claude)

| ID | Corrección | Prueba que falla sin ella |
| --- | --- | --- |
| H-01 | La exclusión usa la misma ventana que el lote de fichas (`cierres(simbolo, ini, as_of)`); las fichas que el Motor rechace se declaran como laguna y el tipo queda PARCIAL. Además, si ML-CLUS-001 se rechaza (series cortas), ya no se calla: limitación «clústeres de exposición no calculados» y run PARCIAL | `test_h01_simbolo_deslistado_no_vacia_su_tipo`, `test_h01_historia_corta_tambien_queda_declarada` |
| H-02 | Con horizonte principal declarado y sin naturaleza, el ejecutor propone `naturaleza_para(hp)`, no la del tipo; un horizonte no ofrecido se declara en `limitaciones` | `test_h02_h5_declarado_sin_naturaleza_…`, `test_h02_horizonte_no_ofrecido_se_declara_como_limitacion` |
| H-03 | Pruebas de comportamiento: ciclo con el horizonte y la justificación del Analista; semáforo VERDE, ÁMBAR y GRIS (`sintesis._semaforo`, extraída) | `test_h03_se_usan_el_horizonte_y_la_justificacion_del_analista`, `test_h03_semaforo` |
| H-04 | Las sesiones de H1 descuentan los cierres habituales (`ps2_festivos`, `[PROPUESTO]`: Viernes Santo y 1-1, 24-12, 25-12, 26-12, 31-12; INC-T53-02 ampliada). El calendario por mercado queda para el perfil de cada tipo | `test_h04_ps2_h1_descuenta_festivos` |
| H-05 | Al empezar cada ciclo, la tabla de horizontes del ejecutor se recarga desde F10 (`_matriz_aplicabilidad`), así que «aplicado en producción» es cierto | `test_h05_degradacion_h5_cambia_la_tabla_del_ciclo_siguiente` |
| H-06 a H-11 | A la deuda técnica, fila T-65, con su ID | — |

**Comprobación:**
- Las 13 pruebas nuevas, contra `8562d1e` (antes de estas correcciones): fallan 10; las otras 3 pasan porque comprueban comportamiento ya corregido en `8562d1e`.
- `r08b_mutaciones_ronda2.sh` revierte cada corrección de H-01 a H-05 en una copia; las 8 mutaciones hacen fallar su prueba.
- r01, r03, r05 y r11, otra vez:
  - r01: los tres casos dan opciones DIV y run PARCIAL con la laguna;
  - r03: H5 sin naturaleza da ESTRUCTURAL, sin bloqueo C17, y el H1 no ofrecido se declara;
  - r05: el ciclo siguiente ya no ofrece H5 (LIMITADO);
  - r11: los cinco casos dan PS2 = True.

## Ronda r02 · APTO (9-11-2026)

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente Claude). Leí la r01, el diff de `e38b6ca` y el código antes de leer `analisis-tecnico.md` y `pruebas.md`. · **Ronda:** r02
- **Scripts de ataque:** `/tmp/claude-0/-home-claude/d1ab3b3e-4909-5455-a67a-e01975b6ec91/scratchpad/qa_t53_r02/` (`r2_01_…` a `r2_07_…`, con sus salidas `.out` al lado). Copiados a `revisores/scripts_qa/`.
- **Cómo se ejecutan:** se recrea el worktree con `git worktree add --detach <scratch>/qa_t53_r02/wt e38b6ca` (ya está borrado). Después, desde una carpeta de trabajo: `PYTHONPATH=<wt>/bloque_a/11_Ejecutor /home/claude/repo/.venv/bin/python r2_0X_….py`. `r2_07_…sh` admite `SRC=<wt>/bloque_a`.

### Reproducción desde limpio

- **Suite de A.** Worktree limpio en `e38b6ca`, con `PYTHONPATH` hacia su ejecutor (comprobé que `bloque_a.__file__` sale del worktree): `pytest -q` da **116 passed** (90 s).
- **Gate completo** (`./tools/check_all.sh` en el worktree, con `.venv` enlazado y `PYTHONPATH` hacia los tres ejecutores del worktree): **12/12** en 4 min 30 s.
  - ruff 3120/3120;
  - mypy A 135, FX 174, B 159;
  - pytest A 116, FX 68, B 141.
- **Pruebas nuevas contra `8562d1e`.** Las 13 pruebas de la QA r01, copiadas sobre `8562d1e`: fallan 10 y pasan 3, como dice `pruebas.md`.
- **Scripts de la r01, otra vez, contra `e38b6ca`:**
  - **r01:** el símbolo deslistado en 2021 (b) y el que empieza después de as_of (control) se excluyen y se declaran: DIV mantiene 2 opciones y el run queda PARCIAL. Con historia corta (a), DIV conserva 2 opciones y ML-CLUS-001 rechazado deja el run PARCIAL.
  - **r03:**
    - (b) H5 sin naturaleza pasa a ESTRUCTURAL, C17 da OK y salen 3 opciones;
    - (c) H1 no ofrecido: el ejecutor propone H2, coherente con TACTICA, y lo declara en `limitaciones` por cada opción.
  - **r05:** F10 P-31 RV×H5 = LIMITADO y `aplicabilidad(cfg)` también. El ciclo siguiente ya no ofrece H5, así que `aplicado_en_produccion: True` es cierto.
  - **r11:** los cinco casos dan PS2 = True.
- **`r08b_mutaciones_ronda2.sh`** con `SRC=<wt>/bloque_a`: las 8 mutaciones hacen fallar su prueba.
  - Comprobé que fallan por la aserción de la mutación y no por el entorno.
  - Una copia sin mutar pasa las 13.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · cada defecto corregido tiene una prueba que falla sin la corrección | sí (con un hueco bajo) | `r08b`: 8 de 8 mutaciones detectadas, incluidas las del semáforo y el horizonte del Analista, que eran el motivo del NO APTO de la r01 (H-03). 10 de las 13 pruebas fallan en `8562d1e`. Queda sin prueba la rama defensiva que declara las fichas rechazadas por el Motor (H-14) |
| CA-2 · suites en verde, línea base subida y gate 12/12 | sí | 116 / 68 / 141; `cuotas.txt` en `pytest_bloque_a=116`; gate completo 12/12; ruff y mypy sin cambios |
| CA-3 · cada hallazgo no corregido, con su motivo | sí | H-06 a H-11 están en la fila T-65 de `Deuda_tecnica_y_pendientes_del_operador.md`, con su ID y su descripción. Un matiz: T-65 resume H-11 como «excluye `revisores/` en todo `.docs`; debería ser solo en los tickets», pero la r01 decía que se excluyen las carpetas `revisores/` de todos los tickets y pedía limitarlo o documentarlo en `CLAUDE.md` |
| CA-4 · propuestas priorizadas | sí | Sin cambios respecto de la r01 |

**Invariantes:**
- **Números escritos a mano:** el código nuevo no introduce ninguno. `ps2_festivos` está marcado `[PROPUESTO]` en el YAML y en INC-T53-02, con T-57 para fijar la lista. Los literales 70/65 de `_umbrales_presentacion` y la ventana de «3 años + 30 días» ya existían. Esa ventana ahora también decide qué símbolos se excluyen; queda dentro de H-08 (T-65).
- **Falla cerrado:** C17 bloquea una naturaleza y un horizonte incoherentes declarados por el Analista y retira las opciones, declarándolo (r2_02). Con la configuración de festivos ausente, PS2 vuelve al cálculo estricto y no se relaja (r2_03).
- **Determinismo:** la tabla de horizontes vigente depende del historial del proceso (H-12).
- **Secretos:** ninguno; el gate `secrets` está en verde.

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-12 | media | `r2_05_cfg_compartida.py`: dos `Bloque` con el mismo dict de configuración y almacenes distintos. A degrada RV×H5 y B no tiene P-31 en su F10. También `r2_04_degradacion_y_recuperacion.py`, paso 3b | **Esperado:** la aplicabilidad depende solo del F10 de cada instancia y de la fecha as_of; el ciclo no muta la configuración del llamador. **Obtenido:** la corrección de H-05 escribe `self.cfg["_tabla_horizontes"]` en el dict compartido, y `_matriz_aplicabilidad` lo usa de respaldo. B ve RV×H5 = LIMITADO y sus opciones salen sin H5; C, con su propia configuración, ofrece H5 en las 3. El dict del llamador gana la clave `_tabla_horizontes`. Con el mismo almacén y la misma fecha, tras una reversión con `valor_vigente` vacío, la misma instancia da LIMITADO y una instancia nueva da SI. Es latente: la CLI, `ejecutar_backtest` (que usa `fusionar`) y las pruebas crean cada uno su configuración. Pero rompe el determinismo, y heredar una tabla mejorada por un tipo 3 de otra instancia relajaría un control | Guardar la tabla vigente en un atributo de la instancia (o pasarla a `aplicabilidad`). Que `_matriz_aplicabilidad` use de respaldo solo la tabla 8.3 estática (`TABLA_HORIZONTES`). Añadir una prueba con dos instancias que comparten la configuración | abierto |
| H-13 | baja | `r2_04_degradacion_y_recuperacion.py`, paso 1, y su traza `r2_04b_recuperacion_traza.py` | El AJU registra `efecto_desde` = as_of + 1 y el CFG `fecha_efecto` = as_of + 1, y la corrección dice «se aplica en el ciclo siguiente». **Obtenido:** el mismo ciclo que degrada (C5) ya envía LIMITADO al Analista, porque `estado("F10", as_of)` filtra por la fecha de registro y no por `fecha_efecto`. Vuelve a haber un registro que no cuenta lo que pasó, aunque en el sentido prudente | Escribir `fecha_efecto` = as_of y documentar que se aplica en el mismo ciclo, o hacer que la lectura de F10 respete `fecha_efecto` | abierto |
| H-14 | baja | `r2_07_mutacion_fichas_rechazadas.sh`: quita `self._fichas_rechazadas[...].append(ficha)` y ejecuta la suite entera | **Obtenido:** pasan las 116. La aserción `assert not rechazadas or "rechazadas" in lagunas` de `test_h01_historia_corta_tambien_queda_declarada` se cumple sin comprobar nada si no se rechaza ninguna ficha. Ningún caso de `r2_01` (8 variantes de historia parcial) ni de `r2_06` (7 de datos anómalos) llega a esa rama | Prueba que fuerce un RECHAZADO del Motor para una ficha (con `monkeypatch` de `motor.servir`) y compruebe la laguna y el estado PARCIAL | abierto |
| H-15 | baja | `r2_06_fichas_rechazadas.py`, casos «cero» (todos los cierres a 0) y «duplicadas» (una fecha repetida) | **Esperado** (CA-06): el símbolo malo se excluye, se declara y el tipo sigue. **Obtenido:** DIV se queda con 0 opciones y PARCIAL, declarado como «datos de mercado no disponibles». La exclusión de H-01 solo cubre `DatosNoDisponibles`, no los datos inválidos. Con precios negativos (caso «negativo»), el run sale COMPLETO sin ninguna laguna y con avisos de `log` | En `senales_clase`, excluir y declarar el símbolo también ante `DatosInvalidos` o cualquier excepción del proveedor para ese símbolo. Validar en HT-01 que los cierres son > 0. Va con H-10 (c) | abierto |
| H-16 | baja | `r2_01_historia_parcial.py`, casos (e) «hueco y vuelve» y (g) «dos símbolos cortos» | ML-CLUS-001 se calcula sobre los finalistas de todos los tipos. Un solo finalista con poca historia lo rechaza entero: la concentración no se mide en ningún tipo y el run queda PARCIAL. Ya se declara, que es lo que pedía H-01. Pero el respaldo, un clúster por proxy, desactiva el control de concentración para todos | Excluir de ML-CLUS-001 los proxies con historia insuficiente, declararlos y calcular los clústeres con el resto | abierto |
| H-17 | baja | `r2_03_festivos_config.py` | Si `ps2_festivos` falta o está vacía, PS2 vuelve en silencio al cálculo anterior a H-04: no se relaja, pero no avisa. Los tipos no se validan: `viernes_santo: "false"` (texto) activa el Viernes Santo; `fijos: "12-25"` (texto) se ignora; `fijos: 1225` lanza `TypeError` en `_puertas`, y con él cae el ciclo. Aparte, el lunes de Pascua no está en la lista `[PROPUESTO]`: un martes con el dato del jueves da PS2 = False. Eso lo decide el operador en T-57 | Validar `ps2_festivos` al cargar la configuración (booleano y lista de «MM-DD») y fallar con un mensaje claro si falta o está mal. Va con H-08 | abierto |

**Sin hallazgo en lo comprobado:**
- **H-01, historia parcial (r2_01):** ninguno de los 8 casos vacía DIV ni rechaza las fichas del lote. Los casos son:
  - un único dato en la ventana;
  - un símbolo deslistado hace un año;
  - salidas a bolsa de hace 3 y 13 meses;
  - un hueco de 2021 a 2026;
  - un dato antiguo más uno futuro;
  - dos símbolos cortos;
  - un CSV vacío.

  Los dos últimos con exclusión se excluyen y se declaran.
- **H-02 y C17 (r2_02):**
  - TACTICA+H5, VALORACION+H2 y ESTRUCTURAL+H3, declarados por el Analista: C17 bloquea, se retiran las opciones y se declara «Opciones retiradas por bloqueo G3», además del `menos_de_tres_motivo`.
  - Una naturaleza inválida («FOO») la rechaza el esquema `FINALISTA` y el tipo queda PARCIAL, declarado.
  - ESTRUCTURAL sin horizonte pasa a H5.
  - El control CICLICA+H3 da OK.
- **H-04 (r2_03):** con la configuración por defecto se cumplen Viernes Santo, Navidad, el 29 de diciembre con el dato del 24, un dato con fecha de festivo y Año Nuevo. El control da False. Las fechas con hora y zona y el orden invertido no fallan.
- **H-05 (r2_04 y r2_04b):** la recuperación con un CFG de tipo 3 que restituye «SI» funciona: el Analista recibe SI y no se vuelve a degradar en el mismo trimestre. Las opciones vigentes conservan sus horizontes por continuidad (fase REVISION_VIGENTES).

### Veredicto

**APTO.** Los motivos:
- H-01 a H-05 están bien corregidos: los scripts de la r01 (r01, r03, r05 y r11) ya no los reproducen, y las 8 mutaciones de `r08b` se detectan.
- CA-1, el motivo del NO APTO de la r01, se cumple: los defectos corregidos tienen pruebas de comportamiento que fallan sin la corrección.
- La suite da 116, el gate 12/12, y H-06 a H-11 están en la deuda (T-65).
- No hay hallazgos críticos ni altos.

H-12 a H-17 deben pasar a la deuda técnica (fila T-65) con su ID. **Recomiendo corregir H-12 antes de conectar A en la Fase 1.** Es una regresión de la corrección de H-05 que rompe el determinismo cuando varias instancias comparten la configuración. Hoy no le afecta a ningún camino del repo, y arreglarlo son dos líneas y una prueba. Si el operador prefiere no cerrar con una media abierta que introdujo la propia corrección, el veredicto pasaría a NO APTO solo por H-12.

## Correcciones tras la r02 (implementación, Claude)

| ID | Corrección | Prueba |
| --- | --- | --- |
| H-12 | `Bloque` trabaja con una copia propia de la configuración (`copy.deepcopy`), y el Evaluador vuelve a la tabla 8.3 fijada al crearlo (`_tabla_base`), no a la última aplicada en memoria | `test_h12_dos_bloques_con_la_misma_configuracion_no_comparten_la_tabla_de_horizontes`; falla al quitar la copia |
| H-13 a H-17 | A la deuda técnica, fila T-65, con su ID | — |

Con H-12 corregido, el veredicto **APTO** de la r02 queda sin la reserva que hacía el revisor.
