# T-188 · QA independiente

- **Revisor:** claude (no implementó; QA formada con el plan, el encargo y el código antes de leer `analisis-tecnico.md`) · **Ronda:** r01 · 24-11-2026
- **Base revisada:** `2d99af6` (PR 3, rama `astra/encargos-bloque-a-c38-c47`, sobre `develop` `9ce57b2`). Commits del ticket: `8bb1d95` (código y pruebas) y `5ef929b` (guardas de `comparar_decisiones_broker` para registros históricos). Worktree propio `<scratchpad>/qa_astra_185_188` con el `.venv` del proyecto enlazado.
- **Vara de medir:** PB-11 y PB-62 del Plan de pruebas V3.0, y la fila C-43 del encargo del 18-11-2026 («T-161 y T-171 fijaron que las lecciones de PRODUCTO no llegan a los agentes de control: no lo deshagas»).

## Reproducción desde limpio

| Orden | Resultado |
| --- | --- |
| `pytest -q tests/test_t185_rotacion.py tests/test_t188_producto.py tests/test_v51.py tests/test_fase3_goldens.py tests/test_t65_resto_t53.py` | 232 pasadas |
| `pytest -q tests/test_t161_guias.py tests/test_t161_r0{2,3,4}.py tests/test_t171_guias.py tests/test_fase4_huecos.py tests/test_integracion.py tests/test_t116_r05.py` | 957 pasadas (la barrera de T-161 y T-171 sigue intacta) |
| Revertir en el worktree el código del ticket (hunk de `interfaz_broker.py` y la llamada a `comparar_decisiones_broker` en `Evaluador.ciclo`) y correr `test_t188_producto.py` | las 2 pruebas FALLAN; con el código vuelto a poner, pasan |
| `python .docs/tickets/T-188/mutantes.py` (de Astra) | 2 de 2 detectados |
| `python .docs/tickets/T-188/revisores/r01_02_mutantes.py` (míos) | **6 de 6 VIVOS** (H-02 a H-04) |
| `pytest -q .docs/tickets/T-188/revisores/r01_01_lecciones_producto.py` | 4 fallan (H-01), 6 pasan |
| ruff y mypy de `evaluador.py`, `interfaz_broker.py` frente a `9ce57b2` | ruff 4 = 4 y 4 = 4; mypy del paquete 102 = 102, sin errores nuevos en esos ficheros. Pruebas nuevas ruff-limpias |

Sin secretos, datos personales ni identificadores de modelo en lo añadido. Ningún texto nuevo con la raíz «valid-» junto a un método (G3-MET-13). No hay números nuevos escritos a mano: `evaluacion.min_calibrar` y `consultas_broker.recurrente` salen de la configuración (INC-T188-01 `[PROPUESTO]`).

## Criterios del plan

| Cláusula | Cumple | Evidencia |
| --- | --- | --- |
| PB-11: RET-, `decision_broker` sin cambio de estado, CT-22, ambos PRG RESUELTO, HAC- con OPP-B, nada al Bloque B | sí (ya lo cubrían `test_peticion_ad_hoc_y_decisiones` y `test_pb11_…`) | suite |
| PB-11: «lección de producto con la comparación enviadas frente a descartadas cuando haya muestra» | **no** | La LEC- se escribe en F6, pero no cumple F6 4.4 y no llega a nadie (H-01); su contenido, la muestra y la ventana temporal no tienen prueba que las mate (H-02, H-03) |
| PB-62: ≤ 3 CT-23 por RUN-, aviso `CONSULTA_RECURRENTE` | sí | `test_consulta_validaciones_agrupacion_y_entrante` |
| PB-62: «LEC- de producto creada» (lección de normalización del CT-01, tres análisis en 8 semanas) | **no** | Misma LEC- inválida (H-01); «análisis distintos» sin prueba que la mate (H-04) |
| C-43: las PRODUCTO no llegan a los agentes de control (T-161, T-171) | sí, pero hoy por accidente | `lecciones_para` no se ha tocado (`TIPOS_TEXTO_DEL_CODIGO` sigue en PREDICTIVA y CALIBRACION) y `r01_01::test_control_no_recibe_producto` pasa; pero pasa también porque las lecciones nuevas no llegan a nadie. La prueba hay que volver a pasarla tras corregir H-01 |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Prueba de regresión | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `r01_01::test_h01_*` (4 fallan) | Esperado: una LEC- de PRODUCTO válida según el esquema de F6 V2.0 (4.4: `ambito` = `{clase, horizonte, agente[], fuente, metodo}`) que llegue a sus `ambito.agente` (AG-17 y AG-02; AG-01 y AG-17), como dice INC-T188-01 («solo van a agentes de producto»). Obtenido: las dos lecciones nuevas llevan `ambito.tema` (`{"agente": […], "tema": "DECISION_BROKER"}` y `"CONSULTA_RECURRENTE"`), que `guias.validar_leccion` rechaza («ambito con claves que no son de F6 4.4: ['tema']»). `Guias.lecciones_para` no se las da a **ningún** agente y `_revisar_lecciones` deja en HA una incidencia **Material** «Lección LEC-… no se da a ningún agente». Las pruebas del ticket solo miran que la entrada esté en F6 | En `Evaluador.comparar_decisiones_broker` y en `ConsultasBroker._recurrencia`, `ambito` con solo claves de F6 4.4: `{"clase": None, "horizonte": None, "agente": ["AG-17", "AG-02"], "metodo": "comparacion_decisiones_broker"}` y `{"clase": None, "horizonte": None, "agente": ["AG-01", "AG-17"], "metodo": "consulta_recurrente_ct23"}`. `metodo` (texto de F6 4.4) distingue las dos de la de `leccion_producto` (mismo `agente`, sin `metodo`), para que la deduplicación de `_nueva_leccion` (por `tipo` + `ambito`) no las confunda. Ajustar las pruebas que filtran por `ambito.tema` y la frase de INC-T188-01 si cambia | En `tests/test_t188_producto.py`: para cada una de las dos lecciones, `validar_leccion(lec, b.cfg) == []`; su id en `b.guias.lecciones_para("AG-17", …)` (y en AG-02 / AG-01 según la lección); **no** en `lecciones_para` de AG-11, AG-18, AG-19 ni AG-20; y ninguna INC de HA con su `leccion_id`. `r01_01` entero en verde | abierto |
| H-02 | media | `r01_02_mutantes.py`: M5 (etiquetas «enviadas»/«descartadas» intercambiadas) y M6 (`total = len(grupo)`: cuenta los fallos como aciertos) VIVOS | Esperado: una prueba que fije la comparación, que es el contenido de la lección. Obtenido: `test_comparacion_por_decision` solo comprueba `"descartadas" in observacion` y `n >= 2` | Sin cambio de código | En `test_comparacion_por_decision`: calcular de F4 (`b.evaluador.resueltos(fin, solo_informe=True)`) los aciertos de cada grupo y exigir `observacion == f"enviadas: {a}/{na} pronósticos acertados. descartadas: {d}/{nd} pronósticos acertados"`, `set(evidencia)` = PRG de las dos opciones y `n == na + nd`. M5 y M6 deben morir | abierto |
| H-03 | media | `r01_02_mutantes.py`: M1 (umbral de muestra ignorado), M2 (decisión a cualquier fecha) y M4 (la primera decisión en vez de la última) VIVOS | Esperado: el criterio dice «cuando haya muestra» y el análisis técnico «excluye las decisiones posteriores al dato y al vencimiento»; ninguna prueba lo mata. (El comportamiento hoy es correcto: `r01_01::test_h02_*` pasan) | Sin cambio de código | Pasar a `tests/test_t188_producto.py` los tres casos de `r01_01` (`test_h02_sin_muestra_no_hay_leccion` con `min_calibrar=2` y una opción por grupo, `test_h02_decision_posterior_al_dato_no_cuenta`, `test_h02_idempotente`) y uno nuevo: la misma opción DESCARTADA y luego ENVIADA antes del dato cuenta como enviada. M1, M2 y M4 deben morir | abierto |
| H-04 | media | `r01_02_mutantes.py`: M3 (contar consultas en vez de análisis) VIVO | Esperado (PB-62, «se repite en tres análisis»): tres consultas del mismo RUN- o sin RUN- no crean lección. Obtenido: la prueba solo envía tres RUN- distintos; contar consultas pasa igual. (Comportamiento correcto hoy: `r01_01::test_h03_*` pasan) | Sin cambio de código | Pasar a `tests/test_t188_producto.py` `test_h03_tres_consultas_del_mismo_analisis_no_crean_leccion` y `test_h03_consultas_sin_run_no_crean_leccion`, y una consulta de fuera de las 8 semanas que no cuenta. M3 debe morir | abierto |
| H-05 | baja | `git diff 9ce57b2 2d99af6 -- bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json docs/evidencias_pruebas_bloque_a.md` | Esperado: «Superada» solo si se cumple todo el criterio y un `comprueba` propio de cada caso. Obtenido: PB-11 y PB-62 pasan a `AUTOMATICA`/«Superada» con `no_comprueba` vacío mientras la LEC- no llega a nadie (H-01); y las dos filas llevan la misma frase («…a partir de decisiones anteriores al resultado y de consultas recurrentes…»), que mezcla los dos casos. En PB-62, el filtro del Analizador («solo las dudas que cambian una conclusión llegan al Broker») lo decide el modelo y no se dice | Tras H-01 a H-04: PB-11 `comprueba` termina «…; con muestra suficiente por grupo (`evaluacion.min_calibrar`), el Evaluador escribe en F6 una LEC- de PRODUCTO que compara los aciertos de las enviadas y de las descartadas, con decisiones anteriores al dato, y solo la reciben AG-17 y AG-02»; PB-62 `comprueba` termina «…; la misma duda en tres análisis (RUN-) distintos en 8 semanas crea una LEC- de PRODUCTO para el CT-01, que reciben AG-01 y AG-17» y `no_comprueba`: «Qué dudas cambian una conclusión lo decide el modelo del Analizador (modo sombra).» Regenerar las evidencias con `.docs/scripts/evidencias_plan_a.py` | `.docs/scripts/evidencias_plan_a.py` (mapa coherente) y una prueba en `test_t188_producto.py` que lea el mapa y exija que el `comprueba` de PB-11 y el de PB-62 son distintos | abierto |

## Vecinas y fuera de alcance

- Los cambios de Astra en `test_fase4_huecos.py` (PB-10) y `test_t159_extremo_a_extremo.py` (PB-52) son de T-189 y T-191; los juzga el revisor de esos tickets.
- La guarda de `5ef929b` en `comparar_decisiones_broker` (saltar PRG sin `opp_id` decidido o sin fechas) es legítima: los PRG antiguos sin esos campos no pueden clasificarse.

## Veredicto

**NO APTO** (un hallazgo alto y tres medios). Vuelve a `ri-implementar`: corregir H-01 y añadir las pruebas de H-02 a H-05; después vuelvo a ejecutar `revisores/r01_01_lecciones_producto.py` y `revisores/r01_02_mutantes.py` (todos los mutantes deben morir) en una r02.
