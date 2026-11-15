"""QA r01 de T-97 (revisor nuevo sin contexto, Claude). CA-6 con los pares del README: EUR/USD (principal) y EUR/SEK (no listada)
al 0,6 % y al 3,1 %, con un sello de K de verdad que lleva una fuente EURSEK (construida por el camino normal de K), bordes
justo en el 0,5 % y el 3 %, cotización inversa (USDEUR), JPY y CHF por defecto principales, y divisas en minúsculas o sin
clasificar. Datos SIMULADOS.

Uso: python3 -I r01_tipo_cambio_divisas.py <marco_comun_c de hoy>
"""
import copy
import sys
from pathlib import Path

MARCO = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(MARCO / "validador"))
sys.path.insert(0, str(MARCO / "pruebas"))
from orquestador import Orquestador  # noqa: E402
from pruebas_k import CAL, construir, escala_todo  # noqa: E402
from pruebas_orquestador import AHORA, CART_E, CFG, Arnes  # noqa: E402

h = Arnes()
DEF = {"tolerancia_tipo_k_rel": 0.03, "tolerancia_tipo_k_rel_principales": 0.005, "divisas_principales": ["USD", "GBP", "JPY", "CHF"]}


def con_sek(e):
    """Añade una fuente EURSEK (copia de la EURUSD a una escala de unas 11,5 coronas por euro)."""
    base = next(f for f in e["fuentes"] if f["fuente_id"] == "SRC-EURUSD")
    sek = copy.deepcopy(base)
    sek["fuente_id"], sek["instrumento"] = "SRC-EURSEK", "EURSEK"
    sek.pop("contraste", None)
    sek["critico"] = False
    sek["procedencia"] = {**sek["procedencia"], "fuente_id": "SRC-EURSEK"} if "fuente_id" in sek["procedencia"] else sek["procedencia"]
    escala_todo(sek["serie"], 10.5)
    e["fuentes"].append(sek)


_, r = construir(mut=con_sek)
s = r["sello"]
fu = {f["instrumento"]: f for f in s["fuentes"]}
h.chk("sello_con_EURSEK_disponible", "EURSEK" in fu and fu["EURSEK"]["estado"] == "DISPONIBLE", [(f["instrumento"], f["estado"]) for f in s["fuentes"]])
k_usd = 1 / fu["EURUSD"]["ultimo_cierre"]
k_sek = 1 / fu["EURSEK"]["ultimo_cierre"]


def foto(tipos):
    return {**copy.deepcopy(CART_E), "fecha_hora": "2026-11-06T08:55:00+00:00", "tipos_cambio_eur": tipos}


def reg(tipos, cfg=None):
    o = Orquestador({**CFG, **DEF, **(cfg or {})}, CAL)
    rs = o.registrar_sello(s, AHORA)
    assert rs["ok"], rs
    return o.registrar_cartera(foto(tipos), "G", AHORA, cuenta="SIM-1")


# CA-6
r = reg({"USD": round(k_usd * 1.006, 8), "SEK": round(k_sek, 8)})
h.chk("CA6_EURUSD_0_6pct_se_rechaza", not r["ok"] and r["codigo"] == "O-29" and "USD" in r["motivo"] and "SEK" not in r["motivo"], r)
r = reg({"USD": round(k_usd, 8), "SEK": round(k_sek * 1.006, 8)})
h.chk("CA6_EURSEK_0_6pct_pasa", r["ok"], r)
r = reg({"USD": round(k_usd, 8), "SEK": round(k_sek * 1.031, 8)})
h.chk("CA6_EURSEK_3_1pct_se_rechaza", not r["ok"] and "SEK" in r["motivo"], r)
r = reg({"USD": round(k_usd * 1.031, 8), "SEK": round(k_sek, 8)})
h.chk("CA6_EURUSD_3_1pct_se_rechaza", not r["ok"] and "USD" in r["motivo"], r)
r = reg({"USD": round(k_usd * 1.031, 8), "SEK": round(k_sek * 1.031, 8)})
h.chk("CA6_los_dos_al_3_1pct_se_rechazan_y_se_citan_los_dos", not r["ok"] and "USD" in r["motivo"] and "SEK" in r["motivo"], r)
r = reg({"USD": round(k_usd * 0.994, 8)})
h.chk("EURUSD_0_6pct_por_debajo_tambien_se_rechaza", not r["ok"], r)

# bordes (la desviación se calcula sobre el cierre: v*ci - 1)
r = reg({"USD": round(k_usd * 1.0049, 8)})
h.chk("EURUSD_0_49pct_pasa", r["ok"], r)
r = reg({"USD": round(k_usd * 1.0051, 8)})
h.chk("EURUSD_0_51pct_se_rechaza", not r["ok"], r)
r = reg({"SEK": round(k_sek * 1.0299, 8)})
h.chk("EURSEK_2_99pct_pasa", r["ok"], r)
r = reg({"SEK": round(k_sek * 1.0301, 8)})
h.chk("EURSEK_3_01pct_se_rechaza", not r["ok"], r)

# la clasificación: lista vacía (todas a la general), SEK como principal, cambio de general a más estricta
r = reg({"USD": round(k_usd * 1.006, 8)}, {"divisas_principales": []})
h.chk("lista_vacia_USD_usa_la_general_y_pasa", r["ok"], r)
r = reg({"SEK": round(k_sek * 1.006, 8)}, {"divisas_principales": ["SEK"]})
h.chk("SEK_declarada_principal_se_endurece", not r["ok"], r)
o = Orquestador({**CFG, **DEF}, CAL)
h.chk("tolerancias_por_divisa", [o.tolerancia_tipo_k(d) for d in ("USD", "GBP", "JPY", "CHF", "SEK", "NOK", "XXX", "usd")]
      == [0.005] * 4 + [0.03] * 4)
r = reg({"usd": round(k_usd * 1.006, 8)})
h.chk("divisa_en_minusculas_en_la_foto_no_entra", not r["ok"] and r["codigo"] == "O-01", r)

# configuraciones que no arrancan
for nombre, cfg in (("principales_mas_laxa", {"tolerancia_tipo_k_rel_principales": 0.031}),
                    ("principales_nan", {"tolerancia_tipo_k_rel_principales": float("nan")}),
                    ("principales_none", {"tolerancia_tipo_k_rel_principales": None}),
                    ("lista_con_numero", {"divisas_principales": ["USD", 1]}),
                    ("lista_con_dict", {"divisas_principales": ["USD", {"x": 1}]}),
                    ("lista_31", {"divisas_principales": [f"A{chr(65 + i // 26)}{chr(65 + i % 26)}" for i in range(31)]})):
    try:
        Orquestador({**CFG, **DEF, **cfg}, CAL)
        h.chk(f"config_{nombre}_no_arranca", False, cfg)
    except ValueError:
        h.chk(f"config_{nombre}_no_arranca_ValueError", True)
    except Exception as ex:   # noqa: BLE001 — hallazgo bajo H-03 de la QA r01: no arranca (falla cerrado), pero no con ValueError
        print(f"   HALLAZGO H-03 (bajo): config_{nombre} no arranca, pero con {type(ex).__name__}: {ex!r}")

print(f"\n{h.n} comprobaciones")
print("RESULTADO:", "TODAS PASAN" if h.ok else "HAY FALLOS")
sys.exit(0 if h.ok else 1)
