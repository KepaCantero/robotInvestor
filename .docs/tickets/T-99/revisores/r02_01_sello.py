"""r02_01 · El sello del registro: escritura cortada entre la línea y el sello, corte a mitad de línea, sello ausente,
sello de otro registro o de un estado anterior, sello mal formado, sello sin registro, y qué hace el registro después.
Uso: python3 -B r02_01_sello.py <raíz>"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r02_comun import AHORA, DESPUES, caso, escribir, fin, lanza, leer, lineas, pre, registro_temporal, rx  # noqa: E402


def base():
    reg = registro_temporal()
    exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
    reg.intento(exp, "v1", DESPUES)
    reg.resultado(exp, 1, "peor", ahora=DESPUES)
    return reg, exp


# 1. Corte entre la línea y el sello (os.replace falla: disco lleno, proceso muerto justo ahí)
reg, exp = base()
real = os.replace


def replace_roto(a, b):
    raise OSError("simulado: el proceso muere antes de mover el sello")


os.replace = replace_roto
err = lanza(lambda: reg.intento(exp, "v2", DESPUES), Exception)
os.replace = real
n_lineas = len(lineas(reg))
caso("corte tras la línea: la llamada falla (no dice que fue bien)", err is not None, f"{type(err).__name__}: {err}")
caso("…y la excepción es RegistroError (la que capturan el banco y los demás llamadores)", isinstance(err, rx.RegistroError),
     f"es {type(err).__name__}: la línea ya está escrita ({n_lineas} líneas) y el sello no")
e2 = lanza(reg.verificar, rx.RegistroError)
caso("corte tras la línea: el registro queda bloqueado (falla cerrado)", e2 is not None, str(e2)[:120])
e3 = lanza(lambda: reg.resultado(exp, 1, "mejor", ahora=DESPUES), rx.RegistroError)
caso("…y no se anota nada más", e3 is not None)
tmp = reg.sello.with_name(reg.sello.name + ".tmp")
caso("…queda el «.sello.tmp» con el sello nuevo (una pista para recuperar, sin herramienta)", tmp.exists(),
     tmp.read_text(encoding="utf-8").strip() if tmp.exists() else "")
caso("(referencia) no hay orden para recuperar un corte (p. ej. «verificar --reparar-sello» que solo avance el sello si la cadena "
     "es válida y crece en una línea)", True, "hay que editar el sello a mano, igual que haría quien quiere tapar un truncado")

# 2. Corte a mitad de la línea (sin salto final)
reg, exp = base()
with open(reg.ruta, "a", encoding="utf-8") as f:
    f.write('{"tipo": "INTENTO", "exp_id": "' + exp)
e = lanza(reg.verificar, rx.RegistroError)
caso("corte a mitad de línea: se detecta", e is not None, str(e)[:100])

# 3. Sello ausente con anotaciones (registro de antes del sello, o sello no subido a git)
reg, exp = base(); reg.sello.unlink()
e = lanza(reg.verificar, rx.RegistroError)
caso("sello ausente con anotaciones: falla cerrado", e is not None, str(e)[:100])
# 3b. registro vacío con sello ausente
reg = registro_temporal(); reg.ruta.write_text("", encoding="utf-8")
caso("registro vacío sin sello: se lee (0 anotaciones)", lanza(reg.verificar) is None)
# 3c. sello con registro ausente (borrado entero)
reg, exp = base(); reg.ruta.unlink()
caso("registro borrado entero con el sello presente: se detecta", lanza(reg.verificar, rx.RegistroError) is not None)
# 3d. registro y sello borrados: la biblioteca dice 0; la línea de órdenes, que no existe
reg, exp = base(); reg.ruta.unlink(); reg.sello.unlink()
caso("(regla declarada) registro y sello borrados fuera de git: la biblioteca lo da por vacío", reg.verificar() == 0,
     "verificar() = 0; solo «verificar» de la línea de órdenes y el ancla de git lo delatan")

# 4. Sello de otro registro (mismo número de anotaciones) o de un estado anterior del mismo registro
reg_a, _ = base()
reg_b = registro_temporal(); e_b = reg_b.prerregistrar(pre(hipotesis="Otra hipótesis bastante larga"), "qa", AHORA)["exp_id"]
reg_b.intento(e_b, "v1", DESPUES); reg_b.resultado(e_b, 1, "peor", ahora=DESPUES)
assert leer(reg_a.sello) != leer(reg_b.sello)
reg_b.sello.write_bytes(leer(reg_a.sello))
caso("sello copiado de otro registro con el mismo número de anotaciones: se detecta",
     lanza(reg_b.verificar, rx.RegistroError) is not None)
reg, exp = base(); viejo = leer(reg.sello); reg.intento(exp, "v1", DESPUES); reg.sello.write_bytes(viejo)
caso("sello de un estado anterior del mismo registro: se detecta", lanza(reg.verificar, rx.RegistroError) is not None)

# 5. Sellos mal formados
for nombre, txt in (("vacío", ""), ("no JSON", "{"), ("lista", "[3]"), ("con clave de más", None), ("seq como texto", None),
                    ("seq booleano (seq 1)", None), ("seq 1.0 (seq 1)", None), ("bytes no UTF-8", None), ("directorio", None)):
    reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
    s = json.loads(reg.sello.read_text(encoding="utf-8"))
    if nombre == "con clave de más":
        txt = json.dumps({**s, "x": 1})
    elif nombre == "seq como texto":
        txt = json.dumps({**s, "seq": "1"})
    elif nombre == "seq booleano (seq 1)":
        txt = json.dumps({**s, "seq": True})
    elif nombre == "seq 1.0 (seq 1)":
        txt = json.dumps({**s, "seq": 1.0})
    if nombre == "bytes no UTF-8":
        reg.sello.write_bytes(b"\xff\xfe")
    elif nombre == "directorio":
        reg.sello.unlink(); reg.sello.mkdir()
    else:
        reg.sello.write_text(txt, encoding="utf-8")
    e = lanza(reg.verificar, Exception)
    if nombre in ("seq booleano (seq 1)", "seq 1.0 (seq 1)"):
        caso(f"(cosmético) sello con {nombre}: se acepta porque True == 1 == 1.0 en Python", True,
             f"verificar: {'acepta' if e is None else type(e).__name__}")
    else:
        caso(f"sello {nombre}: RegistroError", isinstance(e, rx.RegistroError), f"{type(e).__name__}: {str(e)[:80]}")
# 5b. con un sello directorio, ¿qué hace una escritura? (la línea va antes que el sello)
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
antes = leer(reg.ruta)
tmp = reg.sello.with_name(reg.sello.name + ".tmp"); tmp.mkdir()   # un «.sello.tmp» que no se puede escribir
e = lanza(lambda: reg.intento(exp, "v1", DESPUES), Exception)
caso("«.sello.tmp» que no se puede escribir: la escritura falla SIN dejar la línea (validar antes de mutar)",
     e is not None and leer(reg.ruta) == antes,
     f"{type(e).__name__}; líneas antes {antes.count(b'\n')}, después {leer(reg.ruta).count(b'\n')}; "
     f"verificar ahora: {lanza(reg.verificar, rx.RegistroError)}")

# 6. Sello rehecho por quien trunca (fuera de git): el implementador lo declara como límite
reg, exp = base(); ls = lineas(reg); escribir(reg, ls[:-1], sello=True)
caso("(regla declarada) truncar y rehacer el sello fuera de git no se detecta", lanza(reg.verificar) is None,
     "solo el ancla de git lo delata (r02_02)")
fin()
