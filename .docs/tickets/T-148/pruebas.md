# T-148 · Pruebas

Copia `t147` (base `dd166b3`), intérprete `/home/user/robotinvestor/.venv/bin/python`, sin red, sin API y sin servicios de pago (el cliente real, cuando sale, con un SDK falso local). No se lanzó `./tools/check_all.sh` ni la suite completa de A.

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t148.py` (nuevo) | — | 20 pasan |
| `tests/test_t145.py` | 39 | 39 pasan (una igualdad cambia, comentada «T-148») |
| `test_t136_coste.py`, `test_t129_modo_sombra.py`, `test_t131_preparativos.py` | — | pasan (con `test_t145`, 66) |
| Vecinas pedidas (`test_t12*`, `test_t13*`, `test_t14*`, `test_fase2_*`, `test_fase3_goldens.py`) | — | 3061 pasan, 0 fallan (antes de añadir la prueba de M26; `test_t148.py` completo, 20, pasa aparte) |
| `python tests/goldens_ct.py` | coinciden | coinciden |
| `.docs/scripts/borrador_anexo_b.py --comprobar` | 1 en la base (el borrador no estaba al día) | 0 |

**Prueba cambiada.** `test_t145.py::test_h01_la_tabla_de_llamadas_del_ciclo` fijaba `encargo_tok == medido + 52 000` para la contrarréplica, el supuesto S4 que la QA mostró falso. Ahora fija `lee_tok == 52 000` (lo que S4 sigue contando) y el encargo nuevo, medido + 2·8 000·(27 − 0,5·2 500/1 500) − 1 500, igual de exacto. No se debilita.

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_h01_la_respuesta_y_la_contrarreplica_se_acotan_por_el_presupuesto`, `test_h01_con_un_presupuesto_pequeno_el_tope_acota_tambien_a_s4`, `test_h01_el_tope_del_encargo_es_el_de_la_estimacion_previa_del_codigo` (contra `Bloque._estimar_uc` y su código fuente), `test_h01_la_cota_cubre_el_caso_de_la_qa`, `test_h01_la_curacion_se_queda_por_debajo_del_contexto_largo_de_su_tarifa`; `r01_01` del revisor (abajo) |
| CA-2 | `test_h02_el_peso_de_lo_que_lee_cada_busqueda` (2 × 5 × (4 + 3 + 2 + 1) lecturas al precio de escritura, a mano), `test_h03_los_tipos_salen_de_f10`, `test_h03_main_con_estado` |
| CA-3 | `test_h04_r01…`, `test_h04_r04_r05…` (dos configuraciones con los modelos de la tarifa), `test_h04_r06_r07…`, `test_h04_r08_s3_en_el_borde`, `test_h04_r09…`; mutantes (abajo) |
| CA-4 | `test_h05_historia_antigua_invalida_lleva_aviso` (n/d, negativo, fecha repetida), `test_h05_historia_antigua_valida_sin_aviso`, `test_h06_el_borrador_cita_donde_estan_coincide_e_independiente`, `test_h07_inc_t129_01_limites_del_estimador_al_dia` |
| CA-5 | `test_con_t146_la_cota_por_presupuesto_son_los_limites`; la tabla (abajo) |

## Scripts del revisor (antes → después)

| Script | Antes (QA r01 de T-145) | Después |
| --- | --- | --- |
| `T-145/revisores/r01_01_amplificacion_contrarreplica.py <tmp> <m_div> --n 120,150,170 --salida real --k 1` | contrarréplica de N = 150 admitida con 196 239 tok y 2,48 USD, por encima de su cota (2,07) | encargo de la cota 418 913 tok; N = 120: 0,94 USD (cota de la llamada 9,95); N = 150: 1,18; N = 170: cortada por el presupuesto. Coste del ciclo 1,49–2,63 USD frente a la cota 31,50 |
| ídem con `--reparar-papel contrarreplica --modo cota` | — | N = 150: contrarréplica 5,04 USD (cota 9,95), ciclo 6,76; N = 170: 222 410 tok, 5,62 USD, ciclo 7,38 (cota 31,50) |
| `T-145/revisores/r01_03_comprobar_datos_bordes.py <tmp>` | 10 de 10 | 10 de 10; las tres historias inválidas llevan ahora el aviso |
| `T-145/revisores/r01_04_mutantes.py <copia t147_mut>` (sus pruebas) | 5 muertos, 7 vivos (R01, R04–R09) | igual con sus pruebas fijadas (no incluyen `test_t148.py`) |
| el mismo, con `tests/test_t148.py` añadido a sus `PRUEBAS` (copia desechable del script en el scratchpad; `mutantes_revisor_ampliado.py` no entiende un `PRUEBAS` en varias líneas) | — | **12 de 12 muertos** |

## Coste de un ciclo C1 (tarifa del 15-11-2026)

`medir_consumo_a.py` (solo divisas y con los 12 tipos) + `estimar_coste_ciclo_a.py` [`--config doce.yaml`] [`--con-t146`]:

| Tipos activos | Suelo | Cota (código de esta copia) | Cota con T-146 integrado | Por cada 1 000 tokens leídos por búsqueda |
| --- | --- | --- | --- | --- |
| Solo divisas | 0,86 USD | **31,50** (por llamadas; presupuesto 71,93 = límites 46,08 + última llamada 14,57 + caché 5,29 + fuera 5,60 + búsquedas 0,40) | **31,50** (presupuesto 46,08) | +0,40 USD |
| Los 12 tipos | 2,98 USD | **275,77** (por presupuesto = 46,08 + 149,22 + 45,07 + 30,60 + 4,80; por llamadas 310,09) | **46,08** (por llamadas 310,09) | +4,80 USD |

Hasta 14 llamadas, 34 peticiones y 40 búsquedas (divisas) y 91, 254 y 480 (12 tipos). Con `presupuesto_uc.uc_por_busqueda: 0,32` (T-146) y `--con-t146`, igual: el precio por UC de una búsqueda (0,031 USD) no pasa del de Opus (0,128).

## Regresiones (mutantes)

`.docs/tickets/T-147/mutantes.py <copia t147_mut> --ticket T-148`: **8 de 8 muertos** (la contrarréplica con S4, sin el tope del presupuesto, tope sin la salida estimada, tipos siempre de la configuración, F10 ignorado, `--con-t146` igual que sin él, lecturas de la búsqueda sin los reenvíos, sin el aviso de la historia antigua). En la primera pasada «sin el tope del presupuesto» sobrevivió (con la configuración por defecto S4 nunca llega al tope); lo mata `test_h01_con_un_presupuesto_pequeno_el_tope_acota_tambien_a_s4`.

Con el código de la base (`dd166b3`), `test_t148.py` da 14 fallos de 20 (pasan los de R04 a R09 y el borde de S3, que fijan cifras que ya eran así y por eso mataban mutantes que antes sobrevivían, y la historia antigua válida).

## Cuotas

ruff 2838 (cuota 2838); mypy A 109 (cuota 109). Los scripts de `.docs/` no cuentan en esas cuotas.

## Comandos

En `analisis-tecnico.md`, «Comandos».

## Integración con T-146 (15-11-2026)

Al llevar T-148 al árbol principal, que ya tiene T-146, falló `test_h01_el_tope_del_encargo_es_el_de_la_estimacion_previa_del_codigo` (`Bloque._estimar_uc` ya no existe). Cambios y pruebas en el README («Integración con T-146»). Desde `bloque_a/11_Ejecutor`:

| Orden | Resultado |
| --- | --- |
| `pytest -q tests/test_t148.py tests/test_t145.py tests/test_t136_coste.py tests/test_t129_modo_sombra.py` | 74 passed |
| `medir_consumo_a.py` + `estimar_coste_ciclo_a.py` (solo divisas; los 12 tipos con `--config` de `perfiles.activos`) | 28,04 USD (presupuesto 46,08) · 46,08 USD (llamadas 267,71); `--sin-t146`: 28,04 (69,62) · 250,11 (r01; las de los 12 tipos se midieron con un ciclo de solo divisas: QA r01, H-02. Corregidas en la r02, abajo) |

Las cifras de las tablas de arriba son las de antes de la integración.

## Ronda r02 (QA r01 de T-148 NO APTO; copia `t146r02`, con la r02 de T-146)

Desde `bloque_a/11_Ejecutor`, con `PYTHONPATH=$PWD` (sin él, `medir_consumo_a.py` importa el `bloque_a` instalado en el `.venv`, que es el de otra copia):

| Orden | Resultado |
| --- | --- |
| `pytest -q -p no:cacheprovider tests/test_t148.py tests/test_t145.py` | 62 passed (23 + 39; tres pruebas nuevas en `test_t148.py`, `test_r02_*`) |
| `../../.venv/bin/python ../../.docs/scripts/medir_consumo_a.py <m_div> 2024-03-29` y `… <m_12> 2024-03-29 --config doce.yaml` (`perfiles: {activos: [los doce]}`) | 8 y 77 llamadas medidas |
| `../../.venv/bin/python ../../.docs/scripts/estimar_coste_ciclo_a.py <m_div>` · `--sin-t146` | **28,04** (llamadas; presupuesto 46,08) · 28,04 (presupuesto 69,62); peso por 1 000 tokens leídos 0,40 (llamadas, manda) y 0,08 (presupuesto) |
| `… <m_12> --config doce.yaml` · `--sin-t146` | **46,08** (presupuesto; llamadas **268,48**) · **248,02**; peso 0,96 (presupuesto, manda) y 4,80 (llamadas); con `--sin-t146`, 4,80 en las dos |
| `… <m_div> --sin-t146 --con-t146` | error de uso (código 2) |
| `.venv/bin/python -I .docs/tickets/T-148/revisores/r01_01_tope_y_cota_con_t146.py <qa20w>/m_div <qa20w>/m_12 <qa20w>/doce.yaml <trabajo>` (con `PYTHONPATH`) | A: 6 OK (topes 310 123 / 4 167 901 / 3 190 123, como en la r01) · B: 4 OK (también «las dos a la vez», que en la r01 era OBS) · **C: HALLAZGO** (+2,31 UC, como en la r01: la lectura sigue sin reservarse; la salida ya no dice que la acote: el script imprime «?» donde antes citaba la frase) · D: 4 OK |

Las medidas de la r02 dan las mismas cifras que las del revisor (`qa20w/m_div`, `m_12`). Matriz de la r02: H-01 → `test_r02_h01_con_busquedas_la_salida_no_dice_que_el_presupuesto_acote_lo_leido` (la frase no sale con los 12 tipos ni con divisas; el peso, a mano) y `test_r02_h01_el_peso_cubre_la_lectura_que_la_reserva_deja_pasar` (caso C); H-03 → `test_r02_h03_opciones_excluyentes_y_ag18_19_20_en_la_comun`. Las tres fallan con el estimador de la r01 (la frase, la clave del peso y la COMÚN). `test_h04_r04_r05…` cambia: pone también AG-18, AG-19 y AG-20 en la COMÚN (es lo que hace ya el estimador con T-146), con las mismas cifras a mano. Mutantes: `.venv/bin/python .docs/tickets/T-147/mutantes.py <copia «t147_mut»> --ticket T-148` (desde la raíz), **13 de 13 muertos** (M25–M32 de la r01 y M33–M37, uno por corrección de la r02). Cuotas: ruff 2838, mypy A 109.
