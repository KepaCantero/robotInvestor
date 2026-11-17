"""T-165 QA r03 · ataques a la lectura estructural de la r03 (reglas A, B y C, ámbito, forma canónica). Unitarios, con el
Catálogo real (81 IMPLEMENTADO, ninguna VALIDADO) y, en los casos PB-47, ML-CLUS-001 en DOCUMENTADO.

- `test_escapa_*`: lo que, según las reglas DECLARADAS de la r03 (INC-T165-01, ronda r03), tendría que bloquear y no bloquea.
- `test_limite_*`: lo que la r03 declara como límite (sinónimos, sin la raíz): se comprueba que el límite es el declarado; estas
  pruebas pasan si el comportamiento coincide con la declaración (no son hallazgos).
- `test_control_*`: lo que la r03 promete y sí hace.

Uso, desde bloque_a/11_Ejecutor:
    ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-165/revisores/r03_02_ataques_estructurales.py -rf
"""
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

RAIZ = Path.cwd()
sys.path.insert(0, str(RAIZ))
from bloque_a import sintesis as sint  # noqa: E402
from bloque_a.herramientas import ht09  # noqa: E402
from bloque_a.motor import servicio  # noqa: E402

assert Path(sint.__file__).resolve().is_relative_to(RAIZ.resolve()), f"importa otra copia: {sint.__file__}"
B = SimpleNamespace(motor=SimpleNamespace(raiz=None))
OPC = "paquete.clases.RV.opciones[OPP-2026-0001].valoracion"


def _res(texto, ruta=OPC):
    return sint._comprobar_met13(B, [(ruta, texto, "BLOQUEO")])["resultado"]


def _json(obj, ruta="informes_clase.RV[OPP-2026-0001]"):
    return sint._comprobar_met13(B, [(r, t, "BLOQUEO") for r, t in ht09.textos_de(obj, ruta)])["resultado"]


@pytest.fixture
def pb47(monkeypatch):
    original = servicio.madurez_catalogo
    monkeypatch.setattr(servicio, "madurez_catalogo", lambda raiz=None: {**original(raiz), "ML-CLUS-001": "DOCUMENTADO"})


# ------------------------------------------------------------------ escapes a las reglas declaradas
ESCAPA = {
    # V1 · la raíz con tilde («válido», «válida»): misma raíz que «validez», que sí cuenta; no está entre los límites declarados
    "V1a_valido": "ST-DESC-001 es un método válido fuera de muestra.",
    "V1b_valida": "La estrategia de ST-DESC-001 es válida en tres crisis.",
    "V1c_mayusculas": "ST-DESC-001: MÉTODO VÁLIDO.",
}


@pytest.mark.parametrize("caso", sorted(ESCAPA))
def test_escapa(caso):
    assert _res(ESCAPA[caso]) == "BLOQUEO", ESCAPA[caso]


# Sustantivos de método que no están en la lista, en un ámbito sin fichas (límite declarado en general; estos son variantes
# directas de la lista: «metodología» de «método», «fuera de la muestra» de «fuera de muestra»)
CASI_LISTA = {
    "M1_metodologia": "La metodología de selección está validada con veinte años de datos.",
    "M2_fuera_de_la_muestra": "Señal compuesta validada fuera de la muestra.",
    "M3_sistema": "Nuestro sistema de selección está validado.",
}


@pytest.mark.parametrize("caso", sorted(CASI_LISTA))
def test_escapa_casi_lista(caso):
    assert _res(CASI_LISTA[caso]) == "BLOQUEO", CASI_LISTA[caso]


# ------------------------------------------------------------------ límites declarados (deben pasar: así está declarado)
LIMITE = ["ST-DESC-001 está probado en tres crisis y contrastado fuera de muestra.", "RISK-DD-001 es un método fiable y robusto.",
          "ST-DESC-001 ha superado el backtest con diez años de datos.", "ST-DESC-001 is a proven, tested method.",
          "ST-DESC-001 está apto para producción."]


@pytest.mark.parametrize("t", LIMITE)
def test_limite_sinonimos_pasan_como_se_declara(t):
    assert _res(t) == "OK"


def test_limite_forma_canonica_imitada_de_una_ficha_no_servida(pb47):
    """Declarado: el modelo puede escribir la forma canónica correcta de una ficha no servida y nombrarla en uso."""
    assert _res("Los clústeres salen de ML-CLUS-001 [madurez: DOCUMENTADO; no la sirve el Motor] y agrupan las series.") == "OK"


# ------------------------------------------------------------------ controles
CONTROL_BLOQUEA = ["ST-DESC-001 [madurez: VALIDADO]", "ST-DESC-001 [madurez: IMPLEMENTADO] y en la práctica validado.",
                   "[madurez: IMPLEMENTADO]", "ST-DESC-001 no está validado.", "El Motor de cálculo está validado.",
                   "ST_DESC_001 validado.", "ST-DESC-0001 validado.", "vol garch 001 validado.", "VOL‑GARCH‑001 validado."]


@pytest.mark.parametrize("t", CONTROL_BLOQUEA)
def test_control_bloquea(t):
    assert _res(t) == "BLOQUEO"


def test_control_ambito_otro_campo():
    textos = [("paquete.clases.RV.opciones[OPP-2026-0001].valoracion", "Precio en el percentil 80 (ST-DESC-001).", "BLOQUEO"),
              ("paquete.clases.RV.opciones[OPP-2026-0001].mecanismo", "Es un método validado en backtest.", "BLOQUEO")]
    assert sint._comprobar_met13(B, textos)["resultado"] == "BLOQUEO"


@pytest.mark.parametrize("obj", [{"ficha": "ST-DESC-001", "validado": True}, {"ST-DESC-001": "validated"},
                                 {"ficha": "ST-DESC-001", "nivel_madurez": "3"}, {"ficha": "ST-DESC-001", "madurez": {"nivel": "x"}}])
def test_control_json(obj):
    assert _json(obj) == "BLOQUEO"


def test_control_pb47_sin_canonica(pb47):
    assert _res("ML-CLUS-001 no fue rechazado y agrupa las series.") == "BLOQUEO"


def test_control_canonizar_descarta_lo_del_modelo():
    c = {"opp_id": "OPP-2026-0001", "valoracion": "Percentil (ST-DESC-001).", "estado_madurez_metodos": "ST-DESC-001: validado"}
    sint.canonizar_madurez(B, {"RV": {"candidatos": [c]}})
    assert c["estado_madurez_metodos"] == "ST-DESC-001 [madurez: IMPLEMENTADO]"
    assert _json(c) == "OK"
