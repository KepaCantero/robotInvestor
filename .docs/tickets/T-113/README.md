# T-113 · Bloque A: deuda técnica T-104, T-107, T-108, T-109 y T-110

| Campo | Valor |
| --- | --- |
| Estado | EN QA (ronda r02, pendiente de lanzar; la r01 fue NO APTO) |
| Pieza | `bloque_a/11_Ejecutor` |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-13: «Corrige toda la deuda técnica» (la del Bloque A: T-104, T-107, T-108, T-109 y T-110; T-105 es de A-Forex y B) |
| Deuda técnica | T-104, T-107, T-108, T-109 y T-110 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los hallazgos que quedaron en la deuda tras las QA de T-103, T-88, T-106 y T-102, antes del modo sombra con la API.

## Qué se corrige

| Fila | Hallazgo | Corrección |
| --- | --- | --- |
| T-104 | H-54 una línea cortada en `cache_resultados.jsonl` o en la cinta impide arrancar | `leer_jsonl` (`herramientas/ht06_indice.py`): la última línea cortada se descarta. La caché descarta también cualquier otra ilegible y las cuenta; la cinta da el fichero y la línea. r02: quien va a seguir escribiendo deja el fichero acabado en un salto de línea (`acabar_en_salto`), y lo descartado se declara con una incidencia |
| T-104 | H-55 versión de Python | `requires-python = ">=3.12"`. r02: también en el README del ejecutor |
| T-104 | H-56 `contenido_sensible` cuesta profundidad × tamaño | Cada diccionario que no cuelga de otro se serializa una sola vez (r02: también los que cuelgan de una lista, una tupla o un conjunto; en la r01 solo el de arriba) y las hojas se recorren sin recursión; 400 niveles con 1 MB, en 0,3 s (antes 60 s). Si es demasiado profundo para serializarlo o se contiene a sí mismo, falla cerrado |
| T-107 | H-14 la curación de AG-12 va sin presupuesto | Se carga a la bolsa de su tipo |
| T-107 | H-15 `consumo.uc` varía en la cuarta cifra con hilos | La UC del total sale de los tokens sumados |
| T-107 | H-16 `limitaciones` en el orden de los hilos | `cierres` ordenados por tipo, fase y motivo |
| T-108 | H-22 `plan` o campos no serializables lanzan `TypeError` | `_error_de_forma` los rechaza (DATOS_INCOHERENTES, en RC) |
| T-108 | H-23 la cota de MON-EXP no acota la probabilidad de cada reunión | `incertidumbre_probabilidad` sale de la diferencia de filas del jacobiano; `incertidumbre_probabilidad_acumulada`, la de antes |
| T-108 | H-24 ventanas y plazos de MON e IDX sin dominio | `DOMINIOS` y `_dominio` en `fichas_mon_idx.py`, con topes `[PROPUESTO]` (INC-T113-01) |
| T-108 | H-25 mutantes N02, N05 y N10 | Pruebas en `test_t113_deuda.py`, y `approx` sin tolerancia absoluta en `test_t106_r03.py` |
| T-108 | H-27 MON-EXP rechaza curvas escalonadas redondeadas con la precisión declarada | El desajuste admitido es la cota del residuo de mínimos cuadrados, |(I − A·A⁺)·G|·precisión |
| T-109 | H-34 ticker en minúscula tras «la acción», «el valor» o «el título» | Se caza si está en el universo (`perm["tickers"]`). Uno de fuera del universo sigue siendo un límite declarado |
| T-109 | Romanos como cantidad | «las VII ideas» es CIFRA; «Basilea III» y «siglo XXI» siguen siendo nombres. r02: solo un romano bien formado (hasta XXXIX) que no sea una sigla permitida; «Las IIC» y «Los VIX» pasan |
| T-110 | H-50 una o tres frases de 30 s rechazan la respuesta entera | El esquema SINTESIS admite de una a tres. Se toman las dos primeras o se completa con el texto por defecto, y se declara (FORMATO). La instrucción dice «exactamente dos». r02: con ninguna o con cuatro (la respuesta no cumple el esquema) se entregan los textos por defecto y una limitación lo dice |
| T-110 | H-51 mutantes vivos | Una frase por mutante en `test_t113_deuda.py` |
| T-110 | H-49 singular, motivos de claves ajenas y minúscula tras quitar | Concordancia en las frases del código; solo motivos de tipos del paquete; el trozo que queda empieza en mayúscula |
| T-110 | H-52 siglas institucionales | AIE, INE, EPA, TAE y BID entran en `filtro_r21_codigos`; G7, G10 y G20 salen |
| T-110 | H-53 «N·V·D·A» | El punto medio, el punto, el guion y la barra también separan letras sueltas |

## Criterios de aceptación (binarios)

1. CA-1: cada hallazgo de la tabla tiene su corrección y una prueba que falla sin ella.
2. CA-2: la V5 no cambia, salvo lo declarado: la curación cargada a su bolsa (H-14), el singular de la frase por defecto (H-49), el orden de las limitaciones (H-16) y la cuarta cifra de `consumo.uc` y `consumo.uc_llm` del RUN, con la línea del informe técnico que las copia (H-15: la UC del total sale ahora de los tokens sumados; en la QA r01, 10,2447 → 10,2449 en el segundo ciclo).
3. CA-3: el gate da 12/12 sin subir cuotas (ruff baja de 2907 a 2902).

## Registro

- 2026-11-13 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-13 · EN QA · los hallazgos de las cinco filas corregidos; `tests/test_t113_deuda.py` (57); pruebas de T-102 y T-106 adaptadas al cambio buscado. Al editar se vació por error `diseno_v6.py` (un script lo abrió para escribir antes de leerlo); se recuperó de su versión subida y se reaplicaron los cambios
- 2026-11-13 · NO APTO · QA r01: H-01 (alta, regresión de R8 en `contenido_sensible`), H-02, H-03 y H-09 (medias), H-04 a H-08 (bajas); CA-1 no se cumple y ocho mutantes vivos (`qa.md`)
- 2026-11-14 · EN QA · ronda r02: H-01, H-02, H-03, H-06, H-07 y H-09 corregidos con sus pruebas (49 nuevas en `tests/test_t113_deuda.py`, 106 en total); H-05, documentación al día; H-08, decisión `[PROPUESTO]` en INC-T113-01 (la curación es alcance); H-04, corregido en T-118 y no duplicado aquí; CA-2 nombra `consumo.uc`. Los 54 mutantes del revisor: 52 muertos y los 2 equivalentes; los 13 scripts `r01_*`, repetidos (`pruebas.md`). Suite de A: 3874. Gate completo sin lanzar
