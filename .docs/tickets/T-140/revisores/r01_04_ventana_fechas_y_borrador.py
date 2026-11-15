"""QA r01 de T-137 · comprobación de datos en la ventana del ciclo (H-05 de T-131), fechas fuera del calendario (H-19 de
T-134) y borrador del Anexo B (H-06 de T-131).

Uso (desde la raíz de la copia): python -I r01_04_ventana_fechas_y_borrador.py <carpeta temporal>
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
from bloque_a.evaluador import _fecha_de_calendario  # noqa: E402
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles, ProveedorCSV, cargar_universo  # noqa: E402


def modulo(nombre):
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ".docs" / "scripts" / f"{nombre}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


comprobar = modulo("comprobar_datos_a").comprobar
TMP = Path(sys.argv[1])
OK, FALLOS = 0, []


def ver(cond, msg):
    global OK
    OK += bool(cond)
    if not cond:
        FALLOS.append(msg)
    print(f"  {'ok   ' if cond else 'FALLA'} {msg}")


U = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
U1 = U[U["simbolo"] == "EURUSD=X"].reset_index(drop=True)
SYM = "EURUSD=X"
AS_OF = "2026-06-30"
CFG = cargar_config()


def carpeta(nombre, cambio):
    d = TMP / nombre
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    df = pd.read_csv(EJ / "ejemplos" / "datos_sinteticos" / f"{SYM}.csv")
    df["cierre"] = df["cierre"].astype(object)
    df = cambio(df)
    df.to_csv(d / f"{SYM}.csv", index=False)
    return d


def ini_del_ciclo(cfg, as_of):
    """La ventana con que `orquestacion.Bloque` valida un símbolo del universo (líneas de `senales`, T-65 H-08)."""
    ven = parametro(cfg, "senales")
    return str((pd.Timestamp(as_of) - pd.DateOffset(years=int(ven["ventana_anios"]), days=int(ven["margen_dias"]))).date())


def veredicto_ciclo(d, cfg=CFG):
    p = ProveedorCSV(d)
    p.fijar_as_of(AS_OF)
    try:
        p.cierres(SYM, ini_del_ciclo(cfg, AS_OF), AS_OF)
        p.valor_en(SYM, AS_OF)
        return "USA"
    except DatosNoDisponibles as e:      # DatosInvalidos incluido
        return f"EXCLUYE ({type(e).__name__})"


def malo_en(fecha, valor="n/d"):
    def cambio(df):
        f = pd.to_datetime(df["fecha"])
        df.loc[f == f[f >= fecha].min(), "cierre"] = valor
        return df
    return cambio


def _exacto(df, fecha):
    f = pd.to_datetime(df["fecha"])
    if not (f == fecha).any():
        df = pd.concat([df, pd.DataFrame([{"fecha": fecha, "cierre": 1.1}])]).sort_values("fecha")
        f = pd.to_datetime(df["fecha"])
    df.loc[f == fecha, "cierre"] = "n/d"
    return df


ini = ini_del_ciclo(CFG, AS_OF)
print(f"1. borde de la ventana (as_of {AS_OF}, la ventana del ciclo empieza el {ini})")
for nombre, fecha in (("en el primer día de la ventana", ini),
                      ("el día anterior a la ventana", str((pd.Timestamp(ini) - pd.Timedelta(days=1)).date()))):
    d = carpeta("borde_" + fecha, lambda df, fecha=fecha: _exacto(df, fecha))
    f = comprobar(d, U1, AS_OF)[0]
    ciclo = veredicto_ciclo(d)
    ver((f["estado"] == "OK") == (ciclo == "USA"), f"dato malo {nombre} ({fecha}): script {f['estado']}"
        f"{' con aviso' if f['aviso'] else ''} · ciclo {ciclo}")


print("2. otros datos malos anteriores a la ventana: OK con aviso, como usa el ciclo")
for nombre, cambio in (("cierre a cero en 2022", malo_en("2022-06-01", 0)),
                       ("fecha repetida en 2022", lambda df: pd.concat([df, df[df["fecha"] == df["fecha"].iloc[100]]]))):
    d = carpeta(nombre.replace(" ", "_"), cambio)
    f = comprobar(d, U1, AS_OF)[0]
    ver(f["estado"] == "OK" and f["aviso"] and veredicto_ciclo(d) == "USA", f"{nombre}: {f['estado']} · aviso «{f['aviso'][:70]}…»")

print("3. un símbolo que dejó de cotizar antes de la ventana (último cierre en 2022)")
d = carpeta("acaba_2022", lambda df: df[pd.to_datetime(df["fecha"]) < "2023-01-01"])
f = comprobar(d, U1, AS_OF)[0]
ver(f["estado"] == "ANTIGUO", f"estado {f['estado']} (el docstring: FALTA = «no hay archivo», ANTIGUO = último cierre demasiado "
    f"antiguo) · motivo «{f['motivo'][:60]}» · ciclo {veredicto_ciclo(d)}")

print("4. tasa_base.ventana_anios mayor que la de señales (configuración permitida): ¿qué valida cada uno?")
cfg5 = cargar_config()
cfg5["tasa_base"] = dict(cfg5["tasa_base"], ventana_anios=5)
d = carpeta("malo_2022_tb5", malo_en("2022-06-01"))
f = comprobar(d, U1, AS_OF, cfg=cfg5)[0]
print(f"     script {f['estado']} · el ciclo valida el símbolo en {ini_del_ciclo(cfg5, AS_OF)}…: {veredicto_ciclo(d, cfg5)}; la "
      "tasa base (sintesis.py → evaluador.tasa_base) lo lee desde 5 años antes")

print("5. fechas fuera del calendario (`_fecha_de_calendario`)")
for v in ("0000-01-01", "0000-12-31T23:59:59+05:00", "0000-06-15 12:00", "2026-02-29", "2026-13-01", "2026-01-01T24:00"):
    try:
        _fecha_de_calendario(v)
        ver(False, f"{v!r} se lee")
    except ValueError as e:
        ver(True, f"{v!r}: ValueError ({str(e)[:60]})")
    except Exception as e:  # noqa: BLE001
        ver(False, f"{v!r}: {type(e).__name__} (no ValueError)")
for v in ("0001-01-01", "9999-12-31", "1677-09-21", "2262-04-12", "2026-06-30T23:30:00-12:00"):
    try:
        t = _fecha_de_calendario(v)
        ver(t.tzinfo is None and str(t.date()) == v[:10], f"{v!r} se lee como {t.date()}")
    except Exception as e:  # noqa: BLE001
        ver(False, f"{v!r}: {type(e).__name__}: {e}")

print("6. borrador del Anexo B")
b = modulo("borrador_anexo_b").generar()
filas = {ln.split("|")[1].strip(): ln for ln in b.splitlines() if ln.startswith("| CT-")}
ver("Motor" in filas.get("CT-09.RETORNO", "") and "Motor" in filas.get("CT-10.RETORNO", ""), "CT-09 y CT-10: el retorno lo sirve el Motor")
ver("null cuando no aplica" not in b, "sin la explicación fija «null cuando no aplica»")
intro = [ln for ln in b.splitlines() if ln.startswith("- **Retornos internos")]
ver(intro and "CT-06 a CT-14" not in intro[0], f"el §1 no dice que CT-09 y CT-10 se validen con ESQUEMAS: «{intro[0][:110] if intro else ''}…»")

print(f"\nr01_04 T-137: {OK} ok, {len(FALLOS)} fallos")
for x in FALLOS:
    print("  -", x)
