"""QA r02 de T-131 · ¿`comprobar_datos_a.py` da ahora el estado que daría el ciclo? Y lo que el implementador dice de los
dos «fallos» que quedan en los scripts de la r01.

 1. Las dos explicaciones del implementador: (a) las filas repetidas del caso «fechas duplicadas» de r01_01 son de 2026 y
    as_of es 2024; con repetidas dentro del rango, INVALIDO; (b) el «sin reflejar» de r01_02 es el `repr` del diccionario.
 2. La ventana: el ciclo valida los cierres de cada símbolo solo en la ventana del lote (`orquestacion.senales_clase`:
    `senales.ventana_anios` años y `senales.margen_dias` días hasta as_of; la referencia, hasta `tasa_base.ventana_anios`),
    y lo de fuera no cuenta (T-65, QA r03, H-21). El script llama a `cierres(simbolo)` sin inicio, así que valida toda la
    historia hasta as_of. Un cierre malo anterior a la ventana: ¿qué dicen el script y el ciclo?
 3. Fechas de publicación posteriores a as_of, símbolos con ruta y as_of mal escrito.
 4. Borrador: los retornos CT-09 y CT-10 son del Motor (código), no de un agente: ¿hay un esquema de `ESQUEMAS` que
    describir, como propone el borrador?
Uso (desde la raíz): python -I r02_01_ventana_del_ciclo_y_borrador.py
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[4]
EJE = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJE))
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config, parametro  # noqa: E402
from bloque_a.contratos import ESQUEMAS  # noqa: E402
from bloque_a.herramientas.ht01_datos import DatosInvalidos, ProveedorCSV, cargar_universo  # noqa: E402

spec = importlib.util.spec_from_file_location("cd", RAIZ / ".docs" / "scripts" / "comprobar_datos_a.py")
cd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cd)
spec = importlib.util.spec_from_file_location("ba", RAIZ / ".docs" / "scripts" / "borrador_anexo_b.py")
ba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ba)
DATOS = EJE / "ejemplos" / "datos_sinteticos"
U = cargar_universo(RUTA_UNIVERSO_EJEMPLO).head(1)
SIM = U["simbolo"].iloc[0]
CFG = cargar_config()
OK, FALLOS = 0, []


def comprobar(cond, msg):
    global OK
    OK += bool(cond)
    if not cond:
        FALLOS.append(msg)
    print(f"  {'ok   ' if cond else 'FALLA'} {msg}")


def carpeta(estropear):
    d = Path(tempfile.mkdtemp(prefix="qa14_t131_"))
    shutil.copy(DATOS / f"{SIM}.csv", d / f"{SIM}.csv")
    df = pd.read_csv(d / f"{SIM}.csv")
    estropear(df).to_csv(d / f"{SIM}.csv", index=False)
    return d


def ciclo_acepta(d, as_of):
    """Lo que hace `senales_clase` con el símbolo (orquestacion.py: `ini` y `self.proveedor.cierres(f["simbolo"], ini, as_of)`)
    y, para la referencia, `ini_ref`; además `valor_en(as_of)`, que valida solo el último cierre."""
    ven = parametro(CFG, "senales")
    ini = pd.Timestamp(as_of) - pd.DateOffset(years=int(ven["ventana_anios"]), days=int(ven["margen_dias"]))
    ini_ref = min(ini, pd.Timestamp(as_of) - pd.DateOffset(years=int(parametro(CFG, "tasa_base.ventana_anios"))))
    p = ProveedorCSV(d)
    p.fijar_as_of(as_of)
    try:
        p.cierres(SIM, str(min(ini, ini_ref).date()), as_of)
        p.valor_en(SIM, as_of)
        return "acepta", str(min(ini, ini_ref).date())
    except DatosInvalidos as e:
        return f"rechaza ({str(e)[:60]})", str(min(ini, ini_ref).date())


print("1. las explicaciones del implementador")
d = carpeta(lambda df: pd.concat([df, df.tail(3)]))
f = cd.comprobar(d, U, "2024-03-29")[0]
ult = pd.read_csv(d / f"{SIM}.csv")["fecha"].tail(3).tolist()
comprobar(f["estado"] == "OK" and all(x > "2024-03-29" for x in ult),
          f"(a) r01_01 «fechas duplicadas»: repite {ult} (posteriores a as_of 2024-03-29) → {f['estado']}; el ciclo: {ciclo_acepta(d, '2024-03-29')[0]}")
f = cd.comprobar(d, U, "2026-10-30")[0]
comprobar(f["estado"] == "INVALIDO", f"(a) las mismas repetidas con as_of 2026-10-30 (dentro del rango) → {f['estado']}")
shutil.rmtree(d)
texto = ba.generar()
d_div = json.loads(ba.DIVERGENCIAS.read_text(encoding="utf-8"))
for ct in ("CT-11", "CT-12", "CT-13"):
    rech = d_div["por_contrato"][f"{ct}.ENCARGO"]["el_ejecutor_rechaza_el_ejemplo_del_anexo_b"]
    fila = [x for x in texto.splitlines() if x.startswith(f"| {ct}.ENCARGO |")]
    comprobar(fila and rech["motivo"] in fila[0] and rech["clase"] in fila[0] and str(rech)[:40] not in fila[0],
              f"(b) {ct}: la fila lleva la clase y el motivo («{rech['motivo']}»), no el repr del diccionario que buscaba r01_02")

print("2. la ventana del ciclo: un cierre malo anterior a la ventana")
for nombre, cambio in {"cierre «n/d» en 2022-06-01": lambda df: df.assign(cierre=df["cierre"].where(df["fecha"] != "2022-06-01", "n/d")),
                       "cierre 0 en 2022-06-01": lambda df: df.assign(cierre=df["cierre"].where(df["fecha"] != "2022-06-01", 0.0)),
                       "fecha 2022-06-01 repetida": lambda df: pd.concat([df, df[df["fecha"] == "2022-06-01"]])}.items():
    d = carpeta(cambio)
    as_of = "2026-06-30"
    f = cd.comprobar(d, U, as_of)[0]
    ciclo, desde = ciclo_acepta(d, as_of)
    comprobar((f["estado"] == "OK") == (ciclo == "acepta"),
              f"{nombre}, as_of {as_of} (el ciclo mira desde {desde}): script {f['estado']} · ciclo {ciclo}")
    shutil.rmtree(d)

print("3. publicación posterior, símbolo con ruta, as_of mal escrito")
d = carpeta(lambda df: df.assign(fecha_publicacion="2030-01-01"))
f = cd.comprobar(d, U, "2024-03-29")[0]
comprobar(f["estado"] == "FALTA", f"todas las filas publicadas en 2030 → {f['estado']} ({f['motivo'][:60]})")
shutil.rmtree(d)
u2 = U.assign(simbolo="../" + SIM)
f = cd.comprobar(DATOS, u2, "2024-03-29")[0]
comprobar(f["estado"] in ("FALTA", "INVALIDO"), f"símbolo «../{SIM}» → {f['estado']} ({f['motivo'][:60]})")
p = subprocess.run([sys.executable, str(RAIZ / ".docs" / "scripts" / "comprobar_datos_a.py"), str(DATOS), "--as-of", "2024-02-30"],
                   capture_output=True, text=True, cwd=RAIZ)
print(f"     --as-of 2024-02-30: código {p.returncode}; última línea de stderr: {(p.stderr.strip().splitlines() or [''])[-1][:100]}")

print("4. borrador: CT-09 y CT-10 frente a ESQUEMAS")
agentes = {"CT-06": "INFORME_CLASE", "CT-07": "BUSQUEDA", "CT-08": "BUSQUEDA", "CT-11": "CURACION", "CT-12": "PROSPECTIVA",
           "CT-13": "REFUTACION", "CT-14": "DICTAMEN_G3"}   # orquestacion.py, `_invocar(agente, contrato, …, esquema)`
orq = (EJE / "bloque_a" / "orquestacion.py").read_text(encoding="utf-8")
invocados = sorted({c for c in ("CT-06", "CT-07", "CT-08", "CT-09", "CT-10", "CT-11", "CT-12", "CT-13", "CT-14")
                    if f'"{c}", msg' in orq or f'"{c}", cuerpo' in orq or (c in ("CT-07", "CT-08") and "self._invocar(agente, tipo, msg, \"BUSQUEDA\"" in orq)})
print(f"     contratos CT-06 a CT-14 cuyo retorno valida `_invocar` con un esquema de ESQUEMAS: {invocados}")
for ct in ("CT-09", "CT-10"):
    fila = [x for x in texto.splitlines() if x.startswith(f"| {ct}.RETORNO |")]
    propone = bool(fila) and "describir los campos del esquema de `ESQUEMAS` de ese agente" in fila[0]
    comprobar(not (propone and ct not in invocados),
              f"{ct}.RETORNO: el borrador propone describir «el esquema de ESQUEMAS de ese agente» y {ct} "
              f"{'sí' if ct in invocados else 'no'} pasa por `_invocar` (lo sirve el Motor, `motor/servicio.py`)")
comprobar(all(v in ESQUEMAS for v in agentes.values()), "los esquemas de los demás retornos internos existen en ESQUEMAS")

print(f"\nr02_01 T-131: {OK} ok, {len(FALLOS)} fallos")
for f in FALLOS:
    print("  -", f)
