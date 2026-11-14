"""QA r01 de T-117 · Huella de un ciclo semanal simulado, para comparar árboles de código (antes y después) y ejecuciones.

Uso:  cd <árbol>/bloque_a/11_Ejecutor && python <este fichero> v5|v6 <carpeta de trabajo> [clases separadas por comas]
Ejecuta un ciclo con MockClient y los datos de ejemplo en <carpeta de trabajo> (se borra antes; úsese SIEMPRE la misma ruta,
porque F5 guarda la ruta de los entregables y entra en la cadena de huellas) e imprime un JSON con el SHA-256 de cada
fichero del estado y de los entregables, del resultado devuelto y del registro COBERTURA. `cache_resultados.jsonl` se
compara con sus líneas ordenadas: los tipos de activo se analizan en hilos y el orden de escritura de la caché varía entre
ejecuciones (ya era así antes de T-117). Dos salidas iguales = mismo registro y mismos entregables, byte a byte.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "tests")]
from conftest import AS_OF, config_pruebas
from test_t101_v6 import _bloque

import bloque_a

diseno = sys.argv[1]
import shutil

tmp = Path(sys.argv[2]).resolve()
assert "scratchpad" in str(tmp)
shutil.rmtree(tmp, ignore_errors=True)
clases = sys.argv[3].split(",") if len(sys.argv) > 3 else None
b = _bloque(tmp, config_pruebas(diseno=diseno))
r = b.ciclo(AS_OF, alcance={"clases": clases} if clases else None)


def sha(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def contenido(p: Path) -> bytes:
    return b"".join(sorted(p.read_bytes().splitlines(keepends=True))) if p.name == "cache_resultados.jsonl" else p.read_bytes()


def sin_reloj(o):
    """`consumo.latencia_s` es tiempo real de la máquina: lo único del resultado que cambia entre dos ejecuciones iguales."""
    if isinstance(o, dict):
        return {k: sin_reloj(v) for k, v in o.items() if k != "latencia_s"}
    return [sin_reloj(x) for x in o] if isinstance(o, list) else o


def plano(o):
    """Los conjuntos, como listas ordenadas (su orden al imprimirse depende de PYTHONHASHSEED); lo demás no serializable, a texto."""
    return sorted(str(x) for x in o) if isinstance(o, (set, frozenset)) else str(o)


NORM = sin_reloj(json.loads(json.dumps(r, default=plano)))
ficheros = {str(p.relative_to(tmp)): sha(contenido(p)) for p in sorted(tmp.rglob("*")) if p.is_file()}
cob = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "COBERTURA"]
salida = {"codigo": str(Path(bloque_a.__file__).resolve().parents[3].name), "diseno": diseno, "estado": r["estado"], "n_ficheros": len(ficheros),
          "resultado": sha(json.dumps(NORM, sort_keys=True, ensure_ascii=False).encode()), "resultado_norm": NORM,
          "cobertura": sha(json.dumps(cob, sort_keys=True, default=str, ensure_ascii=False).encode()) if cob else None,
          "gc1": {c: {k: v["gc1"][k] for k in ("umbral", "pasan") if k in v.get("gc1", {})} for c, v in (cob[-1]["clases"].items() if cob else [])
                  if v.get("gc1")},
          "top": {c: [o["nombre"] for o in d["opciones"]] for c, d in r["paquete"]["clases"].items()},
          "ficheros": ficheros}
print(json.dumps(salida, ensure_ascii=False, sort_keys=True))
