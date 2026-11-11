# 04 · Arrancar un chat nuevo de Claude

Para quien trabaje en el Robot Investor con Claude y empiece una conversación nueva: se pega este mensaje como **primer mensaje**, tal cual. Claude se conecta al repositorio, lee el relevo más reciente y se pone al día sin depender del historial de otro chat.

Hace falta una sesión de Claude que pueda trabajar con repositorios de GitHub (la del entorno de código). Si el relevo más reciente cambia, se actualiza la ruta del paso 2.

```text
Hola, Claude. Trabajo en el Robot Investor, un proyecto que ya está avanzado. Antes de nada, ponte al día así:

1. Añade a esta sesión el repositorio de GitHub KepaCantero/robotInvestor (rama develop), clónalo y haz `git pull origin develop`.
2. Lee, en este orden: `CLAUDE.md`, `.docs/README.md`, el relevo más reciente (`.docs/tickets/_relevo/2026-11-11_relevo_nuevo_chat.md`), `.docs/memoria/LEEME.md` y los `INDICE.md` de `.docs/memoria/compartida/` y `.docs/memoria/claude/`. No leas el repositorio entero: lo demás, solo cuando la tarea lo pida.
3. Respeta las reglas del §4 del relevo. El repositorio es público: sin secretos ni datos personales, y nunca escribas mi nombre en ficheros. No toques bloques, marco común ni Constitución sin mi autorización. `bloque_b/` está congelado y de `.docs/` no se borra nada.
4. Háblame en español y de usted.
5. Al terminar, resúmeme en cinco líneas dónde estamos y pregúntame qué hacemos hoy. No retomes ninguna tarea por tu cuenta.
```
