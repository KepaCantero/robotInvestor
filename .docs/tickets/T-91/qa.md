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
