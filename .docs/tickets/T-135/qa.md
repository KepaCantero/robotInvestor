# T-135 · QA independiente

- **Revisor:** Claude (subagente revisor nuevo, sin contexto de la implementación) · **Ronda:** r01 · 15-11-2026
- **Base revisada:** copia desconectada en `27905f4` («wip local: T-135»; diferencias con `eb66257`). Sin commit.

## Reproducción desde limpio

Intérprete `/home/user/robotinvestor/.venv/bin/python` (PY). Desde la raíz de la copia salvo que se diga otra cosa.

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A, una vez (`cd bloque_a/11_Ejecutor && $PY -m pytest -q -p no:cacheprovider`) | **5923 passed** en 25 min 18 s, código 0 (línea base 607) |
| `Motor.verificar_casos_control()` en un almacén nuevo | 67/67 superados; 67 entradas en RC, ninguna con el aviso (1.6) |
| `$PY tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff de los tres ejecutores desde la raíz (`ruff check --output-format=concise … \| wc -l`) | 2902 (cuota 2902) |
| mypy de A como el gate (`mypy bloque_a --ignore-missing-imports --no-error-summary \| wc -l`) | 109 (cuota 109); ninguna línea de `frontera_b`, `fichas_mon_idx`, `fichas_p2` ni `fichas_reales` |
| `tools/secrets_scan.py`, `refs_vivas.py`, `nfc_check.py`, `corpus_integridad.py` | sin hallazgos · rutas vivas · NFC · 695 archivos íntegros |
| Scripts de origen: `T-127/revisores/r03_01_cota_aviso_y_origen.py bloque_a/11_Ejecutor` | 11/11 |
| `T-128/revisores/r02_01_chr_flow_e_idx_conc.py bloque_a/11_Ejecutor` | 18/18 |
| `revisores/impl_frecuencia_aviso_token.py bloque_a/11_Ejecutor` | las cifras de `analisis-tecnico.md` (20 tokens sin *staking*: 45,8 % → 5,8 %; con *staking*: 0 %; prudente: 1,3 %) |
| `revisores/impl_mutantes.py bloque_a/11_Ejecutor <scratchpad>/qa16_mut/t135_mut --base eb66257` | REV: 16 de 28 pruebas nuevas fallan con los módulos de `eb66257`; 27 mutantes, **ninguno vivo** |
| Mis scripts: `revisores/r01_01_copias_idx_conc.py` y `r01_02_aviso_firmas.py` (con `python -I`, argumento `bloque_a/11_Ejecutor`) | `r01_01`: 34 ok · 5 hallazgos (H-01 ×4, H-04); `r01_02`: 20 ok · 4 hallazgos (H-02 ×2, H-04 ×2). `r01_02` contra `eb66257` (con `git archive` en una carpeta desechable) para comparar antes y después |

No se lanzó `./tools/check_all.sh` (instrucción de la coordinación), ni las suites de A-Forex y B.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (T-128 H-05) | sí (literal; ver H-01) | `r01_01` [C]: A + copia exacta, ×0,01, ×37 y recortada (desde la sesión 40) → amplitud `null`, sin identificadores en las limitaciones; 19 copias + B servida, 20 y 60 copias + B `null`; 20 copias recortadas cada una desde otra sesión y una cadena de 29 casi copias (cierre transitivo) `null`. Dos valores distintos a mano (prueba `test_h05_dos_valores_distintos…`). [K]: peso de los 5 mayores, HHI, N_ef, HHI sectorial y n idénticos a mano con y sin copias; equiponderado de 8 ⇒ N_ef = 8. `r02_01` 18/18. La prueba de T-128 r02 cambia, comentada «T-135» (justificada, abajo). **Pero** una copia redondeada o con una sesión ausente no se agrupa (H-01). |
| CA-2 (T-128 H-06) | sí | mutante F01 (sin `grupos` en `_sin_dominio`) muerto por `test_h06_chr_flow_dominancia_de_un_grupo_de_copias` |
| CA-3 (T-127 H-06) | sí | `r03_01` 11/11 (A3 sin aviso); `test_h06_dos_tokens…[True/False]`; las copias con un dato movido de `test_t127_r03.py` siguen dando el aviso (suite); RC de los casos de control sin aviso. Ver H-02 (una vía nueva sin aviso). |
| CA-4 (T-127 H-07) | sí | `r01_02` [N]: A en dos partes con el NAV por acción ±4 % da el aviso con y sin `otros_pasivos` (antes de T-135, sin ellos: 0 avisos); el precio movido, aviso; deuda, cap rate, GAV y otros pasivos movidos, rechazo por aportación |
| CA-5 (T-127 H-08) | sí | docstring de `frontera_b.py`: «… salvo que quien pide haya construido los componentes para ello (…límite declarado…)»; `test_h08…` |
| CA-6 | sí | casos de control 67/67; 27/27 mutantes muertos; ruff 2902 ≤ 2902; mypy 109 ≤ 109; INC-T128-01 e INC-T127-01 con «Ronda T-135» y `[PROPUESTO]` |

**Pruebas cambiadas.** `test_t128_r02.py::test_h02_idx_conc_porcentaje_sobre_la_media_de_un_solo_valido`: la aserción
antigua (`{"C00": largo, "C01": largo * 0.5}` → porcentaje 1,0) fijaba como correcta la fuga de H-05; ahora ese caso da
`amplitud` `null` y el caso servido con dos válidos se conserva con una serie distinta (`np.geomspace`: rentabilidad
constante frente a la recta de `largo`, distintas en cada sesión). La primera mitad (un solo válido → `null`) no cambia.
**Justificada, no debilitada.** `test_t127_r03.py::test_h04_el_aviso_cuenta_los_datos_que_coinciden`: la igualdad exacta de
`AVISO_B` gana la clave nueva; sigue fijando `datos_distintos_aviso = 1` y ahora también el 2. **Justificada.**

**Números.** `coincidencias_informativas_minimas = 2` en `AVISO_B`, con su motivo (= `datos_distintos_aviso` + 1) y
`[PROPUESTO]` en INC-T127-01; la regla de copias de la amplitud usa `tolerancia_clon` (1 %) y `peso_maximo_componente`
(95 %) de `FRONTERA_B`, `anios_precios_min` (1 año, «Entradas mínimas» de la ficha IDX-CONC-001, leída por su
identificador) y `DIAS_ANIO` (convención). La petición no los cambia: `r01_01` [P] — `tolerancia_clon`,
`peso_maximo_componente`, `componentes_minimos`, `IDX_CONC_COMPONENTES_MINIMOS`, `coincidencias_informativas_minimas` y una
clave cualquiera se aceptan y no cambian nada (la ficha lee esos números del módulo); `anios_precios_min`, `top_n_rango` y
`ventana_percentil_min_anios` se rechazan como umbrales fijos; `media_amplitud` de 1 a 2520 no reabre la fuga.
**`_params` y las claves no declaradas:** en `fichas_mon_idx` solo se leen de `p` claves con valor por defecto en
`PARAMETROS_POR_DEFECTO` (recorrido AST), salvo `nivel_ic` de IDX-REB-001, opcional y documentado en su docstring (T-106).
Para T-135 no afecta: ninguna regla de la frontera sale de `p`. Queda como observación (O-01).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_01` [C], «vías fuera de la regla»: A (paseo a ~1234 o a ~50) y la misma serie (a) con una sesión menos (`A.drop(A.index[150])`), (b) en libras con 2 decimales (`(A / 100).round(2)`, la acción que cotiza en peniques), (c) de otro proveedor con 2 o 3 decimales frente a 6 | Esperado: una copia a escala de A, amplitud `null` (lo que la regla dice cubrir: «una serie y sus copias, exactas o a escala»). Obtenido: **servida** con el porcentaje de A (0,0 = el de A) y la línea ≈ el doble de la de A, en los cuatro casos. Solo se agrupan copias idénticas en coma flotante: con 2 decimales, 268 de 319 rentabilidades difieren más del 1 % relativo (la tolerancia es por rentabilidad y relativa al mayor, así que los días de rentabilidad pequeña la rompen); con una sesión ausente, la rentabilidad del día siguiente es de dos sesiones en una serie y de una en la otra. No son «rentabilidades perturbadas a propósito»: son la forma corriente de una misma serie de dos fuentes (fugas accidentales con pocos componentes). Una conversión a otra divisa a cambio fijo con 4 decimales a ~1300 sí se agrupa. El desfase de una sesión tampoco se agrupa (límite declarado «muestreada en otras fechas») | (a) Sesión ausente: comparar cada par en su rejilla común (la rentabilidad entre fechas consecutivas en que **las dos** tienen precio), no entre los precios propios de cada serie. (b) Redondeo: una tolerancia que admita el error de redondeo de cada precio (p. ej. el paso mínimo observado en la serie entre su precio), o el cociente de precios. Medido en esta QA: «copia si `max |log(pᵢ/pₖ) − mediana| ≤ 1 %`» agrupa los cuatro casos, no agrupa al índice frente a su rentabilidad total, pero toma por copias el 6 % (19/300) de los pares de índices con ρ ≈ 0,995 y todos los fondos con error de seguimiento de 0,1 %/año: necesitaría su propia cota (número nuevo con origen). Decisión de diseño del implementador; pruebas con los casos de `r01_01` | abierto |
| H-02 | baja | `r01_02` [T]: token de oferta fija y entera en circulación (circulante = total = máxima = 4,2e8, sin emisión ni quema) y una copia con **solo** la oferta circulante −4 %, con y sin *staking* y concentración | Esperado: aviso (un dato de entrada movido, lo que el aviso marca). Obtenido: 0 avisos en T-135; con los módulos de `eb66257`, 1. La firma pone la total a ``None`` cuando es la circulante: en el original va ``None`` y en la copia 4,2e8, así que mover un dato da dos diferencias. Es una regresión del aviso (a cambio, mover la total y la máxima a la vez, dos datos, ahora sí lo da) | En lugar de poner a ``None`` lo que repite otro dato (que crea una diferencia), mantener la firma de antes y no contar como coincidencia informativa la de un dato que repite otro **en los dos** tokens (total = circulante en ambos, máxima = total en ambos). Las dos vías de `r01_02` y los dos tokens fijos del revisor quedan bien | abierto |
| H-03 | baja | `r01_01` [R] (n = 2000 con el mismo generador en un script desechable, ya borrado): IDX-CONC-001 con n series de 2520 sesiones, una salida a bolsa reciente (380 sesiones) y una exclusión antigua sin fechas comunes con ella | Esperado: coste del orden de antes. Obtenido: n = 500 → 6,3 s; n = 1000 → 26 s; n = 2000 → **164 s** (con `eb66257`, 0,7 s; ×235) y 476 MB. `_etiquetas_series_copiadas` recorre las T fechas con matrices n × n y solo corta cuando **todos** los pares ya difieren: un par sin fechas comunes, o una serie que empieza tarde, lo impide. Un índice amplio (2000–3000 valores) tarda minutos | Comparar solo los pares que siguen siendo candidatos (lista dispersa que se vacía) o agrupar primero por la rentabilidad de la primera fecha común redondeada; o un tope de componentes con su origen. Prueba de coste con n = 2000 |
| H-04 | baja (preexistente) | `r01_02` [Z]: IDX-CONC-001 por `valores["precios"]` con un precio 0 (o −1) en la misma sesión de A y de su copia ×2 | Esperado: rechazo (un precio ≤ 0 no es un dato válido; HT-01 los rechaza, `DatosInvalidos`). Obtenido: servida con el porcentaje de A; con el 0, la rentabilidad infinita (`inf − inf` = NaN) hace distintas a las dos series y la copia deja de serlo, con `RuntimeWarning`. `_serie` acepta precios ≤ 0 desde antes de T-135 | Rechazar precios ≤ 0 en los `precios` de IDX-CONC-001 (falla cerrado, como HT-01) |  abierto |
| H-05 | baja | `r01_01` [C]: 2 copias de A + B (A bajo su media, B sobre ella) | Servida (2 distintos, el grupo es 2/3 < 95 %) con porcentaje 1/3 = (2·A + B)/3: despeja A y B por separado; con A y B solos sería 0,5, que no dice cuál. Las copias cuentan como uno para el mínimo y la dominancia, pero cada serie pesa en el cálculo (decisión documentada para no cambiar `test_idx_conc_valores_a_mano`) | Documentarlo como coste en INC-T128-01 o, si se quiere cerrar, que el cálculo cuente cada grupo de copias una vez (cambia el caso a mano con X e Y iguales: decisión del operador) | abierto |

**Observaciones (sin gravedad):**

- O-01. `fichas_mon_idx._params` acepta claves que la ficha no declara y las ignora (FIR-CRED y `fichas_reales` las
  rechazan): una errata como `top_N` pasa en silencio. No afecta a la frontera (ninguna regla sale de `p`). Preexistente;
  apuntarlo en la deuda.
- O-02. Falsos positivos de «copia»: ninguno en 300 semillas para un índice de precios frente a su rentabilidad total
  (dividendo 2 %/año), dos índices de un mercado con ρ ≈ 0,995, y un fondo frente a su índice con un error de seguimiento
  de 0,1 % y 0,01 % al año. Dos series planas de valores distintos un año entero sí se toman por copias (caso degenerado:
  da `null`, falla cerrado).
- O-03. Frecuencia del aviso con «datos corrientes»: los números del implementador se reproducen (5,8 % con 20 tokens sin
  *staking* con el generador de la r03, 1,3 % con el prudente, 0 % con *staking*). Es un aviso, no un rechazo.
- O-04. La fila de T-135 (y la de T-128) no está en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`
  de esta copia, aunque el README del ticket la cita: que la añada quien cierre.

Invariantes: no hay LLM en la ruta (cambios solo en el Motor determinista); los controles no se relajan (el aviso pierde
una vía, H-02, pero ningún rechazo se quita); falla cerrado salvo H-04 (preexistente); ningún número a mano sin origen;
decisiones `[PROPUESTO]`; sin secretos ni datos personales (`secrets_scan`); ninguna vía de orden tocada.

## Veredicto

**APTO** · los seis criterios se cumplen con evidencia y no queda ningún hallazgo crítico ni alto. H-01 (media) y H-02 a
H-05 (bajas) y O-01 pasan a la deuda técnica con su ID (`T-135 H-01`…). Recomendación: corregir H-01 antes del modo sombra,
porque es la forma corriente de la fuga que T-128 H-05 pedía cerrar (hoy solo se agrupan copias idénticas en coma flotante;
con los datos de HT-01 de un solo proveedor eso cubre lo accidental más probable, una misma serie cargada con dos
identificadores, pero no la misma serie de dos fuentes).
