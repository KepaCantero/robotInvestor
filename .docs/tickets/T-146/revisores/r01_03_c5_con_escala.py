"""QA r01 de T-146 · AG-20 (C5) antes del reparto cuando el reparto pasa del ciclo y las bolsas se escalan (`tope_total`).

Uso: python -I r01_03_c5_con_escala.py <ruta a 11_Ejecutor> <carpeta temporal> [N2]
Con un N2 por tipo alto (p. ej. 100 UC, una configuración del operador) y los 12 tipos, el reparto pasa de 240 y cada bolsa se
escala (COMÚN, de 24 a unas 4,7 UC). AG-20 corre antes, contra una bolsa COMÚN sin escalar (24 × 1,25 = 30 UC) y con el
cliente real sobre un SDK falso de peor caso (salida = max_tokens; el primer intento no es JSON). Lo que gasta pasa a COMÚN.
El resto de agentes usa el simulado. Imprime COMÚN consumido frente a su límite escalado y la suma frente al ciclo."""
from __future__ import annotations

import json
import sys
import types
from pathlib import Path

EJ = Path(sys.argv[1]).resolve()
TMP = Path(sys.argv[2]).resolve()
N2 = float(sys.argv[3]) if len(sys.argv) > 3 else 100.0
sys.path.insert(0, str(EJ))
from bloque_a import mock_respuestas  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config  # noqa: E402
from bloque_a.consumo import tokens_de_peticion  # noqa: E402
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo  # noqa: E402
from bloque_a.llm import AnthropicClient, MockClient  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

DOCE = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]
cfg = cargar_config(extra={"modo": "vivo", "perfiles": {"activos": DOCE}, "presupuesto_uc": {"N2": N2},
                           "llm": {"cache_resultados": False}})


class SDK:
    def __init__(self):
        self.n = 0
        self.messages = self

    def create(self, **kw):
        self.n += 1
        msgs = kw["messages"]
        salida = int(kw["max_tokens"])
        entrada = int(tokens_de_peticion(kw["system"], msgs, kw.get("tools")) * 1.35)
        if len([m for m in msgs if m["role"] == "user"]) == 1:
            texto = "análisis " * int(salida * 3.6 / 9)
        else:
            texto = json.dumps(mock_respuestas.responder("AG-20", msgs[:1], 1), ensure_ascii=False)
        uso = types.SimpleNamespace(input_tokens=0, output_tokens=salida, cache_creation_input_tokens=entrada,
                                    cache_read_input_tokens=0, server_tool_use=None)
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


b = Bloque(cfg, ProveedorCSV(EJ / "ejemplos" / "datos_sinteticos"), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
           TMP / "estado", TMP / "ent")
sdk = SDK()
b.agentes.clientes["AG-20"] = AnthropicClient(sdk=sdk)
b.evaluador.ciclo = lambda as_of, run_id: {
    "resueltos": 3, "metricas": {"DIV|H2": {"n": 3, "brier": 0.2, "brier_ref": 0.25, "acierto": {"tasa": 0.66}, "calibracion_global": None}},
    "certificados": {"emitidos": [], "insuficientes": []}, "lecciones_nuevas": []}
capt = {}
original = Bloque._validar_g3


def espia(self, paquete, extras, as_of, run_id, presupuesto=None):
    capt["p"] = presupuesto
    return original(self, paquete, extras, as_of, run_id, presupuesto=presupuesto)


Bloque._validar_g3 = espia
r = b.ciclo("2024-03-29")
p = capt["p"]
ll = [x for x in b.contabilidad.llamadas if x["run_id"] == r["run_id"]]
ag20 = sum(x["uc"] for x in ll if x["agente"] == "AG-20")
pu = cfg["presupuesto_uc"]
com = r["presupuesto"]["COMUN"]
print(f"escala {p._escala:.4f} · peticiones de AG-20 {sdk.n} · AG-20 gastó {ag20:.3f} UC")
print(f"COMUN: asignado (sin escalar) {com['asignado']} · consumido {com['consumido']:.3f} · límite escalado {p.limite('COMUN'):.3f} · "
      f"máximo escalado {p.limite_maximo('COMUN'):.3f}")
suma_max = sum(p.limite_maximo(k) for k in p.asignado)
tot = sum(v["consumido"] for v in r["presupuesto"].values())
print(f"suma de límites máximos {suma_max:.3f} · suma consumida {tot:.3f} · ciclo con la ampliación máxima "
      f"{pu['ciclo_semanal_max'] * (1 + pu['ampliacion_max_autorizable']):.1f}")
pasa = com["consumido"] > p.limite("COMUN") + 1e-4
print("VIOLA: COMÚN pasa de su límite escalado" if pasa else "OK: COMÚN dentro de su límite")
cierres = [c for c in r.get("presupuesto_cierres", [])]
run = b.almacen.estado("F5", clave="id")[r["run_id"]]
print("cierres en COMÚN:", [c["fase"] + ": " + c["motivo"][:70] for c in run["cierres_parciales"] if c["clase"] == "COMUN"])
