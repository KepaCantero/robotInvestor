"""QA r01 de T-145 · `comprobar_datos_a.py` (H-04 de la QA r01 de T-140): ANTIGUO cuando la ventana no tiene datos y la
historia sí, en los bordes. Se comprueba contra lo que hace el ciclo (`ini` de la ventana, la antigüedad PS2).

Uso (desde la raíz de la copia): python -I r01_03_comprobar_datos_bordes.py <carpeta temporal>
"""
import importlib.util
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJ))
import pandas as pd  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config, parametro  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

spec = importlib.util.spec_from_file_location("cd", RAIZ / ".docs" / "scripts" / "comprobar_datos_a.py")
CD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CD)
TMP = Path(sys.argv[1])
CFG = cargar_config()
SYM = "EURUSD=X"
U1 = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
U1 = U1[U1["simbolo"] == SYM].reset_index(drop=True)
BASE = pd.read_csv(EJ / "ejemplos" / "datos_sinteticos" / f"{SYM}.csv")
AS_OF = "2030-06-28"
corte = pd.Timestamp(AS_OF)
sen, tb = parametro(CFG, "senales"), parametro(CFG, "tasa_base")
INI = min(corte - pd.DateOffset(years=int(sen["ventana_anios"]), days=int(sen["margen_dias"])),
          corte - pd.DateOffset(years=int(tb["ventana_anios"])))
fallos = 0


def caso(nombre, filas, esperado, comprobar=None, horizonte="H3"):
    global fallos
    d = TMP / nombre.replace(" ", "_")[:40]
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    if filas is not None:
        df = BASE.head(len(filas)).copy() if len(filas) else BASE.head(0).copy()
        if len(filas):
            df["fecha"] = [str(f) for f, _ in filas]
            df["cierre"] = [c for _, c in filas]
        df.to_csv(d / f"{SYM}.csv", index=False)
    f = CD.comprobar(d, U1, AS_OF, horizonte, CFG)[0]
    ok = f["estado"] == esperado and (comprobar is None or comprobar(f))
    fallos += not ok
    print(f"  {'ok   ' if ok else 'FALLA'} {nombre:58} {f['estado']:8} hasta={f['hasta']} filas={f['filas']} · {f['motivo'][:90]}")


dia = pd.Timedelta(days=1)
print(f"ventana del ciclo desde {INI.date()} hasta {corte.date()}")
caso("sin archivo", None, "FALTA")
caso("archivo con la cabecera sola", [], "FALTA")
caso("historia que acaba un día antes de la ventana", [((INI - dia * 10).date(), 1.1), ((INI - dia).date(), 1.2)], "ANTIGUO",
     lambda f: f["hasta"] == str((INI - dia).date()) and f["filas"] == 0 and f["desde"] is None)
caso("último dato justo en el primer día de la ventana", [((INI - dia).date(), 1.1), (INI.date(), 1.2)], "ANTIGUO",
     lambda f: f["filas"] == 1 and f["hasta"] == str(INI.date()))
caso("solo datos posteriores a as_of", [((corte + dia).date(), 1.1), ((corte + 2 * dia).date(), 1.2)], "FALTA")
caso("historia antigua con el último cierre no numérico", [((INI - dia * 20).date(), 1.1), ((INI - dia * 10).date(), "n/d")],
     "ANTIGUO")
caso("historia antigua con un cierre negativo al final", [((INI - dia * 20).date(), 1.1), ((INI - dia * 10).date(), -3)], "ANTIGUO")
caso("historia antigua con fechas repetidas", [((INI - dia * 20).date(), 1.1), ((INI - dia * 20).date(), 1.2)], "ANTIGUO")
caso("antigua en H1 (antigüedad en sesiones)", [((INI - dia).date(), 1.1)], "ANTIGUO", lambda f: "sesiones" in f["motivo"],
     horizonte="H1")
caso("dato al día (control)", [((corte - dia * 400).date(), 1.0), (corte.date(), 1.1)], "OK")
print(f"\nfallos: {fallos}")
