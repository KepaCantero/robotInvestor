# T-87 · Evidencia de pruebas locales

Desde la raíz del repositorio, con las dependencias del proyecto en `.venv`, ejecutar:

```sh
bash .docs/scripts/gate.sh --completo
.venv/bin/python -m pytest -q bloque_a/11_Ejecutor/tests/test_t87_*.py
.venv/bin/python -m pytest -q bloque_a/10_Herramientas/tests
```

Las 43 regresiones nuevas se reparten en 14 de agentes, 11 de datos, 10 de contratos y 8 de controles. Las de herramientas canónicas dieron 135 pruebas y 38 subpruebas correctas, incluido el verificador de enlaces con un servidor local. Las comprobaciones de estilo y tipos respetan las cuotas del repositorio (3103 hallazgos de Ruff y 116 de mypy en A). Son cuotas de deuda existente.

Para reproducir el ensayo semanal desde la raíz, con una salida temporal nueva por ejecución:

```sh
ejecutor=bloque_a/11_Ejecutor
salida=$(mktemp -d)
PYTHONPATH="$ejecutor" .venv/bin/python -m bloque_a.cli \
    --datos "$ejecutor/ejemplos/datos_sinteticos" --cliente mock --salida "$salida" \
    backtest --desde 2026-07-03 --hasta 2026-07-24 --frecuencia semanal
```

Resultado observado con el perfil por defecto: cuatro ciclos completos, cuatro señales y dos pronósticos, uno resuelto. Este ensayo verifica la ejecución con series sintéticas. La revisión del encargo A→B admitió el borrador de India para el universo coincidente y lo dejó pendiente de autorización. Ver condiciones y casos negativos en [contratos](contratos.md).

Para el marco común de C, ejecutar `bash .docs/scripts/pruebas_marco.sh` con Bash 4 o posterior en una copia desechable con las dependencias disponibles. Algunas suites escriben archivos de prueba.

Validación del 10-11-2026: los 12 controles del repositorio pasaron, sin fallos ni omisiones. Pasaron las 244 pruebas del Bloque A, las 68 de Forex y las 174 del Bloque B. En la copia desechable pasaron las 56 suites del marco común de C.
