# T-141 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; implementó otra sesión) · **Ronda:** r01 · 2026-11-15
- **Copia:** git desconectada en HEAD `a9f402f` (T-141 entra en `19f3f3b`).

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| `pytest -q tests/test_t141_datos_bce.py` (A) | 4 pasan |
| `python -I .docs/scripts/descargar_datos_bce.py <dir>` (descarga real, API pública del BCE, sin clave) | 6 series de 3 039 cierres, 2015-01-02 → 2026-11-13; las seis con las mismas fechas |
| `comprobar_datos_a.py <dir> --clases DIV --as-of 2026-11-13` en H3 y en H1 | 6 de 6 OK, código 0 (sin `--clases`: código 1, porque faltan los otros once tipos, como debe ser) |
| `python -m bloque_a.cli --cliente mock --datos <dir> --as-of 2026-11-13 ciclo` | COMPLETO, ENTREGADA, G3 APTO, top-3 de DIV |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | 4 pruebas en verde (cruces, huecos y no positivos, lectura por HT-01) |
| CA-2 | sí | Descarga real, 6 de 6 OK en H3 y en H1 y ciclo mock ENTREGADA (tabla de arriba) |
| CA-3 | sí | Suite de A (6 122 pasan), ruff 2838 ≤ 2838, mypy A 109 y B 159 en cuota, goldens CT y gates ligeros en verde (misma copia que la QA de T-142). `./tools/check_all.sh` no se lanzó por instrucción |

## Dirección de los cruces (contraste con otra fuente)

`revisores/r01_contraste_fred.py`: contraste con los tipos de mediodía de Nueva York de la Reserva Federal (H.10, FRED `fredgraph.csv`, pública y sin clave). Es una fuente independiente, con otra hora de fijación. Hay 704 días comunes desde 2024-01-01:

| Cruce | Serie de la Reserva Federal | Mediana del desvío | Máximo |
| --- | --- | --- | --- |
| EURUSD=X (USD/EUR) | DEXUSEU | 0,13 % | 1,31 % |
| USDJPY=X (JPY/USD) | DEXJPUS | 0,15 % | 2,18 % |
| GBPUSD=X (USD/GBP) | DEXUSUK | 0,14 % | 1,24 % |
| AUDUSD=X (USD/AUD) | DEXUSAL | 0,18 % | 1,74 % |
| USDCHF=X (CHF/USD) | DEXSZUS | 0,14 % | 1,35 % |
| USDMXN=X (MXN/USD) | DEXMXUS | 0,25 % | 2,07 % |

Los seis cocientes van en la dirección correcta. Un cruce invertido daría un desvío de órdenes de magnitud. Los máximos salen de la diferencia horaria (14:15 CET frente a mediodía en Nueva York) en días de mucho movimiento.

## Ataques (`revisores/`)

- `r02_festivos_y_huecos.py`: huecos reales de la serie (el mayor, de 5 días, en Semana Santa y Navidad: días de cierre de TARGET). También mira la frescura de PS2 en H1, H2 y H3 con `as_of` en el festivo y al día siguiente (Viernes Santo, Lunes de Pascua, 1 de mayo, 26 de diciembre y 1 de enero) y el borde de `fecha_publicacion`: con `as_of` D se ve el dato de D y con D−1 no. Los festivos de una sola plaza (Acción de Gracias, por ejemplo) no dejan hueco, porque el BCE publica igual. El dato es la fijación del BCE, no el cierre de esa plaza.
- `r03_respuestas_raras.py`: respuestas simuladas del servicio, sin red (cuerpo vacío, solo cabecera, falta una moneda, fila repetida, NaN, negativos, HTML con 200, HTTP 404).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `comprobar_datos_a.py <dir> --clases XXX` (o `--clases div`, en minúsculas) `--as-of 2026-11-13; echo $?` | Esperado: error (ningún símbolo comprobado). Obtenido: «0 de 0 símbolos OK» y **código 0**, el mismo verde que con 6 de 6. Una errata deja la comprobación en verde sin mirar nada | Rechazar tipos fuera de los doce (`choices`) y terminar con código distinto de 0 si el universo filtrado queda vacío | abierto |
| H-02 | baja | Docstring de `descargar_datos_bce.py`: «publica … a las 14:15 (CET) … el dato se conoce a las 14:15» | La página del BCE dice que los tipos reflejan el mercado a las 14:15 CET y se **publican hacia las 16:00 CET**. Poner `fecha_publicacion` el mismo día sigue siendo correcto con cortes de fin de día, pero no con un ciclo que corra antes de las 16:00 | Corregir el texto (16:00 CET) y documentar que el «cierre» es la fijación de las 14:15 CET, no un cierre de mercado | abierto |
| H-03 | baja | `r03_respuestas_raras.py <dir>` | Esperado: un mensaje claro y la carpeta sin tocar. Obtenido: (a) las respuestas vacías, la falta de una moneda, el HTML y el 404 acaban en traza (`KeyError`, `EmptyDataError`, `ValueError`, `HTTPError`), aunque con código distinto de 0 y sin escribir nada; (b) si un cruce se queda sin filas válidas (JPY negativo), escribe EURUSD y un USDJPY vacío y luego cae con `IndexError`, y la carpeta queda **a medias**; (c) una fila repetida con otro valor se resuelve en silencio con la primera (`aggfunc="first"`) | Validar todo antes de escribir (ninguna serie vacía, sin fechas repetidas por moneda) y escribir a una carpeta temporal que se renombra al final; mensajes en lugar de trazas | abierto |
| H-04 | baja | `r02_festivos_y_huecos.py <dir>` | El calendario del BCE (TARGET: 1-1, Viernes Santo, Lunes de Pascua, 1-5, 25-12 y 26-12) no es el de `ps2_festivos` (`[PROPUESTO]`: Lunes de Pascua `false`, sin el 1 de mayo; con el 24-12 y el 31-12, en los que el BCE sí publica). Con `as_of` en Lunes de Pascua, H2 da ANTIGUO en los seis símbolos (4 días > 3). Los ciclos semanales en viernes festivo (Viernes Santo, 1-5-2026) dan OK | Llevarlo a T-57 junto a INC-T53-02: festivos por fuente o por plaza | abierto |

## Veredicto

**APTO** (r01). Se cumplen CA-1 a CA-3, los cruces son correctos (contraste independiente) y no hay hallazgos críticos ni altos. H-01 (medio) y H-02 a H-04 (bajos) pasan a la deuda técnica con su ID si no se corrigen antes de cerrar. Los datos descargados no están en el repositorio: se dejaron en el scratchpad y se borraron. El cierre lo hace la sesión coordinadora.
