# T-150 · Análisis técnico

## Causa raíz o motivo

- **H-01.** `sin_datos_protegidos` sustituía las cadenas que da el detector de la más larga a la más corta con `str.replace`. Con dos datos pegados el detector da también una coincidencia que abarca los dos: el correo con el principio de la clave que lo sigue («…@example.comapi», porque el dominio de primer nivel admite letras y el «_» no lo corta) o una «sk-…» que se come las primeras letras del IBAN. Al sustituir esa primero, el resto del segundo dato («_key=VALOR», «2100 0418 …») ya no tenía la forma que el detector reconoce y la comprobación final no lo veía.
- **H-02.** `_cli` recortaba el stderr a sus 2000 últimos caracteres (el stdout a 1000) antes de que `main` lo limpiara: si el corte caía dentro de un dato, su cola ya no se reconocía.
- **H-03.** Las dos limpiezas (mensaje de `jsonschema` antes de recortarlo; `main` limpiando el fallo de un ejecutor) eran correctas pero ninguna prueba las fijaba.
- **H-04.** `resumen.json` y lo que imprime el script llevaban los `opp_id` tal cual; solo el detalle de los errores salía limpio.
- **H-05.** La cota de la regla de niveles supone que cada precio está redondeado a su paso (error de medio paso a cada lado). Truncar deja el valor de verdad en [p̃, p̃ + q): la misma anchura, pero desplazada medio paso; como el desplazamiento relativo q/2p cambia con el precio, ninguna constante cabe en todas las fechas de una serie que cambia bastante de precio (en la vía de la QA, de 36,6 a 50,2) y la copia no se agrupaba. Ensanchar la cota a un paso entero (el mutante Q09) lo resolvería, pero dobla los falsos positivos.
- **H-06.** `pd.to_datetime(..., format=...)` convierte un `TIME_PERIOD` vacío («nan» como texto) en NaT sin error, y la fila llegaba al CSV sin fecha. `http.client.IncompleteRead` (y `BadStatusLine`, etc.) son `http.client.HTTPException`, no `OSError`.
- **O-04, O-06.** `cadena_a_b.py` leía el paquete y la configuración sin capturar sus errores; el error de `yaml` copia la línea que no entiende.
- **O-05.** El mensaje de un `os.replace` que falla decía «no se escribe nada» aunque quedaran CSV ya movidos; un destino que es un enlace simbólico roto se miraba como si no existiera y se descargaba antes de fallar.

## Evidencia

Antes (HEAD `0e08a7d`), desde la raíz: `r01_01_rejillas_qa.py` 2 hallazgos (los dos truncados), `r01_02_mutantes_qa.py` N21 y N27 vivos, `r01_03_r8_y_g3_qa.py` 3 hallazgos (R1, R3, R4) y un OBS de traza (G2, paquete inexistente), `r01_04_bce_qa.py` 1 hallazgo y 3 OBS. Después: los cuatro con **0 hallazgos** (salida en `pruebas.md`). `medir_truncado.py --semillas 300` con la versión de antes (`--modulo`): la copia truncada frente a la original no se agrupa en 296 a 300 de 300 en cada rejilla; con la de ahora, 0 en todas.

## Implementación

- **Archivos cambiados y por qué**
  - `bloque_a/11_Ejecutor/bloque_a/cadena_b.py`: `_sin_tramos` (todas las apariciones de cada dato, también solapadas, como intervalos; los que se solapan o se tocan se unen; cada unión, una sustitución) y `sin_datos_protegidos` la usa (H-01).
  - `bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py`: `_pares_por_hipotesis` y, en `_etiquetas_series_copiadas`, las filas truncadas (logp y cota apiladas, n + i), el índice de la serie (`Ib`, `Kb`) para `hay` y `rend`, y las etiquetas devueltas a la serie (`% n`) (H-05); docstring con los límites (tablas por tramo, redondeo hacia arriba).
  - `.docs/scripts/cadena_a_b.py`: limpiar antes de recortar en `_cli` (H-02); `_sin_datos` y `_resumen` para todo lo que se escribe e imprime (H-04); `_leer_yaml_extra` y `_motivo_lectura` para el `--config-a` y el paquete que no se leen (O-04, O-06; `sin_envio` `PAQUETE_ILEGIBLE`).
  - `.docs/scripts/descargar_datos_bce.py`: NaT → `RespuestaBCE`; `http.client.HTTPException` capturada; `EscrituraIncompleta` y su mensaje; enlace roto en la ruta del destino → `DestinoNoValido` (H-06, O-05).
  - Pruebas: `tests/test_t150.py` (79, nuevo); `tests/test_t149.py` (+2, H-03); `tests/test_t144.py` (`_hueco_de_la_cota`, abajo).
  - Documentación: `docs/incidencias.md` (INC-T127-01: frase de las tablas por tramo en la ronda T-149 y ronda T-150; INC-T142-01: ronda T-150), `bloque_a/11_Ejecutor/README.md` (cadena B), `.docs/README.md` (fila de `cadena_a_b.py`).
- **Decisiones y desviaciones**
  - **H-05 se corrige, no se declara**: la hipótesis truncada desplaza la cota sin ensancharla y no da falsos positivos nuevos en índices ni en la rentabilidad total (300 semillas, `medir_truncado.py` con una o las dos series truncadas, y `T-149/medir_copias.py`). Dos ajustes que salieron de medir: (1) el desplazamiento solo en los precios con q/p ≤ `tolerancia_clon`; desplazando todos, un monetario casi siempre a 1,00 (paso 1) y otro que crece un 1 %/año se agrupaban en 90 de 100 (el caso B del revisor), porque desplazar medio paso de 1 cambia con el precio y alinea por azar; (2) por precio, no por serie: con el umbral por serie, una serie truncada a 0,25 que cruza 100 y pasa pocas sesiones en una década, donde el paso de esa década sale grueso, perdía la hipótesis entera (3 de 200). Hay una prueba de cada uno (`test_h05_un_paso_grande_frente_al_precio_no_se_desplaza`, `test_h05_un_precio_con_paso_grande_no_quita_la_hipotesis_al_resto`) y mutantes que las fijan (F3, F4). Ningún número nuevo: el umbral es el tope de la cota que ya existía.
  - Se conservan tal cual las líneas que mutan los scripts de T-147 y T-149 (M17, M18, M20, Q08–Q10, N06–N12): el bucle de pares no cambia de sangrado; las hipótesis entran por el iterador (`_pares_por_hipotesis`) y las filas apiladas, con el mismo nombre (`logp`, `cota_redondeo`).
  - `tests/test_t144.py::test_t149_la_cota_de_niveles_…`: el par de borde de T-149 («justo fuera» a un 0,1 % del hueco) cae dentro con la combinación redondeada/truncada, cuyo hueco es un 0,6 % menor. `_hueco_de_la_cota` toma ahora el menor de los cuatro huecos (el criterio nuevo de la regla), con los mismos ±0,1 %; la prueba sigue fijando la anchura exacta de la cota y matando Q08 y Q09 (comprobado: `T-147/revisores/r01_03_mutantes_qa.py --ticket T-144`, 0 vivos). No se debilita: la prueba no admite nada que antes rechazara salvo lo que la regla nueva acepta.
  - H-04: en vez de filtrar los `opp_id` por el patrón del esquema, se limpia todo el resumen (también rutas, textos de la vuelta y lo que venga del Bloque B): un dato que llegue por otro campo tampoco sale.
  - O-04/O-06 terminan con 1 (como pide el ticket), no con 2 (el código de «falla un ejecutor o la configuración no casa con los ámbitos de B»). Lo dice el docstring.
  - Extra no pedido, barato y dentro del alcance de O-05: el destino que es un enlace roto (la primera mitad de O-05) se rechaza antes de descargar.
- **Límites conocidos**
  - Redondeo hacia arriba (⌈p/q⌉·q) no se agrupa (sería otra hipótesis; no se ha visto en datos de mercado); una truncada con paso de más del 1 % del precio se queda como redondeada; tablas de paso por tramo de precio (MiFID II): todo declarado en INC-T127-01.
  - Coste de IDX-CONC-001: n = 2000, T = 2520, de ~3,2 s a ~5,7 s y de 551 a 698 MB (cada serie va dos veces).
  - R8: lo que el detector no ve en el original (pegado detrás de una letra, O-03) tampoco se quita (`test_h01_lo_que_el_detector_no_ve_pegado_tampoco_se_quita` lo fija); INC-T123-01.
  - BCE: el traslado no es atómico entre ficheros; ahora el mensaje lo dice con los nombres.
- **Comandos exactos para probarlo** (desde la raíz de la copia)
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t150.py tests/test_t149.py tests/test_t147.py tests/test_t144.py tests/test_t142_cadena_b.py tests/test_t141_datos_bce.py tests/test_t135_motor.py`
  - `.venv/bin/python -I .docs/tickets/T-149/revisores/r01_01_rejillas_qa.py`, `r01_03_r8_y_g3_qa.py <tmp>`, `r01_04_bce_qa.py <tmp>`; `.venv/bin/python .docs/tickets/T-149/revisores/r01_02_mutantes_qa.py <copia «t147_mut»>`
  - `.venv/bin/python .docs/tickets/T-150/mutantes.py <copia «t147_mut»>`; `.venv/bin/python .docs/tickets/T-147/mutantes.py <copia «t147_mut»>`
  - `.venv/bin/python -I .docs/tickets/T-150/medir_truncado.py --semillas 300 [--modulo <frontera_b.py de HEAD>]`
