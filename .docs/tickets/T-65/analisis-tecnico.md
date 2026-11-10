# T-65 · Análisis técnico

## Causa raíz o motivo

La QA de T-53 (r01 y r02) dejó once hallazgos bajos en el Bloque A (H-06 a H-17, sin H-12, que se corrigió allí). La QA de T-66 dejó dos más (H-20 y H-21). La propia T-53 dejó un resto técnico: CA-14 resto, CA-15, CS-08, CS-10 resto, CS-11, CS-18, CS-19 y CS-23. Ninguno cambia una decisión del ciclo con los datos de hoy. Todos tienen la misma raíz: el código confiaba en su entrada o repetía números del YAML:

- **Estado global o compartido.** La tabla de bandas era global del módulo (H-07).
- **Literales de respaldo.** Muchos `.get(clave, literal)` repetían en el código los valores de `por_defecto.yaml` (H-08). Algunos ni coincidían: `ciclo_semanal_max` daba 160 en el código y 240 en el YAML.
- **Datos que no se validaban.** Cierres ≤ 0 (H-15), CSV mal formados, `ps2_festivos` (H-17), contenedores de F3 (H-20).
- **Registros que no contaban lo que pasó.** `estado_g3` en un paquete bloqueado y `fecha_efecto` de la degradación (H-10, H-13).
- **Declaraciones imprecisas.** Un motivo genérico para `DatosInvalidos` (H-10 c) y R9 sin `run_id` (H-21).

## Evidencia

- Hallazgos y scripts de reproducción de la QA en `.docs/tickets/T-53/qa.md` y `.docs/tickets/T-53/revisores/scripts_qa/`. Por ejemplo, `r2_06_fichas_rechazadas.py` reproduce H-15 y `r2_01_historia_parcial.py` reproduce H-16. En `.docs/tickets/T-66/qa.md`, H-20 y H-21.
- Cada corrección tiene una mutación que la quita y hace fallar su prueba: `python3 .docs/tickets/T-65/mutaciones.py` da 39 de 39 detectadas (resultado en `pruebas.md`).
- Al escribir la prueba de H-15 apareció un fallo más que la QA no vio. Un CSV con una fecha ilegible lanzaba un `ValueError`. El cribado ya lo excluía, pero la tasa base de la cesta (`Evaluador.tasa_base`, referencia `CESTA`) volvía a leer el símbolo y el ciclo entero caía. Se corrige en HT-01: un CSV mal formado (sin columnas o con fechas ilegibles) es `DatosInvalidos`.

## Implementación

**Archivos cambiados y por qué** (rutas bajo `bloque_a/11_Ejecutor/`):

| Archivo | Cambio | Puntos |
| --- | --- | --- |
| `bloque_a/configuracion.py` | `parametro(cfg, "a.b")` (configuración, si no `por_defecto.yaml`, si no `KeyError`; una clave nula también falla), `config_por_defecto()`, `sesiones_horizonte()` y `parametros_ht03()`. Se quita `ANTIGUEDAD_PS2`. Anotaciones al estilo actual (ruff baja) | H-08, CA-14, CS-11 |
| `bloque_a/evaluador.py` | Bandas en la instancia (`self.bandas`, `banda_de` y `banda_publicable` del Evaluador). `validar_bandas` sin efectos. Parámetros con `parametro()`; tasa base desde `tasa_base`; réplicas de la resolución desde `evaluacion`; recalibración de RK desde `evaluacion.recalibracion_rk` y `parametros_ht03`. `efecto_desde` = as_of | H-07, H-08, CA-14, CS-10, H-13 |
| `bloque_a/sintesis.py` | Bandas del Evaluador del bloque; umbrales del semáforo y del siguiente paso sin literales; sesiones desde `horizontes`; zona de interés y confianza desde `presentacion` | H-07, H-08, CA-14 |
| `bloque_a/orquestacion.py` | Exclusión y declaración de símbolos con datos inválidos o con cualquier error del proveedor (la fuga corta), con incidencia `DATOS` en HA. `validar_festivos_ps2` y lunes de Pascua. ML-CLUS-001 sin los proxies cortos y con la ventana de la configuración. PS1 y pregunta repetida desde la configuración. Rotación exploratoria configurable (también en la instrucción). `participantes` ordenados. Análisis paralelo dentro de `mensajeria.ambito(clase)`. Contenedor de objeciones mal formado como fuerte abierta. Contrarréplica que sanea solo lo externo, con `run_id` y una incidencia por fuente y run. `parametros_ht03` del YAML. P-30 sin «4.0» | H-08, H-10 c, H-15, H-16, H-17, H-20, H-21, CA-15, CS-10, CS-11, CS-18 |
| `bloque_a/contratos.py` | `Mensajeria.ambito()`: contador de `msg_id` propio del ámbito | CA-15 |
| `bloque_a/redaccion.py` | `carpeta_bloqueados()`; el paquete bloqueado pierde `estado_g3` también en memoria | H-10 a, b |
| `bloque_a/seguimiento.py` | Carpeta de bloqueados común; sin σ semanal, el delta es material y se declara; parámetros con `parametro()` | H-10 b, CA-14, H-08 |
| `bloque_a/herramientas/ht01_datos.py` | `cierres()` rechaza cierres ≤ 0 o no finitos; fechas duplicadas, columnas que faltan y fechas ilegibles son `DatosInvalidos` | H-15 |
| `bloque_a/motor/servicio.py` | `DOCUMENTADAS_CON_CODIGO` y `servible()`: las tres fichas «Documentado» se rechazan y no se ofrecen como alternativa | CS-08 |
| `bloque_a/almacen.py` | `PARAMETROS_SERVICIO` (más P-34, P-38 y P-44) y `PARAMETROS_CALIBRABLES` (más P-35, P-36, P-39 y P-40), según el esquema F10 V3.0 | CS-11 |
| `bloque_a/agentes.py`, `consumo.py`, `interfaz_broker.py`, `llm.py`, `backtest.py` | `.get(clave, literal)` → `parametro()` | H-08 |
| `bloque_a/herramientas/__init__.py` | Cita la prueba que existe | CS-23 |
| `config/por_defecto.yaml` | Marcas `[PROPUESTO]` con su INC y su pregunta. Secciones nuevas: `calendario`, `tasa_base`, `presentacion`, `senales`, `ps1`, `pregunta_repetida`, `redaccion` y `parametros_ht03`. Claves nuevas: `seleccion.rotacion_exploratoria_celdas`, `seguimiento.min_semanas_sigma`, `clusteres.min_semanas_proxy`, `ps2_festivos.lunes_de_pascua` y `evaluacion.recalibracion_rk`. `clusteres.ventana_semanas` pasa de 104 a 156 | H-08, H-09, CA-14, CS-10, CS-11, CS-18 |
| `tests/MAPA_PLAN_DE_PRUEBAS.md` | Rehecho contra el plan V3.0 (67 pruebas) | CS-19 |
| `README.md` (del ejecutor) | Limitaciones 3, 5 bis y 5 ter | CS-08, H-15, H-08 |
| `tests/test_t65_hallazgos.py`, `tests/test_t65_resto_t53.py` | Pruebas nuevas (40 y 24) | todos |
| `tests/test_t53_evaluacion_y_almacen.py` | `test_bandas_desde_configuracion_y_validadas` probaba el comportamiento global que corrige H-07; ahora prueba la tabla de la instancia | H-07 |
| `tests/test_t53_seleccion_y_entrega.py` | `test_h01_historia_corta_tambien_queda_declarada` esperaba «clústeres no calculados» para todos; con H-16 se declara solo el proxy corto | H-16 |

Fuera de `bloque_a/`:

- `tools/refs_vivas.py` (H-11). La excepción general de las carpetas `revisores/` desaparece. Una orden con argumentos cuenta por su script (`.sh` o `.py`). Se quita el sufijo de líneas. Una ruta del paquete Python de un bloque (`bloque_a/<módulo>.py`, dentro de `bloque_a/11_Ejecutor/`) cuenta como viva. El script se reorganiza en funciones (`comprobar`, `normalizar_cita`, `existe`). El encargo situaba el script en .docs/scripts/ (refs_vivas), pero está en `tools/`; se tocó porque el encargo autoriza arreglar ese script.
- `.docs/scripts/prueba_refs_vivas.py`: su prueba (6 casos en un repositorio de juguete).
- `.docs/tickets/T-65/mutaciones.py`: las 39 mutaciones.

**Decisiones tomadas y desviaciones del plan:**

- **`parametro()` cae en `por_defecto.yaml`** cuando una configuración parcial no trae la clave. Es el mismo patrón de `_valor_por_defecto` de T-66, ahora común. Lo que no está en ningún sitio, o está a `null`, falla. La CLI y `ejecutar_backtest` fusionan siempre sobre `por_defecto.yaml`, así que en producción la caída no se da.
- **Sesiones por horizonte.** No se derivan del calendario real, porque cambiarían H4 y H5 (252 → ~261). Se derivan de `horizontes` con dos constantes de convención en `calendario` (5 y 21), que dan exactamente los valores anteriores.
- **CS-18.** La ventana pasa a 156 semanas (Catálogo). Con los datos de ejemplo (desde enero de 2022) no cambió ninguna prueba.
- **H-16.** Un proxy corto queda en un clúster propio y no en el de otro. Su concentración no se ha medido y se declara; el run queda PARCIAL, como antes con el rechazo entero.
- **H-21.** Se tomó la primera opción de la QA (sanear solo lo externo). El origen de cada pieza decide: AG-13, los Analistas, AG-14 y AG-16 no se sanean otra vez. Una pieza sin origen, o con uno desconocido, se sanea, para fallar cerrado. El patrón R9 de `contratos.py` no se toca.
- **H-17.** `lunes_de_pascua` nace en `false`: es el comportamiento de hoy y el que más endurece PS2 en H1. Lo decide el operador en T-57.
- **CS-10, PS1.** El mínimo de raíces está en `ps1.raices_min`. No tiene prueba de efecto propia, porque las raíces HT-01 son primarias de nivel A y PS1 se supera igual. La prueba `test_cs10_todas_las_claves_leidas_existen_en_por_defecto` asegura que todas las claves leídas existen.
- **Cuotas.** ruff de los tres ejecutores baja de 3102 a 3083 (cuota 3109). mypy de A se queda en 123 (cuota 123). `tools/cuotas.txt` no se toca; puede bajarse a 3083 en el commit.

**Límites conocidos:**

- **Literales que siguen en el código.** Quedan literales algorítmicos que no están en el YAML, por ejemplo:
  - `len(sem) > 10` y el margen `weeks=semanas + 2` de GC0;
  - el umbral de 0,6 de familias concordantes;
  - los parámetros de ficha que se pasan al Motor (`ventana: 20`, `ventana_semanas: 26`).

  H-08 trataba los valores del YAML repetidos en el código; estos otros van con la revisión de PA-06 y PA-07.
- **Orden de `cache_resultados.jsonl` (CA-15).** Sigue dependiendo de los hilos. Se busca por clave y su contenido coincide.
- **F10 publica 9 de los 44 parámetros (CS-11).** Va a T-83 y T-57.
- **P-07 (CS-10).** El 20 % del presupuesto de cribado sigue sin traducirse a celdas; va a T-57.
- **Prompt del Analizador (CS-18).** Sigue diciendo ρ ≥ 0,6; es una revisión del corpus con el operador.
- **Fuera del alcance de este ticket, para el coordinador:**
  - `docs/incidencias.md`: la decisión de INC-T53-02 ahora incluye `lunes_de_pascua`, y la de INC-T53-04 se aplica en el mismo ciclo (H-13).
  - La tabla de scripts de `.docs/README.md`: falta `prueba_refs_vivas.py`.
  - La trampa de `CLAUDE.md`: «17 tienen código» sigue siendo cierto, pero solo se sirven 14 (CS-08).

**Comandos exactos para probarlo** (desde la raíz del repositorio):

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider          # suite de A
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t65_hallazgos.py tests/test_t65_resto_t53.py
cd ../.. && python3 .docs/tickets/T-65/mutaciones.py        # 39 mutaciones: todas deben fallar
python3 .docs/scripts/prueba_refs_vivas.py                  # 6/6
python3 tools/refs_vivas.py
.docs/scripts/gate.sh --completo
```

## Correcciones de la QA r01 (NO APTO)

**Causa raíz de los medios:**

- **H-01.** La validación de cierres de H-15 se hacía en `cierres()` sobre todo el rango pedido, y `valor_en()` pedía la historia entera. Un cierre malo antiguo, fuera de la ventana del lote, dejaba sin precio a símbolos sanos. Después, el `except DatosNoDisponibles: pass` del precio en `senales_clase` lo tragaba en silencio: PS2 fallaba (edad 999) y el tipo quedaba sin opciones con el run COMPLETO.
- **H-02.** `pd.read_csv` estaba fuera de `_normalizar_df`. Un CSV vacío o binario lanzaba `EmptyDataError` o `ParserError`, que el cribado sí absorbía, pero la tasa base de la cesta, no.
- **H-03.** Una cita con forma de ruta a un log que no se sube.

**Cambios** (rutas bajo `bloque_a/11_Ejecutor/`):

| Archivo | Cambio | Hallazgo |
| --- | --- | --- |
| `bloque_a/herramientas/ht01_datos.py` | `_cierres_brutos` y `_validar_cierres`. `cierres()` valida el rango pedido; `valor_en()` valida solo el cierre que devuelve; `ultima_fecha()` no valida. La lectura del CSV, en un `try` que convierte cualquier error en `DatosInvalidos` | H-01, H-02 |
| `bloque_a/orquestacion.py` | En `senales_clase`, un precio ilegible excluye y declara el símbolo, y las incidencias `DATOS` se escriben al final con todos los inválidos. `RE_MM_DD` para «MM-DD» estricto. `_ps1()` extraída. ML-CLUS-001 elige los proxies por solape. Texto de GC0 y suelo de COMÚN desde la configuración | H-01, H-04, H-08, H-07, H-05 |
| `bloque_a/evaluador.py` | `_coma()` para la limitación de la tasa base; días de `NO_RESOLUBLE` desde la configuración | H-11, H-05 |
| `bloque_a/sintesis.py` | `regla_fallback` y la tasa base de los hitos H5 desde la configuración | H-05 |
| `bloque_a/seguimiento.py` | Frecuencias sin respaldo 7 (una frecuencia desconocida falla; una personalizada sin `cada_dias` usa la semanal) | H-05 |
| `bloque_a/motor/servicio.py` | `uc.motor_por_plan.<plan>` sin respaldo 0,02 | H-05 |
| `bloque_a/configuracion.py` | `max_tokens.por_defecto` sin respaldo 8000 | H-05 |
| `config/por_defecto.yaml` | `presupuesto_uc.fraccion_minima_comun: 0.1` (`[PROPUESTO]` técnico) | H-05 |
| `tests/test_t65_qa_r01.py` | 20 pruebas nuevas | todos |
| `tools/refs_vivas.py`, `.docs/scripts/prueba_refs_vivas.py` | `rutas_de_cita`: el script y cada argumento con forma de ruta. Dos casos nuevos en la prueba | H-06 |
| `docs/incidencias.md` | INC-T53-02 a 05 marcadas `[PROPUESTO]`; INC-T53-04 al día | H-09 |
| `.docs/tickets/T-65/mutaciones.py` | 11 mutaciones más (50 en total), incluidas las tres que la QA encontró sin detectar (pregunta repetida, recalibración de RK y PS1) | H-08 |

**Decisiones:**

- **H-01.** Se tomó la primera opción de la QA. Solo importa lo que se usa: la ventana del lote (en `senales_clase`) y el cierre que se devuelve (en `valor_en`). Sigue fallando cerrado si el cierre que se usa es malo.
- **H-07.** El orden de elección es determinista (más semanas, luego símbolo). Ante dos proxies sin solape, se queda el que tiene más semanas en común con los ya elegidos.

**Límites que siguen** (H-05):

- el redondeo de la probabilidad de Prospectiva a pasos de 0,05 y su recorte a [0,05; 0,95] (`orquestacion.py`, `_prospectiva`);
- los pesos de las familias de la señal compuesta y su umbral 0,6;
- los parámetros de ficha que se pasan al Motor.

Son reglas del algoritmo, no números de la configuración repetidos, y van con la revisión de PA-06 y PA-07.

**A la deuda técnica:**

- **H-10.** El consumo por tipo en F5 con hilos no es determinista, y ya no lo era antes de T-65. La fila la abre el coordinador.

**Comandos** (además de los de arriba):

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t65_qa_r01.py
../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r01_04_cierre_malo_antiguo.py   # HALLAZGOS: 0
../../.venv/bin/python ../../.docs/tickets/T-65/revisores/r01_01_datos_raros.py          # HALLAZGOS: 0
cd ../.. && python3 .docs/tickets/T-65/mutaciones.py r01                                  # 11/11
```
