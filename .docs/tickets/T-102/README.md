# T-102 · Bloque A V6: filtro R13/R21 frase a frase de los textos del Sintetizador (H-23 y H-24 de T-101)

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
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

## Plan de pruebas

| Prueba | Criterio |
| --- | --- |
| `tests/test_t102_filtro.py`: banco de frases legítimas y prohibidas (54 casos) | CA-1, CA-2 |
| `tests/test_t102_filtro.py`: frase a frase, tarjeta mala y lectura del conjunto | CA-3, CA-4 |
| `tests/test_t101_v6.py` y la batería completa | CA-5 |

## Registro

- 2026-11-12 · ABIERTO · a petición del operador («Corrige el filtro»)
- 2026-11-12 · EN QA · filtro frase a frase con reglas nuevas; 58 pruebas nuevas (30 fallan con el filtro de T-101); A 607
