# T-53 · Análisis técnico

## Diagnóstico

El 9-11-2026 trabajaron en paralelo tres revisores independientes, sin contexto de la implementación:

| Revisión | Hallazgos | Informe |
| --- | --- | --- |
| Defectos de código del ejecutor (`CA-xx`) | 15 verificados con un script de reproducción (5 altos, 6 medios, 4 bajos) y 3 sospechas | `revisores/codigo.md` |
| Coherencia entre la especificación y el código (`CS-xx`) | 28 (1 alto, 12 medios, 15 bajos) | `revisores/consistencia.md` |
| Arquitectura y agentes frente a la Constitución V0.6 (`PA-xx`) | 21 propuestas priorizadas | `revisores/arquitectura.md` |

Claude volvió a ejecutar los scripts de reproducción de los `CA-xx` y comprobó en el código las afirmaciones principales de los otros dos informes antes de corregir nada.

## Correcciones

La implementación se repartió en dos grupos de archivos, sin solapes:
- **Claude:** selección, síntesis, entrega, pausas y datos del ciclo.
- **Un segundo agente:** evaluación, almacén, bóveda y monitor.

| ID | Gravedad | Qué estaba mal | Corrección | Archivos |
| --- | --- | --- | --- | --- |
| CA-01 | alta | Una opción vigente que perdía la protección de continuidad quedaba fuera aunque hubiera un puesto libre, y entraba una nueva peor | La vigente sin protección compite por RK con las nuevas por los puestos libres; solo se sustituye si otra mejor ocupa su puesto (9.6.4 y 9.6.5) | HT-03 (copia del ejecutor y de `10_Herramientas`, idénticas) |
| CA-02 | alta | Un cierre no numérico (`-`, `n.d.`, `1.234,5`) se convertía en un resultado `NO_OCURRIDO` inventado | Se convierte a número antes de filtrar; un cierre inválido rechaza la serie (`DatosInvalidos`) y el pronóstico queda pendiente o `NO_RESOLUBLE`; las filas con fecha de publicación ilegible se rechazan | `ht01_datos.py`, `evaluador.py` |
| CA-03 | alta | Los entregables se escribían antes de validarse y, si la entrega se bloqueaba, quedaban en las carpetas de entrega marcados APTO | Se generan en un borrador, se validan y solo lo no bloqueado se mueve a las carpetas de entrega; lo bloqueado va a `_bloqueados/`, sin `estado_g3`. El informe técnico cita las rutas de entrega. El informe C6 se valida contra su esquema V5.1 y, si se bloquea, tampoco se entrega | `redaccion.py`, `seguimiento.py` |
| CA-04 | alta | Una consulta BLOQUEANTE al Broker no pausaba nada si afectaba a todo el alcance o no declaraba tipos | Una BLOQUEANTE sin tipos pausa todo el alcance; si queda pausado todo, el run no analiza nada y queda PARCIAL con la limitación declarada | `interfaz_broker.py`, `orquestacion.py` |
| CA-05 | media | PS1 (y G1) se superaba solo con la pieza automática de momentum, cuya «dirección» no depende de la tesis | Esa pieza es contexto y no cuenta como raíz de PS1 | `orquestacion.py` |
| CA-06 | alta | Un símbolo del universo sin datos hasta la fecha as_of vaciaba en silencio todo su tipo de activo | El símbolo se excluye del lote de fichas y de la cesta de referencia y se declara como laguna; el tipo queda PARCIAL | `orquestacion.py`, `evaluador.py` |
| CA-07 | media | La corrección de Holm no se detenía en el primer fallo y podía certificar una celda que no lo merece | Procedimiento escalonado, con α en la configuración | `motor/evaluacion.py`, `evaluador.py` |
| CA-08 | media | Los hitos de H5 contaban en la celda H4, en los certificados y en el historial publicado | Se excluyen de esas métricas; se evalúan aparte en `estado_h5` | `evaluador.py` |
| CA-09 | media | F4 aceptaba una segunda alta del mismo pronóstico, una segunda resolución o la resolución de uno inexistente (R11) | Se rechazan con `PronosticoCongelado` y una incidencia en HA | `almacen.py` |
| CA-10 | media | Bóveda: devolvía credenciales caducadas, aceptaba caducidades no ISO (y luego fallaba) y creaba el archivo de secretos con permisos 0644 | Caducidad siempre comprobada, ISO validado antes de escribir y escritura atómica con 0600 desde el primer byte | `ht01_boveda.py` |
| CA-11 | baja | Tres copias del mismo hito H5 pasaban como «≥ 3 hitos» | Se bloquean los identificadores repetidos y menos de 3 fechas distintas | HT-09 (las dos copias) |
| CA-13 | baja | Un certificado perfectamente calibrado (ECE = 0) se revocaba | Se comprueba `None` explícitamente y el umbral va a la configuración (INC-T53-03) | `evaluador.py` |
| CA-14 | baja | Números escritos a mano | PS2 de H1 en sesiones hábiles con límites en la configuración (INC-T53-02); parámetros de clústeres en la configuración; un pronóstico arrastrado sin probabilidad ni banda ya no se rellena con 0,5 | `orquestacion.py`, YAML |
| CS-01 | alta | El ejecutor ignoraba el horizonte principal y la justificación del Analista, y cambiaba en silencio la naturaleza, así que el control C17 no podía fallar | Se usan los del Analista y HT-09 dictamina; el ejecutor solo propone un valor si el Analista no lo declara, y ya no cambia en silencio una naturaleza declarada | `contratos.py`, `sintesis.py` |
| CS-03 | media | El monitor HT-08 no abría instancias de AG-21 a AG-25 | La lista de agentes sin estado se construye desde la de Analistas | `ht08_monitor.py` |
| CS-05 | media | Se publicaban 3 bandas verbales en lugar de las 5 del Anexo A y del esquema, con dos tablas incoherentes | Una sola tabla de 5 bandas en la configuración; los huecos van a la banda más cercana a 50 % | `evaluador.py`, YAML |
| CS-07 | media | La trampa documentada en `CLAUDE.md` era inexacta | Corregida: 17 fichas con código de 60, y las 21 nuevas responden `OPERACION_SIN_FICHA` | `CLAUDE.md` |
| CS-12 | media | La degradación de H5 se calculaba pero no se aplicaba | Se registra en F6 y F10 («Sí → Limitado»; «Limitado → No» como propuesta de tipo 3, INC-T53-04). Tras la QA r01 (H-05), el ejecutor recarga su tabla de horizontes desde F10 al empezar cada ciclo | `evaluador.py`, `almacen.py` |
| CS-17 | media | El semáforo y el siguiente paso contradecían el prompt del Analizador (por ejemplo, se proponía enviar a B con E de 60 a 69) | Siguen al prompt (6.15.5 y 6.16), con los umbrales en la configuración; la `confianza` se deja (INC-T53-05) | `sintesis.py`, YAML |

**Calidad:**
- Las cuotas de ruff bajan de 3487 a 3120: arreglos mecánicos de anotaciones e importaciones en los archivos tocados.
- La de mypy de A se queda en 135.
- La línea base de pruebas de A sube de 58 a 103.
- El corpus se vuelve a congelar a propósito, solo por las dos copias de HT-03 y HT-09 en `10_Herramientas`, que deben ser idénticas a las del ejecutor.

## Lo que no se corrige aquí, y por qué

| ID | Motivo | Destino |
| --- | --- | --- |
| CA-12 | Ambigüedad de la especificación (INC-T53-01) | Decisión del operador |
| CA-15 | Pequeñas diferencias de orden entre ejecuciones idénticas (participantes de F5, identificadores de mensaje). Los registros sustantivos coinciden | Mejora técnica pendiente |
| CA-14 (resto) | Sesiones por horizonte duplicadas en `sintesis.py`, zona de interés ±5 %, tasa base 0,5 por defecto, umbral C6 0,05 con desviación NaN | Mejora técnica pendiente |
| CS-02, CS-15, CS-16, CS-20, CS-21, CS-26, CS-27 | Contradicciones internas del corpus (D0, prompts, esquemas): exigen editar el corpus | Revisión de documentación con el operador |
| CS-04, CS-13, CS-14, CS-22, CS-24, CS-25, CS-28 | Huecos del ejecutor frente al D0 que se solapan con la propuesta de rediseño de agentes (PA-06, PA-07) | Se deciden con las propuestas |
| CS-06 | El tratamiento de H5 (Prospectiva con banda e hitos propios) es un rediseño; en la Fase 1 (divisas) H5 no se usa | Con PA-03 |
| CS-08, CS-11, CS-18, CS-19, CS-23 | Desajustes de recuento, inventario de parámetros y documentación menor | Mejora técnica pendiente |
| CS-09 | Valor en UC de un cálculo PLAN_STD (0,1 en el YAML; el Anexo A sugiere 1). Cambiarlo altera todos los presupuestos | Decisión del operador, con PA-08 (presupuesto en euros) |
| CS-10 (resto) | La rotación exploratoria son 2 celdas fijas en lugar del 20 % del presupuesto; el cálculo de evaluación usa 200 réplicas en lugar de 2000 | Mejora técnica pendiente |

## Correcciones de la QA r01

H-01 a H-05 corregidos con su prueba (detalle en `qa.md`). H-06 a H-11, a la deuda técnica (T-63).
