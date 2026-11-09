# T-53 · Propuestas de arquitectura y de agentes para el operador

El detalle, con las evidencias y las citas, está en `revisores/arquitectura.md` (PA-01 a PA-21). Aquí va la lista que se presenta al operador, ordenada según cuándo conviene hacer cada cosa. La columna «Decide» separa lo que debe decidir el operador [OP] de las mejoras técnicas [TEC].

## Diagnóstico en una frase

El Bloque A que se ejecuta ya es, en gran parte, código determinista: selección, puertas, validación, resolución y seguimiento. Llama a un modelo de IA en unos 8 tipos de llamada. En cambio, la documentación describe 25 agentes, con prompts de unos 593 000 tokens en total. Varios de esos agentes no se invocan nunca: el Motor, el Documentador para el Motor y el mantenimiento C4. En otros la respuesta no cambia nada: el dictamen del Orquestador técnico se ignora, al Analizador se le pide que no cambie la selección y el Evaluador solo redacta. Los 12 analistas son núcleo + perfil en el texto, pero en la ejecución reciben las mismas 6 señales genéricas.

## Antes de conectar A (Fase 1)

| N.º | Propuesta | Beneficio | Decide |
| --- | --- | --- | --- |
| PA-01 | En la Fase 1, solo el perfil de divisas activo; los otros 11 tipos, «no construidos» hasta que haga falta | Un ciclo pasa de 12 tipos a 1; unos 220 000 tokens de prompt menos por ciclo | OP |
| PA-06 | De 25 agentes a unos 6 papeles de IA: Analista de perfil, Prospectiva, Contradictor, un Sintetizador (Analizador y Redactor juntos), respondedor N0 y, si demuestra que aporta, Curador. El resto, código o servicio común | La documentación coincide con lo que se ejecuta; menos coste fijo y menos superficie que auditar | OP |
| PA-07 | Prompts compuestos de núcleo común + perfil corto (unos 3 000–4 000 tokens cada parte), con los números en la configuración, y cada recorte validado como aspirante frente al actual | Unos 180 000 tokens fijos por ciclo se quedan en 25 000–30 000 (−80/85 %), con menos contradicciones | TEC (con validación aspirante/titular) |
| PA-05 | Contradictor de otro proveedor de IA. Ve la evidencia, no el razonamiento del Analista. Decide una regla, no el propio Analista, si una objeción queda resuelta, y su veredicto tiene efecto | El único control interpretativo deja de ser decorativo | OP (coste y proveedor) |
| PA-03 | Torneo de preguntas fijas: cada par × H1/H2/H3, respondidas por todos los agentes, por una referencia simple y por la tasa base. Muestra efectiva corregida por la correlación entre pares. Hitos H5 a 12 meses o menos, como pide la Constitución | Muestra útil en semanas, calibración por agente y certificados creíbles | TEC (OP el alcance) |
| PA-12 | Medir los aciertos frente a «no hacer nada» (la liquidez en euros), no frente a una cesta G10 | El historial responde a la decisión real («¿entro o me quedo en euros?») | OP |
| PA-09 | Backtests con IA anonimizados por defecto; lo anterior a la fecha de corte del modelo no cuenta para certificados ni aprendizaje | Evita aprender de «aciertos» que son memoria del modelo | TEC |
| PA-10 | El aprendizaje automático solo puede endurecer; lo que relaja va por la ruta única de cambios | Conformidad con P8 y §9.6 | OP |
| PA-04 | Datos desde K, con las 6 fichas FX que faltan, y la puerta GC1 de divisas aplicada por código antes de llamar a la IA | Especialización real y menos entrada a la IA | TEC |
| PA-02 | Adaptador de A a los contratos globales CT-G, su ficha CT-G-17 y su batería de conformidad. Falta además un contrato global para encargar trabajo a A (enmienda) | A se puede conectar y sustituir sin tocar su interior | OP (enmienda) + TEC |
| PA-08 | Presupuesto en euros por encargo y por día, con los precios por modelo | Se aplica el §11 y se mide si A compensa su coste (P17) | TEC (OP el tope) |
| PA-11 | Valores por defecto con su justificación y su pregunta del cuestionario; lo que es del usuario pasa a su perfil | Cumple D-44, D-45 y D-47 | TEC |

## Pueden esperar

| N.º | Propuesta | Fase |
| --- | --- | --- |
| PA-13 | A deja de hacer el informe visual para el usuario (lo hacen el Broker y la consola N) | 1 o 2 |
| PA-14 | Medir en cada ciclo cuántas decisiones cambia cada agente (ablación determinista, sin coste en tokens) | 1–2 |
| PA-15 | Una sola evaluación común para A, B y el marco (SC-4 e I) | 1–2 |
| PA-16 | Extraer el Motor de A como SC-3 | 1–2 |
| PA-17 | Auditor de otro proveedor, por muestreo y con el lazo cerrado | 2 |
| PA-18 | Radar tecnológico (está en la Constitución y no en el D0) | 2 |
| PA-19 | API de lotes y salida estructurada | 1 (modo sombra) |
| PA-20 | Compartir el análisis de A entre copias, de forma voluntaria | 2+ |
| PA-21 | Que el Analista dé también su propia probabilidad, para medir su calibración | 1, con PA-03 |

## Decisiones pequeñas pendientes de la corrección

- **INC-T53-01:** si las tres mejores son del mismo clúster y no hay alternativa a ≤ 10 puntos, ¿se publican las tres declarando la concentración (como hoy) o solo dos?
- **CS-09:** valor en UC de un cálculo PLAN_STD (0,1 en la configuración; el Anexo A sugiere 1). Encaja con PA-08.
- **INC-T53-05:** la regla de «confianza» del paquete frente a la barra del Redactor.
- **INC-T53-03:** umbral de revocación de certificados (0,12, sin respaldo en el Anexo A). Para la sesión T-57.

## Estado tras T-66 (10-11-2026)

El operador pidió aplicar las propuestas oportunas y dar por terminado el Bloque A.

**Aplicadas en el ejecutor** (`.docs/tickets/T-66/`):
- PA-01;
- PA-03 (muestra efectiva);
- PA-05 (sin otro proveedor);
- PA-09;
- PA-10;
- PA-14;
- PA-21.

**Aplazadas, con su destino** (deuda técnica T-67):
- PA-02 y PA-03 (torneo);
- PA-04 (con T-54);
- PA-06 y PA-07 (validación con llamadas reales);
- PA-08;
- PA-13 y PA-15 a PA-20.

Lo que decide el operador está en T-57: PA-05 (proveedor), PA-08 (tope), PA-11 y PA-12.
