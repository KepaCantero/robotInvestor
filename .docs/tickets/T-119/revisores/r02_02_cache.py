"""QA r02 de T-119 · caché del Motor (H-06 y H-08 de la r01).

 1. Tipos: se sirve una petición válida y después la misma con un valor de otro tipo (np.float32, Decimal, texto, tupla en vez
    de lista, clave entera en vez de texto, bool en vez de 1, np.int64). Cada variante se sirve también SOLA en un Motor
    nuevo: la caché no puede dar lo que la ficha sola no daría (CACHE_HIT solo si el resultado es el mismo que sin caché).
 2. Configuración en caliente: cambiar m.cfg (sustituir la sección, mutarla en su sitio, quitarla) y la copia en memoria de
    por_defecto.yaml (sección que el Motor no trae): la caché no entrega lo calculado con la configuración anterior.
Uso: .venv/bin/python -I .docs/tickets/T-119/revisores/r02_02_cache.py [ejecutor]
"""
import copy
import decimal
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a import configuracion  # noqa: E402

K = C.Contador("r02_02 T-119 caché")


def resumen(r):
    if r is None:
        return None
    return (str(r["estado"]).startswith("SERVED"), json.dumps(r.get("resultado"), sort_keys=True, default=str) if r.get("resultado") else r.get("detalle", "")[:80])


def servir(m, p):
    r, exc, n = C.servir_contando(m, p)
    return r, exc, n


print("[1] tipos que no son JSON")
VARIANTES = {
    "np.float32": lambda c: c.__setitem__("capitalizacion", np.float32(c["capitalizacion"])),
    "Decimal": lambda c: c.__setitem__("capitalizacion", decimal.Decimal(str(c["capitalizacion"]))),
    "texto": lambda c: c.__setitem__("capitalizacion", str(c["capitalizacion"])),
    "np.int64": lambda c: c.__setitem__("capitalizacion", np.int64(int(c["capitalizacion"]))),
    "bool por 1": lambda c: c.__setitem__("mu_historico", True),
    "np.float64": lambda c: c.__setitem__("capitalizacion", np.float64(c["capitalizacion"])),
}
for nombre, cambio in VARIANTES.items():
    m = C.motor()
    p0 = C.peticion("FIR-CRED-001")
    r0, _, _ = servir(m, p0)
    p1 = C.peticion("FIR-CRED-001")
    cambio(p1["datos"][0]["valores"]["componentes"][0])
    r1, e1, n1 = servir(m, p1)
    solo, es, _ = servir(C.motor(), copy.deepcopy(p1))
    hit = bool(r1 and r1.get("cache_hit"))
    igual = resumen(r1) == resumen(solo)
    print(f"    {nombre:12s} tras la válida: {'CACHE_HIT' if hit else (r1 or {}).get('estado')} · sola: {(solo or {}).get('estado')} · mismo resultado {igual}")
    K.comprobar(f"{nombre}: lo servido tras la válida es lo mismo que sola (sin colarse por la caché)", e1 is None and igual and n1 == 1,
                f"{resumen(r1)} != {resumen(solo)}")
# tupla en vez de lista, clave entera
for nombre, cambio in (("tupla de componentes", lambda v: v.__setitem__("componentes", tuple(v["componentes"]))),
                       ("segmento con clave entera", lambda v: v["segmento"].__setitem__(1, "x"))):
    m = C.motor()
    servir(m, C.peticion("FIR-CRED-001"))
    p1 = C.peticion("FIR-CRED-001")
    cambio(p1["datos"][0]["valores"])
    r1, e1, n1 = servir(m, p1)
    solo, _, _ = servir(C.motor(), copy.deepcopy(p1))
    print(f"    {nombre}: tras la válida {(r1 or {}).get('estado')} hit={bool(r1 and r1.get('cache_hit'))} · sola {(solo or {}).get('estado')}")
    K.comprobar(f"{nombre}: igual que sola", e1 is None and resumen(r1) == resumen(solo), f"{resumen(r1)} != {resumen(solo)}")

print("\n[2] configuración en caliente (FX-BEER-001 lee evaluacion.nivel_ic)")
p = C.peticion("FX-BEER-001")


def ic(r):
    return json.dumps(r["resultado"], sort_keys=True, default=str) if r and str(r["estado"]).startswith("SERVED") else r and r.get("detalle")


def nuevo_igual(cfg_extra=None, defecto=None):
    """Resultado de un Motor nuevo con esa configuración (la referencia)."""
    if defecto is not None:
        configuracion._CONFIG_POR_DEFECTO = defecto
    try:
        m2 = C.motor(**(cfg_extra or {}))
        if cfg_extra is None and defecto is not None:
            m2.cfg.pop("evaluacion", None)
        return ic(m2.servir(copy.deepcopy(p), "AG-18"))
    finally:
        configuracion._CONFIG_POR_DEFECTO = ORIG


ORIG = copy.deepcopy(configuracion.config_por_defecto())
casos = []
m = C.motor()
r_a = m.servir(copy.deepcopy(p), "AG-18")
m.cfg["evaluacion"] = {**m.cfg["evaluacion"], "nivel_ic": 0.99}
r_b = m.servir(copy.deepcopy(p), "AG-18")
casos.append(("sustituir la sección", r_b, nuevo_igual({"evaluacion": {"nivel_ic": 0.99}})))
m.cfg["evaluacion"]["nivel_ic"] = 0.8
r_c = m.servir(copy.deepcopy(p), "AG-18")
casos.append(("mutar la sección en su sitio", r_c, nuevo_igual({"evaluacion": {"nivel_ic": 0.8}})))
m.cfg["evaluacion"]["nivel_ic"] = 0.99   # vuelve a un valor ya calculado: puede salir de la caché, pero con esas cifras
r_d = m.servir(copy.deepcopy(p), "AG-18")
casos.append(("volver a un valor anterior", r_d, nuevo_igual({"evaluacion": {"nivel_ic": 0.99}})))
# sección que el Motor no trae: se toma de por_defecto.yaml; cambiar la copia en memoria
m = C.motor()
m.cfg.pop("evaluacion")
r_e = m.servir(copy.deepcopy(p), "AG-18")
d = copy.deepcopy(ORIG)
d["evaluacion"]["nivel_ic"] = 0.6
configuracion._CONFIG_POR_DEFECTO = d
try:
    r_f = m.servir(copy.deepcopy(p), "AG-18")
finally:
    configuracion._CONFIG_POR_DEFECTO = ORIG
casos.append(("por_defecto.yaml cambiado (sección ausente del Motor)", r_f, nuevo_igual(None, d)))
for nombre, r, ref in casos:
    print(f"    {nombre:52s} hit={r.get('cache_hit')} · igual que un Motor nuevo: {ic(r) == ref}")
    K.comprobar(f"config en caliente, {nombre}: mismas cifras que un Motor nuevo con esa configuración", ic(r) == ref)
print(f"    (control) las cifras cambian con nivel_ic: {ic(r_a) != ic(r_b)}")
sys.exit(K.fin())
