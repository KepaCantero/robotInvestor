# T-113 · Informe de pruebas

## Ronda r01 (commit `3a5fbfe`)

| Suite | Resultado |
| --- | --- |
| `tests/test_t113_deuda.py` | 57 en verde |
| `tests/test_t102_filtro.py`, `tests/test_t101_v6.py` | En verde. Dos pruebas de T-102 se adaptaron al cambio buscado: el singular de H-49 y el esquema de una a tres frases de H-50 |
| `tests/test_t106_r03.py`, `tests/test_fase1_mon_idx.py`, `tests/test_t106_motor.py` | En verde. La prueba de la incertidumbre usa ahora `incertidumbre_probabilidad_acumulada`, sin tolerancia absoluta (N05) |
| `tests/test_t88_consumo.py`, `tests/test_t65*.py`, `tests/test_t92_revision.py` | En verde |
| Oráculo de la QA r03 de T-106 (`r03_03_mon_exp_oraculo.py`) | 4/4. Ninguna curva con la precisión declarada se rechaza ya por «no se puede reproducir» (H-27). La probabilidad de cada reunión queda dentro de su cota (máximo 0,70 de la cota, H-23) |
| Suite completa y gate | En el commit (`commit_limpio.sh`). La QA r01 midió 3693 pruebas de A en verde |

Cuotas: ruff 2902 (antes 2907); mypy de A 109.

## Ronda r02 (rama local `t113r02`, sobre `3fc54d5`)

Entorno: `.venv` del proyecto (Python 3.12), máquina de 4 núcleos compartida con otros trabajos. Todo con el cliente simulado, sin red.

### Recuentos

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t113_deuda.py` | 57 | 106 (49 nuevas, todas `test_r02_*`), 43 s |
| Suite completa de `bloque_a/11_Ejecutor` | 3825 (3874 menos las 49 nuevas; no medido aparte en esta rama) | **3874 en verde**, 1043 s (17 min 23 s, con otro trabajo en la máquina); línea base 607 |

La suite completa incluye `test_t102_filtro.py`, `test_t101_v6.py`, `test_t88_consumo.py`, `test_t106_*.py`, `test_unitarias.py` y `test_fase3_goldens.py`. Las suites de A-Forex y de B no se han ejecutado: la ronda no toca esos paquetes.

### Criterio de aceptación → prueba

| Criterio | Pruebas |
| --- | --- |
| CA-1 (cada hallazgo, su corrección y una prueba que falla sin ella) | Las de la r01 más las de la tabla «Ronda r02» de `analisis-tecnico.md`. Los ocho mutantes vivos de la r01 mueren (abajo) |
| CA-2 (la V5 no cambia salvo lo declarado) | `r01_10` frente a `3a5fbfe^`: 13 136 hojas, 18 distintas, los mismos grupos que en la r01, todos en la lista de CA-2 (que ahora nombra `consumo.uc` y `uc_llm`). Entre la r01 y la r02 solo cambian los tres `_hash` del RUN |
| CA-3 (gate sin subir cuotas) | ruff 2902 (cuota 2902), mypy de A 109 (cuota 109). El gate completo no se ha lanzado en esta ronda (máquina compartida); sí cuatro de sus puertas sueltas (abajo) |

### Regresiones: cada prueba falla sin su corrección

Con mutantes, uno a uno, cada uno en su copia de `bloque_a/` (carpeta desechable, ya borrada):

- **Los 54 del revisor** (`revisores/r01_11_mutantes.py … todos`, sin modificar): **52 mueren con `tests/test_t113_deuda.py`** (en la r01, 43 y uno más con las vecinas). Sobreviven M41 y M43, los dos que la QA r01 dio por equivalentes. Los ocho vivos de la r01 (M24, M11b, M22, M23, M07, M03, M38 y M44) mueren, y M08 muere ya con la batería propia.
- **21 de las correcciones de la r02** (`r02_mutantes_propios.py`, en esta carpeta): R01 a R07 (H-01), R08 a R12 y R16 (H-02), R13 a R15 (H-06), R17 a R19 (H-03), R20 y R21 (H-07). **21 de 21 mueren.**

### Scripts del revisor, antes y después (sin modificarlos)

«Antes» es `3fc54d5`; «después», esta rama. Desde `bloque_a/11_Ejecutor`, con `QA_TMP` en una carpeta temporal.

| Script | Antes | Después |
| --- | --- | --- |
| `r01_01_sensible_diferencial.py` | 29 fallos: 6 casos dirigidos distintos, 23 de 3 000 al azar con R8 perdido, la lista cíclica no termina | **0 fallos**: 0 distintos, 0 de 3 000, los dos ciclos dan `True`. Tiempos (con la máquina cargada): 400 niveles con 1 MB, 0,32 s; 900 niveles, 0,41 s; lista de 200 000 niveles, 2,8 s; lista de 200 000 diccionarios, 20 s (antes 5 s: ahora se serializan) |
| `r01_02_jsonl_cortes.py` | 3 fallos (H-02 y H-06) | **0 fallos**. La cinta con una última línea «12» sin salto sigue dando su error, como espera el script |
| `r01_03_motor_forma.py` | 7 excepciones (5 de H-04, 2 del proveedor simulado del script) | 7, las mismas: H-04 se corrige en T-118 |
| `r01_04_mon_exp_oraculo.py` | 219 sendas, 0 rechazos, 0 reuniones fuera de cota (0,847 y 0,822) | igual |
| `r01_05_dominios_mon_idx.py` | 0 fallos, 0 avisos | igual |
| `r01_06_filtro_sintetizador.py` | 11 fallos (2 de H-03 y 9 frases que ya eran R21 antes de T-113) | 9: los dos de H-03 desaparecen; quedan los 9 anteriores a T-113 (CLI, CV, CCC, XL, LIC, «S.A.», «A/B», «A o B», «E/S») |
| `r01_07_filtro_diferencial.py` | 4 frases legítimas quitadas frente a `3a5fbfe^` | **0**: la salida es idéntica a la de `3a5fbfe^` |
| `r01_08_frases_camino_real.py` | 0 excepciones; 7 casos sin nada declarado | 0 excepciones; **0 casos sin declarar** |
| `r01_09_hilos_consumo_limitaciones.py todo` | 0 fallos (15 comprobaciones) | igual |
| `r01_10_v5_diferencial.py` | 18 hojas distintas frente a `3a5fbfe^` | 18, los mismos grupos; frente a la r01, solo los 3 `_hash` |
| `r01_11_mutantes.py … todos` | 43 + 1 muertos, 2 equivalentes, 8 vivos (dato de la QA r01) | 52 muertos con la batería propia, 2 equivalentes, 0 vivos |
| `r01_12_casos_control_t112.py` | 57 de 57 superadas; 70 manejadores, 70 servibles | igual; el volcado de los 25 casos de MON e IDX, idéntico byte a byte |
| `r01_13_r8_camino_real.py` | por `AnthropicClient.generar`, 2 de 3 contenidos con el par se enviaban al SDK | **0 de 3 enviados**; por `Agentes.invocar`, bloqueado como antes |

### Puertas del gate ejecutadas

```
ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l   # 2902
mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l                              # 109
python tools/corpus_integridad.py   # 695 archivos coinciden
python tools/refs_vivas.py          # todas las rutas existen
python tools/secrets_scan.py        # sin hallazgos
python tools/nfc_check.py           # nombres en forma canónica
```

`./tools/check_all.sh` completo: **no ejecutado** en esta ronda.

### Sin comprobar

- El gate completo y las suites de A-Forex y B.
- H-04 (se comprueba en T-118).
- Que los tres `_hash` del RUN que cambian entre la r01 y la r02 se deban solo a los tiempos de ejecución: es lo esperable (la QA r01 ya los daba por explicados), pero no se ha aislado.
- La API real y un universo real.
