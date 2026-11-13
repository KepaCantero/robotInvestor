# T-112 · Análisis técnico

## Implementación

| Grupo | Módulo | Fichas | Casos de control | Notas |
| --- | --- | --- | --- | --- |
| S · estadística y series | `motor/fichas_series.py` | ST-INF, FX-BRK, FX-STL, FX-REGIME, REG-HMM, FX-COINT, BIB-MET, TEM-DIFF | 36 | `grupo_S.md` |
| R · riesgo, simulación, backtest y modelos | `motor/fichas_riesgo.py` | RISK-VAR, SIM-MC, SCN-H, BT-DSR, BT-PBO, BT-VAR, ML-CAL, ML-PRED, DEC-VOI | 36 | `grupo_R.md` |
| V · valoración de RV, RF, FX y DER | `motor/fichas_valoracion.py` | ACC-ERP, ACC-FACT, ACC-VAL, FIR-PRICE, FIR-CURVE, FIR-CARRY, FIR-SPREAD, FX-MOM, FX-PPA, DER-OPT | 38 | `grupo_V.md` |
| P · inmobiliario, materias primas, cripto y alternativos | `motor/fichas_reales.py` | REI-CAP, REI-FFO, REI-NAV, CMD-INV, CMD-RETDEC, CHR-FLOW, CHR-FUND, ALT-DESMOOTH | 25 | `grupo_P.md` |
| Servicio | `motor/servicio.py` | AUD-REX-001 (CT-10) | 5 | Abajo |

Cada módulo sigue el patrón de T-106 y aplica desde el principio las correcciones de sus tres QA:
- `UMBRALES` fijos: una petición que traiga uno se rechaza;
- dominio de cada parámetro;
- la envoltura `_cerrado`, que traduce excepciones y rechaza los no finitos;
- advertencias en `resultado["advertencias"]`;
- casos de control que comprueban la identidad entera y pueden fallar;
- al menos un oráculo independiente por ficha;
- mutantes de la fórmula principal: mueren todos en los cuatro grupos (S 55, R 43, V 34, P 65).

**Integración en `servicio.py`, hecha por Claude:**
- **Módulos:** `MODULOS_FASE1` y `MODULOS_FASE2`. `FASE1`, `FASE2` y `ESTRICTAS = FASE1 | FASE2`: el Motor rechaza cualquier cifra no finita en todas ellas.
- **Semilla:** `ACEPTA_SEMILLA` reúne las fichas que declaran `semilla`, y la semilla de la petición llega a ellas.
- **BIB-MET-001:** `SOLICITANTES_FICHA` lo limita al Orquestador técnico (AG-18) y al Evaluador (AG-20), como dice la ficha. A cualquier otro le responde CANAL_NO_AUTORIZADO.
- **Código anterior:** ACC-ERP-001, FX-MOM-001 y REI-CAP-001 se rehicieron en sus módulos, porque el código anterior no cumplía la ficha. Se retiraron `f_erp`, `f_cap`, `f_fx_mom` y `_dif`, y `DOCUMENTADAS_CON_CODIGO` queda vacío.
- **AUD-REX-001 (CT-10):**
  - `SERVICIOS_CT10` y `_casos_aud_rex`, que trabaja en un Registro de cálculos aparte;
  - `reejecutar` exige motivo, reconstruye los valores en línea desde el artefacto con su huella, hace la doble pasada y clasifica según el esquema del RC V2.0 (INC-T112-02);
  - por CT-09, AUD-REX-001 responde que se pide por CT-10.
- **Catálogo:** `promover_fichas_catalogo.py` reconoce también «Implementado (heredado)», salta las ya promovidas y rehace el §1.3: 71 IMPLEMENTADO y 10 DOCUMENTADO.

## Decisiones de método

En INC-T112-01 `[PROPUESTO]`, a T-57. Detalle en las notas de cada grupo.

## Límites

- **Lentitud:** REG-HMM-001 con `n_estados: BIC` tarda unos 12 s por pasada con 300 observaciones, y el Motor hace dos. FIR-CURVE-001 tarda unos 1,5 s por llamada.
- **Sin datos reales:** las fichas reciben sus datos en `valores`, como en T-106. Las series de HT-01, solo donde la ficha las pide.
- **Artefactos anteriores:** un artefacto anterior a T-112 con datos en línea no se puede re-ejecutar, porque no guardaba los valores.
- **P2:** las 10 fichas P2 siguen DOCUMENTADO.

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/pytest -q tests/test_fase2_series.py tests/test_fase2_riesgo.py tests/test_fase2_valoracion.py tests/test_fase2_reales.py tests/test_t112_motor.py
../../.venv/bin/python -I ../../.docs/scripts/promover_fichas_catalogo.py --etiqueta "ejecutor, casos de control registrados (T-112)"
```
