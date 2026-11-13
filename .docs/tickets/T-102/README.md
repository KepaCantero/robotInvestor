# T-102 · Bloque A V6: filtro R13/R21 frase a frase de los textos del Sintetizador (H-23 y H-24 de T-101)

| Campo | Valor |
| --- | --- |
| Estado | EN PAUSA (QA r04 detenida; espera la orden del operador) |
| Pieza | `bloque_a/11_Ejecutor` (`bloque_a/diseno_v6.py`) |
| Planifica · implementa · QA | claude · claude · claude, con un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-12: «Corrige el filtro»; tras la QA r02, «sí cambia el diseño» (opción 1: el Sintetizador escribe con marcadores que rellena el código) |
| Deuda técnica | T-102; recoge H-23 y H-24 de la QA r03 de T-101 (fila T-101) |

## Objetivo

Que el filtro R13/R21 de los textos del Sintetizador (diseño V6) no estropee informes normales y cace las compras evidentes. Lo pidió la QA r03 de T-101:
- **H-23:** tiraba 15 de 19 frases normales, y una sola tarjeta afectada hacía caer todos los textos llanos;
- **H-24:** dejaba pasar compras con artículo o con un sustantivo entre medias.

## Alcance

- **Entra:**
  - **Frase a frase:** se quita solo la frase que incumple. Un texto que se queda vacío toma el texto por defecto de ese mismo elemento (tarjeta, frase de 30 segundos o historial), no de todos.
  - **Reglas nuevas:**
    - R13: un porcentaje «de probabilidad, posibilidad, confianza u opciones de», o «probabilidad» unida a una cifra por un enlace («es de», «del», «:»…), pero no «la probabilidad de un recorte hasta el 4,25 %»;
    - R21: tras un verbo de compra o venta, de inversión o de toma de posiciones, cualquier código que sea un instrumento en lo que queda de la frase;
    - no son instrumentos los códigos de la configuración, los pares de divisas sin barra ni las series del universo que no son tickers de fondo;
    - el ISIN solo cuenta fuera de esas series.
  - **Lista `filtro_r21_codigos` ampliada** con siglas de índices, materias primas y bancos centrales.
- **No entra:**
  - el filtro en la V5 ni en HT-09 (queda en la deuda);
  - los nombres propios sin código ni sufijo («entrar en Tesla»), que son un límite declarado.

## Criterios de aceptación (binarios)

1. CA-1: ninguna de las 28 frases legítimas del banco de las QA r02 y r03 de T-101 se quita.
2. CA-2: las 26 frases prohibidas del banco se cazan con su regla, salvo el límite declarado.
3. CA-3: en un texto con una frase prohibida, se conservan las demás frases. Una tarjeta afectada no cambia las otras tarjetas ni las frases de 30 segundos.
4. CA-4: lo quitado se declara en las limitaciones del paquete, y la segunda pasada de HT-09 no bloquea.
5. CA-5: la V5 no cambia, A pasa a 607 pruebas, las cuotas no suben y el gate da 12/12.

### Ronda r02 (QA r01 NO APTO)

6. CA-6 (H-01): las 20 probabilidades numéricas del banco del revisor y las 18 de `R13_R02` se quitan con R13.
7. CA-7 (H-02, H-03): las 38 compras del banco del revisor y las 22 de `R21_R02` se cazan con R21; las 107 frases legítimas del banco del revisor y las 33 de `LEGITIMAS_R02` se conservan.
8. CA-8 (H-04, H-05, H-06): las abreviaturas no parten frases, «…» y el salto de línea sí, un texto limpio sale igual; el glosario quitado se declara y la reescritura no duplica la limitación.
9. CA-9 (H-07): los textos degenerados del revisor se filtran en menos de 2 s en total.
10. CA-10 (H-10): una prueba por el camino real pone una frase prohibida y una legítima en cada texto del Sintetizador; los mutantes de `r02_mutantes.py` mueren.

### Ronda r03 (rediseño con marcadores; sustituye a CA-1, CA-2, CA-6 y CA-7)

11. CA-11: los marcadores se rellenan con datos del paquete después de filtrar; uno desconocido, mal formado o una llave suelta quita la frase.
12. CA-12: ninguna frase con una cifra (también en letra) ni con un código de un instrumento llega al paquete ni a los entregables, en ninguno de los textos del Sintetizador. Incluye las frases de las QA r01 y r02 que pasaban: listas, «recomendamos el ETF X», «la opción preferida es X» y probabilidades en letra.
13. CA-13: las frases escritas como pide el prompt (sin cifras, con siglas de la lista y con marcadores) se conservan.
14. CA-14: CA-3, CA-4, CA-8 y CA-9 siguen cumpliéndose (frase a frase, defectos por elemento, declaración, división y tiempo lineal).

## Plan de pruebas

| Prueba | Criterio |
| --- | --- |
| `tests/test_t102_filtro.py`: banco de frases legítimas y prohibidas (54 casos) | CA-1, CA-2 |
| `tests/test_t102_filtro.py`: frase a frase, tarjeta mala y lectura del conjunto | CA-3, CA-4 |
| `tests/test_t101_v6.py` y la batería completa | CA-5 |

## Registro

- 2026-11-12 · ABIERTO · a petición del operador («Corrige el filtro»)
- 2026-11-12 · EN QA · filtro frase a frase con reglas nuevas; 58 pruebas nuevas (30 fallan con el filtro de T-101); A 607
- 2026-11-12 · NO APTO · QA r01 (revisor nuevo sin contexto): H-01 alto (R13 deja pasar 10 de 20 probabilidades numéricas), H-02, H-03 y H-10 medios, H-04 a H-09 bajos
- 2026-11-12 · EN QA · Ronda r02: R13 amplio que falla cerrado, R21 en toda la frase tras el verbo, división con abreviaturas; H-01 a H-10 corregidos (H-09, el token de CRI, a T-57 como `[PROPUESTO]`); 84 pruebas nuevas (142 en `test_t102_filtro.py`); 44 de 44 mutantes de `r02_mutantes.py` muertos
- 2026-11-12 · NO APTO · QA r02 (revisor nuevo, banco nuevo de 275 frases): FP 19/187 (10 %), FN 14/88 (16 %; R13 11 %, R21 19 %), frente a FN 30/88 de la r01. H-11 y H-12 altos (compras y probabilidades en lista con saltos de línea; formas de recomendar sin verbo de compra), H-13 a H-15 y H-19 medios, H-16 a H-18 bajos. Sin más rondas hasta que decida el operador (tercera ronda sin converger)
- 2026-11-12 · EN CURSO · el operador elige cambiar el diseño (ronda r03): marcadores que rellena el código y una regla estricta sobre el texto libre
- 2026-11-12 · EN QA · Ronda r03: marcadores y regla estricta (CIFRA, R21, MARCADOR); prompt del Sintetizador §4; `tests/test_t102_filtro.py` reescrito (68 pruebas)
- 2026-11-12 · NO APTO · QA r03 (revisor nuevo): H-20 y H-21 altos (probabilidades en letra o con números Unicode; sufijo con punto e índice que tapaba el ticker), H-22, H-23, H-24, H-25 y H-29 medios, H-26 a H-28 y H-30 bajos
- 2026-11-12 · EN QA · Ronda r04: cobertura de la regla (Unicode, NFKC, números en letra, marcadores compuestos, sufijos, homoglifos, vehículos) y los bajos; 43 pruebas nuevas (111 en `test_t102_filtro.py`); límites de R21 declarados
- 2026-11-13 · EN PAUSA · QA r04 detenida a mitad por indicación del operador (trabajo de una en una: antes T-88, T-91 y T-106). Sus scripts parciales `revisores/r04_01` a `r04_06` quedan en el repo, sin veredicto; la QA r04 se relanza entera cuando el operador lo ordene
