# Catálogo de códigos del marco común de C (V0.61)

Generado por `validador/catalogo_codigos.como_markdown()` (pieza 2 del kit 2). Una fila por cada
pareja (módulo, código) de `CATALOGO`: las 281 que aparecen como constantes de texto enteras en los
módulos de `validador/` más E-06, retirada en CT-G-01 0.2.0. Los avisos del Orquestador llevan su
prioridad (MEDIA si no figura en PRIORIDAD_AVISO); «Desde» queda vacío en todas las filas (ver
Documento 0, §2 punto 4).

| Módulo | Código | Qué hace | Efecto | Prioridad | Desde | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `comparador` | `D-01` | entrada inválida | RECHAZA |  |  |  |
| `contratos` | `CT-01` | falta el tipo de mensaje o su versión | RECHAZA |  |  |  |
| `contratos` | `CT-02` | no tiene esquema para la versión (vigente ) | RECHAZA |  |  |  |
| `contratos` | `CT-03` | no cumple el esquema (ruta y motivo) | RECHAZA |  |  |  |
| `contratos` | `CT-04` | vence antes de emitirse | RECHAZA |  |  |  |
| `control_f` | `CF-01` | la envoltura del informe de F no es válida (versión, campos o entrada mal formados) | RECHAZA |  |  |  |
| `control_f` | `CF-02` | el informe no corresponde a esta propuesta (expediente, petición o hash) | RECHAZA |  |  |  |
| `control_f` | `CF-03` | el informe debe estar emitido, vigente y no durar más que la política | RECHAZA |  |  |  |
| `control_f` | `CF-04` | el resultado (o su motivo) no es el que dan las reglas con esas entradas | RECHAZA |  |  |  |
| `control_f` | `CF-05` | la solicitud no coincide con la propuesta (límite, stop, dirección, cartera, instrumento, activo base, divisa de cotización, apalancamiento y cantidad | RECHAZA |  |  |  |
| `control_f` | `CF-06` | no se puede aprobar más de lo solicitado | RECHAZA |  |  |  |
| `control_f` | `CF-07` | la política usada no es la oficial del Orquestador | RECHAZA |  |  |  |
| `control_f` | `CF-08` | la cartera del informe omite una posición o autorización ya comprometida | RECHAZA |  |  |  |
| `control_f` | `CF-09` | el contexto del informe no es el del Orquestador (mandato, evidencia, eventos, autonomía, actividad o precio) | RECHAZA |  |  |  |
| `control_f` | `F-01` | error de cálculo al aplicar el control: la orden sale VETADA | BLOQUEA |  |  |  |
| `control_f` | `F-02` | el stop no está del lado de la pérdida | BLOQUEA |  |  |  |
| `control_f` | `F-03` | el riesgo delante del stop supera el riesgo máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `control_f` | `F-04` | el tamaño supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `control_f` | `F-05` | el apalancamiento supera el máximo de la política | BLOQUEA |  |  |  |
| `control_f` | `F-06` | la exposición total supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `control_f` | `F-07` | la concentración en un activo supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `control_f` | `F-08` | la pérdida del día alcanzó el límite de la política | BLOQUEA |  |  |  |
| `control_f` | `F-09` | más posiciones abiertas que el máximo de la política | BLOQUEA |  |  |  |
| `control_f` | `F-10` | el estado de la cartera está viejo o en el futuro | BLOQUEA |  |  |  |
| `control_f` | `F-11` | el valor de la orden queda por debajo del mínimo de la política | BLOQUEA |  |  |  |
| `control_f` | `F-12` | sin tipo de cambio a euros para la divisa de cotización | BLOQUEA |  |  |  |
| `control_f` | `F-13` | el importe de la orden en euros supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `control_f` | `F-14` | el importe del día en euros supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `control_f` | `F-15` | el importe del activo en euros supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `control_f` | `F-16` | la pérdida del día o de la semana en euros supera el máximo de la política | BLOQUEA |  |  |  |
| `control_f` | `F-17` | demasiadas órdenes en la última hora | BLOQUEA |  |  |  |
| `control_f` | `F-18` | la orden no encaja en el mandato efectivo del contexto | BLOQUEA |  |  |  |
| `control_f` | `F-19` | el instrumento está en las exclusiones duras del contexto | BLOQUEA |  |  |  |
| `control_f` | `F-20` | la evidencia verificada queda por debajo del mínimo de la política | BLOQUEA |  |  |  |
| `control_f` | `F-21` | el calendario de eventos no se puede leer | BLOQUEA |  |  |  |
| `control_f` | `F-22` | la autonomía (nivel, kill-switch u horario) no permite ejecutar la orden | BLOQUEA |  |  |  |
| `control_f` | `F-23` | sin precio del intermediario para el instrumento | BLOQUEA |  |  |  |
| `diario` | `DI-01` | los argumentos de la operación no se pueden guardar tal cual en el diario: no se aplica | RECHAZA |  |  |  |
| `diario` | `DI-02` | línea del diario ilegible, con su hash roto o sin la firma esperada | RECHAZA |  |  |  |
| `diario` | `DI-03` | el diario no tiene un punto de control para el estado guardado | RECHAZA |  |  |  |
| `diario` | `DI-04` | el estado reaplicado no es el del punto de control anotado (el código o los datos cambiaron) | RECHAZA |  |  |  |
| `diario` | `DI-05` | no se pudo escribir en el diario: no se aplica y queda bloqueado hasta reabrirlo | BLOQUEA |  |  |  |
| `diario` | `DI-06` | el diario cambió por fuera: no se aplica nada más; reábrelo para volver al estado anotado | BLOQUEA |  |  |  |
| `diario` | `O-00` | operación que lanzó una excepción no recogida: se anota y se reproduce igual | RECHAZA |  |  |  |
| `diario` | `O-13` | el expediente o la posición vinculados no son íntegros (historial, sobre, propuesta, orden, aprobación o estado) | AVISO |  |  |  |
| `diario` | `PE-01` | no se puede volcar el estado | RECHAZA |  |  |  |
| `diario` | `PE-05` | el estado pasa de bytes: no se hace el punto | RECHAZA |  |  |  |
| `diario` | `PE-07` | la clave debe tener al menos bytes | RECHAZA |  |  |  |
| `dimensionado` | `E-01` | la solicitud debe llevar exactamente los campos exigidos y no una cantidad | RECHAZA |  |  |  |
| `dimensionado` | `E-02` | el stop debe estar del lado de la pérdida y la dirección ser LARGO o CORTO | RECHAZA |  |  |  |
| `dimensionado` | `E-03` | F vetaría: no hay tipo de cambio a euros para la divisa de cotización | RECHAZA |  |  |  |
| `dimensionado` | `E-04` | no hay una cantidad viable por encima del paso y del valor mínimo | RECHAZA |  |  |  |
| `dimensionado` | `F-01` | error de cálculo al aplicar el control: la orden sale VETADA | BLOQUEA |  |  |  |
| `dimensionado` | `F-11` | el valor de la orden queda por debajo del mínimo de la política | BLOQUEA |  |  |  |
| `dimensionado` | `F-12` | sin tipo de cambio a euros para la divisa de cotización | BLOQUEA |  |  |  |
| `ejecucion_g` | `G-01` | sin conexión con el intermediario; la posición sigue y se puede reintentar | RECHAZA |  |  |  |
| `ejecucion_g` | `G-02` | la orden de entrada no llegó al intermediario; se anota como rechazada | RECHAZA |  |  |  |
| `ejecucion_g` | `G-03` | el intermediario no confirma la vía de acceso autorizada | RECHAZA |  |  |  |
| `ejecucion_g` | `G-04` | cierre crítico: la posición no se pudo cerrar | RECHAZA |  |  |  |
| `ejecucion_g` | `G-05` | el Orquestador rechazó la ejecución | RECHAZA |  |  |  |
| `ejecucion_g` | `G-06` | la autorización ya no vale (fue automática y la cartera bajó de nivel, se degradó después o ya no la permite el umbral o el horario, o después se bajó | RECHAZA |  |  |  |
| `ejecucion_g` | `G-08` | fallo con órdenes ya enviadas: estado incierto, hay que conciliar con el intermediario | RECHAZA |  |  |  |
| `ejecucion_g` | `G-09` | cierre no completado; la posición sigue CERRANDO | RECHAZA |  |  |  |
| `ejecucion_g` | `G-10` | la orden de protección declarada no es un stop vivo en el intermediario por lo que queda (lado contrario a la posición, mismo instrumento y vía, canti | RECHAZA |  |  |  |
| `ejecucion_g` | `G-11` | orden de entrada viva hasta su caducidad en el intermediario | INFORMA |  |  |  |
| `ejecucion_g` | `G-12` | reducción no completada; la posición sigue REDUCIENDO con su stop anterior | RECHAZA |  |  |  |
| `ejecucion_g` | `O-01` | el intermediario no da precio para el instrumento o el instante es ilegible | RECHAZA |  |  |  |
| `k_calidad` | `K-00` | entrada o contexto mal formado | BLOQUEA |  |  |  |
| `k_calidad` | `Q-01` | la fecha solicitada no es día hábil en el mercado; se recorta al hábil anterior | AVISO |  |  |  |
| `k_calidad` | `Q-02` | no hay ninguna fuente disponible | BLOQUEA |  |  |  |
| `k_calidad` | `Q-03` | un valor ausente, no numérico, no finito o no positivo | BLOQUEA |  |  |  |
| `k_calidad` | `Q-04` | salto del precio mayor que el umbral de la política (advirtiendo o bloqueando según su factor) | BLOQUEA |  |  |  |
| `k_calidad` | `Q-05` | faltan días hábiles en la ventana de la política | BLOQUEA |  |  |  |
| `k_calidad` | `Q-06` | fechas repetidas o fuera de orden | BLOQUEA |  |  |  |
| `k_calidad` | `Q-07` | una barra incoherente (máximo, mínimo, cierre o volumen) | BLOQUEA |  |  |  |
| `k_calidad` | `Q-08` | ajustes sin versión | BLOQUEA |  |  |  |
| `k_calidad` | `Q-09` | mercado FX sin cruces definidos: coherencia no comprobada | BLOQUEA |  |  |  |
| `k_calidad` | `Q-10` | un dato crítico sin fuente de contraste disponible | AVISO |  |  |  |
| `k_calidad` | `Q-11` | excepción al calcular la calidad: el sello sale BLOQUEADO (falla cerrado) | BLOQUEA |  |  |  |
| `k_calidad` | `Q-12` | el hash declarado de los datos no coincide con el contenido | BLOQUEA |  |  |  |
| `k_calidad` | `Q-13` | el corte es posterior a la fecha de emisión | BLOQUEA |  |  |  |
| `k_calidad` | `Q-14` | procedencia incompleta, licencia no admitida o dato posterior a su obtención | BLOQUEA |  |  |  |
| `k_calidad` | `Q-15` | eventos mal formados o anunciados después de emitir el sello | BLOQUEA |  |  |  |
| `k_calidad` | `S-01` | el sello no es un objeto | RECHAZA |  |  |  |
| `k_calidad` | `S-02` | la fecha del identificador no coincide con fecha_corte | RECHAZA |  |  |  |
| `k_calidad` | `S-03` | el resultado_global no es el peor de los resultados de sus reglas | RECHAZA |  |  |  |
| `k_calidad` | `S-04` | las reglas Q-01 a Q-15 deben figurar exactamente una vez | RECHAZA |  |  |  |
| `k_calidad` | `S-05` | mercado repetido | RECHAZA |  |  |  |
| `k_calidad` | `S-06` | el corte no puede ser posterior a la fecha solicitada | RECHAZA |  |  |  |
| `k_calidad` | `S-07` | un sello no puede reemplazarse a sí mismo | RECHAZA |  |  |  |
| `k_calidad` | `S-08` | el sello está ANULADO | RECHAZA |  |  |  |
| `k_calidad` | `S-09` | una ADVERTENCIA debe llevar detalle | RECHAZA |  |  |  |
| `k_calidad` | `S-10` | el corte del sello no es día hábil de sus mercados | RECHAZA |  |  |  |
| `k_calidad` | `S-11` | versión de esquema desconocida | RECHAZA |  |  |  |
| `k_calidad` | `S-12` | el hash no corresponde al contenido del sello | RECHAZA |  |  |  |
| `k_calidad` | `S-13` | Q-01 debe ser ADVERTENCIA si y solo si el corte difiere de la fecha solicitada | RECHAZA |  |  |  |
| `k_calidad` | `S-14` | la fecha de obtención de la procedencia no cuadra con el cierre (fuentes.procedencia.obtenido_en) | RECHAZA |  |  |  |
| `mandatos` | `E-01` | las restricciones del encargo no pasan la forma que exige SC-1 (claves o lista) | RECHAZA |  |  |  |
| `mandatos` | `E-05` | el horizonte de las restricciones es más amplio que el del mandato | RECHAZA |  |  |  |
| `mandatos` | `E-07` | el tamaño de las restricciones es mayor que el del mandato | RECHAZA |  |  |  |
| `manual_g` | `RM-01` | envoltura inválida: campos, consumer G, valid_until nulo, payload o data_refs (las órdenes del payload) | RECHAZA |  |  |  |
| `manual_g` | `RM-02` | solo el operador declara ejecuciones manuales | RECHAZA |  |  |  |
| `manual_g` | `RM-03` | la ejecución es anterior a la autorización del expediente o a la apertura de la posición | RECHAZA |  |  |  |
| `manual_g` | `RM-04` | la posición no existe o no está ABIERTA, EN_REVISION ni REDUCIENDO | RECHAZA |  |  |  |
| `manual_g` | `RM-05` | la vía de acceso no es la de la propuesta autorizada (un futuro analizado no se opera como contado) | RECHAZA |  |  |  |
| `manual_g` | `RM-06` | una reducción parcial exige una cantidad positiva; para cerrarla entera se declara la cantidad exacta de la posición | RECHAZA |  |  |  |
| `manual_g` | `RM-07` | una reducción parcial exige declarar el stop nuevo que el operador ya colocó por lo que queda | RECHAZA |  |  |  |
| `manual_g` | `RM-08` | instrumento no admitido en esa cartera (lista o exclusiones del mandato) | RECHAZA |  |  |  |
| `manual_g` | `RM-09` | el precio se aleja del límite autorizado más de la tolerancia | RECHAZA |  |  |  |
| `manual_g` | `RM-10` | hay una posición abierta o un expediente autorizado en ese instrumento: vincule el registro a ellos | RECHAZA |  |  |  |
| `manual_g` | `RM-11` | la envoltura no identifica el caso del vínculo (expediente_id y correlation_id; nulos si es LIBRE) | RECHAZA |  |  |  |
| `manual_g` | `RM-12` | no se puede valorar en euros lo que queda (falta el mínimo de F o su tipo de cambio): ciérrala entera | RECHAZA |  |  |  |
| `migraciones` | `DI-02` | el diario no tiene ninguna línea completa | RECHAZA |  |  |  |
| `migraciones` | `MG-01` | no hay camino de migración desde el esquema guardado hasta el de este código, o el registro de migraciones está mal formado | RECHAZA |  |  |  |
| `migraciones` | `MG-02` | la configuración guardada no es la de su huella con el código que la guardó: se tocó; ábrelo con ese código | RECHAZA |  |  |  |
| `migraciones` | `MG-03` | la migración no devuelve un estado que JSON guarde tal cual | RECHAZA |  |  |  |
| `migraciones` | `MG-04` | la migración cambiaría lo que no declara o no se puede cambiar | RECHAZA |  |  |  |
| `migraciones` | `MG-05` | el instante de la migración es anterior al reloj del Orquestador | RECHAZA |  |  |  |
| `migraciones` | `MG-06` | el diario tiene operaciones después de su punto de control: ábrelo con el código que lo escribió y haz punto antes de migrar | RECHAZA |  |  |  |
| `migraciones` | `PE-01` | el estado a migrar debe ser texto | RECHAZA |  |  |  |
| `migraciones` | `PE-05` | no se pudo escribir la migración: ; vuelve a llamar a migrar_ficheros | RECHAZA |  |  |  |
| `orquestador` | `F-03` | el riesgo delante del stop supera el riesgo máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `orquestador` | `F-04` | el tamaño supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `orquestador` | `F-06` | la exposición total supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `orquestador` | `F-07` | la concentración en un activo supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `orquestador` | `F-09` | más posiciones abiertas que el máximo de la política | BLOQUEA |  |  |  |
| `orquestador` | `F-11` | el valor de la orden queda por debajo del mínimo de la política | BLOQUEA |  |  |  |
| `orquestador` | `F-13` | el importe de la orden en euros supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `orquestador` | `F-14` | el importe del día en euros supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `orquestador` | `F-15` | el importe del activo en euros supera el máximo de la política: recorta la cantidad | REDUCE |  |  |  |
| `orquestador` | `O-00` | fallo puntual de la operación pedida: un instante inválido o anterior al último, o una excepción no recogida al ejecutar la operación o al comprobar un registro manual; la operación no se aplica | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-01` | rechazo genérico de la operación pedida: entrada no admitida o condición incumplida; se emite en muchos caminos —entre ellos, resto_parcial distinto de CANCELAR— | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-02` | petición ya atendida o estado ya alcanzado (idempotencia): ya registrado, ya acusado, ya activo, ya configurado, ya ganador o sin nivel nuevo; no cambia nada | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-03` | ya hay otra orden de entrada para este expediente | AVISO | ALTA |  |  |
| `orquestador` | `O-04` | la posición no admite señales en su estado actual (solo abierta o en revisión) | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-05` | la autorización ya no vale (automática con la cartera por debajo de L2 o degradada después, o anterior a una bajada del límite de pérdida): vuelve a p | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-06` | hay operaciones libres declaradas abiertas en ese instrumento: no se mezclan con una posición del sistema | AVISO | MEDIA |  |  |
| `orquestador` | `O-07` | encargo incompleto por presupuesto: no se valida; reemitir o descartar | AVISO | MEDIA |  |  |
| `orquestador` | `O-08` | presupuesto diario agotado o comprometido: no se aceptan encargos nuevos | AVISO | ALTA |  |  |
| `orquestador` | `O-09` | máximo de reintentos sin avance; se avisa al operador | AVISO | ALTA |  |  |
| `orquestador` | `O-10` | la autorización fue automática y el sello del análisis ya no está vigente: la confirma el operador | AVISO | MEDIA |  |  |
| `orquestador` | `O-11` | fechas de corte distintas entre los candidatos: hay que actualizar datos | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-12` | el artefacto es de un modelo no declarado (o alterado) en el Motor | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-13` | el expediente o la posición vinculados no son íntegros (historial, sobre, propuesta, orden, aprobación o estado) | AVISO | ALTA |  |  |
| `orquestador` | `O-14` | CERRADA es un estado terminal | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-15` | la fecha de revisión ya llegó: confirmar la tesis exige fijar la siguiente | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-16` | el restablecimiento no puede ser anterior a la degradación | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-17` | objeción crítica: el expediente queda detenido hasta que el operador la levante o lo descarte | AVISO | ALTA |  |  |
| `orquestador` | `O-18` | diferencias de conciliación con el intermediario | AVISO | ALTA |  |  |
| `orquestador` | `O-19` | cartera degradada a L1 | AVISO | ALTA |  |  |
| `orquestador` | `O-20` | operación libre declarada fuera del sistema (sin control de F ni stop) | AVISO | MEDIA |  |  |
| `orquestador` | `O-21` | los precios del sobre (stop, límite, objetivo) no están en la divisa de cotización del instrumento | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-22` | solo se elige entre los aspirantes de una decisión ajustada (empatados, primeros con otra ponderación o cuando un apartado habría ganado) | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-23` | la solicitud de E no es la propuesta (instrumento, dirección, límite, stop, apalancamiento o cartera) | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-24` | el encargo no cita el mandato vigente de SC-1 para la cartera (versión y huella): pídalo con mandato | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-25` | hay una orden de entrada de G viva para este expediente: cancélela antes de ejecutar a mano | AVISO | ALTA |  |  |
| `orquestador` | `O-26` | la autorización es anterior a un kill-switch: hay que volver a aprobar | AVISO | ALTA |  |  |
| `orquestador` | `O-27` | la autorización del operador exige su aprobación: pantalla_hash, importe_tecleado, canal y segundo_factor | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-28` | la aprobación cae fuera de horario: espere el enfriamiento desde que se generó la pantalla | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-29` | la cartera no es la vigente: la última foto de G del intermediario más las autorizaciones pendientes | RECHAZA | MEDIA |  |  |
| `orquestador` | `O-30` | un candidato apartado habría ganado la comparación; decide el operador | AVISO | ALTA |  |  |
| `orquestador` | `O-31` | la observación venció sin reabrirse; queda descartado | AVISO | MEDIA |  |  |
| `orquestador` | `O-32` | sobre recibido como informe: exclusión dura BLOQUEADO; expediente descartado | AVISO | MEDIA |  |  |
| `orquestador` | `O-33` | sin diversidad de modelo o sin poder comprobar la autoría del Contradictor | AVISO | MEDIA |  |  |
| `orquestador` | `O-34` | el informe de F no trae sus topes de cantidad: no hay con qué acotar la anulación | AVISO | ALTA |  |  |
| `orquestador` | `O-35` | el límite de pérdida se alcanzó en las últimas 24 horas: no se puede subir (Constitución §6) | AVISO | ALTA |  |  |
| `orquestador` | `O-36` | el análisis usa un sello de K con advertencias (p. ej. dato de una sola fuente): autoriza el operador | AVISO | MEDIA |  |  |
| `orquestador` | `O-37` | tope diario de las LIBRES superado, o LIBRES sin poder valorar (T-33) | AVISO | ALTA |  |  |
| `orquestador` | `O-38` | cortacircuito global por pérdida del día o de la semana (T-40) | AVISO | ALTA |  |  |
| `orquestador` | `O-39` | se sube de un nivel en uno: cada nivel exige su periodo mínimo | AVISO | ALTA |  |  |
| `persistencia` | `O-13` | el estado cargado no cuadra : kill-switch activado | AVISO |  |  |  |
| `persistencia` | `PE-01` | el estado tiene valores que no se pueden poner en forma canónica | RECHAZA |  |  |  |
| `persistencia` | `PE-02` | la huella del estado no cuadra: el fichero está roto o se tocó a mano | RECHAZA |  |  |  |
| `persistencia` | `PE-03` | la versión de configuración del documento no es la de la configuración guardada | RECHAZA |  |  |  |
| `persistencia` | `PE-04` | a la configuración guardada le faltan claves de este código: hace falta una migración | RECHAZA |  |  |  |
| `persistencia` | `PE-05` | el estado pasa del tamaño máximo: no se guarda | RECHAZA |  |  |  |
| `persistencia` | `PE-06` | la firma del estado no es válida: se tocó con la clave o sin ella | RECHAZA |  |  |  |
| `persistencia` | `PE-07` | la clave de firma no es válida (longitud, fichero, permisos o lectura) | RECHAZA |  |  |  |
| `persistencia` | `PE-08` | el estado lo guardó otra versión del código (otro esquema): hay que migrarlo (migraciones.migrar) | RECHAZA |  |  |  |
| `reloj` | `RL-01` | el reloj de pared saltó respecto al monótono: alguien cambió la hora o la sincronización dio un salto | RECHAZA |  |  |  |
| `reloj` | `RL-02` | el reloj va detrás del último instante del estado (atrasado o estado de otra máquina) | RECHAZA |  |  |  |
| `reloj` | `RL-03` | el reloj difiere de la referencia externa más de la tolerancia | RECHAZA |  |  |  |
| `reloj` | `RL-04` | el reloj no se ha contrastado (o hace demasiado): contrástalo con una referencia externa | BLOQUEA |  |  |  |
| `reloj` | `RL-05` | el reloj da un instante fuera de lo plausible: no está en hora | RECHAZA |  |  |  |
| `reloj` | `RL-06` | solo el operador rearma el reloj, con un motivo de 15 a 500 caracteres | RECHAZA |  |  |  |
| `reloj` | `RL-07` | el Orquestador no ha visto ningún instante: no hay con qué anotar la degradación | RECHAZA |  |  |  |
| `rotacion` | `CL-01` | la clave vieja ya se retiró: lo firmado con ella no se vuelve a firmar | RECHAZA |  |  |  |
| `rotacion` | `CL-02` | el estado no está íntegro : no se rota; ábrelo y resuélvelo antes | RECHAZA |  |  |  |
| `rotacion` | `CL-03` | el instante de la rotación es anterior al reloj del Orquestador | RECHAZA |  |  |  |
| `rotacion` | `CL-04` | el diario tiene operaciones después de su punto de control: ábrelo y haz punto antes de rotar | RECHAZA |  |  |  |
| `rotacion` | `DI-02` | el diario no tiene ninguna línea completa | RECHAZA |  |  |  |
| `rotacion` | `O-13` | el expediente o la posición vinculados no son íntegros (historial, sobre, propuesta, orden, aprobación o estado) | AVISO |  |  |  |
| `rotacion` | `PE-01` | el estado debe ser texto | RECHAZA |  |  |  |
| `rotacion` | `PE-05` | no se pudo escribir la rotación: ; vuelve a llamar a rotar_ficheros | RECHAZA |  |  |  |
| `validar_contradictor` | `C-01` | número no finito | RECHAZA |  |  |  |
| `validar_contradictor` | `C-02` | no coincide con el sobre del expediente (id o hash) | RECHAZA |  |  |  |
| `validar_contradictor` | `C-03` | la independencia del Contradictor no está declarada o no es válida | RECHAZA |  |  |  |
| `validar_contradictor` | `C-04` | ids de objeción repetidos | RECHAZA |  |  |  |
| `validar_contradictor` | `C-05` | las referencias de evidencia de una objeción no están en el sobre | RECHAZA |  |  |  |
| `validar_contradictor` | `C-06` | el veredicto no cuadra con las objeciones declaradas | RECHAZA |  |  |  |
| `validar_contradictor` | `C-07` | un informe sin objeciones debe haber revisado todo el sobre | RECHAZA |  |  |  |
| `validar_contradictor` | `C-08` | el nivel de análisis del informe no es válido | RECHAZA |  |  |  |
| `validar_contradictor` | `C-09` | el informe debe vencer después de emitirse, no más tarde que el sobre, y no haber vencido | RECHAZA |  |  |  |
| `validar_contradictor` | `C-10` | la cobertura repite partes, las mezcla o cita partes que no existen en el sobre | RECHAZA |  |  |  |
| `validar_contradictor` | `C-11` | la autoría no cuadra con la diversidad declarada o con la del Contradictor configurado | RECHAZA |  |  |  |
| `validar_contradictor` | `C-12` | los escenarios de fallo no cumplen la forma (perdida_pct, evid_refs) | RECHAZA |  |  |  |
| `validar_contradictor` | `C-13` | una objeción mayor o crítica no apunta a un escenario de fallo | RECHAZA |  |  |  |
| `validar_encargo` | `E-01` | número no finito (NaN o infinito) | RECHAZA |  |  |  |
| `validar_encargo` | `E-02` | el destinatario no coincide o el perfil del candidato no está construido | RECHAZA |  |  |  |
| `validar_encargo` | `E-03` | valid_until no es posterior a emitido_en | RECHAZA |  |  |  |
| `validar_encargo` | `E-04` | no es la fecha de corte vigente emitida por K | RECHAZA |  |  |  |
| `validar_encargo` | `E-06` | (retirada en CT-G-01 0.2.0; las restricciones son opcionales por separado) | RECHAZA |  |  | retirada en CT-G-01 0.2.0 (T-51): las restricciones del encargo son opcionales por separado y solo estrechan |
| `validar_encargo` | `E-08` | la ventana de entrega del presupuesto no cabe entre la emisión y la vigencia | RECHAZA |  |  |  |
| `validar_encargo` | `E-09` | el nivel de análisis no admite la operación pedida (abrir y descartar exigen N2 o N3) | RECHAZA |  |  |  |
| `validar_encargo` | `E-10` | payload.candidato.instrumento | RECHAZA |  |  |  |
| `validar_encargo` | `E-11` | el producer del encargo no es un gestor admitido | RECHAZA |  |  |  |
| `validar_encargo` | `E-12` | las referencias del encargo están incompletas o repetidas (sello, paquete B) | RECHAZA |  |  |  |
| `validar_encargo` | `E-13` | la operación no cuadra con la posición (abrir con posición o cerrar sin ella) | RECHAZA |  |  |  |
| `validar_encargo` | `E-14` | el resultado_politica del encargo no es el que dan las reglas de F con esas entradas | RECHAZA |  |  |  |
| `validar_encargo` | `E-15` | el horizonte del encargo no cabe en el tiempo disponible | RECHAZA |  |  |  |
| `validar_encargo` | `E-16` | payload.sello_corte_ref | RECHAZA |  |  |  |
| `validar_encargo` | `E-17` | no es el mandato vigente de SC-1 para : pida el mandato a SC-1 | RECHAZA |  |  |  |
| `validar_encargo` | `R-00` | la comprobación previa de que el encargo y el sobre son válidos antes de cruzarlos | RECHAZA |  |  |  |
| `validar_encargo` | `R-01` | el sobre pertenece a otra petición | RECHAZA |  |  |  |
| `validar_encargo` | `R-02` | el sobre pertenece a otro candidato | RECHAZA |  |  |  |
| `validar_encargo` | `R-03` | payload.identificacion.perfil | RECHAZA |  |  |  |
| `validar_encargo` | `R-04` | payload.identificacion.fecha_corte | RECHAZA |  |  |  |
| `validar_encargo` | `R-05` | payload.identificacion.nivel_analisis | RECHAZA |  |  |  |
| `validar_encargo` | `R-06` | payload.identificacion.cartera_compatible | RECHAZA |  |  |  |
| `validar_encargo` | `R-07` | entregado fuera de plazo | RECHAZA |  |  |  |
| `validar_encargo` | `R-08` | payload.capital.apalancamiento | RECHAZA |  |  |  |
| `validar_encargo` | `R-09` | payload.identificacion.instrumento | RECHAZA |  |  |  |
| `validar_encargo` | `R-10` | el sobre es anterior al encargo | RECHAZA |  |  |  |
| `validar_encargo` | `R-11` | el sobre no cita el sello de corte del encargo | RECHAZA |  |  |  |
| `validar_encargo` | `R-12` | el sobre no cita ninguna fuente de datos (SRC-...) | RECHAZA |  |  |  |
| `validar_encargo` | `R-13` | el horizonte del sobre no encaja con el del mandato | RECHAZA |  |  |  |
| `validar_encargo` | `R-14` | la vía de acceso del sobre no es la que encargó el mandato | RECHAZA |  |  |  |
| `validar_sobre` | `V-01` | número no finito (NaN o infinito) | RECHAZA |  |  |  |
| `validar_sobre` | `V-02` | el perfil del sobre no está construido o no está activo en el contexto | RECHAZA |  |  |  |
| `validar_sobre` | `V-03` | valid_until no es posterior a emitido_en | RECHAZA |  |  |  |
| `validar_sobre` | `V-04` | payload.entrada_salida.fecha_revision | RECHAZA |  |  |  |
| `validar_sobre` | `V-05` | falta; exigido en | RECHAZA |  |  |  |
| `validar_sobre` | `V-06` | payload.identificacion.clase_comparabilidad | RECHAZA |  |  |  |
| `validar_sobre` | `V-07` | estado exige un valor numérico | RECHAZA |  |  |  |
| `validar_sobre` | `V-08` | exige modelo_ref y motor_id (sin ellos es SUPUESTO) | RECHAZA |  |  |  |
| `validar_sobre` | `V-09` | payload.tesis.condiciones_invalidez | RECHAZA |  |  |  |
| `validar_sobre` | `V-10` | payload.evidencia.proporcion | RECHAZA |  |  |  |
| `validar_sobre` | `V-11` | payload.estres_historico.episodios | RECHAZA |  |  |  |
| `validar_sobre` | `V-12` | payload.factores.exposiciones | RECHAZA |  |  |  |
| `validar_sobre` | `V-13` | payload.capa2.escenarios | RECHAZA |  |  |  |
| `validar_sobre` | `V-14` | payload.capa3.tope_confianza | RECHAZA |  |  |  |
| `validar_sobre` | `V-15` | payload.capital.apalancamiento | RECHAZA |  |  |  |
| `validar_sobre` | `V-16` | payload.exclusiones_duras | RECHAZA |  |  |  |
| `validar_sobre` | `V-17` | un valor fuera del rango admisible para su unidad (unidades y rangos por ruta) | RECHAZA |  |  |  |
| `validar_sobre` | `V-18` | payload.cuerpo_especializado.esquema_ref | RECHAZA |  |  |  |
| `validar_sobre` | `V-19` | un número suelto o un estado inventado en el cuerpo especializado | RECHAZA |  |  |  |
| `validar_sobre` | `V-20` | motor_id no figura en referencias.artefactos_motor | RECHAZA |  |  |  |
| `validar_sobre` | `V-21` | valor fuera del rango permitido [, ] | RECHAZA |  |  |  |
| `validar_sobre` | `V-22` | payload.entrada_salida.entrada.limite | RECHAZA |  |  |  |
| `validar_sobre` | `V-23` | de las cifras son NO_ESTIMABLE; máximo | RECHAZA |  |  |  |
| `validar_sobre` | `V-24` | payload.entrada_salida.entrada.ventana_hasta | RECHAZA |  |  |  |
| `validar_sobre` | `V-25` | payload.capa2.horizonte_dias | RECHAZA |  |  |  |
| `validar_sobre` | `V-26` | las cifras citan artefactos del Motor que no existen, son de otro modelo o usan datos posteriores al corte | RECHAZA |  |  |  |
| `vigilancia` | `H-01` | stop ejecutado por el intermediario | INFORMA |  |  |  |
| `vigilancia` | `H-02` | condición de salida cumplida | INFORMA |  |  |  |
| `vigilancia` | `H-03` | dato ausente o viejo | AVISO |  |  |  |
| `vigilancia` | `H-04` | cierre pendiente (CERRANDO) que se reintenta | INFORMA |  |  |  |
| `vigilancia` | `H-05` | stop cumplido sin que el intermediario lo ejecutara | INFORMA |  |  |  |
| `vigilancia` | `H-06` | métrica no soportada | AVISO |  |  |  |
| `vigilancia` | `H-07` | diferencias de conciliación | AVISO |  |  |  |
| `vigilancia` | `H-08` | reducción en curso (REDUCIENDO) que se retoma | INFORMA |  |  |  |
| `vigilancia` | `H-09` | instante sospechoso (no se hace nada) | AVISO |  |  |  |
| `vigilancia` | `H-10` | salida preparada para el operador (L0/L1) | INFORMA |  |  |  |
| `vigilancia` | `H-11` | orden de entrada viva | INFORMA |  |  |  |
| `vigilancia` | `H-12` | reducción parcial por una condición OBJETIVO que declara su fracción (una sola vez | INFORMA |  |  |  |
| `vigilancia` | `H-13` | posición con el estado de control alterado (no se envía nada por ella) | BLOQUEA |  |  |  |
| `vigilancia` | `H-14` | llegó la fecha de revisión de la tesis: la posición pasa a EN_REVISION y la confirma (con fecha nueva) o la cierra el operador | AVISO |  |  |  |
| `vigilancia` | `H-15` | se cumplió la condición de reapertura de un expediente en observación (aviso O-31 | AVISO |  |  |  |
| `vigilancia` | `H-16` | se cumple un escenario de fallo del Contradictor o una invalidez por una métrica que no es el precio: pide revisión y propone | AVISO |  |  |  |
| `vigilancia` | `H-17` | la pérdida no realizada pasa el umbral configurado (y otra vez por cada múltiplo): pide revisión | AVISO |  |  |  |
| `vigilancia` | `H-18` | falta el dato de una señal (o llega sin unidad, en otra unidad o no numérico): no se evalúa | AVISO |  |  |  |
| `vigilancia` | `H-19` | fallo inesperado al vigilar una posición: se informa (degrada su cartera) y se sigue con las demás | AVISO |  |  |  |
