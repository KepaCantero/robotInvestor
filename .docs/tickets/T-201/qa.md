# T-201 · QA

## Ronda r01 · 2026-11-24 · revisor: claude (sesión independiente, no implementó)

**Veredicto: NO APTO** (un hallazgo medio, H-01; tres bajos, H-02 a H-04).

Código revisado: `wip/t201` (`67a52fd0`) sobre `7f92064a` (`git merge-base wip/t201 origin/develop`; no es `6045913`), en un
worktree propio (`qa_t201`) y otro de la base (`qa_t201_base`). La copia del implementador no se tocó. Los mutantes se aplican a
copias del paquete en el scratchpad, nunca al árbol. Scripts y salidas en `revisores/` (r01 a r06). No hay caso del plan de pruebas
(el README lo dice y es correcto: T-201 es un ticket de cuotas sin PB-xx), así que la vara es el README (CA-1 a CA-6) y las reglas
comunes de los tickets de cuotas.

### Lo comprobado

| Qué | Cómo | Resultado |
| --- | --- | --- |
| Gate del implementador | `scratchpad/gate_t201.log` (sobre `67a52fd0`, copia limpia) | 12/12; ruff 2797/2797, mypy A 67/67, FX 174/174, B 159/159; A 8 472, FX 68, B 176 |
| Cuotas = lo que da el gate (punto 6) | órdenes del gate en mi worktree y en la base | ruff 2806 → **2797**, mypy A 102 → **67**; `tools/cuotas.txt` dice exactamente eso; FX y B sin tocar |
| Ningún error nuevo | salidas de mypy y ruff de base y T-201 comparadas sin números de línea | mypy: 35 líneas menos, 0 nuevas; ruff: 9 menos (3 I001 y 6 RUF100 de los envoltorios), 0 nuevas |
| Pruebas nuevas | `tests/test_t201_cuotas.py` en T-201 y copiado sobre la base | 35/35 en T-201; en la base fallan 13 (rama de mypy ×4, mensaje de `ruta`, `_estado_hito` ×8) y pasan 22, que son de equivalencia: lo esperado |
| Vecinas | `test_t201_cuotas`, `test_unitarias` (incluye `test_herramientas_de_referencia_sin_divergencia`), `test_t106/t112/t119/t135_motor`, `test_t53_evaluacion_y_almacen`, `test_t66_evaluacion`, `test_v51` | 369 pasadas |
| Ficheros prohibidos (punto 5) | `git diff --name-only` frente a la PR 3 de Astra (88 ficheros) y a `wip/t196`; `tools/corpus_manifest.txt`; `referencia/` | ningún fichero de código, prueba, configuración, corpus ni `referencia/`. Solo coinciden `docs/incidencias.md` y la deuda técnica, que son registros de solo añadir que todo ticket toca al final (no es hallazgo: el conflicto, si lo hay, es de añadir dos entradas) |
| Silenciadores y configuración (punto 4) | búsqueda en el diff | ningún `type: ignore`, `noqa`, `cast` ni `Any` nuevo (se quitan 7 `noqa`); el `Any` de `ht09.py` ya se importaba; ni pyproject ni opciones de ruff o mypy. Dos anotaciones con `dict` sin parámetros (`metricas: dict`, `ent: dict[str, dict]`) son un `Any` implícito, pero siguen la convención del paquete (`cfg: dict`, `-> dict`) y los errores que quitan eran de inferencia (`dict[str, object]`), no de datos: no tapan ningún fallo real |
| La rama `TYPE_CHECKING` (punto 1) | `r05_mypy_frente_a_ejecucion.py` (salidas `r05_salida_t201.txt`, `r05_salida_base.txt`) | mypy ve los 176 nombres públicos que existen en ejecución (0 «no attribute»; en la base, todos). Siete llamadas mal hechas a propósito (aridad, tipos, retorno) las señala mypy con T-201 y ninguna en la base: la rama no oculta errores, al contrario, los llamadores pasan a comprobarse contra la firma real, y no sale ningún error nuevo en ellos. Mismo fichero en las dos ramas, sin `__all__`: el `*` exporta lo mismo. Única asimetría, sin efecto: `os` (del `except ImportError` de la copia de HT-02) existe para mypy y no en ejecución, y `ht09.ht03`/`ht09.ht07` son `Any` para mypy; ningún código del paquete los usa |
| Identidad en ejecución | pruebas CA-3 y mutantes M17 a M19 | el módulo de `sys.modules` es el de siempre; importar por la ruta de paquete en ejecución lo matan las pruebas |
| Entradas hostiles (punto 2) | `r01_ataques.py` + `r01_sonda.py`: 180 casos con la base y con T-201 en procesos separados (`ruta` con 13 configuraciones; `b_agente` con None, «», minúsculas, 0, False, NaN, lista, dict…; `_cambio` con 8 `seg_id`; `_revision` con 15 hitos raros × 6 formas de `hit_ids`, F4 inyectado; `acierto_direccional` con 16 entradas, flotantes y NaN incluidos; `diferencial_rentabilidades` con 14 × 2; `Motor.servir` con 11 fichas raras) | 175 iguales (66 con la misma excepción y el mismo mensaje); 5 distintos, todos lo declarado: el mensaje del `TypeError` de `ruta` sin la clave (ver H-03). EQUIVALENTE salvo lo declarado |
| Equivalencia del implementador | `equivalencia.sh` reproducido (`r01_equivalencia_reproducida.txt`) | 89/89 ficheros, 62 idénticos en crudo, EQUIVALENTE |
| ¿Normaliza de más? (punto 3) | `r02_sensibilidad_equivalencia.py`: siete cambios a propósito en `r_nuevo` | el testigo sale DISTINTO; **seis cambios de dominio salen EQUIVALENTE** (H-01) |
| ¿Equivale de verdad? | `r03_comparar_estricto.py` (solo rutas, dos latencias, la columna de latencia de `consumo.csv` y los resúmenes encadenados) | EQUIVALENTE con la ejecución real y los siete cambios DISTINTO: la conclusión de T-201 se sostiene; lo que falla es la herramienta |
| Mutantes propios | `r04_mutantes.py` (18 + testigo M00), `r04_salida.txt` | 14 muertos; M10 y M11 equivalentes (motivo en el script); M16 y M01 vivos (H-02, H-03). En una primera pasada M01 «murió» por `test_fase3_goldens.py`, pero el testigo M00 (copia sin mutar) falla igual: dos de sus `test_ca7…` fallan en una copia del paquete sin mutar nada (una lee `docs/incidencias.md` y la deuda, de fuera de `bloque_a/`). Sin ese fichero, el testigo pasa y M01 vive |
| `b_agente` (punto 7) | `r06_b_agente.py` (salidas `r06_salida_t201.txt` = `r06_salida_base.txt`) | ver «Sobre `b_agente`» |

### H-01 · media · `comparar.py` enmascara valores de dominio e instantes: la prueba de equivalencia no ve cambios de comportamiento (CA-5)

- **Reproducir:** ejecutar `equivalencia.sh <copia> 7f92064a` y, sobre la carpeta que deja,
  `python revisores/r02_sensibilidad_equivalencia.py <carpeta> .docs/tickets/T-201/comparar.py <copia>/bloque_a`
  (`r02_salida_comparar.txt`).
- **Esperado:** la regla común de los tickets de cuotas: «idéntica a la de develop, byte a byte salvo rutas temporales y
  latencias». Un cambio en un dato de dominio tiene que dar DISTINTO.
- **Pasa:** dan EQUIVALENTE seis cambios de dominio: la dimensión T `duracion` de una opción en F3 (80 → 10, entrada de HT-03 y de la
  selección), `duracion_sesiones` de un cálculo del Motor en RC (237 → 1; el Motor es uno de los paquetes que toca T-201), la
  `fecha_congelacion` de un pronóstico en F4, una fecha con hora en F3, el `_ts` de F11 y el `timestamp` del acuse de la petición.
  Causas: `LATENCIAS` casa por nombre `duracion[a-z_]*`, `tiempo_[a-z_]*`, `t_[a-z_]+`, `W_[a-z0-9_]+`, `ts`, `creado`… (hoy casan 138
  `duracion` y 90 `duracion_sesiones`, que son datos); `INSTANTE` borra cualquier fecha con hora de cualquier fichero (más de 600 en F2,
  RC, F4, HA, F3…). Y ninguno de ellos difiere entre las dos ejecuciones: quitadas las rutas, lo único que cambia en crudo son
  `latencia_s`, la columna de latencia de `consumo.csv` y los `_hash`/sellos encadenados (comprobado fichero a fichero).
  La «sensibilidad» de `pruebas.md` (estado de F3 y `reintentos`) tocaba justo campos que no se enmascaran.
- **Corrección:** en `comparar.py`, `LATENCIAS` solo con `latencia_s` y `tiempo_respuesta_s`; quitar `INSTANTE` (las dos ejecuciones son
  simultáneas: el `_ts`/`_fecha` de F10, que lleva la fecha del reloj, coincide; si se quiere blindar contra la medianoche, enmascarar
  solo esos dos campos de F10); conservar rutas, `LATENCIA_CSV` y `RESUMEN`. Es lo que hace `revisores/r03_comparar_estricto.py`
  (`r03_salida.txt`: EQUIVALENTE con la ejecución real). Corregir en `pruebas.md` y `handoff.md` la lista de lo que se normaliza.
- **Prueba de regresión:** `r02_sensibilidad_equivalencia.py` contra el `comparar.py` corregido: «puntos ciegos: ninguno»
  (`r02_salida_comparar_estricto.txt`), y `equivalencia.sh` sigue dando EQUIVALENTE. Mejor aún, que `equivalencia.sh` lance él mismo el
  testigo de sensibilidad tras comparar, para que no vuelva a pasar en T-202 y T-203 si reutilizan el script.

### H-02 · baja · Vive un mutante de `acierto_direccional`: la prueba no distingue el array convertido de la secuencia original

- **Reproducir:** `python revisores/r04_mutantes.py <copia>/bloque_a <tmp> M16`: `int(arr.sum())` → `int(sum(o))` pasa las 35 pruebas.
- **Esperado:** el renombrado `o` → `arr` es justo donde se puede volver a usar la variable equivocada; la prueba del cambio no mecánico
  tiene que matarlo (regla del encargo: mutante vivo no equivalente = hallazgo).
- **Pasa:** `test_acierto_direccional_con_lista_y_con_array` solo usa enteros 0/1, donde las dos expresiones coinciden. No es equivalente:
  con `[1.7, 1.7, 0.2]` la base y T-201 dan `aciertos` 2 (`asarray(dtype=int)` trunca; `r01` lo confirma igual en las dos) y el mutante 3.
- **Corrección:** añadir a esa prueba `assert evaluacion.acierto_direccional([1.7, 1.7, 0.2])["aciertos"] == 2` (y `n == 3`).
- **Prueba de regresión:** M16 muere.

### H-03 · baja · `ruta`: el límite «valor vacío» no tiene prueba y el mensaje nuevo dice «no está» también cuando la clave está a null

- **Reproducir:** M01 de `r04_mutantes.py` (`if valor is None:` → `if not valor:`); `r01_sonda.py`, casos `ruta_4` y `ruta_5`.
- **Esperado:** CA-4 pide conservar el comportamiento con los casos raros, y el único cambio declarado es el mensaje cuando falta la clave.
  `ruta({"rutas": {"x": ""}}, "x")` devuelve la raíz del paquete (`Path("")`), igual en base y T-201, y `rutas.x: 0` sigue dando el
  `TypeError` de `Path`; ninguna de las dos cosas está fijada.
- **Pasa:** M01 vive: 142 pruebas pasan (`test_t201_cuotas`, `test_v51`, `test_fase4_huecos`, `test_t65_hallazgos`; el testigo M00 pasa
  las mismas). Además, con `rutas: {prompts: null}` en el YAML (clave presente, valor null) el mensaje dice «rutas.prompts no
  está en la configuración», que es inexacto.
- **Corrección:** mensaje «rutas.{clave} no está en la configuración o es null»; en `test_t201_cuotas.py`, casos `{"x": ""}` →
  `raiz_paquete(cfg)`, `{"x": 0}` → `TypeError` con el mensaje de `Path` (no el nuevo) y `{"x": None}` → el mensaje nuevo.
- **Prueba de regresión:** M01 muere con `tests/test_t201_cuotas.py` solo; la prueba de `{"x": None}` fija el texto.

### H-04 · baja · Las cifras de `referencia/` mezclan dos medidas de mypy

- **Reproducir:** `.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | grep referencia/ | grep -c "error:"`
  → 50 (HT-09 24, HT-02 13, HT-03 13) y 11 notas: las 61 líneas del gate. Sin `--ignore-missing-imports` salen 53 (HT-09 26, HT-02 14):
  los 3 `import-not-found`.
- **Esperado:** que la deuda que se declara «del corpus que no se puede bajar» esté contada como la cuenta el gate.
- **Pasa:** el README («Los 53 errores… (61 líneas de la salida que cuenta el gate…)» y «incluidos sus 3 `import-not-found`»),
  INC-T201-01 y la fila T-201 de la deuda dicen que esos 53, con los 3 `import-not-found`, son la deuda que queda en la cuota; en la medida
  del gate los `import-not-found` no existen y son 50. `analisis-tecnico.md` sí distingue bien las dos medidas.
- **Corrección:** en el README (Objetivo y «No entra»), INC-T201-01 y la fila de la deuda: «61 líneas del gate: 50 errores (HT-09 24,
  HT-02 13, HT-03 13) y 11 notas; sin `--ignore-missing-imports`, 53, por los 3 `import-not-found` de los imports entre copias, que el
  gate no cuenta». El «encargo inicial de 53» puede quedarse como cita, con esa aclaración.
- **Prueba de regresión:** la orden de arriba en `pruebas.md`, con su resultado (50 y 61).

### Sobre `b_agente` (punto 7 del encargo)

Es un defecto real, previo a T-201 y fuera de su alcance (un ticket de cuotas no cambia comportamientos), y merece un ticket propio de
gravedad baja. Ejemplo (`r06_b_agente.py`, igual en base y T-201): una opción de F3 con `clase` «XYZ» (o vacía) admite el alta del
seguimiento, porque `_alta` copia la clase de F3 sin comprobarla; su ciclo C6 registra `CT-06 AG-02 → AG-03` (el analista de renta
variable) con `clase: "XYZ"`, y un `CT-05` con `nivel_por_clase: {"XYZ": "N1"}` y su presupuesto, sin ninguna incidencia en HA. Solo lo
para después G3: el esquema del informe C6 rechaza `tipo_activo: 'XYZ'` y el informe sale BLOQUEADO, así que no se entrega nada. Daño
real: un mensaje atribuido al agente equivocado en el registro (R2) y un ciclo gastado, sin aviso. Solo se alcanza con un F3 que no
escribió el propio sistema (manipulado o migrado). Lo coherente con «falla cerrado»: rechazar el CT-24 ALTA (y el C6) de una opción cuya
clase no está en `AGENTE_CLASE`, con una INC en HA, y que `b_agente` no tenga valor por defecto.

### Para la ronda siguiente

Corregir H-01 a H-04 con sus pruebas. El revisor volverá a pasar `r01_ataques.py`, `r02_sensibilidad_equivalencia.py` (contra el
`comparar.py` corregido), `r04_mutantes.py` (M01, M16 y el resto), `r05_mypy_frente_a_ejecucion.py` y `equivalencia.sh`.

## Ronda r02 · 2026-11-25 · revisor: claude (el mismo de la r01)

**Veredicto: APTO.** Las correcciones de H-01 a H-04 están verificadas con mis scripts, no hay regresiones y no queda ningún hallazgo
abierto de ninguna gravedad.

Revisé `2ab43e36`, encima de `67a52fd0`, en mi worktree (`qa_t201`, con `git checkout --detach 2ab43e36`). El commit trae `qa.md` y
`revisores/` de la r01 sin ningún cambio: lo comparé byte a byte con mi copia de seguridad. Desde la r01 el código solo cambia en
`configuracion.py` (el mensaje de `ruta`) y en `tests/test_t201_cuotas.py` (3 pruebas nuevas y 1 aserción más). El resto es
`comparar.py`, `equivalencia.sh`, `sensibilidad.py` (nuevo) y documentos.

| Qué | Cómo | Resultado |
| --- | --- | --- |
| Gate r02 | `scratchpad/gate_t201_r02b.log` | 12/12; ruff 2797/2797, mypy A 67/67, FX 174, B 159; A 8 475 (r01: 8 472, más las 3 nuevas), FX 68, B 176 |
| Cuotas y errores | órdenes del gate en mi worktree | ruff 2797; mypy A 67, con las mismas líneas que en la r01 (comparadas sin números de línea); 50 errores en `referencia/`; ruff de los dos ficheros tocados limpio |
| Pruebas del ticket | `tests/test_t201_cuotas.py` | 38/38 |
| **H-01** | `equivalencia.sh <copia> 7f92064a` desde limpio (`r02r_equivalencia_y_sensibilidad.txt`); mi `r02_sensibilidad_equivalencia.py` contra el `comparar.py` nuevo (`r02r_sensibilidad_revisor.txt`); `r07_sensibilidad_extra.py` (nuevo, `r07_salida.txt`) | EQUIVALENTE, 89/89, 63 idénticos en crudo (la r02 de `pruebas.md` dice 62; varía con las latencias que coinciden por azar). `sensibilidad.py` da 9/9 DISTINTO y 3/3 EQUIVALENTE en las latencias enmascaradas. Mis 7 cambios dan DISTINTO. r07 comprueba lo que queda junto a lo enmascarado: el número de entradas de un sello, una huella de RC, la columna `uc` de `consumo.csv` y una clave «latencia» que no es ninguna de las dos dan DISTINTO; cambiar solo un resumen da EQUIVALENTE, que es lo previsto. Ya no queda ningún punto ciego. `equivalencia.sh` termina con 1 si falla el testigo, así que no se puede saltar en T-202 ni en T-203. **Cerrado** |
| **H-02** | `r04_mutantes.py` (`r02r_mutantes.txt`) | M16 muere en `test_acierto_direccional_con_lista_y_con_array`. **Cerrado** |
| **H-03** | `r04_mutantes.py` y lectura de las pruebas | M01 muere (`test_ruta_con_la_clave_vacia…`). Las tres pruebas fijan `""` (la raíz del paquete), `0` (el error de `Path`, no el nuevo) y null (el mensaje nuevo, anclado con `^…$`). El mensaje dice «… no está en la configuración o es null». **Cerrado** |
| **H-04** | README, INC-T201-01, fila de la deuda y `analisis-tecnico.md` | Todos dan las dos medidas: 61 líneas del gate (50 errores, HT-09 24, HT-02 13, HT-03 13, y 11 notas) y 53 sin `--ignore-missing-imports`. Comprobado con la orden del gate: 50. El «53» de `handoff.md` está en la sección de traspaso de la r01, con su fecha: es registro histórico. **Cerrado** |
| Regresiones: entradas hostiles | `r01_ataques.py`, base frente a r02 (`r02r_ataques_salida.txt`) | 180 casos: 175 iguales y 5 distintos, todos el mensaje declarado («… o es null») y con el mismo `TypeError` |
| Regresiones: mutantes | `r04_mutantes.py` completo, con el testigo M00 | el testigo pasa; 16 muertos (M01 a M09, M12 a M14 y M16 a M19); M10 y M11 equivalentes, con su motivo; ningún vivo |
| Regresiones: rama de mypy | `r05_mypy_frente_a_ejecucion.py` (`r02r_mypy_frente_a_ejecucion.txt`) | igual que en la r01: mypy ve los 176 nombres de ejecución y detecta las 7 llamadas mal hechas |
| Ficheros prohibidos | `git diff --name-only 67a52fd0 2ab43e36` | solo `configuracion.py`, la prueba del ticket, los documentos del ticket, `docs/incidencias.md` y la deuda; nada de la PR 3, de T-196, del corpus, de `referencia/` ni de la configuración de ruff o mypy; ningún `type: ignore`, `noqa`, `cast` ni `Any` nuevo |

**`b_agente`:** sin cambios, y así tiene que ser: es la observación de INC-T201-01, y la recomendación de la r01 sigue en pie (un ticket
propio, de gravedad baja, que rechace el ALTA y el C6 de una clase que no esté en `AGENTE_CLASE`, con una INC en HA).

**Siguiente paso:** cerrar el ticket (estado CERRADO, fila de la deuda, diario y commit en `develop`). Lo hace quien coordine la
integración; en esta ronda el revisor no hace commit.
