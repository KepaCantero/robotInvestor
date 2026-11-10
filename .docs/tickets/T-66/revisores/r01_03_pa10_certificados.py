"""T-66 · QA r01 · PA-10: aprobar un certificado dos veces, uno retirado, uno de una celda ya vigente, antes de su emisión,
con el tipo equivocado en CT-04; cambiar solo_endurecer después; F6 manipulado a mano."""
import json
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from r01_comun import bloque, cfg, comprobar, fin

from bloque_a.almacen import Almacen
from bloque_a.evaluador import Evaluador

AS_OF = "2026-01-02"


def alta(a, pid, **campos):
    base = {"tipo_entrada": "ALTA", "prg_id": pid, "opp_id": "OPP-1", "clase": "RF", "horizonte": "H3", "prob_interna": 0.65,
            "sentido": "POSITIVO", "en_informe": True, "fecha_emision": "2025-01-02", "referencia_ingenua": {"valor_o_prob": 0.5},
            "estado": "ABIERTO"}
    a.escribir("F4", "AG-10", {**base, **campos})


def resolver(a, pid, o, fecha="2025-12-31"):
    a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                               "resolucion": {"resultado_binario": o, "comprobacion_fuga": "SUPERADA",
                                              "valor_observado": 0.01 if o else -0.01, "fecha_resuelto": fecha}})


def celda_habil(a, n=150, clase="RF", prefijo="PRG-2025"):
    rng = np.random.default_rng(1)
    for i in range(n):
        p = float(rng.choice([0.3, 0.7]))
        o = int(rng.random() < p)
        pid = f"{prefijo}-{i + 1:04d}"
        alta(a, pid, prob_interna=p, clase=clase, fecha_resolucion=str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i)).date()))
        resolver(a, pid, o)


def nuevo(tmp=None, **extra):
    b = bloque(cfg(**extra), tmp=tmp)
    b.fijar_fecha(AS_OF)
    celda_habil(b.almacen)
    return b


# 1 · Aprobar dos veces por CT-04
b = nuevo()
cid = b.evaluador.revisar_certificados(AS_OF)["emitidos"][0]["id"]
d1 = b.decision({"aprobar_certificados": [cid]}, AS_OF)
n_f6 = len(b.almacen.leer("F6"))
d2 = b.decision({"aprobar_certificados": [cid]}, AS_OF)
comprobar("aprobar dos veces: la segunda se rechaza y F6 no cambia",
          d1["certificados_aprobados"] == [cid] and d2["certificados_aprobados"] == [] and d2["rechazos"] and len(b.almacen.leer("F6")) == n_f6,
          f"{d1['estado']} / {d2['estado']} {d2['rechazos']}")

# 2 · Aprobar uno retirado (PROPUESTO que dejó de cumplir y pasó a REVOCADO)
b = nuevo()
cid = b.evaluador.revisar_certificados(AS_OF)["emitidos"][0]["id"]
b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT_REVOCACION", "id": cid, "estado": "REVOCADO", "motivo_cambio": "QA"})
d = b.decision({"aprobar_certificados": [cid]}, AS_OF)
comprobar("aprobar uno retirado: rechazado", d["certificados_aprobados"] == [] and d["rechazos"] and
          not b.evaluador.certificados_vigentes(AS_OF), f"{d['rechazos']}")

# 3 · Aprobar antes de que exista (fecha anterior a la emisión)
b = nuevo()
b.fijar_fecha(AS_OF)
cid = b.evaluador.revisar_certificados(AS_OF)["emitidos"][0]["id"]
try:
    b.evaluador.aprobar_certificados([cid], "2025-06-01")
    comprobar("aprobar con fecha anterior a la emisión: rechazado", False)
except ValueError as e:
    comprobar("aprobar con fecha anterior a la emisión: rechazado", True, str(e)[:80])

# 4 · Celda que ya tiene un VIGENTE: un segundo PROPUESTO de la misma celda no se aprueba
b = nuevo()
cid = b.evaluador.revisar_certificados(AS_OF)["emitidos"][0]["id"]
b.decision({"aprobar_certificados": [cid]}, AS_OF)
b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": "CERT-2026-9001", "estado": "PROPUESTO",
                                   "celda": {"clase": "RF", "horizonte": "H3", "metodo": None}})
d = b.decision({"aprobar_certificados": ["CERT-2026-9001"]}, AS_OF)
comprobar("segundo certificado de una celda vigente: rechazado", d["certificados_aprobados"] == [] and len(b.evaluador.certificados_vigentes(AS_OF)) == 1)

# 5 · CT-04 con un id suelto (cadena) en lugar de lista
b = nuevo()
cid = b.evaluador.revisar_certificados(AS_OF)["emitidos"][0]["id"]
d = b.decision({"aprobar_certificados": cid}, AS_OF)
comprobar("CT-04 con una cadena en lugar de lista: se rechaza con un solo motivo claro", len(d["rechazos"]) == 1,
          f"{len(d['rechazos'])} rechazos, el primero {d['rechazos'][:1]}; vigentes {len(b.evaluador.certificados_vigentes(AS_OF))}")

# 6 · Lista mixta (uno válido y uno desconocido): ¿todo o nada?
b = nuevo()
cid = b.evaluador.revisar_certificados(AS_OF)["emitidos"][0]["id"]
d = b.decision({"aprobar_certificados": [cid, "CERT-2099-0000"]}, AS_OF)
comprobar("lista mixta por CT-04: el válido se aprueba, el desconocido se rechaza y se declara APLICADA_PARCIALMENTE",
          d["certificados_aprobados"] == [cid] and d["estado"] == "APLICADA_PARCIALMENTE", f"{d['estado']}", hallazgo=False)

# 7 · Un PROPUESTO no pasa solo a VIGENTE si después se pone solo_endurecer: false
tmp = tempfile.mkdtemp(prefix="r01_cert_")
b = nuevo(tmp=tmp)
cid = b.evaluador.revisar_certificados(AS_OF)["emitidos"][0]["id"]
b2 = bloque(cfg(aprendizaje={"solo_endurecer": False}), tmp=tmp)
b2.fijar_fecha(AS_OF)
res = b2.evaluador.revisar_certificados(AS_OF)
comprobar("PROPUESTO + solo_endurecer false después: no se vuelve VIGENTE solo", not b2.evaluador.certificados_vigentes(AS_OF)
          and not res["emitidos"], f"propuestos {[c['id'] for c in b2.evaluador.certificados_propuestos(AS_OF)]}")

# 8 · Configuración no válida de solo_endurecer: el Bloque no arranca (falla cerrado)
for malo in ("true", 1, None):
    try:
        bloque(cfg(aprendizaje={"solo_endurecer": malo}))
        comprobar(f"solo_endurecer={malo!r}: el Bloque no arranca", False)
    except (ValueError, KeyError) as e:
        comprobar(f"solo_endurecer={malo!r}: el Bloque no arranca", True, str(e)[:60])

# 9 · F6 manipulado a mano (PROPUESTO → VIGENTE en el archivo): ¿lo detecta la integridad y se deja de usar?
tmp = Path(tempfile.mkdtemp(prefix="r01_f6_"))
a = Almacen(tmp)
a.reloj.fijar(AS_OF)
celda_habil(a)
e = Evaluador(a, None, None, cfg(), None)
cid = e.revisar_certificados(AS_OF)["emitidos"][0]["id"]
f6 = next(p for p in tmp.iterdir() if p.name.startswith("F6") or "F6" in p.name)
txt = f6.read_text(encoding="utf-8").replace('"estado": "PROPUESTO"', '"estado": "VIGENTE"')
f6.write_text(txt, encoding="utf-8")
a2 = Almacen(tmp)
integ = a2.verificar_integridad("F6")
e2 = Evaluador(a2, None, None, cfg(), None)
vig = [c["id"] for c in e2.certificados_vigentes(AS_OF)]
comprobar("F6 manipulado: verificar_integridad lo detecta", integ == {"F6": False}, f"{integ}")
comprobar("F6 manipulado: el certificado manipulado habilita probabilidades sin aprobación", not vig,
          f"vigentes tras manipular {vig} (la integridad se comprueba aparte; anterior a T-66)", hallazgo=False)
fin()
