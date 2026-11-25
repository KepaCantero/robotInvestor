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

- El gate completo y la suite de B (no relanzados, ver arriba).
- Los supervivientes, contra la suite completa de A: solo contra 573 pruebas (las 57 nuevas y 516 vecinas).
- Python 3.10 y 3.11 de verdad (H-55): solo he leído la declaración.
- El filtro con un universo real: solo con el de ejemplo, donde ningún ticker es una palabra española corriente.
- La API real: todo con el cliente simulado o con un SDK simulado.
- Las frases de 30 s entregadas en `r01_08`: el script miró una clave que no existe; me apoyo en la prueba unitaria y en lo declarado en el paquete.

## Veredicto

**NO APTO.** CA-1 no se cumple (H-09, y tres hallazgos de origen corregidos solo en parte: H-54, H-55 y los romanos) y queda un hallazgo alto abierto (H-01, regresión de R8 introducida por la corrección de H-56). El veredicto no depende de la gravedad que se le dé a H-01: con H-01 en media, CA-1 seguiría sin cumplirse. De los 18 hallazgos de origen, 13 están corregidos, 4 en parte (H-54, H-55, H-56 y romanos) y H-27 está corregido pero sin prueba. Para la r02: H-01, H-02, H-03 y H-09; los bajos, corregidos o a la deuda con su ID.

## Ronda r02

- **Revisor:** un revisor nuevo sin el contexto de la implementación (subagente de Claude). Retoma la sesión de otro revisor que se cortó después de escribir `r02_01` a `r02_05` y antes de escribir aquí; esos scripts se han ejecutado tal cual · 2026-11-14

Orden de lectura: `README.md` y la «Ronda r01» de arriba → el diff de `6b9f916` (`llm.py`, `ht06_indice.py`, `diseno_v6.py`, `orquestacion.py`, `tests/test_t113_deuda.py`) → solo al final `analisis-tecnico.md` y `pruebas.md`. «Ejecutado» quiere decir que la evidencia es una salida mía; «leído», que lo deduzco del código.

### Reproducción desde limpio

Copia propia: un `git worktree` con HEAD separado en `b4601c3` (contiene `6b9f916`, y antes `ebadb7d` de T-118), con `/home/user/robotinvestor/.venv` (Python 3.12). Máquina de 4 núcleos compartida (los mutantes corrían a la vez): los tiempos llevan ese margen.

```
cd bloque_a/11_Ejecutor
python -m pytest -q -p no:cacheprovider tests/test_t113_deuda.py tests/test_t120_r8_y_lecciones.py     # 122 passed en 44,6 s (106 de T-113)
python -m pytest -q -p no:cacheprovider tests/test_t102_filtro.py tests/test_t101_v6.py tests/test_unitarias.py \
       tests/test_t87_contratos.py tests/test_fase3_goldens.py                                         # 464 passed en 251,7 s
cd ../..
python tools/corpus_integridad.py; python tools/refs_vivas.py; python tools/secrets_scan.py; python tools/nfc_check.py   # los cuatro, código 0
ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l         # 2902 = cuota
mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l                                  # 109 = cuota
```

**No lanzados, por indicación de quien encarga la QA:** el gate completo (pasó 12/12 al subir `6b9f916`) y la suite completa de A (pasó en ese gate).

### Scripts de la r01, repetidos sin cambios

Desde `bloque_a/11_Ejecutor` de la copia, con `QA_TMP=<carpeta> python ../../.docs/tickets/T-113/revisores/<script>`.

| Script | r01 | r02 (ejecutado) |
| --- | --- | --- |
| `r01_01_sensible_diferencial.py` | 29 fallos (H-01) | **0 fallos**, 33 s. Dict de 5 000 niveles → True; ciclos → True |
| `r01_02_jsonl_cortes.py` | 3 fallos (H-02, H-06) | **0 fallos**. Clave no texto y 100 000 niveles: la caché abre (descarta 1); la cinta da «registro de la grabación sin «clave»» o «ilegible» |
| `r01_03_motor_forma.py` | 7 excepciones (5 de H-04, 2 del proveedor simulado) | **5**: 3 de H-04 (`horizonte`, `modo` y `prioridad` con claves de tipos mezclados: `TypeError`) y las 2 del proveedor. Los cíclicos y muy hondos ya son RECHAZADO (T-118). Ver H-04 |
| `r01_04_mon_exp_oraculo.py` | 0 fallos | **0 fallos**: 219 sendas, 629 reuniones, peor error/cota 0,847 y 0,822 |
| `r01_05_dominios_mon_idx.py` | 0 fallos | **0 fallos** |
| `r01_06_filtro_sintetizador.py` | H-03 y observaciones (11 «FALLO» del banco) | **9**: desaparecen «Las IIC españolas…» y «Los VIX altos…» (H-03). Los 9 que quedan son idénticos en `6b9f916^` (comparado): «Los CLI…», «Sus CV…», «Las CCC…», «Los XL…», «Las LIC…» (siglas fuera de `filtro_r21_codigos`: R21 por la regla estricta), «S.A.», «A/B», «A o B», «E/S». Son la regla de T-102 r03, no de T-113 |
| `r01_07_filtro_diferencial.py` | 4 legítimas quitadas (H-03) | `3a5fbfe^` frente a ahora: **ninguna diferencia** en las 53 frases. `6b9f916^` frente a ahora: las 4 de H-03 vuelven a pasar |
| `r01_08_frases_camino_real.py` | 0 excepciones; H-07 | **0 excepciones**, 55 s. Cero, cuatro, un número en la lista, sin el campo, `frases_30s` texto y «la primera vacía» declaran ahora «El Sintetizador no dio una respuesta válida…». Ver O-5 |
| `r01_09_hilos_consumo_limitaciones.py todo` | 0 fallos | **0 fallos**, 159 s: `consumo`, `limitaciones` y `cierres_parciales` idénticos con 1, 6, 12 y 6 hilos, en V5 y V6 |
| `r01_10_v5_diferencial.py v5` (`6b9f916^` frente a ahora) | 18 hojas explicadas (frente a `3a5fbfe^`) | 13 136 hojas; **3 distintas**: `/ciclo0/run/_hash`, `/ciclo1/run/_hash` y `/ciclo1/run/_hash_prev`. Ningún dato cambia; los hashes, por la cadena del RUN (leído: la configuración por defecto lleva una clave más de T-120; no lo he aislado) |
| `r01_11_mutantes.py todos` | 43 + 1 muertos, 2 equivalentes, 8 vivos | ver «Mutantes» |
| `r01_12_casos_control_t112.py` | 57 de 57 | **67 de 67** superadas (hoy hay más fichas con casos); 80 manejadores, 80 servibles |
| `r01_13_r8_camino_real.py` | por `AnthropicClient.generar`, no se bloqueaba | **todo bloqueado**: 4 de 4 por `Agentes.invocar` y 3 de 3 por `AnthropicClient.generar` (contenido estructurado incluido), 0 envíos al SDK |

### Scripts de la r02

| Script | Qué ataca | Resultado (ejecutado) |
| --- | --- | --- |
| `r02_01_sensible_diferencial.py` (del revisor anterior) | `contenido_sensible` frente al de `3a5fbfe^`: 49 casos dirigidos (dicts en listas, tuplas y conjuntos, anidados y mezclados; claves int, None, tupla y bytes; bytes; objetos con `str` sensible; compartidas y cíclicas; 3 000 niveles) y 20 000 al azar; tiempos | Al azar: **0 regresiones**, 0 excepciones nuevas, todos acaban; 764 más estrictos (ciclos y claves tupla que antes lanzaban) y 4 «antes `TypeError`, ahora False». Dirigidos: **3 regresiones**, las tres con un diccionario dentro de un conjunto que cuelga de otro diccionario: H-10. Tiempos: 400 niveles con 1 MB, 0,26 s; lista de 200 000 dicts pequeños, 2,6 s (antes 2,2); de 10 campos, 23,1 s (antes 21,8); 200 000 veces el mismo dict, 0,09 s (antes 2,3); 16 MB, 4,9 s (antes 5,4) |
| `r02_02_jsonl_tras_corte.py` (del revisor anterior) | caché cortada en cada byte (413 puntos) y cinta (1 249), abrir para grabar, grabar y reabrir; colas raras (sin salto, espacios, `\r`, CRLF, JSON que no es registro, `null`, UTF-8 partida, ilegible en medio, 100 000 corchetes, vacío); la incidencia | **0 fallos.** Ninguna clave perdida, lo grabado tras el corte se recupera siempre; sin corte el fichero no cambia; al reproducir no se toca. La incidencia HERRAMIENTA se registra. Ver O-6 |
| `r02_03_romanos.py` (del revisor anterior) | banco de 42 frases legítimas (las IIC, los VIX, IG, HY, ETF, SICAV, TIPS, REIT, OPA, PMI, IPO, BTP, CDS; Felipe VI, siglo XXI, Fase II, Basilea III/IV, Solvencia II, MiFID II, Juan Pablo II, Carlos III, Capítulo XI; palabras que empiezan por letras de romano: vías, mixtos, xilófonos, Índices, Ideas, Vicios…) y 16 romanos como cantidad; 42 observaciones | **0 legítimas quitadas, 0 cantidades que pasan.** Siglas permitidas hechas de letras de romano en el universo de ejemplo: DIV, IDX, IIC, VIX, XLI, XLV. Observaciones: H-11 |
| `r02_04_mutantes.py todos` (del revisor anterior) | 35 mutantes de las correcciones de la r02 (A, B, C, D, E) y de T-120 (F, G) | ver «Mutantes» |
| `r02_05_r8_camino_real.py` (del revisor anterior) | `AnthropicClient.generar` con SDK simulado (system y mensajes) y `Agentes.invocar` (mensaje y contexto) con 11 formas sucias y 3 limpias, y el estado de H-04 | **0 fallos de R8**: nada sucio llega al SDK ni al cliente; lo limpio llega. Un ciclo en `Agentes.invocar` sale como `ValueError: Circular reference detected` antes de llamar al cliente (cerrado, aunque como excepción y no como PARCIAL). H-04: 4 de 9 peticiones siguen lanzando `TypeError` |
| `r02_06_conjunto_bajo_diccionario.py` (mío) | caso mínimo de H-10 y una variante de la corrección sugerida, dentro del propio script | 4 de 4 regresiones con la función actual; con la variante, 0 |

### Mutantes

Ejecutados uno a uno, sin paralelismo, cada uno en su copia desechable (`.../scratchpad/qa4_mut/`, borrada al acabar): `python .docs/tickets/T-113/revisores/r01_11_mutantes.py <copia> <carpeta> todos` y lo mismo con `r02_04_mutantes.py`. Primero las pruebas del ticket; si sobrevive, las vecinas de cada script (`r01_11`: 516 pruebas; `r02_04`: 471 para T-113 y 97 para T-120).

- **`r01_11` (los 54 de la r01):** **51 muertos por `test_t113_deuda.py`**, entre ellos los ocho que sobrevivían en la r01 (M03, M07, M11b, M22, M23, M24, M38, M44: el mutante de H-09 ya no vive ninguno). **M41 y M43** sobreviven al ticket y a las vecinas: son los dos equivalentes de la r01. **N10: no aplica** (el `except` de los datos de `servicio.py` ya no es único tras T-118; en la r01 moría). 
- **`r02_04` (35 de la r02 y de T-120):** **30 muertos por las pruebas del ticket.** Sobreviven al ticket y a las vecinas cinco: **D6** (la anticipación vuelve a admitir L y C: equivalente, el grupo sigue exigiendo un romano de I, V y X), **F6** (separador también tras «ES»: más estricto, no deshace nada; es de T-120), y tres que **no son equivalentes** y deshacen una parte de las correcciones de la r02 sin que ninguna prueba lo note: **A1b** (no se baja por los conjuntos), **B7** (`acabar_en_salto` vuelve a lanzar `RecursionError` con una cola demasiado anidada: el arranque se rompe) y **C1** (lo descartado de la cinta no se declara; lo de la caché sí lo vigila una prueba). Ver H-12.

### Hallazgos de la r01, uno a uno

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 (alta) | **corregido** en lo que describía (dicts bajo listas, tuplas y conjuntos; ciclos; la última puerta antes de la API), **con una regresión residual baja** (H-10) | Ejecutado: `r01_01` 0 fallos (antes 29); `r01_13` todo bloqueado; `r02_01` 0 regresiones en 20 000 al azar y 3 en 49 dirigidos, todas de la forma de H-10; `r02_05` 0 fallos por el camino real. Termina siempre (ciclos de lista y de dict → True). Coste: igual que antes de T-113 en lo ancho, y lineal en lo hondo |
| H-02 (media) | **corregido** | Ejecutado: `r01_02` 0 fallos; `r02_02` 413 cortes de la caché y 1 249 de la cinta, ninguna entrada válida perdida, lo grabado después siempre se recupera, sin corte ni un byte cambia, al reproducir no se toca; la incidencia se registra. O-6 |
| H-03 (media) | **corregido** | Ejecutado: `r01_07` y `r01_06` (las 4 legítimas de la r01 pasan), `r02_03` 0 de 42 legítimas quitadas y 16 de 16 cantidades cazadas. Límites no declarados: H-11 |
| H-04 (baja) | **no corregido del todo**; el resto está en la deuda (T-121, H-02 de la QA de T-118) | Ejecutado: `r01_03` y `r02_05`: los cíclicos y muy hondos ya se rechazan con entrada en RC, pero `horizonte`, `modo` y `prioridad` con claves de tipos mezclados (`{1: 2, "x": 3}`) y `horizonte` con clave tupla siguen lanzando `TypeError` al llamador (4 casos). `analisis-tecnico.md` dice «corregido en T-118»: no es exacto. T-118 lo dejó abierto como su H-02 (b), apuntado en T-121. Sigue siendo bajo: solo llega desde código Python |
| H-05 (baja) | **corregido** | Leído: README del ejecutor «Python ≥ 3.12» y límites de R21 al día; `analisis-tecnico.md` relleno; el comentario de `DOMINIOS` cita INC-T113-01; INC-T113-01 recoge ±1000 pb, el margen `1e-6` y la curación; CA-2 nombra `consumo.uc`. Salvo la frase sobre H-04 (arriba) |
| H-06 (baja) | **corregido** | Ejecutado: `r01_02` (clave lista, nula, no texto; 100 000 niveles): la caché abre y descarta; la cinta da su error con fichero; `r02_02` «cola de 100 000 corchetes» |
| H-07 (baja) | **corregido** | Ejecutado: `r01_08`: cero, cuatro, un número, sin el campo, texto en vez de lista, la primera vacía → la limitación nueva; una respuesta posterior válida la retira (leído y mutante E2). O-5 |
| H-08 (baja) | **resuelto como decisión `[PROPUESTO]`** | Leído: INC-T113-01, «Curación de AG-12 con presupuesto»: alcance, no control, con sus consecuencias |
| H-09 (media) | **corregido** | Ejecutado (`r01_11`): los ocho supervivientes de la r01 (M03, M07, M11b, M22, M23, M24, M38 y M44) mueren con `test_t113_deuda.py`; M10 (H-15) también |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 cada hallazgo, su corrección y una prueba que falla sin ella | **sí** | Cada fila de la tabla tiene su corrección y al menos un mutante suyo que mata `test_t113_deuda.py`: 51 de 54 de la r01 (los 3 restantes, 2 equivalentes y N10 que ya no aplica) y 30 de 35 de la r02. Las tres partes de la r02 sin prueba (A1b, B7, C1) son líneas secundarias de H-01, H-06 y H-02, cuyas correcciones principales sí tienen la suya: H-12, baja |
| CA-2 la V5 no cambia salvo lo declarado | **sí** | `r01_10` `6b9f916^` frente a ahora: solo los tres hashes del RUN; `r01_09`: consumo y limitaciones estables con hilos |
| CA-3 gate 12/12 sin subir cuotas | **sí, por partes** | ruff 2902, mypy de A 109, los cuatro gates ligeros en verde, las baterías del ticket y las vecinas en verde (586 pruebas). Gate completo: consta 12/12 al subir el commit; no relanzado |

### Hallazgos nuevos

Órdenes desde `bloque_a/11_Ejecutor` de la copia, con `R=../../.docs/tickets/T-113/revisores`.

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-10 | baja | `python $R/r02_06_conjunto_bajo_diccionario.py`; o `python $R/r02_01_sensible_diferencial.py` (las tres «REGRESIÓN» de los dirigidos y los cuatro «OTRO» del azar) | **Esperado:** ningún caso en que antes de T-113 diera True y ahora False. **Obtenido:** un diccionario que solo se alcanza a través de un conjunto o frozenset que cuelga de otro diccionario (`{"a": {DH({"api_key": "…"})}}`, con `DH` una subclase de `dict` con `__hash__`) da False; antes, True. `json.dumps(default=str)` del diccionario de arriba convierte el conjunto con `str` (comillas simples) y `_diccionarios_de_arriba` no baja por los diccionarios. Igual con una clave tupla dentro: antes `TypeError`, ahora False. Baja: un `dict` normal no cabe en un conjunto, y ningún camino del paquete produce esa forma; las hojas de texto (IBAN, AKIA, Bearer) se siguen viendo | `default` que convierta `set`/`frozenset` en lista (en `r02_06`, con eso las 4 dan lo de antes), o bajar también por los conjuntos que cuelgan de un diccionario. Un caso en la prueba diferencial | abierto |
| H-11 | baja | `QA_TMP=<carpeta> python $R/r02_03_romanos.py` (las observaciones «O») | **Esperado:** lo que la regla no caza, o caza de más, está declarado (el README del ejecutor declara solo «sin determinante delante o mayor que XXXIX»). **Obtenido:** pasan sin declarar «Las V ideas pasan.» y «Los X valores mejores.» (romano de una letra tras determinante, dentro de XXXIX), «Las vii ideas» (minúscula), «Mis/Nuestras/Otras/Dichas/Ambas VII ideas» (determinantes fuera de la lista) y «LAS VII IDEAS» (sale por R21). Y quita, sin declararlo, nombres con ordinal romano tras artículo: «Las II Jornadas de inversión ayudan.», «Los XXV Juegos Olímpicos…», «Los III Premios del sector.», «Los VI Presupuestos.», «Los XXI retos del siglo.» | Declarar en el README los dos lados (una letra, minúsculas, otros determinantes; y los nombres con ordinal tras artículo), o ampliar la regla a V y X sueltas tras determinante | abierto |
| H-12 | baja | `python .docs/tickets/T-113/revisores/r02_04_mutantes.py <copia> <carpeta> A1b,B7,C1` (desde la raíz de la copia) | **Esperado:** cada línea de la r02 tiene una prueba que falla sin ella. **Obtenido:** tres mutantes no equivalentes sobreviven a `test_t113_deuda.py` y a 471 pruebas vecinas: A1b (`_diccionarios_de_arriba` no baja por `set`/`frozenset`; el caso `[frozenset]` de la prueba no lleva un diccionario dentro), B7 (`acabar_en_salto` sin capturar `RecursionError`: una cola cortada de 100 000 corchetes rompe el arranque; `r02_02` lo ve con el código actual, ninguna prueba del paquete) y C1 (la incidencia de la cinta no se registra) | Tres casos: un `DH` dentro de un `frozenset`; `acabar_en_salto` con la cola anidada; un `ReplayClient` cortado y la incidencia «grabación del cliente» en HA | abierto |

Observaciones, sin ID: **O-5** «dos frases, la segunda en blanco» (`"   "`) pasa el esquema, se sustituye por el texto por defecto y no se declara nada (con `""` sí se declara, porque el esquema rechaza la respuesta). **O-6** una línea ilegible en medio de la caché no se quita del fichero (solo la del final), así que la incidencia HERRAMIENTA se repite en cada arranque (`r02_02`: 2 y 3 tras dos arranques más); y una cinta cortada del cliente del Contradictor no registra incidencia (solo se mira el cliente principal). **O-7** un ciclo en `Agentes.invocar` sale como excepción (`ValueError` de `json.dumps`) y no como PARCIAL con «bloqueado por R8»; no llega al cliente.

### Sin comprobar

- El gate completo y la suite completa de A (no lanzados, por indicación).
- Los supervivientes de los mutantes contra la suite completa (solo contra el ticket y las vecinas de cada script).
- La causa exacta de los tres hashes distintos de `r01_10` (deducida, no aislada).
- La API real: todo con cliente o SDK simulados.

### Veredicto

**APTO.** Los nueve hallazgos de la r01: H-01, H-02, H-03, H-05, H-06, H-07 y H-09 corregidos (ejecutado), H-08 resuelto como decisión `[PROPUESTO]` en INC-T113-01, y H-04 (bajo) corregido solo en parte, con el resto ya en la deuda (T-121, H-02 de la QA de T-118). CA-1 y CA-2 se cumplen; CA-3, por partes (ruff 2902, mypy 109, gates ligeros y 586 pruebas del ticket y vecinas en verde; el gate completo consta 12/12 al subir el commit y no lo he relanzado). No queda ningún hallazgo crítico ni alto: los nuevos (H-10, H-11 y H-12) y H-04 son bajos y pasan a la deuda técnica con su ID. Ojo con H-10: es una regresión de R8, aunque solo con una forma que hoy nada produce (un diccionario con `__hash__` dentro de un conjunto); conviene cerrarla con la primera ocasión que se toque `llm.py`.
