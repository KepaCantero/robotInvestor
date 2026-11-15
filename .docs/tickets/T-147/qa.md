# T-147 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; implementó Claude) · **Ronda:** r01 · 2026-11-15
- **Copia:** git worktree en el scratchpad con HEAD `f197bc5` («instantánea: integración T-147/T-144/T-148 y QA r01 de T-146») y `.venv` enlazado. Sin red, sin la API y sin coste. Opinión formada con el README, el diff de HEAD y el código antes de leer `analisis-tecnico.md`.

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A, una vez (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | **6338 passed** en 24 min 8 s (línea base ≥ 607); exit 0 |
| `pytest -q tests/test_t147.py tests/test_t142_cadena_b.py tests/test_t144.py tests/test_t148.py tests/test_t145.py` | 218 passed |
| `python tests/goldens_ct.py` · `pytest -q tests/test_fase3_goldens.py` | «goldens de contratos: coinciden» · 102 passed |
| ruff desde la raíz, tres ejecutores (`… \| wc -l`) · mypy de A (`--ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | 2838 (cuota 2838) · 109 (cuota 109) |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py` | rutas vivas · sin hallazgos · NFC · 695 archivos íntegros |
| `.docs/tickets/T-147/mutantes.py <copia desechable con «t147_mut»>` (los 32, de los tres tickets) | **32 de 32 muertos** (grupo T-147: 16 de 16) |
| `T-142/revisores/r01_ataques_peticion.py --trabajo <tmp>` | 36 OK · 4 OBS (lo mismo que declara `pruebas.md`) |
| `bash T-142/revisores/r02_cadena_doce_tipos.sh .venv/bin/python <tmp>` | código 0; 2 entregadas, todas válidas, 2 vueltas CT-04 |
| `T-142/revisores/r03_mutantes.py <copia «t147_mut»>` | 10 de 10 muertos (`muta_paquete` incluido) |
| `python -I T-141/revisores/r03_respuestas_raras.py <tmp>` | normal: código 0 y 6 CSV; los 8 raros: código 1 y 0 CSV |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_h02_la_peticion_con_datos_protegidos_falla_cerrado` y `test_h02_el_script_no_escribe…` en verde; `r01_01` C1: correo en el nombre → `DATOS_PROTEGIDOS` sin el dato. Matiz en H-01: si además el encargo no cumple el esquema, el error es otro y sí lo reproduce |
| CA-2 | sí | pruebas `test_h02_r8_*` en verde (ciclo de los 12 tipos, prompts, goldens); `r01_01` A y B: detecta mayúsculas, subdominios, JSON, `apiKey`, la clave tras un salto de línea en JSON; no marca `react@18.3.1`, `logo@2x.png`, `max_tokens`, una dirección `0x…`, «contraseña: obligatoria», `token_ratio`, «@analista» ni «cierre@2024-03-29». No detecta la «@» codificada (`@`, `%40`), `Authorization: Basic …` ni un `token:` de solo letras: límites declarados en INC-T123-01 (OBS, no hallazgos) |
| CA-3 | sí | `r01_01` D1/D2: `tipos_secundarios` `None`, cadena, repetidos o ajenos → `ENTRADA_B_INVALIDA`; lista vacía, válida; `nivel` en minúsculas, `prioridad` numérica, `peticion` lista, `idioma` «es-es» o numérico, clave con espacio o no textual → `CONFIGURACION_CADENA_B`; D3: la petición válida sale sin mutar el paquete; M02–M06 muertos |
| CA-4 | sí | `r01_02`: `--clases XXX`, `div`, vacío y `RV XXX` → 2; `DIV DIV` y `DIV` → 0 |
| CA-5 | sí | `T-141/revisores/r03_respuestas_raras.py` (arriba); docstring con la fijación de las 14:15 y la publicación hacia las 16:00 (CET). Dos variantes nuevas aún dan traza (H-02) |
| CA-6 | sí | revisores de T-142 y T-141 (arriba); mutantes del grupo T-147, 16 de 16; cuotas 2838 y 109 |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | `.venv/bin/python -I .docs/tickets/T-147/revisores/r01_01_r8_y_peticion.py` (casos C2 a C5) | Esperado (CA-1, R8): ningún error de `construir_peticion` reproduce el dato protegido. Obtenido: si el correo va en un campo con enumeración (`tipo_activo`, `horizonte_principal`), en `tipos_secundarios`, en `cadena_b.peticion.nivel` o una clave en `idioma`, falla con `ENTRADA_B_INVALIDA` o `CONFIGURACION_CADENA_B` y el detalle copia el valor (el mensaje de `jsonschema` lleva la instancia: «'inversor.prueba@…' is not one of …»). `cadena_a_b.py` escribe ese detalle en `resumen.json` y lo imprime. Baja porque solo llega con un paquete que ya no cumple el esquema de A (la redacción lo bloquea en G3, aunque lo escribe) o con la configuración del operador | Pasar el filtro R8 (`contiene_credenciales`) sobre la entrada y la configuración antes de validar el esquema, o redactar la instancia en los mensajes (ruta y validador, sin `e.message`); prueba con un correo en un campo enumerado | abierto |
| H-02 | baja | `.venv/bin/python -I .docs/tickets/T-147/revisores/r01_02_bce_y_clases.py <tmp>` | Esperado (T-141 H-03: «mensajes y código 1 en vez de trazas»): toda respuesta rara termina con 1 sin escribir. Obtenido: una fecha repetida escrita sin ceros («2026-11-3» junto a «2026-11-03») pasa la comprobación de repetidas (compara el texto) y `pivot` cae con `ValueError: Index contains duplicate entries` (traza; no escribe nada); un destino que es un fichero da `FileExistsError` (traza). Ninguna escribe a medias | Buscar las repetidas después de `pd.to_datetime` (sobre la fecha ya convertida) y capturar `OSError` de `escribir` con su mensaje y el código 1 | abierto |
| H-03 | baja | `.venv/bin/python .docs/tickets/T-147/revisores/r01_03_mutantes_qa.py <copia «t147_mut»> --ticket T-147` | 3 de 7 mutantes propios mueren; viven Q02 (el valor de una clave genérica desde 8 caracteres en vez de 16), Q03 (dominio de primer nivel de una letra), Q05 (fechas del BCE en cualquier formato) y Q07 (la sonda sin capturar `ErrorCadenaB`: una opción sin correspondencia con datos protegidos hace caer `cadena_a_b.py --sonda-sin-correspondencia` en vez de anotarse). Ninguno abre un envío con datos protegidos: Q02 y Q03 solo añaden falsos positivos, Q05 deja pasar fechas raras, Q07 falla cerrado con traza | Pruebas de falsos positivos en el borde de 16 caracteres y de un dominio de una letra; una respuesta del BCE con fechas «2026-11-3»; la sonda con una opción sin correspondencia que lleva un correo | abierto |

Observaciones (no son hallazgos de este ticket):

- O-01 (T-142, para la coordinación): `cadena_a_b.py` envía al Bloque B las opciones enviables del `paquete_json` aunque el dictamen G3 del ciclo sea BLOQUEADO (la redacción escribe el paquete también entonces). No he comprobado si el diseño de la Fase 6 lo quiere así.
- Los límites de R8 que `r01_01` marca como OBS (la «@» codificada, `Authorization: Basic`, un `token:` de solo letras) están declarados en INC-T123-01 y en `analisis-tecnico.md`.

Scripts de esta ronda, en `revisores/` (órdenes en los hallazgos): `r01_01_r8_y_peticion.py`, `r01_02_bce_y_clases.py`, `r01_03_mutantes_qa.py` (mutantes propios de T-147, T-144 y T-148).

No comprobado: los revisores de T-141 que necesitan red (`r01_contraste_fred.py`, `r02_festivos_y_huecos.py`); `./tools/check_all.sh` entero, A-Forex y B (fuera del encargo).

## Veredicto

**APTO** · los seis criterios se cumplen con evidencia y no hay hallazgos altos. H-01, H-02 y H-03 son bajos y no rompen ningún criterio: van a un ticket nuevo.
