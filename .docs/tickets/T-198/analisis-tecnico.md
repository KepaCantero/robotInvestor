# T-198 · Análisis técnico

## Causa raíz o motivo

PB-46 (Plan de pruebas V3.0) es «Evaluador → Buscador → F9». T-125 hizo la primera mitad: el Evaluador resuelve los pronósticos de las fuentes, escribe la FUE- en F6 y la manda al Buscador (AG-16) por CT-19. Pero `Bloque._comunicar_fiabilidad` solo creaba el mensaje (`Mensajeria.crear`, estado COMPLETO) y anotaba su msg_id en la FUE-: ningún código lo recibía y F9, que es un archivo del corpus congelado (`05_Archivos_operativos`, hash en el gate corpus-integridad), no tenía dónde guardar lo recibido. La QA r01 de T-159 (H-02) lo señaló y quedó en INC-T159-01 como función que falta.

## Evidencia

- Antes (`origin/develop`, `6045913`): `orquestacion.py`, `_comunicar_fiabilidad`: `self.mensajeria.crear("CT-19", "AG-20", "AG-16", …)` y el `comunicado_ct19` en F6; nada más. `almacen.ARCHIVOS` sin F9; `referencias.py` lee F9 del corpus y solo lo lee.
- Con las pruebas nuevas sobre el código de develop (copia con `almacen.py` y `orquestacion.py` de develop y el resto de T-198): 18 de 19 fallan; la que pasa es la de regresión del cuerpo del CT-19, que no debe cambiar.

## Implementación

- **Archivos cambiados y por qué:**
  - `bloque_a/11_Ejecutor/bloque_a/fiabilidad_f9.py` (nuevo): `CAMPOS_CT19`, `CAMPOS_CONTEXTO`, `FiabilidadNoAtendible`; `atendidas` y `por_comunicar` (FUE- de F6 aún sin entrada en F9, por periodo e id); `cuerpo_ct19`; `comprobar_ct19` (todo el mensaje frente a F6 y F9, antes de escribir); `atender_ct19` (en una transacción: comprueba, salta lo ya atendido y escribe una `FIABILIDAD_MEDIDA` por fuente como AG-16); `fiabilidad_medida` y `anotar_candidatas` (lo que ve el Buscador en un CT-07).
  - `bloque_a/11_Ejecutor/bloque_a/almacen.py`: `ARCHIVOS["F9"] = "F9_registro_fuentes.jsonl"`, propietario AG-16, clave `ref_id`; `TIPOS_F9 = {"FIABILIDAD_MEDIDA"}` en `_comprobar_reserva`; al abrir un almacén ya sellado, un archivo de `ARCHIVOS` que no existe y no tiene sello se sella vacío (`[0, 0…0]`) y se guarda el sello; si existe sin sello, el fallo de integridad de siempre.
  - `bloque_a/11_Ejecutor/bloque_a/orquestacion.py`: `_comunicar_fiabilidad(as_of, run_id)` (antes recibía `res_eval`): bajo el cerrojo del almacén, CT-19 con `por_comunicar`, `comunicado_ct19` en F6 y `atender_ct19`; `FiabilidadNoAtendible` → incidencia DATOS en HA (objeto AG-16, `run_id`) y nada en F9. En `_peticion_conocimiento`, una línea tras `para_clase`: `anotar_candidatas`. Un import.
  - `bloque_a/11_Ejecutor/tests/test_t198_buscador_ct19.py` (20 pruebas), `tests/mapa_plan_pruebas.json` (PB-46, PARCIAL), `docs/evidencias_pruebas_bloque_a.md` (regenerado), `docs/incidencias.md` (INC-T198-01 y la línea de PB-46 en INC-T159-01), `bloque_a/11_Ejecutor/README.md` (tabla de archivos), deuda técnica (fila T-198).
- **Decisiones y desviaciones del plan:** ninguna desviación. Las decisiones `[PROPUESTO]` están en INC-T198-01. No se invoca al Buscador con el modelo para esto: lo único que haría es recalificar Q, que queda fuera; así el consumo del ciclo no cambia. El reintento usa un CT-19 nuevo (un msg_id no se reutiliza) y reescribe `comunicado_ct19` en F6 (append-only).
- **Ficheros de Astra:** `referencias.py` y `mantenimiento_fuentes.py` no se tocan. En `orquestacion.py` la línea nueva de `_peticion_conocimiento` queda unas diez líneas por encima del bloque que cambia la rama `origin/astra/encargos-bloque-a-c38-c47` (filtro de retiradas y cuarentena tras la invocación); `_comunicar_fiabilidad` no lo toca esa rama. El archivo `F9_bajas.md` que esa rama crea en la carpeta del almacén es otro nombre y no choca con `F9_registro_fuentes.jsonl`; si un día se quieren juntar las bajas de F9 en el F9 de la instancia, bastaría añadir su tipo a `TIPOS_F9`.
- **Límites conocidos:**
  - La Q, el nivel y el orden de F9 no cambian: `recalificacion_q: PENDIENTE` (modelo real; las dos fórmulas del criterio 2 no coinciden, INC-T198-01). Por eso PB-46 sigue «Superada en parte».
  - En backtest no hay FUE- (T-125), así que el camino solo se recorre en modo vivo o con pruebas que siembran F2.
  - `_comunicar_fiabilidad` corre en cada ciclo y lee F6 y F9 (sin FUE-, no escribe nada).
- **Comandos exactos para probarlo:**
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t198_buscador_ct19.py tests/test_t125_fiabilidad_fuentes.py tests/test_t125_r02.py tests/test_t125_r03.py`
  - `../../.venv/bin/python ../../.docs/tickets/T-198/mutantes.py .` (sobre una copia si hay otras sesiones en el mismo árbol)
  - Desde la raíz: `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-46`

## Ronda r02 (QA r01 NO APTO)

| Hallazgo | Corrección | Prueba de regresión (`tests/test_t198_buscador_ct19.py`) |
| --- | --- | --- |
| H-01 (media) | La del qa.md. `fiabilidad_f9.apartar_no_atendibles`, llamado en `_comunicar_fiabilidad` justo después de `por_comunicar` y antes de crear el CT-19: una FUE- cuya fuente ya no es de F9 (`fuente_de_opinion_registrada`) no va en el mensaje y deja UNA incidencia DATOS en HA (objeto AG-16, `run_id`) con la marca durable `fue_no_atendible: <fue_id>`; `por_comunicar` excluye las marcadas (`no_atendibles`). Las demás se envían y se atienden. `atender_ct19` sigue siendo todo o nada para un mensaje que llega de fuera. INC-T198-01 lo declara, con las bajas y borrados de F9 del PR 3 de Astra | `test_r02_h01_una_fue_cuya_fuente_salio_de_f9_no_bloquea_a_las_demas` (la del revisor, tres ciclos: A en F9, una marca, un solo CT-19, nada pendiente), `test_r02_h01_con_todas_las_fuentes_fuera_de_f9_no_hay_ct19` (M35–M37) |
| H-02 (baja) | La del qa.md: `ARCHIVOS_NUEVOS = ("F9",)` en `almacen.py` y la migración solo recorre esos | `test_r02_h02_solo_f9_se_sella_vacio_los_demas_borrados_fallan_cerrado` (el script del revisor hecho prueba: HA, F4 y F6); CA-6 sigue pasando para F9 (M38) |
| H-03 (baja) | La primera opción del qa.md: `comprobar_ct19(…, as_of)` exige un `timestamp` ISO 8601 (`RE_FECHA_ISO` del Evaluador), del calendario y no posterior a as_of (`_fecha_del_mensaje`); si no, `FiabilidadNoAtendible`. Se elige esta y no «escribir siempre as_of» porque así un mensaje de fuera con fecha imposible se rechaza en vez de pasar con otra fecha, y la línea de `fecha_ct19` que muta R8 del revisor no cambia. Se captura solo el `ValueError` de `date.fromisoformat` («2026-02-30» cumple el patrón) | `test_r02_h03_un_timestamp_posterior_a_as_of_o_que_no_es_fecha_no_se_atiende` (6 casos: 2099, el día siguiente, «ayer», 30 de febrero, None, un número), `test_r02_h03_un_timestamp_de_as_of_o_anterior_si`; la del revisor (M39–M42) |
| H-04 (media) | Las tres pruebas del qa.md | (a) CA-1 con un PRONOSTICO_FUENTE registrado el 10-06 (después de as_of): no cuenta (R1); (b) `test_r02_h04_una_fue_escrita_despues_de_as_of_no_se_atiende_en_as_of` (R2); (c) `test_r02_h04_en_un_ciclo_el_ct07_no_ve_fiabilidad_posterior_a_as_of` (R5) |
| H-05 (baja) | Las del qa.md | CA-1 afirma `metrica == metodo` de F6 (R3) y añade un CLM PREVISION con bloque que no cuenta (R6); `test_r02_h05_dos_bloques_a_la_vez_un_solo_ct19_y_ninguna_incidencia`: dos `Bloque` sobre la misma carpeta, con una barrera con plazo dentro de `por_comunicar` para que sin el cerrojo los dos lean lo pendiente antes de escribir (R4) |
| H-06 (baja) | `FMD-AAAA-nnnn` declarado en INC-T198-01, en el docstring del módulo y en la tabla de archivos del README del ejecutor; «transacción» cambiado por «cerrojo del almacén, sin vuelta atrás; si falla a mitad, lo escrito queda y el ciclo siguiente completa el resto sin duplicar» en el módulo, `atender_ct19`, el README del ticket, este análisis e INC-T198-01 | `test_r02_h06_si_el_almacen_falla_a_mitad_el_ciclo_siguiente_completa_sin_duplicar` (la del revisor); CA-1 afirma el prefijo `FMD-` |
| H-07 (media) | Gate completo con log propio y nuevo (`scratchpad/gate_t198_r02.log`), lanzado con `setsid nohup`; resultado en `pruebas.md` | el propio gate |

- Pruebas del revisor llevadas a la suite: H-01, H-03, el fallo a mitad (H-06) y el script de sellos (H-02). Las de datos hostiles y dos ciclos seguidos se quedan en `revisores/r01_ataques.py`, que pasa entero.
- Ninguna desviación de las correcciones del qa.md salvo la elección declarada en H-03 (la primera de las dos que propone).
- Las líneas que mutan los scripts del revisor (`r01_mutantes.py`, R1–R9) se conservan tal cual, para que se puedan volver a ejecutar sin cambiarlos.

## Ronda de cierre de la QA r02 (APTO pendiente de tres bajos)

| Hallazgo | Corrección | Prueba de regresión |
| --- | --- | --- |
| H-08 (baja) | La del qa.md: en `apartar_no_atendibles`, si F9 no tiene ninguna ficha cargada (`referencias.fichas["F9"]` vacío), no se marca ninguna FUE-; queda una incidencia DATOS sin marca y se devuelve la lista vacía, así que no hay CT-19 ese ciclo y todo se reintenta en el siguiente | `test_r02_f9_ilegible_un_ciclo_no_quema_las_fue` (la del revisor, llevada a la suite y reforzada: sin CT-19, sin marca, una incidencia, y las dos FUE- atendidas al volver F9); M43 y M44 |
| H-09 (baja) | Decisión del coordinador: `F9_bajas.md` sale de la lista de causas de INC-T198-01; lo retirado sigue siendo de F9 y no se aparta. Si al fusionar con el PR 3 hace falta otra cosa, se verá entonces | cambio de texto |
| H-10 (baja) | La del qa.md: en `test_ca3_dos_instancias_a_la_vez_…`, una barrera con plazo dentro de la sección crítica (envolviendo `fiabilidad_f9.atendidas`), como en la de H-05: sin el cerrojo los cuatro leen lo atendido antes de que nadie escriba | M12 muerto en `mutantes.py` con la máquina cargada; `revisores/r02_m12_repetido.py` sin vivos |

Por indicación del coordinador, sin gate completo en esta ronda (cambian una condición y pruebas; el de la r02 dio 12/12).
