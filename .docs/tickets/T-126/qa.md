# T-126 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no implementó T-126) · **Ronda:** r01 · 2026-11-15
- **Copia revisada:** clon desconectado en `fb3ccd4` (incluye `df4a60a`). Mutantes en una copia desechable aparte («qa7_mut»), ya borrada.
- Opinión formada con el plan (PB-26 y PB-48), el Documento 0 (13.3 y 661: «orden descendente por calidad Q y, a igualdad, por fecha más reciente»; R23; 9.1) y las pruebas, antes de leer `analisis-tecnico.md`.

## Reproducción desde limpio

| Qué | Orden | Resultado |
| --- | --- | --- |
| Pruebas del ticket | dentro de la suite completa de A (`T-116/qa.md`, r04) | en verde |
| No cambia producción | `git show --stat df4a60a` | T-126 solo añade `tests/test_t126_pb26_pb48.py` y documentación |
| Mutantes y ataque | desde la raíz: `python .docs/tickets/T-126/revisores/r01_01_mutantes_y_ataques.py <copia desechable de bloque_a con «_mut»>` | abajo |
| Medida propia de F7–F9 | desde `bloque_a/11_Ejecutor`: `python ../../.docs/tickets/T-126/revisores/r01_02_medida_f7_f9.py` | F7 560, F8 464, F9 389 fichas; 0 fuera de su sección; 2 de nivel D (F9); empates de Q: 221, 225 y 150 (desempate en H-02) |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · pasan sobre los archivos entregados y detectan una mutación de orden, de nivel o de temática | sí | J1 (orden), J2 (nivel) y J3 (temática inventada) mueren con las pruebas reales (ejecutado). La prueba que dice demostrarlo no lo demuestra (H-03), pero las otras sí |
| CA-2 · PB-48 pasa y una lección que relaja un control no llega a HT-03 | sí | `test_pb48_…`; J6 (HT-03 sin PS8) muere. Lo que no se ejerce, en H-01 |
| CA-3 · el mapa cita estas pruebas y las de T-125 | sí | `evidencias_plan_a.py`: 145 citadas, todas existen; PB-26, PB-46 y PB-48 en PARCIAL |
| CA-4 · no cambia producción; gate 12/12 | sí lo primero; el gate no lo pasé (encargo) | `git show --stat df4a60a`; gates ligeros y ruff 2902 en verde |

## Mutantes y ataque (`revisores/r01_01_mutantes_y_ataques.py`, ejecutado)

| Mutante | Qué rompe | Resultado |
| --- | --- | --- |
| J1 | F7: ANA-DOC-0039 pasa de Q 92 a 96 (desorden en TA-01) | MUERTO |
| J2 | F7: ANA-DOC-0061 Q 95 con nivel B | MUERTO |
| J3 | F7: temática TA-99 | MUERTO |
| **J4** | F7: la última ficha de TA-01 se mueve dentro de la sección TA-02 (su campo «Temática» sigue diciendo TA-01) | **VIVO** (H-02) |
| **J5** | el ciclo no pasa nunca a HT-03 la segunda pasada del Analista | **VIVO** (H-01) |
| J6 | control: HT-03 ignora la banda marginal (PS8) | MUERTO |

Ataque A1, en el ciclo de `test_pb48_una_guia_…`: «entradas HT-03: 12 · con segunda pasada: 9 · con algún total en banda marginal: 3 · en banda marginal sin resolver: 3». Ninguna opción del ciclo en banda marginal se resuelve con la segunda pasada, así que el paso 2 del plan («ejecuta una selección con opción en banda marginal» → «segunda pasada registrada») no se ejerce en el ciclo.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | J5 y A1 de `r01_01` | Esperado (regla de las parciales: «No comprueba» dice todo lo que falta): PB-48 pide «segunda pasada registrada» con una opción en banda marginal. Obtenido: en el ciclo de la prueba ninguna opción en banda marginal se resuelve con su segunda pasada (las tres que caen ahí quedan sin resolver y fuera), y quitar del ciclo la segunda pasada entera (J5) deja las dos pruebas en verde: la regla solo se afirma sobre HT-03 llamada a mano. El hueco declarado solo nombra COR- y P3- | Un ciclo con una opción en banda marginal y su segunda pasada (cliente simulado parcheado), afirmando que se aplica y queda registrada, o añadirlo al «No comprueba» de PB-48 |
| H-02 | media | J4 de `r01_01`; Doc. 0, línea 661 | Esperado (plan: «cada referencia en su sección temática del Anexo D; orden descendente por Q y, a igualdad, por fecha»): las dos cosas comprobadas o declaradas. Obtenido: (a) las pruebas agrupan por el campo «Temática» de cada ficha, no por la sección `## TX-nn` en la que está: una ficha en la sección equivocada pasa (J4 vive; hoy no hay ninguna, medido); (b) el desempate por fecha no se comprueba ni se declara. Medido: con el año de la ficha, 195 empates de F7 van del más reciente al más antiguo y 1 al revés (ANA-DOC-0522, 2016, antes que ANA-DOC-0089, «documento vivo» cuyo año sale de la fecha de consulta 2026); F9 no tiene año en sus empates. Dudoso, pero sin decidir | Comprobar la sección física y el desempate (con la regla para documentos sin año), o ponerlos en el «No comprueba» de PB-26 |
| H-03 | baja | Leer `test_pb26_la_comprobacion_detecta_un_orden_o_un_nivel_mal_puestos` | Dice demostrar que «la comprobación no es vacía», pero no ejecuta las comprobaciones de las otras pruebas sobre datos estropeados: repite en línea una expresión propia y prueba `_nivel_de` y que TA-99 no está en el Anexo D. Si alguien vaciara la comprobación de orden de `test_pb26_dentro_…`, esta seguiría en verde | Factorizar las tres comprobaciones en funciones y llamarlas sobre fichas mutadas (como J1–J3) |
| H-04 | baja | Leer `test_pb48_una_guia_…` | La docstring dice que la lección «llega al Analista como contexto», y no se afirma: si la lección no llegara a nadie, la prueba seguiría en verde y no probaría la parte «conflicto» del caso | Afirmar que el CT-06 del Analista de RV lleva `LEC-2026-0901` |

## Invariantes

- No cambia producción ni el corpus. ✔ (los mutantes de F7 solo en la copia desechable)
- Sin LLM en la ruta determinista; R23 por construcción en HT-03. ✔
- Decisiones: INC-T126-01 `[PROPUESTO]` y en la deuda. ✔
- Secretos: nada. ✔

## Lo que no comprobé

- El gate completo y mypy (encargo).
- F8 y F9 con mutantes (solo F7).

## Veredicto

**APTO** · los cuatro criterios se cumplen (CA-4 salvo el gate, que no me tocaba) y no hay hallazgos críticos ni altos. H-01 y H-02 (medias) dejan incompletos los huecos declarados de PB-48 y PB-26 en el mapa de T-116 (los recojo también en la QA r04 de T-116, H-11); H-01 a H-04 pasan a la deuda con su ID. Cerrar el ticket (estado, deuda, diario, commit) queda para quien coordina: este revisor solo escribe en `qa.md` y `revisores/`.

## Ronda r02

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; no es el de la r01 ni quien implementó) · 2026-11-15
- **Copia revisada:** clon desconectado en `41c0ea4` (wip local con T-125 r02, T-116 r05 y T-126 r02). Mutantes en copias desechables con «qa10_mut» en la ruta, ya borradas.
- Opinión formada con el plan (PB-26, PB-48), el Documento 0 (13.3) y `tests/test_t126_r02.py` antes de leer el apartado «Ronda r02» de `analisis-tecnico.md`.

### Reproducción

| Qué | Orden | Resultado |
| --- | --- | --- |
| No cambia producción ni corpus (T-126) | `git diff fb3ccd4 41c0ea4 --stat` | T-126 solo añade `tests/test_t126_r02.py`; `test_t126_pb26_pb48.py` sin tocar; corpus íntegro (695) |
| Suite completa de A, una vez | ver `T-116/qa.md`, ronda r05 | dentro de la suite |
| Mutantes del revisor anterior, tal cual | desde la raíz: `python .docs/tickets/T-126/revisores/r01_01_mutantes_y_ataques.py <copia «qa10_mut»>/bloque_a` | J1, J2, J3, J6 MUERTOS; **J4 y J5 VIVOS** (el script fija `PRUEBAS` en el fichero de la r01, como dice el implementador) |
| Los mismos, con las pruebas nuevas | `python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-126/revisores/r01_01_mutantes_y_ataques.py <copia>/bloque_a tests/test_t126_r02.py` | **J1 a J6, los seis MUERTOS** (J4: 2 fallan; J5: 1) |
| Mutantes nuevos | `python .docs/tickets/T-126/revisores/r02_02_mutantes_nuevos.py <copia «qa10_mut»>/bloque_a` | J7 a J10, los cuatro MUERTOS (abajo) |
| Medida propia del desempate | desde `bloque_a/11_Ejecutor`: `python ../../.docs/tickets/T-126/revisores/r02_01_desempate_medida.py` | abajo |

**El ayudante `mutantes_revisor_ampliado.py`** (leído y ejecutado): busca la línea `PRUEBAS = [...]` del script del revisor, la sustituye por la lista del revisor más las pruebas que se le pasan (sin duplicados, las del revisor primero), y ejecuta el script con `exec` y `sys.argv = [script, copia]`. No toca los mutantes ni el script en disco; la salida imprime la lista de pruebas usada (`pruebas: ['tests/test_t126_pb26_pb48.py', 'tests/test_t126_r02.py']`). Hace lo que dice. Requiere que `PRUEBAS` sea una lista literal en una sola línea (falla con 2 si no).

### ¿Afirman lo que dicen? (`tests/test_t126_r02.py`, leído entero)

| Prueba | Juicio | Por qué |
| --- | --- | --- |
| `test_h02_cada_referencia_esta_fisicamente_en_la_seccion_…` (F7, F8, F9) | bien | Lee la sección `## TX-nn` real de cada ficha y la compara con su campo; inversiones de Q por sección; nivel y temática. J4 (F7), J8 (F9) y J10 (F8) mueren |
| `test_h02_a_igualdad_de_q_va_primero_la_mas_reciente` | bien, con un hueco pequeño (H-05) | J7 (dos fichas empatadas de F7 intercambiadas: ANA-DOC-0048, 2023 ↔ ANA-DOC-0041, 2016) muere. Solo compara pares contiguos |
| `test_h02_el_caso_dudoso_es_un_documento_sin_anio` | bien | Afirma lo que dice INC-T126-01 (ANA-DOC-0089 sin año en su campo; el lector del ejecutor le da 2026) |
| `test_h03_las_comprobaciones_detectan_fichas_estropeadas` | bien | Ahora ejecuta las mismas funciones que las pruebas de los archivos sobre fichas estropeadas (J1–J4 y un desempate al revés); corrige H-03 |
| `test_h01_en_el_ciclo_…_se_resuelve_con_su_segunda_pasada` | bien | Ciclo real con la lección vigente; las entradas de HT-03 en banda marginal llevan la segunda pasada, todas resueltas, sin PS8, y la segunda pasada está en F3. J5 y J9 (el ciclo deja de guardarla en F3) mueren |
| `test_h01_sin_la_segunda_pasada_…` | bien | Contraprueba sobre las mismas entradas |
| `test_h04_la_leccion_…_llega_al_analista_en_su_ct06` | bien | El CT-06 de RV lleva `LEC-2026-0901` y ninguna entrada de HT-03 la nombra (corrige H-04). Que no la nombre no prueba que no la use, pero eso ya lo afirma `test_pb48_una_guia_…` (J6) |

### Mutantes nuevos (`revisores/r02_02_mutantes_nuevos.py`, contra `test_t126_pb26_pb48.py` y `test_t126_r02.py`)

| Mutante | Qué rompe | Resultado |
| --- | --- | --- |
| J7 | F7: desempate por fecha al revés (dos fichas contiguas con Q 90 intercambiadas) | MUERTO (`test_h02_a_igualdad…[F7]`) |
| J8 | F9: la última ficha de TF-01 dentro de la sección TF-02 | MUERTO (`test_h02_cada_referencia…[F9]`) |
| J9 | el ciclo deja de registrar la segunda pasada en F3 | MUERTO (`test_h01_en_el_ciclo…`) |
| J10 | F8: un nivel A pasa a B con la misma Q | MUERTO (dos pruebas de F8) |

### Medida propia del desempate (`revisores/r02_01_desempate_medida.py`)

F7: 560 fichas, 0 desempates al revés contiguos y 0 en toda la secuencia de cada empate (ignorando las fichas sin año), 7 sin año en empates. F8: 464, 0 y 0, 5 sin año. F9: 389, 0 y 0; 387 fichas con el campo «Año» vacío. Los archivos cumplen la regla tal como la fija INC-T126-01. Pero la función de la prueba deja pasar un trío «2010 · sin año · 2020» con la misma Q (devuelve `[]`): un documento sin año entre dos fechados esconde la inversión (H-05).

### Hallazgos de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 (media) | **corregido** | J5 muere; J9 nuevo también; el ciclo resuelve la banda marginal con la segunda pasada y la registra. Lo que no hace el ejecutor (pedirla si falta) está en el «No comprueba» de PB-48 y en INC-T126-01 |
| H-02 (media) | **corregido** | J4, J7 y J8 mueren; el desempate sin año queda `[PROPUESTO]` en INC-T126-01 y en el «No comprueba» de PB-26 |
| H-03 (baja) | **corregido** | las comprobaciones son funciones probadas sobre fichas estropeadas |
| H-04 (baja) | **corregido** | `test_h04_…` |

### Hallazgo nuevo

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida |
| --- | --- | --- | --- | --- |
| H-05 | baja | `r02_01_desempate_medida.py`, última línea | Esperado: «a igualdad de Q, la más reciente primero» entre todas las fichas fechadas de un empate. Obtenido: `desempates_al_reves` solo mira pares contiguos y un «Documento vivo» entre dos fichas fechadas esconde la inversión. Hoy no ocurre en F7–F9 (medido: 0) | Comparar, dentro de cada (sección, Q), la secuencia de años sin las fichas sin año |

### Invariantes

- No cambia producción ni el corpus (los mutantes de F7–F9 solo en la copia desechable). ✔
- Sin LLM en la ruta determinista. ✔
- Decisiones: INC-T126-01 ampliada `[PROPUESTO]` y fila en `Decisiones_del_operador_Bloque_A.md`. ✔
- Secretos: gates en verde; mis scripts no llevan ninguno. ✔

### Lo que no comprobé

- El gate completo (`check_all.sh`), B (encargo).

## Veredicto (r02)

**APTO** · Las pruebas nuevas afirman lo que dicen: J1–J6 del revisor anterior mueren con ellas (J4 y J5, que vivían, también) y mis cuatro mutantes nuevos (J7–J10) mueren. H-01 a H-04 de la r01 están corregidos. Queda H-05 (baja), que pasa a la deuda técnica con su ID. Cerrar el ticket (estado, deuda, diario y commit) queda para quien coordina: este revisor solo escribe en `qa.md` y `revisores/`.
