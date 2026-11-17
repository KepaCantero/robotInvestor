# T-174 · Análisis técnico

## Causa raíz

`ConsultasBroker.responder` (`bloque_a/11_Ejecutor/bloque_a/interfaz_broker.py`) registraba la respuesta y, si la consulta estaba `VENCIDA`, solo devolvía un texto («se trata como petición de revisión (C2)»). Faltaban dos cosas para cumplir §7.9.5:

- no se lanzaba ninguna revisión;
- el ejecutor no guardaba qué informe entregado llevaba qué supuesto, así que no podía saber si había un «informe ya entregado» que revisar.

## Implementación

| Archivo | Cambio |
| --- | --- |
| `bloque_a/interfaz_broker.py` | `responder(..., ejecutar_revision=True)`. Registra en la CNS- los `indices_respondidos`, busca los RUN- entregados con la CNS- en `supuestos_cns` (`_entregados_con`) y, si la respuesta contesta un índice nuevo, abre la revisión (`_revision_c2`): un `ciclo` `AD_HOC` con disparador `CT-23`, que queda en F5 en `revisiones_c2`. `_contestadas` filtra los índices válidos. `nota_revision(disparador)` da el texto que el paquete de la revisión declara en `limitaciones`. Importa `respuesta_final` para relanzar los errores de control o de integridad (como T-169). |
| `bloque_a/orquestacion.py` | Dos líneas: `limitaciones += self.consultas.nota_revision(disparador)` en el F0 de `ciclo`, y `supuestos_cns` en el RUN de F5 (`_registrar_run`), solo si el paquete lleva supuestos. |
| `bloque_a/seguimiento.py` | `supuestos_cns` en el RUN_C6 de F5. Además se quitan dos importaciones sin uso (`copy` y `typing`), con lo que ruff baja 5. |
| `tests/test_t174_pb61_revision_c2.py` | 8 pruebas nuevas (ver `pruebas.md`). |
| `tests/mapa_plan_pruebas.json` | PB-61 → AUTOMATICA, con sus pruebas, `comprueba` y `no_comprueba`. |
| `README.md` del ejecutor | Un párrafo en «Consultas al Broker (CT-23)». |
| `docs/incidencias.md` | INC-T174-01 `[PROPUESTO]`, y la línea de PB-61 de INC-T116-03 marcada como aplicada. |
| `docs/evidencias_pruebas_bloque_a.md` | Regenerado con `evidencias_plan_a.py --ejecutar`. |
| `tools/cuotas.txt` | ruff 2813 → 2808. |

## Decisiones (INC-T174-01, `[PROPUESTO]`)

- **Qué cuenta como invalidación.** Toda respuesta con texto a un índice no contestado antes: el ejecutor no juzga el sentido del texto, y el Anexo B no tiene una marca de confirmación. Se prefiere una revisión de más a dejar sin revisar un informe apoyado en un supuesto que el Broker ya ha contestado.
- **Qué consultas abren revisión.** También la `NO_BLOQUEANTE` contestada en plazo tras una entrega (§7.9.4). `tardia` conserva su significado.
- **Alcance de la revisión.** Los tipos de la CNS- o, si no declara ninguno, los de los RUN- revisados y los C6. Nivel por defecto del AD_HOC; ningún número nuevo.
- **Contratos.** Sin contrato ni mensaje nuevo: la revisión se comunica con su CT-02 y con la salida de `responder`. Los goldens de contratos coinciden sin re-congelar.

## Desviaciones del plan

- La prueba de «pendiente y fallida» se partió en dos: `test_pb61_revision_pendiente_sin_ejecutar` y `test_pb61_revision_fallida_queda_anotada_y_el_error_de_control_se_relanza`.
- Se añadió `test_pb61_un_run_bloqueado_no_cuenta_como_entregado`.
- `responder` devuelve siempre la clave `revision_c2`, que es `None` cuando no hay revisión.

## Límites conocidos

- La respuesta del Broker llega al análisis solo por la pregunta del alcance de la revisión (`foco` de la orden a los Analistas). El ciclo periódico siguiente no la lee.
- Una consulta respondida en `PARCIAL` deja de declarar el supuesto de las preguntas sin contestar. El comportamiento es anterior a T-174 y no se ha cambiado.
- Los RUN- anteriores a T-174 no tienen `supuestos_cns` y no se revisan.
- Con el cliente simulado no se mide si el modelo real inventa un dato del Broker. Eso queda en «No comprueba» de PB-61, para el modo sombra.

## Cómo probarlo

```bash
cd bloque_a/11_Ejecutor
pytest -q tests/test_t174_pb61_revision_c2.py tests/test_v51.py
python tests/goldens_ct.py                                   # goldens de contratos: coinciden
python ../../.docs/tickets/T-174/mutantes_t174.py .. /tmp/copia_t174   # 11 mutantes, todos mueren (M0 sin mutar vive)
cd ../.. && .venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-61
```

El ciclo simulado por la línea de órdenes está en `pruebas.md`.

## Ronda r02 (QA r01 NO APTO, H-01 a H-06)

- **`interfaz_broker.py`: comprobar y reservar.** `responder` calcula los textos contestados fuera del cerrojo; dependen solo de las preguntas, que no cambian, y así un `_contestadas` lento no retiene el cerrojo. Después, bajo `almacen._transaccion()`, relee la CNS-, calcula lo nuevo y lo entregado (a la fecha de la respuesta) y escribe una sola entrada: respuesta, `indices_respondidos` y la reserva en `revisiones_c2` (`EN_CURSO`, o `PENDIENTE` con `ejecutar_revision=False`), con `msg_id`.
- **`interfaz_broker.py`: ejecutar y anotar.** `_ejecutar_revision` lanza el ciclo fuera del cerrojo, con `intento` en el disparador. `_anotar_revision` cambia el elemento por `msg_id` bajo el cerrojo.
  - Un error de control o de integridad deja `INTERRUMPIDA` (si el almacén está íntegro) y una incidencia escalada, y se relanza.
  - Un fallo tras escribir el RUN- toma el estado de su `entrega`.
  - Sin tipos que revisar queda `SIN_ALCANCE`, sin ciclo.
- **`interfaz_broker.py`: relanzar.** `revisiones_pendientes()` lista las revisiones que no han llegado al Broker. `relanzar_revisiones()` reclama cada una bajo el cerrojo antes de lanzarla. `responder` relanza las `INTERRUMPIDA` y `PENDIENTE` de su CNS-.
- **`cli.py`:** `consulta-broker revisiones` y `consulta-broker relanzar [--cns] [--incluir-en-curso]`.
- **Desviación:** las `EN_CURSO` no se relanzan solas desde `responder`. Otro proceso puede estar ejecutándolas (con A2, el segundo proceso las relanzaría y duplicaría la revisión: H-01 otra vez), así que solo se relanzan si se pide expresamente, tras comprobar que el proceso que las lanzó ya no corre.
- **Desviación:** el A8 de la r01 afirmaba `FALLIDA`; con la corrección de H-05 el estado es `ENTREGADA` y A8 falla a propósito.

## Ronda r03 (QA r02, H-07 y H-08)

- **`interfaz_broker.py`: detección de huérfanas.**
  - Hay un conjunto `_EN_MARCHA`, común al proceso, con las revisiones que se están ejecutando; `_ejecutar_revision` las añade y las quita en un `finally`.
  - Hay dos funciones nuevas, `_proceso()` y `_pid_vivo()`; la segunda da `None` en Windows, donde la señal 0 no sirve para consultar.
  - Hay tres métodos nuevos: `_es_huerfana`, `huerfanas()` (con el aviso único bajo el cerrojo) y la marca `huerfana` en `revisiones_pendientes`.
- **`interfaz_broker.py`: intentos y reclamaciones.**
  - `_reserva` deja `proceso` e `intentos: 1` (o `0` si queda PENDIENTE).
  - `relanzar_revisiones` reclama con `proceso` e `intentos + 1`, y antes da por ENTREGADA una EN_CURSO o INTERRUMPIDA cuyo RUN- ya llegó a F5.
  - `_ejecutar_revision` usa el `intentos` reclamado como `disparador.intento` y ya no lo reescribe al terminar.
- **`orquestacion.py`:** una línea al empezar `ciclo`, `self.consultas.huerfanas()`.
- **Límite:** desde otro host no se puede saber si el proceso vive, así que esas revisiones no se marcan; tampoco las reservadas antes de la r03, que no tienen `proceso`. Sin umbral de tiempo, como pidió la QA.

## Ronda de cierre de la QA r03 (H-09 a H-11)

- **`_en_marcha(cns_id, msg_id, alta)`.** La clave lleva la carpeta resuelta del almacén (H-10). En `responder`, el alta va dentro del cerrojo, antes de escribir la reserva EN_CURSO, y la baja en un `finally` que cubre la escritura, `_ejecutar_revision` y SIN_ALCANCE. En `relanzar_revisiones` es igual, alrededor de la reclamación y de la ejecución (H-09).
- **`_es_huerfana` devuelve True, False o None.** None cuando no se puede juzgar: otro host, sin `proceso` o pid no consultable. `huerfanas()` solo avisa con True y vuelve a comprobarlo bajo el cerrojo. `revisiones_pendientes` pone `huerfana: None` y una nota en las EN_CURSO que no se pueden juzgar (H-11).

