# T-91 · Análisis técnico

## Causa

- **H-26:** PS2 al emitir contaba las sesiones con `_sesiones_entre` y `ps2_festivos` (en `orquestacion.py`). La resolución usaba `dias_habiles_entre` de HT-05, sin festivos. Con un cierre de dos días (Navidad en Xetra, Pascua), un H1 válido acababa NO_RESOLUBLE.
- **H-27:** cada serie se medía hasta su último dato. Con una serie parada dentro de la tolerancia, el suceso comparaba ventanas distintas.
- **H-28:** el texto que se congela en cada PRG era el anterior a T-65.
- **H-29:** faltaban pruebas para tres partes de la corrección de H-24.

## Implementación

- `calendario.py` (nuevo): `validar_festivos_ps2`, `_sesiones_entre` y sus constantes, movidos desde `orquestacion.py`, que los reexporta (las pruebas los importan de allí).
- `evaluador.py`:
  - `_edad_ps2` mide la antigüedad como PS2 (H1 en sesiones sin festivos; el resto, en días naturales); la usan `motivo_no_fresca` y `bases_cesta`;
  - en `rentabilidad`, la CESTA vuelve a medir sus miembros hasta el más antiguo si acaban en fechas distintas;
  - en `resolver`, un RELATIVO cuyas series acaban en fechas distintas mide las dos hasta la más antigua, con la misma base congelada. La CESTA sin bases en F4 (registros antiguos) se calcula una vez con el horizonte, para que la segunda medida use los mismos miembros.
- `sintesis.py`: `CRITERIO_RESOLUCION` y `REGLA_FALLBACK`, el texto que se congela en cada PRG y en los hitos H5.
- `backtest.py`: `fecha_dato_proxy` y `fecha_dato_referencia` en `pronosticos.csv`.
- README del ejecutor: la regla de resolución en `pronosticos.csv`, y que `fecha_publicacion` no sirve para revisiones (H-25 de T-65).
- Cuotas: ruff de los archivos tocados, con sus correcciones seguras (2986 → 2962 en el total); mypy de A, 109.

## Límites

- Si al medir hasta la fecha común una serie no tiene dato entre la emisión y esa fecha (un hueco justo ahí), el pronóstico espera y, pasado el plazo, queda NO_RESOLUBLE. Falla cerrado.
- `fecha_dato` sigue siendo la más reciente de las fechas usadas; tras alinear, coincide con la fecha común salvo huecos.
- El plazo de NO_RESOLUBLE sigue en días hábiles sin festivos (`dias_habiles_entre`), como antes.

## Comandos

```bash
.venv/bin/pytest -q bloque_a/11_Ejecutor/tests/test_t91_resolucion.py
```

## Ronda r02 (QA r01 NO APTO)

- **H-01 (alta):** al medir hasta la fecha común, una serie con un hueco justo antes se medía con un dato más viejo que PS2. Ahora `rentabilidad` tiene `hasta`: mide hasta esa fecha, pero la frescura se comprueba frente a la fecha de resolución, también en cada miembro de la CESTA. Si no pasa, el pronóstico espera (`r01_01_resolucion_ataques.py H`: 4 de 4).
- **H-02 (baja):** pruebas con un hueco de un día en la fecha común, que distinguen `fecha_dato` (la más reciente de las usadas) de la del proxy, y la fecha de la CESTA (la más antigua). Mueren N1, N2 y N9 de `r01_02_mutantes.py`.
- **H-03 (baja):** el ejemplo `ejemplos/salida_backtest_simulado/pronosticos.csv` gana las dos columnas, vacías porque se generó antes, y su LEEME lo dice; el comentario de `evaluacion` en `config/por_defecto.yaml` cita INC-T91-01.
- **H-04 (baja, anterior a T-91):** un PRG con `nivel_referencia` como número suelto ya no lanza `TypeError` en la comprobación de fuga: su base es la última sesión ≤ la emisión.

## Ronda r03 (QA r02 NO APTO)

- **H-05:** en `resolver` (proxy y referencia) y en la CESTA (sus miembros), la medida hasta la fecha común se repite hasta que todas las series acaban en la misma fecha. Cada vuelta baja la fecha común, porque la serie que tiene la fecha común la conserva y la que tiene un hueco queda antes. El bucle acaba: o coinciden, o una serie deja de ser fresca frente a la fecha de resolución y el pronóstico espera. Por seguridad, si una vuelta no baja la fecha común, se lanza `DatosNoDisponibles` (espera). Con los cuatro casos del revisor (`r02_03_desalineacion.py`: hueco de un día, Ascensión, fin de año y CESTA con huecos), todas las series acaban en la misma fecha.
- **H-06 (mutantes de `r02_02_mutantes.py`):**
  - mueren Q1, Q4, Q5, Q6, Q9 y Q12; las pruebas nuevas son `test_r03_*`;
  - Q8 ya no se aplica (el `if` es ahora un `while`), y la prueba `test_r03_q5_q8_…` caza su equivalente;
  - son equivalentes con la alineación repetida:
    - Q2 y Q3 (una serie se vuelve a medir sin horizonte): las dos acaban en la misma fecha, así que la frescura de una cubre la de la otra;
    - Q7 (la CESTA sin horizonte): la cubre la frescura del proxy en la misma fecha;
    - Q10 y Q11 (`fecha_dato` del proxy, o la más reciente de la CESTA): todas las fechas coinciden.
- **Límite:** `fecha_dato` es la fecha común. La regla de INC-T91-01, el criterio congelado, el README y la configuración se pusieron al día en el cierre (H-07 de la QA r03): «todas se miden hasta la fecha más reciente en la que todas tienen cierre»; si no la hay, el pronóstico espera.
