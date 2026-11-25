# QA · T-183 · Contar raíces, no menciones (PB-29)

## Ronda r01 · 24-11-2026 · Claude (revisor independiente; implementó Astra)

**Veredicto: NO APTO.** Un hallazgo alto y cinco medios (H-01 a H-06).

### Qué se revisó

- El código del PR 3: la rama `astra/encargos-bloque-a-c38-c47`, en la punta `2d99af6`, sobre `develop` `9ce57b2`. Es el commit `1fffe53`, más los retoques posteriores de `5ef929b` (orden de imports) y `942e74e` (referencias.py, ajeno). Se revisó en un worktree limpio.
- La vara de medir: el criterio del plan para PB-29 («G3-DAT-09 coherente; el Auditor no encuentra doble cómputo») y el resultado esperado («1 raíz y 20 derivadas; `raices_independientes` = 1; PS1 no superada salvo que la raíz sea primaria de nivel A»).
- La definición de G3-DAT-09 en la tabla G3 del system prompt del Orquestador técnico: «`resumen_raices` de una conclusión principal no coincide con el cómputo de raíces independientes de F2».
- El esquema de F2 (reglas 2 y 3 y §4: `grado_independencia`, `raiz_evd_id`) y, del Documento 0 V5.3, CT-11 (los duplicados y las raíces los asigna el ejecutor en código) y PS1.

### Reproducción

| Comprobación | Resultado |
|---|---|
| `tests/test_t183_raices.py` y sus vecinas (`test_t65_qa_r01`, `test_t181_fuentes`, `test_t182_procedencia`, `test_t53_seleccion_y_entrega`, `test_t87_agentes`, PB-26 de T-126) | Verde |
| La prueba nueva sin el cambio (el código de `1fffe53` revertido en el worktree y restaurado después) | Falla (`test_t183_raices.py:28`), como debe |
| `.docs/tickets/T-183/mutantes.py`, el de Astra | Sus 2 mutantes mueren |
| `revisores/r01_mutantes.py`, 9 mutantes propios | Mueren 2 (M6, que lo mata `test_t65`, y M8). Quedan vivos 7: M1, M2, M3, M4, M5, M7 y M9 (H-05) |
| `revisores/r01_ataques_raices.py`, 12 ataques | 4 en verde y 8 en rojo (H-01 a H-04 y H-06) |
| Cuotas sobre lo tocado, frente a `9ce57b2` | No suben: ruff con la configuración del gate da 0 en los ficheros tocados (2807 en total, igual que la cuota) y mypy de A da 102, igual que antes |
| Esquemas, corpus, goldens y R8 | Sin cambios por este ticket. El re-congelado de `formas_flujos_mock.json` es de T-185 |
| G3-MET-13 | Ningún texto nuevo usa la raíz «valid-» |

Lo que sí funciona:

- G3-DAT-09 corre en los paquetes reales del ciclo mock y sale OK (a01).
- Una cifra de raíces manipulada en F2 bloquea el dictamen de un paquete real (a02).
- La raíz primaria de nivel A con 20 derivadas supera PS1 (a07).
- Si las derivadas llegan un ciclo antes que el original, el recuento queda en 1 y la repetición es idempotente (a11).

Cómo reproducirlo, desde `bloque_a/11_Ejecutor`:

```bash
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-183/revisores/r01_ataques_raices.py
../../.venv/bin/python ../../.docs/tickets/T-183/revisores/r01_mutantes.py   # desde la raíz del repo: .venv/bin/python .docs/…
```

### Hallazgos

#### H-01 · alta · G3-DAT-09 no compara el paquete con F2

- **Qué pasa.** `sintesis.control_raices` compara dos datos de F2 entre sí: el `raices_independientes` guardado y el que sale de recontar las mismas EVD de F2. No mira lo que declara la conclusión en el paquete, que es `puertas.PS1` de cada opción, y eso es justo lo que define G3-DAT-09. La puerta PS1 de la opción sale de la unión de las raíces de sus CLM (`f["_raices"]`), y nadie la contrasta con F2.
- **Cómo reproducirlo.** Ataque a03. Se rebajan a nivel C las EVD de PS1 de la primera opción de un paquete real. Recontada desde F2, la opción ya no supera PS1, pero el paquete sigue declarando `PS1 = True`. Aun así, G3-DAT-09 da OK y el dictamen sale APTO.
- **Corrección exacta.**
  - `control_raices(paquete, clms, evds, ps1)` recibe `bloque._ps1`.
  - Por cada opción, calcula la unión de `raices_de_clm` de las CLM que cita, con la misma regla que `_guardar_lote_evidencia`.
  - Añade un BLOQUEO «PS1 declarada sin respaldo de raíces en F2» si `ps1(union) != op["puertas"]["PS1"]`.
  - Mantiene la comprobación por CLM que ya existe.
  - Si `puertas` o `PS1` faltan en la opción, también es BLOQUEO.
  - No hace falta tocar ningún esquema: `puertas` ya está en el paquete.
- **Prueba de regresión.** a03 en `tests/test_t183_raices.py`, sobre un paquete de un ciclo mock.

#### H-02 · media · G3-DAT-09 falla abierto en dos casos

- **Qué pasa.**
  - (a) Una CLM sin la clave `evidencias_ps1` no se comprueba: `if "evidencias_ps1" in clm`. En el ciclo mock son 28 de las 98 CLM, todas las que tienen 0 raíces. Con su `raices_independientes` manipulado a 5, el control da OK.
  - (b) Si una opción cita una CLM que no existe en F2 a la fecha del paquete, `clms.get(cid, {})` la salta y el control da OK.
- **Cómo reproducirlo.** Ataques a04 y a05.
- **Corrección exacta.**
  - Al crear la CLM en `_guardar_lote_evidencia` se escribe siempre `"evidencias_ps1": []`. Así, «sin traza» solo significa «registro histórico».
  - En `control_raices`, una CLM citada que no está en F2 es BLOQUEO («CLM citada sin registro en F2»).
  - Una CLM histórica sin `evidencias_ps1` da ADVERTENCIA («sin traza de PS1; recuento no verificable»), nunca un OK silencioso. Esto se declara en INC-T183-01.
- **Prueba de regresión.** a04 y a05.

#### H-03 · media · Tras la baja de una fuente, F2 queda incoherente y G3-DAT-09 retira opciones válidas

- **Qué pasa.** `mantenimiento_fuentes.avisar_curador` (T-181) marca las EVD como `FUENTE_RETIRADA`, pero no recalcula `raices_independientes` ni `ps1_cumple` de sus CLM. Lo mismo pasa con la cuarentena de T-182 en las CLM que no están en `f["_evidencias"]` del ciclo en curso. En el ciclo siguiente, G3-DAT-09 ve el recuento antiguo, bloquea, y `_validar_g3` retira de la entrega todas las opciones que citan esas CLM. Las retira aunque `revisar_bajas` haya concluido MANTIENE_RESPALDO.
- **Cómo reproducirlo.**
  - Ataque a06, a nivel de F2.
  - De punta a punta, con dos ciclos mock: en el primero, `avisar_curador` da de baja tres REF de PS1; el segundo ciclo da el G3 de F6 BLOQUEADO («Recuento de raíces incoherente en CLM-2026-0020, -0014, -0017») y se retiran OPP-2026-0007, -0005 y -0006.
- **Corrección exacta.**
  - En `avisar_curador`, dentro de la misma transacción, por cada CLM de `e["clm_ids"]` de una EVD recién retirada, se reescribe `raices_independientes = len(sint.raices_de_clm(clm, evds))` y `ps1_cumple`. Se hace lo mismo tras la cuarentena (`orquestacion.py`, la rama de `retirar_por_manipulacion`).
  - En `revisar_bajas`, las raíces se cuentan con `sint.raices_de_clm` (por `origen_documental`) y no por `ref_id`, para que T-181 y T-183 cuenten igual.
- **Prueba de regresión.**
  - a06.
  - Una prueba de dos ciclos: tras la baja de una fuente, el ciclo siguiente da G3-DAT-09 OK, y una opción con respaldo suficiente sigue en la entrega.

#### H-04 · media · Derivadas sin `raiz_evd_id` (esquema de F2, §4 y regla 3)

- **Qué pasa.** El esquema dice que `raiz_evd_id` es obligatorio si la pieza no es RAIZ: «EVD- o "no identificada" con motivo». Queda en `None` en cuatro casos:
  - (a) el original no se ha ingerido (a08);
  - (b) el original sustenta otra CLM (a09), porque `originales` solo mira `clm["evidencias"]`;
  - (c) «Fuente original: RF-0000» viene sin el prefijo REF- (a10);
  - (d) la cadena tiene dos saltos, RF-0002 → RF-0001 → RF-0000 (a10).

  El mutante M9 (enlazar con una DERIVADA) vive por esto mismo.
- **Corrección exacta.**
  - La raíz se resuelve en un paso propio, sobre todas las EVD de F2 (`por_id`) y no solo las de la CLM.
  - Se normaliza el identificador: se añade `REF-` si falta.
  - Se sigue la cadena de «Fuente original» hasta una ficha que no la tenga, con guarda de ciclos.
  - Solo se enlaza con una EVD `RAIZ`.
  - Sin raíz localizable se escribe `raiz_evd_id = "no identificada"` y en `limitaciones` el motivo («derivada de REF-…; original no ingerido o sin ficha»).
- **Prueba de regresión.** a08, a09 y a10.

#### H-05 · media · Mutantes vivos y cláusulas sin prueba

- **Qué pasa.** Con las pruebas del ticket y sus vecinas, quedan vivos estos mutantes:
  - M1: cuentan las EVD retiradas o en cuarentena que siguen en `evidencias_ps1` de ciclos anteriores.
  - M2 y M5: CALC- y HT-01 del mismo proxy cuentan como dos raíces.
  - M3: `ps1_cumple` de la CLM igual al de la opción.
  - M7: G3 lee F2 sin la fecha del paquete.
  - M9: se ve en H-04.

  M4 (dirección) es equivalente: la dirección forma parte del hash y una EVD no cambia de dirección.

  Además, la cláusula «salvo que la raíz sea primaria de nivel A» no tiene prueba en `test_t183_raices.py`: M6 solo lo mata `test_t65`.
- **Corrección exacta.** Añadir a `test_t183_raices.py`:
  - (1) una EVD de `evidencias_ps1` pasa a FUENTE_RETIRADA y luego a CUARENTENA, y deja de contar;
  - (2) una pieza CALC- y una HT-01 del mismo proxy son una sola raíz, en la CLM y en la opción;
  - (3) la semántica de `ps1_cumple` por afirmación, frente a PS1 por opción, declarada en INC-T183-01 y probada;
  - (4) G3 sobre un paquete con fecha anterior a escrituras posteriores de F2 usa F2 a la fecha del paquete;
  - (5) a07.

  Volver a pasar `revisores/r01_mutantes.py`: todos MUERTOS salvo M4, que es equivalente.
- **Prueba de regresión.** Las cinco de arriba.

#### H-06 · media · El caso del plan, tal como está escrito, da 21 raíces

- **Qué pasa.** Con un informe reproducido por 20 medios con variaciones menores y sin metadato de procedencia, el ejecutor da 21 raíces y PS1 superada (a12).
  - La detección de derivadas depende de un campo nuevo de F9, «Fuente original». No lo tiene ninguna ficha real: hay 0 en F9 V3.2, y el formato de F9 es corpus congelado. Tampoco está declarado en INC-T183-01.
  - El «No comprueba» lo motiva por «la identificación semántica… y la revisión humana del Auditor». No es un motivo admitido (tiempo real, API real o usuarios): la regla 2 de F2 pide deduplicar «por hash exacto … y por similitud semántica», y CT-11 asigna duplicados y raíces al ejecutor, en código.
  - El Auditor no es humano: es un agente, y por tanto API real.
- **Corrección exacta.**
  - En `_guardar_lote_evidencia`, deduplicación determinista por similitud entre las piezas de una misma CLM: Jaccard de tríos de palabras del extracto normalizado.
  - Con similitud mayor o igual que `evidencia.umbral_similitud_derivada` (nuevo en `config/por_defecto.yaml`, `[PROPUESTO]`, con INC-T183-02), la pieza posterior pasa a DERIVADA. Su `raiz_evd_id` es la más antigua por `conocible_desde` y, a igualdad, por `evd_id`.
  - Declarar «Fuente original» en INC-T183-01 como `[PROPUESTO]` y como segunda vía.
  - Dejar en `no_comprueba` solo «el recuento del Auditor con el modelo real (API real)».
- **Prueba de regresión.** a12, con un control negativo: dos extractos distintos de la misma afirmación siguen siendo dos raíces.

### Observación fuera del alcance (para el coordinador)

- **O-01.** El Documento 0 (§13.4) dice que `PENDIENTE_BARRIDO` y `PENDIENTE_VERIFICACION_ALTA` «no pueden sustentar por sí solos una afirmación central (PS1) hasta quedar en OK».
  - El ejecutor cuenta esas fuentes en PS1: `_guardar_lote_evidencia` no mira `estado_enlace`. Es anterior a este PR.
  - Afecta a 121 fichas de F7, 10 de F8 y 18 de F9, y a las altas de T-184.
  - Propongo abrir un ticket propio. No se ha contado como hallazgo de T-183.
