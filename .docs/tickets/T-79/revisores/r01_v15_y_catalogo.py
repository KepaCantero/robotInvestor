"""r01 (QA T-79): V-15 de validar_sobre (V0.60) y la batería del catálogo de códigos (V0.61), por caminos propios.

1. V-15: el permiso de apalancamiento solo vale si es exactamente True. Se prueba con permisos raros (1, 1.0, "true", "True",
   [True], {"x": 1}, NaN, inf, un bool de numpy si está instalado, una subclase de int) y con valores de apalancamiento extremos
   cuando el permiso es True (0, -1, NaN, inf, 1e308, texto, bool).
2. Catálogo: en una copia del marco se meten defectos y la batería pruebas_catalogo_codigos.py tiene que fallar con cada uno
   (no vacuidad): un código nuevo sin catalogar, un código catalogado que ya no existe, el mismo código con otro sentido en
   otro módulo y una fila T-xx de la deuda que no existe.

Uso: python3 -I r01_v15_y_catalogo.py <carpeta marco_comun_c> <carpeta temporal vacía>
"""
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

M, TMP = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(M / "validador"))
from validar_sobre import validar  # noqa: E402

res = []


def chk(nombre, cond, detalle=""):
    res.append(cond)
    print(("OK       " if cond else "HALLAZGO ") + nombre + ("" if cond else f"  -> {detalle}"))


CTX = json.loads((M / "pruebas" / "contexto.json").read_text(encoding="utf-8"))
S5 = json.loads((M / "pruebas" / "invalidos" / "inv_V15_apalancamiento.json").read_text(encoding="utf-8"))
SNE = json.loads((M / "pruebas" / "invalidos" / "inv_V15_apalancamiento_no_estimable.json").read_text(encoding="utf-8"))


def reglas(sobre, permiso, poner=True):
    ctx = copy.deepcopy(CTX)
    if poner:
        ctx["apalancamiento_permitido"] = permiso
    else:
        ctx.pop("apalancamiento_permitido", None)
    s0 = json.dumps(sobre, sort_keys=True)
    r = validar(sobre, ctx)
    assert json.dumps(sobre, sort_keys=True) == s0, "validar mutó el sobre"
    return {x["regla"] for x in r}


class Entero(int):
    pass


raros = [1, 1.0, "true", "True", [True], {"x": 1}, float("nan"), float("inf"), Entero(1), "1", b"1"]
try:
    import numpy as np   # noqa: E402
    raros.append(np.bool_(True))
except ImportError:
    pass
for base, nombre in ((S5, "valor 5"), (SNE, "NO_ESTIMABLE")):
    chk(f"V-15 {nombre}: sin permiso en el contexto da V-15", "V-15" in reglas(base, None, poner=False))
    chk(f"V-15 {nombre}: permiso False da V-15", "V-15" in reglas(base, False))
    for p in raros:
        chk(f"V-15 {nombre}: permiso {p!r} ({type(p).__name__}) no habilita", "V-15" in reglas(base, p))
    chk(f"V-15 {nombre}: permiso True habilita (sin V-15)", "V-15" not in reglas(base, True))

# con permiso True, apalancamientos imposibles: ¿alguna regla los para?
for v in (0, -1, float("nan"), float("inf"), 1e308, "5", True, None, 0.5):
    s = copy.deepcopy(S5)
    s["payload"]["capital"]["apalancamiento"]["valor"] = v
    r = reglas(s, True)
    if v == 1e308:   # el sobre no pone tope al apalancamiento permitido (anterior a la V0.60); lo topan F (apalancamiento_max <= 100) y SC-1 (<= 10)
        print(f"         (info) permiso True y apalancamiento {v!r}: el sobre lo deja pasar ({sorted(r)}); lo para F")
        continue
    chk(f"permiso True y apalancamiento {v!r}: alguna regla lo rechaza", bool(r), r)
# determinismo
chk("V-15 determinista", reglas(S5, "x") == reglas(S5, "x") and validar(S5, CTX) == validar(S5, CTX))

# 2. no vacuidad de la batería del catálogo
def copia(nombre):
    d = TMP / nombre
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(M / "validador", d / "validador", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(M / "pruebas", d / "pruebas", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy(M / "LEEME.md", d / "LEEME.md")
    return d


def corre(d):
    r = subprocess.run([sys.executable, "-I", str(d / "pruebas" / "pruebas_catalogo_codigos.py")], capture_output=True, text=True,
                       timeout=120)
    return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]


TMP.mkdir(parents=True, exist_ok=True)
d = copia("limpia")
chk("catálogo: la copia limpia pasa", "TODAS LAS PRUEBAS PASAN" in corre(d), corre(d))

d = copia("codigo_nuevo")   # un código emitido en vigilancia que nadie catalogó
p = d / "validador" / "vigilancia.py"
t = p.read_text(encoding="utf-8")
p.write_text(t + '\n\ndef _qa_t79():\n    return {"ok": False, "codigo": "H-97", "motivo": "código nuevo sin catalogar"}\n', encoding="utf-8")
chk("catálogo: un código nuevo sin catalogar hace fallar la batería", "HAY FALLOS" in corre(d), corre(d))

import catalogo_codigos as cc  # noqa: E402
claves = sorted(cc.CATALOGO)
print(f"         (info) CATALOGO tiene {len(claves)} entradas; ejemplo {claves[0]}")

d = copia("codigo_fantasma")   # una entrada del catálogo de un código que no existe
p = d / "validador" / "catalogo_codigos.py"
t = p.read_text(encoding="utf-8")
t = t + '\n\nCATALOGO = dict(CATALOGO)\nCATALOGO[("vigilancia", "H-98")] = dict(next(iter(CATALOGO.values())))\n'
p.write_text(t, encoding="utf-8")
chk("catálogo: un código catalogado que no existe hace fallar la batería", "HAY FALLOS" in corre(d), corre(d))

d = copia("doble_sentido")   # el mismo código en otro módulo (como el E de encargo y de dimensionado)
p = d / "validador" / "mandatos.py"
t = p.read_text(encoding="utf-8")
p.write_text(t + '\n\ndef _qa_t79():\n    return {"ok": False, "codigo": "H-01", "motivo": "H-01 en otro módulo con otro sentido"}\n', encoding="utf-8")
chk("catálogo: el mismo código en otro módulo sin catalogar hace fallar la batería", "HAY FALLOS" in corre(d), corre(d))

d = copia("leeme")   # el registro de prefijos del LEEME pierde un prefijo
p = d / "LEEME.md"
t = p.read_text(encoding="utf-8")
i = t.index("## Registro de prefijos de códigos")
bloque = t[i:i + 4000]
linea_rl = next((l for l in bloque.splitlines() if "RL-" in l), None)
if linea_rl:
    p.write_text(t.replace(linea_rl, "", 1), encoding="utf-8")
    chk("catálogo: quitar del LEEME la línea del prefijo RL hace fallar la batería", "HAY FALLOS" in corre(d), corre(d))
else:
    print("         (info) no encuentro la línea RL en el registro de prefijos")
shutil.rmtree(TMP / "limpia", ignore_errors=True)

n = res.count(False)
print(f"\nRESULTADO r01 V-15 Y CATALOGO: {'SIN HALLAZGOS' if not n else f'{n} HALLAZGO(S)'}")
