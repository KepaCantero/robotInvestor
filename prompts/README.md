# Prompts de implementación — robotInvestor

Prompts listos para pegar en sesiones de **Claude Code** abiertas en la raíz del repo:

```bash
cd ~/robotInvestor && claude
```

`CLAUDE.md` se auto-carga en cada sesión (reglas, trampas, líneas base de tests) —
los prompts solo definen el alcance de cada sesión.

## Orden de ejecución

| # | Archivo | Qué hace | Modelo recomendado |
|---|---|---|---|
| 00 | `00_ENTORNO.md` | Verifica/instala venv, dependencias y MCPs; deja las 3 suites en verde | cualquiera |
| 0 | `FASE0_VERIFICADOR_IDS.md` | Verificador de consistencia de IDs del corpus (el prerrequisito de todo) | el más capaz (clase Opus) |
| 1 | `FASE1_FICHAS_V5.md` | Las 21 fichas nuevas del Catálogo (IDX/FON/DER/MON/TCV) | Sonnet |
| 2 | `FASE2_FICHAS_RESTANTES.md` | Fichas DOCUMENTADO restantes por prioridad P0/P1 | Sonnet |
| 3 | `FASE3_GOLDENS_CONTRATOS.md` | Esquemas congelados (goldens) para los contratos CT | el más capaz |
| 4 | `FASE4_PLAN_PRUEBAS.md` | Ejecutar los planes de pruebas y registrar evidencias | Sonnet |
| 5 | `FASE5_MODO_SOMBRA.md` | Primer ciclo real con API, en modo sombra | el más capaz |
| 6 | `FASE6_CADENA_A_B.md` | Encargos A→B y conexión al backtester de robotTrading | el más capaz |

Reglas fijas (van dentro de cada prompt, no las quites): kit de contexto cerrado,
F7/F8/F9 solo por identificador, corpus .md intocable, no mezclar bloques, líneas base
de tests innegociables (58/68/118), decisiones documentadas en `docs/incidencias.md`,
prefijo de commit por fase, avance en `docs/AVANCE.md`, y **cierre de fase =
`./tools/check_all.sh` en verde (12/12)** con cuotas sin subir.

## Entre fases

Verifica TÚ el entregable (el criterio de éxito de cada prompt es un comando que
puedes lanzar). Si algo no cuadra, no sigas de fase: la incidencia se documenta y se
corrige antes. Una fase nueva no arranca con la anterior sin verificar.

## Auditorías puntuales (fuera del orden de fases, tras el 00)

| Archivo | Qué hace | Modelo recomendado |
|---|---|---|
| `VERIF_F6_MEMORIA_APRENDIZAJE.md` | Solo lectura: ¿F6 (memoria de aprendizaje) está implementada en los ejecutores o es solo esquema? Matriz 3 bloques × 5 capacidades con evidencia + INC por hueco | el más capaz |
