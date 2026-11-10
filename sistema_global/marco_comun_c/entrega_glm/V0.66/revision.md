# Revisiones — V0.66 (pruebas doradas)

## Revisión propia (autorrepaso antes de entregar, 10 de noviembre de 2026)

Repaso del propio cambio (paso 6 del método): caminos que no fallan cerrado, mutaciones antes de validar,
excepciones posibles y casos frontera. Tres defectos reales, corregidos y fijados con su comprobación
(el detalle en Documento 0 §4):

1. `defecto_01` — avisos que no son lista salían como lista vacía en la foto; ahora `ILEGIBLE`.
2. `defecto_02` — estados y niveles crudos podían llevar un valor no JSON hasta `texto_foto`; ahora pasan
   por la misma limpieza que el resultado.
3. `defecto_03` (sonda S1) — el redondeo a 6 decimales estaba sin fijar: los recorridos de hoy solo
   llevan cantidades exactas y quitarlo no cambiaba ninguna foto; fijado con su comprobación unitaria.

No-vacuidad demostrada con `sondas_no_vacuidad_v066.py`: cinco mutaciones de `doradas.py` en una copia
del árbol (sin redondeo, con «motivo», kill fijo a False, comparador vacío y claves sin ordenar) y la
batería cae en las cinco. Cortesía documental: la tabla de baterías del LEEME no tenía fila para
`pruebas/pruebas_semana.py` (se añadió junto a la de la jornada); no toca ninguna prueba.

## Revisión independiente (hecha el 10 de noviembre de 2026 y aplicada aquí)

La hizo otro GLM en conversación independiente (su informe íntegro: `informe_revision_independiente_V0.66.md`
de esta carpeta, con las dos sondas adversariales en `entrega_glm/revisores/`), con el ZIP ya en verde y sin el
historial de la pieza. Verificó contra el código real, no contra lo que declara la entrega: el lote completo
corrido por él (55 baterías, 0 con fallos, 0 diferencias contra `salida_pruebas.txt`), la batería nueva corrida
tres veces con salida idéntica (incluida una tras `--regenerar` en copia), las fotos entregadas verificadas por
recuento propio (15 y 31 pasos, 0 claves «motivo», 44 floats con ≤ 6 decimales, JSON estricto ordenado), los
gemelos contrastados línea a línea con `pruebas_jornada.py` y `pruebas_semana.py`, las cinco sondas de
no-vacuidad repetidas (LAS CINCO CAZADAS) y el manifiesto SHA-256 de V0.62 como única ancla heredada (105 de
107 ficheros de `validador/` intactos desde V0.62 pos-revisión: solo difieren `consola.py` y `reloj.py`,
coherente con las piezas V0.63 y V0.64).

Resultado: **3 hallazgos (1 medio, 2 bajos), ninguno de producto**. Ninguna conducta de `validador/` ni del
Orquestador cambia con la pieza y en todo lo ejecutado y mutado los módulos respondieron con códigos previstos
por su contrato. Los hallazgos 1 y 2 son de la batería nueva (la pieza), el 3 es de la entrega.

## Hallazgos y correcciones

| # | Gravedad | Hallazgo | Corrección aplicada | Regresión |
| --- | --- | --- | --- | --- |
| 1 | media | **La proyección de las «acciones» a `(regla, codigo, condicion)` pierde `ok` y `posicion`, y ningún ESPERADO los mira: una regresión que los cambiara pasaba en silencio por todo el lote.** Demostrado con dos mutaciones sobre copia: flip de `ok` en la acción H-10 de la jornada y `posicion` fantasma en la H-01 de la semana, ambas inadvertidas por `pruebas_doradas.py` y por las baterías de los recorridos. La documentación, además, se contradecía («solo» los «motivo» en Documento 0 §2 y «todo menos los „motivo"» en el LEEME) | `_acciones` proyecta ahora a `{condicion, codigo, expediente, ok, posicion, regla}`. Las fotos se regeneraron con `--regenerar` y la regeneración está explicada en Documento 0 §5: **2 pasos cambiados, uno por recorrido** (`vigilar_objetivo` con H-10 y `jueves_stop` con H-01, las únicas acciones no vacías de las dos fotos); cada acción gana `ok`, `posicion` y `expediente` (null aquí). Las dos frases ajustadas (Documento 0 §2 y LEEME, cabecera y «Comprobado en las pruebas doradas») | `r01`: `entrega_glm/revisores/hallazgo_1_revision_v066_acciones_ok_posicion.py`. Antes: FALLA (las dos mutaciones inadvertidas, evidencia estática sin `ok`). Ahora: OK — las dos mutaciones CAZADAS (la batería dorada cae y las de los recorridos pasan, que es justo el hueco que se cierra) |
| 2 | baja | **El gemelo de la semana duplicaba a mano la cfg de la batería** (vive dentro de `main()` de `pruebas_semana.py` y no es importable, al contrario que la `CFG` de la jornada): un cambio de escenario dejaba la foto fijando la semana vieja sin avisar (demostrado: TRADING L2→L3 y las dos baterías en verde con la foto entregada byte a byte igual) | La cfg sale a la constante de módulo `CFG_SEMANA` en `pruebas_semana.py` (misma línea movida, sin cambio de comportamiento) y `foto_semana` la importa (`sm.CFG_SEMANA`): un cambio de escenario cambia también la foto, o la batería dorada avisa | `r02`: `entrega_glm/revisores/hallazgo_2_revision_v066_cfg_semana_duplicada.py`. Antes: FALLA. Ahora: OK — `doradas.py` ya no escribe la cfg a mano y la mutación de la sonda da NO APLICABLE (la cfg cambió de forma), que la sonda trata como corregido |
| 3 | baja | **Trazabilidad de las revisiones anteriores, heredada y empeorada:** el informe de V0.65 se citaba y no viajaba; las revisiones de V0.63 y V0.64 seguían «pendiente» sin registro; el manifiesto SHA-256 no se actualizaba desde V0.62; `Deuda_tecnica.md` sigue sin viajar y `notas_deuda.md` citaba filas (T-64 a T-69) no verificables desde el ZIP | (a) `informe_revision_independiente_V0.65.md` copiado a `entrega_glm/V0.65/` y el de esta revisión a esta carpeta; (b) revisiones de V0.63 y V0.64 cerradas como **renunciadas** con nota fechada (sin inventar hallazgos); (c) `manifiesto_sha256.txt` nuevo en esta carpeta, con el alcance del de V0.62 (`validador/`, `esquemas/`, `pruebas/` salvo lo que cambia aquí, y la raíz; `entrega_glm/` fuera a propósito); (d) nota en `notas_deuda.md`: el contenido de T-64 a T-69 viaja en `entrega_glm/V0.65/notas_deuda.md` | Ninguna (documental) |

**Ningún hallazgo es de producto:** ni el Orquestador ni ningún módulo de `validador/` cambian (el manifiesto
SHA-256 de esta carpeta lo deja demostrable desde el propio ZIP); el diff V0.66 → V0.66 pos-revisión toca solo
`pruebas/doradas.py`, `pruebas/pruebas_doradas.py`, `pruebas/pruebas_semana.py` (una línea movida), las dos
fotos regeneradas, `LEEME.md`, los documentos de `entrega_glm/V0.66/` y los añadidos de la revisión.

## Observaciones del revisor, todas atendidas

1. **`str(x)` sobre un `set` sería no determinista entre procesos** (aleatorización de hashes): `_limpia`
   rechaza ahora `set` y `frozenset` como `"ILEGIBLE"` (falla cerrado, determinista), y la comprobación de
   resultados raros lo fija con un set, un frozenset anidado y el resultado exacto.
2. **Colisión de claves tras `str(k)`** (p. ej. `1` y `"1"`): `_limpia` la marca ahora con `"ILEGIBLE"`
   (visible) en vez de fundir las entradas en silencio; fijado en la misma comprobación con `{"1", 1, True}`.
3. **`leer_foto()` y el parámetro `recorridos` sin ejercitar**: ejercitados ahora en la comprobación de la
   carpeta temporal (con y sin carpeta, y `recorridos` con un subconjunto); la fila del Documento 0 §3 lo dice.
4. **La comprobación «no cambia nada» mira el volcado de `persistencia`**: aceptada como estándar del propio
   marco, anotada como límite en Documento 0 §5.
5. **Por encima de `PROFUNDIDAD_TOPE` el comparador trabaja con valores ya cortados**: declarado [PROPUESTO],
   hoy inalcanzable desde los resultados del marco; anotado en Documento 0 §5.
6. **Matiz de redacción del kill**: Documento 0 §3 dice ahora lo que hace el código: un kill falsy que no es
   `None` cuenta como activo (solo `None` lo apaga) y uno que lanza sale `"ILEGIBLE"`.

## Resultado tras corregir

- La batería sigue en **17 comprobaciones** (ninguna se borra ni se debilita; dos ganan contenido: los raros
  con sets y colisiones, y la carpeta temporal con `leer_foto` y `recorridos`) y determinista: dos ejecuciones
  consecutivas con salida idéntica.
- Las fotos entregadas son las regeneradas tras el hallazgo 1 (diff documentado en Documento 0 §5); la batería
  dorada las cuadra byte a byte.
- El lote completo en verde de nuevo: **55 baterías**, todas terminan en «TODAS LAS PRUEBAS PASAN»
  (`salida_pruebas.txt` de esta carpeta, regenerada tras las correcciones).
- **No-vacuidad de las correcciones**: r01 con el árbol anterior FALLA y con el corregido OK (las dos
  mutaciones CAZADAS por la batería dorada); r02 FALLA antes y OK después. Las cinco sondas de no-vacuidad de
  la pieza (`sondas_no_vacuidad_v066.py`) siguen cazadas sobre el árbol corregido.
- La cfg de la semana es ahora la misma constante para la batería y para la foto (`CFG_SEMANA`): la única
  prueba antigua tocada, y es una línea movida sin cambio de comportamiento.
