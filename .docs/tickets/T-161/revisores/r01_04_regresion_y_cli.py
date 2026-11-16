"""QA r01 de T-161 · Sin guías, el ciclo da lo mismo que antes de T-161; y la CLI de las guías con la simulación.

Adapta `.docs/tickets/T-158/revisores/r01_03_regresion_sin_guias.py` (que exige una base anterior a T-158 y emite sin la opción
nueva): reutiliza su `ciclo` y su `volcado`, compara el ciclo sin guías de la base (por defecto HEAD~1, la instantánea anterior
a T-161) con el de la copia actual, y después ejerce por la CLI:
- `guia emitir` de la guía de PB-48 sin la opción: termina con «no se emite» y no escribe HA;
- con `--simular-fallo-del-emisor` y el cliente real (clave ficticia), el reproductor y la grabadora sobre el simulado: se rechaza;
- con `--cliente mock`: se emite, la GUI- lleva `control_emisor`, el ciclo la revisa (COR-, P3-, SUPERSEDED y versión nueva) y
  el ítem en conflicto no está en la guía vigente.

Uso, desde la raíz de la copia: .venv/bin/python .docs/tickets/T-161/revisores/r01_04_regresion_y_cli.py <carpeta_desechable> [base]
Sale 1 si algo difiere o falla.
"""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path.cwd()
PY = str(RAIZ / ".venv" / "bin" / "python")
AS_OF = "2026-06-05"
_spec = importlib.util.spec_from_file_location("r158", RAIZ / ".docs/tickets/T-158/revisores/r01_03_regresion_sin_guias.py")
R158 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R158)


def cli(ejecutor: Path, trabajo: Path, *orden: str, cliente=("--cliente", "mock"), env=None):
    cmd = [PY, "-m", "bloque_a.cli", *cliente, "--datos", "ejemplos/datos_sinteticos", "--estado", str(trabajo / "estado"),
           "--salida", str(trabajo / "salida"), "--as-of", AS_OF, *orden]
    return subprocess.run(cmd, cwd=ejecutor, capture_output=True, text=True, timeout=1800, env={**os.environ, **(env or {})})


def ha(trabajo: Path) -> list[dict]:
    fs = [p for p in (trabajo / "estado").rglob("HA*.jsonl")] if (trabajo / "estado").exists() else []
    return [json.loads(x) for p in fs for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def main() -> int:
    tmp = Path(sys.argv[1]).resolve()
    base = sys.argv[2] if len(sys.argv) > 2 else "HEAD~1"
    mal = []
    prev = tmp / "prev"
    prev.mkdir(parents=True, exist_ok=True)
    arch = subprocess.run(["git", "archive", base, "bloque_a/11_Ejecutor"], cwd=RAIZ, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(prev)], input=arch, check=True)
    ej_prev, ej_act = prev / "bloque_a" / "11_Ejecutor", RAIZ / "bloque_a" / "11_Ejecutor"
    for hermana in (RAIZ / "bloque_a").iterdir():
        destino = prev / "bloque_a" / hermana.name
        if hermana.name != "11_Ejecutor" and not destino.exists():
            destino.symlink_to(hermana)
    assert "simular_fallo_del_emisor" not in (ej_prev / "bloque_a" / "guias.py").read_text(encoding="utf-8"), "la base ya es T-161"
    R158.ciclo(ej_prev, tmp / "t_prev", "ciclo")
    R158.ciclo(ej_act, tmp / "t_act", "ciclo")
    a, b = R158.volcado(tmp / "t_prev"), R158.volcado(tmp / "t_act")
    difieren = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    print(f"[regresión] base {base}: ficheros comparados: {len(set(a) | set(b))}; difieren: {difieren or 'ninguno'}")
    if difieren:
        mal.append("regresión sin guías")
    guia = ("guia", "emitir", "--receptor", "AG-02", "--json", "ejemplos/guias/guia_pb48.json")
    # 1. sin la opción: no se emite
    r = cli(ej_act, tmp / "c_sin", *guia)
    ok = r.returncode != 0 and "no se emite" in r.stderr and not ha(tmp / "c_sin")
    print(f"[cli] sin la opción: código {r.returncode}, «{r.stderr.strip()[:110]}…», HA vacío: {not ha(tmp / 'c_sin')} → {'bien' if ok else 'MAL'}")
    mal += [] if ok else ["cli sin la opción"]
    # 2. con la opción y un cliente que no es el simulado
    repro = tmp / "repro.jsonl"
    repro.write_text(json.dumps({"clave": "x", "texto": "{}", "uso": {}, "modelo": "m"}) + "\n", encoding="utf-8")
    casos = [("anthropic", ("--cliente", "anthropic"), {"ANTHROPIC_API_KEY": "clave-ficticia-de-prueba"}),
             ("reproductor", ("--cliente", "replay", "--replay", str(repro)), None),
             ("grabadora sobre mock", ("--cliente", "replay", "--replay", str(tmp / "grab.jsonl"), "--replay-modo", "grabar"),
              {"BLOQUE_A_CLIENTE_BASE": "mock"})]
    for nombre, cliente, env in casos:
        t = tmp / f"c_{nombre.split()[0]}"
        r = cli(ej_act, t, *guia, "--simular-fallo-del-emisor", cliente=cliente, env=env)
        ok = r.returncode != 0 and "cliente simulado" in r.stderr and not [e for e in ha(t) if e.get("tipo_entrada") == "GUI"]
        print(f"[cli] simulación con {nombre}: código {r.returncode}, «{r.stderr.strip()[-90:]}» → {'bien' if ok else 'MAL'}")
        mal += [] if ok else [f"cli simulación con {nombre}"]
    # 3. con la opción y el simulado: emite con huella; el ciclo la revisa
    t = tmp / "c_mock"
    r = cli(ej_act, t, *guia, "--simular-fallo-del-emisor")
    print(f"[cli] simulación con mock: código {r.returncode} {r.stdout.strip()[:100]}")
    gui = [e for e in ha(t) if e.get("tipo_entrada") == "GUI"]
    huella = bool(gui) and gui[0].get("control_emisor", {}).get("simulado_fallo") is True
    r2 = cli(ej_act, t, "ciclo")
    lista = json.loads(cli(ej_act, t, "guia", "listar").stdout)
    entradas = ha(t)
    cor = [e for e in entradas if e.get("tipo_entrada") == "COR"]
    p3 = [e for e in entradas if e.get("tipo_entrada") == "P3"]
    estado: dict = {}
    for e in entradas:
        if e.get("tipo_entrada") == "GUI":
            estado.setdefault(e["id"], {}).update(e)
    vigente = estado.get("GUI-AG02-0002", {})
    ok = (r.returncode == 0 and r2.returncode == 0 and huella and lista.get("GUI-AG02-0001", {}).get("estado") == "SUPERSEDED"
          and vigente.get("estado") == "ISSUED" and len(vigente.get("items", [])) == 1
          and "segunda pasada" not in json.dumps(vigente["items"], ensure_ascii=False) and "control_emisor" not in vigente
          and estado["GUI-AG02-0001"].get("control_emisor", {}).get("simulado_fallo") is True
          and len(cor) == len(p3) == 1 and p3[0]["estado"] == "PENDING_OPERATOR")
    print(f"[cli] huella en GUI-AG02-0001: {huella}; listar: {json.dumps(lista, ensure_ascii=False)[:160]}…; COR-: {len(cor)}, "
          f"P3-: {[(e['id'], e['estado']) for e in p3]} → {'bien' if ok else 'MAL'}")
    mal += [] if ok else ["cli simulación con mock"]
    print("RESULTADO:", "bien" if not mal else f"MAL: {mal}")
    return 1 if mal else 0


if __name__ == "__main__":
    sys.exit(main())
