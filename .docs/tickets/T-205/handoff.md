# T-205 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-25 · de claude (implementador) a QA (ronda de cierre de la QA r01)

- **Fase en la que se entrega:** ronda de cierre de la QA r01 (APTO pendiente de cierre).
- **Hecho:** H-01, H-02 y H-03 corregidos sin tocar `seguimiento.py` (detalle en `analisis-tecnico.md`, «Ronda de cierre»). Tres pruebas nuevas en `tests/test_t205_clase_seguimiento.py`, que ahora tiene 28. Q1, Q2 y Q11 pasan a `mutantes.py`: 25 de 25 muertos. La prueba de `b_agente` de T-201 se llama ahora `test_b_agente_da_el_analista_de_su_clase_o_falla`. INC-T201-01 dice «Lo corrige T-205 (INC-T205-01)».
- **Cuidado con:**
  - `revisores/r01_mutantes.py` sigue citando el nombre antiguo de la prueba de T-201 en `PRUEBAS`. Sin cambiarlo, pytest no encuentra esa prueba y todos los mutantes «mueren» sin que se ejecute nada. Lo ejecuté con una copia temporal que solo cambia ese nombre: 11 de 11 muertos. No toqué el script del revisor.
  - Q11 (deduplicación fuera de la transacción) murió en la r01 del revisor, pero en mi primera pasada de esta ronda quedó vivo. La prueba de seis procesos solo lo mata si la carrera llega a darse. Añadí `test_c6_la_lectura_de_ha_y_el_inc_van_en_la_misma_transaccion`: otra instancia del almacén intenta el mismo C6 justo después de la lectura de HA, y así lo mata siempre.
- **Commit:** «T-205 cierre: …», encima de `41fcc0bf`, sin push.

## 2026-11-25 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - `b_agente` falla con `ClaseNoAdmitida` si la clase no es uno de los doce tipos.
  - El alta y el C6 se rechazan antes de escribir nada y dejan un INC- OTRO («clase», sin el valor).
  - En el C6, la opción se salta y F11 no avanza. Hay una sola incidencia por (`seg_id`, `f3_seq_clase`, `ciclos_encargo`), y el resto del ciclo da lo mismo que en un gemelo sin la opción estropeada.
  - 25 pruebas nuevas en `tests/test_t205_clase_seguimiento.py` y la de `b_agente` de T-201 actualizada. Mutantes en `mutantes.py`.
- **Falta:** la QA. Commit local, sin push.
- **Commit:** el «wip local: T-205» de la rama `wip/t205`, encima de `origin/develop` 358576c3 (ver `pruebas.md`).
- **Cuidado con:**
  - Las decisiones `[PROPUESTO]` de INC-T205-01: tipo OTRO, deduplicación por la entrada de F3 y no por el valor, el fin del respaldo de F11 en el C6, la comprobación antes de la absorción en C1, y el límite de las fichas que solo llevan `tipo_activo`.
  - La prueba de T-201 `test_b_agente_da_el_analista_de_su_clase_o_falla` cambia de expectativa para None, «XYZ» y `""` (decisión 1 del coordinador). En la ronda de cierre se renombró (antes `test_b_agente_conserva_el_analista_por_defecto`; H-03 de la QA r01).
  - No hay caso del plan de pruebas: ni el mapa ni las evidencias cambian.
- **Scripts útiles:** `.docs/tickets/T-205/mutantes.py`; `.docs/tickets/T-201/revisores/r06_b_agente.py` (reproducción del defecto).
