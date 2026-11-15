# T-145 · Análisis técnico

## Causa raíz

- **H-01.** `estimar()` suma el peor caso de las filas de `llamadas.json`, que son las llamadas que hizo el cliente simulado. Varias llamadas del ciclo dependen de lo que responde el modelo y el simulado no las dispara: las peticiones de conocimiento CT-07/CT-08 (hasta `seleccion.peticiones_conocimiento_por_clase` por tipo, con búsqueda), la contrarréplica CT-13, la reescritura de AG-17 por C12, el segundo dictamen G3 (AG-18) y el informe de aprendizaje (AG-20, solo con pronósticos resueltos). Y el encargo de los agentes que leen a otros crece con lo que escriben esos otros.
- **H-02.** `_forma_de_fecha` admitía un año (19xx/20xx) o una MMAA en cualquier extremo de la serie: «año + cuatro niveles que pasan Luhn» tenía la forma de «año + tarjeta».
- **H-03.** El reparto en tarjetas solo se probaba desde el principio o desde el final, con lo sobrante en un extremo.
- **H-04.** Con la ventana del ciclo, un símbolo cuyos datos acaban antes de la ventana daba `DatosNoDisponibles` y se tomaba por «no hay archivo».
- **H-05.** El texto del §1 del borrador era una cadena fija con «CT-06 a CT-14».
- **H-06.** Faltaban pruebas en esos tramos.

## Hallazgo nuevo: el presupuesto en UC no corta antes de la llamada

`Bloque._invocar` (orquestacion.py) llama si `Presupuesto.puede(bolsa, estimado)`, con `estimado = _estimar_uc(agente, mensaje)`: el encargo medido (más 1 500 tokens), el prompt de sistema **como lectura de caché** y **2 500 tokens de salida**, sin reparación ni continuaciones. Lo real (`_cargar`) se carga **después** de la llamada. Además:

1. durante la fase en paralelo, la escritura de caché de los agentes que trabajan para varios tipos (AG-10, AG-11, AG-12, AG-14, AG-16) se carga como lectura (`leido`, factor 0,1) y la diferencia solo se reparte en `liquidar_primas`, después de la fase;
2. AG-18 (dictamen G3), AG-19 (auditoría) y AG-20 (informe de aprendizaje) se llaman sin presupuesto;
3. las búsquedas web no cuentan en UC (`Contabilidad.uc_de`).

Consecuencia: una bolsa acaba por encima de su límite. Con el peor caso pasado por el cliente real (SDK falso que declara la entrada ×1,35 como escritura de caché y `max_tokens` de salida, primer intento no JSON) y la configuración por defecto (solo DIV): bolsa DIV con 48,4 UC consumidas frente a un límite de 26,3 (asignado 18, +25 % y 3,8 de ampliación autorizada); con los 12 tipos, las doce bolsas de los tipos acaban entre 32 y 42 UC con límites de 22,5 a 26,8. Lo que sí garantiza el código: cada llamada admitida empieza con lo consumido ≤ límite − estimado, y el límite no pasa de `asignado × (1 + ampliacion_max_autorizable)` (`autorizar_hasta_tope`). Así, cada bolsa acaba como mucho en su límite máximo más su última llamada más la caché cargada como lectura; `test_h01_el_presupuesto_se_pasa_…` lo comprueba. No se cambia el ejecutor: el encargo pide documentarlo, y estimar con el peor caso cerraría fases que hoy se hacen; queda en INC-T129-01 para decidir.

## La cota nueva (`estimar_coste_ciclo_a.cota_ciclo`)

La menor de dos, cada una con los supuestos S1–S5 (en `SUPUESTOS`, que imprime el script):

- **Por llamadas.** `LLAMADAS_POR_TIPO` y `LLAMADAS_DEL_CICLO` recogen, de `orquestacion.py`, cuántas llamadas puede hacer como mucho un C1 de la V5 en nivel N2: por tipo, cribado (1), petición de conocimiento (`peticiones_conocimiento_por_clase`, a AG-14 o AG-16, la más cara), prospectiva (1), refutación (1), respuesta a objeciones (1), contrarréplica (1) y curación (1); por ciclo, informe de aprendizaje (1), integración (1), dictamen G3 (2: `_validar_g3` corta en el segundo intento), redacción (2: la reescritura por C12) y auditoría (1). Solo divisas: 14 (se miden 8); 12 tipos: 91 (se miden 77). Cada llamada, en su peor caso (`peor_llamada`): por cada intento `r` y continuación `v`, toda la entrada como escritura de caché con el margen 1,35, más `(r + v) · max_tokens` reenviados (en la reparación `agentes.invocar` reenvía el texto de la última petición de cada intento; en la continuación, `AnthropicClient.generar` reenvía las respuestas pausadas de ese intento) y `r` mensajes de errores (15 de 300 caracteres), `max_tokens` de salida y `max_usos` búsquedas en los agentes con búsqueda. El encargo: el mayor medido para ese agente (si no se llamó, el mayor del ciclo) más la salida máxima de las llamadas que puede leer: las anteriores de su tipo; en las del ciclo, las de su columna «lee» (la integración, solo el cribado; el dictamen, la redacción y la auditoría, todo lo anterior).
- **Por presupuesto.** El presupuesto del ciclo con la ampliación máxima (el mayor sobre los repartos N1/N2 posibles) al peor precio por UC de los agentes de cada bolsa (una UC son 16 000 tokens de entrada o 3 000 de salida: con Opus en las dos bolsas, 0,128 USD), más la última llamada de cada bolsa, la caché cargada como lectura (la escritura cabe en el prompt de sistema), AG-18/19/20 y las búsquedas.

| | Solo divisas | 12 tipos |
| --- | --- | --- |
| Peor caso de las llamadas medidas (T-140) | 4,58 | 56,79 |
| Cota por llamadas | **19,54** | **166,56** |
| Cota por presupuesto | 68,29 (límites 46,08 + última llamada 10,92 + caché 5,29 + fuera 5,60 + búsquedas 0,40) | 233,18 |
| Caminos del revisor (`r01_01` 1 / 1+2; `r01_02` / con C12) | 8,85 / 9,81; 4,57 / 5,04 | 79,18 / 79,33; 36,02 / 36,53 |

En los dos casos manda la cota por llamadas: el presupuesto del ciclo es el mismo (240 UC) con un tipo o con doce, y con uno casi todo va a la bolsa COMÚN (222 UC), que el ciclo no gasta. La cota es holgada a propósito (S4 suma salidas máximas que el ciclo no alcanza en la práctica: con los 12 tipos y las respuestas alargadas del revisor, el mayor encargo de AG-19 es 26 377 tokens y S4 supone 901 003); se puede afinar con el modo sombra, no sin la API.

Contraste del supuesto S4 (`contraste_cota.py`): con las respuestas del simulado alargadas hasta cerca de `max_tokens` (escenario 2 del revisor), ningún encargo pasa del que supone la cota, con divisas y con los 12 tipos.

## R8 (H-02 y H-03): decisión y medidas

Regla nueva (`[PROPUESTO]`, INC-T123-01): en cinco o más grupos de cuatro cifras, la serie **entera** se reparte en tarjetas válidas (red y Luhn), cada una seguida, si acaso, de su caducidad MMAA (mes 01–12); lo que sobra solo va detrás de una tarjeta; un año ya no es fecha. Programación dinámica desde el final (`_tarjetas_de_la_serie`, lineal). Un PIN tras la caducidad se probó y se descartó: marcaba el 7,3 % de las filas «cuatro niveles, fecha MMDD y otro nivel».

| Fila (r01_03 del revisor, 2000 por forma; `medir_filas_r8.py`, 5000) | T-136 | T-140 | T-145 |
| --- | --- | --- | --- |
| año y cuatro niveles (4000–5999) | 0 | 7,5 % | **0** |
| cuatro niveles y el año al final | 0 | 8,2 % | **0** |
| fecha MMDD y cuatro niveles | 0 | 8,2 % | **0** |
| año y cuatro precios del oro | 0 | 5,2 % | **0** |
| con guiones / dos años delante | 0 | 7,3 % / 6,6 % | **0 / 0** |
| ocho niveles (declarado) | 0 | 0,7 % | 0,7 % |
| año y ocho niveles | 0 | 0,4 % | **0** |
| cuatro niveles y la fecha MMDD detrás (límite declarado) | 0 | 7,1 % | 7,1 % |
| cuatro precios del oro y la fecha detrás | 0 | 6,6 % | 5,2 % |
| cinco números al azar (1000–9999) | 0 | 0,3 % | 0,1 % |
| tarjeta, caducidad y otra tarjeta / dos con su caducidad | 0 | 0 | **100 %** |
| tarjeta con caducidad, dos seguidas, con guiones | 0 | 100 % | 100 % |
| año delante («2026 <tarjeta>») | 0 | 100 % | 0 (declarado) |
| año, tarjeta y caducidad; caducidad delante y año detrás; PIN tras la caducidad | 0 | 0 | 0 (declarado) |

## Implementación

- `bloque_a/contratos.py`: `_forma_de_fecha` → `_forma_de_caducidad` (solo MMAA); `_tarjetas_de_la_serie`; `tarjetas_en_texto` la usa en las series largas.
- `.docs/scripts/estimar_coste_ciclo_a.py`: `estimar` no cambia (lo usan T-129, T-136 y T-140, y pasa a llamarse en la salida «peor caso de las llamadas medidas»); nuevos `LLAMADAS_POR_TIPO`, `LLAMADAS_DEL_CICLO`, `SUPUESTOS`, `peor_llamada`, `cota_ciclo` y `calcular`; `main` imprime las tres cifras y los supuestos.
- `.docs/scripts/comprobar_datos_a.py`: sin datos en la ventana, `ultima_fecha` de HT-01 decide entre ANTIGUO (con su último dato en `hasta`) y FALTA; docstring.
- `.docs/scripts/borrador_anexo_b.py`: `_tramos` y dos entradas del §1 derivadas de `RETORNOS_INTERNOS` y `RETORNOS_DEL_MOTOR`; borrador regenerado.
- `tests/test_t140.py`: `test_h02_…` cambia dos casos («2027 <tarjeta>» y «<tarjeta> 1999» dejan de detectarse), comentado «T-145»; es una decisión declarada, no un debilitamiento silencioso.
- `docs/incidencias.md`: INC-T123-01 (regla y tasas), INC-T129-01 (cota del ciclo y el presupuesto que no corta), INC-T114-01 (matiz de CT-09 y CT-10).

## Desviaciones y límites

- La tabla de llamadas está escrita a mano desde `orquestacion.py`; si el ciclo cambia, el script falla cerrado solo cuando el ciclo medido hace más llamadas de un agente de las previstas (una llamada nueva que el simulado no dispara no se ve).
- La cota no modela la ventana de contexto de cada modelo (por encima la API rechaza la petición y no la cobra): es más alta de lo necesario.
- Los scripts de mutantes del revisor de T-140 (`r01_05_mutantes.py`) se refieren a código que ya no existe (T01–T09); sus equivalentes, y los vivos K04, V02, T06 y T07, están en `mutantes_t145.py`.

## Comandos

```bash
py=/home/user/robotinvestor/.venv/bin/python   # o .venv/bin/python
cd bloque_a/11_Ejecutor
$py -m pytest -q -p no:cacheprovider tests/test_t145.py tests/test_t140.py
$py ../../.docs/scripts/medir_consumo_a.py <div>  &&  $py ../../.docs/scripts/estimar_coste_ciclo_a.py <div>
$py ../../.docs/scripts/medir_consumo_a.py <doce> 2024-03-29 --config <doce.yaml>  &&  $py ../../.docs/scripts/estimar_coste_ciclo_a.py <doce> --config <doce.yaml>
$py -I ../../.docs/tickets/T-140/revisores/r01_02_peor_caso_con_cliente_real.py <tmp> [--config <doce.yaml>] [--forzar-c12]
$py -I ../../.docs/tickets/T-145/contraste_cota.py <tmp> [--config <doce.yaml>]
cd ../.. && $py -I .docs/tickets/T-140/revisores/r01_03_tarjetas_series_largas.py <contratos.py de T-136>
$py .docs/tickets/T-145/mutantes_t145.py <copia desechable con «_mut» en la ruta>
```
`<doce.yaml>`: `perfiles: {activos: [RV, RF, DIV, MP, INM, CRI, ALT, IDX, FON, DER, MON, TCV]}`.
