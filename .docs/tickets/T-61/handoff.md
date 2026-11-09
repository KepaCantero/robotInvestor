# T-61 · Traspaso

## 2026-11-09 · de Astra a Claude

- **Fase:** revisión independiente. El cambio de código está en 4bbc952. Esta rama incorpora la organización de a6ceb76.
- **Encargo:** partir del [plan](README.md) y del código del Bloque B. Comprobar los límites entre objeciones de empresa y de sector, los valores de tipo incorrecto, los archivos de precios ausentes o vacíos y los periodos solapados.
- **Evidencia:** [pruebas del implementador](pruebas.md). El experimento del crítico usa datos ficticios. La evaluación de modelos reales y los datos del BCE quedan fuera.
- **Reproducción:** usar `.docs/scripts/gate.sh` con la opción `--completo` y `.docs/scripts/pruebas_marco.sh`. Registrar la revisión propia en [qa.md](qa.md).

## Ampliación · archivo de precios vacío

Revisar también el caso de cero bytes en HT-01 y su prueba de regresión. El cambio se entrega en la rama astra/bloque-b-objeciones-y-evaluacion para revisión de Claude.

## Revisión de Claude · cobertura y comparación con el azar

Rama `astra/bloque-b-backtesting-cobertura-y-azar`, con base en `astra/bloque-b-objeciones-y-evaluacion`. La comparación entre ambas ramas aísla las mejoras de backtesting posteriores a T-61.

- Contrastar en los dos modos que el universo se fija en la fecha de selección, que se mantienen el tamaño y las restricciones del grupo original, y que los empates y los periodos con precios ausentes reciben el tratamiento documentado.
- Comprobar en los CSV los recuentos de elegidos y evaluados y el desfase en días naturales del último cierre. En las métricas, distinguir todos los periodos evaluables de aquellos con selección completa.
- Verificar que las optimizaciones de fechas, lectura de candidatos y pesos conservan los resultados. El control completo pasó 12/12, con 58 pruebas de A, 68 de A Forex y 141 de B. En el ejemplo simulado de acciones de enero de 2025 la selección superó a 104 de 111 grupos admisibles.

Pendiente de revisión independiente.
