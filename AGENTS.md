# Instrucciones para agentes (Astra, Codex y otros)

Este repositorio lo trabajan dos agentes: Claude (Anthropic) y Astra (OpenAI). Las reglas son las mismas para los dos.

1. **Protocolo del proyecto:** lee `CLAUDE.md`. Aunque el nombre sea de Claude, sus reglas (kit de contexto por fase, números solo de la configuración, esquema primero, mock antes que API, líneas base de pruebas, `./tools/check_all.sh` en verde para cerrar) obligan a cualquier agente.
2. **Flujo de trabajo:** planificar → implementar → probar → QA, con una skill por fase en `.agents/skills/`. Visión de conjunto: `.docs/knowledge/02_flujo-de-trabajo.md`. Cada tarea vive en su ticket, `.docs/tickets/T-NN/` (el ID de la deuda técnica), con su `handoff.md` si cambia de manos. La QA la hace siempre el agente que no implementó.
3. **Espacio de trabajo `.docs/`:** al empezar, lee `.docs/README.md` (índice y reglas), `.docs/memoria/LEEME.md` y los índices de la memoria. Escribe solo en tu carpeta de memoria (`.docs/memoria/astra/` en tu caso; créala la primera vez con `.docs/scripts/memoria.sh astra …`) y en `.docs/memoria/compartida/` con entradas nuevas firmadas por ti. Nunca edites la carpeta de otro agente. Lo de cada día va al diario (`.docs/diario/`).
4. **Lo repetible se automatiza:** antes de hacer algo a mano, mira `.docs/scripts/`; si vas a repetirlo, escríbelo como script ahí (sobre `.docs/scripts/common.sh`, con los secretos solo en `.env`) y apúntalo en la tabla de `.docs/README.md`. La próxima vez se ejecuta y no se gastan los mismos tokens.
5. **Fuente de verdad del sistema:** `sistema_global/constitucion/Constitucion_Global.md`. Pendientes y decisiones aplazadas del operador: `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`.
6. **Idioma:** español, en documentos, commits y mensajes al operador.
7. **Repositorio público:** nada de secretos ni de datos personales o financieros del operador.
