"""T-165 QA r01 · de extremo a extremo con el cliente simulado (sin red ni gasto): ¿llega a la entrega una madurez falsa con G3
APTO, y bloquea G3 un ciclo legítimo?

- `test_escapa_*`: el Analista simulado escribe en su informe de clase (campos `valoracion` o `mecanismo`, que pasan al técnico y al
  JSON) una madurez falsa con una redacción que la lectura de T-165 no ve. Lo que pide PB-47: G3 bloquea y ningún entregable lo
  dice. Si la prueba falla, la madurez falsa se entrega.
- `test_fp_*`: ciclos legítimos que G3-MET-13 no debería bloquear (ni retirar opciones).
- `test_control_*`: la siembra de la QA de T-159 sigue bloqueando (el banco no es vacuo).

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r01_02_extremo_a_extremo.py -rf
"""
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))
from conftest import AS_OF, config_pruebas, nuevo_bloque  # noqa: E402

from bloque_a import mock_respuestas  # noqa: E402
from bloque_a import sintesis as sint  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

assert Path(sint.__file__).resolve().is_relative_to(RAIZ.resolve()), f"importa otra copia: {sint.__file__}"


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _g3v(b, run_id):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V" and e["run_id"] == run_id]


def _met13(e):
    return next((c for c in e["comprobaciones"] if c["id"] == "G3-MET-13"), {})


def _documentado(monkeypatch, ficha="ML-CLUS-001"):
    original = servicio.madurez_catalogo
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: {**original(raiz), ficha: "DOCUMENTADO"})


def _sembrar(monkeypatch, campo, cambio):
    original = mock_respuestas._ficha
    sembradas = []

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f[campo] = cambio(f[campo])
        sembradas.append(u["simbolo"])
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    return sembradas


def _resultado(b, r, palabra="validad"):
    g3 = _g3v(b, r["run_id"])
    entregados = {k: Path(v).read_text(encoding="utf-8") for k, v in (r.get("entregables") or {}).items()}
    bloqueado = r.get("entrega") == "BLOQUEADA" or any("_bloqueados" in v for v in (r.get("entregables") or {}).values())
    con = sorted(k for k, t in entregados.items() if palabra in t.lower())
    n_op = sum(len(d["opciones"]) for d in r["paquete"]["clases"].values())
    resumen = {"g3": [(e.get("fase"), e["dictamen_efectivo"], _met13(e).get("resultado")) for e in g3],
               "entrega_bloqueada": bloqueado, "entregables_con_palabra": con, "opciones": n_op}
    print("\n", json.dumps(resumen, ensure_ascii=False))
    return resumen, entregados


def _entregada_con(res):
    return (not res["entrega_bloqueada"]) and bool(res["entregables_con_palabra"])


# ------------------------------------------------------------------ control: la siembra de la QA de T-159
def test_control_siembra_t159_bloquea(tmp_path, universo, monkeypatch):
    _documentado(monkeypatch)
    frase = "Los clústeres de exposición se calculan con ML-CLUS-001, un método validado."
    assert _sembrar(monkeypatch, "mecanismo", lambda x: f"{x} {frase}") is not None
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    res, _ = _resultado(b, r)
    assert res["g3"][0][1] == "BLOQUEADO" and res["g3"][0][2] == "BLOQUEO" and not _entregada_con(res)


# ------------------------------------------------------------------ ¿llega a la entrega una madurez falsa? (Catálogo real)
SIEMBRAS = {
    # la excepción «validado por» + «datos»: dicho del método (ST-DESC-001 está IMPLEMENTADO, no VALIDADO)
    "por_los_datos": ("valoracion", lambda x: x.rstrip(".") + ", un método validado por los datos de los últimos diez años.",
                      "validado por los datos"),
    # la misma afirmación en la frase siguiente
    "frase_siguiente": ("valoracion", lambda x: x + " Es un método validado en backtest.", "método validado en backtest"),
    # el pretérito
    "preterito": ("valoracion", lambda x: x + " ST-DESC-001 se validó en backtest con diez años de datos.", "se validó"),
    # la ficha con guiones no separables (U+2011)
    "guion_no_separable": ("valoracion", lambda x: x + " ST‑DESC‑001 está validado en backtest."),
}


@pytest.mark.parametrize("caso", sorted(SIEMBRAS))
def test_escapa_catalogo_real(caso, tmp_path, universo, monkeypatch):
    campo, cambio, marca = SIEMBRAS[caso]
    assert _sembrar(monkeypatch, campo, cambio) is not None
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    res, entregados = _resultado(b, r, palabra=marca)
    if _entregada_con(res):
        js = entregados.get("paquete_json", "")
        print("  estado_g3 del JSON entregado:", json.loads(js).get("estado_g3") if js else None)
    assert not _entregada_con(res), f"{caso}: entregado con «validad…» y G3 {res['g3']}"


def test_escapa_pb47_declarado_y_luego_validado(tmp_path, universo, monkeypatch):
    """PB-47 con ML-CLUS-001 en DOCUMENTADO: el informe lo declara documentado y, en la frase siguiente, «validado por los datos»."""
    _documentado(monkeypatch)
    _sembrar(monkeypatch, "mecanismo", lambda x: f"{x} Los clústeres usarían ML-CLUS-001 (documentado); en la práctica está "
                                                 "validado por los datos.")
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    res, _ = _resultado(b, r, palabra="validado por los datos")
    assert not _entregada_con(res), f"entregado con «validad…» y G3 {res['g3']}"


# ------------------------------------------------------------------ ¿bloquea de más?
def test_fp_prosa_financiera_retira_opciones(tmp_path, universo, monkeypatch):
    """«Ruptura validada por el volumen» en la valoración (otra acepción de «validado») junto a la ficha servida."""
    b0 = nuevo_bloque(tmp_path / "base", universo)
    r0 = b0.ciclo(AS_OF, alcance={"clases": ["RV"]})
    n0 = sum(len(d["opciones"]) for d in r0["paquete"]["clases"].values())
    _sembrar(monkeypatch, "valoracion", lambda x: "Ruptura alcista validada por el volumen, con el " + x[0].lower() + x[1:])
    b = nuevo_bloque(tmp_path / "fp", universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    res, _ = _resultado(b, r, palabra="ruptura alcista validada")
    print("  opciones sin la frase:", n0)
    assert res["opciones"] == n0 and all(x[2] == "OK" for x in res["g3"]), res


def test_fp_lectura_del_conjunto_bloquea_el_run(tmp_path, universo, monkeypatch):
    """El Analizador (integración) escribe prosa con «validado» en otro sentido y cita una ficha servida: fuera de una opción."""
    original = mock_respuestas._integracion

    def integ(msg, ctx, rng):
        d = original(msg, ctx, rng)
        d["lectura_conjunto"] = ("El impulso quedó validado por la amplitud del mercado, con caídas máximas contenidas "
                                 "(RISK-DD-001) en casi todas las opciones.")
        return d
    monkeypatch.setattr(mock_respuestas, "_integracion", integ)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    res, _ = _resultado(b, r, palabra="amplitud del mercado")
    assert not res["entrega_bloqueada"] and all(x[2] == "OK" for x in res["g3"]), res


def test_fp_v6_con_ml_clus_documentado_sin_siembra(tmp_path, universo, monkeypatch):
    """Diseño V6 (integración determinista, `factores_dominantes` vacío) y ML-CLUS-001 en DOCUMENTADO, sin ninguna siembra: el
    rótulo por defecto de `sintesis.construir` («… correlación semanal ≥ 0,7, ML-CLUS-001») nombra el método que el Motor no
    sirvió."""
    _documentado(monkeypatch)
    cfg = config_pruebas(diseno="v6", auditoria={"en_backtest": True})
    b = nuevo_bloque(tmp_path, universo, cfg=cfg)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    res, _ = _resultado(b, r, palabra="ml-clus-001")
    detalles = [d for e in _g3v(b, r["run_id"]) for d in _met13(e).get("detalle", [])]
    print("  G3-MET-13:", detalles[:2])
    assert not res["entrega_bloqueada"] and all(x[2] in ("OK", None) for x in res["g3"]), res


def test_fp_v5_sin_integracion_con_ml_clus_documentado(tmp_path, universo, monkeypatch):
    """Diseño V5, ML-CLUS-001 en DOCUMENTADO y la integración del Analizador no disponible (salida no conforme): el mismo rótulo."""
    _documentado(monkeypatch)
    monkeypatch.setattr(mock_respuestas, "_integracion", lambda msg, ctx, rng: {"no": "conforme"})
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    res, _ = _resultado(b, r, palabra="ml-clus-001")
    detalles = [d for e in _g3v(b, r["run_id"]) for d in _met13(e).get("detalle", [])]
    print("  G3-MET-13:", detalles[:2])
    assert not res["entrega_bloqueada"] and all(x[2] in ("OK", None) for x in res["g3"]), res


# ------------------------------------------------------------------ el informe de clase de una opción que sí llega a la entrega
def _sembrar_madurez(monkeypatch, valor):
    original = mock_respuestas._ficha

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f["estado_madurez_metodos"] = valor
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)


def test_control_estado_madurez_en_texto_retira_la_opcion(tmp_path, universo, monkeypatch):
    """`estado_madurez_metodos` (no pasa al entregable) dice «ST-DESC-001: validado»: F6 retira las opciones que lo afirman."""
    _sembrar_madurez(monkeypatch, "ST-DESC-001: validado")
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    res, _ = _resultado(b, r)
    assert res["g3"][0][1] == "BLOQUEADO" and res["opciones"] == 0


@pytest.mark.parametrize("valor", [{"ST-DESC-001": "validado"},
                                   [{"ficha_id": "ST-DESC-001", "estado_madurez": "validado"}],
                                   "ST-DESC-001: implementado.\nEl método está validado en backtest."])
def test_escapa_estado_madurez_de_una_opcion_entregada(valor, tmp_path, universo, monkeypatch):
    """Lo mismo en otra forma (objeto con la ficha en la clave, `ficha_id`, o la afirmación en la línea siguiente): la opción
    cuyo informe de clase lo afirma tendría que retirarse como en el control."""
    _sembrar_madurez(monkeypatch, valor)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    res, _ = _resultado(b, r)
    assert res["opciones"] == 0, f"{valor!r}: {res['opciones']} opciones entregadas con G3 {res['g3']}"
