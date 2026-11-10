"""QA r01 de T-92 (revisor nuevo): ataques a la regla nueva de la CESTA (D01/D02) y a la base de las rentabilidades.

Uso: python -I r01_01_cesta_bases.py <ruta a bloque_a/11_Ejecutor>
Imprime OK/FALLO por caso; FALLO = comportamiento que contradice «falla cerrado» o las reglas de T-65 (H-15, H-21, H-25).
"""
import sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ)); sys.path.insert(0, str(EJ / "tests"))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
import pandas as pd
from bloque_a.almacen import Almacen
from bloque_a.evaluador import Evaluador
from bloque_a.herramientas.ht01_datos import ProveedorCSV, DatosNoDisponibles
from test_t53_evaluacion_y_almacen import MotorFalso, _alta

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

def ev(tmp, simbolos=("X", "Y")):
    p = ProveedorCSV(tmp)
    a = Almacen(tmp / "estado"); a.reloj.fijar("2026-06-05")
    return Evaluador(a, p, MotorFalso(), {}, pd.DataFrame({"simbolo": list(simbolos), "clase": ["RV"] * len(simbolos)}))

def csv(tmp, s, txt):
    (tmp / f"{s}.csv").write_text(txt, encoding="utf-8")

# 1. Cierre negativo como último dato conocido al emitir: valor_en lo rechaza (T-65, H-15), _base_conocida no
with tempfile.TemporaryDirectory() as d:
    t = Path(d); e = ev(t)
    csv(t, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    csv(t, "Y", "fecha,cierre\n2026-06-04,100\n2026-06-05,-50\n2026-07-31,60\n")
    e.proveedor.fijar_as_of("2026-06-05")
    try:
        e.proveedor.valor_en("Y", "2026-06-05"); via = "acepta"
    except DatosNoDisponibles:
        via = "rechaza"
    bases = e.bases_cesta("RV", "2026-06-05", "H3")
    informe("1a base de CESTA con cierre negativo al emitir queda fuera o falla", "Y" not in bases,
            f"valor_en {via}; bases_cesta = {bases}")
    e.proveedor.fijar_as_of("2026-07-31")
    try:
        r, _ = e.rentabilidad("CESTA", "RV", "2026-06-05", "2026-07-31", "H3", base=bases)
        informe("1b la CESTA no se resuelve con una base negativa", "Y" not in bases, f"rentabilidad CESTA = {r:.4f}")
    except DatosNoDisponibles as x:
        informe("1b la CESTA no se resuelve con una base negativa", True, str(x)[:80])

# 1c. De extremo a extremo: el PRG con esas bases congeladas (como las escribe sintesis.construir) se RESUELVE
with tempfile.TemporaryDirectory() as d:
    t = Path(d); e = ev(t)
    csv(t, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    csv(t, "Y", "fecha,cierre\n2026-06-04,100\n2026-06-05,-50\n2026-07-31,60\n")
    csv(t, "P", "fecha,cierre\n2026-06-05,100\n2026-07-31,101\n")
    e.proveedor.fijar_as_of("2026-06-05")
    _alta(e.almacen, "PRG-2026-0001", tipo_pronostico="RELATIVO", variable={"serie_ht01": "P"}, referencia_indice="CESTA",
          nivel_referencia={"valor": 100.0, "fecha": "2026-06-05"}, bases_cesta=e.bases_cesta("RV", "2026-06-05", "H3"),
          fecha_resolucion="2026-07-31")
    e.proveedor.fijar_as_of("2026-08-03"); e.almacen.reloj.fijar("2026-08-03")
    r, = e.resolver("2026-08-03")
    informe("1c el PRG con una base negativa en la CESTA no queda RESUELTO", r["estado"] != "RESUELTO",
            f"{r['estado']} {r['resolucion'].get('resultado')} rent_referencia={r['resolucion'].get('rent_referencia')}")

# 2. Fecha duplicada en la emisión (T-65, H-21/H-25: ambigua, se rechaza la serie)
with tempfile.TemporaryDirectory() as d:
    t = Path(d); e = ev(t)
    csv(t, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    csv(t, "Y", "fecha,cierre\n2026-06-05,100\n2026-06-05,200\n2026-07-31,220\n")
    e.proveedor.fijar_as_of("2026-06-05")
    try:
        e.proveedor.valor_en("Y", "2026-06-05"); via = "acepta"
    except DatosNoDisponibles:
        via = "rechaza"
    bases = e.bases_cesta("RV", "2026-06-05", "H3")
    informe("2  base de CESTA con fecha duplicada al emitir queda fuera o falla", "Y" not in bases,
            f"valor_en {via}; bases_cesta = {bases}")

# 3. Bases congeladas manipuladas o raras en F4: cada una debe dar DatosNoDisponibles (espera / NO_RESOLUBLE), nunca cifra
with tempfile.TemporaryDirectory() as d:
    t = Path(d); e = ev(t)
    csv(t, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    csv(t, "Y", "fecha,cierre\n2026-06-05,100\n2026-07-31,90\n")
    e.proveedor.fijar_as_of("2026-07-31")
    casos = {
        "valor negativo": {"X": {"valor": -100.0, "fecha": "2026-06-05"}},
        "valor True": {"X": {"valor": True, "fecha": "2026-06-05"}},
        "valor NaN": {"X": {"valor": float("nan"), "fecha": "2026-06-05"}},
        "valor inf": {"X": {"valor": float("inf"), "fecha": "2026-06-05"}},
        "valor texto": {"X": {"valor": "100", "fecha": "2026-06-05"}},
        "valor 0": {"X": {"valor": 0, "fecha": "2026-06-05"}},
        "fecha posterior": {"X": {"valor": 100.0, "fecha": "2026-06-06"}},
        "fecha basura": {"X": {"valor": 100.0, "fecha": "no-es-fecha"}},
        "lista vacía": [],
        "dict vacío": {},
        "miembro desconocido": {"ZZZ": {"valor": 100.0, "fecha": "2026-06-05"}},
        "ruta fuera": {"../X": {"valor": 100.0, "fecha": "2026-06-05"}},
    }
    for nombre, b in casos.items():
        try:
            r, _ = e.rentabilidad("CESTA", "RV", "2026-06-05", "2026-07-31", "H3", base=b)
            informe(f"3  base congelada «{nombre}»", False, f"da cifra {r}")
        except DatosNoDisponibles:
            informe(f"3  base congelada «{nombre}»", True)
        except Exception as x:
            informe(f"3  base congelada «{nombre}»", False, f"{type(x).__name__} sin capturar (resolver() solo captura DatosNoDisponibles): {x}"[:140])

# 4. Pronóstico antiguo sin bases_cesta, con un miembro añadido al universo DESPUÉS de emitir (pero con historia previa)
with tempfile.TemporaryDirectory() as d:
    t = Path(d)
    csv(t, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    csv(t, "Y", "fecha,cierre\n2026-06-05,100\n2026-07-31,90\n")
    csv(t, "P", "fecha,cierre\n2026-06-05,100\n2026-07-31,120\n")
    e = ev(t, ("X", "Y"))
    _alta(e.almacen, "PRG-2026-0001", tipo_pronostico="RELATIVO", variable={"serie_ht01": "P"}, referencia_indice="CESTA",
          nivel_referencia={"valor": 100.0, "fecha": "2026-06-05"}, fecha_resolucion="2026-07-31")
    e.proveedor.fijar_as_of("2026-08-03"); e.almacen.reloj.fijar("2026-08-03")
    r, = e.resolver("2026-08-03")
    informe("4  PRG antiguo sin bases_cesta se resuelve con la cesta reconstruida al corte de la emisión",
            r["estado"] == "RESUELTO" and abs(r["resolucion"]["rent_referencia"]) < 1e-12, str(r["resolucion"].get("rent_referencia")))

# 5. Una fecha basura en bases_cesta de UN pronóstico no debe tumbar la resolución de los demás
with tempfile.TemporaryDirectory() as d:
    t = Path(d)
    csv(t, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    csv(t, "P", "fecha,cierre\n2026-06-05,100\n2026-07-31,120\n")
    e = ev(t, ("X",))
    _alta(e.almacen, "PRG-2026-0001", tipo_pronostico="RELATIVO", variable={"serie_ht01": "P"}, referencia_indice="CESTA",
          nivel_referencia={"valor": 100.0, "fecha": "2026-06-05"}, bases_cesta={"X": {"valor": 100.0, "fecha": "05/06/2026x"}},
          fecha_resolucion="2026-07-31")
    _alta(e.almacen, "PRG-2026-0002", tipo_pronostico="ABSOLUTO", variable={"serie_ht01": "P"},
          nivel_referencia={"valor": 100.0, "fecha": "2026-06-05"}, fecha_resolucion="2026-07-31")
    e.proveedor.fijar_as_of("2026-08-03"); e.almacen.reloj.fijar("2026-08-03")
    try:
        res = e.resolver("2026-08-03")
        informe("5  una base corrupta no tumba la resolución del resto", any(x["prg_id"] == "PRG-2026-0002" for x in res))
    except Exception as x:
        informe("5  una base corrupta no tumba la resolución del resto", False, f"{type(x).__name__}: {x}"[:120])

print("fallos:", fallos)
