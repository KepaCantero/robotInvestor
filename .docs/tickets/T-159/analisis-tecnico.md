# T-159 · Análisis técnico

## Causa raíz o motivo

`docs/evidencias_pruebas_bloque_a.md` (15-11-2026, commit `5098b09`) tenía 37 casos «Superada en parte»: queda alguna cláusula
del criterio del plan que el ejecutor podría comprobar y ninguna prueba comprueba. Algunas de esas cláusulas el ejecutor ya las
cumple y solo les faltaba la prueba; otras necesitan una función que el ejecutor no tiene.

## Clasificación de los 37

- **A** (8): la cláusula la cumple ya el código; prueba nueva en `tests/test_t159_extremo_a_extremo.py` y la fila pasa a «Superada».
- **B** (27): falta una función del ejecutor. 17 eran conocidos: los 16 del apartado 2 del plan de la noche (INC-T116-01, -02 y
  -03, y PB-48 de INC-T126-01, que lleva T-158) y PB-26 (INC-T126-01, ronda r02). 10 son nuevos o no tenían incidencia propia y
  van a INC-T159-01; uno de ellos (PB-52) lo descubrió una prueba de este ticket.
- **C** (2): lo que falta solo existe con el modelo real.

| PB | Caso | Clase | Motivo |
| --- | --- | --- | --- |
| PB-02 | Top-3 con menos de tres elegibles | A | El caso sembrado de DIV de extremo a extremo: dos opciones, la de banda marginal fuera por su segunda pasada (registrada en F3), C03 (G3-CON-03) en OK y ningún umbral incumplido. |
| PB-03 | Clase sin ninguna opción elegible | A | ALT con sus candidatas sin PS3: cero opciones, GRIS, motivo por candidata en el técnico, sin tarjeta en el visual. Que el Auditor no registre hallazgo es del modelo real. |
| PB-07 | Consulta que escala a análisis | B | Conocido (INC-T116-03; plan de la noche): no hay respuesta final por CT-03 al acabar el RUN-. |
| PB-08 | Ráfaga de peticiones sin límite | B | Nuevo (INC-T159-01): `peticion` y `consulta` atienden cada mensaje en el momento; no hay cola con prioridad y envejecimiento ni presupuesto por nivel. El p90 de N0 es de tiempo real (C). |
| PB-09 | Cambio de periodicidad por el Broker | B | Nuevo (INC-T159-01): `ht05_planificador.proxima_ejecucion` existe pero nada la llama con el P-01 de F10, y el P-01 que escribe el CT-04 guarda solo la hora de entrega. |
| PB-10 | Configuración no permitida rechazada parcialmente | B | Conocido (INC-T116-01): F10 cambia también en P-03. |
| PB-11 | Decisión del Broker sin alterar el análisis | B | Conocido (INC-T116-03): sin lección de producto enviadas frente a descartadas. |
| PB-13 | GC0 negativo con arrastre verificado | B | Nuevo (INC-T159-01): la rotación exploratoria va en celdas fijas (`seleccion.rotacion_exploratoria_celdas`, [PROPUESTO] hasta T-57); `presupuesto_uc.rotacion_exploratoria` (0,20) no lo lee nadie, así que el 15–25 % no se puede medir. AS-06 es del Auditor (C). |
| PB-17 | Ampliación de presupuesto | B | Conocido (INC-T116-02): la AUT- no lleva CPI ni EAC. |
| PB-18 | Cola saturada y apertura de instancia | B | Nuevo (INC-T159-01): HT-08 solo abre por cola; sin disparo por tiempo, sin objetivo de tiempo de ingesta y sin ORD- de cierre. |
| PB-19 | Agente de instancia única saturado | B | Conocido (INC-T116-03): el CAR- solo se anota. |
| PB-20 | Instrucción incrustada en una fuente | B | Nuevo en lo que falta (INC-T159-01): la fuente no se degrada ni se borra en F9 con su línea de baja, y G3-EST-06 no existe en HT-09. |
| PB-21 | Credencial en un mensaje | B | Conocido (INC-T116-03): la incidencia no lleva el tipo de dato protegido. |
| PB-24 | Enlace roto y borrado con registro de bajas | B | Nuevo (INC-T159-01): el ejecutor solo invoca HT-02; la baja no se propaga (EVD FUENTE_RETIRADA, revisión en F3, CT-21 del mes). |
| PB-25 | Contenido cambiado y retractación | C | El recálculo de Q con su motivo lo hace el Documentador (modelo real); la baja con su línea ya está probada (HT-02). |
| PB-26 | Clasificación temática y orden por calidad | B | Conocido (INC-T126-01, r02): el desempate por fecha no alcanza a las fichas sin año (documento vivo, F9). Las 30 altas las hacen los Documentadores (C). |
| PB-29 | Contar raíces, no menciones | B | Nuevo en lo que falta (INC-T159-01): `grado_independencia` es siempre RAIZ y las raíces se cuentan por fuente (veinte medios, veinte raíces); el ejecutor no lee derivadas del Curador. |
| PB-30 | Cifra sin artefacto bloqueada por G3 | A | El caso de extremo a extremo: C08 bloquea, CT-14, retirada, segundo G3V- APTO; dos G3V- en HA y la cifra fuera de la entrega. El tiempo de dictamen es de tiempo real. |
| PB-32 | Certificación de un horizonte | B | Conocido (INC-T116-03): sin la re-ejecución CT-10 coincidente. |
| PB-33 | Revocación de certificado por deterioro | B | Conocido (INC-T116-03): sin la sección «Novedades» de F6. |
| PB-34 | Fuga de información en evaluación | B | Nuevo (INC-T159-01): la resolución con fuga queda FALLIDA y fuera, pero no se registra la corrección en F6. |
| PB-35 | Recalibración dentro de bandas con sombra | B | Nuevo (INC-T159-01): la selección calcula el top-3 en sombra, pero nada cierra el AJU- EN_SOMBRA (CONFIRMADO o REVERTIDO con DM-HLN). |
| PB-36 | Recalibración fuera de bandas rechazada | B | Conocido (INC-T116-03). |
| PB-38 | Objeción fuerte sin resolver impide el top-3 | B | Conocido (INC-T116-03). |
| PB-39 | Informe visual con legibilidad < 70 | A | El ciclo bloquea el visual por C12, pide la reescritura y entrega el reescrito con 70 o más; si sigue por debajo, no se entrega ningún visual. |
| PB-41 | Coherencia entre entregables y entre clases | A | Con un factor común sembrado en RF, INM y RV: clúster común de los tres tipos, `apuestas_independientes` = clústeres, y las mismas OPP- en el mismo orden en los tres entregables. El recuento del Auditor es del modelo real. |
| PB-44 | Historial de aciertos honesto | A | Nueve ciclos con una invalidada, una descartada y una NO_RESOLUBLE: el historial es el recuento de F4 y F3, la NO_RESOLUBLE se declara, `significativo` false con su nota, el mismo dato en los tres entregables y C01 (G3-CON-18) en OK. |
| PB-46 | Fiabilidad de fuentes de opinión | C | La recalificación de Q y el orden en F9 los hace el Buscador con el modelo real (T-125). |
| PB-47 | Estados de madurez | A | Con ML-CLUS-001 en DOCUMENTADO: el Motor lo rechaza, la entrega no cita cifras suyas, declara la limitación y no dice «validado». |
| PB-48 | Conflicto de normas | B | Conocido (INC-T126-01); lo lleva T-158: no se toca. |
| PB-50 | Horizontes según la clase de activo | B | Conocido (INC-T116-03). |
| PB-52 | Modo degradado: herramienta caída | B | **Descubierto por una prueba** (INC-T159-01): con HT-09 caído, `Bloque.ciclo` termina con la excepción; no hay CT-14, ni G3 manual con etiqueta, ni RUN- en F5, ni incidencia. Lo que sí cumple (nada se entrega, nada se congela, ningún APTO) queda probado. |
| PB-58 | Solicitud y provisión de una credencial | B | Conocido (INC-T116-03). |
| PB-61 | Consulta bloqueante al Broker con vencimiento | B | Conocido (INC-T116-03). |
| PB-62 | Filtro, agrupación y recurrencia de consultas | B | Conocido (INC-T116-03). |
| PB-64 | Evaluación de H5 por hitos y degradación | B | Conocido (INC-T116-03). |
| PB-67 | Seguimiento que propone el envío al Bloque B | A | Un C6 del ejecutor da PROPONER_ENVIO_A_B con HT-09 de seguimiento APTO y su paquete; el único mensaje fuera del bloque es el CT-24 al Broker y F3 no cambia. |

Nota sobre los (C): por la definición del documento de evidencias, una fila cuya única cláusula pendiente es del modelo real
podría ser «Superada» con esa cláusula en «No comprueba». El encargo pide dejarlas «en parte»; se dejan así, y la QA o el
operador pueden decidir moverlas.

## Evidencia

- Pruebas: `bloque_a/11_Ejecutor/tests/test_t159_extremo_a_extremo.py` (10 pruebas, unos 45 s).
- PB-52 (B descubierto), desde `bloque_a/11_Ejecutor`: con `sintesis.ht09_validar` sustituida por una función que lanza
  `RuntimeError`, `Bloque.ciclo(AS_OF, alcance={"clases": ["RV"]})` lanza esa excepción; después, HA no tiene ningún G3V-, F5 no
  tiene el RUN- y no hay incidencia HERRAMIENTA (la prueba `test_pb52_con_ht09_caido_nunca_hay_apto_por_defecto_ni_entrega` fija
  la parte que sí se cumple). En `Bloque._validar_g3` no hay `try` alrededor de `sint.ht09_validar`.
- PB-09: `grep -rn proxima_ejecucion bloque_a/11_Ejecutor/bloque_a` solo encuentra su definición; `Bloque.decision` escribe
  P-01 como `f"{periodicidad} · {horario}"` con la hora de entrega.
- PB-13: `grep -rn "rotacion_exploratoria\b" bloque_a/11_Ejecutor/bloque_a` no encuentra ningún lector de
  `presupuesto_uc.rotacion_exploratoria`.
- PB-18: `herramientas/ht08_monitor.py` solo emite `ORD` con `accion: ABRIR` y `CAR`.
- PB-29: `orquestacion.py`, `_registrar_evidencia_clase`: `"grado_independencia": "RAIZ"` y `f["_raices"][evd.get("_raiz", fuente)]`.
- PB-34 y PB-35: `evaluador.py` no escribe en F6 ninguna corrección por fuga ni cierra un AJU- EN_SOMBRA.
- PB-24 y PB-20: `grep -rn "FUENTE_RETIRADA\|CT-21" bloque_a/11_Ejecutor/bloque_a` solo da la matriz de canales.

## Implementación

- Archivos cambiados y por qué:
  - `bloque_a/11_Ejecutor/tests/test_t159_extremo_a_extremo.py` (nuevo): PB-02, PB-03, PB-30, PB-39 (dos), PB-41, PB-44, PB-47,
    PB-67 y la parte cumplida de PB-52.
  - `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`: PB-02, -03, -30, -39, -41, -44, -47 y -67 pasan a AUTOMATICA con sus
    pruebas y su «comprueba»; PB-52 cita su prueba nueva y sigue PARCIAL; los «no comprueba» de PB-08, -09, -13, -18, -20, -24,
    -29, -34, -35 y -52 dicen qué función falta (INC-T159-01).
  - `bloque_a/11_Ejecutor/tests/test_fase4_mapa.py`: el caso parametrizado que estropeaba el «no comprueba» de PB-02 (que ya no es
    PARCIAL y admite «no comprueba» vacío) lo hace ahora sobre PB-08, que sigue PARCIAL. La comprobación no cambia.
  - `docs/evidencias_pruebas_bloque_a.md`: regenerado.
  - `docs/incidencias.md`: INC-T159-01.
- Decisiones y desviaciones:
  - Siembras: el Analista simulado (`mock_respuestas._ficha`) para PB-02 y PB-03, el Redactor simulado (`_redactor`) para PB-39,
    un proveedor de pruebas con un factor común (PB-41) o con una serie que deja de publicarse (PB-44), la madurez de una ficha que
    lee el Motor (PB-47) y la construcción del paquete de síntesis (PB-30, para meter la cifra sin artefacto). Ninguna toca el
    código del ejecutor.
  - Escala de los datos sintéticos: PB-02 tiene seis candidatas DIV (no siete); PB-03, una finalista ALT (el universo tiene dos
    ámbitos ALT y uno pasa el cribado); PB-44 no reproduce las 28 opciones del plan. Se afirma la regla y queda dicho en el mapa.
  - PB-02: la «E = 58» del plan no existe como total de HT-03 (múltiplos de 5, dimensiones de 10 en 10); se siembra una segunda
    pasada de media exacta 57,5, que HT-03 redondea a 55.
  - G3-CON-03 es C03 de HT-09 y G3-CON-18 se cubre con C01 (el historial con su tamaño muestral es obligatorio en el paquete).
- Límites conocidos: los (B) y los (C) siguen «Superada en parte»; los B nuevos necesitan un ticket (INC-T159-01).
- Comandos exactos, desde `bloque_a/11_Ejecutor`:
  - `../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t159_extremo_a_extremo.py tests/test_fase4_mapa.py`
  - desde la raíz: `.venv/bin/python .docs/scripts/evidencias_plan_a.py` (comprobación) y `--ejecutar` (regenera).
