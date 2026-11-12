# C-03 · Revisión del diseño de C

Astra · 12-11-2026 · develop 6a6cad5. Revisión documental; no implementación ni QA del marco.

## Resumen (cinco líneas)

1. Apoyo el núcleo común con kits, sin dar por equivalente un kit de texto a un perfil completo y validado.
2. C debe producir análisis reproducibles y revisados; no decidir compra ni tamaño.
3. Reutilizar requiere comprobar todas las dependencias y emitir una respuesta válida al nuevo encargo.
4. Citar evidencia es necesario, pero no suficiente, para resolver una objeción semántica.
5. Los costes y números máximos de llamadas siguen siendo hipótesis; faltan kits y recorridos reales que los sostengan.

## Base y criterio

Leídos el encargo y la propuesta, Constitución P3/P6/P12/P16/P18/P19 y §§2,3,5,7,9,10,14, Documento 0 del marco y validadores de encargo, sobre y Contradictor. Contrastado con `.docs/diseno/decisiones_operador.md`: pauta común, segundo proveedor y largo plazo paralelo están aceptados como rumbo; aún requieren formalización donde cambian la Constitución. No es una revisión ciega: ya conocía la propuesta por la revisión global anterior. Distingo obligaciones vigentes, decisiones de rumbo y sugerencias propias.

## Veredictos

| Decisión | Veredicto | Motivo y cambio propuesto |
| --- | --- | --- |
| Un Analista con kits | DE ACUERDO CON CAMBIOS | Compartir método y ejecución, no eliminar especialización. Cada kit incluye esquema, métodos, fuentes, casos adversos y criterios de abstención; no basta escribir texto para activar otro activo. |
| Cuatro papeles/modelos | DE ACUERDO CON CAMBIOS | Son funciones, no cuatro llamadas fijas. La especialización se valida por perfil/tarea; una reparación o varios documentos amplían llamadas. Fallo del revisor no autoriza degradar a una revisión propia para invertir. |
| Tasa base Q y vista exterior | DE ACUERDO CON CAMBIOS | Motor calcula sobre cohorte y horizonte definidos antes de observar el resultado, con tamaño efectivo e incertidumbre. Ser Q no convierte cualquier historia en tasa base defendible. Falta de datos devuelve NO_ESTIMABLE. |
| Combinación N3 y objeciones | DE ACUERDO CON CAMBIOS | Combinar solo pronósticos del mismo evento/horizonte, no promediar tesis incompatibles. Pesos congelados y estimados fuera de muestra; divergencia no se borra con la media. Evidencia citada no implica objeción resuelta. |
| N0–N3 y carteras | DE ACUERDO CON CAMBIOS | Importe, incertidumbre y daño potencial, no solo cartera. N1 sirve para cribar; no permitir que un N0 reusado eluda revisión vigente de una decisión nueva. La vía sistemática conserva sus propios controles. |
| Orden DIV, IDX/FON, RV | DE ACUERDO CON CAMBIOS | Coherente con el rumbo aceptado de largo plazo en paralelo L0. Mantener C-RV como prueba de un segundo perfil sustancialmente distinto antes de congelar CT-G-02; no convertir excepción al contador en excepción a seguridad. |
| No repetir B | DE ACUERDO CON CAMBIOS | Reutilizar evidencia identificada y vigente, con cobertura declarada. C debe revisar lo material para su propia tesis y repetir lo invalidado, no aceptar conclusiones de B como dato. |

## Hallazgos y mejoras

**1. Reutilización con contexto completo.** El registro debe identificar instrumento, vía, dirección, horizonte, mandato y versión, sello K, kit/modelo/método, evidencia, informe revisor y caducidad. Cualquier cambio invalida las partes afectadas. Los controles R-01…R-14 de `sistema_global/marco_comun_c/validador/validar_encargo.py` exigen correspondencia con el nuevo expediente y prohíben un sobre anterior al encargo: reutilizar cálculos no permite reenviar el mensaje antiguo. Emitir nueva envoltura con trazabilidad al análisis original y no contar ese mismo pronóstico como observación nueva en SC-4. Reduce coste sin falsear independencia ni muestra.

**2. Resolución sustantiva de objeciones.** El validador CT-G-03 comprueba IDs, referencias, cobertura, gravedad, autoría y correspondencia por hash. Eso acredita estructura y procedencia, no que una cita refute la objeción. Proponer resolución por prueba determinista cuando sea posible y revisión independiente cuando sea semántica; registrar abierta/resuelta/aceptada por operador sin confundir esos estados. Si cambia el sobre, vincular revisión al hash final y revalidar. La cita de una fuente irrelevante debe ser un caso adverso del banco.

**3. Alcance de verificación por nivel.** El Documento 0 §1 exige Contradictor antes de llegar a D; la propuesta deja N1 sin él. Precisar que la criba N1 no es un sobre listo para invertir, y que N0 conserva una revisión vigente o necesita otra si cambió lo material. Una modificación de ese requisito debe aprobarse explícitamente. Conservar validación final tras agregación N3 y tras cualquier corrección, no solo antes del Contradictor.

**4. Prerrequisitos reales de C-DIV.** K: cotizaciones y convención del par, calendarios, tipos/curvas y coste de financiación según instrumento, series disponibles en cada fecha y sus revisiones, episodios de estrés y factores comunes; posicionamiento COT si el método lo utiliza, con su retraso de publicación. SC-3: conversión a EUR, retorno neto del instrumento concreto, costes de entrada/mantenimiento/salida, liquidez, estrés y exposición factorial, y tasa base con método defendible. Un registro de artefactos no equivale a disponer de todos esos cálculos ni datos. Para cada salida se necesita una matriz campo → dato → método → validación → política si falta. Un dato opcional ausente puede permitir resultado parcial; un dato material ausente impide promoverlo, sin paralizar controles de posiciones existentes.

**5. Independencia y agregación.** Misma evidencia y mismos supuestos pueden correlacionar errores aunque cambie el proveedor. Medir esa dependencia y conservar escenarios incompatibles; pesos iguales al inicio no confieren confianza alta. No sumar el número de modelos al número de observaciones de calibración. Anonimizar casos históricos tampoco garantiza que un modelo no reconozca episodios: añadir controles de contaminación y validación hacia delante.

**6. Consumo no demostrado.** N2 de dos o tres llamadas omite reparaciones, varias lecturas, nueva evidencia y resolución de objeciones. N3 «como mucho cinco» tampoco es un máximo operativo si hay reintentos. Presupuestar por expediente con límites de rondas y salida máxima, más caché y herramientas; medir coste por sobre utilizable, no por llamada. N0 ahorra IA, pero K y Motor pueden tener coste. No he ejecutado llamadas reales ni construido kits para atribuir precisión o coste observado a las tablas propuestas.

**7. Perfil completo y conocimiento versionado.** Activación tras banco específico: un bono con opciones, un fondo sintético y una moneda requieren supuestos distintos. El esquema del cuerpo especializado y sus métodos deben existir antes de declarar el perfil ACTIVO. Evitar cargar toda la biblioteca: recuperar referencias concretas y conservar su versión. Esto hace defendible el ahorro; también evita esconder carencias detrás de un texto genérico.

## Respuestas a las seis preguntas

1. Sí al núcleo y cuatro papeles, con kits que sean paquetes verificables y posibilidad de instancias especializadas cuando la evidencia lo justifique.
2. Sí al segundo proveedor ya aceptado; precisar presupuesto, aislamiento y qué ocurre si no está disponible. No sustituye los controles deterministas.
3. Sí al orden propuesto bajo el rumbo aprobado, manteniendo largo plazo en L0 y C-RV para probar heterogeneidad antes de congelar el contrato.
4. Si el otro C-DIV se comparte, usarlo como material a contrastar con el banco y los contratos actuales; su ausencia no bloquea el esqueleto común. No presumir que está validado.
5. Opus solo en N3 puede ser una configuración aspirante, no una regla de calidad: elegir por resultados y coste total de cada tarea.
6. Sí a tasa base por código Q desde Fase 1 donde haya cohorte, datos y método defendibles. No fabricar probabilidad para cumplir el esquema cuando falten.

## Cierre

Diseño recomendable con los cambios anteriores. No se modifica ningún bloque, contrato ni código del marco. Las condiciones son de diseño y verificación futura; no constituyen certificación de un C operativo.
