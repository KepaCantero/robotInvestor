# T-131 · QA independiente

# Ronda r01 · 2026-11-15

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación (Claude; implementó otra sesión de Claude) · **Ronda:** r01
- **Copia revisada:** copia git desconectada en `fe5b7d0` (T-131 entra en ese commit: `.docs/scripts/comprobar_datos_a.py`, `.docs/scripts/borrador_anexo_b.py`, `.docs/diseno/bloque_a/borrador_correccion_anexo_b.md`, `tests/test_t131_preparativos.py`).
- **Orden de lectura:** `README.md` → los dos scripts y la prueba → `ht01_datos.py` (`ProveedorCSV`, `serie`, `cierres`) → `divergencias_anexo_b.json` e INC-T114-01 → mis scripts → al final `analisis-tecnico.md` y `pruebas.md`.

## Reproducción desde limpio

Desde la raíz de la copia, con el intérprete del repositorio (`py`).

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Orden de `pruebas.md` | `py .docs/scripts/comprobar_datos_a.py bloque_a/11_Ejecutor/ejemplos/datos_sinteticos --as-of 2024-03-29` | **57 de 57 OK, código 0**: coincide |
| | `py .docs/scripts/borrador_anexo_b.py --comprobar` | código 0, sin escribir (fecha del fichero intacta) |
| Mi script 1 | `py -I .docs/tickets/T-131/revisores/r01_01_carpetas_estropeadas.py` | **14 ok, 5 fallos** (H-01, H-03). Bien: vacío, binario, separador «;», fechas con zona, fechas imposibles → INVALIDO; solo cabecera y todo posterior a as_of → FALTA; `Date`/`Close` con BOM y un hueco de 40 días → OK; datos acabados el 30-10-2026 con as_of 2027 → todo ANTIGUO y código 1 |
| Mi script 2 | `py -I .docs/tickets/T-131/revisores/r01_02_fidelidad_borrador.py` | 23 de 23 contratos con fila; valores en otro campo y contratos sin campos, todos; rutas de jsonschema traducidas bien formadas; `--comprobar` coincide. Pero 11 de 55 mensajes de los flujos no aparecen (8 son los de los lotes, que cubre el cambio general; 3 no, ver H-02). Los 3 «sin reflejar» de `por_contrato` son falsos avisos de mi script (el motivo «faltan campos mínimos [piezas]» sí está, como «rechaza el ejemplo») |
| Suite, goldens, gates y cuotas | comunes a T-129…T-132 (ver «Comunes» en `T-132/qa.md`) | ver allí |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | **no** | 57/57 OK, el umbral cambia con el horizonte y admite `Date`/`Close`: sí. «Inválido se distingue»: solo para lo que HT-01 rechaza al leer el archivo; un cierre de texto, cero o negativo y las fechas repetidas dan **OK** (H-01) |
| CA-2 | sí en sus términos | `--comprobar` coincide; los 23 contratos tienen fila; sin mensajes de jsonschema sin traducir. Pero ver H-02 (lo que se queda fuera) |
| CA-3 | sí, salvo el gate entero (no lanzado por instrucción) | `test_t131_preparativos.py` en la suite (4 pruebas) |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | alta | `r01_01` [1]: copiar `XLK.csv` de los datos de ejemplo y poner todos los cierres a `n/d`, a 0, en negativo, o repetir las tres últimas filas; `comprobar(carpeta, universo.head(1), "2024-03-29")` | **Esperado** (README: «es inválido (con el motivo de HT-01)»; `analisis-tecnico.md`: «rechaza lo mismo que rechazaría un ciclo»). **Obtenido:** **OK** en los cuatro casos. El script llama a `ProveedorCSV.serie()`, que devuelve las filas marcadas (`_invalido`, `_duplicada`) sin validarlas; la validación de cierres no numéricos, no finitos, ≤ 0 y de fechas repetidas está en `cierres()` y `valor_en()` (`_validar_cierres`), que son las que usa el ciclo, y ahí el símbolo se rechaza. El script falla abierto justo con los defectos más corrientes de un proveedor real («n/d», «-», ceros, filas duplicadas), que es para lo que sirve: decir antes de un ciclo si la carpeta sirve | Validar con `prov.cierres(simbolo)` (o `_validar_cierres` sobre la ventana que pide el ciclo) y dar INVALIDO con su motivo; pruebas con cierre de texto, cero, negativo y fecha repetida | abierto |
| H-02 | media | `r01_02` [2], y comparar el borrador con INC-T114-01 (`docs/incidencias.md`, línea 160 y siguientes) | **Esperado:** el borrador recoge todo lo que difiere (golden e INC-T114-01). **Obtenido:** el generador descarta los mensajes «(raíz)» suponiendo que ya están en «el ejecutor admite que falte», y no siempre lo están: se pierden `query_id` de CT-03 (la consulta no lo lleva, el bloque lo asigna), `run_id` de CT-23 y el tipo de `escalado` en CT-03 (nulo en una respuesta N0; el borrador solo dice «admite que falte»). De INC-T114-01 tampoco están: `fecha_corte` de CT-09, que el ejecutor exige siempre (el Anexo B solo en evaluaciones y backtesting); que los retornos internos CT-06 a CT-14 no se validan en la mensajería sino con `ESQUEMAS`, con otros nombres (el borrador propone «marcarlos opcional», que diría lo contrario de lo que pasa: se exigen, con otros nombres); y «lo que el Anexo B deja abierto» (la codificación de `coincide` y de `independiente`, que el borrador solo nombra como campos que pueden faltar, y los nombres de las claves de `fechas` de CT-11) | Que el generador no descarte un mensaje «(raíz)» si su campo no está en `el_ejecutor_admite_que_falte`, y que lo no-«required» (tipo, enum) salga como fila; añadir a `OTROS` lo de INC-T114-01 que no está en el golden (CT-09 `fecha_corte`, retornos internos con `ESQUEMAS`, lo que queda abierto), y para CT-06 a CT-14 proponer «describir los campos de `ESQUEMAS`» en vez de «opcional» | abierto |
| H-03 | baja | `r01_01` [2]: último cierre el viernes 22-03-2024, as_of el lunes 25-03-2024, `--horizonte H1` | **Esperado:** el mismo estado que el ejecutor, que en H1 cuenta sesiones (`calendario._sesiones_entre`: 1 sesión, dentro del máximo). **Obtenido:** ANTIGUO («hace 3 días, máximo 1 en H1»). `analisis-tecnico.md` dice que es más estricto a propósito y que «se dice en la ayuda del script», pero la ayuda no lo dice | Contar sesiones en H1 con `_sesiones_entre` y `ps2_festivos` (como `orquestacion._puertas`), o decirlo en la ayuda | abierto |
| H-04 | baja | `py .docs/scripts/comprobar_datos_a.py /no/existe` | Termina con código 1, pero con la traza de `FileNotFoundError` en vez de un mensaje | Capturarla y dar el motivo en una línea | abierto |

Los scripts de ataque están en `revisores/` (r01_01 y r01_02).

## Invariantes

- No cambia el ejecutor ni el corpus: el borrador queda en `.docs/diseno/` y dice que no se aplica. ✔
- Falla cerrado: **no** en `comprobar_datos_a.py` (H-01: da OK a datos que el ciclo rechaza).
- Números a mano: el umbral sale de `ps2_antiguedad_maxima_dias` (Anexo A). ✔
- Decisiones del operador: ninguna tomada; el borrador las deja abiertas (CT-22, listas cerradas). ✔
- Secretos y datos personales: ninguno. ✔

## Veredicto

**NO APTO** · H-01 (alta): la comprobación de datos, cuyo fin es saber antes de un ciclo si una carpeta sirve, da OK a cierres de texto, cero o negativos y a fechas repetidas que el ciclo rechaza, así que CA-1 («inválido se distingue») no se cumple. La corrección es pequeña (validar con `cierres()`). Además H-02 (media: el borrador del Anexo B deja fuera tres diferencias del golden y cuatro puntos de INC-T114-01, y para los retornos internos propone lo contrario de lo que pasa) y dos bajos. Tras corregir, vuelvo a ejecutar `r01_01` y `r01_02` en una ronda r02.
