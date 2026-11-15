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

# Ronda r02 · 2026-11-15

- **Revisor:** subagente revisor nuevo, sin contexto de la implementación ni de la r01 (Claude; implementó otra sesión de Claude) · **Ronda:** r02
- **Copia revisada:** copia git desconectada en `197aaca` (instantánea para QA de T-131 r02, T-133 y T-134). Versión de T-130 para comparar y mutantes, en una copia desechable dentro del scratchpad («qa14_mut»), ya borrada.
- **Orden de lectura:** README → diff de `comprobar_datos_a.py` y `borrador_anexo_b.py` → `ht01_datos.py` (`serie`, `cierres`, `_validar_cierres`) y `orquestacion.senales_clase` (la ventana del lote) → el borrador generado, `divergencias_anexo_b.json`, INC-T114-01 y `motor/servicio.py` (lo que devuelve el Motor) → los scripts de la r01 y los míos → al final `analisis-tecnico.md` y `pruebas.md`.

## Reproducción desde limpio

Desde la raíz de la copia, con el intérprete del repositorio (`py`).

| Comprobación | Orden | Resultado |
| --- | --- | --- |
| Orden de `pruebas.md` | `py .docs/scripts/comprobar_datos_a.py bloque_a/11_Ejecutor/ejemplos/datos_sinteticos --as-of 2024-03-29` | **57 de 57 OK, código 0** |
| | `py .docs/scripts/borrador_anexo_b.py --comprobar` | código 0, sin escribir |
| Script r01_01 de la r01, tal cual | `py -I .docs/tickets/T-131/revisores/r01_01_carpetas_estropeadas.py` | **18 ok, 1 «fallo»** («fechas duplicadas»): cierre de texto, cero y negativo → INVALIDO (H-01); H1 del viernes al lunes → OK, 1 sesión (H-03); carpeta inexistente → código 2 con mensaje (H-04) |
| Script r01_02 de la r01, tal cual | `py -I .docs/tickets/T-131/revisores/r01_02_fidelidad_borrador.py` | **7 ok, 1 «fallo»** («cada dato de por_contrato en su fila»); 44/44 mensajes descartados dichos en el borrador |
| Mi script | `py -I .docs/tickets/T-131/revisores/r02_01_ventana_del_ciclo_y_borrador.py` | **8 ok, 5 fallos** (H-05, H-06) |
| Ciclo real con la carpeta de H-05 | copia de los datos de ejemplo con el cierre de `EURUSD=X` del 2022-06-01 a `n/d`; `bloque-a --cliente mock --datos <copia> --as-of 2026-06-30 ciclo` (desde `bloque_a/11_Ejecutor`) y, sobre la misma carpeta, `comprobar_datos_a.py <copia> --as-of 2026-06-30` | el ciclo **usa** `EURUSD=X` (está en F3 y no hay incidencia de HT-01 para él); el script lo da **INVALIDO** («1 cierres no numéricos… 2022-06-01='n/d'») y 56 de 57 |
| Suite, goldens, gates y cuotas | comunes a T-131, T-133 y T-134 (ver «Comunes» abajo) | ver allí |

### Las dos explicaciones del implementador

- **«Fechas duplicadas» da OK con razón: verificado.** El caso de r01_01 repite las tres últimas filas de `XLK.csv` (2026-10-28 a 2026-10-30) con as_of 2024-03-29: son posteriores a as_of, `serie()` no las devuelve y el ciclo tampoco las ve (`cierres` y `valor_en` del ciclo las aceptan). Con as_of 2026-10-30 las mismas filas dan INVALIDO (`r02_01` [1a]). El «fallo» es de mi predecesor, no del script.
- **«Cada dato de por_contrato en su fila» falla por cómo busca r01_02: verificado.** El script busca `str(x)[:40]` de un diccionario, es decir `{'clase': 'MensajeInvalido', 'motivo': "C…`, que nunca estará en una tabla Markdown. Las filas de CT-11, CT-12 y CT-13 llevan la clase y el motivo literal («CT-11: faltan campos mínimos ['piezas']»…) (`r02_01` [1b]). La propia r01 ya lo llamaba «falsos avisos de mi script».

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | 57/57 OK; falta (sin archivo, solo cabecera, todo posterior a as_of o sin publicar), inválido (lectura, columnas, zona, fechas imposibles, cierres de texto, cero, negativos y fechas repetidas en el rango) y antiguo (as_of 2027, H1 en sesiones) se distinguen; `Date`/`Close` con BOM, OK. Pero el script es más estricto que el ciclo con lo anterior a la ventana del lote (H-05) |
| CA-2 | sí | `--comprobar` coincide; 23 de 23 contratos con fila; sin mensajes de jsonschema sin traducir; los siete puntos de H-02 de la r01 (`query_id` de CT-03, `run_id` de CT-23, el tipo de `escalado`, `fecha_corte` de CT-09, retornos internos con `ESQUEMAS`, lo que el Anexo B deja abierto y los campos de cada elemento de los lotes) están. Ver H-06 para CT-09 y CT-10 |
| CA-3 | sí, salvo el gate entero (no lanzado por instrucción) | `test_t131_preparativos.py` (12 pruebas) dentro de la suite completa: 6048 passed |

## Hallazgos de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 (alta) | **corregido** | `r01_01` [1]: cierre `n/d`, cero y negativo → INVALIDO con el motivo de HT-01; fechas repetidas dentro del rango → INVALIDO (`r02_01` [1a] y la prueba nueva) |
| H-02 (media) | **corregido** | `r01_02` [2] 44/44; el §1 y las filas nuevas del §2 recogen lo que faltaba (ver CA-2) |
| H-03 (baja) | **corregido** | `r01_01` [2]: H1 del viernes 22-03-2024 al lunes 25-03-2024 → OK (1 sesión, como `_sesiones_entre` con `ps2_festivos`) |
| H-04 (baja) | **corregido** | `r01_01` [3]: `/no/existe` → código 2 y «no existe la carpeta de datos /no/existe», sin traza |

## Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-05 | media | `r02_01` [2]; y el ciclo real de la tabla de reproducción | **Esperado** (`analisis-tecnico.md` r02: «usa `cierres()`, el que usa el ciclo… Un dato malo posterior a as_of no cuenta, como en el ciclo»; README: dice si la carpeta sirve). **Obtenido:** el script llama a `prov.cierres(simbolo)` **sin inicio**, así que valida toda la historia hasta as_of; el ciclo solo valida la ventana del lote (`senales_clase`: `senales.ventana_anios` + `margen_dias` hasta as_of; la referencia, `tasa_base.ventana_anios`; `valor_en`, solo el último cierre), y lo de fuera no cuenta (T-65, QA r03, H-21). Un cierre `n/d`, a cero o una fecha repetida en 2022 con as_of 2026-06-30 (ventana desde 2023-05-31) da **INVALIDO** en el script y el ciclo usa el símbolo. Con un proveedor real de 10 a 20 años de historia, los ceros o huecos antiguos son corrientes: el script diría que no sirven símbolos que el ciclo usa. Falla cerrado (no da OK a lo que el ciclo rechaza), por eso no es alta | Validar con `prov.cierres(simbolo, inicio, as_of)` con el inicio más antiguo que usa el ciclo (`min(ini, ini_ref)` de `senales_clase`, de la configuración), y si se quiere seguir avisando de lo antiguo, un estado o una nota aparte («dato malo fuera de la ventana del ciclo: no cuenta»); prueba con un cierre malo antes de la ventana | abierto |
| H-06 | baja | `r02_01` [4]; lectura de `borrador_anexo_b.py` | **Esperado:** el borrador describe lo que hace el ejecutor. **Obtenido:** (a) para CT-09.RETORNO y CT-10.RETORNO propone «describir los campos del esquema de `ESQUEMAS` de ese agente», pero esos retornos no son de un agente: los sirve el Motor (`motor/servicio.py`, `servir` y `reejecutar`) y no pasan por `_invocar` ni tienen esquema en `ESQUEMAS` (los otros siete, CT-06/07/08/11/12/13/14, sí). Lo que pasa de verdad: en un retorno con resultado, el Motor emite `artefacto_id`, `resultado`, `clase_cifra` e `informe_calidad_datos` (no `incertidumbre`, que va al Registro de cálculos) y CT-10 emite `coincide`, `diferencias` y `diagnostico`; en un rechazo, no. La frase viene de INC-T114-01 («la respuesta de cada agente se valida con `ESQUEMAS`»), que tiene el mismo matiz. (b) El texto de la fila de tipo está fijo en el generador («el ejecutor envía null cuando no aplica») para cualquier mensaje «type» del golden: hoy solo hay uno (`escalado` de CT-03) y es cierto, pero un golden nuevo con otro tipo saldría con una explicación falsa sin que `--comprobar` lo note (`--comprobar` solo compara con lo generado) | (a) Para CT-09 y CT-10, otra propuesta: «describir los campos del artefacto del Motor (los de `servir`/`reejecutar`)», y matizarlo en INC-T114-01; (b) sacar la explicación del tipo de una tabla por campo, y que el generador falle si encuentra un mensaje «type» o «enum» que no está en ella | abierto |

Observación sin gravedad: `comprobar_datos_a.py … --as-of 2024-02-30` termina con código 1 y la traza de `DateParseError` (la H-04 de la r01 era la carpeta; un as_of mal escrito es lo mismo).

Los scripts de ataque están en `revisores/` (`r02_01_ventana_del_ciclo_y_borrador.py`; los de la r01, sin tocar).

## Invariantes

- No cambia el ejecutor ni el corpus: el borrador queda en `.docs/diseno/` y dice que no se aplica; corpus íntegro (695). ✔
- Falla cerrado: sí. El script ya no da OK a nada que el ciclo rechace; ahora peca de lo contrario con lo anterior a la ventana (H-05). ✔
- Números a mano: el umbral sale de `ps2_antiguedad_maxima_dias` y los festivos de `ps2_festivos`. ✔ (la corrección de H-05 debe sacar la ventana de `senales` y `tasa_base`, no escribirla)
- Decisiones del operador: ninguna tomada; el borrador deja abiertas CT-22 y las listas cerradas. ✔
- Secretos y datos personales: ninguno; `tools/secrets_scan.py` en verde con mis scripts. ✔
- Documentación: README, análisis y pruebas al día con la r02. ✔

## Comunes (T-131 r02, T-133 r01 y T-134 r01, copia en `197aaca`)

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite completa de A, una vez | `cd bloque_a/11_Ejecutor && py -m pytest -q -p no:cacheprovider` | **6048 passed** en 25 min 18 s (línea base 607) |
| Goldens de contratos | `py tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff (tres `11_Ejecutor`, desde la raíz) | `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | **2838** (cuota 2838) |
| mypy de A, como el gate | `cd bloque_a/11_Ejecutor && mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l` | **109** (cuota 109) |
| Gates ligeros | `tools/secrets_scan.py`, `tools/refs_vivas.py`, `tools/nfc_check.py`, `tools/corpus_integridad.py` | los cuatro en verde (corpus: 695 archivos coinciden) |

No lancé `./tools/check_all.sh`, ni A-Forex ni B (encargo).

## Veredicto (r02)

**APTO** · Los cuatro hallazgos de la r01 están corregidos (H-01, el alto, con la validación de `cierres()` y sus pruebas) y las dos explicaciones del implementador son ciertas: los dos «fallos» que quedan en `r01_01` y `r01_02` son de los scripts de la r01, no del código. Los tres criterios se cumplen (CA-3 sin el gate entero). Quedan **H-05 (media)**: el script valida toda la historia y el ciclo solo su ventana, así que da INVALIDO a símbolos que el ciclo usa (falla cerrado; comprobado con un ciclo real); y **H-06 (baja)**: para CT-09 y CT-10 el borrador remite a un esquema de `ESQUEMAS` que no existe, y una explicación fija en el generador. Sin críticos ni altos abiertos: H-05 y H-06 pasan a la deuda técnica con su ID (o se corrigen antes de cerrar; H-05 es pasar el inicio de la ventana a `cierres()`). El cierre (estado, deuda, diario, memoria y commit) queda para quien coordina: este revisor solo escribe en `qa.md` y `revisores/`.
