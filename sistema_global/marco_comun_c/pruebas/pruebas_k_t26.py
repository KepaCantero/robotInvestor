"""Pruebas de T-26 (parte 2): procedencia, licencia, consulta «punto en el tiempo» y calendario de eventos de K (sello
0.2.0, Q-14, Q-15 y S-14), el calendario en la pantalla del operador y el contraste de los tipos de cambio de G con K (T-42).
Datos SIMULADOS."""
from __future__ import annotations

import copy
import sys
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from k_calidad import (LICENCIAS, VERSION_SELLO, construir_sello, eventos_entre, hash_del_sello, punto_en_el_tiempo,  # noqa: E402
                       validar_sello)
from orquestador import Orquestador  # noqa: E402
from pruebas_k import CAL, CTX, EVENTO, PROC, construir, entrada_base, rehash  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_orquestador import AHORA, CFG, Arnes, hasta, nuevo  # noqa: E402


def reglas_no_ok(r):
    return {x["regla"]: x["resultado"] for x in r["resultados"] if x["resultado"] != "OK"}


def fuente(e, fid):
    return next(f for f in e["fuentes"] if f["fuente_id"] == fid)


def foto(usd, hora="2026-11-06T08:55:00+00:00"):
    return {"fecha_hora": hora, "capital_eur": 100000.0, "perdida_dia_eur": 0.0, "posiciones": [], "tipos_cambio_eur": {"USD": usd}}


def main():
    h = Arnes()

    # ================================================================ Q-14 procedencia y licencia
    _, r = construir()
    s = r["sello"]
    f0 = next(x for x in s["fuentes"] if x["fuente_id"] == "SRC-EURUSD")
    h.chk("sello_020_con_procedencia", s["version_esquema"] == VERSION_SELLO == "0.2.0" and f0["procedencia"]["licencia"] in LICENCIAS
          and f0["instrumento"] == "EURUSD" and f0["ultimo_cierre"] > 0 and s["eventos"] == [] and validar_sello(s, {"calendario": CAL}) == [])
    casos = (("sin_procedencia", lambda e: fuente(e, "SRC-GBPUSD").pop("procedencia")),
             ("procedencia_incompleta", lambda e: fuente(e, "SRC-GBPUSD")["procedencia"].pop("referencia")),
             ("licencia_no_admitida", lambda e: fuente(e, "SRC-GBPUSD").update(procedencia=PROC("SRC-GBPUSD", licencia="SOLO-LECTURA-WEB"))),
             ("obtenido_despues_de_emitir", lambda e: fuente(e, "SRC-GBPUSD").update(procedencia=PROC("SRC-GBPUSD", "2026-11-06T09:00:00+00:00"))),
             ("dato_posterior_a_su_obtencion", lambda e: fuente(e, "SRC-GBPUSD").update(procedencia=PROC("SRC-GBPUSD", "2026-11-04T20:00:00+00:00"))),
             ("obtenido_mal_formado", lambda e: fuente(e, "SRC-GBPUSD").update(procedencia=PROC("SRC-GBPUSD", "2026-11-05"))),
             ("referencia_vacia", lambda e: fuente(e, "SRC-GBPUSD")["procedencia"].update(referencia="  ")),
             ("proveedor_mal_formado", lambda e: fuente(e, "SRC-GBPUSD")["procedencia"].update(proveedor="prov sim")))
    for nombre, mut in casos:
        _, r = construir(mut)
        h.chk(f"Q14_{nombre}_bloquea", r["sello"] is None and reglas_no_ok(r).get("Q-14") == "BLOQUEO", reglas_no_ok(r))
    # R-G3: la barra de un día solo existe tras su cierre (22:00 UTC en FX): obtenerla antes es look-ahead
    for nombre, cuando in (("medianoche_utc", "2026-11-05T00:00:01+00:00"), ("vispera_en_hora_local", "2026-11-04T19:00:01-05:00"),
                           ("antes_del_cierre", "2026-11-05T21:59:00+00:00")):
        _, r = construir(lambda e, c=cuando: [f.update(procedencia=PROC(f["fuente_id"], c)) for f in e["fuentes"]])
        h.chk(f"RG3_{nombre}_bloquea", r["sello"] is None and reglas_no_ok(r).get("Q-14") == "BLOQUEO", reglas_no_ok(r))
    _, r = construir(lambda e: [f.update(procedencia=PROC(f["fuente_id"], "2026-11-06T07:30:00+09:00")) for f in e["fuentes"]])   # 22:30Z del 5
    h.chk("RG3_tras_el_cierre_en_otra_zona_vale", r["sello"] is not None, reglas_no_ok(r))
    _, r = construir(lambda e: e["fuentes"].append({"fuente_id": "SRC-CAIDA", "disponible": False}))
    h.chk("Q14_fuente_no_disponible_no_necesita_procedencia", r["sello"] is not None)

    # ---------------------------------------------------------------- S-14 sobre el sello emitido
    def cambia(fn):
        x = copy.deepcopy(s); fn(x); x["hash_sello"] = hash_del_sello(x); return x
    for nombre, fn in (("licencia", lambda x: x["fuentes"][0]["procedencia"].update(licencia="SOLO-LECTURA-WEB")),
                       ("obtenido_tras_emitir", lambda x: x["fuentes"][0]["procedencia"].update(obtenido_en="2026-11-06T09:00:00+00:00")),
                       ("observacion_tras_obtener", lambda x: x["fuentes"][0]["procedencia"].update(obtenido_en="2026-11-04T07:00:00+00:00"))):
        obt = {y["regla"] for y in validar_sello(cambia(fn), {"calendario": CAL})}
        h.chk(f"S14_{nombre}", obt == {"S-14"}, obt)
    obt = {y["regla"] for y in validar_sello(cambia(lambda x: x["fuentes"][0].pop("procedencia")), {"calendario": CAL})}
    h.chk("S01_disponible_sin_procedencia", obt == {"S-01"}, obt)
    obt = {y["regla"] for y in validar_sello(cambia(lambda x: x.update(version_esquema="0.1.0")), {"calendario": CAL})}
    h.chk("S01_version_010_ya_no_vale", "S-01" in obt, obt)

    # ================================================================ Q-15 calendario de eventos
    BCE = EVENTO("2026-11-12", ["EURUSD"], tipo="BANCO_CENTRAL", descripcion="reunión del BCE")
    _, r = construir(lambda e: e["eventos"].extend([BCE, EVENTO("2026-10-15", ["GBPUSD"])]))
    s2 = r["sello"]
    h.chk("calendario_en_el_sello", s2 is not None and [x["fecha"] for x in s2["eventos"]] == ["2026-10-15", "2026-11-12"]
          and validar_sello(s2, {"calendario": CAL}) == [], s2 and s2["eventos"])
    h.chk("evento_futuro_programado_vale", s2["eventos"][1]["tipo"] == "BANCO_CENTRAL")
    for nombre, ev in (("sin_anunciado_en", {k: v for k, v in BCE.items() if k != "anunciado_en"}),
                       ("anunciado_tras_emitir", {**BCE, "anunciado_en": "2026-11-06T09:00:00+00:00"}),
                       ("tipo_desconocido", {**BCE, "tipo": "RUMOR"}), ("sin_instrumentos", {**BCE, "instrumentos": []}),
                       ("descripcion_vacia", {**BCE, "descripcion": ""}), ("clave_extra", {**BCE, "evento_id": "EV-1"})):
        _, r = construir(lambda e, ev=ev: e["eventos"].append(ev))
        h.chk(f"Q15_{nombre}_bloquea", r["sello"] is None and reglas_no_ok(r).get("Q-15") == "BLOQUEO", reglas_no_ok(r))
    x2 = copy.deepcopy(s2); x2["eventos"][0]["anunciado_en"] = "2026-11-06T09:00:00+00:00"; x2["hash_sello"] = hash_del_sello(x2)
    obt = {y["regla"] for y in validar_sello(x2, {"calendario": CAL})}
    h.chk("S14_evento_anunciado_tras_emitir", obt == {"S-14"}, obt)
    x3 = copy.deepcopy(s2); x3["eventos"][0]["fecha"] = "2026-02-30"; x3["hash_sello"] = hash_del_sello(x3)
    h.chk("RM2_evento_con_fecha_imposible_S14", "S-14" in {y["regla"] for y in validar_sello(x3, {"calendario": CAL})} and eventos_entre(x3, "2026-01-01", "2026-12-31") is None)
    h.chk("eventos_entre_filtra", [x["descripcion"] for x in eventos_entre(s2, "2026-11-06", "2026-12-05", "EUR/USD")] == ["reunión del BCE"]
          and eventos_entre(s2, "2026-11-06", "2026-12-05", "GBPUSD") == [] and len(eventos_entre(s2, "2026-10-01", "2026-12-31")) == 2)
    h.chk("eventos_entre_no_lanza_y_distingue_ilegible", eventos_entre(None, "x", "y") is None and eventos_entre(s2, "2026-11-06", "mañana") is None
          and eventos_entre({"eventos": []}, "2026-11-06", "2026-12-05") == [])

    # ================================================================ consulta punto en el tiempo
    e = entrada_base()
    v1 = copy.deepcopy(fuente(e, "SRC-EURUSD"))
    v1.update(fuente_id="SRC-EURUSD-V1", version_conjunto="DS-1", serie=[o for o in v1["serie"] if o["fecha"] <= "2026-11-04"],
              procedencia=PROC("SRC-EURUSD-V1", "2026-11-04T22:30:00+00:00"))
    v2 = copy.deepcopy(fuente(e, "SRC-EURUSD"))
    v2.update(fuente_id="SRC-EURUSD-V2", version_conjunto="DS-2", procedencia=PROC("SRC-EURUSD-V2", "2026-11-05T22:30:00+00:00"))
    for o in v2["serie"]:
        if o["fecha"] == "2026-11-04":
            o["cierre"] = round(o["cierre"] * 1.001, 6)   # el proveedor revisó el cierre del día 4: el original no se sobrescribe
    c4_v1 = next(o["cierre"] for o in v1["serie"] if o["fecha"] == "2026-11-04")
    c4_v2 = next(o["cierre"] for o in v2["serie"] if o["fecha"] == "2026-11-04")
    fs = [v1, v2]
    r1 = punto_en_el_tiempo(fs, "EURUSD", "2026-11-04", "2026-11-04T23:00:00+00:00", CAL)
    r2 = punto_en_el_tiempo(fs, "EURUSD", "2026-11-04", "2026-11-05T23:00:00+00:00", CAL)
    h.chk("pit_lo_que_se_sabia_entonces", r1 and r1["cierre"] == c4_v1 and r1["version_conjunto"] == "DS-1", r1)
    h.chk("pit_la_revision_despues", r2 and r2["cierre"] == c4_v2 and r2["version_conjunto"] == "DS-2" and c4_v1 != c4_v2, r2)
    r3 = punto_en_el_tiempo(fs, "EURUSD", "2026-11-05", "2026-11-04T23:00:00+00:00", CAL)
    h.chk("pit_sin_look_ahead", r3 and r3["fecha"] == "2026-11-04" and r3["cierre"] == c4_v1, r3)
    h.chk("pit_antes_de_obtener_nada", punto_en_el_tiempo(fs, "EURUSD", "2026-11-04", "2026-11-04T10:00:00+00:00", CAL) is None)
    r4 = punto_en_el_tiempo(fs, "EURUSD", "2026-11-04", "2026-11-04T23:00:00+00:00")   # sin calendario: el cierre existe al día siguiente
    h.chk("pit_sin_calendario_prudente", r4 and r4["fecha"] == "2026-11-03", r4)
    # R-M1: dos versiones obtenidas en el mismo instante que no coinciden: no se elige
    v3 = copy.deepcopy(v2); v3.update(fuente_id="SRC-EURUSD-V3", procedencia=PROC("SRC-EURUSD-V3", "2026-11-05T23:30:00+01:00"))
    for o in v3["serie"]:
        if o["fecha"] == "2026-11-04":
            o["cierre"] = round(o["cierre"] * 1.05, 6)
    h.chk("RM1_empate_que_no_coincide_None", punto_en_el_tiempo([v1, v2, v3], "EURUSD", "2026-11-04", "2026-11-05T23:00:00+00:00", CAL) is None)
    v4 = copy.deepcopy(v2); v4.update(fuente_id="SRC-EURUSD-V4", procedencia=PROC("SRC-EURUSD-V4", "2026-11-05T23:30:00+01:00"))
    h.chk("RM1_empate_que_coincide_responde", (punto_en_el_tiempo([v1, v2, v4], "EURUSD", "2026-11-04", "2026-11-05T23:00:00+00:00", CAL) or {}).get("cierre") == c4_v2)
    h.chk("pit_instrumento_desconocido", punto_en_el_tiempo(fs, "GBPUSD", "2026-11-04", "2026-11-05T23:00:00+00:00", CAL) is None)
    h.chk("pit_licencia_no_admitida_no_cuenta",
          punto_en_el_tiempo([{**v2, "procedencia": PROC("X", "2026-11-05T22:30:00+00:00", "SOLO-LECTURA-WEB")}], "EURUSD", "2026-11-04",
                             "2026-11-05T23:00:00+00:00", CAL) is None)
    h.chk("pit_no_lanza", punto_en_el_tiempo(None, "EURUSD", "2026-11-04", "x") is None and punto_en_el_tiempo([7], "EURUSD", "2026-11-04",
                                                                                                        "2026-11-05T20:00:00+00:00") is None)

    # ================================================================ el calendario llega al operador
    _, r = construir(lambda x: x["eventos"].extend([BCE, EVENTO("2026-12-20", ["EURUSD"], descripcion="después de la revisión"),
                                                     EVENTO("2026-11-10", ["GBPUSD"], descripcion="otro par")]))
    o = nuevo(sellos=(r["sello"],))
    hasta(o, "PROPUESTA")
    p = o.pantalla_aprobacion("EXP-0001", informe_f(o), AHORA)["pantalla"]
    h.chk("pantalla_con_los_eventos_hasta_la_revision", [x["descripcion"] for x in p["eventos_k"]] == ["reunión del BCE"], p["eventos_k"])

    # ================================================================ T-42 contraste de tipos de cambio con K
    o = Orquestador({**CFG, "tolerancia_tipo_k_rel": 0.03}, CAL)
    assert o.registrar_sello(s, AHORA)["ok"]
    k = 1 / f0["ultimo_cierre"]
    r = o.registrar_cartera(foto(1.35), "G", AHORA, cuenta="SIM-1")
    h.chk("T42_tipo_lejos_de_K_O29", r["codigo"] == "O-29" and "K" in r["motivo"], r)
    h.chk("T42_tipo_cerca_de_K_vale", o.registrar_cartera(foto(round(k * 1.02, 6)), "G", AHORA, cuenta="SIM-1")["ok"])
    # R-G1: un sello más reciente sin el par no apaga el contraste; R-G2: el par en otra grafía también cuenta
    def sin_eur(e):
        e["fuentes"] = [f for f in e["fuentes"] if "EUR" not in f["fuente_id"]]
        e["cruces"] = []
    _, r = construir(sin_eur, hasta=date(2026, 11, 5), solicitada="2026-11-06")
    o3 = Orquestador({**CFG, "tolerancia_tipo_k_rel": 0.03}, CAL)
    assert o3.registrar_sello(s, AHORA)["ok"] and o3.registrar_sello(r["sello"], AHORA)["ok"]
    h.chk("RG1_sello_reciente_sin_el_par_no_apaga_T42", o3.registrar_cartera(foto(1.35), "G", AHORA, cuenta="SIM-1")["codigo"] == "O-29")
    for grafia in ("EUR/USD", "eurusd", "EUR-USD"):
        _, r = construir(lambda e, g=grafia: [f.update(instrumento=g) for f in e["fuentes"] if f["fuente_id"] in ("SRC-EURUSD", "SRC-EURUSD-B")])
        o4 = Orquestador({**CFG, "tolerancia_tipo_k_rel": 0.03}, CAL)
        assert o4.registrar_sello(r["sello"], AHORA)["ok"]
        h.chk(f"RG2_par_escrito_{grafia}_cuenta", o4.registrar_cartera(foto(1.35), "G", AHORA, cuenta="SIM-1")["codigo"] == "O-29")
    # R-m2: un cierre subnormal no anula el contraste
    xs = copy.deepcopy(s)
    for x in xs["fuentes"]:
        if x.get("instrumento") == "EURUSD":
            x["ultimo_cierre"] = 5e-324
    xs["hash_sello"] = hash_del_sello(xs)
    o5 = Orquestador({**CFG, "tolerancia_tipo_k_rel": 0.03}, CAL)
    assert o5.registrar_sello(xs, AHORA)["ok"]
    h.chk("Rm2_cierre_subnormal_O29", o5.registrar_cartera(foto(1.39), "G", AHORA, cuenta="SIM-1")["codigo"] == "O-29")
    o2 = Orquestador({**CFG, "tolerancia_tipo_k_rel": 0.03}, CAL)
    h.chk("T42_sin_sello_no_hay_contraste", o2.registrar_cartera(foto(1.0), "G", AHORA, cuenta="SIM-1")["ok"])
    for nombre, v in (("cero", 0), ("demasiado", 0.6), ("texto", "0.03"), ("bool", True)):
        try:
            Orquestador({**CFG, "tolerancia_tipo_k_rel": v}, CAL)
            h.chk(f"config_tolerancia_{nombre}_se_rechaza", False)
        except ValueError:
            h.chk(f"config_tolerancia_{nombre}_se_rechaza", True)
    c = Orquestador({k_: v_ for k_, v_ in CFG.items() if k_ != "tolerancia_tipo_k_rel"}, CAL).configuracion()
    h.chk("config_060_tolerancia_por_defecto", c["version_config"] >= "CFG-0.6.0" and c["orquestador"]["tolerancia_tipo_k_rel"] == 0.03)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO K T-26:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
