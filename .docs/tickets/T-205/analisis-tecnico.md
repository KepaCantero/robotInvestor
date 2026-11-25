# T-205 · Análisis técnico

## Causa raíz

`seguimiento.py` no comprobaba en ningún punto que la clase de la opción fuera uno de los doce tipos de activo:

- `_alta` copiaba en F11 `f3[opp_id].get("clase")` tal cual.
- `ciclo_c6` tomaba `opp.get("clase") or enc.get("clase")` y emitía el CT-05 con `nivel_por_clase` y `presupuesto_por_clase` para esa clase, y el CT-06 a `b_agente(clase)`.
- `b_agente` devolvía `AGENTE_CLASE.get(clase, "AG-03")`: una clase desconocida, vacía o None iba al AG-03.

T-201 dejó ese valor por defecto explícito para el None y anotó el defecto en INC-T201-01, sin cambiarlo, porque un ticket de cuotas no cambia comportamientos. La QA r01 de T-201 lo reprodujo con `.docs/tickets/T-201/revisores/r06_b_agente.py`: CT-06 de AG-02 a AG-03, ninguna incidencia, y G3 BLOQUEADO solo después.

## Evidencia

Con `r06_b_agente.py` sobre `origin/develop` 358576c3:
- «XYZ» y `""`: `ct06_registrado [["AG-02","AG-03"]]`, `dictamen_g3v ["BLOQUEADO"]` e `incidencias_nuevas_en_HA []`.
- Con T-205: `ClaseNoAdmitida` en las dos altas, cada una con su INC- en HA (OTRO, «clase», fase ALTA). La opción DIV de control no cambia: su CT-06 va al AG-05, como antes.

## Archivos cambiados

- `bloque_a/11_Ejecutor/bloque_a/seguimiento.py`:
  - `ClaseNoAdmitida(ValueError)` con `inc_id`, y `clase_admitida(clase) -> TypeGuard[str]` (una de las doce claves de `AGENTE_CLASE`; None, `""`, otra grafía u otro tipo no lo son). `AGENTE_CLASE` se importa arriba (`contratos` no importa nada del paquete, así que no hay ciclo).
  - `procesar`: en un ALTA, `_exigir_clase_alta` va antes de registrar el CT-24 de entrada. `_alta` lo vuelve a llamar tras comprobar que la OPP- existe, por si se llama directamente o la clase cambia entre medias.
  - `_exigir_clase_alta`: si la OPP- está en F3 y su clase no se admite, escribe el INC- y lanza `ClaseNoAdmitida`. Si no está en F3, no hace nada y queda el `KeyError` de `_alta`.
  - `_seq_clase`: el `_seq` de la última entrada de F3 de la opción que lleva la clave `clase`.
  - `ciclo_c6`: la clase es `opp.get("clase")`, sin el respaldo de F11, y se comprueba lo primero. Si no se admite, devuelve `_c6_clase_no_admitida`.
  - `_c6_clase_no_admitida`: en una `almacen._transaccion()`, busca en HA un INC- de fase C6 y `campo_afectado` «clase» con la misma clave (`seg_id`, `f3_seq_clase`, `ciclos_encargo`). Si lo encuentra, lo cita; si no, lo escribe. Devuelve `{"seg_id", "opp_id", "ejecutado": False, "motivo", "inc_id", "incidencia_nueva"}`.
  - `b_agente`: lanza `ClaseNoAdmitida` si la clase no se admite. Si se admite, devuelve `AGENTE_CLASE[clase]`.
- `bloque_a/11_Ejecutor/tests/test_t201_cuotas.py`: `test_b_agente_da_el_analista_de_su_clase_o_falla` mantiene sus seis casos. Ahora None, «XYZ» y `""` esperan `ClaseNoAdmitida` (decisión 1 del coordinador).
- `bloque_a/11_Ejecutor/tests/test_t205_clase_seguimiento.py` (nuevo): 25 pruebas.
- `docs/incidencias.md` (INC-T205-01), la deuda técnica (fila T-205) y este ticket.

## Decisiones y desviaciones

- **`b_agente` falla, en contra de lo que dejó T-201.** T-201 solo conservó el comportamiento anterior, sin decidirlo; su propia incidencia dice que «lo coherente con falla cerrado sería rechazarlo». Manda T-205 (decisión 1 del coordinador). `b_agente` solo lo llama el C6, y el C6 comprueba antes la clase, así que la excepción de `b_agente` es una segunda barrera que no se dispara en el flujo normal.
- **INC- de tipo OTRO, sin el valor** (decisión 2). El detalle y los campos de trazabilidad no copian la clase.
- **Deduplicación sin el valor** (decisión 3). La propuesta del coordinador era una incidencia «por opción y valor de clase». Como el valor no puede ir en HA, se identifica por la entrada de F3 que lo fija (`f3_seq_clase`). Así, una nueva escritura de la clase abre otra incidencia aunque repita el valor: un caso más estricto que «por valor», no más laxo. `ciclos_encargo` separa episodios: si la clase se corrige, el ciclo se hace y luego se vuelve a estropear, hay otra incidencia.
- **El respaldo de F11 desaparece.** El informe siempre tomó la clase de F3. Con el respaldo, el CT-05 y el CT-06 podían ir en una clase y el informe en otra (o en None, y G3 lo bloqueaba).
- **La clase se comprueba antes que la absorción en C1.** Así se valida al principio, como en el resto del ejecutor, y una opción VIGENTE con la clase estropeada no se omite como si C1 la cubriera.
- Sin desviaciones del plan.

## Límites conocidos

- El seguimiento solo lee `clase`. Una ficha de F3 con solo `tipo_activo` se rechaza (INC-T205-01). El ejecutor siempre escribe los dos.
- `MODIFICACION`, `PAUSA`, `REANUDACION` y `CANCELACION` de un encargo con la clase estropeada siguen funcionando: no encargan nada a un Analista y permiten que el Broker lo cancele.
- La deduplicación lee HA entero solo cuando hay un rechazo. En el ciclo normal no se lee.
- `ClaseNoAdmitida` sale por la CLI como cualquier `ValueError` del seguimiento (igual que una frecuencia no admitida).

## Cómo probarlo

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q tests/test_t205_clase_seguimiento.py tests/test_t201_cuotas.py tests/test_v51.py
../../.venv/bin/python ../../.docs/tickets/T-205/mutantes.py .
../../.venv/bin/python ../../.docs/tickets/T-201/revisores/r06_b_agente.py . "$(mktemp -d)"   # reproducción de la QA r01 de T-201
```

## Ronda de cierre de la QA r01 (25-11-2026)

La QA r01 dio APTO con tres hallazgos bajos (`qa.md`). Ninguno cambia `seguimiento.py`: los tres se corrigen con pruebas, mutantes y documentación.

| Hallazgo | Corrección | Regresión |
| --- | --- | --- |
| H-01: ninguna prueba veía el orden de la comprobación de la clase frente a la absorción en C1 (mutante Q1 vivo) | Prueba nueva `test_c6_una_opcion_vigente_con_clase_no_admitida_no_se_omite_cubierta_en_c1`. Con F3 «XYZ» y VIGENTE, exige INC- de fase C6, ningún CICLO_OMITIDO, F11 igual y ningún mensaje (modelo: A4 de `revisores/r01_02_ataques.py`) | Q1 pasa a `mutantes.py` y muere |
| H-02: el fallo al escribir el INC- del alta no tenía prueba (mutante Q2 vivo) | Prueba nueva `test_alta_con_ha_rota_sube_el_error_de_ha_y_solo_cambia_el_contador_de_inc`. Con la escritura de HA rota, exige que suba el `OSError` de HA, que solo cambie el contador de INC- y que no haya mensajes, encargo ni INC- (modelo: A6) | Q2 pasa a `mutantes.py` y muere. El ejecutor de mutantes admite ahora varias sustituciones por mutante, porque Q2 las necesita |
| H-03: el nombre de la prueba de `b_agente` de T-201 decía lo contrario de lo que comprueba | Renombrada a `test_b_agente_da_el_analista_de_su_clase_o_falla` en `tests/test_t201_cuotas.py`, `mutantes.py` (PRUEBAS), `pruebas.md`, este análisis y `handoff.md`. En INC-T201-01 (`docs/incidencias.md`) se añade «Lo corrige T-205 (INC-T205-01)» | La prueba renombrada pasa, y M1 a M3 siguen muriendo con ella |
| Fuera de los hallazgos: Q11 del revisor (deduplicación fuera de la transacción) murió en la r01 de la QA, pero quedó vivo en la primera pasada de esta ronda, porque la prueba de seis procesos solo lo ve si la carrera llega a darse | Prueba nueva, determinista, `test_c6_la_lectura_de_ha_y_el_inc_van_en_la_misma_transaccion`. Justo después de que el C6 lea HA, otra instancia del almacén intenta el mismo C6 en un hilo. Con la transacción, espera al cerrojo y cita el INC- ya escrito; sin ella, escribe el suyo | Q11 pasa a `mutantes.py` y muere siempre. Se comprobó aplicándolo a mano: la prueba falla |

No se tocan los scripts del revisor (`revisores/`). Su `r01_mutantes.py` sigue citando el nombre antiguo en `PRUEBAS`, así que se ejecuta con una copia temporal que solo cambia ese nombre (ver `pruebas.md`).
