# T-94 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `.docs/scripts/pruebas_banco_medida.py` | — (nueva) | 10 de 10 en verde (`.venv/bin/python -m pytest -q .docs/scripts/pruebas_banco_medida.py`, unos 21 s) |
| Suites de los bloques y del marco | Sin cambios | Sin cambios: el banco no toca ningún bloque ni el marco (CA-8) |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_integracion_bloque_a`: deja `prerregistro.json`, `informe.json` e `informe.md` |
| CA-2 | `test_exceso_frente_a_la_cesta`: exceso exacto con precios a mano, en LARGO y en CORTO |
| CA-3 | `test_momento_sin_datos_futuros`: alterar precios posteriores al corte no cambia la selección |
| CA-4 | `test_informe_reproducible` y la doble ejecución de `test_integracion_bloque_a`: informes idénticos byte a byte |
| CA-5 | `test_veredictos`: rango que cruza el cero → «todavía no se sabe»; positivo → «mejor»; negativo → «peor» |
| CA-6 | `test_sin_precio_final_queda_sin_resolver`: queda sin resolver y no entra en la media |
| CA-7 | `test_integracion_bloque_a` e `test_informe_reproducible`: la primera línea es el aviso |
| CA-8 | `test_integracion_bloque_a`: `git status` de `bloque_a`, `bloque_b` y el marco común igual antes y después |

Fallo cerrado adicional: `test_simbolo_ausente_detiene` y `test_cargar_precios_falla_si_falta` (el banco se detiene con motivo); `test_neutral_no_se_puntua`.

## Ejecución de ejemplo

`.venv/bin/python .docs/scripts/banco_medida.py a --desde 2024-01-05 --hasta 2026-04-24 --salida <carpeta>` (cliente simulado y datos sintéticos; 3 min 47 s):

| Contendiente | Selecciones | Exceso medio frente a la cesta | Rango del 90 % | Acierto |
| --- | --- | --- | --- | --- |
| titular (A) | 361 | −0,02 % | −0,28 % a +0,25 % | 54 % |
| azar | 361 | −0,08 % | −0,38 % a +0,22 % | 52 % |
| momento | 361 | +0,29 % | +0,00 % a +0,58 % | 59 % |

Titular frente a azar: +0,06 % («todavía no se sabe»); frente a momento: −0,32 % («todavía no se sabe»). Coste del titular: 615 llamadas, 1.289.817 tokens de entrada y 297.510 de salida (3.573 de entrada por selección resuelta).

**Esto no mide a A:** con el cliente simulado, las señales salen de reglas sintéticas, y los precios son de ejemplo. El informe lo dice en su primera línea. Sirve para comprobar la tubería; la medida real llegará con datos de K (T-86) y el cliente real.

## Lint

`ruff check` sobre los dos scripts: sin hallazgos. El gate del repositorio no cubre `.docs/scripts/` (sus cuotas son de los ejecutores); el commit pasa por `commit_limpio.sh`.

## Gate

Se ejecuta en el commit con `.docs/scripts/commit_limpio.sh` (gate completo en una copia limpia).
