# T-91 · QA independiente

## Ronda r01

- **Revisor:** subagente nuevo de Claude, sin contexto de la implementación (regla del operador del 12-11-2026). Opinión formada con el README del ticket, la ronda r05 de T-65 y el código antes de leer `analisis-tecnico.md`.
- **Código revisado:** commit `7feb697` de `develop` (la ronda r02 de T-103, que va en el mismo commit, queda fuera de esta QA). Comparación con `7feb697^` en un worktree aparte.
- **Scripts:** `revisores/r01_01_resolucion_ataques.py` (partes A, H, C, O y B), `r01_02_mutantes.py` (con el motor `.docs/tickets/T-88/revisores/r01_mutar.py`) y `r01_03_compat_pronosticos.py`. Aceptan `--ejecutor RUTA`; se ejecutan con `.venv/bin/python -I`.

### Reproducción desde limpio

- Worktree limpio de `7feb697` con `PYTHONPATH` apuntando a sus tres ejecutores: `./tools/check_all.sh` completo **12/12** (A 737, A-Forex 68, B 176; ruff 2938, mypy A 109).
- `tests/test_t91_resolucion.py`: 10 pruebas, pasan.
- Scripts de la QA r05 de T-65 sobre la copia limpia:
  - `r05_01`, parte F: los 9 casos de festivos RESUELTOS. En la base, los 6 de Navidad y Pascua quedaban ABIERTO y luego NO_RESOLUBLE;
  - `r05_01`, parte X: el caso de punta a punta H4 se mide con proxy y referencia hasta el 2026-05-29. Los recuentos «13 de 96» de X son analíticos y no dependen del código;
  - `r05_01`, parte M: 20 «HALLAZGO» de la CESTA con un miembro parado. Son los mismos 20 en `7feb697^`: el script espera la regla de T-65 («el miembro que no sirve no cuenta») y T-92 (D02) la cambió por «si un miembro no sirve, la CESTA entera espera». No son de T-91;
  - `r05_02` (61 ciclos con series paradas y con huecos) y `r05_04`: 0 hallazgos.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r05_01 F` (arriba) y `test_h26_*`. `r01_01 A`: `_sesiones_entre` coincide con un cálculo propio (dateutil.easter) en 20.000 pares de fechas de 1999 a 2046 con tres juegos de festivos, y `motivo_no_fresca` sigue el calendario de PS2 en Navidad, fin de año y Pascua de 2025 a 2030. PS2 al emitir y la resolución usan la misma función |
| CA-2 | **no** | Con datos sin huecos, sí: `test_h27_*`, `r01_01 C` (miembro parado dentro de la tolerancia: todos los miembros y el proxy hasta su fecha) y `r01_01 O`. Pero con un hueco en la otra serie justo antes de la fecha común, proxy y referencia acaban en fechas distintas, y una de las dos con un dato más viejo que PS2 (H-01) |
| CA-3 | sí | `CRITERIO_RESOLUCION` y `REGLA_FALLBACK` en `sintesis.py`, y el README del ejecutor dice la regla. `r01_01 B`: en un backtest de 17 ciclos, los 169 PRG nuevos (60 hitos H5) congelan el criterio y la regla nuevos. `pronosticos.csv` lleva las dos fechas, coherentes con F4 (iguales en los 77 RELATIVO resueltos, vacías en los no resueltos). `r01_03`: las 30 columnas anteriores en su sitio y con los mismos valores que en `7feb697^`, fila a fila, en los 169 PRG; un lector por nombre de la versión anterior sigue funcionando. Ver H-03 (el ejemplo de salida no está al día) |
| CA-4 | **no** | (a) sí: N12 lo detecta `test_h29_a_…`. (b) y (c) no: los mutantes N1 y N2 sobreviven a la suite (H-02) |
| CA-5 | sí | Gate 12/12 desde limpio, sin subir cuotas |

### Mutantes (`r01_02_mutantes.py`, sobre otra copia)

Primero las pruebas del ticket (`test_t91_resolucion.py` y `test_t65_qa_r04.py`) y, si sobrevive, la suite entera (N1) o las suites de resolución y evaluación (`test_t65_qa_r03`, `test_t65_hallazgos`, `test_t65_resto_t53`, `test_t92_revision`, `test_t66_evaluacion`, `test_t53_evaluacion_y_almacen`, `test_unitarias`, `test_v51`, `test_integracion`, `test_t87_datos`, `test_t101_v6`; N2 a N13). Las copias se restauran con `git checkout` dentro del worktree.

| Mutante | Resultado |
| --- | --- |
| N1 H-29 (b): `fecha_dato` solo del proxy | **sobrevive a la suite entera** |
| N2 H-29 (c): la CESTA devuelve la fecha más reciente de sus miembros | **sobrevive** |
| N3 CESTA alineada a la fecha más reciente | detectado |
| N4 sin alinear los miembros de la CESTA | detectado |
| N5 sin alinear proxy y referencia | detectado |
| N6 proxy y referencia alineados a la más reciente | detectado |
| N7 H-26 vuelta atrás (H1 sin festivos) | detectado |
| N8 calendario sin el lunes de Pascua | detectado (`test_t65_hallazgos`) |
| N9 PRG antiguo de CESTA sin bases: no se congelan antes de alinear | **sobrevive** |
| N10 `pronosticos.csv` con la fecha del proxy como fecha de la referencia | detectado |
| N11 criterio congelado sin la regla de alineación | detectado |
| N12 H-29 (a): PS2 con la referencia ausente usa la fecha del proxy | detectado (`test_h29_a_…`) |
| N13 realineación del proxy con el nivel conocido en vez del congelado | detectado |

### Ataques sin hallazgo

- Festivos de varios años y bordes de PS2 en H1: `r01_01 A`.
- CESTA con un miembro parado (`r01_01 C`): dentro de la tolerancia se resuelve con todos los miembros hasta su fecha; parado en la emisión queda ABIERTO y, pasado el plazo, NO_RESOLUBLE; más allá de la tolerancia, ABIERTO; ya viejo al emitir, queda fuera de las bases congeladas y el PRG se resuelve.
- PRG antiguos (`r01_01 O`): una CESTA sin `bases_cesta` congeladas da el mismo resultado que con ellas. Una referencia con el nivel como número suelto, sin fecha, se alinea y resuelve.
- `pronosticos.csv` compatible: `r01_03`.
- Invariantes: no hay LLM en la resolución. Ningún número nuevo: se usan `ps2_antiguedad_maxima_dias` y `ps2_festivos`. Falla cerrado si una serie no tiene dato posterior a la emisión, salvo en H-01. INC-T91-01 está como `[PROPUESTO]`, con su pregunta para T-57, en `docs/incidencias.md`, y T-91 en la deuda. Nada de secretos ni datos personales.

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | alta | `r01_01_resolucion_ataques.py H` (y, como control, con `--ejecutor <worktree de 7feb697^>/bloque_a/11_Ejecutor`). PRG RV SPY frente a ACWI emitido el 2026-04-17:<br>– H2, resolución el 2026-05-01: ACWI parada el 04-29 (dentro de los 3 días) y SPY sin datos del 04-21 al 04-29;<br>– el mismo con los papeles cambiados;<br>– H4, resolución el 2026-07-17: ACWI parada el 06-26 (21 días) y SPY sin datos del 06-01 al 06-26;<br>– CESTA de DIV: un miembro parado el 04-29 y otro sin datos del 04-22 al 04-29 | **Esperado** (INC-T91-01 y README del ejecutor: cada serie con un dato no más antiguo que PS2 y, si acaban en fechas distintas, «todas se miden hasta la más antigua»; CA-2; README del ticket: «una serie que no sirve sigue dejando el pronóstico en espera»): RESUELTO con todas las series hasta la misma fecha y dentro de PS2, o en espera.<br>**Obtenido:** RESUELTO en los cuatro casos, con ventanas que siguen desalineadas y datos fuera de PS2:<br>– H2: proxy hasta el 04-20 y referencia hasta el 04-29: 11 días, con un máximo de 3;<br>– con los papeles cambiados: 04-29 y 04-21 (10 días);<br>– H4: proxy hasta el 05-29 y referencia hasta el 06-26: 49 días, con un máximo de 30;<br>– CESTA: todo hasta el 04-21, a 10 días de la resolución.<br>La segunda medida (`rentabilidad(…, f0, corte)` sin horizonte) solo exige un dato posterior a la emisión. Con un hueco, el último dato ≤ corte puede ser muy anterior, y no se vuelve a comprobar ni la fecha común ni la antigüedad frente a la fecha de resolución.<br>Es una regresión: `7feb697^` resolvía los cuatro casos con cada serie en su último dato, todos dentro de PS2 (edades 0 y 2, 2 y 0, 0 y 21). El resultado queda congelado en F4 (R11) y cuenta en las métricas y certificados. `analisis-tecnico.md` solo contempla el hueco «sin ningún dato entre la emisión y la fecha común» | Tras la segunda medida, exigir que todas las series acaben en la misma fecha. Si no, volver a medir hasta la nueva mínima, hasta que coincidan (como mucho, una vez por serie). Comprobar además la fecha común con `motivo_no_fresca(d0, común, f1, horizonte)` frente a la fecha de resolución original. Si no sirve, `DatosNoDisponibles` (espera y, pasado el plazo, NO_RESOLUBLE). Lo mismo dentro de la CESTA. Pruebas con estos cuatro casos | abierto |
| H-02 | baja | `r01_02_mutantes.py <copia> --solo=N1` (suite entera), `--solo=N2,N9` | **Esperado** (CA-4; H-29 de T-65: pruebas para (b) y (c) «que fijen `fecha_dato` y la fecha de la CESTA en la resolución»).<br>**Obtenido:** las pruebas citadas en `pruebas.md` no matan los mutantes:<br>– (b) N1: `test_h29_b_…` usa un DIRECCIONAL, donde `fecha_dato` ya es la del proxy, y en `test_h27_proxy…` las dos fechas coinciden tras alinear, así que max = proxy;<br>– (c) N2: en `test_h27_la_cesta…`, tras alinear todos los miembros acaban en la misma fecha, así que min = max.<br>Con la alineación, (b) y (c) solo se distinguen con un hueco, el caso de H-01. Tampoco hay prueba para la CESTA de un PRG antiguo sin bases congeladas (N9) | Al corregir H-01, añadir casos con huecos en los que la fecha de cada serie (o miembro) difiera, de modo que `fecha_dato` y la fecha de la CESTA queden fijadas, y un PRG de CESTA sin `bases_cesta` con un miembro ya viejo al emitir | abierto |
| H-03 | baja | `head -1 bloque_a/11_Ejecutor/ejemplos/salida_backtest_simulado/pronosticos.csv`; `grep -n -B2 ps2_antiguedad_maxima_dias bloque_a/11_Ejecutor/config/por_defecto.yaml` y el comentario de `evaluacion.dias_habiles_no_resoluble` | **Esperado** (H-28 de T-65: documentación al día; recomendación de H-27: la regla `[PROPUESTO]` también «junto a `ps2_antiguedad_maxima_dias`»).<br>**Obtenido:**<br>– El ejemplo de salida del README (`ejemplos/salida_backtest_simulado/pronosticos.csv`) sigue con las 30 columnas anteriores, mientras que el README y el código dan 32. El de `senales.csv` sí coincide con el código. El ejemplo no está en el corpus congelado;<br>– En `config/por_defecto.yaml`, ni el comentario de `ps2_antiguedad_maxima_dias` ni el de `evaluacion` citan INC-T91-01 ni la alineación hasta la fecha más antigua; siguen con el texto de T-65 | Regenerar el ejemplo de salida o, como mínimo, su cabecera. Añadir INC-T91-01 y la alineación al comentario de la configuración | abierto |
| H-04 | baja (anterior a T-91) | `r01_01_resolucion_ataques.py O`, último caso: PRG DIRECCIONAL con `nivel_referencia` como número suelto (registros anteriores a T-92) | **Esperado** (falla cerrado; el resto de `_rentabilidad_serie` admite el número suelto): se resuelve o espera.<br>**Obtenido:** `TypeError: 'float' object is not subscriptable` en `evaluador.py:405` (`fuga_ok = (pd.Timestamp(p["nivel_referencia"]["fecha"]) …`). La excepción sale de `resolver` y deja sin resolver todos los PRG pendientes de ese ciclo. Pasa igual en `7feb697^`, así que no lo introduce T-91; hoy no hay F4 reales | Tomar la fecha de la base devuelta por `_rentabilidad_serie` (`d0`) en lugar de leerla de `p["nivel_referencia"]`. Llevarlo a la deuda con este ID si no se corrige aquí | abierto |

### Veredicto

**NO APTO.** CA-2 y CA-4 no se cumplen:
- H-01 (alta): con un hueco en una serie justo antes de la fecha común, la alineación resuelve con ventanas aún desalineadas y con datos más viejos que PS2 (hasta 49 días en H4, con un máximo de 30). La base resolvía esos mismos casos dentro de PS2. El resultado queda congelado en F4;
- H-02: las mutaciones (b) y (c) de H-29 siguen vivas.

CA-1, CA-3 y CA-5 se cumplen: festivos de PS2 en H1 en varios años, criterio y regla congelados, `pronosticos.csv` compatible y gate 12/12.

Siguiente paso: `ri-implementar` para H-01 y H-02 (y H-03; H-04 es anterior y puede ir a la deuda con su ID). Después, el revisor vuelve a ejecutar `r01_01` (partes H, C, O), `r01_02` y `r01_03` en una ronda r02.

## Ronda r02

- **Revisor:** subagente nuevo de Claude, sin contexto de la implementación ni de la r01 (solo el plan, el código y los `qa.md`). Opinión formada con el README, el diff de `d1a5a1b` y el código antes de leer «Ronda r02» de `analisis-tecnico.md`.
- **Código revisado:** commit `d1a5a1b` de `develop` (la r01 se revisó en `7feb697`). Para no depender del árbol principal (otra sesión empezó a modificar `motor/servicio.py` durante esta QA, desde las 22:41 UTC), las comprobaciones finales se lanzaron contra un worktree limpio de `d1a5a1b`; los controles, contra worktrees de `7feb697` (r01) y `7feb697^`. Los worktrees se borraron al acabar. Durante la QA, `develop` avanzó hasta `5642ed0` (T-102 y T-106) sin tocar el código, las pruebas ni los documentos de T-88 y T-91.
- **Scripts nuevos:** `revisores/r02_01_frescura_y_alineacion.py` (escenarios al azar contra un oráculo propio), `r02_02_mutantes.py` (motor de `.docs/tickets/T-88/revisores/r01_mutar.py`) y `r02_03_desalineacion.py` (cuatro casos fijos de H-05). Aceptan `--ejecutor RUTA`; se ejecutan con `.venv/bin/python -I`.

### Reproducción desde limpio

- Worktree limpio de `d1a5a1b` con `.venv` enlazado y `PYTHONPATH` apuntando a sus tres ejecutores: `./tools/check_all.sh` completo **12/12** (A **740**, A-Forex 68, B 176; ruff 2938 de 2938, mypy A 109, FX 174, B 159; corpus, NFC, YAML, secretos y refs vivas en verde).
- `tests/test_t91_resolucion.py`: 13 pruebas (10 + 3 de la r02), pasan.
- Scripts de la r01, otra vez:
  - `r01_01 A H C O`: **15/15**. Los cuatro casos de H-01 (H2 con el hueco en el proxy, con los papeles cambiados, H4 y CESTA) quedan ahora en espera (ABIERTO); en `7feb697` se resolvían con datos de 10 a 49 días;
  - `r01_01 B`: 7/7 (169 PRG nuevos con el criterio y la regla nuevos; 77 RELATIVO con las dos fechas);
  - `r01_03 --base <7feb697^>`: 4/4. Las 30 columnas anteriores de `pronosticos.csv` en su sitio y con los mismos valores, y un lector por nombre sigue funcionando;
  - `r01_02 <copia>` (mutantes de la r01). Las pruebas del ticket detectan N1 a N7 y N10 a N12; N1 y N2, que en la r01 sobrevivían, ahora mueren. N8 lo detecta `r01_01 A` (en la r01, `test_t65_hallazgos`). N13 ya no se aplica porque la línea cambió; lo sustituyen Q2 a Q5 de `r02_02`.
  - N9 sobrevive a las suites relacionadas, aunque `analisis-tecnico.md` dice «mueren N1, N2 y N9». Es equivalente: sin bases congeladas, `bases_cesta(clase, f0, hz)` depende solo de la emisión y se recalcula igual en cada medida (`r01_01 O` da lo mismo con bases y sin ellas). Basta con corregir la frase.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `r01_01 A` (20.000 pares de fechas y bordes de PS2 de 2025 a 2030), `test_h26_*`. En `r02_01`, 92 escenarios H1 (en unos 3 de cada 10, sin los días de los festivos de PS2 en la serie; emisiones en Navidad de 2025 y Pascua de 2026): el código coincide con un oráculo que cuenta las sesiones sin `ps2_festivos` con un calendario propio (dateutil) |
| CA-2 | **no** | Sin huecos, sí: `test_h27_*` y `r01_01 C` (todas las series hasta la fecha de la parada). H-01 de la r01 está corregido en lo grave: en 400 escenarios al azar (paradas, huecos y festivos en el proxy, ACWI y los siete miembros de la CESTA de RV; H1 a H4) **ningún RESUELTO usa un dato sin dato posterior a su base ni más viejo que PS2** (`r02_01`, comprobación 1; contra `7feb697` la misma comprobación falla en 32 casos). Pero con un hueco o un festivo en la otra serie justo en la fecha común, las series siguen acabando en fechas distintas tras alinear, también con la referencia parada dentro de la tolerancia, que es el caso del criterio: H-05. La propia `test_r02_h02_b` lo da por bueno (SPY hasta el 04-28 y ACWI, parada, hasta el 04-29) |
| CA-3 | sí | `r01_01 B`; `CRITERIO_RESOLUCION` y `REGLA_FALLBACK` congelados en cada PRG nuevo, también en los hitos. H-03 de la r01 corregido: el ejemplo `ejemplos/salida_backtest_simulado/pronosticos.csv` tiene las 32 columnas del código (`COLUMNAS_PRONOSTICOS`), las 30 primeras idénticas fila a fila a las de `d1a5a1b^` y las dos nuevas vacías, como dice su LEEME. El comentario de `evaluacion` en `config/por_defecto.yaml` cita INC-T91-01 |
| CA-4 | sí | (a) N12 de la r01; (b) y (c) ahora con prueba: Q10 y Q11 de `r02_02` (los N1 y N2 de la r01) los detectan `test_r02_h02_b` y `test_r02_h02_c`. Ver H-06 para lo que la r02 añade sin prueba |
| CA-5 | sí | Gate 12/12 desde limpio, sin subir cuotas |

### Ataques

- **Oráculo propio** (`r02_01`, 400 escenarios, semilla 20261112). Emisión en cuatro fechas; PRG DIRECCIONAL, RELATIVO frente a ACWI o RELATIVO frente a la CESTA de RV; a cada serie, al azar, una parada, un hueco cerca de la fecha de resolución, los festivos de PS2 o festivos de otras bolsas. 212 RESUELTOS y 188 en espera (H1 31/61, H2 46/54, H3 65/59, H4 70/14). El código coincide en todos con un oráculo que lee los CSV y aplica la regla r02: estado, fecha del proxy, fecha de la referencia y exceso a 1e-8.
- **Control:** el mismo script contra `7feb697` (`--ejecutor`, 200 escenarios) encuentra 32 datos más viejos que PS2 y 5 resoluciones distintas del oráculo. El ataque sí distingue la r01 de la r02.
- **Casos fijos** (`r02_03`): cuatro casos de H-05, dos de ellos con calendarios naturales (Ascensión en el proxy; fin de año con los festivos de PS2).
- **PRG antiguos** (`r01_01 O`): una CESTA sin bases congeladas da lo mismo que con ellas, y un nivel guardado como número suelto en la referencia o en el proxy se resuelve sin `TypeError`. H-04 de la r01 está corregido.
- **Invariantes:**
  - no hay LLM en la resolución;
  - ningún número nuevo: se usan `ps2_antiguedad_maxima_dias` y `ps2_festivos`;
  - falla cerrado: una serie que no pasa la frescura frente a la fecha de resolución deja el PRG en espera, y pasado el plazo queda NO_RESOLUBLE (`r01_01 C`);
  - INC-T91-01 sigue como `[PROPUESTO]`, con su pregunta para T-57;
  - nada de secretos ni datos personales.

### Mutantes (`r02_02_mutantes.py`, sobre otra copia)

Primero `test_t91_resolucion.py` y `test_t65_qa_r04.py`. Si sobrevive, las suites relacionadas de la r01 (`test_t65_qa_r03`, `test_t65_hallazgos`, `test_t65_resto_t53`, `test_t92_revision`, `test_t66_evaluacion`, `test_t53_evaluacion_y_almacen`, `test_unitarias`, `test_v51`, `test_integracion`, `test_t87_datos`, `test_t101_v6`) y, después, los detectores propios (`r02_01 --n=80` y `r01_01 H O`).

| Mutante | Resultado |
| --- | --- |
| Q1 frescura frente a la fecha común y no frente a la de resolución | **sobrevive a las suites relacionadas**; lo detectan `r02_01` y `r01_01 H O` |
| Q2 el proxy se vuelve a medir sin horizonte | detectado (`test_r02_h01_…`) |
| Q3 la referencia se vuelve a medir sin horizonte | **sobrevive a las suites relacionadas**; lo detectan `r02_01` y `r01_01 H O` |
| Q4 el proxy no se vuelve a medir hasta la fecha común | detectado (`test_h27_proxy…`) |
| Q5 la referencia no se vuelve a medir hasta la fecha común | **sobrevive a las suites relacionadas**; lo detectan `r02_01` y `r01_01 H O` |
| Q6 la CESTA ignora el `hasta` de fuera en la primera pasada | **sobrevive a las suites relacionadas**; lo detecta `r02_01` |
| Q7 la CESTA se vuelve a medir sin horizonte | sobrevive a todo; es equivalente en `resolver`: la CESTA solo es referencia, y el proxy, medido hasta la fecha vieja de la CESTA, ya no pasa la frescura |
| Q8 solo se alinea si la referencia es la más antigua | **sobrevive a las suites relacionadas**; lo detectan `r02_01` y `r01_01 H O` |
| Q9 H-04 vuelta atrás (la fecha de la base, siempre del dict) | **sobrevive a las suites relacionadas**; lo detecta `r01_01 O` |
| Q10 H-02 (b): `fecha_dato` solo del proxy (N1 de la r01) | detectado (`test_r02_h02_b_…`) |
| Q11 H-02 (c): la CESTA devuelve la fecha más reciente (N2 de la r01) | detectado (`test_r02_h02_c_…`) |
| Q12 la serie se mide siempre hasta f1 (se ignora `hasta`) | detectado (`test_h27_proxy…`) |

Las pruebas nuevas cubren el caso del proxy con hueco, pero no la frescura frente a la fecha de resolución en general, ni la referencia, ni la CESTA (H-06).

### Estado de los hallazgos de la r01

| ID | Estado tras la r02 |
| --- | --- |
| H-01 (alta) | corregido en lo grave: ningún dato más viejo que PS2 (`r01_01 H` 4/4 en espera; `r02_01`, 0 de 212). Queda una parte: tras alinear, las series pueden seguir en fechas distintas (H-05) |
| H-02 (baja) | corregido: N1 y N2 (Q10 y Q11) mueren con las pruebas del ticket. N9 sobrevive, pero es equivalente (ver «Reproducción desde limpio») |
| H-03 (baja) | corregido (CA-3) |
| H-04 (baja) | corregido (`r01_01 O`), pero sin prueba (H-06, Q9) |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-05 | media | `r02_03_desalineacion.py` (cuatro casos fijos) y la parte informativa de `r02_01_frescura_y_alineacion.py` (también con `--ejecutor <worktree de d1a5a1b>`) | **Esperado** (CA-2: «proxy y referencia se miden hasta la misma fecha»; criterio que se congela en cada PRG y README del ejecutor: «si las series acaban en fechas distintas, todas se miden hasta la más antigua»; objetivo de H-27: el suceso sobre la misma ventana; H-01 de la r01: «RESUELTO con todas las series hasta la misma fecha y dentro de PS2, o en espera»).<br>**Obtenido:** la r02 vuelve a medir una sola vez hasta la fecha común. Si la otra serie no tiene dato ese día (un hueco o un festivo de su bolsa), se queda con el anterior y el PRG se resuelve con las series en fechas distintas, siempre dentro de PS2:<br>– caso 1, el de `test_r02_h02_b`, con ACWI parada dentro de la tolerancia (el caso de CA-2): SPY hasta el 04-28 y ACWI hasta el 04-29;<br>– caso 2, H3, Ascensión en el proxy y un dato que falta en la referencia: 05-13 y 05-12;<br>– caso 3, H2, fin de año con los festivos de PS2 en el proxy: 12-30 y 01-01;<br>– caso 4, H4 frente a la CESTA: SPY hasta el 07-02 y los siete miembros hasta el 06-22 (10 días de diferencia).<br>En `r02_01`, 8 de 212 RESUELTOS acaban así; repitiendo la alineación hasta que coincidan, los 8 quedarían alineados. La diferencia de ventanas puede llegar al límite de PS2 del horizonte (30 días en H4). La prueba nueva `test_r02_h02_b` fija la desalineación como correcta. Ni INC-T91-01 ni `analisis-tecnico.md` dicen que se acepte: es una decisión sobre la regla `[PROPUESTO]` que no está escrita | Repetir la alineación hasta que todas las series acaben en la misma fecha. Como mucho son tantas pasadas como series, porque la fecha común solo baja. En cada pasada, la frescura frente a la fecha de resolución; si en algún momento no sirve, en espera. Lo mismo dentro de la CESTA y entre el proxy y la CESTA. Cambiar `test_r02_h02_b` para que espere las dos series en el 04-28. Si se prefiere la regla actual, escribirla en INC-T91-01, en el criterio congelado y en el README («se miden con corte en la más antigua; con un hueco, cada una con su último dato anterior»), con su pregunta para T-57, y cambiar CA-2 | abierto |
| H-06 | baja | `r02_02_mutantes.py <copia>` (tabla de arriba) | **Esperado** (como H-02 de la r01 y H-29 de T-65): cada parte de la corrección, con una prueba que falle sin ella.<br>**Obtenido:** de los cuatro casos de H-01 de la r01, solo el primero (hueco en el proxy) tiene prueba. Sobreviven a las suites relacionadas:<br>– Q1: comprobar la frescura frente a la fecha común en vez de frente a la de resolución, que es el núcleo de la corrección;<br>– Q3: volver a medir la referencia sin horizonte, el caso «con los papeles cambiados» de H-01;<br>– Q5, Q6 y Q8: la alineación de la referencia y la de la CESTA;<br>– Q9: la corrección de H-04 de la r01 (nivel como número suelto).<br>Los detectan `r02_01` y `r01_01 H O`, salvo Q9, que solo detecta `r01_01 O`. Q7 (volver a medir la CESTA sin horizonte) es equivalente en `resolver`: la CESTA solo es referencia, y el proxy medido hasta esa fecha ya no pasa la frescura | Llevar a `test_t91_resolucion.py` los otros tres casos de H-01 de la r01 (papeles cambiados, H4 y CESTA), un caso en el que la frescura frente a la fecha común pase y frente a la de resolución no (mata Q1), y un PRG DIRECCIONAL con el nivel como número suelto (mata Q9) | abierto |

### Veredicto

**NO APTO.** CA-2 no se cumple: H-05 (media). Con la referencia parada dentro de la tolerancia y un hueco o un festivo en la otra serie en la fecha común, proxy y referencia se miden hasta fechas distintas, en contra del criterio congelado y de lo que pedía H-01 de la r01, y la prueba nueva lo da por bueno sin que la regla lo declare.

Lo grave de H-01 sí está corregido: en 400 escenarios al azar y en los cuatro casos de la r01, nada se resuelve con un dato más viejo que PS2. El control contra `7feb697` encuentra 32 casos. H-02, H-03 y H-04 de la r01 también están corregidos. CA-1, CA-3, CA-4 y CA-5 se cumplen.

Siguiente paso: `ri-implementar` para H-05, alineando de verdad o declarando la regla y cambiando CA-2, con las pruebas de H-06. Después, el revisor vuelve a ejecutar `r02_01`, `r02_02` y `r02_03` (y `r01_01 H C O`) en una ronda r03. Esta ronda solo escribe este archivo y los scripts `revisores/r02_*`: el estado del ticket queda para el coordinador.
