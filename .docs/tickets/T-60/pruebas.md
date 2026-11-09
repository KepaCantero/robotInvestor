# T-60 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Marco común de C (`.docs/scripts/pruebas_marco.sh`) | 48 en la lista del LEEME (faltaban 2) | 50 entradas ejecutadas en verde: las 49 suites más el ejecutor de casos |
| `tools/refs_vivas.py` | Revisaba `memoria/` y `docs/` | Revisa también `.docs/` y las skills; sin referencias rotas |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `.docs/README.md` con índice, reglas, tabla de scripts y formato del diario |
| CA-2 | En una copia de prueba del repositorio, `nuevo_ticket.sh`: crea el ticket, rechaza el duplicado, rechaza `53` y avisa de `T-999`. `diario.sh`: «Segunda» queda encima de «Primera». `memoria.sh`: crea `astra/` con su índice, sustituye una entrada y marca la anterior en su archivo y en su índice, exige `--autor` en compartida y rechaza el tema `Mal`. `pruebas_marco.sh`: falla con un mensaje claro si falta `jsonschema` y, en el repositorio, 50 de 50 |
| CA-3 | `refs-vivas` en verde y `.docs/scripts/gate.sh` en verde |
| CA-4 | Búsqueda de rutas antiguas (memoria/, docs/flujo_de_trabajo.md, docs/tareas) sin resultados fuera de las entradas de memoria fechadas |

## Gate

`.docs/scripts/gate.sh` con `--completo` antes del commit; el resultado queda en el log de `.docs/scripts/.logs/`.
