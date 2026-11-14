# T-119 · Bloque A: Motor, fichas P2 del Catálogo V5.0

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | `bloque_a/11_Ejecutor` (`bloque_a/motor/`) y el Catálogo del Motor (`bloque_a/04_Motor_conocimiento_y_catalogo/`, corpus congelado) |
| Planifica · implementa · QA | claude (un agente, en una copia de trabajo propia, rama `p2-trabajo`) · el mismo · un revisor que no implementó |
| Aprobación del operador | 2026-11-12: autorización para promover en el Catálogo las fichas que superen sus casos de control, re-congelando el corpus (la misma de T-106 y T-112). Las decisiones de método que la ficha deja abiertas las toma el agente y las apunta como `[PROPUESTO]` |
| Deuda técnica | T-119 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (continuación de la Fase 2 del plan de fases de `CLAUDE.md`) |

## Objetivo

Dar cálculos citables a las 10 fichas de prioridad P2 que el Catálogo V5.0 aún daba por DOCUMENTADO. Cada una se implementa con sus casos de control (§20.2 del Catálogo) y pasa a IMPLEMENTADO si los supera. Es la continuación de T-112, con su mismo método.

## Alcance

**Entra: las 10 fichas, en un módulo nuevo**

| Ficha | Qué calcula | Módulo MC | Clase de cifra | Tolerancia |
| --- | --- | --- | --- | --- |
| FIR-CRED-001 | Merton agregado: distancia al impago, PD y diferencial implícito de un segmento | MC-09 | ESTADISTICA | 1e-6 |
| FX-BEER-001 | Tipo de cambio real de equilibrio (DOLS o Johansen) y desalineamiento | MC-03 | ESTADISTICA | 1e-6 |
| CMD-REAL-001 | Precio real, percentil, tendencia real y razón precio/coste marginal | MC-09 | ESTADISTICA | 1e-10 |
| REI-LEV-001 | Apalancamiento, vencimientos a 24 meses, impacto en FFO, LTV estresado y *covenants* | MC-09 | DETERMINISTA | 1e-10 |
| CHR-ONCHAIN-001 | MVRV, MVRV-Z, NVT y señal NVT con sus percentiles | MC-09 | ESTADISTICA | 1e-10 |
| CHR-TOKEN-001 | FDV/capitalización, inflación neta, desbloqueos, rendimiento real de *staking* y concentración | MC-09 | DETERMINISTA | 1e-10 |
| PRV-PME-001 | KS-PME, alfa directo, PME+, TIR, TVPI y DPI | MC-09 | DETERMINISTA | 1e-8 |
| PRV-CF-001 | TIR, múltiplos, curva J y proyección de Takahashi-Alexander | MC-09 | DETERMINISTA | 1e-8 |
| ALT-HF-001 | Exposición factorial de una estrategia hedge, con desuavizado previo | MC-09 | ESTADISTICA | 1e-8 |
| ALT-AUC-001 | Índice de coleccionables por ventas repetidas o regresión hedónica | MC-09 | ESTADISTICA | 1e-6 |

**Entra también:**
- la integración en `servicio.py`: `MODULOS_P2`, `P2` y `ESTRICTAS = FASE1 | FASE2 | P2`;
- la promoción en el Catálogo con `.docs/scripts/promover_fichas_catalogo.py --etiqueta "ejecutor, casos de control registrados (T-119)"` y el corpus re-congelado en el mismo commit;
- las pruebas que daban por hecho que quedaba una ficha DOCUMENTADO, adaptadas;
- `CLAUDE.md` («Trampas conocidas») y el README del ejecutor, que citan los recuentos.

**No entra:**
- los datos reales: las fichas reciben sus datos en línea, con su fuente, como en T-106 y T-112;
- la copia `.docx` del Catálogo;
- VALIDADO, que pasa por las baterías de `09_Pruebas` (Fase 4);
- la QA, que hace otro agente.

## Diseño

Todo lo de T-112, con las correcciones de sus dos QA aplicadas desde el principio:

- **Manejador.** Firma `fn(ent, params) -> (resultado, limitaciones)`, en `motor/fichas_p2.py`, con `PARAMETROS_POR_DEFECTO` (campo «Parámetros»), `UMBRALES`, `ADVERTENCIAS` («Supuestos y limitaciones», en `resultado["advertencias"]`), `FICHAS` y `CASOS_CONTROL` («Verificación»). Las utilidades de validación son las de `fichas_reales`.
- **Contratos CT afectados:** ninguno cambia de forma. CT-09 sirve diez fichas más y CT-10 las re-ejecuta.
- **Estado persistido:** no cambia de forma. Solo entran entradas nuevas en el Registro de cálculos.
- **Cotas (H-01 de T-112).** Todo parámetro de tamaño y toda lista de datos en línea tiene cota superior en `UMBRALES`, comprobada antes de recorrerla. Además, una cifra de entrada de magnitud mayor que 1e100 se rechaza antes de calcular.
- **Parámetros (H-02).** Un umbral de `UMBRALES` en la petición se rechaza, y también un parámetro que la ficha no declara (salvo `clase`, que añade el servicio).
- **Fallo cerrado.** «Aclaración y rechazo» y «Entradas mínimas» dan `ErrorFicha`. Ninguna cifra no finita en el resultado: lo comprueba la envoltura `_cerrado`, y las diez fichas entran en `ESTRICTAS`, donde el Motor también lo comprueba. Un bloque opcional sin datos se entrega como `null` y se declara.
- **Configuración y fecha de corte (H-04 y H-07).** FX-BEER-001 lee `evaluacion.nivel_ic` de `ent["configuracion"]`. Un dato observado posterior a `ent["fecha_corte"]` se rechaza; las fechas contractuales futuras (vencimientos, desbloqueos) no son observaciones.
- **Semillas (H-05).** Ninguna de las diez usa azar: todas declaran semilla `null`. Una `semilla` en los parámetros se rechaza como no declarada; el servicio ya rechaza dos semillas distintas y registra la de la petición.
- **Frontera con el Bloque B (1.6).** Las fichas con componentes entregan solo el agregado y su dispersión.
- **Dependencias.** Solo numpy, scipy y pandas. ALT-HF-001 usa la regresión de ACC-FACT-001 y el AR(1) de ALT-DESMOOTH-001; FX-BEER-001, el ADF, Johansen y las tablas de FX-COINT-001; CMD-REAL-001, el Mann-Kendall de FX-TREND-001.
- **Números.** Todos salen de la ficha, de otra ficha que se cita, de la configuración o de INC-T119-01 `[PROPUESTO]`, que va a T-57.
- **Decisiones del operador usadas como `[PROPUESTO]`:** las de INC-T119-01 (`docs/incidencias.md`).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Una ficha que pide datos que el repositorio no tiene (en cadena, flujos privados, subastas) | No se puede calcular con HT-01 | Los datos llegan en `valores`, con su fuente declarada; sin fuente, la ficha rechaza. Si aun así no se pudiera implementar con honradez, la ficha se queda en DOCUMENTADO y se declara |
| Métodos iterativos (sistema de Merton, TIR) que no convergen | Cifras inestables | Raíces de Brent con horquilla demostrada, tolerancia y tope de iteraciones fijos; si no converge o no hay raíz, rechazo o `null` declarado |
| Casos de control que no pueden fallar | Promoción sin garantía | Cada caso recalcula el valor esperado por otra vía y falla con las cifras movidas una millonésima; mutantes |
| Otras pruebas daban por hecho que quedaba una ficha DOCUMENTADO | Regresiones rojas al promover | Se adaptan conservando la regla que comprobaban |
| Máquina compartida | Pruebas lentas | Solo las pruebas del módulo mientras se trabaja; la suite completa de A, una vez |

## Criterios de aceptación (binarios)

1. CA-1: cada una de las 10 fichas tiene manejador y casos de control de su «Verificación», y los supera (`verificar_casos_control`, registrado en RC). Una ficha que no los supera no se promueve y se declara.
2. CA-2: el Motor sirve por CT-09 exactamente las fichas con código e IMPLEMENTADO en el Catálogo, y re-ejecuta por CT-10 los cálculos de las diez con coincidencia exacta.
3. CA-3: cada ficha rechaza según su «Aclaración y rechazo» y sus «Entradas mínimas». Ningún umbral se cambia desde la petición, todo parámetro tiene dominio y cota, toda lista de datos tiene cota, y un parámetro no declarado se rechaza.
4. CA-4: nada no finito se sirve, ninguna excepción escapa de `Motor.servir`, un dato posterior a la fecha de corte se rechaza y el resultado es el mismo en dos procesos.
5. CA-5: cada ficha tiene al menos una prueba con un oráculo independiente, y los mutantes de sus fórmulas, cotas y reglas mueren ante sus casos de control o sus pruebas.
6. CA-6: en el Catálogo, las promovidas pasan a IMPLEMENTADO en su fila y en su ficha, el §1.3 cuadra y el corpus se re-congela en el mismo commit, con el motivo.
7. CA-7: las pruebas de A suben, las cuotas de ruff y mypy no suben, y el corpus, las referencias, los secretos y los nombres NFC pasan.

## Plan de pruebas

| Prueba | Tipo (nominal, límite, fallo cerrado, regresión, migración, integración) | Criterio |
| --- | --- | --- |
| `tests/test_t119_p2.py`: casos de control y que cada uno puede fallar | Nominal | CA-1 |
| `tests/test_t119_p2.py`: rechazos por ficha, dominio y cota de cada parámetro, cota de cada lista, umbrales fijos, erratas | Límite y fallo cerrado | CA-3 |
| `tests/test_t119_p2.py`: hojas hostiles, magnitud, fecha de corte, determinismo | Fallo cerrado | CA-4 |
| `tests/test_t119_p2.py`: oráculos independientes por ficha | Nominal | CA-5 |
| `tests/test_t119_motor.py`: Catálogo, CT-09, RC, CT-10, configuración, semillas, entradas hostiles por el servicio, dos procesos | Integración | CA-1, CA-2, CA-4, CA-6 |
| `.docs/tickets/T-119/revisores/impl_p2_mutantes.py` | Mutación | CA-5 |
| `tests/test_fase2_*.py`, `test_t112_motor.py`, `test_t106_*.py`, `test_t87_contratos.py`, `test_t65_resto_t53.py`, `test_unitarias.py` | Regresión | CA-2, CA-7 |
| Suite completa de A, ruff, mypy, `corpus_integridad.py`, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | Gate | CA-7 |

## Scripts

- `.docs/scripts/nuevo_ticket.sh` y `.docs/scripts/promover_fichas_catalogo.py` (de T-106; T-119 le añade que el §1.3 pueda quedar sin fichas DOCUMENTADO y la mención de T-119).
- `.docs/tickets/T-119/revisores/impl_p2_mutantes.py`: mutantes del módulo, en una copia desechable.

## Registro

- 2026-11-13 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-13 · PLANIFICADO · claude · 10 fichas P2 en un módulo; lecciones de las QA de T-106 y T-112 aplicadas desde el diseño
- 2026-11-13 · EN QA · claude · las 10 fichas con código y casos de control superados (33 en total); 1301 pruebas nuevas y 124 mutantes sin vivos; promovidas en el Catálogo (81 IMPLEMENTADO, ninguna en DOCUMENTADO) y corpus re-congelado; decisiones de método en INC-T119-01; detalle en `analisis-tecnico.md` y `pruebas.md`. Sin `git push`: commits locales en la rama `p2-trabajo`
