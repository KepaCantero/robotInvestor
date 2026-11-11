# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque G

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_g/propuesta_claude.md`, la propuesta de Claude para el Bloque G (ejecución, órdenes de protección, libro y conciliación). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Va después de las revisiones de D, E y F (`.docs/diseno/README.md`).

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): P15 y P20; §2 (fila de G); §3 (plano de control); §6 (niveles de autonomía y L1 manual); §7 (plan de largo plazo y vehículo fiscal); §8 (órdenes de protección, conciliación y tolerancias, kill-switch);
   - los Documentos 0 de G: `sistema_global/documentos_0/V0.08_G_ejecucion_y_conciliacion.md`, `sistema_global/documentos_0/V0.15_CT-G-14_y_conciliacion.md`, `sistema_global/documentos_0/V0.18_Orden_de_entrada_viva.md`, `sistema_global/documentos_0/V0.20_Cartera_real_y_euros.md` y `sistema_global/documentos_0/V0.21_T-12_Reduccion_parcial.md`;
   - las filas T-01, T-14, T-30 y T-31 de la deuda técnica.
2. **Juzga cada decisión de la propuesta** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - ejecutar con criterio de coste (tipo de orden, hora, escalonado, divisa) y dónde está la frontera con «opinar sobre el mercado»;
   - medir cada ejecución y devolver el coste real a I;
   - operar fondos (suscripción, reembolso, traspaso, liquidación);
   - los dos libros (operativo por cartera y fiscal por persona);
   - la tabla por cartera y el ciclo de seis pasos;
   - el orden de pruebas antes del dinero real.
3. **Busca en particular:**
   - riesgos nuevos que introduce cada cambio (por ejemplo, órdenes escalonadas que dejan una posición a medias sin stop, o dinero en tránsito de fondos que E o F cuentan dos veces);
   - si la regla fiscal citada (vender primero lo más antiguo, aplicada a la persona) está bien descrita; no la resuelvas tú, márcala para el asesor (P-06);
   - si el ejemplo de 200 operaciones y 0,10 % por operación es razonable como orden de magnitud;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte**, con su efecto en el coste, en la seguridad y en el trabajo de construirlo.
5. **Responde a las seis preguntas** del §9 de la propuesta, en una o dos frases cada una, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas.

Después:
- añade una línea al diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque G" astra`);
- haz commit en develop con `.docs/scripts/commit.sh`, sin tocar ningún bloque ni el marco común;
- avisa al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
