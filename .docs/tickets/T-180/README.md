# T-180 · Bloque A, Evaluador: hallazgos de la QA r01 de T-163 (CT-04 aplica el criterio del certificado a su soporte, horizonte en la caché del Motor, pruebas que afirman el motivo)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO; H-01 subsanado al cerrar) |
| Pieza | bloque_a (ejecutor: `bloque_a/evaluador.py`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (regla del 12-11-2026, `compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: corrige hallazgos de QA y solo endurece (un certificado exige más condiciones). No cambia contratos CT, esquemas del corpus, la Constitución ni los controles. La única decisión nueva (Holm también con una sola celda candidata) la toma el agente por defecto (`compartida/2026-11-13_decide-el-agente-por-defecto`) y se apunta en `Decisiones_del_operador_Bloque_A.md` §4 e INC-T160-01 |
| Deuda técnica | T-180 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la lleva la sesión coordinadora; este ticket no la toca) |

## Objetivo

Cerrar los hallazgos H-01 a H-03 de la QA r01 de T-163 (`.docs/tickets/T-163/qa.md`): que CT-04 (y con él `certificados_vigentes` y
la revisión) compruebe que el cálculo de soporte de un certificado cumple el criterio del certificado y lo pidió el Evaluador; que
dos celdas de distinto horizonte con las mismas entradas tengan cada una su soporte; y que las pruebas afirmen por qué se revoca y
maten los mutantes N03, N04 y N07 del revisor.

## Alcance

- Entra:
  - `bloque_a/11_Ejecutor/bloque_a/evaluador.py`:
    - `motivo_sin_reejecucion` (la usan CT-04, la emisión, `certificados_vigentes` y la revisión), tras las comprobaciones de T-160 y
      T-163, sin cambiar su orden ni sus mensajes:
      - el soporte lo pidió el Evaluador (`solicitante` AG-20), como su CT-10;
      - el soporte cumple el criterio del certificado (`criterio_desfavorable`, la función de la materialidad al proponer; con la CT-10
        citada «SI» es `criterio_certificado` tal cual) sobre las cifras de su `resultado.payload`, con los umbrales de la
        configuración: `evaluacion.min_certificar` (n_eff), `evaluacion.ece_max`, `evaluacion.alfa_holm` (p de DM-HLN ≤ α, condición
        necesaria de Holm) y, si la CT-10 citada es DENTRO_TOLERANCIA, con las cifras movidas en contra lo que permite su tolerancia.
    - `_umbrales_certificado()`: los tres umbrales, leídos en un solo sitio para la revisión y para la comprobación del soporte.
    - `revisar_certificados`: con una sola celda candidata también se aplica Holm (con una hipótesis es la prueba a α), para que el
      criterio al proponer sea el que CT-04 aplica al soporte y el `holm_superado: true` que escribe el CERT- sea cierto.
    - `_verificar_reejecucion`: la petición FC-EVAL-001 lleva `horizonte` en los parámetros, como `metodo` (H-02).
    - `certificados_vigentes`: solo su docstring (la comprobación nueva entra por `motivo_sin_reejecucion`); la revisión revoca, con
      su motivo, el VIGENTE cuyo soporte no cumple el criterio (por la vía de H-02 de T-163) y vuelve a evaluar la celda.
  - `bloque_a/11_Ejecutor/tests/conftest.py`: el ayudante `certificado_con_reejecucion` con 160 pronósticos calibrados en fechas
    distintas (n_eff 160 ≥ 100), con `horizonte` en la petición y una aserción de que su soporte cumple el criterio.
  - Pruebas: `bloque_a/11_Ejecutor/tests/test_t180_hallazgos_t163.py` (nuevo); `test_t53_evaluacion_y_almacen.py::test_umbral_de_revocacion_ece_sale_de_la_configuracion`
    y `test_t66_evaluacion.py::test_pa10_revocar_y_retirar_siguen_siendo_automaticos` afirman el motivo (H-03 a).
  - `docs/incidencias.md` (INC-T160-01, ampliada con T-180), `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (la
    fila de §4 de la re-ejecución CT-10) y `bloque_a/11_Ejecutor/README.md` si cita la comprobación.
- No entra: otros bloques, `sistema_global/marco_comun_c/`, la Constitución, el corpus (695), el Documento 0, los goldens, `guias.py`,
  `herramientas/`, `motor/evaluacion.py`, lo de las lecciones de `evaluador.py` (`_informe_aprendizaje`, origen de las lecciones: T-161
  r03 en paralelo), la deuda técnica. Atar las entradas del soporte a los PRG resueltos de la celda: se queda como límite en
  INC-T160-01 (no sale barato, ver Diseño).

## Diseño

- **El criterio, en CT-04** (H-01). Las cifras del soporte son las del Registro de cálculos (las escribe el Motor), no las del CERT-.
  Con la CT-10 citada «SI», `criterio_desfavorable(payload, 0, …)` es `criterio_certificado(payload, …)`; con DENTRO_TOLERANCIA, la
  materialidad de un paso (`holgura_tolerancia(tol, 1)`). Un certificado legítimo siempre la pasa: al proponer, `m` cumple el criterio
  con las cifras movidas en contra `holgura(pasos)`, el soporte difiere de `m` en ≤ `holgura(1)` y el criterio es monótono en cada
  cifra, así que el soporte movido `holgura(1)` más queda dentro de lo que `m` ya aguantó (la composición de dos pasos es
  `holgura(2)`). Se comprueba al final, después de las cifras, para que los motivos de T-163 no cambien.
- **La p de DM-HLN y Holm.** Holm es un criterio entre celdas y no se puede rehacer con un solo soporte; su condición necesaria sí:
  el umbral de Holm de cualquier celda es ≤ α, así que la p del soporte tiene que ser ≤ `evaluacion.alfa_holm`. Hasta ahora, con una
  sola celda candidata no se exigía DM (`alfa_k = None`): CT-04 rechazaría entonces un certificado legítimo de una celda con p > α, o
  la emisión dejaría una incidencia Material en cada revisión. Se decide (agente, por defecto, endurece) aplicar Holm también con
  una celda: con una hipótesis, Holm es la prueba a α. Casi nunca cambia nada (el IC del BSS por conglomerados es más exigente que
  DM-HLN con h = 1), y hace cierto el `holm_superado: true` de todo CERT-.
- **El solicitante del soporte.** AG-20, como el de la CT-10. Con la caché del Motor, un soporte servido antes a otro solicitante con
  la misma petición daría su `calc_id`: falla cerrado (no hay otro cliente que pida FC-EVAL-001 con `metodo` y `horizonte`).
- **Horizonte en la caché** (H-02). La clave de la caché del Motor ya lleva la clase (`parametros.clase`, que el Motor pone desde la
  petición) pero no el horizonte. Se pone `horizonte` en los parámetros de la petición del Evaluador, como `metodo`: el cambio queda
  en el cliente que lo necesita y no cambia la clave de ninguna otra ficha. CT-04 no lo exige en el soporte (la comprobación de celda
  sigue siendo la de `horizonte` de la entrada, que el Motor escribe de la petición): un certificado de T-163 sigue valiendo si
  cumple el criterio.
- **Atar las entradas del soporte a los PRG** (límite que sigue). Exigiría recalcular en CT-04 y en cada `certificados_vigentes` las
  entradas de la celda (`resueltos` y `_entradas_celda`) a la fecha del soporte y su huella: depende de F4 y de la configuración
  vigentes (admisibles, contaminación, conglomerados), de modo que un PRG resuelto tarde o un cambio de configuración revocaría un
  certificado legítimo, y lo leen la síntesis, G3 y el backtest en cada ciclo. No sale barato; se queda en INC-T160-01.
- **Contratos CT:** ninguno cambia de forma. **Estado persistido:** el RC gana `horizonte` en los parámetros del soporte; nada se
  migra. Un VIGENTE o PROPUESTO cuyo soporte no cumple el criterio deja de valer y la revisión lo revoca o retira (endurece).
- **Números:** los tres umbrales salen de la configuración (`evaluacion.min_certificar`, `ece_max`, `alfa_holm`, Anexo A) y la
  tolerancia, de la ficha (`servicio.IMPLEMENTADAS["FC-EVAL-001"]["tol"]`). Ningún número nuevo.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Un certificado legítimo deja de pasar CT-04 por la materialidad | Celdas que no se certifican nunca | Demostrado arriba (monótono y `holgura(1)` compuesto); prueba con ECE en el borde frente a SI y DENTRO_TOLERANCIA |
| Holm con una celda cambia lo que se propone | Celdas que antes certificaban y ahora no | Solo si p de DM > α con el IC del BSS > 0 (casi imposible); la suite completa lo comprueba; anotado como decisión |
| Pruebas del revisor que forjan certificados con datos que no cumplen el criterio (ECE 0,1 > q90 0,04) | Fallan tras el cambio | Es lo que H-01 pide cambiar; se anota en `pruebas.md` y las pruebas del ticket usan datos que sí lo cumplen |
| Los mutantes de r01_02 y r01_03 dejan de aplicar | No se puede repetir la ronda de QA | Se conservan las líneas que mutan; se ejecutan todos |
| Otra sesión (T-161 r03) toca `evaluador.py` | Conflicto al integrar | Solo se tocan los métodos de certificados, lejos de lo de las lecciones |

## Criterios de aceptación (binarios)

1. CA-1 (H-01): CT-04 rechaza (ValueError, F6 sin cambios) un PROPUESTO cuyo soporte no cumple el criterio (cada condición por
   separado: n_eff, extremo inferior del IC, ECE frente al q90 y frente al tope, p de DM), con los umbrales que dé la configuración,
   y uno cuyo soporte no pidió AG-20; aprueba el legítimo; con una CT-10 DENTRO_TOLERANCIA aplica la materialidad.
2. CA-2 (H-01): la revisión revoca, con su motivo, un VIGENTE cuyo soporte no cumple el criterio, y `certificados_vigentes` no lo
   devuelve; un VIGENTE legítimo sigue.
3. CA-3 (H-01): con una sola celda candidata, una p de DM-HLN > α impide proponer (Holm con una hipótesis).
4. CA-4 (H-01): el ayudante `certificado_con_reejecucion` escribe un certificado cuyo soporte cumple el criterio (n_eff ≥ 100) y
   las pruebas que lo usan siguen pasando sin cambiar sus aserciones.
5. CA-5 (H-02): dos celdas de la misma clase en H2 y H3 con las mismas entradas se certifican las dos, cada una con su soporte.
6. CA-6 (H-03): t53 y t66 afirman el motivo de la revocación y de la retirada; pruebas que matan N03, N04 y N07.
7. CA-7: las `test_h01_*` y `test_h02_*` de `.docs/tickets/T-163/revisores/r01_01_ataques.py` pasan; el resto también, salvo las que
   forjan un certificado «válido por sí mismo» con datos que no cumplen el criterio (por diseño).
8. CA-8: mutantes de r01_02 (T-163) y r01_03 (T-160) aplican todos; solo viven los equivalentes.
9. CA-9: regresión: `test_t163_hallazgos_t160.py`, `test_t160_reejecucion_certificado.py`, `test_t66_evaluacion.py`, goldens, gates
   ligeros y la suite completa de A en verde (≥ 607); ruff ≤ 2813; mypy A ≤ 109; PB-32 sigue «Superada».

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Soporte de una celda de habilidad débil (las entradas reales): CT-04 rechaza, F6 sin cambios | fallo cerrado / regresión | CA-1 |
| Cada condición del criterio por separado sobre el soporte (con el CERT- coherente) | límite / fallo cerrado | CA-1 |
| Umbrales de la configuración (`min_certificar`, `ece_max`, `alfa_holm` cambiados) | límite | CA-1 |
| Soporte pedido por AG-18 con todo lo demás igual | fallo cerrado | CA-1 |
| ECE en el borde del q90 con la CT-10 SI y DENTRO_TOLERANCIA | límite (materialidad) | CA-1 |
| VIGENTE con soporte débil: revisión, motivo, `certificados_vigentes` | regresión / integración | CA-2 |
| Una celda candidata con `alfa_holm` mínimo | regresión | CA-3 |
| Ayudante: aserción del criterio; pruebas que lo usan | regresión | CA-4 |
| H2 y H3 con las mismas entradas; `horizonte` en los parámetros | regresión | CA-5 |
| t53 y t66 con el motivo; muestra efectiva, Brier de referencia, lote con dos PROPUESTO | regresión (mutantes) | CA-6 |
| `r01_01_ataques.py` de T-163 | regresión | CA-7 |
| `r01_02_mutantes.py` y `r01_03_mutantes.py` en copias desechables | mutantes | CA-8 |
| Vecinas, goldens, gates ligeros, suite de A, cuotas, evidencias de PB-32 | regresión | CA-9 |

## Scripts

`.docs/scripts/mutantes_revisor_ampliado.py` (mutantes del revisor con las pruebas nuevas), `tests/goldens_ct.py`,
`.docs/scripts/evidencias_plan_a.py` (comprobar el mapa; `--pb PB-32`). Ninguno nuevo.

## Registro

- 2026-11-16 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-16 · PLANIFICADO · claude · plan y criterios escritos
- 2026-11-16 · EN CURSO · claude · implementación y pruebas
- 2026-11-16 · EN QA · claude · implementado y probado (`pruebas.md`); commit local «wip local: T-180»; el commit definitivo lo hace la sesión coordinadora
