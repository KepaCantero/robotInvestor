# T-177 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-18 · cierre 3 · de claude al revisor (tercera ronda de cierre de la QA r03)

- **Fase en la que se entrega:** QA (verificación de H-19).
- **Hecho:**
  - M08 restituido en `mutantes_t177.py`, como en `5f98163`.
  - `test_t177_cierre3_h19_urgencia_sin_contenido_se_reduce_a_normal` (`" "`, `[""]`, `{"": ""}`): da SOLICITADA y la urgencia queda NORMAL en la CRD- y en el CT-25.
  - El código no cambia.
- **Commit:** local, «wip local: T-177 cierre 3» (sin push, sin rebase).
- **Cuidado con:** la segunda ronda de cierre decía, en `pruebas.md` y en su traspaso, que M08 era equivalente. Era un error y ya está corregido.

## 2026-11-18 · cierre 2 · de claude al revisor (segunda ronda de cierre de la QA r03)

- **Fase en la que se entrega:** QA (verificación de H-18).
- **Hecho:**
  - H-18, con la corrección exacta de `qa.md`, en `contratos._subarbol_sensible`: `CAMPOS_SOLICITUD_LITERALES` y `URGENCIAS`.
  - Los tres `test_r03c_HALLAZGO_H18_*` invertidos.
  - Pruebas en `test_t177`: `test_t177_cierre2_h18_*`.
  - Mutantes nuevos M42 a M44.
- **Commit:** local, «wip local: T-177 cierre 2» (sin push).
- **Cuidado con:**
  - `test_t177_urgencia_y_denegada_no_se_vuelve_a_pedir` cambia: antes `MUY_ALTA` se reducía a NORMAL y ahora rechaza el retorno.
  - La prueba de H-17 que combinaba `impacto` con `impacto_si_falta` deja de llevar `impacto`.
  - (Corregido en la tercera ronda de cierre: M08 no era equivalente, H-19.)

## 2026-11-18 · cierre · de claude al revisor de la ronda de cierre de la QA r03

- **Fase en la que se entrega:** QA (ronda de cierre de la QA r03, que fue APTO con cuatro bajos).
- **Hecho:**
  - H-14 a H-17, con la corrección de `qa.md` y una prueba cada uno (`test_t177_cierre_*`).
  - `r03_ataques_regla_comun.py` con sus HALLAZGO invertidos.
  - `r03_corpus_formatos.py`: 97 ejemplos y 0 bloqueos.
  - 6 mutantes nuevos (M36 a M41).
- **Commit:** local, «wip local: T-177 cierre» (sin push).
- **Cuidado con:**
  - `_publico` solo actúa en las claves ambiguas fuera del subárbol, no en el barrido del retorno entero (lo fija la prueba `lei_en_finalista_con_solicitud` del revisor).
  - `credencial_ref` con texto dentro de una solicitud ahora descarta el retorno (H-17).

## 2026-11-18 · r03 · de claude al revisor de la QA r03

- **Fase en la que se entrega:** QA (r03, tras la QA r02 NO APTO).
- **Hecho:**
  - **Regla común** (`contratos.retorno_con_credencial`, usada por `llm.respuesta_segura`, por la segunda barrera de `agentes` y por `Credenciales.desde_retorno`):
    - solo mira los retornos con `solicitudes_credenciales`, leídos primero como JSON (H-09);
    - dentro del subárbol, una ficha opaca en cualquier clave u hoja, o un número bajo una clave de valor (H-08, H-11);
    - fuera, solo las claves inequívocas, o las de `CAMPOS_VALOR_AMBIGUOS` con ficha opaca (H-12).
  - `contratos.ficha_opaca` (H-10 y H-13).
  - El simulado de los Analistas emite `solicitudes_credenciales: []` e `indicadores[].valor` de texto.
  - La C4 reserva la bolsa bajo la transacción.
  - HALLAZGO_* invertidos en `r01` y `r02`; `r01_ataques_r8.py` y `r02_concurrencia_presupuesto.py` adaptados (ver «Cuidado con»).
  - `r02_falsos_positivos.py`: V5 y V6, `texto` y `sin`, COMPLETO con 0 bloqueos (limitaciones 2 y 3, como en `c9daa4e`).
- **Commit:** local, «wip local: T-177 r03» (sin push).
- **Cuidado con:**
  - **Extensión de la r03:** con alguna solicitud no vacía, el retorno se mira entero por fichas opacas (así caen los casos `en_lagunas` y `sintesis_con_json` del revisor).
  - **Pruebas del revisor adaptadas:** la barrera que exigía dos C4 a la vez dentro de `solicitar` o de `uc_c4_semana` no se puede cumplir con la reserva bajo la transacción.
    - `test_r01_c4_concurrente_dos_bloques` ejerce ahora H-03 en `desde_retorno` y, además, dos C4 a la vez.
    - `test_r02_h07_carrera_del_presupuesto` espera con `sleep` y comprueba COMPLETO más SIN_PRESUPUESTO sin pasar de la bolsa.
  - **Reserva colgada:** si un proceso muere a mitad de la C4, la reserva `EN_CURSO` bloquea la semana (falla cerrado, INC-T177-01).

## 2026-11-17 · r02 · de claude al revisor de la QA r02

- **Fase en la que se entrega:** QA (r02, tras la QA r01 NO APTO).
- **Hecho:**
  - **H-01 y H-04 (altas):** `llm.solicitud_con_valor` en `respuesta_segura`, antes de la caché y de la cinta. Mira el dict entero, compara la clave normalizada (también la de `solicitudes_credenciales`) y falla cerrado si no puede leerlo. `agentes.invocar` la repite como segunda barrera, también al leer la caché.
  - **H-02:** las previas se buscan por `alias_de`. **H-03:** `solicitar` comprueba y escribe dentro de `almacen._transaccion()`.
  - **H-05:** `clave_normalizada` y la lista ampliada; también en la respuesta del Broker (`responder`).
  - **H-06:** `RE_FICHA_OPACA` con `LONGITUD_MIN_VALOR_OPACO`, común con `RE_VALOR_GENERICO`; el retorno se rechaza entero y tampoco llega a la caché. El caso LEI está en INC-T177-01.
  - **H-07:** `SIN_SERVICIOS` sin llamar al BFA; tope semanal real con las C4- de los 7 días (`SIN_PRESUPUESTO`).
  - `revisores/r01_ataques_r8.py` con los HALLAZGO invertidos (y los límites de detección con aserción): 15/15. 30 pruebas nuevas en `test_t177` (43 en total); 25/25 mutantes muertos (13 nuevos).
  - Evidencias de PB-58: «Superada» con su preparación. Deuda: T-179 (pendiente del operador).
- **Commit:** local, «wip local: T-177 r02» (sin push).
- **Cuidado con:**
  - Desviación: `solicitud_con_valor` solo cuenta un campo de valor que lleva texto (un `valor` numérico no bloquea). Backtest mock 2024-01-05 → 2024-02-02 idéntico a develop en `senales.csv`, `pronosticos.csv` y `metricas.json`, sin ninguna incidencia de contenido sensible.
  - Un segmento largo de letras y cifras tras una «/» de una URL en el motivo se rechaza (falla cerrado; documentado).
  - Con el cliente simulado, una C4 cuesta unas 0,18 UC: caben unas siete por semana antes de `SIN_PRESUPUESTO` (la reserva del peor caso de T-146 corta antes de agotar las 3 UC).

## 2026-11-17 · de claude a astra (o un revisor que no implementó)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - Paso 1 de PB-58: mantenimiento C4 de credenciales del BFA (`mantenimiento_c4.py`, orden `credencial c4`). AG-16 recibe solo alias y estado en la bóveda de los servicios de `credenciales.servicios_bfa` y devuelve `solicitudes_credenciales`.
  - Paso 2: `Credenciales.desde_retorno` (AG-01) valida, deduplica por alias, comprueba HT-01 y emite el CT-25 con `solicitar`; la C4- queda en F5.
  - R8: un retorno con un campo de valor en `solicitudes_credenciales` se bloquea en `agentes.invocar` antes de la caché (antes el valor llegaba a `cache_resultados.jsonl`); el Coordinador rechaza además el retorno íntegro con SEGURIDAD en HA.
  - 16 pruebas nuevas, 12/12 mutantes muertos, ciclo de punta a punta por la CLI con el simulado, PB-58 «Superada», INC-T177-01 `[PROPUESTO]`.
- **Falta:** la QA independiente.
- **Commit:** local, «wip local: T-177» (sin push).
- **Cuidado con:**
  - `credenciales.servicios_bfa` está vacía por defecto (decisión del operador); las pruebas y el script la rellenan con un servicio ficticio.
  - El retorno del BFA no pasa por la mensajería (no hay par AG-16 → AG-01 en `CANALES`): es deliberado para no cambiar los goldens (INC-T177-01).
  - El cambio de `agentes.py` solo mira `solicitudes_credenciales`; un campo `valor` en otro retorno sigue siendo corriente.
  - Conflictos posibles con T-176 y T-178 en `mapa_plan_pruebas.json`, `docs/evidencias_pruebas_bloque_a.md`, `docs/incidencias.md`, `MAPA_PLAN_DE_PRUEBAS.md` y la deuda técnica: aquí solo cambian la fila PB-58, una frase de INC-T116-03, INC-T177-01 (antes de INC-T175-01) y la fila T-177.
- **Scripts útiles:**
  - `.docs/tickets/T-177/mutantes_t177.py`
  - `.docs/tickets/T-177/ciclo_mock_t177.sh`
  - `.docs/scripts/evidencias_plan_a.py --pb PB-58`
