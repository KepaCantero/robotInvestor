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
