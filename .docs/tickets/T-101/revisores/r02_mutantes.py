"""QA r02 de T-101 · Mutantes de las correcciones de la ronda r02 contra la batería `tests/test_t101_v6.py`.

Mismo método que `r01_mutantes.py` (que se reutiliza): copia `bloque_a/` de la raíz indicada a una carpeta temporal por
mutante, aplica UNA mutación textual y ejecuta la batería de T-101. Un mutante «sobrevive» si la batería sigue en verde.
N10 es el M10 de la r01 adaptado al texto nuevo de `_aplicar_integracion`.

Uso: .venv/bin/python -I .docs/tickets/T-101/revisores/r02_mutantes.py <raiz_repo> [n_paralelo] [ids separados por comas]
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_mutantes as base  # noqa: E402  (lee RAIZ, PAR y SOLO de sys.argv igual que aquí)

D6, ORQ = "bloque_a/diseno_v6.py", "bloque_a/orquestacion.py"

MUTANTES = [
    ("N01", D6, "    if _R13.search(t):\n        return \"R13\"\n", "", "el filtro deja de mirar R13"),
    ("N02", D6, "    if _R21.search(t) or sint._UNITARIA.search(t):", "    if sint._UNITARIA.search(t):", "el filtro R21 solo con _UNITARIA"),
    ("N03", D6, "    if malas:\n        paquete[\"limitaciones\"]", "    if False:\n        paquete[\"limitaciones\"]",
     "los textos llanos no se filtran"),
    ("N04", ORQ, "incompleto_v6 = bool((info_prosp or {}).get(\"omitidos\")", "incompleto_v6 = False and bool((info_prosp or {}).get(\"omitidos\")",
     "lo que la V6 no entrega no deja el run PARCIAL"),
    ("N05", D6, "        if reintento:   # QA r01 de T-101, H-04: otro encargo", "        if False:   # QA r01 de T-101, H-04: otro encargo",
     "el reintento de Prospectiva sale de la caché"),
    ("N06", D6, "        if reintento:   # H-04\n", "        if False:   # H-04\n", "el reintento del Contradictor sale de la caché"),
    ("N07", ORQ, "            instr += v6.NOTA_GC1\n", "            pass\n", "sin nota de GC1 para el Analista"),
    ("N08", D6, " and math.isfinite(float(v))", "", "NaN e infinito vuelven a contar como señal"),
    ("N09", D6, "    if d != \"v6\":\n        return False\n", "    if d != \"v6\":\n        return False\n    return True\n",
     "la sección v6 no se valida"),
    ("N10", D6, "    descartados = []\n\n    def _ok(campo, t):",
     "    descartados = []\n    paquete.update({k: v for k, v in d.items() if k not in (\"tarjetas\",)})\n\n    def _ok(campo, t):",
     "el Sintetizador escribe en el paquete (M10 de la r01, adaptado)"),
    ("N11", D6, "            if sim not in finalistas:\n                filas.append", "            if False:\n                filas.append",
     "sin filas ANALISTA (H-01)"),
    ("N12", D6, "            if x.get(\"opp_id\") in top and x.get(\"opp_id\") not in por_opp:", "            if False:",
     "sin fila para la vigente mantenida (H-01)"),
    ("N13", D6, "        for x in s.get(\"cerradas\", []):\n            filas.append", "        for x in []:\n            filas.append",
     "sin fila para la vigente cerrada (H-01)"),
    ("N14", ORQ, "            if info_critica and info_critica[\"sin_respuesta\"]:", "            if False:",
     "lo que el Contradictor no devuelve no se declara (H-03)"),
    ("N15", D6, "            elif _ref(c, f) in sin_respuesta:   # QA r01 de T-101, H-03", "            elif False:",
     "la cobertura no marca «no la devolvió» (H-03)"),
    ("N16", D6, "        if any(v[\"sin_precio\"] for v in clases.values()) and not any(", "        if False and any(",
     "el contrafactual no espera sin precios (H-10)"),
    ("N17", ORQ, "        if presupuesto_override:\n            asign.update(presupuesto_override)\n        if self.v6:",
     "        if self.v6:", "se pierde el override con la V6 (H-07)"),
    ("N18", D6, "[:lim[\"preguntas\"]]", "", "sin tope de preguntas del Sintetizador (H-08)"),
    ("N19", D6, "    if descartados:\n        nuevas.append", "    if False:\n        nuevas.append",
     "los textos descartados por R13/R21 no se declaran (H-09)"),
    ("N20", D6, "    sin_respuesta = sorted({r for ronda in rondas for r in ronda.get(\"sin_respuesta\", [])})",
     "    sin_respuesta = []", "sin_respuesta vacío (H-03)"),
    ("N22", D6, "presupuesto={\"uc\": presupuesto.asignado.get(\"COMUN\")})", "presupuesto={\"uc\": 2})",
     "CT-15 vuelve al presupuesto escrito a mano (H-08)"),
]

if __name__ == "__main__":
    lista = [m for m in MUTANTES if not base.SOLO or m[0] in base.SOLO]
    with ThreadPoolExecutor(base.PAR) as ex:
        res = list(ex.map(base.correr, lista))
    for mid, desc, est, det in res:
        print(f"{mid} {est:10} {desc} · {det}")
    vivos = [r for r in res if r[2] == "SOBREVIVE"]
    print(f"\n{len(res) - len(vivos)}/{len(res)} matados; sobreviven: {[r[0] for r in vivos]}")
