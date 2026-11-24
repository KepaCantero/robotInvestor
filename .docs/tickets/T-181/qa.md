# QA r01 · T-181 · Enlace roto, contenido cambiado y retractación (PB-24 y PB-25)

| Campo | Valor |
| --- | --- |
| Revisor | Claude (no implementó; revisión independiente) |
| Fecha | 24-11-2026 |
| Código revisado | rama `astra/encargos-bloque-a-c38-c47`, tip `2d99af6`, sobre `develop` `9ce57b2`; commits de T-181: `9eaeab4` (y lo que tocan `5ef929b` y `64dc158` en los mismos ficheros) |
| Veredicto | **NO APTO** (1 alto, 3 medios, 4 bajos) |

## Qué se ha hecho

- Worktree limpio en `2d99af6` con la venv del proyecto (Python 3.12). `test_t181_fuentes.py`: 11 superadas. Vecinas (T-182, T-183, T-184, goldens de la Fase 3, integración, unitarias y HT-02 de `10_Herramientas`): 266 superadas.
- Sin el cambio fallan: con el código de `9ce57b2` (y `mantenimiento_fuentes.py` presente) fallan las 3 pruebas que pasan por `Referencias` y la CLI; sin el módulo, la colección entera.
- `mutantes.py` del ticket: los 8 mueren.
- Mutantes propios (`revisores/r01_mutantes.py`): **17 vivos de 18**; uno es equivalente (`incidencia_red`: con la red caída todas las filas ya se saltan por falta de código HTTP).
- Ataques propios (`revisores/r01_ataques.py`): entradas hostiles del custodio, bordes de la rúbrica, registro manipulado, idempotencia, cierre de mes y dos ciclos mock completos. Salen 6 HALLAZGO, recogidos abajo.
- Cuotas: ruff 2807 → 2807 y mypy A 102 → 102. Los ficheros nuevos están limpios en ruff. `mantenimiento_fuentes.py:166` suma una nota de mypy, compensada en otro fichero (H-08).
- Invariantes: R8 (motivo filtrado), G3-MET-13 (ningún texto nuevo con «valid-») y corpus congelado intacto, todos bien. No hay LLM en la ruta. Se escribe bajo `_transaccion()` y con `publicar()` comparando el original. Los números de la rúbrica están escritos a mano (H-05).

## Criterios de aceptación

| # | Criterio | Resultado |
| --- | --- | --- |
| 1 | Baja una vez en el registro y aviso al Curador | Cumple: hay línea, CT-11 y deduplicación por `baja_id`. El mensaje CT-11 no cumple su esquema del Anexo B (H-04) |
| 2 | EVD retirada y revisión separada de las oportunidades vigentes | **No cumple en el flujo real** (H-01). Puede además relajar PS1 (H-02) |
| 3 | CT-21 con las bajas del mes | Cumple tras el cierre del mes. Los nombres de campo se apartan de los prompts (H-04), y la cláusula del cierre no tiene prueba (H-03) |
| 4 | Q recalculada con motivo, reparación con copia original y retractación confirmada | Cumple. Faltan pruebas de bordes y de R8 (H-03). Números de §13.3 escritos en código (H-05) |
| 5 | Red, reintentos y consultas previas coherentes | Cumple a medias: una revisión se pierde en silencio y el estado de las fichas sin respuesta deja de actualizarse (H-07). El registro es frágil (H-06) |

## Hallazgos

### H-01 · alta · Al arrastrar una opción se vacía `evidencias_ps1`, y entonces cualquier baja le quita PS1 aunque le sobrevivan raíces suficientes

- **Reproducir:** `r01_ataques.py`, apartado 3. Un ciclo mock completo el 05-06-2026 deja 23 opciones PROPUESTA con `evidencias_ps1`. Al ciclo siguiente pasan a VIGENTE (arrastre) y 22 quedan con `evidencias_ps1 = []`: la escritura F3 de `orquestacion.py` usa `f.get("_evidencias_ps1", [])` y la ficha arrastrada (construida desde `v` hacia la línea 1841) no lo trae. Después basta la baja de una sola fuente de OPP-2026-0008, que conserva tres raíces A/B: `revisar_bajas` concluye REQUIERE_REEVALUACION y escribe `ps1: False`.
- **Se esperaba:** MANTIENE_RESPALDO y `ps1` sin cambios cuando las raíces supervivientes bastan (criterio 2, y lo que el propio README describe).
- **Por qué no lo vio la prueba:** `test_baja_con_registro_y_propagacion` escribe F3 a mano, con `evidencias_ps1` ya rellena. Ninguna prueba pasa por dos ciclos. El mutante `f["_evidencias_ps1"].append(...) → pass` sigue vivo.
- **Corrección:** en la ficha arrastrada, `"_evidencias_ps1": list(v.get("evidencias_ps1", []))` junto a `"_evidencias"`. Además, en la escritura F3, `f.get("_evidencias_ps1", (f.get("_previa") or {}).get("evidencias_ps1", []))`, para que ningún otro camino vacíe la lista. Mientras no se corrija, PB-24 no puede figurar como «Superada» en `mapa_plan_pruebas.json` ni en las evidencias.
- **Prueba de regresión:** dos ciclos mock y una baja (en `refs.bajas` o en una copia de F7) de una REF de una VIGENTE con al menos dos raíces A/B más. Se afirma que la lista no está vacía tras el arrastre, MANTIENE_RESPALDO, `ps1 is True`, y REQUIERE_REEVALUACION cuando solo queda una raíz. El apartado 3 de `r01_ataques.py` debe salir OK.

### H-02 · media · La revisión tras una baja puede devolver PS1 a una opción que no lo tenía

- **Reproducir:** `r01_ataques.py`, OPP-B: VIGENTE, `ps1: False`, una evidencia retirada y dos raíces B supervivientes. Tras `revisar_bajas` queda `ps1: True` y MANTIENE_RESPALDO.
- **Se esperaba:** una baja solo puede quitar respaldo. «Los controles nunca se relajan solos».
- **Corrección:** `mantiene = op.get("ps1") is True and bloque._ps1(raices)`.
- **Prueba de regresión:** la de OPP-B (VIGENTE sin PS1 y una baja): `ps1` sigue en False y la conclusión es REQUIERE_REEVALUACION.

### H-03 · media · Las pruebas no matan las cláusulas del criterio: 17 mutantes vivos

Ver `revisores/r01_mutantes.py`. Siguen vivos y cambian el comportamiento:

| Mutante | Cláusula sin prueba | Prueba que hay que añadir a `test_t181_fuentes.py` |
| --- | --- | --- |
| `if mes < fecha[:7] and` → `if` | CT-21 solo tras el cierre del mes (INC-T-181-01) | `revisar_bajas` el mismo mes: ningún `mes_bajas` en HA |
| `estado != "VIGENTE"` → `False` | solo se revisan las vigentes | una opción DESCARTADA sin `revision_bajas` |
| `… - retiradas` quitado | la raíz retirada no cuenta | OPP con la retirada como raíz A primaria → REQUIERE (OPP-A de `r01_ataques.py`) |
| filtro R8 y `<>` del motivo → `False`; motivo multilínea | R8 y una línea en el registro | `ValueError` con credencial ficticia (en dos cadenas), con `<` y con `\n` |
| `not ficha.campo("Copia archivada")` quitado; DOI sin respuesta | «sin alternativa» | ficha con copia archivada, o con DOI sin código: se conserva |
| RETRACTADA sin `r["retractacion"]` | la retractación exige el indicio de HT-02 | `ValueError` con estado OK |
| `rev["url"] != url` y `copia["retractacion"]` quitados | la reparación usa la copia del barrido y no retractada | `ValueError` en los dos casos |
| `q >= ficha.q` → `q > ficha.q`; `q >= 65` → `q >= 66` | DEGRADAR baja Q; niveles en los bordes | Q igual → `ValueError`; 80/79/65/64/50/49 → A/B/B/C/C/D |
| deduplicación de la EVD y de la revisión F3 | idempotencia (criterio 1 y 5) | tres pasadas: una marca FUENTE_RETIRADA y una revisión por opción |
| `orquestacion.py`: no descartar piezas de REF dadas de baja | el ciclo siguiente no usa la fuente retirada | ciclo con una REF de baja citada por el modelo en modo no backtest: no forma EVD |
| `cli.py`: `dia <= datos["fecha"]` quitado | lectura al corte | baja con fecha posterior al barrido: no hay CT-11 |

- **Corrección:** añadir esas pruebas (`r01_ataques.py` sirve de modelo) y volver a pasar `r01_mutantes.py`: tienen que quedar todos MUERTOS salvo el equivalente, que se explica en `pruebas.md`.

### H-04 · media · El CT-11 `fuente_retirada` no cumple el esquema CT-11 del Anexo B, y el CT-21 no usa los campos de los prompts

- **Reproducir:** validar `{"tipo": "fuente_retirada", "piezas": [{"ref_id": …, "fecha_baja": …}]}` con `tests/goldens/anexo_b_esquemas.json["CT-11.ENCARGO"]`. Sale: `'indice' / 'fuente' / 'extracto' / 'afirmacion' / 'direccion' is a required property`. Ningún golden lo detecta, porque el ciclo mock no tiene bajas, y no hay incidencia. El CT-21 lleva `mes` y una lista de REF-. Los prompts de los Documentadores (§5.7) y del Buscador (§4.5) piden `periodo` y `bajas` con su motivo.
- **Corrección:** construir cada pieza con los campos del Anexo B: `indice`, `fuente` (REF-id), `extracto` vacío, `afirmacion` («Fuente retirada de Fx el AAAA-MM-DD: motivo») y `direccion` neutra. Se conservan `tipo` y `fecha_baja`, que el esquema admite como campos de más. En CT-21, `periodo` y `bajas: [{"ref_id", "motivo"}]`, leyendo el motivo de la fila del registro. Si se prefiere otra forma, se declara como `INC-T-181-02 [PROPUESTO]` y se registra la divergencia en `divergencias_anexo_b.json`, con su línea en `REGISTRO.md`.
- **Prueba de regresión:** en `test_baja_con_registro_y_propagacion`, validar el `mensaje` del CT-11 con el esquema derivado (jsonschema) y comprobar `periodo` y el motivo en el CT-21.

### H-05 · baja · Rúbrica y niveles de Q escritos en el código

- `RUBRICAS` y los cortes 80/65/50 (`mantenimiento_fuentes.py:15` y `:42`, repetidos en `altas_referencias.py:47`) salen del cuerpo del Documento 0 (§13.3), no del Anexo A, de la configuración ni de una ficha. No hay incidencia `[PROPUESTO]` (regla 2).
- **Corrección:** llevarlos a `config/por_defecto.yaml` (p. ej. `referencias: {rubricas: {F7: […], F8: […], F9: […]}, niveles_q: {A: 80, B: 65, C: 50}}`) con la referencia a §13.3, leerlos con `parametro()` en los dos módulos y declarar `INC-T-181-03 [PROPUESTO]`.
- **Prueba de regresión:** con una configuración que cambie `niveles_q.B`, el nivel de una Q en el borde cambia.

### H-06 · baja · La lectura del Registro de bajas es frágil

- **Reproducir (`r01_ataques.py`):**
  - Una fila con fecha imposible (`2026-13-45`) lanza `ValueError: month must be in 1..12` sin decir de qué archivo ni de qué línea. Como `Referencias()` lee el registro al construirse, una errata del custodio impide arrancar el Bloque y la CLI.
  - `ht02.borrar_ficha` escribe en cualquier encabezado que contenga «registro de bajas» (p. ej. «## Registro de bajas (R24)»), pero `bajas_registradas` exige el encabezado exacto. Esa baja no se propaga a F2 y nadie avisa.
- **Corrección:** reconocer la sección con el mismo criterio que `borrar_ficha` (`RE_TITULO` y `"registro de bajas" in _norm_clave(linea)`). Ante una fecha inválida, fallar cerrado con un `ValueError` que nombre el archivo y la fila. Una sola función de lectura para los dos usos.
- **Prueba de regresión:** los dos casos de `r01_ataques.py`: la variante del encabezado se lee, y la fecha imposible da un error que cita la fila.

### H-07 · baja · Una decisión del custodio se pierde en silencio y las fichas sin respuesta dejan de anotarse

- **Reproducir:** `tratar("F8", ficha, informe_sin_codigo_http, {RID: revision})` devuelve el catálogo sin aplicar la decisión y sin avisar (`r01_ataques.py`). Además, esas fichas ya no reciben `Estado del enlace`, `Última verificación` ni `Primer fallo`. En `9ce57b2`, `verificar-enlaces --aplicar` sí los escribía con HT-02. Un servidor muerto para siempre no llega nunca a la baja, y eso no está declarado.
- **Corrección:** si hay una revisión para un id sin observación HTTP, `ValueError("La revisión exige una observación HTTP del barrido")`. Para las filas sin respuesta, aplicar el estado y la fecha sin borrar, como hacía HT-02, o declararlo en INC-T-181-01 con su motivo.
- **Prueba de regresión:** la revisión sin observación da `ValueError`. Una ficha sin respuesta queda con `Última verificación` del barrido y sigue en el catálogo.

### H-08 · baja · Una nota de mypy nueva que cuenta en el gate

- `mantenimiento_fuentes.py:166` (`meses: dict[...]` dentro de una función sin anotar) produce `annotation-unchecked`, que el gate cuenta como una línea. Queda compensada por otro fichero (la cuota sigue en 102), pero el código nuevo debería dejarla más baja (regla 9).
- **Corrección:** quitar la anotación o anotar la firma de `revisar_bajas`, y bajar `mypy_bloque_a` si el total baja.
- **Prueba de regresión:** el gate de mypy de A da una línea menos que antes.

## Veredicto

**NO APTO.** H-01 rompe el criterio 2 en el flujo real. H-02 a H-04 son medios. Según la regla del operador, los bajos también se corrigen en la ronda r02. Para la r02 vuelvo a pasar `revisores/r01_ataques.py` y `revisores/r01_mutantes.py`, además de las pruebas de la implementadora.
