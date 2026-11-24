# T-198 · Bloque A: PB-46, el Buscador atiende el CT-19 de fiabilidad de fuentes (F9 de la instancia)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (24-11-2026, QA r02 APTO y ronda de cierre verificada, sin hallazgos abiertos) |
| Pieza | bloque_a (ejecutor): `bloque_a/11_Ejecutor/bloque_a/fiabilidad_f9.py` (nuevo), `bloque_a/almacen.py` (F9 de la instancia), dos puntos de `bloque_a/orquestacion.py` |
| Planifica · implementa · QA | claude · claude · el agente que no implementó |
| Aprobación del operador | Encargo de la sesión coordinadora (24-11-2026) sobre el hueco de PB-46 que dejó la QA r01 de T-159 (H-02, INC-T159-01); sin decisión nueva del operador |
| Deuda técnica | T-198 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que el CT-19 FIABILIDAD_FUENTES que el Evaluador (AG-20) envía al Buscador de Fuentes Avanzadas (AG-16) deje de ser un mensaje que nadie atiende: el Buscador lo recibe, el ejecutor comprueba que cuadra con F6 y F9 y deja la fiabilidad medida en F9 (de la instancia), y el Buscador la ve en sus búsquedas. Es la parte de «2) CT-19 al Buscador. 3) Recalificación en F9» de PB-46 que no depende del modelo real.

## Fuentes

- Plan de pruebas V3.0, PB-46: pasos «1) Resolución y revisión mensual. 2) CT-19 al Buscador. 3) Recalificación en F9»; criterio «FUE- en F6; Q y orden actualizados en F9 con motivo».
- Evidencias (`docs/evidencias_pruebas_bloque_a.md`, fila PB-46, «No comprueba»): «el CT-19 al Buscador se crea COMPLETO y nadie lo atiende: no hay en F9 dónde escribir la recalificación (QA r01 de T-159, H-02; INC-T159-01)».
- Documento 0 V5.3: 12.5 («la comunica al Buscador, que la incorpora a su calidad en F9»), AG-16 en 4 («mide la fiabilidad de las fuentes de opinión con el Evaluador»), F9 en 5.1 (propietario AG-16), R6, CT-19 en el Anexo B («al Buscador, `tipo` FIABILIDAD_FUENTES y `fuentes`») y la rúbrica de F9 en 13.3 (criterio 2, neutro 10/20).
- Prompt del Buscador V5.0 (`02_System_prompts`, datos de runtime): sección 3 (entrada: fuentes con «Q, nivel y `fiabilidad_medida` (si existe)»), 4.4 (bloque «Fiabilidad medida» de la ficha), 5.3 punto 4, 6.3 (criterio 2), 9 y 12 («Sin CT-19 del Evaluador»).
- Esquema de F6 V2.0, 4.5 (FUE-). F9 V3.2 («Cómo usar»: escribe solo AG-16; tipo `RECALIFICACION` en «Novedades»).
- T-125 (el ciclo Evaluador → CT-19, cerrado) y su límite: la recalificación de Q y el orden los hace el Buscador con el modelo real.

## Alcance

- **Entra:**
  - **F9 de la instancia en el almacén** (`almacen.ARCHIVOS["F9"]`, propietario AG-16, clave `ref_id`), append-only y encadenado como los demás, encima de las fichas del corpus congelado, que no cambian. AG-16 solo puede escribir en él entradas `FIABILIDAD_MEDIDA`. Un almacén sellado antes de T-198 abre y sella F9 vacío; un F9 que existe sin sello, o un F9 borrado con su sello, falla cerrado.
  - **Atención del CT-19** (`fiabilidad_f9.atender_ct19`): se comprueba el mensaje entero antes de escribir (CT-19 de AG-20 a AG-16, `tipo` FIABILIDAD_FUENTES, fuentes no vacías, cada una con exactamente los campos de la FUE-, igual a su FUE- de F6, con el `comunicado_ct19` de ese mensaje y un `ref_id` que es fuente de F9, sin `fue_id` repetidos). Si algo no cuadra, `FiabilidadNoAtendible` y nada en F9. Si cuadra, una entrada `FIABILIDAD_MEDIDA` por fuente con el bloque «Fiabilidad medida» del prompt (4.4): pronósticos registrados, resueltos, aciertos, BSS, BSS contraído, puntos del criterio 2 del Evaluador, `calc_id`, métrica, ventana, fecha del CT-19, `recibido_via` (msg_id), `run_id` y `recalificacion_q: PENDIENTE`. Comprobación y escrituras bajo el cerrojo del almacén (sin vuelta atrás: si el almacén falla a mitad, lo ya escrito queda y el ciclo siguiente completa el resto sin duplicar).
  - **En el ciclo** (`Bloque._comunicar_fiabilidad`): el CT-19 lleva las FUE- de F6 que aún no están en F9 (las nuevas y las que quedaron sin atender) y el Buscador lo atiende en el acto. Si no cuadra, una incidencia DATOS en HA y se reintenta en el ciclo siguiente con un CT-19 nuevo. Una FUE- ya atendida no se reenvía ni se duplica, tampoco con dos procesos a la vez.
  - **Al Buscador** (`Bloque._peticion_conocimiento`): las fuentes de F9 ofrecidas en un CT-07 llevan `fiabilidad_medida` si la tienen (y solo lo conocible en `as_of`).
- **No entra (motivado):**
  - La recalificación de Q, el nivel, el orden dentro de la temática y la línea `RECALIFICACION` de «Novedades»: los hace el Buscador con el modelo real (T-125). Además, el prompt (6.3) da otra contracción (S por bandas de BSS y n / (n + 30)) que la del esquema de F6 con la que el Evaluador calcula los puntos (k = 20): elegir es del modelo y, si se quiere fijar, del operador (INC-T198-01).
  - El camino en backtest: no entra ningún pronóstico de una fuente de F9 sin fecha (T-125); sin FUE- no hay CT-19.
  - El apartado `fiabilidad` del CT-21 mensual del Buscador (lo lleva el mantenimiento de fuentes, T-181 de Astra).
  - Cambiar contratos, esquemas o el corpus.

## Diseño

- **Contratos y esquemas:** ninguno cambia. El CT-19 al Buscador conserva su cuerpo (`tipo` y `fuentes` con los campos de la FUE-); el Anexo B no exige más. Ninguna respuesta del modelo nueva: el Buscador no se invoca para esto (lo que haría con el modelo es la recalificación, fuera de alcance).
- **Estado persistido:** `F9_registro_fuentes.jsonl` en la carpeta del almacén (nuevo) y su sello en `sellos_integridad.json`. No se escribe en F6 nada nuevo salvo el `comunicado_ct19` de siempre (se reescribe si la FUE- se reenvía).
- **Números:** ninguno nuevo. La ventana es `fiabilidad_fuentes.ventana_meses`; los puntos son los de la FUE-.
- **Cómo falla cerrado:** todo el mensaje se comprueba antes de la primera escritura; se captura solo `FiabilidadNoAtendible` (un error del almacén sale del ciclo); un archivo F9 sin sello o sin archivo con sello no abre.
- **Ficheros de Astra** (`referencias.py`, `mantenimiento_fuentes.py`, rama `origin/astra/encargos-bloque-a-c38-c47`): no se tocan. En `orquestacion.py`, una línea nueva justo después de `cand = self.referencias.para_clase(…)` en `_peticion_conocimiento`, lejos del bloque que Astra cambia en esa función, y `_comunicar_fiabilidad`, que Astra no toca.
- **Decisiones `[PROPUESTO]`** (INC-T198-01): F9 de la instancia en el almacén como lugar de escritura del Buscador; qué campos lleva la fiabilidad medida; `recalificacion_q: PENDIENTE`; el reintento con un CT-19 nuevo; `pronosticos_registrados` contado en F2.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Añadir un archivo al almacén | Un almacén sellado antes no abriría (falta el sello de F9) | Al abrir, un archivo que no existe y no tiene sello se sella vacío; si existe sin sello, falla cerrado (prueba CA-6) |
| Conflicto de fusión con Astra en `orquestacion.py` | Trabajo repetido | Dos puntos pequeños, lejos de sus bloques; `referencias.py` y `mantenimiento_fuentes.py` sin tocar |
| Reenviar FUE- de almacenes antiguos | Un CT-19 más en el primer ciclo tras T-198 | Es lo correcto: nunca se atendieron. Se dice en el handoff |
| Ciclos mock distintos | Goldens o consumo cambian | Sin FUE- no se escribe ni se anota nada; se comprueba con el ciclo mock y el backtest |

## Criterios de aceptación (binarios)

Del criterio del plan («FUE- en F6; Q y orden actualizados en F9 con motivo»), la parte del ejecutor:

1. CA-1: con las dos fuentes del plan (25 pronósticos, una con habilidad y otra sin ella), el CT-19 al Buscador se atiende y deja en F9 de la instancia, escrita por AG-16, una entrada por fuente con la fiabilidad medida igual a su FUE- de F6 (n, aciertos, BSS, BSS contraído, puntos y `calc_id`), los pronósticos registrados, la ventana, la fecha del CT-19, el msg_id que la trajo y `recalificacion_q` PENDIENTE; la hábil por encima del neutro y la otra por debajo; la Q del corpus no cambia. También en un ciclo y con la configuración por defecto.
2. CA-2: un CT-19 que no cuadra (emisor, receptor, contrato o tipo; sin msg_id; sin fuentes; un campo de más o de menos; un `fue_id` repetido o que no está en F6; un valor distinto del de F6; otro `comunicado_ct19`; un `ref_id` que no es fuente de F9) no escribe nada en F9, aunque otra fuente del mensaje cuadre; en el ciclo deja una incidencia en HA y se reintenta en el siguiente; un error del almacén no se traga.
3. CA-3: atender dos veces el mismo CT-19 no duplica, el ciclo siguiente no reenvía lo atendido, y cuatro instancias a la vez dejan una entrada por fuente con el almacén íntegro.
4. CA-4: una FUE- comunicada y sin atender (como en un almacén de antes de T-198) sale en el CT-19 del ciclo siguiente y se atiende con el msg_id nuevo; de una fuente con dos FUE-, la más reciente queda la última en F9.
5. CA-5: en un CT-07 al Buscador, la fuente de F9 con fiabilidad medida la lleva en sus candidatas; las demás y las de F7 no; antes de la fecha de la entrada, tampoco (sin fuga).
6. CA-6: solo AG-16 escribe en F9 de la instancia y solo `FIABILIDAD_MEDIDA`; un almacén sellado antes de T-198 abre y sella F9 vacío; F9 sin sello o borrado con su sello falla cerrado.
7. CA-7: sin FUE- no hay CT-19 al Buscador, ni archivo F9, ni anotación; el cuerpo del CT-19 no cambia; ningún texto de F9 dice «valid…» (R8, G3-MET-13); ciclo mock y backtest iguales que en develop; suite de A ≥ 607 y sin fallos nuevos; cuotas sin subir; gate 12/12.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t198_buscador_ct19.py::test_ca1_…` (3) | nominal, integración, configuración por defecto | CA-1 |
| `…::test_ca2_…` (5; 16 mensajes malos, uno sin msg_id y una fuente fuera de F9) | fallo cerrado, integración | CA-2 |
| `…::test_ca3_…` (2) | idempotencia, concurrencia | CA-3 |
| `…::test_ca4_…` (2) | reintento, límite | CA-4 |
| `…::test_ca5_…` (2) | nominal, integración, sin fuga | CA-5 |
| `…::test_ca6_…` (3) | matriz de escritura, migración, fallo cerrado | CA-6 |
| `…::test_ca7_…` (3), suites de T-125, ciclo mock y backtest, suite de A, gate | regresión | CA-7 |
| `mutantes.py` | robustez de las pruebas | todos |

## Scripts

`.docs/tickets/T-198/mutantes.py` (nuevo); `.docs/scripts/evidencias_plan_a.py --pb PB-46` y `--ejecutar`.

## Registro

- 2026-11-24 · ABIERTO · claude · encargo de la sesión coordinadora sobre el «No comprueba» de PB-46
- 2026-11-24 · PLANIFICADO · claude · plan con el Documento 0 V5.3 (12.5, CT-19, F9), el prompt del Buscador V5.0 y T-125
- 2026-11-24 · EN CURSO · claude · implementación (`fiabilidad_f9.py`, `almacen.py`, dos puntos de `orquestacion.py`)
- 2026-11-24 · EN QA (r01) · claude · 20 pruebas nuevas, 34 mutantes muertos, mapa y evidencias (PB-46 sigue «Superada en parte»), ciclo mock y backtest, gate; commit local
- 2026-11-24 · NO APTO · QA r01 (revisor independiente): H-01, H-04 y H-07 medios; H-02, H-03, H-05 y H-06 bajos (`qa.md`)
- 2026-11-24 · EN QA (r02: QA r01 NO APTO) · claude · los siete corregidos con su prueba (`test_r02_…` y CA-1 reforzada), R1–R6 del revisor en `mutantes.py`, scripts de `revisores/` en verde, gate completo con log propio (`pruebas.md`)
- 2026-11-24 · APTO con ronda de cierre · QA r02: H-08, H-09 y H-10, bajos (`qa.md`)
- 2026-11-24 · EN QA (ronda de cierre de la QA r02) · claude · H-08 (F9 ilegible: sin marca y reintento), H-09 (INC-T198-01 sin `F9_bajas.md`, decisión del coordinador), H-10 (barrera dentro de la sección crítica en CA-3); sin gate completo, por indicación del coordinador
- 2026-11-24 · ronda de cierre verificada · APTO sin nada abierto (`qa.md`).
- 2026-11-24 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
