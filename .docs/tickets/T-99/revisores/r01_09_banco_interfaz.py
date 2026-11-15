"""r01_09 · Interfaz del banco de medida con el registro (solo la interfaz: el banco pasó su QA en T-94). Se sustituye el
titular y la estadística por dobles para controlar el veredicto de cada ejecución (titular no determinista).
Uso: .venv/bin/python -B r01_09_banco_interfaz.py <raíz>"""
import argparse
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r01_comun import RAIZ, caso, fin, rx  # noqa: E402

import banco_medida as bm  # noqa: E402  (r01_comun ya puso .docs/scripts en sys.path)

TMP = Path(tempfile.mkdtemp(prefix="r01_t99_banco_"))
UNIV = TMP / "universo.csv"; UNIV.write_text("simbolo,clase\nS0,C\n", encoding="utf-8")
cola = []          # veredictos que dará cada ejecución
fallo = {"en": None}


def titular_falso(*a, **k):
    if fallo["en"] == "titular":
        raise RuntimeError("el titular revienta")
    return {"universo": str(UNIV), "datos": str(TMP), "selecciones": [], "fecha_fin": "2025-05-30", "consumo": {}}


def informe_falso(*a, **k):
    if fallo["en"] == "registro_roto":
        with open(REG, "a", encoding="utf-8") as f:   # otro proceso rompe la cadena mientras el banco evalúa
            f.write('{"x": 1}\n')
    v = cola.pop(0)
    return {"comparaciones": {"azar": {"veredicto": v}, "momento": {"veredicto": v}}}


bm.titular_a = titular_falso
bm.cargar_precios = lambda *a, **k: None
bm.evaluar = lambda *a, **k: {}
bm.azar = lambda *a, **k: []
bm.momento = lambda *a, **k: []
bm.construir_informe = informe_falso
bm.informe_md = lambda *a, **k: ""
bm._aviso = lambda *a, **k: None
REG = TMP / "reg.jsonl"


def ns(salida, **kw):
    d = {"desde": "2025-03-07", "hasta": "2025-05-30", "salida": str(TMP / salida), "cliente": "anthropic", "frecuencia": None,
         "clases": None, "semilla": 7, "remuestreos": 2000, "ventana": 63, "registro": str(REG), "experimento": None, "max_variantes": 1}
    d.update(kw)
    return argparse.Namespace(**d)


# 1. Titular no determinista: misma orden cuatro veces
for i, v in enumerate(("peor", "peor", "todavía no se sabe", "mejor")):
    cola.append(v); bm.ejecutar_a(ns(f"r{i}"))
reg = rx.Registro(REG)
exp = next(x["exp_id"] for x in reg.anotaciones() if x["tipo"] == "PRERREGISTRO")
r = reg.resumen(exp)
caso("banco: repetir la misma orden hasta que sale «mejor» no deja el experimento adoptable (T-133, H-21)", not r["adoptable"],
     f"variantes={r['variantes']}, veredictos={r['veredictos']}, adoptables={r['adoptables']}")

# 2. --max-variantes en una ejecución posterior se ignora sin avisar
cola.append("peor"); inf = bm.ejecutar_a(ns("m5", semilla=8, max_variantes=5))
caso("--max-variantes 5 al reutilizar un experimento de máximo 1: se rechaza o se avisa", inf["experimento"]["dentro_del_maximo"]
     or any("max" in x for x in inf.get("advertencias_titular", [])),
     f"dentro_del_maximo={inf['experimento']['dentro_del_maximo']}, sin aviso: el máximo prerregistrado manda en silencio")

# 3. --registro "" desactiva el registro sin decirlo
cola.append("mejor"); antes = REG.read_bytes()
inf = bm.ejecutar_a(ns("vacio", registro=""))
caso("--registro vacío: el banco se niega o avisa (cada ejecución de la línea de órdenes cuenta)",
     REG.read_bytes() != antes or "experimento" in inf, "ejecuta sin anotar nada y sin aviso; solo «verificar» lo notaría")

# 4. Fallo del titular: queda «fallido» (CA-5)
fallo["en"] = "titular"
try:
    bm.ejecutar_a(ns("f1"))
except RuntimeError:
    pass
fallo["en"] = None
r = reg.resumen(exp)
caso("un titular que revienta deja el intento como «fallido» (CA-5)", r["veredictos"][str(r["intentos"])] == "fallido")

# 5. Fallo al escribir prerregistro.json (después del intento y fuera del try): ¿queda «fallido»?
(TMP / "f2").mkdir(); (TMP / "f2" / "prerregistro.json").mkdir()
try:
    bm.ejecutar_a(ns("f2"))
    e5 = None
except Exception as e:
    e5 = e
r = reg.resumen(exp)
caso("un fallo al escribir prerregistro.json deja el intento como «fallido»", not r["sin_resultado"],
     f"error {type(e5).__name__}; sin_resultado={r['sin_resultado']}")

# 6. Cadena rota entre el intento y el resultado: ¿BancoError (código 2) o excepción cruda?
REG2 = TMP / "reg2.jsonl"; REG = REG2
fallo["en"] = "registro_roto"; cola.append("mejor")
try:
    bm.ejecutar_a(ns("rr", registro=str(REG2)))
    e6 = None
except Exception as e:
    e6 = e
fallo["en"] = None
caso("cadena rota a mitad de ejecución: el banco para con BancoError (código 2 en la línea de órdenes)", isinstance(e6, bm.BancoError),
     f"sale {type(e6).__name__}: {str(e6)[:80]}")

# 7. Documentación: ¿el periodo forma parte de la identidad del experimento?
doc = bm.__doc__
caso("docstring del banco y código dicen lo mismo sobre el periodo", "misma hipótesis, objeto y periodo" not in doc,
     "el docstring dice «misma hipótesis, objeto y periodo»; el código y la prueba H-14 tratan otro periodo como otra variante")
caso("el registro del repositorio no se tocó", not (RAIZ / ".docs" / "experimentos").exists())
fin()
