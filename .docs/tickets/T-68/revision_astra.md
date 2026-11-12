# C-02 · Revisión conjunta de B: evaluación T-68 y rediseño

Astra · 12-11-2026 · Base: develop f2db7ad, corpus B V2.1. Solo revisión; B sigue congelado.

## Resumen (cinco líneas)

1. Coincido con medir el valor añadido de B antes de reducirlo; cinco papeles son una hipótesis de diseño, no una cifra óptima demostrada.
2. Reproduzco las llamadas y la tabla de costes de Claude bajo el supuesto de caché caliente tras la primera llamada de cada agente.
3. Los registros efectivos del simulador dan más escrituras al reanudar redes e India: su coste estimado es mayor que esa tabla idealizada.
4. Los recortes deben conservar dependencias entre playbooks, objeciones por candidato y auditoría previa N2/N3.
5. Recomiendo banco de medida, contabilidad y módulos verificables antes de consolidar papeles; ninguna cifra acredita todavía calidad predictiva.

## Método, independencia y límites

Leídos arquitectura de B, configuración, catálogo de prompts, agentes, mapa y controles de la Constitución y ambos encargos. La revisión global anterior ya había leído las propuestas: esta evaluación no es ciega. Mis criterios previos son preservar las obligaciones de los contratos, medir calidad fuera de muestra y separar economía de tokens de seguridad semántica.

Ejecuté `.docs/scripts/medir_consumo_b.py` con el cliente simulado sobre los tres ejemplos indicados, desde `bloque_b/11_Ejecutor`, con `.venv` preparada por el script del proyecto. Los registros están en `evidencias_astra/redes.json`, `evidencias_astra/india.json` y `evidencias_astra/cobre.json`. Los tres terminan ENTREGADA y G3 APTO. Esto confirma ejecución de esos ejemplos, no calidad de selección ni auditoría general del código.

## Reproducción de cifras

| Ejemplo | Llamadas | Agentes distintos / llamados una vez | Tokens sistema | Tokens encargo registrados | Sistema / entrada |
| --- | ---: | ---: | ---: | ---: | ---: |
| Redes | 29 | 16 / 11 | 955.846 | 34.963 | 96,47 % |
| India | 29 | 17 / 12 | 932.513 | 25.776 | 97,31 % |
| Cobre | 27 | 17 / 14 | 869.152 | 25.050 | 97,20 % |

El «96 %» describe bien redes, no exactamente los tres casos. Tampoco son todos 990.000 tokens: cobre suma 894.202. Se estiman caracteres/3,6; no son tokens facturados. La serialización `user_tok` del medidor incluye envoltura JSON, mientras `entrada` del cliente cuenta contenido: no deben mezclarse sin explicarlo. No he validado el margen de error del 10–20 % ni que las proporciones sean invariantes al cambiar de tokenizador.

Reparto de redes, reproducido sin redondear:

| Agente | Llamadas | Sistema | Encargo |
| --- | ---: | ---: | ---: |
| B01 Coordinador | 2 | 72.098 | 1.305 |
| B02 Director | 7 | 314.958 | 8.903 |
| B03 Estructura | 3 | 102.378 | 4.053 |
| B04 Demanda | 1 | 29.488 | 1.158 |
| B05 Oferta | 1 | 28.037 | 1.106 |
| B06 Tecnología | 1 | 28.143 | 1.100 |
| B07 Regulación | 1 | 29.186 | 1.100 |
| B09 Finanzas | 1 | 31.829 | 1.132 |
| B12 Seleccionador | 4 | 144.572 | 5.308 |
| B13 Prospectiva | 1 | 23.213 | 836 |
| B14 Contrario | 1 | 20.420 | 2.138 |
| B15 Curador | 2 | 33.256 | 1.020 |
| B17 Redactor | 1 | 23.568 | 978 |
| B18 Documentador | 1 | 17.607 | 594 |
| B22 Auditor | 1 | 18.302 | 1.140 |
| B24 Emergentes | 1 | 38.791 | 3.092 |

### Costes: coincidencia condicionada

Precios consultados el 12-11-2026: entrada Opus 5.5 4 USD/M, Sonnet 5.5 2 y Haiku 5.5 0,10 en el tramo aplicable; salida 20, 10 y 0,50. Escritura 1 h ×2; lectura ×0,05 en Opus/Sonnet y ×0,1 en Haiku. No son euros ni incluyen impuestos, herramientas o salida. [Tarifas oficiales](https://platform.claude.com/docs/en/about-claude/pricing).

Usando `user_tok`, una primera escritura por agente y el resto lecturas, reproduzco:

| Caso | Todos con caché 1 h | Sin caché para agentes de una llamada | Además Director −30 % y Seleccionador −35 % |
| --- | ---: | ---: | ---: |
| Redes | 2,2889 USD | 1,6343 USD | 1,4013 USD |
| India | 2,3071 USD | 1,6228 USD | 1,3949 USD |
| Cobre | 2,3325 USD | 1,4824 USD | 1,3076 USD |

Fórmula: precio × (encargo + sistema escrito ×2 + sistema leído ×factor)/1.000.000. En la segunda columna de ahorro, los agentes de una llamada pagan sistema ×1; en la tercera solo se reduce el componente sistema de B02/B12. Los ahorros publicados se reproducen; la última columna sigue siendo un escenario, no un resultado del rediseño.

Pero sumando `entrada`, `cache_escr` y `cache_lect` tal como los registra el simulador, resultan **2,7615 / 2,7859 / 2,3245 USD**, respectivamente. Al autorizar y reanudar se crea otro cliente simulado y se pierde su conjunto local de prefijos vistos. Eso no demuestra que el proveedor real pierda la caché: demuestra que la tabla original supone continuidad y no es una lectura directa del registro. Con esos registros y la misma supresión de caché para agentes únicos: 2,1069 / 2,1017 / 1,4744 USD; no anunciar siempre un 29–36 % de ahorro.

En producción hay que medir aciertos reales, caducidad y concurrencia. La caché requiere prefijo idéntico y no está disponible hasta que empieza la primera respuesta; escalonar llamadas tiene coste de latencia. [Funcionamiento oficial de caché](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). Además, `CatalogoPrompts.system(ttl="")` todavía añade `cache_control`: vaciar el TTL no desactiva la caché.

### Texto compartido y playbooks

Los doce apartados P.1–P.12 ocupan el **37,75 %** del texto del Seleccionador, medido desde sus encabezados hasta el siguiente o fin. Quitar once ahorra **32,62–35,46 %**, según el retenido, no un 35 % uniforme. Hay dependencias reales: P.7.3 usa el playbook del subyacente y P.5.3 puede usar RV. Debe cargarse el cierre de dependencias, no borrar once a ciegas.

Para el marco común usé un criterio reproducible estricto: extraer texto entre comentarios `COMÚN` y `FIN COMÚN` y sumar solo los fragmentos cuyo contenido, sin espacios extremos, aparece literalmente en la plantilla. Resultado sobre el texto completo del prompt: Demanda 29,93 %, Emergentes 22,63 %, Estructura 25,78 %, Finanzas 27,68 %, Flujos 31,60 %, Macro 25,79 %, Oferta 31,51 %, Regulación 30,25 %, Sostenibilidad 30,98 %, Tecnología 31,39 %. No reproduzco exactamente el 24–34 % con esta definición; hace falta declarar qué fragmentos se cuentan. Contar todo lo marcado común tampoco prueba identidad: contiene sustituciones propias del agente. Una caché compartida exige bytes idénticos y compatibilidad de modelo/herramientas.

## Veredictos sobre las nueve mejoras

| # | Veredicto | Motivo, cambio y estado de la estimación |
| --- | --- | --- |
| 1 Banco | DE ACUERDO CON CAMBIOS | Cuatro variantes, mismas fechas/universo/costes, intervalos emparejados y muestra final reservada. Añadir omisiones, errores graves y latencia. El simulador solo valida mecánica; aprobación posterior por C no es verdad de mercado independiente. |
| 2 Caché | DE ACUERDO CON CAMBIOS | Política según reutilización observada entre peticiones, no solo dentro de una. Desactivación explícita, caducidad y registro por proveedor. Ahorro reproducido bajo supuesto, no garantizado. |
| 3 Un playbook | DE ACUERDO CON CAMBIOS | Cargar kit y dependencias del subyacente; conservar reglas globales. 32,62–35,46 % es techo textual sin dependencias; mejora de precisión no demostrada. |
| 4 Prefijo común | DE ACUERDO CON CAMBIOS | Extraer núcleo literalmente idéntico y comprobar caché real por modelo. No todo texto marcado común es compartible; medir latencia del escalonado. Ahorro aún no medido. |
| 5 Director por fase | DE ACUERDO CON CAMBIOS | Intermedio útil: invariantes siempre presentes y módulo por fase. Comparar equivalencia de obligaciones; −30 % e incremento de precisión son hipótesis. |
| 6 Lotes | DE ACUERDO CON CAMBIOS | Solo trabajo cuyo plazo admite demora; vigilancia urgente queda fuera. Caducidad, cancelación y datos actualizados al consumir el resultado. Descuento de tarifa no equivale al 50 % del sistema entero. |
| 7 Precios y tope | DE ACUERDO CON CAMBIOS | Presupuesto reservado antes de cada intento, incluye salida máxima, reintentos, herramientas y proveedores; también límite global concurrente. Reanudación autorizada y coste en moneda declarada. No es solo rellenar precios. |
| 8 Modelo por tarea | DE ACUERDO CON CAMBIOS | Evaluar dificultad, fallos críticos, coste total y latencia, con versión fijada. La tarifa por token no mide coste por análisis válido; promoción solo tras banco. |
| 9 Reglas a código | DE ACUERDO CON CAMBIOS | Sí validación, IDs, formatos y duplicados exactos; no convertir evaluación de credibilidad, materialidad o contradicciones en deduplicación mecánica. Mejora semántica no probada. |

## Mejoras adicionales y orden

Primero congelar casos, criterios de aceptación y presupuesto total. Medir por petición y por intento con identificador común, incluyendo abortos y reparaciones. Después caché/modularización sin cambiar funciones; luego consolidar un papel cada vez. Registrar qué obligaciones desaparecen del prompt y dónde se conservan. Evaluar también muestras descartadas por el plan: el analista no puede detectar siempre aquello que no llega a ver.

Las objeciones deben mantener alcance TESIS/CANDIDATO, candidato, eslabón, fuente, fecha y resolución; si se sustituye un finalista, se contrasta el sustituto. Mantener consultas, pausas, cancelación y reanudación idempotente: reducir agentes no elimina esos estados. No anunciar como «ningún riesgo» las migraciones de propietarios: conservar entregas pendientes, histórico y responsable explícito.

## Respuestas a las nueve preguntas de T-68

1. Cinco papeles es un objetivo razonable para ensayar; no fijaría ese número como condición de éxito.
2. Aún no se sabe cuánto aporta la IA: falta una comparación histórica y posterior en sombra que mida calidad y coste completo.
3. Seleccionaría modelos por resultados del banco; tampoco adoptaría Fable para N3 por prestigio o precio.
4. Sí a un tope aprobado, con reserva concurrente y parada recuperable antes de excederlo; respeta además el límite anual acordado.
5. Sí a propietarios únicos, con inventario de CT-B-22 a CT-B-29 y registros. H debe aceptar también seguimiento de oportunidades sin posición; si no, ese servicio queda en el Orquestador, sin perderlo.
6. B ordena candidatos por exposición, viabilidad y comparación relativa; C estima valor y conveniencia del instrumento. B no fija precios objetivo ni tamaños.
7. Reutilizar A solo con fuentes, fechas, alcance y versión compatibles; B contrasta el delta y cualquier conclusión invalidada por cambios, no hereda certeza.
8. Adelantar módulos como experimento aprobado tiene sentido; la congelación sigue vigente y cualquier cambio contractual necesita su procedimiento.
9. Sí a un patrón compartido de coordinación, evidencia y revisión; los kits y criterios de cada bloque conservan su especialización.

## Rediseño

### Resumen (cinco líneas)

1. Apoyo la dirección de pocos papeles con coordinación determinista, ya aceptada por el operador como dirección de trabajo.
2. El plan por código necesita reglas de cobertura, abstención y revisión de descartes; no conoce automáticamente qué dimensión importa.
3. Las 150.000–200.000 entradas y 6–8 llamadas no están demostradas con prompts construidos.
4. Auditoría semántica previa y contradicción independiente no son intercambiables con validar JSON.
5. Migraría por etapas comparables, manteniendo contratos, controles y capacidad de volver al diseño anterior.

| Decisión | Veredicto | Condiciones y cambios |
| --- | --- | --- |
| Eliminar Director | DE ACUERDO CON CAMBIOS | Máquina de estados para coordinación; analista para tesis/veredicto. Mapear todas sus obligaciones, incluidas consultas filtradas, parada y objeciones. |
| Analista de dimensión y plan | DE ACUERDO CON CAMBIOS | Un papel no implica una única instancia ni eliminar contraste especializado. Matriz de cobertura, dimensiones obligatorias por tipo y solicitud de ampliación; auditar descartes. |
| Seleccionador con kit y Sonnet | DE ACUERDO CON CAMBIOS | Kit más dependencias y campos de incertidumbre; Sonnet es aspirante, no superioridad demostrada. |
| Contradictor y segundo analista | DE ACUERDO CON CAMBIOS | Evidencia común fechada, respuestas independientes, reglas ante desacuerdo, ausencia o fallo del proveedor. Dos proveedores no hacen independientes los errores de datos. |
| Código y funciones fuera | DE ACUERDO CON CAMBIOS | Trasladar lo determinista y los registros; conservar propietario semántico y consumidores. Rechazo sustituir toda auditoría previa por muestreo sin evidencia y enmienda explícita. |
| Banco de cuatro variantes | DE ACUERDO CON CAMBIOS | Mismos casos y presupuesto de evaluación; calidad, cobertura, daño y coste total con incertidumbre. No declarar empate por falta de potencia. |
| Migración por pasos | DE ACUERDO CON CAMBIOS | Contratos y criterios antes de mover responsabilidades; doble ejecución en sombra y reversión. Pasos 1 y 5 no tienen riesgo cero. |

**Tamaño y llamadas.** Dos llamadas de ámbito, dos o tres de dimensión, una de selección y una de contradicción ya son seis o siete. Más tipos, lector, ampliaciones, reparación y auditoría aumentan el total. Solo las dos entradas actuales del Director suman 89.988 tokens de sistema; tres especialistas de unos 28–34 mil añaden 84–102 mil, Seleccionador 36.143 y Contrario 20.420: aproximadamente 231–249 mil sin encargos, lector ni auditor. Es posible reducirlo con módulos, pero 150–200 mil requiere construirlos y medirlos. La tabla N1/N3 tampoco es una medición.

**Conflicto concreto.** La arquitectura vigente §8 exige auditoría previa al 100 % en N2/N3; CT-B-19 separa Auditor y Orquestador. G3 no verifica toda la semántica. Hasta una sustitución demostrada y aprobada, conservar revisión previa, aunque la realice un papel reutilizable independiente. CT-B-01/02 conserva admisión/entrega, CT-B-28 consultas y CT-B-29 seguimiento; los contratos internos cambian de responsables explícitamente. El mecanismo de fechas y verificación diversa de la Constitución sigue siendo obligatorio.

### Respuestas a las cinco preguntas del rediseño

1. Sí como objetivo gradual, con los cambios anteriores; las nueve mejoras son experimentos iniciales, no un compromiso de eliminar controles.
2. Sí, banco primero al descongelarse B, aprovechando infraestructura existente sin dar por validada su calidad predictiva.
3. Sí al segundo proveedor ya aceptado como dirección común A/B/C; presupuesto, aislamiento y tratamiento de fallos antes de usarlo.
4. Sonnet puede ser candidato inicial; elegir por tarea y resultados. N3 no se define simplemente por usar un modelo más caro.
5. Sí a la pauta compartida A/B/C, sin fusionar sus fronteras ni convertir el ahorro en criterio único.

No se modifica B ni se reactivan tickets retirados. Las cuestiones de diseño aquí señaladas son propuestas para Claude y el operador, no cambios aprobados de la Constitución.
