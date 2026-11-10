"""Catálogo de los códigos de resultado y de aviso del marco común de C (V0.61, pieza 2 del kit 2).

Una sola lista con lo que significa cada código y qué hace, para que una pieza nueva no reutilice un código
con otro sentido, no use uno sin documentarlo ni deje uno documentado que ya no existe. La clave de
`CATALOGO` es `(modulo, codigo)` —el nombre del fichero de `validador/` sin `.py`— y el valor lleva:

- `"que"`: texto corto con lo que significa, tomado del mensaje del código, del docstring del módulo, del
  comentario de la línea que lo emite o, para las reglas que construyen su mensaje por fuera, del nombre de
  los casos inválidos de su batería (que documentan cada regla); nunca inventado. Los que llegaron sin nada
  quedan como `"(sin documentar)"` y la batería los cuenta como pendientes;
- `"efecto"`: RECHAZA (la operación o el mensaje no se acepta), REDUCE (la operación se ACEPTA con la
  cantidad recortada: las reglas de F que no vetan, `control_f` responde «REDUCIDO» con
  `cantidad_aprobada > 0`), AVISO (se anota un aviso al operador), BLOQUEA (se bloquea el flujo: el sello
  no se emite, el diario o el reloj se bloquean, F veta la orden), INFORMA (cambia el estado o prepara una
  acción sin rechazar nada) u OK;
- `"desde"`: la versión que introdujo el código, o None si no se puede afirmar (GLM no toca git; el LEEME
  menciona los códigos fuera de orden, de modo que la primera mención no prueba nada);
- los avisos del Orquestador llevan además `"prioridad"`, la de `PRIORIDAD_AVISO` (`"MEDIA"` si no figura,
  que es como el propio Orquestador los trata);
- los códigos con muchos sitios de emisión de significados distintos llevan `"familia": True` y un texto
  de nivel familia que no documenta un solo caso (O-00, O-01 y O-02 del Orquestador; revisión, hallazgo 4);
- los códigos retirados llevan `"retirado": True` y `"motivo"`: documentados y fuera del código (E-06, la
  única retirada del contrato vigente; las retiradas históricas que registra el LEEME, como D-03 en V0.17,
  no entran en el catálogo —criterio declarado tras la revisión, hallazgo 7—).

El módulo no está en `MODULOS_ESQUEMA` (no cambia el esquema del código) y no emite ni decide nada: es un
catálogo de solo lectura con las funciones que lo comprueban.

- `codigos_en_el_codigo(carpeta)`: recorre los `.py` de `carpeta` (salvo este módulo) y devuelve el conjunto
  de pares `(modulo, codigo)` de los códigos que aparecen como constantes de texto enteras (ast.Constant de
  tipo str que casan enteros con la expresión de la pieza: una o dos letras mayúsculas, guion y dos cifras;
  por ejemplo «V-01», «O-13», «RM-07» o «PE-08»), con `ast`, no a grep, para no confundir comentarios ni
  fragmentos dentro de mensajes más largos;
- `sitios_de_emision(carpeta)`: las llamadas que emiten cada código en los `.py` de `carpeta` (salvo este
  módulo): para cada `(modulo, codigo)`, cuántos sitios de emisión hay, los mensajes literales distintos y
  los resultados y envoltorios de esas llamadas («BLOQUEO», «ADVERTENCIA», `_bloqueo`…). Con `ast`, no a
  grep, igual que la anterior (un fichero ilegible no aporta nada);
- `prefijos_del_leeme(ruta)`: lee la tabla del «Registro de prefijos de códigos» del LEEME y devuelve los
  prefijos que registra;
- `como_markdown()`: el catálogo como tabla Markdown ordenada por módulo y código (se entrega en
  `entrega_glm/V0.61/catalogo_codigos.md`).

`COLISIONES_ADMITIDAS` registra los pares de módulos que comparten códigos con su explicación: la E del
encargo y la E del dimensionado, los códigos de F que el Orquestador y el dimensionado consumen o acotan, y
los códigos de persistencia y del diario que la infraestructura T-03 (migraciones, rotación) reutiliza con
el mismo significado. Los dos choques REALES (O-00 y O-01, con significados distintos en dos módulos) están
admitidos con su explicación, anotados en la deuda técnica (T-70 y T-71) sin renombrar nada y declarados en
`CHOQUES_REALES`, que la batería vigila exigiendo textos distintos por módulo (r01). Las reglas de F que
aprueban con menos cantidad están en `REGLAS_QUE_REDUCEN` y llevan efecto REDUCE (r03).
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

EXPRESION_CODIGO = re.compile(r"[A-Z]{1,2}-\d{2}")
EFECTOS = ("RECHAZA", "REDUCE", "AVISO", "BLOQUEA", "INFORMA", "OK")

# Las reglas de F que no vetan: `control_f` las responde con "REDUCE" y devuelve "REDUCIDO" con
# `cantidad_aprobada > 0` (la orden queda APROBADA, recortada), de modo que su efecto no es RECHAZA
# (revisión, hallazgo 3; Documento 0 §2 punto 3). Las filas de `control_f` y sus copias del Orquestador
# llevan efecto REDUCE y la batería lo exige (r03).
REGLAS_QUE_REDUCEN = frozenset({"F-03", "F-04", "F-06", "F-07", "F-13", "F-14", "F-15"})

# Los choques reales declarados con su fila de deuda técnica: el mismo código con significados distintos
# en dos módulos (revisión, hallazgo 1). La batería (r01) exige que los textos `que` de los dos módulos
# sean distintos, que el par esté admitido en `COLISIONES_ADMITIDAS` y que toda explicación «CHOQUE REAL»
# cite una de estas deudas.
CHOQUES_REALES = {
    ("orquestador", "diario", "O-00"): "T-70",
    ("orquestador", "ejecucion_g", "O-01"): "T-71",
}

# {(modulo, codigo): {"que", "efecto", "desde", "prioridad"?, "retirado"?, "motivo"?}}
CATALOGO = {
    ("comparador", "D-01"): {"que": "entrada inválida", "efecto": "RECHAZA", "desde": None},
    ("contratos", "CT-01"): {"que": "falta el tipo de mensaje o su versión", "efecto": "RECHAZA", "desde": None},
    ("contratos", "CT-02"): {"que": "no tiene esquema para la versión (vigente )", "efecto": "RECHAZA", "desde": None},
    ("contratos", "CT-03"): {"que": "no cumple el esquema (ruta y motivo)", "efecto": "RECHAZA", "desde": None},
    ("contratos", "CT-04"): {"que": "vence antes de emitirse", "efecto": "RECHAZA", "desde": None},
    ("control_f", "CF-01"): {"que": "la envoltura del informe de F no es válida (versión, campos o entrada mal formados)", "efecto": "RECHAZA", "desde": None},
    ("control_f", "CF-02"): {"que": "el informe no corresponde a esta propuesta (expediente, petición o hash)", "efecto": "RECHAZA", "desde": None},
    ("control_f", "CF-03"): {"que": "el informe debe estar emitido, vigente y no durar más que la política", "efecto": "RECHAZA", "desde": None},
    ("control_f", "CF-04"): {"que": "el resultado (o su motivo) no es el que dan las reglas con esas entradas", "efecto": "RECHAZA", "desde": None},
    ("control_f", "CF-05"): {"que": "la solicitud no coincide con la propuesta (límite, stop, dirección, cartera, instrumento, activo base, divisa de cotización, apalancamiento y cantidad", "efecto": "RECHAZA", "desde": None},
    ("control_f", "CF-06"): {"que": "no se puede aprobar más de lo solicitado", "efecto": "RECHAZA", "desde": None},
    ("control_f", "CF-07"): {"que": "la política usada no es la oficial del Orquestador", "efecto": "RECHAZA", "desde": None},
    ("control_f", "CF-08"): {"que": "la cartera del informe omite una posición o autorización ya comprometida", "efecto": "RECHAZA", "desde": None},
    ("control_f", "CF-09"): {"que": "el contexto del informe no es el del Orquestador (mandato, evidencia, eventos, autonomía, actividad o precio)", "efecto": "RECHAZA", "desde": None},
    ("control_f", "F-01"): {"que": "error de cálculo al aplicar el control: la orden sale VETADA", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-02"): {"que": "el stop no está del lado de la pérdida", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-03"): {"que": "el riesgo delante del stop supera el riesgo máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("control_f", "F-04"): {"que": "el tamaño supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("control_f", "F-05"): {"que": "el apalancamiento supera el máximo de la política", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-06"): {"que": "la exposición total supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("control_f", "F-07"): {"que": "la concentración en un activo supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("control_f", "F-08"): {"que": "la pérdida del día alcanzó el límite de la política", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-09"): {"que": "más posiciones abiertas que el máximo de la política", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-10"): {"que": "el estado de la cartera está viejo o en el futuro", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-11"): {"que": "el valor de la orden queda por debajo del mínimo de la política", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-12"): {"que": "sin tipo de cambio a euros para la divisa de cotización", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-13"): {"que": "el importe de la orden en euros supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("control_f", "F-14"): {"que": "el importe del día en euros supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("control_f", "F-15"): {"que": "el importe del activo en euros supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("control_f", "F-16"): {"que": "la pérdida del día o de la semana en euros supera el máximo de la política", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-17"): {"que": "demasiadas órdenes en la última hora", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-18"): {"que": "la orden no encaja en el mandato efectivo del contexto", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-19"): {"que": "el instrumento está en las exclusiones duras del contexto", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-20"): {"que": "la evidencia verificada queda por debajo del mínimo de la política", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-21"): {"que": "el calendario de eventos no se puede leer", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-22"): {"que": "la autonomía (nivel, kill-switch u horario) no permite ejecutar la orden", "efecto": "BLOQUEA", "desde": None},
    ("control_f", "F-23"): {"que": "sin precio del intermediario para el instrumento", "efecto": "BLOQUEA", "desde": None},
    ("diario", "DI-01"): {"que": "los argumentos de la operación no se pueden guardar tal cual en el diario: no se aplica", "efecto": "RECHAZA", "desde": None},
    ("diario", "DI-02"): {"que": "línea del diario ilegible, con su hash roto o sin la firma esperada", "efecto": "RECHAZA", "desde": None},
    ("diario", "DI-03"): {"que": "el diario no tiene un punto de control para el estado guardado", "efecto": "RECHAZA", "desde": None},
    ("diario", "DI-04"): {"que": "el estado reaplicado no es el del punto de control anotado (el código o los datos cambiaron)", "efecto": "RECHAZA", "desde": None},
    ("diario", "DI-05"): {"que": "no se pudo escribir en el diario: no se aplica y queda bloqueado hasta reabrirlo", "efecto": "BLOQUEA", "desde": None},
    ("diario", "DI-06"): {"que": "el diario cambió por fuera: no se aplica nada más; reábrelo para volver al estado anotado", "efecto": "BLOQUEA", "desde": None},
    ("diario", "O-00"): {"que": "operación que lanzó una excepción no recogida: se anota y se reproduce igual", "efecto": "RECHAZA", "desde": None},
    ("diario", "O-13"): {"que": "el expediente o la posición vinculados no son íntegros (historial, sobre, propuesta, orden, aprobación o estado)", "efecto": "AVISO", "desde": None},
    ("diario", "PE-01"): {"que": "no se puede volcar el estado", "efecto": "RECHAZA", "desde": None},
    ("diario", "PE-05"): {"que": "el estado pasa de bytes: no se hace el punto", "efecto": "RECHAZA", "desde": None},
    ("diario", "PE-07"): {"que": "la clave debe tener al menos bytes", "efecto": "RECHAZA", "desde": None},
    ("dimensionado", "E-01"): {"que": "la solicitud debe llevar exactamente los campos exigidos y no una cantidad", "efecto": "RECHAZA", "desde": None},
    ("dimensionado", "E-02"): {"que": "el stop debe estar del lado de la pérdida y la dirección ser LARGO o CORTO", "efecto": "RECHAZA", "desde": None},
    ("dimensionado", "E-03"): {"que": "F vetaría: no hay tipo de cambio a euros para la divisa de cotización", "efecto": "RECHAZA", "desde": None},
    ("dimensionado", "E-04"): {"que": "no hay una cantidad viable por encima del paso y del valor mínimo", "efecto": "RECHAZA", "desde": None},
    ("dimensionado", "F-01"): {"que": "error de cálculo al aplicar el control: la orden sale VETADA", "efecto": "BLOQUEA", "desde": None},
    ("dimensionado", "F-11"): {"que": "el valor de la orden queda por debajo del mínimo de la política", "efecto": "BLOQUEA", "desde": None},
    ("dimensionado", "F-12"): {"que": "sin tipo de cambio a euros para la divisa de cotización", "efecto": "BLOQUEA", "desde": None},
    ("ejecucion_g", "G-01"): {"que": "sin conexión con el intermediario; la posición sigue y se puede reintentar", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "G-02"): {"que": "la orden de entrada no llegó al intermediario; se anota como rechazada", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "G-03"): {"que": "el intermediario no confirma la vía de acceso autorizada", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "G-04"): {"que": "cierre crítico: la posición no se pudo cerrar", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "G-05"): {"que": "el Orquestador rechazó la ejecución", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "G-06"): {"que": "la autorización ya no vale (fue automática y la cartera bajó de nivel, se degradó después o ya no la permite el umbral o el horario, o después se bajó", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "G-08"): {"que": "fallo con órdenes ya enviadas: estado incierto, hay que conciliar con el intermediario", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "G-09"): {"que": "cierre no completado; la posición sigue CERRANDO", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "G-10"): {"que": "la orden de protección declarada no es un stop vivo en el intermediario por lo que queda (lado contrario a la posición, mismo instrumento y vía, canti", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "G-11"): {"que": "orden de entrada viva hasta su caducidad en el intermediario", "efecto": "INFORMA", "desde": None},
    ("ejecucion_g", "G-12"): {"que": "reducción no completada; la posición sigue REDUCIENDO con su stop anterior", "efecto": "RECHAZA", "desde": None},
    ("ejecucion_g", "O-01"): {"que": "el intermediario no da precio para el instrumento o el instante es ilegible", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "K-00"): {"que": "entrada o contexto mal formado", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-01"): {"que": "la fecha solicitada no es día hábil en el mercado; se recorta al hábil anterior", "efecto": "AVISO", "desde": None},
    ("k_calidad", "Q-02"): {"que": "no hay ninguna fuente disponible", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-03"): {"que": "un valor ausente, no numérico, no finito o no positivo", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-04"): {"que": "salto del precio mayor que el umbral de la política (advirtiendo o bloqueando según su factor)", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-05"): {"que": "faltan días hábiles en la ventana de la política", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-06"): {"que": "fechas repetidas o fuera de orden", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-07"): {"que": "una barra incoherente (máximo, mínimo, cierre o volumen)", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-08"): {"que": "ajustes sin versión", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-09"): {"que": "mercado FX sin cruces definidos: coherencia no comprobada", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-10"): {"que": "un dato crítico sin fuente de contraste disponible", "efecto": "AVISO", "desde": None},
    ("k_calidad", "Q-11"): {"que": "excepción al calcular la calidad: el sello sale BLOQUEADO (falla cerrado)", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-12"): {"que": "el hash declarado de los datos no coincide con el contenido", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-13"): {"que": "el corte es posterior a la fecha de emisión", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-14"): {"que": "procedencia incompleta, licencia no admitida o dato posterior a su obtención", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "Q-15"): {"que": "eventos mal formados o anunciados después de emitir el sello", "efecto": "BLOQUEA", "desde": None},
    ("k_calidad", "S-01"): {"que": "el sello no es un objeto", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-02"): {"que": "la fecha del identificador no coincide con fecha_corte", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-03"): {"que": "el resultado_global no es el peor de los resultados de sus reglas", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-04"): {"que": "las reglas Q-01 a Q-15 deben figurar exactamente una vez", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-05"): {"que": "mercado repetido", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-06"): {"que": "el corte no puede ser posterior a la fecha solicitada", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-07"): {"que": "un sello no puede reemplazarse a sí mismo", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-08"): {"que": "el sello está ANULADO", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-09"): {"que": "una ADVERTENCIA debe llevar detalle", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-10"): {"que": "el corte del sello no es día hábil de sus mercados", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-11"): {"que": "versión de esquema desconocida", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-12"): {"que": "el hash no corresponde al contenido del sello", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-13"): {"que": "Q-01 debe ser ADVERTENCIA si y solo si el corte difiere de la fecha solicitada", "efecto": "RECHAZA", "desde": None},
    ("k_calidad", "S-14"): {"que": "la fecha de obtención de la procedencia no cuadra con el cierre (fuentes.procedencia.obtenido_en)", "efecto": "RECHAZA", "desde": None},
    ("mandatos", "E-01"): {"que": "las restricciones del encargo no pasan la forma que exige SC-1 (claves o lista)", "efecto": "RECHAZA", "desde": None},
    ("mandatos", "E-05"): {"que": "el horizonte de las restricciones es más amplio que el del mandato", "efecto": "RECHAZA", "desde": None},
    ("mandatos", "E-07"): {"que": "el tamaño de las restricciones es mayor que el del mandato", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-01"): {"que": "envoltura inválida: campos, consumer G, valid_until nulo, payload o data_refs (las órdenes del payload)", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-02"): {"que": "solo el operador declara ejecuciones manuales", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-03"): {"que": "la ejecución es anterior a la autorización del expediente o a la apertura de la posición", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-04"): {"que": "la posición no existe o no está ABIERTA, EN_REVISION ni REDUCIENDO", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-05"): {"que": "la vía de acceso no es la de la propuesta autorizada (un futuro analizado no se opera como contado)", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-06"): {"que": "una reducción parcial exige una cantidad positiva; para cerrarla entera se declara la cantidad exacta de la posición", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-07"): {"que": "una reducción parcial exige declarar el stop nuevo que el operador ya colocó por lo que queda", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-08"): {"que": "instrumento no admitido en esa cartera (lista o exclusiones del mandato)", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-09"): {"que": "el precio se aleja del límite autorizado más de la tolerancia", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-10"): {"que": "hay una posición abierta o un expediente autorizado en ese instrumento: vincule el registro a ellos", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-11"): {"que": "la envoltura no identifica el caso del vínculo (expediente_id y correlation_id; nulos si es LIBRE)", "efecto": "RECHAZA", "desde": None},
    ("manual_g", "RM-12"): {"que": "no se puede valorar en euros lo que queda (falta el mínimo de F o su tipo de cambio): ciérrala entera", "efecto": "RECHAZA", "desde": None},
    ("migraciones", "DI-02"): {"que": "el diario no tiene ninguna línea completa", "efecto": "RECHAZA", "desde": None},
    ("migraciones", "MG-01"): {"que": "no hay camino de migración desde el esquema guardado hasta el de este código, o el registro de migraciones está mal formado", "efecto": "RECHAZA", "desde": None},
    ("migraciones", "MG-02"): {"que": "la configuración guardada no es la de su huella con el código que la guardó: se tocó; ábrelo con ese código", "efecto": "RECHAZA", "desde": None},
    ("migraciones", "MG-03"): {"que": "la migración no devuelve un estado que JSON guarde tal cual", "efecto": "RECHAZA", "desde": None},
    ("migraciones", "MG-04"): {"que": "la migración cambiaría lo que no declara o no se puede cambiar", "efecto": "RECHAZA", "desde": None},
    ("migraciones", "MG-05"): {"que": "el instante de la migración es anterior al reloj del Orquestador", "efecto": "RECHAZA", "desde": None},
    ("migraciones", "MG-06"): {"que": "el diario tiene operaciones después de su punto de control: ábrelo con el código que lo escribió y haz punto antes de migrar", "efecto": "RECHAZA", "desde": None},
    ("migraciones", "PE-01"): {"que": "el estado a migrar debe ser texto", "efecto": "RECHAZA", "desde": None},
    ("migraciones", "PE-05"): {"que": "no se pudo escribir la migración: ; vuelve a llamar a migrar_ficheros", "efecto": "RECHAZA", "desde": None},
    ("orquestador", "F-03"): {"que": "el riesgo delante del stop supera el riesgo máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("orquestador", "F-04"): {"que": "el tamaño supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("orquestador", "F-06"): {"que": "la exposición total supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("orquestador", "F-07"): {"que": "la concentración en un activo supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("orquestador", "F-09"): {"que": "más posiciones abiertas que el máximo de la política", "efecto": "BLOQUEA", "desde": None},
    ("orquestador", "F-11"): {"que": "el valor de la orden queda por debajo del mínimo de la política", "efecto": "BLOQUEA", "desde": None},
    ("orquestador", "F-13"): {"que": "el importe de la orden en euros supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("orquestador", "F-14"): {"que": "el importe del día en euros supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("orquestador", "F-15"): {"que": "el importe del activo en euros supera el máximo de la política: recorta la cantidad", "efecto": "REDUCE", "desde": None},
    ("orquestador", "O-00"): {"que": "fallo puntual de la operación pedida: un instante inválido o anterior al último, o una excepción no recogida al ejecutar la operación o al comprobar un registro manual; la operación no se aplica", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA", "familia": True},
    ("orquestador", "O-01"): {"que": "rechazo genérico de la operación pedida: entrada no admitida o condición incumplida; se emite en muchos caminos —entre ellos, resto_parcial distinto de CANCELAR—", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA", "familia": True},
    ("orquestador", "O-02"): {"que": "petición ya atendida o estado ya alcanzado (idempotencia): ya registrado, ya acusado, ya activo, ya configurado, ya ganador o sin nivel nuevo; no cambia nada", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA", "familia": True},
    ("orquestador", "O-03"): {"que": "ya hay otra orden de entrada para este expediente", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-04"): {"que": "la posición no admite señales en su estado actual (solo abierta o en revisión)", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-05"): {"que": "la autorización ya no vale (automática con la cartera por debajo de L2 o degradada después, o anterior a una bajada del límite de pérdida): vuelve a p", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-06"): {"que": "hay operaciones libres declaradas abiertas en ese instrumento: no se mezclan con una posición del sistema", "efecto": "AVISO", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-07"): {"que": "encargo incompleto por presupuesto: no se valida; reemitir o descartar", "efecto": "AVISO", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-08"): {"que": "presupuesto diario agotado o comprometido: no se aceptan encargos nuevos", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-09"): {"que": "máximo de reintentos sin avance; se avisa al operador", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-10"): {"que": "la autorización fue automática y el sello del análisis ya no está vigente: la confirma el operador", "efecto": "AVISO", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-11"): {"que": "fechas de corte distintas entre los candidatos: hay que actualizar datos", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-12"): {"que": "el artefacto es de un modelo no declarado (o alterado) en el Motor", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-13"): {"que": "el expediente o la posición vinculados no son íntegros (historial, sobre, propuesta, orden, aprobación o estado)", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-14"): {"que": "CERRADA es un estado terminal", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-15"): {"que": "la fecha de revisión ya llegó: confirmar la tesis exige fijar la siguiente", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-16"): {"que": "el restablecimiento no puede ser anterior a la degradación", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-17"): {"que": "objeción crítica: el expediente queda detenido hasta que el operador la levante o lo descarte", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-18"): {"que": "diferencias de conciliación con el intermediario", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-19"): {"que": "cartera degradada a L1", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-20"): {"que": "operación libre declarada fuera del sistema (sin control de F ni stop)", "efecto": "AVISO", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-21"): {"que": "los precios del sobre (stop, límite, objetivo) no están en la divisa de cotización del instrumento", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-22"): {"que": "solo se elige entre los aspirantes de una decisión ajustada (empatados, primeros con otra ponderación o cuando un apartado habría ganado)", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-23"): {"que": "la solicitud de E no es la propuesta (instrumento, dirección, límite, stop, apalancamiento o cartera)", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-24"): {"que": "el encargo no cita el mandato vigente de SC-1 para la cartera (versión y huella): pídalo con mandato", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-25"): {"que": "hay una orden de entrada de G viva para este expediente: cancélela antes de ejecutar a mano", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-26"): {"que": "la autorización es anterior a un kill-switch: hay que volver a aprobar", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-27"): {"que": "la autorización del operador exige su aprobación: pantalla_hash, importe_tecleado, canal y segundo_factor", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-28"): {"que": "la aprobación cae fuera de horario: espere el enfriamiento desde que se generó la pantalla", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-29"): {"que": "la cartera no es la vigente: la última foto de G del intermediario más las autorizaciones pendientes", "efecto": "RECHAZA", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-30"): {"que": "un candidato apartado habría ganado la comparación; decide el operador", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-31"): {"que": "la observación venció sin reabrirse; queda descartado", "efecto": "AVISO", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-32"): {"que": "sobre recibido como informe: exclusión dura BLOQUEADO; expediente descartado", "efecto": "AVISO", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-33"): {"que": "sin diversidad de modelo o sin poder comprobar la autoría del Contradictor", "efecto": "AVISO", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-34"): {"que": "el informe de F no trae sus topes de cantidad: no hay con qué acotar la anulación", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-35"): {"que": "el límite de pérdida se alcanzó en las últimas 24 horas: no se puede subir (Constitución §6)", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-36"): {"que": "el análisis usa un sello de K con advertencias (p. ej. dato de una sola fuente): autoriza el operador", "efecto": "AVISO", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-37"): {"que": "tope diario de las LIBRES superado, o LIBRES sin poder valorar (T-33)", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-38"): {"que": "cortacircuito global por pérdida del día o de la semana (T-40)", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-39"): {"que": "se sube de un nivel en uno: cada nivel exige su periodo mínimo", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("orquestador", "O-40"): {"que": "alarma de sequía: en el plazo ninguna oportunidad llegó a invertirse habiendo candidatos que pasaron el análisis (D-22)", "efecto": "AVISO", "desde": None, "prioridad": "MEDIA"},
    ("orquestador", "O-41"): {"que": "tras el plazo de juicio, el robot no supera a la cartera sombra en términos reales: se propone gestión pasiva y decide el operador (P17)", "efecto": "AVISO", "desde": None, "prioridad": "ALTA"},
    ("persistencia", "O-13"): {"que": "el estado cargado no cuadra : kill-switch activado", "efecto": "AVISO", "desde": None},
    ("persistencia", "PE-01"): {"que": "el estado tiene valores que no se pueden poner en forma canónica", "efecto": "RECHAZA", "desde": None},
    ("persistencia", "PE-02"): {"que": "la huella del estado no cuadra: el fichero está roto o se tocó a mano", "efecto": "RECHAZA", "desde": None},
    ("persistencia", "PE-03"): {"que": "la versión de configuración del documento no es la de la configuración guardada", "efecto": "RECHAZA", "desde": None},
    ("persistencia", "PE-04"): {"que": "a la configuración guardada le faltan claves de este código: hace falta una migración", "efecto": "RECHAZA", "desde": None},
    ("persistencia", "PE-05"): {"que": "el estado pasa del tamaño máximo: no se guarda", "efecto": "RECHAZA", "desde": None},
    ("persistencia", "PE-06"): {"que": "la firma del estado no es válida: se tocó con la clave o sin ella", "efecto": "RECHAZA", "desde": None},
    ("persistencia", "PE-07"): {"que": "la clave de firma no es válida (longitud, fichero, permisos o lectura)", "efecto": "RECHAZA", "desde": None},
    ("persistencia", "PE-08"): {"que": "el estado lo guardó otra versión del código (otro esquema): hay que migrarlo (migraciones.migrar)", "efecto": "RECHAZA", "desde": None},
    ("reloj", "RL-01"): {"que": "el reloj de pared saltó respecto al monótono: alguien cambió la hora o la sincronización dio un salto", "efecto": "RECHAZA", "desde": None},
    ("reloj", "RL-02"): {"que": "el reloj va detrás del último instante del estado (atrasado o estado de otra máquina)", "efecto": "RECHAZA", "desde": None},
    ("reloj", "RL-03"): {"que": "el reloj difiere de la referencia externa más de la tolerancia", "efecto": "RECHAZA", "desde": None},
    ("reloj", "RL-04"): {"que": "el reloj no se ha contrastado (o hace demasiado): contrástalo con una referencia externa", "efecto": "BLOQUEA", "desde": None},
    ("reloj", "RL-05"): {"que": "el reloj da un instante fuera de lo plausible: no está en hora", "efecto": "RECHAZA", "desde": None},
    ("reloj", "RL-06"): {"que": "solo el operador rearma el reloj, con un motivo de 15 a 500 caracteres", "efecto": "RECHAZA", "desde": None},
    ("reloj", "RL-07"): {"que": "el Orquestador no ha visto ningún instante: no hay con qué anotar la degradación", "efecto": "RECHAZA", "desde": None},
    ("rotacion", "CL-01"): {"que": "la clave vieja ya se retiró: lo firmado con ella no se vuelve a firmar", "efecto": "RECHAZA", "desde": None},
    ("rotacion", "CL-02"): {"que": "el estado no está íntegro : no se rota; ábrelo y resuélvelo antes", "efecto": "RECHAZA", "desde": None},
    ("rotacion", "CL-03"): {"que": "el instante de la rotación es anterior al reloj del Orquestador", "efecto": "RECHAZA", "desde": None},
    ("rotacion", "CL-04"): {"que": "el diario tiene operaciones después de su punto de control: ábrelo y haz punto antes de rotar", "efecto": "RECHAZA", "desde": None},
    ("rotacion", "DI-02"): {"que": "el diario no tiene ninguna línea completa", "efecto": "RECHAZA", "desde": None},
    ("rotacion", "O-13"): {"que": "el expediente o la posición vinculados no son íntegros (historial, sobre, propuesta, orden, aprobación o estado)", "efecto": "AVISO", "desde": None},
    ("rotacion", "PE-01"): {"que": "el estado debe ser texto", "efecto": "RECHAZA", "desde": None},
    ("rotacion", "PE-05"): {"que": "no se pudo escribir la rotación: ; vuelve a llamar a rotar_ficheros", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-01"): {"que": "número no finito", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-02"): {"que": "no coincide con el sobre del expediente (id o hash)", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-03"): {"que": "la independencia del Contradictor no está declarada o no es válida", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-04"): {"que": "ids de objeción repetidos", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-05"): {"que": "las referencias de evidencia de una objeción no están en el sobre", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-06"): {"que": "el veredicto no cuadra con las objeciones declaradas", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-07"): {"que": "un informe sin objeciones debe haber revisado todo el sobre", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-08"): {"que": "el nivel de análisis del informe no es válido", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-09"): {"que": "el informe debe vencer después de emitirse, no más tarde que el sobre, y no haber vencido", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-10"): {"que": "la cobertura repite partes, las mezcla o cita partes que no existen en el sobre", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-11"): {"que": "la autoría no cuadra con la diversidad declarada o con la del Contradictor configurado", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-12"): {"que": "los escenarios de fallo no cumplen la forma (perdida_pct, evid_refs)", "efecto": "RECHAZA", "desde": None},
    ("validar_contradictor", "C-13"): {"que": "una objeción mayor o crítica no apunta a un escenario de fallo", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-01"): {"que": "número no finito (NaN o infinito)", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-02"): {"que": "el destinatario no coincide o el perfil del candidato no está construido", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-03"): {"que": "valid_until no es posterior a emitido_en", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-04"): {"que": "no es la fecha de corte vigente emitida por K", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-06"): {"que": "(retirada en CT-G-01 0.2.0; las restricciones son opcionales por separado)", "efecto": "RECHAZA", "desde": None, "retirado": True, "motivo": "retirada en CT-G-01 0.2.0 (T-51): las restricciones del encargo son opcionales por separado y solo estrechan"},
    ("validar_encargo", "E-08"): {"que": "la ventana de entrega del presupuesto no cabe entre la emisión y la vigencia", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-09"): {"que": "el nivel de análisis no admite la operación pedida (abrir y descartar exigen N2 o N3)", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-10"): {"que": "payload.candidato.instrumento", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-11"): {"que": "el producer del encargo no es un gestor admitido", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-12"): {"que": "las referencias del encargo están incompletas o repetidas (sello, paquete B)", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-13"): {"que": "la operación no cuadra con la posición (abrir con posición o cerrar sin ella)", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-14"): {"que": "el resultado_politica del encargo no es el que dan las reglas de F con esas entradas", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-15"): {"que": "el horizonte del encargo no cabe en el tiempo disponible", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-16"): {"que": "payload.sello_corte_ref", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "E-17"): {"que": "no es el mandato vigente de SC-1 para : pida el mandato a SC-1", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-00"): {"que": "la comprobación previa de que el encargo y el sobre son válidos antes de cruzarlos", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-01"): {"que": "el sobre pertenece a otra petición", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-02"): {"que": "el sobre pertenece a otro candidato", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-03"): {"que": "payload.identificacion.perfil", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-04"): {"que": "payload.identificacion.fecha_corte", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-05"): {"que": "payload.identificacion.nivel_analisis", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-06"): {"que": "payload.identificacion.cartera_compatible", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-07"): {"que": "entregado fuera de plazo", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-08"): {"que": "payload.capital.apalancamiento", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-09"): {"que": "payload.identificacion.instrumento", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-10"): {"que": "el sobre es anterior al encargo", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-11"): {"que": "el sobre no cita el sello de corte del encargo", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-12"): {"que": "el sobre no cita ninguna fuente de datos (SRC-...)", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-13"): {"que": "el horizonte del sobre no encaja con el del mandato", "efecto": "RECHAZA", "desde": None},
    ("validar_encargo", "R-14"): {"que": "la vía de acceso del sobre no es la que encargó el mandato", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-01"): {"que": "número no finito (NaN o infinito)", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-02"): {"que": "el perfil del sobre no está construido o no está activo en el contexto", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-03"): {"que": "valid_until no es posterior a emitido_en", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-04"): {"que": "payload.entrada_salida.fecha_revision", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-05"): {"que": "falta; exigido en", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-06"): {"que": "payload.identificacion.clase_comparabilidad", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-07"): {"que": "estado exige un valor numérico", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-08"): {"que": "exige modelo_ref y motor_id (sin ellos es SUPUESTO)", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-09"): {"que": "payload.tesis.condiciones_invalidez", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-10"): {"que": "payload.evidencia.proporcion", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-11"): {"que": "payload.estres_historico.episodios", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-12"): {"que": "payload.factores.exposiciones", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-13"): {"que": "payload.capa2.escenarios", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-14"): {"que": "payload.capa3.tope_confianza", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-15"): {"que": "payload.capital.apalancamiento", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-16"): {"que": "payload.exclusiones_duras", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-17"): {"que": "un valor fuera del rango admisible para su unidad (unidades y rangos por ruta)", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-18"): {"que": "payload.cuerpo_especializado.esquema_ref", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-19"): {"que": "un número suelto o un estado inventado en el cuerpo especializado", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-20"): {"que": "motor_id no figura en referencias.artefactos_motor", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-21"): {"que": "valor fuera del rango permitido [, ]", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-22"): {"que": "payload.entrada_salida.entrada.limite", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-23"): {"que": "de las cifras son NO_ESTIMABLE; máximo", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-24"): {"que": "payload.entrada_salida.entrada.ventana_hasta", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-25"): {"que": "payload.capa2.horizonte_dias", "efecto": "RECHAZA", "desde": None},
    ("validar_sobre", "V-26"): {"que": "las cifras citan artefactos del Motor que no existen, son de otro modelo o usan datos posteriores al corte", "efecto": "RECHAZA", "desde": None},
    ("vigilancia", "H-01"): {"que": "stop ejecutado por el intermediario", "efecto": "INFORMA", "desde": None},
    ("vigilancia", "H-02"): {"que": "condición de salida cumplida", "efecto": "INFORMA", "desde": None},
    ("vigilancia", "H-03"): {"que": "dato ausente o viejo", "efecto": "AVISO", "desde": None},
    ("vigilancia", "H-04"): {"que": "cierre pendiente (CERRANDO) que se reintenta", "efecto": "INFORMA", "desde": None},
    ("vigilancia", "H-05"): {"que": "stop cumplido sin que el intermediario lo ejecutara", "efecto": "INFORMA", "desde": None},
    ("vigilancia", "H-06"): {"que": "métrica no soportada", "efecto": "AVISO", "desde": None},
    ("vigilancia", "H-07"): {"que": "diferencias de conciliación", "efecto": "AVISO", "desde": None},
    ("vigilancia", "H-08"): {"que": "reducción en curso (REDUCIENDO) que se retoma", "efecto": "INFORMA", "desde": None},
    ("vigilancia", "H-09"): {"que": "instante sospechoso (no se hace nada)", "efecto": "AVISO", "desde": None},
    ("vigilancia", "H-10"): {"que": "salida preparada para el operador (L0/L1)", "efecto": "INFORMA", "desde": None},
    ("vigilancia", "H-11"): {"que": "orden de entrada viva", "efecto": "INFORMA", "desde": None},
    ("vigilancia", "H-12"): {"que": "reducción parcial por una condición OBJETIVO que declara su fracción (una sola vez", "efecto": "INFORMA", "desde": None},
    ("vigilancia", "H-13"): {"que": "posición con el estado de control alterado (no se envía nada por ella)", "efecto": "BLOQUEA", "desde": None},
    ("vigilancia", "H-14"): {"que": "llegó la fecha de revisión de la tesis: la posición pasa a EN_REVISION y la confirma (con fecha nueva) o la cierra el operador", "efecto": "AVISO", "desde": None},
    ("vigilancia", "H-15"): {"que": "se cumplió la condición de reapertura de un expediente en observación (aviso O-31", "efecto": "AVISO", "desde": None},
    ("vigilancia", "H-16"): {"que": "se cumple un escenario de fallo del Contradictor o una invalidez por una métrica que no es el precio: pide revisión y propone", "efecto": "AVISO", "desde": None},
    ("vigilancia", "H-17"): {"que": "la pérdida no realizada pasa el umbral configurado (y otra vez por cada múltiplo): pide revisión", "efecto": "AVISO", "desde": None},
    ("vigilancia", "H-18"): {"que": "falta el dato de una señal (o llega sin unidad, en otra unidad o no numérico): no se evalúa", "efecto": "AVISO", "desde": None},
    ("vigilancia", "H-19"): {"que": "fallo inesperado al vigilar una posición: se informa (degrada su cartera) y se sigue con las demás", "efecto": "AVISO", "desde": None},
}

# Pares de módulos que comparten códigos, con su explicación (cualquiera de las dos órdenes del par).
COLISIONES_ADMITIDAS = {
    ("dimensionado", "validar_encargo"): "la E del dimensionado y la E del encargo: prefijo común con significados distintos; se distingue por el módulo (registro de prefijos del LEEME)",
    ("dimensionado", "mandatos"): "E-01: mandatos (SC-1) valida la forma de las restricciones con los códigos E del encargo, y el dimensionado tiene su propia E-01 de forma de la solicitud",
    ("mandatos", "validar_encargo"): "mandatos (SC-1) valida la forma de las restricciones del encargo y responde con los mismos códigos E que el validador del encargo: mismo código y significado",
    ("control_f", "dimensionado"): "el dimensionado responde con códigos de F (F-01 forma, F-11 valor mínimo, F-12 divisa) porque su viabilidad depende del control de F: mismo código y significado",
    ("control_f", "orquestador"): "el Orquestador lleva constantes de F (los topes que acotan una anulación: F-03, F-04, F-06, F-07, F-09, F-11, F-13, F-14, F-15) para construir el contexto: el código es de F",
    ("dimensionado", "orquestador"): "F-11 (valor mínimo de F) aparece en el dimensionado como frontera de viabilidad y en el Orquestador como tope de anulación: el código es de F",
    ("diario", "orquestador"): "el Diario envuelve al Orquestador: O-00 cuando una operación lanza (misma familia de fallo de la operación, documentado en su docstring) y O-13 por integridad al reaplicar",
    ("ejecucion_g", "orquestador"): "CHOQUE REAL, sin resolver (deuda T-71): G responde O-01 cuando el intermediario no da precio o el instante es ilegible, y el Orquestador usa O-01 para el resto_parcial de condiciones_entrada: mismo código, significados distintos",
    ("diario", "migraciones"): "la infraestructura T-03 reutiliza los códigos de persistencia y del diario con el mismo significado (PE-01, PE-05 y DI-02 al migrar con el diario); documentado en sus docstrings",
    ("diario", "rotacion"): "la infraestructura T-03 reutiliza los códigos de persistencia y del diario con el mismo significado (PE-01, PE-05, DI-02 y O-13 al rotar la clave); documentado en sus docstrings",
    ("diario", "persistencia"): "la infraestructura T-03 reutiliza los códigos de persistencia con el mismo significado (PE-01, PE-05 y PE-07 en el diario; O-13 por integridad); documentado en sus docstrings",
    ("migraciones", "persistencia"): "la infraestructura T-03 reutiliza los códigos de persistencia con el mismo significado (PE-01 y PE-05 al migrar); documentado en sus docstrings",
    ("migraciones", "rotacion"): "la infraestructura T-03 reutiliza los códigos de persistencia y del diario con el mismo significado (PE-01, PE-05 y DI-02 al rotar la clave); documentado en sus docstrings",
    ("persistencia", "rotacion"): "la infraestructura T-03 reutiliza los códigos de persistencia con el mismo significado (PE-01, PE-05 y O-13 al rotar la clave); documentado en sus docstrings",
    ("orquestador", "persistencia"): "CHOQUE REAL, sin resolver (deuda T-70): O-00 es en el Orquestador el rechazo de un instante inválido y en el Diario la marca de una operación que lanza; O-13 es el mismo código de integridad reutilizado por la carga (documentado)",
    ("orquestador", "rotacion"): "O-13 por integridad antes de rotar la clave: el mismo código del Orquestador, reutilizado por la rotación (documentado en su docstring)",
}


def codigos_en_el_codigo(carpeta):
    """Los códigos que aparecen como constantes de texto enteras en los `.py` de `carpeta` (Path o texto),
    excluido este módulo: conjunto de pares `(modulo, codigo)`. Con `ast`, no a grep: solo los ast.Constant
    de tipo str que casan ENTEROS con la expresión, de modo que un comentario o una mención dentro de un
    mensaje más largo no cuentan. Un fichero ilegible no aporta códigos (falla cerrado)."""
    raiz = Path(carpeta)
    out = set()
    for ruta in sorted(raiz.glob("*.py")):
        if ruta.stem == "catalogo_codigos":
            continue
        try:
            arbol = ast.parse(ruta.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, ValueError):
            continue
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str) \
                    and EXPRESION_CODIGO.fullmatch(nodo.value):
                out.add((ruta.stem, nodo.value))
    return out


def _literal_de(nodo):
    """El texto literal de un Constant de tipo str, o la parte literal inicial de un f-string (JoinedStr:
    las Constant hasta el primer hueco), o None."""
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
        return nodo.value
    if isinstance(nodo, ast.JoinedStr):
        partes = []
        for v in nodo.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                partes.append(v.value)
            else:
                break
        return "".join(partes)
    return None


RESULTADOS_EMISION = frozenset({"OK", "ADVERTENCIA", "BLOQUEO"})   # lo que k_calidad pone como argumento


def sitios_de_emision(carpeta):
    """Las llamadas que emiten cada código en los `.py` de `carpeta` (Path o texto), excluido este módulo:
    diccionario `(modulo, codigo) -> {"sitios", "mensajes", "resultados", "envoltorios"}`. Un sitio es una
    llamada con el código como argumento posicional (Constant que casa ENTERO con la expresión, como en
    `codigos_en_el_codigo`); el mensaje es el argumento posicional siguiente (Constant o parte literal de un
    f-string), o el siguiente si aquel es un resultado de `RESULTADOS_EMISION` (k_calidad los lleva entre el
    código y el detalle), o el keyword `motivo`/`detalle`; `resultados` junta los de `RESULTADOS_EMISION`
    vistos en la llamada y `envoltorios` el nombre de la función llamada (p. ej. `_bloqueo`). Con `ast`, no
    a grep; un fichero ilegible no aporta nada (falla cerrado)."""
    raiz = Path(carpeta)
    out = {}
    for ruta in sorted(raiz.glob("*.py")):
        if ruta.stem == "catalogo_codigos":
            continue
        try:
            arbol = ast.parse(ruta.read_text(encoding="utf-8"))
        except (OSError, SyntaxError, ValueError):
            continue
        for nodo in ast.walk(arbol):
            if not isinstance(nodo, ast.Call):
                continue
            if isinstance(nodo.func, ast.Name):
                envoltorio = nodo.func.id
            elif isinstance(nodo.func, ast.Attribute):
                envoltorio = nodo.func.attr
            else:
                envoltorio = ""
            args = nodo.args
            for i, a in enumerate(args):
                if not (isinstance(a, ast.Constant) and isinstance(a.value, str)
                        and EXPRESION_CODIGO.fullmatch(a.value)):
                    continue
                d = out.setdefault((ruta.stem, a.value),
                                   {"sitios": 0, "mensajes": set(), "resultados": set(), "envoltorios": set()})
                d["sitios"] += 1
                if envoltorio:
                    d["envoltorios"].add(envoltorio)
                for otro in args[i + 1:]:
                    if isinstance(otro, ast.Constant) and isinstance(otro.value, str) \
                            and otro.value in RESULTADOS_EMISION:
                        d["resultados"].add(otro.value)
                msj = _literal_de(args[i + 1]) if i + 1 < len(args) else None
                if msj in RESULTADOS_EMISION and i + 2 < len(args):
                    msj = _literal_de(args[i + 2])
                if msj is None:
                    for kw in nodo.keywords:
                        if kw.arg in ("motivo", "detalle"):
                            msj = _literal_de(kw.value)
                            break
                if msj:
                    d["mensajes"].add(msj.strip())
    return out


def prefijos_del_leeme(ruta):
    """Los prefijos que registra la tabla «Registro de prefijos de códigos» del LEEME, sin el guion
    (por ejemplo «V», «RM» o «PE») (Path o texto)."""
    contenido = Path(ruta).read_text(encoding="utf-8")
    inicio = contenido.find("## Registro de prefijos de códigos")
    if inicio < 0:
        return set()
    fin = contenido.find("\n## ", inicio + 1)
    bloque = contenido[inicio:fin if fin > 0 else len(contenido)]
    out = set()
    for linea in bloque.splitlines():
        if not linea.strip().startswith("|"):
            continue
        primera = linea.split("|")[1]
        for m in re.finditer(r"`([A-Z]{1,2}-)`", primera):
            out.add(m.group(1)[:-1])   # prefijos sin el guion: «V», «RM», «PE»…
    return out


def como_markdown():
    """El catálogo como tabla Markdown ordenada por módulo y código (módulo, código, qué hace, efecto,
    prioridad, desde y notas de retirada)."""
    filas = ["| Módulo | Código | Qué hace | Efecto | Prioridad | Desde | Notas |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    for (modulo, codigo) in sorted(CATALOGO):
        d = CATALOGO[(modulo, codigo)]
        notas = d.get("motivo", "") if d.get("retirado") else ""
        desde = d["desde"] if d["desde"] is not None else ""
        filas.append(f"| `{modulo}` | `{codigo}` | {d['que']} | {d['efecto']} | {d.get('prioridad', '')} | "
                     f"{desde} | {notas} |")
    return "\n".join(filas)
