"""r01 (QA T-79): el panel de la V0.64 y Reloj.estado() por caminos que no cubren pruebas_consola_sistema.py ni la sonda
r01_panel_v064.py de Claude. Cada línea «HALLAZGO» es un comportamiento que no falla cerrado o no dice la verdad.

Uso: python3 -I r01_panel_otros_caminos.py <carpeta marco_comun_c> <carpeta temporal vacía>
"""
import copy
import hashlib
import json
import os
import sys
from pathlib import Path

M, TMP = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(M / "validador"))
sys.path.insert(0, str(M / "pruebas"))
import diario as di  # noqa: E402
import migraciones as mg  # noqa: E402
from consola import panel  # noqa: E402
from parametros import PARAMETROS  # noqa: E402
from pruebas_consola_sistema import nuevo_diario, nuevo_reloj  # noqa: E402
from pruebas_orquestador import AHORA, hasta, nuevo  # noqa: E402

res = []


def chk(nombre, cond, detalle=""):
    res.append(cond)
    print(("OK       " if cond else "HALLAZGO ") + nombre + ("" if cond else f"  -> {detalle}"))


def linea(p, que):
    return next((x for x in p["comprobaciones"] if x["que"] == que), None)


def foto_reloj(r):
    return copy.deepcopy({k: v for k, v in vars(r).items() if not callable(v)})


def sha(ruta):
    return hashlib.sha256(Path(ruta).read_bytes()).hexdigest()


# 1. «degradadas» corrupta pero falsa (None, [], 0, ""): ¿pinta «autonomía plena» y el panel verde?
for malo in (None, [], 0, "", set()):
    o = nuevo()
    o.degradadas = malo
    p = panel(o, AHORA)
    chk(f"degradadas={malo!r}: el panel no sale VERDE", p["nivel"] != "VERDE", (p["nivel"], linea(p, "autonomia"), linea(p, "integridad")))
# (info) ¿un estado guardado con degradadas=None y la huella rehecha se carga? (la huella no es autenticidad: sin clave, sí)
import persistencia as pe  # noqa: E402
o = nuevo(); txt = pe.volcar(o, AHORA); dd = json.loads(txt); dd["estado"]["degradadas"] = None; dd["huella"] = pe._huella(dd["estado"])
c = pe.cargar(json.dumps(dd, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
if c["ok"]:
    try:
        c["orquestador"].nivel("TACTICA"); nv = "sin excepción"
    except Exception as ex:   # noqa: BLE001
        nv = type(ex).__name__
    print(f"         (info) estado con degradadas=None y huella rehecha: cargar ok; o.nivel() da {nv}; panel {panel(c['orquestador'], AHORA)['nivel']}")
else:
    print(f"         (info) estado con degradadas=None y huella rehecha: cargar {c['codigo']}")
# 1b. una cartera desconocida en degradadas
o = nuevo(); o.degradadas = {"INVENTADA": {"motivo": "x", "ahora": AHORA}}
p = panel(o, AHORA)
chk("degradadas con cartera inventada: el panel no sale VERDE", p["nivel"] != "VERDE", p["nivel"])

# 2. Reloj.estado() con registros corruptos: la foto nunca debe ser más optimista que el reloj
f, r = nuevo_reloj()
r.bloqueo = "RL-01 escrito a mano"
e = r.estado()
chk("estado() con bloqueo que no es dict: sigue diciendo bloqueado", e["bloqueo"] is not None, e)
chk("y el panel lo pinta ROJO", linea(panel(nuevo(), AHORA, reloj=r), "reloj")["nivel"] == "ROJO")
f, r = nuevo_reloj()
r.bloqueo = {"codigo": "RL-01", "motivo": "prueba"}
r.incidentes = None
e = r.estado()
chk("estado() bloqueado con incidentes ilegibles: sigue diciendo bloqueado", e["bloqueo"] is not None, e)
chk("y el panel lo pinta ROJO", linea(panel(nuevo(), AHORA, reloj=r), "reloj")["nivel"] == "ROJO")

# 3. monótono que retrocede respecto del contraste: ahora() lo bloquea (RL-01); ¿qué dice el panel antes?
f, r = nuevo_reloj()
f.pasa(5)
assert r.ahora()["ok"]
f.m -= 100   # el monótono vuelve atrás
l = linea(panel(nuevo(), AHORA, reloj=r), "reloj")
a = r.ahora()
chk("monótono hacia atrás: el panel no dice VERDE", l["nivel"] != "VERDE", l)
print(f"         (info) panel: {l['nivel']}; después ahora() da {a['codigo']}")

# 4. tolerancia del reloj tocada tras construirlo (NaN): ¿el panel y ahora() fallan abierto?
f, r = nuevo_reloj()
r.max_sin_contraste_s = float("nan")
f.pasa(10 * 24 * 3600)
l = linea(panel(nuevo(), AHORA, reloj=r), "reloj")
chk("tolerancia NaN y 10 días sin contraste: el panel no dice VERDE", l["nivel"] != "VERDE", l)
print(f"         (info) con la misma tolerancia ahora() da ok={r.ahora()['ok']} (mismo criterio que el panel)")

# 5. el panel no toca el reloj ni el diario ni sus ficheros, y es determinista con los dos
TMP.mkdir(parents=True, exist_ok=True)
o = nuevo(); hasta(o, "ABIERTA")
d = nuevo_diario(str(TMP / "d5"), o)
f, r = nuevo_reloj()
f.pasa(60)
antes_r, antes_n, antes_roto = foto_reloj(r), d._n, d._roto
antes_f = (sha(TMP / "d5" / "estado.json"), sha(TMP / "d5" / "diario"))
p1 = panel(d, AHORA, reloj=r, diario=d)
p2 = panel(d, AHORA, reloj=r, diario=d)
chk("panel con reloj y diario: determinista", json.dumps(p1, sort_keys=True) == json.dumps(p2, sort_keys=True))
chk("panel no muta el reloj (ni el suelo, ni la última lectura, ni incidentes)", foto_reloj(r) == antes_r)
chk("panel no muta el diario ni escribe en sus ficheros", (d._n, d._roto) == (antes_n, antes_roto)
    and (sha(TMP / "d5" / "estado.json"), sha(TMP / "d5" / "diario")) == antes_f)
p3 = panel(d.orquestador, AHORA, reloj=r, diario=d)
chk("panel sobre el Diario (proxy) = panel sobre su Orquestador", json.dumps(p1, sort_keys=True) == json.dumps(p3, sort_keys=True))

# 6. diario desincronizado: el Orquestador cambia sin pasar por el diario; la próxima operación del diario dará DI-06
o = nuevo()
d = nuevo_diario(str(TMP / "d6"), o)
assert d.orquestador.detectar("EXP-0005", "COR-0005", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]   # por fuera
l = linea(panel(d.orquestador, AHORA, diario=d), "diario")
sig = d.detectar("EXP-0006", "COR-0006", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)
chk("diario desincronizado por fuera: el panel no dice «diario operativo» VERDE", l["nivel"] != "VERDE",
    f"panel {l['nivel']} «{l['motivo']}»; la operación siguiente del diario da {sig['codigo']}")

# 7. el borde del tope con operaciones reales: con tope = _n, VERDE; con tope = _n - 1, ÁMBAR; y tras punto(), VERDE
o = nuevo()
d = nuevo_diario(str(TMP / "d7"), o)
for i in range(2):
    assert d.detectar(f"EXP-00{i+1:02d}", f"COR-00{i+1:02d}", "DISCRECIONAL", "TACTICA", "GESTOR_TACTICA", AHORA)["ok"]
n = d._n
lv = linea(panel(d, AHORA, diario=d, lineas_diario_ambar=n), "diario")
la = linea(panel(d, AHORA, diario=d, lineas_diario_ambar=n - 1), "diario")
chk(f"borde del tope ({n} líneas): tope {n} VERDE y tope {n - 1} ÁMBAR", lv["nivel"] == "VERDE" and la["nivel"] == "AMBAR", (lv, la))
assert d.punto(AHORA)["ok"]
chk("tras punto() vuelve a VERDE con tope 1", linea(panel(d, AHORA, diario=d, lineas_diario_ambar=1), "diario")["nivel"] == "VERDE")
for tope in (10 ** 30, 1):
    l = linea(panel(d, AHORA, diario=d, lineas_diario_ambar=tope), "diario")
    chk(f"tope {tope}: sin excepción y con nivel", l["nivel"] in ("VERDE", "AMBAR"), l)
chk("tope por defecto = PARAMETROS (1000) y PARAMETROS es de solo lectura",
    PARAMETROS["n_lineas_diario_ambar"] == 1000 and not hasattr(PARAMETROS, "__setitem__"))
try:
    PARAMETROS["n_lineas_diario_ambar"] = 1   # type: ignore[index]
    chk("PARAMETROS no se puede reescribir", False, "se dejó escribir")
except TypeError:
    chk("PARAMETROS no se puede reescribir", True)

# 8. migración real: línea VERDE; después cualquier otra entrada de límites la retira (por diseño)
viejo = (M / "pruebas" / "estados" / "estado_V0_52.json").read_text(encoding="ascii")
mr = mg.migrar(viejo, "2026-11-08T10:00:00+00:00", "QA T-79: migración para ver la línea del panel")
l = linea(panel(mr["orquestador"], "2026-11-08T10:00:00+00:00"), "migracion")
chk("tras migrar V0.52 -> V0.67 la línea dice MIG-004 y MIG-005", l is not None and l["nivel"] == "VERDE" and "MIG-004, MIG-005" in l["motivo"], l)
o = mr["orquestador"]
o.limites["entradas"][-1]["migraciones"] = ["MIG-004", 5]
l = linea(panel(o, "2026-11-08T10:00:00+00:00"), "migracion")
chk("una migración anotada con ids raros: ROJO y el panel lo ve (integridad o línea)", l is not None and l["nivel"] == "ROJO", l)

n = res.count(False)
print(f"\nRESULTADO r01 PANEL OTROS CAMINOS: {'SIN HALLAZGOS' if not n else f'{n} HALLAZGO(S)'}")
