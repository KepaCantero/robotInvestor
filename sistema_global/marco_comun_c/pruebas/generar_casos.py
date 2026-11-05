"""Genera los sobres de prueba (válidos e inválidos) y el contexto común.

Los datos son SIMULADOS: no representan mercado real ni un análisis real.
Cada caso inválido parte de un válido y rompe exactamente una regla.
"""
import copy
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
from validar_sobre import proporcion_real, _cifras  # noqa: E402
EPISODIOS = ["EP-2008-LEHMAN", "EP-2011-EUROZONA", "EP-2015-SNB",
             "EP-2018-Q4", "EP-2020-COVID", "EP-2022-TIPOS"]
FACTORES = ["TIPOS", "RV", "USD", "CREDITO", "INFLACION",
            "MATERIAS_PRIMAS", "VOLATILIDAD", "LIQUIDEZ"]

CTX = {
    "ahora": "2026-11-06T09:00:00+00:00",
    "fecha_corte_encargo": "2026-11-05",
    "perfiles_activos": ["C-DIV", "C-RV", "C-CRI"],     # C-CRI activo solo para probar clase K
    "clases_ratificadas": {"C-DIV": "Q", "C-RV": "Q", "C-CRI": "K", "C-RF": "S"},
    "apalancamiento_permitido": False,
}


def cifra(valor, unidad, estado="ESTIMADO", n=1):
    c = {"valor": valor, "unidad": unidad, "estado": estado}
    if estado in ("VERIFICADO", "ESTIMADO"):
        c["modelo_ref"] = f"MOD-SIM-{n:02d}"
        c["motor_id"] = f"MOTOR-RUN-{n:04d}"
    return c


def base(perfil, clase, nivel, instrumento, via):
    tope = {"Q": 0.80, "S": 0.60, "K": 0.40}[clase]
    return {
        "event_id": f"EV-{perfil}-0001", "correlation_id": "COR-0001",
        "expediente_id": "EXP-0001", "producer": perfil, "consumer": "D",
        "tipo_mensaje": "CT-G-02", "version_esquema": "0.1.0",
        "emitido_en": "2026-11-05T18:00:00+00:00", "valid_until": "2026-11-08T18:00:00+00:00",
        "data_refs": ["K-20261105-001", "SRC-EURUSD", "EVID-0001"],
        "payload": {
            "identificacion": {
                "perfil": perfil, "clase_comparabilidad": clase, "instrumento": instrumento,
                "via_acceso": via, "direccion": "LARGO", "cartera_compatible": ["TACTICA"],
                "nivel_analisis": nivel, "fecha_corte": "2026-11-05", "divisa_base": "EUR"},
            "tesis": {
                "resumen": "Tesis de ejemplo con datos simulados.",
                "supuestos": ["Supuesto A de ejemplo"],
                "condiciones_invalidez": [{
                    "id": "INV-1", "descripcion": "Cierre por debajo del nivel de invalidez",
                    "metrica": "precio_cierre", "operador": "<", "umbral": 1.05, "unidad": "EUR"}]},
            "entrada_salida": {
                "entrada": "Límite en 1,08 durante 3 días",
                "stop": cifra(1.05, "EUR", "SUPUESTO"), "objetivo": cifra(1.14, "EUR", "SUPUESTO"),
                "fecha_revision": "2026-12-05"},
            "liquidez": {
                "tiempo_salida": cifra(1, "días"), "coste_salida": cifra(2, "pb", n=2),
                "tamano_max_sin_impacto": cifra(50000, "EUR", n=3)},
            "costes": {
                "entrada": cifra(2, "pb", n=4), "mantenimiento_anual": cifra(35, "pb", n=5),
                "salida": cifra(2, "pb", n=6),
                "impacto_fiscal": cifra(None, "EUR", "NO_ESTIMABLE")},
            "capital": {
                "capital_necesario": cifra(1000, "EUR", n=7), "margen": cifra(0, "EUR", "VERIFICADO", 8),
                "apalancamiento": cifra(0, "x", "VERIFICADO", 9)},
            "estres_historico": {
                "conjunto_version": "EST-v0",
                "episodios": [{"episodio_id": e, "perdida": cifra(-4.0 - i, "%", n=10 + i)}
                              for i, e in enumerate(EPISODIOS)]},
            "factores": {
                "conjunto_version": "FAC-v0", "ventana_dias": 750,
                "calidad_ajuste": cifra(0.35, "R2", n=20),
                "exposiciones": [{"factor": f, "beta": cifra(round(0.1 * (i - 3), 2), "beta", n=21 + i)}
                                 for i, f in enumerate(FACTORES)]},
            "evidencia": {"frescura_horas": 6,
                          "proporcion": {"VERIFICADO": 0.5, "ESTIMADO": 0.3, "SUPUESTO": 0.2}},
            "exclusiones_duras": {"sanciones": "OK", "invertibilidad": "OK", "acceso": "OK"},
            "referencias": {"cuerpo_especializado_ref": f"{perfil}-CUERPO-0001",
                            "artefactos_motor": ["MOTOR-RUN-0001"]},
            "cuerpo_especializado": {"esquema_ref": f"{perfil}-cuerpo", "version": "0.0.1",
                                     "contenido": {"nota": "campos propios del perfil"}},
        },
        "incertidumbre": ["Datos simulados para pruebas"],
        "resultado_politica": {"controles": ["SC-6"], "resultado": "APROBADO",
                               "version_politica": "POL-0.1"},
    }


def fin(s):
    """Completa lo derivado: artefactos del Motor citados y proporción real de evidencia."""
    p = s["payload"]
    p["referencias"]["artefactos_motor"] = sorted({c["motor_id"] for _, c in _cifras(p) if c.get("motor_id")})
    real = proporcion_real(p)
    p["evidencia"]["proporcion"] = {k: round(v, 4) for k, v in real.items()}
    tot = sum(p["evidencia"]["proporcion"].values())
    p["evidencia"]["proporcion"]["ESTIMADO"] = round(p["evidencia"]["proporcion"]["ESTIMADO"] + (1 - tot), 4)
    return s


def n3(s, tope, conf, discrepa=False, estimado=False):
    p = s["payload"]
    if estimado:
        p["capa2"] = {"estado": "ESTIMADO", "metodo": "Simulación histórica de bloques",
                      "base_datos": "Serie K-20261105-001",
                      "escenarios": [
                          {"nombre": "base", "probabilidad": 0.5, "rentabilidad_neta_pct": 1.5, "horizonte_dias": 90},
                          {"nombre": "adverso", "probabilidad": 0.3, "rentabilidad_neta_pct": -4.0, "horizonte_dias": 90},
                          {"nombre": "favorable", "probabilidad": 0.2, "rentabilidad_neta_pct": 5.0, "horizonte_dias": 90}]}
    else:
        p["capa2"] = {"estado": "NO_ESTIMABLE"}
    p["capa3"] = {"tope_confianza": tope, "confianza": conf,
                  "doble_analisis": {"realizado": True, "discrepa": discrepa}}
    return s


def validos():
    div = n3(base("C-DIV", "Q", "N3", "EUR/USD", "Futuro de divisas, vencimiento trimestral"),
             0.80, 0.70, estimado=True)
    # Perfil muy distinto (renta variable) solo para la prueba de estrés del marco
    rv = n3(base("C-RV", "Q", "N3", "ETF acciones Europa", "ETF cotizado en bolsa europea"),
            0.80, 0.55, discrepa=True)           # discrepa => tope efectivo 0,60
    rv["payload"]["costes"]["mantenimiento_anual"] = cifra(15, "pb", n=5)
    rv["payload"]["capa2"] = {"estado": "SUPUESTO"}
    cri = n3(base("C-CRI", "K", "N2", "BTC/EUR", "Custodia en intermediario regulado"), 0.40, 0.30)
    del cri["payload"]["capa2"]; del cri["payload"]["capa3"]
    for k in ("liquidez", "costes", "entrada_salida"):
        pass
    cri["payload"]["estres_historico"]["episodios"] = [
        {"episodio_id": e, "perdida": (cifra(None, "%", "NO_ESTIMABLE") if i < 3 else cifra(-30.0 - i, "%", n=40 + i))}
        for i, e in enumerate(EPISODIOS)]
    cri["payload"]["factores"]["exposiciones"] = [
        {"factor": f, "beta": cifra(None, "beta", "NO_ESTIMABLE")} for f in FACTORES]
    cri["payload"]["factores"]["calidad_ajuste"] = cifra(None, "R2", "NO_ESTIMABLE")
    return {"valido_div_n3.json": fin(div), "valido_rv_n3_discrepa.json": fin(rv),
            "valido_cri_k_no_estimable.json": fin(cri)}


def invalidos():
    out = {}
    d = lambda: copy.deepcopy(validos()["valido_div_n3.json"])
    c = lambda: copy.deepcopy(validos()["valido_cri_k_no_estimable.json"])

    def caso(nombre, fn, base=d):
        s = base(); fn(s); out[nombre] = s

    P = lambda s: s["payload"]
    caso("inv_V01_version_desconocida", lambda s: s.update(version_esquema="9.9.9"))
    caso("inv_V01_version_no_texto", lambda s: s.update(version_esquema=["0.1.0"]))
    caso("inv_V01_falta_campo", lambda s: P(s)["tesis"].pop("resumen"))
    caso("inv_V01_emitido_sin_zona", lambda s: s.update(emitido_en="2026-11-05T18:00:00"))
    caso("inv_V01_fecha_mal_formada", lambda s: P(s)["entrada_salida"].update(fecha_revision="mañana"))
    caso("inv_V01_consumer_desconocido", lambda s: s.update(consumer="X"))
    caso("inv_V01_sin_resultado_politica", lambda s: s.pop("resultado_politica"))
    caso("inv_V02_perfil_no_construido", lambda s: (s.update(producer="C-RF"),
         P(s)["identificacion"].update(perfil="C-RF", clase_comparabilidad="S"),
         P(s)["capa3"].update(tope_confianza=0.60, confianza=0.50),
         P(s)["cuerpo_especializado"].update(esquema_ref="C-RF-cuerpo")))
    caso("inv_V03_caducado", lambda s: s.update(valid_until="2026-11-05T19:00:00+00:00"))
    caso("inv_V03_vigencia_excesiva", lambda s: s.update(valid_until="2036-11-05T18:00:00+00:00"))
    caso("inv_V03_valid_until_anterior", lambda s: s.update(valid_until="2026-11-05T17:00:00+00:00"))
    caso("inv_V03_emitido_en_futuro", lambda s: s.update(emitido_en="2026-11-07T18:00:00+00:00",
                                                          valid_until="2026-11-09T18:00:00+00:00"))
    caso("inv_V04_fecha_corte_distinta", lambda s: P(s)["identificacion"].update(fecha_corte="2026-11-04"))
    caso("inv_V04_revision_anterior_al_corte", lambda s: P(s)["entrada_salida"].update(fecha_revision="2026-11-01"))
    caso("inv_V05_n3_sin_capa3", lambda s: P(s).pop("capa3"))
    caso("inv_V05_n1_sin_capital", lambda s: (P(s)["identificacion"].update(nivel_analisis="N1"),
         P(s).pop("capital"), fin(s)))
    caso("inv_V06_clase_no_ratificada", lambda s: (P(s)["identificacion"].update(clase_comparabilidad="S"),
         P(s)["capa3"].update(tope_confianza=0.60, confianza=0.50)))
    caso("inv_V07_no_estimable_con_valor", lambda s: P(s)["costes"]["impacto_fiscal"].update(valor=3.0))
    caso("inv_V08_estimado_sin_modelo", lambda s: P(s)["liquidez"]["coste_salida"].pop("modelo_ref"))
    caso("inv_V09_sin_condicion_invalidez", lambda s: P(s)["tesis"].update(condiciones_invalidez=[]))
    caso("inv_V10_proporcion_no_suma_1", lambda s: P(s)["evidencia"]["proporcion"].update(VERIFICADO=0.0))
    caso("inv_V10_proporcion_falsa", lambda s: P(s)["evidencia"]["proporcion"].update(VERIFICADO=0.9, ESTIMADO=0.05, SUPUESTO=0.05))
    caso("inv_V11_falta_episodio", lambda s: P(s)["estres_historico"]["episodios"].pop())
    caso("inv_V12_falta_factor", lambda s: P(s)["factores"]["exposiciones"].pop())
    caso("inv_V13_probabilidades_no_suman_1", lambda s: P(s)["capa2"]["escenarios"][0].update(probabilidad=0.9))
    caso("inv_V13_estimado_sin_metodo", lambda s: P(s)["capa2"].pop("metodo"))
    caso("inv_V13_un_solo_escenario", lambda s: P(s)["capa2"].update(escenarios=[
        {"nombre": "unico", "probabilidad": 1.0, "rentabilidad_neta_pct": 50.0, "horizonte_dias": 90}]))
    caso("inv_V13_no_estimable_con_metodo", lambda s: P(s)["capa2"].update(estado="NO_ESTIMABLE"))
    caso("inv_V14_confianza_sobre_tope", lambda s: P(s)["capa3"].update(confianza=0.95))
    caso("inv_V14_discrepa_sin_rebaja", lambda s: (P(s)["capa3"]["doble_analisis"].update(discrepa=True),
         P(s)["capa3"].update(confianza=0.70)))
    caso("inv_V14_tope_mal_declarado", lambda s: P(s)["capa3"].update(tope_confianza=0.99))
    caso("inv_V14_n3_sin_doble_analisis", lambda s: P(s)["capa3"]["doble_analisis"].update(realizado=False))
    caso("inv_V15_apalancamiento", lambda s: P(s)["capital"]["apalancamiento"].update(valor=5))
    def apal_ne(s):
        a = P(s)["capital"]["apalancamiento"]
        a.update(valor=None, estado="NO_ESTIMABLE"); a.pop("modelo_ref"); a.pop("motor_id"); fin(s)
    caso("inv_V15_apalancamiento_no_estimable", apal_ne)
    caso("inv_V16_bloqueado", lambda s: P(s)["exclusiones_duras"].update(sanciones="BLOQUEADO"))
    caso("inv_V16_desconocido_en_n3", lambda s: P(s)["exclusiones_duras"].update(acceso="DESCONOCIDO"))
    caso("inv_V17_unidad_costes", lambda s: P(s)["costes"]["entrada"].update(unidad="%"))
    caso("inv_V17_unidad_coste_salida", lambda s: P(s)["liquidez"]["coste_salida"].update(unidad="EUR"))
    caso("inv_V18_esquema_propio_ajeno", lambda s: P(s)["cuerpo_especializado"].update(esquema_ref="C-RV-cuerpo"))
    caso("inv_V18_sin_cuerpo", lambda s: P(s).pop("cuerpo_especializado"))
    caso("inv_V19_numero_suelto_en_cuerpo", lambda s: P(s)["cuerpo_especializado"]["contenido"].update(
        rentabilidad_esperada=12.5))
    caso("inv_V19_estado_inventado_en_cuerpo", lambda s: P(s)["cuerpo_especializado"]["contenido"].update(
        dato={"valor": 5, "unidad": "EUR", "estado": "MAGICO"}))
    caso("inv_V20_motor_no_listado", lambda s: P(s)["liquidez"]["coste_salida"].update(motor_id="INEXISTENTE"))
    caso("inv_V20_supuesto_con_modelo", lambda s: P(s)["entrada_salida"]["stop"].update(modelo_ref="MOD-X"))
    caso("inv_V21_perdida_imposible", lambda s: P(s)["estres_historico"]["episodios"][0]["perdida"].update(valor=-500.0))
    caso("inv_V21_r2_fuera_de_rango", lambda s: P(s)["factores"]["calidad_ajuste"].update(valor=7.0))
    caso("inv_V21_tiempo_negativo", lambda s: P(s)["liquidez"]["tiempo_salida"].update(valor=-1))
    caso("inv_V22_stop_sobre_objetivo", lambda s: P(s)["entrada_salida"]["stop"].update(valor=2.0))
    def vaciar(s):
        """Sobre K de nivel N2 en el que casi todo es NO_ESTIMABLE."""
        pl = s["payload"]
        celdas = ([e["perdida"] for e in pl["estres_historico"]["episodios"]]
                  + [e["beta"] for e in pl["factores"]["exposiciones"]]
                  + [pl["factores"]["calidad_ajuste"]])
        for x in celdas:
            x.update(valor=None, estado="NO_ESTIMABLE")
            x.pop("modelo_ref", None); x.pop("motor_id", None)
        fin(s)
    caso("inv_V23_sobre_vacio_n2", vaciar, base=c)
    return out


def casos_nan():
    """Sobres con NaN o infinito: json.dumps los escribe; el cargador estricto los rechaza."""
    out = {}
    s = copy.deepcopy(validos()["valido_div_n3.json"])
    s["payload"]["capa3"]["confianza"] = float("nan")
    out["inv_V01_confianza_nan.json"] = s
    s = copy.deepcopy(validos()["valido_div_n3.json"])
    s["payload"]["liquidez"]["tamano_max_sin_impacto"]["valor"] = float("inf")
    out["inv_V01_infinito.json"] = s
    return out


if __name__ == "__main__":
    (AQUI / "contexto.json").write_text(json.dumps(CTX, ensure_ascii=False, indent=2), encoding="utf-8")
    for nombre, s in validos().items():
        (AQUI / "validos" / nombre).write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    inv = {f"{k}.json": v for k, v in invalidos().items()}
    inv.update(casos_nan())
    for viejo in (AQUI / "invalidos").glob("*.json"):
        viejo.unlink()
    for nombre, s in inv.items():
        (AQUI / "invalidos" / nombre).write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    print("casos generados:", len(validos()), "válidos,", len(inv), "inválidos")
