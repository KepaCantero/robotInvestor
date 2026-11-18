# T-176 · Análisis técnico

## Causa raíz o motivo

PB-36 y PB-33 del Plan de pruebas V3.0 quedaban «Superada en parte» (INC-T116-03):

- **PB-36.** `Evaluador.recalibrar` solo movía los pesos de RK (P-11); el umbral E (P-09) no se recalibraba, ningún camino trataba un CALIBRABLE con banda PENDIENTE_OPERADOR (P-05) y la P3-EVAL- fuera de banda se quedaba en F6: nadie la enviaba por CT-19 ni la registraba en la cola de tipo 3 de HA.
- **PB-33.** La revocación y la lección de sobreconfianza quedaban como entradas sueltas de F6; no había sección «Novedades» (regla 7 del esquema de F6; 3.1 del Documento 0).

## Evidencia

- Fila de cada caso y su «No comprueba» en `docs/evidencias_pruebas_bloque_a.md` antes de T-176; INC-T116-03 (PB-33, PB-36).
- Anexo A del Documento 0 V5.3: «Umbrales de elegibilidad · E ≥ 60 … · Calibrable (±5/trimestre; ±10 total)»; esquema F10 V3.0 4.3: P-05 «PENDIENTE_OPERADOR»; regla 2 de F10: sin banda, todo cambio es tipo 3; esquema de F6 4.7 (P3-EVAL-, `elevada_via`) y regla 7 (Novedades).

## Implementación

- **`bloque_a/evaluador.py`**
  - `proponer_ajuste(param_id, componente, objetivo, evidencia, as_of, run_id)`: valida CALIBRABLE (si no, ValueError), lee vigente e inicial (`_valor_f10`: F10 o la clave de la configuración, `CLAVE_CONFIG_F10`), mira la banda en `evaluacion.bandas_f10` y deja AJU- PROPUESTO (dentro) o P3-EVAL- ENVIADA (fuera de banda / sin banda) con evidencia, impacto, pruebas de regresión y plan de reversión. Nunca escribe F10. Idempotente con la misma propuesta abierta.
  - `evidencia_umbral_e(as_of)`: índice de Youden sobre los PRG resueltos admisibles con la E de su opción.
  - `revision_trimestral(as_of, run_id)`: una por trimestre (`RTR-AAAA-Tn`), con los estimadores de `ESTIMADORES_TRIMESTRALES` (hoy, P-09 · E).
  - `publicar_novedades(as_of, run_id)`: sección `NOV-AAAA-Www` con altas, revocaciones, ajustes y lecciones nuevas.
  - `ajuste_en_sombra` solo devuelve AJU- de P-11 (la sombra de HT-03 compara pesos de RK).
  - `ciclo` llama a la revisión (tras la publicación de estados H5) y a Novedades (al final), las dos sin tumbar C5 si fallan (incidencia).
- **`bloque_a/orquestacion.py`**: `Bloque.elevar_propuestas_tipo3(as_of, run_id)` (CT-19 AG-20 → AG-18, entrada P3 PENDING_OPERATOR en HA por AG-18, `elevada_via` en F6), llamada en el ciclo después de `_comunicar_fiabilidad`. Además un `startswith` con tupla (PIE810) para bajar la cuota de ruff.
- **`config/por_defecto.yaml`**: `evaluacion.bandas_f10` (P-09 del Anexo A; P-05 PENDIENTE_OPERADOR).
- **`tests/test_t176_pb36_pb33.py`** (13 pruebas, con 4 casos parametrizados del límite de banda) y `tests/mapa_plan_pruebas.json` (PB-33 y PB-36 AUTOMATICA).
- **`docs/incidencias.md`**: INC-T176-01 y las dos líneas de INC-T116-03 marcadas «Aplicada en T-176».
- **`tools/cuotas.txt`**: ruff 2813 → 2812.

Decisiones y desviaciones: todas en INC-T176-01. Desviaciones del plan: las pruebas van en un solo fichero (`test_t176_pb36_pb33.py`) en lugar de dos; la revisión trimestral no deja RTR- cuando ningún estimador da objetivo (se repite en el C5 siguiente), en vez de dejarlo siempre.

Límites conocidos:
- Con datos del ejecutor F4 solo tiene opciones elegibles: el estimador del umbral E solo puede proponer subirlo.
- Sin estimador para P-05 (se prueba con evidencia sembrada, como dice la preparación del plan).
- La decisión del operador sobre la P3- no tiene lector (ni la de PB-48).
- La orden `evaluar` de la línea de órdenes no eleva (CT-19 exige `run_id`); lo hace el ciclo siguiente.
- «Novedades» no entra en el contexto de los agentes.
- Ningún golden de contratos cambia (no se toca la mensajería ni los esquemas).

Comandos exactos:

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q tests/test_t176_pb36_pb33.py
.venv/bin/python .docs/tickets/T-176/mutantes.py                  # desde la raíz: 28/28 muertos
.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-36     # y --pb PB-33
```

## Ronda r02 (QA r01 NO APTO)

Cada hallazgo con la corrección exacta de `qa.md` y su prueba de regresión en `tests/test_t176_pb36_pb33.py`:

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-01 (media) | `recalibrar` devuelve la P3- de P-11 abierta (ENVIADA, `parametro` P-11 u objeto «P-11 pesos de RK») en vez de crear otra; la nueva lleva `parametro` y `trimestre` | `test_r02_h01_recalibrar_dos_semanas_deja_una_p3_de_p11_en_f6_y_en_ha` |
| H-02 | `plan_reversion` en la P3- de P-11 (mismo texto que `proponer_ajuste`) | `test_p3_de_p11_tambien_se_eleva` (ampliada) |
| H-03 | En `proponer_ajuste`, una P3- ENVIADA del mismo parámetro y componente bloquea cualquier objetivo; el AJU- PROPUESTO solo el mismo; el RTR- registra la abierta | `test_r02_h03_una_p3_abierta_del_parametro_bloquea_cualquier_otro_objetivo`, `test_r02_h03_la_revision_registra_la_p3_abierta` |
| H-04 | `with self.almacen._transaccion()` en `proponer_ajuste`, `revision_trimestral` y `Bloque.elevar_propuestas_tipo3` (cuerpos en `_proponer_ajuste`, `_revision_trimestral` y `_elevar_propuestas_tipo3`) | `test_r02_h04_propuestas_y_revisiones_concurrentes_no_se_duplican`, `test_r02_h04_elevaciones_concurrentes_dejan_una_entrada_en_ha` |
| H-05 | `evaluacion.bateria_regresion` (§6 del plan, literal) y `evaluacion.regresion_r18` (PB-10, PB-34, PB-35, PB-36, PB-50) en `por_defecto.yaml`; `pruebas_regresion_p3(cfg)` en `proponer_ajuste` y `recalibrar`; fuera `PRUEBAS_REGRESION_AJUSTE` | `test_pb36_umbral_e_…` y `test_p3_de_p11_…` comparan con la lista |
| H-06 | Pendientes de elevar: las P3-EVAL- sin `elevada_via` **o** sin entrada en HA | `test_r02_h06_una_p3_con_elevada_via_pero_fuera_de_ha_se_eleva` |

Mutantes nuevos M29–M37 (y M15 sobre la línea nueva de H-03). INC-T176-01 con la ronda r02.

## Ronda de cierre de la QA r02 (H-07)

`recalibrar` pasa su cuerpo a `_recalibrar` y queda como `with self.almacen._transaccion(): return self._recalibrar(as_of, run_id)`, para que la deduplicación de la P3- de P-11 (H-01) compruebe y escriba de una vez. Regresión: `test_r03_h07_seis_recalibraciones_a_la_vez_dejan_una_sola_p3_de_p11`; mutante M38 (sin la transacción).
