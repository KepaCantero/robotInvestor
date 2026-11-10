# Revisión independiente — V0.61 (catálogo de códigos)

Estado: **revisión ejecutada el 9 de noviembre de 2026 y ocho hallazgos corregidos** (sección 0 de las
directrices). La revisión se hizo en otra conversación, con el ZIP de la pieza ya en verde y el prompt de la
sección 9, sin el historial de la pieza. El revisor verificó contra el código real, no contra lo que declara
la entrega: (1) el lote completo en su propia ejecución —51 baterías, todas en «TODAS LAS PRUEBAS PASAN», sin
una línea FALLA, coincidente con la `salida_pruebas.txt` entregada—; (2) recuentos propios (282 entradas,
281 pares, 250 códigos distintos) con un método de minado distinto al de la pieza (`tokenize` frente al
`ast`), coincidente al 100 % en los dos sentidos; (3) el contraste de cada fila muestreada del catálogo con
lo que su módulo emite de verdad; (4) la no-vacuidad de la batería con sondas propias (`sondas_revisor_v061.py`,
en la raíz: S1, constante nueva «H-99» inyectada en una copia de `validador/`, hace fallar la batería en la
comprobación de cobertura; S4, entrada borrada del catálogo, hace fallar como debe; S2 y S3, textos y
efectos corregidos, no alteraban el resultado: ningún check protegía la exactitud del contenido) y (5)
conteos auxiliares (O-01 ×71, O-00 ×3, O-02 ×12 en `orquestador.py`). El informe íntegro del revisor está
copiado en `informe_revision_independiente.md` de esta carpeta. Resultado: **ocho hallazgos (cuatro medios,
cuatro bajos), ninguno de producto**: tres filas o grupos de filas del catálogo con significado o efecto
equivocados, el límite de los códigos genéricos sin declarar y cuatro imprecisiones documentales; las
promesas de la pieza (cobertura completa código↔catálogo, registro de prefijos, colisiones completas,
batería determinista y no-vacua para la estructura) se cumplieron.

## Hallazgos y correcciones

| # | Gravedad | Hallazgo | Corrección aplicada | Regresión |
| --- | --- | --- | --- | --- |
| 1 | media | (`diario`, `O-00`) documentaba el significado del ORQUESTADOR («instante inválido o anterior al último»); el Diario solo lo emite para «excepción al aplicar {metodo}» (`diario.py:167`, docstring línea 23), y la fila contradecía al propio módulo, a `COLISIONES_ADMITIDAS`, al Documento 0 §2 punto 7 y a notas_deuda (T-61) | Texto del Diario = «operación que lanzó una excepción no recogida: se anota y se reproduce igual» (el propuesto por el revisor) y choque declarado en `CHOQUES_REALES` con su deuda T-61 | `r01_los_pares_con_choque_real_tienen_textos_distintos_por_modulo` |
| 2 | media | Efecto BLOQUEA falso en `Q-01` y `Q-10`: ambas SOLO emiten ADVERTENCIA (`k_calidad.py:292` y `:476`) y el sello SÍ se emite (S-13 liga Q-01 a ADVERTENCIA); contradecía el criterio del §2 punto 3 y la definición de BLOQUEA | Efecto AVISO para ambas filas (el texto de Q-01, «se recorta al hábil anterior», deja de contradecirse a sí mismo) | `r02_el_efecto_BLOQUEA_de_las_reglas_Q_exige_un_BLOQUEO_real` |
| 3 | media | 14 filas RECHAZA que en realidad APRUEBAN con menos cantidad: F-03, F-04, F-06, F-07, F-13, F-14 y F-15 de `control_f` y sus copias del Orquestador; `control_f` devuelve «REDUCIDO» con `cantidad_aprobada > 0` (`control_f.py:260`) y el §2 punto 3 las llamaba «que REDUCE» sin declarar el mapeo | `REDUCE` añadido a `EFECTOS`, conjunto `REGLAS_QUE_REDUCEN` declarado y efecto REDUCE en las 14 filas; §2 punto 3 reescrito y reparto actualizado (182 RECHAZA / 14 REDUCE / 39 BLOQUEA / 38 AVISO / 9 INFORMA) | `r03_las_reglas_que_REDUCEN_no_son_RECHAZA` |
| 4 | media | Textos de códigos genéricos tomados de UNA sola emisión, sin declarar el límite: O-01 del Orquestador (~71 caminos) documentaba solo el «resto_parcial» (T-62 heredaba esa estrechez), O-00 del Orquestador (3 usos, DOS significados) y O-02 (12 usos de idempotencia) | Textos de nivel FAMILIA para O-00, O-01 y O-02 del Orquestador con `"familia": True` (el de O-01, el propuesto por el revisor) y límite declarado en §2 punto 1 y §5 del Documento 0 | `r04_codigos_con_muchas_emisiones_llevan_texto_de_familia` |
| 5 | baja | «Quince pares» frente a DIECISÉIS reales (`COLISIONES_ADMITIDAS` tiene 16, todos necesarios) | «dieciséis» en los cinco sitios: Documento 0 (§1 y §2 punto 7), LEEME (párrafo de fecha y punto «Comprobado») y notas_briefing | `r05_el_recuento_de_pares_admitidos_es_el_declarado` |
| 6 | baja | `Deuda_tecnica.md` declarado como cambiado (T-60 RESUELTO, T-61, T-62) pero NO viaja en el ZIP: el cambio no era verificable en la entrega | §4 del Documento 0, LEEME y notas_briefing citan que su contenido viaja resumido en `notas_deuda.md` de la carpeta, que abre con esa nota | Ninguna (documental) |
| 7 | baja | Criterio de retiradas sin declarar: el catálogo daba de alta E-06 pero no D-03 «retirado en V0.17» ni G-07 «no se usa», citados por el LEEME | Criterio declarado en §2 punto 1 del Documento 0, en el docstring del módulo y en el punto «Comprobado» del LEEME: solo la retirada del contrato vigente (E-06) entra en el catálogo; las históricas siguen en el LEEME | Ninguna (documental; el `r06` opcional del revisor no se añade porque el criterio declarado deja fuera del catálogo a D-03 a propósito) |
| 8 | baja | Exactitud menor: «en los 21 módulos» (se recorren 21, pero solo 18 contienen constantes: consola, motor y parametros no emiten ninguna) y «dos letras mayúsculas» frente a la expresión real `[A-Z]{1,2}` (una o dos) | Las frases ajustadas en LEEME, Documento 0 (§1 y §2 punto 5), notas_briefing y docstring del módulo, con un ejemplo de una letra («V-01») | Ninguna (documental) |

Observaciones del revisor, todas atendidas sin cambio de código: (1) `catalogo_codigos.md` es un preámbulo
más la salida exacta de `como_markdown()`: la frase del §4 del Documento 0 se ajustó a lo que el fichero es;
(2) Q-04, Q-05 y Q-09 son MIXTAS según el factor de la política: anotadas fila a fila en §2 punto 3, que
declara por qué quedan en BLOQUEA (efecto dominante, falla cerrado); (3) (`dimensionado`, `F-11`) con
BLOQUEA como frontera de viabilidad se mantiene; (4) el reparto AVISO/RECHAZA de la familia O cuadraba con
el mecanismo real y no cambió. Además, la matización del §5 del informe quedó reflejada: T-61 y T-62 siguen
abiertas como decisión del operador, y la descripción de T-62 está matizada en el Documento 0 (§2 punto 7 y
§5), el LEEME y notas_deuda (el O-01 del Orquestador es un rechazo genérico y el «resto_parcial» fue solo el
caso que motivó la anotación). T-60 sigue RESUELTO.

## Resultado tras corregir

- La batería queda en **23 comprobaciones** (las 18 de la pieza y las cinco regresiones r01 a r05) y sigue
  determinista: dos ejecuciones consecutivas con salida idéntica byte a byte.
- El lote completo en verde de nuevo: **51 baterías**, todas terminan en «TODAS LAS PRUEBAS PASAN» y sin una
  sola línea FALLA (`salida_pruebas.txt` de esta carpeta, regenerada tras las correcciones).
- **No-vacuidad de las regresiones, verificada revirtiendo cada corrección**: los textos antiguos de
  O-00/O-01/O-02 del Orquestador hacen fallar r04 (y r01 si el texto del Diario converge al del
  Orquestador); Q-01 o Q-10 de vuelta a BLOQUEA hacen fallar r02; F-03 o F-14 de vuelta a RECHAZA hacen
  fallar r03; un par de menos en `COLISIONES_ADMITIDAS` hace fallar r05 (y la comprobación de colisiones);
  y una explicación «CHOQUE REAL» que cite una deuda sin choque declarado hace fallar r01.
- Las sondas del revisor se re-ejecutaron sobre el estado corregido: **S1 y S4 siguen fallando como deben**
  y **S5 sigue cuadrando** (250 códigos distintos; «O-01» ×71, «O-00» ×3, «O-02» ×12); S2 y S3, diseñadas
  contra la entrega SIN corregir, son hoy no-operativas (los valores que inyectan son ya los del catálogo):
  la protección que pedían la dan ahora r01, r02 y r04 en sentido inverso, como se acaba de describir.
- Sin cambios de producto: ni el Orquestador ni ningún validador ni el resto de baterías cambian; el diff
  V0.61 → V0.61 pos-revisión toca solo `validador/catalogo_codigos.py`,
  `pruebas/pruebas_catalogo_codigos.py`, `LEEME.md`, los documentos de `entrega_glm/V0.61/` y las dos
  piezas de la revisión (`informe_revision_independiente.md` y `sondas_revisor_v061.py`, esta última con la
  ruta relativa a la raíz de `marcoC` como única adaptación al original del revisor).
