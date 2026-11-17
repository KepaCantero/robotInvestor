# T-164 · Bloque A: hallazgos de la QA r02 del verificador de IDs (T-157)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r02 APTO tras la ronda de cierre) |
| Pieza | bloque_a (herramientas): `bloque_a/11_Ejecutor/bloque_a/herramientas/verificador_ids.py` y `tests/test_t157_verificador_ids.py` |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin el contexto de la implementación (`compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: herramienta de medida; no cambia contratos, corpus, controles ni el comportamiento del ejecutor (tipo «corrección, pruebas» de `ri-planificar`) |
| Deuda técnica | T-164 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar los hallazgos abiertos de la QA r02 de T-157 (`.docs/tickets/T-157/qa.md`, «Hallazgos nuevos»): H-09 (media), H-10,
H-11 y H-12 (bajas), y comprobar que H-04 sigue documentado. Ahora, porque la Fase 0 está cerrada y el verificador se volverá a
usar al recargar el corpus (D-2 a D-4).

## Alcance

- **Entra:** `verificador_ids.py` (las reglas de H-09 y H-10 y la escritura de H-11; versión 1.0.0 → 1.1.0), sus pruebas en
  `tests/test_t157_verificador_ids.py` (H-12 y una prueba por corrección), `INC-T157-01` en `docs/incidencias.md` (los criterios
  nuevos), la fila T-164 de la deuda técnica y este ticket con su script de mutantes (`mutantes_t164.py`).
- **Entra también** (a petición de la sesión coordinadora): regenerar `docs/auditoria_ids_bloque_a.*` con el verificador 1.1.0.
  Cambia por T-143 (Documento 0 V5.2, huella del corpus, citas, y las huellas de `contratos.py` y `servicio.py` que cambiaron
  después de T-157) y por la versión del verificador. Los hallazgos no cambian (`pruebas.md`, «Informe regenerado»).
- **No entra:** el corpus congelado, otros bloques, las decisiones D-2 a D-4 (del operador).

## Diseño

- **H-09: la excusa del símbolo, por aparición y contexto.** El diccionario de símbolos declarados (`serie_ht01`/`simbolo` con
  el ID como valor entero) se mantiene, pero ya no excusa todas las apariciones. Cada aparición de un ID declarado se excusa solo si:
  (1) está dentro del valor de un campo de serie (`serie_ht01`, `simbolo`), o (2) no está en un contexto de ficha. Contexto de
  ficha: el valor (cadena o array de escalares) de un campo de ficha `CAMPOS_FICHA = ("ficha_id", "method_id", "operacion",
  "estado_madurez_metodos")` —los campos del corpus cuyo valor es una ficha— o la palabra «ficha»/«fichas» antes de la aparición
  en la misma frase. La frase empieza tras el último «.», «!» o «?» seguido de espacio que no cierra una abreviatura («p.», «ej.»,
  «e.g.», «i.e.», «vs.», «cf.», «pág.», «núm.», sin distinguir mayúsculas desde la ronda de cierre, H-07) o, dentro de un valor JSON, en su clave. En un array de objetos cuentan las claves de dentro.
  Así queda desde la r02 (QA r01: H-01 y H-02); antes «;» cortaba la frase y la frase de un valor empezaba en el propio valor.
  Límite (H-03): el contexto se lee en la línea de la cita (ver INC-T157-01).
  Se aplica igual a las familias conocidas y a las desconocidas (`FAMILIA_DESCONOCIDA`): una aparición excusada de familia
  desconocida pasa a INFO `CITA_EN_CONTEXTO_AJENO` en lugar de omitirse. Alternativa descartada: excusar solo en el mismo archivo
  que la declaración; rompería `IDX-FICT-001` en el Registro de pronósticos congelados, que se declara en otros archivos.
- **H-10: fichas con otro número de cifras.** Un ID con la forma de cita de ficha (familia conocida y segmentos intermedios) y
  una, dos, cuatro o más cifras finales es ERROR `FICHA_CITADA_INEXISTENTE`, con «(¿X?)» cuando hay una ficha parecida (mismo
  criterio de `DISTANCIA_PARECIDO`). Las cifras son la propia forma de los ID del Catálogo (`RE_ID_FICHA`, tres), no un número
  nuevo: el patrón nuevo es «otra cantidad que no sea esa». Con la misma excusa de símbolo que H-09.
- **H-11: escritura atómica en grupo.** `_escribir_todo` comprueba los destinos como hasta ahora, después escribe **todos** los
  temporales y solo cuando todos están escritos los renombra (la auditoría la última). Si un temporal o un renombrado falla, borra
  los temporales que queden y relanza el `OSError` (salida 2). Límite: un fallo de `os.replace` a mitad de los renombrados deja
  renombrados los anteriores (no hay transacción entre archivos); se documenta. r02 (QA r01: H-04 y H-05): un destino pedido dos
  veces es `EntradaInvalida`, y el temporal toma los permisos del destino que ya existe antes de renombrarse.
- **H-12:** una prueba por mutante vivo (N02, N04, N05, N06, N07, N08) y `mutantes_t164.py` con esos y los de las reglas nuevas.
- **H-04:** sin cambio de código; se comprueba que INC-T157-01 y `test_e_referencias` lo recogen.
- **Estado persistido:** no hay. **Esquema del informe:** no cambia (los códigos de hallazgo ya admiten `^[A-Z0-9_]+$`).
- **Números:** ninguno nuevo. **Fallo cerrado:** igual que antes; con un destino que no admite archivos, salida 2 y nada escrito.
- **Decisiones `[PROPUESTO]`:** los criterios técnicos nuevos, en INC-T157-01 (técnicos, del verificador).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La regla de contexto de ficha da errores falsos en el corpus real | Informe real con errores nuevos | Comparar el informe con el de develop; hoy el único símbolo con forma de ficha (IDX-FICT-001) nunca va tras «ficha» ni en un campo de ficha |
| El patrón de H-10 casa con otros identificadores | Errores falsos | Exige una familia de ficha conocida y un segmento intermedio; en el corpus real no casa nada (comprobado con `grep`) |
| Reescribir reglas deja inaplicables mutantes de los revisores | `r02_02_mutantes.py` sale ROTO | Conservar los textos mutados; si uno se reescribe, explicarlo y cubrirlo con un mutante propio |

## Criterios de aceptación (binarios)

1. **CA-1 (H-09):** una ficha declarada como símbolo en otro archivo y citada «con la ficha X», o como valor de `ficha_id`
   en la misma línea que su `serie_ht01`, da ERROR; la aparición como valor de la serie y la prosa sin «ficha» siguen en INFO.
2. **CA-2 (H-10):** «FX-TREND-01» y «FX-TREND-0001» dan ERROR con «¿FX-TREND-001?» (en el juguete, AA-ALFA-01 y AA-ALFA-0001).
3. **CA-3 (H-11):** `--json <válido> --md /proc/x.md --auditoria <doc>` sale 2 sin dejar el JSON, ni la auditoría cambiada, ni
   temporales; lo mismo cuando falla un temporal o un renombrado (simulado).
4. **CA-4 (H-12):** los 6 mutantes vivos de `r02_02_mutantes.py` mueren y `mutantes_t164.py` no deja ningún vivo (nulo vivo).
5. **CA-5:** `r02_01_ataques.py` da 16/16; `r01_01_cifras.py` 21/21; `r01_02_siembra.py` y `r01_03_mutantes.py` como en la r02
   (fallos ya explicados allí); `mutantes_t157.py` sin vivos.
6. **CA-6:** el informe del repo real es el de develop salvo el número de versión del verificador.
7. **CA-7:** ruff ≤ 2813, mypy A ≤ 109; suite completa de A sin fallos; gates ligeros en verde; corpus íntegro.
8. **CA-8 (H-04):** INC-T157-01 lo documenta y `test_e_referencias` exige el AVISO.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t164_h09_simbolo_no_excusa_como_ficha` | regresión | CA-1 |
| `test_t164_h09_simbolo_de_familia_desconocida` | regresión (N04) | CA-1, CA-4 |
| `test_t164_h10_ficha_con_otro_numero_de_cifras` | regresión | CA-2 |
| `test_t164_h11_*` (temporal que falla, renombrado que falla) | fallo cerrado (N06) | CA-3, CA-4 |
| `test_t164_h12_destino_carpeta_es_entrada_invalida` | fallo cerrado (N05) | CA-4 |
| `test_t164_h12_rango_con_un_extremo_ajeno_no_excusa_el_otro` | límite (N02) | CA-4 |
| `test_t164_h12_formula_y_jel_solo_excusan_lo_suyo` | límite (N07, N08) | CA-4 |
| Scripts del revisor de T-157 y `mutantes_t164.py` | mutación, ataque | CA-4, CA-5 |
| Verificador sobre el repo real frente al de develop | regresión | CA-6 |
| Suite completa de A, ruff, mypy, gates ligeros | gate | CA-7 |

## Scripts

`.docs/scripts/nuevo_ticket.sh`, `.docs/tickets/T-157/revisores/*.py`, `.docs/tickets/T-157/mutantes_t157.py`,
`.docs/tickets/T-164/mutantes_t164.py` (nuevo) y `.docs/scripts/evidencias_plan_a.py` (si cambia el mapa de pruebas).

## Registro

- 2026-11-17 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-17 · PLANIFICADO · claude · plan, criterios y pruebas; tipo «corrección», sin aprobación del operador
- 2026-11-17 · EN CURSO · claude · H-09 a H-12 implementados con 9 pruebas nuevas; `mutantes_t164.py`
- 2026-11-17 · EN QA (r01) · claude · scripts del revisor de T-157 como se esperaba, mutantes propios todos matados, informe real igual al de develop salvo la versión del verificador; commit local «wip local: T-164», sin push
- 2026-11-17 · EN QA (r01) · claude · `docs/auditoria_ids_bloque_a.*` regenerado (por T-143 y la versión 1.1.0); la copia adaptada de `r01_02_siembra`, 39/43
- 2026-11-17 · EN QA (r01) → NO APTO · revisor · H-01 (media) y H-02 a H-06 (bajas) en `qa.md`
- 2026-11-17 · EN QA (r02: QA r01 NO APTO) · claude · H-01 a H-06 corregidos según `qa.md` (H-03 y H-06 solo documentación); 2 pruebas y 6 mutantes nuevos
- 2026-11-17 · QA r02 APTO · revisor · un solo bajo, H-07 (abreviaturas «Ej.» e «i.e.»)
- 2026-11-17 · EN QA (ronda de cierre de la QA r02) · claude · H-07 corregido como dice `qa.md`; 57 pruebas, `r02_01_regresiones` 19/19, mutantes de T-164 todos matados
- 2026-11-17 · CERRADO · revisor · ronda de cierre comprobada: H-07 corregido; QA r02 APTO (`qa.md`, «Ronda de cierre»)
