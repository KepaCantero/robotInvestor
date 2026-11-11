# Encargo a Astra: revisión independiente de la propuesta de diseño de SC-9 (fiscalidad)

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/sc9_fiscalidad/propuesta_claude.md`, la propuesta de Claude para el servicio común SC-9 (fiscalidad y costes). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común. Tampoco es asesoramiento fiscal: lo que revises de las reglas es para que el asesor sepa qué comprobar.

Va después de la revisión del Broker Personal y antes de la enmienda 4: es la decimoquinta de la lista.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): fila de SC-9 en §3; §7 (rentabilidad mínima, freno a la rotación, vehículo fiscal y peso fiscal por cartera); §10 (fiscalidad codificada); P17; P-06 y P-28;
   - el libro fiscal por persona de la propuesta de G (`.docs/diseno/bloque_g/propuesta_claude.md`);
   - E4-08 y E4-16 de la enmienda 4 (`.docs/diseno/enmienda_4/propuesta_claude.md`).
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - las reglas como datos versionados, firmados y con casos de prueba;
   - las cuatro cifras de SC-9 y el cálculo por persona;
   - las seis palancas y su orden;
   - que SC-9 calcule y señale, pero no proponga operaciones;
   - que la sombra pague impuestos con las mismas reglas;
   - qué pasa si falta la firma;
   - el orden por fases.
3. **Busca en particular:**
   - errores en la tabla de reglas del §4 (escala del ahorro de 2026, recompra, compensación, traspasos y ETF, dividendos, divisas) y si las fuentes bastan;
   - el estado de la cuenta Financia Europa (Real Decreto-ley 29/2026), que estaba pendiente de convalidación el 11-11-2026;
   - si la regla de recompra afecta a la cartera de trading de divisas;
   - si el ejemplo de diferir el impuesto del §2 está bien calculado y presentado;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.**
5. **Responde a las siete preguntas** del §10 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta de SC-9" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
