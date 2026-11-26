# Correcciones tras la comprobación propia de T-181, T-182, T-188 y T-192

La base de esta corrección local es `c4f2d1b`. Los hallazgos se reprodujeron en esa versión. La foto de la segunda revisión identificaba los cuatro tickets rechazados. El diagnóstico escrito de Claude seguía pendiente al preparar el cambio.

| Ticket | Qué repetir en una revisión posterior |
| --- | --- |
| [T-181](../../tickets/T-181/pruebas.md) | Retirar una referencia y volver a consultar el día anterior con un lector recién creado. Interrumpir la entrega del aviso y repetir el comando original. Una baja antigua sin instantánea conserva únicamente lo que consta en su registro. |
| [T-182](../../tickets/T-182/pruebas.md) | Pasar prosa financiera con sujeto explícito por el saneamiento de entrada y por la publicación del informe. El reconocedor de sujetos cubre un vocabulario financiero acotado. |
| [T-188](../../tickets/T-188/pruebas.md) | Enviar dos dudas distintas en los mismos tres análisis y repetirlas en un cuarto. Verificar la lista de evidencias y el destinatario de cada lección. Comprobar la entrega de la comparación de decisiones con el mínimo ordinario por grupo. |
| [T-192](../../tickets/T-192/pruebas.md) | Representar en el mismo CSV la primera publicación y la revisión de una misma observación. Comprobar que la resolución conserva la primera y que el cálculo histórico solo usa las publicaciones disponibles al emitir. |

El informe del plan se genera con la copia de trabajo basada en el commit anterior. Para repetir los controles, usar el código y el mapa del commit que incluye esta nota. Claude conserva la revisión independiente. Cuando llegue su dictamen, contrastar cada hallazgo con estas regresiones y registrar los casos que la revisión propia hubiera pasado por alto.
