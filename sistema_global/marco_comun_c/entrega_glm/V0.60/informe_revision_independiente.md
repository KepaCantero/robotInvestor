# Revisión independiente — V0.60, pieza 1 del kit 2 (robustez de los seis validadores de mensajes)

Fecha de la revisión: 9 de noviembre de 2026. Revisor: GLM (conversación de revisión independiente,
según las secciones 0 y 9 de las directrices del kit 2). Entorno: Python 3.12.16, jsonschema 4.26.0.
Verificación contra el código real, no contra lo que declara la entrega.

**Estado: revisión ejecutada — cuatro hallazgos (2 medios, 2 bajos), ninguno de producto.**
Los seis validadores se comportan como promete la pieza en todo lo sondeado (incluidas cinco sondas
adversariales propias); los cuatro hallazgos son de **cobertura de la batería** y de **exactitud del
Documento 0 y del LEEME**, que prometen algo más de lo que la batería demuestra. `validar_sobre.py`
quedó byte a byte como estaba tras la prueba de no-vacuidad (se restauró y el lote cierra en verde).

## Qué se verificó

1. **El lote completo en verde, en mi propia ejecución**: las 50 baterías (`ejecutar_pruebas.py` no se
   ejecuta aparte; 50 ficheros `pruebas_*.py`), todas terminan en «TODAS LAS PRUEBAS PASAN» y sin una
   sola línea FALLA; coincide con la `salida_pruebas.txt` entregada (mismos resultados, tiempos ±10 %).
2. **La batería nueva**: 65 comprobaciones (cuenta exacta, coincide con el desglose de §4: 2 del
   generador + 12 del sobre + 2 de defecto_01 + 7 del encargo + 6 del informe + 17 del sello + 5 de E +
   7 de H + 6 del anidado + 1 de determinismo), 1.900 casos mutados + 12 casos fijos, semilla 20261110
   (nunca el random global), sello rotado 4:1 entre sello y calendario, ~30 s de reloj (30,2 s en mi
   ejecución, menos de los 90 exigidos). **Determinista**: dos ejecuciones consecutivas con salida
   idéntica byte a byte. Los fixtures existen (7 sobres, 2 encargos, 7 sellos) y las bases dan lista
   vacía antes de mutar.
3. **La no-vacuidad del defecto_01**: restaurada la línea de V0.53
   (`not ctx.get("apalancamiento_permitido", False)`), la batería nueva FALLA exactamente en
   `defecto_01_permiso_ajeno_no_habilita_apalancamiento_V15` y las otras 64 siguen en verde (la
   corrección no aprieta de más: con permiso `True` y apalancamiento 2 el sobre sigue válido). Las
   baterías antiguas del camino del sobre (sobre_t27, encargo, encargo_t51, extremo, integracion_v053,
   orquestador, propuesta, jornada) **siguen pasando con la línea antigua**: ninguna usaba un permiso
   no booleano en el camino del sobre (el `"false"` de `pruebas_encargo.py:158` va al camino del
   encargo, que ya exigía `is True` antes de esta pieza). `validar_sobre.py` se restauró después
   byte a byte y la batería vuelve a estar en verde.
4. **Los seis validadores, leídos contra los predicados de la batería**: los cuatro envoltorios de
   mensajes atrapan `RecursionError`/`MemoryError` (está en sus `ERRORES`), `dimensionar` captura
   `Exception` → E-01 y `vigilar` captura por posición (H-19) y en el instante (H-09). Los casos fijos
   del calendario (sin `version`, sin `mercados`, `anios` de texto, `hora_cierre_utc` mal formada →
   S-01 por el constructor de `Calendario`) son reales, y los seis casos de anidado a 500 niveles
   construyen cada uno su estructura fresca (sin `deepcopy` que desborde la batería). El recuento de
   comprobaciones por bloque y la rotación declarados en §4 coinciden con el código.
5. **Sondas adversariales propias** (`sondas_revisor_v060.py`, todas cierran): `dimensionar` no muta
   ninguna de sus cuatro entradas en 300 casos mutados (idem con `paso=0,5`); los borrados que dejan
   una lista bajo su `minItems` acaban en la regla de esquema; `estado` del sello alterado dentro del
   enum queda sin S-12 pero el encargo lo ve con E-16; `sc3`/`sello_encargo` corruptos dan V-01;
   cobertura real de H con la semilla de la batería (151 casos rotos / 49 frescos, solo H-03 en rotos).
6. **Sin cambios de esquema, configuración ni migraciones**: `version_config` sigue en CFG-0.11.0, el
   registro de contratos no varía y `pruebas_migraciones_t03.py` está en verde sin registrar nada.
   Límite de la revisión: el ZIP no trae instantánea de V0.53, de modo que el diff byte a byte
   V0.53 → V0.60 no es verificable aquí; los indicios (CFG, registro, migraciones en verde, lote
   completo en verde) son coherentes con «solo los ficheros declarados en §4».

## Hallazgos

| # | Gravedad | Dónde | Hallazgo | Script | FALLA antes | Corrección propuesta |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | media | `pruebas/pruebas_robustez_validadores.py` (bucle de E; foto de H) + Documento 0 §1/§2.2 + LEEME | La batería **no demuestra «no muta la entrada» para `dimensionar`** (ni para `ahora`/T1 en `vigilar`, donde la foto cubre solo los datos), aunque §1 promete «las cuatro promesas para los seis validadores» y el LEEME dice «no lanzan, no mutan la entrada…» a secas. El protocolo de §2.2 (foto del par antes de llamar) no es el que aplica el bucle de E: no hay foto ni comparación posterior. El producto está limpio (sonda: 300 casos sin mutación) | `hallazgo_1_revision_v060_no_muta_dimensionar.py` | exit 1: sección E sin foto/_igual_nan ni comprobación de no-mutar | Foto con `_igual_nan` de las cuatro entradas en el bucle de E y de T1 en H, comprobación (o sumada a las existentes) + regresión `r01_…`; ajustar §1/§2.2 y el LEEME a lo que la batería hace |
| 2 | media | Batería (CLAVES_CTX_SOBRE, ADMITE_*) + Documento 0 §1 y §2.4 | **Claves del contexto que el Orquestador pasa siempre no se mutan**: `validar_sobre` lee también `sc3` y `sello_encargo` (camino V-26; el Orquestador los pasa en cada llamada, orquestador.py:1791-1793) y `validar_informe` lee `autoria_c`/`autoria_contradictor` cuando están configuradas (orquestador.py:1820). §1 promete «mutando tanto el mensaje como cada clave de su contexto» y §2.4 dice «solo lee» una enumeración que omite esas claves. El producto falla cerrado: sc3 corrupto → V-01; sello_encargo corrupto (con sc3 presente) → V-01 | `hallazgo_2_revision_v060_contexto_sc3_sello.py` | exit 1: producto OK, batería sin esas claves | Incluir `sc3` y `sello_encargo` en la rotación del sobre (ADMITE: V-01/V-26) y un caso del informe con `autoria_c`/`autoria_contradictor` mutadas (regresión `r02_…`); corregir §1 y §2.4 |
| 3 | baja | Batería (`_forma_real`) + Documento 0 §2.3 | `_forma_real` reclasifica TODO borrado de elemento de lista como «de valor» («el esquema admite cualquier longitud sobre su mínimo»), pero **no mira el mínimo**: borrar el último elemento de una lista con `minItems` 1 (cartera_compatible e incertidumbre del sobre; escenarios_fallo y evid_refs del informe; mercados y fuentes del sello) o de `resultado_reglas` (15→14, minItems 15) **rompe la forma del esquema** y la batería deja de exigir ahí la regla de esquema (solo las promesas generales). El validador de verdad sí falla cerrado en los seis casos sondeados (V-01/C-01/S-01) | `hallazgo_3_revision_v060_minitems_borrados.py` | exit 1: producto OK en 6/6, batería sin la exigencia | Reclasificar como «de forma» el borrado que deja la lista vacía o bajo su mínimo (o exigir la regla de esquema también en esos casos) + regresión `r03_…` |
| 4 | baja | Documento 0 §2.3 y §3 (fila S-12) + LEEME («el sello da S-12 en toda mutación de valor que respeta la forma») | La promesa S-12 es **falsa para `estado`**: `hash_del_sello` excluye `hash_sello` y `estado` («cambia en la vida del sello»), de modo que VIGENTE→CADUCADO (dentro del enum del esquema, respeta la forma) deja el sello VÁLIDO y sin S-12. El veneno de la batería nunca produce un valor del enum, así que `sello_valor_que_respeta_la_forma_da_S12` no puede verlo. La conducta es defendible y por capas (el encargo la ve con E-16), pero la documentación no declara la excepción como hace con las demás | `hallazgo_4_revision_v060_sello_estado_sin_S12.py` (fija el comportamiento real; el defecto está en el texto) | exit 1 solo en la pata de documento | Declarar la excepción de `estado` en §2/§3 y en el LEEME, y fijar el comportamiento con el caso (estado alterado → sin S-12; E-16 en el encargo) |

Ninguno de los cuatro hallazgos invalida el defecto_01 ni la batería en su conjunto: la corrección de
V-15 es real, mínima y correctamente fijada, y las cuatro promesas siguen demostradas para los
validadores de mensajes (sobre, encargo, informe, sello) en el espacio que la batería sí cubre.

## Sospechas investigadas y descartadas (sin camino dañino)

- **`autoria_c` mal formada** en el contexto del informe: `diversidad()` la trata como «desconocida»
  (None) y la comprobación C-11 desaparece **en silencio** (sonda S-4c: el informe sigue válido). Sin
  camino práctico: el Orquestador valida la configuración con `_autoria_ok` (orquestador.py:289-290) y
  el Documento 0 no promete nada para esa clave (no la muta). Sugerencia menor: distinguir «ausente»
  (None, legítimo) de «mal formada» (C-01) en una pieza futura.
- **Granularidad de los predicados** `_afecta_sobre`/`_afecta_encargo`: en algunas ramas cuentan como
  «afecta» mutaciones que el validador no consulta (p. ej. cualquier clave bajo
  `clases_ratificadas[perfil]` del sobre, o bajo `resultado_politica.controles` del encargo). Con la
  semilla y los fixtures actuales no dispara; con otros fixtures (varias clases ratificadas por
  perfil, `controles` con claves opcionales) podría producir FALLA espurias. Es fragilidad de prueba,
  no de producto: conviene saberlo antes de tocar los fixtures.
- **Comentario impreciso en `_calendario_afecta`** («quitar un festivo… no puede discrepar con lo
  declarado»): quitar un festivo del intervalo consultado SÍ puede disparar S-10 (la recomputación
  cuenta más días hábiles) y, vía encargo, E-16. Sin consecuencia: la exigencia de regla se aplica por
  la rama de lista no vacía, que no consulta el predicado, y quitar un festivo fuera del intervalo no
  cambia nada.
- **NaN/infinitos en el sello**: aunque `_validar_sello` no tiene un barrido propio de no finitos como
  `validar_sobre`, toda mutación de valor deja el hash sin cuadrar → S-12, y las comparaciones con NaN
  son inertes pero el sello ya viene rechazado. Cubierto.
- **`hash_del_sello` excluye `estado`** (diseño): cubierto por el hallazgo 4; el consumidor siempre
  comprueba el estado (E-16) y `estado_sello` falla cerrado (cualquier problema → CADUCADO).

## Veredicto

Pieza sólida: el defecto_01 es real y está bien corregido (no-vacuidad demostrada contra la línea de
V0.53; sin sobre-estrechar), la batería es determinista y su contabilidad cuadra, y los seis
validadores no dieron ningún contraejemplo en las sondas. Antes de cerrar la pieza: incorporar las
correcciones 1-3 (batería + regresiones r01-r03) y la corrección 4 (texto del Documento 0/LEEME), y
actualizar `revision.md` con este informe.

*Scripts de la revisión (en la raíz de `marcoC/`): `sondas_revisor_v060.py`,
`hallazgo_1_revision_v060_no_muta_dimensionar.py`, `hallazgo_2_revision_v060_contexto_sc3_sello.py`,
`hallazgo_3_revision_v060_minitems_borrados.py`,
`hallazgo_4_revision_v060_sello_estado_sin_S12.py`.*
