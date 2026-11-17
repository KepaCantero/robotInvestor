"""QA r01 de T-169 (revisor) · `enviar_pendientes` entre procesos y `ciclo`/`consulta` frente a T-162 (`3533cb7`, HEAD~1).

Uso, desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-169/revisores/r01_02_procesos_y_base.py <trabajo> <bloque_a de HEAD~1>
  <trabajo>: carpeta desechable (se crea); <bloque_a de HEAD~1>: extracción de `git archive HEAD~1 bloque_a`.
Cada escenario corre en un proceso hijo con `-I`. Imprime OK / FALLO / ANOTADO por comprobación y termina con 1 si alguna FALLA.
Sin red ni coste.
"""
import json
import subprocess
import sys
import textwrap
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
PY = str(RAIZ / ".venv" / "bin" / "python")
HEAD = RAIZ / "bloque_a" / "11_Ejecutor"
TRABAJO = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve() / "11_Ejecutor"
TRABAJO.mkdir(parents=True, exist_ok=True)
fallos = 0

PREAMBULO = textwrap.dedent('''
    import copy, json, os, sys, time
    EJ = sys.argv[1]
    sys.path.insert(0, EJ + "/tests"); sys.path.insert(0, EJ)
    from pathlib import Path
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config
    from bloque_a.herramientas.ht01_datos import cargar_universo, ProveedorCSV
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque
    from conftest import AS_OF, DATOS, config_pruebas
    U = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    def bloque(tmp, cfg=None):
        return Bloque(cfg or config_pruebas(), ProveedorCSV(DATOS), U, MockClient(), Path(tmp) / "estado", Path(tmp) / "ent")
    def div(tmp):
        return bloque(tmp, cargar_config(extra={"modo": "backtest"}))
    def espiar(b):
        vistos = []
        crear = b.mensajeria.crear
        def f(*a, **k):
            m = crear(*a, **k); vistos.append(copy.deepcopy(m)); return m
        b.mensajeria.crear = f
        return vistos
    PB07 = "¿Qué opinas de la renta variable india frente a la indonesia a 6 meses?"
    ORO = "¿Qué opinas del oro frente a la plata a 6 meses?"
    def salida(x):
        print("@@" + json.dumps(x, ensure_ascii=False, sort_keys=True, default=str))
    def limpio(e):
        fuera = ("_ts", "_hash", "_hash_prev", "fecha_respuesta", "timestamp", "fecha_entrega")
        out = {k: v for k, v in e.items() if k not in fuera}
        if isinstance(out.get("respuesta_final"), dict) and "timestamp" in out["respuesta_final"]:   # la final guardada en F5
            out["respuesta_final"] = {k: v for k, v in out["respuesta_final"].items() if k != "timestamp"}
        return out
    def volcado(b, ms):
        f = {a: [limpio(e) for e in b.almacen.leer(a)] for a in ("F1", "F2", "F3", "F4", "F5", "F6", "F10", "F11", "RC", "HA")}
        texto = json.dumps({"mensajes": [limpio(m) for m in ms], "f": f}, ensure_ascii=False, default=str)
        return json.loads(texto.replace(str(Path(sys.argv[2]).resolve()), "<TRABAJO>"))   # las rutas de los entregables
''')


def hijo(codigo: str, ejecutor: Path, *args, esperado=0):
    r = subprocess.run([PY, "-I", "-c", PREAMBULO + textwrap.dedent(codigo), str(ejecutor), *map(str, args)],
                       capture_output=True, text=True, timeout=3000, check=False)
    if r.returncode != esperado:
        print(r.stdout[-2000:], r.stderr[-3000:])
    return r.returncode, [json.loads(x[2:]) for x in r.stdout.splitlines() if x.startswith("@@")]


def comprobar(nombre, cond, detalle=""):
    global fallos
    print(("OK     " if cond else "FALLO  ") + nombre + (f" · {detalle}" if detalle else ""), flush=True)
    fallos += 0 if cond else 1


def anotar(nombre, detalle):
    print("ANOTADO " + nombre + " · " + detalle, flush=True)


def a_la_vez(codigo, n, carpeta, *args):
    marca = carpeta / "ya"
    if marca.exists():
        marca.unlink()
    procs = [subprocess.Popen([PY, "-I", "-c", PREAMBULO + textwrap.dedent(codigo), str(HEAD), str(carpeta), str(marca), *args],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(n)]
    time.sleep(20)
    marca.write_text("ya")
    res = []
    for p in procs:
        out, err = p.communicate(timeout=900)
        res += [json.loads(x[2:]) for x in out.splitlines() if x.startswith("@@")]
        if p.returncode:
            print(err[-2000:])
    return res


# ---------------------------------------------------------------- 1 · enviar_pendientes en 4 procesos a la vez
PREPARA = '''
    from bloque_a import respuesta_final
    b = div(sys.argv[2])
    respuesta_final.enviar = lambda *a, **k: None
    q = b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)
    if len(sys.argv) > 3:   # una pendiente que la mensajería rechaza (R8 en la clase del fallo guardada)
        esc = b.almacen.estado("F5", clave="id")[q["query_id"]]["escalado"]
        b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "QRY", "id": q["query_id"], "fallo_analisis": "de luis.qa169@ejemplo.com",
                                           "escalado": {**esc, "estado_run": "FALLIDO"}})
    salida({"qry": q["query_id"], "pend": respuesta_final.pendientes(b.almacen)})
'''
UNO = '''
    from bloque_a import respuesta_final
    b = div(sys.argv[2])
    ms = espiar(b)
    while not Path(sys.argv[3]).exists():
        time.sleep(0.01)
    r = respuesta_final.enviar_pendientes(b, AS_OF)
    salida({"enviadas": [(x["msg_id"], x["repetido"]) for x in r],
            "finales": len([m for m in ms if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO"])})
'''
CUENTA = '''
    b = div(sys.argv[2])
    q = sys.argv[3]
    f5 = [e for e in b.almacen.leer("F5") if e.get("id") == q]
    salida({"finales": len([e for e in f5 if e.get("respuesta_final")]), "apartadas": len([e for e in f5 if e.get("final_no_enviable")]),
            "inc": len([e for e in b.almacen.leer("HA") if q in e.get("detalle", "") and "apartada" in e.get("detalle", "")]),
            "correo_en_ha": "luis.qa169" in json.dumps(b.almacen.leer("HA")), "integridad": b.almacen.verificar_integridad()})
'''
for caso, extra in (("enviable", ()), ("rechazada", ("r8",))):
    carpeta = TRABAJO / f"procesos_{caso}"
    _, d = hijo(PREPARA, HEAD, carpeta, *extra)
    qry = d[0]["qry"]
    res = a_la_vez(UNO, 4, carpeta)
    _, c = hijo(CUENTA, HEAD, carpeta, qry)
    c = c[0]
    if caso == "enviable":
        comprobar("procesos · 4 a la vez con una pendiente enviable: un solo mensaje y una sola final en F5",
                  sum(x["finales"] for x in res) == 1 and c["finales"] == 1 and all(c["integridad"].values()), str(res))
    else:
        anotar("procesos · 4 a la vez con una pendiente rechazada (R8)", json.dumps(c, ensure_ascii=False))
        comprobar("procesos · la rechazada no sale, no copia el correo y el almacén queda íntegro",
                  sum(x["finales"] for x in res) == 0 and c["finales"] == 0 and not c["correo_en_ha"] and all(c["integridad"].values()))
        comprobar("procesos · la rechazada se aparta una sola vez (H-03 de esta QA si falla)", c["apartadas"] == 1 and c["inc"] == 1,
                  f"{c['apartadas']} apartados, {c['inc']} incidencias")

# ---------------------------------------------------------------- 2 · sin pendientes, ciclo y consulta iguales que en HEAD~1
CICLO = '''
    b = bloque(sys.argv[2])
    ms = espiar(b)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    salida(volcado(b, ms))
'''
CONSULTA = '''
    b = bloque(sys.argv[2])
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ms = espiar(b)
    q = b.consulta(PB07, as_of=AS_OF)
    salida(volcado(b, ms))
'''
for nombre, codigo in (("ciclo RV", CICLO), ("ciclo RV y consulta escalada PB-07", CONSULTA)):
    _, h = hijo(codigo, HEAD, TRABAJO / f"head_{len(codigo)}")
    _, b0 = hijo(codigo, BASE, TRABAJO / f"base_{len(codigo)}")
    h, b0 = h[0], b0[0]
    if codigo is CICLO:
        comprobar(f"HEAD~1 · {nombre}: mensajes iguales", h["mensajes"] == b0["mensajes"], f"{len(h['mensajes'])} mensajes")
        distintos = [a for a in h["f"] if h["f"][a] != b0["f"][a]]
        comprobar(f"HEAD~1 · {nombre}: F1–F11, RC y HA iguales", not distintos, str(distintos))
    else:
        comprobar(f"HEAD~1 · {nombre}: mensajes iguales", h["mensajes"] == b0["mensajes"], f"{len(h['mensajes'])} mensajes")
        distintos = [a for a in h["f"] if a != "F5" and h["f"][a] != b0["f"][a]]
        comprobar(f"HEAD~1 · {nombre}: todo igual salvo F5", not distintos, str(distintos))
        f5h = [e for e in h["f"]["F5"] if not e.get("provisional_msg_id")]
        f5b = b0["f"]["F5"]
        quitar_seq = [{k: v for k, v in e.items() if k != "_seq"} for e in f5h]
        comprobar(f"HEAD~1 · {nombre}: F5 solo añade el registro de la provisional",
                  quitar_seq == [{k: v for k, v in e.items() if k != "_seq"} for e in f5b]
                  and len(h["f"]["F5"]) == len(f5b) + 1, f"{len(h['f']['F5'])} frente a {len(f5b)}")

print("fallos:", fallos)
sys.exit(1 if fallos else 0)
