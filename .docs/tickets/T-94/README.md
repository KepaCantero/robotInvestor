# T-94 · Banco de medida para A, B y C

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r03 APTO, 15-11-2026) |
| Pieza | `.docs/scripts` (fuera de los bloques): `banco_medida.py` y sus pruebas |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (operador, 15-11-2026: «Vamos a empezar con los Tickets») |
| Aprobación del operador | aprobada el 2026-11-11: «Te autorizo que empieces con el banco de medida y las plantillas» (tras aceptar la tanda 1: pauta común de A, B y C con banco de medida) |
| Deuda técnica | T-94 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Medir, con los mismos datos y fechas de corte, si el diseño actual de un bloque de búsqueda o selección elige mejor que referencias baratas (azar y una regla de solo código), y cuánto cuesta. Es el paso 0 de los rediseños de A, B y C (propuestas en `.docs/diseno/`): ningún recorte se acepta sin pasar por aquí.

## Alcance

- Entra:
  - el banco genérico: contendientes que devuelven selecciones (fecha, símbolo, dirección, horizonte) y un evaluador común;
  - el Bloque A completo como titular, ejecutado en modo backtest con el cliente simulado (o real, si se pide) y con el consumo de cada llamada;
  - dos referencias: azar con semilla y momento (solo código, sin datos posteriores al corte);
  - prerregistro sellado con huella antes de evaluar;
  - informe en JSON y en Markdown con rangos y el veredicto «todavía no se sabe» cuando el rango incluye el cero (decisión 6 de la tanda 1).
- No entra:
  - cambiar nada de `bloque_a/`, `bloque_b/` ni del marco común (solo se importan funciones de A para ejecutarlo);
  - evaluar la calidad de B y C: B no tiene modo backtest y C no existe aún. Queda la interfaz para conectarlos (un contendiente más);
  - datos reales: con los datos sintéticos del ejemplo el resultado solo prueba la tubería. Con datos de K (T-86) el mismo banco da la medida de verdad.

## Diseño

- **Contendiente:** función que, dadas las fechas de corte y el universo, devuelve filas `fecha_asof, clase, simbolo, direccion, horizonte` y su consumo. Tres en la primera versión:
  - `titular_a`: el Bloque A tal cual, en backtest; se espía el cliente para contar llamadas y tokens por agente, como `medir_consumo_a.py`;
  - `azar`: mismo número de selecciones por fecha y clase que el titular, elegidas al azar dentro de la clase con semilla fija;
  - `momento`: mismo número por fecha y clase, las de mayor rentabilidad en las últimas 63 sesiones hasta la fecha de corte (solo datos conocidos entonces).
- **Evaluador común:** para cada selección, rentabilidad del símbolo entre el último cierre conocido en la fecha de corte y el último cierre en la fecha de resolución (horizontes de la configuración de A), menos la de la **cesta de su clase** (media de todos los símbolos del universo de esa clase en la misma ventana), con signo según la dirección. Es la pregunta de A: ¿eligió dentro de la clase mejor que la media? Si falta el precio final, la selección queda sin resolver; nunca se estima.
- **Estadística:** media del exceso, tasa de acierto y rango del 90 % por remuestreo con semilla. Diferencia del titular frente a cada referencia, con su rango: «mejor», «peor» o «todavía no se sabe».
- **Coste:** llamadas, tokens de entrada y salida y coste estimado del titular (de su `consumo.csv`); las referencias cuestan cero. Coste por selección resuelta.
- **Prerregistro:** antes de evaluar se escribe `prerregistro.json` (hipótesis, contendientes, ventana, semilla, métrica y versión del banco) y su huella SHA-256; el informe la cita.
- Estado persistido: no cambia nada del sistema; todo va a una carpeta de salida.
- Números: semilla, ventana de momento (63 sesiones) y remuestreos (2.000) son argumentos con valor por defecto; no salen de ningún Documento 0 porque el banco no es parte del robot.
- Cómo falla cerrado: si el titular falla, si una fecha no tiene datos o si el universo no casa con los datos, el banco se detiene con el motivo; no rellena huecos.
- **Ronda r02 (QA r01, H-01 y H-02):** una apuesta repetida sobre el mismo activo, clase y dirección mientras su ventana sigue abierta cuenta una vez; el rango remuestrea fechas de corte enteras; sin `--min-efectivas` fechas por lado (10) no hay veredicto. El detalle de la ronda está en `analisis-tecnico.md`. **Ronda r03 (QA r02, H-13):** solo cuentan las fechas de corte cuyas ventanas no se solapan, calculadas con el titular y comunes a todos.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Fuga de datos futuros en la referencia de momento | Una referencia mejor de lo que sería | Solo usa cierres hasta la fecha de corte; prueba que cambiar precios posteriores no cambia la selección |
| Leer el resultado con datos sintéticos como real | Conclusiones falsas | El informe lo dice en la primera línea cuando el cliente es simulado o los datos son de ejemplo |
| Pocas selecciones | Rangos enormes | Veredicto «todavía no se sabe» y número de selecciones visible |
| Acoplamiento a A | Si A cambia sus salidas, el banco se rompe | Lee solo `senales.csv` y `consumo.csv` por nombre de columna; prueba de integración con A real |

## Criterios de aceptación (binarios)

1. CA-1: `banco_medida.py a` ejecuta el titular A con el cliente simulado sobre los datos de ejemplo y deja `prerregistro.json`, `informe.json` e `informe.md`.
2. CA-2: el evaluador da el exceso exacto en un caso construido a mano (precios conocidos).
3. CA-3: la referencia de momento no cambia si se alteran precios posteriores a la fecha de corte.
4. CA-4: con la misma semilla, dos ejecuciones dan el mismo informe byte a byte.
5. CA-5: con el rango incluyendo el cero, el veredicto es «todavía no se sabe».
6. CA-6: una selección sin precio final queda sin resolver y no entra en la media.
7. CA-7: el informe declara en su primera línea si el cliente es simulado o los datos son de ejemplo.
8. CA-8: no se modifica ningún fichero de `bloque_a/`, `bloque_b/` ni `sistema_global/marco_comun_c/`, y el gate del repositorio sigue en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Exceso frente a la cesta con precios a mano | Nominal | CA-2 |
| Momento con precios futuros alterados | Límite | CA-3 |
| Dos ejecuciones con la misma semilla | Regresión | CA-4 |
| Veredicto con rango que cruza el cero y con rango positivo | Límite | CA-5 |
| Selección con fecha de resolución fuera de los datos | Fallo cerrado | CA-6 |
| Símbolo de la selección ausente en los datos | Fallo cerrado | se detiene con motivo |
| Banco completo sobre A con cliente simulado | Integración | CA-1, CA-7 |
| `git status` de bloques y marco tras la ejecución; `./tools/check_all.sh` | Regresión | CA-8 |

## Scripts

Crea `.docs/scripts/banco_medida.py` y `.docs/scripts/pruebas_banco_medida.py`. Se inspira en `.docs/scripts/medir_consumo_a.py` para espiar el cliente.

## Registro

- 2026-11-11 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-11 · EN CURSO · claude · plan escrito; implementa claude, QA astra cuando termine sus revisiones de diseño
- 2026-11-11 · EN QA · claude · banco y pruebas (10/10) listos; informe en `pruebas.md`. Espera la QA de Astra
- 2026-11-15 · NO APTO · QA r01 (revisor nuevo, base `df4a60a`, gate 12/12): H-01 y H-02 altos (el rango trata como independientes selecciones repetidas de la misma oportunidad y da «mejor» con una sola selección por lado; sin habilidad, veredicto firme el 42,5 % y el 87 % de las veces), H-03 a H-08 medios (valores no finitos sin fallo cerrado, prerregistro creado en cada ejecución, intento sin resultado, referencias con menos selecciones, coste sin caché, aviso de fuga perdido), H-09 a H-12 bajos. Detalle en `qa.md`
- 2026-11-15 · EN QA · Ronda r02, por orden del operador («Corrige todos los hallazgos de T-94 hasta que supere la QA»): H-01 a H-12 corregidos en el banco 0.3.0 con su prueba de regresión cada uno; 51 pruebas, 29 mutantes muertos; `r01_02` en 3,0 %, 0,0 % y 0,0 % de veredictos firmes sin habilidad
- 2026-11-15 · NO APTO · QA r02 (revisor nuevo, base `cc2dd22`, gate 12/12): CA-1 a CA-8 se cumplen; H-13 alto (ventanas solapadas sobre activos distintos: 23 % de veredictos firmes sin habilidad), H-14 a H-16 medios y H-17 a H-20 bajos
- 2026-11-15 · EN QA · Ronda r03: solo fechas sin solape (simulación nula con fechas suficientes: 9,5 % y 10,0 %); experimento por fuente; `verificar` con `informe.md` y sin registro; fechas AAAA-MM-DD estrictas; consumo estricto; cotas de un veredicto; 82 pruebas y 57 mutantes muertos
- 2026-11-15 · CERRADO · QA r03 APTO (revisor nuevo, base `1e896e6`, gate 12/12): H-01 a H-20 corregidos; simulación nula propia con fechas suficientes entre el 10,4 % y el 13,7 % de veredictos firmes sin habilidad; H-21 a H-29 (medios y bajos) a la deuda como T-133
