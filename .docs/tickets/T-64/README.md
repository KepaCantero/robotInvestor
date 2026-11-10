# T-64 · Fechas de la evidencia de cierre

**Alcance acordado:** inspeccionar las fechas actuales y preparar una prueba reproducible antes de modificar el ejecutor. Base 76cdc40. Astra prepara los casos; Claude puede reproducirlos.

Una empresa comunica retrasos el 10 de marzo de 2025. El 20 de marzo se intenta cerrar una objeción fuerte con un informe. El objeto del ensayo es el catálogo de fuentes de B y su aplicación al cierre. La prueba conserva la misma petición y distingue el día del incidente, el día observado, la publicación, la primera disponibilidad y el registro local. Se evalúa al final del día, sin redes ni modelos externos.

**Aceptación del diagnóstico:** ejecutar los tres casos acordados con la lógica de T-63, registrar comportamiento observado y esperado, y explicar si el límite procede del registro local o del contenido del informe. Como controles, probar una publicación reciente sobre datos antiguos y una referencia futura ya presente en una importación histórica. La prueba supone que el informe adecuado versa sobre los pedidos afectados. No evalúa su significado ni la veracidad de una fuente real.

## Corrección autorizada

Astra implementa sobre 1ef8bd7 y Claude realiza la revisión independiente. Para cerrar una objeción fuerte, verificar fecha estructurada del incidente y fechas de observación, publicación y primera disponibilidad de todas las citas. El corte diario se interpreta en la zona del expediente. Con resolución diaria se exige un hecho posterior al día del incidente; no se infiere la cronología de dos sucesos del mismo día. Un cálculo reciente o una descarga reciente no sustituyen la fecha de la observación. Las referencias deben seguir perteneciendo a la petición. Verificar los cinco casos originales, campos ausentes o inválidos, embargo, límite de corte y una entrega completa B→C. Conservar las entregas históricas ya emitidas.

**Estado actual: CERRADO.** QA de Claude APTO el 10-11-2026 ([qa.md](qa.md)); fusionado en `develop`. H-01 (baja) queda en la deuda técnica.
