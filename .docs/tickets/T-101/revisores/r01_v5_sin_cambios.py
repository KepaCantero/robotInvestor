"""QA r01 de T-101 · La V5 no cambia de comportamiento.

Ejecuta el mismo ciclo C1 (doce perfiles, cliente simulado, AS_OF fijo, dos semanas) con `diseno: v5` sobre el código de
una raíz dada y vuelca a JSON: las llamadas al modelo (agente, modelo, clase, fase y tokens), la selección por tipo, el
paquete JSON entregado y el contenido de la carpeta de estado (sin marcas de tiempo ni latencias).

Uso:
  python -I r01_v5_sin_cambios.py volcar <raiz_repo> <salida.json>
  python -I r01_v5_sin_cambios.py comparar <a.json> <b.json>
"""
import json
import re
import sys
from pathlib import Path

VOLATILES = re.compile(r"^(ts|timestamp|creado|creado_en|fecha_creacion|hora|latencia_s|intento|duracion_s|generado_en|.*_ts)$")


def _limpiar(x):
    if isinstance(x, dict):
        return {k: _limpiar(v) for k, v in sorted(x.items()) if not VOLATILES.match(str(k))}
    if isinstance(x, list):
        return [_limpiar(v) for v in x]
    return x


def volcar(raiz: str, salida: str) -> None:
    ejec = Path(raiz) / "bloque_a" / "11_Ejecutor"
    sys.path.insert(0, str(ejec))
    import tempfile

    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config, fusionar
    from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque
    assert Path(sys.modules["bloque_a"].__file__).resolve().is_relative_to(ejec.resolve()), sys.modules["bloque_a"].__file__
    tmp = Path(tempfile.mkdtemp(prefix="r01_v5_"))
    cfg = cargar_config(extra=fusionar({"modo": "backtest", "evaluacion": {"bootstrap_replicas": 300, "simulaciones_ece": 300},
                                        "perfiles": {"activos": ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]}},
                                       {}))
    if "diseno" in cfg:
        assert cfg["diseno"] == "v5"
    cli = MockClient()
    b = Bloque(cfg, ProveedorCSV(ejec / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cli, tmp / "estado", tmp / "ent")
    out = {"runs": []}
    for fecha in ("2026-06-05", "2026-06-12"):
        r = b.ciclo(fecha)
        out["runs"].append({"as_of": fecha, "estado": r["estado"], "g3": r["g3"]["dictamen"],
                            "g3_entregables": (r.get("g3_entregables") or {}).get("dictamen"),
                            "seleccion": {c: [(o["opp_id"], o["indicador_seguimiento"]["simbolo"]) for o in d["opciones"]]
                                          for c, d in r["paquete"]["clases"].items()},
                            "limitaciones": r["paquete"]["limitaciones"],
                            "consumo": {k: v for k, v in r["consumo"].items() if k not in ("latencia_s", "reintentos")}})
    out["llamadas"] = [{k: x.get(k) for k in ("run_id", "agente", "modelo", "clase", "fase", "cache_hit", "uc", "entrada", "salida",
                                               "cache_escritura", "cache_lectura", "busquedas_web")} for x in b.contabilidad.llamadas]
    estado = {}
    for p in sorted((tmp / "estado").rglob("*")):
        if p.is_file() and p.suffix in (".jsonl", ".json"):
            filas = []
            for ln in p.read_text(encoding="utf-8").splitlines():
                try:
                    filas.append(_limpiar(json.loads(ln)))
                except json.JSONDecodeError:
                    filas.append(ln)
            estado[str(p.relative_to(tmp))] = filas
    out["estado"] = estado
    ent = {}
    for p in sorted((tmp / "ent").rglob("*paquete-json*.json")):
        ent[p.name] = _limpiar(json.loads(p.read_text(encoding="utf-8")))
    out["paquetes_json"] = ent
    Path(salida).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str, sort_keys=True), encoding="utf-8")
    print("llamadas", len(out["llamadas"]), "archivos de estado", len(estado), "paquetes", len(ent))


def _dif(a, b, ruta="", out=None, maxn=40):
    out = [] if out is None else out
    if len(out) >= maxn:
        return out
    if type(a) is not type(b):
        out.append(f"{ruta}: tipo {type(a).__name__} != {type(b).__name__}")
    elif isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{ruta}/{k}: solo en {'b' if k not in a else 'a'}")
            else:
                _dif(a[k], b[k], f"{ruta}/{k}", out, maxn)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append(f"{ruta}: longitud {len(a)} != {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            _dif(x, y, f"{ruta}[{i}]", out, maxn)
    elif a != b:
        out.append(f"{ruta}: {str(a)[:80]!r} != {str(b)[:80]!r}")
    return out


RUTAS = re.compile(r"^/tmp/[^/]+/")


def _normalizar(d: dict) -> dict:
    """Los Analistas se llaman en hilos: el orden de las llamadas y quién escribe primero la caché (y por tanto el consumo
    por tipo) varían entre dos ejecuciones del MISMO código. Se compara sin orden: multiconjunto de llamadas con la entrada
    total (entrada + escritura + lectura de caché), filas de estado ordenadas, sin cadenas de hash, rutas temporales ni
    consumo por tipo."""
    def fila(x):
        if isinstance(x, dict):
            return {k: fila(v) for k, v in x.items() if k not in ("_hash", "_hash_prev", "consumido", "clave", "uc")}
        if isinstance(x, list):
            return [fila(v) for v in x]
        if isinstance(x, str):
            return RUTAS.sub("/tmp/X/", x)
        return x
    ll = sorted(json.dumps({"run_id": x["run_id"], "agente": x["agente"], "modelo": x["modelo"], "clase": x["clase"], "fase": x["fase"],
                            "entrada_total": x["entrada"] + x["cache_escritura"] + x["cache_lectura"], "salida": x["salida"],
                            "cache_hit": x["cache_hit"]}, sort_keys=True) for x in d["llamadas"])
    est = {k: sorted(json.dumps(fila(v), sort_keys=True, default=str) for v in filas) for k, filas in d["estado"].items()}
    runs = [{**r, "consumo": {k: v for k, v in r["consumo"].items() if k not in ("por_agente", "por_clase", "uc", "uc_llm", "coste_estimado",
                                                                                  "cache_escritura", "cache_lectura", "entrada")}} for r in d["runs"]]
    return {"runs": fila(runs), "llamadas": ll, "paquetes_json": fila(d["paquetes_json"]), "estado": est}


def comparar(fa: str, fb: str) -> int:
    a, b = json.loads(Path(fa).read_text()), json.loads(Path(fb).read_text())
    a, b = _normalizar(a), _normalizar(b)
    total = 0
    for k in ("runs", "llamadas", "paquetes_json", "estado"):
        d = _dif(a[k], b[k], k)
        total += len(d)
        print(f"== {k}: {'IGUAL' if not d else str(len(d)) + ' diferencias (primeras)'}")
        for x in d[:40]:
            print("  ", x)
    return 1 if total else 0


if __name__ == "__main__":
    if sys.argv[1] == "volcar":
        volcar(sys.argv[2], sys.argv[3])
    else:
        sys.exit(comparar(sys.argv[2], sys.argv[3]))
