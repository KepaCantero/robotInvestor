# Sistema global del Robot Investor

Esta carpeta reúne lo que gobierna el sistema por encima de los bloques A, A Forex y B: la Constitución global, el código de referencia de la Fase 1 («marco común de C») y los documentos de diseño y seguimiento de cada pieza. Es independiente de `bloque_*/`: no toca su corpus ni sus gates.

| Carpeta | Contenido |
| --- | --- |
| `constitucion/` | `Constitucion_Global.md`: la Constitución global (V0.3 vigente; el historial de git conserva la V0.1). Es la fuente de verdad: si algo de esta carpeta la contradice, vale la Constitución. |
| `marco_comun_c/` | Código de referencia de la Fase 1 en Python (V0.42; V0.37 a V0.41 las hace GLM en paralelo desde V0.36). Recorrido completo con datos simulados: detección, encargo, sobre, comparación, dimensionado, propuesta, control de riesgo, autorización, ejecución, vigilancia y cierre. Determinista, sin LLM, sin intermediario real. Su `LEEME.md` describe módulos, códigos y pruebas. |
| `documentos_0/` | Un Documento 0 por pieza, nombrado por la versión del código que la introdujo (problema, diseño, reglas, revisión independiente y límites). |
| `seguimiento/` | Deuda técnica (D-xx del operador, T-xx técnicas), briefing de arranque para retomar el trabajo en otra conversación y cuestionario de decisiones del operador. |

## Cómo comprobar el código

Requiere Python 3 con `jsonschema`. Desde `sistema_global/marco_comun_c/`:

```bash
for f in pruebas/ejecutar_pruebas.py pruebas/pruebas_*.py; do python3 "$f" | tail -1; done
```

Cada una de las 35 suites acaba con «TODAS LAS PRUEBAS PASAN».

## Historial

Cada versión del código (V0.1 a V0.36 y V0.42) es un commit propio con la fecha y hora de su entrega, de modo que `git log -- sistema_global/marco_comun_c` muestra cómo se construyó pieza a pieza. Los documentos se editaron en Claude Docs y se exportaron a Markdown el 5 de noviembre de 2026; las fechas y menciones de su cabecera quedan como texto y el diagrama de estados del Orquestador no se exporta.

## Siguiente paso

T-27 está cerrada entera (V0.28 a V0.32). Lo siguiente es preparar la fijación de las versiones 1.0.0 de los contratos (T-06), que espera a que el operador ratifique lo pendiente, o seguir con la deuda técnica que no depende del operador: T-44 y T-33 (con GLM), el resto de T-03, T-18 y T-52. T-17 (confianza y costes en D) se cerró en V0.35 y T-22 (controles de la §8 en F) en V0.36, con importes propuestos (D-11 y D-31). Lo que depende del operador está en la tabla D de `seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`.
