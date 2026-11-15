"""r01_03 · Ficheros dañados: no UTF-8, BOM, CRLF, JSON válido con otro esquema y cadena correcta, línea que no es un objeto,
y la línea de órdenes ante ellos (¿código 2 y mensaje, o traza?). Uso: python3 r01_03_ficheros_danados.py <raíz>"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import AHORA, DESPUES, RAIZ, caso, escribir, fin, lanza, lineas, pre, recadenar, registro_temporal, rx  # noqa: E402

CLI = RAIZ / ".docs" / "scripts" / "registro_experimentos.py"


def cli(reg, *args):
    p = subprocess.run([sys.executable, str(CLI), "--registro", str(reg.ruta), *args], capture_output=True, text=True)
    return p.returncode, (p.stderr.strip().splitlines() or [""])[-1]


# 1. bytes no UTF-8
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
with open(reg.ruta, "ab") as f:
    f.write(b'\xff\xfe{"x": 1}\n')
e = lanza(reg.verificar, Exception)
caso("bytes no UTF-8: la biblioteca lanza RegistroError", isinstance(e, rx.RegistroError), repr(e)[:120])
rc, msg = cli(reg, "verificar")
caso("bytes no UTF-8: la línea de órdenes sale con 2 y un mensaje", rc == 2, f"rc={rc} · {msg[:120]}")

# 2. BOM al principio (lo pone un editor de Windows)
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
raw = reg.ruta.read_bytes(); reg.ruta.write_bytes(b"\xef\xbb\xbf" + raw)
e = lanza(reg.verificar, Exception)
caso("BOM inicial: falla cerrado con RegistroError", isinstance(e, rx.RegistroError), repr(e)[:120])

# 3. CRLF: el contenido es el mismo
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]; reg.intento(exp, "v1", DESPUES)
reg.ruta.write_bytes(reg.ruta.read_bytes().replace(b"\n", b"\r\n"))
e = lanza(reg.verificar, Exception)
caso("CRLF: se lee igual (mismo contenido)", e is None, repr(e)[:120] if e else "")

# 4. JSON válido con otro esquema y la cadena bien calculada: sin «tipo»
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
objs = [json.loads(x) for x in lineas(reg)] + [{"hola": "mundo"}]
escribir(reg, recadenar(objs))
e = lanza(reg.verificar, Exception)
caso("anotación sin «tipo» con cadena correcta: verificar() la rechaza", e is not None, f"verificar = {reg.verificar() if e is None else e!r}")
e = lanza(lambda: reg.intento(exp, "v1", DESPUES), Exception)
caso("…y anotar después falla con RegistroError (no KeyError)", isinstance(e, rx.RegistroError), repr(e)[:120])
rc, msg = cli(reg, "intento", exp)
caso("…y la línea de órdenes sale con 2 y un mensaje, no con una traza", rc == 2, f"rc={rc} · {msg[:120]}")
rc, msg = cli(reg, "ver")
caso("…y «ver» sale con 2 y un mensaje", rc == 2, f"rc={rc} · {msg[:120]}")

# 5. tipo desconocido con todos los campos y cadena correcta
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]
objs = [json.loads(x) for x in lineas(reg)] + [{"tipo": "BORRADO", "exp_id": exp, "n": 1}]
escribir(reg, recadenar(objs))
e = lanza(reg.verificar, Exception)
caso("anotación de un tipo que no existe (BORRADO) con cadena correcta: se rechaza", e is not None,
     f"verificar = {reg.verificar() if e is None else e!r}")

# 6. resultado con veredicto inventado y cadena correcta (escrito a mano)
reg = registro_temporal(); exp = reg.prerregistrar(pre(), "qa", AHORA)["exp_id"]; reg.intento(exp, "v1", DESPUES)
objs = [json.loads(x) for x in lineas(reg)] + [{"tipo": "RESULTADO", "exp_id": exp, "n": 1, "veredicto": "mejor", "detalle": {},
                                                "registrado_en": DESPUES}]
objs[1]["dentro_del_maximo"] = True
escribir(reg, recadenar(objs))
caso("(referencia) un resultado escrito a mano con la cadena recalculada pasa verificar()", reg.verificar() == 3)

# 7. intento escrito a mano que se declara dentro del máximo siendo la variante 3 de max 2
reg = registro_temporal(); exp = reg.prerregistrar(pre(max_variantes=1), "qa", AHORA)["exp_id"]
reg.intento(exp, "v1", DESPUES); reg.resultado(exp, 1, "peor", ahora=DESPUES)
reg.intento(exp, "v2", DESPUES)
objs = [json.loads(x) for x in lineas(reg)]
objs[3]["dentro_del_maximo"] = True
objs.append({"tipo": "RESULTADO", "exp_id": exp, "n": 2, "veredicto": "mejor", "detalle": {}, "registrado_en": DESPUES})
escribir(reg, recadenar(objs))
caso("«dentro_del_maximo» falseado (cadena recalculada): resumen() lo recalcula y no lo da por adoptable",
     not reg.adoptable(exp), f"adoptable = {reg.adoptable(exp)}: resumen() se fía del campo guardado")

# 8. línea que es una lista JSON
reg = registro_temporal(); reg.prerregistrar(pre(), "qa", AHORA)
with open(reg.ruta, "a", encoding="utf-8") as f:
    f.write("[1, 2]\n")
e = lanza(reg.verificar, Exception)
caso("línea que es una lista JSON: RegistroError", isinstance(e, rx.RegistroError), repr(e)[:100])

# 9. fichero que es un directorio
reg = registro_temporal(); reg.ruta.mkdir()
rc, msg = cli(reg, "verificar")
caso("--registro que es un directorio: 2 y mensaje", rc == 2, f"rc={rc} · {msg[:100]}")
fin()
