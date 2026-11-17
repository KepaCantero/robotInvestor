"""T-165 r03 · falsos positivos y escapes de G3-MET-13 con el enfoque estructural, con el Catálogo real (81 fichas IMPLEMENTADO,
ninguna VALIDADO).

Mide en las dos direcciones:
- banco 3 (nuevo, escrito después de la r03 y no usado para cambiar nada): 30 frases legítimas de análisis que nombran fichas y no
  usan la raíz «valid-», 15 legítimas que sí la usan en otro sentido y 15 madurez falsas;
- todas las frases legítimas y falsas de los bancos anteriores: `r02_bancos_frases.py` (implementador) y `revisores/r01_01`,
  `revisores/r02_01` (revisor), con los ejemplos de `estado_madurez_metodos` de los prompts.

Con la r03 una frase legítima bloquea si y solo si lleva la raíz «valid-» (o «implement-» con una ficha por debajo de
IMPLEMENTADO) junto a un método, o nombra una ficha que el Motor no sirve sin su forma canónica: el script lo comprueba.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python ../../.docs/tickets/T-165/r03_bancos_frases.py
"""
import importlib.util
import re
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path.cwd()))
from bloque_a import sintesis as sint

B = SimpleNamespace(motor=SimpleNamespace(raiz=None))
T165 = Path(__file__).resolve().parent
RAIZ_VALID = re.compile(r"(?<![a-záéíóúüñ])(?:re|con|pre)?valid", re.IGNORECASE)

LEGITIMAS_3_SIN_RAIZ = [
 "El precio está en el percentil 92 % de sus tres últimos años (ST-DESC-001), lo que pide prudencia en la entrada.",
 "La caída máxima de los últimos tres años (RISK-DD-001) fue del 31 %, por encima de la media de la clase.",
 "El impulso a doce meses (ACC-MOM-001) sigue positivo, aunque se ha moderado en las cuatro últimas semanas.",
 "La volatilidad realizada de 20 sesiones (FX-VOL-001) está en mínimos del año.",
 "Con FX-TREND-001 la media de 26 semanas apunta al alza; el cruce se produjo en marzo.",
 "La tasa de crecimiento anual compuesta (FIN-CAGR-001) del índice es del 7,8 % en diez años.",
 "Hemos contrastado la serie del proveedor con la del banco central antes de calcular ST-DESC-001.",
 "El cálculo de RISK-DD-001 se comprobó con la serie semanal y con la diaria: coinciden.",
 "Los clústeres de ML-CLUS-001 agrupan las tres opciones de bolsa estadounidense en uno.",
 "La prima de riesgo (IDX-ERP-001) es la más baja desde 2007.",
 "El diferencial de crédito (FIR-SPREAD-001) se ha estrechado 40 puntos básicos en el trimestre.",
 "El carry de la divisa (FX-CARRY-001) compensa una depreciación de hasta el 3 % anual.",
 "Según la paridad de poder adquisitivo (FX-PPA-001) el yen está barato frente al dólar.",
 "La pendiente de la curva (TCV-SLOPE-001) volvió a ser positiva en mayo.",
 "La tesis se invalida si el precio cierra dos semanas bajo la media de 26 semanas (FX-TREND-001).",
 "Invalidación: percentil por encima del 98 % (ST-DESC-001) con el impulso negativo.",
 "El riesgo sintético es 3/5 (RISK-DD-001) y la liquidez del vehículo es alta.",
 "La serie tiene huecos en 2020; ST-DESC-001 se calcula con la ventana disponible y lo declaramos.",
 "Lo que no sabemos: si la volatilidad (FX-VOL-001) seguirá baja tras la reunión del banco central.",
 "El factor común de las tres opciones es el dólar, según ML-CLUS-001.",
 "El percentil (ST-DESC-001) y la caída máxima (RISK-DD-001) apuntan en la misma dirección.",
 "La evolución del impulso (ACC-MOM-001) frente al ciclo anterior es neutra.",
 "El modelo de la curva se apoya en TCV-SLOPE-001 y en la inflación implícita.",
 "Revisamos la ficha ST-DESC-001 del Catálogo antes de usarla: la ventana es de tres años.",
 "Confirmado por el dato de empleo, el escenario base sigue siendo el de aterrizaje suave (ST-DESC-001 en el 60 %).",
 "El indicador de seguimiento es el precio semanal; el umbral sale de ST-DESC-001.",
 "La estrategia de carry (FX-CARRY-001) sufre cuando sube la volatilidad.",
 "Probado el escenario adverso, la caída máxima (RISK-DD-001) sería del 40 %.",
 "Verificamos que el cálculo de FIN-CAGR-001 usa precios ajustados por dividendos.",
 "El análisis por clúster (ML-CLUS-001) reduce las apuestas independientes de 12 a 7.",
]
LEGITIMAS_3_CON_RAIZ = [
 "La ruptura del máximo anual quedó validada por el volumen; el percentil (ST-DESC-001) es 97 %.",
 "El dato de inflación validó la tesis de desinflación, con la curva (TCV-SLOPE-001) en positivo.",
 "La validez de la tesis depende del crédito: el diferencial (FIR-SPREAD-001) es el indicador.",
 "Ningún método del ciclo está validado: ST-DESC-001 y RISK-DD-001 están implementados.",
 "ST-DESC-001 no está validado fuera de muestra.",
 "El soporte de 4.200 puntos se ha validado tres veces; el impulso (ACC-MOM-001) es positivo.",
 "El operador validó el perfil de riesgo; el riesgo sintético es 2/5 (RISK-DD-001).",
 "La señal de compra, validada por el cierre semanal, coincide con FX-TREND-001.",
 "Es una hipótesis válida y validable: el carry (FX-CARRY-001) la sostiene.",
 "El escenario del consenso, validado por los futuros, deja el percentil (ST-DESC-001) en el 70 %.",
 "VOL-GARCH-001 está implementado y su validación está pendiente.",
 "La lectura técnica se valida con el cierre del viernes; el percentil (ST-DESC-001) es 85 %.",
 "Los datos del proveedor están validados por su auditor; ST-DESC-001 los usa.",
 "Validamos la serie con otra fuente antes de calcular RISK-DD-001.",
 "La entrada se revalida cada semana con el impulso (ACC-MOM-001).",
]
FALSAS_3 = [
 "ST-DESC-001 es un método validado por el Evaluador.", "La caída máxima sale de RISK-DD-001, ya validada en tres crisis.",
 "ACC-MOM-001 superó la validación fuera de muestra con buena nota.", "Validado: FX-TREND-001 (10 años de datos).",
 "El clúster de ML-CLUS-001, una herramienta validada, deja 7 apuestas.", "ST_DESC_001 está validada.",
 "FIN-CAGR-001 [madurez: VALIDADO] da un 8 %.", "La ficha fx.vol.001 es fiable y está validada.",
 "Este cálculo está validado en backtest.", "ST-DESC-001 cuenta con una validación completa.",
 "IDX-ERP-001: validated out of sample.", "La prima sale de IDX-ERP-001.\n\nEs un modelo validado.",
 "| Ficha | Madurez |\n|---|---|\n| RISK-DD-001 | validada |", "ST-DESC-0001 se validó en 2025.",
 "FIR-SPREAD-001 revalidado con datos de 2024.",
]


def _cargar(nombre):
    spec = importlib.util.spec_from_file_location(nombre, T165 / "revisores" / f"{nombre}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _res(t):
    return sint._comprobar_met13(B, [("r", t, "BLOQUEO")])["resultado"]


def medir(nombre, legitimas, falsas, detalle=False):
    fp = [t for t in legitimas if _res(t) != "OK"]
    fn = [t for t in falsas if _res(t) != "BLOQUEO"]
    sin_raiz = [t for t in fp if not RAIZ_VALID.search(t)]
    print(f"{nombre}: legítimas que bloquean {len(fp)} de {len(legitimas)} ({len(sin_raiz)} sin la raíz «valid-») · "
          f"falsas que pasan {len(fn)} de {len(falsas)}")
    for t in (fp if detalle else sin_raiz):
        print("  FP:", t.replace("\n", "⏎"))
    for t in fn:
        print("  FN:", t.replace("\n", "⏎"))
    return fp, fn


if __name__ == "__main__":
    sys.path.insert(0, str(T165))
    import r02_bancos_frases as r02

    r01 = _cargar("r01_01_ataques_texto")
    r02r = _cargar("r02_01_ataques_nuevos")
    medir("banco 3 · legítimas sin la raíz (sin ajustar)", LEGITIMAS_3_SIN_RAIZ, FALSAS_3, detalle=True)
    medir("banco 3 · legítimas con la raíz (sin ajustar)", LEGITIMAS_3_CON_RAIZ, [], detalle=True)
    medir("r02 bancos 1 y 2 del implementador", r02.LEGITIMAS_1 + r02.LEGITIMAS_2, r02.FALSAS_1 + r02.FALSAS_2)
    medir("r01_01 del revisor (texto)", list(r01.FP.values()) + list(r01.CONTROL_OK.values()) + r01.EJEMPLOS,
          list(r01.ESCAPA_TEXTO.values()) + list(r01.CONTROL_BLOQUEA.values()))
    medir("r02_01 del revisor (texto)", list(r02r.FP.values()) + r02r.CONTROL_OK,
          list(r02r.ESCAPA.values()) + r02r.CONTROL_BLOQUEA)
