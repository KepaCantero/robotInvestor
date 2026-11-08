# Instrucciones para agentes (Astra, Codex y otros)

Este repositorio lo trabajan dos agentes: Claude (Anthropic) y Astra (OpenAI). Las reglas son las mismas para los dos.

1. **Protocolo del proyecto:** lee `CLAUDE.md`. Aunque el nombre sea de Claude, sus reglas (kit de contexto por fase, números solo de la configuración, esquema primero, mock antes que API, líneas base de pruebas, `./tools/check_all.sh` en verde para cerrar) obligan a cualquier agente.
2. **Flujo de trabajo:** planificar → implementar → probar → QA, con una skill por fase en `.agents/skills/`. Visión de conjunto: `docs/flujo_de_trabajo.md`. La QA la hace siempre el agente que no implementó.
3. **Memoria:** al empezar, lee `memoria/LEEME.md` y los índices. Escribe solo en tu carpeta (`memoria/astra/` en tu caso; créala la primera vez siguiendo el LEEME) y en `memoria/compartida/` con entradas nuevas firmadas por ti. Nunca edites la carpeta de otro agente.
4. **Fuente de verdad del sistema:** `sistema_global/constitucion/Constitucion_Global.md`. Pendientes y decisiones aplazadas del operador: `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`.
5. **Idioma:** español, en documentos, commits y mensajes al operador.
6. **Repositorio público:** nada de secretos ni de datos personales o financieros del operador.
