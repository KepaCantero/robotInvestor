# T-113 · Bloque A: deuda técnica T-104, T-107, T-108, T-109 y T-110

| Campo | Valor |
| --- | --- |
| Estado | EN QA (ronda r01, pendiente de lanzar) |
| Pieza | `bloque_a/11_Ejecutor` |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-13: «Corrige toda la deuda técnica» (la del Bloque A: T-104, T-107, T-108, T-109 y T-110; T-105 es de A-Forex y B) |
| Deuda técnica | T-104, T-107, T-108, T-109 y T-110 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los hallazgos que quedaron en la deuda tras las QA de T-103, T-88, T-106 y T-102, antes del modo sombra con la API.

## Qué se corrige

| Fila | Hallazgo | Corrección |
| --- | --- | --- |
| T-104 | H-54 una línea cortada en `cache_resultados.jsonl` o en la cinta impide arrancar | `leer_jsonl` (`herramientas/ht06_indice.py`): la última línea cortada se descarta. La caché descarta también cualquier otra ilegible y las cuenta; la cinta da el fichero y la línea |
| T-104 | H-55 versión de Python | `requires-python = ">=3.12"` |
| T-104 | H-56 `contenido_sensible` cuesta profundidad × tamaño | Se serializa una vez el contenedor de arriba y se recorren las hojas sin recursión; 400 niveles con 1 MB, en 0,2 s (antes 60 s). Si es demasiado profundo para serializarlo, falla cerrado |
| T-107 | H-14 la curación de AG-12 va sin presupuesto | Se carga a la bolsa de su tipo |
| T-107 | H-15 `consumo.uc` varía en la cuarta cifra con hilos | La UC del total sale de los tokens sumados |
| T-107 | H-16 `limitaciones` en el orden de los hilos | `cierres` ordenados por tipo, fase y motivo |
| T-108 | H-22 `plan` o campos no serializables lanzan `TypeError` | `_error_de_forma` los rechaza (DATOS_INCOHERENTES, en RC) |
| T-108 | H-23 la cota de MON-EXP no acota la probabilidad de cada reunión | `incertidumbre_probabilidad` sale de la diferencia de filas del jacobiano; `incertidumbre_probabilidad_acumulada`, la de antes |
| T-108 | H-24 ventanas y plazos de MON e IDX sin dominio | `DOMINIOS` y `_dominio` en `fichas_mon_idx.py`, con topes `[PROPUESTO]` (INC-T113-01) |
| T-108 | H-25 mutantes N02, N05 y N10 | Pruebas en `test_t113_deuda.py`, y `approx` sin tolerancia absoluta en `test_t106_r03.py` |
| T-108 | H-27 MON-EXP rechaza curvas escalonadas redondeadas con la precisión declarada | El desajuste admitido es la cota del residuo de mínimos cuadrados, |(I − A·A⁺)·G|·precisión |
| T-109 | H-34 ticker en minúscula tras «la acción», «el valor» o «el título» | Se caza si está en el universo (`perm["tickers"]`). Uno de fuera del universo sigue siendo un límite declarado |
| T-109 | Romanos como cantidad | «las VII ideas» es CIFRA; «Basilea III» y «siglo XXI» siguen siendo nombres |
| T-110 | H-50 una o tres frases de 30 s rechazan la respuesta entera | El esquema SINTESIS admite de una a tres. Se toman las dos primeras o se completa con el texto por defecto, y se declara (FORMATO). La instrucción dice «exactamente dos» |
| T-110 | H-51 mutantes vivos | Una frase por mutante en `test_t113_deuda.py` |
| T-110 | H-49 singular, motivos de claves ajenas y minúscula tras quitar | Concordancia en las frases del código; solo motivos de tipos del paquete; el trozo que queda empieza en mayúscula |
| T-110 | H-52 siglas institucionales | AIE, INE, EPA, TAE y BID entran en `filtro_r21_codigos`; G7, G10 y G20 salen |
| T-110 | H-53 «N·V·D·A» | El punto medio, el punto, el guion y la barra también separan letras sueltas |

## Criterios de aceptación (binarios)

1. CA-1: cada hallazgo de la tabla tiene su corrección y una prueba que falla sin ella.
2. CA-2: la V5 no cambia, salvo lo declarado: la curación cargada a su bolsa (H-14), el singular de la frase por defecto (H-49) y el orden de las limitaciones (H-16).
3. CA-3: el gate da 12/12 sin subir cuotas (ruff baja de 2907 a 2902).

## Registro

- 2026-11-13 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-13 · EN QA · los hallazgos de las cinco filas corregidos; `tests/test_t113_deuda.py` (57); pruebas de T-102 y T-106 adaptadas al cambio buscado. Al editar se vació por error `diseno_v6.py` (un script lo abrió para escribir antes de leerlo); se recuperó de su versión subida y se reaplicaron los cambios
