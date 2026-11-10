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
