"""QA r02 de T-92 (revisor nuevo): bordes de H-06 (base al emitir), H-14 (fecha de la base), H-15 (plazo con solo fecha de
CT-23) y H-09 (umbral de la observación de HT-01).

Uso: python -I r02_04_bases_plazos_umbral.py <ruta a bloque_a/11_Ejecutor>
"""
import sys, tempfile
from pathlib import Path
EJ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(EJ)); sys.path.insert(0, str(EJ / "tests"))
import bloque_a
assert Path(bloque_a.__file__).resolve().is_relative_to(EJ), bloque_a.__file__
import pandas as pd
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles
from conftest import AS_OF, nuevo_bloque
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo
from test_t87_datos import _csv, _evaluador

fallos = 0
def informe(nombre, ok, detalle=""):
    global fallos
    fallos += 0 if ok else 1
    print(("OK    " if ok else "FALLO ") + nombre + (f" — {detalle}" if detalle else ""))

# 1. H-06: la base al emitir se valida como cualquier cierre de HT-01
casos = {
    "cierre negativo": "2026-06-04,100\n2026-06-05,-50\n",
    "cierre 0": "2026-06-04,100\n2026-06-05,0\n",
    "fecha repetida": "2026-06-05,100\n2026-06-05,101\n",
    "cierre no numérico": "2026-06-04,100\n2026-06-05,n.d.\n",
    "cierre inf": "2026-06-04,100\n2026-06-05,inf\n",
}
for nombre, filas in casos.items():
    with tempfile.TemporaryDirectory() as d:
        t = Path(d); e = _evaluador(t)
        _csv(t, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
        _csv(t, "Y", "fecha,cierre\n" + filas + "2026-07-31,60\n")
        e.proveedor.fijar_as_of("2026-06-05")
        try:
            bases = e.bases_cesta("RV", "2026-06-05", "H3"); ok = set(bases) == {"X"}; det = str(sorted(bases))
        except Exception as x:
            ok, det = False, f"{type(x).__name__}: {x}"
        informe(f"1  miembro con {nombre} al emitir queda fuera de la CESTA (y el resto sigue)", ok, det)
# un cierre malo antiguo no deja fuera a un miembro sano (como valor_en, QA r01 de T-65, H-01)
with tempfile.TemporaryDirectory() as d:
    t = Path(d); e = _evaluador(t)
    _csv(t, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    _csv(t, "Y", "fecha,cierre\n2026-06-01,-1\n2026-06-02,2026\n2026-06-02,7\n2026-06-05,100\n2026-07-31,60\n")
    e.proveedor.fijar_as_of("2026-06-05")
    informe("1b un cierre malo anterior a la base no deja fuera a un miembro sano", set(e.bases_cesta("RV", "2026-06-05", "H3")) == {"X", "Y"})
# la base congelada es la publicada al emitir aunque luego se revise (D01)
with tempfile.TemporaryDirectory() as d:
    t = Path(d); e = _evaluador(t)
    _csv(t, "X", "fecha,cierre,fecha_publicacion\n2026-06-05,100,2026-06-05\n2026-06-05,-3,2026-06-20\n2026-07-31,110,2026-07-31\n")
    e.proveedor.fijar_as_of("2026-06-05")
    b = e._base_conocida("X", "2026-06-05")
    e.proveedor.fijar_as_of("2026-08-03")
    try:
        r, _ = e.rentabilidad("X", "RV", "2026-06-05", "2026-07-31", "H3", base=b); det = f"r={r:.3f}"; ok = abs(r - 0.1) < 1e-9
    except DatosNoDisponibles as x:
        ok, det = True, f"espera: {x}"   # la fila revisada duplica la fecha: también es aceptable que no resuelva
    informe("1c una revisión posterior (fila duplicada publicada después) no cambia la base congelada", ok, f"base={b}; {det}")

# 2. H-14: más formas ilegibles de la fecha de una base congelada
with tempfile.TemporaryDirectory() as d:
    t = Path(d); e = _evaluador(t)
    _csv(t, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,110\n")
    e.proveedor.fijar_as_of("2026-08-03")
    for f in [{"a": 1}, float("nan"), "NaT", "2026-13-45", 1e30, b"2026-06-05", True]:
        try:
            e.rentabilidad("X", "RV", "2026-06-05", "2026-07-31", "H3", base={"valor": 100.0, "fecha": f}); ok, det = False, "resuelve"
        except DatosNoDisponibles:
            ok, det = True, ""
        except Exception as x:
            ok, det = False, f"{type(x).__name__}: {x}"
        informe(f"2  base con fecha {f!r} → DatosNoDisponibles (no tumba C5)", ok, det)

# 3. H-15: un plazo con solo fecha vale todo ese día en Madrid, también los días de cambio de hora
universo = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
for dia, ultimo_dentro, primero_fuera in [("2026-06-08", "2026-06-08T21:59Z", "2026-06-08T22:00Z"),
                                          ("2026-03-29", "2026-03-29T21:59Z", "2026-03-29T22:00Z"),   # 23 h (verano)
                                          ("2026-10-25", "2026-10-25T22:59Z", "2026-10-25T23:00Z")]:  # 25 h (invierno)
    with tempfile.TemporaryDirectory() as d:
        b = nuevo_bloque(d, universo)
        c = b.consultas.enviar({"tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"],
                                "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}], "plazo_respuesta": dia}, AS_OF)
        dentro = b.consultas.vencer(ultimo_dentro)
        fuera = b.consultas.vencer(primero_fuera)
        informe(f"3  plazo «{dia}»: abierto a las 23:59 de Madrid y vencido a las 00:00 del día siguiente",
                dentro == [] and fuera == [c["cns_id"]], f"a {ultimo_dentro}: {dentro}; a {primero_fuera}: {fuera}")
for forma in ["2026-6-8", "20260608", "2026-06-08T00:00", "8/6/2026"]:
    with tempfile.TemporaryDirectory() as d:
        b = nuevo_bloque(d, universo)
        try:
            c = b.consultas.enviar({"tipo": "OTRA", "modo": "BLOQUEANTE", "clases": ["RV"],
                                    "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}], "plazo_respuesta": forma}, AS_OF)
            det = f"guardado {c['plazo_respuesta']}"
        except ValueError as x:
            det = f"rechazado: {x}"
        print(f"INFO  3b plazo «{forma}» → {det}")

# 4. H-09: el umbral de la configuración se valida (no acepta valores sin sentido)
with tempfile.TemporaryDirectory() as d:
    b = nuevo_bloque(d, universo)
    s = {"senal_compuesta": 0.55, "tendencia_26s": "alcista"}
    for malo in (float("nan"), True, -1, 7, "0.5"):
        b.cfg["senales"]["umbral_favorable"] = malo
        try:
            r = b._observacion_ht01("X", s)["direccion"]; ok, det = False, f"acepta y da {r}"
        except (ValueError, TypeError, KeyError) as x:
            ok, det = True, type(x).__name__
        informe(f"4  umbral_favorable={malo!r} se rechaza", ok, det)
print("fallos:", fallos)
