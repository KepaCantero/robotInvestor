# T-197 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-24 · de claude (implementador) a QA (segunda ronda de cierre de la QA r02)

- **Hecho:** tres pruebas para H-09 y H-10 (el código no cambia); M66 a M68 en `mutantes.py` (los C1 a C3 del revisor).
- **Commit:** «T-197 cierre 2: …», encima de `1cd14ec4`, sin push. Sin gate completo.

## 2026-11-24 · de claude (implementador) a QA (ronda de cierre de la QA r02)

- **Hecho:** H-07 y H-08 corregidos con su prueba y sus mutantes (tabla «Ronda de cierre» de `analisis-tecnico.md`); la desviación de H-02 de la r02 queda deshecha.
- **Cuidado con:** `revisores/r01_01_ataques.py::test_a9` falla ahora en su última aserción (`"estado_run" not in f5`), la que la QA r02 sustituye por B3. El resto de r01_01 pasa.
- **Commit:** «T-197 cierre: …», encima de `2512a133`, sin push. Sin gate completo (lo pasa la integración, por indicación de la coordinación).

## 2026-11-24 · de claude (implementador, r02) a QA (r02)

- **Fase en la que se entrega:** QA (r02), después del NO APTO de la r01.
- **Hecho:** los seis hallazgos están corregidos, cada uno con su prueba (tabla «Ronda r02» de `analisis-tecnico.md`). Los ataques del revisor dan 35/35; sus mutantes, 16 muertos de 17 (R4, equivalente); `mutantes.py`, 58 muertos de 58.
- **Cuidado con:**
  - H-02: el cierre de un disparo huérfano va en `cierre_huerfano.estado_run` (FALLIDO), no en `estado_run`, porque A9 exige que la reserva siga sin `estado_run` después del sondeo. Con el proceso vivo la salida es EN_CURSO: la prueba de hilos espera ahora 1 EMITIDO y 3 EN_CURSO mientras el ciclo corre. A4 (procesos que terminan en milisegundos) sigue dando 3 DESCARTADO_DUPLICADO; si un proceso llegara mientras otro sigue en el ciclo, vería EN_CURSO, que es lo que pide H-02.
  - H-01: `semana_ancla_quincenal` va en todos los CFG- de P-01 (None si no es quincenal), para que la vista consolidada de F10 no arrastre la de un CFG- anterior.
- **Commit:** «T-197 r02: …», encima de `47a4316`, sin push.

## 2026-11-24 · de claude (implementador) a QA (otro agente)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - El CT-04 escribe el P-01 completo: «QUINCENAL · LUN 07:00 · entrega MIE 08:00» (la ejecución, 49 h antes de la entrega, la deduce HT-05). Lee también el P-01 de dos partes anterior a T-197 y rechaza con motivo lo que HT-05 no puede programar.
  - HT-05 tiene el calendario del C1 por periodicidad y `planificacion_c1.py` lo usa con el P-01 de F10 y su fecha de efecto: `bloque-a planificar` dice el siguiente C1 y, con `--ejecutar`, dispara una sola vez el C1 vencido (reserva DISPARO en F5 en una transacción; EMITIDO, RECUPERADO o PERDIDO; FALLIDO si el ciclo se corta).
  - 18 pruebas en `tests/test_t197_periodicidad.py`; 32 mutantes en `mutantes.py`, todos muertos; gate 12/12; PB-09 «Superada» en el mapa y en las evidencias.
- **Falta:** la QA. Commit local en `wip/t197`, sin push.
- **Cuidado con:**
  - Las decisiones `[PROPUESTO]` de INC-T197-01: el formato del P-01, el adelanto de la quincenal y la mensual, el redondeo hacia abajo, el ancla de la quincenal, solo el último disparo pendiente cuenta, los duplicados no se escriben en F5 y un ciclo cortado no se repite solo.
  - T-189 (Astra) cambia la parte de horizontes del mismo `decision`: aquí solo cambia la parte P-01 y la línea del valor. `git merge-tree` con `origin/astra/encargos-bloque-a-c38-c47`: el código se fusiona sin conflictos; `docs/incidencias.md` choca porque las dos ramas añaden al final (ver `pruebas.md`).
  - Las pruebas sustituyen `orquestacion.Reloj` para que el F10 inicial nazca el día de la instalación (29-05-2026): sin eso, F10 lleva la fecha real del sistema.
- **Scripts útiles:** `.docs/scripts/evidencias_plan_a.py --pb PB-09`; `.docs/tickets/T-197/mutantes.py`.
