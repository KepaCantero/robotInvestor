# T-206 · Análisis técnico

## Causa raíz

`Almacen.incidencia(tipo, …)` escribía en HA el `tipo` que recibía, sin compararlo con el esquema. Ocho llamadas pasaban `"DATOS"`, que no está en el enumerado de 4.8 del esquema de HA V2.0. Las pruebas de esas rutas daban DATOS por bueno: siete ficheros buscaban `tipo == "DATOS"` y uno escribía DATOS directamente.

| Fichero | Línea en develop | Qué declara |
| --- | --- | --- |
| `interfaz_broker.py` | 260 | Revisión C2 sin tipos de activo que revisar (escalada al operador) |
| `interfaz_broker.py` | 416 | Consulta CT-23 con un plazo que no se puede leer |
| `orquestacion.py` | 416 | HT-01: referencia de comparación inválida (el tipo no se analiza) |
| `orquestacion.py` | 502 | HT-01: datos inválidos de un símbolo (se excluye del cribado) |
| `orquestacion.py` | 819 | CT-19 que el Buscador no atiende (no cuadra con F6 o F9) |
| `orquestacion.py` | 1515 | Pronóstico de fuente no registrable |
| `fiabilidad_f9.py` | 86 | F9 sin fichas cargadas |
| `fiabilidad_f9.py` | 95 | FUE- cuya fuente ya no es de F9 (marca `fue_no_atendible`) |

**Otros llamadores.** Se leyó el paquete entero con el AST. Además de esos ocho, los tipos que se usan son CANAL_NO_PREVISTO, HERRAMIENTA, MANIPULACION, OTRO y SEGURIDAD en `incidencia`, y ACCESO_FUERA_DE_MATRIZ y ESCRITURA en `_incidencia_interna`. Todos están en el esquema. Ninguna INC- se escribe por `escribir` directamente.

**Lectores.** Ningún código del ejecutor filtra HA por `tipo == "DATOS"`. Los lectores de INC- son estos:
- `guias.py`, por `leccion_id`;
- `cola_peticiones.py`, por `peticion_huerfana`;
- `mantenimiento_c4.py`, por `reserva_huerfana`;
- `fiabilidad_f9.no_atendibles`, por `fue_no_atendible`;
- `orquestacion.estado`, por `escalado_operador`, que muestra el `tipo`.

Todos van por una marca y no por el tipo. Las antiguas y las nuevas se leen igual. No se encontró ningún lector en `dashboard/`, en `.docs/scripts/` ni en `tools/`.

## Implementación

Archivos cambiados:

- **`bloque_a/11_Ejecutor/bloque_a/almacen.py`**:
  - `TIPOS_INCIDENCIA`: el enumerado de 4.8, con la cita del esquema. Es el único sitio del código que lo fija, y una prueba lo compara con la línea del corpus.
  - `TIPO_INCIDENCIA_DATOS = "OTRO"` y `CATEGORIA_DATOS = "DATOS"`.
  - `TipoIncidenciaNoAdmitido(ValueError)`.
  - `_comprobar_tipo_incidencia`: el tipo tiene que ser texto y estar en la tupla. Lo llaman `incidencia` y `_incidencia_interna` antes de `nuevo_id`, así que un rechazo no gasta el contador ni escribe nada.
  - `incidencia_de_datos(detalle, objeto, severidad, **extra)`: llama a `incidencia("OTRO", …, categoria="DATOS", …)`. Es el único sitio que decide cómo se escribe un problema de datos.
  - `es_incidencia_de_datos(entrada)`: una INC- con `tipo` DATOS, la antigua, o con `categoria` DATOS, la nueva.
- **`interfaz_broker.py`, `orquestacion.py` y `fiabilidad_f9.py`**: en las ocho llamadas, `incidencia("DATOS", ` pasa a `incidencia_de_datos(`. Las dos cadenas tienen veinte caracteres, así que la sangría de las líneas siguientes no cambia, y el resto de argumentos es el mismo. En `fiabilidad_f9.py` también cambian tres docstrings: «incidencia DATOS» pasa a «incidencia de datos». En `orquestacion.py` no se toca nada más. Su comentario de la línea 405 dice «incidencia DATOS» en el sentido de «de datos» y se deja igual, para que el rebase del PR 3 de Astra sea fácil.
- **Pruebas existentes** (`test_t198_buscador_ct19.py`, `test_t125_r02.py`, `test_t65_qa_r01.py`, `test_t65_qa_r02.py`, `test_t65_qa_r03.py`, `test_t65_hallazgos.py`, `test_t103_r8_y_bajos.py` y `test_t116_r05.py`): `tipo == "DATOS"` pasa a `es_incidencia_de_datos(…)`, y la llamada directa con DATOS de `test_t116_r05` pasa a `incidencia_de_datos`. Siguen comprobando lo mismo, ahora con el lector que admite las dos formas. El número de pruebas no cambia.
- **`tests/test_t206_tipo_incidencia.py`** (nuevo): 35 casos.

## Decisiones (INC-T206-01 `[PROPUESTO]`)

- **OTRO en los ocho.** Ninguno es una herramienta caída ni un fallo de una pieza, que es el sentido que tienen HERRAMIENTA en el ejecutor y la «herramienta caída» del §17.5 del Documento 0. Son datos que no valen o que no cuadran. Un único tipo para los ocho hace que el lector sea sencillo y que no haya que decidir caso por caso.
- **`categoria` DATOS.** Es un campo que el esquema no nombra, igual que `detalle`, `run_id`, `fragmento` o `fue_no_atendible`, que el ejecutor ya escribe. Lleva la categoría y no el valor, así que cumple la regla 4 del esquema y R8. `campo_afectado` es otra cosa: el nombre del campo con datos protegidos de un mensaje (CT-25, R8).
- **Con `incidencia_de_datos` en lugar de `incidencia("OTRO", …, categoria="DATOS")` en cada sitio**: así la decisión está en un único sitio y cambia un solo token por línea.

## Límites conocidos

- ~~`Almacen.escribir` no comprueba el tipo de una INC- montada a mano~~: corregido en la ronda de cierre (H-04).
- No hay un esquema JSON de HA en el corpus ni en `06_Plantillas_entregables`. El esquema JSON de las pruebas se construye con los campos de 4.8 que escribe el ejecutor. `id` va en lugar de `inc_id`, como en todas las entradas de HA del ejecutor, que usan `id` como clave (`CLAVES["HA"]`).
- Las INC- antiguas con DATOS siguen en los almacenes existentes, porque HA es append-only. La vista `estado` las muestra con su tipo antiguo.

## Comandos

Desde `bloque_a/11_Ejecutor`:

```bash
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t206_tipo_incidencia.py
../../.venv/bin/python ../../.docs/tickets/T-206/mutantes.py .
```

Desde la raíz de la copia:

```bash
.docs/tickets/T-201/equivalencia.sh . origin/develop
```

## Ronda de cierre de la QA r01 (APTO pendiente de cierre, H-01 a H-06, todos bajos)

Primero se rebasó sobre `6c8910c1` (T-205). Solo chocaron los añadidos al final de `docs/incidencias.md` y de la deuda, y se resolvieron juntando las dos entradas.

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-01 · gate de antes del rebase | Gate completo sobre el commit final, con su log en el scratchpad (`gate_t206_cierre.log`), citado en `pruebas.md`. Evidencias regeneradas | El log 12/12 |
| H-02 · subclase de `str` permisiva | `_comprobar_tipo_incidencia`: `type(tipo) is not str` (el tipo exacto). M4 ya no es equivalente y sale de `EQUIVALENTES` | `test_ca2_un_tipo_fuera_…`, que suma `_Permisivo()` y `_TextoPermisivo("DATOS")`; M4 y M4b muertos; `r01_01` §1 |
| H-03 · `categoria` DATOS con cualquier tipo | `incidencia` (y `escribir`) rechazan `categoria` fuera de la pareja OTRO con DATOS (también con un valor que no es exactamente `str`), antes del id. `es_incidencia_de_datos` exige la pareja o la DATOS antigua | `test_ca2_categoria_solo_en_la_pareja_otro_datos_…` (7 casos, byte a byte), `test_ca4_el_lector_…` con SEGURIDAD/HERRAMIENTA + DATOS; M21 a M26; `r01_01` §2 |
| H-04 · `escribir` admitía una INC- montada a mano | `_comprobar_reserva`, para HA e INC: la misma comprobación (tipo y categoría). `escribir` la rechaza con `EscrituraFueraDeReserva` sin escribir nada; con AG-18 en HA no deja una incidencia recursiva, igual que antes. `test_t198_…::test_r02_h02_…` lleva ahora `tipo` OTRO, y no cambia lo que prueba. Las INC- antiguas de CA-4 se montan con la comprobación desactivada por `monkeypatch` solo mientras se montan | `test_ca2_escribir_rechaza_una_inc_montada_a_mano_…` (7 casos, byte a byte); `test_ca4_un_ha_antiguo_…`, que también comprueba que la comprobación vuelve a estar activa; M27 y M28; `r01_01` §3 |
| H-05 · CA-3 no probaba la conservación | `_conserva(...)` en las ocho `test_ca3_*`: objeto, severidad, tratamiento, `run_id`, `escalado_operador` y `fue_no_atendible`, con los valores de develop (los que el camino no lleva, ausentes) | Los diez mutantes vivos del revisor (Q6, Q14, Q15, Q16, Q18, Q20, Q21, Q22, Q24 y Q25), copiados a `mutantes.py`: muertos con `test_t206` sola |
| H-06 · textos y vista `estado` | README del ejecutor (CT-23): «incidencia de datos en HA (OTRO con `categoria` DATOS; las de antes de T-206, DATOS)». Comentario de `orquestacion.py`: «incidencia de datos». `estado` añade `categoria` a una escalada solo si la INC- la lleva | `test_ca4_el_estado_del_operador_…` (DATOS en la nueva, ninguna en la antigua ni en una HERRAMIENTA); `test_ca4_la_documentacion_ya_no_habla_de_incidencias_datos`; M29 y M30; equivalencia con develop |

Los anclajes de r01_02 (Q1 a Q25) siguen en el código, salvo Q4 y Q5, que tenían que cambiar con H-02. `es_incidencia_de_datos` se escribió de forma que conserva el anclaje de Q11 y Q12.

**Scripts del revisor.** La corrección que pide el `qa.md` choca con tres puntos de sus propios scripts. En esos puntos los adapté lo mínimo, con un comentario «Ronda de cierre (implementador, …)». Las comprobaciones no cambian.
- `r01_01` §2: el rechazo de `incidencia("SEGURIDAD", …, categoria="DATOS")` cuenta como OK si no escribe nada. Antes el script esperaba una entrada sin `categoria`, y el rechazo lo hacía caer. El lector se prueba con la entrada montada a mano.
- `r01_01` §4 y `r01_03`: el HA antiguo se monta con la comprobación desactivada solo durante el montaje, porque `escribir` ya rechaza DATOS (H-04).
- `r01_02`: el anclaje de Q4 y Q5 es la línea nueva de H-02.

El diff exacto frente a los scripts tal como los dejó la QA r01 está en `cierre_adaptacion_revisores.diff`, en esta misma carpeta.
