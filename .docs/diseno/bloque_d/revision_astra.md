# C-04 · Revisión del diseño de D

Astra · 12-11-2026 · develop e91eebc. Solo diseño; sin cambios en bloques ni marco.

## Resumen (cinco líneas)

1. Apoyo comparar decisiones completas sobre la cartera, con costes, frente a alternativas explícitas.
2. El crecimiento compuesto es un objetivo útil, pero no sustituye restricciones de pérdida, liquidez y necesidades del mandato.
3. Hay que definir qué rango se compara: distribución del resultado y precisión de la ventaja estimada son objetos diferentes.
4. Un tamaño cambiado por E puede cambiar el ganador de D: hace falta revisión acotada del resultado final.
5. La comparación por valor esperado entre Q/S/K sigue pendiente y no se habilita con esta revisión.

## Base de la revisión

Encargo y propuesta de D, Constitución P1/P3/P5/P17/P19 y §§2,4.1,5,7, comparador actual y decisiones del operador. No es revisión ciega: la propuesta ya se leyó en la auditoría global anterior. Mi criterio es evaluar alternativas ejecutables sobre el mismo estado y horizonte, preservando incertidumbre y separación entre proponer, aprobar y ejecutar.

El comparador actual en `sistema_global/marco_comun_c/validador/comparador.py` aplica suelos de costes, riesgo conservador, topes de confianza y sensibilidad, y separa clases. La propuesta amplía sustancialmente sus entradas: cartera, operaciones pendientes, costes no lineales y calibración. No es un mero cambio de fórmula ni una QA del código actual.

## Veredictos por decisión

| Decisión | Veredicto | Motivo y mejora |
| --- | --- | --- |
| Crecimiento compuesto neto | DE ACUERDO CON CAMBIOS | Objetivo sujeto al mandato y restricciones de trayectoria. Usar método declarado; la aproximación media-varianza no cubre cualquier distribución. |
| Un comparador por perfiles | DE ACUERDO | Núcleo común, horizonte/calendario y costes por mandato. Evita divergencias entre tres implementaciones. |
| Cuatro opciones | DE ACUERDO CON CAMBIOS | Incluir mantener las posiciones actuales, aplicar el plan base, reducir y conservar liquidez necesaria. «No hacer nada» y comprar el benchmark no son físicamente la misma acción. |
| Contracción por historial | DE ACUERDO CON CAMBIOS | No convertir Brier directamente en precisión de rentabilidad. Modelar error del objetivo relevante con muestras independientes, versiones congeladas y salida si no hay tasa base defendible. |
| Aportación marginal | DE ACUERDO CON CAMBIOS | Correcto incluir cartera; comparar planes completos, operaciones pendientes y financiación. Revalidar con tamaño final de E; efectos no lineales impiden escalar siempre por 1.000 EUR. |
| Ventana común y reinversión | DE ACUERDO CON CAMBIOS | Misma ventana y escenarios; incluir liquidación, costes, disponibilidad del dinero y riesgo del benchmark. No suponer acceso inmediato a una inversión alternativa. |
| Extremo bajo y tres salidas | EN DESACUERDO | En su formulación actual mezcla rangos sin definirlos y usa solapamiento como desempate. Sustituir por incertidumbre de la diferencia emparejada y estados distintos para empate, falta de datos y falta de ventaja. |
| D/E separados, Kelly común | DE ACUERDO CON CAMBIOS | Compartir objetivo/modelo versionado, no aprobación. Kelly fraccional es una alternativa a validar, no una garantía ni el único modelo apto para todo mandato. |
| Cero tokens y aprendizaje I | DE ACUERDO CON CAMBIOS | Cero llamadas LLM dentro de D es viable; datos, simulación y validación sí cuestan. Ajustes aprendidos pasan por I/J/F/operador; no actualización libre de pesos. |

## Comprobaciones y puntos débiles

**Ejemplos numéricos.** `(1,03 × 0,97 − 1) × 100 = −0,09 %`, correcto; repetir cincuenta pares dejaría aproximadamente −4,40 %, bajo esa secuencia hipotética. `1,02^26 − 1 = 67,34 %`; con 365/14 periodos, 67,58 %. El «68 %» es un redondeo razonable de una hipótesis de reinversión, no una previsión. La advertencia contra extrapolarla es acertada.

**Objetivo y aproximación.** Para retornos pequeños, el desarrollo de `E[log(1+r)]` contiene el segundo momento `E[r²]`, no solo la varianza; descartar términos exige justificar la aproximación. Para colas, saltos o riqueza no positiva, no basta una penalización cuadrática. Kelly persigue crecimiento de largo plazo bajo supuestos; limitar caídas exige restricciones adicionales. Esto también se estudia explícitamente en [Busseti, Ryu y Boyd, Risk-Constrained Kelly Gambling](https://www.web.stanford.edu/~boyd/papers/kelly.html). No garantiza la máxima ganancia observada de la semana siguiente.

**El rango de la diferencia.** Proponer dos salidas distintas: distribución de pérdidas/ganancias futuras y rango de incertidumbre de la ventaja estimada frente a la referencia. Calcular diferencias con las mismas fechas/escenarios. Dos opciones con `A = Z + 1` y `B = Z` pueden tener rangos individuales ampliamente solapados y una diferencia constante de 1: el solapamiento no demuestra empate. Tampoco el extremo bajo de un candidato frente a un benchmark puntual trata simétricamente su incertidumbre. Fija el criterio antes de mirar resultados y corrige la selección entre muchas opciones. Optimizar estimaciones ruidosas sesga al alza el valor de la opción elegida: [Smith y Winkler, The Optimizer’s Curse](https://jimsmith.host.dartmouth.edu/wp-content/uploads/2022/04/The_Optimizers_Curse.pdf).

**D ↔ E sin bucle libre.** E proporciona tamaño de referencia y restricciones; D compara planes; E devuelve el tamaño factible final. Si cambia materialmente coste, exposición o ventaja, una comprobación determinista vuelve a evaluar los finalistas sobre ese mismo estado. Limitar rondas y caducidad; si no converge, escalar o abstenerse. F mantiene su control independiente. Una tabla anterior a otra operación concurrente no autoriza gastar de nuevo el mismo efectivo.

**Abstenerse por datos no es ordenar una compra pasiva.** P5 sí define el benchmark como referencia y destino por defecto; P20 exige E/F/G para toda orden. Registrar por separado la decisión analítica, el motivo y el plan operativo. Si faltan datos para operar o hay una incidencia de conciliación, no enviar una compra del benchmark automáticamente. Mantener el estado existente puede ser la única acción segura hasta resolverla.

**Corto plazo.** Incorporar diferencial, deslizamiento condicionado por tamaño/volatilidad, órdenes pendientes, capacidad conjunta, señales caducadas y simultaneidad correlacionada. El hecho de que J validara una estrategia no prueba que cada operación futura cumpla costes y condiciones actuales. La exención general de cada operación del freno a la rotación necesita definición y aprobación; no puede inferirse solo de la validación inicial.

**Costes y fiscalidad.** Si los escenarios ya son netos, no volver a descontar los mismos costes. Aclarar si el margen constitucional de rotación se mide sobre ventaja bruta o sobre neta ya descontada, con una fórmula única D/E/SC-9. No asumir que toda venta genera impuesto: usar el efecto calculado para el caso por SC-9, no una regla universal en D.

**Datos y orden.** Primero snapshot de G/K, mandatos y referencias ejecutables; después costes por instrumento e intermediario y factores/escenarios conjuntos; luego comparación simple validada; después estimación de error/calibración suficiente y optimización. No esperar a I completo para registrar resultados, pero sí esperar evidencia antes de conceder peso aprendido. Las operaciones no son automáticamente observaciones independientes.

## Compatibilidad y criterios para validar

La Constitución §5, regla 1, dice: «D usa una puntuación única solo dentro de la misma clase». E8 de las decisiones del operador pospone cambiarlo hasta antes de Fase 2: rangos prudentes no autorizan mezclar Q/S/K por valor esperado. El nuevo CT-G-05 debe declarar estado de cartera, tamaño, horizonte, método del rango, referencia, costes ya descontados y vigencia. No se modifica aquí ese contrato.

Medir abstenciones por causa y calidad de descartados, exceso neto contra referencia y contra mantener, frecuencia de elección, pérdidas en estrés, rotación y estabilidad ante costes y tamaños. Separar validación temporal y reserva final; reutilizar indefinidamente tablas para elegir reglas también sobreajusta. Umbrales, tamaños de muestra y nivel de confianza quedan en configuración aprobada, no se inventan en este informe.

## Respuestas a las ocho preguntas

1. Sí como objetivo económico común, sujeto a restricciones explícitas y al horizonte del mandato; no como única consideración.
2. Reparto por operador en SC-1; D puede informar de alternativas comparables sin mover dinero por su cuenta.
3. Fracción prudente como aspirante en simulado, sin afirmar que una fracción universal controla el riesgo. No reproduzco aquí parámetros privados.
4. Mantener la regla actual hasta la decisión pendiente E8. Para casos sin distribución defendible, no fabricar valor esperado.
5. Sí a reforzar y sustituir como opciones cuando sean viables; incluir también mantener/reducir y costes completos.
6. Separados, con modelo compartido y revalidación acotada tras el tamaño final. No confundir comparación con aprobación de riesgo.
7. Exigir muestra efectiva y precisión suficiente por tarea/horizonte; no un número de operaciones universal ni muchas posiciones correlacionadas contadas como independientes.
8. Benchmark como hipótesis explícita de reinversión, incluyendo plazos y costes. La tasa de oportunidades observada por I solo la sustituye tras validación fuera de muestra y aprobación.

Conclusión: buena dirección, con dos cambios prioritarios —rangos de diferencias y cierre D/E— antes de convertirla en especificación implementable.
