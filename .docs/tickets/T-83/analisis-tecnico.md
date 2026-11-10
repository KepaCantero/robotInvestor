# T-83 · Análisis técnico

## Causa raíz o motivo

D-45 (Constitución V0.6, §9 punto 4, ratificada el 2026-11-09) pide que todo parámetro tenga un valor por defecto prudente **con su justificación escrita** y que llegue **con su pregunta del cuestionario** (D-44, §2 punto 4). En el marco solo había el valor y, a veces, una marca `[PROPUESTO]`/`[RATIFICADO]` en un comentario. Un comentario no lo puede leer el asesor de configuración, no dice por qué ni qué preguntar, y nada impedía añadir un parámetro sin justificar (PC3-07 de la V0.67, PARCIAL).

## Evidencia

- `sistema_global/documentos_0/V0.67_Integracion_del_kit_2_de_GLM.md`, fila PC3-07: «hay valor y marca, no hay justificación ni pregunta como datos».
- Antes de este ticket no existía ningún registro con justificación ni pregunta de un parámetro. `git grep -n "pregunta" HEAD -- sistema_global/marco_comun_c/validador` solo encuentra el campo `pregunta` del modo CONSULTA (T-80), que no tiene nada que ver.
- Las marcas de los comentarios mezclan dos espacios de nombres. «[PROPUESTO, D-29]» en `k_licencias_admitidas` es la D-29 de la tabla de pendientes de la deuda técnica (licencias de K). «(D-22, D-27, P-17)» en `o_dias_sequia` son decisiones de la Constitución. Por eso las fuentes llevan el documento delante.
- Algunos comentarios de `CONFIG_DEFECTO` están desplazados:
  - el de `anulaciones_veto_mes` (T-50) está en la línea de `tolerancia_tipo_k_rel`;
  - el del Contradictor exigido (T-48) está en la línea de `matriz_autonomia`.

  No se corrigen, porque son de otro módulo y la tarea no los toca. El análisis del fuente los atribuye a la clave de su línea, y como todos dicen `[PROPUESTO]`, coinciden con el estado documentado.

## Implementación

- **Archivos:**
  - `sistema_global/marco_comun_c/validador/parametros_doc.py` (nuevo): tabla `DOC` de solo lectura con 85 registros (estado, fuente, justificación, pregunta) y las funciones `doc`, `faltan`, `por_estado`, `preguntas_pendientes`, `defectos` y `tablas_del_codigo`. Solo importa la biblioteca estándar al cargarse; las tablas del código se importan al llamar.
  - `sistema_global/marco_comun_c/pruebas/pruebas_parametros_doc_t83.py` (nueva): 62 comprobaciones.
  - `sistema_global/marco_comun_c/LEEME.md`: título, cabecera V0.72, dos filas de la tabla, «Cómo se ejecuta» y el punto «Comprobado en».
  - `sistema_global/documentos_0/V0.72_Valores_por_defecto_documentados.md` (nuevo).
- **Recuento por estado:**
  - 4 `RATIFICADO`: `o_dias_sequia`, `n_dias_embudo`, `i_meses_juicio_sombra` y `nivel_autonomia`;
  - 77 `PROPUESTO`;
  - 4 `TECNICO`: `version_config`, `contradictor_desactivado_motivo`, `politica_f` y `divisas_cotizacion`.
- **Decisiones:**
  - **Fuera de `MODULOS_ESQUEMA`.** La huella del esquema describe lo que el sistema hace y guarda; la justificación y la pregunta son texto para personas. Con el módulo dentro, cada corrección de redacción exigiría versión de esquema y migración sin cambiar ninguna decisión. La relación con los valores la vigila la batería en los dos sentidos.
  - **`POLITICA_DEFECTO` se documenta límite a límite.** Por eso `CONFIG_DEFECTO["politica_f"]` es un contenedor `TECNICO` (la batería comprueba que es el mismo objeto y que ninguno de sus límites es técnico).
  - **`nivel_autonomia` es `RATIFICADO`.** La Constitución (§6, «Matriz de autonomía», D-45) ratifica L1 como valor por defecto de cualquier copia nueva, y `{}` significa L1. Los demás valores de la autonomía (matriz vacía, umbral L2, promoción) siguen `PROPUESTO`.
  - **`apalancamiento_max` y `exposicion_max_pct` siguen `PROPUESTO`.** Citan D-45 («sin apalancamiento» por defecto), pero el docstring de F declara todos sus límites `[PROPUESTO]`, y en la duda se deja `PROPUESTO`.
  - **`autoria_c` y `autoria_contradictor` son `PROPUESTO`** y no técnicos, porque la deuda (D-25, D-06) los deja al operador.
  - **Regla de `TECNICO`:** solo en `CONFIG_DEFECTO` y sin ningún número dentro, porque los docstrings de `parametros.py`, `k_calidad.py`, `orquestador.py` y `control_f.py` declaran sus valores numéricos de partida `[PROPUESTO]`. La batería lo comprueba.
  - **Preguntas también para los `RATIFICADO`.** D-45 pide una pregunta para todo parámetro, y los cambios posteriores pasan por el mismo cuestionario (D-46). Las preguntas no llevan nombres de código (sin «_») ni se repiten.
  - **Fuentes con el documento delante.** «Constitución D-45», «Deuda D-29», «Deuda T-75», «V0.67». Además de evitar la confusión de espacios de nombres, esto impide que el catálogo de códigos (`EXPRESION_CODIGO`, que busca textos enteros como «D-29» en `validador/`) los tome por códigos de error.
  - **La batería copia el `Arnes`** (solo `chk`) en lugar de importarlo de `pruebas_orquestador.py`. Ese módulo inserta la carpeta `validador` real al principio de `sys.path`, y eso estropearía los subprocesos que apuntan a una copia con `T83_VALIDADOR`.
- **Desviaciones del plan:**
  - se añadió `defectos()` (forma de la propia tabla) y `tablas_del_codigo()`;
  - una mutación más: quitar una pregunta a un `PROPUESTO`.
- **Límites conocidos:**
  - Constantes sueltas con marca fuera de las tres tablas, sin documentar aquí. Para una continuación de T-83:
    - `MAX_SALTO_S`, `MAX_DESFASE_S`, `MAX_SIN_CONTRASTE_S` y `TOPE_SIN_CONTRASTE_S` de `reloj.py`;
    - `FACTOR_DISCREPANCIA` y `VIGENCIA_MAX` de `validar_sobre.py`;
    - `REFERENCIA_EFECTIVO` de `comparador.py`;
    - `TIPOS_EVENTO_RESTRINGIDOS` y `VETOS_ANULABLES`;
    - `PRIORIDAD_AVISO` y `NIVEL_BAJO` del Orquestador;
    - el detalle de `mandatos.MANDATOS_DEFECTO`;
    - las subclaves de `aprobacion`, `avisos`, `kill_switch` y `promocion_nivel`, documentadas como un todo en su clave.
  - Las tres claves de `CONFIG_OBLIGATORIA` (`perfiles_activos`, `clases_ratificadas`, `apalancamiento_permitido`) no tienen valor por defecto a propósito. Eso choca con la letra de D-45 («una copia nueva funciona desde el primer día»). Es una observación para T-57, no se decide aquí.
  - La batería solo comprueba la forma de cada justificación y de cada pregunta. Su contenido debe revisarlo una persona; la QA y la sesión T-57 son el sitio.
  - La justificación de los valores de K, D, H y E sale del uso en el código y de los tickets que los consolidaron (T-25, T-17, T-21), no de un documento de diseño con el porqué original.
- **Comandos exactos:**
  - `cd sistema_global/marco_comun_c && ../../.venv/bin/python -I pruebas/pruebas_parametros_doc_t83.py`
  - `.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c`
  - `.docs/scripts/pruebas_marco.sh`
  - `.docs/scripts/gate.sh --completo`

## Ronda r02: corrección de la QA r01

El operador reabrió la tarea tras la QA r01 NO APTO (`qa.md`). Se tocan solo `validador/parametros_doc.py`, la batería, el LEEME del marco, el Documento 0 V0.72 y este ticket. Ningún valor del código cambia.

| Hallazgo | Causa raíz | Corrección | Prueba (falla con HEAD `dd96e19`, pasa ahora) |
| --- | --- | --- | --- |
| H-01 (media) | Apliqué «en la duda, PROPUESTO» sin buscar el apalancamiento en el registro de decisiones del §15: la D-16 («no habilitados hasta que el operador lo decida, no antes de la Fase 3») sí fija el valor | `apalancamiento_max` de F pasa a RATIFICADO, con fuentes «Constitución D-16», «Constitución D-45» y «Deuda D-12», sin pregunta y con `cerrada_por` = «Constitución D-16» (campo nuevo: un RATIFICADO que la Constitución no deja preguntar todavía). El mismo criterio alcanza al apalancamiento del mandato, que pasa a RATIFICADO. `exposicion_max_pct` sigue PROPUESTO (el operador puede bajarla, no subirla), pero cita D-16 y su pregunta no ofrece pasar del total. `instrumentos_permitidos` cita D-16 (derivados y CFD cerrados). El LEEME dice ahora «los seis que ella fija» | `apalancamiento_ratificado_por_D16_sin_pregunta_*`, `la_D16_esta_ratificada_y_cierra_el_apalancamiento`, `ninguna_pregunta_pendiente_ofrece_apalancamiento`, `exposicion_cita_D16_*`, `los_ratificados_son_los_de_la_constitucion` (6) y la mutación `apalancamiento_otra_vez_propuesto` |
| H-02 (media) | Documenté las compuestas como un todo, con una pregunta, y `faltan()` solo miraba el primer nivel | Seis subtablas (`SUBTABLAS`): `aprobacion` (5 campos, incluidos `canales`, con segundo factor y D-19, y `enfriamiento_tras_perdida_dia_eur`, D-18), `avisos` (4), `kill_switch` (1), `promocion_nivel` (1), `mandatos` (7 campos comunes a las tres carteras) y `referencias` (2). La clave compuesta queda con `detalle` (la subtabla), sin pregunta y con el estado de sus campos. `politica_f` usa el mismo mecanismo con `detalle` = `POLITICA_DEFECTO` y pasa de TECNICO a PROPUESTO por agregación. `faltan()` recorre los campos (`SIN_DOCUMENTAR`, `NO_EXISTE`, `NO_ES_COMPUESTA`). Los mapas con una misma decisión por entrada (por cartera con valor simple, o por divisa, instrumento o perfil) siguen como un todo: una entrada nueva la delata `valor_documentado` (H-05) | `aprobacion_pregunta_cada_valor`, `aprobacion_canal_*_D19`, `aprobacion_perdida_*_D18`, `mandatos_*`, `compuestas_documentadas_campo_a_campo`, `toda_compuesta_de_campos_fijos_va_campo_a_campo`, `cobertura_CONFIG_DEFECTO.*`, `faltan_detecta_un_campo_*`, `faltan_detecta_una_compuesta_que_deja_de_serlo` y las mutaciones `subclave_nueva_en_aprobacion`, `subclave_nueva_en_promocion` y `campo_nuevo_en_el_mandato` |
| H-03 (baja) | Leí el horario como un permiso, sin seguir `motivos_espera` en el Orquestador | `aprobacion.horario_utc`: «Fuera de 07:00 a 21:00 UTC no se prohíbe aprobar, pero hay que esperar 30 minutos, y una cartera en L3 actúa como en L2». La pregunta es en qué horario se puede atender el sistema para aprobar sin espera | `aprobacion_horario_es_espera_y_no_prohibicion` (comprueba también el texto del código y que los 30 minutos son `enfriamiento_min`) |
| H-04 (baja) | Redacción | `revision_max_dias`: «¿Cuánto tiempo como máximo puede pasar sin revisar una inversión abierta?». `rangos_tipo_cambio_eur`, como confirmación: «¿Te vale el rango recomendado…?». `referencias.rentabilidad_anual_pct`: dice que es un marcador, no un valor prudente, que T-37 lo traerá de los datos y que el §7 pide un índice real. `mandatos.benchmark_ref` cita el §7 (efectivo solo si lo elige el operador) | `revision_pregunta_por_el_maximo`, `rangos_de_cambio_se_preguntan_como_confirmacion`, `referencia_dice_que_es_un_marcador_contra_el_7` |
| H-05 (baja) | Nada ataba el texto al valor que justifica | Campo `valor_documentado` en todo registro simple (bloque `_VALOR_DOCUMENTADO`, en forma JSON) y `desfasados(tablas)`, que compara con `valor_actual()`. Cambiar un valor obliga a revisar su texto y actualizarlo | `valores_documentados_al_dia`, `valor_documentado_igual_al_del_codigo_en_cada_registro`, `desfasados_detecta_*` y las mutaciones `valor_cambiado_en_parametros` (`k_min_observaciones` 20 → 40) y `valor_cambiado_en_politica` (`max_posiciones` 10 → 25) |
| H-06 (baja) | `preguntas_pendientes()` no reutilizaba la validación de `faltan()` | Valida las tablas como `faltan()` (`_comprueba_tablas`) y lanza ValueError si la documentación no cuadra con el código (algo sin documentar, documentado que no existe o con el valor cambiado): un cuestionario incompleto o que pregunta por otro valor no se presenta | `preguntas_pendientes_falla_cerrado_como_faltan` (clave ausente, `{}`, clave nueva, valor cambiado y una lista) y `preguntas_pendientes_con_el_codigo_de_hoy` |

- **Recuento tras la r02:** 105 registros (85 claves y 20 campos):
  - 6 RATIFICADO;
  - 94 PROPUESTO, siete de ellos claves compuestas sin pregunta propia;
  - 5 TECNICO: `version_config`, `contradictor_desactivado_motivo`, `divisas_cotizacion`, `mandatos.version` y `referencias.benchmark_ref`.

  `preguntas_pendientes()` da 87 preguntas.
- **Decisiones de la r02:**
  - **`cerrada_por` en lugar de una pregunta.** El encargo pedía quitar la pregunta que ofrecía activar el apalancamiento. Un RATIFICADO sin pregunta solo vale con una decisión ratificada de la Constitución que lo cierre, y esa decisión debe estar en su fuente. Cuando el operador pueda decidirlo (Fase 3), se le pondrá su pregunta y se quitará `cerrada_por`.
  - **`referencias.benchmark_ref` es TECNICO.** La configuración del Orquestador exige que sea igual al benchmark del mandato, así que la decisión se pregunta una sola vez, en el mandato.
  - **Los campos de `mandatos` se documentan una vez para las tres carteras.** Su valor es `{cartera: valor}` y su pregunta dice «cada cartera». `faltan()` exige que las tres tengan los mismos campos.
  - **`_VALOR_DOCUMENTADO` repite los valores del código.** No es un número a mano en el sentido de la regla 2, porque no decide nada: es la copia con la que se compara para saber si el texto sigue hablando del valor actual.
  - **`matriz_autonomia` sigue PROPUESTO.** Revisada con el criterio de H-01: L1 por defecto está ratificado, pero qué carteras puede autorizar la matriz en L2 no lo fija ninguna decisión. `exige_contradictor_en` sigue PROPUESTO, porque D-35 ratifica varios análisis en N3, no el Contradictor en N2; su pregunta lo dice.
- **Límites que quedan:**
  - Lo ya anotado: las constantes sueltas con marca fuera de las tres tablas y `CONFIG_OBLIGATORIA`.
  - **El docstring de `control_f.py` dice «Todos los límites son valores de partida [PROPUESTO]»,** y el apalancamiento ya es RATIFICADO. No se toca, porque es otro módulo. Habría que matizarlo cuando se toque F. La comprobación de los docstrings solo exige que declaren sus valores de partida.
  - **Nada en el código impide hoy un instrumento derivado en un mandato** con `instrumentos_permitidos` None. D-16 lo cierra en la Constitución, y el universo de la Fase 1 son pares de divisas al contado (`perfiles_activos`). Es una observación para la deuda de F o de SC-1, no de esta tarea.
  - La batería entera no arranca con el módulo de HEAD, porque usa la API nueva. La prueba de que cada regresión falla sin la corrección es `.docs/tickets/T-83/r02_contra_head.py`.
- **Comandos de la r02:**
  - `.venv/bin/python -I .docs/tickets/T-83/r02_contra_head.py` (por defecto contra HEAD; admite otro commit);
  - `cd sistema_global/marco_comun_c && ../../.venv/bin/python -I pruebas/pruebas_parametros_doc_t83.py`;
  - `.docs/scripts/pruebas_marco.sh` y `.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c`.
