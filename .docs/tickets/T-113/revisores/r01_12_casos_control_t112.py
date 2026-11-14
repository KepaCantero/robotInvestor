"""QA r01 de T-113 · T-113 no estropea T-112 (Motor Fase 2) ni T-106: todos los casos de control siguen superados, las fichas
citables son las mismas y los resultados de los casos de control de MON e IDX no cambian frente a 3a5fbfe^ salvo lo declarado
(las incertidumbres de MON-EXP).
Uso: cd <árbol>/bloque_a/11_Ejecutor && python <este script> [salida.json]"""
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402


class _P:
    as_of = None
    nombre = "pruebas"


m = servicio.Motor(Almacen(Path(tempfile.mkdtemp(prefix="qa_t113_cc_", dir=os.environ.get("QA_TMP")))), _P(), cargar_config())
res = m.verificar_casos_control()
mal = {f: [c for c in r.get("casos", r.get("resultados", [])) if not c.get("superado")] for f, r in res.items()
       if not (r.get("superados") if "superados" in r else r.get("estado") == "SERVED")}
print("claves de un resultado:", sorted(next(iter(res.values()))))
print(f"fichas con casos de control: {len(res)}; no superadas: {len(mal)} {dict(list(mal.items())[:5])}")
print("fase 1:", len(servicio.FASE1), "· fase 2:", len(servicio.FASE2), "· manejadores:", len(servicio.IMPLEMENTADAS),
      "· servibles:", sum(1 for f in servicio.IMPLEMENTADAS if servicio.servible(f, m.raiz)))
if len(sys.argv) > 1:
    out = {}
    for ficha in sorted(servicio.CASOS_CONTROL):
        if not ficha.startswith(("MON-", "IDX-")):
            continue
        for i, caso in enumerate(servicio.CASOS_CONTROL[ficha]):
            ent, _ = m._resolver_datos(caso.get("datos") or [], None)
            m._contexto(ent, caso.get("fecha_corte"))
            try:
                r, lim = servicio.IMPLEMENTADAS[ficha]["fn"](ent, dict(caso.get("parametros") or {}))
                out[f"{ficha}#{i}"] = {"r": servicio._limpio(r) if hasattr(servicio, "_limpio") else r, "lim": lim}
            except Exception as e:  # noqa: BLE001
                out[f"{ficha}#{i}"] = {"exc": f"{type(e).__name__}: {e}"}
    Path(sys.argv[1]).write_text(json.dumps(out, sort_keys=True, default=str, ensure_ascii=False), encoding="utf-8")
    print("escrito", sys.argv[1], len(out), "casos")
