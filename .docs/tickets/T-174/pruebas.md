# T-174 · Pruebas

## Recuento

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`pytest -q bloque_a/11_Ejecutor`, casos recogidos) | 7975 | 7983 (+8 en `tests/test_t174_pb61_revision_c2.py`) |
| Bloque A, ejecución completa al final | — | 7980 superadas, 2 omitidas y 1 fallo esperado. El fallo era `test_fase4_mapa.py::test_h05_el_documento_publicado_coincide_con_el_mapa`: el documento de evidencias aún no estaba regenerado. Tras `evidencias_plan_a.py --ejecutar` pasa (`tests/test_fase4_mapa.py`: 23 de 23) |
| Bloque A-Forex, Bloque B | sin tocar | sin tocar (no se ejecutan; mypy igual: 174 y 159) |

## Matriz criterio → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 (RUN AD_HOC con disparador CT-23 y revisados) | `test_pb61_respuesta_tardia_que_invalida_el_supuesto_abre_una_revision_c2` |
| CA-2 (sin el supuesto, nota en paquete, JSON e informe técnico, C19 OK, CT-02 al Broker) | ídem |
| CA-3 (`revisiones_c2` en F5, `revision_c2` y `accion` en la respuesta) | ídem |
| CA-4 (sin informe entregado, no hay revisión) | `test_pb61_sin_informe_entregado_no_hay_revision`, `test_pb61_un_run_bloqueado_no_cuenta_como_entregado` |
| CA-5 (sin índices nuevos no se reabre; índices inválidos o booleanos no cuentan) | `test_pb61_segunda_respuesta_sin_indices_nuevos_no_reabre` |
| CA-6 (PENDIENTE, FALLIDA sin el texto del error, el error de control se relanza) | `test_pb61_revision_pendiente_sin_ejecutar`, `test_pb61_revision_fallida_queda_anotada_y_el_error_de_control_se_relanza` |
| CA-7 (NO_BLOQUEANTE en plazo, informe C6) | `test_pb61_no_bloqueante_contestada_en_plazo_tras_una_entrega`, `test_pb61_informe_de_seguimiento_c6_entregado_con_el_supuesto` |
| CA-8 (mapa, evidencias, suite, cuotas, goldens) | `tests/test_fase4_mapa.py`; `evidencias_plan_a.py --ejecutar`: 219 de 219; `goldens_ct.py`: coinciden; ruff 2808, mypy A 109 |
| Regresión | `test_v51.py::test_consulta_bloqueante_pausa_y_vencimiento` sigue en verde (la `accion` nombra la revisión) |

## Regresión: fallan sin la corrección

- Sin el cambio de código, la primera prueba falla en `supuestos_cns` (KeyError), comprobado antes de implementar.
- El fichero de mutantes cubre lo demás.

## Mutantes propios

Script: `.docs/tickets/T-174/mutantes_t174.py <carpeta bloque_a> <copia>`. Copia el `bloque_a` entero; con solo `11_Ejecutor` todas las pruebas fallan por el corpus que falta. M0 es la copia sin mutar y tiene que vivir.

| Mutante | Resultado |
| --- | --- |
| M0 sin mutar | vive (control) |
| M1 no abre revisión | muere |
| M2 RUN sin `supuestos_cns` | muere |
| M3 sin nota en limitaciones | muere |
| M4 reabre siempre | muere |
| M5 cuenta RUN bloqueados | muere |
| M6 C6 sin `supuestos_cns` | muere |
| M7 esconde errores de control | muere |
| M8 admite índices booleanos | muere (en la primera pasada vivía; se añadió la comprobación con `indice: True` sobre un índice aún sin contestar) |
| M9 sin los tipos de los revisados | muere |
| M10 la revisión ve la consulta sin la respuesta registrada | muere |
| M11 copia el texto del error en la incidencia | muere |

## Ciclo simulado por la línea de órdenes (cliente mock, código del worktree)

```bash
cd bloque_a/11_Ejecutor
B="python -c 'import sys;from bloque_a.cli import main;main()' --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv --estado $T/estado --salida $T/salida"
$B --as-of 2026-06-05 consulta-broker enviar --json '{"tipo":"ACLARACION_ALCANCE","modo":"BLOQUEANTE","preguntas":[{"texto":"¿Incluimos el franco suizo?","supuesto_declarado":"No se incluye"}]}'
$B --as-of 2026-06-05 ciclo        # RUN-2026-0001 PARCIAL, SIN_RESULTADO (todo el alcance pausado)
$B --as-of 2026-06-12 ciclo        # RUN-2026-0002 COMPLETO, ENTREGADA, con el supuesto declarado
$B --as-of 2026-06-12 consulta-broker responder --cns CNS-2026-0001 --json '{"respuestas":[{"indice":0,"texto":"Sí, inclúyelo"}]}'
```

Resultado:

- `tardia: true`;
- `revision_c2`: RUN-2026-0003, ENTREGADA, revisa RUN-2026-0002, clases DIV;
- el informe técnico y el paquete JSON de RUN-2026-0003 llevan «Revisión C2 de RUN-2026-0002: el Broker contestó a CNS-2026-0001 después de la entrega y el supuesto declarado «No se incluye» ya no se aplica (7.9.5)».

Con `clases: ["CRI"]` no se abre revisión, porque en la configuración por defecto solo DIV está activo y CRI no se analiza; así debe ser.

> **Nota.** El comando `bloque-a` instalado en el `.venv` apunta al repositorio principal, no al worktree. Para probar el código del worktree hay que usar `python -c 'from bloque_a.cli import main; main()'` desde su `11_Ejecutor`.

## Gate

`./tools/check_all.sh` no se ejecutó entero; sus doce comprobaciones se pasaron por separado:

- corpus-integridad, nombres-nfc, yaml-configs, secrets y refs-vivas: en verde;
- ruff: 2808, con cuota 2808 (bajada desde 2813 en `tools/cuotas.txt`);
- mypy: A 109 ≤ 109, A-Forex 174 ≤ 174, B 159 ≤ 159;
- pytest A: la ejecución completa de arriba;
- pytest A-Forex y B: no se ejecutaron, porque no se tocaron.

El gate completo queda para la QA y la integración, junto con lo de las sesiones paralelas.

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q tests/test_t174_pb61_revision_c2.py tests/test_v51.py tests/test_fase4_mapa.py
../../.venv/bin/python tests/goldens_ct.py
../../.venv/bin/python -m pytest -q                       # suite completa (~44 min con la máquina cargada)
cd ../.. && .venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
```

## Commit

Commit local en el worktree (detached, sin push): «wip local: T-174». El hash está en el informe de entrega y en `git log -1`.

## Ronda r02 (QA r01 NO APTO)

Base: rebase sobre `origin/develop` 375d24b (T-165 y T-171). Un conflicto en la deuda técnica, en la fila nueva junto a T-171 y T-172; se conservaron los dos lados.

| Qué | Resultado |
| --- | --- |
| `tests/test_t174_pb61_revision_c2.py` | 18 pruebas: 8 de la r01 y 10 nuevas `test_r02_*`. Todas en verde |
| `revisores/r01_01_ataques.py` (desde `bloque_a/11_Ejecutor`) | 19 de 20 en verde. A2 (H-01), A3 (H-02), A7 (H-03) y A9 (H-04) pasan. **A8 falla a propósito**: afirma `FALLIDA`, y la corrección pedida para H-05 deja `ENTREGADA` cuando el RUN- de la revisión llegó al Broker. La cubre `test_r02_h05_un_fallo_tras_entregar_deja_la_revision_entregada` |
| `test_v51.py`, `test_t162_respuesta_final.py`, `test_t169_hallazgos_t162.py`, `test_t169_r02.py` | 76 en verde |
| `tests/goldens_ct.py` | coinciden |
| Mutantes (`mutantes_t174.py`, 21 más el control M0) | los 21 mueren y M0 vive. Nuevos: M12 sin cerrojo, M13 sin releer la CNS-, M14 sin INTERRUMPIDA, M15 `responder` no relanza, M16 relanza las EN_CURSO, M17 sin intersección, M18 sin fecha, M19 siempre FALLIDA, M20 sin escalado, M21 relanzar sin reclamar |
| Suite completa de A (una vez) | 8164 superadas, 2 omitidas y 1 fallo esperado (`test_fase4_mapa::test_h05…`: el documento de evidencias aún sin regenerar), que pasa tras `evidencias_plan_a.py --ejecutar` |
| Ciclo mock por línea de órdenes | Enviar una BLOQUEANTE sin tipos; ciclo 06-05 (SIN_RESULTADO); ciclo 06-12 (RUN-2026-0002 ENTREGADA); `responder` → revisión RUN-2026-0003 ENTREGADA, revisa RUN-2026-0002, DIV, `intentos` 1. La misma respuesta repetida: `revision_c2` null, nada relanzado. `consulta-broker revisiones` → `[]`. La nota «Revisión C2 de RUN-2026-0002…» aparece en el informe técnico |
| Cuotas | ruff 2808 (cuota 2808; develop 2813) · mypy A 109 ≤ 109 |

## Ronda r03 (QA r02, H-07 y H-08)

| Qué | Resultado |
| --- | --- |
| `tests/test_t174_pb61_revision_c2.py` | 22 en verde (4 nuevas `test_r03_*`) |
| `revisores/r01_01_ataques.py` y `revisores/r02_01_ataques.py` | 20 y 5 en verde: B4 (H-07) pasa, y A8 se corrigió para esperar ENTREGADA (H-05) |
| `test_v51.py` · T-162 y T-169 (`test_t162_respuesta_final.py`, `test_t169_*`) | 13 en verde · 65 en verde |
| `tests/goldens_ct.py` | coinciden |
| Mutantes | M1 a M21 mueren en la pasada completa. En esa pasada M22 (sin `huerfanas` en el ciclo) y M23 (avisa en cada ciclo) vivían. Para M22, la prueba ahora mira el aviso tras el primer ciclo y antes de `responder`. Para M23, la comprobación del aviso pasa a hacerse solo bajo el cerrojo. Con eso, la pasada filtrada `"H-07\|H-08"` da M22 a M28 muertos y M0 vivo |
| Ciclo mock por línea de órdenes, con un proceso que muere (`os._exit` en el ciclo de la revisión) | `revisiones` → `[('EN_CURSO', huerfana True, INC-2026-0002, intentos 1)]`; dos `ciclo` después, 1 solo aviso en HA; `relanzar` sin opción → `[]`; `relanzar --incluir-en-curso` → ENTREGADA RUN-2026-0004, intentos 2; `revisiones` → `[]` |
| Cuotas | ruff 2808 (cuota 2808) · mypy A 109 ≤ 109; una anotación de tipo evita el error nuevo |
| Suite completa de A | no se repite en la r03: la coordinación no la pide y la r02 la pasó entera. Los cambios de la r03 se limitan a `interfaz_broker.py` y a una línea de `orquestacion.py`, que cubren las pruebas de arriba |

## Ronda de cierre de la QA r03 (H-09 a H-11)

| Qué | Resultado |
| --- | --- |
| `tests/test_t174_pb61_revision_c2.py` | 26 en verde (4 nuevas `test_cierre_*`) |
| `revisores/r01_01`, `r02_01` y `r03_01` | 20, 5 y 3 en verde (C1, C2 y C3 incluidas) |
| `test_v51.py` · T-162/T-169 | 13 · 63 en verde |
| `tests/goldens_ct.py` | coinciden |
| Mutantes M0 a M33 | ver la línea «vivos» de la pasada completa en el informe de entrega. Los nuevos son M29 (alta tras escribir), M30 (sin baja si falla la escritura), M31 (clave sin carpeta), M32 (sin la marca de no juzgable) y M33 (otro host juzgado por el pid) |
