# T-164 · Pruebas

Todo se ejecuta desde `bloque_a/11_Ejecutor` de la copia `t164` (base `e35d284`), con `../../.venv/bin/python`, sin red ni coste.

| Suite o script | Antes (develop `e35d284`) | Después |
| --- | --- | --- |
| `tests/test_t157_verificador_ids.py` | 46 superadas | **55 superadas** (9 `test_t164_*` nuevas) |
| Las 9 `test_t164_*` con el `verificador_ids.py` de develop | — | 6 fallan (H-09 ×2, H-10, H-11 ×3) y 3 pasan (las de H-12 protegen un comportamiento que ya era correcto) |
| `T-157/revisores/r02_01_ataques.py` | 11/16 | **16/16** |
| `T-157/revisores/r02_02_mutantes.py` | 6 vivos (N02, N04–N08) | **0 vivos**: 9 matados. N04 sale ROTO porque su texto (`if x in simbolos: continue`) era el defecto de H-09 y ya no existe; lo cubren T08 y T09 |
| `T-157/revisores/r01_01_cifras.py` | 21/21 | 21/21 («FALLOS: ninguno») |
| `T-157/revisores/r01_03_mutantes.py` | 25 matados; M13 vivo por el arnés, M10 ROTO | igual: 25 matados, M13 (arnés) y M10 (regla retirada en la r02) |
| `T-157/revisores/r01_02_siembra.py` | no se ejecuta: fija el Documento 0 V5.1 y T-143 lo cambió a V5.2 (`FileNotFoundError`) | copia adaptada `T-164/r01_02_siembra_v52.py`: 38/43 antes de regenerar el informe y **39/43** después. Fallan las 2 de H-04 (aviso a propósito), las 2 de T-143 que esperaban 3 errores (ahora 2, por T-160) y «el JSON del repositorio coincide»: `docs/auditoria_ids_bloque_a.json` ya no es lo que develop genera desde T-143. Los 4 primeros son los de la r02; el quinto viene de T-143, no de T-164 |
| `T-157/mutantes_t157.py` | 13 matados | 13 matados. Tras el primer cambio, «r02 cualquier campo JSON declara símbolo» quedó vivo y lo mató un caso nuevo en `TRAMPAS` (ver `analisis-tecnico.md`) |
| `T-164/mutantes_t164.py` (nuevo) | — | **14 matados**, nulo vivo, ninguno ROTO |
| Verificador sobre el repo real, con `PYTHONHASHSEED` 0, 1, 3 y 7 | — | un solo JSON y un solo Markdown |
| ruff (las tres carpetas de ejecutor) | 2813 | **2813** (cuota 2813); los archivos de T-164, «All checks passed!» |
| mypy `bloque_a/11_Ejecutor/bloque_a` | 109 | **109** (cuota 109); ninguno en `verificador_ids.py` |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py` | en verde | en verde; «Corpus íntegro: 696 archivos» |
| Suite completa de A | — | **7528 superadas, 2 omitidas, 0 fallos** |

## Informe real frente a develop

`python -m bloque_a.herramientas.verificador_ids --json … --md …` con el código de develop y con el de T-164: salida 1 en los dos,
2 errores (FX-MC10-003, RF-0123), 2 avisos y las mismas notas. El `diff` solo da una línea en cada archivo: la versión del
verificador, `"version": "1.0.0"` → `"1.1.0"` en el JSON y «1.0.0» → «1.1.0» en el pie del Markdown. H-09 no cambia nada real porque
el único símbolo con forma de ficha, IDX-FICT-001, nunca va tras «ficha» ni en un campo de ficha; en el valor de `afirmacion` del
Registro de pronósticos congelados sigue excusado. H-10 tampoco, porque en el corpus no hay ninguna ficha de familia conocida con
otro número de cifras (comprobado con `grep`). `docs/auditoria_ids_bloque_a.*` se regenera en este ticket (ver «Informe regenerado»).

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 (H-09) | `test_t164_h09_simbolo_no_excusa_como_ficha`, `test_t164_h09_simbolo_de_familia_desconocida`; `r02_01` §2; T01–T09 |
| CA-2 (H-10) | `test_t164_h10_ficha_con_otro_numero_de_cifras`; `r02_01` §2; T10–T12 |
| CA-3 (H-11) | `test_t164_h11_carpeta_que_no_admite_archivos` (`/proc`), `test_t164_h11_temporal_que_falla_no_deja_nada`, `test_t164_h11_renombrado_que_falla_no_deja_temporales`; `r02_01` §4; T13–T14 |
| CA-4 (H-12) | `test_t164_h12_*` y las anteriores; `r02_02_mutantes.py` sin vivos; `mutantes_t164.py` |
| CA-5 | los scripts del revisor, en la tabla de arriba |
| CA-6 | «Informe real frente a develop» |
| CA-7 | ruff, mypy, gates ligeros y suite completa |
| CA-8 (H-04) | INC-T157-01, «Referencias con otro número de cifras (r02, H-04: se mantiene)»; `test_e_referencias` exige AVISO `REF_FORMA_DISTINTA` para `RF-1` |

## Regresiones

Las 6 pruebas de H-09, H-10 y H-11 fallan con el `verificador_ids.py` de develop: lo comprobé poniendo ese archivo en la copia y
ejecutando `-k t164`. Cada mutante de `mutantes_t164.py` vuelve a una parte del código de antes (T01: la excusa global; T08: omitir
entero el símbolo de familia desconocida; T13: renombrar nada más escribir) o quita una pieza nueva, y alguna prueba lo detecta.

## Mapa de pruebas del plan

`.docs/scripts/evidencias_plan_a.py` (sin `--ejecutar`): mapa válido, 67 pruebas del plan y 204 automáticas citadas.
`mapa_plan_pruebas.json` no cita `test_t157_verificador_ids.py`, así que no cambia y no hay evidencias que regenerar.

## Suite completa

Una pasada en `bloque_a/11_Ejecutor` con el código final (`../../.venv/bin/python -m pytest -q -p no:cacheprovider`, en segundo plano y con otra suite de A en paralelo): **7528 superadas, 2 omitidas, 0 fallos** en 35 min (salida 0). 7528 ≥ 607. Dos pasadas anteriores se cortaron por reinicios del contenedor, no por fallos, y no cuentan.

## Informe regenerado (`docs/auditoria_ids_bloque_a.*`)

A petición de la sesión coordinadora, se regenera con el verificador 1.1.0 sobre el corpus de develop (Documento 0 V5.2), con la orden
del propio documento (`--json ../../docs/auditoria_ids_bloque_a.json --auditoria ../../docs/auditoria_ids_bloque_a.md`). Hay dos
motivos por los que cambia:

1. **T-143 y los tickets del código posteriores a T-157.** El informe del repositorio se generó con el Documento 0 V5.1. Ahora el
   Documento 0 es la V5.2 (otro archivo, otra versión, otro sha256), la huella del corpus es otra y algunas cuentas de citas suben
   en 1 o 2, porque la V5.2 cita más. También cambian las huellas de `contratos.py` y `motor/servicio.py`, que tocaron
   T-143, T-161, T-163 y T-165.
2. **La versión del verificador**, de 1.0.0 a 1.1.0 (T-164).

Los errores, los avisos y las notas no cambian: 2 errores (FX-MC10-003, RF-0123) y 2 avisos. El JSON regenerado es, byte a byte,
el que da el verificador de develop salvo la línea `"version"`. Con el informe regenerado, la copia adaptada de `r01_02_siembra`
pasa «el JSON del repositorio coincide con una ejecución nueva» y da 39/43. Los 4 fallos que quedan son los ya explicados en la r02
de T-157: 2 de H-04 y 2 de T-143 que esperaban 3 errores.

## Ronda r02 (QA r01 NO APTO)

Se ejecutan solo las pruebas del verificador (indicación de la sesión coordinadora): la r02 solo toca `verificador_ids.py`, sus
pruebas, la documentación y los scripts de mutantes. La suite completa es la de la r01: 7528 superadas.

| Suite o script | r01 | r02 |
| --- | --- | --- |
| `tests/test_t157_verificador_ids.py` | 55 | **57 superadas**; con el verificador de la r01, fallan 3 (`test_t164_h09_simbolo_no_excusa_como_ficha`, `test_t164_r02_h04_*` y `test_t164_r02_h05_*`) |
| `T-164/revisores/r01_01_excusa.py` | 18/25 | **25/25** |
| `T-164/revisores/r01_02_escritura.py` | 5/6; modo 0o640 → 0o644 | **6/6**; modo 0o640 → 0o640 |
| `T-164/revisores/r01_03_cifras.py` | 9/9 | 9/9 |
| `T-157/revisores/r02_01_ataques.py` | 16/16 | 16/16 |
| `T-157/revisores/r01_01_cifras.py` | «FALLOS: ninguno» | «FALLOS: ninguno» |
| `T-164/mutantes_t164.py` | 14 matados | **20 matados** (14 + T15 a T20), nulo vivo, ninguno ROTO |
| `T-157/mutantes_t157.py` | 13 matados | 13 matados, nulo vivo |
| `T-157/revisores/r02_02_mutantes.py` | 0 vivos (N04 ROTO) | 0 vivos, 9 matados; N04 ROTO (como en la r01) |
| `T-157/revisores/r01_03_mutantes.py` | 25 matados, M13 arnés, M10 ROTO | **26 matados**: M13 («main sale 0 con errores»), que antes solo vivía por el arnés, ahora lo mata `test_t164_r02_h05_*`, que exige salida 1 en proceso; M10 sigue ROTO |
| Informe real frente a develop | solo la versión | solo la versión. `docs/auditoria_ids_bloque_a.json` y `.md` son, byte a byte, lo que da una ejecución nueva: no hay que regenerarlos |
| ruff (tres ejecutores) / mypy A | 2813 / 109 | **2813 / 109** (cuotas 2813 y 109); corpus íntegro (696) y refs vivas en verde |

## Ronda de cierre de la QA r02 (H-07)

Corrección exacta de `qa.md` («Ronda r02», H-07). `RE_FIN_FRASE` reconoce también «i.e.» y no distingue mayúsculas. El texto de
INC-T157-01 (4) y el docstring de `_como_ficha` nombran la lista cerrada de abreviaturas. `SIMBOLOS` gana la línea «Una ficha de
índices (Ej. AA-SERIE-003).», con su ERROR esperado. T17 y T18 llevan ya la expresión nueva, y T05 se rehace porque el patrón
termina ahora en `",` y no en `")`.

| Qué | Resultado |
| --- | --- |
| `tests/test_t157_verificador_ids.py` | 57 superadas |
| `T-164/revisores/r02_01_regresiones.py` | **19/19**; A06 («Ej.») y A07 («i.e.») dan ERROR |
| `T-164/revisores/r01_01_excusa.py` | 25/25 |
| `T-164/mutantes_t164.py` | 20 matados, nulo vivo, ninguno ROTO |
| Informe real | igual que el de develop salvo la versión; `docs/auditoria_ids_bloque_a.json` y el Markdown, sin cambios |
| ruff / mypy A | 2813 / 109 (cuotas 2813 y 109); corpus íntegro (696) y refs vivas en verde |
