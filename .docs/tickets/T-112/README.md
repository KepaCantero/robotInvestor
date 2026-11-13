# T-112 · Bloque A: Motor Fase 2, fichas P0 y P1 del Catálogo V5.0

| Campo | Valor |
| --- | --- |
| Estado | EN QA (ronda r02; la QA r02, pendiente por indicación del operador) |
| Pieza | `bloque_a/11_Ejecutor` (`bloque_a/motor/`) y el Catálogo del Motor (`bloque_a/04_Motor_conocimiento_y_catalogo/`, corpus congelado) |
| Planifica · implementa · QA | claude · claude con cuatro agentes, uno por grupo de fichas; integración, Claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-12: «2) sí, te autorizo» (promover en el Catálogo las fichas que superen sus casos de control, re-congelando el corpus). 2026-11-13: «continuamos con la implementación del bloque A»; es el punto 3 del orden de tareas obligatorias de A («las fichas documentadas que más pesan en la selección, por prioridad, no todas») |
| Deuda técnica | T-112 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (Fase 2 del plan de fases de `CLAUDE.md`) |

## Objetivo

Dar cálculos citables a las fichas de prioridad P0 y P1 que hoy no los tienen: 25 DOCUMENTADO y 11 «Implementado (heredado)» de la línea V3.0, que no tienen código en el ejecutor vigente. Cada una se implementa con sus casos de control (§20.2 del Catálogo) y pasa a IMPLEMENTADO si los supera. Las 10 de P2 quedan fuera.

## Alcance

**Entra: las 36 fichas, en cuatro grupos y un servicio**

| Grupo | Módulo | Fichas |
| --- | --- | --- |
| S · estadística y series | `motor/fichas_series.py` | ST-INF-001, FX-BRK-001, FX-STL-001, FX-REGIME-001, REG-HMM-001, FX-COINT-001, BIB-MET-001, TEM-DIFF-001 |
| R · riesgo, simulación, backtest y modelos | `motor/fichas_riesgo.py` | RISK-VAR-001, SIM-MC-001, SCN-H-001, BT-DSR-001, BT-PBO-001, BT-VAR-001, ML-CAL-001, ML-PRED-001, DEC-VOI-001 |
| V · valoración de RV, RF, FX y DER | `motor/fichas_valoracion.py` | ACC-ERP-001, ACC-FACT-001, ACC-VAL-001, FIR-PRICE-001, FIR-CURVE-001, FIR-CARRY-001, FIR-SPREAD-001, FX-MOM-001, FX-PPA-001, DER-OPT-001 |
| P · inmobiliario, materias primas, cripto y alternativos | `motor/fichas_reales.py` | REI-CAP-001, REI-FFO-001, REI-NAV-001, CMD-INV-001, CMD-RETDEC-001, CHR-FLOW-001, CHR-FUND-001, ALT-DESMOOTH-001 |
| Servicio | `motor/servicio.py` | AUD-REX-001, la re-ejecución independiente CT-10 que ya existe (`Motor.reejecutar`): solo le faltan sus casos de control |

**Entra también:**
- la integración en `servicio.py`: `IMPLEMENTADAS`, `CASOS_CONTROL` y `FASE1` (que pasa a llamarse `ESTRICTAS` y cubre la Fase 1 y la Fase 2);
- las fichas promovidas salen de `DOCUMENTADAS_CON_CODIGO`;
- la promoción en el Catálogo con `.docs/scripts/promover_fichas_catalogo.py`, con la etiqueta T-112, y el corpus re-congelado en el mismo commit.

**No entra:**
- las 10 fichas P2;
- los datos reales, porque la fuente está por decidir;
- la copia `.docx` del Catálogo;
- VALIDADO, que pasa por las baterías de `09_Pruebas` (Fase 4);
- los hallazgos de T-108, que se resuelven aparte. Las lecciones de T-108 sí se aplican desde el principio (§Diseño).

## Diseño

Todo lo de T-106, más las correcciones de sus tres QA, aplicadas desde el principio:

- **Manejador.** Firma `fn(ent, params) -> (resultado, limitaciones)`, con:
  - `PARAMETROS_POR_DEFECTO`, sacados del campo «Parámetros» de cada ficha;
  - `CASOS_CONTROL`, sacados de su «Verificación»;
  - `ADVERTENCIAS`, sacadas de sus «Supuestos y limitaciones», en `resultado["advertencias"]` y no como limitaciones.
- **Umbrales fijos (T-106, H-14).** Los umbrales de rechazo y de limitación y los rangos admitidos van en un diccionario `UMBRALES` por ficha. Una petición que traiga uno se rechaza («umbral fijo de la ficha»).
- **Dominio de cada parámetro (T-108, H-24).** Todo parámetro de la petición tiene tipo y rango: ventana entera positiva, nivel en (0, 1), lo que diga la ficha. Lo que la ficha no fija se toma de otra ficha del Catálogo y se cita, o se declara en INC-T112-01 `[PROPUESTO]`.
- **Fallo cerrado:**
  - entradas mal formadas, «Aclaración y rechazo» y «Entradas mínimas» dan `ErrorFicha`;
  - ninguna cifra no finita en el resultado: la ficha rechaza, o da `None` con una limitación si la ficha lo prevé, y se declara;
  - las fichas nuevas entran en `ESTRICTAS`, donde el Motor también rechaza cualquier no finito.
- **Determinismo.** Las fichas con azar (SIM-MC, SCN-H, BT-PBO, ML-PRED, bootstrap) usan una semilla explícita: la de la petición, o una por defecto en `PARAMETROS_POR_DEFECTO`. Dos pasadas iguales dan el mismo resultado.
- **Casos de control que prueban la identidad entera (T-106, H-08).** Cada caso comprueba lo que dice la «Verificación», con datos que no anulen sus términos. Para que un caso cuente, tiene que poder fallar.
- **Oráculos independientes en las pruebas (T-106, H-18).** Cada ficha tiene al menos una prueba que recalcula su resultado a mano o por otra vía, sin llamar al código de la ficha.
- **Dependencias:**
  - solo numpy, scipy y pandas, que son dependencias de A;
  - statsmodels y scikit-learn no son dependencias de A y no se usan: Markov switching, HMM y cointegración se escriben con numpy y scipy;
  - si una ficha necesita otra, la importa del módulo de su grupo; por ejemplo, BT-VAR usa RISK-VAR.
- **Lo que ya tiene código:**
  - ACC-ERP-001, FX-MOM-001 y REI-CAP-001 tienen código en `servicio.py` o `operaciones.py` y siguen en `DOCUMENTADAS_CON_CODIGO`. Su grupo los revisa frente a la ficha y los conserva o rehace en su módulo;
  - las 11 heredadas no tienen código en el ejecutor: se implementan desde la ficha. No se usa `99_Historico*`.
- **Estado persistido.** No cambia de forma: solo entran entradas CASOS_CONTROL nuevas en RC.
- **Números.** Todos salen de la ficha, de otra ficha que se cita o de INC-T112-01 `[PROPUESTO]`, que va a T-57.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Una ficha sin «Verificación» comprobable | No se puede promover | No se promueve: queda con código y DOCUMENTADO, en `DOCUMENTADAS_CON_CODIGO`, y se declara |
| Métodos iterativos (Markov switching, HMM, NSS, volatilidad implícita) que no convergen | Cifras inestables | Rechazo con DATOS_INSUFICIENTES o CONVERGENCIA si no converge en el tope de iteraciones de la ficha; semilla e inicialización fijas |
| Cuatro agentes a la vez | Carga de la máquina y conflictos en `servicio.py` | Cada agente solo toca su módulo y su fichero de pruebas, y solo ejecuta sus pruebas. La integración en `servicio.py` la hace Claude |
| Una ficha que pide datos que el ejecutor no da (precios en tiempo real, flujos, balances) | No se puede calcular con HT-01 | Los datos llegan en `valores`, como en T-106. La limitación se declara y el analista los aporta con su fuente |

## Criterios de aceptación (binarios)

1. CA-1: cada una de las 36 fichas tiene manejador y casos de control de su «Verificación», y los supera (`verificar_casos_control`, registrado en RC). Una ficha que no los supera no se promueve y se declara.
2. CA-2: el Motor sirve exactamente las fichas con código e IMPLEMENTADO en el Catálogo.
3. CA-3: cada ficha rechaza según su «Aclaración y rechazo» y sus «Entradas mínimas», y es determinista. Ningún umbral de la ficha se puede cambiar desde la petición, y todo parámetro de la petición tiene dominio.
4. CA-4: cada ficha tiene al menos una prueba con un oráculo independiente. Los mutantes de su fórmula principal mueren ante sus casos de control o sus pruebas.
5. CA-5: en el Catálogo, las promovidas pasan a IMPLEMENTADO en su fila y en su ficha, el §1.3 cuadra y el corpus se re-congela en el mismo commit, con el motivo.
6. CA-6: el gate da 12/12, sin subir cuotas, y A sube de las 1481 pruebas de hoy.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_fase2_series.py`, `tests/test_fase2_riesgo.py`, `tests/test_fase2_valoracion.py`, `tests/test_fase2_reales.py` | Casos de control, rechazos, dominio de parámetros, umbrales fijos, determinismo y oráculos | CA-1, CA-3, CA-4 |
| `tests/test_t112_motor.py` | Integración: coherencia código ↔ Catálogo, RC, CT-09 por ficha, AUD-REX y la re-ejecución | CA-1, CA-2 |
| Mutantes por grupo (scripts en `revisores/`) | Mutación | CA-4 |
| `.docs/scripts/promover_fichas_catalogo.py --etiqueta T-112` | Promoción | CA-5 |
| `./tools/check_all.sh` | Gate | CA-6 |

## Scripts

`.docs/scripts/promover_fichas_catalogo.py` (de T-106) y `.docs/scripts/commit_limpio.sh`.

## Registro

- 2026-11-13 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-13 · PLANIFICADO · 36 fichas en cuatro grupos y AUD-REX; lecciones de las QA de T-106 aplicadas desde el diseño
- 2026-11-13 · EN QA · 35 fichas en cuatro módulos y AUD-REX-001 (CT-10) en el servicio, todas con sus casos de control superados (140 en la Fase 2 y 5 de AUD-REX); promovidas en el Catálogo (71 IMPLEMENTADO, 10 DOCUMENTADO) y corpus re-congelado; decisiones de método en INC-T112-01 y CT-10 en INC-T112-02; A con 3319 pruebas
- 2026-11-13 · NO APTO · QA r01 (revisor nuevo, commit `efd1bb3`): H-01 alto (parámetros de tamaño sin cota: una petición agotaba la memoria o colgaba el ejecutor), H-02, H-04, H-07 y H-08 medios, H-03, H-05 y H-06 bajos
- 2026-11-13 · EN QA · Ronda r02:
  - cotas de tamaño en `UMBRALES` en los cuatro grupos, y `MemoryError` y `RecursionError` pasan a RECHAZADO;
  - R y P rechazan los parámetros no declarados;
  - EVT y GARCH con tolerancias fijadas;
  - las fichas reciben la configuración del Motor y la fecha de corte, y rechazan los datos posteriores;
  - semillas: dos distintas se rechazan y el artefacto registra la usada;
  - la fecha de corte entra en la clave de la caché;
  - AUD-REX-001 tiene un caso con parámetros;
  - pruebas que matan los mutantes de H-08.

  El operador pide parar antes de la QA r02 por su límite de consumo semanal.
