# Notas de deuda — V0.61 (catálogo de códigos)

- **Tabla T (pendientes de deuda técnica):** una fila RESUELTA y dos nuevas (el fichero `Deuda_tecnica.md`
  del repositorio no viaja en el ZIP —hallazgo 6 de la revisión—: estas notas resumen su contenido para
  V0.61).
  - **T-60 «Catálogo de códigos al día» — RESUELTO en V0.61.** El módulo `validador/catalogo_codigos.py`
    (CATALOGO con 282 entradas: las 281 que aparecen en el código más E-06 retirada), las funciones
    `codigos_en_el_codigo` (con ast), `sitios_de_emision`, `prefijos_del_leeme` y `como_markdown`, la
    batería `pruebas_catalogo_codigos.py` (23 comprobaciones: las 18 de la pieza y las cinco regresiones
    r01 a r05 de la revisión) y el registro de prefijos del LEEME completado
    (R, K, CL, PE, DI, MG, RL) mantienen el catálogo al día.
  - **T-61 (nueva, sin resolver): choque real O-00.** En el Orquestador es el rechazo de un instante
    inválido o anterior al último (y la envoltura de excepciones al ejecutar o comprobar); en el Diario es
    la marca de una operación que lanza una excepción no recogida por `@_seguro`. Mismo código, significados
    distintos. Se anota en `COLISIONES_ADMITIDAS` con su explicación y en `CHOQUES_REALES` (r01 exige
    textos distintos por módulo: la revisión, hallazgo 1, corrigió el catálogo, que daba el mismo texto en
    los dos); renombrar el del Diario exigiría migrar el diario ya escrito (decisión del operador,
    Fase 2).
  - **T-62 (nueva, sin resolver): choque real O-01.** En el Orquestador es un rechazo genérico de la
    operación pedida —la revisión (hallazgo 4) matiza la descripción: el «condiciones_entrada.resto_parcial:
    solo CANCELAR» fue solo el caso que motivó la anotación, de ~71 caminos de emisión—; en G es «el
    intermediario no da precio para el instrumento o el instante es ilegible».
    Se anota en `COLISIONES_ADMITIDAS` y en `CHOQUES_REALES`; renombrar el de G exigiría revisar pruebas y
    pantallas (decisión del
    operador, Fase 2). La aceptación de la pieza prohíbe renombrar: los dos choques quedan documentados sin
    tocar ningún código.
- **Tabla D (decisiones del operador):** ninguna fila nueva. La pieza no añade valores de configuración ni
  de parámetros: el catálogo es documentación, no configuración, y el módulo no está en `MODULOS_ESQUEMA`.
- **Observación para el revisor** (no es deuda): el efecto del catálogo es una clasificación por contrato
  del módulo (RECHAZA por defecto; REDUCE para las reglas de F que aprueban con menos cantidad; BLOQUEA
  para las reglas que vetan o bloquean el flujo; AVISO para los avisos del Orquestador, los de H y las
  reglas Q que solo emiten ADVERTENCIA —Q-01 y Q-10—; INFORMA para las que preparan una acción); la parte
  verificable la vigila la batería (r02 y r03). Los textos provienen del mensaje del código, del docstring,
  del comentario de la
  línea que lo emite, del nombre de los casos inválidos de su batería o del LEEME, con la fuente citada en
  el docstring del módulo; los códigos genéricos declarados con `"familia": True` (O-00, O-01 y O-02 del
  Orquestador) llevan un texto de nivel familia que no cita un caso con su ruta (r04); `"desde"` queda a
  None en todas las entradas.
