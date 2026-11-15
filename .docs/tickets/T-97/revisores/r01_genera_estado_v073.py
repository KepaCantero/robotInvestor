"""QA r01 de T-97 (revisor nuevo sin contexto, Claude). Genera un estado guardado AUTÉNTICO de la V0.73 con el código de la
V0.73 (un worktree del commit anterior a T-97), con valores personalizados y un expediente AUTORIZADA pendiente de enviar.
Datos SIMULADOS.

Con un tercer argumento «v074» genera el mismo estado con el código de la V0.74 (worktree del commit de T-97), para probar la
cadena V0.74 -> V0.76 (solo MIG-011).

Uso: python3 -I r01_genera_estado_v073.py <marco_comun_c de la V0.73 o V0.74> <salida.json> [v074]
"""
import copy
import sys
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
import persistencia as pe  # noqa: E402
import pruebas_orquestador as po  # noqa: E402
from control_f import POLITICA_DEFECTO, VERSION_REGLAS  # noqa: E402
from orquestador import CONFIG_DEFECTO, Orquestador  # noqa: E402

V074 = len(sys.argv) > 3 and sys.argv[3] == "v074"
if V074:
    assert VERSION_REGLAS == "F-0.4.0" and CONFIG_DEFECTO["version_config"] == "CFG-0.12.0", "no es el código de la V0.74"
else:
    assert VERSION_REGLAS == "F-0.3.0" and CONFIG_DEFECTO["version_config"] == "CFG-0.11.0", "no es el código de la V0.73"
    assert "tope_anual_gasto_pct_capital" not in CONFIG_DEFECTO

# valores personalizados (los de una copia que ya había ajustado su SC-1)
pol = {**POLITICA_DEFECTO, "valor_min_eur": 10.0, "importe_max_dia_eur": 30000.0, "perdida_semana_max_eur": 4000.0}
cfg = {**po.CFG, "politica_f": pol, "tolerancia_tipo_k_rel": 0.2, "dia_coste_max_eur": 40.0}
if V074:   # en la V0.74 la copia personaliza también las claves nuevas
    cfg.update({"tope_anual_gasto_pct_capital": 2.0, "capital_referencia_eur": 100000.0, "tolerancia_tipo_k_rel_principales": 0.2,
                "divisas_principales": ["USD", "GBP"]})
    pol["perdida_semana_max_pct_tactica"] = 3.0
o = Orquestador(cfg, po.CAL)
for s in (po.S1,):
    assert o.registrar_sello(s, po.AHORA)["ok"]
po.registrar_motor(o, po.S1["sello_id"])
po.hasta(o, "AUTORIZADA", n=1)
r = o.registrar_gasto("EV-ENC-0001", 3.0, 1.0, po.AHORA)
assert r["ok"], r
assert o.integridad() == [], o.integridad()
texto = pe.volcar(o, po.AHORA)
Path(sys.argv[2]).write_text(texto, encoding="ascii")
print("estado V0.74 guardado:" if V074 else "estado V0.73 guardado:", sys.argv[2], "esquema", pe.esquema_actual(), "expedientes", {k: v["estado"] for k, v in o.expedientes.items()})
