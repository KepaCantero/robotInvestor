"""r03_06 · Rutas públicas del banco (H-24) y lo que el banco deja fuera del registro, con dobles del titular y de la
estadística (como r02_07): qué rutas de la máquina quedan en el prerregistro del registro, en prerregistro.json y en
experimento.json, y si una copia de los datos en otra carpeta abre un experimento nuevo con su máximo de variantes intacto.
Uso: .venv/bin/python -B r03_06_banco_rutas.py <raíz>"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r03_comun import RAIZ, borrar, caso, fin, rx, tmpdir  # noqa: E402

import banco_medida as bm  # noqa: E402

TMP = tmpdir("r03_t99_banco_")
UNIV = TMP / "universo.csv"; UNIV.write_text("simbolo,clase\nS0,C\n", encoding="utf-8")
cola = []
bm.titular_a = lambda *a, **k: {"universo": str(UNIV), "datos": str(TMP), "selecciones": [], "fecha_fin": "2025-05-30", "consumo": {}}
bm.cargar_precios = lambda *a, **k: None
bm.evaluar = lambda *a, **k: {}
bm.azar = lambda *a, **k: []
bm.momento = lambda *a, **k: []
visto = {}
bm.construir_informe = lambda *a, **k: (visto.update(advertencias=a[8]) or
                                        {"comparaciones": {"azar": {"veredicto": cola[0]}, "momento": {"veredicto": cola.pop(0)}}})
bm.informe_md = lambda *a, **k: ""
bm._aviso = lambda *a, **k: None


def ns(reg, salida, **kw):
    d = {"desde": "2025-03-07", "hasta": "2025-05-30", "salida": str(TMP / salida), "cliente": "mock", "frecuencia": None,
         "clases": None, "semilla": 7, "remuestreos": 2000, "ventana": 63, "registro": str(reg) if reg else None,
         "experimento": None, "max_variantes": 1}
    d.update(kw)
    return argparse.Namespace(**d)


casa = TMP / "home" / "usuario_de_prueba" / "datos"   # una carpeta «de la máquina» con un nombre de usuario
casa.mkdir(parents=True)
REG = TMP / "reg.jsonl"
cola.append("peor")
bm.ejecutar_a(ns(REG, "s1", datos=str(casa), universo=str(UNIV)))
txt_reg = REG.read_text(encoding="utf-8")
txt_pre = (TMP / "s1" / "prerregistro.json").read_text(encoding="utf-8")
txt_exp = (TMP / "s1" / "experimento.json").read_text(encoding="utf-8")
caso("el registro no guarda la carpeta de la máquina de --datos (H-24)", "usuario_de_prueba" not in txt_reg and str(TMP) not in txt_reg,
     json.loads(txt_reg.splitlines()[0])["contenido"]["datos"][:120])
caso("prerregistro.json tampoco", "usuario_de_prueba" not in txt_pre and str(TMP) not in txt_pre)
caso("experimento.json tampoco (la r02 lo citaba en H-24)", str(TMP) not in txt_exp, json.loads(txt_exp).get("registro"))

# Una copia de los mismos datos en otra carpeta: ¿otro experimento, con su máximo de variantes sin gastar?
otra = TMP / "copia" / "datos"; otra.mkdir(parents=True)
cola.append("mejor")
inf = bm.ejecutar_a(ns(REG, "s2", datos=str(otra), universo=str(UNIV)))
exps = sorted({x["exp_id"] for x in rx.Registro(REG).anotaciones() if x["tipo"] == "PRERREGISTRO"})
adop = {e: rx.Registro(REG).adoptable(e) for e in exps}
caso("(regla declarada, T-133 H-22) los mismos datos en otra carpeta abren otro experimento, y el informe lo advierte",
     len(exps) == 2 and any("misma hipótesis" in a for a in visto.get("advertencias") or []), f"experimentos {exps}; adoptables {adop}; advertencias {visto.get('advertencias')}")

borrar(TMP)
fin()
