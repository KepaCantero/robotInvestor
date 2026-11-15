# T-94 · Análisis técnico

## Causa raíz o motivo

**Primera versión (11-11-2026).** El banco de medida es el paso 0 de los rediseños de A, B y C: compara al titular con dos referencias baratas (azar y momento) con los mismos datos y fechas de corte, con prerregistro sellado.

**Ronda r02 (15-11-2026, QA r01 NO APTO).** El veredicto del banco afirmaba más de lo que medía. Hay dos causas.
- **H-01.** Contaba como observaciones independientes las filas de `senales.csv`. Pero A repite cada semana la misma oportunidad VIGENTE, con ventanas H3 de seis meses que se solapan. En el ejemplo, 39 filas eran 4 apuestas.
- **H-02.** No había un tamaño mínimo de muestra. Con una sola observación por lado, el remuestreo da un rango de anchura cero y un veredicto firme.

Los demás hallazgos (H-03 a H-12) eran huecos de fallo cerrado, de prerregistro, de coste y de documentación.

## Evidencia

- `.docs/tickets/T-94/qa.md` (QA r01) y los scripts del revisor `revisores/r01_01` a `r01_08`.
- `r01_02_pseudorreplicacion.py` frente a la versión 0.3.0. En un mundo sin habilidad, la tasa de veredictos firmes queda así:

| Escenario | r01 | r02 |
| --- | --- | --- |
| A: elección nueva cada semana, sin solape | ≈ 10 % | 3,0 % |
| B: la misma oportunidad repetida, H3 | 42,5 % | 0,0 % |
| C: una selección por lado | 87 % | 0,0 % |

- Ejecución del README (`--desde 2026-03-06 --hasta 2026-05-29`, cliente simulado):
  - antes: «mejor» frente a las dos referencias, con 24 «resueltas»;
  - ahora: 39 selecciones, de las que 35 son repetidas y 4 resueltas, en 2 fechas efectivas;
  - veredicto: «todavía no se sabe», por pocas observaciones efectivas.

## Implementación

**Archivos:**
- `.docs/scripts/banco_medida.py`, versión 0.3.0;
- `.docs/scripts/pruebas_banco_medida.py`, de 12 a 51 pruebas;
- `.docs/scripts/registro_experimentos.py`, solo dos avisos de ruff: un import sin usar y el orden de los imports;
- `.docs/tickets/T-94/mutantes_r02.py`, 29 mutantes sobre una copia.

**Hallazgo a hallazgo:**

| Hallazgo | Corrección |
| --- | --- |
| H-01 | Una apuesta sobre el mismo activo, la misma clase y la misma dirección, con su ventana aún abierta en la fecha de corte, queda `repetida` y fuera de la media. La regla es la misma para el titular y para las referencias. El rango remuestrea **fechas de corte enteras** (todas las selecciones de una fecha juntas), y el número de fechas distintas es el de observaciones efectivas. El informe publica selecciones, repetidas, resueltas y fechas efectivas. |
| H-02 | Con menos de `--min-efectivas` fechas efectivas por lado (10 por defecto) no hay veredicto: «todavía no se sabe», con el motivo. El 10 es el mínimo de conglomerados que A exige para certificar (`evaluacion.min_conglomerados_bootstrap`). |
| H-03 | Las series se validan en `cargar_precios`, `evaluar` y `momento`: columnas presentes, fechas legibles, sin zona horaria y cierres finitos y positivos. Si algo falla, `BancoError` con el símbolo y la fecha. `rentabilidad` da `None` con un extremo no finito o no positivo. Los JSON se escriben con `allow_nan=False`. |
| H-04 | Sin `--experimento`, el banco reutiliza el experimento ya prerregistrado con la misma hipótesis, objeto y periodo. Otra semilla u otros parámetros son otra variante del mismo experimento, de modo que quedan fuera del máximo de variantes y no son adoptables. Un `--experimento` con otra hipótesis, objeto o periodo se rechaza antes de anotar nada. El informe avisa si hay varios experimentos con la misma hipótesis. La orden `verificar <carpeta>` recalcula la huella de `prerregistro.json`, la compara con la que cita el informe y comprueba el intento y el resultado en el registro (`experimento.json`). |
| H-05 | Todo lo que va después de anotar el intento está dentro del `try` (`BaseException`). El intento queda «fallido» con el tipo y el motivo, y la excepción se relanza. |
| H-06 | `azar` y `momento` se detienen con el motivo si no pueden dar tantas selecciones como el titular en una fecha y clase. |
| H-07 | `leer_consumo` suma llamadas, tokens de entrada, de salida, escritos en caché y leídos de caché, uc y coste estimado. Un coste de 0 no se trata como «sin dato». El Markdown publica el coste por selección resuelta. |
| H-08 | Las advertencias de `metricas.json` y los pronósticos que el titular apartó por contaminación se copian al informe. Con un cliente que no es el simulado y la advertencia de fuga por conocimiento del modelo, ninguna comparación da veredicto firme. |
| H-09 | El aviso tiene partes independientes: cliente simulado, datos de ejemplo y universo de ejemplo. Las opciones `--datos` y `--universo` llegan al titular y al prerregistro. |
| H-10 | `evaluar` se detiene con el motivo ante una clase ajena al universo, un símbolo de otra clase o una dirección desconocida. Remuestreos, ventana, mínimo de efectivas y nivel se validan en las funciones y en la línea de órdenes. |
| H-11 | Hay pruebas del borde del cero, del nivel frente a un oráculo normal (al 80 % y al 90 %), de momento en CORTO, de la semilla por fecha y clase, y de que el informe cita la huella del fichero. Los 29 mutantes de `mutantes_r02.py` mueren. |
| H-12 | Este análisis, `pruebas.md` y la fila de la deuda están al día. El nivel es un argumento (`--nivel`) y los valores por defecto se declaran `[PROPUESTO]` en la deuda. |

**Decisiones y desviaciones del plan:**
- El intento del registro se guarda aparte, en `experimento.json`, y no dentro de `informe.json`. Así dos ejecuciones iguales siguen dando el mismo informe byte a byte (CA-4), aunque sean dos intentos distintos.
- Una semilla distinta de la prerregistrada no se rechaza: cuenta como otra variante. Así se ve en el registro que se probó más de una semilla, y ninguna es adoptable fuera del máximo.
- El remuestreo de cada lado es independiente. Como titular y referencias comparten fechas, el rango tiende a ser conservador: en el escenario A, un 3 % de veredictos firmes frente al 10 % nominal.

**Límites conocidos:**
- Con datos reales, dos oportunidades distintas de la misma fecha pueden estar correlacionadas, y eso lo absorbe el remuestreo por fecha. En cambio, dos fechas consecutivas con ventanas solapadas sobre activos distintos se tratan como independientes. El mínimo de 10 fechas efectivas lo mitiga, pero no lo elimina.
- No se ha probado con el cliente real ni con datos de K (T-86).

**Comandos para probarlo:**

```bash
.venv/bin/python -m pytest -q .docs/scripts/pruebas_banco_medida.py .docs/scripts/pruebas_registro_experimentos.py
.venv/bin/python -B .docs/tickets/T-94/mutantes_r02.py
.venv/bin/python .docs/scripts/banco_medida.py a --desde 2026-03-06 --hasta 2026-05-29 --salida <carpeta> --registro <carpeta>/r.jsonl
.venv/bin/python .docs/scripts/banco_medida.py verificar <carpeta>
```
