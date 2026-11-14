# T-118 · Análisis técnico

## Causa raíz o motivo

La QA r02 de T-112 (veredicto APTO) dejó siete hallazgos abiertos. Todos están en el Motor Fase 2 del Bloque A.

| ID | Causa |
| --- | --- |
| H-09 | El grupo R recibía `ent["fecha_corte"]` y no la leía. ML-PRED-001 solo comprobaba su propia regla de fuga (`conocible_desde` ≤ fecha de uso), no el corte de la petición. ML-CAL-001 tenía el mismo hueco cuando sus pares llevan fecha; la QA no lo vio porque sus casos de control no traen fechas |
| H-10 | La r02 de T-112 acotó los parámetros de tamaño, no los datos. En R, `_vector` y `_rendimientos` leían listas de cualquier longitud. BT-VAR-001 en modo generado ajusta un modelo por observación, y BT-PBO-001 ordena las configuraciones en cada una de sus hasta 184 756 combinaciones |
| H-11 | Desde la r02 de T-112 las fichas leen números de la configuración del Motor, pero el artefacto no los guardaba. `reejecutar` recalculaba con la configuración vigente y, si la cifra cambiaba con la misma versión de ficha, culpaba al original |
| H-12 | S y P no recibían la configuración: su envoltura la descartaba (S) o no la leía (P). Las cotas «de la configuración» estaban copiadas como literales |
| H-13 | Tres sitios de `servir` fuera de un `try`: la copia de `valores` (`copy.deepcopy`), la comparación de las dos semillas (`!=` con un array) y `clase` y `perfil` usados como condición. Además, un campo muy anidado pasaba la comprobación de la forma (`json.dumps` lo admite) y agotaba la pila al copiarlo para escribirlo en RC |
| H-14 | `reejecutar` llamaba al manejador sin capturar `ErrorFicha` |
| H-15 | Las cifras de los documentos se escribieron antes de cerrar los casos de control |

## Evidencia

Los scripts del revisor, sin tocar, antes (según `.docs/tickets/T-112/qa.md`) y después. Se ejecutan con `.venv/bin/python -I .docs/tickets/T-112/revisores/<script>`.

| Script | Hallazgo | Antes | Después |
| --- | --- | --- | --- |
| `r02_03_fecha_corte_y_cache.py` | H-09 | 14/17; ML-PRED-001 entre las fichas que sirven datos posteriores al corte | 14/17; ML-PRED-001 ya no está. Los tres fallos que quedan no son hallazgos (ver abajo) |
| `r02_02_costes_y_tamanos.py C` | H-10 | BT-VAR-001 con 100 000 rendimientos no termina en 300 s; BT-PBO-001 con 3 000 configuraciones, 118 s | 3/3. Los dos se rechazan en 0,1 s y 0,3 s. Las llamadas admitidas tardan como mucho 17,9 s |
| `r02_07_semillas_ct10_config.py` | H-11, H-12, H-14 y H-15 | 32/36 | **36/36**. DEC-VOI-001 con el umbral E cambiado: SI. Artefacto con un parámetro fuera de cota: NO y ERROR_REEJECUCION. 136 casos de control |
| `r02_01_hostiles_anidados.py` | H-13 | 706 `RecursionError` y 16 escapes en los campos de la petición | Ver `pruebas.md` |

Los tres fallos que quedan en `r02_03` ya estaban en la QA r02 y no son hallazgos:
- dos son falsos positivos que el propio revisor declara: el vencimiento de un bono o de un futuro es posterior al corte por naturaleza (FIR-PRICE-001, CHR-FUND-001), y REI-FFO-001 rechaza con razón un ejercicio que cierra el día del corte;
- el tercero es la observación de la caché, que entrega el mismo objeto a todos los clientes. Es del ejecutor original y queda fuera de este ticket.

## Implementación

### Archivos cambiados

| Archivo | Hallazgo | Qué cambia |
| --- | --- | --- |
| `bloque_a/motor/fichas_riesgo.py` | H-09 | `_corte` y `_hasta_corte` (nuevas). `f_ml_pred` rechaza si la última de `fechas`, o de `conocible_desde` de una variable, es posterior al corte. `f_ml_cal` rechaza si lo es la última fecha de sus pares |
| `bloque_a/motor/fichas_riesgo.py` | H-10 | Bloque «cotas de los datos» detrás de `UMBRALES`. `_observaciones_maximas` y `_acotado` (nuevas). `_vector`, `_rendimientos`, `_dinamica`, `_matriz_pbo` y `_alinear` aceptan un máximo, que se comprueba antes de leer los elementos. Lo usan `_datos_var`, `f_sim_mc`, `f_scn_h`, `f_bt_dsr`, `f_bt_pbo`, `f_bt_var`, `f_ml_cal`, `f_ml_pred` y `_prior` |
| `bloque_a/motor/servicio.py` | H-11 | `_ConfiguracionLeida` y `_configuracion_usada` (nuevas). `_contexto` acepta la configuración que entrega. `servir` guarda `artefacto.configuracion_usada`. `reejecutar` re-ejecuta con ella y clasifica |
| `bloque_a/motor/servicio.py` | H-13 | `PROFUNDIDAD_MAXIMA`, `_demasiado_anidado` y `_distintas` (nuevas). `_error_de_forma` comprueba la profundidad y el tipo de `clase` y `perfil`. `servir` compara las semillas con `_distintas` y convierte `RecursionError` y `MemoryError` de la resolución de datos en RECHAZADO |
| `bloque_a/motor/servicio.py` | H-14 | `reejecutar` captura el fallo del manejador y lo registra |
| `bloque_a/motor/fichas_series.py` | H-12 | `OBS_MAXIMAS_SERIES` y `OBS_MAXIMAS_REGIME` salen de `por_defecto.yaml`. `_configuracion` y `_obs_maximas` (nuevas). `_cerrado` conserva la configuración, `_parametros` pone la cota del Motor y `_univariante` la usa |
| `bloque_a/motor/fichas_reales.py` | H-12 | `SESIONES_SEMANA` sale de `por_defecto.yaml`. `_configuracion` (nueva). `_validar_parametros` y `_parametros` aceptan la configuración, y `f_chr_flow` se la pasa |
| `tests/test_t118_hallazgos.py` | todos | Nuevo |
| `tests/test_fase2_riesgo.py` | H-10 | Dos pruebas de T-112 usaban 3 000 observaciones, por encima de la cota nueva. Ahora usan 2 520 (`H5`); sus comprobaciones no cambian |
| `tests/test_t112_motor.py` | H-11 | Una prueba exigía que la ficha recibiera el mismo objeto que `Motor.cfg` (`is`). Ahora recibe esa configuración dentro del registro de lecturas: la prueba exige que sea igual (`==`) |
| `.docs/tickets/T-112/README.md`, `pruebas.md`, `analisis-tecnico.md` | H-15 | Cifras corregidas, marcando las viejas |
| `docs/incidencias.md` | — | INC-T118-01 |

### Cotas de los datos del grupo R (H-10)

| Ficha | Dato | Cota | Origen |
| --- | --- | --- | --- |
| Todas menos DEC-VOI-001 | Una historia: rendimientos (en línea o serie de HT-01), residuos, VaR previsto, resultados, pares, fechas, observaciones de cada configuración | Sesiones de H5: 2 520 por defecto | `horizontes.H5` y `calendario` de la configuración del Motor, en cada llamada |
| RISK-VAR-001 | `distribucion.rendimientos` (de MC-05) | 1 000 000 | Máximo de trayectorias de SIM-MC-001 («Parámetros») |
| DEC-VOI-001 | `muestras.valores` | 1 000 000 | El mismo |
| SCN-H-001 | Estados de `regimen` | 4 | REG-HMM-001, «Parámetros»: n_estados 2–4 |
| ML-CAL-001 | Horizontes | 5 | `HORIZONTES` del Documento 0 (H1–H5) |
| BT-PBO-001 | Configuraciones | 1 000 | `[PROPUESTO]` INC-T118-01: la cota de contrastes de ST-INF-001 |
| ML-PRED-001 | Variables | 20 | `[PROPUESTO]` INC-T118-01: el tope que la ficha da a la rejilla |
| Petición (H-13) | Niveles de anidamiento | 32 | `[PROPUESTO]` INC-T118-01, técnico |

Ninguna se puede cambiar desde la petición: una clave de `UMBRALES` en los parámetros se rechaza, como antes.

### Decisiones tomadas

Las que la especificación dejaba abiertas están en INC-T118-01. Las de implementación:

- **H-09.**
  - Se compara por día. Con el corte en la última fecha de los datos, se sirve.
  - `conocible_desde` se comprueba antes que la regla de fuga de la ficha, para que el motivo sea el corte.
- **H-10.**
  - BT-VAR-001 en modo generado no necesita un presupuesto aparte: con la historia acotada, el caso más caro es el de la ventana más corta.
  - Los datos y las series de HT-01 comparten cota. Con n + 1 precios se admiten n rendimientos.
- **H-11.**
  - No hay una lista escrita a mano de «qué lee cada ficha». La ficha recibe la configuración del Motor en un `dict` que apunta las secciones (claves de primer nivel) que se le consultan. Lo que se guarda es lo que de verdad se leyó en esa llamada.
  - De cada sección se guarda su valor en la configuración del Motor y la huella de la misma sección en `por_defecto.yaml`. La huella hace falta porque `parametro` toma de ahí lo que la configuración del Motor no traiga.
  - Una ficha que no lee la configuración deja `configuracion_usada: {}`. No es lo mismo que no tener el campo (artefacto anterior).
  - Clasificación cuando el resultado no coincide, con datos y versión iguales:
    - consta toda la configuración leída y es la vigente: ERROR_ORIGINAL, como antes;
    - falta alguna sección o alguna ya no es la vigente: CONVENCION_DISTINTA, y el diagnóstico nombra las secciones.
  - Si coincide, es SI aunque la configuración haya cambiado. La entrada lo anota en `reejecucion.configuracion`.
  - Los seis casos de control de AUD-REX-001 no cambian. El caso con otra configuración es una prueba, no un caso de control nuevo: así no cambia el recuento y no hay conflicto con quien añade fichas.
- **H-12.**
  - `UMBRALES` de S y P sigue mostrando números, ahora calculados de `por_defecto.yaml` al importar. En cada llamada manda la configuración del Motor.
  - Los extremos de los rangos de H2 y H5 (8 semanas, 30 años) no están en la configuración y se quedan en el código. Ver INC-T118-01.
- **H-13.**
  - La profundidad se mide con una pila propia, sin recursión, antes de copiar o escribir nada. El rechazo no depende de cuánta pila le quede al llamador.
  - Se mantiene además la captura de `RecursionError` en la resolución de datos, como segunda barrera.
  - No hay una captura general alrededor de `servir`. Taparía un fallo posterior a la escritura en RC y dejaría un RECHAZO detrás de un SERVICIO.
- **H-14.** La categoría es `ERROR_REEJECUCION`, que el esquema del Registro V2.0 ya tenía. Lo que R16 declara imposible sigue lanzando su excepción: sin motivo, sin artefacto o sin los valores en línea.

### Desviaciones

- Se tocaron tres pruebas de T-112 (tabla de arriba). Ninguna pierde una comprobación.
- No se actualizó `bloque_a/11_Ejecutor/README.md`: no describe ni las cotas ni CT-10, y otro trabajo en curso lo está editando.

### Límites conocidos

- **Granularidad de H-11.** Se guarda la sección entera (por ejemplo, todo `evaluacion`). Si cambia una clave de esa sección que la ficha no usa, la re-ejecución la da por «distinta de la vigente». Solo tiene efecto cuando además el resultado no coincide: sale CONVENCION_DISTINTA en vez de ERROR_ORIGINAL.
- **Lecturas que no se apuntan.** El registro apunta `[]`, `get` e `in`. Una ficha que recorriera la configuración entera (`items`, iteración) no quedaría apuntada. Hoy ninguna lo hace: todas leen con `parametro`, `parametros_ht03` y `sesiones_horizonte`.
- **Artefactos anteriores.** Se re-ejecutan con la configuración vigente. Si su ficha lee la configuración y el resultado no coincide, la categoría es CONVENCION_DISTINTA, también cuando la causa sea un resultado alterado.
- **Errores de datos en `reejecutar`.** Una serie de HT-01 que ya no está disponible sigue lanzando la excepción del proveedor. H-14 solo cubre el rechazo de la ficha.
- **Cotas de S que siguen a mano.** Las 520 semanas de REG-HMM-001 y los 360 meses de TEM-DIFF-001 se derivan de los rangos de H5. La QA no las señaló y no se han tocado.
- **Coste.** El servicio más caro del grupo R tarda 52 s por el Motor. Los más caros del Motor siguen siendo los del grupo S que midió la QA r02 (REG-HMM-001 y FX-REGIME-001, 52 s y 76 s), fuera de este ticket.

### Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/pytest -q tests/test_t118_hallazgos.py
../../.venv/bin/pytest -q tests/test_fase2_series.py tests/test_fase2_riesgo.py tests/test_fase2_valoracion.py tests/test_fase2_reales.py
../../.venv/bin/pytest -q tests/test_t112_motor.py tests/test_t113_deuda.py tests/test_t106_*.py tests/test_integracion.py
../../.venv/bin/python ../../.docs/tickets/T-118/revisores/impl_costes_motor.py
cd ../..
.venv/bin/python -I .docs/tickets/T-112/revisores/r02_07_semillas_ct10_config.py
.venv/bin/python .docs/tickets/T-118/revisores/impl_mutantes.py "$PWD" /tmp/t118_mut
```
