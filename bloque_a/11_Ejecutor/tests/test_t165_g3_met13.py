"""T-165 · G3-MET-13 «Madurez declarada» (PB-47, R22): comprobación complementaria de HT-09 en el ejecutor.

Unitarias de `ht09.comprobar_madurez` (lo que bloquea y las frases que no deben saltar), de `sintesis.g3_met13` (dónde se
localiza cada incidencia) y de extremo a extremo con el cliente simulado (`MockClient`, sin red ni coste): PB-47 con su
preparación completa (método en DOCUMENTADO e informe de clase que lo llama «validado»), la corrección de la declaración, el
informe técnico y el visual, y el ciclo normal sin falsos positivos.
"""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from bloque_a.herramientas import ht09
from bloque_a.motor import servicio
from bloque_a.redaccion import Redaccion
from conftest import AS_OF, nuevo_bloque

from bloque_a import mock_respuestas
from bloque_a import sintesis as sint

MADUREZ = {"ML-CLUS-001": "DOCUMENTADO", "ST-DESC-001": "IMPLEMENTADO", "DER-OPT-001": "DOCUMENTADO",
           "VOL-GARCH-001": "IMPLEMENTADO", "FX-PPA-001": "IMPLEMENTADO", "FX-COINT-001": "IMPLEMENTADO",
           "FON-DISC-001": "DOCUMENTADO", "AUD-REX-001": "IMPLEMENTADO", "IDX-CONC-001": "Implementado (referencia)"}


def _sirve(f):
    return ht09.nivel_catalogo(MADUREZ.get(f)) >= 2


def _comp(texto, sev="BLOQUEO", madurez=MADUREZ, sirve=_sirve):
    return ht09.comprobar_madurez([("r", texto, sev)], madurez, sirve, madurez)


# ------------------------------------------------------------------ comprobar_madurez: lo que bloquea
@pytest.mark.parametrize("texto, ficha", [
    ("Los clústeres de exposición se calculan con ML-CLUS-001, un método validado.", "ML-CLUS-001"),   # PB-47
    ("ST-DESC-001 está validado en backtest", "ST-DESC-001"),           # nada está VALIDADO en el Catálogo
    ("ML-CLUS-001 está implementado", "ML-CLUS-001"),                  # implementado para un DOCUMENTADO
    ("DER-OPT-001 y ST-DESC-001: implementados", "DER-OPT-001"),       # plural: a todas las de la frase
    ("La señal sale de ML-SUPER-001", "ML-SUPER-001"),                  # una ficha que no existe y no se sirve
    ("ML-SUPER-001 documentado", "ML-SUPER-001"),                       # «documentado» de algo que no tiene ficha
    ("N efectivo ML-CLUS-001: 12", "ML-CLUS-001"),                      # nombrada sin servirse ni declararlo
    ("ST-DESC-001 (implementado) y ML-CLUS-001", "ML-CLUS-001"),        # la palabra va a la más cercana
    ("ML-CLUS-001 y ST-DESC-001 implementado", "ML-CLUS-001"),          # sin la palabra, la regla B: no se sirve
    ("FX-PPA-001 VALIDATED", "FX-PPA-001"),
    ("ML-CLUS-001 no está validado, pero sí implementado", "ML-CLUS-001"),
    ("ST-DESC-001 validado por el Motor", "ST-DESC-001"),               # «por» + algo que no es una persona ni un dato
    ("ST-DESC-001 validado por backtest", "ST-DESC-001"),
    ("ML-CLUS-001 documentado por el operador", "ML-CLUS-001"),        # no es una declaración de madurez: regla B
])
def test_bloquea_una_madurez_que_el_catalogo_no_da_o_un_metodo_que_no_se_sirve(texto, ficha):
    c = _comp(texto)
    assert c["resultado"] == "BLOQUEO", c
    assert c["id"] == "G3-MET-13" and any(ficha in i["detalle"] and i["severidad"] == "BLOQUEO" and i["ruta"] == "r"
                                          for i in c["incidencias"])


# ------------------------------------------------------------------ comprobar_madurez: sin falsos positivos
@pytest.mark.parametrize("texto", [
    "El umbral fue validado por el operador.",                                   # sin método en la frase
    "Precio en el percentil 96% (ST-DESC-001), umbral validado por el operador.",   # lo hizo una persona
    "La tesis, validada por el dato de empleo, se apoya en ST-DESC-001.",          # o un dato
    "Precio en el percentil 96% de sus últimos tres años (ST-DESC-001).",        # servida y sin madurez: no salta
    "Precio (ST-DESC-001); el umbral fue validado por el operador.",             # otra frase
    "DER-OPT-001 documentado; VOL-GARCH-001 implementado",                       # ejemplo del prompt de Derivados
    "FON-DISC-001: documentado, no validado",                                    # ejemplo del prompt de Fondos
    "FX-PPA-001, FX-COINT-001: implementados, validación pendiente",             # ejemplo del prompt de Divisas
    "ML-CLUS-001 aún no ha sido implementado",
    "ST-DESC-001 todavía no está validado",
    "Ficha ML-CLUS-001 con código pero «DOCUMENTADO» en el Catálogo: no entrega cifras citables",   # el Motor
    "ML-CLUS-001: METODO_NO_IMPLEMENTADO",
    "fichas del Motor rechazadas en este ciclo: ML-CLUS-001, DER-OPT-001 (sus señales faltan)",
    "el resto tampoco se agrupa (ML-CLUS-001 rechazado)",
    "ST-DESC-001 (implementado) y ML-CLUS-001 (documentado)",
    "IDX-CONC-001 implementado",                                                  # «Implementado (referencia)»
    "Re-ejecución CT-10 con AUD-REX-001",                                         # CT-10: se sirve
    "CALC-2026-0001 de OPP-2026-0003, G3-MET-13 y DEC-2026-001: todo validado",  # no son fichas
    "ST-DESC-001 documentado",                                                    # infradeclarar no salta
    "METODO_NO_IMPLEMENTADO es un código validado",
])
def test_no_salta_con_frases_que_no_sobredeclaran(texto):
    c = _comp(texto)
    assert c["resultado"] == "OK" and not c["incidencias"], c


def test_formato_de_hT09_y_severidad_advertencia_sin_extracto():
    c = _comp("ML-CLUS-001, un método validado. OPP-2026-0007", sev="ADVERTENCIA")
    assert set(c) == {"id", "nombre", "resultado", "incidencias", "datos"} and c["resultado"] == "ADVERTENCIA"
    assert c["nombre"] == ht09.NOMBRE_MET13 and c["datos"]["fichas_citadas"] == ["ML-CLUS-001"]
    (i,) = c["incidencias"]
    assert set(i) == {"severidad", "ruta", "detalle"} and "OPP-" not in i["detalle"]
    assert "«validado»" in i["detalle"] and "«DOCUMENTADO»" in i["detalle"]


def test_sin_catalogo_legible_toda_mencion_bloquea():
    c = ht09.comprobar_madurez([("r", "Percentil (ST-DESC-001).", "BLOQUEO")], {}, lambda f: False, servicio.FICHAS_CATALOGO)
    assert c["resultado"] == "BLOQUEO"


def test_una_mencion_repetida_en_la_misma_ruta_se_anota_una_vez():
    c = ht09.comprobar_madurez([("r", "ML-CLUS-001 validado.", "BLOQUEO")] * 3, MADUREZ, _sirve, MADUREZ)
    assert len(c["incidencias"]) == 1


def test_textos_de_lleva_el_opp_en_la_ruta_y_lee_el_campo_de_madurez_con_su_metodo():
    obj = {"clases": {"RV": {"opciones": [{"opp_id": "OPP-2026-0004", "mecanismo": "x",
                                           "calculo": {"metodo": "DER-OPT-001", "estado_madurez_metodo": "implementado"}}]}},
           "otro": {"metodo": "DER-OPT-001", "estado_madurez_metodo": "documentado"}}
    t = dict(ht09.textos_de(obj, "paquete"))
    assert t["paquete.clases.RV.opciones[OPP-2026-0004].mecanismo"] == "x"
    assert t["paquete.clases.RV.opciones[OPP-2026-0004].calculo.estado_madurez_metodo"] == "DER-OPT-001 implementado"
    assert "paquete.otro.metodo" not in t                      # el hermano no se lee suelto
    c = ht09.comprobar_madurez([(r, x, "BLOQUEO") for r, x in t.items()], MADUREZ, _sirve, MADUREZ)
    assert [i["ruta"] for i in c["incidencias"]] == ["paquete.clases.RV.opciones[OPP-2026-0004].calculo.estado_madurez_metodo"]


def test_texto_html_separa_frases_por_etiquetas():
    t = ht09.texto_html("<p>Percentil (ST-DESC-001)</p><p>El plan fue validado por el operador &amp; el Broker</p>")
    assert _comp(t)["resultado"] == "OK"
    assert _comp(ht09.texto_html("<li>ST-DESC-001 está <b>validado</b></li>"))["resultado"] == "BLOQUEO"


# ------------------------------------------------------------------ sintesis.g3_met13: dónde se localiza
def test_g3_met13_localiza_en_la_opcion_y_advierte_de_lo_que_no_se_entrega(monkeypatch):
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: dict(MADUREZ))
    bloque = SimpleNamespace(motor=SimpleNamespace(raiz=None))
    frase = "Calculado con ML-CLUS-001, un método validado."
    paquete = {"clases": {"RV": {"opciones": [{"opp_id": "OPP-2026-0001", "mecanismo": "Persistencia del impulso."}]}},
               "limitaciones": ["ninguna"]}
    extras = {"seleccion": {"RV": {"candidatos": [{"opp_id": "OPP-2026-0001", "proxy": "AAA", "mecanismo": frase},
                                                  {"opp_id": "OPP-2026-0002", "proxy": "BBB", "valoracion": frase}]}},
              "analisis": {"RV": {"regimen": "Régimen alcista; ST-DESC-001 está validado.", "lagunas": []}}}
    c = sint.g3_met13(bloque, paquete, extras, None)
    por_ruta = {i["ruta"]: i["severidad"] for i in c["incidencias"]}
    assert por_ruta == {"informes_clase.RV[OPP-2026-0001].mecanismo": "BLOQUEO",
                        "informes_clase.RV.no_entregada[BBB].valoracion": "ADVERTENCIA",
                        "informes_clase.RV.regimen": "ADVERTENCIA"}
    assert c["resultado"] == "BLOQUEO"
    # Sin la candidata que es opción, solo quedan advertencias (lo que no llega a la entrega)
    extras["seleccion"]["RV"]["candidatos"].pop(0)
    assert sint.g3_met13(bloque, paquete, extras, None)["resultado"] == "ADVERTENCIA"
    # Y un paquete que lo dice fuera de una opción bloquea sin OPP- (todo el run)
    paquete["limitaciones"] = [frase]
    c = sint.g3_met13(bloque, paquete, {}, None)
    assert [(i["ruta"], i["severidad"]) for i in c["incidencias"]] == [("paquete.limitaciones[0]", "BLOQUEO")]


def test_g3_met13_visual_ilegible_falla_cerrado(monkeypatch, tmp_path):
    bloque = SimpleNamespace(motor=SimpleNamespace(raiz=None))
    c = sint.g3_met13(bloque, {"clases": {}}, {}, str(tmp_path / "no_existe.html"))
    assert c["resultado"] == "BLOQUEO" and c["incidencias"][0]["ruta"] == "informe_visual"


def test_recalcular_dictamen_y_motivo_como_la_referencia():
    res = {"dictamen": "APTO", "motivo": "Todas las comprobaciones superadas", "resumen": {"ok": 1, "advertencias": 0, "bloqueos": 0},
           "comprobaciones": [{"id": "C01", "nombre": "Campos", "resultado": "OK", "incidencias": []},
                              {"id": "G3-MET-13", "nombre": ht09.NOMBRE_MET13, "resultado": "ADVERTENCIA", "incidencias": [{}]}]}
    sint._recalcular(res)
    assert res["dictamen"] == "APTO_CON_ADVERTENCIAS" and res["motivo"] == f"G3-MET-13 {ht09.NOMBRE_MET13}"
    res["comprobaciones"][1]["resultado"] = "BLOQUEO"
    sint._recalcular(res)
    assert res["dictamen"] == "BLOQUEADO" and res["resumen"] == {"ok": 1, "advertencias": 0, "bloqueos": 1}


# ------------------------------------------------------------------ de extremo a extremo (cliente simulado)
FRASE = "Los clústeres de exposición se calculan con ML-CLUS-001, un método validado."


def _g3v(b, run_id, fase="F6"):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V" and e["run_id"] == run_id and e.get("fase") == fase]


def _met13(g3v):
    return next(c for c in g3v["comprobaciones"] if c["id"] == "G3-MET-13")


def _documentado(monkeypatch, ficha="ML-CLUS-001"):
    original = servicio.madurez_catalogo
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: {**original(raiz), ficha: "DOCUMENTADO"})


def _sembrar(monkeypatch, frase):
    original = mock_respuestas._ficha
    sembradas = []

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f["mecanismo"] = f"{f['mecanismo']} {frase}"
        sembradas.append(u["simbolo"])
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    return sembradas


def test_pb47_informe_de_clase_que_llama_validado_a_un_metodo_documentado_bloquea_g3(tmp_path, universo, monkeypatch):
    """PB-47 con su preparación completa: ML-CLUS-001 en DOCUMENTADO y un informe de clase que lo llama «validado». HT-09
    (G3-MET-13) bloquea; las opciones que lo afirman se retiran (CT-14) y el entregable final no lo presenta como validado ni
    usa el método."""
    _documentado(monkeypatch)
    sembradas = _sembrar(monkeypatch, FRASE)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    assert sembradas
    f6 = _g3v(b, r["run_id"])
    assert f6[0]["dictamen_efectivo"] == "BLOQUEADO" and _met13(f6[0])["resultado"] == "BLOQUEO"
    assert any("«validado» para ML-CLUS-001" in d and "«DOCUMENTADO»" in d for d in _met13(f6[0])["detalle"])
    ct14 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-14"]           # al Orquestador, que no lo da por bueno
    assert ct14 and ct14[0]["emisor"] == "AG-02" and ct14[0]["receptor"] == "AG-18"
    assert f6[0]["excepcion"]["dictamen_orquestador"] == "BLOQUEADO"
    assert len(f6) == 2 and f6[1]["dictamen_efectivo"] != "BLOQUEADO"              # la corrección: se retiran las afectadas
    assert all(not d["opciones"] for d in r["paquete"]["clases"].values())       # todas lo afirmaban
    assert any("Opciones retiradas por bloqueo G3" in x for x in r["paquete"]["limitaciones"])
    entregados = {k: Path(v).read_text(encoding="utf-8") for k, v in (r.get("entregables") or {}).items()}
    assert entregados and not [k for k, t in entregados.items() if "validado" in t.lower()]
    js = json.loads(entregados["paquete_json"])
    servidos = {e["calc_id"]: e for e in b.almacen.leer("RC") if e.get("estado") in ("SERVED", "SERVED_WITH_LIMITATIONS")}
    citados = {c for d in js["clases"].values() for o in d["opciones"] for c in o["calculos"]}
    assert all(servidos[c]["operacion"]["ficha_id"] != "ML-CLUS-001" for c in citados)


def test_pb47_corregida_la_declaracion_documentado_la_entrega_pasa(tmp_path, universo, monkeypatch):
    """«BLOQUEADO hasta corregir la declaración»: el mismo informe de clase que lo declara «documentado» pasa G3 y se entrega."""
    _documentado(monkeypatch)
    _sembrar(monkeypatch, "Los clústeres de exposición usarían ML-CLUS-001, que está documentado y no se sirve.")
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    f6, f7 = _g3v(b, r["run_id"]), _g3v(b, r["run_id"], "F7")
    assert len(f6) == 1 and f6[0]["dictamen_efectivo"] == "APTO" and _met13(f6[0])["resultado"] == "OK"
    assert f7 and f7[0]["dictamen_efectivo"] == "APTO" and _met13(f7[0])["resultado"] == "OK"
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"
    assert all(d["opciones"] for d in r["paquete"]["clases"].values())
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    assert "documentado" in tecnico and "N efectivo ML-CLUS-001" not in tecnico   # el rótulo no cita lo que no se usó


def test_un_metodo_no_servido_solo_en_el_tecnico_bloquea_la_entrega_en_f7(tmp_path, universo, monkeypatch):
    original = Redaccion.tecnico

    def tecnico(self, *a, **k):
        return original(self, *a, **k) + "\nLa volatilidad sale de ML-SUPER-001.\n"
    monkeypatch.setattr(Redaccion, "tecnico", tecnico)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r.get("entrega") == "BLOQUEADA" and "G3-MET-13" in r["g3_entregables"]["bloqueos"]
    (f7,) = _g3v(b, r["run_id"], "F7")
    assert f7["dictamen_efectivo"] == "BLOQUEADO" and f7["dictamen_ht09"] == "BLOQUEADO"
    assert _met13(f7)["resultado"] == "BLOQUEO" and any("ML-SUPER-001" in d for d in _met13(f7)["detalle"])
    assert all("_bloqueados" in v for v in r["entregables"].values())
    assert not [e for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "ALTA"]   # nada se congela


def test_un_visual_que_presenta_un_metodo_como_validado_bloquea_en_f7(tmp_path, universo, monkeypatch):
    original = Redaccion.visual

    def visual(self, *a, **k):
        return original(self, *a, **k).replace("</body>", "<p>El percentil sale de ST-DESC-001, un método validado.</p></body>")
    monkeypatch.setattr(Redaccion, "visual", visual)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    (f7,) = _g3v(b, r["run_id"], "F7")
    assert f7["dictamen_efectivo"] == "BLOQUEADO" and _met13(f7)["resultado"] == "BLOQUEO"
    assert r.get("entrega") == "BLOQUEADA" and all("_bloqueados" in v for v in r["entregables"].values())


def test_el_ciclo_simulado_normal_sigue_apto_y_la_comprobacion_ve_las_fichas(tmp_path, universo, monkeypatch):
    """Sin falsos positivos: el ciclo normal (doce tipos) da G3 APTO en F6 y F7 con G3-MET-13 OK, y no es vacuo: la
    comprobación lee menciones de fichas servidas (ST-DESC-001, RISK-DD-001, ML-CLUS-001)."""
    vistos = []
    original = ht09.comprobar_madurez

    def espia(*a, **k):
        c = original(*a, **k)
        vistos.append(c)
        return c
    monkeypatch.setattr(ht09, "comprobar_madurez", espia)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF)
    f6, f7 = _g3v(b, r["run_id"]), _g3v(b, r["run_id"], "F7")
    assert [e["dictamen_efectivo"] for e in f6 + f7] == ["APTO", "APTO"]
    assert all(_met13(e)["resultado"] == "OK" for e in f6 + f7)
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"
    citadas = {f for c in vistos for f in c["datos"]["fichas_citadas"]}
    assert {"ST-DESC-001", "RISK-DD-001", "ML-CLUS-001"} <= citadas and all(c["resultado"] == "OK" for c in vistos)
    assert "N efectivo ML-CLUS-001" in Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
