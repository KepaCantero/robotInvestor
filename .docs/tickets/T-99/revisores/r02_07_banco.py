"""r02_07 · Interfaz del banco de medida con el registro 0.2.0 (con dobles del titular y de la estadística, como r01_09):
--sin-registro, fallo al escribir prerregistro.json, --experimento con otro máximo, motivo de fallo que no es UTF-8, corte
del sello al anotar el resultado, «.lock» que es un directorio y dos bancos a la vez sobre un registro nuevo.
Uso: .venv/bin/python -B r02_07_banco.py <raíz>"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r02_comun import RAIZ, SCRIPTS, caso, fin, lanza, leer, rx, tmpdir  # noqa: E402

import banco_medida as bm  # noqa: E402

TMP = tmpdir("r02_t99_banco_")
UNIV = TMP / "universo.csv"; UNIV.write_text("simbolo,clase\nS0,C\n", encoding="utf-8")
cola, fallo = [], {"en": None}


def titular_falso(*a, **k):
    if fallo["en"] == "titular":
        raise RuntimeError("el titular revienta")
    if fallo["en"] == "surrogate":
        raise FileNotFoundError("no existe " + b"/datos/\xff.csv".decode("utf-8", "surrogateescape"))
    return {"universo": str(UNIV), "datos": str(TMP), "selecciones": [], "fecha_fin": "2025-05-30", "consumo": {}}


bm.titular_a = titular_falso
bm.cargar_precios = lambda *a, **k: None
bm.evaluar = lambda *a, **k: {}
bm.azar = lambda *a, **k: []
bm.momento = lambda *a, **k: []
bm.construir_informe = lambda *a, **k: {"comparaciones": {"azar": {"veredicto": cola[0]}, "momento": {"veredicto": cola.pop(0)}}}
bm.informe_md = lambda *a, **k: ""
bm._aviso = lambda *a, **k: None


def ns(reg, salida, **kw):
    d = {"desde": "2025-03-07", "hasta": "2025-05-30", "salida": str(TMP / salida), "cliente": "mock", "frecuencia": None,
         "clases": None, "semilla": 7, "remuestreos": 2000, "ventana": 63, "registro": str(reg) if reg else None,
         "experimento": None, "max_variantes": 1}
    d.update(kw)
    return argparse.Namespace(**d)


def ultimo_resultado(reg):
    rs = [x for x in rx.Registro(reg).anotaciones() if x["tipo"] == "RESULTADO"]
    return rs[-1]["veredicto"] if rs else None


# 1. --sin-registro: no anota nada y «verificar» lo dice
REG = TMP / "r1.jsonl"
cola.append("mejor"); bm.ejecutar_a(ns(None, "s1"))
caso("--sin-registro: no crea el registro ni experimento.json", not REG.exists() and not (TMP / "s1" / "experimento.json").exists())
caso("…y «verificar» de esa carpeta lo dice", any("experimento.json" in p for p in bm.verificar(TMP / "s1")), str(bm.verificar(TMP / "s1")))
cola.append("mejor")
rc = bm.main(["a", "--desde", "2025-03-07", "--hasta", "2025-05-30", "--salida", str(TMP / "s1m"), "--sin-registro"])
caso("--sin-registro desde la línea de órdenes del banco: código 0 y sin experimento.json ni registro del repositorio",
     rc == 0 and not (TMP / "s1m" / "experimento.json").exists() and not (RAIZ / ".docs" / "experimentos").exists(), f"rc={rc}")

# 2. prerregistro.json que no se puede escribir (es un directorio): el intento queda «fallido» (r01 H-08.3)
REG = TMP / "r2.jsonl"; (TMP / "s2").mkdir(); (TMP / "s2" / "prerregistro.json").mkdir()
e = lanza(lambda: bm.ejecutar_a(ns(REG, "s2")), BaseException)
caso("prerregistro.json imposible de escribir: falla y el intento queda «fallido»", e is not None and ultimo_resultado(REG) == "fallido",
     f"{type(e).__name__}; último resultado {ultimo_resultado(REG)}")

# 3. --experimento con otro máximo: BancoError y el registro sin tocar
REG = TMP / "r3.jsonl"; cola.append("peor"); bm.ejecutar_a(ns(REG, "s3"))
exp = next(x["exp_id"] for x in rx.Registro(REG).anotaciones() if x["tipo"] == "PRERREGISTRO")
antes = leer(REG)
e = lanza(lambda: bm.ejecutar_a(ns(REG, "s3b", experimento=exp, max_variantes=3)), Exception)
caso("--experimento con otro --max-variantes: BancoError y el registro sin tocar", isinstance(e, bm.BancoError) and leer(REG) == antes)
e = lanza(lambda: bm.ejecutar_a(ns(REG, "s3c", experimento="EXP-2026-9999")), Exception)
caso("--experimento que no existe: BancoError y sin tocar", isinstance(e, bm.BancoError) and leer(REG) == antes, f"{type(e).__name__}")

# 4. Un fallo cuyo mensaje lleva bytes que no son UTF-8 (una ruta del sistema): ¿queda «fallido»?
REG = TMP / "r4.jsonl"; fallo["en"] = "surrogate"
e = lanza(lambda: bm.ejecutar_a(ns(REG, "s4")), BaseException); fallo["en"] = None
r = rx.Registro(REG)
caso("fallo con una ruta no UTF-8 en el mensaje: el intento queda «fallido» (CA-5)", ultimo_resultado(REG) == "fallido",
     f"sale {type(e).__name__}: {str(e)[:90]}; intentos sin resultado: {r.resumen(r.anotaciones()[0]['exp_id'])['sin_resultado']}")
caso("…y el error que sale es el original o un BancoError, no un UnicodeEncodeError", isinstance(e, (FileNotFoundError, bm.BancoError)),
     f"{type(e).__name__}")

# 5. Corte del sello al anotar el resultado (disco lleno justo ahí)
REG = TMP / "r5.jsonl"; cola.append("mejor")
real = os.replace
llamadas = {"n": 0}


def replace_que_falla_al_final(a, b):
    llamadas["n"] += 1
    if llamadas["n"] == 3:   # 1: prerregistro, 2: intento, 3: resultado
        raise OSError("simulado: sin espacio al mover el sello")
    return real(a, b)


os.replace = replace_que_falla_al_final
e = lanza(lambda: bm.ejecutar_a(ns(REG, "s5")), BaseException); os.replace = real
caso("corte del sello en el resultado: el banco se detiene con BancoError (código 2, sin traza)", isinstance(e, bm.BancoError),
     f"sale {type(e).__name__}: {str(e)[:80]}")
caso("…y el registro queda bloqueado (falla cerrado, sin herramienta para recuperarlo)",
     lanza(rx.Registro(REG).verificar, rx.RegistroError) is not None)

# 6. «.lock» que es un directorio
REG = TMP / "r6.jsonl"; REG.with_name("r6.jsonl.lock").mkdir()
e = lanza(lambda: bm.main(["a", "--desde", "2025-03-07", "--hasta", "2025-05-30", "--salida", str(TMP / "s6"), "--registro", str(REG)]),
          BaseException)
caso("«.lock» directorio desde la línea de órdenes del banco: código 2 sin traza", e is None, f"{type(e).__name__ if e else ''}")

# 7. Dos bancos a la vez sobre un registro nuevo: ¿uno o dos prerregistros de la misma hipótesis y fuente?
HIJO = r"""
import argparse, sys, time
sys.path.insert(0, sys.argv[1])
import banco_medida as bm
bm.titular_a = lambda *a, **k: {"universo": sys.argv[4], "datos": sys.argv[3], "selecciones": [], "fecha_fin": "2025-05-30", "consumo": {}}
bm.cargar_precios = lambda *a, **k: None; bm.evaluar = lambda *a, **k: {}; bm.azar = lambda *a, **k: []; bm.momento = lambda *a, **k: []
bm.construir_informe = lambda *a, **k: {"comparaciones": {"azar": {"veredicto": "mejor"}, "momento": {"veredicto": "mejor"}}}
bm.informe_md = lambda *a, **k: ""; bm._aviso = lambda *a, **k: None
t0 = float(sys.argv[7])
while time.time() < t0:
    pass
try:
    bm.ejecutar_a(argparse.Namespace(desde="2025-03-07", hasta="2025-05-30", salida=sys.argv[5], cliente="mock", frecuencia=None,
        clases=None, semilla=int(sys.argv[6]), remuestreos=2000, ventana=63, registro=sys.argv[2], experimento=None, max_variantes=1))
    print("ok")
except Exception as e:
    print("error", type(e).__name__, e)
"""
dobles = 0; rondas = 6
for ronda in range(rondas):
    REG = TMP / f"r7_{ronda}.jsonl"; t0 = time.time() + 1.0
    ps = [subprocess.Popen([sys.executable, "-B", "-c", HIJO, str(SCRIPTS), str(REG), str(TMP), str(UNIV), str(TMP / f"s7_{ronda}_{k}"),
                            str(7 + k), str(t0)], stdout=subprocess.PIPE, text=True) for k in range(2)]
    [p.communicate() for p in ps]
    reg = rx.Registro(REG)
    pres = [x for x in reg.anotaciones() if x["tipo"] == "PRERREGISTRO"]
    if len(pres) > 1 and all(reg.adoptable(x["exp_id"]) for x in pres):
        dobles += 1
caso("dos bancos a la vez con semillas distintas y max 1: no quedan dos experimentos de la misma hipótesis y fuente, cada uno "
     "con su variante «dentro del máximo» y adoptable", dobles == 0,
     f"{dobles}/{rondas} rondas con dos prerregistros iguales y las dos variantes adoptables (la elección reutilizar/prerregistrar "
     "se hace fuera del cerrojo)")
fin()
