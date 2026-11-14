# T-113 · QA independiente

- **Revisor:** un revisor nuevo sin el contexto de la implementación (subagente de Claude; la implementación es de Claude) · **Ronda:** r01 · 2026-11-13

## Ronda r01

Orden de lectura: `README.md` del ticket → las filas de origen en los `qa.md` de T-103, T-88, T-106 y T-102 → el código y las pruebas de `3a5fbfe` → solo al final `analisis-tecnico.md` y `pruebas.md`.

### Reproducción desde limpio

Copia propia: un `git worktree` de `ab95d41` (contiene `3a5fbfe`), con el entorno del proyecto (`.venv`, Python 3.12). La máquina tiene 4 núcleos y la compartían otros dos trabajos: los tiempos llevan ese margen.

```
cd bloque_a/11_Ejecutor
python -m pytest -q tests/test_t113_deuda.py     # 57 passed en 16,17 s
python -m pytest -q -p no:cacheprovider          # 3693 passed en 641,80 s (10 min 41 s); la línea base es 607
ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l   # 2902 = cuota
mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l                              # 109 = cuota
python tools/secrets_scan.py                     # sin hallazgos (con mis scripts dentro)
```

**El gate completo (`./tools/check_all.sh`) no lo he lanzado en esta ronda**, por indicación de quien encarga la QA: pasó 12/12 sobre este mismo commit una hora antes (consta en `.docs/tickets/T-112/qa.md`, «Ronda r02») y había otro corriendo en la máquina. De sus doce puertas he repetido yo cuatro (pytest de A, ruff, mypy de A y secretos). Las suites de A-Forex y de B no las he ejecutado: el commit no toca esos paquetes.

### Scripts de esta ronda (`revisores/`)

Todos se ejecutan desde `bloque_a/11_Ejecutor` de la copia, con `python ../../.docs/tickets/T-113/revisores/<script>`. Los que crean carpetas temporales las ponen en `$QA_TMP` si está definida.

| Script | Qué ataca | Resultado |
| --- | --- | --- |
| `r01_01_sensible_diferencial.py` | `contenido_sensible` nuevo frente al de `3a5fbfe^`: 22 casos dirigidos, 3 000 estructuras al azar, tiempos, profundidad y ciclos | 29 fallos: H-01 |
| `r01_02_jsonl_cortes.py` | caché y cinta cortadas en cada byte, líneas ilegibles, vacías, 45 MB, y seguir escribiendo tras un corte | 3 fallos: H-02 y H-06 |
| `r01_03_motor_forma.py` | 57 peticiones del Motor mal formadas | 7 excepciones: 5 son H-04; 2 son de mi proveedor simulado y no cuentan |
| `r01_04_mon_exp_oraculo.py` | H-23 y H-27 con un oráculo propio (sendas conocidas, curva exacta redondeada) | 0 fallos |
| `r01_05_dominios_mon_idx.py` | cada parámetro de `DOMINIOS` dentro, en el borde, fuera y con 21 tipos raros; listas; por el Motor | 174 bien, 0 fallos |
| `r01_06_filtro_sintetizador.py` | tickers en minúscula, romanos, letras sueltas, siglas, mayúscula tras quitar | H-03 y observaciones |
| `r01_07_filtro_diferencial.py` | 53 frases, antes y después de T-113 | 4 frases legítimas que antes pasaban y ahora se quitan: H-03 |
| `r01_08_frases_camino_real.py` | un ciclo V6 con el Sintetizador devolviendo 0, 1, 2, 3 o 4 frases y otras formas | 0 excepciones; H-07 |
| `r01_09_hilos_consumo_limitaciones.py` | `consumo` y `limitaciones` con 1, 6, 12 y 6 hilos, V5 y V6, presupuestos justos | 0 fallos (en `3a5fbfe^`, 5) |
| `r01_10_v5_diferencial.py` | dos ciclos V5 de doce perfiles, antes y después (13 136 hojas) | 18 hojas distintas, todas explicadas |
| `r01_11_mutantes.py` | 54 mutantes, uno a uno | 43 mueren con la batería nueva, 1 con las vecinas, 2 equivalentes, 8 vivos |
| `r01_12_casos_control_t112.py` | casos de control de las 57 fichas, y los de MON e IDX antes y después | 57 de 57 superadas |
| `r01_13_r8_camino_real.py` | alcance real de H-01 | por `Agentes.invocar` se bloquea; por `AnthropicClient.generar`, no |

### Hallazgos de origen, uno a uno

«Ejecutado» quiere decir que la evidencia es una salida mía; «leído», que lo deduzco del código.

| Fila | Hallazgo | Estado | Evidencia |
| --- | --- | --- | --- |
| T-104 | H-54 línea cortada en la caché o en la cinta | **parcial** | Ejecutado (`r01_02`): la caché abre en los 277 puntos de corte de un fichero de cuatro registros y conserva las líneas completas; la cinta abre en todos; una línea ilegible en medio se tolera en la caché y da «fichero: línea N» en la cinta; 45 MB y 200 000 líneas, 0,6 s. **Pero** si después del corte se graba otra respuesta, se pega a la línea cortada: en la cinta, el siguiente arranque vuelve a fallar y esa respuesta se pierde (H-02). Y la caché sigue sin arrancar con un registro cuya `clave` no es texto (H-06) |
| T-104 | H-55 versión de Python | **parcial** | Leído: `pyproject.toml` dice `>=3.12`. El README del ejecutor, que el hallazgo de origen citaba, sigue diciendo «Python ≥ 3.10» (línea 22): H-05 |
| T-104 | H-56 `contenido_sensible` profundidad × tamaño | **corregido en tiempo, con una regresión** | Ejecutado (`r01_01`): 400 niveles con 1 MB, 0,18 s; 900 niveles, 0,20 s; 50 niveles con 16 MB, 3,0 s; lista de 200 000 niveles, 0,3 s. Un diccionario de 5 000 niveles da True (falla cerrado). **Regresión de R8**: H-01 |
| T-107 | H-14 curación de AG-12 sin presupuesto | **corregido** | Ejecutado (`r01_09`): las 11 llamadas de AG-12 de un ciclo V5 de doce perfiles llevan presupuesto (en `3a5fbfe^`, 0 de 11). Con 3,0 UC por tipo las limitaciones por presupuesto pasan de 10 a 21: es el cambio declarado. Ver H-08 |
| T-107 | H-15 `consumo.uc` varía con hilos | **corregido** | Ejecutado (`r01_09`): `consumo` idéntico con 1, 6, 12 y 6 hilos en V5 (3,0 UC, 3,6 UC y por defecto) y en V6 (1,4 UC). En `3a5fbfe^`, tres variantes: 49,3639 y 49,364; 53,8103 y 53,8101; 56,3518 y 56,3517 |
| T-107 | H-16 `limitaciones` en el orden de los hilos | **corregido** (con una prueba que no lo vigila: H-09) | Ejecutado (`r01_09`): `limitaciones` idénticas con 1, 6, 12 y 6 hilos. En `3a5fbfe^`, cuatro variantes con 3,0 UC y dos con 3,6 UC |
| T-108 | H-22 `plan` o campos no serializables | **corregido** para lo que cita el origen | Ejecutado (`r01_03`): `plan` lista, dict, None, 0, NaN, bytes, tupla, conjunto, vacío; `parametros` con claves mezcladas, None, tupla, cíclico y muy hondo; `perfil`, `clase` y `semilla` con claves mezcladas: todos RECHAZADO y una entrada más en RC. Quedan otros campos de la misma familia: H-04 |
| T-108 | H-23 cota de la probabilidad de cada reunión | **corregido** | Ejecutado (`r01_04`, oráculo propio): 219 sendas servidas, 629 reuniones; el error real supera la cota publicada en 0 reuniones, ni en la de la reunión ni en la acumulada; peor error/cota, 0,847 y 0,822 |
| T-108 | H-24 ventanas y plazos sin dominio | **corregido** | Ejecutado (`r01_05`): los 16 parámetros de `DOMINIOS`, dentro (se sirven o dan ErrorFicha, nunca otra excepción, menos de 20 s), fuera y con 21 tipos raros (None, bool, texto, NaN, infinito, complejo, 10⁴⁰⁰…): 174 comprobaciones, 0 fallos. Por el Motor, RECHAZADO con entrada en RC, y el caso de control intacto se sigue sirviendo |
| T-108 | H-25 mutantes N02, N05 y N10 | **corregido** | Ejecutado (`r01_11`): M25 (N02), M26 y M27 (N05) y N10 mueren con `test_t113_deuda.py` |
| T-108 | H-27 falsos rechazos de MON-EXP | **corregido en el código, sin prueba en el paquete** | Ejecutado (`r01_04`): 0 rechazos «no se puede reproducir» en 219 curvas escalonadas exactas redondeadas a 1 pb o 0,1 pb; tres curvas lisas con la precisión declarada se siguen rechazando. **El mutante M24 (cota a 0) sobrevive a toda la batería**: H-09 |
| T-109 | H-34 ticker en minúscula tras «la acción», «el valor» o «el título» | **corregido**, con el límite declarado | Ejecutado (`r01_06`): con tres tickers del universo, se caza tras «la acción», «el valor», «el título», con mayúscula inicial, sin tilde, con dos espacios y con espacio duro. 31 frases legítimas con «acción», «valor» y «título» pasan. Siguen pasando el plural («las acciones acwi»), «la acción de acwi», «el bono», «la cripto», «el token» y la forma «Acwi»: observación O-1 |
| T-109 | Romanos como cantidad | **parcial** | Ejecutado (`r01_06`): «las VII», «los III», «sus IV», «estas XII», «unas XX» son CIFRA; «Basilea III», «Solvencia II», «siglo XXI», «Fase II», «Carlos III» pasan. **Pero la regla quita «Las IIC…» y «Los VIX…»**, siglas de la lista permitida: H-03 |
| T-110 | H-50 una o tres frases de 30 s | **corregido** para una y tres | Ejecutado (`r01_08`, ciclo V6 real): con una o con tres frases el ciclo acaba COMPLETO, G3 APTO, y el paquete declara «Frases llanas del Sintetizador quitadas (FORMATO): 1». Leído: la instrucción dice «exactamente dos». Con cero o cuatro frases sigue pasando lo del origen: H-07 |
| T-110 | H-51 mutantes vivos | **corregido** | Ejecutado (`r01_11`): ver «Mutantes» |
| T-110 | H-49 singular, motivos ajenos y minúscula | **corregido** | Ejecutado (`r01_06`, `r01_08`, `r01_11`): «1 idea en 1 tipo», «De 1 idea … analizada»; las claves «ZETA» y «RV 2027» se quitan y se declaran (FORMATO: 2); «Hay un 70 % de subida; el dólar pesa.» queda en «El dólar pesa.». Tras quitar, «¿el dólar pesa?» y ««el dólar» pesa.» siguen en minúscula, e «iPhone» pasa a «IPhone»: observación O-2. Los motivos de un tipo del paquete con tres opciones se conservan en la redacción interna; el origen pedía quitarlos, el README del ticket no |
| T-110 | H-52 siglas institucionales | **corregido** | Ejecutado (`r01_06`): AIE, INE, EPA, TAE y BID pasan y están en la lista; G7, G10 y G20 ya no están. Ninguna de las cinco es ticker del universo de ejemplo. Aparte, y anterior a T-113: SOFR está dos veces en la lista |
| T-110 | H-53 «N·V·D·A» | **corregido** para los separadores del README | Ejecutado (`r01_06`): «·», «‧», «∙», «•», «.», «-», «/» se cazan. Pasan «N,V,D,A», «N\|V\|D\|A», «N*V*D*A», «N+V+D+A», «N:V:D:A», «N'V'D'A», la raya, «N - V - D - A» y «(N)(V)(D)(A)»: el origen pedía «cualquier signo no alfanumérico» o declararlo como límite; no está declarado (O-3) |

### Mutantes (`r01_11_mutantes.py`)

54 mutantes, uno a uno y sin paralelismo, cada uno en su copia de `bloque_a/`: `python .docs/tickets/T-113/revisores/r01_11_mutantes.py <copia> <carpeta_mutantes> todos`. Primero `tests/test_t113_deuda.py`; si sobrevive, las baterías vecinas (`test_t102_filtro`, `test_t106_r03`, `test_t103_r8_y_bajos`, `test_t93_hallazgos`, `test_t92_revision`, `test_t101_v6`: 516 pruebas). La suite completa no se pasó a cada superviviente (10 minutos cada una).

- **Mueren con `test_t113_deuda.py` (43):** M01, M02, M04 (H-54); M05 (H-55); M06 (H-56); M09 (H-14); M10 (H-15, dos pasadas de dos); M11 (H-16); M12, M13 (H-22); M14 (H-23); M15 a M21 (H-24); M25 a M27 y N10 (H-25); M28, M29 (H-34); M30 (romanos); M31 a M33 (H-50); M34 a M37 y M39 (H-49); M40 (H-52); M42 (H-53); S16, S17, S19, S20, S34, S41, W25 y W37 (H-51, con los mismos textos de la QA de T-102).
- **Muere solo con las vecinas (1):** M08 (las hojas de texto no se miran; lo mata `test_t93_hallazgos`).
- **Equivalentes (2):** M41 (G7, G10 y G20 de vuelta en la lista: CIFRA los quita igual) y M43 (sin «-» ni «/» como separadores: «N-V-D-A» y «N/V/D/A» ya eran R21 en `3a5fbfe^` por otra regla; lo mismo «N.V.D.A»).
- **Sobreviven a todo lo ejecutado (8):**

| Mutante | Qué deshace | Hallazgo |
| --- | --- | --- |
| M24 | H-27: `cota_nodo = 0.0` (vuelve a exigir la precisión sola) | H-09 |
| M11b | H-16: se recorre `presupuesto.cierres` sin ordenar, dejando el texto `sorted(...)` en la fuente | H-09 |
| M22 | H-24: `sesiones_estimacion` de IDX-REB admite 0 y negativos | H-09 |
| M23 | H-24: `ventana_percentil_anios` de IDX-CONC admite 0 y negativos | H-09 |
| M07 | H-56: un diccionario demasiado profundo ya no falla cerrado | H-09 |
| M03 | H-54: la caché no descarta un registro que no es {clave, valor} | H-09 |
| M38 | H-49: la clave ajena quitada no se declara | H-09 |
| M44 | H-50: la instrucción vuelve a ser la ambigua | H-09 |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 cada hallazgo, su corrección y una prueba que falla sin ella | **no** | H-54, H-55 y los romanos están corregidos solo en parte (H-02, H-05, H-03). H-27 no tiene ninguna prueba en el paquete (M24 vive). H-16 tiene una prueba que mira el texto de la fuente, no el comportamiento (M11b vive). De H-24 quedan sin prueba dos de los parámetros que citaba el origen (M22 y M23 viven) |
| CA-2 la V5 no cambia salvo lo declarado | **sí**, con una nota | `r01_10`: dos ciclos V5 seguidos de doce perfiles, antes y después: 13 136 hojas, 18 distintas. Son `presupuesto/<tipo>/consumido` (la curación, H-14, declarada), los `_hash` del RUN, y `consumo.uc` y `uc_llm` del segundo ciclo (10,2447 → 10,2449), con la línea del informe técnico que los copia. Este último cambio es el efecto de H-15 y la lista de CA-2 no lo nombra |
| CA-3 gate 12/12 sin subir cuotas | **no comprobado por mí entero** | Gate no relanzado (ver arriba). Lo que he repetido: 3693 pruebas de A en verde, ruff 2902 (cuota 2902, antes 2907), mypy de A 109 (cuota 109), secretos sin hallazgos |

### Invariantes (punto 4 de la skill)

- **Fallo cerrado y validar antes de mutar:** las peticiones mal formadas se rechazan antes de servir y dejan una sola entrada en RC; tras las 57 de `r01_03` el almacén reabre con sus 50 entradas. Excepciones: H-01 (R8 deja de ver una forma) y H-04 (excepción al llamador, sin escritura).
- **Sin LLM en la ruta determinista ni controles relajados:** el commit no toca F ni G. La curación de AG-12 ahora se puede saltar por presupuesto (H-08); sus alertas solo se registran, la deduplicación, las raíces y R9 siguen siendo del código (leído).
- **Números a mano:** los topes de `DOMINIOS` están en INC-T113-01 `[PROPUESTO]`, salvo el rango ±1000 pb de `escenarios_pb` y el margen `1e-6` de la cota del nodo, que no constan (H-05). «H5 de la configuración» no está en `por_defecto.yaml`: 120 y 2520 están escritos en el código.
- **Secretos:** `tools/secrets_scan.py` sin hallazgos; mis claves falsas van partidas.
- **Documentación:** no está al día (H-05).
- **T-112 intacto:** `r01_12`: 57 fichas con casos de control, 57 superadas; 70 manejadores, 70 servibles. Los resultados de los 25 casos de control de MON e IDX solo cambian en las incertidumbres de MON-EXP (lo declarado).

### Hallazgos nuevos

Todas las órdenes, desde `bloque_a/11_Ejecutor` de la copia, con `R=../../.docs/tickets/T-113/revisores`.

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `python $R/r01_01_sensible_diferencial.py` y `python $R/r01_13_r8_camino_real.py`. A mano: `contenido_sensible([{"api" + "_key": "abcdef"}])` | **Esperado:** el cambio de H-56 solo cambia el coste. **Obtenido:** regresión de R8. Solo se serializa el contenedor de arriba y solo si es un diccionario; un diccionario dentro de una lista, tupla o conjunto ya no se serializa, así que el patrón «"clave": "valor"» de `RE_SECRETO`, un secreto en una clave y un objeto cuyo `str` es un secreto dejan de verse: True antes, False ahora (6 de 22 casos dirigidos; 23 de 3 000 al azar; ningún caso al revés). Los dos puntos de llamada pasan justo esa forma (`[mensaje, contexto, system, texto_u]` y `[system, mensajes]`). Por `Agentes.invocar` se sigue bloqueando, porque el encargo viaja también como texto JSON; por `AnthropicClient.generar` con contenido estructurado, la última puerta antes de la API, se bloqueaba en `3a5fbfe^` y ahora se envía al SDK. Hoy el orquestador solo manda texto, por eso no es crítica. Además, una lista que se contiene a sí misma ya no acaba (antes, `RecursionError`) | Serializar una vez cada diccionario que no cuelgue de otro ya serializado (sigue siendo lineal), o serializar el contenedor de arriba sea del tipo que sea; llevar la cuenta de los `id` vistos. Prueba diferencial con listas, tuplas y conjuntos que contengan diccionarios | abierto |
| H-02 | media | `python $R/r01_02_jsonl_cortes.py` («seguir escribiendo tras una línea cortada») | **Esperado:** tras una escritura cortada se puede seguir grabando. **Obtenido:** `ReplayClient` en modo grabar descarta la línea cortada al leer pero no la quita del fichero; la siguiente respuesta se escribe pegada a ella. Al reabrir: `ValueError: …cinta3.jsonl: línea 2 ilegible`, y esa respuesta (pagada, con la API) se pierde. Es el arranque roto de H-54 un arranque más tarde. En la caché pasa lo mismo sin error: lo guardado justo después del corte no se recupera. `descartadas` no se lee ni se registra en ningún sitio | Al cargar, truncar el fichero al último «\n» si acaba en una línea cortada, o escribir «\n» antes de añadir. Registrar una incidencia con `descartadas`. Prueba: cortar, grabar, reabrir | abierto |
| H-03 | media | `python $R/r01_07_filtro_diferencial.py` en `3a5fbfe^` y en el árbol actual, y `diff`; o `v6.frase_prohibida("Las IIC españolas ganan peso.", perm)` | **Esperado:** no se quitan textos legítimos; IIC y VIX están en `filtro_r21_codigos` y se ofrecen al Sintetizador como siglas que puede usar. **Obtenido:** CIFRA en «Las IIC españolas ganan peso.», «Las IIC y los fondos pesan.», «Sus IIC ganan.» y «Los VIX altos asustan.»; en `3a5fbfe^` pasaban. La expresión de los romanos admite la coincidencia vacía: tras el determinante basta que la palabra sea de letras I, V, X, L, C. IIC casi siempre va con «las» | Exigir un romano no vacío y bien formado (por ejemplo `(?=[IVX]{2,}\b)(?:X{1,3}(?:IX|IV|V?I{0,3})|IX|IV|VI{0,3}|I{2,3})\b`) y excluir lo que esté en `perm["codigos"]`. Añadir «Las IIC…» a las legítimas | abierto |
| H-04 | baja | `QA_TMP=<carpeta> python $R/r01_03_motor_forma.py` | **Esperado:** cualquier petición mal formada, RECHAZADO en RC. **Obtenido:** `horizonte`, `modo` o `prioridad` con claves de tipos mezclados o cíclicos, y unos `valores` muy hondos, lanzan `TypeError`, `ValueError` o `RecursionError` al llamador. No se escribe nada. Solo llegan desde código Python, como el resto de H-22 | Meter esos campos en la comprobación de `clave_hash` de `_error_de_forma`, o envolver la escritura del registro | abierto |
| H-05 | baja | lectura | **Documentación sin poner al día.** `analisis-tecnico.md` de T-113 es la plantilla vacía. El README del ejecutor sigue diciendo «Python ≥ 3.10» (línea 22) y da como límites de R21 el ticker en minúscula tras «la acción» y los romanos como cantidad (línea 126). `pruebas.md` no da cifras de la suite ni del gate. El comentario de `DOMINIOS` cita INC-T112-01 y es INC-T113-01. INC-T113-01 no recoge el rango ±1000 pb de `escenarios_pb` ni el margen `1e-6`. CA-2 no nombra el cambio de `consumo.uc` de H-15 | Rellenar y corregir | abierto |
| H-06 | baja | `python $R/r01_02_jsonl_cortes.py` («líneas raras») | Una línea de la caché con `clave` lista da `TypeError: unhashable type` al arrancar, y una con 100 000 niveles, `RecursionError`. Hace falta un fichero manipulado; un corte no lo produce | Comprobar que `clave` es texto y capturar `RecursionError` en `leer_jsonl` | abierto |
| H-07 | baja | `QA_TMP=<carpeta> python $R/r01_08_frases_camino_real.py` | Con cero o cuatro frases de 30 s, una vacía o un número en la lista, el esquema rechaza la respuesta entera y se entregan los textos por defecto, G3 APTO, **sin ninguna limitación que lo diga**: la segunda mitad del H-50 de origen sigue igual fuera de «una o tres» | Declarar en las limitaciones que la respuesta del Sintetizador no valió | abierto |
| H-08 | baja | `python $R/r01_09_hilos_consumo_limitaciones.py v5` | Con la curación en la bolsa, un presupuesto justo la cierra: con 3,0 UC por tipo, 21 limitaciones por presupuesto en vez de 10, y las piezas quedan sin clasificar ni alertas, con el texto «controles intactos (R16)». Si la curación es alcance o control es una decisión del operador y no está en INC-T113-01 | Añadirlo a INC-T113-01 como `[PROPUESTO]` | abierto |
| H-09 | media | `python .docs/tickets/T-113/revisores/r01_11_mutantes.py <copia> <carpeta> M24,M11b,M22,M23,M07,M03,M38,M44` | **CA-1.** H-27 no tiene ninguna prueba en el paquete (se comprobó con el oráculo de la QA, fuera de la suite). `test_h16_…` comprueba que la fuente contiene el texto `sorted(...)` y ordena una lista suya: no ejercita `sintesis.construir`. De H-24 no hay prueba de `sesiones_estimacion` ni de `ventana_percentil_anios`, que el origen citaba. Sin prueba también: el fallo cerrado de H-56, el registro que no es {clave, valor}, la declaración de la clave ajena y la instrucción «exactamente dos». `test_h15_…` mata su mutante solo si los hilos se cruzan en tres ciclos (lo mató dos veces de dos) | Una prueba por superviviente: el oráculo de H-27 en pequeño; `limitaciones` con cierres desordenados por `construir`; los dos parámetros que faltan | abierto |

Observaciones, sin ID: **O-1** tras el plural («las acciones acwi»), «la acción de acwi», «el bono», «la cripto», «el token» o con inicial mayúscula («Acwi»), el ticker del universo sigue pasando; el origen sugería añadir bono, cripto y token. **O-2** tras quitar, «¿el dólar pesa?» sigue en minúscula e «iPhone» pasa a «IPhone». **O-3** separadores que siguen pasando («,», «|», «*», «+», «:», la raya, «N - V - D - A»), sin declarar como límite. **O-4** `precision_cotizacion` admite el texto "0.0001" (anterior a T-113).

### Sin comprobar

- El gate completo y las suites de A-Forex y B (no relanzados, ver arriba).
- Los supervivientes, contra la suite completa de A: solo contra 573 pruebas (las 57 nuevas y 516 vecinas).
- Python 3.10 y 3.11 de verdad (H-55): solo he leído la declaración.
- El filtro con un universo real: solo con el de ejemplo, donde ningún ticker es una palabra española corriente.
- La API real: todo con el cliente simulado o con un SDK simulado.
- Las frases de 30 s entregadas en `r01_08`: el script miró una clave que no existe; me apoyo en la prueba unitaria y en lo declarado en el paquete.

## Veredicto

**NO APTO.** CA-1 no se cumple (H-09, y tres hallazgos de origen corregidos solo en parte: H-54, H-55 y los romanos) y queda un hallazgo alto abierto (H-01, regresión de R8 introducida por la corrección de H-56). El veredicto no depende de la gravedad que se le dé a H-01: con H-01 en media, CA-1 seguiría sin cumplirse. De los 18 hallazgos de origen, 13 están corregidos, 4 en parte (H-54, H-55, H-56 y romanos) y H-27 está corregido pero sin prueba. Para la r02: H-01, H-02, H-03 y H-09; los bajos, corregidos o a la deuda con su ID.
