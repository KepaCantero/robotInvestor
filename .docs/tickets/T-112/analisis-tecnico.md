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

## Ronda r02 (QA r01 NO APTO)

El detalle por grupo, con cada cota y su origen, está en la sección «Ronda r02» de `grupo_S.md`, `grupo_R.md`, `grupo_V.md` y `grupo_P.md`.

- **H-01 (alta):**
  - cada parámetro de tamaño de la petición tiene cota superior en `UMBRALES`, comprobada antes de calcular. Por ejemplo: réplicas ≤ 10 000 (FC-EVAL-001), trayectorias 1 000–1 000 000 (SIM-MC-001), horizonte ≤ H5 en sesiones (configuración), arranques de REG-HMM ≤ 50 y pasos de DER-OPT ≤ 1 000;
  - `servir` convierte también `MemoryError` y `RecursionError` en RECHAZADO con su entrada en RC;
  - con todas las cotas al máximo, el servicio más caro es REG-HMM-001, unos 4 min en dos pasadas y menos de 1 GB. Se declara en INC-T112-01.
- **H-02:** R y P rechazan, como S y V, las claves que no declaran (salvo `clase`).
- **H-03:** EVT-POT con una máxima verosimilitud propia de la GPD y el GARCH QMLE con Nelder-Mead, `xatol` = `fatol` = 1e-10. Un artefacto anterior con esos métodos ya no coincide en CT-10 a 1e-6.
- **H-04 y H-07:**
  - `servir`, `verificar_casos_control` y `reejecutar` añaden a `ent` la configuración del Motor y la fecha de corte;
  - DEC-VOI, ML-CAL, ML-PRED y SCN-H leen la configuración en cada llamada;
  - todas las fichas con datos fechados rechazan uno posterior al corte («no conocible»), y ACC-VAL también uno posterior a la fecha de valoración;
  - la fecha de corte entra en la clave de la caché. Si no entrara, una petición con un corte anterior se serviría desde la caché de otra con un corte posterior.
- **H-05:** dos semillas distintas (en la petición y en los parámetros) se rechazan, y el artefacto registra la usada. La comparación no usa un conjunto, para que una semilla no hashable no rompa `servir`.
- **H-06:** un solicitante que no es texto se rechaza con CANAL_NO_AUTORIZADO.
- **H-08:** pruebas con valores a mano para cada mutante vivo. AUD-REX-001 tiene un sexto caso con parámetros que cambian el resultado (`CASO_AUD_REX_PARAMETROS`, FON-DISC-001).
- **De paso:**
  - una fuga en los datos sintéticos de un caso de REI-NAV;
  - un borde numérico de GLM en ALT-DESMOOTH (factorización en banda);
  - DER-OPT con `pasos = 2`;
  - un LOESS por bandas en FX-STL (de 156 s a 6 s con 2 520 observaciones).

