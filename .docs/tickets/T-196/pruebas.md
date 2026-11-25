# T-196 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t196.py` | — | 41 (14 funciones más los casos de los `parametrize`) |
| Bloque A completo (gate) | — | 8400 passed |
| A-Forex, B | sin tocar | sin tocar |

## Criterio de aceptación → prueba

Todas las pruebas están en `tests/test_t196.py`.

| Criterio | Prueba |
| --- | --- |
| CA-1 registradas | `test_pb08_rafaga_del_plan_65_registradas_n0_sin_esperar_y_servicio_por_prioridad`: 25 CT-01 (5 ALTA, 15 NORMAL y 5 BAJA, mezclados) y 40 CT-03 (30 N0 y 10 analíticas), intercalados en 10 minutos con instantes inyectados. Quedan 25 PET- de CT-01, 40 QRY- y 10 PET- de escalado en F5. `test_cli_encola_y_atiende` |
| CA-2 sin rechazo por número | `test_200_peticiones_en_cola_sin_rechazo_y_un_msg_id_repetido_no_duplica` (posición 200, UC por delante = 199 × N2, mismo `msg_id` → misma PET-) y la ráfaga (todas ENCOLADAS) |
| CA-3 respondidas o con plazo | La ráfaga: acuse con plazo para cada CT-01, respuesta N0 o provisional «En cola…» con `run_id` nulo para cada CT-03 y, tras atender, una sola final por cada escalada. Además: `test_servicio_real_de_un_ct01_y_de_una_consulta_escalada_con_su_final` (final validada con jsonschema contra `respuesta_final.ESQUEMA`) y `test_la_final_pendiente_de_una_consulta_atendida_otro_dia_cita_su_run` |
| CA-4 prioridad con envejecimiento | `test_prioridad_efectiva_base_envejecimiento_y_su_maximo`, `test_una_baja_que_espera_alcanza_a_una_normal_recien_llegada`, `test_la_urgencia_por_fecha_objetivo_cercana_adelanta_la_peticion` (con el margen justo), `test_desempate_por_nivel_menor_y_despues_por_llegada` y la ráfaga (35 servidas en el orden esperado) |
| CA-5 N0 sin esperar | La ráfaga: 30 N0 respondidas con 25 o más peticiones en cola, ningún RUN- nuevo hasta atender y el p90 del tiempo de proceso (cliente simulado) por debajo de `objetivo_n0` (P-21). Además, `test_p90_por_rango_mas_proximo` y `test_la_configuracion_por_defecto_tiene_los_numeros_de_la_cola` |
| CA-6 presupuesto por nivel | `test_presupuesto_proporcional_por_nivel_igual_que_el_ciclo` (N1, N2 y N3 frente a `presupuesto_uc` y a `Bloque._reparto`) y el servicio real (el RUN- tiene el nivel de la PET-) |
| CA-7 servicio | El servicio real (ENCOLADA → EN_CURSO → ATENDIDA, `pet_id` en el disparador del RUN-), `test_un_ciclo_que_falla_deja_fallida_incidencia_y_el_resto_encolado`, `test_dos_bloques_y_varios_hilos_nunca_toman_la_misma_peticion` (concurrencia: 4 hilos sobre 2 instancias del almacén), `test_maximo_limita_las_servidas` |
| CA-8 falla cerrado | `test_un_ct01_invalido_se_rechaza_sin_escribir_nada` (10 casos), `test_un_instante_invalido_se_rechaza` (6), `test_un_instante_anterior_a_una_recepcion_no_ordena_ni_sirve`, `test_maximo_invalido_se_rechaza` (5), `test_consulta_en_cola_con_urgencia_desconocida_o_sin_escalado_se_rechaza_sin_escribir`, `test_la_final_de_una_consulta_en_cola_no_sale_y_sin_pet_si`, `test_la_consulta_urgente_escala_con_prioridad_alta` |
| CA-9 regresión | `test_por_defecto_la_consulta_y_la_peticion_siguen_atendiendose_en_el_momento`, la suite completa (gate), el ciclo mock y el backtest frente a develop, y las evidencias regeneradas |

## Regresiones y mutantes

- **Sin el cambio, las pruebas nuevas fallan.** En `origin/develop` no existen `bloque_a/cola_peticiones.py`, `Bloque.cola` ni `consulta(…, encolar_escalado=)`, así que falla la importación de `test_t196.py`. Cada pieza esencial tiene además su mutante muerto.
- **Mutantes** (`.docs/tickets/T-196/mutantes.py`): 33, ejecutados en una copia completa del paquete. Los 33 están muertos.
  - En la primera pasada, 32 muertos y 1 vivo: M30, que quita la validación temprana de la urgencia en `consulta`. La validación posterior ya rechazaba sin escribir en F5, pero después de crear el CT-03 y de llamar al modelo. La prueba ahora exige además que la mensajería no haya creado nada, y M30 muere.
  - M15 («la toma no marca EN_CURSO») hace que `atender` no termine. El script cuenta como muerto lo que agota el tiempo.
- **Evidencias:** `.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar` da «358 de 358 pruebas citadas superadas». PB-08 sigue «Superada en parte», ahora solo por el p90 de N0 en tiempo real (modo sombra).

## Ciclo mock y backtest frente a develop

El script es `comparar196.sh`, en la carpeta de trabajo de la sesión. Ejecuta las dos versiones con el cliente mock: develop, extraída con `git archive 6045913 bloque_a`, y esta copia.

- **Backtest del README** (`backtest --desde 2024-01-05 --hasta 2024-03-29`): rc 0 en los dos. `senales.csv`, `pronosticos.csv` y `metricas.json` son idénticos byte a byte.
- **Ciclo** `--as-of 2024-03-29 ciclo`: rc 0 en los dos. El resumen y los ficheros de estado (F1–F6, F10, HA, RC, caché) son iguales sin los campos internos. Solo difieren las rutas absolutas de los entregables en F5 y en el resumen, porque las carpetas de salida son distintas.

Las rutas por defecto no cambian nada.

## Gate

`./tools/check_all.sh` completo, en la copia: **12/12 en verde** (RC 0). corpus-integridad (705), nombres-nfc, yaml-configs, secrets y refs-vivas OK; ruff 2807 (cuota 2807), mypy A 102, A-Forex 174 y B 159 (cuotas sin subir); pytest A 8400 passed (≥ 607), A-Forex 68 (≥ 68), B 176 (≥ 174). Las cuotas no bajan: los ficheros nuevos están limpios y no se tocó código ajeno.

## Ronda r02 (QA r01 NO APTO)

| Suite | r01 | r02 |
| --- | --- | --- |
| `tests/test_t196.py` | 41 | 56 (+15: H-01 con reloj y sin él, H-02 ×2, H-03, H-04, H-06, H-07, H-08 con `KeyboardInterrupt`, H-09 ×3, recepciones concurrentes (R7), y las dos horas del cambio de hora en el `parametrize` de instantes inválidos) |

- **Ataques del revisor** (`revisores/r01_ataques.py`, sin cambiarlo): **10 de 10 OK**. A9 sigue fallando cerrado, como aceptó el revisor.
- **Mutantes del revisor** (`revisores/r01_mutantes.py`): **13 de 14 muertos**; R11 es equivalente, como dice el qa.md.
  - En la primera pasada de la r02 quedó vivo R7 (recepción sin transacción), que en la r01 había muerto.
  - Lo mata la prueba nueva `test_recepciones_concurrentes_dan_posiciones_distintas`: 4 instancias del almacén reciben a la vez con el mismo instante. Con R7, dos recepciones comunican la misma posición (falló 3 de 3 veces).
  - Esa prueba crea antes la tabla de acuses de cada instancia. Su `ALTER TABLE` inicial no es concurrente (`contratos.Mensajeria._acuses`): con varias instancias nuevas a la vez da `duplicate column name: error`. Es anterior a T-196 y queda fuera de este ticket.
- **Mutantes propios** (`mutantes.py`): **55 de 55 muertos**. Son los 33 de la r01, R2, R4, R6, R9, R10, R12 y R13 del revisor como M34 a M40, M55 (R7) y 14 nuevos de la r02 (M41 a M54).
  - En la primera pasada quedó vivo M50 (`reconciliar` sin fijar el día). La prueba de la huérfana ahora reconcilia desde una instancia nueva, con el reloj sin fijar, y M50 muere.
- **Equivalencia** (`revisores/r01_equivalencia.py`): el RUN- servido por la cola coincide con el de `Bloque.peticion` y F3 y F4 son iguales. Solo difieren las rutas temporales de los entregables, como en la r01.
- **Evidencias:** `evidencias_plan_a.py --ejecutar` da 364 de 364 citadas superadas (PB-08 sigue «en parte», solo por el p90 en tiempo real).
- **Gate:** `./tools/check_all.sh` completo, con `setsid nohup` y el log en `gate_t196_r02.log` (carpeta de trabajo de la sesión): **12/12 en verde**, RC 0.
  - Cifras: ruff 2807, mypy A 102, A-Forex 174 y B 159 (cuotas sin subir); pytest A 8415, A-Forex 68 y B 176.
  - Un primer intento (`gate_t196_r02_intento1.log`) dio mypy A 103. El error era `valor.floor` sobre un `datetime`; ahora es `pd.Timestamp(valor).floor("us")`, sin cambio de comportamiento. M52 sigue muerto.

## Ronda r03 (QA r02 NO APTO)

| Suite | r02 | r03 |
| --- | --- | --- |
| `tests/test_t196.py` | 56 | 62 (+6: N-01, N-02, Q2, Q8, Q10 y Q11) |

- **Ataques del revisor:**
  - `revisores/r01_ataques.py`: 10 de 10 OK.
  - `revisores/r02_ataques.py`: B1 a B4 OK; B6 (la carrera de `_acuses`, otro ticket) no se reprodujo en esta pasada (0 de 15).
  - **B5 da ERROR**, y es lo que pide la corrección. El script solo da OK si se sirven 3 peticiones con un reloj que retrocede; la corrección exacta de N-02 (qa.md y coordinador) es lanzar `PeticionInvalida`. `atender` lanza en la segunda toma, el caso termina con esa excepción y su segunda parte no llega a ejecutarse. Lo prueba `test_atender_con_un_reloj_que_retrocede_falla_cerrado`: una ATENDIDA, dos ENCOLADAS y `PeticionInvalida`.
  - `revisores/r02_final_doble.py`: la final no se duplica. Hay 3 CT-03 en el registro: la entrada, la provisional y una sola final. `enviar_pendientes` sin fecha da `[]`, y con la fecha de la consulta devuelve la misma final como `repetido`.
- **Mutantes**, en copias limpias del paquete:
  - `revisores/r01_mutantes.py`: 13 de 14 muertos; R11, equivalente.
  - `revisores/r02_mutantes.py`: 12 de 12 muertos.
  - `mutantes.py`: 61 de 61 muertos (M56 a M61 nuevos).
- **Evidencias:** 366 de 366 citadas superadas. PB-08 sigue «en parte», solo por el p90 en tiempo real.
- **Gate:** `./tools/check_all.sh` completo, con `setsid nohup` y el log en `gate_t196_r03.log` (carpeta de trabajo de la sesión): **12/12**, RC 0. Ruff 2807, mypy A 102, A-Forex 174 y B 159; pytest A 8421, A-Forex 68 y B 176.

## Ronda de cierre de la QA r03

- **Pruebas:** `tests/test_t196.py` tiene 63 (+1: el segundo caso del reloj que retrocede, M-01), todas superadas.
- **Mutantes**, en copias limpias del paquete:
  - `mutantes.py`: **62 de 62 muertos**; M62 es P1.
  - `revisores/r03_mutantes.py`: **2 de 2 muertos** (P1 y P2).
- **Ataques** (`revisores/r03_ataques.py`): B1 a B5 OK. B6 confirma la carrera de `_acuses` (1 de 15), que es de T-200 y no se toca aquí.
- **Gate:** no se lanza, por orden del coordinador.
  - El código no cambia y solo se añade una prueba.
  - El recuento de ruff del gate, desde la raíz, sigue en 2807.
  - La prueba que crea la tabla de acuses antes de las recepciones concurrentes no se cambia: se simplificará al integrar T-200.
