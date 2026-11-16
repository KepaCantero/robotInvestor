"""T-158 QA r01 · Sin guías, el ciclo da lo mismo que antes de T-158.

Extrae el ejecutor de la versión anterior (`git archive <base>`, por defecto HEAD~1) en una carpeta desechable (el resto de
`bloque_a/`, que T-158 no toca, se enlaza), ejecuta el mismo
ciclo con la CLI y el cliente simulado en las dos versiones (`python -m bloque_a.cli --cliente mock … ciclo`) y compara todo el
estado (F1–F6, F10, RC, HA, contadores) y los entregables, quitando solo los sellos de tiempo, las huellas encadenadas y
la ruta de la carpeta de trabajo.
Después, en la versión actual, emite la guía de ejemplo de PB-48 por la CLI, repite el ciclo y lista las guías (`guia listar`).

Uso, desde la raíz de la copia:
    .venv/bin/python .docs/tickets/T-158/revisores/r01_03_regresion_sin_guias.py <carpeta_desechable> [base]
Sale 1 si algo difiere.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path.cwd()
PY = str(RAIZ / ".venv" / "bin" / "python")
AS_OF = "2026-06-05"
VOLATIL = {"_ts", "_hash", "_hash_prev", "timestamp", "ts", "acuse"}
RE_TS = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(\+\d{2}:\d{2}|Z)?")


def ciclo(ejecutor: Path, trabajo: Path, *orden: str) -> str:
    cmd = [PY, "-m", "bloque_a.cli", "--cliente", "mock", "--datos", "ejemplos/datos_sinteticos", "--estado", str(trabajo / "estado"),
           "--salida", str(trabajo / "salida"), "--as-of", AS_OF, *orden]
    r = subprocess.run(cmd, cwd=ejecutor, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        raise SystemExit(f"{' '.join(orden)} falló en {ejecutor}:\n{r.stderr[-3000:]}")
    return r.stdout


def limpiar(obj):
    if isinstance(obj, dict):
        return {k: limpiar(v) for k, v in obj.items() if k not in VOLATIL}
    if isinstance(obj, list):
        return [limpiar(x) for x in obj]
    if isinstance(obj, str):
        return RE_TS.sub("<TS>", obj)
    return obj


def volcado(carpeta: Path) -> dict[str, object]:
    """Contenido de la carpeta de trabajo; la ruta absoluta de la propia carpeta se cambia por <TRABAJO> y el fichero de sellos
    (huellas de lo demás, que llevan esa ruta) no se compara."""
    out: dict[str, object] = {}
    for p in sorted(carpeta.rglob("*")):
        if not p.is_file() or p.name == "sellos_integridad.json":
            continue
        rel = str(p.relative_to(carpeta))
        texto = p.read_text(encoding="utf-8", errors="replace").replace(str(carpeta), "<TRABAJO>")
        if p.suffix == ".jsonl":
            out[rel] = [limpiar(json.loads(x)) for x in texto.splitlines() if x.strip()]
        elif p.suffix == ".json":
            try:
                out[rel] = limpiar(json.loads(texto))
            except json.JSONDecodeError:
                out[rel] = RE_TS.sub("<TS>", texto)
        else:
            out[rel] = RE_TS.sub("<TS>", texto)
    return out


def main() -> int:
    tmp = Path(sys.argv[1]).resolve()
    base = sys.argv[2] if len(sys.argv) > 2 else "HEAD~1"
    prev = tmp / "prev"
    prev.mkdir(parents=True, exist_ok=True)
    arch = subprocess.run(["git", "archive", base, "bloque_a/11_Ejecutor"], cwd=RAIZ, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(prev)], input=arch, check=True)
    ej_prev, ej_act = prev / "bloque_a" / "11_Ejecutor", RAIZ / "bloque_a" / "11_Ejecutor"
    for hermana in (RAIZ / "bloque_a").iterdir():   # el corpus del bloque (prompts, archivos operativos…) no cambia: enlace
        destino = prev / "bloque_a" / hermana.name
        if hermana.name != "11_Ejecutor" and not destino.exists():
            destino.symlink_to(hermana)
    assert not (ej_prev / "bloque_a" / "guias.py").exists(), "la base ya tiene guias.py"
    ciclo(ej_prev, tmp / "t_prev", "ciclo")
    ciclo(ej_act, tmp / "t_act", "ciclo")
    a, b = volcado(tmp / "t_prev"), volcado(tmp / "t_act")
    difieren = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    print(f"ficheros comparados: {len(set(a) | set(b))}; difieren: {difieren or 'ninguno'}")
    for k in difieren[:5]:
        print(" ", k, "solo en una" if (k not in a or k not in b) else "")
    # La CLI con la guía de ejemplo de PB-48
    print(ciclo(ej_act, tmp / "t_guia", "guia", "emitir", "--receptor", "AG-02", "--json", "ejemplos/guias/guia_pb48.json")[:400])
    ciclo(ej_act, tmp / "t_guia", "ciclo")
    lista = json.loads(ciclo(ej_act, tmp / "t_guia", "guia", "listar"))
    print(json.dumps(lista, ensure_ascii=False))
    ha = [json.loads(x) for x in (tmp / "t_guia" / "estado").rglob("HA*.jsonl").__next__().read_text(encoding="utf-8").splitlines()]
    cor = [e for e in ha if e.get("tipo_entrada") == "COR"]
    p3 = [e for e in ha if e.get("tipo_entrada") == "P3"]
    print(f"COR-: {[e['id'] for e in cor]}  P3-: {[(e['id'], e['estado']) for e in p3]}")
    ok_cli = (lista.get("GUI-AG02-0001", {}).get("estado") == "SUPERSEDED" and lista.get("GUI-AG02-0002", {}).get("estado") == "ISSUED"
              and len(cor) == len(p3) == 1)
    print("CLI con la guía de PB-48:", "bien" if ok_cli else "MAL")
    return 1 if difieren or not ok_cli else 0


if __name__ == "__main__":
    sys.exit(main())
