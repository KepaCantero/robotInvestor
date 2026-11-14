"""T-126 · Los dos casos del Plan de pruebas que no tenían prueba: PB-26 (clasificación temática y orden por calidad de F7,
F8 y F9) y PB-48 (conflicto de normas: la más restrictiva, R23)."""
import itertools
import re
from pathlib import Path

import pytest
from bloque_a.configuracion import cargar_config
from bloque_a.herramientas import ht02
from bloque_a.referencias import Referencias
from conftest import AS_OF, nuevo_bloque

RAIZ = Path(__file__).resolve().parents[2]
DOC0 = next((RAIZ / "01_Gobernanza").glob("Documento 0*.md")).read_text(encoding="utf-8")
PREFIJO = {"F7": "TA", "F8": "TM", "F9": "TF"}


def _taxonomia():
    """Códigos temáticos del Anexo D del Documento 0, por archivo."""
    anexo = DOC0[DOC0.index("## ANEXO D."):DOC0.index("## ANEXO E.")]
    return {k: set(re.findall(rf"\b({p}-\d{{2}})\b", anexo)) for k, p in PREFIJO.items()}


def _nivel_de(q):
    """13.3 del Documento 0: A (Q ≥ 80), B (65–79), C (50–64), D (< 50)."""
    return "A" if q >= 80 else "B" if q >= 65 else "C" if q >= 50 else "D"


@pytest.fixture(scope="module")
def refs():
    return Referencias(cargar_config())


# ---------------------------------------------------------------- PB-26
@pytest.mark.parametrize("archivo", ["F7", "F8", "F9"])
def test_pb26_cada_referencia_esta_en_una_tematica_del_anexo_d(refs, archivo):
    tax = _taxonomia()[archivo]
    fichas = refs.fichas[archivo]
    assert len(tax) >= 10 and len(fichas) > 300
    assert [f["ref_id"] for f in fichas if f["tematica"] not in tax] == []           # 100 % con temática válida


@pytest.mark.parametrize("archivo", ["F7", "F8", "F9"])
def test_pb26_dentro_de_cada_tematica_el_orden_es_por_calidad_descendente(refs, archivo):
    secciones: dict[str, list] = {}
    for f in refs.fichas[archivo]:
        secciones.setdefault(f["tematica"], []).append(f)
    inversiones = []
    for tem, fs in secciones.items():
        for a, b in itertools.pairwise(fs):
            if b["q"] > a["q"]:
                inversiones.append((tem, a["ref_id"], a["q"], b["ref_id"], b["q"]))
    assert inversiones == []                                                           # 0 inversiones


@pytest.mark.parametrize("archivo", ["F7", "F8", "F9"])
def test_pb26_el_nivel_es_coherente_con_la_calidad(refs, archivo):
    malos = [(f["ref_id"], f["q"], f["nivel"]) for f in refs.fichas[archivo] if f["nivel"] != _nivel_de(f["q"])]
    assert malos == []


def test_pb26_una_fuente_de_nivel_d_esta_marcada_como_candidata_a_baja_o_unica(refs):
    texto = {k: Path(p).read_text(encoding="utf-8") for k, p in refs.rutas.items() if k in PREFIJO}
    d = [(k, f["ref_id"]) for k in PREFIJO for f in refs.fichas[k] if f["nivel"] == "D"]
    for k, rid in d:
        lineas = texto[k].splitlines()
        ficha = next(x for x in ht02.leer_fichas(lineas) if x.id == rid)
        cuerpo = " ".join(str(v) for v in ficha.campos.values()).lower() if hasattr(ficha, "campos") else ""
        assert "baja" in cuerpo or "única" in cuerpo or "unica" in cuerpo, (k, rid)


def test_pb26_la_comprobacion_detecta_un_orden_o_un_nivel_mal_puestos(refs):
    """La comprobación no es vacía: un desorden, un nivel o una temática inventados se ven."""
    fs = [dict(f) for f in refs.fichas["F7"][:3]]
    fs[0]["q"], fs[1]["q"] = fs[1]["q"] - 1, fs[0]["q"] + 1
    assert any(b["q"] > a["q"] for a, b in itertools.pairwise(fs))
    assert _nivel_de(79) == "B" and _nivel_de(80) == "A" and _nivel_de(49) == "D" and _nivel_de(50) == "C"
    assert "TA-99" not in _taxonomia()["F7"]


# ---------------------------------------------------------------- PB-48
def _lecciones_que_relajan(b):
    b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": "LEC-2026-0901", "fecha": AS_OF, "ambito": {"clase": "RV"},
                                       "nivel": "A", "tipo": "OPERATIVA", "observacion": "La segunda pasada en banda marginal cuesta",
                                       "evidencia": [], "recomendacion": "Omitir la segunda pasada en banda marginal para ahorrar",
                                       "fuerza": "estadistica", "n": 40, "caducidad": "2027-06-05", "estado": "VIGENTE",
                                       "origen": "DETERMINISTA"})


def test_pb48_una_guia_que_relaja_un_control_no_llega_a_la_elegibilidad(tmp_path, universo, monkeypatch):
    """R23: la regla más restrictiva manda. Una lección vigente que sugiere omitir la segunda pasada en banda marginal
    (contradice 9.1) llega al Analista como contexto, pero la elegibilidad la decide HT-03 por código, y lo que HT-03 recibe
    no lleva lecciones: ninguna opción entregada deja de cumplir los controles por la lección."""
    from bloque_a.herramientas import ht03
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    _lecciones_que_relajan(b)
    entradas = []
    original = ht03.evaluar_opcion

    def anotar(op, *args, **kwargs):
        entradas.append(op)
        return original(op, *args, **kwargs)
    monkeypatch.setattr(ht03, "evaluar_opcion", anotar)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert entradas and all("Omitir la segunda pasada" not in repr(e) for e in entradas)
    for o in r["paquete"]["clases"]["RV"]["opciones"]:
        f3 = b.almacen.estado("F3")[o["opp_id"]]
        assert f3["elegible"] and not [m for m in f3.get("motivos_no_elegible") or []]


def test_pb48_ht03_exige_la_segunda_pasada_en_banda_marginal():
    """La regla de 9.1 vive en el código de HT-03: sin segunda pasada, una opción en banda marginal no es elegible."""
    import sys
    sys.path.insert(0, str(RAIZ / "10_Herramientas" / "tests"))
    from bloque_a.herramientas import ht03
    from test_ht03_puntuaciones import dims, opcion, todas
    sin = ht03.evaluar_opcion(opcion(dimensiones=dims(70, 60, 70)))
    assert not sin["elegible"] and "PS8_BANDA_MARGINAL" in [m["codigo"] for m in sin["motivos_no_elegible"]]
    con = ht03.evaluar_opcion(opcion(dimensiones=dims(70, 60, 70), segunda_pasada={"E": todas("E", 60)}))
    assert con["elegible"]
