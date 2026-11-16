# T-157 · QA independiente

- **Revisor:** Claude, revisor nuevo sin el contexto de la implementación (subagente; formé opinión con el prompt, el plan y el
  código antes de leer `analisis-tecnico.md`) · **Ronda:** r01 · 16-11-2026 · copia `qa28` en `55e2ec5`, sin red ni gasto.

## Reproducción desde limpio

Desde `bloque_a/11_Ejecutor` de la copia:

| Paso | Resultado |
| --- | --- |
| `../../.venv/bin/python -m bloque_a.herramientas.verificador_ids --json <tmp>.json --auditoria <copia de docs/auditoria_ids_bloque_a.md>` | salida 1; «3 errores, 3 avisos»; Documento 0 V5.1 y Catálogo V5.0 |
| La misma orden otra vez, en otro proceso | **otro JSON**: `F2`/`F02` y `F5`/`F05` cambian de orden en `archivos.citas` (y la fila F2 en el Markdown). Ver H-01 |
| `PYTHONHASHSEED` 0 a 5 | 3 JSON distintos; el de `docs/auditoria_ids_bloque_a.json` es solo uno de ellos |
| `tests/test_t157_verificador_ids.py` | 34 superadas (dentro de los mutantes, cada pasada) |
| `.docs/tickets/T-157/mutantes_t157.py` (del implementador) | nulo vivo; los 6 mutantes, matados |
| Suite completa de A (`python -m pytest -q -p no:cacheprovider`) | 6672 superadas, 2 omitidas, 0 fallos (47 min) |
| ruff (las tres carpetas de ejecutor) | 2831 (cuota 2831); los dos archivos nuevos, «All checks passed!» |
| mypy `bloque_a/11_Ejecutor/bloque_a` | 109 (cuota 109); ninguno en `verificador_ids.py` |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py` | en verde; «Corpus íntegro: 695 archivos» después de todas mis pasadas |

## Comprobaciones del encargo

1. **Cada error y cada aviso es real** (contrastado a mano con el corpus y el código):
   - `evaluador.py:491` escribe `"catalog_version": "4.0"` en la entrada RC de la tasa base (FC-EVAL-001, que sí existe): ERROR real.
   - FX-MC10-003 (`Registro de cálculos del Motor (esquema V2.0).md:92`) está en un ejemplo marcado «EJEMPLO FICTICIO», pero es
     un `ficha_id` que el Catálogo V5.0 no tiene: ERROR real como inconsistencia de ID (D-3 lo trata bien).
   - RF-0123 (prompt del Evaluador, l. 116, ejemplo CT-19): única aparición en el corpus; F9 tiene 389 RF con huecos y esa no
     está, ni en el Registro de bajas: ERROR real.
   - Las 8 menciones al «Catálogo V4.0»: MC-01 l. 23 (prosa) y l. 240, MC-02 a MC-05 (valor de `operacion` en ejemplos JSON),
     funciones del Motor l. 23 y el ejemplo de RC l. 92 (`"catalog_version":"4.0"`). Un patrón mío más ancho (sin distinguir
     mayúsculas, «catálogo … 4.0» o `catalog_version … 4.0`) da exactamente las mismas 8.
   - Docstring de `motor/operaciones.py` l. 1: «Catálogo de cálculos V4.0», real; los demás `.py` del Motor citan V5.0.
   - «RF-1» (Auditor l. 459) es la tarjeta de renta fija del informe visual (`#tarjeta-RF-1`, «RF×H2»): bien como AVISO.
2. **Notas informativas.** El informe tiene **13** INFO, no 15: 11 `CITA_EN_CONTEXTO_AJENO` y 2 `CODIGO_FUERA_DE_05` (CC y ENT,
   que en §5.1 no son archivos de `05`). Las 13 son correctas una a una: R30 y F31 están en la lista de códigos JEL del
   Documentador (l. 368); F12 ×4 en `(F1 − F12) / F12` (Materias Primas, l. 81 y 111); F02 y F12 en «Resultados de F02–F12» de
   las funciones del Auditor y de Prospectiva, F05 en «ORQ-F03 a F05»; IDX-FICT-001 es la serie ficticia en `serie_ht01`,
   `simbolo` y `afirmacion`. Ningún error real del corpus actual queda escondido. Pero las reglas son más anchas de lo que dice
   INC-T157-01 y esconderían errores reales sembrados (H-02, H-03). Siembra (`r01_02_siembra.py`, 43 comprobaciones): las seis
   clases nominales dan ERROR (CT-26, R28, F12 en prosa de un prompt, ficha solo en el código, ficha IMPLEMENTADO sin código,
   ID cambiado FX-MOMM-001 ↔ FX-MOM-001, RF-9999, PS9, ficha citada VOL-GARH-001), y «Catálogo V4.1» da AVISO.
3. **Cifras, recontadas con código propio** (`r01_01_cifras.py`, sin importar el verificador): 81 encabezados `### ID`, 81
   filas en el índice §4 (el mismo conjunto), las 81 con madurez IMPLEMENTADO, 81 IMPLEMENTADO y 0 en las otras tres clases, 21 en
   secciones «V5.0» (el 60 frente a 81); 25 CT en §6.1, iguales a las 25 de `CANALES`; R1–R27; PS1–PS8; el mapa F1–F11, FM, RC y
   HA → archivo por H1, idéntico al del informe; ninguna CT, R (salvo R30 JEL) ni PS citada fuera de rango; referencias de (e)
   sin entrada: solo RF-0123 y RF-1.
4. **Falla cerrado y es robusto.** Salida 2 y sin JSON en 9 casos: sin Documento 0, con dos, sin Catálogo, con dos, Documento 0
   que no es UTF-8, sin §6.1, Documento 0 que es una carpeta, Catálogo sin §4 y raíz inexistente. No lee `99_Historico*` (ni en
   la raíz ni dentro de `01_Gobernanza/`). El JSON escrito valida contra `ESQUEMA_INFORME`; el informe dice versión, nombre y
   huella del Documento 0 y del Catálogo. **T-143 simulado** en dos variantes (la V5.1, con su `.docx`, a
   `99_Historico_V5.1/` y a `01_Gobernanza/99_Historico_V5.1/`; una V5.2 con título V5.2 y una regla R28 nueva): lee la V5.2,
   R28 pasa a definida sin error, una cita sembrada en el histórico no aparece, y siguen los 3 errores. Fallo: con un destino
   de salida que no existe no sale 2 (H-06).
5. **Restricciones.** Ningún `.md` ni `.docx` del corpus cambia (huellas de todos antes y después de mis pasadas, más
   `corpus_integridad.py`). No toca `bloque_a_forex/` ni `bloque_b/`. D-1 a D-4 solo se proponen (INC-T157-02 a 05); el código de
   `evaluador.py` y `operaciones.py` sigue igual. Quién decide: D-1 es código del ejecutor y la decide el agente por defecto
   (regla del 13-11-2026), correcto; D-2 a D-4 cambian una entrega congelada y por eso las decide el operador, también correcto
   según los límites de esa misma regla. Observación en H-08.
6. **Determinismo.** No se cumple entre procesos (H-01). Dentro de un proceso sí, y es lo único que prueba la suite.
7. **Mutantes.** Los 6 del implementador, matados. De los 27 míos (`r01_03_mutantes.py`), 13 matados y 14 vivos (H-07). M13
   (`main` sale 0 con errores) queda vivo solo por mi arnés, que muta el módulo dentro del proceso; la prueba que lanza un
   subproceso lo mataría con el cambio escrito en el archivo, así que no lo cuento.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | Salida 1 con 3 errores; sin opciones escribe el Markdown por la salida estándar; `--json`, `--md` y `--auditoria` escriben |
| CA-2 | sí | Pruebas del corpus de juguete y `r01_02_siembra.py` §1: un ERROR por clase (a) a (f) sembrado en el corpus real |
| CA-3 | sí | `test_c_archivos_y_mapa_por_h1`; `r01_01_cifras.py`: el mapa por H1 coincide con mi recuento |
| CA-4 | sí | 9 casos de salida 2 sin informe (`r01_02_siembra.py` §3); para el destino de salida, ver H-06 |
| CA-5 | **no** | Versión y huellas, bien; **dos ejecuciones dan JSON distintos** según `PYTHONHASHSEED` (H-01) |
| CA-6 | sí | `test_informe_que_no_valida_no_se_escribe`; el JSON escrito valida |
| CA-7 | sí | `test_no_lee_historico_ni_ejecutor`; T-143 simulado con una cita sembrada en el histórico |
| CA-8 | sí | `r01_01_cifras.py`: 21 comprobaciones contadas aparte, todas iguales |
| CA-9 | sí | D-1 a D-4 en la auditoría, con INC-T157-02 a 05; INC-T157-01 con los criterios técnicos |
| CA-10 | sí | Suite de A: 6672 superadas, 2 omitidas, 0 fallos; ruff 2831, mypy A 109, gates ligeros en verde |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media (incumple CA-5) | Desde `bloque_a/11_Ejecutor`: `for s in 0 1 3; do PYTHONHASHSEED=$s ../../.venv/bin/python -m bloque_a.herramientas.verificador_ids --json /tmp/h$s.json; done; md5sum /tmp/h*.json`; o `r01_02_siembra.py` §5 | Esperado: el mismo JSON y el mismo Markdown en cada ejecución. Obtenido: 2 o 3 JSON distintos; `F2`/`F02` y `F5`/`F05` cambian de orden en `archivos.citas` y en la tabla F del Markdown, así que `docs/auditoria_ids_bloque_a.*` cambia al regenerarlo sin que cambie nada. Causa: `_clave_id("F2") == _clave_id("F02")`, y `sorted(set(...), key=_clave_id)` deja el empate al orden del `set`, que depende del hash de la cadena en cada proceso. La prueba de determinismo ejecuta dos veces en el mismo proceso y no lo ve (mutante M26, vivo) | Desempatar por la cadena en todos los `sorted` (`key=lambda x: (_clave_id(x), x)`, o que `_clave_id` devuelva `(…, x)`), y una prueba que lance dos subprocesos con `PYTHONHASHSEED` distintos y compare los bytes | abierto |
| H-02 | media | `r01_02_siembra.py` §2: `{"estado_madurez_metodos":"FIR-CARYY-001: implementado"}` y `{"metodo":"Brier frente a la referencia (FC-EVAL-009)"}` en un prompt | Esperado: ERROR `FICHA_CITADA_INEXISTENTE`. Obtenido: INFO «valor del campo JSON «estado_madurez_metodos», que no es el de una ficha». La regla excusa cualquier ficha dentro de cualquier valor de cadena cuyo campo no sea `ficha_id`, `method_id` u `operacion` (`RE_CAMPO_JSON` admite texto antes del ID). Su premisa no se cumple en el corpus: `estado_madurez_metodos` lleva ID de ficha en 7 ejemplos de los prompts de los Analistas (FIR-CARRY-001, FX-PPA-001, VOL-GARCH-001…), y los valores en prosa también. Hoy no esconde nada real (todas existen), pero un error real de la clase (d) quedaría en nota | Excusar solo cuando el ID es el valor entero del campo (`"campo":"ID"`) y el campo está en una lista de campos que no son de ficha (`serie_ht01`, `simbolo`…), o al revés: lista blanca de campos ajenos. Prueba con `estado_madurez_metodos` y con prosa dentro de un valor | abierto |
| H-03 | baja | `r01_02_siembra.py` §2: «Clasificación JEL de la fuente; el contrato CT-27 manda.», «`R29 = R1 + R2`» y «el archivo F13 no existe» en las funciones del Auditor | Esperado: ERROR. Obtenido: INFO en los tres casos. «JEL» excusa toda la línea, un operador excusa todo lo que haya entre comillas invertidas, y una fila `AUD-F13` excusa cualquier F13 del documento. Los INFO reales de hoy están bien explicados | JEL: solo los códigos de la lista que sigue a «JEL». Fórmula: solo las F (las otras clases no tienen notación de fórmula). Función local: solo en las filas de la tabla de funciones o en rangos «F02–F12», «de … a F05» |
| H-04 | baja | `r01_02_siembra.py` §2: «Lee RF-123 y RF-00123.» | Esperado: ERROR (lo más probable es un error de tecleo de una RF de 4 cifras). Obtenido: AVISO `REF_FORMA_DISTINTA`. Está documentado en INC-T157-01 y no queda en nota, pero se pierde de vista entre los avisos | ERROR cuando el prefijo es de (e) y no hay otra lectura, o AVISO solo si el texto dice de qué es el ID (tarjeta, figura…), como «tarjeta RF-1» | abierto |
| H-05 | baja | `r01_02_siembra.py` §2: «Usa la ficha GARCH-VOL-001.», «Según el catálogo v4.0 del Motor.» y «CT‑28» con guion U+2011 | Esperado: algún hallazgo. Obtenido: ninguno. La cita de ficha solo reconoce las familias del Catálogo y del código; la mención de versión distingue mayúsculas; los patrones solo aceptan el guion ASCII. Hoy el corpus no tiene ninguno de los tres (mi patrón ancho da las mismas 8 menciones; la única «ficha» de familia desconocida, WI-METH-001, es una serie de F9) | Menciones sin distinguir mayúsculas; normalizar los guiones Unicode a «-» antes de buscar; dar INFO «posible ficha de una familia desconocida» para la forma `XX(-YY)+-NNN` que no case | abierto |
| H-06 | baja | `r01_02_siembra.py` §3: `--auditoria <doc con marcas> --json /no/existe/i.json` | Esperado: salida 2 y nada escrito. Obtenido: traza `FileNotFoundError` y **salida 1**, la misma que «hay errores», con la auditoría ya reescrita y el JSON sin escribir: las dos salidas quedan desparejas | Comprobar los destinos antes de escribir, capturar `OSError` como fallo cerrado (2) y escribir la auditoría la última (o en un temporal que se renombra) | abierto |
| H-07 | baja | `r01_03_mutantes.py` | 14 mutantes vivos. Las pruebas no protegen: `FILA_DUPLICADA` (M01), `FICHA_DUPLICADA` (M02), `TOTAL_DISTINTO` (M03), `CT_SOLO_CODIGO` de `CANALES_V6` y `CAMPOS_MINIMOS` (M04), `FICHA_DUPLICADA_CODIGO` (M05), `ALTERNATIVA_SIN_FICHA` (M06) y `REF_DEFINIDA_Y_DE_BAJA` (M07); tampoco el escaneo de versiones en los `.py` (M09), del que sale el único error real del código (`evaluador.py:491`) y que ninguna prueba mira con el código real; ni las carpetas con punto (M12), ni la cuenta de «errores» en `validar_informe` (M20), ni las marcas repetidas (M21), ni el desempate (M26, ver H-01). Además, `test_documento_0_en_nfd_se_encuentra` no prueba la NFC: `PATRON_DOC0` no lleva acentos y quitar `_nfc` en `_unico` no la rompe (M14); la NFC solo importa para el patrón del Catálogo | Una prueba por protección. Para M09, que `Codigo.desde_paquete` sobre el paquete real dé `CATALOG_VERSION_LITERAL` en `evaluador.py` mientras exista. Para M14, el Catálogo con nombre en NFD | abierto |
| H-08 | baja | Lectura de INC-T157-03, de la auditoría y del registro de decisiones | (1) D-2 deja las menciones V4.0 de los prompts MC-01 a MC-05 para «la próxima entrega», pero esos prompts son datos que el ejecutor manda al modelo, y la API real (Fase 5, modo sombra) ya está autorizada: con la API, «con la ficha VIGENTE del Catálogo V4.0» llega al modelo. Conviene que el operador sepa que la decisión es previa a la Fase 5. (2) D-1 a D-4 no están en `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`, donde la regla del 13-11-2026 pide apuntar las decisiones; hoy solo constan en la fila T-157 de la deuda. (3) INC-T157-03 cuenta 6 + 1 menciones y el AVISO, 8: la octava es el ejemplo de RC, que va en D-3. Cuadra, pero no se dice | Añadir a D-2 «antes de la Fase 5 con API real», apuntar D-1 a D-4 en el registro de decisiones al cerrar el ticket, y en INC-T157-03 decir que la octava mención va en D-3 | abierto |

Los scripts de ataque van en `revisores/` dentro de este ticket, numerados por ronda y sin sobrescribir. Orden, desde
`bloque_a/11_Ejecutor`:

```bash
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids --json /tmp/r01.json         # salida 1
../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r01_01_cifras.py /tmp/r01.json    # recuento propio; 0 si todo cuadra
../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r01_02_siembra.py                 # siembra, fallo cerrado, T-143, determinismo; hoy 31/43
../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r01_03_mutantes.py                # 27 mutantes; hoy 14 vivos
../../.venv/bin/python ../../.docs/tickets/T-157/mutantes_t157.py                            # los del implementador
```

`r01_02_siembra.py` trabaja en copias temporales de `bloque_a/` y comprueba al final que ningún `.md` ni `.docx` del corpus
cambió. Las 12 comprobaciones que hoy fallan son H-01 a H-06; tras la corrección deberían pasar todas, salvo las de H-04 y
H-05 si se decide mantener ese criterio (entonces se documenta en INC-T157-01 y se ajusta la comprobación en r02).

## Suite completa

Una pasada en `bloque_a/11_Ejecutor` (`../../.venv/bin/python -m pytest -q -p no:cacheprovider`): **6672 superadas, 2 omitidas, 0 fallos** en 47 min 7 s (salida 0). La primera pasada la cortó el reinicio de la sesión sin resultado; esta es la segunda y la única completa. 6672 ≥ 607 y cubre las 34 de T-157 (la instantánea trae también las pruebas de T-156).

## Veredicto

**NO APTO** · CA-5 no se cumple: el informe no es determinista entre procesos (H-01, media). Además, H-02 (media): la regla
del campo JSON escondería en una nota un error real de la clase (d). No hay hallazgos críticos ni altos. Los datos del
informe actual salen del corpus y del código, y los he comprobado: los 3 errores y los 3 avisos son reales y ninguna de las 13
notas esconde nada. Siguiente: el implementador corrige H-01 y H-02 con sus pruebas (y, si quiere, H-03 a H-07), regenera
`docs/auditoria_ids_bloque_a.*`, y el revisor repite los tres scripts r01 en una ronda r02.
