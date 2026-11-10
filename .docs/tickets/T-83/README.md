# T-83 · Valores por defecto con su justificación y su pregunta como datos (D-45), marco V0.72

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | sistema_global/marco_comun_c |
| Planifica · implementa · QA | claude · claude · el otro agente (Astra) o un revisor nuevo sin contexto |
| Aprobación del operador | No necesaria: tarea técnica (documentación como datos de valores que ya existen; no cambia ningún valor ni ningún control). Aplica D-45, ratificada el 2026-11-09 |
| Deuda técnica | T-83 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (PC3-07; relacionada con T-57 y PA-11 de T-67) |

## Objetivo

Que cada valor por defecto del marco común de C lleve, como datos que un programa puede leer, su estado (ratificado, propuesto o técnico), su fuente, su justificación y la pregunta del cuestionario guiado (Constitución V0.6, §2 punto 4 y §9 punto 4, D-44 y D-45). Hoy solo hay valor y una marca `[PROPUESTO]` en comentarios (PC3-07 de la V0.67), y el asesor de configuración y la sesión T-57 necesitan la justificación y la pregunta.

## Alcance

- **Entra:**
  - módulo nuevo `sistema_global/marco_comun_c/validador/parametros_doc.py` con la tabla de documentación de las 85 claves de hoy: las 31 de `parametros.PARAMETROS`, las 32 de `orquestador.CONFIG_DEFECTO` y las 22 de `control_f.POLITICA_DEFECTO` (la política de F viaja dentro de `CONFIG_DEFECTO["politica_f"]`, así que cada límite de F se documenta por separado);
  - funciones `doc(clave, tabla=None)`, `faltan(tablas=None)`, `por_estado(estado)` y `preguntas_pendientes()`;
  - batería nueva `pruebas/pruebas_parametros_doc_t83.py`;
  - LEEME del marco (título, cabecera V0.72, tabla y «Cómo se ejecuta») y Documento 0 `sistema_global/documentos_0/V0.72_Valores_por_defecto_documentados.md`.
- **No entra:**
  - cambiar ningún valor, ni `VERSION_PARAMETROS`, ni `version_config`, ni otro módulo del marco;
  - añadir `parametros_doc` a `persistencia.MODULOS_ESQUEMA` (ver «Diseño»);
  - las constantes sueltas con marca `[PROPUESTO]` fuera de las tres tablas (`MANDATOS_DEFECTO` de SC-1 en detalle, `TOPE_SIN_CONTRASTE_S` del reloj, `NIVEL_BAJO`, `VETOS_ANULABLES`, `TIPOS_EVENTO_RESTRINGIDOS`, `REFERENCIA_EFECTIVO`, prioridades de avisos): quedan anotadas en `analisis-tecnico.md` para una continuación;
  - las claves de `CONFIG_OBLIGATORIA` (no tienen valor por defecto a propósito);
  - el cuestionario en sí (lo construye el Broker, T-57/T-59) y la deuda técnica (no se toca en esta tarea).

## Diseño

- **Contratos CT-G y estado persistido:** no cambian. El módulo nuevo no se añade a `MODULOS_ESQUEMA`: la huella del esquema del código describe lo que el sistema hace y guarda; la justificación y la pregunta son texto para personas y para el asesor, y meterlos en la huella obligaría a una versión de esquema y una migración por cada corrección de redacción, sin cambiar ninguna decisión. La relación con los valores la vigila la batería (cobertura en los dos sentidos), no la huella.
- **Forma de cada registro:** `estado` (`RATIFICADO`, `PROPUESTO` o `TECNICO`), `fuente` (tupla de identificadores con el documento delante: «Constitución D-45», «Constitución P-17», «Deuda D-29», «Deuda T-75» o «V0.67» para un Documento 0; con prefijo para no confundir las D-xx de la Constitución con las D-xx de la tabla de pendientes de la deuda técnica, que los comentarios del código mezclan, y para que el catálogo de códigos, que busca textos enteros como «D-29», no los tome por códigos), `justificacion` (una o dos frases) y `pregunta` (lenguaje sencillo, de «¿» a «?»; obligatoria salvo en `TECNICO`, donde es None; también en `RATIFICADO`, porque D-45 y D-46 piden pregunta para todo parámetro y los cambios posteriores usan el mismo cuestionario).
- **Criterio de estado:**
  - `RATIFICADO` solo si una decisión ratificada de la Constitución fija ese valor (`o_dias_sequia`, `n_dias_embudo`, `i_meses_juicio_sombra`, y el nivel por defecto L1 de `nivel_autonomia`, §6 con D-45);
  - `TECNICO` solo para claves sin ningún número dentro que no decide el operador (versión de la configuración, tabla de divisas de cotización de instrumentos, motivo de desactivación vacía y el contenedor `politica_f`, documentado clave a clave);
  - todo lo demás `PROPUESTO`: los docstrings de `parametros.py`, `k_calidad.py`, `orquestador.py` y `control_f.py` declaran todos sus umbrales y límites «de partida [PROPUESTO]», y en la duda, `PROPUESTO`.
- **Números:** ninguno nuevo; no se cambia ningún valor. La batería no escribe valores a mano: compara con las tablas del código.
- **Cómo falla cerrado:** `doc()` lanza `KeyError` si la clave no está documentada o no existe, y `ValueError` si es ambigua entre tablas o la tabla no existe; `por_estado()` lanza `ValueError` con un estado desconocido; los registros son de solo lectura (`MappingProxyType`) y `doc()`/`preguntas_pendientes()` devuelven copias.
- **Decisiones del operador usadas como `[PROPUESTO]`:** ninguna nueva; los `PROPUESTO` ya lo eran y su pregunta es la que hará el cuestionario en T-57.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Alguien añade un parámetro sin documentarlo | El cuestionario no lo pregunta | `faltan()` y la batería fallan; la batería lo demuestra añadiendo uno a una copia del código |
| El estado documentado contradice la marca del comentario | Se pregunta lo ratificado o se da por ratificado lo propuesto | Análisis del fuente (`ast` + `tokenize`) de las tres tablas y de cada `_P[...]`/`PARAMETROS[...]` con marca en `validador/`; mutación de una marca en una copia |
| Una fuente cita un identificador que no existe | Trazabilidad falsa | La batería busca cada identificador en la Constitución, en la deuda técnica o en `documentos_0/` |
| Un texto del módulo casa con la expresión de códigos del catálogo | Falla `pruebas_catalogo_codigos.py` | Fuentes con prefijo («Deuda D-29»); se ejecutan todas las baterías |

## Criterios de aceptación (binarios)

1. CA-1: `faltan()` devuelve `[]` con el código de hoy: toda clave de `PARAMETROS`, `CONFIG_DEFECTO` y `POLITICA_DEFECTO` está documentada y no hay documentación de claves que no existen.
2. CA-2: todo registro tiene un estado válido, una fuente no vacía con identificadores bien formados y existentes, una justificación de una o dos frases; `PROPUESTO` y `RATIFICADO` llevan pregunta en lenguaje sencillo (de «¿» a «?», sin nombres de código), `TECNICO` lleva None y no tiene números dentro; `RATIFICADO` cita una decisión ratificada de la Constitución.
3. CA-3: toda marca `[RATIFICADO]`/`[PROPUESTO]` de los comentarios del código sobre una clave de las tres tablas, o sobre una línea que lee `PARAMETROS[...]`, coincide con su estado documentado.
4. CA-4: añadir un parámetro sin documentar (en `PARAMETROS`, `CONFIG_DEFECTO` o `POLITICA_DEFECTO`) o cambiar una marca de comentario en una copia del código hace fallar la batería; la copia sin cambios pasa.
5. CA-5: `doc()`, `faltan()`, `por_estado()` y `preguntas_pendientes()` se comportan como dice el diseño (copias, errores, orden determinista, valores de partida actuales en las preguntas pendientes).
6. CA-6: no cambia ningún valor ni otro módulo: `VERSION_PARAMETROS`, `version_config`, `MODULOS_ESQUEMA` y la huella del esquema siguen igual; las 61 baterías pasan y `leeme_marco.py` da «SIN DIFERENCIAS».

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `pruebas_parametros_doc_t83.py` · `cobertura_*`, `faltan_vacio_con_el_codigo_de_hoy` | nominal | CA-1 |
| `estado_valido_*`, `fuente_*`, `justificacion_*`, `pregunta_*`, `tecnico_*`, `ratificado_*` | nominal y límite | CA-2 |
| `marcas_*` (análisis del fuente) y `el_analisis_ve_*` (no vacuidad) | regresión | CA-3 |
| `mutacion_*` (copia del código en una carpeta temporal y la batería en un subproceso) | fallo cerrado | CA-4 |
| `doc_*`, `por_estado_*`, `preguntas_pendientes_*`, `faltan_detecta_*` | nominal y fallo cerrado | CA-5 |
| `no_cambia_*`; `.docs/scripts/pruebas_marco.sh` y `leeme_marco.py` | regresión e integración | CA-6 |

## Scripts

- `.docs/scripts/nuevo_ticket.sh` (abrir el ticket).
- `.docs/scripts/pruebas_marco.sh` (todas las baterías del marco).
- `.docs/scripts/leeme_marco.py` (LEEME frente al disco).

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · PLANIFICADO · claude · plan, criterios y plan de pruebas
- 2026-11-10 · EN QA · claude · V0.72 implementada: `parametros_doc.py` con 85 claves (4 RATIFICADO, 77 PROPUESTO, 4 TECNICO); batería nueva con 62 comprobaciones; 61 baterías en verde; sin commit (por indicación del encargo); traspaso en `handoff.md`
