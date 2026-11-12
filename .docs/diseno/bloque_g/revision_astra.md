# C-07 · Revisión del diseño de G

Astra · 12-11-2026 · develop b3e91de. Solo documentación local; no publicar sin autorización.

## Resumen (cinco líneas)

1. Apoyo G determinista como único canal de ejecución, con libro y conciliación trazables.
2. Optimizar el envío exige límites aprobados de precio, plazo, cantidad y coste; no puede abrir una nueva decisión de inversión.
3. Una orden sin confirmación queda incierta, con recursos reservados; no equivale a no haber operado.
4. Fondos y traspasos necesitan estados propios de aceptación, valoración y liquidación, no una adaptación superficial de órdenes bursátiles.
5. Los dos libros son vistas de hechos comunes; no dos fuentes que puedan corregirse o discrepar sin rastro.

## Base y contraste con el estado actual

Leídos encargo y propuesta, Constitución P15/P20 y §§2,3,6,7,8; Documentos 0 V0.08, V0.15, V0.18, V0.20 y V0.21; filas T-01/T-14/T-30/T-31 y puntos pertinentes de `sistema_global/marco_comun_c/validador/ejecucion_g.py`. No es revisión ciega ni QA del código: la propuesta ya se conocía de la pasada global.

Hay que corregir el diagnóstico «simulado y sin disparo de stops»: `mover_precio` del simulador ya dispara stops cruzados al precio nuevo, y V0.09 de H lo documenta. T-14 conserva una descripción antigua; la conexión real y su verificación siguen pendientes, pero esa simulación concreta no falta entera. V0.20 también documenta la foto de cartera desde G, conversión a euros y autorizaciones pendientes. V0.21 conserva protección durante reducción con órdenes de solo reducción. Estos avances deben ser la base del diseño.

## Veredictos

| Decisión | Veredicto | Motivo y cambio |
| --- | --- | --- |
| Ejecución por coste | DE ACUERDO CON CAMBIOS | Política determinista aprobada; límite de demora, cantidad padre, precio, participación y coste total. Si deja de ser viable, devolver incidencia, no cambiar la tesis. |
| Medir cada ejecución | DE ACUERDO CON CAMBIOS | Medir también canceladas, rechazadas y no ejecutadas; referencia de precio sellada en decisión y llegada. Incluir espera, oportunidad perdida, comisiones y FX sin duplicarlos. |
| Fondos y traspasos | DE ACUERDO CON CAMBIOS | Estados específicos y capacidades por intermediario/fondo, con dinero indisponible durante tránsito. Elegibilidad fiscal la da SC-9, no la palabra «fondo». |
| Dos libros | DE ACUERDO CON CAMBIOS | Un registro inmutable de hechos y vistas operativa/fiscal reconciliables, con identidades de instrumento, cuenta y titular. Correcciones por nuevos asientos, no sobrescritura. |
| Tabla por cartera y seis pasos | DE ACUERDO CON CAMBIOS | Buen marco, pero frecuencia por eventos y riesgo además de calendario. Revalidar antes de cada tramo y cubrir parcialidades; registrar siempre posiciones reales aunque estén desprotegidas. |
| Pruebas antes de dinero real | DE ACUERDO CON CAMBIOS | Autenticación, separación L0/real y contabilidad primero; simulación adversa y prueba del adaptador. Paper trading no acredita deslizamiento ni todas las garantías del broker real. |

## Hallazgos y propuestas

**1. Envío durable y estado incierto.** Anotar antes de enviar es correcto, pero esa anotación debe sobrevivir a un reinicio. Vincular orden padre, tramos, autorización, intentos y respuestas. Reintentar la misma intención con identidad estable hasta conocer su resultado; un intento nuevo solo tras estado terminal confirmado que lo permita. Si el broker no responde después del envío, mantener estado incierto, saldo y cantidad reservados, consultar antes de repetir y admitir respuestas tardías/desordenadas. El contrato §11 «se trata como no ejecutada» debe significar no confirmada, nunca recursos libres.

**2. No ocultar lo ejecutado.** «Nada se da por abierto» no puede hacer desaparecer exposición real del libro de control. Distinguir posición detectada pendiente de conciliación, protegida/no protegida y posición plenamente conciliada. El cierre de emergencia es una operación que también puede fallar. G-04/G-08 deben mantener cantidad posible o conocida visible para F, H y operador, conservando reservas y protección. No anunciar «nunca desconocida» como garantía que la red puede impedir cumplir.

**3. Tramos y protección.** La cantidad acumulada, no cada tramo aislado, consume la autorización y límites de volumen/coste. Tras cada ejecución parcial debe existir protección acorde al instrumento o una respuesta de emergencia definida. Preferir capacidades nativas verificadas cuando corresponda; no suponer que todos los adaptadores garantizan bracket, OCO y solo reducción de igual forma. Probar stop que salta mientras se cancela/amplía otro tramo, cancelación tardía y relleno adicional. No ampliar precio, plazo o capital para completar una orden que dejó de cumplir lo aprobado.

**4. Libro de efectivo y liquidación.** Separar saldo contable, disponible, reservado y en tránsito por cuenta/divisa. Una suscripción aceptada aún no tiene necesariamente cantidad/valor liquidativo definitivo; un reembolso no es efectivo disponible hasta la condición de liquidación prevista. Un traspaso tiene fases y posibles rechazos entre origen y destino. Reconocer un mismo movimiento una vez, aun si llegan aviso del broker, movimiento bancario y confirmación fiscal. Transferencias entre cuentas propias no son beneficio ni aportación externa nueva.

**5. Identidad y dos carteras.** Constitución §4.2.5 dice: «Un mismo activo en dos carteras son dos posiciones». La propuesta de permitir aumentos pero no posiciones independientes debe precisar el alcance: se puede tener posición neta por cuenta/intermediario y asignaciones internas separadas por libro. No fusionar tesis, stops o condiciones incompatibles perdiendo responsabilidad. Impedir inicialmente ciertos solapes puede ser una restricción operativa declarada, no una reinterpretación silenciosa de la Constitución.

**6. Fiscalidad a validar.** El libro fiscal debe recibir todos los hechos relevantes de la persona, con trazabilidad a cuentas y operaciones, mientras SC-9 determina agrupaciones de valores homogéneos, lotes y reglas. Una cola por ticker no basta para identidad fiscal. «Los traspasos no tributan» debe sustituirse por diferimiento si se cumplen requisitos, preservando historia fiscal: la [AEAT describe condiciones y exclusiones del régimen](https://www3.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c11-ganancias-perdidas-patrimoniales/determinacion-importe-ganancias-perdidas-patrimon-especificas/transmisiones-reembolsos-acciones-iic/regimen-especial-diferimiento-tributacion.html). El asesor P-06 valida aplicación, titularidad, homogeneidad y alcance entre cuentas. No resuelvo aquí esa fiscalidad ni certifico vehículos.

**7. Conciliación e incidentes.** La propuesta dice que una diferencia sin explicar deja la cartera en L1. Constitución §§8/11 la identifica además como desencadenante del kill-switch: no basta una degradación sin cancelar/bloquear entradas y seguir el procedimiento. Tolerancia numérica no es causa explicada; registrar evento, importe, moneda, fecha y justificación. Detectar acumulación de pequeñas diferencias. Los datos de K sobre eventos corporativos son previsión/referencia; contrastar el hecho aplicado y su fecha con el custodio antes de cuadrar cantidades y efectivo.

**8. Coste y calidad de ejecución.** Para comprar, comparar precio real con referencia sellada; para vender, cambiar signo. Separar movimiento durante espera, diferencial/impacto, comisiones y conversión con convención única. Conservar órdenes no completadas para que el sistema no parezca barato por ejecutar solo las fáciles. Modelos aprendidos de costes se validan por instrumento, tamaño y estado de mercado antes de cambiar D/E/F: no ajuste automático sin la ruta de aprobación. Elegir hora por liquidez es política comprobable, no una regla universal por mercado.

## Ejemplo de las 200 operaciones

`200 × 0,10 % = 20 %` solo permite hablar de veinte puntos sobre capital si cada operación de ida y vuelta mueve un nominal equivalente a ese capital y el coste incluye ambas piernas. Si cada operación mueve el 10 % del capital, el coste simple sería dos puntos. Si el coste del 0,10 % se aplica sucesivamente al capital restante, el arrastre aislado sería `0,999^200−1 ≈ −18,14 %`. Ninguna cifra prueba la rotación real de este robot. La enseñanza correcta es medir coste sobre nominal y rotación, no deducir pérdida anual solo del número de operaciones.

## Orden y pruebas exigibles al futuro diseño

Primero autenticación y separación irrevocable de permisos L0/real; después registro durable, efectivo y estados inciertos; luego semántica del adaptador, fondos y optimización. Ensayar caída antes/después de envío, acuse perdido, reinicio, eventos duplicados y fuera de orden, ejecución durante cancelación, cierre/stop concurrentes, saldo insuficiente, cambio corporativo, transferencias y liquidaciones tardías. Las pruebas de simulación no sustituyen el contraste de capacidades del intermediario elegido. No se ejecuta esta batería ni se reabren T-01/T-14/T-30/T-31 en esta revisión.

## Respuestas a las seis preguntas

1. Dos intermediarios es el rumbo ya aceptado; seleccionar por capacidades probadas y coste total, sin suponer que una API nominal cubre los casos críticos.
2. Permitir asignaciones por cartera cuando el libro agregado y SC-9 lo soporten; si se restringe inicialmente el solape, declararlo y conservar visibilidad del patrimonio.
3. Aumentar exige recalcular coste, riesgo y protección agregada, conservando lotes/asignaciones internas. No borrar identidades de posiciones entre carteras.
4. G puede escalonar solo bajo política y límites aprobados del plan padre; cada tramo consume el mismo presupuesto y respeta caducidad y protección.
5. Saldos en divisas si son compatibles con mandato y necesidades de liquidez; ahorrar conversiones no justifica acumular exposición cambiaria sin control.
6. Subcuentas pueden facilitar separación operativa; no sustituyen consolidación de riesgo, conciliación ni el tratamiento fiscal pertinente de la persona.

Cierre documental local. No se modifican bloques, adaptadores, reglas fiscales ni contratos.
