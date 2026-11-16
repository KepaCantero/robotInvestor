# T-156 · QA independiente

- **Revisor:** Claude, subagente revisor nuevo sin el contexto de la implementación (regla del 12-11-2026: Claude puede revisar lo suyo con un revisor nuevo) · **Ronda:** r01 · 16-11-2026

## Reproducción desde limpio

Copia: git worktree en el scratchpad sobre la instantánea `a23d333`, con `.venv` enlazado; sin red, sin la API y sin gasto (SDK real sobre `httpx2.MockTransport`, clave «clave-falsa-qa»). Mutantes en copias desechables (`git archive HEAD bloque_a .docs tools`), borradas al acabar.

| Orden (desde la raíz de la copia salvo que se diga) | Resultado |
| --- | --- |
| `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider` (una vez, en segundo plano) | **6638 passed, 2 skipped**, exit 0, 37 min 56 s (T-154: 6624 + las 14 nuevas) |
| `… -m pytest -q -p no:cacheprovider tests/test_t154.py tests/test_t151_reintentos.py tests/test_t146_presupuesto.py tests/test_t148*.py tests/test_fase3_goldens.py` | **273 passed** |
| `… -m pytest -q -p no:cacheprovider tests/test_t154.py -k t156` · `python tests/goldens_ct.py` | 14 passed · «goldens de contratos: coinciden» |
| `.venv/bin/python tools/refs_vivas.py` · `secrets_scan.py` · `nfc_check.py` · `corpus_integridad.py` | exit 0 los cuatro; corpus **695** archivos coinciden |
| `.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | **2831** (cuota 2831) |
| `.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` | **109** (cuota 109) |
| `.venv/bin/python -I .docs/tickets/T-154/revisores/r01_01_unidad_t154.py bloque_a/11_Ejecutor` | **todo OK**; las líneas OBS de `cobro_posible_desde` ahora dicen que 0, 599, 600 y 10⁶ se rechazan y 100 se acepta |
| `.venv/bin/python -I .docs/tickets/T-154/revisores/r01_02_ciclo_f9.py bloque_a/11_Ejecutor <tmp>` | **todo OK** (los nueve escenarios; firma «dos» `1e93cbd84b45`) |
| `.venv/bin/python -I .docs/tickets/T-151/revisores/r01_01_reintentos_unidad.py bloque_a/11_Ejecutor` | **9/9 OK**, 3 OBS (las mismas X9, X10 y X12 de la QA de T-154) |

### Mutantes

| Script | Copia | Resultado |
| --- | --- | --- |
| `.docs/tickets/T-154/revisores/r01_03_mutantes_qa.py` (R01–R11) | `…/qa25_mut_t156b` | **11/11 muertos**: R01, R02 y R03 mueren con las pruebas. Además, aplicados uno a uno, cada uno rompe **exactamente un** caso de `test_t156_h02_cada_lista_sola_basta_para_escribir_f9` (el de su lista) |
| `.docs/tickets/T-154/mutantes_t154.py` | `…/qa27_t154_mut` | **17/18 muertos, P09 NO APLICA**, exit 1 (H-01 de esta QA). P09 adaptado a la línea nueva (`… or not ESTADO_HTTP_MIN <= desde <= PRIMER_ESTADO_5XX:` → `if False:`) muere: 12 pruebas fallan |
| `.docs/tickets/T-151/mutantes_t151.py` | `…/qa27_t151_mut` | **18/18** |
| `.docs/tickets/T-156/revisores/r01_02_mutantes_qa.py` (propios, S01–S15) `--scripts` | `…/qa25_mut_t156_r01` | **14/15 muertos**; vive **S08** (quitar el rechazo de booleanos), que es **equivalente**: `True` y `False` valen 1 y 0 y el rango ya los deja fuera (tampoco lo ve `r01_01`) |

## Scripts del revisor (`revisores/`, en este orden)

1. `.venv/bin/python -I .docs/tickets/T-156/revisores/r01_01_rango_cobro.py bloque_a/11_Ejecutor <tmp>`. Unidad, sin red:
   - **V01**, bordes: 100 y 500 se admiten, también el valor por defecto; 99, 501, 599, 600, 0, −1 y 10⁶ dan ValueError con el nombre de la clave.
   - **V02**, tipos: True, False, 500.0, 450.5, NaN, ±inf, −0.0, «500», «», «5xx», `[500]`, un dict, `Decimal`, `Fraction`, `complex`, `numpy.int64(500)` y `numpy.float64` dan ValueError; `None` da KeyError.
   - **V03**, clave ausente: sin la clave sale la de `por_defecto.yaml` (500). Si tampoco está allí, KeyError.
   - **V04**, YAML del operador por `crear_cliente("anthropic")`: `600`, `5e2`, `500.0`, `yes`, `~` y `"500"` se rechazan antes de crear el SDK (0 SDK creados); `0x1F4`, 100 y 500 valen.
   - **V05**, monotonía: 6 015 000 clasificaciones (d de 100 a 500 × estados de 0 a 999 × 5 valores de `x-should-retry` × 3 configuraciones de estados). Con d < 500 el reintento es siempre el mismo y el cobro nunca es menor que con 500. Con 500 es la regla por defecto.
   - **V06**, de punta a punta con el SDK real: con 400 un 450 se carga una vez por su peor caso y con 500 se suelta; un 404 con 100 se carga; un 429 se suelta con cualquier valor; sin reservas colgadas.

   **Todo OK.**
2. `.venv/bin/python .docs/tickets/T-156/revisores/r01_02_mutantes_qa.py <copia con «qa25_» y «_mut»> --scripts`. Mutantes S01 a S15:
   - S01 a S11, el rango: bordes estrictos, topes 599 y 0, la validación de antes, sin tope, sin comprobar el entero, sin rechazar booleanos, recorte silencioso a 500, 500 escrito en `clasificar_error` y un error que no nombra la clave.
   - S12 a S15, la F9: `algo()` sin `sin_respuesta`, los recortes condicionados a los excesos, la F9 con todo el presupuesto en vez del tramo y el tramo sin la marca.

   Resultado arriba.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_t156_h01_cobro_posible_desde_con_rango` (11 casos) y `test_t154_las_claves_nuevas_invalidas_fallan_cerrado`; `r01_01` V01–V04 (bordes, 18 tipos raros, clave nula o ausente, YAML real); S01–S07 y S09–S11 muertos. El 500 por defecto vale. El cambio de `test_t154_h01_la_clasificacion_de_los_5xx_sale_de_la_configuracion` (de 600 a 400, con 450 y 399) **no la debilita**: sigue mostrando que la configuración manda, ahora hacia el lado que se admite. Lo comprueba S10 (500 escrito en `clasificar_error`), que muere, igual que P03 de `mutantes_t154.py`. Que con 100 ≤ d < 500 la cuenta es igual o más prudente lo comprueba V05, de forma exhaustiva |
| CA-2 | sí | La prueba parametrizada tiene tres casos, uno por lista, y comprueba que la lista va sola en la F9 y que las otras van vacías. R01, R02 y R03 mueren, y cada uno rompe solo su caso. S13 (los recortes condicionados a los excesos) también muere con ella. S12, S14 y S15 mueren con las pruebas de T-154 |
| CA-3 | sí | Las pruebas de T-154, T-151, T-146 y T-148 y los goldens: 273 passed. Suite completa: 6638/2. Ruff 2831 y mypy A 109, iguales a la cuota. Gates ligeros en verde. `r01_01` y `r01_02` de T-154 y `r01_01` de T-151 en verde. `mutantes_t151.py` 18/18. `mutantes_t154.py` 17/18 con P09 sin aplicar (H-01) |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja (herramientas de regresión) | `.venv/bin/python .docs/tickets/T-154/mutantes_t154.py <copia con «t154_mut»>` | **Esperado:** el script de mutantes de T-154 sigue aplicando entero después de T-156, que cambió la línea que muta P09. **Obtenido:** «P09 NO APLICA (0 apariciones)», 17/18 y exit 1. El ataque sigue cubierto: P09 adaptado a la línea nueva muere (12 pruebas fallan), y S05 y S06 de esta QA también. Pero quien vuelva a pasar el script lo verá fallar sin saber por qué | Cambiar la cadena de P09 en `mutantes_t154.py` por la comprobación nueva (`… or not ESTADO_HTTP_MIN <= desde <= PRIMER_ESTADO_5XX:`) y anotarlo en la cabecera del script | abierto |
| H-02 | baja (documentación) | Leer `.docs/tickets/T-156/pruebas.md` | **Esperado:** `ri-probar` pide la evidencia de cada criterio. El CA-3 nombra las suites de T-154, T-151, T-146 y T-148, los goldens y las cuotas, y el CA-2 nombra los mutantes R01–R03. **Obtenido:** `pruebas.md` solo registra `pytest -k t156` (14 passed). No registra el CA-3, ni los mutantes, ni que `mutantes_t154.py` deja de aplicar. Tampoco hay `analisis-tecnico.md` (el diseño está en el README, que basta para este tamaño) | Completar `pruebas.md` con las órdenes y los resultados del CA-2 y del CA-3 (los de esta QA valen como referencia) | abierto |

Observaciones (sin hallazgo):

- **S08 es equivalente.** El `isinstance(desde, bool)` sobra para el rango, porque `True` y `False` valen 1 y 0. No estorba y deja el mismo patrón que las otras claves.
- **Subclases de `int`.** Un `IntEnum` o una subclase de `int` dentro del rango se admiten, y fuera de él se rechazan. YAML no las produce, así que no tiene efecto.
- **De 100 a 399 es lo mismo que 400.** El SDK solo levanta `APIStatusError` con 4xx y 5xx, así que en la práctica un valor entre 100 y 399 equivale a 400: cualquier error de estado se cobraría por su peor caso. Es prudente y está declarado en INC-T146-01 («más prudente»).
- **Cuándo se valida.** La regla se valida al crear el cliente real (`crear_cliente("anthropic")`), antes de crear el SDK y de enviar ninguna petición (V04). Con `--cliente mock` no se valida, pero en ese modo nada se clasifica ni se cobra. Es el mismo comportamiento que tenían las claves de T-151 y T-154.

**Invariantes del sistema:**

- T-156 solo toca la validación de la configuración del cliente LLM y una prueba. Ningún camino nuevo llega a una orden.
- No hay LLM en ninguna ruta de control.
- Los controles no se relajan: el rango solo quita valores que fallaban abierto, y V05 prueba que todo lo que se admite es igual de prudente o más.
- Falla cerrado antes de crear el cliente.
- Los dos límites nuevos son del protocolo (RFC 9110 §15), con su comentario, no parámetros de ajuste. El valor sigue en `config/por_defecto.yaml`.
- La decisión es `[PROPUESTO]` y está en INC-T146-01.
- Sin secretos ni datos personales (gate en verde).
- El README del ejecutor no necesita cambio. La deuda técnica la deja el implementador con T-156 en QA, y este revisor no la toca.

**No comprobado:**

- El comportamiento real de la API, sin red ni gasto.
- `./tools/check_all.sh` entero. A-Forex y B no se tocan; los gates ligeros, las cuotas y la suite de A sí se comprobaron.

## Veredicto

**APTO.** Los tres criterios se cumplen con evidencia y no hay hallazgos críticos ni altos. H-01 (`mutantes_t154.py` deja de aplicar P09) y H-02 (`pruebas.md` incompleto) son bajos: no afectan al código ni a la cuenta y quedan para la deuda técnica o para una corrección menor. Este revisor no cierra el ticket ni toca la deuda técnica.
