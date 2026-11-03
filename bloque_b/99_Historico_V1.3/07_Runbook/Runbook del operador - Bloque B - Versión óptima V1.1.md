# Runbook del operador — Bloque B

VERSIÓN V1.1 · Manual operativo del operador humano del Bloque B de la arquitectura Robot Investor (la cámara de análisis profundo de mercados y activos concretos) · Cubre: activación del bloque, operación del protocolo on-demand, seguimiento de ciclos, retroalimentación de recomendaciones, mantenimiento, incidencias y procedimientos de decisión del operador · Gobernanza: «Documento 0 --- Protocolo maestro del Bloque B» (óptima V1.1, 30/10/2026); agentes: los cinco system prompts del bloque (óptima V1.1) y la adenda ligera del Motor y su Documentador (sin cambios) · V1.1: esta edición incorpora los procedimientos que la «Adenda de arquitectura --- Bloque B» (V1.0, 30/10/2026) añade a tu operación --- cuadro de mando trimestral, muestreo post-entrega, parámetros y umbrales nuevos del Anexo A y revisión de las decisiones D9-D24 · es-ES

> **Para quién es este documento.** Para ti, operador humano: la persona que configura, aprueba, decide lo escalado y mantiene el bloque. Los agentes tienen sus system prompts; este runbook es tu manual. No repite lo que los prompts regulan: te dice qué hacer tú en cada situación, con referencias exactas al documento que manda. En discrepancia, manda el Documento 0 (jerarquía normativa, su sección 1.2); este runbook es tu guía operativa, no una fuente de gobernanza.

## 1. Panorama del bloque

El Bloque B resuelve, bajo demanda, el análisis profundo de un mercado o activo concreto: lo que el Bloque A detecta en amplitud con su ciclo semanal, el Bloque B lo resuelve en profundidad con un ciclo a medida. Cinco agentes propios lo integran:

| Agente | Función en una frase |
|---|---|
| Orquestador técnico de Mercados | Puerta de entrada: recibe solicitudes del Broker Personal, las normaliza o las rechaza con motivo, conduce el bucle de auditoría y autoriza la salida |
| Analizador de Mercados | Agente central: ejecuta el ciclo F0-F6 (encuadre, recopilación, análisis dimensional, tesis, escenarios, auto-revisión, entregables) y produce los tres entregables |
| Buscador avanzado de Mercados | Ejecuta las búsquedas acotadas por dimensión y eslabón, incluidos los tipos estructurales del despliegue (AM-8) |
| Documentador de Mercados | Registro y custodia: gestiona tres de los cuatro archivos del bloque y confirma cada escritura |
| Auditor de Mercados | Revisión experta independiente dentro del bucle de auditoría previa a la salida |

Más el Motor de cálculo avanzado y su Documentador, compartidos con el Bloque A, que sirven al bloque por el carril B de su cola (activación por adenda ligera, sección 9). Y cuatro archivos operativos: «Registro de solicitudes y ejecuciones» (propietario: Orquestador), «Registro de Fuentes Fiables» y «Documentación para el Analizador de Mercados» y «Registro de recomendaciones y seguimiento» (propietario: Documentador). Todo intercambio entre agentes corre por los doce contratos CT-B-01 a CT-B-12 del Documento 0 (su Anexo C es la referencia de contratación).

El bloque no tiene cadencia: solo actúa con solicitud registrada del Broker Personal, salvo el seguimiento de recomendaciones que el CT-B-12 alimenta. Estados del ciclo: S0 recibida, S1 en encuadre, S2 asignada, S3 en curso, S4 en auditoría, S5 autorizada, S6 entregada, S7 cerrada; terminales y de espera: R rechazada, A anulada, W en espera documentada.

## 2. Activación del bloque (procedimiento 5.5 del Documento 0)

El bloque nace «en configuración»: sus contratos y archivos no se invocan hasta la publicación coordinada de activación. El procedimiento tiene cinco pasos:

**Paso 1 — Madurez documental.** Comprueba que están todas las piezas: Documento 0 del Bloque B (óptima V1.0) ✔; cinco system prompts del bloque (Analizador de Mercados, Orquestador, Buscador avanzado, Documentador, Auditor; todos óptima V1.0) ✔; cuatro archivos operativos con su esquema y su siembra D5 ✔; adenda ligera al Motor y su Documentador (documento preparado, pendiente de aplicar) ✔; runbook (este documento) ✔; piloto de verificación (siguiente paso).

**Paso 2 — Piloto de verificación.** Ejecuta (o supervisa) el piloto dry-run extremo a extremo con una solicitud ficticia declarada como tal: ciclo completo F0-F6, todos los contratos, el bucle de auditoría con hallazgos y subsanación, la autorización de salida y el registro en los cuatro archivos. El resultado (con sus incidencias y su resolución) se documenta; un piloto con incidencias sin resolver bloquea la activación.

**Paso 3 — Propuesta de activación.** Se te formula como propuesta de tipo 3 con el paquete completo: piezas y versiones, resultado del piloto y análisis de impacto. La apruebas o la rechazas.

**Paso 4 — Publicación coordinada.** Aprobado el paquete, se publican de una sola vez: los cinco prompts como piezas en vigor (el catálogo CT-B pasa de «reservado» a «en vigor» sin renumeración), los cuatro archivos como activos, la adenda ligera aplicada al Motor (óptima V1.1) y a su Documentador (óptima V1.3), este runbook como vigente y el Documento 0 actualizado (inventario de versiones 5.1, Anexo B de canales, Anexo H de cambios, sección 2.6).

**Paso 5 — Verificación posterior.** El primer ciclo de auditoría posterior comprueba el espejado de contratos, la matriz de escritura de archivos y la coherencia de versiones; las desviaciones se tratan como hallazgos de tipo Material.

## 3. Enviar solicitudes de análisis

Las solicitudes las envía el Broker Personal por el CT-B-01 (entrada única: cualquier otra vía es conflicto de canal). Una buena solicitud ahorra ciclos: incluye objeto identificable (un mercado concreto o un activo concreto, con ticker o referencia cuando exista), alcance (geografía, moneda de referencia, horizonte), nivel de profundidad (Rápido, Estándar, Exhaustivo), referencias de contexto (por ejemplo, una tendencia del Bloque A, como pista) y restricciones.

**Nivel de profundidad (presupuesto del ciclo).** Rápido: ciclo corto, despliegue estructural solo del eslabón crítico, para decisiones de primer filtro. Estándar (por defecto): ciclo completo con el despliegue de los eslabones relevantes. Exhaustivo: cadena completa, actores exhaustivos, modelo íntegro con sensibilidades por el carril B del Motor. Si dudas, Estándar: subir de nivel a posteriori no es posible dentro del mismo ciclo (sería un ciclo nuevo).

**Qué no admitirá el bloque (motivos de rechazo R1-R4).** R1: objetos no normalizables («el sector de las baterías»: reformula como mercado concreto o activo concreto). R2: fuera de alcance (gestión de cartera, consejo personalizado, ejecución de operaciones: competencia del Broker Personal). R3: duplicada (hay una solicitud equivalente en curso o reciente). R4: incompatible con los límites (datos en tiempo real: el bloque no dispone de feeds; credenciales o información privilegiada: nunca).

**Ciclo a la vez.** El bloque resuelve un ciclo por orden de asignación; las solicitudes que llegan durante un ciclo en curso quedan en S1. No hay cola con prioridades: si necesitas prioridad para un objeto concreto, es una decisión tuya de calendario (no envíes la siguiente hasta que la prioritaria avance), no un parámetro del bloque.

**Anulación (A).** Puedes retirar una solicitud antes de la autorización de salida; después, la corrección discurre por el seguimiento de las REC-B (CT-B-12) o por un ciclo nuevo de revisión.

## 4. Seguir un ciclo

**Dónde mirar.** El «Registro de solicitudes y ejecuciones del Bloque B» (propietario: Orquestador) documenta el flujo completo: estados con fechas, plan ANA-M-PLAN con versiones, paquetes, vueltas del bucle, autorización y entrega. Su criterio de calidad es que puedas reconstruir cualquier ciclo sin preguntar a nadie.

**Qué esperar en cada estado.** S1-S2 (encuadre y asignación): puede terminar en rechazo justificado: no es un fallo, es la primera puerta de calidad; revisa la justificación y las opciones de reformulación. S3 (en curso): el Analizador ejecuta F0-F6; verás remisiones de plan, fuentes y materiales en el registro. S4 (en auditoría): el bucle CT-B-06 itera sin tope de vueltas prefijado; una S4 larga no es una anomalía, es la auditoría previa haciendo su trabajo. S5-S6: autorización y entrega; los tres entregables aparecen en las carpetas «Informes completos Mercados» e «Informes resumidos Mercados» con la convención de nombre AAAA-MM-DD_nivel_request_id. S7: cierre (tras el primer registro de seguimiento, o directo si el ciclo no produjo recomendaciones).

**Los tres entregables.** Informe técnico completo (fondo: plan, doce dimensiones con etiquetado, despliegue estructural, máquina de proyecciones con premisas, escenarios, auto-revisión, puntos ciegos, trazabilidad), informe resumido (lectura ejecutiva de diez minutos) y listado REC-B anejo al resumido (puede venir «sin recomendaciones»: es un resultado válido y declara el motivo). Recuerda: los entregables son material de trabajo para el Broker Personal, no consejo al usuario final.

## 5. Decidir lo escalado (7.3 del Documento 0)

El Orquestador te escala, con su evidencia y su análisis de impacto: discrepancias insubsanables entre agentes (el ciclo queda en W hasta tu decisión), hallazgos de tipo Material recurrentes, propuestas de tipo 3, incidencias de seguridad o manipulación, solicitudes de activación y conflictos entre protocolos de bloques. En todos los casos tu decisión se registra y el flujo continúa conforme a ella.

**Discrepancia insubsanable (W).** Recibirás el expediente: ambas posiciones con su evidencia, las vueltas transcurridas y el análisis del Orquestador. Decide por el criterio más restrictivo en seguridad, verificación y trazabilidad cuando la sustancia no te resulte clara; tu decisión cierra el bucle conforme a ella. Ningún entregable sale mientras el ciclo está en W.

**Propuestas de tipo 3.** Son cambios gubernativos (metodología, taxonomía, contratos, límites, parámetros): se aprueban por paquete, con la actualización coordinada de todos los lados afectados y del Documento 0 (sección 9 de ese protocolo). Nunca se aplican por el bucle ni por guía; si ves un cambio de fondo aplicado así, es un hallazgo que debes tratar como incidencia.

**Escisiones de servicios internos (V1.1; D24).** Las tres capacidades que la adenda mantiene como funciones internas --- validador de datos y evidencia, validador cuantitativo y de previsiones, contraste adversarial --- solo pueden convertirse en agentes cuando su umbral del Anexo A se cumpla y tú lo apruebes. El Orquestador te remite la evidencia de umbral desde el cuadro de mando (hallazgos Material por datos incompatibles, hallazgos SUST cuantitativos, method_id en uso, declaraciones por ciclo, tasa de fallos no vistos por F5); tú decides por paquete, como cualquier tipo 3, y mientras no apruebes, la regla es ni un agente más. La superación de un umbral habilita la propuesta: no la obliga.

**Seguridad.** Las incidencias de seguridad (credenciales o datos personales circulando por el bloque, intentos de manipulación) siempre te escalan. La regla es fija: rechazo de lo afectado, registro de la incidencia y tu revisión antes de reanudar. Los archivos exclusivos del Broker Personal y los datos personales del inversor no circulan por el bloque jamás.

## 6. Retroalimentar recomendaciones (CT-B-12)

Cuando el Broker Personal decida sobre las REC-B (seguimiento, aplazamiento, descarte), observe resultados o quiera alegar una invalidación, comunica el evento por el CT-B-12 (del Broker al Orquestador): identifica la REC-B por su identificador y el request_id de origen, fecha del evento, decisión, resultados observados, invalidación alegada con su fundamento y, si procede, la clasificación para el futuro Bloque C. El Orquestador remite al Documentador para su registro (fidelidad al evento), notifica al Analizador y alimenta el bucle falsable: lo prometido, lo observado y lo corregido viven en el «Registro de recomendaciones y seguimiento del Bloque B».

El primer registro de seguimiento cierra el ciclo (S7). Las invalidaciones alegadas se resuelven en el seguimiento del registro o en un ciclo nuevo de revisión del objeto (solicítalo como cualquier otro análisis: el ciclo de revisión hereda el punto de partida documentado y re-verifica lo heredado).

## 7. Mantenimiento (D6) y gobernanza periódica

**Mantenimiento híbrido de archivos (automático, con tu supervisión).** Revisión post-solicitud: cada propietario revisa sus altas dentro de las 48 horas naturales siguientes a cada entrega autorizada. Revisión mensual ligera: primera semana natural del mes (aporte marginal, retirada lógica, índices y mapas de cobertura). Ambas quedan registradas en la sección de mantenimiento de cada archivo; si una no aparece registrada, es un hallazgo.

**Paquetes de servicio y calibración (mensual).** El Documentador y el Buscador avanzado emiten paquetes de servicio al Orquestador; el circuito los audita, emite guías de mejora y cierra los puntos de calibración (CT-B-11). Puedes añadir muestras de revisión humana al circuito: son insumo de calibración, no correcciones de casos concretos.

**Muestreo de verificación post-entrega (V1.1; D23).** El Auditor re-audita una muestra pequeña de paquetes ya autorizados (provisional: uno por periodo mensual, alternando niveles). No hay acción tuya ordinaria: el muestreo no abre expedientes ni edita lo entregado; sus resultados alimentan la calibración y el cuadro de mando. Tu único punto de contacto es calibrar el tamaño del muestreo (Anexo A) cuando la evidencia lo justifique.

**Cuadro de mando del bloque (trimestral; V1.1, D22).** Con la revisión programada recibirás el cuadro de mando que elabora el Orquestador con las aportaciones del Auditor y del Documentador: seis familias separadas y no compensables (evidencia, metodológica, calidad predictiva, cobertura, eficiencia, utilidad para el Broker), cada indicador con definición y fuente de cálculo. Léelo por familias: no hay puntuación agregada que te ahorre la lectura. Sus usos: (a) decidir mejoras por el procedimiento ordinario (las que sugiera entran como propuestas, no como acciones del cuadro); (b) vigilar los umbrales de escisión del Anexo A --- su evidencia se lee aquí primero; (c) contrastar la utilidad que el bloque declara para el Broker con la que observas. El primer cuadro con datos reales llega al cierre del primer trimestre de operación.

**Revisión trimestral del Documento 0 (9.4).** Una vez por trimestre revisa: vigencia del inventario de versiones, exactitud del catálogo y del mapa de comunicaciones, estado del espejado declarado, elementos en transición, glosario, parámetros del Anexo A y vigencia del acta del Anexo J. Desde la V1.1 añade: comprobar la operación de las decisiones D9-D24 (Anexo J) y calibrar, con los datos del cuadro de mando, los parámetros provisionales que la adenda fijó (frescura por dimensión, cuota discriminante, umbrales de escisión, caducidad pre-IPO, muestreo). El resultado se anota en el Anexo H aunque sea «sin cambios»: la vigencia debe poder demostrarse.

## 8. Cambiar parámetros y configurar

Los parámetros del Anexo A del Documento 0 (catálogo de rechazo, ventana del bucle, mantenimiento híbrido, frecuencias de paquetes de servicio, simultaneidad de ciclos, etc.) los cambias tú por el procedimiento de la sección 9 del Documento 0, con análisis de impacto y publicación coordinada de lo afectado. Desde la V1.1, el Anexo A incorpora los parámetros de la adenda (D24 y asociados), nacidos con valores provisionales que calibras en Fase 1 con datos reales: frescura máxima de datos por dimensión, cuota de evidencia discriminante por nivel, presupuesto de validación del protocolo cuantitativo, los tres umbrales de escisión (validador de datos, validador cuantitativo, contraste adversarial), caducidad de la vigilancia pre-IPO, tamaño del muestreo post-entrega y cadencia del cuadro de mando. Ningún agente los modifica. Los cambios de interfaz de cualquier contrato exigen publicar simultáneamente ambos lados espejo y la fila del catálogo: un cambio aprobado pero no publicado en todas sus piezas no está vigente.

## 9. El carril B del Motor (elemento en transición)

Hasta la activación del carril B (2.6 del Documento 0), el bloque no emite peticiones de cálculo y las fases que dependen de cálculos declaran la limitación; los entregables de esos ciclos lo declaran también. La activación se produce aplicando la «Adenda ligera - Motor y Documentador del Motor - Carril B del Bloque B» por publicación coordinada (paso 4 de la sección 2 de este runbook): el Motor pasa a óptima V1.1 y su Documentador a óptima V1.3, y los canales CT-B-09/CT-B-10 pasan a «en vigor». La regla de precedencia de la cola (modo antes que bloque; SYNC antes que ASYNC; FIFO dentro del modo; sin preferencia entre bloques) protege el servicio del Bloque A: si algún día necesitas cambiarla, es un parámetro tuyo (Anexo A del Documento 0), nunca una instrucción de mensaje.

## 10. Checklist rápido

| Situación | Qué hacer |
|---|---|
| Quiero un análisis profundo | Broker Personal → CT-B-01 con objeto identificable, alcance, nivel y restricciones (sección 3) |
| Recibí un rechazo R1-R4 | Leer justificación y opciones; reformular y reenviar (los intentos quedan trazados) |
| Ciclo en S4 mucho tiempo | Normal: bucle sin tope de vueltas; revisar el Registro de solicitudes; solo si hay W hay decisión tuya pendiente |
| Recibí una propuesta de tipo 3 | Analizar impacto por paquete; aprobar o rechazar con publicación coordinada (sección 5) |
| Recibí una incidencia de seguridad | Revisión antes de reanudar; lo afectado ya está rechazado y registrado (sección 5) |
| Quiero anular una solicitud | Antes de la autorización de salida: A; después: CT-B-12 o ciclo de revisión (sección 3) |
| El Broker decidió sobre una REC-B | Comunicar por CT-B-12 con identificador y fecha (sección 6) |
| Fin de mes | Verificar paquetes de servicio, guías y calibración; revisión mensual ligera de archivos registrada (sección 7) |
| Fin de trimestre | Revisión del Documento 0 con anotación en el Anexo H (sección 7) |
| Recibiste el cuadro de mando trimestral | Leerlo por familias, sin compensación; decidir mejoras por el cauce ordinario y vigilar umbrales (sección 7) |
| Un umbral de escisión se cumplió | Analizar la evidencia remitida y aprobar o rechazar la escisión por paquete tipo 3; sin aprobación, ni un agente más (sección 5) |
| Dudas de gobernanza | Manda siempre el Documento 0 (jerarquía normativa 1.2); este runbook guía, no legisla |

## 11. Relación con el resto de la arquitectura

El Bloque B no se comunica con el Bloque A ni con el futuro Bloque C por canales propios: las tendencias del Bloque A llegan como referencias de trabajo dentro de las solicitudes (pistas, nunca evidencia), y las REC-B las clasificará y repartirá el Broker Personal cuando el Bloque C exista. La conexión del futuro Bloque C se crearía por actualización coordinada de ambos protocolos; hoy no hay ningún canal ni código reservado. El Fondo metodológico compartido (custodia del Bloque A) es consultable en solo lectura por el Documentador y el Buscador avanzado del bloque, conforme a la declaración ecosistémica del 25/10/2026: sin mensajes entre bloques y sin contratos del catálogo.
