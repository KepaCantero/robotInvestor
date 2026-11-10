"""QA r01 de T-72 (V0.69, T-85): valores raros en las tolerancias del Reloj, por la vía pública y tocando lo privado (`_tol`).

Para cada posición (salto, desfase, contraste) y cada veneno (NaN, inf, -inf, negativos, cero, bool, texto, None, Decimal,
enteros enormes, 1e308), en un reloj ya contrastado:
  A. ¿lanza alguna operación (ahora, contrastar, comprobar_estado, estado, rearmar) o el panel?
  B. ¿da instantes pasado el tope de contraste por defecto (24 h), leyendo cada hora durante diez días, sin contrastar otra vez?
  C. ¿da instantes tras un salto de una hora del reloj de pared?
  D. ¿un reloj bloqueado se desbloquea por la tolerancia rara?
  E. ¿pinta el panel VERDE con diez días sin contraste?
  F. ¿acepta contrastar con una referencia que difiere un día?
Además: `_tol` entero sustituido (None, (), tupla corta, texto) y la vía pública (setattr, del, __dict__, object.__setattr__),
y el constructor con un `max_sin_contraste_s` finito enorme (sin tope, a diferencia de salto y desfase).

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.69/qa/r01_02_tolerancias_raras.py
Imprime una tabla; «HALLAZGO» marca lo que contradice la frase «una tolerancia rota bloquea o no da instantes, y el reloj
sigue sin lanzar» del Documento 0 de la V0.69. Sale con 1 si hay alguno.
"""
import os
import sys
from decimal import Decimal

M = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(M, "validador"))
sys.path.insert(0, os.path.join(M, "pruebas"))
import reloj as rl  # noqa: E402
from pruebas_consola_sistema import comp  # noqa: E402
from pruebas_orquestador import AHORA, nuevo  # noqa: E402
from pruebas_reloj_t03 import iso, nuevo_reloj  # noqa: E402

DIEZ_DIAS = 10 * 86400.0
VENENOS = [("nan", float("nan")), ("inf", float("inf")), ("-inf", float("-inf")), ("-1", -1.0), ("0", 0.0), ("-0.0", -0.0),
           ("True", True), ("False", False), ("texto", "2"), ("None", None), ("Decimal(NaN)", Decimal("NaN")),
           ("Decimal(Inf)", Decimal("Infinity")), ("10**400", 10 ** 400), ("1e308", 1e308)]
hallazgos = []


class Est:
    def __init__(self, u):
        self.ultimo_ahora = u


def con_tol(pos, v, contrastar=True):
    f, r = nuevo_reloj(contrastar=contrastar)
    t = list(r._tol)
    t[pos] = v
    r._tol = tuple(t)
    return f, r


def seguro(fn):
    try:
        return fn(), None
    except Exception as ex:   # noqa: BLE001
        return None, f"{type(ex).__name__}: {ex}"[:80]


print(f"{'pos':10} {'veneno':14} {'lanza':6} {'10 días':8} {'salto 1h':9} {'desbloq':8} {'panel':6} {'ref 1d':7}")
for pos, nom in enumerate(("salto", "desfase", "contraste")):
    for etq, v in VENENOS:
        lanza = []
        # A + B: diez días sin contraste, leyendo cada hora (sin saltos)
        f, r = con_tol(pos, v)
        dio_tarde = False
        for k in range(240):
            f.pasa(3600.0)
            x, e = seguro(r.ahora)
            if e:
                lanza.append(("ahora", e))
                break
            if x["ok"] and (k + 1) * 3600.0 > rl.MAX_SIN_CONTRASTE_S:   # pasado el tope de contraste por defecto
                dio_tarde = True
        for nombre, fn in (("estado", r.estado), ("comprobar_estado", lambda: r.comprobar_estado(Est(iso(f.p)))),
                           ("contrastar", lambda: r.contrastar(iso(f.p), "REF")),
                           ("panel", lambda: comp(nuevo(), "reloj", reloj=r))):
            _, e = seguro(fn)
            if e:
                lanza.append((nombre, e))
        # E: panel con diez días sin contraste (reloj recién contrastado, sin lecturas intermedias)
        f, r = con_tol(pos, v)
        f.pasa(DIEZ_DIAS)
        p, e = seguro(lambda: comp(nuevo(), "reloj", reloj=r))
        panel_n = p["nivel"] if p else "LANZA"
        # C: salto de una hora del reloj de pared
        f, r = con_tol(pos, v)
        f.pasa(1.0, pared=3601.0)
        x, e = seguro(r.ahora)
        salto = bool(x and x["ok"])
        # D: bloqueado (salto) y luego leer otra vez
        f, r = con_tol(pos, v)
        f.pasa(1.0, pared=-3600.0)
        seguro(r.ahora)
        bloq_antes = r.bloqueo is not None
        f.pasa(1.0)
        x, e = seguro(r.ahora)
        desbloq = bloq_antes and (r.bloqueo is None or bool(x and x["ok"]))
        # F: contraste con una referencia que va un día por detrás o por delante
        f, r = con_tol(pos, v, contrastar=False)
        x1, _ = seguro(lambda: r.contrastar(iso(f.p - 86400.0), "REF"))
        f, r = con_tol(pos, v, contrastar=False)
        x2, _ = seguro(lambda: r.contrastar(iso(f.p + 86400.0), "REF"))
        ref_dia = bool(x1 and x1["ok"]) or bool(x2 and x2["ok"])
        malo = bool(lanza) or dio_tarde or salto or desbloq or panel_n == "VERDE" or ref_dia
        print(f"{nom:10} {etq:14} {('SÍ' if lanza else 'no'):6} {('SÍ' if dio_tarde else 'no'):8} {('SÍ' if salto else 'no'):9} "
              f"{('SÍ' if desbloq else 'no'):8} {panel_n:6} {('SÍ' if ref_dia else 'no'):7} {'HALLAZGO' if malo else ''} {lanza[:2] if lanza else ''}")
        if malo:
            hallazgos.append((nom, etq, lanza[:1], dio_tarde, salto, desbloq, panel_n, ref_dia))

# _tol sustituido entero
print()
for etq, v in (("None", None), ("()", ()), ("(2.0,)", (2.0,)), ("texto", "abc"), ("lista", [2.0, 5.0, 86400.0])):
    f, r = nuevo_reloj()
    r._tol = v
    f.pasa(1.0)
    res = {}
    for nombre, fn in (("ahora", r.ahora), ("contrastar", lambda: r.contrastar(iso(f.p), "REF")),
                       ("comprobar_estado", lambda: r.comprobar_estado(Est(iso(f.p)))), ("estado", r.estado),
                       ("panel", lambda: comp(nuevo(), "reloj", reloj=r)["nivel"])):
        x, e = seguro(fn)
        res[nombre] = ("LANZA " + e) if e else (x if nombre == "panel" else x.get("codigo", "foto"))
    lanza = [k for k, w in res.items() if str(w).startswith("LANZA")]
    print(f"_tol = {etq:8}", res, "HALLAZGO" if lanza else "")
    if lanza:
        hallazgos.append(("_tol entero", etq, lanza))

# vía pública
print()
f, r = nuevo_reloj()
for intento, fn in (("setattr", lambda: setattr(r, "max_sin_contraste_s", float("nan"))),
                    ("delattr", lambda: delattr(r, "max_sin_contraste_s")),
                    ("__dict__", lambda: r.__dict__.__setitem__("max_sin_contraste_s", float("nan"))),
                    ("object.__setattr__", lambda: object.__setattr__(r, "max_sin_contraste_s", float("nan")))):
    _, e = seguro(fn)
    print(f"vía pública {intento:20}: {'rechazado' if e else 'aceptado'}; max_sin_contraste_s = {r.max_sin_contraste_s}")
f.pasa(DIEZ_DIAS)
x = r.ahora()
print("tras los intentos, diez días después: ahora() ok =", x["ok"], x["codigo"])
if x["ok"]:
    hallazgos.append(("vía pública", "instantes sin contrastar"))

# constructor: contraste finito enorme (salto y desfase tienen tope; contraste no)
print()
for c in (1e308, 1e12):
    try:
        f, r = nuevo_reloj(max_sin_contraste_s=c)
    except ValueError:
        print(f"constructor max_sin_contraste_s={c}: rechazado")
        continue
    f.pasa(365 * 86400.0)
    x = r.ahora()
    print(f"constructor max_sin_contraste_s={c}: aceptado; un año sin contrastar, ahora() ok = {x['ok']}; panel =",
          comp(nuevo(), "reloj", reloj=r)["nivel"], "HALLAZGO (anterior a la V0.69)" if x["ok"] else "")
    if x["ok"]:
        hallazgos.append(("constructor", c))

print(f"\n{len(hallazgos)} casos marcados")
print("RESULTADO r01_02:", "SIN HALLAZGOS" if not hallazgos else "HAY HALLAZGOS")
sys.exit(1 if hallazgos else 0)
