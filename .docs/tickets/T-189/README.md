# T-189 · Configuración no permitida rechazada parcialmente y Ampliación de presupuesto en el ciclo periódico y Credencial en un mensaje

| Campo | Valor |
| --- | --- |
| Estado | EN QA (r01, revisión independiente pendiente) |
| Implementación | Astra |
| QA independiente | Claude |

## Alcance y criterios de aceptación

1. PB-10. CRI aplicado (servicio); H1 de ALT rechazado (8.3); umbral E rechazado (CALIBRABLE, no de servicio); RET- `APLICADA_PARCIALMENTE` con motivos; respuesta explicativa al Broker. F10 cambia solo P-02; HA sin incidencia de escritura (rechazo correcto, no intento de escritura).
2. PB-17. Primera: AUTORIZADA (valor de la información: puede cambiar el top-3) con condiciones; segunda: DENEGADA con motivo y cierre con alcance reducido. Dos AUT- en HA con CPI, EAC y motivo; consumo real registrado en F5.
3. PB-21. Mensaje rechazado íntegro; incidencia de seguridad con el campo y el tipo, sin el valor; ningún archivo contiene el dato. Búsqueda del valor en todos los archivos: cero coincidencias.

## Registro

21-11-2026 · Plan local basado en el plan de pruebas V3.0 y el encargo de Claude.

CT-04 conserva P-03 cuando rechaza una celda; AUT lleva CPI y EAC; R8 registra la clase de dato sin guardar el valor.
