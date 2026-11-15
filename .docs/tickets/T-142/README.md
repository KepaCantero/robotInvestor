# T-142 · Bloque A → B: cadena de encargos

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | Lado A: `bloque_a/11_Ejecutor/bloque_a/` (un módulo que construye la petición CT-B-01 a partir de una opción con su `paquete_para_bloque_B`) y sus pruebas; `.docs/scripts/cadena_a_b.py` (de punta a punta, con las dos CLI). El Bloque B no se cambia salvo que falte algo imprescindible para recibir el encargo (y entonces, cambio mínimo, con su prueba en B) |
| Planifica · implementa · QA | claude · un agente · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-15: «La parte de Astra que necesitamos la haremos nosotros y el resto del bloque B que lo haga Astra» |
| Deuda técnica | T-142 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (Fase 6 del plan de `CLAUDE.md`) |

## Lo que ya hay

- El Bloque A emite en su paquete JSON (`06_Plantillas_entregables/Esquema JSON - Paquete de oportunidades - V5.0.json`) un `paquete_para_bloque_B` por opción (Anexo B del Documento 0 de A).
- El Bloque B V2.1 recibe peticiones CT-B-01 con `origen: BLOQUE_A` y ese paquete (`bloque_b/11_Ejecutor/bloque_b/orquestacion.py`; ejemplo `bloque_b/11_Ejecutor/ejemplos/peticiones/peticion_redes_bloque_a.json`), siempre a través del Broker (Documento 0 de B, R5 y §1).
- El Bloque B tiene su propio universo de ámbitos (`bloque_b/11_Ejecutor/config/ambitos_ejemplo.yaml`, con `clave_universo`); el del A es de símbolos (`bloque_a/11_Ejecutor/config/universo_ejemplo.csv`).

## Plan

1. **Petición CT-B-01 desde A** (papel del Broker, en código, sin modelo): de una opción del paquete de A que el Broker decide enviar (`siguiente_paso` de envío al B), construir la petición con `origen: BLOQUE_A`, el `paquete_para_bloque_B` tal cual, `objeto`, `tipos_activo_admitidos`, `horizontes`, `preguntas`, `marco_invertibilidad` y `nivel`, con los nombres del Documento 0 de B (§6.1, CT-B-01). Ningún campo inventado; lo que A no da, lo que dice el Documento 0 de B para el valor por defecto, o vacío.
2. **Correspondencia de ámbitos** (`[PROPUESTO]`): cómo pasa el Broker del ámbito de A a la `clave_universo` de B. Propuesta: una tabla en la configuración del lado A (`x_clave_universo`), y si no hay correspondencia, la petición va sin clave y B responde lo que su Documento 0 prevea (aclaración o `AMBITO_INDETERMINADO`): falla cerrado, sin inventar.
3. **De punta a punta** (`.docs/scripts/cadena_a_b.py`, sin importar código de un bloque en el otro: el B se ejecuta por su CLI `bloque-b analizar --json`): ciclo mock de A → opciones enviables → peticiones CT-B-01 → B mock → paquete de análisis de B validado contra su esquema (`bloque_b/06_Plantillas_entregables/Esquema JSON - Paquete de análisis de mercado - Bloque B - V2.0.json`) → resumen de la cadena.
4. **Vuelta**: qué hace A con lo que devuelve B (si el Documento 0 de A prevé un registro de la respuesta del B, aplicarlo; si no, documentarlo como incidencia).

## Criterios de aceptación (binarios)

1. CA-1: cada petición construida por A la admite el ejecutor de B (sin `MensajeInvalido` ni rechazo de admisión) cuando hay correspondencia de ámbito, y una sin correspondencia termina en lo que el Documento 0 de B prevé, sin inventar la clave.
2. CA-2: `cadena_a_b.py` con el cliente simulado en los dos bloques termina con al menos un paquete de B ENTREGADO y válido contra su esquema.
3. CA-3: pruebas nuevas en A (la petición, campo a campo, frente al Documento 0 de B) y, si se toca B, en B; las líneas base de A y B no bajan; gate 12/12.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · PLANIFICADO · claude · plan
- 2026-11-15 · EN QA · claude · implementado y probado: `bloque_a/cadena_b.py` (petición CT-B-01, correspondencia `[PROPUESTO]` que falla cerrado, CT-04 de vuelta), 30 pruebas, `.docs/scripts/cadena_a_b.py` (1 entrega de B válida; la sonda muestra que B V2.1 sin clave elige un ámbito él mismo); el Bloque B no se ha tocado; INC-T142-01; sin commit (lo hace la sesión coordinadora)
- 2026-11-15 · CERRADO · QA r01 APTO (revisor nuevo sin contexto); hallazgos (H-01 a H-03 medios, H-04 a H-06 bajos) en T-147
