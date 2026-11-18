# T-177 · PB-58: el BFA envía solicitudes_credenciales en el mantenimiento C4 y el Coordinador emite el CT-25

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (18-11-2026, QA r03 APTO) |
| Pieza | bloque_a/11_Ejecutor (interfaz_broker, mantenimiento C4 nuevo, cli, mock) |
| Planifica · implementa · QA | claude · claude · astra (o un revisor que no implementó) |
| Aprobación del operador | no necesaria (hueco del ejecutor frente al plan de pruebas V3.0; no cambia ningún formato congelado) |
| Deuda técnica | T-177 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

PB-58 («Solicitud y provisión de una credencial por CT-25», plan V3.0) sale «Superada en parte»: la CRD- en F5 sin valor y el servicio degradado y declarado ya están (INC-T116-03), pero faltan los pasos 1 y 2 del plan. El ejecutor no tiene el mantenimiento C4 en el que el Buscador de Fuentes Avanzadas (AG-16) comprueba la bóveda y devuelve `solicitudes_credenciales`, ni el Coordinador que las lee, deduplica, comprueba en HT-01 y emite el CT-25 (Documento 0 V5.3, 7.10.1 y 7.10.2; punto 13 del plan de la noche del 15-11-2026).

## Alcance

- Entra:
  - **Paso 1 (BFA, C4).** Una revisión C4 de credenciales del BFA (`mantenimiento_c4.py`, nuevo): el ejecutor da a AG-16 el estado en la bóveda de HT-01 (alias y estado, nunca el valor) de los servicios de pago o API que tiene declarados, y AG-16 devuelve su retorno con `solicitudes_credenciales` (servicio, motivo, impacto si falta). La fila «Mensual (V5.1)» de la tabla 5.4 del prompt del BFA.
  - **Paso 2 (Coordinador).** `Credenciales.desde_retorno` (AG-01): valida cada solicitud, rechaza íntegro un retorno que trae un valor (6.2.5, incidencia SEGURIDAD sin copiarlo), deduplica por alias de la bóveda, comprueba en HT-01 que la credencial falta de verdad y emite el CT-25 con `solicitar` (servicio, uso previsto, solicitante AG-16, impacto). Lo resuelto queda en F5 (entrada `C4_CREDENCIALES`).
  - Orden de la CLI: `credencial c4` (el ciclo C4 lo lanza el planificador externo; el ejecutor no tiene demonio).
  - Respuesta simulada de AG-16 en el mantenimiento C4 (pide lo que no está PROVISTA).
  - Pruebas del criterio completo de PB-58 (pasos 1 a 4), mapa y evidencias.
- No entra:
  - El otro origen del paso 1, el retorno parcial del CT-05 del Analizador (sigue en INC-T116-03: el ejecutor no lee ese retorno).
  - El resto del mantenimiento C4 (barridos HT-02, Novedades, CT-21): ya existe `ht02` aparte y no lo pide PB-58.
  - Canales nuevos en `contratos.CANALES`: el retorno del BFA no pasa por la mensajería (como el de CT-07), así que los goldens no cambian; el CT-25 sale AG-01 → BROKER como hoy.
  - Esquemas de respuesta nuevos: el retorno C4 usa `BUSQUEDA` (que ya admite campos adicionales); `solicitudes_credenciales` lo valida el Coordinador.
  - El corpus congelado y los otros bloques.

## Diseño

- Contratos CT afectados: ninguno cambia de forma. CT-25 se emite con los mismos campos (`crd_id`, `servicio`, `herramienta`, `uso_previsto`, `solicitante`, `impacto_si_falta`, `urgencia`).
- Estado persistido: F5 gana un tipo de entrada `C4_CREDENCIALES` (C4- con los servicios revisados y lo resuelto de cada solicitud, sin valores). No hay versión de esquema de F5 que migrar (F5 ya guarda tipos libres: CRD, RUN, AVISO_CT22…).
- Números y su origen:
  - Presupuesto de la llamada: «BFA 3 UC/semana» del Anexo A (fila «Presupuesto del mantenimiento continuo (C4)») → `presupuesto_uc.c4_semana.BFA: 3` en `config/por_defecto.yaml` (con DOC-A 3 y DOC-M 2 para completar la fila, sin uso todavía).
  - Plazos y recordatorios de CT-25: los de `credenciales.*` que ya existen.
- Lista de servicios del BFA: `credenciales.servicios_bfa` en `config/por_defecto.yaml`, vacía por defecto `[PROPUESTO]` (qué APIs de pago contrata el operador es decisión suya, T-57). F9 no sirve como fuente: su regla (c) dice que las fuentes de acceso restringido solo se usan por su contenido público. Con el cliente real, el BFA puede añadir un servicio que no esté en la lista; el Coordinador lo trata igual.
- Cómo falla cerrado:
  - Retorno sin datos (R8 en `agentes.invocar`, salida no conforme, sin presupuesto): no se emite ningún CT-25 y la C4- lo dice.
  - Solicitud mal formada (sin servicio, sin motivo o sin impacto de texto, de tipo no dict): se descarta con su motivo en la C4-; no se inventa el campo.
  - Una solicitud con un campo de valor (`CAMPOS_VALOR`) o algo que `contiene_credenciales` reconoce: el retorno entero se rechaza, incidencia SEGURIDAD en HA sin copiar el dato, ninguna CT-25.
  - Duplicados (mismo alias de la bóveda): una sola solicitud. PROVISTA en HT-01: no se pide (`solicitar` ya devuelve PROVISTA sin molestar al Broker). Abierta o DENEGADA: lo que ya hace `solicitar`.
- Decisiones `[PROPUESTO]`: lista de servicios vacía por defecto; el C4 de credenciales se ejecuta cuando se pide (sin comprobar la periodicidad mensual: repetirlo no duplica nada); urgencia NORMAL salvo que el BFA diga ALTA. En INC-T177-01.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| El valor llega a un contexto o a un archivo | Fallo de R8 | El BFA solo recibe alias y estado; prueba que espía todos los contextos y lee todo el estado, la mensajería y los entregables |
| Cambiar flujos del ciclo y los goldens | Diferencias espurias para T-176/T-178 | El C4 no se llama desde el ciclo; `goldens_ct.py` sin cambios |
| Choque con T-176/T-178 en ficheros compartidos | Merge costoso | Módulo nuevo; en compartidos solo líneas añadidas (mapa y evidencias, fila PB-58) |

## Criterios de aceptación (binarios)

1. CA-1: con un servicio declarado del BFA en estado AUSENTE, `credencial c4` (y `mantenimiento_c4`) invoca a AG-16 con el estado de la bóveda sin valores, y su retorno trae `solicitudes_credenciales` con ese servicio.
2. CA-2: el Coordinador emite un CT-25 AG-01 → BROKER con solicitante AG-16, uso previsto e impacto del retorno, y la CRD- queda en F5 SOLICITADA sin valor; la C4- de F5 lo enlaza.
3. CA-3: deduplicación y comprobación en HT-01: dos solicitudes del mismo servicio dan un solo CT-25; un servicio PROVISTA no da ninguno; una segunda C4 con la solicitud abierta no da otro.
4. CA-4: fallo cerrado: un retorno con un campo de valor se rechaza íntegro (SEGURIDAD en HA, ningún CT-25, el valor en ningún archivo); una solicitud mal formada se descarta con motivo; un retorno vacío no emite nada.
5. CA-5: PB-58 completo: tras la C4 el ciclo declara el servicio degradado; el Broker deposita en la bóveda y responde PROVISTA con el alias; la herramienta obtiene el valor; una segunda C4 se resuelve sin CT-25 nuevo; el valor no aparece en mensajes, F1–F11, HA, entregables ni contextos de agentes.
6. CA-6: PB-58 pasa a «Superada» en el mapa y en las evidencias; suite de A ≥ 607; ruff ≤ 2813; mypy de A ≤ 102; `goldens_ct.py` sin diferencias.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t177_pb58_c4_bfa_solicita_y_coordinador_emite_ct25` | integración | CA-1, CA-2 |
| `test_t177_desde_retorno_deduplica_y_comprueba_ht01` | límite | CA-3 |
| `test_t177_retorno_con_valor_se_rechaza_integro`, `…_mal_formada…`, `…_retorno_vacio…` | fallo cerrado | CA-4 |
| `test_t177_pb58_criterio_completo` (pasos 1 a 4, espía de contextos) | integración · seguridad | CA-5 |
| CLI `credencial c4` con cliente mock | integración | CA-1 |
| Mutantes propios (sin dedup, sin comprobar HT-01, sin rechazo del valor, solicitante otro, sin C4 en F5) | regresión | CA-2..CA-4 |
| `evidencias_plan_a.py --ejecutar`, `goldens_ct.py`, suite completa de A, ruff y mypy | regresión | CA-6 |

## Scripts

- `.docs/scripts/evidencias_plan_a.py` (mapa y evidencias).
- `bloque_a/11_Ejecutor/tests/goldens_ct.py` (comprobación).
- `.docs/tickets/T-177/mutantes_t177.py` (mutantes propios, en el ticket).

## Registro

- 2026-11-17 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-17 · PLANIFICADO · claude · plan, criterios y pruebas escritos
- 2026-11-17 · EN CURSO · claude · implementación y pruebas (analisis-tecnico.md, pruebas.md); desviación: `agentes.py` bloquea por R8 un valor en `solicitudes_credenciales` (la caché lo guardaba)
- 2026-11-17 · EN QA (r01) · claude · 16 pruebas, 12/12 mutantes, gate 12/12 en verde, PB-58 «Superada»; commit local «wip local: T-177»
- 2026-11-17 · QA r01 NO APTO · claude (revisor) · H-01 y H-04 altos (R8: el valor llegaba a la caché y a la cinta), H-02 y H-03 medios (CT-25 duplicado), H-05 a H-07 bajos
- 2026-11-17 · EN QA (r02: QA r01 NO APTO) · claude · los siete hallazgos corregidos con su prueba (`analisis-tecnico.md`, «Ronda r02»); fila T-179 en la deuda (pendiente del operador: declarar `credenciales.servicios_bfa`)
- 2026-11-18 · QA r02 NO APTO · claude (revisor nuevo) · H-08 y H-12 altos (un valor bajo una clave no listada llegaba a la caché; con la API real se descartaban todos los informes de Analista), H-09 medio, H-10, H-11 y H-13 bajos
- 2026-11-18 · EN QA (r03: QA r02 NO APTO) · claude · los seis hallazgos y la observación de la bolsa corregidos (`analisis-tecnico.md`, «Ronda r03»)
- 2026-11-18 · QA r03 APTO · claude (revisor) · cuatro bajos abiertos (H-14 a H-17)
- 2026-11-18 · EN QA (ronda de cierre de la QA r03) · claude · H-14 a H-17 corregidos con su prueba
- 2026-11-18 · verificación de la ronda de cierre · claude (revisor) · H-14 a H-17 bien; H-18 bajo nuevo
- 2026-11-18 · EN QA (segunda ronda de cierre de la QA r03) · claude · H-18 corregido con su prueba y tres mutantes
- 2026-11-18 · verificación de la segunda ronda de cierre · claude (revisor) · H-18 bien; H-19 bajo: M08 no era equivalente
- 2026-11-18 · EN QA (tercera ronda de cierre de la QA r03) · claude · M08 restituido y su prueba en `test_t177`
- 2026-11-18 · CERRADO · claude (revisor) · QA r03 APTO tras tres rondas de cierre: H-01 a H-19 corregidos con su prueba; mutantes 42/42 muertos (M08 incluido); scripts r01, r02, r03, r03c y r03d en verde; PB-58 Superada (con su preparación), lista de servicios pendiente del operador en T-179
