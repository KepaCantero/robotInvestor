# T-102 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t102_filtro.py` | — | 58 (28 legítimas, 26 prohibidas, 4 de comportamiento) |
| `tests/test_t101_v6.py` | 73 | 73 (una aserción adaptada al texto nuevo de la limitación) |
| A | 549 | 607 |

Con el filtro de T-101 (commit `9b4741a`), 30 de las 58 pruebas fallan. Las 28 que ya pasaban son frases legítimas que aquel filtro tampoco quitaba.

Cuotas: ruff 2986 y mypy de A 109, sin cambios.

## Gate

`./tools/check_all.sh` completo con `commit_limpio.sh` en el commit.

## Ronda r02

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t102_filtro.py` | 58 | 142 (84 nuevas: 18 R13, 22 R21, 33 legítimas, 7 de división, 4 de comportamiento) |
| `tests/test_t101_v6.py` | 73 | 73 |
| `revisores/r01_banco_frases.py` | FP 15/107, FN 6/58 (R13 10/20 en la r01 antes de su corrección de la tabla) | FP 0/107, FN 0/58 |
| Banco de control (no usado para ajustar) | — | FP 0/25, FN 1/24 → 0/24 tras corregir el fallo que encontró (IGNORECASE en la cadena de excepción) |
| `revisores/r01_ataques_t102.py` | — | 14 OK, 1 OBS (saltos y «…», ahora bien separados), 1 FALLO que no lo es: `division_deja_fragmentos` da por prohibida «Comprar bonos de EE.UU. a dos años», que con la r02 es legítima (un segmento), así que el texto sale entero |

Mutantes (`r02_mutantes.py`, 44, contra `tests/test_t102_filtro.py`): 40 muertos en la primera pasada; los 4 vivos (sin `_UNITARIA`, sin el ISIN sin verbo, un texto limpio que pierde sus separadores y sin el corte en «si») señalaban huecos de las pruebas. Con un caso nuevo para cada uno, mueren los 44.

## Ronda r03 (rediseño)

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t102_filtro.py` | 142 (bancos y verbos del filtro de patrones) | 68 (24 legítimas, 32 prohibidas con su regla, 12 de comportamiento y del camino real) |
| `tests/test_t101_v6.py` | 73 | 73 (bancos de la r03 de T-101 adaptados: las legítimas sin cifras ni tickers y R13 → CIFRA; preguntas de prueba sin números) |

`r02_mutantes.py` ya no aplica: las expresiones que mutaba (verbos, cortes, excepciones de R13) han desaparecido.

## Ronda r04

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t102_filtro.py` | 68 | 111 |
| `tests/test_t101_v6.py` | 73 | 73 |
| `revisores/r03_01_ataques.py` | R13 25/26 y R21 30/30 pasan; rendimiento 9,6 s | R13 0/26 y R21 4/30 pasan (los límites declarados); rendimiento 0,48 s |
| `revisores/r03_02_banco_prompt.py` | legítimas quitadas 1/128; prohibidas que pasan 26/45 | legítimas quitadas 1/128; prohibidas que pasan 2/45 (y 2/3 límites) |

Cuotas: ruff 2908 y mypy de A 109, sin cambios. A en total y el gate: los da el commit (`commit_limpio.sh`).

## Ronda r05

| Suite | r04 | r05 |
| --- | --- | --- |
| `test_t102_filtro.py` | 111 | 182 (H-31 a H-33, H-35 a H-39 y una frase por mutante vivo) |
| `test_t101_v6.py` | 73 | 73 |

Scripts de la QA r04 en el árbol de la r05:
- `r04_10_banco_control.py . --detalle`: legítimas quitadas 0/55; prohibidas que pasan 3/44, las tres de H-34 (límite declarado, T-109). De las exóticas, pasan 0/5; de las 9 de control, se quitan las 9;
- `r04_11_camino_real.py .`: `fugas`, llegan 3/3 (las de H-34); `listas`, llegan 0/6; `cli`, sin fallos y sin frases quitadas del simulado;
- `r04_12_rendimiento.py .`: 0,97 s en total y ningún caso no lineal;
- `r04_13_mutantes.py <copia> 3 todos`: mueren 31 de 45; sobrevive N45, que la QA r04 ya dio por equivalente (H-38); no aplican 13, cuyas reglas la r05 quitó porque otras más generales las cubren;
- `r03_03_mutantes.py <copia> 3 todos`: mueren 16 y no sobrevive ninguno; 22 no aplican.

Cuotas: ruff 2908 y mypy de A 109, sin cambios.

## Ronda r06

| Suite | r05 | r06 |
| --- | --- | --- |
| `test_t102_filtro.py` | 182 | 260 (H-40 a H-46, una frase por mutante vivo y CA-15; los marcadores de cuenta pasan de legítimos a prohibidos) |
| `test_t101_v6.py` | 73 | 73 |

Scripts de la QA r05 en el árbol de la r06:
- `r05_01_banco.py .`: prohibidas que pasan, 0 de 40 (antes 38). Legítimas quitadas, 7 de 68: las 7 llevan marcadores de cuenta, que desde la r06 se quitan por diseño (CA-15). Coste aparte: 15 de 18 legítimas con un número en letra;
- `r05_02_camino_real.py .`: `listas` llegan 0/4; las 7 legítimas con marcadores de cuenta no llegan y se declaran; `cli` sale con código 0 y tres ficheros;
- `r05_03_rendimiento.py .`: 0,56 s en total, ningún caso no lineal;
- mutantes, sobre una copia completa:
  - `r05_04`: mueren 22 de 48; sobrevive R27, que la QA r05 ya dio por equivalente; no aplican 25, cuyas expresiones cambiaron;
  - `r04_13`: mueren 23 de 45; sobrevive N45, equivalente;
  - `r03_03`: mueren 13 y no sobrevive ninguno.

Cuotas: ruff 2908 y mypy de A 109, sin cambios. Gate (`commit_limpio.sh`, commit `5e9780d`): 12/12, A con 1481 pruebas, A-Forex 68 y B 176. El banco ciego de CA-12 y CA-13 lo escribió el revisor de la QA r06 (`r06_01_banco_ciego.py`).
