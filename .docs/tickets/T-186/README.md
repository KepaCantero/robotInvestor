# T-186 · Bloque A: kit para pasar PB-40 (comprensión del informe visual por usuarios inexpertos)

| Campo | Valor |
| --- | --- |
| Estado | KIT LISTO (18-11-2026); la prueba la pasa el operador con 10 personas |
| Pieza | Plan de pruebas del Bloque A V3.0, PB-40 (RP-14) |
| Planifica · implementa | claude · claude |
| Aprobación del operador | 18-11-2026: «Ahora PB-40» |
| Deuda técnica | T-186 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Qué pide el plan

| Campo | Contenido |
| --- | --- |
| Preparación | Informe visual de un ciclo de pruebas; 10 personas sin formación financiera |
| Pasos | 1) Lectura cronometrada. 2) Cuestionario de 5 preguntas (qué oportunidades, por qué, riesgo, horizonte, qué no es) |
| Criterio de aprobación | Mediana de lectura < 3 min; ≥ 80 % de respuestas correctas; nadie interpreta el informe como recomendación personal |

No se puede automatizar: necesita personas reales. Este ticket deja el material listo para que el operador la pase y para que el resultado se registre sin trabajo a mano.

## El kit

- **Informe:** `.docs/tickets/T-186/kit_pb40/informe_visual_RUN-2024-0001.html`. Es el informe visual de un ciclo con el cliente simulado, del 29-03-2024, con la configuración por defecto. Lleva tres ideas de monedas (Japón, Australia y América Latina), riesgo 2 de 5 y plazo principal de meses.
  - Se eligió el perfil por defecto (solo DIV, el de la Fase 1). Con los doce tipos, el simulado repite el mismo nombre en las tres tarjetas de cada tipo, y eso confundiría a los participantes por un defecto del simulado, no del informe.
- **Página de la prueba:** un Artifact privado del operador, «Prueba PB-40», en https://claude.ai/artifact/C8hsnikkiBUjq68BVy5Fya. Se arma con `.docs/tickets/T-186/kit_pb40/armar.py` a partir de `.docs/tickets/T-186/kit_pb40/plantilla_prueba.html`.
  - **Cómo se usa:** la maneja quien dirige la prueba, en su propio dispositivo. A cada persona se le da un código (P01…); no se guarda ningún nombre.
  - **Lectura:** el informe se muestra tal cual se entrega y el reloj corre hasta que la persona pulsa «He terminado de leer».
  - **Cuestionario:** cinco preguntas de elección única, con el informe ya oculto. Cada pregunta tiene «No lo sé» y el orden de las opciones se baraja por participante. La quinta es la de recomendación personal: elegir un «Sí» cuenta como interpretarlo como recomendación.
  - **Resultados:** cada participante queda en el almacén del Artifact (colección `participaciones`). La pestaña «Resultados» calcula la mediana, el porcentaje de aciertos, cuántos lo toman por recomendación y el veredicto, que solo se da con 10 participantes o más.
- **Respuestas correctas:** salen del propio informe. La clave está en `PREGUNTAS` dentro de la plantilla.

## Cuando el operador la haya pasado

Claude lee el almacén del Artifact y escribe el resultado en el `pruebas.md` del ticket: mediana, porcentaje, recomendación, tabla por pregunta y por participante. Después actualiza PB-40 en `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json` y regenera las evidencias. Si no se cumple el criterio, abre un ticket con lo que haya que cambiar en el informe visual (plantilla o redacción de AG-17).

## Registro

- 2026-11-18 · claude · Kit preparado y página publicada (privada). El almacén de resultados está vacío.
