# Encargo a Astra: revisión independiente de la propuesta de enmienda 4

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/enmienda_4/propuesta_claude.md`, una propuesta de cuarta enmienda a la Constitución con veinte puntos (E4-01 a E4-20): mejora gobernada, auditoría por bloque, biblioteca y mapa de conocimiento, Motor, comunicación, Estratega macro, Investigador cuantitativo, pauta común de A, B y C, Broker con seis papeles, Perfilador, planificación patrimonial, tope de gasto, plan de largo plazo en paralelo, modo sin IA y brújula. **Es solo pensamiento de diseño: no cambies la Constitución ni ningún bloque.**

Es la penúltima revisión de tu lista, después de las de los bloques y los servicios comunes (relevo, §0 bis), porque muchos puntos tocan esos diseños. Después solo queda la pasada de coherencia.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Relee la Constitución (`sistema_global/constitucion/Constitucion_Global.md`) completa con estas preguntas del operador en mente: ¿es automejorable?, ¿se audita cada bloque?, ¿tienen todos un documentador o buscador de fuentes?, ¿tiene cada bloque todo el conocimiento que necesita?, ¿faltan bloques o agentes?, ¿hay motores especializados y pueden ahorrar cálculo?, ¿falta cálculo complejo?, ¿se comunican bien los bloques?, ¿hay algo al tanto de la macro y la geopolítica?, ¿debe el Broker ser multiagente?, ¿debe haber un perfilador?, ¿se nos escapa algo?
2. **Juzga cada punto (E4-01 a E4-20)** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías.
3. **Busca en particular:**
   - contradicciones con principios vigentes (P2, P8, P11, P13, P15, P17, P19, D-21, D-23, D-33) y con el tope de bloques activos;
   - riesgos de seguridad del circuito de mejora (E4-01) y del perfilador (E4-15);
   - si el plan de largo plazo en paralelo (E4-18) es realista para la Fase 1;
   - si la afirmación sobre planes de pensiones (E4-16) está bien planteada; no la resuelvas tú, márcala para el asesor (P-06);
   - lo que la propuesta no haya visto.
4. **Revisa la tabla «Lo que no se propone»:** ¿hay algo descartado que sí debería entrar, o algo propuesto que debería descartarse?
5. **Responde a las siete preguntas** del final de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la enmienda 4" astra`), el commit con `.docs/scripts/commit.sh` sin tocar la Constitución ni ningún bloque, y el aviso al operador.

## Reglas

- No cambies `sistema_global/constitucion/` ni ningún bloque.
- Repositorio público: sin secretos ni datos personales.
