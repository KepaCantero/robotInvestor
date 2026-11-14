# .docs · espacio de trabajo de los agentes

Todo lo que Claude, Astra y las personas del equipo necesitan para trabajar en el repositorio sin depender del historial de una conversación. Estructura propuesta por Kepa el 9-11-2026, adaptada al proyecto (en español y con commit, porque se comparte entre personas y agentes).

**¿Chat nuevo o recién llegado?** Empieza por el relevo más reciente: `.docs/tickets/_relevo/2026-11-11_relevo_nuevo_chat.md` (estado del proyecto, dónde está cada cosa y cómo se trabaja).

| Carpeta | Para qué sirve | Quién escribe |
| --- | --- | --- |
| `.docs/README.md` | Este índice y las reglas | Cualquiera, con cuidado |
| `.docs/tickets/` | Una carpeta por ticket (`T-NN`, el mismo ID que en la deuda técnica): `README.md` (estado, alcance, aceptación y plan), `analisis-tecnico.md` (causa raíz, evidencia e implementación), `pruebas.md`, `qa.md` y, solo si el trabajo cambia de manos, `handoff.md`. Plantillas en `.docs/tickets/_plantilla/` | El agente que lleva el ticket; la QA, el revisor |
| `.docs/diario/` | Diario por mes (`AAAA-MM.md`), la entrada más reciente arriba | Quien trabaja ese día |
| `.docs/scripts/` | Scripts de trabajo: todo lo que se hace más de una vez | Cualquiera |
| `.docs/knowledge/` | Documentos de incorporación, estáticos y numerados | Cualquiera, al cambiar el modo de trabajo |
| `.docs/diseno/` | Propuestas de diseño de cada bloque y sus revisiones independientes, para discutir con el operador antes de construir; no se implementan hasta que él cierra el diseño | El agente que propone y el que revisa |
| `.docs/plantillas_operador/` | Plantillas en blanco que el operador rellena fuera del repositorio: ficha de restricciones, inventario del patrimonio, preguntas al asesor fiscal y carta de instrucciones. Nunca se suben rellenas | El agente que las propone; el operador las rellena en privado |
| `.docs/memoria/` | Memoria indexada de los agentes: `compartida/` y una carpeta por agente | Cada agente en la suya y en `compartida/` |

## Reglas

1. **Nunca se borra nada de `.docs/`.** Lo viejo se marca (ticket `CERRADO`, entrada de memoria `sustituida`) y se conserva.
2. **Nunca se hace commit de secretos.** Los tokens viven en `.env`, en la raíz del repositorio (está en `.gitignore`), y solo los carga `.docs/scripts/common.sh`. Plantilla: `.docs/scripts/env.ejemplo`.
3. **Nada personal ni financiero de ningún usuario** (el repositorio es público y cada usuario tiene su propia copia, D-47).
4. **Lo repetible se automatiza.** Antes de hacer algo a mano, mira `.docs/scripts/`. Si vas a hacer algo que se repetirá (comprobar, probar, crear, publicar, migrar), escríbelo como script, guárdalo ahí y apúntalo en la tabla de scripts. La próxima vez se ejecuta el script y no se gastan otra vez los mismos tokens.
5. **Los traspasos van dentro del ticket** (`handoff.md`), no en la raíz ni en la memoria.
6. **Carpetas basura conocidas** (no se leen, no se citan, no se suben): `.venv/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.docs/scripts/.logs/`, `estado_bloque_a/`, `entregables/`.

## Scripts

| Script | Qué hace |
| --- | --- |
| `.docs/scripts/fechas_evidencia_b.sh` | Diagnóstico temporal T-64 del cierre de objeciones. Devuelve 1 si hay discrepancias con los casos esperados. |
| `.docs/scripts/common.sh` | Base de todos: modo estricto, raíz del repo, carga de `.env`, `requiere_var`, `requiere_cmd`, Python del proyecto |
| `.docs/scripts/gate.sh` | Gate rápido (`--core`) o completo (`--completo`), con el log en `.docs/scripts/.logs/` |
| `.docs/scripts/pruebas_marco.sh` | Todas las suites del marco común de C, leídas del LEEME; avisa de las que falten en él |
| `.docs/scripts/leeme_marco.py` | Comprueba que el LEEME del marco común de C coincide con el disco: lista de ejecución y número de comprobaciones de cada batería (se ejecutan todas) |
| `.docs/scripts/prueba_refs_vivas.py` | Prueba del gate `refs-vivas` (`tools/refs_vivas.py`): revisa las carpetas `revisores/`, entiende citas con argumentos y sufijos de línea (T-65, H-11) |
| `.docs/scripts/nuevo_ticket.sh` | Crea `.docs/tickets/T-NN/` desde la plantilla |
| `.docs/scripts/diario.sh` | Añade la entrada de hoy al diario del mes, arriba |
| `.docs/scripts/memoria.sh` | Crea una entrada de memoria, la indexa y, con `--sustituye`, marca la anterior |
| `.docs/scripts/commit.sh` | Gate, commit (autor y líneas finales desde `.env`) y push a `develop` |
| `.docs/scripts/medir_consumo_a.py` | Llamadas y tokens de entrada por agente de un ciclo simulado del Bloque A (cliente mock; `--config` para activar más perfiles) |
| `.docs/scripts/medir_consumo_b.py` | Llamadas y tokens de entrada por agente de un análisis simulado del Bloque B (cliente mock), para comparar variantes de prompts, caché o modelos |
| `.docs/scripts/comparar_disenos_a.py` | Bloque A V5 frente a V6 (T-101) en los mismos ciclos con el cliente simulado: llamadas y tokens por agente, caché y coincidencia de la selección. Solo flujo y consumo, no calidad |
| `.docs/scripts/banco_medida.py` | Banco de medida (T-94): el titular (hoy, el Bloque A en backtest) frente a azar y momento, con los mismos datos y fechas de corte; prerregistro sellado, exceso frente a la cesta de la clase con rango y veredicto, y coste. Pruebas en `.docs/scripts/pruebas_banco_medida.py` |
| `.docs/scripts/commit_limpio.sh` | (`--borrar=ruta` quita un fichero que la tarea elimina.) Commit desde una copia limpia de HEAD con solo las rutas de la tarea (pruebas del marco, su LEEME y gate completo allí), para cuando el árbol tiene cambios a medias de otras tareas; sube las copias probadas |
| `.docs/scripts/preparar_entorno.sh` | Crea `.venv` con Python 3.12 y las versiones fijadas en `tools/requisitos_entorno.txt` (T-96); `--comprobar` compara lo instalado con el fichero y nombra lo que difiere |
| `.docs/scripts/cola_astra.py` | Cola de Astra (`.docs/tickets/_relevo/cola_astra.md`): la siguiente tarea y lo que se podría perder (marcada HECHA sin entregable, entregable sin marcar, borradores, EN CURSO abandonado, cambios sin subir); `--json` para automatizar. Pruebas en `.docs/scripts/pruebas_cola_astra.py` |
| `.docs/scripts/registro_experimentos.py` | Registro de experimentos (T-99): prerregistro sellado, intentos y resultados en un fichero encadenado por huellas (por defecto «.docs/experimentos/registro.jsonl», que nace con el primer experimento); dice si un resultado es adoptable. El banco de medida lo usa. Pruebas en `.docs/scripts/pruebas_registro_experimentos.py` |
| `.docs/scripts/pruebas_borradores_contratos.py` | Pruebas de los borradores de esquema de `.docs/diseno/contratos/` (CT-G-08 0.4.0 y CT-G-24 0.1.0) |
| `.docs/scripts/qa_rama.sh` | QA de una rama de otro agente: commits, archivos, si se fusiona por avance rápido, copia limpia y pruebas de cada pieza tocada contra el código de la rama |
| `bloque_a/11_Ejecutor/tests/goldens_ct.py` | Goldens de los contratos CT del Bloque A (T-114): sin opciones comprueba (1 si algo difiere); `--update --motivo "…"` re-congela y lo anota en `tests/goldens/REGISTRO.md`. Se ejecuta desde `bloque_a/11_Ejecutor` |
| `.docs/scripts/evidencias_plan_a.py` | Plan de pruebas del Bloque A (T-116): sin opciones comprueba el mapa `tests/mapa_plan_pruebas.json` contra el plan y la suite; `--ejecutar` ejecuta las pruebas citadas y regenera `docs/evidencias_pruebas_bloque_a.md`; `--pb PB-NN` repite una fila. Con el Python del `.venv` |

## Diario: formato

```markdown
## AAAA-MM-DD — <título> (<autor>)

**Resultado.** Qué quedó hecho.
**Causas y hallazgos.** Qué se descubrió y por qué pasó lo que pasó.
**Correcciones.** Qué se arregló.
**Operaciones y siguiente.** Commits, despliegues, y lo próximo.
```

## Diario, memoria y tickets: qué va dónde

- **Ticket:** todo sobre una tarea concreta, de principio a fin.
- **Diario:** qué pasó cada día, en orden cronológico; enlaza a los tickets.
- **Memoria:** lo que conviene saber siempre (reglas, lecciones, estado), indexado para leer solo lo necesario.
- **Knowledge:** cómo se trabaja aquí, para quien llega nuevo.
