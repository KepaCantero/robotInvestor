# C-05 · Revisión del diseño de E

Astra · 12-11-2026 · develop 9017e87. Solo documentación local; no publicar sin autorización expresa.

## Resumen (cinco líneas)

1. Apoyo las tres capas de E y que dimensionar sea código sujeto a F.
2. La tabla de Kelly reproduce una aproximación concreta; no demuestra que un cuarto sea seguro ni óptimo en la práctica.
3. Stop, volatilidad y correlación son estimaciones de riesgo, no límites garantizados de pérdida.
4. Falta cerrar el intercambio con D y reservar conjuntamente dinero y riesgo ante planes simultáneos.
5. Priorizaría un plan simple reproducible y controles conjuntos antes de ajustar tamaños con rentabilidades aprendidas.

## Base de la revisión

Encargo/propuesta de E, revisión de D, Constitución §§2,4,7,8, Documento 0 V0.10 y `sistema_global/marco_comun_c/validador/dimensionado.py`. Ya conocía la propuesta por la auditoría global; no presento esta revisión como ciega. Se distingue diseño futuro de código vigente: este último ya convierte mediante `divisa_cotizacion` y `tipo_cambio`, aunque el Documento 0 antiguo todavía enumera la conversión como pendiente. No he hecho QA del ejecutor ni reactivado tickets retirados.

## Veredictos

| Decisión | Veredicto | Motivo y mejora |
| --- | --- | --- |
| Plan base, posiciones y vista global | DE ACUERDO CON CAMBIOS | Buen reparto. Todas las capas usan el mismo estado conciliado, incluyen posiciones pendientes y patrimonio externo declarado pertinente; no duplicar presupuestos entre capas. |
| Tamaño por riesgo, retorno para inclinar | DE ACUERDO CON CAMBIOS | Prudente como dirección, pero volatilidad/correlación también tienen error y cambian. Añadir escenarios adversos, límites nominales y sensibilidad; no llamar conocido al riesgo. |
| Kelly fraccional y un cuarto | DE ACUERDO CON CAMBIOS | Referencia aspirante, no regla universal. Calcular sobre cartera y ventajas netas; admitir no estimable. El cuarto requiere validación frente a asignación simple, no adopción por la tabla teórica. |
| Tabla por cartera | DE ACUERDO CON CAMBIOS | Mandato y perfil comunes, con métodos distintos por instrumento. Sumar stops no mide todo el riesgo; largo plazo también necesita liquidez y escenario de retirada. |
| Ciclo de cinco pasos | DE ACUERDO CON CAMBIOS | Añadir reserva de recursos, dependencias entre patas y comprobación al tamaño final. La vista global puede originar revisión, no autorizar por sí misma movimientos entre libros. |
| Fronteras D/F/M/H/G | DE ACUERDO CON CAMBIOS | Conservarlas, pero corregir «E no vuelve a comparar»: D debe comprobar si la cantidad final invalida su decisión. G decide detalles de envío dentro del plan; F sigue aprobando cada acción. |
| Cero tokens e históricos | DE ACUERDO CON CAMBIOS | Cero LLM en E sí; cero coste o ausencia de anticipación no. Datos, ajustes de parámetros y selección de reglas pueden filtrar el futuro aunque todo sea código. |

## Tabla de Kelly: comprobación y límites

Hay una imprecisión de notación. Si `x` es exposición, la aproximación es `g(x)=x·μ−x²·σ²/2`, con óptimo `x*=μ/σ²`. Si `f` es fracción de ese óptimo, `x=f·x*` y `g(f·x*)/g(x*)=2f−f²`. No usar a la vez `f` como exposición y fracción del óptimo.

La tabla da 43,75 % (redondeado a 44 %), 75 %, 100 %, 75 % y 0 % para f=1/4, 1/2, 1, 3/2 y 2. Se reproduce bajo esa aproximación, ventaja conocida, varianza fija y ausencia de costes no lineales. La volatilidad escala linealmente ahí; no ocurre necesariamente con opciones, liquidaciones, costes mínimos o exposición que cambia con el precio. Sobreestimar al doble la ventaja solo duplica ese óptimo si lo demás permanece igual.

Kelly fraccional no impone por sí mismo una probabilidad máxima de caída ni un suelo patrimonial. Las restricciones explícitas de caída son un problema adicional, tratado en [Busseti, Ryu y Boyd](https://www.web.stanford.edu/~boyd/papers/kelly.html). No se deduce de esa literatura que una fracción concreta sea óptima para este robot.

## Mejoras prioritarias

**Riesgo de cartera antes que Kelly individual.** Dos posiciones ligadas al dólar o dos estrategias sobre el mismo mercado no son apuestas independientes. Evaluar conjunto, escenarios de crisis y exposición nominal, incluyendo órdenes autorizadas, ejecuciones parciales y fondos subyacentes. Correlación estimada baja no permite superar límites nominales; si faltan datos materiales, no sustituirlos por cero. Sin evidencia suficiente de ventaja, usar el plan aprobado y una referencia simple, no inventar un Kelly.

**Reserva de dinero y riesgo.** Dos planes pueden parecer válidos contra el mismo saldo y excederlo al ejecutarse juntos. El servicio propietario del estado debe reservar recursos de forma indivisible al autorizar, con versión de estado, vigencia y liberación solo ante cancelación/conciliación confirmada. Una orden incierta conserva la reserva. E propone esa reserva; F la controla y G la consume. Esto es requisito de arquitectura, no afirmación de que el marco falle hoy en todas esas situaciones.

**Cerrar D/E.** D evalúa un tamaño de referencia; E devuelve el factible. Si el tamaño, financiación o costes cambian materialmente, revalidar con D antes de aprobación. Límite de rondas, resultado trazable y no intervención libre de otro agente. Compartir el objetivo no hace equivalentes resultados calculados con cantidades diferentes.

**Plan ejecutable por etapas.** Una compra financiada con venta no puede asumir el dinero disponible antes de liquidación. Definir dependencias, reservas fiscales, redondeo por instrumento, mínimos, comisiones y qué hacer con ejecución parcial o rechazo de una pata. Una aportación repetida por error no crea dos saldos: identificador e idempotencia del evento de G. E fija límites y prioridades del plan; G gestiona ejecución dentro de ellos sin reinterpretar el objetivo.

**Volatilidad y caída.** Reducir exposición después de una subida de volatilidad puede vender tras la caída y recomprar tras la recuperación. Un freno por drawdown puede proteger frente a deriva o convertir ruido en rotación. Comparar políticas con bandas, persistencia de señal, plazos de revisión y costes, contra pesos estables; no prometer mejor rentabilidad. Toda rehabilitación y aumento sigue autonomía y política aprobadas. La decisión E3 del operador exige aprobación de cambios al principio.

**Presupuesto de pérdida.** «Cuánto acepto perder en un año malo» es comprensible, pero necesita horizonte, probabilidad, escenario y tratamiento de pérdidas más extremas. No hay una conversión única de esa frase a volatilidad o distancia al stop. Una orden stop tampoco garantiza precio de salida: el propio Documento 0 reconoce huecos. Separar pérdida calculada al stop, pérdida bajo estrés y restricciones nominales. El camino de riesgo del largo plazo atiende objetivos y liquidez, no solo la fecha final.

**Fiscalidad: pendiente del asesor.** No aplicar «FIFO y dos meses» a todos los productos como regla genérica. La [AEAT distingue condiciones de integración diferida por recompra y valores homogéneos](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-ayuda-presentacion/irpf-2025/7-cumplimentacion-irpf/7_6-ganancias-perdidas-patrimoniales/7_6_1-conceptos-generales/7_6_1_1-concepto-ganancias-perdidas-patrimoniales/integracion-diferida-perdidas-patrimoniales.html). SC-9 debe devolver tratamiento y procedencia de la regla para el instrumento y ejercicio, contemplando operaciones de todas las cuentas pertinentes. Señalo la simplificación para P-06; no certifico ni implemento reglas fiscales. Con reglas provisionales, no atribuir ahorro fiscal confirmado.

**Independencia de F.** Preguntar sus topes evita fórmulas divergentes, pero F puede discrepar justificadamente si cambian precios, política o estado. E no se autoaprueba al consultar F; la comprobación en ejecución permanece. Compartir métodos no sustituye datos independientes ni las pruebas adversas de F. La concentración mínima antes de M ya es exigida por Constitución §7.

## Validación propuesta y orden

Primero estados y reservas, plan base y aportaciones idempotentes; después encaje conjunto, costes y escenarios; finalmente inclinaciones por ventaja suficientemente medida. Comparar con pesos del mandato y tamaño fijo prudente, no solo con la versión más compleja. Medir exceso neto, caídas, rotación, incumplimientos, recursos bloqueados, sensibilidad a costes y errores de estimación; separar datos de ajuste y prueba. Los inputs procedentes de C/J tampoco quedan libres de anticipación porque E sea determinista.

## Respuestas a las siete preguntas

1. Un cuarto puede ensayarse como hipótesis pública de la propuesta, no adoptarse como umbral de seguridad. No traslado aquí los valores privados confirmados del operador.
2. Presupuesto en euros y porcentaje, acompañado de horizonte y escenario/probabilidad; evitar presentarlo como pérdida máxima garantizada.
3. Ajuste por volatilidad como aspirante en trading/táctica, con bandas y costes; mantener el plan base de largo plazo salvo política explícita validada.
4. Freno de trading ligado a pérdida/deriva y procedimiento de rehabilitación; medir falsas alarmas. No aumentar riesgo para recuperar.
5. Bandas y aportaciones primero, sujetas a liquidez y coste. Su anchura sale de configuración aprobada y de pruebas, no de una preferencia verbal.
6. Movimientos entre estrategias solo si la matriz de autonomía y las asignaciones aprobadas lo permiten; de otro modo aprobación expresa. No confundir rebalanceo con permiso para cambiar estrategia.
7. Revisión anual programada más eventos materiales que justifican propuesta; el operador aprueba movimientos entre carteras. Un límite agotado no habilita transferir para esquivarlo.

No se cambia código, configuración ni contratos. Cierre documental en local; publicación suspendida por instrucción expresa del operador.
