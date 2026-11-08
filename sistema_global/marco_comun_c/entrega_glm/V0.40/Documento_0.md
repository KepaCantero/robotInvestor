# Documento 0 — Pantalla de aprobación con las cifras de la §8 (V0.40) — GLM, pendiente de revisión

## 1. Problema y alcance

Desde V0.36 (T-22), F decide con un contexto que construye el Orquestador: el precio del intermediario con su hora, la actividad del día (importe ya autorizado, órdenes de la última hora y pérdida de la semana), los eventos del calendario de K y la política con sus límites (F-13 a F-23). Pero la pantalla de aprobación de la §6 solo enseña las cifras de la propuesta (cantidad, precio límite, stop, importe, riesgo, tipo de cambio…): el operador aprueba sin ver con qué cifras del contexto decidió F y, para verlas, tendría que abrir el informe CT-G-08. La Constitución pide lo contrario: la cola de aprobaciones presenta «cifras calculadas por F, sin texto de un LLM», y el operador debe poder ver con qué datos se tomó la decisión.

**Qué entra en esta versión.** La pantalla de aprobación (`pantalla_aprobacion`) añade diez campos con las cifras de la §8 que F usó, todos sacados del propio informe de F (`entradas.contexto` y `entradas.politica`) y colocados antes del cálculo del hash: como el hash de la pantalla cubre los campos nuevos, el operador aprueba también esas cifras. Batería nueva `pruebas/pruebas_pantalla_f.py` (28 comprobaciones).

**Qué queda fuera.** No cambia `_comprobar_aprobacion`: ya recalcula el hash de la pantalla guardada (excluyendo `hash` y `usada`), de modo que tocar cualquier campo nuevo de la pantalla guardada rompe la aprobación con O-27 sin tocar una línea. No se toca `consola.py` (hoy no presenta pantallas al operador). No se recalcula nada con el estado actual: si el estado cambió desde la emisión del informe, la pantalla sigue mostrando lo que F vio (y los controles O-10 ya impiden autorizar con un informe que no vio lo autorizado después). No hay configuración nueva, ni reglas nuevas, ni decisiones del operador que ratificar: no hay filas de deuda ni valores [PROPUESTO].

## 2. Diseño

**Dónde.** En `validador/orquestador.py`, método `pantalla_aprobacion`: después de construir el diccionario `p` con las cifras de siempre y antes de `p["hash"] = _hash(p)`. Nada más cambia en el método: la anulación de veto sigue calculando `q` (la cantidad que F habría aprobado sin el veto) antes de construir `p`, así que el importe de la pantalla y el importe del día ya usan la cantidad anulada «como ya se hace».

**De dónde salen las cifras.** De `cf = aplanar_informe(control_f)`, es decir de `cf["entradas"]["contexto"]` y `cf["entradas"]["politica"]` del propio informe. Cuando el flujo llega a construir la pantalla, el informe ya pasó `validar_informe_f` (CF-01 a CF-09) dentro de `_comprobar_autorizacion`: CF-07 exige que la política sea la oficial del Orquestador y CF-09 que el contexto sea exactamente el que el Orquestador habría dado en el instante de emisión. Además, CF-04 recalculó F con esas mismas entradas sin error, y `_forma_contexto` valida la forma del contexto (el precio del intermediario es None o `{valor, fecha_hora}` con valor finito y mayor que cero; la actividad lleva sus tres cifras; los eventos son una lista o None). Por eso las lecturas no pueden lanzar y no hacen falta valores por defecto disimulados: si algo no está, es None y se muestra como None (caso prudente).

**Campos nuevos de la pantalla** (nombres exactos, en el mismo orden en que se añaden):

| Campo | Origen | Qué enseña |
| --- | --- | --- |
| `precio_intermediario` | `contexto.precio_intermediario["valor"]` | La última cotización de G que F vio para el instrumento; None si no hay |
| `precio_intermediario_en` | la `fecha_hora` de esa cotización | Cuándo se la dio G; None si no hay precio |
| `deriva_pct` | `round(abs(limite / precio - 1) * 100, 4)` | La misma deriva que mide F-23 entre el límite de entrada de la propuesta y el precio del intermediario; None si no hay precio. El precio es mayor que cero por `_forma_contexto`: no hay división por cero |
| `importe_dia_eur` | `round(contexto.actividad.importe_dia_eur + importe, 2)` | Lo que quedaría autorizado hoy si se aprueba esta pantalla: lo ya autorizado por los demás expedientes (el contexto del informe excluye el propio, `_actividad(expediente_id, a)`) más el importe de esta pantalla; con anulación de veto, el importe es el de la cantidad anulada |
| `limite_dia_eur` | `politica.importe_max_dia_eur` | El límite de F-14 con el que F controló |
| `perdida_semana_eur` | `contexto.actividad.perdida_semana_eur` | La pérdida de la semana que F vio (F-16) |
| `limite_semana_eur` | `politica.perdida_semana_max_eur` | Su límite |
| `ordenes_ultima_hora` | `contexto.actividad.ordenes_ultima_hora` | Las órdenes de la última hora que F contó (F-17) |
| `limite_ordenes_hora` | `politica.ordenes_max_hora` | Su límite |
| `eventos_f` | `contexto.eventos`, tal cual (copia profunda) | Los eventos del calendario de K que F usó para F-21; pueden ser None. Copia profunda para que la pantalla guardada no comparta objetos con el informe del llamador |

**Hash y aprobación.** `p["hash"]` se calcula después de añadir los campos, de modo que el hash de la pantalla ata también estas cifras: el operador las aprueba al aprobar la pantalla. `_comprobar_aprobacion` no cambia: compara el hash recalculado de la pantalla guardada (excluyendo `hash` y `usada`) con el hash citado en la aprobación, así que una pantalla guardada alterada en cualquier campo nuevo da O-27. La pantalla sigue siendo solo cifras: ni «texto», ni «resumen», ni «tesis».

**Casos límite.**

- Sin cotización registrada del intermediario: `precio_intermediario`, `precio_intermediario_en` y `deriva_pct` a None. Por los flujos públicos esa pantalla no es alcanzable: F-23 veta («sin precio del intermediario») y F-23 no está entre los vetos anulables (solo lo están F-09 y F-11, VETOS_ANULABLES), y un informe vetado solo por F-09/F-11 exige F-23 en OK, es decir, con precio presente. La lectura a None es defensiva (fail-closed): si un informe llegara con el precio ausente, la pantalla enseña None en vez de inventarse una cifra o de lanzar.
- Anulación de veto: `q` es la cantidad anulada; `p["importe"]` y `importe_dia_eur` la usan, igual que el resto de cifras de la pantalla.
- Informe VETADO sin anulación: no hay pantalla (O-06, como siempre); los campos nuevos no cambian ese camino.
- Determinismo: las cifras vienen del informe, que ya está fijado; no hay reloj del sistema ni azar. Dos llamadas con los mismos argumentos dan la misma pantalla y el mismo hash.
- Consola: hoy no presenta pantallas (no hay ninguna referencia a pantallas en `consola.py`): no se toca.

## 3. Reglas y comprobaciones

No hay reglas ni avisos nuevos: el cambio no añade códigos (ninguna entrada nueva en `PRIORIDAD_AVISO` ni prefijo nuevo en el registro). Refuerza los existentes:

| Código o regla | Qué pasa ahora | Efecto |
| --- | --- | --- |
| §6 (cola de aprobaciones) | La pantalla enseña las cifras de la §8 con las que F decidió (tabla de la sección 2), junto a las de la propuesta | El operador ve con qué datos aprobó F sin abrir el CT-G-08 |
| O-27 (aprobación atada a la pantalla) | El hash de la pantalla cubre los diez campos nuevos (se calcula después de añadirlos) | Tocar un campo nuevo de la pantalla guardada rompe la aprobación: `autorizar` da O-27; aprobar la pantalla es aprobar también estas cifras |
| CF-07 y CF-09 (informe de F) | Son los que garantizan que `entradas.politica` es la oficial y `entradas.contexto` el del Orquestador al instante de emisión | Las cifras de la pantalla no se pueden manipular desde el informe: si el contexto no es el exacto, no hay pantalla (O-01) |
| F-14, F-16, F-17, F-21, F-23 | Sus límites y cifras se muestran (`limite_dia_eur`, `limite_semana_eur`, `limite_ordenes_hora`, `eventos_f`, `deriva_pct`) | Solo se muestran: el que veta o recorta sigue siendo F en su flujo de siempre; la pantalla no es un control nuevo |

Cambios en reglas existentes: ninguno (ni `control_f.py` ni `_comprobar_aprobacion` cambian; las 62 comprobaciones de `pruebas_aprobacion.py` pasan sin tocar una línea).

## 4. Códigos, API, pruebas y revisión independiente

**Funciones nuevas o cambiadas.** Una sola, con la misma firma: `Orquestador.pantalla_aprobacion(expediente_id, control_f, ahora, actor="OPERADOR", anular_veto=None)` — añade los diez campos de la sección 2 al diccionario `p` antes de `p["hash"] = _hash(p)`. No hay funciones nuevas, ni atributos nuevos, ni configuración nueva (`version_config` no sube), ni mensajes nuevos.

**Batería nueva.** `pruebas/pruebas_pantalla_f.py`, 28 comprobaciones: los campos nuevos coinciden con el contexto del informe (precio y deriva, actividad y límites, eventos); la pantalla no recalcula con el estado actual (una cotización nueva del intermediario no cambia la pantalla ya construida); `deriva_pct` calculada a mano con un precio distinto del límite (cotización 1,11 registrada con `o.registrar_cotizacion` antes del informe, dentro del 2 % de F-23: 0,9009 %) y tocar `deriva_pct` en la pantalla guardada da O-27; `importe_dia_eur` suma lo ya autorizado hoy (110,00 € en el primer expediente; 220,00 € para otro expediente tras autorizar el primero por 110,00 €, con `hasta(o, "AUTORIZADA")` y `hasta(o, "PROPUESTA", n=3)`); el hash guardado cubre toda la pantalla y cada campo nuevo por separado (diez comprobaciones, una por campo); dos pantallas del mismo informe dan el mismo hash; la pantalla sigue sin textos; con la anulación de un veto (informe F-09 con el tope F-14 recortando a 86,363636 unidades y F-11 veta) la cantidad es la anulada (86,363636), el importe 95,00 € y `importe_dia_eur` 205,00 €, no los 220,00 € que daría la cantidad pedida, y la autorización llega tras el enfriamiento.

**Pruebas antiguas que cambiaron:** ninguna. El bucle completo (`ejecutar_pruebas.py` + las 37 baterías de `pruebas/pruebas_*.py`) pasa entero: 38 ejecuciones, ninguna línea FALLA.

**Revisión independiente.** Ejecutada (sección 7 de las directrices) en otra conversación, con el ZIP de la pieza en verde y el prompt de la sección 7, sin el historial de la pieza; un hallazgo reproducible, de documentación y gravedad baja, corregido (el detalle, en `entrega_glm/V0.40/revision.md`; los scripts del revisor quedan intactos byte a byte en la raíz de `marcoC/` y dan OK tras el arreglo):

- **Hallazgo 1 (baja), `hallazgo_v40_1_doc_cuenta_comprobaciones.py`:** el resumen de la sección 1 decía que la batería nueva tiene 21 comprobaciones y la batería define y ejecuta 28 (la cifra que ya daban la propia sección 4 de este documento, `LEEME.md`, `notas_briefing.md` y la salida real): cifra resumida obsoleta, sin efecto en el código ni en las pruebas. Arreglo: 21 → 28 en el resumen. Regresión: el propio script del revisor, que queda como comprobación re-ejecutable (FALLA antes, OK después); no se añade comprobación a la batería para no acoplarla a los documentos de entrega. Además, el revisor verificó el diff completo V0.39 → V0.40, reejecutó las 38 baterías (todas en verde), comprobó el determinismo de la batería nueva (dos ejecuciones, diff vacío) y ejecutó nueve sondas adversariales propias (`sondas_revisor_v040.py`: contexto extranjero, NaN, precio 0 o ausente, infinitos, entero 10**400, mutación del informe tras la pantalla y manipulación de cada uno de los diez campos de la pantalla guardada): todas cierran (O-01/O-06/O-34/O-27, sin pantalla y sin adelantar estado); también comprobó la no-vacuidad de la batería (contra el código de V0.39 falla enseguida con KeyError) y los dos scripts de los hallazgos de T-40 de la revisión anterior siguen en OK (r01/r02, fuera de esta pieza).

**Baterías que pasan:** 38 de 38 (37 baterías + el bucle de `ejecutar_pruebas.py`), entre ellas la nueva `pruebas_pantalla_f.py` (28 comprobaciones, determinista: dos ejecuciones, misma salida).

## 5. Límites y deuda técnica

- **La pantalla solo muestra; no re-comprueba.** Los límites que enseña son los que F ya aplicó al decidir: si el operador aprueba con un campo en rojo (por ejemplo `importe_dia_eur` por encima de `limite_dia_eur`), es que F vetó o recortó por eso, y la pantalla lo enseña; nada nuevo veta en la pantalla.
- **Las cifras son las de la emisión, no las actuales.** Por diseño (y exigido por CF-09), la pantalla muestra el contexto congelado del informe: si el precio del intermediario o la actividad cambiaron después, la pantalla no lo sabe (y los controles O-10 ya impiden autorizar con un informe que no vio una autorización posterior).
- **La pantalla sin precio del intermediario no es alcanzable por flujos públicos:** F-23 veta sin precio y no es anulable (solo lo son F-09 y F-11), y un informe vetado solo por F-09/F-11 exige F-23 en OK. La lectura a None de `precio_intermediario`, `precio_intermediario_en` y `deriva_pct` es defensiva (fail-closed); lo mismo cabe decir de `eventos_f` a None.
- **Deuda técnica:** ninguna fila cambia. No hay decisiones nuevas que ratificar: los límites mostrados son los de D-11, ya abiertos. La pieza no toca T-40 ni ninguna otra deuda abierta.

