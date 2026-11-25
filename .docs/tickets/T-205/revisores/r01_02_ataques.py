"""QA r01 de T-205 (revisor): ataques al rechazo de la clase en el alta (CT-24) y en el C6.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python -I <ruta>/r01_02_ataques.py <carpeta_temporal>
Imprime una línea PASA o FALLA por ataque y sale con 1 si alguno falla. Sin red: cliente simulado y datos sintéticos."""
import json
import shutil
import sys
from pathlib import Path

EJ = Path.cwd()
sys.path.insert(0, str(EJ))
sys.path.insert(0, str(EJ / "tests"))
from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.seguimiento import ClaseNoAdmitida  # noqa: E402

TMP = Path(sys.argv[1])
shutil.rmtree(TMP, ignore_errors=True)
TMP.mkdir(parents=True)
UNI = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
MARCA = "MARCA" + "_T205_" + "QA"   # valor de clase que no debe aparecer fuera de F3
fallos = []


def ok(nombre, cond, detalle=""):
    print(("PASA  " if cond else "FALLA ") + nombre + (f"  [{detalle}]" if detalle and not cond else ""), flush=True)
    if not cond:
        fallos.append(nombre)


# Base: un C1 de RV
base = TMP / "base"
b0 = nuevo_bloque(base, UNI)
r = b0.ciclo(AS_OF, alcance={"clases": ["RV"]})
OPPS = [o["opp_id"] for o in r["paquete"]["clases"]["RV"]["opciones"]]
n = [0]


def copia():
    n[0] += 1
    d = TMP / f"c{n[0]:02d}"
    for c in ("estado", "ent"):
        if (base / c).exists():
            shutil.copytree(base / c, d / c)
    b = nuevo_bloque(d, UNI)
    msgs = []
    crear = b.mensajeria.crear

    def espia(*a, **k):
        m = crear(*a, **k)
        msgs.append(m)
        return m
    b.mensajeria.crear = espia
    return b, msgs, d


def poner(b, opp, valor, fecha=AS_OF, **extra):
    b.fijar_fecha(fecha)
    b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": opp, "clase": valor, **extra})


def alta(b, opp, fecha=AS_OF):
    return b.seguimientos.procesar({"accion": "ALTA", "opp_id": opp, "frecuencia": "SEMANAL", "motivo": "qa"}, fecha)


def incs(b):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and e.get("campo_afectado") == "clase"]


def foto(b):
    return {p.name: p.read_bytes() for p in sorted(b.almacen.carpeta.iterdir()) if p.is_file() and p.suffix in (".jsonl", ".json")}


def apariciones(d, marca):
    """Ficheros (bajo la copia) que contienen la marca, salvo F3."""
    return sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file() and marca.encode() in p.read_bytes()
                  and not p.name.startswith("F3_"))


# A1: valores hostiles de la clase en F3 → alta rechazada con un INC- y nada más
for valor in (["RV"], {"RV": 1}, 3, True, 0.0, "rv", " RV", "RV\u200b", "\uff32\uff36", "RV\n", MARCA):
    b, msgs, d = copia()
    poner(b, OPPS[0], valor)
    antes = foto(b)
    try:
        alta(b, OPPS[0])
        ok(f"A1 alta con clase {valor!r} rechazada", False, "aceptada")
        continue
    except ClaseNoAdmitida as e:
        texto = str(e)
    despues = foto(b)
    cambian = {k for k in antes.keys() | despues.keys() if antes.get(k) != despues.get(k)}
    ok(f"A1 alta con clase {valor!r} rechazada sin escribir más que HA",
       cambian <= {"HA_historial_auditorias.jsonl", "contadores.json", "sellos_integridad.json"} and msgs == [] and len(incs(b)) == 1,
       f"{cambian} {len(msgs)} {len(incs(b))}")
    if valor == MARCA:
        ok("A1 el valor no sale ni en HA ni en el mensaje de la excepción", MARCA not in texto and apariciones(d, MARCA) == [],
           f"{apariciones(d, MARCA)}")

# A2: C6 con la marca: ni HA, ni F5, ni F11, ni entregables, ni el resultado llevan el valor
b, msgs, d = copia()
seg = alta(b, OPPS[0])["seg_id"]
poner(b, OPPS[0], MARCA)
res = []
for dia in ("2026-06-12", "2026-06-13", "2026-06-14"):
    res += b.seguimientos.ejecutar(dia)
ok("A2 C6 con la marca: el valor solo está en F3", apariciones(d, MARCA) == [] and MARCA not in json.dumps(res)
   and not [m for m in msgs if MARCA in json.dumps(m, default=str)], f"{apariciones(d, MARCA)}")
ok("A2 tres días, un solo INC-", len(incs(b)) == 1 and len({x["inc_id"] for x in res}) == 1, f"{len(incs(b))}")

# A3: 30 días seguidos y acciones del Broker entre medias: el mismo episodio, una incidencia
b, msgs, d = copia()
seg = alta(b, OPPS[0])["seg_id"]
poner(b, OPPS[0], "XYZ")
import pandas as pd  # noqa: E402
for i in range(30):
    b.seguimientos.ejecutar(str((pd.Timestamp("2026-06-12") + pd.Timedelta(days=i)).date()))
n30 = len(incs(b))
enc = b.seguimientos.encargos()[seg]
ok("A3 treinta días vencido: un INC- y F11 sin avanzar", n30 == 1 and enc["proximo_ciclo"] == "2026-06-12" and enc["ciclos"] == 0,
   f"{n30} {enc['proximo_ciclo']}")
b.seguimientos.procesar({"accion": "MODIFICACION", "seg_id": seg, "motivo": "otro"}, "2026-07-12")
b.seguimientos.procesar({"accion": "PAUSA", "seg_id": seg}, "2026-07-12")
b.seguimientos.procesar({"accion": "REANUDACION", "seg_id": seg}, "2026-07-12")
for i in range(10):
    b.seguimientos.ejecutar(str((pd.Timestamp("2026-07-19") + pd.Timedelta(days=i)).date()))
ok("A3 modificar, pausar y reanudar no abren otro INC- (mismo episodio)", len(incs(b)) == 1, f"{len(incs(b))}")

# A4: opción VIGENTE con la clase estropeada: no se omite «cubierta en C1», se salta con su INC- y F11 no cambia
b, msgs, d = copia()
seg = alta(b, OPPS[0])["seg_id"]
poner(b, OPPS[0], "XYZ", estado="VIGENTE")
n_f11 = len(b.almacen.leer("F11"))
[x] = b.seguimientos.ejecutar("2026-06-12")
ok("A4 VIGENTE con clase mala: INC- y sin CICLO_OMITIDO", x.get("inc_id") and len(b.almacen.leer("F11")) == n_f11, f"{x}")

# A5: corregida, absorbida en C1 (VIGENTE, sin ciclo hecho) y vuelta a estropear con el mismo valor: otro episodio
b, msgs, d = copia()
seg = alta(b, OPPS[0])["seg_id"]
poner(b, OPPS[0], "XYZ")
b.seguimientos.ejecutar("2026-06-12")
poner(b, OPPS[0], "RV", "2026-06-12", estado="VIGENTE")
[x] = b.seguimientos.ejecutar("2026-06-12")
ok("A5 corregida y VIGENTE: cubierta en C1", x.get("motivo") == "cubierto en C1", f"{x}")
poner(b, OPPS[0], "XYZ", "2026-06-19", estado="PROPUESTA")
b.seguimientos.ejecutar("2026-06-19")
ok("A5 vuelta a estropear tras la absorción (ciclos sigue en 0): otro INC-", len(incs(b)) == 2, f"{len(incs(b))}")

# A6: fallo al escribir el INC- del alta (HA rota): sube el error y no queda ni encargo, ni F3, ni F5, ni mensajes
b, msgs, d = copia()
poner(b, OPPS[0], "XYZ")
antes = foto(b)
orig = b.almacen.escribir


def roto(archivo, *a, **k):
    if archivo == "HA":
        raise OSError("disco lleno")
    return orig(archivo, *a, **k)


b.almacen.escribir = roto
try:
    alta(b, OPPS[0])
    ok("A6 alta con HA rota no sigue", False, "aceptada")
except ClaseNoAdmitida:
    ok("A6 alta con HA rota: sube el error de HA, no ClaseNoAdmitida sin INC-", False, "ClaseNoAdmitida sin INC-")
except OSError:
    despues = foto(b)
    cambian = {k for k in antes.keys() | despues.keys() if antes.get(k) != despues.get(k)}
    ok("A6 alta con HA rota: OSError y solo el contador de INC-", cambian <= {"contadores.json"} and msgs == [], f"{cambian}")
b.almacen.escribir = orig

# A7: fallo a mitad de un C6 con tres encargos (el segundo estropeado): el primero hecho, nada a medias; al reintentar, cada uno
# una vez
b, msgs, d = copia()
segs = [alta(b, o)["seg_id"] for o in OPPS[:3]]
poner(b, OPPS[1], "XYZ")
orig_inc = b.almacen.incidencia


def inc_roto(*a, **k):
    raise OSError("disco lleno")


b.almacen.incidencia = inc_roto
try:
    b.seguimientos.ejecutar("2026-06-12")
    ok("A7 el fallo del INC- sube", False)
except OSError:
    pass
b.almacen.incidencia = orig_inc
e = b.seguimientos.encargos()
ok("A7 tras el fallo: el primero hecho, el segundo y el tercero intactos",
   [e[s]["ciclos"] for s in segs] == [1, 0, 0] and not [m for m in msgs if m.get("seg_id") in segs[1:] and m["contrato"] in ("CT-05", "CT-06")],
   f"{[e[s]['ciclos'] for s in segs]}")
res = b.seguimientos.ejecutar("2026-06-12")
e = b.seguimientos.encargos()
ok("A7 al reintentar: el primero no se repite, el segundo se salta con su INC-, el tercero se hace",
   [x["seg_id"] for x in res] == segs[1:] and [e[s]["ciclos"] for s in segs] == [1, 0, 1] and len(incs(b)) == 1,
   f"{[x['seg_id'] for x in res]} {[e[s]['ciclos'] for s in segs]} {len(incs(b))}")
ok("A7 integridad del almacén", all(b.almacen.verificar_integridad().values()))

# A8: dos encargos de la misma opción, estropeada después: un INC- por encargo, y siguen siendo dos al cabo de 5 días
b, msgs, d = copia()
s1, s2 = alta(b, OPPS[0])["seg_id"], alta(b, OPPS[0])["seg_id"]
poner(b, OPPS[0], "")
for i in range(5):
    b.seguimientos.ejecutar(str((pd.Timestamp("2026-06-12") + pd.Timedelta(days=i)).date()))
ok("A8 dos encargos de la misma opción: dos INC-", sorted(x["objeto"] for x in incs(b)) == sorted([s1, s2]), f"{len(incs(b))}")

# A9: F11 manipulado con otra clase y F3 buena: manda la de F3 (RV → AG-03), sin INC-
b, msgs, d = copia()
seg = alta(b, OPPS[0])["seg_id"]
b.almacen.escribir("F11", "AG-01", {"tipo_entrada": "MODIFICACION", "seg_id": seg, "clase": "XYZ"})
del msgs[:]
[x] = b.seguimientos.ejecutar("2026-06-12")
ct06 = [m for m in msgs if m["contrato"] == "CT-06"]
ok("A9 F11 con otra clase: la de F3 manda", x["ejecutado"] and [m["receptor"] for m in ct06] == ["AG-03"] and not incs(b), f"{x.get('motivo')}")

# A10: campos del INC- según el esquema de HA (4.8) y tipo del enumerado
b, msgs, d = copia()
seg = alta(b, OPPS[0])["seg_id"]
poner(b, OPPS[0], None)
b.seguimientos.ejecutar("2026-06-12")
poner(b, OPPS[1], None)
try:
    alta(b, OPPS[1])
except ClaseNoAdmitida:
    pass
TIPOS = {"SEGURIDAD", "MANIPULACION", "CANAL_NO_PREVISTO", "ACCESO_FUERA_DE_MATRIZ", "HERRAMIENTA", "ESCRITURA", "OTRO"}
campos = {"id", "tipo", "severidad", "objeto", "campo_afectado", "tratamiento", "escalado_operador"}
ok("A10 INC- con los campos de 4.8 y tipo OTRO", len(incs(b)) == 2 and all(campos <= set(i) and i["tipo"] in TIPOS and i["tipo"] == "OTRO"
                                                                          for i in incs(b)))

# A11: OPP- de F11 que no está en F3, varios días: un INC-
b, msgs, d = copia()
b.fijar_fecha(AS_OF)
b.almacen.escribir("F11", "AG-01", {"tipo_entrada": "ALTA", "seg_id": "SEG-2026-0901", "opp_id": "OPP-2026-0901", "clase": "RV",
                                     "estado": "ACTIVO", "frecuencia": "SEMANAL", "fecha_alta": AS_OF, "ciclos": 0, "proximo_ciclo": "2026-06-12"})
for i in range(4):
    b.seguimientos.ejecutar(str((pd.Timestamp("2026-06-12") + pd.Timedelta(days=i)).date()))
ok("A11 OPP- fuera de F3, cuatro días: un INC-", len(incs(b)) == 1 and msgs == [])

# A12: un opp_id que no es una cadena en el alta: falla antes de escribir nada
for opp in (["OPP-2026-0001"], {"a": 1}):
    b, msgs, d = copia()
    antes = foto(b)
    try:
        alta(b, opp)
        ok(f"A12 alta con opp_id {opp!r}", False, "aceptada")
    except (TypeError, KeyError, ValueError) as e:
        ok(f"A12 alta con opp_id {opp!r}: {type(e).__name__} sin escribir nada", foto(b) == antes and not incs(b))

print(f"{len(fallos)} fallos: {fallos}")
sys.exit(1 if fallos else 0)
