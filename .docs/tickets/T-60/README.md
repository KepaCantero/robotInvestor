# T-60 · Espacio de trabajo .docs (propuesta de Kepa)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | Repositorio: `.docs/`, skills y documentación de trabajo |
| Planifica · implementa · QA | claude · claude · el operador (cambio de organización del trabajo; no toca código del sistema) |
| Aprobación del operador | Aprobada el 2026-11-09: «Aplica los cambios que me dice Kepa por favor» |
| Deuda técnica | T-60 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Adoptar la estructura de trabajo que Kepa usa con agentes: un único espacio `.docs/` con índice y reglas, tickets, diario, scripts y conocimiento, y la regla de convertir en script todo lo repetible para no gastar los mismos tokens dos veces.

## Alcance

- Entra:
  - `.docs/README.md`, con el índice y las reglas;
  - `.docs/tickets/`, con su plantilla;
  - `.docs/diario/`;
  - `.docs/scripts/`, con `common.sh`, `env.ejemplo` y seis scripts;
  - `.docs/knowledge/` (01 a 03);
  - la memoria, que se traslada a `.docs/memoria/`;
  - las skills, `AGENTS.md`, `CLAUDE.md`, el briefing y el gate `refs-vivas`, actualizados.
- No entra: código del sistema ni la Constitución.

## Diseño

Se adapta la propuesta de Kepa en tres puntos:

1. **En español**, por la regla del operador, aunque Kepa propone el conocimiento en inglés.
2. **Con commit.** En el trabajo de Kepa, `.docs/` no se sube; aquí se comparte entre personas y agentes por GitHub, así que la regla pasa a ser «nunca se hace commit de secretos».
3. **Las claves de ticket son las `T-NN` de la deuda técnica**, para no tener dos numeraciones.

Los traspasos pasan de la memoria a `handoff.md` dentro de cada ticket.

## Criterios de aceptación (binarios)

1. CA-1: la estructura existe con el índice y las reglas de `.docs/README.md`.
2. CA-2: cada script funciona en una copia de prueba y falla con un mensaje claro ante un mal uso.
3. CA-3: ninguna referencia rota (`refs-vivas`) y el gate en verde.
4. CA-4: las skills, `AGENTS.md` y `CLAUDE.md` apuntan a las rutas nuevas e incluyen la regla de automatizar en scripts.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `nuevo_ticket.sh`: crea, rechaza duplicado, rechaza ID mal formado, avisa si no está en la deuda | nominal, fallo cerrado | CA-2 |
| `diario.sh`: crea el mes y pone la entrada más reciente arriba | nominal | CA-2 |
| `memoria.sh`: crea carpeta e índice, sustituye, exige `--autor` en compartida, valida el tema | nominal, fallo cerrado | CA-2 |
| `pruebas_marco.sh`: ejecuta las suites y detecta las que falten en el LEEME | integración | CA-2 |
| `gate.sh` y `tools/refs_vivas.py` | integración | CA-3 |

## Scripts

Crea los seis de `.docs/scripts/` (tabla en `.docs/README.md`).

## Registro

- 2026-11-09 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-09 · CERRADO · claude · estructura montada y probada; `pruebas_marco.sh` encontró dos suites que faltaban en el LEEME del marco (corregido)
