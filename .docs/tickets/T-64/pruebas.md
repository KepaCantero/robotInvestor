# T-64 · Resultado sobre T-63

**Incidente ficticio:** 10 de marzo de 2025. **Decisión:** 20 de marzo. Se ejecutaron el almacén F2, el catálogo de contraste y la función de cierre del ejecutor en un entorno temporal nuevo por caso. La fecha de disponibilidad coincide con la publicación en estos ejemplos.

| Informe | Fecha observada | Publicado | Alta local | Esperado | Observado |
| --- | --- | --- | --- | --- | --- |
| Informe anterior | 28 feb | 5 mar | 5 mar | Abierta | Cerrada |
| Recuperación de los pedidos afectados | 17 mar | 18 mar | 18 mar | Cerrada | Cerrada |
| Informe posterior al corte | 17 mar | 25 mar | 25 mar | Abierta | Abierta |
| Publicación reciente sobre febrero | 28 feb | 18 mar | 18 mar | Abierta | Cerrada |
| Control de importación con fecha futura | 17 mar | 25 mar | 20 mar | Abierta | Cerrada |

El último caso introduce deliberadamente un registro incoherente para simular un histórico precargado. Es una prueba de resistencia, no evidencia de que los datos de producción estén contaminados.

Ejecutar desde la raíz con el entorno Python del proyecto:

```sh
.docs/scripts/fechas_evidencia_b.sh
```

En la base 76cdc40 se obtuvieron tres discrepancias entre cinco casos y el programa devolvió 1. Ese código permite repetir el mismo ensayo después de la futura corrección. Se midió el cierre de la objeción, sin invocar modelos reales ni emitir recomendaciones de cartera.

Los doce controles existentes del repositorio pasaron sin omisiones, incluidas 152 pruebas de B. El diagnóstico de fechas es independiente de esos controles y sus tres discrepancias siguen abiertas.

## Después de la corrección

Se repitió el mismo diagnóstico, con fecha_incidente en el objeto estructurado y sin modificar las fechas ni las expectativas. Resultado: cero discrepancias en cinco casos. En el informe anterior y en el informe reciente sobre febrero, la referencia queda visible como antecedente y la objeción queda abierta. El 18 de marzo puede cerrarse con la medición del 17. La publicación del 25 queda fuera del catálogo tanto en almacenamiento cronológico como en una importación precargada.

Se añadieron 15 pruebas automáticas en test_fechas_evidencia.py: diez sobre fechas ausentes, imposibles en su secuencia, formatos, embargo y frontera horaria del corte; cuatro por la entrada de notas del analista, el registro y la entrega a C para un eslabón; y una sobre reanudación de un cierre heredado sin fechas. El caso del mismo día y el del incidente desconocido quedan abiertos. En las cajas se comprueban las fechas y el motivo.

Revalidación final: 167 pruebas de B frente a 152 antes, 58 de A y 68 de Forex; pasaron los doce controles sin omisiones y las 50 suites del marco global en copia temporal. La cuota de Ruff baja de 3482 a 3481. Estos resultados son de Astra, con QA independiente pendiente.
