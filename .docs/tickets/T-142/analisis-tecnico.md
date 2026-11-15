# T-142 · Análisis técnico

## Causa raíz o motivo

El Bloque A emite por opción un `paquete_para_bloque_B` (Anexo B del Documento 0 de A) y el Bloque B V2.1 recibe peticiones CT-B-01 con `origen: BLOQUE_A` (Anexo B.1 del Documento 0 de B), siempre a través del Broker (R5 de B, 2.2 y R4 de A). Faltaba ese paso del Broker: elegir las opciones, escribir la petición con los nombres de B y decir qué ámbito del universo de B corresponde a cada ámbito de A. Fase 6 del plan de `CLAUDE.md`. Aprobado por el operador el 15-11-2026: el lado que necesita el Bloque A lo hace Claude; el Bloque B V3 (C-37), Astra.

## Evidencia

- Anexo B.1 del Documento 0 del Bloque B: los campos de `peticion`. §6.1: CT-B-01 es Broker → COORD. 7.4 F0: admisibilidad con `AMBITO_INDETERMINADO`.
- `bloque_b/11_Ejecutor/README.md` (3): la petición fija el ámbito con `objeto.clave_universo` o, desde el Bloque A, con `paquete_para_bloque_B.x_clave_universo`; el ejemplo `bloque_b/11_Ejecutor/ejemplos/peticiones/peticion_redes_bloque_a.json` pone las dos.
- `bloque_b/11_Ejecutor/bloque_b/orquestacion.py`: `_admisibilidad` solo rechaza un `BLOQUE_A` sin paquete. En `_f0`, si el Director no da una clave válida, se usa `objeto.clave_universo` o la primera de `ambitos_ejemplo.yaml`. El Director simulado (`mock_respuestas._plan`) lee `x_clave_universo` y, si no la hay, busca por las tres primeras palabras del nombre del ámbito. Por eso una petición sin clave nunca termina en `AMBITO_INDETERMINADO`. Comprobado con la sonda de `cadena_a_b.py`: USD/JPY sin clave → admitida como `divisas_materias_primas`.
- Documento 0 del Bloque A, 7.7 y Anexo B (CT-04): la vuelta prevista es la decisión `ENVIADA_A_BLOQUE_B` y un `resultado_comunicado` `{opp_id, texto}`. No hay campo para el resultado del Bloque B.

## Implementación

- **Archivos nuevos**
  - `bloque_a/11_Ejecutor/bloque_a/cadena_b.py`: el papel del Broker, sin modelo. `opciones_enviables`, `construir_peticion`, `clave_universo_b`, `errores_entrada_b`, `ct04_desde_respuesta_b` y `ErrorCadenaB`, con su código. No importa nada del Bloque B.
  - `bloque_a/11_Ejecutor/tests/test_t142_cadena_b.py`: 30 pruebas. Leen como datos el Documento 0 de B (B.1), su ejemplo de petición y sus ámbitos, y el Documento 0 de A (CT-04).
  - `.docs/scripts/cadena_a_b.py`: de punta a punta con las dos CLI simuladas, ejecutadas como `python -m bloque_x.cli` desde el `11_Ejecutor` de la copia. Las CLI instaladas apuntan al árbol principal.
- **Archivos cambiados**
  - `bloque_a/11_Ejecutor/config/por_defecto.yaml`: sección `cadena_b` `[PROPUESTO]`, con `correspondencia_ambitos` (cuatro filas) y `peticion` (nivel, prioridad, perfil del marco).
  - `bloque_a/11_Ejecutor/README.md`: estructura y una sección «Cadena con el Bloque B».
  - `docs/incidencias.md`: INC-T142-01.
  - `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`: una fila en la sección 6.
  - `.docs/README.md`: fila del script.
- **Bloque B:** no se ha tocado. Su ejecutor admite las peticiones tal como están.

### Decisiones (detalle y porqué en INC-T142-01)

1. **Campos.** Exactamente los de B.1, sin el sobre común, como los ejemplos del Bloque B.
   - El encargo va tal cual, validado antes contra `$defs/entrada_bloque_B` del esquema del Bloque A. Se le añade una sola extensión `x_`, la clave.
   - Lo que A no da lleva los valores neutros de B.1, desde la configuración: AUTO, NORMAL y `MINORISTA_UE_DEFECTO`.
   - Lo demás va vacío o nulo. `pet_ref_broker` = `<run_id>/<opp_id>`.
2. **Correspondencia.** Por el símbolo del indicador de seguimiento, que identifica el ámbito en el universo de A. Solo las cuatro filas que encajan por tipo y contenido.
3. **Falla cerrado.** Sin fila, la petición no se construye. La sonda (`exigir_correspondencia=False`, solo en el script) existe para documentar qué hace el Bloque B V2.1 sin clave.
4. **Broker en la cadena.** Envía las opciones `ENVIAR_A_BLOQUE_B`. Ante PT30 autoriza la opción que recomienda el Bloque B, hasta `--max-autorizaciones`; no responde consultas bloqueantes.
5. **Vuelta.** Un CT-04 por opción enviada, con `ENVIADA_A_BLOQUE_B` y el texto con los identificadores de B. Se aplica con `bloque-a decision`, que escribe en F3 (`decision_broker`) y en F5 (RET) y avisa por CT-22. La pregunta de si A debe aprender de los veredictos de B queda para el operador.

### Desviaciones del plan

- El plan proponía, sin correspondencia, mandar la petición sin clave y que B contestara lo que prevé su Documento 0. No se hace por defecto: el Bloque B V2.1 no contesta `AMBITO_INDETERMINADO`, sino que elige un ámbito él mismo (evidencia arriba). Se falla cerrado en el Broker y queda una nota para el Bloque B V3 en INC-T142-01. CA-1, segunda mitad: la opción sin correspondencia termina con `SIN_CORRESPONDENCIA_AMBITO`, sin clave inventada. Lo que haría B con ella queda medido por la sonda.
- `objeto.tipo_objeto_sugerido` va nulo: una tabla `tipo_opcion` → tipo de objeto sería otra decisión sin respaldo, y B.1 admite null.

### Límites conocidos

- La correspondencia cubre los universos de ejemplo. Con universos reales hay que rehacer la tabla.
- El ámbito de A puede ser más estrecho que el de B: AUD/USD frente a las divisas de materias primas frente al euro. B lo trata como pista y encuadra el suyo.
- El Bloque B V2.1 no valida el `paquete_para_bloque_B` contra un esquema. Por eso lo valida el Broker, con el esquema de A.
- La vuelta es texto: el Evaluador de A no usa el resultado de B.
- En el simulado, el veredicto de B es VIGILAR, sin candidatos prioritarios. Es mecanismo, no calidad.

## Comandos exactos para probarlo

```bash
# desde la raíz de la copia
cd bloque_a/11_Ejecutor && /home/user/robotinvestor/.venv/bin/python -m pytest -q tests/test_t142_cadena_b.py   # 30
/home/user/robotinvestor/.venv/bin/python tests/goldens_ct.py                                                     # coinciden
cd ../.. && /home/user/robotinvestor/.venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <carpeta nueva> --sonda-sin-correspondencia   # código 0
```
