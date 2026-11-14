# T-117 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude) · **Ronda:** r01 · 2026-11-13
- Orden de lectura: `README.md` del ticket → `diseno_v6.py`, `por_defecto.yaml` y `test_t117_gc1.py` → mis ataques → al final `analisis-tecnico.md` y `pruebas.md`.
- Lo que digo «ejecutado» lo he ejecutado yo en mi copia; lo que digo «leído» es deducción de lectura.

## Ronda r01

### Reproducción desde limpio

Copia propia (`git worktree` en `2ff0630`, HEAD separado; lo de los tres tickets es `git diff ab95d41 HEAD`). Python del `.venv` del repositorio. Máquina compartida con otros cuatro trabajos: los tiempos son orientativos.

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite del Bloque A, una vez | `cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider` | **3811 passed in 684 s**; el árbol queda limpio |
| Pruebas del ticket | `python -m pytest -q tests/test_t117_gc1.py` | 43 passed |
| Corpus, refs, secretos, NFC | `tools/corpus_integridad.py`, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | los cuatro en verde (695 archivos del corpus) |
| ruff (como el gate) | sobre los tres `11_Ejecutor`, `--output-format=concise \| wc -l` | 2902 (cuota 2902) |
| mypy (como el gate) | `mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` | 109 (cuota 109) |
| Único código de producción tocado | `git diff --stat ab95d41 HEAD -- bloque_a/11_Ejecutor/bloque_a` | solo `diseno_v6.py` (+25 −6); además `config/por_defecto.yaml` |

No ejecuté `tools/check_all.sh` completo (indicación del encargo: máquina compartida). El «gate 12/12» de CA-6 queda comprobado por partes; el implementador tampoco lo ha pasado todavía (`pruebas.md`: «lo pasa `commit_limpio.sh` al hacer el commit»). **Es condición de cierre.**

### Mis scripts (`revisores/`)

| Script | Qué hace | Resultado |
| --- | --- | --- |
| `r01_01_medida_inc_t117_01.py` | Repite la medida de INC-T117-01 con `Bloque.senales_clase`: mi muestra (15 viernes cada 3 semanas desde el 15-08-2025) y la del implementador (`17 2025-07-04 4W-FRI`) | Ver «La medida» |
| `r01_02_ataques_gc1.py` | Límites del umbral, señal no finita o de tipo raro, recuento de familias ausente, negativo o no entero, 34 configuraciones, y el umbral que recibe el Analista | Ver hallazgos H-01 a H-03 y H-06 |
| `r01_03_ciclo_huella.py` + `r01_04_comparar_huellas.py` | Huella (SHA-256 de cada fichero del estado y de los entregables, y del resultado) de un ciclo semanal de los doce tipos, en `ab95d41` y en HEAD, con `PYTHONHASHSEED` 1 y 7 | V5: idéntico antes y después; V6: determinista |
| `r01_05_mutantes_gc1.py` | 30 mutantes de `gc1()`, de `validar()` y del YAML contra `test_t117_gc1.py` | 26 muertos, 4 vivos (uno equivalente). G08 y G30 siguen vivos también contra `test_t101_v6.py`, `test_t102_filtro.py` y `test_t117_gc1.py` juntos (376 passed) |
| `r01_06_registro_decisiones.py` | Muestreo del registro de decisiones contra `por_defecto.yaml` (31 claves) | 31 de 31: la clave existe y vale lo que dice |

Órdenes (desde `bloque_a/11_Ejecutor` salvo la última, desde la raíz; `R=../../.docs/tickets/T-117/revisores`):

```bash
python $R/r01_01_medida_inc_t117_01.py 15                      # mi muestra
python $R/r01_01_medida_inc_t117_01.py 17 2025-07-04 4W-FRI    # la muestra de INC-T117-01
python $R/r01_02_ataques_gc1.py
PYTHONHASHSEED=1 python $R/r01_03_ciclo_huella.py v5 <carpeta fija del scratchpad> > head.json   # y lo mismo en un árbol de ab95d41
python $R/r01_04_comparar_huellas.py head.json head_otra_semilla.json base.json
python .docs/tickets/T-117/revisores/r01_05_mutantes_gc1.py <copia desechable>
python .docs/tickets/T-117/revisores/r01_06_registro_decisiones.py
```

### Criterios de aceptación

| Criterio | Cumple | Evidencia (ejecutada salvo que diga otra cosa) |
| --- | --- | --- |
| CA-1 · valores por defecto decididos; umbral general y diseño por defecto sin cambios | sí | `r01_06`: `umbral_por_perfil` = {RF, MON, TCV: 0,65}, `familias_min` = 2, `senal_por_perfil` = compuesta en los doce, `seleccion.umbral_senal_gc1` = 0,75, `diseno` = v5. Mutantes G25 a G29 (cambiar cualquiera de esos valores en el YAML) mueren. **V5 antes y después:** un ciclo semanal de los doce tipos en `ab95d41` y en HEAD deja los 16 ficheros (F1 a F5, F10, HA, RC, caché, contadores, sellos y los tres entregables) **idénticos byte a byte**; el resultado devuelto solo difiere en `consumo.por_agente.*.uc` en la cuarta decimal, igual que entre dos ejecuciones del mismo código (ruido previo, ver «Fuera del ticket») |
| CA-2 · cada tipo usa su umbral; el borde pasa y un valor inmediatamente inferior no | sí | `r01_02` §1: 0,65 y `0.6500000000000001` pasan en RF, `0.6499999999999999` no; 0,75 pasa en RV y `0.7499999999999999` no. Mutantes G01 (`>` por `>=`), G02 (ignorar el umbral del tipo) y G10 (registrar el general) mueren. En el ciclo, el registro lleva 0,65 en RF, MON y TCV y 0,75 en los otros nueve |
| CA-3 · concordancia con la señal compuesta; sin recuento no se descarta; con otra señal no se exige; con `familias_min: 0` no se exige | sí | `r01_02` §3 y §5; mutantes G03 a G06, G11, G23 y G24 mueren. Salvedad en H-02: «sin recuento» incluye cualquier recuento que no sea un `int` de Python |
| CA-4 · una configuración no válida se rechaza al crear el Bloque y una válida se acepta | sí, con salvedad (H-03) | `r01_02` §5: 21 inválidas rechazadas con `ValueError` y sin excepciones no controladas; mutantes G12 a G14 y G16 a G23 mueren. Salvedad: `umbral_por_perfil` igual a `0`, `""`, `[]` o `False` se acepta en silencio |
| CA-5 · en un ciclo V6 el registro de cobertura lleva el umbral de cada tipo | sí | Ciclo V6 de los doce tipos (`r01_03`): `COBERTURA.clases[*].gc1.umbral` = 0,65 en RF, MON y TCV; 0,75 en los demás |
| CA-6 · pruebas de T-101, T-102, T-113 y T-88 en verde; gate 12/12; cuotas sin subir | sí por partes; gate entero pendiente | Suite completa 3811 passed; ruff 2902 y mypy 109, iguales a la cuota; gates ligeros en verde. `tools/check_all.sh` no ejecutado por nadie todavía |

### Lo que ataqué y aguantó

- **Señal no finita o de tipo raro** (`nan`, `inf`, `-inf`, `None`, booleano, texto, lista, diccionario, `Decimal`): ninguna excepción; el ámbito llega marcado `SIN_SENAL_MEDIBLE`, como ya hacía T-101. Ninguno entra como `PASA`.
- **Familias negativas** (−1, −5): descartado, con su motivo. **Familias 4** (más de las que hay): pasa.
- **Tope de candidatas:** con más ámbitos sobre el umbral que `max_candidatas`, los de una sola familia no ocupan plaza (pasan 8 con dos familias). El orden de entrada no cambia el registro y la llamada es idempotente.
- **Determinismo de la V6:** dos ciclos de los doce tipos con `PYTHONHASHSEED` 1 y 7 dan los 16 ficheros y el resultado idénticos.
- **Efecto real del cambio en la V6** (ciclo de ejemplo, `ab95d41` → HEAD): RF pasa de ningún ámbito a `EMB`; TCV de uno a dos (`^VIX`); MON sigue en ninguno. El top de TCV pasa de 1 a 3 opciones. Los otros nueve tipos no cambian.
- **V5 con `v6.gc1` inválido:** el Bloque se crea; la sección solo se valida y se usa con `diseno: v6` (leído y ejecutado).

### La medida de INC-T117-01, repetida

Ámbitos por fecha que pasan GC1 con los datos de ejemplo. «Su muestra» son las 17 fechas del implementador, que reproduje; «mi muestra» son 15 fechas distintas.

| Tipo | Ámbitos | ≥ 0,75 (su muestra · la mía) | ≥ 0,65 y dos familias (su muestra · la mía) | Tendencia neutra (su muestra · la mía) |
| --- | --- | --- | --- | --- |
| RV | 7 | 1,47 · 1,73 | 3,06 · 3,13 | 34 % · 35 % |
| RF | 8 | **0,82** · 1,00 | **2,06** · 2,20 | 48 % · 43 % |
| DIV | 6 | 1,65 · 1,80 | 2,29 · 2,47 | 31 % · 28 % |
| MP | 6 | 1,88 · 2,13 | 2,94 · 3,00 | 45 % · 42 % |
| IDX | 6 | 1,94 · 2,40 | 3,06 · 3,47 | 35 % · 32 % |
| FON | 4 | 1,53 · 1,73 | 1,71 · 1,73 | 31 % · 27 % |
| DER | 3 | 0,71 · 0,73 | 0,88 · 0,93 | 45 % · 60 % |
| INM | 3 | 0,76 · 0,73 | 1,06 · 0,93 | 43 % · 44 % |
| CRI | 3 | 0,59 · 0,73 | 1,59 · 1,87 | 24 % · 16 % |
| ALT | 2 | 0,88 · 1,00 | 0,88 · 1,00 | 15 % · 3 % |
| MON | 3 | **0,47** · 0,60 | **1,12** · 1,27 | **18 %** · 18 % |
| TCV | 6 | **0,94** · 1,07 | **2,06** · 2,27 | 49 % · 57 % |

- **Las cifras de la incidencia son ciertas.** Con su muestra obtengo 0,8 / 0,5 / 0,9 en RF, MON y TCV con 0,75; 1,5 a 1,9 en RV, DIV, MP e IDX; 2,1 / 1,1 / 2,1 con 0,65 y dos familias; DER pasa de 0,7 a 0,9 («apenas cambia»); «sin tendencia» en 65 de 136 observaciones de RF y 50 de 102 de TCV. Con mi muestra las cifras suben un poco y el orden entre tipos se mantiene.
- **Con 0,75 la concordancia no cambia nada** en ninguna de las dos muestras (columna «≥ 0,75» igual a «≥ 0,75 y dos familias» en los doce tipos); con 0,65 sí recorta (ALT: de 1,7 a 0,9; DIV: de 3,0 a 2,3).
- **Lo que la medida no sostiene** (H-04): la causa que se da para MON y la frase «frente a 1,5 a 1,9 en los demás» del YAML.

**Juicio sobre la decisión.** Bajar a 0,65 solo en RF, MON y TCV y exigir dos familias está razonado y es prudente: son los tres tipos con menor fracción de su universo sobre 0,75 (RF 10 %, MON 16 %, TCV 16 %, frente a 20 % a 44 % en los demás), con 0,65 quedan cerca del resto, la concordancia compensa la bajada y el tope de candidatas no cambia. No bajar DER, INM, CRI y ALT (dos o tres ámbitos) es defendible y el análisis técnico lo dice; la incidencia solo explica DER. Está bien declarada como provisional: `[PROPUESTO]` en el YAML y en INC-T117-01, fila propia en la deuda y tres filas en el registro de decisiones, con el límite (datos sintéticos, universo de 2 a 8 ámbitos) y el camino de recalibración (falsos negativos de la exploración). Solo afecta a la V6, que no es el diseño por defecto.

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `python $R/r01_02_ataques_gc1.py`, apartado 7 (ciclo V6 de RF y RV, espiando el CT-06). Código: `orquestacion.py:790` | Esperado: el Analista recibe el umbral que aplicó GC1 por código. Obtenido: en RF (y MON, TCV) el CT-06 lleva `umbral_senal_gc1: 0.75` mientras el registro dice `umbral: 0.65` y el ámbito viaja marcado `PASA` («su señal llega al umbral», `NOTA_GC1`) con señal de 0,65 a 0,75. Con el modelo real, el Analista puede descartar en su cribado justo los ámbitos que el cambio deja pasar; el cliente simulado no lo ve porque usa su propio umbral fijo | Con la V6 y GC1 por código, enviar en el CT-06 el umbral del tipo (el mismo valor que va al registro), y una prueba que compare los dos | abierto |
| H-02 | baja | `r01_02`, apartado 3 | Esperado: un recuento de familias menor que dos descarta, sea cual sea su tipo numérico, o un tipo anómalo falla cerrado. Obtenido: `1.0`, `0.0`, `1.9`, `numpy.int64(1)`, `numpy.int32(1)`, `Decimal(1)`, `True` y `False` **pasan** (se tratan como «sin recuento»). Hoy `senales_clase` da un `int` de Python y no se alcanza; si el recuento llegara de pandas o numpy, la comprobación dejaría de actuar en silencio. Sin prueba (mutante G07 vivo) | Aceptar `numbers.Integral` (y floats enteros), o tratar un recuento presente y de tipo no entero como descarte; prueba con `numpy.int64` | abierto |
| H-03 | baja | `r01_02`, apartado 5: `umbral_por_perfil` = `0`, `""`, `[]`, `False` | Esperado: rechazo al crear el Bloque (no es un diccionario), como con `[0.6]`, `"abc"` o `0.65`. Obtenido: se acepta y todos los tipos usan el umbral general sin aviso (`… or {}` oculta el tipo erróneo, en `validar()` y en `gc1()`) | Validar con `is None` en vez de `or {}`; añadir los cuatro casos a `test_una_configuracion_invalida_se_rechaza` | abierto |
| H-04 | baja | `r01_01` con `17 2025-07-04 4W-FRI`; comentario de `por_defecto.yaml` sobre `umbral_por_perfil`, INC-T117-01 y `analisis-tecnico.md` | Esperado: la causa y la comparación que justifican los valores coinciden con la medida. Obtenido: (a) «la tendencia suele quedar neutra» vale para RF (48 %) y TCV (49 %), pero no para MON (18 %, el segundo más bajo de los doce) y tampoco distingue a RF de MP (45 %) o INM (43 %); (b) el YAML dice «frente a 1,5 a 1,9 en los demás», y DER (0,71), INM (0,76), CRI (0,59) y ALT (0,88) también están por debajo de 1 (la incidencia lo dice bien: «en RV, DIV, MP e IDX») | Corregir las dos frases: en MON la causa es otra (tres ámbitos y poca señal de momento o valoración), y la comparación es con RV, DIV, MP e IDX; añadir a la incidencia por qué no se bajan INM, CRI y ALT (ya está en el análisis técnico) | abierto |
| H-05 | baja | `python .docs/tickets/T-117/revisores/r01_05_mutantes_gc1.py <copia>`: vivos G08 y G30 (y G07, de H-02; G15 es equivalente: sin `isfinite`, `nan` e `inf` siguen rechazados por el rango). Leer `test_en_el_diseno_v5_nada_cambia` | Tres huecos de pruebas: (a) `test_en_el_diseno_v5_nada_cambia` solo afirma que `b.v6` es falso y que el umbral general es 0,75: no compara nada del V5 (lo he comparado yo, y no cambia); (b) G08: aplicar el tope de candidatas antes del filtro de familias no rompe ninguna prueba; (c) G30: comparar con un 2 fijo en vez de con `familias_min` no rompe ninguna prueba (solo se prueban los valores 0 y 2; 1 y 3 se aceptan pero no se ejercitan) | Una prueba con más ámbitos sobre el umbral que `max_candidatas` y algunos de una familia; una con `familias_min` 1 y 3; y que la prueba del V5 compare el registro de un ciclo o se quite el nombre | abierto |
| H-06 | baja | `r01_02`, apartado 1: señal 0,64999 en RF | El motivo del descarte queda «senal_compuesta 0.65 < 0.65» (redondeo a dos decimales): con umbrales por tipo el borde es más frecuente y el motivo parece contradictorio | Escribir la señal con cuatro decimales, como el campo `senal` del mismo descarte | abierto |

Ninguno crítico ni alto. H-01 es el que conviene corregir antes de usar la V6 con el modelo real; si no se corrige ahora, pasa a la deuda con su ID junto con H-02 a H-06.

### Invariantes (punto 4 de la skill)

- Ruta determinista sin LLM: `gc1()` y `validar()` son código puro. ✔ (leído)
- Números de configuración: los tres valores nuevos están en `por_defecto.yaml`. `FAMILIAS_SENAL_COMPUESTA = 3` es el número de familias que calcula `senales_clase` (estructural). El 0,6 que define «familia concordante» está escrito en `orquestacion.py:400` desde antes de este ticket: queda fuera de su alcance, pero el recuento que ahora decide depende de él (apuntarlo en la deuda).
- Los controles no se relajan solos: bajar el umbral de tres tipos relaja un filtro de selección «Calibrable» del Anexo A; lo decide el agente bajo la regla del operador del 13-11-2026, queda `[PROPUESTO]`, en la deuda y en el registro, y solo en la V6. La concordancia endurece. ✔
- Falla cerrado y valida antes de mutar: la validación corre al crear el Bloque. Dos excepciones menores: H-02 y H-03.
- Decisiones del operador: ninguna en silencio. ✔ Secretos y datos personales: `tools/secrets_scan.py` en verde. ✔
- Documentación: README del ticket, INC-T117-01, fila T-117 de la deuda (EN QA) y registro de decisiones al día. `pruebas.md` deja el gate para el commit.

### Fuera del ticket (para la deuda, no cuentan en el veredicto)

- El resultado que devuelve `Bloque.ciclo()` en el V5 no es idéntico entre dos ejecuciones iguales: `consumo.por_agente.*.uc` cambia en la cuarta decimal (suma en hilos) y `consumo.latencia_s` es tiempo real. Los archivos sí son idénticos. Ya pasaba en `ab95d41`.
- `cache_resultados.jsonl` se escribe en un orden que depende de los hilos (mismo contenido, distinto orden de líneas).
- Una señal `numpy.float32` o `numpy.int64` se trata como «sin señal medible» (comprobación de tipo de T-101).

## Veredicto

**APTO** · Los seis criterios se cumplen (CA-4 con la salvedad de H-03; CA-6 por partes) y no queda ningún hallazgo crítico ni alto. Quedan abiertos uno medio (H-01) y cinco bajos (H-02 a H-06), que se corrigen o pasan a la deuda con su ID. **Condición de cierre:** `./tools/check_all.sh` 12/12 en el commit, que en esta ronda no ha ejecutado nadie.
