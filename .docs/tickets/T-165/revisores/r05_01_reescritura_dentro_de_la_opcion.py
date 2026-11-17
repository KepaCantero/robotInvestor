"""T-165 QA r05 · la reescritura R22 dentro de las opciones (CT-06 y CT-13, H-33 y H-34) y el simulado que obedece.

- `test_coste_*`: ¿se reescribe el informe de clase entero por un campo que el ejecutor sobrescribe de todos modos
  (`estado_madurez_metodos`, que los prompts de los Analistas piden con «documentado, implementado o validado»)?
- `test_traza_*`: una madurez falsa («validado» de una ficha IMPLEMENTADO) que la reescritura quita, ¿deja rastro en HA? R22:
  «Presentar como validado lo que no lo está es un hallazgo».
- `test_debil_*`: con el simulado obediente (por defecto), ¿siguen ejerciéndose los bloqueos de G3-MET-13 dentro de una opción?

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r05_01_reescritura_dentro_de_la_opcion.py -rf
"""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("r01_02", Path(__file__).with_name("r01_02_extremo_a_extremo.py"))
r01 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r01)
AS_OF, nuevo_bloque, mock_respuestas = r01.AS_OF, r01.nuevo_bloque, r01.mock_respuestas
universo = r01.universo   # fixture

from bloque_a.orquestacion import Bloque  # noqa: E402


def _llamadas(monkeypatch):
    vistas = []
    original = Bloque._invocar

    def espia(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k):
        vistas.append((agente, contrato, esquema, bool(isinstance(mensaje, dict) and mensaje.get("reescritura"))))
        return original(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k)
    monkeypatch.setattr(Bloque, "_invocar", espia)
    return vistas


def _n(r):
    return sum(len(d["opciones"]) for d in r["paquete"]["clases"].values())


def test_coste_estado_madurez_no_dispara_la_reescritura_del_informe(tmp_path, universo, monkeypatch):
    """El Analista declara la madurez como pide su prompt (R22) en `estado_madurez_metodos`. El ejecutor la sobrescribe
    (`canonizar_madurez`): no hace falta reescribir el informe de clase, la llamada más cara del ciclo."""
    original = mock_respuestas._ficha
    monkeypatch.setattr(mock_respuestas, "_ficha", lambda u, msg, ctx, rng, iny: {
        **original(u, msg, ctx, rng, iny), "estado_madurez_metodos": "ST-DESC-001: implementado, no validado"})
    vistas = _llamadas(monkeypatch)
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    ct06 = [x for x in vistas if x[1] == "CT-06" and x[2] == "INFORME_CLASE"]
    print("\n  CT-06 INFORME_CLASE (reescritura):", [x[3] for x in ct06])
    assert not any(x[3] for x in ct06), "se reescribe el informe de clase por un campo que el ejecutor sobrescribe"


def test_traza_madurez_falsa_reescrita_queda_en_ha(tmp_path, universo, monkeypatch):
    """«ST-DESC-001 está validado en backtest» (ficha IMPLEMENTADO): la reescritura la quita. Esperado: el hallazgo R22 consta en
    HA (como `canonizar_madurez` deja lo descartado desde la r04)."""
    r01._sembrar(monkeypatch, "valoracion", lambda x: x + " ST-DESC-001 está validado en backtest con diez años de datos.")
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    textos = {k: Path(v).read_text(encoding="utf-8").lower() for k, v in (r.get("entregables") or {}).items()}
    print("\n  entrega:", r.get("entrega"), "· opciones", _n(r),
          "· «validado en backtest» entregado:", any("validado en backtest" in t for t in textos.values()),
          "· «comprobar en backtest»:", any("comprobar en backtest" in t for t in textos.values()))
    assert not any("validado en backtest" in t for t in textos.values())
    ha = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "validado en backtest" in str(e).lower()]
    assert ha, "la madurez falsa que dijo el modelo desaparece sin rastro (R22: es un hallazgo)"


def test_debil_bloqueo_dentro_de_la_opcion_con_modelo_desobediente(tmp_path, universo, monkeypatch):
    """Control: sin obediencia, la raíz que persiste retira la opción (falla cerrado)."""
    monkeypatch.setattr(mock_respuestas, "_obedece_r22", lambda msg, d: d)
    n0 = _n(nuevo_bloque(tmp_path / "b", universo).ciclo(AS_OF, alcance={"clases": ["RV"]}))
    r01._sembrar(monkeypatch, "valoracion", lambda x: x + " ST-DESC-001 está validado en backtest.")
    r = nuevo_bloque(tmp_path / "s", universo).ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert _n(r) < n0


def test_debil_contradictor_desobediente_retira(tmp_path, universo, monkeypatch):
    monkeypatch.setattr(mock_respuestas, "_obedece_r22", lambda msg, d: d)
    vistas = _llamadas(monkeypatch)
    original = mock_respuestas._contrarias

    def contrarias(msg, ctx, rng):
        d = original(msg, ctx, rng)
        for x in d.get("resultados", []):
            for o in x.get("objeciones", []):
                o["que_la_resolveria"] = "Una validación fuera de muestra del impulso"
        return d
    monkeypatch.setattr(mock_respuestas, "_contrarias", contrarias)
    r = nuevo_bloque(tmp_path, universo).ciclo(AS_OF, alcance={"clases": ["RV"]})
    refut = [x[3] for x in vistas if x[2] == "REFUTACION"]
    print("\n  REFUTACION (reescritura):", refut, "· opciones", _n(r))
    assert refut == [False, True] and _n(r) == 0


# ------------------------------------------------------------------ otros textos dentro de la opción sin reescritura
def test_fp_prospectiva_declara_r22(tmp_path, universo, monkeypatch):
    """Prompt de Prospectiva, R22: «Declaras el estado de madurez de cada método (documentado, implementado, validado)». Su texto
    va al pronóstico de la opción; CT-12 no tiene reescritura."""
    vistas = _llamadas(monkeypatch)
    n0 = _n(nuevo_bloque(tmp_path / "b", universo).ciclo(AS_OF, alcance={"clases": ["RV"]}))
    original = mock_respuestas._prospectiva

    def pros(msg, ctx, rng):
        d = original(msg, ctx, rng)
        for x in d["resultados"]:
            for h in x["escenarios"].values():
                h["base"] = "continuidad (ACC-MOM-001, implementado y aún no validado)"
        return d
    monkeypatch.setattr(mock_respuestas, "_prospectiva", pros)
    r = nuevo_bloque(tmp_path / "s", universo).ciclo(AS_OF, alcance={"clases": ["RV"]})
    print("\n  PROSPECTIVA (reescritura):", [x[3] for x in vistas if x[2] == "PROSPECTIVA"][-2:], "· opciones", n0, "→", _n(r))
    assert _n(r) == n0


def test_fp_respuesta_a_objeciones(tmp_path, universo, monkeypatch):
    """El Analista responde a la objeción (CT-06, RESPUESTA_OBJECIONES): su respuesta va a `objeciones[].respuesta`; sin reescritura."""
    n0 = _n(nuevo_bloque(tmp_path / "b", universo).ciclo(AS_OF, alcance={"clases": ["RV"]}))
    original = mock_respuestas._analista

    def analista(msg, ctx, rng, iny):
        d = original(msg, ctx, rng, iny)
        for x in d.get("respuestas", []):
            x["respuesta"] = "El impulso se ha validado con los datos de HT-01 de las últimas cuatro semanas."
        return d
    monkeypatch.setattr(mock_respuestas, "_analista", analista)
    r = nuevo_bloque(tmp_path / "s", universo).ciclo(AS_OF, alcance={"clases": ["RV"]})
    print("\n  opciones", n0, "→", _n(r))
    assert _n(r) == n0
