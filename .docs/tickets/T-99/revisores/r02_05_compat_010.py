"""r02_05 · Registros escritos por la versión 0.1.0 (la de `bb2d692`): ¿los lee la 0.2.0? ¿Con qué mensaje? ¿Hay camino de
migración? Se extrae la 0.1.0 con «git show» a una carpeta temporal y se escriben con ella registros en /tmp.
Uso: python3 -B r02_05_compat_010.py <raíz>"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r02_comun import AHORA, DESPUES, RAIZ, caso, fin, lanza, pre, rx, tmpdir  # noqa: E402

d = tmpdir("r02_t99_v010_")
fuente = subprocess.run(["git", "-C", str(RAIZ), "show", "bb2d692:.docs/scripts/registro_experimentos.py"], capture_output=True,
                        text=True, check=True).stdout
(d / "registro_010.py").write_text(fuente, encoding="utf-8")
spec = importlib.util.spec_from_file_location("registro_010", d / "registro_010.py")
v010 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v010)
caso("(referencia) versión extraída", v010.VERSION == "0.1.0", v010.VERSION)


def escrito_por_010(variantes=("v1",), ahora=None):
    r = v010.Registro(tmpdir() / "registro.jsonl")
    e = r.prerregistrar(pre(), "qa", ahora or AHORA)["exp_id"]
    for v in variantes:
        n = r.intento(e, v, DESPUES)["n"]; r.resultado(e, n, "peor", ahora=DESPUES)
    return r, e


# 1. Un registro 0.1.0 normal, con la 0.2.0
r, e = escrito_por_010()
nuevo = rx.Registro(r.ruta)
x = lanza(nuevo.verificar, rx.RegistroError)
caso("registro 0.1.0: la 0.2.0 falla cerrado (no lo da por bueno sin sello)", x is not None, str(x)[:100])
caso("…y el mensaje dice que es un registro de la versión 0.1.0 y cómo migrarlo (no solo que «falta el sello»)",
     x is not None and ("0.1.0" in str(x) or "migr" in str(x)), str(x)[:100])
# 2. Con un sello hecho a mano a partir de la última línea: ¿el resto de la forma 0.1.0 valida en 0.2.0?
ult = json.loads(r.ruta.read_text(encoding="utf-8").splitlines()[-1])
nuevo.sello.write_text(json.dumps({"seq": ult["_seq"], "hash": ult["_hash"]}) + "\n", encoding="utf-8")
x = lanza(nuevo.verificar, rx.RegistroError)
caso("registro 0.1.0 con sello rehecho: su forma valida con las reglas 0.2.0", x is None, str(x or "")[:100])
caso("…y se puede seguir anotando con la 0.2.0", lanza(lambda: nuevo.intento(e, "v1", DESPUES)) is None)
# 3. Lo que la 0.1.0 aceptaba y la 0.2.0 ya no: un registro antiguo con eso no se puede leer (falla cerrado)
for nombre, cambio in (("datos vacío", {"datos": ""}), ("fecha imposible", {"desde": "2026-02-30"})):
    r = v010.Registro(tmpdir() / "registro.jsonl")
    lanza(lambda: r.prerregistrar(pre(**cambio), "qa", AHORA))
    if not r.ruta.exists():
        caso(f"(referencia) la 0.1.0 ya rechazaba {nombre}", True)
        continue
    ult = json.loads(r.ruta.read_text(encoding="utf-8").splitlines()[-1])
    rx.Registro(r.ruta).sello.write_text(json.dumps({"seq": ult["_seq"], "hash": ult["_hash"]}), encoding="utf-8")
    x = lanza(rx.Registro(r.ruta).verificar, rx.RegistroError)
    caso(f"0.1.0 con {nombre}: la 0.2.0 lo rechaza al leer (falla cerrado)", x is not None, str(x)[:90])
# 4. Variante NFD escrita por la 0.1.0 (no normalizaba): ¿la 0.2.0 la cuenta como la misma que la NFC?
import unicodedata  # noqa: E402
r, e = escrito_por_010(variantes=(unicodedata.normalize("NFD", "única"),))
ult = json.loads(r.ruta.read_text(encoding="utf-8").splitlines()[-1])
nuevo = rx.Registro(r.ruta); nuevo.sello.write_text(json.dumps({"seq": ult["_seq"], "hash": ult["_hash"]}), encoding="utf-8")
i = lanza(lambda: nuevo.intento(e, "única", DESPUES))
it = nuevo.experimento(e)["intentos"][-1] if i is None else None
caso("(baja) variante NFD de la 0.1.0 y la misma en NFC con la 0.2.0: la misma variante", bool(it and it["dentro_del_maximo"])
     and nuevo.resumen(e)["variantes"] == 1, f"variantes={nuevo.resumen(e)['variantes'] if i is None else i}")
fin()
