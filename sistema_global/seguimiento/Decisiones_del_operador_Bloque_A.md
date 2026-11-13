# Decisiones del operador en el Bloque A — registro

Todo lo importante del Bloque A que es elección del operador: qué se decidió, con qué valor funciona hoy, quién lo decidió y dónde se cambia. Sirve para revisar o cambiar cualquiera más adelante sin buscar por el repositorio.

**Regla vigente (13-11-2026).** El operador pidió que el agente decida por defecto lo que antes esperaba su respuesta y que lo apunte aquí. En la columna «Quién»:

- **Operador:** lo dijo él.
- **Agente:** lo eligió Claude o Astra por defecto. En el código y en las incidencias sigue marcado `[PROPUESTO]`.
- **Entrega:** viene del Documento 0 (Anexo A) y nadie lo ha cambiado.

Cómo cambiar un valor: casi todos están en `bloque_a/11_Ejecutor/config/por_defecto.yaml`, en la clave que da la columna «Dónde». Basta decirle al agente «cambia X a Y»: él edita la clave, pasa las pruebas y lo anota aquí. Las decisiones del sistema global (carteras, límites en euros, autonomía, controles) no están en este registro: son las D-01 a D-34 de `Deuda_tecnica_y_pendientes_del_operador.md` y el `Cuestionario_de_decisiones_del_operador.md`.

Se sigue preguntando antes de actuar cuando algo gasta dinero o usa una credencial, no se puede deshacer, sale del repositorio, cambia la Constitución o los controles, o reparte trabajo a Astra.

## 1. Decisiones de rumbo

| Qué | Valor hoy | Quién | Fecha | Dónde y cómo se cambia |
| --- | --- | --- | --- | --- |
| Diseño del Bloque A que se ejecuta | V5 (los 25 agentes de la entrega). La V6 es aspirante y se cambia cuando el banco con la API real la respalde | Agente | 12-11-2026 | `diseno: v5` → `v6` |
| Tipos de activo activos | Solo divisas (DIV); los otros once se activan cuando tengan datos y fichas | Agente (PA-01) | 10-11-2026 | `perfiles.activos` |
| Qué manda si el Documento 0 y el código difieren | El código; el Anexo B se corrige en la próxima entrega | Operador | 13-11-2026 | INC-T114-01 en `docs/incidencias.md` |
| Bloque A Forex | Es una prueba del Bloque A solo con divisas; no se integra en el bloque final | Operador | 13-11-2026 | T-115 en la deuda (aplazada) |
| Filtro de los textos del Sintetizador V6 | «Umbrales y sin cifras libres»: las cuentas las escribe el código | Operador | 12-11-2026 | INC-T102-01 |
| Promover en el Catálogo las fichas que superen sus casos de control | Autorizado, con re-congelado del corpus | Operador | 12-11-2026 | `.docs/scripts/promover_fichas_catalogo.py` |
| Fuente de datos históricos reales | **Sin decidir.** Hoy, datos sintéticos de ejemplo | — | — | Cuesta dinero o exige una cuenta: se pregunta |
| API real (modo sombra, Fase 5) | **Sin decidir.** Necesita clave y autorización de gasto | — | — | Se pregunta siempre |
| Las 10 fichas P2 del Motor | No se hacen por ahora: son opcionales y tocan el Motor recién cerrado | Agente | 13-11-2026 | Se pide como tarea nueva |
| Huecos del plan de pruebas que se cubren | Los siete baratos (PB-10, 16, 17, 22, 33, 45, 59); PB-26 y PB-48 quedan sin prueba y PB-46 sin implementar | Operador (confirmó la lista del agente) | 13-11-2026 | T-116 |

## 2. Selección de oportunidades

| Qué | Valor hoy | Quién | Fecha | Dónde y cómo se cambia |
| --- | --- | --- | --- | --- |
| Umbral de señal para investigar un ámbito (GC1) | 0,75 de señal compuesta | Entrega | — | `seleccion.umbral_senal_gc1` |
| GC1 en la V6: umbral propio por tipo | 0,65 en renta fija, liquidez y tipos, curvas y volatilidad; 0,75 en los demás. Provisional hasta tener datos reales | Agente (INC-T117-01) | 13-11-2026 | `v6.gc1.umbral_por_perfil` |
| GC1 en la V6: señal que manda en cada tipo | La señal compuesta en los doce | Agente (INC-T117-01) | 13-11-2026 | `v6.gc1.senal_por_perfil` |
| GC1 en la V6: familias de señal que deben coincidir | 2 (lo pide el Anexo A) | Agente (INC-T117-01) | 13-11-2026 | `v6.gc1.familias_min` |
| Ámbitos que no pasan GC1 y se ofrecen igual, para medir lo que el filtro deja escapar | 2 por tipo | Agente | 12-11-2026 | `v6.gc1.exploracion_celdas` |
| Candidatas y finalistas por tipo | 8 y 5 | Entrega | — | `seleccion.max_candidatas`, `seleccion.max_finalistas` |
| Opciones que se publican por tipo | 3 como máximo | Entrega | — | `parametros_ht03.max_opciones_por_clase` |
| Si las tres mejores son en el fondo la misma apuesta | Se publican las tres avisando de la concentración, si no hay alternativa a 10 puntos | Agente (INC-T53-01) | 09-11-2026 | `parametros_ht03.max_por_cluster`, `parametros_ht03.diversidad_margen_rk` |
| Solidez y atractivo mínimos para proponer el envío al Bloque B | Solidez (E) 70; atractivo (A) 65 para seguir estudiando | Agente (INC-T53-05) | 09-11-2026 | `seleccion.siguiente_paso`, `seleccion.semaforo` |
| Confianza «probable» en la presentación | Con solidez (E) de 70 o más; si no, «especulativo» | Agente (INC-T53-05) | 09-11-2026 | `presentacion.confianza_probable_E` |
| Cuánto se dedica a explorar ideas nuevas en un ciclo ligero | 2 ámbitos por tipo | Agente | 10-11-2026 | `seleccion.rotacion_exploratoria_celdas` |
| Fuentes independientes mínimas para dar algo por corroborado | 2 | Entrega | — | `ps1.raices_min` |
| Efecto de una «tesis frágil» | Baja la confianza a «especulativo»; frágil con 2 objeciones moderadas | Agente (INC-T66-01) | 10-11-2026 | `contrarias.moderadas_para_fragil` |
| Criptomonedas concretas (BTC, ETH) en los textos | Se tratan como un instrumento concreto: el Bloque A no las nombra | Agente | 12-11-2026 | Lista de siglas permitidas del filtro (T-102) |

## 3. Presupuesto de cómputo

| Qué | Valor hoy | Quién | Fecha | Dónde y cómo se cambia |
| --- | --- | --- | --- | --- |
| Presupuesto por nivel de análisis | N0 1 UC, N1 5, N2 18, N3 50; ciclo semanal 240 como máximo | Entrega | — | `presupuesto_uc` |
| Ampliación sin pedir autorización y tope total | +25 % y +50 % de la base | Entrega; la lectura del tope, Agente (INC-T92-01) | 10-11-2026 | `presupuesto_uc.ampliacion_*` |
| Reparto del presupuesto entre fases | Cribado 35 %, investigación 20 %, prospectiva 15 %, refutación 20 %, respuesta 10 % | Entrega | — | `presupuesto_uc.reparto_fases` |
| Fracción de ciclos que audita el Auditor en la V6 | 25 % | Agente | 12-11-2026 | `v6.auditoria_fraccion` |

## 4. Evaluación y aprendizaje

| Qué | Valor hoy | Quién | Fecha | Dónde y cómo se cambia |
| --- | --- | --- | --- | --- |
| Ajustes automáticos solo prudentes | Sí: degradar y revocar es automático; un certificado nuevo o un cambio de pesos espera la aprobación del operador | Agente (PA-10) | 10-11-2026 | `aprendizaje.solo_endurecer` |
| Calibración a partir de la cual se revoca un certificado | ECE de 0,12 o más | Agente (INC-T53-03) | 09-11-2026 | `evaluacion.ece_revocacion` |
| Degradación del horizonte de décadas (H5) | Con 20 hitos y menos de la mitad cumplidos: «Sí → Limitado» sola; «Limitado → No» solo como propuesta | Agente (INC-T53-04) | 09-11-2026 | `evaluacion.degradacion_h5_*` |
| Recalibración de los pesos de la puntuación | Pasos de 0,05, con bandas de ±0,05 por trimestre y ±0,15 en total; tres meses en sombra | Entrega; sombra y mínimo, Agente | 10-11-2026 | `evaluacion.recalibracion_rk` |
| Antigüedad máxima de los datos y festivos | H1 se cuenta en sesiones, sin los cierres habituales de mercado | Agente (INC-T53-02) | 09-11-2026 | `ps2_antiguedad_maxima_dias`, `ps2_festivos` |
| Cómo se resuelve un pronóstico con series que acaban en fechas distintas | Todas se miden en la última fecha común; si no la hay, espera | Agente (INC-T91-01) | 12-11-2026 | `evaluacion` (T-91) |
| Pregunta repetida que genera una lección | 3 veces en 4 semanas | Entrega | — | `pregunta_repetida` |
| Backtest con un modelo real | Se anonimiza; lo anterior a la fecha de corte del modelo no cuenta para certificar | Agente (PA-09) | 10-11-2026 | `backtest.anonimizar`, `backtest.fecha_corte_modelo` |

## 5. Motor de cálculo

| Qué | Valor hoy | Quién | Fecha | Dónde y cómo se cambia |
| --- | --- | --- | --- | --- |
| Decisiones de método de las 21 fichas de la Fase 1 | Umbrales fijos, rangos y tratamiento de cifras no finitas | Agente (INC-T106-01) | 12-11-2026 | `docs/incidencias.md` y cada ficha |
| Decisiones de método y cotas de las 36 fichas de la Fase 2 | Cotas de tamaño, tolerancias, semillas | Agente (INC-T112-01) | 13-11-2026 | `docs/incidencias.md` y `UMBRALES` de cada grupo |
| Rangos de las fichas de liquidez e índices y otros cierres de deuda | Horizontes hasta H5, listas de hasta 12 elementos, etc. | Agente (INC-T113-01) | 13-11-2026 | `docs/incidencias.md` |
| Hallazgos abiertos de la QA de la Fase 2 (H-09 a H-15) | Sin corregir; H-09 antes del modo sombra | Agente | 13-11-2026 | T-118 en la deuda |

## 6. Contratos y pruebas

| Qué | Valor hoy | Quién | Fecha | Dónde y cómo se cambia |
| --- | --- | --- | --- | --- |
| Formatos de los contratos CT | Congelados; cambiar uno exige re-congelar con motivo | Agente | 13-11-2026 | `bloque_a/11_Ejecutor/tests/goldens/README.md` |
| Ejemplo publicado del informe de seguimiento, que no cumple su esquema | No se toca la entrega; se corrige en la próxima | Agente (INC-T114-02) | 13-11-2026 | `docs/incidencias.md` |
| El Broker pide horizontes con una lista global, no por tipo | Se deja así | Agente (INC-T116-01) | 13-11-2026 | `docs/incidencias.md` |
| La autorización de ampliación no registra CPI ni EAC | No se añaden por ahora | Agente (INC-T116-02) | 13-11-2026 | `docs/incidencias.md` |

## Cómo se mantiene

- Cada decisión nueva que tome el agente por defecto añade o cambia una fila aquí, en el mismo commit.
- Si el operador cambia una decisión, la fila pasa a «Operador» con la fecha, y el valor anterior queda en el historial de git.
- El detalle y el porqué de cada una están en la incidencia o el ticket que cita la fila.
