# Informe de revisión independiente — V0.65 (pieza 6 del kit 2: pasada de coherencia contra la Constitución)

**Revisor:** GLM (conversación independiente, sin el historial de la pieza; 10 de noviembre de 2026)
**Alcance:** `entrega_glm/V0.65/pasada_coherencia.md` (tabla de 183 filas, hallazgos PC2-01 a PC2-08),
`generar_pasada.py`, los ocho scripts de `scripts/pc2_*.py`, `notas_deuda.md` (T-64 a T-69),
`notas_briefing.md`, `revision.md`, `salida_pruebas.txt` y la promesa «no cambia código, esquemas ni
pruebas; el único fichero del marco tocado es `LEEME.md`».
**Método:** el mandado por `revision.md` de la pieza — (1) 20 filas de la tabla elegidas al azar con
`random.Random(20261113)` sobre los números de fila, (2) los ocho scripts de los hallazgos ejecutados
desde la carpeta `marcoC`, (3) búsqueda de requisitos de la Constitución que la tabla no recoja — más la
verificación contra el código real propia de toda revisión: lote completo de 54 baterías ejecutado por el
revisor, regeneración del documento con el generador entregado y diff, sondas propias sobre el verificador
de citas y sobre las afirmaciones de código de los ocho hallazgos (`sondas_revisor_v065.py`, adjunta).
**Límite declarado antes de empezar:** la Constitución Global V0.4 **no viaja en el ZIP**. Los puntos (1)
y (2) del mandato se ejecutaron íntegros; el punto (3) y la comprobación de fidelidad de los parafraseos
solo pudieron hacerse con la evidencia interna del ZIP (secciones citadas en el código, en las entregas
anteriores y en los propios hallazgos). Este punto queda para rehacer con la Constitución delante.

**Resultado: 2 hallazgos documentales bajos y 3 observaciones; ninguno de producto.** Las 183 filas
resisten la verificación mecánica completa (recuento, numeración, regeneración byte a byte), las 20 filas
muestreadas resisten la verificación de citas y de juicio (todas las comprobaciones citadas pasan en
ejecución propia y el estado asignado es correcto en las 20), los ocho scripts dan FALLA como declara la
entrega, y cada afirmación de código de los ocho hallazgos salió cierta salvo una imprecisión de atribución
en la explicación del falso OK de PC2-06. No se propone ninguna fila de deuda nueva ni se abre hallazgo de
código: las correcciones son de texto.

---

## 1. Lo verificado en verde (evidencia de la propia ejecución del revisor)

1. **Lote completo en verde:** las 54 baterías ejecutadas por el revisor (Python 3.12.16, el mismo de la
   entrega), todas en «TODAS LAS PRUEBAS PASAN», 0 con fallos; las líneas de resultado coinciden una a
   una con la `salida_pruebas.txt` entregada (54/54, comparación automática sin tiempos) y también con
   las de `entrega_glm/V0.64/salida_pruebas.txt` (54/54): coherente con «la pieza no cambia código».
2. **Los ocho scripts dan FALLA** (PC2-01 a PC2-08, ejecutados desde `marcoC`), que es lo que
   `revision.md` exige mientras la divergencia exista.
3. **El generador reproduce el entregable byte a byte:** `python3 entrega_glm/V0.65/generar_pasada.py`
   verifica las 183 filas (183 «dónde» y «prueba») y escribe un `pasada_coherencia.md` **idéntico byte a
   byte** al entregado (`diff` vacío).
4. **El verificador de citas no es vacuo (sonda S1).** Con una función inventada inyectada en una fila
   (`autorizar_inexistente`) o una comprobación inventada (`pantalla_que_no_existe_en_la_bateria`) sobre
   una copia del árbol, el generador lista el fallo, sale con exit 1 y **no reescribe el documento**. La
   promesa «si una sola cita no cuadra, no escribe nada» se cumple.
5. **Recuentos:** 183 filas, numeración 1..183 sin huecos ni repeticiones, y estados exactamente los
   afirmados: 91 CUMPLE, 48 PARCIAL, 20 FALTA, 1 CONTRADICE, 23 FUERA DE FASE 1 (160 filas que tocan a la
   Fase 1; la cuenta «de las 160 filas» del resumen es correcta).
6. **Las cinco citas que el autocontrol dice haber corregido existían de verdad:** el caso real de la
   primera es `inv_V02_perfil_no_construido` y está en `generar_casos.py`; `reduccion_parcial_vuelve_a_abierta`
   está en `pruebas_orquestador.py` (no en `pruebas_reduccion.py`); `estado_sello_del_corte_vigente` no existe en
   ninguna batería; `colision_de_ids_ya_no_se_puede_crear` está en `pruebas_consola.py` (no en
   `pruebas_orquestador.py`); `registro_version_REG030` está en `pruebas_envoltura.py` (no en
   `pruebas_contratos.py`). El relato del autocontrol (Documento 0 §4 y revision.md) es fiel.
7. **Continuidad de la deuda:** la última fila nueva de `entrega_glm/V0.64/notas_deuda.md` es T-63, y
   T-64..T-69 no aparecen en ninguna entrega anterior del ZIP (sin colisión); las seis filas nuevas
   entran sin resolver, como dice `notas_deuda.md`.
8. **LEEME.md con los tres cambios prometidos:** cabecera «…— V0.65 (provisional, 0.x)», párrafo
   «Fecha: 10 de noviembre de 2026 (V0.65…)» y punto «Comprobado en la pasada de coherencia» (línea 214),
   con recuentos correctos (183; 91/48/20/1/23; ocho hallazgos con FALLA).

## 2. La muestra de 20 filas (mandato 1)

`random.Random(20261113).sample(range(1, 184), 20)` → **3, 5, 8, 13, 14, 17, 25, 29, 34, 46, 77, 79, 94,
101, 118, 128, 132, 142, 154, 164** (interpretación declarada: muestreo uniforme sobre los números de
fila; caen 6 CUMPLE, 8 PARCIAL, 4 FALTA y 2 FUERA DE FASE 1; la única CONTRADICE, fila 65, no sale en la
muestra — se comprobó aparte, véase más abajo).

Para cada fila se verificó: (a) cada cita «dónde» con `ast` — el módulo existe en `validador/` y el nombre
está definido (función, método de clase, clase o constante, respetando la marca «(constante)»/«(clase)» de
la cita); (b) cada cita «prueba» **ejecutando la batería citada una vez** y exigiendo el nombre completo
de la comprobación en una línea «OK» de su salida (para `ejecutar_pruebas.py`, que el caso existe y el
runner le da OK); (c) el estado, leyendo el código que sostiene la fila. Resultado: **las 20 filas
cuadran en sus citas y en su estado.**

| Fila | § | Estado | Verificación del revisor |
| --- | --- | --- | --- |
| 3 | §1 P1 | CUMPLE | O-05 aparece 45 veces en `orquestador.py` (actor en cada método público) y G-05 en `ejecucion_g.py`; las tres comprobaciones citadas pasan |
| 5 | §1 P3 | CUMPLE | V-08 marca SUPUESTO sin `modelo_ref`/`motor_id` (`validar_sobre.py:256`) y V-26 cruza con el registro SC-3; batería T-26 en verde |
| 8 | §1 P6 | PARCIAL | V-09 y H-16 existen y pasan; lo congelado antes del resultado (SC-4) es Fase 3 — el estado PARCIAL es correcto |
| 13 | §1 P11 | FALTA | Ni «lector», ni «SC-11», ni «aislado» en `validador/` (coincide con el script de PC2-06) |
| 14 | §1 P12 | FUERA | Regla de proceso; la refactorización de A/B es Fase 2 (§14) |
| 17 | §1 P15 | PARCIAL | F-23 existe y veta sin precio del intermediario; no hay latido ni verificación externa del Contradictor en el código |
| 25 | §2 Broker | PARCIAL | Actores BROKER/GESTOR_* en el código; el Broker conversacional no está en el marco |
| 29 | §2 registro | PARCIAL | O-03 rechaza el duplicado; no hay almacén común consultable por otros bloques (PC2-05) |
| 34 | §2 perfiles | PARCIAL | V-02 en `validar_sobre.py` y R-03 en `validar_encargo.py`; no hay constante con los doce códigos (solo `perfiles_activos: ["C-DIV"]` en `CFG_ESQUEMA`) |
| 46 | §3 registros | FALTA | Sin COT/13F/CNMV/directivos en `k_calidad.py` y sin registros comunes en el Orquestador |
| 77 | §6 niveles | CUMPLE | L0–L3 en el código y «sin dato = L1» en `CONFIG_DEFECTO` (`orquestador.py:90`) |
| 79 | §6 apalanc. | CUMPLE | `apalancamiento_permitido: False` en `CFG_ESQUEMA` (`persistencia.py:119`) y F-05 veta |
| 94 | §7 benchmark | PARCIAL | `REFERENCIA_EFECTIVO` vive en `comparador.py` y alimenta `CONFIG_DEFECTO["referencias"]` [PROPUESTO]; su rentabilidad sale de la configuración — T-37 correcta |
| 101 | §7 libros | FUERA | `dimensionar` existe (E mínimo) y CT-G-07 está PENDIENTE en el registro; el plan por libros es Fase 2 |
| 118 | §8 conciliación | CUMPLE | Tolerancias, «explicada» y «discrepancia» con las comprobaciones citadas en verde |
| 128 | §9.9 sombra | FALTA | Ni «sombra», ni «índice mundial», ni «aportes» en `validador/` (PC2-04) |
| 132 | §10.2 pit | CUMPLE | `punto_en_el_tiempo` existe y las dos comprobaciones PIT pasan |
| 142 | §10 economía | PARCIAL | El sello con reemplazo registrado funciona; los filtros baratos son de A/B y el almacén común no existe |
| 154 | §11 incidente | FALTA | Nada detecta inyección ni credenciales comprometidas en `validador/`; el kill manual y el automático sí existen — el estado FALTA con esa nota es exacto |
| 164 | §12.3 entornos | PARCIAL | Todo corre sobre `BrokerSimulado` y no hay canal a producción; la comprobación de la semana pasa |

**Fila 65 (CONTRADICE, fuera de muestra pero única de su estado):** G-06 admite solo una posición por
instrumento y las dos comprobaciones citadas (`segunda_posicion_en_el_mismo_instrumento_G06_sin_enviar`,
`…_O06`) pasan; la fila documenta la contradicción y remite a T-13. Correcta.

## 3. Hallazgos

| # | Gravedad | Hallazgo | Corrección propuesta |
| --- | --- | --- | --- |
| 1 | baja | **La explicación del falso OK de PC2-06 no es reproducible: la «noticia» no estaba en el docstring de H.** Documento 0 §4, `revision.md` y `notas_briefing.md` atribuyen el falso OK a «la palabra «noticia» en docstrings de H y de pruebas» («el docstring de H-16 habla de «una noticia»»). En el código que viaja (V0.64 intacto: las 54 líneas de batería son idénticas a la salida de V0.64), `validador/` **no contiene ninguna** ocurrencia de «noti» (ni «noticia» ni «notificar»): el docstring de H-16 (`vigilancia.py:14`) habla de «una invalidez por una métrica que no es el precio», sin «noticia». La «una noticia» real está en un **argumento de una llamada de prueba**: `pruebas/pruebas_orquestador.py:529` (`o.proponer_sobre_posicion(P, "la tesis parece debilitada por una noticia", "H", AHORA)`) y, si el primer script barría los .md de la entrega, en los textos de la propia tabla y del LEEME. La segunda mitad del relato sí es cierta: «lector» está en `pruebas_robustez_t03.py:36,226` (la prueba de T-03). La corrección hecha (acotar a `validador/` con patrones del servicio: SC-11, sc11, riesgos_geopoliticos, lectores?_de_contenido, lecturas_aisladas) es correcta y el script da FALLA — el fondo está bien, la atribución no | Reescribir la frase en los tres documentos: el falso OK venía de las pruebas (motivo de `proponer_sobre_posicion` en `pruebas_orquestador.py:529`, «lector» en `pruebas_robustez_t03.py`) y de los propios textos de la entrega si el primer barrido los incluía; el docstring de H-16 no dice «noticia» |
| 2 | baja | **§9.5 y §9.10 no tienen fila ni mención en todo el árbol: la tabla salta de §9.4 a §9.6 y de §9.9 a §9.11 sin cortesía ni explicación.** El método de la propia tabla (paso 2) promete «donde una sección no tiene requisitos verificables en el código hay una fila que lo dice». O esas subsecciones existen en la Constitución y la tabla las saltó sin declararlo — el caso del hallazgo de esta revisión —, o no existen y la promesa del método sobra. Este revisor no puede decidirlo: **la Constitución no viaja en el ZIP** (límite declarado al principio). Es el único candidato real que la búsqueda interna produjo como «requisito posiblemente no recogido» | Rehacer el mandato 3 con la Constitución delante: si §9.5/§9.10 existen, añadir la fila que toque (o la fila de cortesía); si no existen, quitar la impresión de numeración continua o anotarlo en el método. Cuando el operador la ratifique, resolver también R3 |

**Observaciones (sin corrección exigida):**

3. **Citas de deuda no verificables desde el ZIP (recurrencia del hallazgo 4 de V0.62).** La tabla y los
   hallazgos remiten a T-13, T-37, T-40, T-53, T-54, T-56, T-57, T-58 y a toda la serie P-02..P-24; de
   todo eso, solo T-63 (en `notas_deuda` de V0.64) y las nuevas T-64..T-69 son comprobables aquí —
   `Deuda_tecnica.md` no viaja y ninguna de esas filas se cita con su texto. Lo mismo vale para
   «dif contra el ZIP de V0.64: solo `LEEME.md` modificado» (cabecera de `salida_pruebas.txt`): sin el
   ZIP anterior no se puede repetir, aunque la identidad de las 54 líneas de batería entre V0.64, V0.65 y
   la ejecución propia lo hace verosímil. El manifiesto SHA-256 que introdujo V0.62 no se ha vuelto a
   usar desde V0.62.
4. **Precisión de «el registro marca todas las envolturas COMPLETA» (fila 68 y PC2-08).** Cierta a nivel
   de contrato: las once entradas con esquema llevan `envoltura: "COMPLETA"` en su cabecera. Estrictamente,
   dos versiones RETIRADA llevan otro valor (CT-G-08 0.1.0 «PARCIAL», CT-G-14 0.1.0 «PROPIA»); «todas»
   vale para las vigentes, que es lo que el hallazgo quiere decir.
5. **Trazabilidad de subsecciones.** El código cita §6.1/§6.2/§6.3 (cabecera de `pruebas_operador_t50.py`
   y docstrings del Orquestador) y las entregas de V0.39 citaban §7.3 (cortacircuitos por estrategia,
   Fase 4); la tabla los cubre de facto (filas 85–87, 98, 102, 115 y 117) pero nunca nombra esas
   subsecciones en su columna §. Un lector que trace §6.x o §7.x por número no las encontrará.
6. **Micro-recuento:** «desde entonces hay 50 versiones (V0.14 a V0.64…)» (Documento 0 §1): V0.14..V0.64
   son 51 números de versión; si ninguna se saltó, la cifra es 51. No es verificable desde el ZIP (las
   entregas intermedias no viajan todas).

## 4. Sondas del revisor (`sondas_revisor_v065.py`)

| Sonda | Qué prueba | Resultado |
| --- | --- | --- |
| S0 | Lote completo propio (54 baterías) | 0 con fallos; líneas idénticas a V0.64 y V0.65 entregadas |
| S1a/S1b | Camino negativo del verificador de citas (copia del árbol, función y comprobación inventadas) | exit 1, lista el fallo y NO reescribe el documento |
| S2 | Los ocho scripts de hallazgo | FALLA los ocho |
| S3 | Regeneración de `pasada_coherencia.md` | Byte a byte idéntica al entregado |
| S4 | Muestra de 20 filas: citas con `ast` (tipo incluido) y comprobaciones con ejecución propia (nombre completo en línea OK) | 20/20 sin problemas |
| S5 | Afirmaciones de código de los hallazgos: `POLITICA_DEFECTO` y `CLAVES_CONTEXTO` de F sin volumen/liquidez/coste/margen; campos `confianza`/`incertidumbre`/`resultado_politica` de los esquemas CT-G-01/02/03/08/14; sin COT/13F/CNMV en K; sin embudo/sequía en `consola.panel`; sin `methodology_version` en esquemas ni validador; sin «sombra» | Todas ciertas (con la precisión del registro de contratos de la observación 4) |
| S6 | Continuidad de deuda y LEEME | T-63 última de V0.64; T-64..T-69 sin colisión; LEEME con los tres cambios |

## 5. Resultado

La pieza hace lo que dice: el documento regenera idéntico byte a byte, el verificador de citas funciona
también en su camino negativo, la tabla cuadra en recuentos, en sus citas y — en lo muestreado y en lo
comprobado por los scripts — en sus estados; los ocho hallazgos describen divergencias reales frente al
código (todas sus afirmaciones de código verificadas salvo la atribución del falso OK de PC2-06) y las
seis filas de deuda propuesta entran en orden sin resolver. **Ningún hallazgo es de producto** (la pieza
no toca código y no hay conducta que refutar). Las correcciones son documentales: la frase del falso OK de
PC2-06 en tres documentos (hallazgo 1) y la resolución de §9.5/§9.10 con la Constitución delante
(hallazgo 2). El mandato 3 de la revisión (requisitos no recogidos) queda **incompleto por materiales**:
sin la Constitución en el ZIP solo se puede buscar con la evidencia interna, y esa búsqueda produjo un
solo candidato real (§9.5/§9.10) más dos mejoras de trazabilidad (§6.1–6.3, §7.3). Con las dos
correcciones y ese punto re-hecho con la Constitución, la pieza queda en condiciones de cierre; ninguna
fila de deuda abre ni se resuelve por esta revisión.
