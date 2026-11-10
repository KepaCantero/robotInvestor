# T-87 · Guía de los cambios

El diagnóstico en `2065e48` abarcó 36 casos: A1–A8 sobre agentes, D01–D10 sobre datos y evaluación, C1–C8 sobre contratos, y O1–O10 sobre operación. Se partió de `bc90534`, que ya incluye las correcciones de T-53 y T-66. El control de la objeción fuerte enviada como texto no era un fallo reproducible: se conserva la validación booleana y la refutación de T-66.

- **Registro y operación:** [controles.md](controles.md). Los adjuntos de credenciales, las fechas de efecto y los mandatos del operador se comprueban antes de utilizarse. La cadena de registros añade una referencia al final confirmado y exclusión mutua entre escritores. Véanse las instrucciones de respaldo y recuperación.
- **Datos y evaluación:** [datos.md](datos.md). Se trata por separado cuándo sucedió algo y cuándo se podía saber. Las ventanas relativas tienen que ser válidas para todas sus patas. El método forma parte de la celda de certificación. Las salidas antiguas se conservan; los certificados sin método no autorizan porcentajes de un método nuevo.
- **Agentes:** [agentes.md](agentes.md). Se verifican procedencia, corte temporal y estados reales de llamada, incluida la ruta de reparación. Caché, simulación y repetición se distinguen, con pruebas offline.
- **Mensajería, entrega y frontera:** [contratos.md](contratos.md). Reservas durables para reintentos, estados del sobre y del objeto distinguidos, control R21 en el ejecutor, ejemplo de paquete conforme y borrador de encargo a B condicionado a una correspondencia explícita. El catálogo diferencia ficha reconocida de operación realmente disponible.

La entrega implementa controles verificables. No sustituye las 64 fichas documentadas por operaciones de cálculo ni ejecuta un ensayo de inversión o de calidad de un modelo de pago. Las propuestas de rediseño que el operador y Claude aplazaron siguen en T-67. Los documentos de gobierno, los prompts y el corpus canónico congelado permanecen en la versión de la base.
