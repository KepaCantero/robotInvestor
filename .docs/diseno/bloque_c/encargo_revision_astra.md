# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque C

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_c/propuesta_claude.md`, la propuesta de Claude para el Bloque C (análisis en profundidad de un candidato y sobre CT-G-02): un solo Analista con un kit por perfil, cuatro papeles de IA (Lector, Analista, Analistas independientes y Contradictor de otro proveedor), y coordinación, cifras, validación y combinación en código. **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Es la tercera revisión del orden natural (A, B, C, D, E, F, G, H): va después de las de A y B, porque sigue su misma pauta.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): P3, P6, P12, P16, P18 y P19; §2 (fila de C y los doce perfiles); §3 (verificación diversa y lectores aislados); §5 (sobre por capas, clases Q, S y K y reglas de comparabilidad); §7 (escalera de verificación); §9 (calibración, torneo, aspirante frente a titular); §10 (economía del análisis);
   - el Documento 0 del marco común: `sistema_global/documentos_0/V0.01_Marco_comun_C_y_sobre_CT-G-02.md`, y los validadores de `sistema_global/marco_comun_c/validador/` que tocan a C (`validar_sobre.py`, `validar_encargo.py`, `validar_contradictor.py`).
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - un Analista con kits frente a un equipo por perfil;
   - los cuatro papeles y sus modelos por nivel;
   - la tasa base calculada por el Motor en clase Q y la vista exterior primero;
   - la combinación de N3 por regla y la resolución de objeciones por regla;
   - los niveles N0 a N3 y la tabla por cartera;
   - el orden de construcción (C-DIV, C-IDX y C-FON, después C-RV) frente a lo que dice la Fase 2;
   - la frontera con B (C no repite lo que B contrastó).
3. **Busca en particular:**
   - si un solo Analista con kit puede alcanzar la profundidad de un especialista en tipos de activo muy distintos (por ejemplo, renta fija frente a criptoactivos);
   - si las estimaciones de consumo se sostienen;
   - qué datos de K y módulos del Motor hacen falta antes de que C-DIV funcione de verdad;
   - conflictos con la Constitución o con los contratos CT-G-01, CT-G-02 y CT-G-03.
4. **Propón lo que falte**, con su efecto en precisión y en consumo.
5. **Responde a las seis preguntas** del §9 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque C" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
