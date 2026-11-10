# T-80 · Análisis técnico

## Causa raíz o motivo

La Constitución V0.6 ratificó D-28 (vía `DIRECTA` y modo `CONSULTA`) después de que se escribiera el Orquestador. La pasada de coherencia de la V0.67 (PC3-01) lo dejó como CONTRADICE: `detectar()` solo admitía `DISCRECIONAL` y `SISTEMATICA`, y todo expediente nacía `DETECTADA`.

## Evidencia

- `entrega_claude/V0.67/scripts/pc3_01_via_directa.py` daba FALLA con la V0.67.
- `entrega_claude/V0.68/scripts/pc3_01_via_directa.py` da CUMPLE con la V0.68.

## Implementación

- **`validador/orquestador.py`:**
  - `abrir_directa`, `consultar`, `analisis_vigentes`, `consultas_ok`, `_origen_reutilizable`, `_analisis_vigente`, `_candidato_d`, `_dif_cortes` y `_anota_sc5`;
  - `emitir_encargo` se parte en `_emitir`, con `nace` para el expediente que nace con su encargo;
  - `comparar` se parte en `_comparar`, con `motivo_unico` para E;
  - la identidad de los `DIRECTA` se amplía y `_identidad_ok` acepta el encargo de la reutilización;
  - `integridad`, `_rota` y `cabezas` incluyen el rastro;
  - `detectar` remite a `abrir_directa` cuando le piden `DIRECTA`.
- **`validador/migraciones.py`:** `ESQUEMA_V0_68` y MIG-006. **`validador/esquemas_codigo.json`:** el esquema V0.68 registrado.
- **Pruebas:**
  - `pruebas/pruebas_via_directa_t80.py`, nueva;
  - `pruebas/pruebas_integracion_v053.py`: esquema actual V0.68 y cadenas hasta MIG-006, sin debilitar lo de V0.67.
- **Documentos:** LEEME del marco y Documento 0 de la V0.68.
- **Decisiones y desviaciones:**
  - Por E, el historial deja los pasos `VALIDADA` → `COMPARADA` en la misma llamada. El expediente aparece `COMPARADA` y la cadena deja auditada la comparación frente al benchmark.
  - «Se devuelve a D» se implementa como un rechazo explícito (O-22 con `devolver_a`), no como un nacimiento silencioso en otro estado.
  - El análisis de nivel bajo de D lo encarga el Broker (el Orquestador no redacta encargos) y el Orquestador exige que sea de nivel bajo.
- **Límites conocidos:** ver el Documento 0, §7 (T-87).
- **Comandos:**
  - `python3 -I pruebas/pruebas_via_directa_t80.py`;
  - `.docs/scripts/pruebas_marco.sh`;
  - el gate completo: `.docs/scripts/gate.sh` con la opción `--completo`.
