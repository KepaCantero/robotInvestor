# T-187 · Traspaso

## 2026-11-18 · de claude a revisores independientes (paso 3) y al otro agente (QA)

- **Fase en la que se entrega:** probar (pasos 1 y 2 hechos; paso 3 preparado).
- **Hecho:** script, pruebas, mutantes, informe y muestra; INC-T187-01; fila T-187 de la deuda.
- **Falta:**
  1. **Contraste del paso 3.** Revisores que no hayan escrito los prompts rellenan `veredicto` (CORRECTA, ERRONEA, NO_VERIFICABLE), `nota` (con la fuente consultada) y `revisor` de cada afirmación de `muestra_afirmaciones.json`. Criterio de PB-51: ≥ 95 % correctas (denominador propuesto en INC-T187-01). No regenerar la muestra después de empezar: `--comprobar` dice si el corpus o el script cambiaron.
  2. **QA** del script y de los criterios (`analisis-tecnico.md`), por el otro agente.
  3. **Operador (T-57):** topes de tamaño de los 21 papeles sin orientación y los criterios `[PROPUESTO]` de INC-T187-01.
- **Commit:** local en la copia de trabajo, sin push («wip local: T-187»).
- **Cuidado con:** los recuentos son heurísticos y están documentados como tales; el Anexo G sí está en el Documento 0 V5.3 (en mayúsculas). El script importa del ejecutor los nombres de agente y la aproximación de tokens: si cambian, cambian el informe y la prueba de regresión.
- **Scripts útiles:** `revision_prompts_pb51.py --comprobar`, `mutantes_pb51.py`.

## 2026-11-18 · de claude al otro agente (QA r01)

- **Fase en la que se entrega:** QA (los tres pasos hechos; estado del README «EN QA (r01)»).
- **Hecho en esta entrega:** contraste del paso 3 con los veredictos de cuatro revisores independientes (`veredictos/lote_1.json` a `lote_4.json`, más `veredictos/comentario.json`): lectura y validación en `revision_prompts_pb51.py` (falla cerrado con 2), recuentos por lote, por prompt y totales con los dos denominadores, sección del paso 3 en `informe_pb51.md`; 17 pruebas y 22 mutantes nuevos (63 muertos); INC-T187-02 (denominador: las verificables) e INC-T187-03 (las 9 erratas, para la próxima entrega del corpus); `bloque_a/11_Ejecutor/tests/test_t187_pb51.py` y PB-51 «Superada» en el mapa y en las evidencias.
- **Resultado:** 260 CORRECTA, 9 ERRONEA, 81 NO_VERIFICABLE; 96,7 % sobre las 269 verificables (pasa) y 74,3 % sobre las 350. Las dos discutibles no cambian el veredicto (97,4 % en los dos supuestos).
- **Para la QA:** comprobar los recuentos desde los lotes con un script propio; que `comentario.json` sea fiel a las notas de los revisores (el script solo comprueba que casa con los veredictos); el criterio del denominador y que el «resultado esperado» del plan («ninguna errónea») no se cumple al pie de la letra (INC-T187-02); que `test_t187_pb51.py` del ejecutor dependa de un script de `.docs/tickets/` es una decisión discutible (alternativa: ampliar `evidencias_plan_a.py` para filas documentales con evidencia).
- **Falta del operador:** los criterios `[PROPUESTO]` de INC-T187-01 y 02, los topes de tamaño de T-57 y autorizar la corrección de las erratas en la próxima entrega del corpus (INC-T187-03).
- **Commit:** local en la rama `wip/t187`, sin push («wip local: T-187 paso 3»).

## 2026-11-18 · de claude al otro agente (QA r02)

- **Fase en la que se entrega:** QA r02 (estado del README «EN QA (r02: QA r01 NO APTO)»).
- **Hecho:** H-01 a H-07 de `qa.md`, cada uno con su prueba de regresión (detalle en `pruebas.md`, «Ronda r02», y en `analisis-tecnico.md`, «Ronda r02»). PB-51 queda «Superada en parte». El script, sus pruebas y sus mutantes están ahora en `.docs/scripts/` (`revision_prompts_pb51.py`, `pruebas_revision_prompts_pb51.py`, `mutantes_revision_prompts_pb51.py`); los datos siguen en el ticket.
- **Dónde me aparto de `qa.md`** (explicado en `analisis-tecnico.md`): la cita de los dudosos va en `dudosas_cita_nota` y no dentro de cada dudosa, porque `r01_04` lee `dudosas` como texto; la sensibilidad se queda en la clave `sensibilidad`, atribuida a quien escribe el comentario, y `discutibles` queda vacía; las cifras por fuente son las de la clasificación del script (249 de memoria, 3 web y 8 de cálculo, frente a 251 y 5 de `qa.md`); `r01_03` se ejecuta con una copia que solo cambia la ruta del script.
- **Commit:** local en `wip/t187`, sin push («wip local: T-187 r02»).

## 2026-11-18 · de claude al otro agente (ronda de cierre de la QA r02)

- **Hecho:** H-08 (las rutas viejas salen de `tools/refs_allowlist.txt` y la cita del diario queda marcada) y H-09 (`MIN_PALABRAS_CITA = 3` `[PROPUESTO]` y la columna «Cita de la nota» en el informe), con sus pruebas y los mutantes M79 a M81. Detalle en `analisis-tecnico.md` y `pruebas.md` («Ronda de cierre de la QA r02»).
- **Commit:** local en `wip/t187`, sin push («wip local: T-187 cierre r02»).
