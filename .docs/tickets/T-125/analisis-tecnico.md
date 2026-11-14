# T-125 · Análisis técnico

## Motivo

PB-46 era uno de los tres casos del plan «sin prueba» y la funcionalidad no existía (FUE- no se escribía nunca). Es un hueco menor de la deuda que el operador pidió completar.

## Implementación

- `evaluador.py`: `_campos_pronostico_fuente`, `Evaluador.pronosticos_de_fuentes`, `_cierre_en` y `fiabilidad_fuentes`; `ciclo` devuelve `fiabilidad_fuentes`.
- `orquestacion.py`: `_comunicar_fiabilidad` (CT-19 a AG-16) tras el informe de aprendizaje; `_registrar_evidencia_clase` guarda `pronostico_fuente` en la CLM cuando la pieza es PRONOSTICO_FUENTE.
- `config/por_defecto.yaml`: sección `fiabilidad_fuentes`.
- Decisiones `[PROPUESTO]` (INC-T125-01): mínimo de 5 pronósticos; ventana de 24 meses; probabilidad 0,7 para un pronóstico explícito sin ella; referencia ingenua 0,5; antigüedad máxima del cierre la de H2 (3 días); una FUE- por fuente y mes.
- Límites: la recalificación de Q y el orden en F9 los hace el Buscador con el modelo real (fuera del ejecutor); con el cliente simulado no se generan piezas PRONOSTICO_FUENTE, así que en un ciclo normal no sale ninguna FUE-.
- Comandos: desde `bloque_a/11_Ejecutor`, `python -m pytest -q tests/test_t125_fiabilidad_fuentes.py`.
