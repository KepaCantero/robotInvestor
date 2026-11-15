"""QA r01 de T-131 · `comprobar_datos_a.py` con carpetas estropeadas: ¿da el estado que daría el ejecutor?

Cada caso copia los datos de ejemplo de un símbolo a una carpeta temporal, los estropea y compara el estado del script con
lo que hace HT-01 (`ProveedorCSV`) del ejecutor. Además: H1 un lunes con el último cierre del viernes (el ejecutor cuenta
sesiones en H1, `orquestacion._sesiones_entre`), el código de salida y la salida de la orden de pruebas.md.
Uso (desde la raíz): python -I r01_01_carpetas_estropeadas.py
"""
import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[4]
EJE = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJE))
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

spec = importlib.util.spec_from_file_location("cd", RAIZ / ".docs" / "scripts" / "comprobar_datos_a.py")
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)
DATOS = EJE / "ejemplos" / "datos_sinteticos"
U = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
OK, FALLOS = 0, []


def comprobar(cond, msg):
    global OK
    OK += cond
    if not cond:
        FALLOS.append(msg)
    print(f"  {'ok   ' if cond else 'FALLA'} {msg}")


def caso(nombre, estropear, esperado, as_of="2024-03-29", horizonte="H3"):
    u = U.head(1)
    s = u["simbolo"].iloc[0]
    d = Path(tempfile.mkdtemp(prefix="qa_t131_"))
    shutil.copy(DATOS / f"{s}.csv", d / f"{s}.csv")
    estropear(d / f"{s}.csv")
    try:
        f = cd.comprobar(d, u, as_of, horizonte)[0]
        estado, motivo = f["estado"], f["motivo"]
    except Exception as e:  # noqa: BLE001
        estado, motivo = f"EXCEPCIÓN {type(e).__name__}", str(e)[:100]
    comprobar(estado in esperado, f"{nombre:48} → {estado} {motivo[:70]!r} (esperado {'/'.join(esperado)})")
    shutil.rmtree(d)


def reescribir(fn):
    def _(p):
        df = pd.read_csv(p)
        fn(df).to_csv(p, index=False)
    return _


print("1. carpetas estropeadas")
caso("vacío", lambda p: p.write_text("", encoding="utf-8"), {"INVALIDO"})
caso("solo cabecera", lambda p: p.write_text("fecha,cierre\n", encoding="utf-8"), {"INVALIDO", "FALTA"})
caso("binario", lambda p: p.write_bytes(b"\x00\xff" * 50), {"INVALIDO"})
caso("separador ;", lambda p: p.write_text(p.read_text(encoding="utf-8").replace(",", ";"), encoding="utf-8"), {"INVALIDO", "OK"})
caso("fechas duplicadas", reescribir(lambda df: pd.concat([df, df.tail(3)])), {"INVALIDO"})
caso("fechas desordenadas", reescribir(lambda df: df.iloc[::-1]), {"OK", "INVALIDO"})
caso("cierre con NaN en la última fila", reescribir(lambda df: df.assign(cierre=df["cierre"].where(df.index < len(df) - 1))),
     {"INVALIDO", "OK", "ANTIGUO"})
caso("cierre negativo", reescribir(lambda df: df.assign(cierre=-df["cierre"])), {"INVALIDO"})
caso("cierre cero", reescribir(lambda df: df.assign(cierre=0.0)), {"INVALIDO"})
caso("cierre de texto", reescribir(lambda df: df.assign(cierre="n/d")), {"INVALIDO"})
caso("fechas con zona horaria", reescribir(lambda df: df.assign(fecha=df["fecha"].astype(str) + "T00:00:00+02:00")), {"INVALIDO"})
caso("fechas imposibles", reescribir(lambda df: df.assign(fecha="2024-02-30")), {"INVALIDO"})
caso("todo posterior a as_of", reescribir(lambda df: df.assign(fecha=pd.to_datetime(df["fecha"]) + pd.Timedelta(days=4000))),
     {"FALTA", "INVALIDO"})
caso("cabecera Date/Close con BOM", lambda p: p.write_text(
    "﻿" + p.read_text(encoding="utf-8").replace("fecha", "Date", 1).replace("cierre", "Close", 1), encoding="utf-8"), {"OK"})
caso("un hueco de 40 días (H3)", reescribir(lambda df: df[(pd.to_datetime(df["fecha"]) < "2024-01-10")
                                                          | (pd.to_datetime(df["fecha"]) > "2024-02-19")]), {"OK"})

print("2. antigüedad en H1: último cierre el viernes, as_of el lunes (el ejecutor cuenta sesiones en H1)")
caso("H1, viernes 2024-03-22 → lunes 2024-03-25", reescribir(lambda df: df[pd.to_datetime(df["fecha"]) <= "2024-03-22"]),
     {"OK"}, as_of="2024-03-25", horizonte="H1")
sys.path.insert(0, str(EJE))
from bloque_a import orquestacion  # noqa: E402
fest = cargar_config()["ps2_festivos"]
try:
    ses = orquestacion._sesiones_entre("2024-03-22", "2024-03-25", orquestacion._festivos(fest) if hasattr(orquestacion, "_festivos") else fest)
    print(f"     sesiones entre el viernes y el lunes según el ejecutor: {ses}")
except Exception as e:  # noqa: BLE001
    print(f"     (no se pudo llamar a _sesiones_entre: {type(e).__name__}: {e})")

print("3. la orden de pruebas.md")
p = subprocess.run([sys.executable, str(RAIZ / ".docs" / "scripts" / "comprobar_datos_a.py"), str(DATOS), "--as-of", "2024-03-29"],
                   capture_output=True, text=True, cwd=RAIZ)
comprobar(p.returncode == 0 and "57 de 57 símbolos OK" in p.stdout, f"datos de ejemplo: código {p.returncode}, "
          f"{[x for x in p.stdout.splitlines() if 'símbolos OK' in x]}")
p = subprocess.run([sys.executable, str(RAIZ / ".docs" / "scripts" / "comprobar_datos_a.py"), str(DATOS), "--as-of", "2027-06-30"],
                   capture_output=True, text=True, cwd=RAIZ)
comprobar(p.returncode == 1, f"con as_of 2027-06-30 (los datos acaban el 2026-10-30) todo ANTIGUO y código 1: código {p.returncode}")
p = subprocess.run([sys.executable, str(RAIZ / ".docs" / "scripts" / "comprobar_datos_a.py"), "/no/existe"],
                   capture_output=True, text=True, cwd=RAIZ)
comprobar(p.returncode != 0, f"carpeta inexistente: código {p.returncode} ({p.stderr.strip().splitlines()[-1][:90] if p.stderr else ''})")

print(f"\nr01_01 T-131: {OK} ok, {len(FALLOS)} fallos")
for f in FALLOS:
    print("  -", f)
