"""T-165 r02 · dos bancos de frases nuevos (ni del ticket ni del revisor) para medir G3-MET-13 en las dos direcciones, con el
Catálogo real (81 fichas IMPLEMENTADO, ninguna VALIDADO).

- Banco 1: se usó para ajustar la r02 (dato o estrategia como sujeto, una persona como sujeto, la ficha entre la negación y la
  palabra). Antes del ajuste: 5 de 20 legítimas bloqueaban; después, 1 (aceptada).
- Banco 2: escrito después del ajuste y no usado para cambiar nada: la cifra honesta.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python ../../.docs/tickets/T-165/r02_bancos_frases.py
"""
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path.cwd()))
from bloque_a import sintesis as sint

B = SimpleNamespace(motor=SimpleNamespace(raiz=None))


def medir(nombre, legitimas, falsas):
    fp = [t for t in legitimas if sint._comprobar_met13(B, [("r", t, "BLOQUEO")])["resultado"] != "OK"]
    fn = [t for t in falsas if sint._comprobar_met13(B, [("r", t, "BLOQUEO")])["resultado"] != "BLOQUEO"]
    print(f"{nombre}: legítimas que bloquean {len(fp)} de {len(legitimas)} · falsas que pasan {len(fn)} de {len(falsas)}")
    for t in fp:
        print("  FP:", t)
    for t in fn:
        print("  FN:", t)


LEGITIMAS_1 = [
 "El percentil (ST-DESC-001) confirma que el precio está caro.",
 "Con ST-DESC-001 en el percentil 90, la valoración exige cautela; el dato de PMI fue validado por la oficina estadística.",
 "La caída máxima (RISK-DD-001) es moderada. El modelo macro del BCE está validado por su comité.",
 "Riesgo sintético 3/5 (RISK-DD-001). La previsión del consenso quedó validada en la última reunión.",
 "FX-CARRY-001 indica carry positivo; la estrategia fue probada en la crisis de 2008 por muchos gestores.",
 "La tendencia (FX-TREND-001) es alcista y el cruce de medias quedó confirmado.",
 "VOL-GARCH-001 estima la volatilidad; su validación fuera de muestra está pendiente.",
 "ST-DESC-001: implementado (sin validación independiente).",
 "El método ST-DESC-001 está implementado; no ha sido validado.",
 "Momentum (ACC-MOM-001) positivo. El rebote fue validado por el volumen.",
 "ML-CLUS-001 agrupa las series; los clústeres no están validados todavía.",
 "El escenario de tipos, contrastado con el mercado de futuros, encaja con FIR-CURVE-001.",
 "El cálculo FIN-CAGR-001 da un 8 % anual; la cifra está documentada en el anexo.",
 "| ST-DESC-001 | implementado | validación pendiente |",
 "La hipótesis de desinflación, verificada en los datos de mayo, apoya el carry (FX-CARRY-001).",
 "El soporte técnico se comprobó dos veces; el percentil (ST-DESC-001) es 40.",
 "Hasta que FX-PPA-001 esté validado, la paridad se usa solo como contexto.",
 "IDX-ERP-001 implementado; documentación completa en el Catálogo.",
 "El usuario ha validado su perfil de riesgo. El riesgo (RISK-DD-001) es 2/5.",
 "La señal de FX-TREND-001 no está confirmada ni validada.",
]
FALSAS_1 = [
 "ST-DESC-001 está validado.", "El percentil sale de ST-DESC-001, cuya validación fue satisfactoria.",
 "VOL-GARCH-001 quedó plenamente validado tras el backtest.", "FX-TREND-001: validado (10 años).",
 "Según el Catálogo, ML-CLUS-001 está validado.", "El modelo (ACC-MOM-001) ha sido verificado con datos reales.",
 "RISK-DD-001 es un método probado.", "Usamos FIR-CURVE-001, ya validada por el Evaluador.",
 "FX-CARRY-001\n\nEste método está validado en backtest.", "| Ficha | Estado |\n|---|---|\n| FIN-CAGR-001 | VALIDADO |",
 "ST‐DESC‐001 validada.", "st desc 001 validado", "VOL-GARCH validado.", "FX-PPA-001 se validó en 2024.",
 "Los métodos FX-PPA-001 y FX-COINT-001 fueron validados.",
]

LEGITIMAS_2 = [
 "El diferencial de crédito (FIR-SPREAD-001) se amplía; la lectura del mercado quedó validada por el dato de quiebras.",
 "Según IDX-ERP-001 la prima es baja. La tesis de rotación sectorial fue confirmada por los flujos.",
 "La curva (FIR-CURVE-001) se empina, en línea con el recorte implementado por la Reserva Federal.",
 "TCV-SLOPE-001 implementado; su calibración con datos reales está pendiente.",
 "La política documentada del banco central apunta a recortes; el carry (FX-CARRY-001) sigue positivo.",
 "El rango de 1,05 a 1,10 fue validado varias veces; la volatilidad (FX-VOL-001) es baja.",
 "Momentum (ACC-MOM-001) del 12 %. El movimiento quedó verificado al cierre semanal.",
 "Ningún método del Catálogo está validado todavía; usamos ST-DESC-001 (implementado).",
 "ST-DESC-001 todavía no se ha podido validar fuera de muestra.",
 "El precio, en el percentil 80 (ST-DESC-001), supera el máximo validado de 2021.",
 "VOL-GARCH-001: implementado. Validación fuera de muestra: pendiente.",
 "La subida de tipos ya implementada por el BCE reduce el carry (FX-CARRY-001).",
 "El objetivo de inflación fue verificado en las actas; la curva (FIR-CURVE-001) lo descuenta.",
 "| Indicador | Ficha | Estado |\n|---|---|---|\n| Percentil | ST-DESC-001 | implementado |",
 "El inversor validó el plan; el riesgo (RISK-DD-001) es 3/5.",
]
FALSAS_2 = [
 "La prima (IDX-ERP-001) es fiable: el método fue validado con 30 años de datos.",
 "FIR-SPREAD-001 ha sido validado.", "Se usa TCV-SLOPE-001, que ya superó la validación.",
 "ACC-MOM-001 (validado en 2025) marca un 12 %.", "El cálculo de ST-DESC-001 está verificado.",
 "Ficha VOL‐GARCH‐001: validada.", "FX-VOL-001.\n\nMétodo validado.", "La ficha fx-vol-001 se validó en enero.",
 "{IDX-ERP-001} validado", "RISK-DD-001 — comprobado en tres crisis.",
]

if __name__ == "__main__":
    medir("banco 1 (ajuste)", LEGITIMAS_1, FALSAS_1)
    medir("banco 2 (sin ajustar)", LEGITIMAS_2, FALSAS_2)
