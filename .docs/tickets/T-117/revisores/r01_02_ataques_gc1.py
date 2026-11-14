"""QA r01 de T-117 · Ataques a `diseno_v6.gc1()` y a la validación de `v6.gc1`: límites, tipos raros, señal no finita,
familias ausentes, negativas o no enteras. Solo lee y usa carpetas temporales.

Uso, desde bloque_a/11_Ejecutor:  python <este fichero>
Imprime lo observado; marca con «!!» lo que un revisor esperaría distinto (no es un gate: termina con 0).
"""
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "tests")]
import numpy as np
from conftest import AS_OF, config_pruebas
from test_t101_v6 import _bloque

from bloque_a import diseno_v6 as v6

TMP = Path(tempfile.mkdtemp())
n = 0


def bloque(**gc1):
    global n
    n += 1
    return _bloque(TMP / str(n), config_pruebas(diseno="v6", v6={"gc1": gc1} if gc1 else {}))


def amb(s, senal, fam="__sin__"):
    sen = {"senal_compuesta": senal}
    if fam != "__sin__":
        sen["familias_concordantes"] = fam
    return {"simbolo": s, "senales": sen}


b = bloque(exploracion_celdas=0)
print("== 1 · borde del umbral (RF 0,65; RV 0,75), con dos familias")
for clase, vals in (("RF", [0.65, 0.6500000000000001, 0.6499999999999999, 0.64999, np.float64(0.65), np.float32(0.65), 1, 0, -0.1, 1.5]),
                    ("RV", [0.75, 0.7499999999999999, np.float64(0.75), 0.74])):
    for v in vals:
        try:
            _, reg = v6.gc1(b, clase, [amb("X", v, 2)], [], AS_OF)
            print(f"  {clase} señal {v!r:<22} ({type(v).__name__}) → pasan={reg['pasan']} sin_señal={reg['sin_senal_medible']} descartes={[d['motivo'] for d in reg['descartes']]}")
        except Exception as e:  # noqa: BLE001
            print(f"  {clase} señal {v!r} → EXCEPCIÓN {type(e).__name__}: {e}")

print("== 2 · señal no finita o de tipo raro (RF)")
for v in (float("nan"), float("inf"), float("-inf"), None, True, False, "0.9", [0.9], {"v": 0.9}, Decimal("0.9"), np.nan, np.int64(1)):
    try:
        f, reg = v6.gc1(b, "RF", [amb("X", v, 3)], [], AS_OF)
        marca = [u["gc1"] for u in f]
        aviso = "  !!" if marca == ["PASA"] and not isinstance(v, (int, float, np.floating, np.integer)) else ""
        print(f"  señal {v!r:<12} ({type(v).__name__}) → marca={marca} pasan={reg['pasan']} sin_señal={reg['sin_senal_medible']}{aviso}")
    except Exception as e:  # noqa: BLE001
        print(f"  señal {v!r} ({type(v).__name__}) → EXCEPCIÓN {type(e).__name__}: {e}  !!")

print("== 3 · recuento de familias (RF, señal 0,90, familias_min 2): ¿pasa?")
for fam in ("__sin__", None, 0, 1, 2, 3, 4, -1, -5, 1.0, 1.9, 2.0, 0.0, float("nan"), True, False, "1", "0", [1], np.int64(1), np.int64(0), np.int32(1),
            np.float64(1.0), Decimal(1)):
    try:
        _, reg = v6.gc1(b, "RF", [amb("X", 0.9, fam)], [], AS_OF)
        pasa = reg["pasan"] == ["X"]
        menos = False
        try:
            menos = not isinstance(fam, str) and fam is not None and fam != "__sin__" and float(fam) < 2
        except Exception:  # noqa: BLE001
            pass
        aviso = "  !! menos de dos familias y pasa" if pasa and menos else ""
        print(f"  familias {fam!r:<10} ({type(fam).__name__:<8}) → {'PASA' if pasa else 'descartado: ' + str([d['motivo'] for d in reg['descartes']])}{aviso}")
    except Exception as e:  # noqa: BLE001
        print(f"  familias {fam!r} → EXCEPCIÓN {type(e).__name__}: {e}  !!")

print("== 4 · orden: tope de candidatas y familias; vigentes; exploración")
cfg_b = bloque(exploracion_celdas=0)
maxc = int(v6.parametro(cfg_b.cfg, "seleccion.max_candidatas"))
uni = [amb(f"U{i:02d}", 0.99 - i * 0.01, 1 if i < 3 else 3) for i in range(maxc + 4)]
_, reg = v6.gc1(cfg_b, "RF", uni, [], AS_OF)
print(f"  max_candidatas={maxc}: pasan {len(reg['pasan'])} ({reg['pasan'][:3]}…); los 3 de más señal, con una familia, no ocupan plaza: "
      f"{all(s not in reg['pasan'] for s in ('U00', 'U01', 'U02')) and len(reg['pasan']) == maxc}")
print(f"  motivos: {sorted({d['motivo'] for d in reg['descartes']})}")
_, reg2 = v6.gc1(cfg_b, "RF", list(reversed(uni)), [], AS_OF)
print(f"  el orden de entrada no cambia el registro: {reg == reg2}")
_, reg3 = v6.gc1(cfg_b, "RF", uni, [], AS_OF)
print(f"  idempotente (misma llamada, mismo registro): {reg == reg3}")
print(f"  universo vacío: {v6.gc1(cfg_b, 'RF', [], [], AS_OF)[1]['pasan']}")

print("== 5 · configuración: ¿se rechaza al crear el Bloque?")
casos = [("umbral_por_perfil", x) for x in (0, "", [], False, "abc", 0.65, [0.65], {"RF": "0.65"}, {"rf": 0.65}, {1: 0.65}, {"RF": 1e-300}, {"RF": 0.0},
                                             {"RF": -0.0}, {"RF": 1.0000000001}, {"RF": np.float64(0.65)}, {"RF": np.float32(0.65)}, {"RF": Decimal("0.65")},
                                             {"RF": [0.65]}, {"RF": {"u": 0.65}}, {"RF": 0.65, "XX": 0.5}, {None: 0.5}, {"RF": 1})]
casos += [("familias_min", x) for x in (None, 2.0, np.int64(2), "", [], {}, 0, 3, 4, -0, False, 1.0)]
for clave, valor in casos:
    try:
        bb = bloque(**{clave: valor})
        visto = v6.op(bb, f"gc1.{clave}")
        _, reg = v6.gc1(bb, "RF", [amb("X", 0.7, 1), amb("Y", 0.7, 2)], [], AS_OF)
        raro = clave == "umbral_por_perfil" and not isinstance(valor, dict) or clave == "familias_min" and not isinstance(valor, int)
        print(f"  {clave}={valor!r:<26} → ACEPTADA; en cfg={visto!r}; RF: umbral={reg['umbral']} familias_min={reg['familias_min']} pasan={reg['pasan']}"
              f"{'  !! tipo no válido aceptado' if raro else ''}")
    except ValueError as e:
        print(f"  {clave}={valor!r:<26} → rechazada: {str(e)[:70]}")
    except Exception as e:  # noqa: BLE001
        print(f"  {clave}={valor!r:<26} → EXCEPCIÓN no controlada {type(e).__name__}: {str(e)[:80]}  !!")

print("== 6 · con diseño V5 la sección v6.gc1 no se valida ni se usa")
try:
    b5 = _bloque(TMP / "v5", config_pruebas(v6={"gc1": {"umbral_por_perfil": {"XX": 9}, "familias_min": 99}}))
    print(f"  V5 con v6.gc1 inválido → se crea (v6={b5.v6}): la validación solo corre con diseno v6")
except Exception as e:  # noqa: BLE001
    print(f"  V5 con v6.gc1 inválido → {type(e).__name__}: {e}")

print("== 7 · umbral que recibe el Analista en el CT-06 frente al que aplicó GC1 por código (ciclo V6, RF y RV)")
bc = _bloque(TMP / "ciclo", config_pruebas(diseno="v6"))
vistos = {}
crear = bc.mensajeria.crear


def anotar(contrato, emisor, receptor, cuerpo, **kw):
    if contrato == "CT-06" and "umbral_senal_gc1" in cuerpo:
        vistos.setdefault(cuerpo["clase"], cuerpo["umbral_senal_gc1"])
    return crear(contrato, emisor, receptor, cuerpo, **kw)


bc.mensajeria.crear = anotar
bc.ciclo(AS_OF, alcance={"clases": ["RF", "RV"]})
cob = [e for e in bc.almacen.leer("HA") if e.get("tipo_entrada") == "COBERTURA"][-1]["clases"]
for c in ("RF", "RV"):
    g = cob[c]["gc1"]
    print(f"  {c}: GC1 por código umbral={g['umbral']} pasan={g['pasan']} · el CT-06 dice umbral_senal_gc1={vistos.get(c)}"
          f"{'  !! el Analista recibe otro umbral' if vistos.get(c) != g['umbral'] else ''}")
