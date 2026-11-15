"""QA r01 de T-121 · H-01: la regla nueva de CT-10 (ERROR_ORIGINAL frente a CONVENCION_DISTINTA).

Artefacto de DEC-VOI-001 (lee `parametros_ht03`) y de RISK-VAR-001 (lee `horizontes`), bueno y con una cifra alterada. Se
simula un cambio de `config/por_defecto.yaml` sustituyendo la copia en memoria (`configuracion._CONFIG_POR_DEFECTO`), que
es la que leen `parametro` y `_configuracion_usada`.
 A. ¿un error real sigue en CONVENCION_DISTINTA? por_defecto.yaml: (1) cambia el valor de la clave leída; (2) gana una clave
    nueva en la misma sección, que la ficha no lee; (3) pierde una clave que la ficha no lee; (4) cambia otra sección.
 B. ¿una convención real se clasifica como error? (1) el Motor original sin la sección en su configuración (se toma de
    por_defecto.yaml) y después cambia por_defecto.yaml en la clave leída; (2) artefacto sin `configuracion_usada`;
    (3) `configuracion_usada` sin la sección leída.
Uso: .venv/bin/python -I r01_02_h01_ct10.py
"""
import copy
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "T-118" / "revisores"))
import r01_comun as C  # noqa: E402

C.preparar(sys.argv)
from bloque_a import configuracion  # noqa: E402
from bloque_a.almacen import Almacen  # noqa: E402
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

K = C.Contador("r01_02 T-121 H-01")
ORIGINAL = copy.deepcopy(configuracion.config_por_defecto())


def con_defecto(cambio):
    d = copy.deepcopy(ORIGINAL)
    cambio(d)
    configuracion._CONFIG_POR_DEFECTO = d


def restaurar():
    configuracion._CONFIG_POR_DEFECTO = copy.deepcopy(ORIGINAL)


def copia(m, calc, cambio):
    e = copy.deepcopy(m.almacen.estado("RC")[calc])
    cambio(e)
    e["calc_id"] = m.almacen.nuevo_id("CALC")
    m.almacen.escribir("RC", "AG-13", e)
    return e["calc_id"]


def ree(m, calc):
    try:
        out = m.reejecutar(calc, "QA r01 de T-121")
        return out["coincide"], out["categoria"]
    except Exception as e:  # noqa: BLE001
        return "EXC", f"{type(e).__name__}: {e}"[:120]


tmp = tempfile.mkdtemp(prefix="qa_t121_h01_")
m = C.motor(tmp)
voi = m.servir(C.peticion("DEC-VOI-001", 1), "AG-18")["calc_id"]
var = m.servir(C.peticion("RISK-VAR-001"), "AG-18")["calc_id"]
reg_voi = m.almacen.estado("RC")[voi]["artefacto"]["configuracion_usada"]
print("  secciones guardadas DEC-VOI-001:", sorted(reg_voi), "· con valor:", sorted(k for k, v in reg_voi.items() if "valor" in v))
malo_voi = copia(m, voi, lambda e: e["resultado"]["payload"].__setitem__("voi_puntos", e["resultado"]["payload"]["voi_puntos"] + 1.0))
malo_var = copia(m, var, lambda e: e["resultado"]["payload"].__setitem__("n", e["resultado"]["payload"]["n"] + 1))


def ciclo(nombre, cambio, esperado_malo, calcs=(voi, malo_voi), extra=None):
    con_defecto(cambio)
    try:
        mm = servicio.Motor(Almacen(Path(tmp)), C.Proveedor(), cargar_config(extra=extra))
        mm.cfg = copy.deepcopy(configuracion._CONFIG_POR_DEFECTO) if extra is None else mm.cfg   # la vigente sigue al fichero
        bueno, malo = ree(mm, calcs[0]), ree(mm, calcs[1])
    finally:
        restaurar()
    print(f"    {nombre}: bueno {bueno} · alterado {malo}")
    K.comprobar(f"{nombre}: alterado → {esperado_malo}", malo[1] == esperado_malo and bueno[0] in ("SI", "DENTRO_TOLERANCIA"),
                f"bueno {bueno} malo {malo}")


print("\n[A] error real del original: ¿sigue siendo ERROR_ORIGINAL si cambia por_defecto.yaml?")
ciclo("A0 sin cambios", lambda d: None, "ERROR_ORIGINAL")
ciclo("A1 cambia umbral E (la clave leída) en por_defecto.yaml", lambda d: d["parametros_ht03"]["umbrales"].__setitem__("E", 68), "ERROR_ORIGINAL")
ciclo("A2 por_defecto.yaml gana una clave nueva en parametros_ht03 (no la lee nadie)",
      lambda d: d["parametros_ht03"].__setitem__("clave_nueva_t57", 1), "ERROR_ORIGINAL")
ciclo("A2b gana una clave nueva dentro de parametros_ht03.umbrales",
      lambda d: d["parametros_ht03"]["umbrales"].__setitem__("Z", 99), "ERROR_ORIGINAL")
ciclo("A3 pierde una clave de parametros_ht03 que la ficha no lee",
      lambda d: d["parametros_ht03"].pop(next(k for k in d["parametros_ht03"] if k not in ("umbrales",))), "ERROR_ORIGINAL")
ciclo("A4 cambia otra sección (uc)", lambda d: d.setdefault("uc", {}).__setitem__("clave_qa", 1), "ERROR_ORIGINAL")
ciclo("A5 RISK-VAR-001: horizontes gana un H6", lambda d: d["horizontes"].__setitem__("H6", {"meses": 240}), "ERROR_ORIGINAL",
      calcs=(var, malo_var))

print("\n[B] ¿una convención real (la re-ejecución no pudo usar la configuración de entonces) se culpa al original?")
# B1: Motor original SIN la sección parametros_ht03 en su configuración: se registra sin valor y se toma del fichero
tmpb = tempfile.mkdtemp(prefix="qa_t121_h01b_")
cfg_sin = cargar_config()
cfg_sin.pop("parametros_ht03")
mb = servicio.Motor(Almacen(Path(tmpb)), C.Proveedor(), cfg_sin)
rb = mb.servir(C.peticion("DEC-VOI-001", 1), "AG-18")["calc_id"]
regb = mb.almacen.estado("RC")[rb]["artefacto"]["configuracion_usada"]["parametros_ht03"]
print("    B1 registro sin la sección en la configuración del Motor:", regb)
con_defecto(lambda d: d["parametros_ht03"]["umbrales"].__setitem__("E", 68))
try:
    mb2 = servicio.Motor(Almacen(Path(tmpb)), C.Proveedor(), cfg_sin)
    b1 = ree(mb2, rb)
finally:
    restaurar()
print(f"    B1 bueno con por_defecto.yaml cambiado en la clave leída: {b1}")
K.comprobar("B1 un original bueno calculado con el fichero de entonces no se culpa: no ERROR_ORIGINAL", b1[1] != "ERROR_ORIGINAL", str(b1))
# B2 sin configuracion_usada, cambio de la vigente
b2c = copia(m, voi, lambda e: e["artefacto"].pop("configuracion_usada"))
mm = C.motor(tmp, parametros_ht03={"umbrales": {"E": 68}})
b2 = ree(mm, b2c)
print(f"    B2 bueno sin configuracion_usada y E vigente 68: {b2}")
K.comprobar("B2 sin configuración registrada: no ERROR_ORIGINAL", b2[1] != "ERROR_ORIGINAL", str(b2))
b3c = copia(m, voi, lambda e: e["artefacto"]["configuracion_usada"].pop("parametros_ht03"))
b3 = ree(mm, b3c)
print(f"    B3 bueno sin la sección leída en el registro y E vigente 68: {b3}")
K.comprobar("B3 sección leída sin registro: no ERROR_ORIGINAL", b3[1] != "ERROR_ORIGINAL", str(b3))
# B4 registro con la sección como no-dict (manipulado) y la vigente cambiada
b4c = copia(m, voi, lambda e: e["artefacto"]["configuracion_usada"].__setitem__("parametros_ht03", "x"))
b4 = ree(mm, b4c)
print(f"    B4 bueno con la sección registrada ilegible y E vigente 68: {b4}")
K.comprobar("B4 sección registrada ilegible: no ERROR_ORIGINAL", b4[1] != "ERROR_ORIGINAL", str(b4))
sys.exit(K.fin())
