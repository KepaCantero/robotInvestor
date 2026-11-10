# Informe de revisión independiente — V0.62 (pieza 3 del kit 2: robustez de la infraestructura T-03)

**Revisor:** GLM (conversación independiente, sin el historial de la pieza; 9 de noviembre de 2026)
**Alcance:** `pruebas/pruebas_robustez_t03.py` (NUEVO), cambios en `LEEME.md`, `entrega_glm/V0.62/*` y la
promesa de que no cambia nada en `validador/` ni en el Orquestador.
**Método:** verificación contra el código real (no contra lo que declara la entrega): lote completo de 52
baterías ejecutado por el revisor, la batería nueva corrida dos veces y comparada byte a byte, recuentos
propios, contraste de cada `esperados` de la batería con lo que los módulos T-03 devuelven de verdad
(lectura de `persistencia.py`, `diario.py`, `migraciones.py`, `reloj.py` y `rotacion.py`) y **cinco sondas
adversariales propias** (`sondas_revisor_v062.py`, adjuntas): un barrido de 60 semillas × 24 casos por
objetivo (1.440 casos por objetivo) para medir la fragilidad de las expectativas, casos construidos a mano
sin azar, y las dos sondas de no-vacuidad repetidas por el revisor sobre copias.

**Resultado: 4 hallazgos (1 medio, 3 bajos), ninguno de producto.** Los módulos T-03 cumplen las cuatro
promesas en todo lo ejecutado y la batería es determinista, no-vacua y fiel al diseño en 36 de sus 39
comprobaciones. El hallazgo medio es de la batería: **cuatro objetivos tienen `esperados` más estrechos que
el contrato real del módulo** (un `PE-03` alcanzable y no admitido), de modo que la entrega pasa con la
semilla 20261111 después de una tirada que tenía en torno a **2 de cada 3 de probabilidades de salir mal
solo por el objetivo del diario**. Es la misma clase de defecto que el auto-repaso (d) del Documento 0
corrigió en tres sitios antes de entregar; quedaron un cuarto y un quinto. Detalle abajo.

---

## 1. Lo verificado en verde (evidencia de la propia ejecución del revisor)

1. **Lote completo en verde:** 52 baterías ejecutadas por el revisor (Python 3.12.16), todas terminan en
   «TODAS LAS PRUEBAS PASAN», sin una línea FALLA; los textos de resultado coinciden uno a uno con
   `salida_pruebas.txt` (0 diferencias, comparación automática).
2. **La batería nueva:** **39 comprobaciones** (claim: 39), todas OK; **dos ejecuciones con salida idéntica
   byte a byte** (`diff` vacío) y ~11,6–12,2 s de reloj (claim: ~11 s). Semilla propia
   `random.Random(20261111)`, nunca el global (verificado en el código).
3. **Recuentos:** 870 casos = 240 + 180 + 150 + 150 + 150, con rotación exacta (40×6, 60×3, 30×5 en los
   tres bloques); los nombres de las comprobaciones citan 200/120/120 casos de texto y cuadran con la
   aritmética (240−40 instantes, 180−60 argumentos, 150−30 ficheros).
4. **Excepciones por diseño, verificadas contra los módulos:** la firma se comprueba ANTES que la huella
   (`persistencia.py:324-339`), así que un firmado tocado da PE-06 y el `esperados {PE-01, PE-06}` es
   correcto; `clave_valida` rechaza la clave de 32 ceros (`persistencia.py:92-95`: menos de 8 valores
   distintos), así que la prueba de la bóveda con `bytes(32)` es real; la envoltura O-00 existe
   (`diario.py:167`); `degradar_por_reloj` solo admite códigos RL-01/02/03/05 (RL-06) y `nuevo()` deja
   `ultimo_ahora` fijado por el sello inicial, así que RL-07 es inalcanzable en los casos «incidente»;
   `rearmar` sin bloqueo → RL-06; `comprobar_estado` con `ultimo_ahora` imposible → RL-02 (el conjunto
   {OK, RL-02} es exacto); `contrastar` con referencia imposible → RL-06 sin bloquear y desfasada válida →
   RL-03 con bloqueo; `camino` con registro roto → None (probado).
5. **Sin cambios de esquema ni de configuración:** `version_config` = CFG-0.11.0; el esquema del código
   (`esquema_actual()` = `0a18459e…`) está en `esquemas_codigo.json` y `pruebas_migraciones_t03.py` pasa en
   el lote sin registrar nada.
6. **LEEME actualizado en los cinco puntos declarados:** cabecera («…y robustez de la infraestructura
   T-03 — V0.62»), párrafo de fecha (línea 3), fila de la tabla (línea 42), línea de ejecución (línea 185)
   y punto «Comprobado en la robustez de la infraestructura T-03» (línea 201), con recuentos correctos.
7. **No-vacuidad, confirmada por el revisor en copias:** con la cadena de hashes del diario desactivada,
   la batería FALLA **exactamente** en las dos comprobaciones declaradas (S3: se cuela una línea de punto
   tocado → OK, y la última línea tocada responde DI-04). Con la huella desactivada la batería también
   muere — pero en CUATRO comprobaciones, no en dos (hallazgo 2).

## 2. Hallazgos

| # | Gravedad | Hallazgo | Corrección propuesta | Regresión |
| --- | --- | --- | --- | --- |
| 1 | **media** | **Cuatro `esperados` más estrechos que el contrato real del módulo: la batería puede fallar en falso con otra semilla.** Los cuatro objetivos que mutan el documento ENTERO (`_mutar_doc` sin `dentro_estado`, y los tres que llaman a `_mutar_en_sitio` sobre la raíz) pueden caer en la cabecera, y una cabecera con `formato` cambiado por otro texto (o `version_config`) da **PE-03** (`persistencia.py:315-316` y `:355-356`), que no está admitido: `diario_estado` admite {PE-01, PE-02, PE-06} (`pruebas_robustez_t03.py:334`), `migraciones_texto` {OK, PE-01, PE-02} (:403), `rotacion_texto` {PE-01, PE-02, PE-06, CL-02} (:586) y `rotacion_sin_firmar` {PE-01, PE-02, CL-02} (:610). Medido con 60 semillas × 24 casos por objetivo (sonda S1): **PE-03 aparece en `diario_estado` 19–27 veces de 1.440 (≈1,3–1,9 % por caso) → entre el 55 % y el 68 % de las semillas darían un fallo falso con sus 60 casos; en `rotacion_sin_firmar`, 5–10/1.440 (≈10–19 %); en `migraciones_texto`, ~2 %; y en `rotacion_texto` es alcanzable por construcción aunque no salió en el muestreo**. Los cuatro casos reproducidos SIN azar en la sonda S1b. La entrega pasa porque la secuencia compartida del rng de 20261111 no sorteó esas rutas: la batería quedó en verde tras una tirada con ~2/3 de probabilidad de salir mal | Añadir PE-03 a los `esperados` de los cuatro objetivos (y por la misma razón, revisar PE-04/PE-08); alternativa más fina: que los objetivos de «estado» muten SOLO dentro del estado y los de «cabecera» solo fuera, con esperados separados — es lo que el auto-repaso (d) ya hizo en tres sitios, aquí faltó el resto | `r01_los_esperados_cubren_todo_lo_que_el_modulo_puede_responder`: para cada objetivo, un barrido corto con N semillas (p. ej. 25) cuyo conjunto de códigos observados debe estar ⊆ `esperados` (con la batería actual, r01 falla en los cuatro objetivos) |
| 2 | **baja** | **La sonda de no-vacuidad de la huella no falla «exactamente» en las dos comprobaciones declaradas, sino en cuatro.** Con `_huella` desactivado en `persistencia.py` (sonda S2, copia), además de `persistencia_falla_cerrado_con_la_regla_correcta_en_240_casos` y `persistencia_toda_mutacion_del_estado…_nunca_ok` (las declaradas) también caen `diario_el_estado_tocado_no_abre_PE01_PE02_o_PE06` (el estado tocado carga y el punto ya no cuadra: DI-02/O-13) y `rotacion_un_texto_mutado_no_se_rota_y_las_claves_o_metadatos_imposibles_fallan_cerrado` (el caso `sin_firmar` llega a responder **OK o PE-04** — que es exactamente lo que la huella impide). Contradice el «exactamente» con nombres de `revision.md`, el «exactamente en sus comprobaciones de PE-02» de Documento 0 §5 y el de `notas_briefing.md`; el LEEME («falla en las comprobaciones de PE-02») sí aguanta. La no-vacuidad sigue demostrada — y las dos caídas extra son más evidencia del hallazgo 1 — pero la precisión declarada es falsa; la sonda del diario (S3) sí es exacta | Ajustar las tres frases (o rehacer la sonda aislando los dos objetivos de persistencia, p. ej. con una semilla dedicada) | Ninguna (documental); r01 vigila el fondo |
| 3 | **baja** | **Franquicias muertas en los `esperados`, descritas en los documentos como si fueran alcanzables.** (a) `rotacion_claves` admite PE-07 (:591), pero `_previas` (`rotacion.py:66-77`) devuelve CL-01 para toda clave inválida ANTES de que `pe.cargar` pueda dar PE-07: los cuatro combos de la sonda S1b dan CL-01. (b) La franquicia OK de la «ÚLTIMA línea mutada» del diario (:320, «regla del corte» de Documento 0 §2.2) es inalcanzable: la batería escribe siempre el salto final, así que `incompleta=False` y la última línea mutada es DI-02 siempre (30/30 en S1c); el OK solo llegaría con un fichero SIN salto final, caso que la batería no construye aquí (lo cubre su caso fijo de línea cortada). (c) Menores, del mismo tipo: MG-02 en `migraciones_registro`, PE-02/CL-02 en `rotacion_texto`/`sin_firmar` y PE-06 en `diario_estado` son inalcanzables con el generador actual. Ninguno causa fallos falsos (son permisivos), pero Documento 0 §2.2 los cita como expectativas activas | Retirar las franquicias muertas o anotarlas como permisivas en la cabecera de la batería y en Documento 0 §2.2 | Ninguna (documental) |
| 4 | **baja** | **Tres verificaciones declaradas no son reproducibles desde el ZIP:** «no se toca el Orquestador ni ningún módulo de `validador/` (diff por fichero frente al ZIP de V0.61)», «sin borrar ni debilitar ninguna prueba antigua (regla 7)» y «`Deuda_tecnica.md` queda intacto» exigen comparar con el estado anterior, que no viaja; tampoco viaja `corre_baterias.py`, citado en la cabecera de `salida_pruebas.txt`. Todo lo que SÍ es verificable desde el ZIP salió en verde (§1). (Heredado: `Deuda_tecnica.md` ya no viajaba en V0.60/V0.61 — hallazgo 6 de V0.61 —; `notas_deuda.md` declara ahora el arreglo «viaja resumido», pero Documento 0 §5 no recuerda dónde está el contenido) | Incluir un manifiesto de hashes SHA-256 de los ficheros heredados (o el ZIP anterior), y `corre_baterias.py`; citar en Documento 0 §5 que el contenido de la deuda viaja en `notas_deuda.md` | Ninguna (documental) |

**Ningún hallazgo es de producto:** ninguna conducta de `validador/` ni del Orquestador cambia; en todos
los barridos y casos construidos los cinco módulos respondieron con códigos previstos por SU contrato
(PE-03 ante una cabecera mentirosa es exactamente lo que `verificar` documenta) y ninguna promesa de las
cuatro quedó refutada. Los hallazgos 1–3 son de la batería (expectativas), el 4 es de la entrega.

## 3. Sondas del revisor (`sondas_revisor_v062.py`)

| Sonda | Qué prueba | Resultado |
| --- | --- | --- |
| S1 | Barrido de 60 semillas × 24 casos por objetivo (1.440 por objetivo), mismos bucles que la batería | PE-03 fuera de `esperados` en `diario_estado` (19–27/1.440 entre corridas), `rotacion_sin_firmar` (5–10/1.440) y `migraciones_texto` (0–2/1.440); `persistencia_*` y `migraciones_rehecho` limpios |
| S1b | Casos construidos a mano (sin azar) | `formato="x"` en la cabecera → **PE-03 en los cuatro objetivos** (los cuatro fuera de `esperados`); `rotacion_claves` → CL-01 en los cuatro combos (PE-07 inalcanzable); última línea del diario mutada → DI-02 30/30 (franquicia OK inalcanzable) |
| S2 | Huella desactivada en copia de `persistencia.py` | La batería FALLA en **4** comprobaciones (las 2 declaradas + diario estado + rotación sin_firmar) — la entrega declara «exactamente» 2 |
| S3 | Cadena de hashes desactivada en copia de `diario.py` | La batería FALLA **exactamente en las 2 declaradas** (línea 12/19 → OK: un punto tocado se cuela; última línea → DI-04) |
| S5 | Conteos auxiliares | 39 comprobaciones (claim ✓); 870 casos por constantes y rotación (claim ✓); `version_config` CFG-0.11.0 (claim ✓); esquema del código presente en `esquemas_codigo.json` (claim ✓) |

## 4. Observaciones (sin corrección exigida)

1. `cargar_de` y `verificar` se ejercitan de forma transitiva o ligera (`cargar_de` vía `di.abrir`;
   `verificar` en la foto de no-mutar y en el anidado de 500 niveles), aunque la cabecera de la batería
   las lista junto a las directamente fuzzadas. Como `cargar` las envuelve, la cobertura real es buena;
   conviene saberlo al leer la cabecera.
2. Los casos «estado» del diario restauran el fichero de estado pero no el de diario, así que ese caso
   prueba en realidad (estado mutado + diario dejado por el caso «línea» anterior, también mutado). Con
   los módulos en su contrato no cambia nada (el estado falla antes de leer el diario), pero complica
   razonar sondas — es la razón de la tercera caída de S2 —. Restaurar ambos ficheros también aquí.
3. La frecuencia del hallazgo 1 depende del tamaño del estado (más atributos → menos probabilidad por
   caso de caer en la cabecera). Con el estado actual (~500 nodos) el riesgo del objetivo del diario es
   alto; si el estado crece, bajará — pero r01 lo vigila sin depender de eso.
4. La promesa «la batería entera, la misma salida byte a byte» es verificable solo con la semilla y el
   código congelados: cualquier edición de la batería (p. ej. al corregir el hallazgo 1) cambiará la
   salida — regenerar entonces `salida_pruebas.txt` y la frase de determinismo.

## 5. Resultado

Un hallazgo medio (1: cuatro `esperados` más estrechos que el contrato real, con ~2/3 de probabilidad de
fallo falso por semilla en el objetivo del diario — la entrega pasó por la tirada buena de la semilla
20261111) y tres bajos (2: la sonda de no-vacuidad de la huella cae en 4 comprobaciones, no en las 2
declaradas; 3: franquicias muertas descritas como activas; 4: verificaciones no reproducibles desde el
ZIP). **Ninguno es de producto:** los cinco módulos T-03 cumplen las cuatro promesas en todo lo ejecutado
por el revisor, la batería es determinista, no-vacua (confirmado por el revisor en las dos sondas) y el
lote de 52 baterías está en verde y coincide con `salida_pruebas.txt`. Con la corrección r01 (esperados al
contrato real) y los ajustes documentales 2–4, la pieza queda en condiciones de cierre; ninguna fila de
deuda abre ni se resuelve por esta revisión.
