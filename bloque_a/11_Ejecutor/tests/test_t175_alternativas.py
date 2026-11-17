"""T-175 (PB-38): la opción que se queda fuera del top-3 por una objeción fuerte sin resolver figura en el informe técnico como
alternativa documentada (4.N.4 de la plantilla V5.0) y su objeción, en la sección 6, como SIN_RESOLVER."""
import json
import re
from pathlib import Path

import pytest
from bloque_a.redaccion import Redaccion, coherencia
from conftest import AS_OF, nuevo_bloque

from bloque_a import sintesis as sint


def _seccion(md: str, titulo: str, siguiente: str) -> str:
    i = md.index(titulo)
    return md[i:md.index(siguiente, i + len(titulo))]


def _abiertas_f3(b):
    return [e for e in b.almacen.leer("F3", AS_OF) if e.get("objeciones_internas")
            and any(o["fuerza"] == "fuerte" and not o["resuelta"] for o in e["objeciones_internas"])]


@pytest.fixture(scope="module")
def ciclo_rv(tmp_path_factory, universo):
    b = nuevo_bloque(tmp_path_factory.mktemp("t175"), universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    return b, r, Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")


def test_pb38_la_opcion_con_objecion_fuerte_sin_resolver_es_una_alternativa_documentada_en_el_tecnico(ciclo_rv):
    b, r, md = ciclo_rv
    (e,) = [x for x in _abiertas_f3(b) if x["clase"] == "RV"]
    oid = e["opp_id"]
    obj = next(o for o in e["objeciones_internas"] if o["fuerza"] == "fuerte" and not o["resuelta"])
    sel = [o["opp_id"] for o in r["paquete"]["clases"]["RV"]["opciones"]]
    # fuera del top-3 y no elegible en F3 (lo que ya se cumplía)
    assert oid not in sel and not e["elegible"] and e["estado"] == "EN_OBSERVACION"
    # 4.1.4: la alternativa con su puerta, su motivo (con la OBJ-) y lo que tendría que ocurrir
    alt = _seccion(md, "#### 4.1.4 Alternativas descartadas relevantes", "## 5.")
    assert "| Candidata | Puerta en la que quedó | Motivo | Qué tendría que ocurrir |" in alt
    (fila,) = [x for x in alt.splitlines() if f"`{oid}`" in x]
    celdas = [c.strip() for c in fila.strip("|").split(" | ")]
    assert len(celdas) == 4
    assert celdas[0].startswith(e["nombre"]) and f"(RK {e['puntuaciones_totales']['RK']})" in celdas[0]
    assert celdas[1] == "G2"
    assert "objeción(es) fuerte(s) sin resolver" in celdas[2] and obj["objecion_id"] in celdas[2]
    assert "Resolver las objeciones fuertes con evidencia" in celdas[3] and obj["que_la_resolveria"] in celdas[3]
    # va después de la ficha de la última opción de su clase y antes de la clase siguiente / la sección 5
    assert md.index("#### 4.1.4") > md.index(f"`{sel[-1]}`")
    # sección 6: la objeción fuerte, SIN_RESOLVER, con la OPP- de la alternativa
    s6 = _seccion(md, "## 6. Objeciones y respuestas", "## 7.")
    filas6 = [x for x in s6.splitlines() if x.startswith(f"| `{oid}` (alternativa descartada) |")]
    assert any(f"| fuerte | {obj['resumen']} |" in x and x.endswith("| SIN_RESOLVER |") for x in filas6)
    assert len(filas6) == sum(1 for o in e["objeciones_internas"] if o["fuerza"] in ("fuerte", "moderada"))


def test_pb38_la_alternativa_no_entra_en_el_json_ni_altera_la_coherencia_ni_el_dictamen(ciclo_rv):
    b, r, md = ciclo_rv
    (e,) = [x for x in _abiertas_f3(b) if x["clase"] == "RV"]
    js = json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    assert e["opp_id"] not in json.dumps(js)
    assert r.get("entrega") != "BLOQUEADA" and r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS")
    assert coherencia(r["entregables"], js) == []
    # la alternativa no se cuenta como opción: ni encabezado ##### ni celda de RK del top-3
    assert e["opp_id"] not in re.findall(r"^##### \d+\. .*· `(OPP-\d{4}-\d+)`", md, re.MULTILINE)
    # lo que escribe el ejecutor en la alternativa no lleva la raíz «valid-» (G3-MET-13)
    alt = _seccion(md, "#### 4.1.4", "## 5.")
    assert not re.search(r"(?i)v[aá]lid", alt)


def _f(oid, elegible, rk=50, motivos=None, **kw):
    f = {"opp_id": oid, "nombre": f"Ámbito {oid}", "_ht03": {"elegible": elegible, "puntuaciones": {"RK": rk},
                                                          "motivos_no_elegible": motivos if motivos is not None else
                                                          ([] if elegible else [{"codigo": "E_BAJO", "detalle": "E=40 < 60", "falta": 20}])}}
    f.update(kw)
    return f


def _fuerte(oid="OBJ-X-01", resuelta=False, **kw):
    return {"objecion_id": oid, "fuerza": "fuerte", "resumen": "Una sola raíz", "respuesta": "Respuesta con evidencia suficiente",
            "resuelta": resuelta, "que_la_resolveria": "Una segunda raíz", **kw}


def test_solo_se_listan_las_no_elegibles_que_no_son_opcion_ni_vigentes_ni_de_arrastre_en_orden_de_rk():
    paquete = {"clases": {"RV": {"opciones": [{"opp_id": "OPP-2026-0001"}]}}}
    cands = [_f("OPP-2026-0001", False),                                  # es opción (no debería pasar, pero no se duplica)
             _f("OPP-2026-0002", True),                                   # elegible fuera del top-3 por RK: no se descarta
             _f("OPP-2026-0003", False, _vigente=True),                   # vigente no elegible: sale en la sección 5
             _f("OPP-2026-0004", False, _arrastre=True),                  # arrastre
             _f("OPP-2026-0005", False, rk=40),
             _f("OPP-2026-0006", False, rk=70),
             _f("OPP-2026-0007", False, rk=None),
             {"opp_id": "OPP-2026-0008"},                                 # sin HT-03: mal formada
             _f("OPP-2026-0009", False, motivos=[]),                      # no elegible sin motivo: no se inventa
             _f(None, False), "no es un dict", _f("OPP-2026-0010", "no"),  # sin OPP-, no dict, elegible que no es booleano
             # r02 (QA r01, H-02): estructuras que no son listas y RK que no se puede escribir ni ordenar
             _f("OPP-2026-0011", False, motivos=7),                        # motivos que no son una lista: no se lista
             _f("OPP-2026-0012", False, rk=60, _objeciones=7),             # objeciones que no son una lista: se ignoran
             _f("OPP-2026-0013", False, rk=True), _f("OPP-2026-0014", False, rk=float("nan")),
             _f("OPP-2026-0015", False, rk=float("inf"))]
    out = sint.alternativas_descartadas(paquete, {"seleccion": {"RV": {"candidatos": cands}, "RF": "mal", "MP": {"candidatos": []},
                                                                "DIV": {"candidatos": 5}}})
    assert list(out) == ["RV"]
    assert [a["opp_id"] for a in out["RV"]] == ["OPP-2026-0006", "OPP-2026-0012", "OPP-2026-0005", "OPP-2026-0007",
                                                 "OPP-2026-0013", "OPP-2026-0014", "OPP-2026-0015"]
    a = out["RV"][0]
    assert a["puertas"] == [] and a["motivo"] == ["E=40 < 60"] and a["condicion"] == ["E debería subir al menos 20 puntos (E=40 < 60)"]
    assert [x["rk"] for x in out["RV"][3:]] == [None] * 4 and out["RV"][1]["objeciones"] == []
    assert all(x["retirados"] == [] for x in out["RV"])
    assert sint.alternativas_descartadas({"clases": {}}, {}) == {}


def test_objeciones_de_la_alternativa_estado_y_condicion():
    mot = [{"codigo": "PUERTA_NO_SUPERADA", "detalle": "G2 no superada", "puerta": "G2"},
           {"codigo": "OBJECION_FUERTE", "detalle": "2 objeción(es) fuerte(s) sin resolver"}]
    objs = [_fuerte("OBJ-X-01"), _fuerte("OBJ-X-02", que_la_resolveria=None), _fuerte("OBJ-X-03", resuelta=True),
            {"objecion_id": "OBJ-X-04", "fuerza": "moderada", "resumen": "Moderada", "respuesta": None},
            {"objecion_id": "OBJ-X-05", "fuerza": "debil", "resumen": "Débil"}, "mal formada"]
    (a,) = sint.alternativas_descartadas({"clases": {}}, {"seleccion": {"RV": {"candidatos": [
        _f("OPP-2026-0001", False, motivos=mot, _objeciones=objs)]}}})["RV"]
    assert a["puertas"] == ["G2"]
    assert a["motivo"] == ["G2 no superada", "2 objeción(es) fuerte(s) sin resolver (OBJ-X-01, OBJ-X-02)"]
    assert a["condicion"] == ["Superar la puerta G2", "Resolver las objeciones fuertes con evidencia", "OBJ-X-01: Una segunda raíz"]
    assert [(o["objecion_id"], o["estado"]) for o in a["objeciones"]] == [
        ("OBJ-X-01", "SIN_RESOLVER"), ("OBJ-X-02", "SIN_RESOLVER"), ("OBJ-X-03", "RESPONDIDA"), ("OBJ-X-04", "SIN_RESOLVER")]


def test_la_regla_del_estado_es_la_del_top3():
    assert sint._objecion_respondida({"fuerza": "fuerte", "respuesta": "x" * 10, "resuelta": True})
    assert not sint._objecion_respondida({"fuerza": "fuerte", "respuesta": "x" * 10, "resuelta": False})
    assert not sint._objecion_respondida({"fuerza": "moderada", "respuesta": "x" * 9})
    assert sint._objecion_respondida({"fuerza": "moderada", "respuesta": "x" * 10})
    assert not sint._objecion_respondida({"fuerza": "moderada", "respuesta": 1234567890})


def test_un_texto_con_barra_o_salto_de_linea_no_rompe_las_tablas(ciclo_rv, monkeypatch):
    b, r, _ = ciclo_rv
    fila = {"opp_id": "OPP-2026-0099", "nombre": "Ámbito | con barra\ny salto", "rk": 50, "puertas": ["G2"],
            "motivo": ["motivo | uno"], "condicion": [],
            "objeciones": [{"objecion_id": "OBJ-Z-01", "fuerza": "fuerte", "resumen": "a | b\nc", "respuesta": None, "estado": "SIN_RESOLVER"}]}
    monkeypatch.setattr(sint, "alternativas_descartadas", lambda p, e: {"RV": [fila], "XX": [dict(fila, opp_id="OPP-2026-0098")]})
    md = b.redaccion.tecnico(r["paquete"], {"gc0": r["gc0"]}, {"dictamen": "APTO"}, {}, "COMPLETO", {})
    alt = _seccion(md, "#### 4.1.4", "## 5.")
    (f,) = [x for x in alt.splitlines() if "OPP-2026-0099" in x]
    assert len(re.split(r"(?<!\\)\|", f.strip().strip("|"))) == 4 and "Ámbito \\| con barra y salto" in f and f.endswith("| — |")
    s6 = _seccion(md, "## 6.", "## 7.")
    (g,) = [x for x in s6.splitlines() if "OPP-2026-0099" in x]
    assert len(re.split(r"(?<!\\)\|", g.strip().strip("|"))) == 5 and "a \\| b c" in g and "| — | SIN_RESOLVER |" in g
    assert "OPP-2026-0098" not in md   # una clase que no está en el paquete no se lista


def _contradictor_con(monkeypatch, texto: str, obedece: bool):
    """El Contradictor (AG-11) añade `texto` a las objeciones de XLK, la candidata de RV que acaba como alternativa, y la fuerte
    sigue sin resolver. Si no `obedece`, la reescritura R22 repite la primera respuesta (la raíz persiste) (revisor r01_02)."""
    import copy

    from bloque_a import mock_respuestas
    original, primera = mock_respuestas.responder, {}
    if not obedece:
        monkeypatch.setattr(mock_respuestas, "_obedece_r22", lambda msg, d: d)

    def responder(agente, mensajes, semilla):
        enc = mock_respuestas.extraer_encargo(mensajes[0]["content"])["mensaje"]
        r22 = isinstance(enc, dict) and isinstance(enc.get("reescritura"), dict) and enc["reescritura"].get("r22")
        if agente == "AG-11" and r22 and "x" in primera and not obedece:
            return copy.deepcopy(primera["x"])
        d = original(agente, mensajes, semilla)
        if agente == "AG-11" and isinstance(d, dict) and isinstance(d.get("resultados"), list):
            for x in d["resultados"]:
                if isinstance(x, dict) and x.get("ref") == "XLK":
                    for o in x.get("objeciones", []):
                        o["argumento"] += " " + texto
                        if o.get("que_la_resolveria"):
                            o["que_la_resolveria"] += " " + texto
                if isinstance(x, dict) and str(x.get("objecion_id", "")).startswith("OBJ-XLK-"):
                    x["resuelta"] = False
            if not r22 and isinstance(enc, dict) and enc.get("peticiones"):
                primera["x"] = copy.deepcopy(d)
        return d
    monkeypatch.setattr(mock_respuestas, "responder", responder)


@pytest.mark.parametrize("texto,obedece", [("Falta el cálculo RISK-XYZ-999 de la cola.", True),        # regla B: no se reescribe
                                           ("La señal no está validada fuera de muestra.", False)])  # la raíz persiste
def test_un_texto_del_modelo_que_g3_met13_rechaza_en_una_alternativa_se_retira_y_la_entrega_sale(
        tmp_path, universo, monkeypatch, texto, obedece):
    """r02 (QA r01, H-01): el texto del modelo de una alternativa que G3-MET-13 rechazaría no bloquea la entrega: se sustituye en
    el técnico (íntegro en F3), la fila sigue (PB-38) y queda una ADVERTENCIA de G3-MET-13 en el G3V de F7."""
    _contradictor_con(monkeypatch, texto, obedece)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r.get("entrega") != "BLOQUEADA" and "G3-MET-13" not in (r.get("g3_entregables") or {}).get("bloqueos", [])
    assert not any("_bloqueados" in v for v in r["entregables"].values())
    md = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    (e,) = [x for x in _abiertas_f3(b) if x["clase"] == "RV"]
    alt = _seccion(md, "#### 4.1.4 Alternativas descartadas relevantes", "## 5.")
    (fila,) = [x for x in alt.splitlines() if f"`{e['opp_id']}`" in x]
    assert texto not in md and "RISK-XYZ-999" not in md and not re.search(r"(?i)v[aá]lid", alt)
    assert "OBJ-XLK-02" in fila and "Resolver las objeciones fuertes con evidencia" in fila   # lo del ejecutor se queda
    s6 = _seccion(md, "## 6. Objeciones y respuestas", "## 7.")
    filas6 = [x for x in s6.splitlines() if x.startswith(f"| `{e['opp_id']}` (alternativa descartada) |")]
    assert filas6 and all(sint.TEXTO_RETIRADO_MET13 in x for x in filas6)
    assert any("| fuerte |" in x and x.endswith("| SIN_RESOLVER |") for x in filas6)
    # íntegro en F3 y avisado en HA
    assert any(texto in o["resumen"] for o in e["objeciones_internas"])
    (f7,) = [g for g in b.almacen.leer("HA", AS_OF) if g.get("tipo_entrada") == "G3V" and g.get("fase") == "F7"]
    m13 = next(c for c in f7["comprobaciones"] if c["id"] == "G3-MET-13")
    assert m13["resultado"] == "ADVERTENCIA" and any(f"alternativa {e['opp_id']} retirado del técnico" in d for d in m13["detalle"])
    assert f7["dictamen_efectivo"] == "APTO_CON_ADVERTENCIAS"


def test_la_sustitucion_cubre_nombre_resumen_respuesta_y_que_la_resolveria(ciclo_rv):
    b, _, _ = ciclo_rv
    malo = "Una sola raíz, validada con ST-DESC-001."
    mot = [{"codigo": "OBJECION_FUERTE", "detalle": "1 objeción(es) fuerte(s) sin resolver"}]
    f = _f("OPP-2026-0001", False, motivos=mot, proxy="XLK", nombre="Sector validado por ST-DESC-001",
           _objeciones=[_fuerte("OBJ-X-01", resumen=malo, respuesta=malo, que_la_resolveria=malo),
                        {"objecion_id": "OBJ-X-02", "fuerza": "moderada", "resumen": "Moderada limpia", "respuesta": None},
                        # sin método en el propio texto: la regla A no salta sola, pero en el técnico la tabla es un párrafo
                        {"objecion_id": "OBJ-X-03", "fuerza": "moderada", "resumen": "Tesis validada por el mercado.", "respuesta": None}])
    ext = {"seleccion": {"RV": {"candidatos": [f]}}}
    (a,) = sint.alternativas_descartadas({"clases": {}}, ext, b)["RV"]
    assert a["nombre"] == "XLK" and a["condicion"] == ["Resolver las objeciones fuertes con evidencia"]
    assert [(o["resumen"], o["respuesta"]) for o in a["objeciones"]] == [(sint.TEXTO_RETIRADO_MET13, sint.TEXTO_RETIRADO_MET13),
                                                                       ("Moderada limpia", None), (sint.TEXTO_RETIRADO_MET13, None)]
    assert a["retirados"] == ["«qué la resolvería» de OBJ-X-01", "nombre", "resumen de OBJ-X-01", "respuesta de OBJ-X-01",
                              "resumen de OBJ-X-03"]
    # sin bloque no se sustituye nada (el técnico de las pruebas unitarias); con un texto limpio, tampoco
    (s,) = sint.alternativas_descartadas({"clases": {}}, ext)["RV"]
    assert s["nombre"] == "Sector validado por ST-DESC-001" and s["retirados"] == []
    res = {"comprobaciones": [{"id": "G3-MET-13", "nombre": "x", "resultado": "BLOQUEO", "incidencias": []}], "dictamen": "BLOQUEADO",
           "resumen": {}}
    assert sint.advertir_alternativas_retiradas(res, {"RV": [a]}) and res["comprobaciones"][0]["resultado"] == "BLOQUEO"   # no rebaja
    res2 = {"comprobaciones": [], "dictamen": "APTO", "resumen": {}}
    assert sint.advertir_alternativas_retiradas(res2, {"RV": [s]}) == [] and res2["comprobaciones"] == []
    assert sint.advertir_alternativas_retiradas(res2, {"RV": [a]}) and res2["comprobaciones"][0]["resultado"] == "ADVERTENCIA"
    assert res2["dictamen"] == "APTO_CON_ADVERTENCIAS"


def test_tecnico_sin_seleccion_en_extras_no_cambia(ciclo_rv):
    b, r, _ = ciclo_rv
    md = Redaccion.tecnico(b.redaccion, r["paquete"], {"gc0": r["gc0"]}, {"dictamen": "APTO"}, {}, "COMPLETO", {})
    assert "Alternativas descartadas" not in md and "(alternativa descartada)" not in md


def test_pb38_tambien_en_el_diseno_v6(tmp_path, universo, monkeypatch):
    """En el V6 de solo RV el simulado resuelve la objeción fuerte; aquí el Contradictor la deja sin resolver (contrarréplica no
    convencida). En el V6 de doce clases salen sin forzar nada (4.2.4 y 4.4.4, revisor r01_03)."""
    from conftest import config_pruebas

    from bloque_a import mock_respuestas
    original = mock_respuestas.responder

    def responder(agente, mensajes, semilla):
        d = original(agente, mensajes, semilla)
        if isinstance(d, dict) and isinstance(d.get("resultados"), list):
            d = dict(d, resultados=[dict(x, resuelta=False) if isinstance(x, dict) and "objecion_id" in x else x for x in d["resultados"]])
        return d
    monkeypatch.setattr(mock_respuestas, "responder", responder)
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(diseno="v6"))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    md = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    abiertas = [x for x in _abiertas_f3(b) if x["clase"] == "RV" and x["opp_id"] not in
                {o["opp_id"] for o in r["paquete"]["clases"]["RV"]["opciones"]} and not x.get("_vigente")]
    assert abiertas, "el simulado debe dejar una objeción fuerte sin resolver también en el V6"
    alt = _seccion(md, "#### 4.1.4 Alternativas descartadas relevantes", "## 5.")
    s6 = _seccion(md, "## 6. Objeciones y respuestas", "## 7.")
    for e in abiertas:
        assert f"`{e['opp_id']}`" in alt
        assert any(x.startswith(f"| `{e['opp_id']}` (alternativa descartada) | fuerte |") and x.endswith("| SIN_RESOLVER |")
                   for x in s6.splitlines())
    assert r.get("entrega") != "BLOQUEADA"


def test_un_bloqueo_de_g3_met13_no_queda_tapado_por_seis_alternativas_retiradas_en_el_g3v():
    """QA r02 (H-04): el G3V de F7 guarda cinco detalles por comprobación; los BLOQUEOS van siempre delante."""
    from bloque_a.redaccion import detalles_g3v
    res = {"comprobaciones": [{"id": "G3-MET-13", "nombre": "x", "resultado": "BLOQUEO", "resumen": {},
                               "incidencias": [{"severidad": "ADVERTENCIA", "ruta": "informes_clase", "detalle": "aviso previo"},
                                               {"severidad": "BLOQUEO", "ruta": "informe_visual", "detalle": "bloqueo del visual"}]}],
           "dictamen": "BLOQUEADO", "resumen": {}}
    alts = {"RV": [{"opp_id": f"OPP-2026-{n:04d}", "retirados": ["nombre"]} for n in range(1, 7)]}
    assert len(sint.advertir_alternativas_retiradas(res, alts)) == 6
    (c,) = res["comprobaciones"]
    assert c["resultado"] == "BLOQUEO"
    d = detalles_g3v(c)
    assert len(d) == 5 and d[0] == "bloqueo del visual"
    assert d[1:] == [f"G3-MET-13: texto de la alternativa OPP-2026-{n:04d} retirado del técnico (nombre); íntegro en F3" for n in range(1, 5)]
    # las incidencias ya quedan con los BLOQUEOS delante (también los que añade el técnico después) ...
    assert c["incidencias"][0]["severidad"] == "BLOQUEO"
    # ... y el G3V los pone delante aunque lleguen detrás
    crudo = {"incidencias": [{"severidad": "ADVERTENCIA", "detalle": f"a{n}"} for n in range(6)] + [{"severidad": "BLOQUEO", "detalle": "b"}]}
    assert detalles_g3v(crudo) == ["b", "a0", "a1", "a2", "a3"]


def test_el_bloqueo_que_anade_el_tecnico_va_delante_de_las_advertencias_de_las_alternativas(ciclo_rv):
    b, _, _ = ciclo_rv
    res = {"comprobaciones": [{"id": "G3-MET-13", "nombre": "x", "resultado": "OK", "incidencias": [], "datos": {"fichas_citadas": []}}],
           "dictamen": "APTO", "resumen": {}}
    sint.advertir_alternativas_retiradas(res, {"RV": [{"opp_id": f"OPP-2026-{n:04d}", "retirados": ["nombre"]} for n in range(1, 7)]})
    assert sint.g3_met13_tecnico(b, res, "El método ST-DESC-001 está validado.")
    (c,) = res["comprobaciones"]
    assert c["resultado"] == "BLOQUEO" and c["incidencias"][0]["severidad"] == "BLOQUEO" and len(c["incidencias"]) == 7
