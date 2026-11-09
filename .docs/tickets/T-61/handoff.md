# T-61 · Traspaso

## 2026-11-09 · de Astra a Claude

- **Fase:** revisión independiente. El cambio de código está en 4bbc952. Esta rama incorpora la organización de a6ceb76.
- **Encargo:** partir del [plan](README.md) y del código del Bloque B. Comprobar los límites entre objeciones de empresa y de sector, los valores de tipo incorrecto, los archivos de precios ausentes o vacíos y los periodos solapados.
- **Evidencia:** [pruebas del implementador](pruebas.md). El experimento del crítico usa datos ficticios. La evaluación de modelos reales y los datos del BCE quedan fuera.
- **Reproducción:** usar `.docs/scripts/gate.sh` con la opción `--completo` y `.docs/scripts/pruebas_marco.sh`. Registrar la revisión propia en [qa.md](qa.md).
