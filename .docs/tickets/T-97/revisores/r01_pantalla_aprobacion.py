"""QA r01 de T-97 (revisor nuevo sin contexto, Claude). La pantalla de aprobación del operador (V0.40: «las cifras de la §8 con las
que F decidió») con una cartera de 20.000 €: ¿enseña los límites de F-14 y F-16 que F aplicó (los del %, más estrictos) o los
de euros? Datos SIMULADOS.

Uso: python3 -I r01_pantalla_aprobacion.py <marco_comun_c de hoy>
"""
import sys
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import CART_E, AHORA, Arnes, hasta, nuevo  # noqa: E402

h = Arnes()
o = nuevo()
hasta(o, "PROPUESTA", n=1, cartera_e={**CART_E, "capital_eur": 20000.0})
inf = informe_f(o, "EXP-0001", 1, cartera={"capital_eur": 20000.0})
ctl = {c["regla"]: c for c in inf["resultado_politica"]["controles"]}
f16 = [c for c in inf["resultado_politica"]["controles"] if c["regla"] == "F-16" and c["limite"] != 2500.0]
r = o.pantalla_aprobacion("EXP-0001", inf, AHORA)
assert r["ok"], r
p = r["pantalla"]
fx = p["tipo_cambio_eur"]
lim_f14_eur = ctl["F-14"]["limite"] * 1.10 * fx   # F-14 lleva el límite en unidades; en euros con el precio límite
print("   F aplicó: F-14 (euros) =", round(lim_f14_eur, 2), "· F-16 semana =", [c["limite"] for c in f16])
print("   la pantalla enseña: limite_dia_eur =", p["limite_dia_eur"], "· limite_semana_eur =", p["limite_semana_eur"])
h.chk("pantalla_limite_del_dia_es_el_que_aplico_F_5000", abs(p["limite_dia_eur"] - 5000.0) < 0.01, p["limite_dia_eur"])
h.chk("pantalla_limite_semana_es_el_que_aplico_F_1000", f16 and abs(p["limite_semana_eur"] - f16[0]["limite"]) < 0.01, (p["limite_semana_eur"], f16))
print(f"\n{h.n} comprobaciones")
print("RESULTADO:", "TODAS PASAN" if h.ok else "HAY FALLOS (H-02)")
sys.exit(0 if h.ok else 1)
