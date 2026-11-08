"""Pruebas de V0.40: la pantalla de aprobación enseña las cifras de la §8 con las que F decidió (§6: «cifras calculadas por F,
sin texto de un LLM»). Los diez campos nuevos salen del propio informe de F (entradas.contexto y entradas.politica), no del estado
actual; el hash de la pantalla los cubre, así que aprobar la pantalla es aprobar esas cifras. Datos SIMULADOS.

Uso: python3 pruebas/pruebas_pantalla_f.py
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from control_f import POLITICA_DEFECTO, aplanar_informe  # noqa: E402
from orquestador import _hash  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, autorizar_op, hasta, nuevo  # noqa: E402

EID = "EXP-0001"
T = lambda m: f"2026-11-06T{9 + m // 60:02d}:{m % 60:02d}:00+00:00"   # noqa: E731 - minutos tras las 09:00
T_ESPERA = "2026-11-06T09:31:00+00:00"   # pasado el enfriamiento de la anulación (30 min [PROPUESTO])
MOTIVO = "Oportunidad revisada a mano: el tope de posiciones se cumple al cerrar otra hoy"
POS10 = [{"instrumento": f"XAU{i}", "activo_base": f"X{i:02d}", "valor_eur": 100.0} for i in range(10)]   # F-09: 10 posiciones
NUEVOS = ("precio_intermediario", "precio_intermediario_en", "deriva_pct", "importe_dia_eur", "limite_dia_eur",
          "perdida_semana_eur", "limite_semana_eur", "ordenes_ultima_hora", "limite_ordenes_hora", "eventos_f")


def propuesta(cfg=None):
    o = nuevo(cfg)
    hasta(o, "PROPUESTA")
    return o


def aprob(p, **kw):
    a = {"pantalla_hash": p["hash"], "importe_tecleado": p["importe"], "canal": "CONSOLA", "segundo_factor": True}
    a.update(kw)
    return a


def main():
    h = Arnes()
    # ---------------------------------------------------------------- los campos nuevos salen del informe, no del estado actual
    o = propuesta(); F = informe_f(o)
    ctx = aplanar_informe(F)["entradas"]["contexto"]
    pol = aplanar_informe(F)["entradas"]["politica"]
    p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
    h.chk("precio_y_deriva_coinciden_con_el_contexto",
          p["precio_intermediario"] == ctx["precio_intermediario"]["valor"] == 1.10
          and p["precio_intermediario_en"] == ctx["precio_intermediario"]["fecha_hora"] == "2026-11-06T08:50:00+00:00"
          and p["deriva_pct"] == 0.0, (p["precio_intermediario"], p["precio_intermediario_en"], p["deriva_pct"]))
    h.chk("actividad_y_limites_coinciden_con_el_contexto",
          p["importe_dia_eur"] == round(ctx["actividad"]["importe_dia_eur"] + p["importe"], 2) == 110.0
          and p["limite_dia_eur"] == pol["importe_max_dia_eur"] == 50000.0
          and p["perdida_semana_eur"] == ctx["actividad"]["perdida_semana_eur"] == 0.0
          and p["limite_semana_eur"] == pol["perdida_semana_max_eur"] == 5000.0
          and p["ordenes_ultima_hora"] == ctx["actividad"]["ordenes_ultima_hora"] == 0
          and p["limite_ordenes_hora"] == pol["ordenes_max_hora"] == 10, p)
    h.chk("eventos_f_son_los_del_contexto", p["eventos_f"] == ctx["eventos"] and (p["eventos_f"] is None or isinstance(p["eventos_f"], list)),
          (p["eventos_f"], ctx["eventos"]))
    h.chk("la_pantalla_no_recalcula_con_el_estado_actual",
          o.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.20, "fecha_hora": T(5)}, "G", T(5))["ok"]
          and (p2 := o.pantalla_aprobacion(EID, F, T(5)))["ok"]
          and p2["pantalla"]["precio_intermediario"] == 1.10 and p2["pantalla"]["deriva_pct"] == 0.0
          and p2["pantalla"]["precio_intermediario"] != 1.20
          and all(p2["pantalla"][c] == p[c] for c in NUEVOS), p2)
    # ---------------------------------------------------------------- deriva_pct con un precio distinto del límite
    o = propuesta()
    h.chk("cotizacion_previa_del_intermediario", o.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.11, "fecha_hora": T(0)}, "G", AHORA)["ok"])
    F = informe_f(o)   # el informe cota el límite: como ya hay una cotización de ese instante, no la pisa
    p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
    h.chk("deriva_pct_calculada_a_mano", p["precio_intermediario"] == 1.11 and p["deriva_pct"] == round(abs(1.10 / 1.11 - 1) * 100, 4)
          == 0.9009 and p["precio_intermediario_en"] == "2026-11-06T09:00:00+00:00", (p["precio_intermediario"], p["deriva_pct"]))
    h.chk("tocar_deriva_pct_de_la_pantalla_guardada_da_O27",
          (o.pantallas[EID].__setitem__("deriva_pct", 0) or True)
          and o.autorizar(EID, "OPERADOR", F, AHORA, aprob(p))["codigo"] == "O-27"
          and o.expedientes[EID]["estado"] == "PROPUESTA")
    # ---------------------------------------------------------------- importe_dia_eur suma lo ya autorizado hoy
    o = propuesta(); F1 = informe_f(o)
    p1 = o.pantalla_aprobacion(EID, F1, AHORA)["pantalla"]
    h.chk("primer_expediente_cuenta_solo_su_importe", p1["importe_dia_eur"] == 110.0 and p1["ordenes_ultima_hora"] == 0, p1)
    h.chk("autorizacion_del_primero", autorizar_op(o, EID, F1)["ok"] and o.expedientes[EID]["estado"] == "AUTORIZADA")
    hasta(o, "PROPUESTA", n=3)
    F3 = informe_f(o, "EXP-0003", n=3)
    p3 = o.pantalla_aprobacion("EXP-0003", F3, AHORA)["pantalla"]
    h.chk("importe_dia_eur_suma_lo_ya_autorizado_hoy", p3["importe_dia_eur"] == round(110.0 + p3["importe"], 2) == 220.0
          and p3["ordenes_ultima_hora"] == 1, (p3["importe_dia_eur"], p3["ordenes_ultima_hora"]))
    # ---------------------------------------------------------------- el hash cubre los campos nuevos
    o = propuesta(); F = informe_f(o)
    p = o.pantalla_aprobacion(EID, F, AHORA)["pantalla"]
    guardada = {k: v for k, v in o.pantallas[EID].items() if k != "usada"}
    h.chk("el_hash_guardado_cubre_toda_la_pantalla", guardada["hash"] == _hash({k: v for k, v in guardada.items() if k != "hash"}))
    OTRO = {"precio_intermediario": 1.11, "precio_intermediario_en": "2026-11-06T08:59:00+00:00", "deriva_pct": 0.9009,
            "importe_dia_eur": 111.0, "limite_dia_eur": 49999.0, "perdida_semana_eur": 1.0, "limite_semana_eur": 4999.0,
            "ordenes_ultima_hora": 1, "limite_ordenes_hora": 9, "eventos_f": [{"fecha": "2026-11-07", "tipo": "RESULTADOS"}]}
    for campo in NUEVOS:
        tocada = {**guardada, campo: OTRO[campo]}
        tocada.pop("hash")
        h.chk(f"el_hash_cubre_{campo}", _hash(tocada) != guardada["hash"])
    h.chk("dos_pantallas_del_mismo_informe_mismo_hash",
          (p2 := o.pantalla_aprobacion(EID, F, AHORA)["pantalla"])["hash"] == p["hash"]
          and all(p2[c] == p[c] for c in NUEVOS), p2["hash"])
    # ---------------------------------------------------------------- la pantalla sigue siendo solo cifras
    h.chk("la_pantalla_sigue_sin_textos", not any(k in p for k in ("texto", "resumen", "tesis", "tesis_resumen"))
          and all(not isinstance(v, str) or k in ("informe_f_hash", "hash", "instrumento", "via_acceso", "direccion", "fecha_revision",
                                                  "unidad_importe", "divisa_cotizacion", "cartera", "valid_until_f", "generada_en",
                                                  "caduca_en", "enfriamiento_hasta", "resultado_f", "expediente_id", "informe_f",
                                                  "precio_intermediario_en") for k, v in p.items()), sorted(p))
    # ---------------------------------------------------------------- anulación de veto: el importe del día usa la cantidad anulada
    # F-14 recorta la anulación (E no lo ve: va en el contexto, y el recálculo de E va sin él): con 110 EUR ya autorizados hoy
    # e importe_max_dia_eur 205, el tope F-14 deja 86.363636 unidades (95.0 EUR) y F-11 veta porque no llega al valor mínimo.
    # importe_max_orden_eur sube a 120 para que F-13 (que E sí ve) no recorte la propuesta de 100 unidades.
    o = nuevo({"politica_f": {**POLITICA_DEFECTO, "importe_max_orden_eur": 120.0, "importe_max_dia_eur": 205.0}})
    hasta(o, "AUTORIZADA")
    hasta(o, "PROPUESTA", n=3)
    inf = informe_f(o, "EXP-0003", n=3, cartera={"posiciones": POS10})   # F-09 veta; F-14 recorta y F-11 veta por valor mínimo
    vetos = [c["regla"] for c in aplanar_informe(inf)["controles"] if c["resultado"] == "VETA"]
    h.chk("el_informe_veta_f09_y_f11", sorted(vetos) == ["F-09", "F-11"], vetos)
    r = o.pantalla_aprobacion("EXP-0003", inf, AHORA, anular_veto={"motivo": MOTIVO})
    p = r["pantalla"]
    h.chk("pantalla_de_anulacion_con_la_cantidad_anulada", r["ok"] and p["resultado_f"] == "VETADO"
          and p["anulacion"]["vetos"] == ["F-09", "F-11"] and p["cantidad"] == 86.363636 != 100.0
          and p["importe"] == 95.0, (p.get("cantidad"), p.get("importe")))
    h.chk("el_importe_del_dia_usa_la_cantidad_anulada", p["importe_dia_eur"] == round(110.0 + p["importe"], 2) == 205.0 != 220.0,
          p["importe_dia_eur"])
    h.chk("los_campos_nuevos_tambien_en_la_anulacion",
          p["precio_intermediario"] == aplanar_informe(inf)["entradas"]["contexto"]["precio_intermediario"]["valor"]
          and p["limite_dia_eur"] == 205.0 and p["limite_ordenes_hora"] == 10)
    h.chk("anulacion_autoriza_tras_el_enfriamiento", o.autorizar("EXP-0003", "OPERADOR", inf, T_ESPERA, aprob(p))["ok"]
          and o.expedientes["EXP-0003"]["estado"] == "AUTORIZADA")
    print(f"\n{h.n} comprobaciones")
    print("RESULTADO PANTALLA F:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
