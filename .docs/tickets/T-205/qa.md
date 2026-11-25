# T-205 · QA independiente

- **Revisor:** claude, en una sesión que no implementó T-205 (subagente de QA, sin el contexto de la implementación) · **Ronda:** r01 · 25-11-2026
- **Base:** `origin/develop` 358576c3 (con T-201). **Revisado:** `wip/t205` 41fcc0bf, en un worktree propio (la copia del implementador no se tocó).

## Reproducción desde limpio

- **Worktree propio** de `wip/t205` y otro de 358576c3. El `.venv` del proyecto, enlazado.
- **Pruebas del ticket y de `b_agente` de T-201:** `pytest tests/test_t205_clase_seguimiento.py tests/test_t201_cuotas.py` da 63 superadas.
- **Sin el cambio fallan:** se copiaron las pruebas nuevas al árbol de 358576c3, con `ClaseNoAdmitida = ValueError` y un `clase_admitida` de prueba solo para que se pudieran recoger. Fallan 23 de 25. Las 2 que pasan son de regresión y tienen que pasar igual: las doce clases buenas y la OPP- que no está en F3, que da `KeyError`.
- **Vecinas:** `test_fase3_goldens`, `test_fase4_huecos`, `test_t159_extremo_a_extremo`, `test_t174_pb61_revision_c2`, `test_t65_hallazgos`, `test_t65_qa_r01`, `test_t65_resto_t53`, `test_t87_controles`, `test_v51`, `test_v5` y `test_integracion` dan **411 superadas**.
- **Reproducción de la QA r01 de T-201** (`.docs/tickets/T-201/revisores/r06_b_agente.py`): las altas con «XYZ» y con `""` dan `ClaseNoAdmitida` con su INC-. La DIV de control sigue yendo al AG-05.
- **ruff** de `seguimiento.py` y `test_t201_cuotas.py`: los mismos 3 ISC004 que en develop, que ya estaban. `test_t205_clase_seguimiento.py` sale limpio.
- **Gate del implementador** (`./tools/check_all.sh`, log en el scratchpad, `gate_t205.log`): **12/12 en verde**.
  - ruff 2797 ≤ 2797 y mypy de A 67 ≤ 67.
  - pytest A 8569, A-Forex 68 y B 176.
  - Corpus íntegro (705 archivos).
  - No se relanzó, por la carga de la máquina (orden del coordinador).

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_b_agente_falla_…` (7 casos) y `test_b_agente_da_el_analista_…`. En `r01_02` A1, `clase_admitida` también rechaza `["RV"]`, `{"RV": 1}`, `True`, `0.0`, `"RV\n"`, `"RV​"` y `"ＲＶ"` |
| CA-2 | sí | Pruebas del alta. En `r01_02` A1, con 11 valores hostiles solo cambian HA, los contadores y los sellos; no sale ningún mensaje y queda un INC-. En A12, un `opp_id` que no es una cadena da `TypeError` sin escribir nada. El caso de un fallo al escribir el INC- del alta no tiene prueba: es H-02 |
| CA-3 | sí | `test_c6_salta_…` (con un gemelo), `test_c6_de_un_encargo_cuya_opp_no_esta_en_f3_…` y `test_c6_forzado_…`. `r01_02`: en A9, un F11 manipulado con otra clase no cambia nada, porque manda F3; en A11, una OPP- que no está en F3 deja un solo INC- en cuatro días. Lo que no tiene prueba es el orden frente a la absorción en C1: es H-01 |
| CA-4 | sí | `test_c6_una_sola_incidencia_…`, `test_c6_un_inc_de_otra_fase_…` y `test_c6_varios_procesos_…`. `r01_02`: en A3, 30 días vencido dejan un solo INC- y F11 no avanza; tampoco abren otro MODIFICACION, PAUSA ni REANUDACION. En A5, corregida, absorbida en C1 y vuelta a estropear con el mismo valor abre otro INC-. En A8, dos encargos de la misma opción dejan dos INC- |
| CA-5 | sí (C6) | `test_c6_un_fallo_al_escribir_la_incidencia_…`. En `r01_02` A7, si falla a mitad de un C6 de tres encargos, el primero queda hecho y los otros dos intactos. Al reintentar, ninguno se repite y la integridad del almacén se mantiene. El alta, en H-02 |
| CA-6 | sí | Las pruebas nuevas fallan sin el cambio y el gate sale 12/12. Las cuotas no suben. El ciclo mock y el backtest dan lo mismo que en develop (abajo) |

### Ciclo mock y backtest (`revisores/r01_03_mock.sh`)

Se ejecutó en los dos árboles, con la salida en la **misma carpeta**, para poder comparar byte a byte. Pasos:
1. El backtest del README.
2. Un C1 a 2024-03-29.
3. `seguimiento alta` de OPP-2024-0001.
4. `seguimiento ejecutar` a 2024-04-05.

Los pasos 1 a 4 dan rc 0 en los dos árboles.
- Las salidas de los cuatro pasos y todo el estado tras el paso 4 son idénticos, F5 y F11 incluidos.
- `bt/` es idéntico salvo `consumo.csv`, en el que solo cambia `latencia_s`.
- `ent/` es idéntico.

Pasos extra: se pone una marca como clase en F3, se da de alta otra opción por la CLI y se ejecuta el C6 dos días seguidos.
- **En develop,** el alta se acepta, salen dos C6 BLOQUEADOS y la marca aparece en F5, F11 y los informes de `_bloqueados/`.
- **Con T-205,** el alta sale con rc 1 y `ClaseNoAdmitida`. El C6 se salta con el mismo INC- los dos días (`incidencia_nueva` true y luego false), y **la marca no aparece fuera de F3**.

## Lo que se pidió mirar

- **Quitar el respaldo de F11. No cambia nada en un encargo legítimo.**
  - `_alta` copia en F11 la clase de F3, y F3 es append-only, así que el respaldo solo actuaba si F3 perdía la opción o su clase pasaba a vacía o None. Eso solo pasa con un F3 manipulado o un almacén roto.
  - Aun así, el informe siempre tomó `tipo_activo` de F3, así que en esos casos salía BLOQUEADO.
  - Desde el primer commit del repo, las entradas de F3 que escribe C1 (`orquestacion.py`) llevan siempre `clase` y `tipo_activo`, con una clase de la selección. Son las ALTA y ACTUALIZACION de los candidatos y las ALTA de las exploratorias. Ninguna otra escritura de F3 lleva `clase`.
  - El ciclo mock con alta y C6 es idéntico al de develop.
- **Deduplicación.**
  - No se repite cada día: 30 días dejan un INC- (A3) y una OPP- que no está en F3, cuatro días, también uno (A11).
  - No falta ninguno en los casos que cambian el episodio: otra escritura de la clase, un ciclo hecho entre medias, una absorción en C1 seguida de otra rotura (A5) y otro encargo (A8).
  - MODIFICACION, PAUSA y REANUDACION no abren otro, lo que es coherente con «mientras siga igual».
  - C1 no reescribe la clase de una opción con la clase estropeada. `vigentes` y `_opp_id` filtran por `clase`, así que la clave tampoco cambia sola en cada C1.
- **Límite de las fichas que solo llevan `tipo_activo`.**
  - Está declarado con honestidad y es anterior a T-205. Además afecta a todo el ejecutor, no solo al seguimiento: `orquestacion.py` lee `v["clase"]` en el arrastre, y `vigentes` y `_opp_id` filtran por `clase`.
  - T-205 no lo empeora. Antes, una ficha así iba al AG-03 sin aviso y su informe salía BLOQUEADO; ahora el alta se rechaza con un INC-.
  - Leer `tipo_activo`, el nombre canónico del esquema de F3 V3.0, sería un cambio de todo el ejecutor. No cabe en este ticket y no es un hallazgo de T-205. Queda como observación para el coordinador.
- **Nada a medias.**
  - Alta: con HA rota, sube el error de HA y solo cambia el contador de INC- (A6).
  - C6: si falla a mitad, el estado queda coherente y se puede reintentar (A7).
- **El valor de la clase no sale en ningún sitio.** Con una marca como clase, no aparece en HA, F5, F11, mensajes, resultados, el texto de la excepción ni los entregables, ni por la API (A1 y A2) ni por la CLI.
- **T-201 no se debilita.**
  - El cambio de `test_t201_cuotas.py` mantiene los seis casos. Las tres clases buenas siguen comprobando su Analista. None, «XYZ» y `""` pasan a esperar `ClaseNoAdmitida`, como manda la decisión 1, que es más estricta.
  - El nombre de la prueba sí dice ahora lo contrario de lo que comprueba (H-03).

## Mutantes

- **Del implementador** (`mutantes.py`): 22 de 22 muertos en esta copia.
- **Propios** (`revisores/r01_mutantes.py`): 9 de 11 muertos.

Mueren:
- Q3: la comprobación por verdad.
- Q4: la clase de F11.
- Q5: el valor en el detalle del C6.
- Q6: un cerrojo solo entre hilos.
- Q7: la primera entrada de F3.
- Q8: las mayúsculas.
- Q9: que F11 avance al omitir.
- Q10: el INC- del alta sin `opp_id`.
- Q11: la lectura de HA fuera de la transacción.

Quedan **vivos Q1 y Q2**, que no son equivalentes: son H-01 y H-02. `revisores/r01_04_testigo.py` comprueba que los ataques A4 y A6 los detectan, así que sirven de modelo para las pruebas de regresión.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | Mutante Q1 (`r01_mutantes.py`): pasar la absorción en C1 antes de la comprobación de la clase. Las 25 pruebas siguen pasando | El README (Diseño, «Orden en el C6») e INC-T205-01 deciden que una opción VIGENTE con la clase estropeada no se omite «cubierta en C1». Con el mutante, se escribe CICLO_OMITIDO, F11 avanza y no queda INC-, y ninguna prueba lo ve (ninguna opción de las pruebas está VIGENTE) | Añadir a `test_t205_clase_seguimiento.py` una prueba, por ejemplo `test_c6_una_opcion_vigente_con_clase_no_admitida_no_se_omite_cubierta_en_c1`. Una entrada de F3 con `clase` «XYZ» y `estado` VIGENTE debe dar `ejecutado` False, `inc_id`, ningún CICLO_OMITIDO y F11 igual (modelo: `r01_02` A4). Añadir Q1 a `mutantes.py` | corregido (ronda de cierre, ea1d19c5) |
| H-02 | baja | Mutante Q2: si `almacen.incidencia` falla en el alta, `_exigir_clase_alta` vuelve sin rechazar y el alta sigue. Las 25 pruebas siguen pasando | CA-5 («si falla la escritura del INC-, no cambia ningún fichero del estado y no sale ningún mensaje») solo se prueba en el C6. Con el mutante, un HA roto deja dar de alta, en F11, un encargo con la clase estropeada y sin INC- | Añadir una prueba del alta con `almacen.incidencia` (o la escritura de HA) rota. El error de HA debe subir, no `ClaseNoAdmitida` ni un acuse. Solo puede cambiar el contador de INC-, y no deben salir mensajes, F11, F3 ni F5 (modelo: `r01_02` A6). Añadir Q2 a `mutantes.py` | corregido (ronda de cierre, ea1d19c5) |
| H-03 | baja | `tests/test_t201_cuotas.py::test_b_agente_conserva_el_analista_por_defecto` | Con T-205, la prueba comprueba lo contrario de lo que dice su nombre: que None, «XYZ» y `""` ya **no** van al Analista por defecto. Además, la observación de INC-T201-01 en `docs/incidencias.md` («queda propuesto para un ticket aparte») no dice que T-205 la corrige | Renombrar la prueba, por ejemplo a `test_b_agente_da_el_analista_de_su_clase_o_falla`, y actualizar las referencias en `mutantes.py` (PRUEBAS), `pruebas.md`, `analisis-tecnico.md` y `handoff.md` de T-205. Añadir a esa observación de INC-T201-01: «Lo corrige T-205 (INC-T205-01)». Regresión: la prueba renombrada pasa y `mutantes.py` sigue matando M1 a M3 con ella | corregido (ronda de cierre, ea1d19c5) |

### Observaciones (no son hallazgos)

- Las cuotas no suben, aunque tampoco bajan. Los 3 ISC004 de `seguimiento.py` ya estaban y el criterio del encargo es que no suban.
- El límite de `tipo_activo` es de todo el ejecutor (arriba). Si el operador quiere que se lea el nombre canónico del esquema de F3 V3.0, tiene que ser un ticket del ejecutor entero, no del seguimiento.

## Scripts del revisor (`revisores/`)

- `r01_02_ataques.py`: 29 ataques (A1 a A12). Con T-205, todos PASA. Se ejecuta con `python -I … <carpeta temporal>`.
- `r01_03_mock.sh`: backtest, C1, alta y C6 por la CLI, en la misma carpeta de salida para comparar dos árboles; con pasos extra de clase estropeada.
- `r01_mutantes.py`: 11 mutantes propios (Q1 a Q11).
- `r01_04_testigo.py`: comprueba que A4 y A6 detectan Q1 y Q2.

## Veredicto

**APTO pendiente de la ronda de cierre.** Hay tres hallazgos bajos (H-01, H-02 y H-03) y ninguno alto ni medio. Todos los criterios se cumplen. El comportamiento es correcto en todos los ataques. Tiene que corregirlos quien implementó, con sus pruebas de regresión. En la ronda de cierre, el revisor volverá a ejecutar `r01_mutantes.py` (Q1 y Q2 deben morir), `r01_02_ataques.py` y las pruebas.

## Ronda de cierre de la QA r01 (25-11-2026)

- **Revisado:** ea1d19c5, encima de 41fcc0bf, en el mismo worktree. El commit lleva mi `qa.md` y mis `revisores/` de la r01 sin cambios: los comparé byte a byte con mi copia guardada.
- **`seguimiento.py` no cambia** entre 41fcc0bf y ea1d19c5. El diff solo toca las pruebas, `mutantes.py` y la documentación.

### Correcciones

| Hallazgo | Verificación | Resultado |
| --- | --- | --- |
| H-01 | `test_c6_una_opcion_vigente_con_clase_no_admitida_no_se_omite_cubierta_en_c1`: F3 con «XYZ» y VIGENTE; exige el INC- de C6, ningún CICLO_OMITIDO, F11 igual y ningún mensaje | Q1 muere en `mutantes.py` y en `r01_mutantes.py`. Corregido |
| H-02 | `test_alta_con_ha_rota_sube_el_error_de_ha_y_solo_cambia_el_contador_de_inc`: escritura de HA rota; exige que suba el `OSError` y que solo cambie `contadores.json`, sin mensajes, encargo ni INC- | Q2 muere en los dos. Corregido |
| H-03 | La prueba de T-201 se llama ahora `test_b_agente_da_el_analista_de_su_clase_o_falla`, con los mismos seis casos. INC-T201-01 termina con «Lo corrige T-205 (INC-T205-01)». README, `pruebas.md`, `analisis-tecnico.md` y `mutantes.py` están al día | M1 a M3 siguen muriendo con ella. Corregido, salvo la frase de `handoff.md` de H-04 |
| Q11 | `test_c6_la_lectura_de_ha_y_el_inc_van_en_la_misma_transaccion`, determinista | Ver abajo. Mata Q11 siempre |

**La prueba de Q11, con la máquina cargada** (`revisores/rc_01_q11_carga.py`).
- La prueba usa un hilo con otra instancia del almacén. `flock` se toma por descripción de fichero abierto, así que la segunda instancia espera al cerrojo también dentro del mismo proceso.
- Con el código tal cual, el hilo no puede leer F11 ni HA hasta que se suelta el cerrojo, así que la prueba pasa sea cual sea la carga. El `join(timeout=2)` solo decide si el mutante llega a escribir antes. Por eso el riesgo no es un falso fallo sino que, con una carga extrema, el mutante sobreviva una vez.
- Medido con 6 procesos que queman CPU, además de los mutantes de las dos listas corriendo a la vez (carga media de 9,8 en 4 núcleos):
  - código tal cual: **15 de 15 pasan**;
  - mutante Q11: **15 de 15 mueren**.

### Regresiones

- **Pruebas:** `test_t205_clase_seguimiento.py` (28) y `test_t201_cuotas.py` dan 66 superadas.
- **Mutantes del implementador:** `mutantes.py` en una copia aparte, 25 de 25 muertos.
- **Mis mutantes:** `r01_mutantes.py`, con PRUEBAS cambiado al nombre nuevo (lo único que cambia en él), 11 de 11 muertos.
  - Le he añadido una comprobación previa: si las pruebas no pasan sin mutar, el script se para. Así no vuelve a «matar» mutantes sin ejecutar nada, como habría pasado con el nombre antiguo. Lo comprobé con el nombre antiguo: se para con rc 1.
  - Sin mutar, las pruebas de PRUEBAS dan 34 superadas, así que las muertes son de verdad.
- **Ataques:** `r01_02_ataques.py`, 29 PASA.
- **Cuotas y gates ligeros:** ruff del gate 2797 y mypy de A 67, como la cuota. ruff de las dos pruebas tocadas, limpio. Corpus íntegro (705), NFC, refs-vivas y secretos, en verde.
- **Gate completo:** no se relanza, por orden del coordinador. El código del paquete es el mismo que pasó 12/12; solo hay 3 pruebas más.

### Hallazgo nuevo

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-04 | baja | `.docs/tickets/T-205/handoff.md`, línea 26 (sección del 41fcc0bf) | Al cambiar el nombre en H-03, la frase quedó así: «La prueba de T-201 `test_b_agente_da_el_analista_de_su_clase_o_falla` cambia de expectativa… **El nombre de la prueba se conserva.**» Se contradice: el nombre ya no se conserva | Cambiar «El nombre de la prueba se conserva.» por «En la ronda de cierre se renombró (antes `test_b_agente_conserva_el_analista_por_defecto`; H-03 de la QA r01).». Regresión: `grep -n "se conserva" .docs/tickets/T-205/handoff.md` no devuelve nada | corregido (ab892812) |

### Observaciones (no son hallazgos)

- `.docs/tickets/T-201/pruebas.md` (línea 54) cita todavía el nombre antiguo. Es el registro de un ticket cerrado, que describe lo que había en T-201, y no se toca.
- El `mutantes.py` del implementador no comprueba que sus pruebas pasen sin mutar. Ahora sus PRUEBAS existen, y lo comprobé aparte (34 superadas), así que su 25 de 25 es real.

### Veredicto de la ronda de cierre

**APTO pendiente de H-04 (baja), que es una frase de `handoff.md`.** H-01, H-02 y H-03 están corregidos y verificados, y Q11 muere siempre, también con la máquina cargada. No hay ninguna regresión. Cuando se corrija H-04 lo compruebo con el `grep` de la tabla, sin otra ronda de pruebas, porque no toca código. Entonces será **APTO sin nada abierto**.

## Veredicto final (25-11-2026)

- **H-04, verificado en ab892812.** El commit solo cambia esa línea de `handoff.md`, con la frase propuesta. Además trae mis ficheros de la ronda de cierre, idénticos a mi copia. `grep -n "se conserva" .docs/tickets/T-205/handoff.md` no devuelve nada (rc 1).
- **Nada más cambia:** el código y las pruebas son los de ea1d19c5, ya verificados.

**APTO sin nada abierto.** H-01 a H-04 están corregidos y verificados.
