# T-102 · Bloque A V6: filtro R13/R21 frase a frase de los textos del Sintetizador (H-23 y H-24 de T-101)

| Campo | Valor |
| --- | --- |
| Estado | EN QA (ronda r02) |
| Pieza | `bloque_a/11_Ejecutor` (`bloque_a/diseno_v6.py`) |
| Planifica · implementa · QA | claude · claude · claude, con un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-12: «Corrige el filtro» |
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
