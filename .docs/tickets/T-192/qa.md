# QA · T-192 · PB-34 (fuga detectada) y PB-35 (recalibración con evaluación sombra)

## Ronda r01 · 24-11-2026 · Claude (revisor independiente; no implementó)

**Veredicto: NO APTO** (1 hallazgo alto, 2 medios y 4 bajos).

Código revisado: rama `astra/encargos-bloque-a-c38-c47`, tip `2d99af6`, sobre `develop` `9ce57b2`. Commit del ticket:
`7038e1b`. `5ef929b` endurece después `sombra.py` (pares de dos números finitos). Ficheros: `evaluador.py`
(`resolver`, `resueltos`, `corregir_fugas`, `cerrar_sombra`, `ciclo`), `sombra.py` (nuevo) y `orquestacion.py`
(`rk_pareado` en la sombra de cada RUN-).

Vara de medir, plan V3.0: PB-34 «Ningún AJU- ni CERT- apoyado en métricas FALLIDA; corrección registrada en F6», con
«recálculo con vintage y tasa base sin fuga como entrada nueva; recalibración bloqueada hasta disponer de métricas
limpias»; PB-35 «Bandas respetadas; sombra registrada; decisión documentada con DM-HLN», con «al cierre, CONFIRMADO o
REVERTIDO según la regla, con registro». La regla es la del prompt del Evaluador V5.0, 8: se revierte «si la nueva
versión es peor con DM-HLN p < 0,10 o si su métrica objetivo es inferior y no hay ganancia en ninguna otra»; se
confirma en otro caso. El registro es el AJU- del esquema de F6 V2.0, 4.6.

### Reproducción desde limpio

Worktree propio en `2d99af6`, Python 3.12, venv del repo.

| Comprobación | Resultado |
|---|---|
| `tests/test_t192_evaluacion.py` (3 pruebas) | 3 superadas |
| Las pruebas nuevas con el código de `9ce57b2` (revertido `7038e1b` en un worktree aparte) | las 3 fallan |
| `mutantes.py` de Astra (2 mutantes) | los 2 muertos |
| Vecinas: `test_t173.py`, `test_t176_pb36_pb33.py`, `test_t66_evaluacion.py`, `test_t65_qa_r01.py`, `test_unitarias.py`, `test_integracion.py` | 189 superadas en una sola tanda (con `test_t178.py`, `test_t53_evaluacion_y_almacen.py` y las del ticket) |
| `revisores/r01_mutantes_revisor.py` (14 mutantes propios; dos de control de Astra mueren con el mismo ejecutor) | **14 vivos** (H-02) |
| `revisores/r02_ataques_sombra.py` (cierre de sombra con ruido y con la configuración por defecto) | 3 fallos de 8 (H-01, H-03, H-05) |
| `revisores/r03_ataques_fuga.py` (PB-34 de punta a punta con el cliente simulado: C1 y dos C5) | 1 fallo de 15 (H-06) |
| ruff y mypy de los ficheros tocados frente a `9ce57b2` | sin subida (ruff: `evaluador.py` 3 = 3, `sombra.py` 0, prueba nueva 0; mypy A 102 = 102) |

Lo que sí cumple, con evidencia de `r03_ataques_fuga.py`: una tasa base calculada después de la emisión, o con un dato
posterior a la emisión dentro de la base, deja la resolución FALLIDA con `fuga_tasa_base`; la FALLIDA no entra en el
FC-EVAL-001 del día ni cita su CALC-; C5 recalcula RI-TB con el corte original (`as_of` del nuevo CALC- = emisión;
ningún dato posterior), registra una entrada nueva en F6 con `brier_ref` y `log_ref` recalculados y el `brier` del
modelo intacto; F4 no se reescribe; `resueltos()` usa la referencia y las puntuaciones corregidas; un segundo C5 no
duplica la corrección; la integridad del almacén se mantiene. De `r02_ataques_sombra.py`: con ruido y la muestra
mínima rebajada, una mejora clara se CONFIRMA (p = 0,999) y un empeoramiento claro se REVIERTE (p = 0,0007), también
con pronósticos NEGATIVOS; el día anterior a `sombra_hasta` no se cierra, el mismo día sí, y no se cierra dos veces.
T-176 y T-173 no se rompen: la recalibración sigue sin proponer con un AJU- EN_SOMBRA, las bandas y el acumulado solo
cuentan EN_SOMBRA y CONFIRMADO, y la DM-HLN es la de `motor/evaluacion.py`, sin cambios.

### Hallazgos

#### H-01 · alta · Con la configuración por defecto, la sombra no se puede confirmar nunca

- **Reproducción:** `r02_ataques_sombra.py`, caso 1: configuración por defecto, un trimestre de sombra semanal con una
  mejora clara del IC de Spearman: `REVERTIDO · Muestra pareada insuficiente · fechas = 12`.
- **Causa:** `sombra.comparar` exige `len(medias) >= evaluacion.min_calibrar`, es decir, 30 **fechas** de RUN- con
  pares. `min_calibrar` es el mínimo de 30 **pronósticos resueltos** por celda del Anexo A (regla 5 de F6). Con
  `meses_sombra: 3` y ciclo semanal hay como mucho 13 fechas: la regla de cierre degenera en «REVERTIDO siempre». La
  prueba del ticket solo pasa porque rebaja `min_calibrar` a 3.
- **Corrección:** en `sombra.comparar`, contar la muestra en pronósticos pareados resueltos:
  `n_pares = sum(len(f) for f in series.values())`; muestra insuficiente si `n_pares < min_calibrar` o si hay menos
  de 3 fechas (el mínimo del propio `diebold_mariano_hln`, que con n < 3 devuelve p None). Guardar `n_pares` y
  `n_fechas` en el registro. Declarar la regla en INC-T192-01.
- **Prueba de regresión:** con la configuración por defecto (sin tocar `min_calibrar`), 13 fechas semanales con 3 PRG
  pareados cada una (39 ≥ 30) y una mejora clara: CONFIRMADO; con 9 fechas de 3 PRG (27 < 30): REVERTIDO por muestra.

#### H-02 · media · Las pruebas no matan ninguno de los 14 mutantes del revisor

`revisores/r01_mutantes_revisor.py` pasa `test_t192_evaluacion.py` con cada mutante. Todos quedan vivos:

| Mutante | Qué deja de comprobarse |
|---|---|
| M01, M02 | la FALLIDA entra en el FC-EVAL-001 del día o cita su CALC- |
| M03 | el recálculo se hace con la fecha del C5 (una fuga nueva en la corrección) |
| M04, M06 | la corrección no recalcula `brier_ref`/`log_ref`, o `resueltos()` no la aplica |
| M05 | cada C5 escribe otra corrección del mismo PRG |
| M07 | DM-HLN con el sentido invertido (los datos de la prueba tienen varianza 0: p = 0,5 en los dos sentidos) |
| M08, M09, M10 | entran RUN- no entregados, fuera de la ventana o de otro AJU- |
| M11 | se ignora el sentido del pronóstico |
| M12 | se cierra antes de `sombra_hasta` |
| M13 | se ignora el umbral de p del DM-HLN |
| M14 | se ignora la muestra mínima |

Los comportamientos son correctos hoy (lo muestran `r02` y `r03`), pero ninguna prueba los ata.

- **Corrección:** llevar a `tests/test_t192_evaluacion.py` los casos de `r03_ataques_fuga.py` (FALLIDA fuera del
  FC-EVAL-001 y sin CALC-; corte original del recálculo; `brier_ref`/`log_ref`; `resueltos()` corregido; segundo C5 sin
  duplicar; un dato posterior dentro de la base) y los de `r02_ataques_sombra.py` con ruido (mejora y empeora con
  p real, sentido NEGATIVO, día anterior y día de `sombra_hasta`), más tres casos de filtro: un RUN- no ENTREGADA, un
  RUN- fuera de `[efecto_desde, sombra_hasta]` y la sombra de otro `aju_id`, que no cuentan. Añadir los 14 mutantes a
  `mutantes.py` del ticket.
- **Prueba de regresión:** `revisores/r01_mutantes_revisor.py` con los 14 muertos.

#### H-03 · media · El AJU- cerrado no sigue el esquema de F6

- **Reproducción:** `r02_ataques_sombra.py`, caso 4: el cierre escribe `dm_hln`, `estado`, `fecha_cierre`,
  `fechas_pareadas`, `ic_anterior`, `ic_nueva` y `motivo_cierre`. El esquema de F6 V2.0, 4.6, define
  `resultado_sombra {metrica_nueva, metrica_anterior, dm_hln_p, decisiones_top3_cambiadas, decision CONFIRMADO·REVERTIDO}`.
  Falta `decisiones_top3_cambiadas`, que el prompt del Evaluador (8) también pide comparar y que el ejecutor ya tiene
  (`cambios` de la sombra de cada RUN- y la entrada SOM- de F6). Regla 3 del proyecto: el formato sale del artefacto.
- **Corrección:** escribir en el AJU- de cierre `resultado_sombra` con esas cinco claves (`metrica_*` = IC medio,
  `dm_hln_p` = `p_unilateral`, `decisiones_top3_cambiadas` = suma de `cambios` de los RUN- de la ventana con ese
  `aju_id`, `decision` = el estado) además de `estado`; el detalle (`dm_hln` completo, fechas, n) puede ir aparte.
- **Prueba de regresión:** las claves de `resultado_sombra` son las del esquema y `decisiones_top3_cambiadas` es la suma
  de `cambios` sembrados en los RUN- de la ventana (y no cuenta los de fuera).

#### H-04 · baja · La regla de cierre usa un número de otro parámetro y simplifica la regla sin declararlo

- **Qué pasa:** el umbral del DM-HLN es `evaluacion.alfa_holm` (el α de Holm del certificado de horizonte, R13). Su
  valor coincide hoy (0,10), pero el 0,10 de la reversión es otro número, del prompt del Evaluador 8. Además se
  revierte con «IC medio inferior» sin mirar «no hay ganancia en ninguna otra» métrica. INC-T192-01 no lo declara.
- **Corrección:** clave propia `evaluacion.recalibracion_rk.p_reversion: 0.10` con comentario de origen (prompt del
  Evaluador V5.0, 8) y `[PROPUESTO]` en INC-T192-01, que recoja también la simplificación a una métrica (o implementar
  la segunda: `decisiones_top3_cambiadas` no es una ganancia, así que basta con declararlo).
- **Prueba de regresión:** con `p_reversion` distinto de `alfa_holm` (p. ej. 0,01 frente a 0,10) y una serie con
  p ≈ 0,05, la decisión sigue a `p_reversion`.

#### H-05 · baja · Un registro histórico incompleto tumba el resto del C5

- **Reproducción:** `r02_ataques_sombra.py`, caso 5: una resolución RESUELTO sin `valor_observado` dentro de la ventana:
  `KeyError('valor_observado')` en `sombra.comparar`. `Evaluador.ciclo` no protege `cerrar_sombra` (sí protege la
  degradación DM, la revisión trimestral, la fiabilidad y las novedades, que van después): en cada C5, mientras el AJU-
  siga EN_SOMBRA, nada de eso se ejecuta y el Orquestador solo ve «Evaluador no disponible».
- **Corrección:** en `comparar`, saltar la fila si `valor_observado` no es un número finito o falta `sentido`/`clase`
  (como ya se hace con `rk_pareado`); en `ciclo`, envolver `cerrar_sombra` como las demás fases (incidencia
  HERRAMIENTA y `aju = self.recalibrar(...)` no se ejecuta ese ciclo).
- **Prueba de regresión:** el caso 5 de `r02` cierra la sombra sin excepción; y con `comparar` forzado a fallar,
  `Evaluador.ciclo` termina, deja la incidencia y publica las novedades.

#### H-06 · baja · La fuga detectada no avisa y la corrección no está declarada en el esquema

- **Reproducción:** `r03_ataques_fuga.py`, último caso: tras detectar la fuga y corregirla, HA no tiene ninguna entrada.
  La tabla de fallos del prompt del Evaluador V5.0 dice «Fuga detectada a posteriori: métricas recalculadas como entrada
  nueva; certificados afectados revocados; ajustes afectados revertidos; aviso al Orquestador». Si el recálculo no se
  puede hacer (`DatosNoDisponibles` en `corregir_fugas`), se calla y el PRG queda fuera sin rastro. Además, el tipo
  de entrada `CORRECCION_FUGA` de F6 no está en el esquema de F6 V2.0 (que solo tiene RES-, MET-, CERT-, LEC-, FUE-,
  AJU-, P3-EVAL-, HAC-, PRO-/BAN-) ni en INC-T192-01 (regla 7: ambigüedad del spec, incidencia).
- **Corrección:** en `resolver`, por cada FALLIDA por tasa base, `almacen.incidencia("OTRO", …, prg_id,
  severidad="Operativa", tratamiento="resolución FALLIDA; corrección en C5")`; en `corregir_fugas`, al registrar la
  corrección, un `COR-` en HA (esquema HA V2.0, 4.8: `entrada_corregida`, `motivo`, `comunicado_a: ["AG-18"]`), y si
  no se puede recalcular, una incidencia HERRAMIENTA. Declarar en INC-T192-01 la entrada `CORRECCION_FUGA` de F6 y sus
  campos.
- **Prueba de regresión:** el último caso de `r03` encuentra el aviso y el COR- (uno, también tras el segundo C5), y con
  el proveedor sin datos para el recálculo queda una incidencia y ninguna corrección.

#### H-07 · baja · El mapa y las evidencias mezclan PB-34 y PB-35

- **Qué pasa:** en `tests/mapa_plan_pruebas.json` (y en `docs/evidencias_pruebas_bloque_a.md`, generado de él), el
  «comprueba» de PB-34 termina con «…y documenta la decisión de sombra mediante comparaciones pareadas y DM-HLN» (es
  PB-35) y el de PB-35 empieza su añadido con «F6 conserva la corrección de la base contaminada…» (es PB-34). El «no
  comprueba» de PB-35 («Datos de prueba controlados») no dice qué falta.
- **Corrección:** PB-34: «…F6 registra la corrección (RI-TB con el corte original y puntuaciones de referencia
  recalculadas) como entrada nueva y las métricas la usan». PB-35: «…al cierre de la sombra, CONFIRMADO o REVERTIDO
  con DM-HLN sobre los IC de RK pareados, registrado en el AJU- (resultado_sombra)». «No comprueba» de PB-35: la
  aplicación a producción (PA-10, decisión del operador) y una sombra con resultados reales. Regenerar las evidencias
  con `.docs/scripts/evidencias_plan_a.py --ejecutar`.
- **Prueba de regresión:** la prueba de coherencia del mapa (la que ya liga mapa y evidencias) en verde tras regenerar.

### Invariantes

- Números: H-01 (un mínimo de pronósticos usado como mínimo de fechas) y H-04. Los recortes 0,01/0,99 del log son los
  mismos que ya usa `resolver`.
- Esquemas y corpus congelados: ningún fichero congelado cambia; `rk_pareado` es un campo nuevo de la sombra del RUN-
  de F5, no de un contrato CT, y no toca ningún golden. F6: H-03 y H-06.
- Fallar cerrado: muestra insuficiente o p None revierten; un par no numérico se salta; `cerrar_sombra` y
  `corregir_fugas` van en una transacción del almacén. H-05 es la excepción.
- Los controles no se relajan solos: CONFIRMADO no toca F10 ni la configuración (PA-10), como dice el handoff.
- R8 y G3-MET-13: sin textos ni datos protegidos nuevos (la única raíz «valid-» es el nombre de una variable).
- Pruebas antiguas: este ticket no cambia ninguna. Los cambios de `test_fase4_huecos.py` (T-189) y
  `test_t159_extremo_a_extremo.py` (T-191; `5ef929b` solo quita un `import` sin uso) son de otros tickets.
- Mapa y evidencias: PB-34 y PB-35 siguen «Superada en parte» y PARCIAL, sin subir a «Superada»: honesto en el estado.
  El texto: H-07.

### Regresión

Una sola tanda con `test_t173.py`, `test_t176_pb36_pb33.py`, `test_t178.py`, `test_t66_evaluacion.py`, `test_t65_qa_r01.py`, `test_t53_evaluacion_y_almacen.py`, `test_unitarias.py`, `test_integracion.py` y las de T-192 y T-193: 189 superadas, 0 fallos (8 min 29 s). El gate completo (12/12) lo pasa el coordinador
sobre la copia del PR.

### Scripts del revisor

- `revisores/r01_mutantes_revisor.py`: mutantes propios (`python -I .docs/tickets/T-192/revisores/r01_mutantes_revisor.py`).
- `revisores/r02_ataques_sombra.py` y `revisores/r03_ataques_fuga.py`: desde `bloque_a/11_Ejecutor`.

Para la ronda r02: los tres scripts sin fallos y las pruebas de regresión de cada hallazgo.
