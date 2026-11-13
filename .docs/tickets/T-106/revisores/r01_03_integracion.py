"""QA r01 de T-106 · Integración: Motor ↔ Catálogo, fallo cerrado del Catálogo, CT-09 de punta a punta, RC, §1.3 y corpus.

1. Lo servible = código ∩ IMPLEMENTADO del Catálogo (y las 21 V5.0 dentro).
2. Catálogo ausente, vacío, con bytes no UTF-8, con una fila degradada o con una fila de DOCUMENTADAS_CON_CODIGO
   subida a IMPLEMENTADO: el Motor debe fallar cerrado (sin excepción, sin servir lo que no toca).
3. Ejecutor movido de sitio con `rutas.raiz_paquete` (README del ejecutor): ¿encuentra el Catálogo el Motor?
4. CT-09 de punta a punta con los datos nominales de cada caso: estado SERVED / SERVED_WITH_LIMITATIONS y por qué.
   Una entrada mal formada: ¿RECHAZADO registrado en RC, o una excepción que sube al llamador?
5. §1.3 y la línea «Prioridad y madurez» de cada ficha frente a la tabla; manifiesto del corpus frente al archivo.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_03_integracion.py [RAIZ]
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r01_comun as C  # noqa: E402

M = C.preparar(sys.argv[1] if len(sys.argv) > 1 else None)
S, RAIZ = M["servicio"], M["raiz"]
CAT = RAIZ / "bloque_a" / S.RUTA_CATALOGO[0] / S.RUTA_CATALOGO[1]
V50 = sorted(S.CASOS_CONTROL)

# ------------------------------------------------------------------ 1. servible = código ∩ IMPLEMENTADO
S.madurez_catalogo.cache_clear()
mad = S.madurez_catalogo()
impl = {f for f, v in mad.items() if v.startswith(("IMPLEMENTADO", "VALIDADO"))}
serv = {f for f in S.IMPLEMENTADAS if S.servible(f)}
C.informe("tabla del Catálogo con 81 fichas leídas", len(mad) == 81, str(len(mad)))
C.informe("servible = código ∩ IMPLEMENTADO (salvo GARCH sin arch)",
          serv | ({"VOL-GARCH-001"} if not S.garch_disponible() else set()) == impl, f"{len(serv)} servibles, {len(impl)} IMPL")
C.informe("las 21 V5.0 son servibles", set(V50) <= serv)
C.informe("ninguna DOCUMENTADA_CON_CODIGO es servible", not (S.DOCUMENTADAS_CON_CODIGO & serv))


# ------------------------------------------------------------------ 2. Catálogo manipulado (copia temporal)
def con_catalogo(texto: bytes | None):
    d = Path(tempfile.mkdtemp(prefix="qa_t106_cat_"))
    if texto is not None:
        p = d / S.RUTA_CATALOGO[0] / S.RUTA_CATALOGO[1]
        p.parent.mkdir(parents=True)
        p.write_bytes(texto)
    return d


orig = CAT.read_bytes()
txt = orig.decode("utf-8")
casos = {
    "ausente": None,
    "vacío": b"",
    "bytes no UTF-8": orig[:2000] + b"\xff\xfe" + orig[2000:],
    "MON-YLD degradada a Documentado": re.sub(r"^(\| MON-YLD-001 \|.*\| P1 \| )IMPLEMENTADO[^|]*\|", r"\1Documentado |", txt,
                                              flags=re.M).encode(),
    "ACC-ERP subida a IMPLEMENTADO": re.sub(r"^(\| ACC-ERP-001 \|.*\| P\d \| )Documentado \|", r"\1IMPLEMENTADO |", txt,
                                            flags=re.M).encode(),
    "fila falsa de MON-YLD ANTES de la tabla, en Documentado": txt.replace(
        "\n## ", "\n| MON-YLD-001 | x | MC-01 | x | x | P1 | Documentado |\n\n## ", 1).encode(),
}
for nombre, contenido in casos.items():
    d = con_catalogo(contenido)
    S.madurez_catalogo.cache_clear()
    os.environ["BLOQUE_A_RAIZ"] = str(d)
    try:
        serv2 = {f for f in S.IMPLEMENTADAS if S.servible(f)}
        err = None
    except Exception as e:  # noqa: BLE001
        serv2, err = set(), f"{type(e).__name__}: {e}"[:120]
    finally:
        os.environ.pop("BLOQUE_A_RAIZ", None)
        shutil.rmtree(d, ignore_errors=True)
    if nombre in ("ausente", "vacío", "bytes no UTF-8"):
        C.informe(f"Catálogo {nombre}: nada servible y sin excepción", err is None and not serv2, err or f"{len(serv2)} servibles")
    elif nombre.startswith("MON-YLD degradada"):
        C.informe(f"Catálogo con {nombre}: deja de servirse solo esa", err is None and serv2 == serv - {"MON-YLD-001"})
    elif nombre.startswith("ACC-ERP"):
        C.informe(f"Catálogo con {nombre}: sigue sin servirse (DOCUMENTADAS_CON_CODIGO)", err is None and serv2 == serv)
    else:
        C.informe(f"Catálogo con {nombre}: manda la tabla del §2, no la primera fila que encaja",
                  err is None and "MON-YLD-001" in serv2, "la fila falsa gana" if "MON-YLD-001" not in serv2 else "")
S.madurez_catalogo.cache_clear()

# Caché: un Catálogo que cambia en caliente no se relee (lru_cache) — informativo
d = con_catalogo(None)
os.environ["BLOQUE_A_RAIZ"] = str(d)
S.madurez_catalogo.cache_clear()
vacio = S.madurez_catalogo()
p = d / S.RUTA_CATALOGO[0] / S.RUTA_CATALOGO[1]
p.parent.mkdir(parents=True)
p.write_bytes(orig)
despues = S.madurez_catalogo()
os.environ.pop("BLOQUE_A_RAIZ", None)
shutil.rmtree(d, ignore_errors=True)
S.madurez_catalogo.cache_clear()
print(f"      (informativo) Catálogo ausente al primer uso y restaurado después: el proceso sigue sin servir nada "
      f"({len(vacio)} → {len(despues)} fichas leídas; lru_cache sin invalidación)")

# ------------------------------------------------------------------ 3. ejecutor movido con rutas.raiz_paquete
movido = Path(tempfile.mkdtemp(prefix="qa_t106_mov_"))
shutil.copytree(M["ejec"], movido / "11_Ejecutor", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
codigo = f"""
import sys; sys.path.insert(0, {str(movido / '11_Ejecutor')!r})
from pathlib import Path
import tempfile
from bloque_a.configuracion import cargar_config, raiz_paquete
from bloque_a.almacen import Almacen
from bloque_a.motor import servicio as S
cfg = cargar_config()
cfg.setdefault("rutas", {{}})["raiz_paquete"] = {str(RAIZ / 'bloque_a')!r}
assert Path(S.__file__).resolve().is_relative_to(Path({str(movido)!r}).resolve())
print("raiz_paquete(cfg) =", raiz_paquete(cfg))
print("prompts visibles:", (raiz_paquete(cfg) / "02_System_prompts").exists())
print("servibles:", sum(1 for f in S.IMPLEMENTADAS if S.servible(f)))
"""
out = subprocess.run([sys.executable, "-I", "-B", "-c", codigo], capture_output=True, text=True, timeout=120)
shutil.rmtree(movido, ignore_errors=True)
m = re.search(r"servibles: (\d+)", out.stdout)
C.informe("ejecutor movido con rutas.raiz_paquete (README): el Motor encuentra el Catálogo y sirve lo IMPLEMENTADO",
          bool(m) and int(m.group(1)) == len(serv), (out.stdout.strip().replace("\n", " | ") or out.stderr[-300:]))

# ------------------------------------------------------------------ 4. CT-09 de punta a punta
tmp = Path(tempfile.mkdtemp(prefix="qa_t106_ct09_"))
mo = C.motor(tmp)
estados: dict[str, tuple[str, list]] = {}
for f in V50:
    caso = S.CASOS_CONTROL[f][0]
    r = mo.servir({"operacion": f, "datos": caso.get("datos") or [], "parametros": dict(caso.get("parametros") or {}),
                   "fecha_corte": "2026-11-12"}, "AG-21")
    estados[f] = (r["estado"], r.get("limitaciones") or [])
con_lim = sorted(f for f, (e, _) in estados.items() if e == "SERVED_WITH_LIMITATIONS")
siempre = []
for f in con_lim:
    mod = next(mm for mm in M["mods"] if f in mm.FICHAS)
    src = Path(mod.__file__).read_text(encoding="utf-8")
    fijas = [x for x in estados[f][1] if x[:40] in src]
    if fijas and len(fijas) == len(estados[f][1]):
        siempre.append(f)
print("      estados CT-09 con los datos nominales:", dict(Counter(e for e, _ in estados.values())))
C.informe("SERVED_WITH_LIMITATIONS solo por problemas de los datos, no por las advertencias fijas de la ficha",
          not siempre, f"solo advertencias fijas como limitaciones en: {siempre}")
# entrada mal formada por CT-09: ¿RECHAZADO + RC, o excepción?
malas = {"IDX-REL-001": lambda v: v["indice_a"]["historia"][-1].update(per_adelantado="n/d"),
         "MON-EXP-001": lambda v: v.update(reuniones="2026-12-17"),
         "MON-REAL-001": lambda v: v["divisas"].update(USD="sin datos"),
         "IDX-ERP-001": lambda v: v["escenarios"].update(bajo=0.005)}
for f, mutar in malas.items():
    caso = S.CASOS_CONTROL[f][0]
    ent = C.entrada(caso)
    mutar(ent["valores"])
    n_rc = len(mo.almacen.leer("RC"))
    try:
        r = mo.servir({"operacion": f, "datos": [{"valores": ent["valores"]}], "parametros": dict(caso.get("parametros") or {}),
                       "fecha_corte": "2026-11-12"}, "AG-21")
        res, det = r["estado"] == "RECHAZADO" and len(mo.almacen.leer("RC")) == n_rc + 1, f"{r['estado']} {r.get('motivo')}"
        if r["estado"] != "RECHAZADO":
            det += f" · {str(r.get('resultado'))[:160]}"
    except Exception as e:  # noqa: BLE001
        res, det = False, f"excepción {type(e).__name__}: {str(e)[:100]} (sin entrada en RC)"
    C.informe(f"CT-09 {f} con un dato mal formado → RECHAZADO registrado en RC", res, det)
shutil.rmtree(tmp, ignore_errors=True)

# verificar_casos_control: 21 entradas, 53 casos
tmp = Path(tempfile.mkdtemp(prefix="qa_t106_cc_"))
mo = C.motor(tmp)
res = mo.verificar_casos_control(run_id="QA-R01")
rc = [e for e in mo.almacen.leer("RC") if e.get("tipo_entrada") == "CASOS_CONTROL"]
C.informe("verificar_casos_control: 21 fichas, 53 casos superados, 21 entradas en RC",
          len(res) == 21 and sum(len(r["casos"]) for r in res.values()) == 53 and all(r["superados"] for r in res.values())
          and len(rc) == 21, f"{sum(len(r['casos']) for r in res.values())} casos")
shutil.rmtree(tmp, ignore_errors=True)

# ------------------------------------------------------------------ 5. §1.3, fichas y corpus
filas = re.findall(r"^\| ([A-Z]+(?:-[A-Z0-9]+)+-\d{3}) \|.*\| P\d \| ([^|]+?) \|\s*$", txt, re.M)
cnt = Counter("impl" if v.startswith("IMPLEMENTADO") else "her" if v.startswith("Implementado") else
              "doc" if v.startswith("Documentado") else v for _, v in filas)
sec13 = re.search(r"^Estado actual de las (\d+) fichas: (\d+) \*\*IMPLEMENTADO\*\*.*?; (\d+) heredadas.*?; (\d+) \*\*DOCUMENTADO\*\*",
                  txt, re.M)
C.informe("§1.3 cuadra con la tabla (81 = 35 + 11 + 35)", bool(sec13) and [int(x) for x in sec13.groups()] ==
          [len(filas), cnt["impl"], cnt["her"], cnt["doc"]] == [81, 35, 11, 35], f"{sec13.groups() if sec13 else None} {dict(cnt)}")
discrep = []
for fid, v in filas:
    mm = re.search(rf"^### {re.escape(fid)} ·.*?\*\*Prioridad y madurez\.\*\* P\d · ([^\n]+)", txt, re.M | re.S)
    if not mm:
        discrep.append(f"{fid}: sin ficha")
        continue
    a, b = v.split(" (")[0].upper(), mm.group(1).split(" (")[0].rstrip(".").upper()
    if a != b and not (a == "IMPLEMENTADO" and b.startswith("IMPLEMENTADO")):
        discrep.append(f"{fid}: tabla {v!r} · ficha {mm.group(1)!r}")
C.informe("la madurez de la tabla coincide con la de cada ficha (81)", not discrep, "; ".join(discrep[:6]))
v50_fichas = [fid for fid in V50 if re.search(rf"^### {re.escape(fid)} ·.*?madurez\.\*\* P\d · IMPLEMENTADO", txt, re.M | re.S)]
C.informe("las 21 V5.0 en IMPLEMENTADO en su ficha", len(v50_fichas) == 21)
man = (RAIZ / "tools" / "corpus_manifest.txt").read_text(encoding="utf-8")
h = hashlib.sha256(orig).hexdigest()
rel = str(CAT.relative_to(RAIZ))
linea = next((x for x in man.splitlines() if rel in x), "")
C.informe("manifiesto del corpus con la huella actual del Catálogo", h in linea, linea[:100])
sys.exit(C.resumen())
