# Informe de revisión independiente — V0.66 (pieza 7 del kit 2: pruebas doradas de la jornada y de la semana)

**Revisor:** GLM (conversación independiente, sin el historial de la pieza; 10 de noviembre de 2026)
**Alcance:** `pruebas/doradas.py` (NUEVO), `pruebas/pruebas_doradas.py` (NUEVO), `pruebas/doradas/jornada.json` y
`semana.json` (NUEVOS), cambios en `LEEME.md` y `entrega_glm/V0.66/*`; la promesa de que no cambia nada en
`validador/`, en los esquemas ni en la configuración, y de que ninguna prueba antigua se borra ni se debilita.
**Método:** verificación contra el código real (no contra lo que declara la entrega): lote completo de 55
baterías ejecutado por el revisor y comparado línea a línea con `salida_pruebas.txt`; la batería nueva corrida
tres veces (dos en el árbol y una tras `--regenerar` en una copia), salida idéntica; recuento propio de pasos,
comprobaciones, claves y floats de las dos fotos entregadas; contraste de los gemelos de `doradas.py` con los
recorridos reales de `pruebas_jornada.py` y `pruebas_semana.py` línea a línea; repetición de las cinco sondas de
no-vacuidad de la entrega sobre copias; y **dos sondas adversariales propias** (hallazgos 1 y 2, scripts
adjuntos): mutaciones de `validador/vigilancia.py` y de `pruebas_semana.py` en copias del árbol, medidas contra
`pruebas_doradas.py` y contra las baterías de los recorridos. Comparación de hashes SHA-256 contra el manifiesto
de V0.62 (la única ancla heredada que viaja) para acotar qué cambió en `validador/` desde V0.62 pos-revisión.

**Resultado: 3 hallazgos (1 medio, 2 bajos), ninguno de producto.** La pieza hace lo que promete en todo lo
verificado: las fotos son la del gemelo fiel de los dos recorridos, determinista entre procesos, el comparador
informa con el camino exacto, y la no-vacuidad declarada se confirma. El hallazgo medio es de la batería (la
pieza ES la batería): **la proyección de las «acciones» a `(regla, codigo, condicion)` pierde `ok` y
`posicion`, que ningún ESPERADO mira tampoco**, de modo que una regresión que cambie el `ok` o la `posicion`
informados de una acción de H pasa en silencio por todo el lote — justo lo que una prueba dorada existe para
cazar. Detalle abajo.

---

## 1. Lo verificado en verde (evidencia de la propia ejecución del revisor)

1. **Lote completo en verde:** 55 baterías ejecutadas por el revisor (Python 3.12.16), todas terminan en «TODAS
   LAS PRUEBAS PASAN»; la comparación automática con `salida_pruebas.txt` da **0 diferencias** (nombres y última
   línea; los tiempos varían con la carga, p. ej. `pruebas_doradas` 5,4 s declarada / 7,6 s bajo carga).
2. **La batería nueva:** **17 comprobaciones** (claim: 17), todas OK; **tres ejecuciones con salida idéntica**
   (dos seguidas en el árbol, `diff` vacío; una tras `--regenerar` en una copia temporal, que reescribe las dos
   fotos — 15 y 31 pasos —, imprime el recordatorio del Documento 0 y deja la batería otra vez en verde).
3. **Las fotos entregadas, verificadas por recuento propio:** 15 entradas en `jornada.json` y 31 en `semana.json`
   (46 = los 15 pasos de `pasos()` + los 31 de `pasos_semana()`), **0 claves «motivo»** a cualquier profundidad,
   44 floats en total **todos con ≤ 6 decimales**, JSON estricto ordenado e indentado (recargado y re-volcado
   igual), los puntos de giro documentados donde tocan (kill activo en `kill`/`viernes_kill`/`viernes_conciliar`,
   rearme con `rearmes == 1`, degradación a L1, cierres CERRADA, `POS-EXP-0003` con 50,0) y los **dos O-19 del
   viernes** presentes (`viernes_kill`: `["O-19", "O-19", "O-26"]`, ordenados y con duplicados, como declara el
   LEEME).
4. **Los gemelos son fieles a las baterías:** `foto_jornada` usa el mismo `nuevo(CFG)` + `broker()` y los mismos
   15 pasos de `pruebas_jornada.py` (importa `CFG`, no lo duplica); `foto_semana` replica el bucle de
   `pruebas_semana.py` con la misma secuencia de instantes (noches de 120 s, arranque con reloj nuevo,
   `comprobar_estado` y `contrastar` incluidos) y los mismos 31 pasos con sus deltas; el diario, los cortes y los
   puntos de control quedan fuera, como declara el Documento 0 §5, y no cambian el estado del Orquestador.
5. **No-vacuidad de la entrega, confirmada por el revisor:** las cinco sondas de
   `sondas_no_vacuidad_v066.py` repetidas sobre copias caen las cinco (S1 en la comprobación del redondeo, S2/S5
   en la byte a byte, S3 además en el Orquestador roto y en los puntos de giro, S4 en las tres del comparador) —
   «LAS CINCO CAZADAS», como declara `revision.md`.
6. **Los tres defectos del autorrepaso existen como se cuentan y están fijados:** `defecto_01` por
   `_O_Avisos_Raros` (avisos en diccionario → `ILEGIBLE`), `defecto_02` por la limpieza común de estados y
   niveles, `defecto_03` (sonda S1 de la entrega) por la comprobación unitaria del redondeo; la API del
   Documento 0 §4 está completa (8 funciones, 7 constantes, `PROFUNDIDAD_TOPE = 60 [PROPUESTO]`,
   `DECIMALES = 6`).
7. **LEEME actualizado donde declara:** cabecera (L1), fecha y resumen de la pieza (L3, con el «dif contra el
   ZIP de V0.65» y la cortesía documental), fila de `pruebas_doradas` en la tabla (L48) y **fila de
   `pruebas_semana` añadida junto a la de la jornada** (L47, la cortesía), el comando en «Cómo se ejecuta»
   (L190) y la sección «Comprobado en las pruebas doradas» (L234), con recuentos correctos (57 filas de tabla =
   55 baterías + 2 auxiliares).
8. **`validador/` apenas ha cambiado desde la última ancla disponible:** contra el manifiesto SHA-256 de V0.62
   pos-revisión (107 ficheros), **105 siguen byte a byte iguales** y solo difieren `validador/consola.py` y
   `validador/reloj.py` — coherente con el alcance declarado de las piezas V0.63 (semana con reloj) y V0.64
   (panel de la consola). En particular `vigilancia.py`, `orquestador.py` y `ejecucion_g.py` están intactos
   desde V0.62, lo que refuerza la declaración de V0.66 («nada en `validador/`») para todo lo que el manifiesto
   puede ver.

**Ninguna promesa de la pieza quedó refutada en producto:** los recorridos, el Orquestador y los módulos
responden con los códigos previstos por su contrato en todas las ejecuciones y mutaciones probadas.

## 2. Hallazgos

| # | Gravedad | Hallazgo | Corrección propuesta | Regresión |
| --- | --- | --- | --- | --- |
| 1 | **media** | **La proyección de las «acciones» pierde `ok` y `posicion`, y ningún ESPERADO los mira: una regresión que los cambie pasa en silencio por todo el lote.** `_acciones` (`pruebas/doradas.py:74-86`) reduce cada acción de H a `{condicion, codigo, regla}`; pierde `ok`, `posicion`/`expediente`, `senal`, `perdida_pct`, `nivel` y `aviso_registrado` (`vigilancia.py:98,104,127,161,210…`). Los ESPERADO de los recorridos tampoco los miran en los pasos que llevan acciones: `vigilar_objetivo` (jornada) comprueba solo `(regla, condicion, codigo)` de H-10 (`pruebas_jornada.py:114`; el `ok: False` de H-10 no lo comprueba nada) y `jueves_stop` (semana) solo `regla` y `ok` de H-01 (`pruebas_semana.py:355`; la `posicion` no la mira nadie). **Demostrado con dos mutaciones sobre copia (sonda H1):** (S1) flip `ok: False→True` en la acción H-10 → `pruebas_doradas` PASA y `pruebas_jornada` PASA; (S2) `posicion: pid → "POS-FANTASMA"` en la acción H-01 → `pruebas_doradas` PASA y `pruebas_semana` PASA. La foto entregada es ella misma la evidencia: la acción H-10 de `jornada.json` es `{"codigo": "H-10", "condicion": "OBJ-1", "regla": "H-10"}`, sin `ok` ni `posicion`. Además la documentación se contradice: Documento 0 §2 dice que «se quitan **solo** los textos de motivo» y el LEEME (L234) que «el resumen guarda del resultado todo menos los „motivo"», pero en las acciones se quita también esto. La ceguera afecta a los 8 pasos que llevan «acciones» (1 de la jornada, 7 de la semana) | Proyectar a `{condicion, codigo, ok, expediente, posicion, regla}` (coste cero: las fotos regeneran con un diff de 8 pasos que se explica al aceptarlo) o, alternativa más fina, guardar la acción entera sin «motivo» (ya se quita a cualquier profundidad) asumiendo más churn futuro; y ajustar las dos frases (Documento 0 §2 «solo los textos de motivo» y LEEME L234 «todo menos los „motivo"»). Nótese la incoherencia actual: las listas de `no_evaluadas` SÍ viajan enteras (menos «motivo»), las de `acciones` no | `hallazgo_1_revision_v066_acciones_ok_posicion.py` (adjunto): imprime FALLA con el árbol actual (las dos mutaciones inadvertidas) y OK cuando la corrección las caza; sirve como `r01` al aplicar el arreglo |
| 2 | **baja** | **El gemelo de la semana duplica a mano la cfg de la batería, y un cambio de escenario deja la foto fijando la semana vieja sin avisar.** `foto_semana` (`pruebas/doradas.py:158`) construye su Orquestador con `{"nivel_autonomia": {"TACTICA": "L2", "TRADING": "L2"}}` escrito en el propio módulo, porque la `cfg` de `pruebas_semana.py` vive DENTRO de `main()` (`:370`) y no es importable — `foto_jornada` sí importa `CFG` de `pruebas_jornada.py`. **Demostrado (sonda H2):** cambiando `TRADING: L2→L3` en la cfg de `main()`, `pruebas_semana` se adapta y PASA, y `pruebas_doradas` PASA con la foto entregada byte a byte igual: la foto dorada ya no documenta el recorrido de la batería y nada lo dice. La misma deriva es imposible hoy en la jornada (cfg importada) | Sacar la cfg a una constante de módulo `CFG_SEMANA` en `pruebas_semana.py` (una línea movida, sin cambio de comportamiento) e importarla en `doradas.py`; con el arreglo, un cambio de escenario regenera la foto (se acepta a propósito) o la batería dorada avisa | `hallazgo_2_revision_v066_cfg_semana_duplicada.py` (adjunto): imprime FALLA con el árbol actual y OK cuando el import hace que la batería dorada caiga con el escenario cambiado; sirve como `r02` |
| 3 | **baja** | **Trazabilidad de las revisiones anteriores, heredada y empeorada:** (a) `revision.md` de V0.65 cita `informe_revision_independiente_V0.65.md` y **ese informe no viaja en el ZIP** (los de V0.60, V0.61 y V0.62 sí); (b) las revisiones independientes de **V0.63 y V0.64 siguen «pendiente»** en sus `revision.md`, sin registro de que se hicieran ni de sus hallazgos; (c) el **manifiesto SHA-256** de los ficheros heredados (práctica que el propio LEEME, L11, describe como parte del método desde el hallazgo 4 de V0.62) solo viaja en V0.62 — V0.63 a V0.66 no lo actualizan; (d) `Deuda_tecnica.md` sigue sin viajar (inherited V0.62 hallazgo 4) y `notas_deuda.md` de V0.66 vuelve a citarlo («Cambios en „Deuda técnica y pendientes del operador" de `Deuda_tecnica.md`: ninguno»), de modo que las filas que dice seguir sin resolver (T-64 a T-69, última resuelta T-60) **no son verificables desde el ZIP**. Nada de esto afecta a la pieza V0.66 en sí | Incluir los informes que se citan (o sus hallazgos resumidos en el propio `revision.md`), cerrar o dar por renunciadas las revisiones de V0.63/V0.64 con una nota, recuperar el manifiesto por entrega (el de V0.62 demostró hoy su valor: acotó `validador/` a 2 ficheros) y recordar en `notas_deuda.md` dónde está el contenido de la deuda o adjuntar la tabla | Ninguna de código; documental |

**Ningún hallazgo es de producto:** ninguna conducta de `validador/` ni del Orquestador cambia con la pieza y
en todo lo ejecutado y mutado los módulos respondieron con códigos previstos por su contrato. Los hallazgos 1 y
2 son de la batería nueva (la pieza), el 3 es de la entrega.

## 3. Sondas del revisor (adjuntas)

| Sonda | Qué prueba | Resultado |
| --- | --- | --- |
| `hallazgo_1_revision_v066_acciones_ok_posicion.py` | Dos mutaciones de `vigilancia.py` en copia: S1 flip de `ok` en la acción H-10 (jornada), S2 `posicion` fantasma en la acción H-01 (semana; H-01 no lo mira el guarda interno de `vigilar`, así que la mutación no tiene efectos laterales); corre `pruebas_doradas` y la batería del recorrido en cada caso. Con árbol actual: **las dos INADVERTIDAS** | FALLA (defecto presente); OK cuando la corrección del hallazgo 1 las caza |
| `hallazgo_2_revision_v066_cfg_semana_duplicada.py` | Cambia la cfg de `main()` en `pruebas_semana.py` (TRADING L2→L3) en copia y corre `pruebas_semana` y `pruebas_doradas`; además comprueba con `ast` que la cfg no es constante de módulo y que `doradas.py` la escribe a mano | FALLA (la foto queda fijando el escenario viejo y ambas baterías pasan); OK con el import |
| Lote propio | 55 baterías con `corre_baterias.py` | 0 con fallos; 0 diferencias contra `salida_pruebas.txt` |
| Sondas de la entrega | Las 5 mutaciones de `sondas_no_vacuidad_v066.py` | LAS CINCO CAZADAS (confirmado) |
| Recuentos propios | Pasos (15+31=46), comprobaciones (17), claves «motivo» (0), floats >6 dec (0), ejecuciones idénticas (3), `--regenerar` en copia (ok), fila de la semana en el LEEME (L47) | Todo según lo declarado |

## 4. Observaciones (sin corrección exigida)

1. **`str(x)` sobre un `set` sería no determinista entre procesos** (aleatorización de hashes de cadenas): si
   una pieza futura mete un `set` en un resultado, la promesa «byte a byte en cualquier máquina» se rompería en
   silencio — `_limpia` lo convertiría en texto con un orden que varía por proceso. Hoy no hay sets en los
   resultados (verificado: fotos idénticas entre procesos en las tres ejecuciones), y el `volcar` del estado
   los excluye de facto. Rechazar `set`/`frozenset` explícitamente en `_limpia` (ILEGIBLE) lo dejaría cerrado.
2. **Colisión de claves tras `str(k)`** (p. ej. `1` y `"1"`): `_limpia` las fusiona en silencio y la foto pierde
   una entrada sin que el comparador avise. Igual de teórico hoy; lo mismo que el punto 1 se cierra de un plumazo.
3. **`leer_foto()` y el parámetro `recorridos` de `generar_fotos()` no están ejercitados** por la batería (la
   batería lee los ficheros directamente). API declarada y sin uso: o se ejercita o se anota como tal.
4. **La comprobación «no cambia nada» se hace contra `pe.volcar`**: un efecto lateral sobre un atributo fuera
   del volcado no se vería. Es el estándar del propio marco (las baterías gemelas usan el mismo patrón); se
   acepta, con la nota de que la promesa del Documento 0 es «no cambia nada» y el volcado es una aproximación.
5. **Por encima de `PROFUNDIDAD_TOPE`, `_dif` compara valores ya cortados**: dos fotos con contenido distinto
   más allá de 60 niveles darían `"(...)" == "(...)"` y pasarían. Hoy imposible (ningún resultado del marco
   llega ahí) y declarado `[PROPUESTO]`; lo deja cerrado el mismo tratamiento del punto 1 si se hace.
6. **El kill «ilegible»**: con un `o.kill` que lanza, la foto da `ILEGIBLE`; con un `o.kill` falsy pero no None
   (0, `""`) da `True` (activo). Documento 0 §3 lo resume como «el kill ilegible cuenta como activo», que solo
   describe el segundo caso; matiz de redacción, no de conducta.

## 5. Límites de la revisión

- **El ZIP de V0.65 no viaja**: las declaraciones «dif contra el ZIP de V0.65», «nada en `validador/`» y
  «ninguna prueba antigua cambia» no son verificables en su exactitud desde este ZIP (misma limitación que el
  hallazgo 4 de V0.62). Lo que sí queda acotado con el manifiesto de V0.62: solo `consola.py` y `reloj.py`
  difieren en `validador/` desde V0.62 pos-revisión, y el lote completo pasa sin tocar nada de lo heredado.
- La revisión cubre a fondo la pieza V0.66 y su perímetro (los dos recorridos, `vigilancia.py` como productor
  de las acciones y la infraestructura de fotos); el resto de `validador/` se verifica por el lote y por el
  manifiesto, no por re-lectura línea a línea (ya revisados en las iteraciones anteriores del marco).

## 6. Propuesta de anotación para `entrega_glm/V0.66/revision.md` (sección «Revisión independiente»)

```markdown
## Revisión independiente (hecha el 10 de noviembre de 2026)

La hizo otro GLM en conversación independiente (su informe: `informe_revision_independiente_V0.66.md`, con los
scripts `hallazgo_1_revision_v066_acciones_ok_posicion.py` y `hallazgo_2_revision_v066_cfg_semana_duplicada.py`
en `entrega_glm/revisores/`). Lote completo repetido por el revisor (55 baterías, 0 con fallos, 0 diferencias
contra `salida_pruebas.txt`), fotos verificadas por recuento propio, gemelos contrastados con las baterías de
los recorridos, las cinco sondas de no-vacuidad repetidas (cazadas) y dos sondas adversariales propias.

Resultado: 3 hallazgos (1 medio, 2 bajos), ninguno de producto:

1. MEDIA — la proyección de las «acciones» pierde `ok` y `posicion` y ningún ESPERADO los mira: una regresión
   que los cambie pasa en silencio por todo el lote (demostrado con dos mutaciones sobre copia). Arreglo
   propuesto: proyectar a {condicion, codigo, ok, expediente, posicion, regla} y ajustar las dos frases
   («solo los textos de motivo» en Documento 0 §2 y «todo menos los „motivo"» en el LEEME L234).
2. BAJA — el gemelo de la semana duplica a mano la cfg de la batería (no importable: vive dentro de main()):
   un cambio de escenario deja la foto fijando la semana vieja sin avisar (demostrado). Arreglo: constante
   CFG_SEMANA a nivel de módulo e importada.
3. BAJA — trazabilidad: el informe de V0.65 se cita y no viaja; revisiones de V0.63/V0.64 sin cerrar;
   manifiesto SHA-256 sin actualizar desde V0.62; `Deuda_tecnica.md` sigue sin viajar.
```
