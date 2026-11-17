"""T-165 QA r04 · la reescritura R22 (H-28) y sus límites, de extremo a extremo con el cliente simulado (sin red ni gasto).

- `test_reescritura_*`: la reescritura no abre camino a una madurez falsa, sigue el número de la configuración y falla cerrado.
- `test_laguna_*`: qué le llega al Broker de una laguna del Analista que lleva la raíz.
- `test_fp_contradictor_*`: el Contradictor (AG-11, REFUTACION) no recibe la regla R22; su objeción natural («validación fuera
  de muestra») está dentro de la opción.
- `test_limite_fondos_*`: el ejemplo de Fondos del corpus, con un Analista que sí sigue la regla en la reescritura… que no hay.

Las siembras escriben la raíz solo en la primera respuesta (como un modelo que obedece la reescritura), salvo donde se dice.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r04_01_reescritura_y_limites.py -rf
"""
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


def _llamadas(monkeypatch):
    vistas = []
    original = Bloque._invocar

    def espia(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k):
        vistas.append((agente, esquema, bool(isinstance(mensaje, dict) and mensaje.get("reescritura")), instrucciones))
        return original(self, agente, contrato, mensaje, esquema, instrucciones, *a, **k)
    monkeypatch.setattr(Bloque, "_invocar", espia)
    return vistas


def _entregado(b, r):
    return bool(r.get("entregables")) and r.get("entrega") != "BLOQUEADA" and not any(
        "_bloqueados" in v for v in (r.get("entregables") or {}).values())


def _textos_entregados(r):
    return {k: Path(v).read_text(encoding="utf-8") for k, v in (r.get("entregables") or {}).items()}


def _n_opciones(r):
    return sum(len(d["opciones"]) for d in r["paquete"]["clases"].values())


# ------------------------------------------------------------------ la reescritura no abre camino a una madurez falsa
def test_reescritura_con_forma_canonica_falsa_bloquea(tmp_path, universo, monkeypatch):
    """La reescritura quita la raíz de la prosa pero imita la forma canónica con VALIDADO: G3-MET-13 lo vuelve a leer."""
    original = mock_respuestas._integracion

    def integ(msg, ctx, rng):
        d = original(msg, ctx, rng)
        if msg.get("reescritura"):
            d["lectura_conjunto"] = "Las opciones usan ST-DESC-001 [madurez: VALIDADO] y dependen del impulso."
        return d
    monkeypatch.setattr(mock_respuestas, "_integracion", integ)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    txt = _textos_entregados(r)
    assert not (_entregado(b, r) and any("madurez: validado" in t.lower() for t in txt.values())), r.get("entrega")


def test_reescritura_con_canonica_de_otro_nivel_bloquea(tmp_path, universo, monkeypatch):
    """ML-CLUS-001 en DOCUMENTADO en el Catálogo; la reescritura (sin raíz) la declara IMPLEMENTADO en forma canónica: regla C."""
    r01._documentado(monkeypatch)
    original = mock_respuestas._integracion

    def integ(msg, ctx, rng):
        d = original(msg, ctx, rng)
        if msg.get("reescritura"):
            d["lectura_conjunto"] = "Los clústeres salen de ML-CLUS-001 [madurez: IMPLEMENTADO]."
        return d
    monkeypatch.setattr(mock_respuestas, "_integracion", integ)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    txt = _textos_entregados(r)
    assert not (_entregado(b, r) and any("ml-clus-001 [madurez: implementado]" in t.lower() for t in txt.values()))


# ------------------------------------------------------------------ el número sale de la configuración y falla cerrado
@pytest.mark.parametrize("n", [0, 2])
def test_reescritura_sigue_la_configuracion(n, tmp_path, universo, monkeypatch):
    """Con la raíz que persiste: 1 + n llamadas a la integración, y bloqueo (falla cerrado)."""
    original = mock_respuestas._integracion
    monkeypatch.setattr(mock_respuestas, "_integracion",
                        lambda msg, ctx, rng: {**original(msg, ctx, rng), "lectura_conjunto": "Aún no validado."})
    vistas = _llamadas(monkeypatch)
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas(redaccion={"reescrituras_r22": n}))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    integ = [x for x in vistas if x[0] == "AG-02" and x[1] == "INTEGRACION"]
    assert len(integ) == 1 + n and [x[2] for x in integ] == [False] + [True] * n
    assert not _entregado(b, r)


def test_reescritura_sin_respuesta_falla_cerrado(tmp_path, universo, monkeypatch):
    """La reescritura no da respuesta (None): se queda la primera, con la raíz, y G3-MET-13 bloquea."""
    original = Bloque._invocar

    def invocar(self, agente, contrato, mensaje, *a, **k):
        if isinstance(mensaje, dict) and mensaje.get("reescritura") and agente == "AG-02":
            return None
        return original(self, agente, contrato, mensaje, *a, **k)
    monkeypatch.setattr(Bloque, "_invocar", invocar)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert not _entregado(b, r)
    assert any(ht09.tiene_raiz_valid(x) for x in r["paquete"]["limitaciones"])


def test_reescritura_instruccion_de_la_integracion(monkeypatch, tmp_path, universo):
    """La reescritura de la integración ¿lleva la instrucción original? (la del Redactor y la del Sintetizador sí)."""
    vistas = _llamadas(monkeypatch)
    b = nuevo_bloque(tmp_path, universo)
    b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    prim, re_ = [x[3] for x in vistas if x[0] == "AG-02" and x[1] == "INTEGRACION"]
    print("\n  primera:", prim[:200], "\n  reescritura:", re_[:200])
    assert "No cambies la selección" in re_, "la reescritura pierde «No cambies la selección: la ha hecho HT-03»"


def test_reescritura_coste_en_la_bolsa_comun(tmp_path, universo, monkeypatch):
    """La reescritura se contabiliza (bolsa COMÚN) como una llamada más de AG-02."""
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    cons = b.contabilidad.resumen(r["run_id"])["por_agente"]
    print("\n  AG-02:", cons.get("AG-02"))
    assert cons["AG-02"]["llamadas"] == 2 and cons["AG-02"]["uc"] > 0


# ------------------------------------------------------------------ lagunas
def _analista_parcial(monkeypatch, laguna):
    original = mock_respuestas._analista

    def analista(msg, ctx, rng, inyectado):
        d = original(msg, ctx, rng, inyectado)
        if msg.get("fase") == "CRIBADO_E_INVESTIGACION":
            d["estado"] = "PARCIAL"
            d["lagunas"] = [laguna]
        return d
    monkeypatch.setattr(mock_respuestas, "_analista", analista)


LAGUNAS = {
    "divisas_prompt": "Validación pendiente de la batería mínima del perfil FX; decláralo así (R22).",
    "dato_no_comprobado": "No se pudo validar el dato de flujos del proveedor: falta la serie de posicionamiento.",
}


@pytest.mark.parametrize("caso", sorted(LAGUNAS))
def test_laguna_con_la_raiz_llega_al_broker(caso, tmp_path, universo, monkeypatch):
    """Esperado: el Broker sabe QUÉ no se pudo comprobar (la carencia), aunque sin la palabra. Obtenido en la r04: un texto genérico."""
    _analista_parcial(monkeypatch, LAGUNAS[caso])
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    lim = [x for x in r["paquete"]["limitaciones"] if "alcance reducido" in x]
    print("\n  limitaciones:", lim, "· entregado:", _entregado(b, r))
    assert _entregado(b, r)
    clave = "batería mínima" if caso == "divisas_prompt" else "posicionamiento"
    assert any(clave in x for x in lim), f"la carencia no llega al Broker: {lim}"


# ------------------------------------------------------------------ el Contradictor no recibe la regla
def test_fp_contradictor_objecion_fuera_de_muestra(tmp_path, universo, monkeypatch):
    """La objeción más natural contra una señal cuantitativa: «falta validación fuera de muestra». La escribe AG-11 (REFUTACION),
    cuya instrucción no lleva `REGLA_R22_REDACCION`; va a `objeciones[].resumen` y `que_cambiaria_la_conclusion` de la opción."""
    vistas = _llamadas(monkeypatch)
    n0 = _n_opciones(nuevo_bloque(tmp_path / "base", universo).ciclo(AS_OF, alcance={"clases": ["RV"]}))
    original = mock_respuestas._contrarias

    def contrarias(msg, ctx, rng):
        d = original(msg, ctx, rng)
        for x in d.get("resultados", []):
            for o in x.get("objeciones", []):
                if o.get("fuerza") == "moderada":
                    o["que_la_resolveria"] = "Una validación fuera de muestra del impulso"
        return d
    monkeypatch.setattr(mock_respuestas, "_contrarias", contrarias)
    b = nuevo_bloque(tmp_path / "fp", universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    refut = [x[3] for x in vistas if x[1] == "REFUTACION"]
    print("\n  regla en REFUTACION:", [ht09.REGLA_R22_REDACCION in i for i in refut], "· opciones", n0, "→", _n_opciones(r))
    assert _n_opciones(r) == n0, "el Contradictor retira las opciones con su objeción"


def test_regla_en_la_refutacion():
    from bloque_a import diseno_v6
    assert ht09.REGLA_R22_REDACCION in diseno_v6.INSTR_REFUTACION


# ------------------------------------------------------------------ el límite dentro de una opción: Fondos del corpus
def test_limite_fondos_ejemplo_del_corpus_retira_la_opcion(tmp_path, universo, monkeypatch):
    """Límite declarado: dentro de una opción no hay reescritura. Se mide (no es un fallo del script si se retira)."""
    n0 = _n_opciones(nuevo_bloque(tmp_path / "base", universo).ciclo(AS_OF, alcance={"clases": ["RV"]}))
    r01._sembrar(monkeypatch, "valoracion", lambda x: x + " Las recompras y ventas de activos cerca del NAV validan las valoraciones.")
    b = nuevo_bloque(tmp_path / "fp", universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    print("\n  opciones", n0, "→", _n_opciones(r), "· entregado", _entregado(b, r))
    assert _n_opciones(r) < n0
