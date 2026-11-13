"""QA r01 de T-101 · CA-8: ¿la V6 «lee más caché» que la V5? Un ciclo C1 con los doce perfiles por diseño (simulador).

Imprime llamadas, tokens de entrada (sin caché, escritura, lectura), proporción leída de caché, UC y coste estimado.
Uso: .venv/bin/python -I .docs/tickets/T-101/revisores/r01_ca8_consumo.py <raiz_repo>
"""
import sys
import tempfile
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor" / "tests"))
sys.path.insert(0, str(RAIZ / "bloque_a" / "11_Ejecutor"))
from conftest import AS_OF, DATOS, config_pruebas  # noqa: E402

from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

out = {}
for d in ("v5", "v6"):
    t = Path(tempfile.mkdtemp(prefix=f"r01_ca8_{d}_"))
    b = Bloque(config_pruebas(diseno=d), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), t / "e", t / "n")
    c = b.ciclo(AS_OF)["consumo"]
    tot = c["entrada"] + c["cache_escritura"] + c["cache_lectura"]
    out[d] = c
    print(f"{d}: llamadas={c['llamadas']} entrada={c['entrada']} escritura={c['cache_escritura']} lectura={c['cache_lectura']} "
          f"total={tot} lectura/total={c['cache_lectura'] / tot:.3f} uc_llm={c['uc_llm']} coste_estimado={c.get('coste_estimado')}")
a, b_ = out["v5"], out["v6"]
print("V6 lee más caché que V5 (absoluto):", b_["cache_lectura"] > a["cache_lectura"])
print("V6 lee más caché que V5 (proporción):",
      b_["cache_lectura"] / (b_["entrada"] + b_["cache_escritura"] + b_["cache_lectura"])
      > a["cache_lectura"] / (a["entrada"] + a["cache_escritura"] + a["cache_lectura"]))
