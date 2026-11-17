"""QA r01 de T-175 (revisor): casos raros de `sintesis.alternativas_descartadas` y de las celdas de 4.N.4 y la sección 6.

    cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-175/revisores/r01_01_casos_raros.py
Imprime una línea por caso: OK (como se espera) o RARO (para el qa.md). Sale con 0 siempre: es un informe, no una prueba.
"""
import math
import re
import sys

sys.path.insert(0, ".")   # el paquete de esta copia, no el instalado
from bloque_a import redaccion as red  # noqa: E402
from bloque_a import sintesis as sint  # noqa: E402

MOT = [{"codigo": "OBJECION_FUERTE", "detalle": "1 objeción(es) fuerte(s) sin resolver"}]


def f(oid, rk=50, motivos=None, **kw):
    d = {"opp_id": oid, "nombre": f"Ámbito {oid}", "_ht03": {"elegible": False, "puntuaciones": {"RK": rk},
                                                           "motivos_no_elegible": MOT if motivos is None else motivos}}
    d.update(kw)
    return d


def alt(cands, paquete=None):
    return sint.alternativas_descartadas(paquete or {"clases": {}}, {"seleccion": {"RV": {"candidatos": cands}}})


def caso(nombre, fn):
    try:
        ok, detalle = fn()
        print(("OK   " if ok else "RARO ") + nombre + (f" · {detalle}" if detalle else ""))
    except Exception as e:   # noqa: BLE001
        print(f"RARO {nombre} · excepción {type(e).__name__}: {e}")


# 1. sin alternativas
caso("sin alternativas", lambda: (alt([]) == {} and sint.alternativas_descartadas({"clases": {}}, {"seleccion": {}}) == {}, ""))
# 2. más que max_finalistas (la función no recorta: depende de que aguas arriba solo haya finalistas GC3)
caso("8 no elegibles: se listan todas", lambda: (len(alt([f(f"OPP-2026-{i:04d}", rk=i) for i in range(1, 9)])["RV"]) == 8,
                                                 "la función no recorta; el tope sale de GC3 (ver H-03)"))
# 3. objeción fuerte sin «qué la resolvería» (None, vacío, no texto)
o = [{"objecion_id": "OBJ-A-01", "fuerza": "fuerte", "resumen": "R", "resuelta": False, "que_la_resolveria": q} for q in (None, "", "  ", 7)]
caso("fuerte sin qué_la_resolvería", lambda: ((a := alt([f("OPP-2026-0001", _objeciones=o)])["RV"][0])["condicion"]
                                             == ["Resolver las objeciones fuertes con evidencia"], a["condicion"]))
# 4. caracteres especiales en el nombre
for nombre in ("A | B", "A\nB", "A\r\nB", "A B", "A `x` B", "<script>alert(1)</script>", "**negrita**", "", None, 123, "A \\| B"):
    def _n(nombre=nombre):
        a = alt([f("OPP-2026-0001", nombre=nombre)])["RV"][0]
        celda = red._celda(a["nombre"])
        fila = f"| {celda} · `x` | G2 | m | c |"
        partes = re.split(r"(?<!\\)\|", fila.strip().strip("|"))
        return len(partes) == 4 and "\n" not in fila, repr(celda)
    caso(f"nombre {nombre!r}", _n)
# 5. RK raros
for rk in (True, -5, math.nan, math.inf, "70", 0):
    def _r(rk=rk):
        out = alt([f("OPP-2026-0001", rk=rk), f("OPP-2026-0002", rk=50), f("OPP-2026-0003", rk=None)])["RV"]
        return True, f"orden {[x['opp_id'][-1] for x in out]} · rk mostrado {out[[x['opp_id'] for x in out].index('OPP-2026-0001')]['rk']!r}"
    caso(f"RK {rk!r}", _r)
# 6. estructuras internas mal formadas (HT-03 las escribe el ejecutor; se mira si rompen el informe)
for etiqueta, kw in (("puntuaciones lista", {"_ht03": {"elegible": False, "puntuaciones": [], "motivos_no_elegible": MOT}}),
                     ("motivos int", {"_ht03": {"elegible": False, "motivos_no_elegible": 3}}),
                     ("_objeciones int", {"_objeciones": 3}),
                     ("_objeciones dict", {"_objeciones": {"fuerza": "fuerte"}}),
                     ("detalle None", {"_ht03": {"elegible": False, "motivos_no_elegible": [{"codigo": "E_BAJO", "detalle": None, "falta": None}]}})):
    caso(f"mal formada: {etiqueta}", lambda kw=kw: (True, repr(alt([f("OPP-2026-0001", **kw)]).get("RV", [{}])[0].get("motivo"))))
# 7. idempotencia y no mutación
c = [f("OPP-2026-0001", _objeciones=[{"objecion_id": "OBJ-A-01", "fuerza": "fuerte", "resumen": "R", "resuelta": False,
                                     "que_la_resolveria": "Q"}])]
import copy  # noqa: E402
antes = copy.deepcopy(c)
caso("idempotente y sin mutar la entrada", lambda: (alt(c) == alt(c) and c == antes, ""))
# 8. orden de llamada: la misma candidata en dos clases
caso("misma OPP en dos clases", lambda: (True, str({k: [x["opp_id"] for x in v] for k, v in sint.alternativas_descartadas(
    {"clases": {}}, {"seleccion": {"RV": {"candidatos": [f("OPP-2026-0001")]}, "RF": {"candidatos": [f("OPP-2026-0001")]}}}).items()})))
