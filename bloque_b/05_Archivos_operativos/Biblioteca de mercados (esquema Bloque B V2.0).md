# Esquema de archivo operativo — F6 Biblioteca de mercados

**Bloque B · Robot Investor · Versión óptima V2.0 · actualizado V2.1, 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.1 (ante discrepancia, manda el Documento 0).

---

## 1. Propósito

F6 es la **memoria reutilizable por ámbito** del Bloque B (Documento 0, 5.1, 10.2 y 13.1). Cada ficha **MKT-B** es la ficha viva de un ámbito ya analizado y entregado: delimitación, tipo de objeto, mapa de la cadena de valor (sub-bloques 4a–4e), cifras clave con su DAT-B o CALC-B, actores por eslabón, universos de candidatos por tipo de activo con su fecha, fuentes clave de F9, ficha de régimen vigente, veredictos históricos con su resultado y **una caducidad por dimensión**. Las fichas **RGM-B** conservan las evaluaciones de régimen reutilizables.

Su función es la **eficiencia sin pérdida de rigor**: la puerta GC0 (9.8) decide en F0 qué dimensiones vigentes y sin cambio material se reutilizan (con re-verificación de primer uso) y cuáles se trabajan de nuevo; F1 se reduce a comprobar el delta; el Seleccionador parte del universo vigente; el Coordinador responde consultas N0 diciendo qué dimensión está caducada.

**No es**: un archivo de trabajo en curso (R6: solo contiene lo **entregado**), ni un sustituto de F2 (las cifras remiten a su DAT-B o CALC-B), ni de F3 (los veredictos se referencian por REC-B).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-B02 Director del Análisis de Mercado (una instancia por petición; escrituras **serializadas por clave MKT-B**, para que dos peticiones sobre ámbitos solapados no sobrescriban la misma ficha, 4.5) |
| Momento de escritura | Fase F10 de una petición entregada (nueva versión por dimensión); **V2.1**: también tras un **informe de parada** entregado (solo lo verificado; como mínimo la fecha y el motivo de la parada) y tras cada **ciclo de seguimiento** entregado (delta de las dimensiones clave); y tarea de fondo de 7.6 (solo marcar caducidades vencidas, con HT-05) |
| Lectores | Plano P2, AG-B01 (respuestas N0), AG-B21, AG-B22, AG-B23 |
| Contratos | CT-B-08 (la memoria relevante viaja en la orden de análisis), CT-B-09 (`reutilizable_F6` en el encargo dimensional), CT-B-10 (`universo_F6` en el encargo de selección) |
| Herramientas | HT-05 (vencimientos de caducidad), HT-06 (índice y búsqueda de ámbitos solapados), HT-01 (comprobación del cambio material) |

## 3. Reglas

1. **Solo contenido entregado** (5.2.2; R6): una ficha se crea o actualiza únicamente con el contenido de una REC-B `ENTREGADO` (incluida la de un informe de parada, `DETENIDO_EN_PUERTA`) o de un ciclo de seguimiento entregado (CIC-B del archivo F11). Nada de una petición en curso, cancelada, caducada o bloqueada entra en F6.
2. **Viva pero versionada**: cada actualización crea una **versión nueva por dimensión**; la anterior queda consultable (`supersedes`). Nunca se sobrescribe ni se borra una versión.
3. **Caducidad por dimensión** (Anexo A, calibrable): D1, D4 y D11, 12 meses · D2, D3 y D5, 6 meses · D6 y D8, 3 meses · D7 y D12, 1 mes · D9, 7 días (H1–H2), 1 mes (H3–H4) o 3 meses (H5, V2.1) · radar de emergentes, 3 meses (V2.1) · D10, 7 días · universos de candidatos, 1 mes · fichas de régimen, 1 mes. La caducidad se calcula desde el `data_cutoff` de la versión, no desde la fecha de escritura.
4. **GC0 (9.8)**: una dimensión es reutilizable si (a) no está caducada y (b) no hay **cambio material** desde su fecha: precio del indicador del ámbito > 1,5 desviaciones típicas desde la ficha; evento relevante del calendario; dato con sorpresa > 1 desviación típica; condición de invalidación a < 10 % (Anexo A). La decisión GC0 se registra en el PLAN-B con su motivo.
5. **Re-verificación de primer uso**: toda dimensión, régimen o universo reutilizado se re-verifica en su primer uso dentro de la petición (cifras clave contra su fuente, estado de las referencias en F7–F9 y de las EVD-B en F2); el resultado se anota en `usos`. Si la re-verificación falla, la dimensión se trata como caducada.
6. **Herencia no es evidencia** (R31): el contenido de la Biblioteca acelera el trabajo, pero sus afirmaciones se citan por su CLM-B vigente en F2; si su evidencia tiene `FUENTE_RETIRADA` o `REFUTADA`, la dimensión pierde la condición de reutilizable.
7. **Fichas de régimen**: se reutilizan con re-verificación de primer uso y se sustituyen (`supersedes`) cuando el régimen cambia; solo el mecanismo demostrado autoriza a apoyar una premisa crítica en la persistencia de una relación (8.9).
8. **Universos**: se guardan por tipo de activo con su fecha, sus fuentes, sus filtros y sus exclusiones motivadas, **incluidos los miembros excluidos y los deslistados posteriores conocidos**, para no introducir sesgo de supervivencia al reutilizarlos.
9. **Ámbitos solapados**: la ficha declara sus relaciones (`contiene`, `contenida_en`, `solapa_con`) para que GC0 encuentre memoria útil sin confundir ámbitos.
10. Sin datos personales ni claves (R10, R11).
11. **Cadena jerárquica y emergentes (V2.1)**: la cadena de valor se guarda como **desglose jerárquico** (macro → sub → actividad → insumo; ESL-) con, por eslabón, métricas, indicadores de cuello en semáforo, PCB, AE y la señal de resolución, y el **radar de emergentes** (EMG-B con PEM y vía de exposición). Caducidad (Anexo A): el desglose, los cuellos y el AE siguen la de D4 (12 meses), con el cambio material de GC0 como disparador de revisión anticipada; el **radar de emergentes**, 3 meses.
12. **Coincidencia con la Biblioteca en PV1 (V2.1)**: una ficha vigente con veredicto DESCARTAR y sin cambio material es un criterio **eliminatorio** de PV1 (`BIBLIOTECA_DESCARTAR`, 7.10).

## 4. Formato de entrada

### 4.1 Ficha de mercado (MKT-B)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `mkt_id` | Identificador | Sí | `MKT-B-NNNN` (estable por ámbito) |
| `nombre` / `nombre_llano` | Texto | Sí | — |
| `tipo_objeto` | Enumerado | Sí | Seis tipos de 2.5 |
| `delimitacion` | Objeto | Sí | `{incluye, excluye, region, clasificaciones_de_partida (GICS/ICB/NACE), correccion_por_exposicion}` |
| `relaciones` | Objeto | No | `{contiene[], contenida_en[], solapa_con[]}` (MKT-B) |
| `dimensiones` | Objeto | Sí | Claves D1…D12; cada una con su lista de versiones (4.2) |
| `cadena_valor` | Objeto | Sí | Versión vigente de 4a–4e: `{mapa (eslabones, participantes, HHI/CRn, costes, margen, dependencias), actores (establecidos y emergentes por eslabón, con invertibilidad), vigilancia_tecnologica (0–2, 2–5, 5+ años), cuellos [{eslabon, causa, persistencia, senal_resolucion, favorecidos, perjudicados, perdedores_sistematicos}], segundo_orden}` con `data_cutoff` y `rec_id` de origen |
| `cifras_clave` | Lista | Sí | `{nombre (TAM, crecimiento, márgenes, valoración agregada…), valor, unidad, divisa, fecha, dat_id o calc_id, etiqueta_epistemica, clase_cifra, dimension}` |
| `universos` | Objeto | Sí | Claves = tipos de activo aplicables; cada uno con versiones (4.3) |
| `fuentes_clave` | Lista | Sí | Fichas de F9 (y F7) por dimensión |
| `regimen_vigente` | Identificador | Sí | RGM-B |
| `historial_analisis` | Lista | Sí | `{rec_id, pet_id, fecha, veredicto, A, E, C, resultado (de F3 cuando lo haya)}` |
| `vigilancia_pre_salida` | Lista | No | `{actor, eslabon, salida_verosimil, caducidad (dos horizontes sin señal)}` |
| `desglose_cadena` | Objeto | Sí (V2.1) | `{eslabones [{eslabon_id, padre, nivel macro·sub·actividad·insumo, nombre, papel_ambito, metricas, cuello_botella {severidad, persistencia, relevancia_valor, PCB, material, indicadores, senal_resolucion, calc_id}, atractivo {AE, desglose, calc_id}}], eslabon_critico, rec_id, data_cutoff, caduca}` (VC-DESG-001, VC-BOT-001) |
| `radar_emergentes` | Lista | No (V2.1) | `{emg_id, eslabon_id, nombre, tipo, via_exposicion, PEM, calc_id, rec_id, fecha, caduca}` (EMG-PEM-001) |
| `paradas` | Lista | No (V2.1) | `{rec_id, pet_id, puerta, sugerencia, motivos, fecha}` (informe de parada) |
| `seguimientos` | Lista | No (V2.1) | `{seg_id, ciclo_id, fecha, semaforo, dimensiones_actualizadas}` |
| `estado` | Enumerado | Sí | Sección 5 |

### 4.2 Versión de dimensión

| Campo | Valores / formato |
|---|---|
| `version` | `MKT-B-NNNN-Dk-vN` |
| `dimension` | D1…D12 |
| `rec_id` / `pet_id` | Origen (entregado) |
| `profundidad_tratada` | P0…P3 (o «excluida con motivo») |
| `resumen` | Conclusión de la dimensión con etiquetas epistémicas |
| `clm_ids` / `calc_ids` / `dat_ids` | Remisiones a F2 y RC |
| `confianza` | `{nivel, factores}` |
| `lagunas` | Lista |
| `data_cutoff` / `caduca` | Fechas (regla 3) |
| `estado` | VIGENTE · CADUCADA · SUSTITUIDA · NO_REUTILIZABLE (evidencia retirada o refutada) |
| `usos` | `{pet_id, fecha, gc0 REUTILIZADA·DELTA·DESCARTADA, reverificacion OK·FALLIDA, motivo}` (append-only) |
| `actualizado_por_ciclo` | CIC-B del archivo F11 si la versión procede de un ciclo de seguimiento (V2.1) |
| `supersedes` | Versión anterior |

### 4.3 Versión de universo

`version` (`MKT-B-NNNN-<tipo>-vN`), `tipo_activo`, `playbook`, `fecha_universo`, `fuentes` (HT-11, F9), `tamano_bruto`, `filtros_aplicados` (PC1 del playbook y marco 2.7 con su versión), `exclusiones_por_motivo`, `miembros_ref` (CALC-B del universo completo con métricas), `bajas_posteriores_conocidas` (`{instrumento, fecha, motivo deslistado·fusión·suspensión}`), `marco_invertibilidad` (el usado), `caduca` (1 mes), `estado`, `usos`.

### 4.4 Ficha de régimen (RGM-B)

| Campo | Valores / formato |
|---|---|
| `rgm_id` | `RGM-B-AAAA-NNNN` |
| `alcance` | Ámbito (MKT-B) o régimen macro y financiero general |
| `variables` | `{variable, estado, tendencia, dato (DAT-B o CALC-B), fecha}` |
| `variables_dominantes` | Lista |
| `relaciones_estables` | `{relacion, naturaleza HISTORICA_OBSERVADA (ventana)·CAUSAL_DEMOSTRADA (mecanismo), evidencia}` |
| `estado_confianza` | definido · mixto · incierto · en_transicion |
| `criterio_cambio_estructural` | Qué observación distinguiría un cambio de régimen de una fluctuación |
| `rec_id` de origen / `data_cutoff` / `caduca` | — |
| `estado` / `supersedes` | VIGENTE · CADUCADA · SUSTITUIDA |

## 5. Estados y transiciones

| Objeto | Transiciones |
|---|---|
| MKT-B | ACTIVA (al menos una dimensión vigente) ↔ LATENTE (todas caducadas; consultable como historia) |
| Versión de dimensión o de universo | VIGENTE → CADUCADA (HT-05, por fecha) · SUSTITUIDA (versión nueva) · NO_REUTILIZABLE (evidencia retirada o refutada; re-verificación fallida) |
| RGM-B | VIGENTE → CADUCADA · SUSTITUIDA |

La tarea de fondo del Director (7.6) solo ejecuta VIGENTE → CADUCADA; ninguna otra transición ocurre sin una petición entregada, un informe de parada entregado o un ciclo de seguimiento entregado (V2.1).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Por ámbito y solapamiento | `mkt_id`, `relaciones`, `tipo_objeto`, `region` | GC0 en F0 |
| Dimensiones vigentes | `dimensiones.*.estado` = VIGENTE, `caduca` | Reutilización; estimación (reduce el grafo) |
| Universos vigentes | `universos.*.estado`, `fecha_universo` | Encargo de selección (`universo_F6`) |
| Regímenes vigentes | `RGM-B.estado` | F1 y F3 |
| Caducidades próximas | `caduca` | HT-05; respuestas N0 (`caducidades_afectadas`) |
| Por REC-B | `historial_analisis.rec_id` | Evaluación; historial de aciertos por ámbito |
| Por eslabón y cuello (V2.1) | `desglose_cadena.eslabones.eslabon_id`, `PCB`, `material` | Reutilización del desglose; PV3 |
| Emergentes (V2.1) | `radar_emergentes.emg_id`, `via_exposicion` | Radar de AG-B24; vigilancia pre-salida |
| Paradas y ciclos (V2.1) | `paradas.puerta`, `seguimientos.seg_id` | PV1 (BIBLIOTECA_DESCARTAR); ciclos N1-SEG |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"version":"MKT-B-0012-D9-v3","dimension":"D9","rec_id":"REC-B-2026-0007","pet_id":"PET-B-2026-0007","profundidad_tratada":"P2",
 "resumen":"[INTERPRETACIÓN] El DCF inverso del agregado descuenta un crecimiento de ingresos del 14 % anual a 5 años frente a un 9–12 % plausible según D2/D8",
 "clm_ids":["CLM-B-2026-0210"],"calc_ids":["CALC-B-2026-0133"],"dat_ids":["DAT-B-2026-0031"],"confianza":{"nivel":"media","factores":["dispersión de márgenes entre eslabones","consenso de terceros como insumo"]},
 "lagunas":["sin desglose de márgenes del eslabón de sustratos"],"data_cutoff":"2026-11-07","caduca":"2026-12-07","estado":"VIGENTE",
 "usos":[{"pet_id":"PET-B-2026-0015","fecha":"2026-11-20","gc0":"DELTA","reverificacion":"OK","motivo":"índice del ámbito +1,7 σ desde la ficha: cambio material en D9"}],
 "supersedes":"MKT-B-0012-D9-v2"}
```
