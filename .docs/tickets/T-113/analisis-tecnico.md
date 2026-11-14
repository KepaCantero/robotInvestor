# T-113 · Análisis técnico

## Causa raíz o motivo

Las QA de T-103, T-88, T-106 y T-102 dejaron en la deuda dieciocho hallazgos del Bloque A (filas T-104, T-107, T-108, T-109 y T-110). Ninguno bloqueaba el ciclo simulado, pero varios sí el modo sombra con la API: un arranque roto por una línea cortada, un control de R8 con coste cuadrático, llamadas sin presupuesto, cifras que cambiaban con los hilos y peticiones del Motor que lanzaban excepción en lugar de rechazarse.

Causa de cada grupo:

- **T-104 (H-54, H-55, H-56).** La caché y la cinta se leían con `json.loads` línea a línea, sin tolerar una escritura cortada. `pyproject.toml` declaraba una versión de Python en la que el paquete no funciona. `contenido_sensible` volvía a serializar en cada nivel todo lo que tenía debajo.
- **T-107 (H-14, H-15, H-16).** La curación de AG-12 se invocaba sin el objeto `Presupuesto`. La UC total del RUN sumaba cifras ya redondeadas, y cuál se redondeaba dependía de qué hilo escribía antes un prefijo de caché. Las limitaciones por presupuesto salían en el orden en que los hilos cerraban.
- **T-108 (H-22 a H-27).** `_error_de_forma` no comprobaba que `plan` fuese un texto ni que lo que entra en la clave de la caché se pudiera serializar. La incertidumbre de la probabilidad de cada reunión de MON-EXP-001 era la del tipo acumulado, que no la acota. Las ventanas y plazos de MON e IDX no tenían dominio. La reproducción de los nodos exigía la precisión de una cotización, cuando el redondeo deja en cada nodo el residuo de mínimos cuadrados.
- **T-109 y T-110 (filtro y textos del Sintetizador).** Reglas que faltaban (ticker del universo en minúscula tras «la acción», romanos como cantidad, letras sueltas con otros separadores, siglas institucionales), el esquema que rechazaba la respuesta entera con una o tres frases de 30 s, y frases del código sin concordancia.

## Evidencia

- Las filas de origen, con su reproducción: `qa.md` de T-103 (H-54 a H-56), T-88 (H-14 a H-16), T-106 (H-22 a H-27) y T-102 (H-34, H-49 a H-53), en `.docs/tickets/`.
- La QA r01 de este ticket (`qa.md`, «Ronda r01») y sus trece scripts (`revisores/r01_*.py`).
- Pruebas: `bloque_a/11_Ejecutor/tests/test_t113_deuda.py` (57 en la r01; las de la r02 se llaman `test_r02_*`).

## Implementación

- Archivos cambiados y por qué (commit `3a5fbfe`, ronda r01):
  - `bloque_a/herramientas/ht06_indice.py`: `leer_jsonl` y la caché tolerante (H-54).
  - `bloque_a/llm.py`: `contenido_sensible` sin recursión (H-56) y `ReplayClient` con `leer_jsonl` (H-54).
  - `pyproject.toml`: `requires-python = ">=3.12"` (H-55).
  - `bloque_a/orquestacion.py`: la curación de AG-12 recibe el presupuesto (H-14).
  - `bloque_a/consumo.py`: la UC del total, de los tokens sumados (H-15).
  - `bloque_a/sintesis.py`: `cierres` ordenados (H-16).
  - `bloque_a/motor/servicio.py`: `_error_de_forma` rechaza `plan` que no es texto y campos no serializables (H-22).
  - `bloque_a/motor/fichas_mon_idx.py`: `DOMINIOS` y `_dominio` (H-24), cota de cada reunión (H-23), cota del residuo (H-27), `_recomendados` como umbral fijo (H-25).
  - `bloque_a/diseno_v6.py`, `contratos.py`, `redaccion.py`, `config/por_defecto.yaml`: filtro y textos del Sintetizador (H-34, romanos, H-49 a H-53).
- Decisiones tomadas y desviaciones del plan: las de INC-T113-01 en `docs/incidencias.md`, todas `[PROPUESTO]`.
- Límites conocidos: los de INC-T113-01 y el apartado «Límites declarados de R21» del README del ejecutor.
- Comandos exactos para probarlo: los de `pruebas.md`.

## Ronda r02

Corrige los hallazgos H-01 a H-09 de la QA r01 (NO APTO). Rama local `t113r02`, sobre `3fc54d5`.

### Qué se cambió, hallazgo a hallazgo

| Hallazgo | Fichero y función | Cambio | Prueba (en `tests/test_t113_deuda.py`) |
| --- | --- | --- | --- |
| H-01 (alta) | `bloque_a/llm.py`: `contenido_sensible` y la nueva `_diccionarios_de_arriba` | La causa: la r01 serializaba solo el contenedor de arriba y solo si era un diccionario, así que el patrón «"clave": "valor"», un secreto en una clave o un objeto cuyo `str` es un secreto dejaban de verse dentro de una lista, una tupla o un conjunto. Ahora se serializa, una vez, **cada diccionario que no cuelga de otro**, bajando por listas, tuplas y conjuntos sin recursión (sigue siendo lineal: cada diccionario se serializa una vez, dentro del suyo o solo). Las hojas se recorren con una lista de contenedores ya vistos, así que siempre termina. Una estructura que se contiene a sí misma (`ValueError`, del recorrido o de `json.dumps`) o demasiado honda (`RecursionError`) da `True`: falla cerrado. Un diccionario con claves que no son texto sigue siendo `TypeError`, como antes de T-113; si cuelga de una lista, el error se lanza después de mirar lo demás, porque un secreto hallado pesa más | `test_r02_h01_un_diccionario_bajo_una_lista_tupla_o_conjunto_se_sigue_viendo` (9 casos), `test_r02_h01_diferencial_con_la_version_anterior` (3 000 estructuras con semilla, frente a la función de antes de `3a5fbfe` copiada en la prueba), `test_r02_h01_ciclos_y_demasiado_hondo_fallan_cerrado_y_terminan`, `test_r02_h01_lineal_con_listas_de_diccionarios`, `test_r02_h01_la_ultima_puerta_antes_de_la_api_bloquea_el_contenido_estructurado` |
| H-02 (media) | `bloque_a/herramientas/ht06_indice.py`: nueva `acabar_en_salto`, llamada desde `CacheResultados.__init__`; `bloque_a/llm.py`: `ReplayClient.__init__`; `bloque_a/orquestacion.py`: `Bloque.__init__` | Después de leer el fichero sin error, quien va a seguir escribiendo lo deja acabado en «\n»: la línea cortada del final se quita y a una última línea entera sin salto se le pone. La caché, siempre; la cinta, solo en modo `grabar` (al reproducir no se toca el fichero). Si la lectura falla (línea ilegible en medio de la cinta), no se toca nada. El contador `descartadas` de la caché y de la cinta lo lee `Bloque.__init__`, que registra una incidencia `HERRAMIENTA` en HA | `test_r02_h02_tras_un_corte_se_puede_seguir_grabando_en_la_cache`, `…_en_la_cinta`, `test_r02_h02_las_lineas_descartadas_se_declaran_al_arrancar` |
| H-03 (media) | `bloque_a/diseno_v6.py`: `frase_prohibida` | La expresión de los romanos admitía la coincidencia vacía: tras el determinante bastaba una palabra con letras I, V, X, L o C. Ahora la palabra entera tiene que ser un romano bien formado de dos letras o más (hasta XXXIX) y no estar en `perm["codigos"]` | `test_r02_h03_una_sigla_permitida_tras_un_determinante_no_es_una_cifra` (5 frases), `test_r02_h03_los_romanos_como_cantidad_siguen_siendo_cifra` (7), `test_r02_h03_un_romano_que_es_sigla_permitida_no_es_cifra` |
| H-04 (baja) | — | **No se corrige aquí: corregido en T-118** (hallazgo H-13 de la QA de T-112, en `_error_de_forma` de `motor/servicio.py`). Hacerlo dos veces en el mismo sitio daría un conflicto al fusionar. `servicio.py` no se toca en esta ronda | La de T-118. `r01_03` sigue dando aquí las mismas 7 excepciones (5 de H-04 y 2 del proveedor simulado del revisor) |
| H-05 (baja) | `.docs/tickets/T-113/analisis-tecnico.md`, `pruebas.md`; `bloque_a/11_Ejecutor/README.md`; `docs/incidencias.md`; comentario de `DOMINIOS` en `motor/fichas_mon_idx.py` | Este documento, relleno. README del ejecutor: «Python ≥ 3.12» y los límites de R21 puestos al día (los dos que ya no lo son, fuera; las observaciones O-1 y O-3 de la QA, dentro). INC-T113-01: el rango ±1000 pb de `escenarios_pb`, el margen `1e-6` y que 120 y 2520 están escritos en el módulo. El comentario cita INC-T113-01 | — |
| H-06 (baja) | `ht06_indice.py`: `leer_jsonl` y `CacheResultados.__init__`; `llm.py`: `ReplayClient.__init__` | `leer_jsonl` trata `RecursionError` como línea ilegible. La caché descarta, y cuenta, un registro cuya `clave` no es un texto. La cinta da su error de siempre («registro de la grabación sin «clave»») en vez de `TypeError` | `test_r02_h06_la_cache_descarta_un_registro_que_no_vale` (5 casos; mata también M03), `test_r02_h06_la_cinta_rechaza_una_clave_que_no_es_texto` |
| H-07 (baja) | `diseno_v6.py`: `_redaccion_segura` y la constante `_SIN_SINTESIS` | Sin una respuesta válida del Sintetizador (ninguna frase, cuatro, una vacía, un número en la lista…) el paquete lleva la limitación «El Sintetizador no dio una respuesta válida: la integración y los textos llanos son los que el código escribe por defecto». Si una reescritura posterior sí vale, la limitación se retira | `test_r02_h07_sin_respuesta_valida_del_sintetizador_se_declara`, `test_r02_h07_cero_o_cuatro_frases_por_el_ciclo_se_declaran` (ciclo V6) |
| H-08 (baja) | `docs/incidencias.md` (INC-T113-01) | Sin cambio de comportamiento. Decisión `[PROPUESTO]`: la curación de AG-12 es alcance, no control. El texto «alcance reducido, controles intactos (R16)» no se cambia: bajo esa decisión es cierto (la deduplicación por hash, el recuento de raíces y R9 son del código) | — |
| H-09 (media) | `tests/test_t113_deuda.py` | Una prueba por mutante vivo. M24: `test_r02_h27_…` (el oráculo de la QA en pequeño, 120 sendas con semilla). M11b: `test_r02_h16_…` (un ciclo V5 con presupuesto justo y los cierres desordenados a propósito antes de `sintesis.construir`; se mira el paquete). M22 y M23: `test_r02_h24_sesiones_de_estimacion_y_ventana_del_percentil_con_dominio` y `test_r02_h24_los_parametros_de_dominio_en_su_borde_se_admiten`. M07: `test_r02_h01_ciclos_y_demasiado_hondo_…`. M03: `test_r02_h06_…`. M38 y M44: `test_r02_h49_la_clave_ajena_quitada_se_declara_y_h50_la_instruccion_pide_exactamente_dos`. El menor de H-15: `test_r02_h15_la_uc_total_sale_de_los_tokens_sumados`, sin hilos | las citadas |
| CA-2 | `.docs/tickets/T-113/README.md` | La lista de excepciones nombra ahora la cuarta cifra de `consumo.uc` y `uc_llm` (H-15) | — |

### Decisiones y desviaciones

- **`acabar_en_salto` es una función aparte**, no un parámetro de `leer_jsonl`: `leer_jsonl` no escribe nunca, y los textos que mutan los scripts del revisor (`M01` a `M04`) siguen en su sitio.
- **La cinta con una última línea sin salto que es JSON válido pero no un registro («12») sigue dando error.** El script `r01_02` lo espera así (cuenta como fallo que abra). Queda declarado en INC-T113-01.
- **`TypeError` con claves que no son texto**: se conserva el comportamiento anterior a T-113 en vez de dar `True`, para que el diferencial con la versión anterior sea exacto. En los dos casos no se envía nada.
- **H-07 declara cualquier respuesta no válida**, no solo «cero o cuatro frases»: `_redaccion_segura` no sabe por qué no hay respuesta (esquema, R8, presupuesto), y en todos los casos los textos son los del código.
- **Observaciones O-1 a O-4 de la QA**: O-1 y O-3 quedan declaradas como límites (README del ejecutor e INC-T113-01). O-2 (minúscula tras «¿» o tras unas comillas, e «iPhone») y O-4 (`precision_cotizacion` como texto, anterior a T-113) no se tocan.
- **«H5 de la configuración»**: los topes 120 y 2520 coinciden con `horizontes.H5` de `por_defecto.yaml`, pero están escritos en `fichas_mon_idx.py`. Las fichas no reciben la configuración; leerla sería un cambio de interfaz. Queda declarado en INC-T113-01.

### Límites conocidos

- El coste de `contenido_sensible` con una lista de 200 000 diccionarios sueltos sube de 5 s a 12 s en la máquina de pruebas: ahora cada uno se serializa y se mira, que es justo lo que faltaba. Sigue siendo lineal (igual que el mismo contenido dentro de un diccionario).
- H-04 sigue abierto en esta rama hasta que se fusione T-118.
- Un romano mayor que XXXIX como cantidad («las XLII ideas») no se caza.

### Comandos exactos para probarlo

```
cd bloque_a/11_Ejecutor
python -m pytest -q -p no:cacheprovider tests/test_t113_deuda.py
python ../../.docs/tickets/T-113/revisores/r01_01_sensible_diferencial.py      # y el resto de r01_*
python ../../.docs/tickets/T-113/revisores/r01_11_mutantes.py <raíz de la copia> <carpeta> todos   # desde la raíz
```
