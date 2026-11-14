"""QA r01 de T-118 · regresión del ciclo simulado V5 de A: mismo estado y mismos entregables antes y después.

Uso: r01_06_regresion_ciclo.py <ejecutor_antes> <ejecutor_despues> <carpeta_salidas>
Ejecuta en cada ejecutor el backtest de CLAUDE.md (`--cliente mock … backtest --desde 2024-01-05 --hasta 2024-03-29`) con
el paquete de ese ejecutor, en la MISMA ruta de salida, y compara fichero a fichero. Lo que T-118 cambia a propósito es el
Registro de cálculos (`artefacto.configuracion_usada` en los SERVICIO y `reejecucion.configuracion` en las REEJECUCION) y,
con él, su cadena de hash y su sello: el RC se compara además sin esos campos ni la cadena. `consumo.csv` lleva latencias.
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

antes, despues, salidas = (Path(a).resolve() for a in sys.argv[1:4])
PY = Path(__file__).resolve().parents[4] / ".venv" / "bin" / "python"
ARGS = ["--cliente", "mock", "--datos", "ejemplos/datos_sinteticos", "--universo", "config/universo_ejemplo.csv"]
CADENA = {"_hash", "_hash_prev", "_ts"}


def correr(eje: Path, destino: Path) -> float:
    out = destino.parent / "salida_mock"
    shutil.rmtree(out, ignore_errors=True)
    shutil.rmtree(destino, ignore_errors=True)
    out.mkdir(parents=True)
    codigo = f"import sys; sys.path.insert(0, {str(eje)!r}); sys.argv = ['bloque-a'] + sys.argv[1:]; from bloque_a.cli import main; sys.exit(main())"
    t0 = time.time()
    r = subprocess.run([str(PY), "-I", "-c", codigo, *ARGS, "--salida", str(out), "backtest", "--desde", "2024-01-05", "--hasta", "2024-03-29"],
                       cwd=eje, capture_output=True, text=True)
    (destino.parent / f"{destino.name}.log").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit(f"el ciclo falla en {eje} ({r.returncode})")
    out.rename(destino)
    return time.time() - t0


def rc_sin_t118(linea: str) -> dict:
    e = json.loads(linea)
    for k in CADENA:
        e.pop(k, None)
    if isinstance(e.get("artefacto"), dict):
        e["artefacto"].pop("configuracion_usada", None)
    if isinstance(e.get("reejecucion"), dict):
        e["reejecucion"].pop("configuracion", None)
    return e


ta, td = correr(antes, salidas / "antes"), correr(despues, salidas / "despues")
print(f"ciclo antes {ta:.0f} s · después {td:.0f} s")
fa = {p.relative_to(salidas / "antes") for p in (salidas / "antes").rglob("*") if p.is_file()}
fd = {p.relative_to(salidas / "despues") for p in (salidas / "despues").rglob("*") if p.is_file()}
print(f"ficheros: antes {len(fa)}, después {len(fd)}; solo antes {sorted(map(str, fa - fd))}; solo después {sorted(map(str, fd - fa))}")
distintos = [rel for rel in sorted(fa & fd) if (salidas / "antes" / rel).read_bytes() != (salidas / "despues" / rel).read_bytes()]
print(f"idénticos byte a byte: {len(fa & fd) - len(distintos)} de {len(fa & fd)}")
mal = 0
for rel in distintos:
    a = (salidas / "antes" / rel).read_text(encoding="utf-8", errors="replace")
    b = (salidas / "despues" / rel).read_text(encoding="utf-8", errors="replace")
    if rel.name == "RC_registro_calculos.jsonl":
        la, lb = [rc_sin_t118(x) for x in a.splitlines() if x.strip()], [rc_sin_t118(x) for x in b.splitlines() if x.strip()]
        dif = [i for i, (x, y) in enumerate(zip(la, lb)) if x != y]
        nuevos = sum(1 for x in b.splitlines() if '"configuracion_usada"' in x)
        con = sum(1 for x in b.splitlines() if x.strip() and json.loads(x).get("artefacto", {}).get("configuracion_usada"))
        print(f"  {rel}: {len(la)} y {len(lb)} entradas; distintas sin los campos de T-118 ni la cadena: {len(dif)}; "
              f"con `configuracion_usada`: {nuevos} (no vacío en {con}); bytes {len(a.encode())} → {len(b.encode())} "
              f"(+{100 * (len(b.encode()) - len(a.encode())) / len(a.encode()):.2f} %)")
        mal += bool(dif) or len(la) != len(lb)
        for i in dif[:3]:
            ka = {k for k in set(la[i]) | set(lb[i]) if la[i].get(k) != lb[i].get(k)}
            print(f"     entrada {i}: difieren {sorted(ka)}")
    elif rel.name == "consumo.csv":
        fa_, fb_ = [x.split(",") for x in a.splitlines()], [x.split(",") for x in b.splitlines()]
        cab = fa_[0]
        cols = [i for i, c in enumerate(cab) if "latencia" not in c and "duracion" not in c and c not in ("ts", "hora")]
        igual = len(fa_) == len(fb_) and all([x[i] for i in cols] == [y[i] for i in cols] for x, y in zip(fa_, fb_))
        print(f"  {rel}: {'igual salvo latencias' if igual else 'DISTINTO'} (columnas: {cab})")
        mal += not igual
    elif rel.name == "sellos_integridad.json":
        ja, jb = json.loads(a), json.loads(b)
        claves = sorted(k for k in set(ja) | set(jb) if ja.get(k) != jb.get(k))
        print(f"  {rel}: difieren los sellos de {claves} (se espera solo RC)")
        mal += claves != ["RC"]
    else:
        print(f"  {rel}: DISTINTO ({len(a)} y {len(b)} caracteres)")
        try:
            ja, jb = json.loads(a), json.loads(b)
            if isinstance(ja, dict):
                print(f"     claves que difieren: {sorted(k for k in set(ja) | set(jb) if ja.get(k) != jb.get(k))[:12]}")
        except ValueError:
            pass
        mal += 1


def prof(x):
    if isinstance(x, dict):
        return 1 + max([prof(v) for v in x.values()] + [0])
    if isinstance(x, list):
        return 1 + max([prof(v) for v in x] + [0])
    return 0


rc = [json.loads(x) for x in (salidas / "despues" / "estado" / "RC_registro_calculos.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
tipos = {}
for e in rc:
    tipos[e.get("tipo_entrada")] = tipos.get(e.get("tipo_entrada"), 0) + 1
print(f"RC del ciclo: {tipos}; anidamiento máximo de lo que el ciclo pide al Motor (parámetros y datos de cada entrada): "
      f"{max(max(prof(e.get('parametros')), prof(e.get('datos'))) for e in rc)} niveles (el tope de una petición es 32)")
print("RESULTADO:", "sin diferencias fuera de los campos nuevos del RC, su cadena y las latencias" if not mal else f"{mal} ficheros con diferencias de fondo")
sys.exit(1 if mal else 0)
