"""Sondas del revisor sobre la batería de la pieza 3 (V0.62, robustez de la infraestructura T-03).

Ejecutar desde la raíz de marcoC:  python3 sondas_revisor_v062.py

S1  Fragilidad de expectativas: repite los bucles de mutación de la batería (los mismos objetivos y
    `esperados`) con 60 semillas distintas y cuenta los códigos observados. Un código fuera de los
    `esperados` de la batería = fallo falso latente (la entrega solo pasa con la semilla 20261111).
S1b Casos construidos a mano (sin azar): PE-03 es alcanzable en los cuatro objetivos que mutan el
    documento entero y NO está admitido; PE-07 declarado en `rotacion_claves` es inalcanzable
    (`_previas` da CL-01 antes); y la franquicia OK de la última línea del diario es inalcanzable
    (la batería escribe siempre el salto final: la última línea mutada es DI-02).
S2  No-vacuidad (huella): desactivar la comprobación de la huella del estado en una COPIA de
    persistencia.py -> la batería FALLA. La entrega declara que falla «exactamente» en DOS
    comprobaciones; aquí se ve que falla en CUATRO.
S3  No-vacuidad (diario): desactivar la cadena de hashes en una COPIA de diario.py -> la batería
    FALLA exactamente en las DOS comprobaciones declaradas (control positivo de S2).

Datos SIMULADOS. No toca los ficheros de la entrega: todas las sondas trabajan sobre copias
temporales o sobre estructuras en memoria.
"""
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "validador"))
sys.path.insert(0, str(RAIZ / "pruebas"))

import diario as di  # noqa: E402
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
import rotacion as rt  # noqa: E402
from pruebas_orquestador import nuevo, hasta  # noqa: E402
from pruebas_robustez import _mutar_en_sitio  # noqa: E402
from pruebas_robustez_t03 import T, TM, MOTIVO, K1, K2, _mutar_doc, _rehacer, _texto_doc  # noqa: E402

print("S1: fragilidad de expectativas (60 semillas x 24 casos por objetivo)")
ESPERADOS = {
    "persistencia_estado": {"PE-01", "PE-02"},
    "persistencia_cabecera": {"PE-01", "PE-02", "PE-03", "PE-08"},
    "persistencia_raiz": {"PE-01", "PE-02", "PE-03", "PE-08"},
    "persistencia_firmado": {"PE-01", "PE-06"},
    "persistencia_rehecho": {"OK", "O-13", "PE-01", "PE-02", "PE-03", "PE-04"},
    "diario_estado": {"PE-01", "PE-02", "PE-06"},
    "migraciones_texto": {"OK", "PE-01", "PE-02"},
    "migraciones_rehecho": {"OK", "PE-01", "PE-02"},
    "rotacion_texto": {"PE-01", "PE-02", "PE-06", "CL-02"},
    "rotacion_sin_firmar": {"PE-01", "PE-02", "CL-02"},
}
o_base = nuevo()
hasta(o_base, "AUTORIZADA", n=1)
t0 = pe.volcar(o_base, T)
t1 = pe.volcar(o_base, T, K1)
td = tempfile.mkdtemp()
re_, rd_ = os.path.join(td, "base.e"), os.path.join(td, "base.d")
hasta(di.crear(nuevo(), re_, rd_, T)["diario"], "PROPUESTA")
estado_puro = open(re_, encoding="ascii").read()
obs = defaultdict(lambda: defaultdict(int))
for s in range(60):
    rng = random.Random(1000 + s)
    for _ in range(24):
        for nombre, texto, fn in (
            ("persistencia_estado", _mutar_doc(t0, rng, dentro_estado=True), pe.cargar),
            ("persistencia_cabecera", _mutar_doc(t0, rng, dentro_estado=False), pe.cargar),
            ("persistencia_firmado", _mutar_doc(t1, rng, dentro_estado=rng.random() < 0.5), pe.cargar),
            ("persistencia_rehecho", _rehacer(_mutar_doc(t0, rng, dentro_estado=True)), pe.cargar),
            ("migraciones_texto", _mutar_doc(t0, rng, dentro_estado=rng.random() < 0.5), None),
            ("migraciones_rehecho", _rehacer(_mutar_doc(t0, rng, dentro_estado=True)), None),
        ):
            try:
                r = pe.cargar(texto) if fn else mg.migrar(texto, TM, MOTIVO)
                obs[nombre][r["codigo"]] += 1
            except Exception as ex:  # noqa: BLE001
                obs[nombre][f"LANZA {type(ex).__name__}"] += 1
        raiz, _ = _mutar_en_sitio(json.loads(t0), rng)
        obs["persistencia_raiz"][pe.cargar(raiz if isinstance(raiz, str) else _texto_doc(raiz))["codigo"]] += 1
        for nombre, args in (
            ("rotacion_texto", (_mutar_doc(t1, rng, dentro_estado=rng.random() < 0.5), TM, MOTIVO, K1, K2)),
            ("rotacion_sin_firmar", (_mutar_doc(t0, rng, dentro_estado=rng.random() < 0.5), TM, MOTIVO, None, K1)),
        ):
            obs[nombre][rt.rotar(*args)["codigo"]] += 1
        d_e, _ = _mutar_en_sitio(json.loads(estado_puro), rng)
        re_i, rd_i = os.path.join(td, "s.e"), os.path.join(td, "s.d")
        with open(re_i, "w", encoding="utf-8") as f:
            f.write(_texto_doc(d_e))
        with open(rd_i, "w", encoding="ascii") as f:
            f.write(estado_puro.splitlines()[0] + "\n")
        obs["diario_estado"][di.abrir(re_i, rd_i)["codigo"]] += 1
fuera_total = 0
for nombre in ESPERADOS:
    codes = dict(obs[nombre])
    malos = {c: n for c, n in codes.items() if c not in ESPERADOS[nombre]}
    fuera_total += bool(malos)
    print(f"  {nombre:24} " + ", ".join(f"{c}x{n}" for c, n in sorted(codes.items(), key=lambda kv: -kv[1]))
          + (f"   <<< FUERA: {malos}" if malos else ""))
print(f"  -> objetivos con codigos fuera de sus esperados: {fuera_total} de {len(ESPERADOS)}\n")

print("S1b: casos construidos a mano (sin azar)")


def con_formato(texto, v="x"):
    d = json.loads(texto)
    d["formato"] = v
    return _texto_doc(d)


r = None  # (los cuatro objetivos, uno a uno, sin azar)
d = json.loads(estado_puro)
d["formato"] = "x"
with open(os.path.join(td, "b1.e"), "w", encoding="utf-8") as f:
    f.write(_texto_doc(d))
with open(os.path.join(td, "b1.d"), "w", encoding="ascii") as f:
    f.write(estado_puro.splitlines()[0] + "\n")
print("  diario_estado      formato='x' ->", di.abrir(os.path.join(td, "b1.e"), os.path.join(td, "b1.d"))["codigo"],
      " (esperados de la bateria: PE-01/PE-02/PE-06)")
print("  migraciones_texto  formato='x' ->", mg.migrar(con_formato(t0), TM, MOTIVO)["codigo"],
      " (esperados: OK/PE-01/PE-02)")
print("  rotacion_texto     formato='x' ->", rt.rotar(con_formato(t1), TM, MOTIVO, K1, K2)["codigo"],
      " (esperados: PE-01/PE-02/PE-06/CL-02)")
print("  rotacion_sin_firmar formato='x' ->", rt.rotar(con_formato(t0), TM, MOTIVO, None, K1)["codigo"],
      " (esperados: PE-01/PE-02/CL-02)")
for cv, cn in ((K1, "K1"), ("K1", K2), (7, K2), (K1, None)):
    print(f"  rotacion_claves    vieja={str(cv)[:6]!r:8} nueva={str(cn)[:6]!r:8} ->",
          rt.rotar(t1, TM, MOTIVO, cv, cn)["codigo"], " (PE-07 declarado: inalcanzable, _previas da CL-01)")
codigos = set()
rng = random.Random(7)
lineas = estado_puro.splitlines()
for _ in range(30):
    e = json.loads(open(rd_, encoding="ascii").read().splitlines()[-1])
    e, _ = _mutar_en_sitio(e, rng)
    with open(os.path.join(td, "b2.e"), "w", encoding="ascii") as f:
        f.write(estado_puro)
    with open(os.path.join(td, "b2.d"), "w", encoding="ascii") as f:
        f.write("\n".join(lineas[:-1] + [_texto_doc(e)]) + "\n")
    codigos.add(di.abrir(os.path.join(td, "b2.e"), os.path.join(td, "b2.d"))["codigo"])
print("  ultima linea mutada (30 casos, con salto final):", sorted(codigos),
      " (la franquicia OK del 'corte' es inalcanzable)\n")

print("S2: no-vacuidad con la huella desactivada (copia temporal de persistencia.py)")


def bateria_en_copia(fichero, viejo, nuevo_txt):
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "marcoC"
        shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns("entrega_glm", "*.pyc", "__pycache__"))
        p = copia / "validador" / fichero
        src = p.read_text(encoding="utf-8")
        assert viejo in src, f"no encuentro el fragmento en {fichero}"
        p.write_text(src.replace(viejo, nuevo_txt), encoding="utf-8")
        r = subprocess.run([sys.executable, str(copia / "pruebas" / "pruebas_robustez_t03.py")],
                           capture_output=True, text=True, cwd=str(copia))
        return r.returncode, [l for l in r.stdout.splitlines() if l.startswith("FALLA")], \
            [l for l in r.stdout.splitlines() if l.startswith("RESULTADO")]


rc, falas, res = bateria_en_copia("persistencia.py", 'if _huella(doc["estado"]) != doc["huella"]:', "if False:")
print(f"  exit={rc}  {res[0] if res else '(sin resultado)'}")
for f in falas:
    print("   ", f[:150])
print(f"  -> falla en {len(falas)} comprobaciones; la entrega declara 'exactamente' 2\n")

print("S3: no-vacuidad con la cadena de hashes desactivada (copia temporal de diario.py)")
rc, falas, res = bateria_en_copia(
    "diario.py", 'and _h({k: v for k, v in e.items() if k not in ("hash", "firma")}) == e["hash"]', "and True")
print(f"  exit={rc}  {res[0] if res else '(sin resultado)'}")
for f in falas:
    print("   ", f[:150])
print(f"  -> falla en {len(falas)} comprobaciones; la entrega declara 'exactamente' 2")

shutil.rmtree(td, ignore_errors=True)
