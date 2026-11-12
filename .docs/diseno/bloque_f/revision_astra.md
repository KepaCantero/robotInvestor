# C-06 · Revisión del diseño de F

Astra · 12-11-2026 · develop d544556. Solo documentación local. T-74 continúa pendiente, sin implementación.

## Resumen (cinco líneas)

1. Apoyo F determinista, independiente y con límites por orden, cartera y conjunto.
2. Facilitar reducciones no permite omitir autorización, estado conciliado ni protección contra órdenes concurrentes.
3. Reequilibrar comprando sigue pudiendo aumentar riesgo: no aceptaría una exención general de controles.
4. Concentrar un fondo desconocido solo en su región principal no es conservador para todas las exposiciones.
5. Un control que nunca se activa puede ser valioso; no juzgar su utilidad solo por la rentabilidad de operaciones vetadas.

## Base

Encargo/propuesta de F, Constitución P1/P2/P8/P15/P20 y §§6–8,11, Documento 0 V0.07, `sistema_global/marco_comun_c/validador/control_f.py` y T-74. Contrastado además con decisiones del operador y cambios 47 y 78 de las dos partes de enmienda 5 para no señalar como ausentes defensas que Claude ya propone. No es revisión ciega ni QA del marco: la propuesta se conocía de la auditoría anterior.

El documento antiguo describe once reglas; el código actual incluye F-01…F-23 y CF-09 para el contexto oficial del Orquestador. CF-08 contempla posiciones y autorizaciones ya comprometidas. La necesidad de reservar atómicamente ante simultaneidad es una exigencia de diseño adicional, no una afirmación de que esas protecciones existentes no estén.

## Veredictos

| Decisión | Veredicto | Motivo y cambio |
| --- | --- | --- |
| Asimetría por acción | DE ACUERDO CON CAMBIOS | Deduce acción desde posición conciliada, mantiene permisos y cantidad disponible. «Reducir posición» no siempre reduce riesgo global si se cierra una cobertura. Precisar este caso con el operador. |
| Exención de reequilibrio | EN DESACUERDO | La exención genérica por etiqueta no es defendible ni está vigente. Un ciclo aprobado y acotado podría tener excepciones específicas, conservando límites globales, liquidez, autorización y kill-switch de entradas. |
| Política por cartera y tres niveles | DE ACUERDO CON CAMBIOS | Prevalece el límite más restrictivo aplicable; consumo agregado incluye pendientes. No reiniciar contadores con cierres, reaperturas o cambios de libro. |
| Estado solo desde G conciliado | DE ACUERDO CON CAMBIOS | Buena fuente autorizada, con respaldo de estados del intermediario, frescura y versión. No basta un objeto que declare estar conciliado. Incluir operaciones manuales y dudosas. |
| Mirar dentro de fondos y suplencia | DE ACUERDO CON CAMBIOS | Sí al detalle con fecha y cobertura. Rechazo asignar todo solo a región/divisa principal como prudencia universal: puede ocultar otra concentración. |
| Reducir por evento catalizador | DE ACUERDO CON CAMBIOS | Solo bajo política aprobada, calendario verificable y estrés específico. La palabra «catalizador» en una tesis no habilita excepción; no inventar fracción fija. |
| Medición I y batería de ataque | DE ACUERDO CON CAMBIOS | Añadir fallos raros, falsos negativos, indisponibilidad y resistencia a suplantación. No retirar controles por no activarse ni declarar errado un veto porque luego habría ganado. |

## Hallazgos y mejoras prioritarias

**1. Asimetría ya mejorada, pero con límites semánticos.** El cambio 47 ya deduce la acción desde G, distingue exceso vendido, conserva matriz de autonomía y trata posición sin conciliar como error de forma. Son mejoras acertadas sobre la propuesta inicial. Falta exigir reducción contra cantidad libre tras órdenes pendientes: dos ventas separadas no pueden consumir dos veces la misma posición. Una reducción no habilita una reapertura posterior; la segunda operación pasa todos los controles.

Cerrar una cobertura puede bajar cantidad o exposición bruta y aumentar la pérdida de la cartera en un escenario adverso. No llamarlo automáticamente «bajar riesgo». Recomiendo que el operador defina conjuntos de cobertura, condiciones de cierre y permisos previos para esos casos; F puede verificar identificadores y cantidades sin depender de un modelo de correlación. Esto matiza el rumbo de asimetría aceptado y debe volver al operador antes de formalizarlo; no lo cambio unilateralmente.

**2. Proteger no es una etiqueta libre.** Verificar lado, instrumento, cantidad, posición protegida y tipo de orden admitido. Al sustituir una protección, no dejar la posición desprotegida por cancelar antes de confirmar la nueva, ni permitir dos órdenes que produzcan una posición inversa. G/SC-10 deben definir sustitución, confirmación y protección de solo reducción cuando exista. F conserva el límite de cantidad y permisos, aunque no aplique pérdidas o frecuencia como veto ordinario a esa acción.

**3. Reequilibrio: distinción normativa.** Constitución §8.11 exime de la rentabilidad mínima al plan; no concede por ello exención de pérdidas, eventos o concentración. El cambio 78 sigue PROPUESTO: lo restringe al ciclo de aportaciones, importe de la aportación y acercamiento al mandato, y su §9 aclara que el kill-switch sí lo bloquea. Reconozco ese avance. Añadir identificador único del ciclo, consumo agregado de la aportación, mandato aprobado vigente y controles globales independientes. Una orden aislada que acerca un peso no garantiza que el conjunto lo haga; tampoco puede repetirse hasta multiplicar la aportación.

**4. Reservas y permisos ligados a la orden final.** Autorización y reserva indivisibles, vinculadas a hash de la orden, versión de política/estado, cantidad restante y caducidad. Consumo por ejecuciones parciales y liberación tras confirmación, no ante silencio. CF-08 cubre compromisos visibles; el diseño debe garantizar que dos aprobaciones simultáneas no parten de la misma vista libre. Incluir fraccionamiento de órdenes, varios libros y múltiples intermediarios. Esto amplía el diseño de coordinación, sin reactivar T-74.

**5. Estado incierto y disponibilidad.** «Sin confirmación = no ejecutada» en Constitución §11 necesita precisarse para no liberar dinero o posición prematuramente. Distinguir estado desconocido de rechazo confirmado. Con conciliación rota se bloquean nuevas exposiciones y se escalan los casos; no cancelar protecciones nativas. Definir procedimiento autenticado de recuperación/cierre con información suficiente, sin usar la falta de datos como permiso de acción automática.

**6. Exposición desconocida.** Un fondo mayoritariamente de una región también puede agravar la exposición ya alta a otra. Sin composición, etiquetar desconocido, conservar la parte conocida y presupuestar la parte no cubierta de forma conservadora por dimensión relevante; si no se puede justificar un margen seguro para una entrada, no promoverla automáticamente. Divisa de cotización, divisa de activos y cobertura de divisa no son intercambiables. Sumar niveles de un mismo fondo sin distinguir jerarquías también duplica exposición.

**7. Evaluación de un control.** La frase «uno que nunca se toca no protege» es incorrecta como criterio general: un límite puede evitar accidentes raros o disuadir propuestas inválidas. Medir cobertura de peligros, defectos inyectados, falsos positivos/negativos y coste operativo además de rentabilidad contrafactual. Un veto correcto puede impedir una operación que gana; una entrada indebida puede ganar por suerte. El control se juzga respecto a su mandato y evidencia disponible en ese momento. Mantener catálogo mínimo de controles obligatorios aunque falte muestra de incidentes reales.

**8. Endurecer y rehabilitar.** La respuesta automática inmediata debe estar en una política preaprobada, no ser una nueva regla inventada por I o un agente. La matriz de §6 y P8 sigue vigente; rehabilitación manual donde la Constitución la exige. La decisión del operador E3 mantiene aprobación de cambios al principio. T-74 ya incluye volumen, liquidez, costes/margen, exposiciones compartidas y políticas por cartera: no presentar esos cinco asuntos como descubrimientos nuevos.

## Aritmética y alcance de la protección

La recuperación tras pérdida `L` es `L/(1−L)`: 10 % exige 11,11 %, 20 % exige 25 %, 50 % exige 100 % y 75 % exige 300 %. Para 33 % es 49,25 %; 50 % exacto correspondería a 33⅓ %. La tabla es orientativa con redondeos.

«Cortar las colas sin tocar el centro» es una aspiración, no una propiedad demostrada. Límites y stops no garantizan recuperación ni pérdida máxima ante saltos, falta de liquidez o fallo de infraestructura. F puede acotar exposición y acciones permitidas; el plan debe declarar el riesgo residual y probar escenarios adversos sin prometer eliminarlo.

## Respuestas a las seis preguntas

1. Sí al rumbo de facilitar reducciones y protecciones, conservando deducción desde G, permisos y cantidad libre; resolver explícitamente el cierre de coberturas.
2. No a exención general. Considerar únicamente excepciones concretas del ciclo aprobado, manteniendo límites globales y bloqueo de entradas por kill-switch; el cambio 78 aún requiere ratificación.
3. Sí a política por cartera más global, con consumo conjunto y versiones. No incluyo valores privados del operador.
4. Reducción por evento solo si política y estrés la justifican; la fracción debe validarse por instrumento y tipo de evento, no salir del texto de una tesis.
5. Sí a escenarios de hueco como límite adicional conservador; un salto supuesto no es el peor salto posible ni una garantía de pérdida.
6. No a toda la exposición en región/divisa principal como sustituto universal. Cobertura conocida más incertidumbre explícita, y restricciones prudentes sobre nuevas exposiciones mientras falten datos.

No se modifican F, contratos ni T-74. Publicación suspendida: entregable, diario y estado quedan en local.

### Nota de contraste con G · 12-11-2026

Al preparar la revisión siguiente, el Documento 0 `sistema_global/documentos_0/V0.20_Cartera_real_y_euros.md` confirma que la foto de G desde el intermediario, su registro vigente y la suma de autorizaciones pendientes ya se incorporaron al marco (T-11/T-10). Por tanto, la propuesta de F no debe presentar toda esa conexión como inexistente. Lo pendiente es asegurar su funcionamiento con fuente real y actores autenticados, y precisar las garantías de concurrencia y conciliación: esta revisión no acredita su ausencia completa ni sustituye una QA de esos recorridos.
