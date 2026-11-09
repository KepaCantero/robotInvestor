# T-66 · Análisis técnico

## Motivo

El 10-11-2026, el operador pidió aplicar ya las propuestas oportunas de la revisión T-53 y dar por terminado el Bloque A. Aquí se aplican las que se pueden programar y probar en el ejecutor sin otro proveedor de IA, sin K y sin llamadas reales. Las demás tienen su motivo en el README y su destino en la deuda técnica (T-67).

## Implementación

El trabajo se repartió en dos grupos de archivos, sin solapes:
- **Claude:** orquestación, síntesis, contratos, simulado y configuración.
- **Un segundo agente:** evaluación (`evaluador.py` y `motor/evaluacion.py`), en una copia aparte.

Se juntó sin conflictos (merge de `ca7683d`).

| Propuesta | Cambio | Archivos |
| --- | --- | --- |
| PA-01 | `perfiles.activos` (`[PROPUESTO]`: solo DIV) con `perfiles_activos()`, que falla cerrado sin la clave o con tipos desconocidos. F10 P-02 nace de ahí. Un tipo pedido y no activo da NO_ESTIMABLE y se declara | `configuracion.py`, `orquestacion.py`, YAML, `tests/conftest.py` (las pruebas activan los 12) |
| H-06 (T-65) | Sin tipos que analizar: `_run_sin_analisis()` devuelve PARCIAL y `entrega: SIN_RESULTADO` con sus limitaciones, y lo registra en F5, sin redactar ni validar un paquete vacío | `orquestacion.py` |
| PA-05 | CT-13 sin tesis, mecanismo, pre-mortem ni dimensiones; con las afirmaciones verificables de Prospectiva y la evidencia (fuente, afirmación, dirección). Una objeción fuerte se resuelve solo con `evidencia_citada` verificable más la confirmación de AG-11 en la fase `CONTRARREPLICA`. Veredicto por regla (`_veredicto_refutacion`), guardado en F3 junto al del modelo. Efecto de una tesis frágil: confianza «especulativo» | `orquestacion.py`, `sintesis.py`, `contratos.py`, `mock_respuestas.py`, YAML |
| PA-09 | `LLMClient.conocimiento_previo` (verdadero por defecto; falso en el simulado). `backtest.anonimizar: auto`. `Bloque.contaminacion_posible(as_of)` marca cada PRG (falla cerrado sin fecha de corte). El Evaluador excluye esos PRG de lo que aprende (`resueltos(admisibles=True)`), y el informe de backtest los muestra aparte | `llm.py`, `orquestacion.py`, `sintesis.py`, `backtest.py`, `evaluador.py` |
| PA-10 | `aprendizaje.solo_endurecer` (`[PROPUESTO]`): los certificados nacen PROPUESTO y se aprueban por CT-04 (`aprobar_certificados`), y la recalibración nunca pasa sola a producción. Un PROPUESTO cuya celda deja de cumplir el criterio se retira solo | `evaluador.py`, `orquestacion.py` (CT-04) |
| PA-03 (parte) | `n_efectiva` (Kish, con ρ intraclase por ANOVA sobre los residuos y conglomerados por fecha de resolución), bootstrap del BSS por fechas y `criterio_certificado` sobre `n_eff` | `motor/evaluacion.py`, `evaluador.py`, YAML |
| PA-14 | `_ablacion()`: el top-3 sin objeciones y la coincidencia con el top-3 por señal compuesta, en `seleccion[c]["ablacion"]` y en el RUN de F5 | `orquestacion.py` |
| PA-21 | `FINALISTA.probabilidades_propias`, PRG `prob_analista` (0,05–0,95; si no, `null`) y la métrica `analista_vs_prospectiva` por celda | `contratos.py`, `sintesis.py`, `mock_respuestas.py`, `evaluador.py` |

**Desviaciones del plan:**
- **PA-05, sin relevancia ALTA para una tesis frágil.** El Anexo A no tiene ese disparador, y C10 daría una advertencia en cada ciclo (INC-T66-01).
- **PA-05, el simulado de AG-11.** Ya no ve las dimensiones del Analista: decide con las fuentes distintas y con el azar reproducible del encargo. Por eso cambia algo el top-3 del simulado. Ninguna prueba anterior dependía de ese detalle.
- **PA-10, retirada de propuestas.** El segundo agente añadió la retirada de un PROPUESTO cuya celda deja de cumplir el criterio. Se mantiene: es prudente y evita aprobar una propuesta caducada.
- **Valor elegido sin respaldo en el Anexo A:** `evaluacion.min_conglomerados_bootstrap: 10`. Se apunta en T-57.
- **Calidad.** `modelo_de()` falla cerrado si no hay modelo configurado, en lugar de devolver `None`. Arreglos menores de tipos.

**Límites conocidos:**
- El Contradictor sigue siendo del mismo proveedor (PA-05, T-57).
- La referencia simple de PA-14 solo se registra: todavía no hay un análisis de varias semanas que la compare con el resultado (con PA-03 y SC-4).
- `n_eff` usa conglomerados por fecha, no por fecha y divisa base.

**Para probarlo:**
- `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q`
- `.docs/tickets/T-66/revisores/mutaciones_orquestacion.sh`
