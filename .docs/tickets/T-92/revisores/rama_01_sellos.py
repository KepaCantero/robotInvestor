"""Revisión de Claude (antes de T-92) de la rama astra/bloque-a-integridad-y-evidencia, O6/O7: sellos de integridad.
Uso: python -I rama_01_sellos.py <carpeta 11_Ejecutor de la rama>"""
import json, os, sys, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from bloque_a.almacen import Almacen
import bloque_a; assert sys.argv[1] in bloque_a.__file__, bloque_a.__file__

def nuevo(t):
    a = Almacen(t)
    for k in ("uno", "dos", "tres"):
        a.escribir("F5", "AG-01", {"id": k})
    return a

res = {}
# S1: truncar la última línea y borrar el fichero de sellos → ¿se acepta como almacén «legado»?
with tempfile.TemporaryDirectory() as t:
    nuevo(t)
    p = Path(t) / "F5_Registro_de_consumo.jsonl" if (Path(t) / "F5_Registro_de_consumo.jsonl").exists() else next(Path(t).glob("F5*"))
    lineas = p.read_text(encoding="utf-8").splitlines()
    p.write_text("\n".join(lineas[:-1]) + "\n", encoding="utf-8")
    (Path(t) / "sellos_integridad.json").unlink()
    try:
        b = Almacen(t)
        res["S1_truncado_mas_sello_borrado_se_acepta"] = (list(b.estado("F5")), b.verificar_integridad("F5"))
    except Exception as ex:
        res["S1_truncado_mas_sello_borrado_se_acepta"] = f"rechazado: {ex!r}"
# S2: sello presente pero ilegible (JSON roto) → ¿falla cerrado con un error claro?
with tempfile.TemporaryDirectory() as t:
    nuevo(t)
    (Path(t) / "sellos_integridad.json").write_text("{", encoding="utf-8")
    try:
        Almacen(t); res["S2_sello_ilegible"] = "ABRE"
    except Exception as ex:
        res["S2_sello_ilegible"] = f"rechaza: {type(ex).__name__}"
# S3: sello de un fichero que falta (alguien borra F5 entero y su entrada del sello)
with tempfile.TemporaryDirectory() as t:
    nuevo(t)
    p = next(Path(t).glob("F5*"))
    p.unlink()
    s = json.loads((Path(t) / "sellos_integridad.json").read_text())
    s.pop("F5")
    (Path(t) / "sellos_integridad.json").write_text(json.dumps(s))
    try:
        b = Almacen(t); res["S3_F5_borrado_y_quitado_del_sello"] = f"ABRE con F5={list(b.estado('F5'))}"
    except Exception as ex:
        res["S3_F5_borrado_y_quitado_del_sello"] = f"rechaza: {type(ex).__name__}: {ex}"
# S4: verificar_integridad con el fichero manipulado después de abrir
with tempfile.TemporaryDirectory() as t:
    a = nuevo(t)
    p = next(Path(t).glob("F5*"))
    l = p.read_text(encoding="utf-8").splitlines()
    p.write_text("\n".join(l[:-1]) + "\n", encoding="utf-8")
    try:
        res["S4_verificar_tras_truncar"] = a.verificar_integridad("F5")
    except Exception as ex:
        res["S4_verificar_tras_truncar"] = f"lanza {type(ex).__name__}"
    try:
        a.leer("F5"); res["S4b_leer_tras_truncar"] = "LEE"
    except Exception as ex:
        res["S4b_leer_tras_truncar"] = f"lanza {type(ex).__name__}"
for k, v in res.items():
    print(k, "→", v)
