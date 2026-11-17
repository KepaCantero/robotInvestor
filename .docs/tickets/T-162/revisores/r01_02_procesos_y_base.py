"""QA r01 de T-162 (revisor) · procesos, reinicio a mitad, determinismo entre procesos y comparación con la base (f2b3ad4).

Uso, desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-162/revisores/r01_02_procesos_y_base.py <trabajo> [<bloque_a de la base>]
  <trabajo>: carpeta desechable (se crea); <bloque_a de la base>: extracción de `git archive f2b3ad4 bloque_a` (opcional;
  sin ella no se hacen las comparaciones con la base).
Cada escenario corre en un proceso hijo con `-I` y el paquete que toca en `sys.path`. Imprime una línea por comprobación
(OK / FALLO / ANOTADO) y termina con 1 si alguna FALLA. Sin red ni coste.
"""
import json
import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
PY = str(RAIZ / ".venv" / "bin" / "python")
HEAD = RAIZ / "bloque_a" / "11_Ejecutor"
TRABAJO = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve() / "11_Ejecutor" if len(sys.argv) > 2 else None
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
''')


def hijo(codigo: str, ejecutor: Path, *args, env=None, esperado=0):
    r = subprocess.run([PY, "-I", "-c", PREAMBULO + textwrap.dedent(codigo), str(ejecutor), *map(str, args)],
                       capture_output=True, text=True, check=False, env={**os.environ, **(env or {})}, timeout=3000)
    datos = [json.loads(x[2:]) for x in r.stdout.splitlines() if x.startswith("@@")]
    if r.returncode != esperado:
        print(r.stdout[-3000:], r.stderr[-3000:])
    return r.returncode, datos, r.stderr


def comprobar(nombre, cond, detalle=""):
    global fallos
    print(("OK     " if cond else "FALLO  ") + nombre + (f" · {detalle}" if detalle else ""))
    fallos += 0 if cond else 1


def anotar(nombre, detalle):
    print("ANOTADO " + nombre + " · " + detalle)


# ---------------------------------------------------------------- 1 · determinismo entre procesos (ENTREGADO, RV)
ESCENARIO_PB07 = '''
    b = bloque(sys.argv[2])
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ms = espiar(b)
    q = b.consulta(PB07, as_of=AS_OF)
    salida({"ct03": [m for m in ms if m["contrato"] == "CT-03"], "f5": [{k: v for k, v in e.items() if k not in ("_ts", "_hash", "_hash_prev")}
            for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY"], "q": {k: v for k, v in q.items() if k != "consumo"}})
'''
salidas = []
for n, semilla in enumerate(("1", "4242")):
    rc, d, _ = hijo(ESCENARIO_PB07, HEAD, TRABAJO / f"det{n}", env={"PYTHONHASHSEED": semilla})
    salidas.append(d[0] if d else None)
comprobar("determinismo: dos procesos (con -I, semilla de hash aleatoria en cada uno), CT-03 y F5 iguales byte a byte",
          salidas[0] is not None and json.dumps(salidas[0]["ct03"], sort_keys=True) == json.dumps(salidas[1]["ct03"], sort_keys=True)
          and json.dumps(salidas[0]["f5"], sort_keys=True) == json.dumps(salidas[1]["f5"], sort_keys=True))
fin = salidas[0]["q"]["respuesta_final"] if salidas[0] else {}
comprobar("determinismo: la final es ENTREGADO con referencias", fin.get("respuesta_final", {}).get("resultado_analisis") == "ENTREGADO"
          and len(fin.get("referencias", [])) > 1, f"{len(fin.get('referencias', []))} referencias")

# ---------------------------------------------------------------- 2 · reinicio a mitad: el proceso muere tras la provisional
MUERE = '''
    from bloque_a import respuesta_final
    b = bloque(sys.argv[2], cfg=cargar_config(extra={"modo": "backtest"}))
    ms = espiar(b)
    def morir(*a, **k):
        salida({"provisional": [m for m in ms if m["contrato"] == "CT-03" and m["tipo_mensaje"] == "RETORNO"]})
        sys.stdout.flush(); os._exit(9)
    respuesta_final.enviar = morir
    b.consulta(ORO, as_of=AS_OF)
'''
rc, d, _ = hijo(MUERE, HEAD, TRABAJO / "reinicio", esperado=9)
prov = d[0]["provisional"][0] if d else {}
comprobar("reinicio: el proceso muere justo después de crear la provisional", rc == 9 and prov.get("msg_id", "").startswith("MSG-"))
TRAS_REINICIO = '''
    from bloque_a import respuesta_final
    b = bloque(sys.argv[2], cfg=cargar_config(extra={"modo": "backtest"}))
    q = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY"]
    texto_f5 = json.dumps(q, ensure_ascii=False)
    out = {"n_qry": len(q), "con_final": any(e.get("respuesta_final") for e in q), "msg_prov_en_f5": sys.argv[3] in texto_f5,
           "integridad": b.almacen.verificar_integridad()}
    # ¿se puede enviar la final después del reinicio? (con el msg_id verdadero y con uno inventado)
    fin = respuesta_final.enviar(b, q[0]["id"], "MSG-2026-999999", AS_OF)
    out["inventado_aceptado"] = fin["respuesta_final"]["provisional_msg_id"]
    out["resultado"] = fin["respuesta_final"]["resultado_analisis"]
    salida(out)
'''
rc, d, _ = hijo(TRAS_REINICIO, HEAD, TRABAJO / "reinicio", prov.get("msg_id", "MSG-x"))
r = d[0] if d else {}
comprobar("reinicio: el almacén queda íntegro y con la QRY sin final", rc == 0 and all(r.get("integridad", {}).values())
          and r.get("n_qry") == 1 and not r.get("con_final"))
anotar("reinicio: F5 guarda el msg_id de la provisional", str(r.get("msg_prov_en_f5")))
anotar("reinicio: `enviar` acepta un provisional_msg_id inventado", f"{r.get('inventado_aceptado')} → {r.get('resultado')}")

# ---------------------------------------------------------------- 3 · idempotencia entre procesos (4 a la vez) y tras reiniciar
PREPARA = '''
    from bloque_a import respuesta_final
    b = bloque(sys.argv[2], cfg=cargar_config(extra={"modo": "backtest"}))
    respuesta_final.enviar = lambda *a, **k: None
    q = b.consulta(ORO, as_of=AS_OF)
    salida({"qry": q["query_id"], "msg": q["msg_id"]})
'''
rc, d, _ = hijo(PREPARA, HEAD, TRABAJO / "procesos")
qry, msg = d[0]["qry"], d[0]["msg"]
UNO = '''
    from bloque_a import respuesta_final
    b = bloque(sys.argv[2], cfg=cargar_config(extra={"modo": "backtest"}))
    marca = Path(sys.argv[5])
    while not marca.exists():
        time.sleep(0.01)
    fin = respuesta_final.enviar(b, sys.argv[3], sys.argv[4], AS_OF)
    salida({"repetido": fin["repetido"], "msg_id": fin["msg_id"]})
'''
marca = TRABAJO / "procesos" / "ya"
if marca.exists():
    marca.unlink()
procs = [subprocess.Popen([PY, "-I", "-c", PREAMBULO + textwrap.dedent(UNO), str(HEAD), str(TRABAJO / "procesos"), qry, msg, str(marca)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(4)]
time.sleep(25)   # los cuatro abren el almacén antes de la señal
marca.write_text("ya")
res = []
for p in procs:
    out, err = p.communicate(timeout=600)
    res += [json.loads(x[2:]) for x in out.splitlines() if x.startswith("@@")]
    if p.returncode:
        print(err[-2000:])
CUENTA = '''
    b = bloque(sys.argv[2], cfg=cargar_config(extra={"modo": "backtest"}))
    from bloque_a import respuesta_final
    fin = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "QRY" and e.get("id") == sys.argv[3] and e.get("respuesta_final")]
    otra = respuesta_final.enviar(b, sys.argv[3], sys.argv[4], AS_OF)
    salida({"finales": len(fin), "tras_reinicio_repetido": otra["repetido"], "integridad": b.almacen.verificar_integridad()})
'''
rc, d, _ = hijo(CUENTA, HEAD, TRABAJO / "procesos", qry, msg)
c = d[0] if d else {}
comprobar("procesos: 4 a la vez → una sola final nueva, el resto repetida, mismo msg_id",
          sorted(x["repetido"] for x in res) == [False, True, True, True] and len({x["msg_id"] for x in res}) == 1, str(res))
comprobar("procesos: una sola entrada de la final en F5; tras reiniciar, `repetido`; almacén íntegro",
          c.get("finales") == 1 and c.get("tras_reinicio_repetido") is True and all(c.get("integridad", {}).values()))

# ---------------------------------------------------------------- 4 · el try/except: un fallo de integridad a mitad del RUN-
INTEGRIDAD = '''
    b = bloque(sys.argv[2])
    # sello de F2 manipulado con el bloque ya abierto (otro proceso, o un disco que se corrompe): la consulta lee F1–F6
    # (las firmas de los ficheros no cambian) y el primer `escribir` de F2, dentro del RUN-, falla la integridad
    ruta = b.almacen._ruta_sellos
    sellos = json.loads(ruta.read_text())
    sellos["F2"] = [999, "0" * 64]
    ruta.write_text(json.dumps(sellos))
    ms = espiar(b)
    try:
        q = b.consulta(PB07, as_of=AS_OF)
    except Exception as e:
        salida({"excepcion": type(e).__name__, "texto": str(e)[:120]}); sys.exit(0)
    ha = [e for e in b.almacen.leer("HA") if e.get("tipo") in ("HERRAMIENTA", "INTEGRIDAD", "SEGURIDAD", "OTRO")]
    salida({"excepcion": None, "final": q["respuesta_final"]["respuesta_final"], "estado_run": q["escalado"]["estado_run"],
            "ha": [(e["tipo"], e["detalle"], e.get("escalado_operador")) for e in ha],
            "ct03": len([m for m in ms if m["contrato"] == "CT-03"])})
'''
rc, d, _ = hijo(INTEGRIDAD, HEAD, TRABAJO / "integridad_head")
h = d[0] if d else {}
anotar("integridad (T-162): la consulta", json.dumps(h, ensure_ascii=False))
if BASE:
    rc, d, _ = hijo(INTEGRIDAD.replace('q["respuesta_final"]["respuesta_final"]', 'None'), BASE, TRABAJO / "integridad_base")
    anotar("integridad (base f2b3ad4): la consulta", json.dumps(d[0] if d else {}, ensure_ascii=False))

# ---------------------------------------------------------------- 5 · con la base: provisional y --sin-escalado iguales
if BASE:
    for i, (nombre, codigo) in enumerate((("escala (PB-07, RV)", ESCENARIO_PB07),
                           ("sin escalado (oro)", ESCENARIO_PB07.replace('    b.ciclo(AS_OF, alcance={"clases": ["RV"]})\n', '')
                            .replace("b.consulta(PB07, as_of=AS_OF)", "b.consulta(ORO, as_of=AS_OF, ejecutar_escalado=False)")))):
        _, dh, _ = hijo(codigo, HEAD, TRABAJO / f"cmp_head_{i}")
        _, db, _ = hijo(codigo, BASE, TRABAJO / f"cmp_base_{i}")
        h, b0 = dh[0], db[0]
        prov_h = [m for m in h["ct03"] if m["tipo_mensaje"] == "RETORNO"]
        prov_b = [m for m in b0["ct03"] if m["tipo_mensaje"] == "RETORNO"]
        comprobar(f"base · {nombre}: la provisional y el encargo CT-03 son iguales byte a byte",
                  len(prov_b) == 1 and len(prov_h) == 2 and json.dumps(prov_h[0], sort_keys=True) == json.dumps(prov_b[0], sort_keys=True)
                  and [m for m in h["ct03"] if m["tipo_mensaje"] == "ENCARGO"] == [m for m in b0["ct03"] if m["tipo_mensaje"] == "ENCARGO"])
        comprobar(f"base · {nombre}: la primera entrada QRY de F5 es igual (salvo la hora)",
                  [{k: v for k, v in e.items() if k not in ("_hash", "_hash_prev", "fecha_respuesta")} for e in h["f5"][:1]]
                  == [{k: v for k, v in e.items() if k not in ("_hash", "_hash_prev", "fecha_respuesta")} for e in b0["f5"]])
        sin_final = {k: v for k, v in h["q"].items() if k != "respuesta_final"}
        comprobar(f"base · {nombre}: lo que devuelve `consulta` es igual salvo `respuesta_final`", sin_final == b0["q"],
                  str(sorted(set(h["q"]) ^ set(b0["q"]))))

print("fallos:", fallos)
sys.exit(1 if fallos else 0)
