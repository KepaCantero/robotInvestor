"""T-165 QA r06 · la reescritura R22 en `Bloque._invocar`: los agentes excluidos, el bucle, la cota y la incidencia (R8).

- `test_excluido_no_llega_*`: se marca todo texto libre (cadenas con un espacio) de las respuestas simuladas de cada agente de
  `ht09.AGENTES_SIN_TEXTO_ENTREGADO` con un marcador propio y se buscan en el paquete y en los tres entregables. Esperado:
  ningún marcador llega (si llega, ese agente no puede estar excluido).
- `test_excluido_con_raiz_*`: lo mismo con la raíz: ni retira opciones ni bloquea.
- `test_bucle_*`: con un modelo que nunca obedece, cada llamada cubierta se repite como mucho `redaccion.reescrituras_r22` veces.
- `test_incidencia_*`: la incidencia de H-39 en HA solo lleva texto de la respuesta (no del mensaje ni del contexto).

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r06_01_agentes_excluidos_y_bucle.py -rf
"""
import collections
import importlib.util
import json
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location("r01_02", Path(__file__).with_name("r01_02_extremo_a_extremo.py"))
r01 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r01)
AS_OF, nuevo_bloque, mock_respuestas, config_pruebas = r01.AS_OF, r01.nuevo_bloque, r01.mock_respuestas, r01.config_pruebas
universo = r01.universo   # fixture

from bloque_a.herramientas import ht09  # noqa: E402
from bloque_a.orquestacion import Bloque  # noqa: E402

V6 = {"diseno": "v6", "auditoria": {"en_backtest": True}}


def _marcar(d, marca):
    if isinstance(d, str):
        return f"{d} {marca}" if " " in d else d
    if isinstance(d, dict):
        return {k: _marcar(v, marca) for k, v in d.items()}
    if isinstance(d, list):
        return [_marcar(v, marca) for v in d]
    return d


def _sembrar_excluidos(monkeypatch, con_raiz):
    original = mock_respuestas.responder

    def responder(agente, mensajes, semilla):
        d = original(agente, mensajes, semilla)
        if agente in ht09.AGENTES_SIN_TEXTO_ENTREGADO:
            marca = f"zq{agente.replace('-', '')}" + (" validado" if con_raiz else "")
            return _marcar(d, marca)
        return d
    monkeypatch.setattr(mock_respuestas, "responder", responder)


def _ciclo(tmp_path, universo, cfg_extra, clases=("RV", "RF")):
    cfg = config_pruebas(**cfg_extra) if cfg_extra else None
    b = nuevo_bloque(tmp_path, universo, cfg=cfg) if cfg else nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": list(clases)})
    return b, r


def _textos(r):
    t = {k: Path(v).read_text(encoding="utf-8") for k, v in (r.get("entregables") or {}).items()}
    t["paquete_en_memoria"] = json.dumps(r["paquete"], ensure_ascii=False)
    return t


def _n(r):
    return sum(len(d["opciones"]) for d in r["paquete"]["clases"].values())


@pytest.mark.parametrize("diseno", ["v5", "v6"])
def test_excluido_no_llega_al_entregable(diseno, tmp_path, universo, monkeypatch):
    _sembrar_excluidos(monkeypatch, con_raiz=False)
    _, r = _ciclo(tmp_path, universo, V6 if diseno == "v6" else None)
    llegan = {k: sorted({w for w in t.split() if w.startswith("zqAG")}) for k, t in _textos(r).items()}
    llegan = {k: v for k, v in llegan.items() if v}
    print("\n  marcadores en los entregables:", llegan)
    assert not llegan


@pytest.mark.parametrize("diseno", ["v5", "v6"])
def test_excluido_con_raiz_no_retira_ni_bloquea(diseno, tmp_path, universo, monkeypatch):
    cfg = V6 if diseno == "v6" else None
    n0 = _n(_ciclo(tmp_path / "b", universo, cfg)[1])
    _sembrar_excluidos(monkeypatch, con_raiz=True)
    b, r = _ciclo(tmp_path / "s", universo, cfg)
    print("\n  opciones", n0, "→", _n(r), "· entrega", r.get("entrega"))
    assert _n(r) == n0 and r.get("entregables") and r.get("entrega") != "BLOQUEADA"


@pytest.mark.parametrize("diseno", ["v5", "v6"])
@pytest.mark.parametrize("n", [1, 2])
def test_bucle_acotado_con_un_modelo_que_nunca_obedece(diseno, n, tmp_path, universo, monkeypatch):
    """Toda respuesta de un agente cubierto lleva la raíz siempre (también en la reescritura): cada llamada original se repite
    como mucho n veces, y no hay reescritura de una reescritura."""
    monkeypatch.setattr(mock_respuestas, "_obedece_r22", lambda msg, d: d)
    original = mock_respuestas.responder

    def responder(agente, mensajes, semilla):
        d = original(agente, mensajes, semilla)
        if agente not in ht09.AGENTES_SIN_TEXTO_ENTREGADO and isinstance(d, dict):
            d = {**d, "autoevaluacion": "Sin validar."}
        return d
    monkeypatch.setattr(mock_respuestas, "responder", responder)
    vistas = []
    orig = Bloque._invocar_una

    def espia(self, agente, contrato, mensaje, esquema, *a, **k):
        re_ = isinstance(mensaje, dict) and isinstance(mensaje.get("reescritura"), dict) and bool(mensaje["reescritura"].get("r22"))
        vistas.append((agente, esquema, re_))
        return orig(self, agente, contrato, mensaje, esquema, *a, **k)
    monkeypatch.setattr(Bloque, "_invocar_una", espia)
    extra = {**(V6 if diseno == "v6" else {}), "redaccion": {"reescrituras_r22": n}}
    b, r = _ciclo(tmp_path, universo, extra, clases=("RV",))
    orig_c = collections.Counter((a, e) for a, e, x in vistas if not x)
    re_c = collections.Counter((a, e) for a, e, x in vistas if x)
    print("\n  originales:", dict(orig_c), "\n  reescrituras:", dict(re_c))
    for k, v in re_c.items():
        assert v <= n * orig_c[k], (k, v, orig_c[k])
    assert not any(a in ht09.AGENTES_SIN_TEXTO_ENTREGADO for a, _ in re_c)
    incs = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "reescrita por la raíz" in e.get("detalle", "")]
    assert len(incs) == sum(re_c.values())


def test_incidencia_solo_lleva_texto_de_la_respuesta(tmp_path, universo, monkeypatch):
    """La frase sembrada en la respuesta llega a `frases_r22`; un texto del mensaje (la pregunta del Broker, el universo) no."""
    r01._sembrar(monkeypatch, "valoracion", lambda x: x + " ST-DESC-001 está validado en backtest.")
    b, r = _ciclo(tmp_path, universo, None, clases=("RV",))
    incs = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and e.get("frases_r22") is not None]
    print("\n  incidencias:", [(i["detalle"], len(i["frases_r22"])) for i in incs][:4])
    assert incs and all(len(i["frases_r22"]) <= 10 for i in incs)
    assert all(len(f["texto"]) <= 200 for i in incs for f in i["frases_r22"])
    assert any("validado en backtest" in f["texto"] for i in incs for f in i["frases_r22"])
