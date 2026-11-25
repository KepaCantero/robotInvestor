"""QA r01 de T-191 (Claude). Ejecutar desde bloque_a/11_Ejecutor con la venv: python ../../.docs/tickets/T-191/revisores/r01_ataques.py
«HALLAZGO» marca lo que contradice el criterio o un invariante."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tests")
import conftest  # noqa: E402
from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a import sintesis  # noqa: E402
from bloque_a.contratos import DatosSensibles  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

U = cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO)
ORIGINAL = sintesis.ht09_validar


def linea(ok, texto):
    print(("ok       " if ok else "HALLAZGO ") + texto, flush=True)


def ciclo_con(control):
    tmp = Path(tempfile.mkdtemp())
    b = nuevo_bloque(tmp, U)
    sintesis.ht09_validar = control
    try:
        return b, tmp, b.ciclo(AS_OF, alcance={"clases": ["RV"]}), None
    except BaseException as e:  # noqa: BLE001
        return b, tmp, None, e
    finally:
        sintesis.ht09_validar = ORIGINAL


def caido(*a):
    raise RuntimeError("HT-09 no disponible")


# 1 · caso nominal: qué deja el ciclo
b, tmp, r, e = ciclo_con(caido)
ha = b.almacen.leer("HA")
inc = [x for x in ha if x.get("tipo") == "HERRAMIENTA"]
ct14 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-14"]
g3v = [x for x in ha if x.get("tipo_entrada") == "G3V"]
run = b.almacen.estado("F5").get(r["run_id"]) if r else None
print("   CT-14:", [(m["emisor"], m["receptor"], list((m.get("contenido") or m.get("payload") or {}).keys()) if isinstance(m, dict) else None) for m in ct14])
print("   G3V:", [(x["id"], x.get("tipo_control"), x.get("dictamen_ht09"), x.get("dictamen_efectivo")) for x in g3v])
print("   INC HERRAMIENTA:", [(x.get("detalle"), x.get("fase"), x.get("msg_id")) for x in inc])
print("   RUN F5:", {k: (run or {}).get(k) for k in ("estado", "entrega", "g3", "limitaciones")})
linea(bool(inc) and inc[0].get("msg_id") == (ct14[0]["msg_id"] if ct14 else None), "1a incidencia HERRAMIENTA ligada a la CT-14")
linea(bool(ct14) and ct14[0]["emisor"] == "AG-02" and ct14[0]["receptor"] == "AG-18", "1b CT-14 del Analizador (AG-02) al Orquestador (AG-18)")
linea(not any(x.get("dictamen_efectivo", "").startswith("APTO") for x in g3v), "1c ningún G3V APTO")
linea(not [p for p in (tmp / "ent").rglob("*") if p.is_file()] if (tmp / "ent").exists() else True, "1d nada en las carpetas de entrega")

# 2 · un fallo de integridad del almacén durante el control: ¿se toma por herramienta caída?
def integridad(bloque, *a):
    ruta = bloque.almacen.carpeta / "F2.jsonl"
    cand = [p for p in bloque.almacen.carpeta.iterdir() if p.name.startswith("F2")]
    ruta = cand[0] if cand else ruta
    datos = ruta.read_text(encoding="utf-8").split("\n")
    e0 = json.loads(datos[0]); e0["manipulado"] = True; datos[0] = json.dumps(e0, ensure_ascii=False)
    ruta.write_text("\n".join(datos), encoding="utf-8")
    bloque.almacen._firmas.clear() if hasattr(bloque.almacen, "_firmas") else None
    return ORIGINAL(bloque, *a)

b, tmp, r, e = ciclo_con(integridad)
inc = [x for x in (b.almacen._entradas.get("HA") or []) if x.get("tipo") == "HERRAMIENTA"]
print("   2:", "excepción", type(e).__name__, str(e)[:120] if e else "", "· resultado", (r or {}).get("entrega"), "· INC HERRAMIENTA", len(inc))
linea(e is not None and "integridad" in str(e).lower() and not inc,
      "2 un fallo de integridad en el control para el ciclo y no se registra como herramienta caída")

# 3 · un error de control (R6 / R8) dentro de HT-09: ¿se convierte en «herramienta caída»?
for exc in (DatosSensibles("dato protegido"), PermissionError("escritura fuera de reserva"), KeyError("bug del ejecutor"), TypeError("bug")):
    def falla(*a, _e=exc):
        raise _e
    b, tmp, r, e = ciclo_con(falla)
    inc = [x for x in b.almacen.leer("HA") if x.get("tipo") == "HERRAMIENTA"] if e is None else []
    linea(e is not None or isinstance(exc, (KeyError, TypeError)),
          f"3 {type(exc).__name__} dentro del control: excepción={type(e).__name__ if e else None} entrega={(r or {}).get('entrega')} INC HERRAMIENTA={len(inc)}")

# 4 · falla también la CT-14 (mensajería) dentro del respaldo: ¿queda F5/HA a medias?
from bloque_a import contratos  # noqa: E402
crear = contratos.Mensajeria.crear
def crear_falla(self, contrato, *a, **k):
    if contrato == "CT-14":
        raise OSError("mensajería caída")
    return crear(self, contrato, *a, **k)
contratos.Mensajeria.crear = crear_falla
b, tmp, r, e = ciclo_con(caido)
contratos.Mensajeria.crear = crear
inc = [x for x in b.almacen.leer("HA") if x.get("tipo") == "HERRAMIENTA"]
print("   4:", type(e).__name__ if e else None, "· INC", len(inc), "· integridad", all(b.almacen.verificar_integridad().values()))
