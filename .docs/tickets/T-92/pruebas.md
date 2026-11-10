# T-92 · Pruebas

## Ronda r04 (10-11-2026)

- Gate completo 12/12: A 439 (nueva línea base), A-Forex 68 y B 176; ruff baja a 3072 y mypy de A queda en 115.
- `test_t92_revision.py` amplía las pruebas con H-25 a H-30. La QA r03 comprobó que, de las 17 pruebas nuevas de la r03, 15 fallan con el código de la r02 (`6f02e11`) y 2 pasan: la de tiempo, porque la r02 ya era lineal, y la del umbral `None`, que ya daba `KeyError`.
- Sondas: ver el README, «Ronda r04».

## Ronda r03 (10-11-2026)

- Gate completo 12/12: A 420 (nueva línea base), A-Forex 68 y B 176; ruff 3077 y mypy de A 115, en su cuota.
- `test_t92_revision.py` tiene 51 pruebas, entre ellas H-17 a H-23: 2000 claves realistas, entradas adversarias de hasta 140 KB, una clave tras un salto de línea, recuperación con más de un registro, instancia viva, validación previa, Ctrl-C tras el sello, cambios de hora y umbral inválido.
- Sondas de la QA r02 con el código de la r03: `r02_01`, `r02_02` y `r02_03` dan 0 fallos; `r02_04` da 1, explicado en el README.

## Ronda r02 (10-11-2026)

- Gate completo 12/12: A 401 (nueva línea base), A-Forex 68, B 176; ruff 3077 y mypy de A 115, en su cuota.
- `test_t92_revision.py`: 32 pruebas, todas en verde; con el código de la rama de Astra fallan 27 (abajo).
- Sondas de la QA r01 con el código de la r02: `r01_01` da 1 fallo (1c, expectativa superada, ver el README), `r01_02` da 1 (H-11, límite declarado), `r01_03` ya no puede construir su caso (H-08) y `r01_04` da 0.
- `rama_03_falsos_positivos_r8.py`: 0 líneas del corpus operativo tomadas por secreto (eran 6).

## Ronda r01 (10-11-2026, sobre la copia de develop con T-92)

- Gate completo, `.docs/scripts/gate.sh --completo`: 12/12, con el código de la copia en `PYTHONPATH` (el entorno tiene los bloques instalados en modo editable desde la copia principal):
  - A: 386 pruebas (eran 326);
  - A-Forex: 68;
  - B: 176.
- Cuotas que bajan: ruff de 3109 a 3077 y mypy de A de 123 a 115. Línea base de A: 386.
- Las 43 pruebas de Astra (`tests/test_t87_*.py`) pasan sobre develop. Tres se han ajustado a reglas de develop, cada una con su motivo:
  - `test_t87_controles.py::test_sello_legacy_y_disco_sin_espacio_al_confirmar`: un directorio anterior tampoco tiene la marca de formato (H-02);
  - `test_t87_datos.py::test_dos_degradaciones_en_misma_fecha_de_efecto`: la degradación de H5 rige desde el mismo ciclo (T-65, H-13);
  - `test_t87_contratos.py::test_ejemplo_publicado_cumple_el_esquema`: queda solo la parte del ejemplo, porque `preparar-encargo-b` no entra.
- `tests/test_t92_revision.py`: 17 pruebas en la r01 (H-01 a H-05 y la frontera entre D02 y la PS2 de T-65) y 32 en la r02 (más H-06 a H-15 y los literales de respaldo de H-05).
- Dos pruebas de T-65 cambian a propósito por D02: `test_t65_qa_r03.py::test_r03_h16_…` y `test_t65_qa_r04.py::test_r04_h24_…`. Un miembro que deja de publicar después de la emisión ya no se quita de la CESTA: la CESTA no sirve. Se mantiene que nunca entra con 0.

## Que las pruebas nuevas fallan con el código de la rama de Astra

Copiando `test_t92_revision.py` de la r02 a la rama de Astra (`76b90e6`) y ejecutándolo con el código de esa rama, fallan 27 y pasan 5:
- **Pasan** las cuatro de claves reales (R8 ya las detectaba) y la del tope con la configuración cambiada.
- **Fallan** todas las de H-01 a H-15, las de D02 con frescura y la de los literales de respaldo (`test_t65_h05_…`).

En la r01 eran 13 fallos y 4 pasos (el README decía 12 por error).

## Comandos

```bash
W=<copia con T-92>
export PYTHONPATH=$W/bloque_a/11_Ejecutor:$W/bloque_a_forex/11_Ejecutor:$W/bloque_b/11_Ejecutor
cd $W && .docs/scripts/gate.sh --completo
.venv/bin/python -m pytest -q -p no:cacheprovider bloque_a/11_Ejecutor/tests/test_t92_revision.py bloque_a/11_Ejecutor/tests/test_t87_contratos.py
```
