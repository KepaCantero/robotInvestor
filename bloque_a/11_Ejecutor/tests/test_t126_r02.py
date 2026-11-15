"""T-126 · Ronda r02: hallazgos de la QA r01 (`.docs/tickets/T-126/qa.md`).

- H-01: en un ciclo, una opción en banda marginal se resuelve con la segunda pasada del Analista, que llega a HT-03 y queda
  registrada en F3, con la lección que sugiere omitirla vigente (PB-48; J5 del revisor).
- H-02: cada referencia está en la sección `## TX-nn` de su temática (no solo su campo «Temática»; J4) y, a igualdad de Q,
  la más reciente va primero (desempate por fecha, con la regla para los documentos sin año de publicación).
- H-03: las comprobaciones de PB-26 son funciones y se ejecutan también sobre fichas estropeadas (no son vacías).
- H-04: la lección que relaja el control llega al Analista de RV en su CT-06.
"""
import itertools
import re
from pathlib import Path

import pytest
from bloque_a.configuracion import cargar_config
from bloque_a.herramientas import ht02, ht03
from bloque_a.referencias import Referencias
from conftest import AS_OF, nuevo_bloque
from test_t126_pb26_pb48 import _lecciones_que_relajan, _nivel_de, _taxonomia

from bloque_a import mock_respuestas

RE_ANIO = re.compile(r"^\s*((?:19|20)\d{2})\b")


@pytest.fixture(scope="module")
def refs():
    return Referencias(cargar_config())


# ---------------------------------------------------------------- comprobaciones de PB-26 (H-03: funciones reutilizables)
def fichas_con_seccion(ruta: Path) -> list[dict]:
    """Fichas de un archivo en su orden, con la sección `## TX-nn` en la que están físicamente, su campo «Temática», su Q y el
    año de publicación del campo «Año» (None si no es un año: «Documento vivo», sin fecha…)."""
    lineas = Path(ruta).read_text(encoding="utf-8").splitlines()
    inicio = {f.linea_inicio: f for f in ht02.leer_fichas(lineas)}
    out, seccion = [], None
    for i, ln in enumerate(lineas):
        m = re.match(r"^## (T[AMF]-\d{2})\b", ln)
        if m:
            seccion = m.group(1)
        if i in inicio:
            f = inicio[i]
            tem = re.search(r"\b(T[AMF]-\d{2})\b", f.campo("Temática", "Ámbito metodológico") or "")
            anio = RE_ANIO.match(f.campo("Año") or "")
            out.append({"ref_id": f.id, "seccion": seccion, "tematica": tem.group(1) if tem else None, "q": f.q, "nivel": f.nivel,
                        "anio": int(anio.group(1)) if anio else None})
    return out


def fuera_de_su_seccion(fichas):
    return [(f["ref_id"], f["tematica"], f["seccion"]) for f in fichas if f["tematica"] != f["seccion"]]


def inversiones_de_q(fichas):
    return [(a["ref_id"], b["ref_id"]) for a, b in itertools.pairwise(fichas) if a["seccion"] == b["seccion"] and b["q"] > a["q"]]


def desempates_al_reves(fichas):
    """A igualdad de Q dentro de una sección, la de fecha más reciente primero (Documento 0, 13.3). Solo se comparan dos fichas
    con año de publicación; un documento sin año («Documento vivo») no tiene fecha con la que desempatar (`[PROPUESTO]`,
    INC-T126-01)."""
    return [(a["ref_id"], a["anio"], b["ref_id"], b["anio"]) for a, b in itertools.pairwise(fichas)
            if a["seccion"] == b["seccion"] and a["q"] == b["q"] and a["anio"] is not None and b["anio"] is not None
            and b["anio"] > a["anio"]]


def niveles_incoherentes(fichas):
    return [(f["ref_id"], f["q"], f["nivel"]) for f in fichas if f["nivel"] != _nivel_de(f["q"])]


def tematicas_invalidas(fichas, tax):
    return [f["ref_id"] for f in fichas if f["tematica"] not in tax]


@pytest.mark.parametrize("archivo", ["F7", "F8", "F9"])
def test_h02_cada_referencia_esta_fisicamente_en_la_seccion_de_su_tematica(refs, archivo):
    fichas = fichas_con_seccion(refs.rutas[archivo])
    assert len(fichas) == len(refs.fichas[archivo]) > 300
    assert fuera_de_su_seccion(fichas) == [] and inversiones_de_q(fichas) == []
    assert tematicas_invalidas(fichas, _taxonomia()[archivo]) == [] and niveles_incoherentes(fichas) == []


@pytest.mark.parametrize("archivo", ["F7", "F8", "F9"])
def test_h02_a_igualdad_de_q_va_primero_la_mas_reciente(refs, archivo):
    fichas = fichas_con_seccion(refs.rutas[archivo])
    assert desempates_al_reves(fichas) == []


def test_h02_el_caso_dudoso_es_un_documento_sin_anio(refs):
    """ANA-DOC-0522 (2016) va antes que ANA-DOC-0089 con la misma Q: la segunda es un «Documento vivo» (su año, 2026, sale de
    la fecha de consulta), así que no tiene fecha de publicación con la que desempatar."""
    f7 = {f["ref_id"]: f for f in fichas_con_seccion(refs.rutas["F7"])}
    assert f7["ANA-DOC-0522"]["anio"] == 2016 and f7["ANA-DOC-0089"]["anio"] is None
    assert f7["ANA-DOC-0522"]["q"] == f7["ANA-DOC-0089"]["q"]
    assert next(f for f in refs.fichas["F7"] if f["ref_id"] == "ANA-DOC-0089")["anio"] == 2026   # el lector del ejecutor, en cambio


def test_h03_las_comprobaciones_detectan_fichas_estropeadas(refs):
    fichas = fichas_con_seccion(refs.rutas["F7"])
    tax = _taxonomia()["F7"]
    sec = [f for f in fichas if f["seccion"] == "TA-01"]
    assert len(sec) >= 3
    mal = [dict(f) for f in fichas]
    i = mal.index(next(f for f in mal if f["ref_id"] == sec[1]["ref_id"]))
    mal[i]["q"] = sec[0]["q"] + 1                                                          # J1: desorden por Q
    assert inversiones_de_q(mal)
    mal = [dict(f) for f in fichas]
    mal[0]["nivel"] = "B" if mal[0]["nivel"] != "B" else "A"                              # J2: nivel incoherente
    assert niveles_incoherentes(mal)
    mal = [dict(f) for f in fichas]
    mal[0]["tematica"] = "TA-99"                                                           # J3: temática inventada
    assert tematicas_invalidas(mal, tax) and fuera_de_su_seccion(mal)
    mal = [dict(f) for f in fichas]
    j = mal.index(next(f for f in mal if f["ref_id"] == sec[-1]["ref_id"]))
    mal[j]["seccion"] = "TA-02"                                                            # J4: en la sección equivocada
    assert fuera_de_su_seccion(mal) == [(sec[-1]["ref_id"], "TA-01", "TA-02")]
    a, b = sec[0], sec[1]
    empate = [{**a, "q": 90, "anio": 2010}, {**b, "q": 90, "anio": 2020}]                  # desempate al revés
    assert desempates_al_reves(empate) and not desempates_al_reves(empate[::-1])
    assert not desempates_al_reves([{**a, "q": 90, "anio": 2010}, {**b, "q": 90, "anio": None}])


# ---------------------------------------------------------------- PB-48 en un ciclo (H-01 y H-04)
@pytest.fixture
def ciclo_pb48(tmp_path, universo, monkeypatch):
    """El caso del plan: la lección que sugiere omitir la segunda pasada vigente y el Analista que, aun así, la hace para
    todas las dimensiones (la regla más restrictiva, 9.1). Se anotan las entradas y salidas de HT-03 y los CT-06."""
    original = mock_respuestas._ficha

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f["segunda_pasada"] = {k: dict(v) for k, v in f["dimensiones"].items() if isinstance(v, dict)}
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    evaluadas = []
    evaluar = ht03.evaluar_opcion

    def anotar(op, *args, **kwargs):
        r = evaluar(op, *args, **kwargs)
        evaluadas.append((op, r))
        return r
    monkeypatch.setattr(ht03, "evaluar_opcion", anotar)
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    _lecciones_que_relajan(b)
    ct06 = []
    crear = b.mensajeria.crear

    def anotar_msg(contrato, emisor, receptor, cuerpo, **kw):
        if contrato == "CT-06":
            ct06.append((receptor, cuerpo))
        return crear(contrato, emisor, receptor, cuerpo, **kw)
    monkeypatch.setattr(b.mensajeria, "crear", anotar_msg)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    return b, r, [(op, res) for op, res in evaluadas if op.get("opp_id") != "PROV"], ct06


def test_h01_en_el_ciclo_una_opcion_en_banda_marginal_se_resuelve_con_su_segunda_pasada(ciclo_pb48):
    b, _, evaluadas, _ = ciclo_pb48
    marginales = [(op, res) for op, res in evaluadas if res["banda_marginal"]]
    assert marginales                                                                     # el paso 2 del plan se ejerce
    for op, res in marginales:
        assert op["segunda_pasada"]                                                       # HT-03 recibe la segunda pasada
        assert all(bm["resuelta"] and "total_segunda_pasada" in bm for bm in res["banda_marginal"])
        assert "PS8_BANDA_MARGINAL" not in [m["codigo"] for m in res["motivos_no_elegible"]]
    f3 = b.almacen.estado("F3")
    registradas = [op["opp_id"] for op, _ in marginales if op["opp_id"] in f3]
    assert registradas and all(f3[o].get("segunda_pasada") for o in registradas)          # segunda pasada registrada


def test_h04_la_leccion_que_relaja_el_control_llega_al_analista_en_su_ct06(ciclo_pb48):
    _, _, evaluadas, ct06 = ciclo_pb48
    analista_rv = [c for _, c in ct06 if c.get("clase") == "RV" and c.get("fase") in ("CRIBADO_E_INVESTIGACION", "REVISION_VIGENTES")]
    assert analista_rv and all("LEC-2026-0901" in c["lecciones"] for c in analista_rv)    # llega como contexto
    assert evaluadas and all("LEC-2026-0901" not in repr(op) for op, _ in evaluadas)       # pero no a la elegibilidad


def test_h01_sin_la_segunda_pasada_esas_opciones_no_serian_elegibles(ciclo_pb48):
    """Contraprueba: las mismas entradas sin segunda pasada quedan fuera por PS8 (lo que haría la guía si se obedeciera)."""
    b, _, evaluadas, _ = ciclo_pb48
    marginales = [op for op, res in evaluadas if res["banda_marginal"]]
    assert marginales
    for op in marginales:
        sin = ht03.evaluar_opcion({**op, "segunda_pasada": {}}, b.params_ht03)
        assert "PS8_BANDA_MARGINAL" in [m["codigo"] for m in sin["motivos_no_elegible"]]
