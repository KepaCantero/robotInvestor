"""Sondas adversariales del revisor para la pieza V0.40 (pantalla con las cifras de F).
No es un hallazgo: cada sonda imprime CIERRA (fail-closed correcto) o ABRE (defecto)."""
import copy
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]   # V0.53: la ruta de la máquina de GLM no existe aquí
sys.path.insert(0, str(AQUI / "validador"))
sys.path.insert(0, str(AQUI / "pruebas"))

from control_f import aplanar_informe, construir_informe  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, nuevo, hasta, autorizar_op  # noqa: E402

EID = "EXP-0001"
H = Arnes()


def sonda(nombre, ok_si_cierra, detalle=""):
    H.n += 1
    print(f"{'CIERRA' if ok_si_cierra else 'ABRE  '} {nombre} {detalle}")
    H.ok &= ok_si_cierra


def propuesta():
    o = nuevo()
    hasta(o, "PROPUESTA")
    return o


# S1: informe con un contexto extranjero (autocoherente: CF-04 pasaría) pero no el del Orquestador -> sin pantalla (CF-09, O-01)
o = propuesta()
F = informe_f(o)
bueno = copy.deepcopy(aplanar_informe(F)["entradas"]["contexto"])
falso = copy.deepcopy(F)
aplanar_informe(falso)["entradas"]["contexto"]["actividad"]["importe_dia_eur"] = 1.0   # contexto mintiendo
r = o.pantalla_aprobacion(EID, falso, AHORA)
sonda("S1 contexto_extranjero_no_llega_a_pantalla", not r["ok"] and r["codigo"] == "O-01", (r["codigo"], r["motivo"][:60]))

# S2: NaN en la actividad del contexto del informe -> sin pantalla (O-01)
o = propuesta()
F = informe_f(o)
falso = copy.deepcopy(F)
aplanar_informe(falso)["entradas"]["contexto"]["actividad"]["importe_dia_eur"] = float("nan")
r = o.pantalla_aprobacion(EID, falso, AHORA)
sonda("S2 nan_en_actividad_no_llega_a_pantalla", not r["ok"] and r["codigo"] == "O-01", (r["codigo"], r["motivo"][:60]))

# S3: precio del intermediario 0 en el informe -> F-01 VETA al recalcular CF-04 -> sin pantalla; anulacion -> O-34
o = propuesta()
F = informe_f(o)
falso = copy.deepcopy(F)
aplanar_informe(falso)["entradas"]["contexto"]["precio_intermediario"] = {"valor": 0.0, "fecha_hora": "2026-11-06T08:50:00+00:00"}
r = o.pantalla_aprobacion(EID, falso, AHORA)
sonda("S3 precio_cero_sin_pantalla", not r["ok"] and EID not in o.pantallas, (r["codigo"], r["motivo"][:60]))
r2 = o.pantalla_aprobacion(EID, falso, AHORA, anular_veto={"motivo": "Motivo de prueba de anulación suficiente"})
sonda("S3b precio_cero_anulacion_rechazada", not r2["ok"] and EID not in o.pantallas, (r2["codigo"], r2["motivo"][:60]))

# S4: precio ausente (None) -> F-23 veta (no anulable) -> sin pantalla aunque se pida anulacion de F-09/F-11
o = propuesta()
F = informe_f(o)
falso = copy.deepcopy(F)
pl = aplanar_informe(falso)["entradas"]["contexto"]
pl["precio_intermediario"] = None
pl["actividad"]["importe_dia_eur"] = 0.0   # para que F-14 no recorte y los vetos sean F-09/F-11/F-23
r = o.pantalla_aprobacion(EID, falso, AHORA, anular_veto={"motivo": "Motivo de prueba de anulación suficiente"})
sonda("S4 sin_precio_anulacion_rechazada", not r["ok"] and EID not in o.pantallas, (r["codigo"], r["motivo"][:60]))

# S5: mutar el contexto del informe DESPUES de la pantalla: la pantalla guardada no cambia y autorizar da O-27
o = propuesta()
F = informe_f(o)
p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
ev_antes = copy.deepcopy(p["eventos_f"])
aplanar_informe(F)["entradas"]["contexto"]["eventos"].append({"fecha": "2026-11-06", "tipo": "RESULTADOS"})
r = o.autorizar(EID, "OPERADOR", F, AHORA, {"pantalla_hash": p["hash"], "importe_tecleado": p["importe"], "canal": "CONSOLA", "segundo_factor": True})
sonda("S5 eventos_f_no_comparte_objeto_y_rechaza", p["eventos_f"] == ev_antes and not r["ok"]
      and o.expedientes[EID]["estado"] == "PROPUESTA", (r["codigo"], p["eventos_f"] == ev_antes))

# S6: tocar CADA campo nuevo de la pantalla guardada -> O-27 (extremo a extremo, uno por uno)
NUEVOS = ("precio_intermediario", "precio_intermediario_en", "deriva_pct", "importe_dia_eur", "limite_dia_eur",
          "perdida_semana_eur", "limite_semana_eur", "ordenes_ultima_hora", "limite_ordenes_hora", "eventos_f")
OTRO = {"precio_intermediario": 1.11, "precio_intermediario_en": "2026-11-06T08:59:00+00:00", "deriva_pct": 0.9009,
        "importe_dia_eur": 111.0, "limite_dia_eur": 49999.0, "perdida_semana_eur": 1.0, "limite_semana_eur": 4999.0,
        "ordenes_ultima_hora": 1, "limite_ordenes_hora": 9, "eventos_f": [{"fecha": "2026-11-07", "tipo": "RESULTADOS"}]}
todos = True
for campo in NUEVOS:
    o = propuesta()
    F = informe_f(o)
    p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
    o.pantallas[EID][campo] = OTRO[campo]
    r = o.autorizar(EID, "OPERADOR", F, AHORA, {"pantalla_hash": p["hash"], "importe_tecleado": p["importe"], "canal": "CONSOLA", "segundo_factor": True})
    bien = r["codigo"] == "O-27" and o.expedientes[EID]["estado"] == "PROPUESTA"
    todos &= bien
    print(f"       tocar {campo}: {'O-27' if bien else r['codigo']}")
sonda("S6 hash_cubre_los_diez_campos_extremo_a_extremo", todos)

# S7: entero enorme en la cotizacion del intermediario -> G lo rechaza (no puede entrar en el contexto del Orquestador)
o = propuesta()
r = o.registrar_cotizacion({"instrumento": "EURUSD", "valor": 10 ** 400, "fecha_hora": "2026-11-06T08:55:00+00:00"}, "G", AHORA)
sonda("S7 entero_enorme_rechazado_en_cotizacion", not r["ok"] and r["codigo"] == "O-01", (r["codigo"],))

# S8: inf en perdida_semana del contexto (suma desbordada) -> _forma_contexto lo cierra: informe F-01, sin pantalla ni anulacion
o = propuesta()
F = informe_f(o)
falso = copy.deepcopy(F)
aplanar_informe(falso)["entradas"]["contexto"]["actividad"]["perdida_semana_eur"] = math.inf
r = o.pantalla_aprobacion(EID, falso, AHORA, anular_veto={"motivo": "Motivo de prueba de anulación suficiente"})
sonda("S8 inf_en_semana_sin_pantalla", not r["ok"] and EID not in o.pantallas, (r["codigo"], r["motivo"][:60]))

print(f"\n{H.n} sondas:", "TODAS CIERRAN (sin defecto reproducible)" if H.ok else "HAY SONDA QUE ABRE")
sys.exit(0 if H.ok else 1)
