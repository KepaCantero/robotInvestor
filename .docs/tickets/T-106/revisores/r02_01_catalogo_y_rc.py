"""QA r02 de T-106 · «Manda el Catálogo» a través del Motor (no de la función suelta), registro de los casos de control en
RC y coherencia de la promoción y del corpus.

1. Motor ↔ Catálogo, con el Catálogo en una raíz temporal señalada por `rutas.raiz_paquete` (H-04):
   - Catálogo íntegro: el Motor sirve exactamente código ∩ IMPLEMENTADO;
   - una ficha V5.0 degradada en la tabla del §4 → RECHAZADO (METODO_NO_IMPLEMENTADO) con la madurez en el detalle;
   - la ficha degradada solo en su línea «Prioridad y madurez» (la tabla del §4 sigue en IMPLEMENTADO) → informativo;
   - sin «## 5.» (tabla sin cierre), bytes no UTF-8, Catálogo que es una carpeta → nada servible, sin excepción;
   - fila falsa en Documentado fuera del §4 (en el §1 y en el §5) → no manda;
   - relectura: el Catálogo se cambia en caliente (otra fecha de modificación) → el Motor lo ve; y el caso límite
     de un cambio que conserva la fecha de modificación (informativo);
   - ejecutor movido (copia en otra carpeta) con `rutas.raiz_paquete`: el Motor sirve lo IMPLEMENTADO.
2. RC: `verificar_casos_control` escribe 21 entradas CASOS_CONTROL con todos sus casos (66), superados, la madurez del
   Catálogo y `verificar_integridad` en verde; una ficha sin casos o desconocida → REJECTED; repetirlo no cambia nada
   salvo los identificadores; un caso que falla se registra como no superado.
3. Promoción: §4, línea de madurez de cada ficha y recuento del §1.3; Catálogo sin cambios desde la r01 (`7064f60`) y
   huella del manifiesto del corpus.

Uso: .venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_01_catalogo_y_rc.py [RAIZ]
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
ORIG = CAT.read_bytes()
TXT = ORIG.decode("utf-8")
V50 = sorted(S.CASOS_CONTROL)
TMP = Path(tempfile.mkdtemp(prefix="qa_r02_t106_"))


def raiz_con(contenido: bytes | None, carpeta: bool = False) -> Path:
    d = Path(tempfile.mkdtemp(dir=TMP))
    p = d / S.RUTA_CATALOGO[0] / S.RUTA_CATALOGO[1]
    p.parent.mkdir(parents=True)
    if carpeta:
        p.mkdir()
    elif contenido is not None:
        p.write_bytes(contenido)
    return d


def motor_en(raiz: Path):
    cfg = M["cargar_config"]()
    cfg.setdefault("rutas", {})["raiz_paquete"] = str(raiz)
    return S.Motor(M["Almacen"](Path(tempfile.mkdtemp(dir=TMP))), C.Proveedor(), cfg)


def servir(mo, ficha):
    caso = S.CASOS_CONTROL[ficha][0] if ficha in S.CASOS_CONTROL else {}
    return mo.servir({"operacion": ficha, "datos": caso.get("datos") or [], "parametros": dict(caso.get("parametros") or {}),
                      "fecha_corte": "2026-11-12"}, "AG-21")


def servibles(mo) -> set[str]:
    return {f for f in S.IMPLEMENTADAS if S.servible(f, mo.raiz)}


def degradar(txt: str, ficha: str) -> str:
    return re.sub(rf"^(\| {ficha} \|.*\| P\d \| )IMPLEMENTADO[^|]*\|", r"\1Documentado |", txt, flags=re.M)


# ------------------------------------------------------------------ 1. Motor ↔ Catálogo
mad = S.madurez_catalogo(RAIZ / "bloque_a")
impl = {f for f, v in mad.items() if v.startswith(("IMPLEMENTADO", "VALIDADO"))}
mo = motor_en(raiz_con(ORIG))
serv = servibles(mo)
C.informe("§4 leída: 81 fichas", len(mad) == 81, str(len(mad)))
C.informe("Motor: servible = código ∩ IMPLEMENTADO (salvo GARCH sin arch) y las 21 V5.0 dentro",
          serv | ({"VOL-GARCH-001"} if not S.garch_disponible() else set()) == impl and set(V50) <= serv,
          f"{len(serv)} servibles · {len(impl)} IMPLEMENTADO")
estados = {f: servir(mo, f)["estado"] for f in V50}
C.informe("Motor: las 21 V5.0 se sirven por CT-09 con su primer caso", all(e != "RECHAZADO" for e in estados.values()),
          str({f: e for f, e in estados.items() if e == "RECHAZADO"}))

mo = motor_en(raiz_con(degradar(TXT, "DER-VRP-001").encode()))
r = servir(mo, "DER-VRP-001")
C.informe("tabla del §4 con DER-VRP-001 en Documentado → RECHAZADO METODO_NO_IMPLEMENTADO, detalle con la madurez",
          r["estado"] == "RECHAZADO" and r["motivo"] == "METODO_NO_IMPLEMENTADO" and "Documentado" in r["detalle"]
          and servibles(mo) == serv - {"DER-VRP-001"}, f"{r['estado']} · {r.get('detalle', '')[:120]}")
rc = [e for e in mo.almacen.leer("RC") if e.get("operacion", {}).get("ficha_id") == "DER-VRP-001"]
C.informe("…y el rechazo queda en RC", bool(rc) and rc[-1]["tipo_entrada"] == "RECHAZO")

solo_ficha = re.sub(r"(### DER-VRP-001 ·.*?\*\*Prioridad y madurez\.\*\* P\d · )IMPLEMENTADO[^\n]*", r"\1Documentado.", TXT,
                    count=1, flags=re.S)
mo = motor_en(raiz_con(solo_ficha.encode()))
print(f"      (informativo) DER-VRP-001 en Documentado solo en su ficha (tabla del §4 en IMPLEMENTADO): "
      f"{'se sirve' if 'DER-VRP-001' in servibles(mo) else 'no se sirve'}; manda la tabla del §4")

i4, i5 = TXT.index("\n## 4."), TXT.index("\n## 5.")
for nombre, contenido, carpeta in (
        ("sin cabecera «## 5.»", (TXT[:i5] + TXT[i5:].replace("\n## 5.", "\n## Cinco.", 1)).encode(), False),
        ("bytes no UTF-8 dentro del §4", ORIG[:i4 + 500] + b"\xff\xfe" + ORIG[i4 + 500:], False),
        ("vacío", b"", False), ("ausente", None, False), ("una carpeta en lugar del archivo", None, True)):
    try:
        mo = motor_en(raiz_con(contenido, carpeta))
        n, e = len(servibles(mo)), servir(mo, "MON-YLD-001")["estado"]
        C.informe(f"Catálogo {nombre}: nada servible, RECHAZADO y sin excepción", n == 0 and e == "RECHAZADO", f"{n} servibles · {e}")
    except Exception as exc:  # noqa: BLE001
        C.informe(f"Catálogo {nombre}: nada servible, RECHAZADO y sin excepción", False, f"{type(exc).__name__}: {exc}"[:160])

fila_falsa = "\n| MON-YLD-001 | x | MC-01 | x | x | P1 | Documentado |\n"
for donde, txt in (("en el §1", TXT.replace("\n## 2.", fila_falsa + "\n## 2.", 1)),
                   ("en el §5", TXT.replace("\n## 6.", fila_falsa + "\n## 6.", 1))):
    mo = motor_en(raiz_con(txt.encode()))
    C.informe(f"fila falsa de MON-YLD-001 en Documentado {donde}: no manda (solo la tabla del §4)", "MON-YLD-001" in servibles(mo))

# Relectura en caliente
d = raiz_con(ORIG)
mo = motor_en(d)
p = d / S.RUTA_CATALOGO[0] / S.RUTA_CATALOGO[1]
antes = "IDX-CONC-001" in servibles(mo)
st = p.stat()
p.write_bytes(degradar(TXT, "IDX-CONC-001").encode())
os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000))
C.informe("Catálogo cambiado en caliente (otra fecha de modificación): el Motor lo ve sin reiniciar",
          antes and "IDX-CONC-001" not in servibles(mo) and servir(mo, "IDX-CONC-001")["estado"] == "RECHAZADO")
p.write_bytes(ORIG)
os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000))   # misma fecha que la versión degradada
print(f"      (informativo) cambio que conserva la fecha de modificación (p. ej., copia con `cp -p`): "
      f"{'se ve' if 'IDX-CONC-001' in servibles(mo) else 'NO se ve (caché por ruta y mtime_ns)'}")
cache = S._madurez.cache_info()
print(f"      (informativo) caché de la madurez: {cache}")

# Ejecutor movido con rutas.raiz_paquete, a través del Motor
movido = TMP / "movido"
shutil.copytree(M["ejec"], movido / "11_Ejecutor", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"))
codigo = f"""
import sys, tempfile; sys.path.insert(0, {str(movido / '11_Ejecutor')!r})
from pathlib import Path
from bloque_a.configuracion import cargar_config
from bloque_a.almacen import Almacen
from bloque_a.motor import servicio as S
assert Path(S.__file__).resolve().is_relative_to(Path({str(movido)!r}).resolve())
class P:
    as_of = None; nombre = "qa"
cfg = cargar_config(); cfg.setdefault("rutas", {{}})["raiz_paquete"] = {str(RAIZ / 'bloque_a')!r}
mo = S.Motor(Almacen(Path(tempfile.mkdtemp(dir={str(TMP)!r}))), P(), cfg)
print("servibles:", sum(1 for f in S.IMPLEMENTADAS if S.servible(f, mo.raiz)))
c = S.CASOS_CONTROL["MON-YLD-001"][0]
print("estado:", mo.servir({{"operacion": "MON-YLD-001", "datos": c["datos"], "parametros": c.get("parametros") or {{}}}}, "AG-21")["estado"])
"""
out = subprocess.run([sys.executable, "-I", "-B", "-c", codigo], capture_output=True, text=True, timeout=300, cwd=str(TMP))
m = re.search(r"servibles: (\d+)", out.stdout)
C.informe("ejecutor movido + rutas.raiz_paquete: el Motor sirve lo IMPLEMENTADO (H-04)",
          bool(m) and int(m.group(1)) == len(serv) and "estado: SERV" in out.stdout,
          out.stdout.strip().replace("\n", " | ") or out.stderr[-300:])

# ------------------------------------------------------------------ 2. RC: casos de control
mo = motor_en(RAIZ / "bloque_a")
res = mo.verificar_casos_control(run_id="QA-R02")
rc = [e for e in mo.almacen.leer("RC") if e.get("tipo_entrada") == "CASOS_CONTROL"]
n_casos = sum(len(v) for v in S.CASOS_CONTROL.values())
C.informe("verificar_casos_control: 21 fichas, 66 casos, todos superados", len(res) == 21 and n_casos == 66
          and sum(len(r["casos"]) for r in res.values()) == 66 and all(r["superados"] for r in res.values()),
          f"{n_casos} casos; por ficha {dict(Counter({f: len(v) for f, v in S.CASOS_CONTROL.items()}))}")
C.informe("RC: 21 entradas CASOS_CONTROL, una por ficha, con sus casos, estado SERVED, la madurez y CT-10",
          len(rc) == 21 and sorted(e["operacion"]["ficha_id"] for e in rc) == V50
          and all(len(e["casos_control"]) == len(S.CASOS_CONTROL[e["operacion"]["ficha_id"]]) and e["estado"] == "SERVED"
                  and str(e["madurez_catalogo"]).startswith("IMPLEMENTADO") and e["contrato"] == "CT-10" for e in rc))
C.informe("RC: calc_id únicos y run_id registrado", len({e["calc_id"] for e in rc}) == 21 and all(e["run_id"] == "QA-R02" for e in rc))
C.informe("RC íntegro tras escribir (verificar_integridad)", mo.almacen.verificar_integridad("RC").get("RC") is True)
res2 = mo.verificar_casos_control(run_id="QA-R02")
C.informe("repetir verificar_casos_control: mismos resultados (salvo calc_id)",
          {f: [c["superado"] for c in r["casos"]] for f, r in res.items()} == {f: [c["superado"] for c in r["casos"]] for f, r in res2.items()})
raro = mo.verificar_casos_control(["XYZ-NADA-001", "ACC-MOM-001"], run_id="QA-R02")
C.informe("ficha desconocida o sin casos de control: REJECTED registrado (no se supera en vacío)",
          not raro["XYZ-NADA-001"]["superados"] and not raro["ACC-MOM-001"]["superados"])
# un caso que falla (comprobación alterada en memoria) se registra como no superado
caso = S.CASOS_CONTROL["MON-YLD-001"][0]
orig_c = caso["comprobar"]
caso["comprobar"] = lambda r: False
try:
    malo = mo.verificar_casos_control(["MON-YLD-001"], run_id="QA-R02")["MON-YLD-001"]
finally:
    caso["comprobar"] = orig_c
ult = [e for e in mo.almacen.leer("RC") if e.get("tipo_entrada") == "CASOS_CONTROL"][-1]
C.informe("un caso que no se supera: REJECTED en RC con el caso marcado", not malo["superados"] and ult["estado"] == "REJECTED"
          and ult["casos_control"][0]["superado"] is False)

# ------------------------------------------------------------------ 3. Promoción y corpus
filas = re.findall(r"^\| ([A-Z]+(?:-[A-Z0-9]+)+-\d{3}) \|.*\| P\d \| ([^|]+?) \|\s*$", TXT[i4:i5], re.M)
cnt = Counter("impl" if v.startswith("IMPLEMENTADO") else "her" if v.startswith("Implementado") else
              "doc" if v.startswith("Documentado") else v for _, v in filas)
sec13 = re.search(r"Estado actual de las (\d+) fichas: (\d+) \*\*IMPLEMENTADO\*\* \((\d+) del ejecutor V1\.0.*?y (\d+) con casos de "
                  r"control registrados, T-106\); (\d+) heredadas.*?; (\d+) \*\*DOCUMENTADO\*\*", TXT)
C.informe("§1.3 = tabla del §4: 81 = 35 (14 + 21) + 11 + 35", bool(sec13) and [int(x) for x in sec13.groups()] ==
          [len(filas), cnt["impl"], cnt["impl"] - 21, 21, cnt["her"], cnt["doc"]] == [81, 35, 14, 21, 11, 35],
          f"{sec13.groups() if sec13 else None} · {dict(cnt)}")
mal = []
for fid in V50:
    fila = dict(filas).get(fid, "")
    mm = re.search(rf"^### {re.escape(fid)} ·.*?\*\*Prioridad y madurez\.\*\* (P\d) · ([^\n]+)", TXT, re.M | re.S)
    if not (fila.startswith("IMPLEMENTADO") and mm and mm.group(2).startswith("IMPLEMENTADO") and "T-106" in fila):
        mal.append(fid)
C.informe("las 21 en IMPLEMENTADO en la tabla del §4 y en su ficha", not mal, str(mal))
codigo_sin_impl = sorted(f for f in S.IMPLEMENTADAS if f not in impl and f not in S.DOCUMENTADAS_CON_CODIGO)
C.informe("ninguna ficha con código fuera de DOCUMENTADAS_CON_CODIGO queda sin IMPLEMENTADO", not codigo_sin_impl, str(codigo_sin_impl))
git = ["git", "-C", str(RAIZ)]
dif = subprocess.run(git + ["diff", "--stat", "7064f60", "HEAD", "--", str(CAT.relative_to(RAIZ))], capture_output=True, text=True)
C.informe("Catálogo sin cambios desde la r01 (7064f60): la r02 no lo toca", dif.returncode == 0 and not dif.stdout.strip(), dif.stdout[:120])
man = (RAIZ / "tools" / "corpus_manifest.txt").read_text(encoding="utf-8")
linea = next((x for x in man.splitlines() if str(CAT.relative_to(RAIZ)) in x), "")
C.informe("manifiesto del corpus con la huella actual del Catálogo", hashlib.sha256(ORIG).hexdigest() in linea)
docx = subprocess.run(git + ["diff", "--name-only", "1b8c699", "HEAD", "--", "*.docx"], capture_output=True, text=True)
C.informe("ningún .docx tocado desde antes de T-106", not docx.stdout.strip(), docx.stdout[:200])

shutil.rmtree(TMP, ignore_errors=True)
sys.exit(C.resumen())
