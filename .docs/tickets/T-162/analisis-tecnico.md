# T-162 · Análisis técnico

## Causa raíz o motivo

`Bloque.consulta` (`bloque_a/11_Ejecutor/bloque_a/orquestacion.py`) clasifica la consulta y, si es de ruta ANALITICA, lanza el
RUN- ad hoc de forma síncrona y después crea **una sola** CT-03 RETORNO: la provisional, con el `escalado` (nivel, plazo, RUN- y
su estado). No había código que, con el RUN- terminado, respondiera al Broker con lo que el análisis entregó, que es lo que piden
§7.6.3 del Documento 0 («entrega primero una respuesta provisional») y PB-07 («respuesta final por CT-03 con referencias»).
Además, si el RUN- lanzaba una excepción, subía sin dejar ni la provisional ni rastro en F5 (INC-T116-03, fila PB-07).

## Evidencia

- Antes: `test_pb07_la_consulta_de_contraste_responde_provisional_con_nivel_y_plazo` encuentra una CT-03 RETORNO por consulta; el
  mapa (`tests/mapa_plan_pruebas.json`) daba PB-07 por PARCIAL con ese hueco.
- Después, con el simulado (`../../.venv/bin/python -m pytest -q tests/test_t162_respuesta_final.py -k pb07`, desde
  `bloque_a/11_Ejecutor`), la consulta del plan da: CT-03 ENCARGO → CT-05 AD_HOC → … → CT-02 del RUN- → CT-03 provisional →
  CT-03 final, con `respuesta_final.resultado_analisis` ENTREGADO, el `run_id` en el sobre y 25 referencias (el RUN-, tres OPP-
  y sus TND-, CLM- y PRG-).

## Implementación

### Archivos cambiados y por qué

| Archivo | Cambio |
| --- | --- |
| `bloque_a/11_Ejecutor/bloque_a/respuesta_final.py` (nuevo) | `ESQUEMA` (JSON Schema 2020-12 del cuerpo de la final, con las reglas de coherencia entre resultado y referencias), `construir` (cuerpo determinista desde F1–F5), `validar` (esquema + estado común coherente con el resultado), `registrada` (la final guardada en F5) y `enviar` (idempotente, bajo la transacción del almacén: comprobar F5 → construir → validar → `Mensajeria.crear` → F5) |
| `bloque_a/11_Ejecutor/bloque_a/orquestacion.py` | Solo `consulta`: el `self.ciclo(...)` del escalado va en `try/except Exception` (fallo: incidencia HERRAMIENTA en HA con la clase del error, `estado_run` FALLIDO y el RUN- si llegó a F5); tras la provisional, `respuesta_final.enviar(...)` si hubo escalado; la salida añade `respuesta_final`. El camino sin fallo deja la provisional igual, byte a byte |
| `bloque_a/11_Ejecutor/tests/test_t162_respuesta_final.py` (nuevo) | 22 pruebas (ver `pruebas.md`) |
| `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json` | PB-07 pasa a AUTOMATICA con las pruebas nuevas; `no_comprueba` deja solo lo que exige el modelo real |
| `docs/evidencias_pruebas_bloque_a.md` | Regenerado con `.docs/scripts/evidencias_plan_a.py --ejecutar` |
| `docs/incidencias.md` | INC-T162-01 y la nota «Aplicada en T-162» de PB-07 en INC-T116-03 |
| `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` | Una fila en §6 |
| `bloque_a/11_Ejecutor/README.md` | Un punto en §9 bis |

No se tocan `contratos.py` (el canal AG-01 → BROKER y los campos mínimos de CT-03 ya admiten la final), `cli.py` (imprime la
salida de `consulta`, que ya lleva la final), los goldens, el corpus ni el Documento 0.

### Forma del mensaje nuevo

```json
{"msg_id": "MSG-2026-000011", "contrato": "CT-03", "version_contrato": "5.1", "emisor": "AG-01", "receptor": "BROKER",
 "timestamp": "…", "tipo_mensaje": "RETORNO", "query_id": "QRY-2026-0001", "run_id": "RUN-2026-0002",
 "consumo": {}, "estado": "COMPLETO", "autoevaluacion": "",
 "limitaciones": ["…las del RUN-…"],
 "clase_consulta": "CONTRASTE", "ruta": "ANALITICA",
 "respuesta": "Análisis RUN-2026-0002 terminado completo y entregado (nivel N2; Renta variable). Opciones del top-3: Renta variable: OPP-2026-0001 «…» (confianza probable), …",
 "referencias": ["RUN-2026-0002", "OPP-2026-0001", "TND-2026-0001", "CLM-2026-0001", "…", "PRG-2026-0010", "…"],
 "confianza": "probable",
 "escalado": {"nivel": "N2", "clases": ["RV"], "plazo_estimado": "…", "respuesta_provisional": "…", "run_id": "RUN-2026-0002", "estado_run": "COMPLETO"},
 "respuesta_final": {"provisional_msg_id": "MSG-2026-000010", "resultado_analisis": "ENTREGADO"}}
```

En F5, una entrada más del mismo QRY- (autor AG-01): `{"tipo_entrada": "QRY", "id": "QRY-…", "estado": "RESPONDIDA_FINAL" |
"FINAL_SIN_RESULTADO", "respuesta_final": <el mensaje sin el sobre, con msg_id, timestamp, run_id y estado>,
"referencias_descartadas_final": […]}`.

### Decisiones tomadas y desviaciones del plan

- Todas las de INC-T162-01, `[PROPUESTO]`: campo `respuesta_final`; cinco resultados; referencias (RUN-, OPP-, TND-, CLM-, PRG-;
  sin HIT-); existencia estricta (clave de una entrada, no una mención: más estricta que la de la ruta N0, que acepta cualquier
  mención); confianza; texto del código; final también si el RUN- falla o no se lanza; la excepción del RUN- no se relanza.
- El esquema de la final vive en `respuesta_final.ESQUEMA` y no en `contratos.ESQUEMAS`, que son las salidas de los agentes y
  tienen su golden (`esquemas_respuestas.json`). Reutiliza de `ESQUEMAS["CONSULTA"]` los enumerados de `clase_consulta` y
  `confianza`.
- `respuesta_final.enviar` usa `Almacen._transaccion()` (privada, reentrante en el mismo hilo y con cerrojo de fichero entre
  procesos) para que la comprobación de F5 y la escritura sean atómicas; dentro, `Mensajeria.crear` y `Almacen.escribir` vuelven
  a entrar en ella sin bloquearse.
- Desviación del plan: `tests/MAPA_PLAN_DE_PRUEBAS.md` no se toca (es el mapa histórico del 3-11, conservado tal cual por T-116).

### Goldens: no se re-congelan (para coordinar)

`../../.venv/bin/python tests/goldens_ct.py` (desde `bloque_a/11_Ejecutor`) da **1 diferencia**:
`formas_flujos_mock.json`, solo en el flujo `consulta_que_escala`, solo en `CT-03.RETORNO`, y solo añade (las otras seis goldens,
`divergencias_anexo_b.json` incluida, coinciden: la final cumple el esquema derivado del Anexo B de CT-03). Huella congelada
`693eda19…7482`; la generada con T-162, `6b7339b2…6c24`. En `test_fase3_goldens.py` falla por eso
`test_ca1_cada_golden_coincide_byte_a_byte[formas_flujos_mock.json]` (y nada más). Diff exacto:

```diff
--- tests/goldens/formas_flujos_mock.json (congelado)
+++ generado con T-162
@@ -1459,7 +1459,8 @@
     },
     "CT-03.RETORNO": {
      "combinaciones_de_claves_a_veces": [
-      ""
+      "",
+      "respuesta_final run_id"
      ],
      "emisores": [
       "AG-01"
@@ -1467,7 +1468,12 @@
      "receptores": [
       "BROKER"
      ],
-     "rutas_a_veces": {},
+     "rutas_a_veces": {
+      "limitaciones[]": "string",
+      "referencias[]": "string",
+      "respuesta_final": "object",
+      "run_id": "string"
+     },
      "rutas_siempre": {
       "autoevaluacion": "string",
       "clase_consulta": "string",
@@ -1490,6 +1496,8 @@
       "receptor": "string",
       "referencias": "array",
       "respuesta": "string",
+      "respuesta_final.provisional_msg_id": "string",
+      "respuesta_final.resultado_analisis": "string",
       "ruta": "string",
       "timestamp": "string",
       "tipo_mensaje": "string",
@@ -1500,7 +1508,8 @@
        "CONTRASTE"
       ],
       "confianza": [
-       "especulativo"
+       "especulativo",
+       "probable"
       ],
       "ruta": [
        "ANALITICA"
```

Lectura: `rutas_siempre` no pierde ninguna ruta (la provisional no cambia); las de `respuesta_final.*` salen en «siempre» porque
la regla de `goldens_ct.rutas` cuenta sobre los objetos `respuesta_final` vistos, que son uno. Para re-congelar, cuando lo decida
la sesión coordinadora (con el Anexo B de la V5.2 describiendo la final):
`../../.venv/bin/python tests/goldens_ct.py --update --motivo "T-162: respuesta final por CT-03 de una consulta escalada (PB-07)"`.

### Límites conocidos

- En el ejecutor síncrono la provisional se crea al terminar el RUN- (no se cambia para no tocar su forma) y la final justo
  después: el Broker las recibe seguidas. El tiempo real de la provisional (< 2 minutos) solo se mide con la API (modo sombra).
- El texto de la final es mecánico (identificadores, nombres y confianzas); no resume la tesis de cada opción.
- Un fallo entre la creación del mensaje y su escritura en F5 (por ejemplo, un disco lleno) dejaría el mensaje en el registro en
  memoria sin la marca de F5: un reintento lo volvería a crear. F5 es el registro persistente; el resto del bloque hace lo mismo.
- Con `--sin-escalado` la final (NO_EJECUTADO) sale a la vez que la provisional, cuyo `plazo_estimado` sigue diciendo «mismo
  día»: el texto de la provisional no se toca.

### Comandos exactos para probarlo

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t162_respuesta_final.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_integracion.py tests/test_fase4_huecos.py tests/test_t65_qa_r01.py \
  tests/test_t66_propuestas.py tests/test_t101_v6.py tests/test_t87_contratos.py tests/test_t92_revision.py tests/test_fase3_goldens.py
../../.venv/bin/python tests/goldens_ct.py            # 1 diferencia esperada: formas_flujos_mock.json (ver arriba)
../../.venv/bin/python -m bloque_a.cli --datos ejemplos/datos_sinteticos --estado "$TMP/estado" --salida "$TMP/sal" \
  --as-of 2026-06-05 consulta "¿Qué opinas del oro frente a la plata a 6 meses?"
cd ../.. && .venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-07
```
