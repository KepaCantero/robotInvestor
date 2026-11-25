"""QA r01 de T-201 (revisor): ¿es un defecto real que `b_agente` mande al AG-03 una opción con una clase desconocida?

Uso: python r06_b_agente.py <11_Ejecutor> <carpeta_tmp>
Escribe en F3 una opción con clase desconocida («XYZ»), otra con la clase vacía y una DIV de control, da de alta su seguimiento (CT-24 ALTA) y fuerza
su ciclo C6. Imprime a quién va el CT-06, qué clase lleva, el dictamen del informe C6 y si queda alguna incidencia en HA.
Se ejecuta igual con la base y con T-201: T-201 no cambia esto (es la observación de INC-T201-01).
"""
import json
import sys
from pathlib import Path

EJ, TMP = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(EJ))
sys.path.insert(0, str(EJ / "tests"))
sys.dont_write_bytecode = True

from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402

from bloque_a import seguimiento  # noqa: E402

ESQUEMA: list = []
_orig = seguimiento._errores_esquema_seguimiento


def _espia(b_, informe):
    errores = _orig(b_, informe)
    ESQUEMA.append({"clase_informe": (informe.get("opcion") or {}).get("clase", informe.get("clase")), "errores": errores})
    return errores


seguimiento._errores_esquema_seguimiento = _espia
b = nuevo_bloque(TMP, cargar_universo(RUTA_UNIVERSO_EJEMPLO))
b.fijar_fecha(AS_OF)
for opp_id, clase in (("OPP-2026-0901", "XYZ"), ("OPP-2026-0902", ""), ("OPP-2026-0903", "DIV")):
    ficha = {"tipo_entrada": "ALTA", "opp_id": opp_id, "estado": "DESCARTADA", "horizonte_principal": "H3",
             "indicador_seguimiento": {"simbolo": "EURUSD=X"}}
    if clase is not None:
        ficha["clase"] = clase
    b.fijar_fecha(AS_OF)   # el C6 anterior dejó el reloj en el 12-06: la ficha y el alta van con la fecha del alta
    try:
        b.almacen.escribir("F3", "AG-02", ficha)
        acuse = b.seguimientos.procesar({"accion": "ALTA", "opp_id": opp_id, "frecuencia": "SEMANAL", "motivo": "QA T-201",
                                         "senales_interes": [], "fecha_fin": None}, AS_OF)
        n_ha = len(b.almacen.leer("HA"))
        [r] = b.seguimientos.ejecutar("2026-06-12", seg_id=acuse["seg_id"], forzar=True)
        ct06 = [m for m in b.mensajeria.registro if m.get("contrato") == "CT-06"][-1:]
        inc = [e for e in b.almacen.leer("HA")[n_ha:] if e.get("tipo_entrada") == "INC"]
        g3v = [e for e in b.almacen.leer("HA")[n_ha:] if e.get("tipo_entrada") == "G3V"]
        print(json.dumps({"opp": opp_id, "clase_en_F3": clase, "ciclo_c6": {k: r.get(k) for k in ("ejecutado", "dictamen", "entregado",
                                                                                                    "recomendacion", "motivo")},
                          "ct06_registrado": [(m["emisor"], m["receptor"]) for m in ct06],
                          "errores_esquema_c6": ESQUEMA[-1:],
                          "dictamen_g3v": [e.get("dictamen_ht09") for e in g3v],
                          "incidencias_nuevas_en_HA": [(e.get("tipo"), e.get("detalle", "")[:120]) for e in inc]},
                         ensure_ascii=False, default=str))
    except Exception as e:   # noqa: BLE001
        print(json.dumps({"opp": opp_id, "clase_en_F3": clase, "excepcion": f"{type(e).__name__}: {str(e)[:300]}"}, ensure_ascii=False))
