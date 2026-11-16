"""T-159 QA r01 · sondas del revisor sobre los casos que se dan por «Superada» y sobre PB-52.

- PB-47 con la preparación completa del plan: además del método en DOCUMENTADO, «un informe de clase que lo describe como
  validado». El plan espera G3 BLOQUEADO hasta corregir la declaración (G3-MET-13). La siembra es la misma que usa la prueba
  de PB-30 o PB-39 (lo que devuelve el agente simulado).
- PB-52: qué deja en el almacén un ciclo que termina con la excepción de HT-09, y si el ciclo siguiente (con HT-09 de vuelta)
  arranca limpio o hereda algo del ciclo caído (opciones en F3 que nunca se entregaron, un RUN- a medias).
- PB-03 a escala: cuántas candidatas ALT llegan al análisis (el plan pide tres).

Las pruebas `test_hNN_*` afirman lo que pide el plan y FALLAN mientras el hallazgo NN siga abierto (ver qa.md).

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-159/revisores/r01_02_sondas.py
"""
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tests"))
from conftest import AS_OF, nuevo_bloque  # noqa: E402

from bloque_a import mock_respuestas  # noqa: E402
from bloque_a import sintesis as sint  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

FRASE = "Los clústeres de exposición se calculan con ML-CLUS-001, un método validado."


@pytest.fixture(scope="module")
def universo():
    return cargar_universo(RUTA_UNIVERSO_EJEMPLO)


def _g3v(b, run_id, fase="F6"):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V" and e["run_id"] == run_id and e.get("fase") == fase]


def test_h01_pb47_un_informe_que_llama_validado_al_metodo_documentado_no_se_entrega_asi(tmp_path, universo, monkeypatch):
    original_madurez = servicio.madurez_catalogo
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: {**original_madurez(raiz), "ML-CLUS-001": "DOCUMENTADO"})
    original = mock_respuestas._ficha
    sembradas = []

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        f["mecanismo"] = f"{f['mecanismo']} {FRASE}"
        f["valoracion"] = f"{f['valoracion']} {FRASE}"
        sembradas.append(u["simbolo"])
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    assert sembradas
    g3 = _g3v(b, r["run_id"]) + _g3v(b, r["run_id"], "F7")
    entregados = {k: Path(v).read_text(encoding="utf-8") for k, v in (r.get("entregables") or {}).items()}
    con_frase = sorted(k for k, t in entregados.items() if "validado" in t.lower())
    print("\nPB-47 · dictámenes G3:", [x["dictamen_efectivo"] for x in g3], "· entregables con «validado»:", con_frase)
    # Lo que pide el plan: G3 bloquea hasta corregir la declaración; ningún entregable presenta el método como validado
    assert not con_frase, f"entregados con «validado»: {con_frase} (dictámenes {[x['dictamen_efectivo'] for x in g3]})"


def test_pb52_lo_que_deja_un_ciclo_con_ht09_caido_y_el_ciclo_siguiente(tmp_path, universo, monkeypatch):
    def caido(*a, **k):
        raise RuntimeError("HT-09 no disponible")
    monkeypatch.setattr(sint, "ht09_validar", caido)
    b = nuevo_bloque(tmp_path, universo)
    antes = {a: len(b.almacen.leer(a)) for a in ("F1", "F2", "F3", "F4", "F5", "F6", "RC", "HA")}
    with pytest.raises(RuntimeError):
        b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    despues = {a: len(b.almacen.leer(a)) for a in antes}
    f3 = [e for e in b.almacen.estado("F3").values() if e.get("clase") == "RV"]
    run_f5 = [e for e in b.almacen.leer("F5") if str(e.get("id", "")).startswith("RUN-")]
    print("\nPB-52 · entradas añadidas por el ciclo caído:", {a: despues[a] - antes[a] for a in antes})
    print("PB-52 · F3 de RV:", sorted({(e.get("estado"), e.get("decision_broker", {}).get("decision") if isinstance(e.get("decision_broker"), dict) else None) for e in f3}, key=str),
          "· RUN- en F5:", [e.get("estado") for e in run_f5])
    assert b.almacen.verificar_integridad() and all(b.almacen.verificar_integridad().values())
    # El ciclo siguiente, con HT-09 de vuelta: arranca y entrega; ninguna opción del ciclo caído se da por «vigente»
    monkeypatch.undo()
    r2 = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r2["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS") and r2["entregables"]
    js = json.loads(Path(r2["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
    caidas = {e["opp_id"] for e in f3}
    vigentes = [o["opp_id"] for o in js["clases"]["RV"]["opciones"] if o.get("vigente_nueva") == "VIGENTE" or o.get("vigente")]
    print("PB-52 · opciones del ciclo caído en F3:", len(caidas), "· marcadas vigentes en el siguiente:", sorted(set(vigentes) & caidas))
    assert not (set(vigentes) & caidas), "una opción que nunca se entregó sale como vigente en el ciclo siguiente"


def test_pb03_cuantas_candidatas_alt_llegan_al_analisis(tmp_path, universo, monkeypatch):
    original = mock_respuestas._ficha
    alt = []

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        if msg["clase"] == "ALT":
            alt.append(u["simbolo"])
            f["invertibilidad"] = {"universo_suficiente": False, "nota": "Sin vehículo minorista."}
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["ALT"]})
    n_universo = int((universo["clase"] == "ALT").sum())
    print(f"\nPB-03 · ámbitos ALT en el universo de ejemplo: {n_universo}; analizados: {sorted(set(alt))}")
    assert alt
