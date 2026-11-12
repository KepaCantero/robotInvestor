"""QA r01 de T-101 · Mutantes contra la batería `tests/test_t101_v6.py`.

Copia `bloque_a/` de la raíz indicada a una carpeta temporal por mutante, aplica UNA mutación textual al código de la V6 y
ejecuta la batería de T-101. Un mutante «sobrevive» si la batería sigue en verde: hay un comportamiento del ticket que
ninguna prueba vigila.

Uso: .venv/bin/python -I .docs/tickets/T-101/revisores/r01_mutantes.py <raiz_repo> [n_paralelo] [ids separados por comas]
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
PAR = int(sys.argv[2]) if len(sys.argv) > 2 else 3
SOLO = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
PY = str(Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python")
D6, ORQ, PR, CT, LLM, AG = ("bloque_a/diseno_v6.py", "bloque_a/orquestacion.py", "bloque_a/prompts.py", "bloque_a/contratos.py",
                            "bloque_a/llm.py", "bloque_a/agentes.py")

# (id, archivo, texto original, texto mutado, qué rompe)
MUTANTES = [
    ("M01", D6, 'if float(u["senales"][clave]) >= umbral][:maxc]', 'if float(u["senales"][clave]) >= umbral]', "GC1 sin tope max_candidatas"),
    ("M02", D6, '    for u in sin:\n        marca[u["simbolo"]] = "SIN_SENAL_MEDIBLE"\n', "", "GC1 descarta lo que no tiene señal"),
    ("M03", D6, "u[\"simbolo\"]))[:n_expl]", "u[\"simbolo\"]))[:0]", "GC1 sin exploración"),
    ("M04", D6, "    if faltan:   # control de cobertura", "    if False:   # control de cobertura", "Prospectiva sin reintento"),
    ("M05", D6, "            omitidos.append(r)\n", "            pass\n", "omisión de Prospectiva no declarada"),
    ("M06", D6, "    if faltan:\n        for lote in _lotes(faltan, por_lote):", "    if False:\n        for lote in _lotes(faltan, por_lote):",
     "Contradictor sin reintento"),
    ("M07", D6, "for ronda in range(max_rondas + 1):", "for ronda in range(1):", "sin rondas de sustitución"),
    ("M08", D6, 'f["_critica_pendiente"], f["_sin_critica"] = False, True', 'f["_critica_pendiente"], f["_sin_critica"] = True, True',
     "lo que queda con la crítica pendiente sigue siendo elegible (sale sin crítica)"),
    ("M09", ORQ, 'ps5 = (refut is not None or bool(f.get("_critica_pendiente")))', "ps5 = True", "PS5 siempre superada"),
    ("M10", D6, '    """Solo se toman textos: el Sintetizador no puede cambiar la selección, las puntuaciones, las fechas ni las cifras."""\n',
     '    """Mutante."""\n    paquete.update({k: v for k, v in d.items() if k not in ("tarjetas",)})\n', "el Sintetizador escribe en el paquete"),
    ("M11", D6, 'if e.get("tipo_entrada") != "COBERTURA" or e["id"] in hechas:', 'if e.get("tipo_entrada") != "COBERTURA":',
     "contrafactual resuelto más de una vez"),
    ("M12", D6, "        if vence > hoy:\n            continue\n", "", "contrafactual antes de vencer"),
    ("M13", CT, "+ (CANALES_V6.get(contrato, []) if v6 else [])", "+ (CANALES_V6.get(contrato, []) if True else [])", "canales V6 abiertos en la V5"),
    ("M14", ORQ, 'if f.get("_opp_fijado"):', "if False:", "el OPP- cambia entre rondas"),
    ("M15", D6, "out[c] = round(out[c] - parte, 6)", "out[c] = round(out[c], 6)", "la bolsa del ciclo suma presupuesto"),
    ("M16", D6, "    h = int(hashlib.sha256(run_id.encode()).hexdigest(), 16) % 10000\n", "    return True\n", "Auditor en todos los runs"),
    ("M17", D6, "x[\"simbolo\"]))[:n_muestra]", "x[\"simbolo\"]))", "muestra de descartes sin tope"),
    ("M18", ORQ, 'if info_critica and info_critica["sin_critica"]:', "if False:", "lo no criticado no se declara"),
    ("M19", PR, 'if n in ("6", "10") or mar.get(n, "").strip() != txt.strip():', 'if n in ("6", "10"):', "el kit pierde §11/§12"),
    ("M20", LLM, "leido = max((t for k, t in puntos if k in self._vistos), default=0)", "leido = 0", "simulador sin caché por prefijo"),
    ("M21", AG, "cliente = self.clientes.get(agente, self.cliente)", "cliente = self.cliente", "se ignora el cliente del Contradictor"),
    ("M22", D6, '        if u["simbolo"] in simb_vig and u["simbolo"] not in marca:\n            marca[u["simbolo"]] = "VIGENTE"\n', "",
     "GC1 deja fuera las vigentes"),
    ("M23", D6, '    reg["falsos_negativos"] = sorted(', '    return\n    reg["falsos_negativos"] = sorted(', "no se cuentan los falsos negativos"),
    ("M24", ORQ, "        if self.v6 and not v6.op(self, \"informe_aprendizaje_llm\"):", "        if False:", "la V6 llama a AG-20"),
    ("M25", D6, '            if isinstance(x, dict) and x.get("ref") in pedidos and x["ref"] not in res:\n                res[x["ref"]] = x\n\n    for lote in lotes:',
     '            if isinstance(x, dict) and x.get("ref") and x["ref"] not in res:\n                res[x["ref"]] = x\n\n    for lote in lotes:',
     "Prospectiva acepta refs no pedidas"),
    ("M26", ORQ, "if self.v6 and not v6.auditar_este_run(self, run_id):", "if False:", "Auditor sin muestreo en la V6"),
    ("M27", D6, '            elif (c, f["proxy"]) in sin_critica:\n                fase, motivo = "CRITICA"',
     '            elif False:\n                fase, motivo = "CRITICA"', "la cobertura no marca la fase CRITICA"),
]


def correr(m):
    mid, arch, viejo, nuevo, desc = m
    tmp = Path(tempfile.mkdtemp(prefix=f"r01_{mid}_"))
    try:
        shutil.copytree(RAIZ / "bloque_a", tmp / "bloque_a", ignore=shutil.ignore_patterns("*.docx", "__pycache__", "estado_bloque_a"))
        p = tmp / "bloque_a" / "11_Ejecutor" / arch
        s = p.read_text(encoding="utf-8")
        if s.count(viejo) != 1:
            return mid, desc, f"NO APLICA ({s.count(viejo)} apariciones)", ""
        p.write_text(s.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t101_v6.py"],
                           cwd=tmp / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, timeout=900)
        ult = (r.stdout.strip().splitlines() or [""])[-1]
        fallida = next((ln for ln in r.stdout.splitlines() if ln.startswith("FAILED") or ln.startswith("ERROR")), "")
        return mid, desc, "MATADO" if r.returncode else "SOBREVIVE", (fallida or ult)[:160]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    lista = [m for m in MUTANTES if not SOLO or m[0] in SOLO]
    with ThreadPoolExecutor(PAR) as ex:
        res = list(ex.map(correr, lista))
    for mid, desc, est, det in res:
        print(f"{mid} {est:10} {desc} · {det}")
    vivos = [r for r in res if r[2] == "SOBREVIVE"]
    print(f"\n{len(res) - len(vivos)}/{len(res)} matados; sobreviven: {[r[0] for r in vivos]}")
