# T-122 · Bloque A: hallazgos abiertos de las QA de T-113 (r02) y T-120 (r01)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `contratos.py`, `evaluador.py`, `llm.py`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | no necesaria (corrección; el agente decide por defecto desde el 13-11-2026) |
| Deuda técnica | T-122 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Corregir los hallazgos que dejaron abiertos la QA r02 de T-113 y la QA r01 de T-120 (las dos APTO), antes del modo sombra.

## Qué se corrige

| Origen | Hallazgo | Corrección |
| --- | --- | --- |
| T-120 H-01 (media) | Un IBAN con espacio duro o en formato impreso («ES91 2100 0418 45 0200051332») se admitía y quedaba en F5 y en la caché | `contratos.RE_SECRETO`: `ES` (también en minúsculas), dos cifras de control y 20 cifras con hasta dos separadores seguidos (cualquier espacio Unicode, punto o guion) en cualquier agrupación |
| T-120 H-02 (baja) | `aprendizaje.lecciones_por_encargo` no fallaba cerrado (−1 daba 13 de 14 lecciones; `True`, `2.7` y «4» se aceptaban) | `evaluador.lecciones_por_encargo`: entero de 1 a 10 (12.3 del Documento 0) o `ValueError`, también al crear el Evaluador |
| T-113 H-10 (baja) | Un diccionario al que solo se llega por un conjunto colgado de otro diccionario no se veía en `contenido_sensible` | Si la estructura tiene conjuntos, segunda pasada con los conjuntos volcados como listas; la primera se conserva (un «"api_key": <conjunto>» se sigue detectando) y las claves que no son texto siguen siendo `TypeError` |
| T-113 H-11 (baja) | Límites de la regla de los romanos sin declarar | Declarados en INC-T122-01 |
| T-113 H-12 (baja) | Tres líneas de la r02 sin prueba (mutantes A1b, B7, C1) | Pruebas nuevas |

## Criterios de aceptación (binarios)

1. CA-1: las formas del IBAN de la QA (espacio duro, espacio estrecho, formato impreso, dos espacios, minúsculas) se detectan y se rechazan por CT-04, CT-03 y CT-23 sin dejar el dato en ningún archivo; los textos legítimos de las pruebas de T-120 y T-122 no se marcan.
2. CA-2: un máximo de lecciones que no sea un entero de 1 a 10 falla al crear el Evaluador.
3. CA-3: `r02_06_conjunto_bajo_diccionario.py` da 0 regresiones; `r01_01_sensible_diferencial.py`, 0 fallos.
4. CA-4: los mutantes A1b, B7 y C1 mueren ante las pruebas nuevas.
5. CA-5: goldens de contratos sin cambios; gate 12/12.

## Plan de pruebas

`tests/test_t122_hallazgos.py` (37 pruebas): formas del IBAN y su negativo, CT-04 con espacio duro, máximo de lecciones válido e inválido, diccionarios dentro de conjuntos, cola demasiado anidada (B7), cinta con líneas descartadas (C1), volcado de un conjunto.

## Registro

- 2026-11-14 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-14 · EN QA · claude · corregido; scripts de los revisores: `r01_03_iban_fuera_de_lo_declarado.py` pasa de 6 formas admitidas a 0, `r01_01_iban_banco.py` 0 fallos, `r02_06` 0 regresiones, `r01_01_sensible_diferencial.py` 0 fallos, `r01_13_r8_camino_real.py` nada enviado al SDK
- 2026-11-14 · CERRADO (14-11-2026): QA r01 APTO. Hallazgos abiertos (H-13 y H-14, bajos) en T-127 · revisor nuevo sin contexto (`qa.md`)
- 2026-11-14 · CERRADO · claude · hallazgos bajos de la QA r01 resueltos aparte: H-13 se queda (el 10 es un tope citado del 12.3 del Documento 0, no un parámetro; anotado en INC-T122-01) y H-14 corregido (`max_n` explícito validado de 1 a 10; la prueba de T-120 que pedía 12 pasa a esperar el rechazo)
