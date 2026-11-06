"""Pruebas de T-03 (primera parte, V0.42): guardar y volver a cargar el estado del Orquestador sin perder nada y sin fiarse
del fichero (PE-01 a PE-05 y O-13 con kill-switch si no cuadra). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_persistencia_t03.py
"""
import copy
import json
import os
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))
import persistencia as pe  # noqa: E402
from ejecucion_g import conciliar, ejecutar, reducir  # noqa: E402
from pruebas_control_f import informe_f  # noqa: E402
from pruebas_ejecucion_g import autorizado, broker  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, autorizar_op, hasta, nuevo  # noqa: E402

T = "2026-11-06T09:30:00+00:00"


def rehacer(texto, cambio):
    """Aplica `cambio` al estado de un volcado y rehace la huella (lo que haría quien edita el fichero sabiendo cómo)."""
    d = json.loads(texto)
    cambio(d)
    d["atributos"] = sorted(d["estado"])
    d["huella"] = pe._huella(d["estado"])
    return pe._texto(d)


def ida_y_vuelta(o):
    t = pe.volcar(o, T)
    r = pe.cargar(t)
    return t, r, (pe.volcar(r["orquestador"], T) if r["orquestador"] else None)


def main():
    h = Arnes()

    # ------------------------------------------------------------------ ida y vuelta en distintos estados
    estados = {}
    o = nuevo(); estados["recien_creado"] = o
    o = nuevo(); hasta(o, "PROPUESTA"); estados["propuesta"] = o
    o, b = autorizado(); estados["autorizada"] = o
    o, b = autorizado(); assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]; estados["posicion_abierta"] = o
    conciliar(o, b, AHORA)
    estados["conciliada"] = o
    o, b = autorizado(); assert ejecutar(o, "EXP-0001", b, AHORA)["ok"]
    pid = next(iter(o.posiciones))
    rr = reducir(o, pid, b, AHORA, cantidad=o.posiciones[pid]["cantidad"] / 2, actor="OPERADOR", motivo="Reducción de prueba de la persistencia")
    estados["tras_reducir"] = o
    o = nuevo(); hasta(o, "PROPUESTA"); o.activar_kill_switch("prueba de persistencia", "OPERADOR", AHORA); estados["con_kill_switch"] = o
    for nombre, o in estados.items():
        t, r, t2 = ida_y_vuelta(o)
        h.chk(f"ida_y_vuelta_{nombre}", r["ok"] and r["codigo"] == "OK" and t2 == t and r["orquestador"].integridad() == [], (r["codigo"], r["motivo"]))
    h.chk("la_reduccion_de_prueba_se_hizo", rr["ok"] and estados["tras_reducir"].posiciones[pid]["reducciones"] != [], rr)
    d = json.loads(pe.volcar(estados["posicion_abierta"], T))
    h.chk("documento_con_su_forma", set(d) == pe.CLAVES and d["formato"] == pe.FORMATO and d["atributos"] == sorted(vars(estados["posicion_abierta"]))
          and len(d["huella"]) == 64 and d["version_config"] == estados["posicion_abierta"].cfg["version_config"])
    h.chk("volcar_es_determinista", pe.volcar(estados["conciliada"], T) == pe.volcar(estados["conciliada"], T))

    # ------------------------------------------------------------------ continuidad: lo cargado se comporta igual que lo original
    o1, b1 = autorizado()
    o2 = pe.cargar(pe.volcar(o1, T))["orquestador"]
    b2 = broker()
    r1, r2 = ejecutar(o1, "EXP-0001", b1, AHORA), ejecutar(o2, "EXP-0001", b2, AHORA)
    h.chk("continuidad_ejecutar_igual", r1 == r2 and pe.volcar(o1, T) == pe.volcar(o2, T), (r1, r2))
    c1, c2 = conciliar(o1, b1, AHORA), conciliar(o2, b2, AHORA)
    h.chk("continuidad_conciliar_igual", c1 == c2 and pe.volcar(o1, T) == pe.volcar(o2, T))
    o3 = nuevo(); hasta(o3, "PROPUESTA")
    o4 = pe.cargar(pe.volcar(o3, T))["orquestador"]
    inf3, inf4 = informe_f(o3), informe_f(o4)
    h.chk("continuidad_autorizar_igual", autorizar_op(o3, "EXP-0001", inf3, AHORA) == autorizar_op(o4, "EXP-0001", inf4, AHORA)
          and pe.volcar(o3, T) == pe.volcar(o4, T))
    h.chk("lo_cargado_es_independiente", (lambda t: (pe.cargar(t)["orquestador"].avisos.append({"x": 1}), pe.volcar(pe.cargar(t)["orquestador"], T) == t)[1])(pe.volcar(o3, T)))

    # ------------------------------------------------------------------ el reloj y el kill-switch sobreviven al reinicio
    o = pe.cargar(pe.volcar(estados["posicion_abierta"], T))["orquestador"]
    h.chk("el_reloj_no_retrocede_tras_cargar", o.ultimo_ahora == estados["posicion_abierta"].ultimo_ahora
          and o.registrar_cotizacion({"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": "2026-11-06T08:00:00+00:00"}, "G", "2026-11-06T08:00:00+00:00")["codigo"] == "O-16")
    o = pe.cargar(pe.volcar(estados["con_kill_switch"], T))["orquestador"]
    h.chk("el_kill_switch_sigue_activo_tras_cargar", o.kill is not None and o.kill["motivo"] == "prueba de persistencia"
          and autorizar_op(o, "EXP-0001", informe_f(o), AHORA)["codigo"] == "O-26")

    # ------------------------------------------------------------------ guardar en disco
    with tempfile.TemporaryDirectory() as d:
        ruta = os.path.join(d, "estado.json")
        g1 = pe.guardar(estados["propuesta"], ruta, T)
        g2 = pe.guardar(estados["posicion_abierta"], ruta, T)   # sustituye al anterior
        r = pe.cargar_de(ruta)
        h.chk("guardar_y_cargar_de_disco", g1["ok"] and g2["ok"] and r["ok"] and pe.volcar(r["orquestador"], T) == pe.volcar(estados["posicion_abierta"], T)
              and g2["huella"] == json.loads(pe.volcar(estados["posicion_abierta"], T))["huella"], (g1, g2, r["codigo"]))
        h.chk("guardar_no_deja_temporales", sorted(os.listdir(d)) == ["estado.json"], os.listdir(d))
        h.chk("guardar_en_carpeta_inexistente_PE05", pe.guardar(estados["propuesta"], os.path.join(d, "no", "existe.json"), T)["codigo"] == "PE-05")
        h.chk("cargar_fichero_inexistente_PE05", pe.cargar_de(os.path.join(d, "nada.json"))["codigo"] == "PE-05")
        with open(os.path.join(d, "binario.json"), "wb") as f:
            f.write(b"\xff\xfe\x00rompe")
        h.chk("cargar_fichero_no_utf8_PE05", pe.cargar_de(os.path.join(d, "binario.json"))["codigo"] == "PE-05")
    h.chk("guardar_con_instante_ilegible_PE01", pe.guardar(estados["propuesta"], "/tmp/x.json", "ayer")["codigo"] == "PE-01")

    # ------------------------------------------------------------------ PE-01 a PE-04: lo que no se monta
    t = pe.volcar(estados["autorizada"], T)
    for nombre, texto in (("no_es_json", "{roto"), ("vacio", ""), ("lista", "[]"), ("con_NaN", t.replace('"version_config":', '"x":NaN,"version_config":', 1)),
                          ("sin_huella", pe._texto({k: v for k, v in json.loads(t).items() if k != "huella"})),
                          ("clave_de_mas", pe._texto({**json.loads(t), "extra": 1})),
                          ("huella_no_hex", pe._texto({**json.loads(t), "huella": "z" * 64})),
                          ("estado_no_objeto", pe._texto({**json.loads(t), "estado": []})),
                          ("guardado_en_ilegible", pe._texto({**json.loads(t), "guardado_en": "ayer"}))):
        r = pe.cargar(texto)
        h.chk(f"PE01_{nombre}", r["codigo"] == "PE-01" and r["orquestador"] is None, r["codigo"])
    d = json.loads(t)
    d["estado"]["ultimo_ahora"] = "2026-11-05T00:00:00+00:00"   # se atrasa el reloj sin rehacer la huella
    h.chk("PE02_estado_tocado_sin_rehacer_la_huella", pe.cargar(pe._texto(d))["codigo"] == "PE-02")
    for nombre, cambio in (("formato", lambda x: x.__setitem__("formato", "ESTADO-ORQUESTADOR-9.9.9")),
                           ("version_config", lambda x: x.__setitem__("version_config", "CFG-0.1.0")),
                           ("version_de_la_cfg_guardada", lambda x: x["estado"]["cfg"].__setitem__("version_config", "CFG-0.1.0")),
                           ("falta_un_atributo", lambda x: x["estado"].pop("cotizaciones")),
                           ("sobra_un_atributo", lambda x: x["estado"].__setitem__("puerta_trasera", {}))):
        r = pe.cargar(rehacer(t, cambio))
        h.chk(f"PE03_{nombre}", r["codigo"] == "PE-03" and r["orquestador"] is None, (r["codigo"], r["motivo"]))
    d = json.loads(t)
    d["atributos"] = sorted(d["atributos"] + ["otro"])
    d["huella"] = pe._huella(d["estado"])
    h.chk("PE03_lista_de_atributos_que_no_es_la_del_estado", pe.cargar(pe._texto(d))["codigo"] == "PE-03")
    for nombre, cambio in (("politica_invalida", lambda x: x["estado"]["cfg"]["politica_f"].__setitem__("riesgo_max_pct", -1)),
                           ("clave_de_cfg_desconocida", lambda x: x["estado"]["cfg"].__setitem__("errata", 1)),
                           ("calendario_invalido", lambda x: x["estado"].__setitem__("cal_def", "no es un calendario"))):
        r = pe.cargar(rehacer(t, cambio))
        h.chk(f"PE04_{nombre}", r["codigo"] == "PE-04" and r["orquestador"] is None, (r["codigo"], r["motivo"]))
    r = pe.cargar(rehacer(t, lambda x: x["estado"].__setitem__("expedientes", "no es un diccionario")))
    h.chk("PE04_estado_que_no_se_puede_comprobar", r["codigo"] == "PE-04" and r["orquestador"] is None, (r["codigo"], r["motivo"]))

    # ------------------------------------------------------------------ O-13: se monta, no cuadra, kill-switch
    def toca_historial(x):
        x["estado"]["expedientes"]["EXP-0001"]["historial"][-1]["motivo"] = "lo cambió alguien"
    r = pe.cargar(rehacer(t, toca_historial))
    o = r["orquestador"]
    h.chk("O13_historial_tocado_carga_con_kill_switch", r["codigo"] == "O-13" and o is not None and o.kill is not None
          and "EXP:EXP-0001" in r["integridad"] and any(a["codigo"] == "O-26" for a in o.avisos), (r["codigo"], r.get("integridad")))
    h.chk("O13_y_no_se_puede_operar", o.orden_entrada("EXP-0001", "ORD-X", "ENVIADA", 0.0, "G", AHORA)["ok"] is False)
    r = pe.cargar(rehacer(t, lambda x: x["estado"]["cfg"].__setitem__("alerta_perdida_pct", -7.0)))   # válida, pero no la de la huella
    h.chk("O13_configuracion_cambiada_es_CONFIG", r["codigo"] == "O-13" and "CONFIG" in r["integridad"], (r["codigo"], r.get("integridad")))
    tp = pe.volcar(estados["posicion_abierta"], T)
    pid = next(iter(estados["posicion_abierta"].posiciones))
    r = pe.cargar(rehacer(tp, lambda x: x["estado"]["posiciones"][pid].__setitem__("cantidad", 1.0)))
    h.chk("O13_posicion_tocada_es_POS", r["codigo"] == "O-13" and f"POS:{pid}" in r["integridad"], (r["codigo"], r.get("integridad")))

    # ------------------------------------------------------------------ lo que JSON no guarda tal cual no se vuelca
    o = nuevo()
    o.degradadas = {"TACTICA": ("motivo", "tupla")}
    try:
        pe.volcar(o, T)
        h.chk("volcar_rechaza_tuplas", False)
    except ValueError as ex:
        h.chk("volcar_rechaza_tuplas", "degradadas" in str(ex), str(ex))
    o = nuevo()
    o.avisos.append({"x": float("nan")})
    h.chk("guardar_rechaza_NaN_PE01", pe.guardar(o, "/tmp/nunca.json", T)["codigo"] == "PE-01" and not os.path.exists("/tmp/nunca.json"))
    o = nuevo()
    o.fotos = {1: "clave no textual"}
    h.chk("volcar_rechaza_claves_no_textuales", pe.guardar(o, "/tmp/nunca.json", T)["codigo"] == "PE-01")

    # ------------------------------------------------------------------ regresiones de la revisión independiente de T-03
    o = nuevo()
    hasta(o, "EN_ANALISIS", n=2); hasta(o, "EN_ANALISIS", n=1)   # se crean EXP-0002 y luego EXP-0001
    c = pe.cargar(pe.volcar(o, T))["orquestador"]
    h.chk("r01_se_conserva_el_orden_de_insercion", list(c.expedientes) == list(o.expedientes) == ["EXP-0002", "EXP-0001"]
          and list(c.encargos) == list(o.encargos), (list(c.expedientes), list(o.expedientes)))
    ra, rb = o.barrer("2026-12-31T00:00:00+00:00"), c.barrer("2026-12-31T00:00:00+00:00")
    h.chk("r01_y_se_comporta_igual_al_barrer", ra == rb and o.avisos == c.avisos and pe.volcar(o, T) == pe.volcar(c, T), (ra, rb))
    t = pe.volcar(estados["autorizada"], T)
    r = pe.cargar(rehacer(t, lambda x: x["estado"]["cfg"].pop("avisos")))
    h.chk("r02_configuracion_guardada_incompleta_PE04_sin_lanzar", r["codigo"] == "PE-04" and r["orquestador"] is None, (r["codigo"], r["motivo"]))
    o = nuevo(); hasta(o, "PROPUESTA")
    o.activar_kill_switch("motivo con un surrogado suelto \udc80 que no es UTF-8", "OPERADOR", AHORA)
    with tempfile.TemporaryDirectory() as d:
        g = pe.guardar(o, os.path.join(d, "e.json"), T)
        r = pe.cargar_de(os.path.join(d, "e.json"))
        h.chk("r03_un_texto_con_surrogado_se_guarda_y_vuelve_igual", g["ok"] and r["ok"] and r["orquestador"].kill == o.kill
              and pe.volcar(r["orquestador"], T) == pe.volcar(o, T), (g, r["codigo"]))
    o = nuevo(); hasta(o, "AUTORIZADA")
    o.activar_kill_switch("kill previo", "OPERADOR", AHORA)
    for a_ in o.avisos:
        a_["acusado"] = True
    def rompe(x):
        x["estado"]["expedientes"]["EXP-0001"]["historial"][-1]["motivo"] = "tocado"
    r = pe.cargar(rehacer(pe.volcar(o, T), rompe))
    nuevos = [a_ for a_ in r["orquestador"].avisos if a_["codigo"] == "O-13" and not a_.get("acusado")]
    h.chk("r04_con_kill_previo_queda_un_aviso_O13_sin_acusar", r["codigo"] == "O-13" and len(nuevos) == 1, r["orquestador"].avisos[-2:])
    o = nuevo({"version_config": "CFG-0.1.1"})
    with tempfile.TemporaryDirectory() as d:
        g = pe.guardar(o, os.path.join(d, "e.json"), T)
        r = pe.cargar_de(os.path.join(d, "e.json"))
        h.chk("r05_una_version_de_configuracion_propia_se_vuelve_a_cargar", g["ok"] and r["ok"], (g, r["codigo"], r["motivo"]))
    r = pe.cargar(rehacer(t, lambda x: (x.__setitem__("version_config", "CFG-0.9.9"), x["estado"]["cfg"].__setitem__("version_config", "CFG-0.9.9"))))
    h.chk("r05_cambiar_la_version_en_los_dos_sitios_lo_ve_CONFIG", r["codigo"] == "O-13" and "CONFIG" in r["integridad"], (r["codigo"], r.get("integridad")))
    h.chk("r06_rutas_raras_no_lanzan", pe.guardar(estados["propuesta"], "a\x00b", T)["codigo"] == "PE-05"
          and pe.guardar(estados["propuesta"], None, T)["codigo"] == "PE-05"
          and pe.cargar_de("a\x00b")["codigo"] == "PE-05" and pe.cargar_de(None)["codigo"] == "PE-05")
    viejo = pe.MAX_BYTES
    try:
        pe.MAX_BYTES = 1000
        with tempfile.TemporaryDirectory() as d:
            pe.guardar(estados["propuesta"], os.path.join(d, "e.json"), T)
            h.chk("r07_un_fichero_mayor_que_el_maximo_no_se_lee", pe.cargar_de(os.path.join(d, "e.json"))["codigo"] == "PE-05")
    finally:
        pe.MAX_BYTES = viejo
    try:
        pe.volcar(estados["propuesta"], "2026-13-45T99:99:99Z")
        h.chk("r08_instante_imposible_no_se_vuelca", False)
    except ValueError:
        h.chk("r08_instante_imposible_no_se_vuelca", True)
    h.chk("r08_digitos_no_ascii_PE01", pe.cargar(pe._texto({**json.loads(t), "guardado_en": "２026-11-06T09:30:00+00:00"}))["codigo"] == "PE-01")

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO PERSISTENCIA T-03:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
