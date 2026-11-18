"""QA r01 de T-177 (revisor independiente). Ataques a R8 y a la deduplicación del mantenimiento C4 del BFA.

Ejecutar desde bloque_a/11_Ejecutor:  python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-177/revisores/r01_ataques_r8.py
Los valores son ficticios y van partidos en dos cadenas. Una prueba marcada «HALLAZGO» documenta un fallo (pasa si el fallo
sigue presente); al corregirlo hay que invertir su aserción."""
import importlib
import json
import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor" / "tests"))
from conftest import AS_OF, config_pruebas, nuevo_bloque, universo  # noqa: E402,F401

from bloque_a.mantenimiento_c4 import mantenimiento_c4  # noqa: E402

mock_respuestas = importlib.import_module("bloque_a.mock_respuestas")
SECRETO = "QaFicticio" + "77ZzKk"          # 16 caracteres, letras y cifras: no es una credencial real
FICHA = {"servicio": "API de fondos cerrados", "uso_previsto": "Cribado de FON", "impacto_si_falta": "Datos públicos"}
BASE = {"servicio": FICHA["servicio"], "motivo": "m", "impacto_si_falta": "i"}


def _bloque(tmp, universo, servicios=(FICHA,), **kw):
    return nuevo_bloque(tmp, universo, cfg=config_pruebas(credenciales={"servicios_bfa": list(servicios)}), **kw)


def _ct25(b):
    return [m for m in b.mensajeria.registro if m.get("contrato") == "CT-25"] if isinstance(b.mensajeria.registro, list) else []


def _aparece(tmp, valor):
    return sorted(str(p.relative_to(tmp)) for p in Path(tmp).rglob("*")
                  if p.is_file() and p.name != "secretos.json" and valor in p.read_text(encoding="utf-8", errors="ignore"))


def _retorno(sol_o_extra, top=None):
    r = {"referencias": [], "sintesis": "s", "lagunas": []}
    if sol_o_extra is not None:
        r["solicitudes_credenciales"] = sol_o_extra
    r.update(top or {})
    return r


# Variantes que el código debe bloquear antes de la caché y no dejar en ningún archivo
BLOQUEADAS = {
    "plano": [{**BASE, "valor": SECRETO}],
    "anidado": [{**BASE, "detalle": {"extra": [{"secreto": SECRETO}]}}],
    "mayusculas": [{**BASE, "API_KEY": SECRETO}],
    "en_lista": [{**BASE, "token": [SECRETO]}],
    "motivo_etiquetado": [{**BASE, "motivo": "password=" + SECRETO}],
    "alias_sk": [{**BASE, "servicio": "svc sk-ant-api03-" + "AbCdEfGhIjKlMnOpQrStUvWx"}],
}


@pytest.mark.parametrize("nombre", sorted(BLOQUEADAS))
def test_r01_variantes_bloqueadas(tmp_path, universo, monkeypatch, nombre):
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: _retorno(BLOQUEADAS[nombre]))
    b = _bloque(tmp_path, universo)
    r = mantenimiento_c4(b, AS_OF)
    assert r["solicitudes"] == [] and r["estado_retorno"] == "SIN_RESULTADO", r
    marca = SECRETO if nombre != "alias_sk" else "AbCdEfGhIjKl"
    assert _aparece(tmp_path, marca) == []
    assert not [c for c in b.almacen.estado("F5").values() if c.get("tipo_entrada") == "CRD"]


# H-01: el bloqueo nuevo de `agentes.invocar` solo mira la clave exacta `solicitudes_credenciales`; un campo de valor en otro
# sitio del retorno (o con la clave en otra grafía) pasa la validación BUSQUEDA (admite campos adicionales), se guarda en la
# caché y solo después `desde_retorno` rechaza el retorno.
FUGA_CACHE = {
    "valor_en_raiz": _retorno([BASE], top={"valor": SECRETO}),
    "clave_en_mayusculas": {"referencias": [], "sintesis": "s", "lagunas": [],
                            "Solicitudes_Credenciales": [{**BASE, "valor": SECRETO}]},
}


@pytest.mark.parametrize("nombre", sorted(FUGA_CACHE))
def test_r01_HALLAZGO_H01_valor_fuera_de_la_clave_exacta_llega_a_la_cache(tmp_path, universo, monkeypatch, nombre):
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: FUGA_CACHE[nombre])
    b = _bloque(tmp_path, universo)
    r = mantenimiento_c4(b, AS_OF)
    # r02 (invertida): `llm.respuesta_segura` lo bloquea antes de la caché; el Coordinador no recibe nada
    assert r["estado_retorno"] == "SIN_RESULTADO" and r["solicitudes"] == []
    assert _aparece(tmp_path, SECRETO) == []


# H-02: la deduplicación entre C4 distintas compara `servicio` literal (`solicitar`), no el alias de la bóveda
def test_r01_HALLAZGO_H02_segunda_c4_con_otra_grafia_duplica_el_ct25(tmp_path, universo, monkeypatch):
    grafias = iter(["API de fondos cerrados", "api de fondos cerrados"])
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4",
                        lambda msg: _retorno([{**BASE, "servicio": next(grafias)}]))
    b = _bloque(tmp_path, universo)
    r1, r2 = mantenimiento_c4(b, AS_OF), mantenimiento_c4(b, AS_OF)
    crd = [c for c in b.almacen.estado("F5").values() if c.get("tipo_entrada") == "CRD"]
    assert r1["solicitudes"][0]["resultado"] == "SOLICITADA"
    assert r2["solicitudes"][0]["resultado"] == "YA_SOLICITADA"       # r02 (invertida)
    assert len(crd) == 1                                               # un solo CT-25 para el mismo alias


# Repetición: la misma C4 dos veces (misma grafía) no duplica
def test_r01_c4_repetida_no_duplica(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    r1, r2 = mantenimiento_c4(b, AS_OF), mantenimiento_c4(b, AS_OF)
    assert r1["solicitudes"][0]["resultado"] == "SOLICITADA" and r2["solicitudes"][0]["resultado"] == "YA_SOLICITADA"


# Concurrencia: dos procesos (dos Bloque sobre la misma carpeta de estado) a la vez
def test_r01_c4_concurrente_dos_bloques(tmp_path, universo):
    b1, b2 = _bloque(tmp_path, universo), _bloque(tmp_path, universo)
    barrera = threading.Barrier(2)
    for b in (b1, b2):
        orig = b.credenciales.solicitar

        def solicitar(*a, _o=orig, **kw):
            barrera.wait(timeout=30)
            return _o(*a, **kw)
        b.credenciales.solicitar = solicitar
    # r03 (adaptada por la implementación, observación de la QA r02): la C4 reserva la bolsa semanal dentro de la transacción,
    # así que dos C4 a la vez ya no llegan las dos a `solicitar` (la segunda queda SIN_PRESUPUESTO y la barrera no se
    # cumpliría). La carrera de H-03 se ejerce donde está, en el Coordinador: dos `desde_retorno` a la vez sobre el mismo estado
    retorno = {"solicitudes_credenciales": [dict(BASE)]}
    res = []
    hilos = [threading.Thread(target=lambda b=b: res.append(b.credenciales.desde_retorno(retorno, "AG-16", AS_OF)))
             for b in (b1, b2)]
    [h.start() for h in hilos]
    [h.join(60) for h in hilos]
    crd = [c for c in b1.almacen.estado("F5").values() if c.get("tipo_entrada") == "CRD"]
    print("CRD tras dos solicitudes concurrentes:", len(crd), [x["solicitudes"][0]["resultado"] for x in res])
    assert len(res) == 2 and len(crd) == 1                             # r02 (H-03)
    # y dos C4 a la vez: un solo CT-25 y la otra SIN_PRESUPUESTO (o YA_SOLICITADA si llega después)
    b3, b4 = _bloque(tmp_path / "c4", universo), _bloque(tmp_path / "c4", universo)
    res2 = []
    hilos = [threading.Thread(target=lambda b=b: res2.append(mantenimiento_c4(b, AS_OF))) for b in (b3, b4)]
    [h.start() for h in hilos]
    [h.join(120) for h in hilos]
    crd = [c for c in b3.almacen.estado("F5").values() if c.get("tipo_entrada") == "CRD"]
    print("C4 concurrentes:", [x["estado_retorno"] for x in res2])
    assert len(res2) == 2 and len(crd) == 1


# Límites de detección (documentados, no bloqueados): campo con otro nombre y valor sin etiqueta en el motivo
NO_DETECTADAS = {
    "campo_credencial": [{**BASE, "credencial": SECRETO}],
    "motivo_sin_etiqueta": [{**BASE, "motivo": "usar " + SECRETO}],
}


@pytest.mark.parametrize("nombre", sorted(NO_DETECTADAS))
def test_r01_limite_detector(tmp_path, universo, monkeypatch, nombre):
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: _retorno(NO_DETECTADAS[nombre]))
    b = _bloque(tmp_path, universo)
    r = mantenimiento_c4(b, AS_OF)
    print(nombre, r["rechazo"], [s["resultado"] for s in r["solicitudes"]], _aparece(tmp_path, SECRETO))
    assert r["solicitudes"] == [] and _aparece(tmp_path, SECRETO) == []   # r02 (H-05 y H-06)


# Falsos positivos: el bloqueo nuevo no toca retornos normales (solo mira `solicitudes_credenciales`)
def test_r01_sin_falsos_positivos_en_retornos_normales():
    from bloque_a.contratos import claves_valor_credencial
    normal = {"referencias": [{"ref_id": "R1", "valor": 3.2, "token": "x"}], "solicitudes_credenciales": None}
    assert claves_valor_credencial(normal.get("solicitudes_credenciales")) == []
    assert claves_valor_credencial([{**BASE}]) == []


# H-04: en modo «grabar», ReplayClient escribe el texto crudo en la cinta antes de que `agentes.invocar` aplique el bloqueo
# nuevo: la solicitud con un campo de valor que no entra en la caché sí entra en la grabación
def test_r01_HALLAZGO_H04_la_cinta_de_grabacion_guarda_el_valor(tmp_path, universo, monkeypatch):
    from bloque_a.llm import MockClient, ReplayClient
    monkeypatch.setattr(mock_respuestas, "_mantenimiento_c4", lambda msg: _retorno([{**BASE, "valor": SECRETO}]))
    cinta = tmp_path / "cinta.jsonl"
    b = _bloque(tmp_path, universo, cliente=ReplayClient(cinta, "grabar", MockClient()))
    r = mantenimiento_c4(b, AS_OF)
    assert r["solicitudes"] == [] and r["estado_retorno"] == "SIN_RESULTADO"
    assert _aparece(tmp_path, SECRETO) == []                           # r02 (invertida)
