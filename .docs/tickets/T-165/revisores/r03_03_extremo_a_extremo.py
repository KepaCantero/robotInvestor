"""T-165 QA r03 · de extremo a extremo con el cliente simulado (sin red ni gasto): el riesgo operativo del falso positivo con
frases que piden o traen los propios prompts del corpus y el ejecutor, dos escapes y la forma canónica frente al esquema.

- `test_fp_*`: la frase sale del corpus o del ejecutor (se cita de dónde). Esperado: el ciclo entrega sin perder opciones. Si la
  prueba falla, en un run real con esa redacción se retiran opciones o cae el run entero.
- `test_escapa_*`: madurez falsa que llega a la entrega con G3 APTO.
- `test_esquema_*`: la anotación canónica rompe el esquema del JSON entregado.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider -s ../../.docs/tickets/T-165/revisores/r03_03_extremo_a_extremo.py -rf
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


def _ciclo(tmp_path, universo, marca, clases=("RV",), cfg=None):
    b = nuevo_bloque(tmp_path, universo, cfg=cfg) if cfg else nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": list(clases)})
    res, entregados = r01._resultado(b, r, palabra=marca)
    js = entregados.get("paquete_json", "")
    res["estado_g3_json"] = json.loads(js).get("estado_g3") if js else None
    for e in r01._g3v(b, r["run_id"]):
        bloq = [c["id"] for c in e["comprobaciones"] if c["resultado"] == "BLOQUEO"]
        det = r01._met13(e).get("detalle") or [i.get("detalle") for i in r01._met13(e).get("incidencias", [])]
        print(f"  {e.get('fase')} bloqueos {bloq} · G3-MET-13: {[str(d)[:200] for d in det[:2]]}")
    return res


def _n_base(tmp_path, universo, clases=("RV",), cfg=None):
    b0 = nuevo_bloque(tmp_path / "base", universo, cfg=cfg) if cfg else nuevo_bloque(tmp_path / "base", universo)
    r0 = b0.ciclo(AS_OF, alcance={"clases": list(clases)})
    return sum(len(d["opciones"]) for d in r0["paquete"]["clases"].values())


def _sin_perdida(res, n0):
    return not res["entrega_bloqueada"] and res["opciones"] == n0 and all(x[2] == "OK" for x in res["g3"])


# ------------------------------------------------------------------ falsos positivos con frases del corpus o del ejecutor
FICHA = {
    # Ejemplo de ficha del prompt del Analista de Fondos (02_System_prompts, bloque JSON de la candidata), campo valoracion
    "fondos_ejemplo_del_prompt": ("valoracion", lambda x: x + " Las recompras y ventas de activos cerca del NAV validan las "
                                  "valoraciones.", "validan las valoraciones"),
    # Preguntas de los prompts de RF, Monetarios y Tipos: «¿Qué catalizador fechado puede validar o invalidar la tesis?»
    "catalizador_de_la_tesis": ("catalizadores", lambda x: [{**x[0], "evento": "Reunión del BCE, que puede validar la "
                                        "tesis"}] + x[1:], "validar la tesis"),
}


@pytest.mark.parametrize("caso", sorted(FICHA))
def test_fp_informe_de_clase(caso, tmp_path, universo, monkeypatch):
    n0 = _n_base(tmp_path, universo)
    campo, cambio, marca = FICHA[caso]
    r01._sembrar(monkeypatch, campo, cambio)
    res = _ciclo(tmp_path / "fp", universo, marca)
    print("  opciones sin la frase:", n0)
    assert _sin_perdida(res, n0), res


INTEGRACION = {
    # Prompt del Analizador, tabla de reglas: «R22 | Declaras si cada método usado está documentado, implementado o validado»
    "analizador_declara_r22": "Métodos usados (R22): ST-DESC-001 y RISK-DD-001, implementados y aún no validados.",
    # Prompt del Analizador, tabla de degradación: «Las finalistas afectadas quedan, como máximo, en «Pendiente de validación» (PS5)»
    "analizador_degradacion_ps5": "Contrarias no disponible: las finalistas de RF quedan, como máximo, en «Pendiente de "
                                          "validación» (PS5); el riesgo se mide con RISK-DD-001.",
}


@pytest.mark.parametrize("caso", sorted(INTEGRACION))
def test_fp_lectura_del_conjunto(caso, tmp_path, universo, monkeypatch):
    original = mock_respuestas._integracion

    def integ(msg, ctx, rng):
        d = original(msg, ctx, rng)
        d["lectura_conjunto"] = INTEGRACION[caso]
        return d
    monkeypatch.setattr(mock_respuestas, "_integracion", integ)
    res = _ciclo(tmp_path, universo, "valid", clases=("RV", "RF"))
    assert not res["entrega_bloqueada"] and all(x[2] == "OK" for x in res["g3"]), res


def test_fp_sintetizador_v6_repite_la_instruccion_del_ejecutor(tmp_path, universo, monkeypatch):
    """`diseno_v6.INSTR_SINTESIS` (texto del ejecutor) dice al Sintetizador «Sobre el paquete ya validado…» y «vienen calculadas
    y validadas». Si el modelo lo repite en la lectura del conjunto, cae la entrega en F7."""
    original = mock_respuestas._sintetizador

    def sint_(msg, ctx, rng):
        d = original(msg, ctx, rng)
        d["lectura_conjunto"] = "Sobre el paquete ya validado, las opciones dependen sobre todo del impulso de precios."
        return d
    monkeypatch.setattr(mock_respuestas, "_sintetizador", sint_)
    cfg = config_pruebas(diseno="v6", auditoria={"en_backtest": True})
    res = _ciclo(tmp_path, universo, "paquete ya validado", clases=("RV", "RF"), cfg=cfg)
    assert not res["entrega_bloqueada"], res


def test_fp_ruta_de_salida_con_la_raiz(tmp_path, universo):
    """Ciclo normal sin siembra; la carpeta de salida del operador se llama «validaciones». El técnico cita las rutas de sus
    entregables hermanos (texto del ejecutor) y G3-MET-13 las lee como prosa."""
    res = _ciclo(tmp_path / "validaciones", universo, "validaciones")
    assert not res["entrega_bloqueada"], res


# Los identificadores de los casos no llevan la raíz: el nombre de la prueba entra en la ruta temporal (ver la prueba anterior)
# ------------------------------------------------------------------ escapes
ESCAPA = {
    "raiz_con_tilde": ("valoracion", lambda x: x + " ST-DESC-001 es un método válido fuera de muestra.", "método válido"),
}


@pytest.mark.parametrize("caso", sorted(ESCAPA))
def test_escapa(caso, tmp_path, universo, monkeypatch):
    campo, cambio, marca = ESCAPA[caso]
    r01._sembrar(monkeypatch, campo, cambio)
    res = _ciclo(tmp_path, universo, marca)
    print("  estado_g3 del JSON entregado:", res["estado_g3_json"])
    assert not r01._entregada_con(res), f"{caso}: entregado con «{marca}» y G3 {res['g3']}"


def test_limite_sinonimo_llega_como_se_declara(tmp_path, universo, monkeypatch):
    """Límite declarado (no es hallazgo): un sinónimo sin la raíz llega a la entrega, con la madurez canónica al lado."""
    r01._sembrar(monkeypatch, "valoracion", lambda x: x + " ST-DESC-001 está probado en tres crisis.")
    res = _ciclo(tmp_path, universo, "probado en tres crisis")
    assert r01._entregada_con(res)


# ------------------------------------------------------------------ la forma canónica frente al esquema
def test_esquema_nombre_llano_con_ficha_cerca_del_maximo(tmp_path, universo, monkeypatch):
    """`nombre_llano` tiene maxLength 70 y el ejecutor lo recorta a 70; con una ficha dentro, la anotación (+24) lo pasa."""
    r01._sembrar(monkeypatch, "nombre_llano", lambda x: "Bolsa tecnológica barata según ST-DESC-001 y su rango")
    res = _ciclo(tmp_path, universo, "st-desc-001")
    assert not res["entrega_bloqueada"], res
