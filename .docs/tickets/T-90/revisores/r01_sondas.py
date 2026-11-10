"""QA r01 de T-90 · sondas de ataque sobre la exclusión declarada de notas con fechas fuera de corte.

Ejecución: .venv/bin/python .docs/tickets/T-90/revisores/r01_sondas.py [S1 S2 ...]
Cada sonda imprime OK / FALLA con el detalle. Código de salida 1 si alguna falla.
"""
import re
import sys

sys.path.insert(0, __import__("os").path.dirname(__file__))
from r01_comun import AS_OF, MARCA, ejecutar, f3, marcas_en_f2, marcas_en_paquete, nota  # noqa: E402

FRASE = "excluida por fechas de fuente posteriores al corte"
RES = []


def comprobar(sonda, cond, detalle=""):
    RES.append((sonda, bool(cond)))
    print(f"[{'OK' if cond else 'FALLA'}] {sonda}: {detalle}")


def degradados_t90(o):
    return [x for x in o["paquete"]["estados_degradados"] if FRASE in x]


def portada(tec):
    return tec[:4000]


def s1_varias_notas_varias_dimensiones():
    """Varias notas excluidas (futuras, incoherentes, ilegibles) en varias dimensiones + notas válidas intactas."""
    extra = {
        "D2": [nota("D2 futura", f3("2099-01-01", "2099-01-02", "2099-01-02")),
               nota("D2 valida", f3("2026-10-01", "2026-10-02", "2026-10-03"))],
        "D4": [nota("D4 incoherente (publicación antes del hecho)", f3("2026-10-05", "2026-10-01", "2026-10-06"))],
        "D8": [nota("D8 ilegible", f3("ayer", "2026-10-01", "2026-10-02"))],
        "D9": [nota("D9 conocible un día después del corte", f3("2026-11-03", "2026-11-03", "2026-11-04")),
               nota("D9 en el borde (conocible el día del corte)", f3("2026-11-03", "2026-11-03", AS_OF))],
    }
    o = ejecutar(extra)
    comprobar("S1.estado", o["res"].get("estado_peticion") == "ENTREGADA", o["res"].get("estado_peticion"))
    if "paquete" not in o:
        return
    f2 = marcas_en_f2(o)
    pq = marcas_en_paquete(o)
    validas = [f"{MARCA} D2 valida", f"{MARCA} D9 en el borde (conocible el día del corte)"]
    comprobar("S1.f2_solo_validas", f2 == sorted(validas), f2)
    comprobar("S1.paquete_solo_validas", pq == sorted(validas), pq)
    deg = degradados_t90(o)
    dims = sorted(x.split(":")[0] for x in deg)
    comprobar("S1.declaradas_por_dim", dims == ["D2", "D4", "D8", "D9"], deg)
    comprobar("S1.especialista_nombrado", all(re.search(r"nota de (AG-B\d\d|DIR) ", x) for x in deg), deg)
    tec = o["tecnico"]
    comprobar("S1.en_informe_tecnico", all(x in tec for x in deg), "")
    comprobar("S1.en_portada_40c", all(x[:40] in portada(tec) for x in deg), "")
    g3 = {x["pasada"]: x["dictamen"] for x in o["g3"]}
    comprobar("S1.g3", all(v in ("APTO", "APTO_CON_ADVERTENCIAS") for v in g3.values()), g3)
    comprobar("S1.dedup_paquete", len(o["paquete"]["estados_degradados"]) == len(set(o["paquete"]["estados_degradados"])), "")
    # la nota válida conserva sus fechas en la EVD
    evd = [e for e in o["ent"].alm.leer("F2") if e.get("tipo_entrada") == "EVD"
           and (e.get("fechas") or {}).get("conocible_desde") == "2026-10-03"]
    comprobar("S1.valida_con_fechas_en_evd", len(evd) == 1, len(evd))
    return o


def s2_formas_raras():
    """fechas None / texto / lista / parcial / hora sin zona / campos en la raíz: todas se excluyen y se declaran."""
    extra = {
        "D1": [{**nota("D1 fechas None"), "fechas": None}],
        "D3": [nota("D3 fechas texto", "2026-10-01")],
        "D5": [nota("D5 fechas lista", ["2026-10-01"])],
        "D6": [nota("D6 parcial (solo publicación)", {"fecha_publicacion": "2026-10-01"})],
        "D7": [nota("D7 hora sin zona", f3("2026-10-01T10:00:00", "2026-10-01T10:00:00", "2026-10-01T10:00:00"))],
        "D10": [nota("D10 fechas en la raíz y futuras", None, fecha_fenomeno="2099-01-01", fecha_publicacion="2099-01-01",
                     conocible_desde="2099-01-01")],
        "D11": [nota("D11 tipo número", f3(20261001, 20261001, 20261001))],
    }
    o = ejecutar(extra)
    comprobar("S2.estado", o["res"].get("estado_peticion") == "ENTREGADA", o["res"].get("estado_peticion"))
    if "paquete" not in o:
        return
    comprobar("S2.nada_en_f2", marcas_en_f2(o) == [], marcas_en_f2(o))
    comprobar("S2.nada_en_paquete", marcas_en_paquete(o) == [], marcas_en_paquete(o))
    dims = sorted(x.split(":")[0] for x in degradados_t90(o))
    esperadas = sorted(d for d in extra if any(dd["dim"] == d for dd in o["paquete"]["dimensiones"]))
    comprobar("S2.declaradas", dims == esperadas, f"declaradas {dims} · esperadas {esperadas}")
    print("    texto:", degradados_t90(o)[:2])


def s3_dos_notas_misma_dimension():
    """Dos notas excluidas del mismo especialista en la misma dimensión: ¿se cuenta cuántas?"""
    extra = {"D2": [nota("D2 futura A", f3("2099-01-01", "2099-01-01", "2099-01-01")),
                    nota("D2 futura B", f3("2098-01-01", "2098-01-01", "2098-01-01"))]}
    o = ejecutar(extra)
    if "paquete" not in o:
        comprobar("S3.estado", False, o["res"].get("estado_peticion"))
        return
    deg = degradados_t90(o)
    comprobar("S3.nada_en_paquete", marcas_en_paquete(o) == [], "")
    print(f"    entradas en el paquete para 2 notas excluidas: {len(deg)} -> {deg}")
    comprobar("S3.informa_del_numero", len(deg) == 2 or any("2 notas" in x for x in deg),
              "(observación: el paquete deduplica y no dice cuántas notas se excluyeron)")


def s4_todas_las_notas_de_una_dimension():
    """Una sola nota excluida en D2 (las simuladas siguen): se declara D2."""
    extra = {"D2": [nota("D2 futura", f3("2099-01-01", "2099-01-01", "2099-01-01"))]}
    o = ejecutar(extra)
    if "paquete" not in o:
        comprobar("S4.estado", False, o["res"].get("estado_peticion"))
        return
    comprobar("S4.declarada", any(x.startswith("D2:") for x in degradados_t90(o)), degradados_t90(o))


def s5_determinismo():
    """Dos ejecuciones idénticas dan los mismos estados degradados, en el mismo orden."""
    extra = {"D2": [nota("D2 futura", f3("2099-01-01", "2099-01-01", "2099-01-01"))],
             "D9": [nota("D9 futura", f3("2099-01-01", "2099-01-01", "2099-01-01"))],
             "D4": [nota("D4 futura", f3("2099-01-01", "2099-01-01", "2099-01-01"))]}
    a = ejecutar(extra)
    b = ejecutar(extra)
    if "paquete" not in a or "paquete" not in b:
        comprobar("S5.estado", False, "")
        return
    comprobar("S5.mismos_estados_mismo_orden", a["paquete"]["estados_degradados"] == b["paquete"]["estados_degradados"],
              a["paquete"]["estados_degradados"])
    fila = lambda t: next(l for l in t.splitlines() if l.startswith("| Estados degradados"))  # noqa: E731
    comprobar("S5.misma_fila_tecnico", fila(a["tecnico"]) == fila(b["tecnico"]), fila(a["tecnico"])[:200])


def s6_muchas_dimensiones_portada():
    """Una nota futura en cada una de las 12 dimensiones: ¿cabe la declaración en la portada (G3B-ENT-09, 4000 car.)?"""
    extra = {f"D{i}": [nota(f"D{i} futura", f3("2099-01-01", "2099-01-01", "2099-01-01"))] for i in range(1, 13)}
    o = ejecutar(extra)
    est = o["res"].get("estado_peticion")
    fid = [x for x in o["g3"] if x["pasada"] == "FIDELIDAD_ENTREGABLES"]
    fallos = [f for x in fid for f in x.get("fallos") or []]
    comprobar("S6.estado", est == "ENTREGADA", f"{est} · fallos G3 fidelidad: {fallos[:3]}")
    if "paquete" in o:
        deg = degradados_t90(o)
        tec = o["tecnico"]
        pos = tec.find("| Estados degradados")
        print(f"    {len(deg)} declaraciones; la fila empieza en el carácter {pos} y mide "
              f"{len(next(l for l in tec.splitlines() if l.startswith('| Estados degradados')))}")


def s7_posicion_de_la_fila():
    """Margen de la portada: posición de la fila «Estados degradados» en una entrega sin exclusiones."""
    o = ejecutar({})
    tec = o["tecnico"]
    pos = tec.find("| Estados degradados")
    print(f"    sin exclusiones: fila en el carácter {pos}; cada declaración T-90 mide ~105 car.; "
          f"caben ~{(4000 - pos) // 107} antes de salirse de la portada")
    comprobar("S7.sin_declaraciones_t90", degradados_t90(o) == [], degradados_t90(o))


SONDAS = {"S1": s1_varias_notas_varias_dimensiones, "S2": s2_formas_raras, "S3": s3_dos_notas_misma_dimension,
          "S4": s4_todas_las_notas_de_una_dimension, "S5": s5_determinismo, "S6": s6_muchas_dimensiones_portada,
          "S7": s7_posicion_de_la_fila}

if __name__ == "__main__":
    for k in (sys.argv[1:] or SONDAS):
        print(f"== {k}: {SONDAS[k].__doc__.strip()}")
        SONDAS[k]()
    malas = [s for s, ok in RES if not ok]
    print(f"\nResumen: {len(RES) - len(malas)} OK · {len(malas)} FALLA {malas}")
    sys.exit(1 if malas else 0)
