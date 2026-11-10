# T-92 · Correcciones de la auditoría de Astra al Bloque A, revisadas e integradas sobre develop

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r04 APTO, 11-11-2026; H-32 a H-39, medios y bajos, en la deuda como T-93) |
| Pieza | bloque_a |
| Planifica · implementa · QA | Astra (auditoría y correcciones, rama `astra/bloque-a-integridad-y-evidencia`, commit `76b90e6`) · Claude (revisión, selección e integración sobre develop) · un revisor nuevo sin contexto |
| Aprobación del operador | Pedida por el operador el 2026-11-10: «Quiero que evalúes bajo tu criterio las propuestas e implementes aquellas que consideres que ofrecen mejorías al bloque A» |
| Deuda técnica | T-92 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Llevar a develop las correcciones de la auditoría de Astra al Bloque A que mejoran el bloque, sin deshacer lo que T-65 cerró después de que Astra partiera de `bc90534`, y corregir los defectos que la revisión encontró en la rama.

## Por qué un ticket nuevo

- La rama de Astra parte de `bc90534`, anterior a las cinco rondas de T-65: al fusionarla chocan 13 ficheros (evaluación, síntesis, contratos, agentes, Motor, cuotas, líneas base).
- Astra la numeró T-87, pero en develop T-87 ya es SC-5 (marco común de C, abierto en T-80). Sus documentos se conservan en `auditoria_astra/` como evidencia.

## Qué entra (evaluación de cada propuesta)

La matriz completa de Astra está en `auditoria_astra/`: `datos.md`, `agentes.md`, `contratos.md` y `controles.md`. Se integran:

| Grupo | Casos | Decisión |
| --- | --- | --- |
| Datos y evaluación | D01 base congelada al emitir; D02 CESTA con la composición de la emisión; D05 certificado por clase × horizonte × método (R13 del Documento 0); D08 backtest en una salida vacía; D09 huella con las fechas; D10 CSV solo dentro de la raíz de datos; O3 F10 por fecha de efecto | Entran |
| Agentes | A1 clave de caché con cliente, prompt, esquema y límite; A2 R8 en lo que se envía y se recibe; A3 la cinta conserva truncamiento y rechazo; A4 rechazo o pausa → PARCIAL; A5 referencias dentro del corte; A6 tope de ampliación con lo ya autorizado; A7 error del SDK → PARCIAL saneado; A8 CALC contrastados | Entran (A2 con el patrón corregido, H-01; A6 con números de la configuración, INC-T92-01) |
| Contratos | C2 sobre; C3 acuse durable de CT-01; C4 alias de CT-25 del servicio pedido; C5 CT-04 validado antes de escribir; C7 ejemplo conforme; C8 control de R21 | Entran (C3 con reconciliación, H-03) |
| Controles | O2 hora del plazo de CT-23; O4 permisos de F10; O5 cerrojo entre procesos; O6 sin alta fantasma; O7 sellos de final de cadena; O9 SEG forzado tras su fin; O10 CT-22 validado antes de persistir | Entran (O7 con marca de formato, H-02) |

## Qué no entra

- **C6, despacho del Motor:** develop (T-65, CS-08) ya rechaza con `METODO_NO_IMPLEMENTADO` las fichas documentadas, también las tres que tienen código pero el Catálogo da por «Documentado» (`DOCUMENTADAS_CON_CODIGO`). La rama volvía a darles cifras citables (H-04). Se conserva lo de develop y la lista de 81 fichas de la V5.0.
- **`bloque-a preparar-encargo-b`:** es una función nueva (el borrador de CT-B-01 para B), no una corrección. Va con la Fase 6 (cadena A→B). Queda en la rama de Astra.
- Las líneas base y cuotas de la rama (A 244): manda develop (A 326), más las pruebas nuevas.

## Hallazgos de la revisión de la rama (corregidos aquí)

| ID | Gravedad | Hallazgo | Corrección |
| --- | --- | --- | --- |
| H-01 | Media | El filtro R8 nuevo de A2 usa `sk-[A-Za-z0-9_-]{20,}` sin límite por la izquierda: «risk-and-return-of-venture-capital», «disk-…» o «task-…» se toman por una clave. Seis líneas del corpus operativo (F7 y el registro de fuentes) lo disparan, y el encargo o la respuesta se descartan como PARCIAL sin llamar al modelo (`revisores/rama_02_prompts_sensibles.py` y `rama_03_falsos_positivos_r8.py`) | Patrón con `(?<![A-Za-z0-9_-])sk-`; pruebas de palabras corrientes y de claves reales |
| H-02 | Baja | O7: si se borra `sellos_integridad.json`, el almacén se trata como anterior a los sellos y un truncado del final se vuelve a sellar en silencio (`revisores/rama_01_sellos.py`, S1) | Marca `formato_almacen.json`: un almacén ya sellado sin su fichero de sellos falla cerrado; uno anterior se sella al abrirlo |
| H-03 | Baja | C3: un fallo dentro del ciclo deja el `msg_id` reservado para siempre, sin estado legible ni forma de liberarlo | `estado_reserva()` (COMPLETADO, FALLIDO con la clase del error, EN_CURSO, DESCONOCIDO); `reconciliar(msg_id, motivo)` y `bloque-a reconciliar-mensaje`, con incidencia en HA; el texto del error no se guarda |
| H-04 | Alta (al integrar) | C6 deshacía la decisión de T-65 (CS-08) sobre las fichas «Documentado» con código | Se conserva lo de develop (prueba `test_fichas_documentadas_con_codigo_siguen_sin_cifras_citables`) |
| H-05 | Media (al integrar) | Las fusiones con T-65 cambian reglas: frescura por serie y horizonte (H-24), fecha de efecto de H5 desde el mismo ciclo (H-13), parámetros sin literales de respaldo (H-05) | Se conservan las tres; D02 sustituye la regla de T-65 de quitar de la CESTA al miembro que no sirve (ver Diseño) |

## Diseño

- **Base de las rentabilidades (D01 y T-65):** la base es la congelada en F4 al emitir (`nivel_referencia`, `nivel_referencia_indice`, `bases_cesta`); si falta, la conocida al emitir (corte de conocimiento de HT-01). Encima se aplica la frescura de T-65: cada serie necesita un dato posterior a la base y no más antiguo que la antigüedad de PS2 del horizonte.
- **CESTA (D02):** cuentan los mismos miembros que al emitir. Si un miembro no sirve, la CESTA no sirve y el pronóstico espera (después, NO_RESOLUBLE). Sustituye la regla de T-65 de dejarlo fuera: saber al resolver que un miembro dejó de publicarse es información posterior a la emisión (sesgo de supervivencia, fuga).
- **Tope de ampliación (A6):** total ≤ base × (1 + `ampliacion_max_autorizable`), con los dos números de la configuración. Es la lectura prudente del Anexo A; la otra lectura (+50 % además del +25 % automático) está en INC-T92-01, `[PROPUESTO]`, para T-57.
- **Estado persistido:**
  - ficheros nuevos en la carpeta de estado: `sellos_integridad.json`, `formato_almacen.json`, `acuses.sqlite3` y `.almacen.lock`;
  - un almacén anterior se sella al abrirlo (no se puede saber si ya le faltaba el último registro);
  - una tabla de acuses anterior gana la columna `error`.
- **Falla cerrado:**
  - un almacén manipulado o sin sellos no abre;
  - una base inválida o posterior no resuelve;
  - una referencia fuera del corte no llega a F2;
  - un turno incompleto es PARCIAL.

## Criterios de aceptación (binarios)

1. CA-1: las 43 pruebas de Astra (`test_t87_*`) y las de `test_t92_revision.py` pasan sobre develop.
2. CA-2: las pruebas de T-65 (r01 a r04) y de T-53 y T-66 siguen pasando, salvo las que prueban la regla de la CESTA que D02 sustituye, que se cambian con su motivo.
3. CA-3: gate completo 12/12, con la línea base de A subida al nuevo total.
4. CA-4: H-01 a H-05 tienen su prueba, y cada una falla con el código de la rama de Astra.
5. CA-5: INC-T92-01 registrada como `[PROPUESTO]` y en T-57.

## Ronda r02 (correcciones de la QA r01)

| ID | Gravedad | Corrección |
| --- | --- | --- |
| H-06 | Alta | `_base_conocida` valida el cierre de la base con `_validar_cierres` de HT-01, que rechaza cierres no positivos, no finitos, booleanos y fechas repetidas. Un miembro así al emitir queda fuera de la CESTA, igual que en develop (se sabía al emitir). `_rentabilidad_serie` rechaza además una base congelada ≤ 0 |
| H-07 | Media | Patrón `sk-` de R8: no va pegado a una letra, cifra, «.», «/» o «-», y tiene un tramo de al menos 16 caracteres sin guion (la parte aleatoria de una clave). «/sk-hynix-posts-record-…» o «sk-hynix-posts-record-quarterly-profit» ya no son claves; `OPENAI_KEY_sk-…`, `sk-ant-api03-…`, `sk-proj-…` o una clave en hexadecimal sí. Las 6 líneas del corpus operativo dan 0 |
| H-08 | Media | El `msg_id` del Broker tiene su propio espacio, `MSG-BRK-AAAA-NNNNNN`, y nunca coincide con los que numera el bloque |
| H-09 | Media | `senales.umbral_favorable: 0.5` en `por_defecto.yaml` (`[PROPUESTO]`, el punto medio de la escala 0–1) |
| H-10 | Media | Una interrupción (Ctrl-C o `SystemExit`) durante la escritura también trunca la línea. Si el proceso murió entre el registro y el sello, al abrir se apartan los registros sin confirmar a `*.no_confirmado.jsonl`, la cadena se queda en lo sellado y se anota una incidencia en HA. Menos registros que el sello sigue siendo un fallo de integridad |
| H-11 | Baja | Límite declarado, que pasa a la deuda: quien borre a la vez el final, los sellos y la marca reescribe la carpeta, y eso exige una copia o una firma externas |
| H-12 | Baja | `reconciliar` escribe primero la incidencia en HA y después libera la reserva |
| H-13 | Baja | La primera respuesta de CT-01 se devuelve en la misma forma que se guarda, así que la repetida es idéntica |
| H-14 | Baja | Una fecha ilegible en una base congelada da `DatosNoDisponibles` y no tumba C5 |
| H-15 | Baja | Un plazo de CT-23 que solo trae la fecha vence al terminar ese día, como antes |
| H-16 | Baja | `ri-probar/SKILL.md` con A ≥ 386, enlace del README a `T-92/auditoria_astra/handoff.md` y recuentos de las pruebas al día |

**Sondas de la QA r01:**
- `r01_01` (1c): el miembro con cierre negativo al emitir ya no se congela, así que el PRG se resuelve con el resto de la CESTA. Es la regla de develop; la sonda esperaba que no se resolviera porque estaba escrita contra el defecto.
- `r01_02` (2): es H-11, el límite declarado.
- `r01_03`: su caso de un `msg_id` externo igual a uno interno ya no se puede construir, porque `crear` lo rechaza (H-08).

## Ronda r03 (correcciones de la QA r02)

| ID | Gravedad | Corrección |
| --- | --- | --- |
| H-17 | Alta | R8 detecta las claves `sk-` en dos pasos:<br>1. Un candidato lineal: «sk-» sin una letra, cifra, «.», «/» o «-» pegados delante, seguido de 20 caracteres o más de `[A-Za-z0-9_-]`.<br>2. `_es_clave_sk` decide en Python. Es clave si lleva un prefijo de proveedor (`ant-`, `proj-`, `svcacct-`, `admin-`), si tiene un tramo de 16 o más sin «-» ni «_», o si mezcla mayúsculas y cifras.<br><br>Resultados: 2000 claves realistas detectadas (`sk-ant-api03-…`, `sk-proj-…`, `sk-svcacct-…` y genéricas, con «_» y «-»); entradas adversarias de hasta 140 KB en menos de 2 s; los textos de H-01 y H-07 y los nombres de fichero con «_» de `r02_01` no cuentan como clave |
| H-18 | Media | `contiene_credenciales` busca en el volcado JSON y además en cada texto tal cual, así que una clave tras un salto de línea o un tabulador se detecta |
| H-19 | Media | La recuperación solo admite UN registro por encima del sello (lo que deja una escritura cortada). Más de uno es un fallo de integridad. Solo se recupera al abrir: una instancia viva falla cerrado (`verificar_integridad` da False y la escritura siguiente se rechaza) |
| H-20 | Baja | Al abrir, primero se validan todos los ficheros y después se aplican las recuperaciones: si uno no valida, no se ha reescrito nada |
| H-21 | Baja | Si la interrupción llega cuando el sello nuevo ya está en disco, el registro se da por confirmado y no se trunca |
| H-22 | Baja | Un plazo con solo fecha («2026-06-08», «2026-6-8» o «20260608») vence a la medianoche local siguiente, calculada en la zona del reloj, también los días de cambio de hora |
| H-23 | Baja | `senales.umbral_favorable` debe ser un número en [0, 1] (NaN, booleanos, texto o valores fuera fallan cerrado) y está en T-57 |
| H-24 | Baja | Fila T-92 de la deuda al día; H-11 declarado como límite en la deuda; diseño de las rondas en `analisis-tecnico.md` |

**Sondas de la QA r02:** con el código de la r03, `r02_01`, `r02_02` y `r02_03` dan 0 fallos. `r02_04` (caso 3) marca los días de cambio de hora porque envía la consulta el 5-6 con un plazo de marzo, y el 29-3 esa consulta aún no existe; con la consulta enviada antes del plazo, `test_r02_h22_…` comprueba los dos cambios de hora.

## Ronda r04 (correcciones de la QA r03)

| ID | Gravedad | Corrección |
| --- | --- | --- |
| H-25 | Alta | El candidato «sk-» solo exige que no haya una letra o una cifra pegada delante, así que «/», «-», «.», «_», `key-` o un espacio valen. El texto se mira también con los escapes de JSON («\\n», «\\t», «\\r», «\\/») sustituidos |
| H-26 | Media | La regla se invierte: es clave todo lo que no tenga forma de texto corriente (ver `analisis-tecnico.md`, «Ronda r04»). Se detectan los UUID (también con `lf-`), el hexadecimal con «-», las minúsculas con «_», `token_urlsafe`, «SK-» y los `bytes` |
| H-27 | Media | Más de un fichero con registros sin sello es un fallo de integridad: una escritura cortada deja como mucho uno en todo el almacén |
| H-28 | Baja | Los códigos de periodo de los informes («2024Q4», «FY2023», «3Q24») cuentan como texto |
| H-29 | Baja | Una última línea a medio escribir se aparta al abrir, como las demás no confirmadas. Si el proceso muere entre reescribir y anotar la incidencia, el rastro queda en el fichero apartado; es un límite declarado |
| H-30 | Baja | El plazo de CT-23 solo admite ISO 8601 («2026-06-08», «20260608», con hora y zona opcionales). Una medianoche inexistente pasa a la primera hora válida |
| H-31 | Baja | `pruebas.md` con el recuento contra la r02, README del ejecutor en singular y con la instancia viva, y límites del sello restaurado en `analisis-tecnico.md` |

**Sondas:** con el código de la r04 dan 0 fallos `r03_01`, `r03_02`, `r02_01`, `r02_02` y `r02_03`. `r03_03` da 1 (caso 2a) a propósito: la r04 rechaza «2026-6-8» y «2026/06/08». Siguen marcando las ya explicadas: `r02_04` caso 3, `r01_01` caso 1c, `r01_02` caso 2 (H-11) y `r01_03` caso 1. Desde la r04, «2026-6-8» se rechaza en lugar de entenderse.

## Cierre

QA r04 **APTO** (`qa.md`, «Ronda r04»): CA-1 a CA-5 cumplidos y ningún hallazgo crítico ni alto. Gate 12/12 (A 439, A-Forex 68, B 176).

Quedan en la deuda como **T-93** los hallazgos medios y bajos de la r04. La QA recomienda corregir H-32 y H-34 antes del modo sombra con API:
- **H-32 (media):** R8 no ve una clave pegada a otros escapes (`\\uXXXX`, `\\b`, `\\f`, `%XX`, `\\xNN`).
- **H-33 (media):** falsos positivos con URL de prensa financiera en minúsculas.
- **H-34 (media):** un almacén anterior a los sellos con la última línea a medias.
- **H-35 a H-39 (bajos):** corte a mitad de un carácter UTF-8; claves hechas solo de tramos que parecen texto; plazo numérico o `date` en CT-23; un plazo no ISO guardado por develop bloquea `vencer()`; documentación.

Sigue el límite H-11, en la fila T-92.
