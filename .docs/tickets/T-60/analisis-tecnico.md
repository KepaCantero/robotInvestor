# T-60 · Análisis técnico

## Causa raíz o motivo

El trabajo de los agentes estaba disperso:
- la memoria, en `memoria/`;
- el flujo, en docs/;
- las tareas, en una carpeta prevista, docs/tareas/, que nunca llegó a usarse;
- los traspasos, en la memoria.

Además, había tareas repetidas a mano en cada sesión: el gate, las suites del marco, las entradas de memoria, el commit y el push. Repetirlas así cuesta tokens y abre la puerta a hacerlas distinto cada vez.

## Evidencia

- En las sesiones del 8 y 9 de noviembre se ejecutaron a mano, decenas de veces, las mismas secuencias: gate rápido, comprobación de referencias, commit con autor y líneas finales, y push; también la creación de entradas de memoria y el marcado de las sustituidas.
- Al convertir en script las suites del marco, `pruebas_marco.sh` encontró que `pruebas_nivel_cambio_t18.py` y `pruebas_reduccion_t43.py` no figuraban en la lista «Cómo se ejecuta» del LEEME, así que quien siguiera el LEEME no las habría ejecutado.

## Implementación

**Archivos movidos (con historial):**
- memoria/ → `.docs/memoria/`;
- docs/flujo_de_trabajo.md → `.docs/knowledge/02_flujo-de-trabajo.md`;
- la plantilla del plan → `.docs/tickets/_plantilla/README.md`.

**Archivos nuevos:**
- `.docs/README.md`;
- las plantillas de ticket;
- `.docs/knowledge/01_que-es-el-robot-investor.md` y `.docs/knowledge/03_scripts-y-ahorro-de-tokens.md`;
- en `.docs/scripts/`: `common.sh`, `env.ejemplo`, `gate.sh`, `pruebas_marco.sh`, `nuevo_ticket.sh`, `diario.sh`, `memoria.sh` y `commit.sh`.

**Archivos cambiados:**
- las cuatro skills (rutas del ticket, `handoff.md`, uso de los scripts, sección «Scripts: lo repetible, automatizado» y cierre con diario);
- `AGENTS.md` y `CLAUDE.md`;
- el briefing;
- `.docs/memoria/LEEME.md`;
- `tools/refs_vivas.py`, que ahora revisa `.docs/` y trata `T-NN` y `AAAA` como marcadores de posición;
- `tools/refs_allowlist.txt`;
- `.gitignore`, que ignora `.docs/scripts/.logs/`;
- el LEEME del marco, con las dos suites que faltaban.

**Límites conocidos:**
- Los scripts son de bash y Python. En Windows hace falta Git Bash o WSL.
- `commit.sh` añade por defecto todo lo cambiado (`git add -A`); para limitarlo, se le pasan las rutas.

**Comandos para probarlo:**
- `.docs/scripts/gate.sh`
- `.docs/scripts/pruebas_marco.sh`
- `.docs/scripts/nuevo_ticket.sh` con un ticket de prueba (`T-999`), en una copia del repositorio.
