"""T-133 QA r01 · `verificar` contra el registro del agente (H-23): ¿rompe usos legítimos? ¿sigue viendo manipulaciones?

Se ejecuta con el banco de un WORKTREE (el registro por defecto cae en <worktree>/.docs/experimentos, nunca en el del
repositorio principal) y con RI_AGENTE=qa-r01-t133, para no tocar el registro de ningún agente; el fichero se borra al final.
Titular falso (se sustituye `titular_a`) y datos en un temporal.
1. Uso normal: `a` con el registro por defecto y `verificar <carpeta>` sin --registro.
2. La carpeta de salida movida o copiada a otro sitio (archivar la evidencia en un ticket): sin y con --registro.
3. Otro agente (otro registro) que verifica con y sin --registro.
4. `a` con --registro propio y `verificar` sin --registro (el uso de CA-1 de T-94) y con él.
5. Rutas relativas y carpeta alcanzada por un enlace simbólico.
6. Manipulaciones: «registro» de experimento.json con tipos raros, «intento» cambiado, «dentro_del_maximo» cambiado.
Uso: .venv/bin/python -B r01_02_verificar_usos.py <carpeta de banco_medida.py de un worktree>"""
import contextlib
import io
import json
import os
import random
import shutil
import sys
import tempfile
from pathlib import Path

os.environ["RI_AGENTE"] = "qa-r01-t133"
import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
if len(sys.argv) < 2:
    sys.exit("uso: r01_02_verificar_usos.py <carpeta de banco_medida.py de un worktree>")
CARPETA = Path(sys.argv[1]).resolve()
if CARPETA == Path(__file__).resolve().parents[4] / "scripts":
    sys.exit("no con el banco del repositorio principal: el registro por defecto caería en su .docs/experimentos")
sys.path.insert(0, str(CARPETA))
import banco_medida as bm
import registro_experimentos as rx

fallos = []


def ok(cond, msg):
    print(("OK   " if cond else "FALLO ") + msg)
    if not cond:
        fallos.append(msg)


DEF = rx.REGISTRO_DEFECTO
assert DEF is not None and str(DEF).startswith(str(CARPETA.parents[1])), DEF
assert not DEF.exists(), f"{DEF} ya existe: no se toca"
TMP = Path(tempfile.mkdtemp(prefix="r01_t133_verificar_"))
datos = TMP / "datos"
datos.mkdir()
fechas = pd.bdate_range("2023-01-02", "2026-06-30")
rng = np.random.default_rng(5)
sims = [f"S{i}" for i in range(8)]
for s in sims:
    pd.DataFrame({"fecha": fechas.strftime("%Y-%m-%d"),
                  "cierre": 100 * np.exp(np.cumsum(rng.normal(0, 0.01, len(fechas))))}).to_csv(datos / f"{s}.csv", index=False)
universo = TMP / "universo.csv"
pd.DataFrame({"simbolo": sims, "clase": ["C"] * 8}).to_csv(universo, index=False)
CORTES = pd.date_range("2024-01-05", periods=30, freq="7D")


def titular(desde, hasta, carpeta, cliente, frecuencia, clases, **kw):
    r = random.Random(desde)
    sel = [{"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": r.choice(sims), "direccion": "LARGO", "horizonte": "H"}
           for c in CORTES]
    return {"selecciones": sel, "consumo": {"llamadas": 1, "tokens_entrada": 1, "tokens_salida": 1, "coste_estimado": None},
            "datos": datos, "universo": universo, "fecha_fin": lambda ini, h: ini + pd.Timedelta(days=5),
            "advertencias": [], "excluidos_contaminacion": 0}


bm.titular_a = titular


def orden(*args):
    err = io.StringIO()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
        codigo = bm.main(list(map(str, args)))
    return codigo, [x for x in err.getvalue().splitlines() if x.strip()]


def a(salida, *extra, desde="2024-01-05"):
    c, e = orden("a", "--desde", desde, "--hasta", "2024-07-26", "--salida", salida, "--datos", datos, "--universo", universo,
                 "--remuestreos", 200, *extra)
    assert c == 0, e
    return Path(salida)


try:
    # 1. Uso normal
    c1 = a(TMP / "s1")
    cod, err = orden("verificar", c1)
    print(f"   verificar sin --registro tras `a` con el registro por defecto: código {cod} {err}")
    ok(cod == 0, "uso normal: `a` con el registro por defecto y `verificar <carpeta>` sin --registro pasan")

    # 2. La carpeta movida / copiada
    archivo = TMP / "ticket" / "evidencias" / "s1"
    archivo.parent.mkdir(parents=True)
    shutil.copytree(c1, archivo)
    cod, err = orden("verificar", archivo)
    print(f"   copia de la carpeta en otro sitio, sin --registro: código {cod} {err}")
    ok(cod == 0, "una carpeta auténtica copiada a otro sitio (evidencia archivada) se verifica sin --registro")
    cod, err = orden("verificar", archivo, "--registro", DEF)
    print(f"   la misma copia con --registro del agente: código {cod} {err}")
    ok(cod == 0, "una carpeta auténtica copiada a otro sitio se verifica con --registro (README: «avisa si la carpeta cita otro»)")
    movida = TMP / "movida"
    shutil.move(str(c1), movida)
    cod, err = orden("verificar", movida)
    print(f"   la carpeta movida (mv), sin --registro: código {cod} {err}")
    ok(cod == 0, "una carpeta auténtica movida se verifica")

    # 3. Otro agente
    otro = TMP / "registro_astra.jsonl"
    c3 = a(TMP / "s3", "--registro", otro, desde="2024-01-12")
    cod, err = orden("verificar", c3)
    print(f"   carpeta anotada en el registro de otro agente, verificada sin --registro: código {cod} {err}")
    ok(cod != 0, "verificar sin --registro no da por buena una carpeta de otro registro (comprueba contra el del agente)")
    cod, err = orden("verificar", c3, "--registro", otro)
    ok(cod == 0, "con --registro del otro agente, la carpeta auténtica pasa")

    # 4. Relativas y enlaces simbólicos
    previo = os.getcwd()
    os.chdir(TMP)
    try:
        c4 = a("rel/s4", "--registro", "rel_reg.jsonl", desde="2024-01-19")
        cod, err = orden("verificar", "rel/s4", "--registro", "rel_reg.jsonl")
    finally:
        os.chdir(previo)
    ok(cod == 0, f"rutas relativas en `a` y en `verificar` (código {cod} {err})")
    enlace = TMP / "enlace"
    os.symlink(TMP / "rel", enlace)
    cod, err = orden("verificar", enlace / "s4", "--registro", TMP / "rel_reg.jsonl")
    ok(cod == 0, f"la carpeta alcanzada por un enlace simbólico (código {cod} {err})")

    # 5. Manipulaciones de experimento.json
    c5 = a(TMP / "s5", desde="2024-01-26")
    fe = c5 / "experimento.json"
    original = fe.read_text(encoding="utf-8")
    for nombre, cambio in (("registro nulo", {"registro": None}), ("registro numérico", {"registro": 7}),
                           ("registro absoluto a otro", {"registro": str(otro)}), ("intento 1", {"intento": 1}),
                           ("dentro_del_maximo como texto", {"dentro_del_maximo": "true"}),
                           ("exp_id de otro experimento", {"exp_id": "EXP-2026-0099"})):
        e = json.loads(original)
        e.update(cambio)
        fe.write_text(json.dumps(e), encoding="utf-8")
        cod, err = orden("verificar", c5)
        ok(cod != 0, f"experimento.json con {nombre}: verificar lo ve (código {cod}, {err[:1]})")
    fe.write_text("[1, 2]", encoding="utf-8")
    try:
        cod, err = orden("verificar", c5)
        ok(cod != 0, f"experimento.json que es una lista: verificar lo ve sin traza (código {cod})")
    except Exception as ex:   # noqa: BLE001
        ok(False, f"experimento.json que es una lista: traza {type(ex).__name__}: {ex}")
    fe.write_text(original, encoding="utf-8")
    ok(orden("verificar", c5)[0] == 0, "restaurado, vuelve a pasar")
finally:
    for f in (DEF, Path(str(DEF) + ".sello"), Path(str(DEF) + ".cerrojo")):
        f.unlink(missing_ok=True)
    with contextlib.suppress(OSError):
        DEF.parent.rmdir()
    shutil.rmtree(TMP, ignore_errors=True)

print()
print(f"{len(fallos)} fallo(s)")
for f in fallos:
    print(" - " + f)
sys.exit(1 if fallos else 0)
