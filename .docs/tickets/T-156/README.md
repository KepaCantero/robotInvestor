# T-156 · Bloque A: rango de `cobro_posible_desde` y una prueba de F9 por lista

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (ejecutor): `bloque_a/llm.py` (`ReglaReintentos.de_config`), `tests/test_t154.py`, `config/por_defecto.yaml` (comentario), `docs/incidencias.md` (INC-T146-01) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; las decisiones nuevas van como `[PROPUESTO]` |
| Deuda técnica | T-156 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los dos hallazgos bajos de la QA r01 de T-154 (`.docs/tickets/T-154/qa.md`).

## Alcance

- **Entra:**
  - **H-01.** `llm.reintentos.cobro_posible_desde` no tenía rango. Con 600 o más, un 501, un 520 o un 500 con `x-should-retry: false` volvían a soltarse como no cobrados, así que la cuenta fallaba abierta.
  - **H-02.** La prueba de la entrada `PRESUPUESTO_F9` anotaba los cierres, los recortes y los excesos a la vez, y no veía que `TramoPresupuesto.algo()` olvidara uno (mutantes R01 a R03 del revisor).
- **No entra:** las observaciones de la QA:
  - H-03 cobra de más a propósito y está declarado.
  - `retry-after-ms` tiene prioridad sobre `retry-after`, como en el SDK.
  - Si `agentes.invocar` lanza tras una petición cobrable, el grupo no se marca. No se reprodujo en un ciclo.

## Diseño

- **Cómo falla cerrado.**
  - `ReglaReintentos.de_config` rechaza un `cobro_posible_desde` que no sea un entero entre 100 y 500. Los dos límites son del protocolo HTTP (RFC 9110, §15), no parámetros de ajuste, y van en las constantes `ESTADO_HTTP_MIN` y `PRIMER_ESTADO_5XX` de `llm.py`.
  - El tope es 500 y no 599: con cualquier valor admitido, la cuenta es igual de prudente que con 500 o más prudente.
- **Pruebas** (`tests/test_t154.py`).
  - `test_t156_h01_cobro_posible_desde_con_rango`: valores dentro, fuera, de otro tipo y booleanos.
  - `test_t156_h02_cada_lista_sola_basta_para_escribir_f9`: una incidencia sola de cada lista escribe F9 con ella y con las otras listas vacías.
- **Estado persistido:** no cambia.

## Criterios de aceptación

1. Un `cobro_posible_desde` fuera de 100…500, booleano o que no sea entero se rechaza con un error que lo nombra. El valor por defecto, 500, sigue valiendo.
2. Cada una de las tres listas, sola, basta para escribir `PRESUPUESTO_F9`. Los mutantes R01 a R03 de `.docs/tickets/T-154/revisores/r01_03_mutantes_qa.py` mueren.
3. Las pruebas de T-154, T-151, T-146 y T-148, los goldens, ruff ≤ 2831 y mypy de A ≤ 109, en verde.
