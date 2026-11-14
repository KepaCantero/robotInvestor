# T-121 · Análisis técnico

## Causa raíz o motivo

- **H-04.** Las fichas de la Fase 1 (T-106) se escribieron antes de que el Motor pasara la fecha de corte a las fichas (`ent["fecha_corte"]`, H-07 de la QA r01 de T-112). La Fase 2 y la P2 la leen con `_corte` y `_hasta_corte`; `fichas_mon_idx.py` y `fichas_tcv.py` no la leían, y `fichas_fon_der.py` solo usaba una «fecha de corte» propia de FON-DISC-001 y FON-FLOW-001, que es la última fecha de sus datos. El servicio solo comprobaba las series de HT-01 (FUGA_DE_INFORMACION), no los valores en línea.
- **H-01.** T-118 hizo que la re-ejecución usara la configuración guardada en el artefacto, pero la clasificación siguió mirando si la configuración vigente era otra (`cambiadas`): un cambio de cualquier clave de una sección leída pasaba un error real del original a CONVENCION_DISTINTA, aunque la re-ejecución sí había reproducido sus condiciones.
- **H-02.** `_error_de_forma` miraba la forma y la profundidad, no que lo que va al Registro se pudiera escribir: `Almacen.escribir` copia, serializa como JSON y codifica en UTF-8, y fallaba con un sustituto Unicode suelto, un generador o una clave que no es de JSON. Los argumentos `solicitante`, `run_id` y `msg_id` no se miraban.
- **H-03.** En `reejecutar`, la resolución de los datos y la lectura del artefacto estaban fuera del `try` que registra la re-ejecución fallida (T-118 solo cubría el rechazo de la ficha).
- **H-05.** `UMBRALES["REG-HMM-001"]["obs_maximas"]` era el literal 520, derivado a mano de `horizontes.H5` (120 meses).
- **H-06.** Cinco correcciones de T-118 sin una prueba que fallara al deshacerlas.

## Evidencia

Scripts del revisor de T-118, sin modificar, desde la raíz de la copia (`.venv/bin/python -I -W ignore .docs/tickets/T-118/revisores/<script>`). «Antes» es lo que dejó escrito la QA r01 de T-118 en su `qa.md`, y en H-04 también una sonda propia contra el código anterior (el de `develop`, sin T-121): con el corte en la víspera de la última fecha observada, los 42 casos de control de las 14 fichas se servían.

| Hallazgo | Script | Antes | Después |
| --- | --- | --- | --- |
| H-04 | `r01_01_h09_fecha_corte.py` | 14 fichas de la Fase 1 servían con el corte en la víspera (40 casos según el revisor; 42 según la sonda) | **60/60**; de los 148 casos con fechas, 20 se sirven con el corte en la víspera y todos son fechas futuras por naturaleza: vencimientos (CHR-FUND, FIR-PRICE, REI-LEV), desbloqueos (CHR-TOKEN), efectividad anunciada (IDX-REB) y reuniones (MON-EXP). Ninguna de las 14 |
| H-01 | `r01_03_h11_ct10_configuracion.py` | Bloque 5: NO / CONVENCION_DISTINTA al cambiar el umbral E, otra clave de `parametros_ht03` o `horizontes.H1` | **34/34**; bloque 5: ERROR_ORIGINAL en los cuatro cambios |
| H-02 y H-03 | `r01_05_h13_h14_fuzz.py` | Bloque 1: 104 escapes en 5 758 llamadas; bloque 3: 33 de 124 artefactos alterados escapan | Ver `pruebas.md` |
| H-05 | `r01_04_h12_configuracion.py` | REG-HMM-001 seguía en 520 con H5 en 60 meses | **47/47**; con H5 en 60 meses, 260 |
| H-06 | `r01_07_mutantes.py --solo M05,M38,M50,M68,M78` | Los cinco vivos | Ver `pruebas.md` |

## Implementación

### Archivos cambiados y por qué

| Archivo | Hallazgo | Cambio |
| --- | --- | --- |
| `bloque_a/motor/fichas_fon_der.py` | H-04 | `_hasta_corte_peticion` (por día, sin confundirla con la «fecha de corte» de la ficha); en `f_fon_disc` y `f_fon_flow` sobre `fechas` (la `fecha_nav` de cada miembro ya no puede pasar de la última fecha) y en `_rend_diarios` (FON-LEV-001) sobre las fechas de las rentabilidades |
| `bloque_a/motor/fichas_mon_idx.py` | H-04 | `_corte`, `_dia` y `_hasta_corte`. MON-YLD: la fecha de cada segmento y la historia de cada diferencial. MON-EXP: la fecha de los datos y la de cada decisión ya tomada (no los nodos, los contratos ni las reuniones). MON-REAL: fin del periodo y *vintages* de cada renovación, e historia ex ante. MON-FIX: la fecha. IDX-ERP: historia del múltiplo, historia del BPA real y fecha del consenso (`_erp_indice` recibe el corte). IDX-CONC: composición, precios, índices ponderado y equiponderado e historia de las métricas. IDX-REL: las dos historias. IDX-REB: anuncio, fecha de los activos indexados y rentabilidades de los eventos comparables (`_car_evento`); no la efectividad |
| `bloque_a/motor/fichas_tcv.py` | H-04 | `_PosteriorAlCorte` (subclase de `ErrorFicha`), `_corte` (un número, un booleano o una lista no son una fecha) y `_hasta_corte`. TCV-SLOPE: fechas de la curva (los `conocible_desde` ya no pasan de su fecha). TCV-BEI: encuestas e historia. TCV-CDS y TCV-VIXTS: historia. TCV-TP: curva de ACM, serie publicada y encuesta; en `f_tcv_tp`, un dato posterior al corte en la segunda vía rechaza la petición en vez de degradarse a «segunda vía no calculada» |
| `bloque_a/motor/fichas_series.py` | H-05 | `SEMANAS_POR_ANIO`, `MESES_POR_ANIO`, `_semanas_h5(cfg)` y `OBS_MAXIMAS_HMM`; `_obs_maximas("REG-HMM-001", cfg)` lee H5 de la configuración del Motor en cada llamada |
| `bloque_a/motor/servicio.py` | H-02 | `CAMPOS_REGISTRO`, `CAMPOS_TEXTO` y `_escribible`; `Motor._error_de_forma` rechaza lo que no se puede escribir y `horizonte`, `modo` y `prioridad` que no son texto; `Motor.servir` comprueba `solicitante`, `run_id` y `msg_id` (la entrada los lleva vacíos; un solicitante que no es texto sigue siendo CANAL_NO_AUTORIZADO, la regla de T-112 r02 H-06) y su firma admite `solicitante: Any` (lo valida) |
| `bloque_a/motor/servicio.py` | H-03 | `Motor.reejecutar`: la resolución de los datos, la ficha del artefacto y la lectura de sus parámetros y su resultado van dentro de un `try`; `Motor._reejecucion_fallida` y `_reejecucion_fallida_entrada` registran NO / ERROR_REEJECUCION con la causa |
| `bloque_a/motor/servicio.py` | H-01 | `Motor.reejecutar`: `no_reproducidas` (secciones leídas sin registro, registros ilegibles, y secciones cuya huella de `por_defecto.yaml` ha cambiado y de las que el valor guardado no trae todas las claves, `_cubre`) sustituye a «sin registro o distinta de la vigente» como condición de CONVENCION_DISTINTA. `distinta_de_la_vigente` sigue anotándose en la entrada |
| `tests/test_t121_hallazgos.py` | todos | Nuevo: 116 pruebas |
| `tests/test_t118_hallazgos.py` | H-01, H-05, H-06 | `test_h11_error_original_…` pide ahora ERROR_ORIGINAL con la configuración vigente cambiada (H-01); `test_h12_las_cotas_de_s_y_p_…` ya no exige que REG-HMM-001 se quede en 520 con H5 en 60 meses (H-05); cinco pruebas nuevas (siete con los parámetros) para M05, M38, M50, M68 y M78 (H-06), con el hallazgo de origen en el nombre para que el script del revisor las filtre con `-k` |
| `tests/test_t106_motor.py`, `tests/test_t106_r03.py` | H-04 | Servían los casos de control con el corte en 2026-11-12, y los datos sintéticos de IDX-ERP-001 llegan a 2029-12-31: el corte pasa a esa fecha. Las afirmaciones no cambian |
| `docs/incidencias.md` | — | INC-T121-01 |
| `.docs/tickets/T-121/revisores/impl_mutantes.py` | — | Mutantes de las correcciones |

### Decisiones tomadas y desviaciones del plan

- Todas en INC-T121-01 `[PROPUESTO]`. Las que más pesan: qué fechas son observaciones (H-04), la regla de CONVENCION_DISTINTA (H-01) y el motivo de un solicitante que no es texto (H-02).
- **H-01, más allá de la sugerencia del revisor.** Mirar solo la huella de `por_defecto.yaml` volvería a ablandar la categoría tras la sesión T-57, que cambiará ese fichero: el artefacto guarda la sección entera, pero su huella ya no sería la vigente. Por eso la huella solo cuenta si el valor guardado no trae todas las claves de la sección del fichero actual (`_cubre`): si las trae, la ficha no toma nada de él.
- **H-02, el solicitante.** El punto de guardado rechazaba un solicitante que no es texto como DATOS_INCOHERENTES, y una prueba de T-112 (`test_r02_h06_un_solicitante_no_textual_es_un_rechazo`) pide CANAL_NO_AUTORIZADO. Se conserva la regla de T-112.
- **H-04, más allá de las 14.** MON-EXP-001 e IDX-REB-001 no estaban en la lista del revisor (sus fechas posteriores son futuras por naturaleza), pero tienen fechas observadas que tampoco se comparaban (la de los datos, las decisiones, el anuncio, los activos indexados, los eventos comparables). Se comparan; las futuras, no. Sus casos de control dan el mismo resultado.

### Límites conocidos

- **Fechas sin campo propio.** Lo que un bloque declara sin fecha (por ejemplo, la expectativa de inflación de MON-REAL-001 o el tipo oficial de MON-EXP-001) va con la fecha de los datos: no hay forma de comprobarlo.
- **Series de HT-01.** Las comprueba el servicio con su `fin` (FUGA_DE_INFORMACION); las fichas no las vuelven a mirar.
- **Granularidad de H-01.** `_cubre` mira las claves de la sección del `por_defecto.yaml` actual; una clave que el fichero de entonces tenía y el actual no, y que el valor guardado tampoco traía, no se detecta. No ocurre con una configuración cargada con `cargar_config`, que fusiona el fichero entero.
- **Coste.** Las comprobaciones son lineales en el tamaño de los datos y no cambian el coste de ninguna ficha de forma apreciable.

### Comandos exactos para probarlo

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/pytest -q tests/test_t121_hallazgos.py tests/test_t118_hallazgos.py tests/test_t106_motor.py tests/test_t106_r03.py
cd ../..
.venv/bin/python -I -W ignore .docs/tickets/T-118/revisores/r01_01_h09_fecha_corte.py
.venv/bin/python -I -W ignore .docs/tickets/T-118/revisores/r01_03_h11_ct10_configuracion.py
.venv/bin/python -I -W ignore .docs/tickets/T-118/revisores/r01_04_h12_configuracion.py
.venv/bin/python -I -W ignore .docs/tickets/T-118/revisores/r01_05_h13_h14_fuzz.py          # unos 45 min
.venv/bin/python .docs/tickets/T-118/revisores/r01_07_mutantes.py <copia con «qa2_mut» en la ruta> --solo M05,M38,M50,M68,M78
.venv/bin/python .docs/tickets/T-121/revisores/impl_mutantes.py bloque_a/11_Ejecutor <carpeta desechable>
```
