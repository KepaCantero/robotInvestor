"""QA r01 de T-113 · CA-2: la V5 no cambia salvo lo declarado. Vuelca, normalizado, el resultado de dos ciclos V5 seguidos de
doce perfiles (paquete, RUN de F5 sin tiempos, entregables) para compararlo entre 3a5fbfe^ y el árbol actual:
  cd <árbol>/bloque_a/11_Ejecutor && python <este script> salida.json [v5|v6]
y después `python <este script> --comparar a.json b.json`."""
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

if sys.argv[1] == "--comparar":
    a, b = (json.loads(Path(p).read_text(encoding="utf-8")) for p in sys.argv[2:4])

    def plano(x, pref=""):
        if isinstance(x, dict):
            for k, v in x.items():
                yield from plano(v, f"{pref}/{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                yield from plano(v, f"{pref}[{i}]")
        else:
            yield pref, x
    pa, pb = dict(plano(a)), dict(plano(b))
    difs = sorted(k for k in set(pa) | set(pb) if pa.get(k, "<falta>") != pb.get(k, "<falta>"))
    print(f"hojas: {len(pa)} y {len(pb)}; distintas: {len(difs)}")
    grupos: dict = {}
    for k in difs:
        g = re.sub(r"\[\d+\]", "[]", k)
        g = re.sub(r"/(RV|RF|DIV|MP|IDX|FON|DER|INM|CRI|ALT|MON|TCV|COMUN)(?=/|$)", "/<tipo>", g)
        grupos.setdefault(g, []).append(k)
    for g, ks in sorted(grupos.items()):
        k = ks[0]
        print(f"  {len(ks):4d} × {g}\n         p. ej. {k}: {str(pa.get(k, '<falta>'))[:110]!r} -> {str(pb.get(k, '<falta>'))[:110]!r}")
    sys.exit(0)

sys.path.insert(0, ".")
sys.path.insert(0, "tests")
import pandas as pd  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402
from conftest import AS_OF, DATOS, config_pruebas  # noqa: E402

diseno = sys.argv[2] if len(sys.argv) > 2 else "v5"
tmp = Path(tempfile.mkdtemp(prefix="qa_t113_v5_", dir=os.environ.get("QA_TMP")))
b = Bloque(config_pruebas(diseno=diseno, paralelismo={"hilos_analistas": 1}), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
           tmp / "estado", tmp / "ent")
out = {}
for n, fecha in enumerate((AS_OF, str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date()))):
    res = b.ciclo(fecha)
    run = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"][-1]

    def limpio(x):
        if isinstance(x, dict):
            return {k: limpio(v) for k, v in x.items() if k not in ("latencia_s", "hash", "hash_previo", "ts", "timestamp", "creado", "duracion_s")}
        if isinstance(x, list):
            return [limpio(v) for v in x]
        if isinstance(x, str):
            return x.replace(str(tmp), "<tmp>")
        return x
    ent = {}
    for raiz in (tmp / "ent",):
        for p in sorted(raiz.rglob("*")):
            if p.is_file() and p.suffix in (".md", ".json", ".csv", ".html", ".txt"):
                texto = p.read_text(encoding="utf-8", errors="replace").replace(str(tmp), "<tmp>")
                ent[str(p.relative_to(raiz))] = hashlib.sha256(texto.encode()).hexdigest()[:16] if p.suffix != ".md" else texto.split("\n")
    out[f"ciclo{n}"] = {"paquete": limpio(res["paquete"]), "run": limpio(run), "g3": limpio(res.get("g3")), "entregables": ent}
Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, sort_keys=True, default=str), encoding="utf-8")
print("escrito", sys.argv[1])
