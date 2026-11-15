"""T-122 · Hallazgos abiertos de la QA r01 de T-120 (H-01 y H-02) y de la QA r02 de T-113 (H-10 y H-12)."""
import json

import pytest
from bloque_a.almacen import Almacen
from bloque_a.contratos import DatosSensibles, secretos_en_texto
from bloque_a.evaluador import (
    LECCIONES_POR_ENCARGO_MAX,
    Evaluador,
    lecciones_por_encargo,
)
from bloque_a.llm import contenido_sensible
from conftest import AS_OF, config_pruebas, nuevo_bloque

DIGITOS = "91" + "21000418450200051332"           # IBAN de ejemplo de la documentación bancaria, partido
G = [DIGITOS[i:i + 4] for i in range(2, 22, 4)]


# ---------------------------------------------------------------- T-120 H-01 · formas corrientes del IBAN
@pytest.mark.parametrize("texto", [
    "ES" + DIGITOS[:2] + " " + " ".join(G),                         # espacio duro (copiado de una web o un PDF)
    "ES" + DIGITOS[:2] + " " + " ".join(G),                         # espacio estrecho
    "ES" + DIGITOS[:2] + " " + " ".join([G[0], G[1], G[2][:2], G[2][2:] + G[3] + G[4]]),   # formato impreso: 4 4 2 10
    "ES" + DIGITOS[:2] + "  " + "  ".join(G),                                 # dos espacios
    "ES" + DIGITOS[:2] + "- " + "- ".join(G),                                 # guion y espacio
    "ES" + DIGITOS[:2] + "   " + "   ".join(G),                               # tres separadores (T-123 r02, H-01)
    "ES" + DIGITOS[:2] + "\t" + "\t".join(G),
    "cobren en ES" + DIGITOS + " gracias",                                    # todo junto, como antes
    "es" + DIGITOS[:2] + " " + " ".join(G), "Es" + DIGITOS,                   # en minúsculas
])
def test_t120_h01_el_iban_se_detecta_en_sus_formas_corrientes(texto):
    assert secretos_en_texto(texto)


@pytest.mark.parametrize("texto", [
    "ES" + DIGITOS[:2] + " " + " ".join(G)[:-1],                              # una cifra de menos
    "ES" + DIGITOS[:2] + " " + " ".join(G) + "0",                             # una de más
    "ES" + DIGITOS[:2] + "    " + "    ".join(G),                             # cuatro separadores (T-123 r02: tres sí)
    "RES" + DIGITOS, "xES" + DIGITOS,                                         # pegado a una letra
    "ISIN ES0113900J37 y ES0000012B88", "El índice ES50 cerró en 4 900 puntos el 2026-06-05.",
    "Entre 2100 0418 4502 y 0005 1332 hay series de cuatro cifras.",
])
def test_t120_h01_lo_que_no_es_un_iban_no_se_marca(texto):
    assert secretos_en_texto(texto) == []


def test_t120_h01_un_ct04_con_un_iban_con_espacio_duro_se_rechaza_y_no_queda_en_ningun_archivo(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    iban = "ES" + DIGITOS[:2] + " " + " ".join(G)
    with pytest.raises(DatosSensibles):
        b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": f"cobren en {iban}"}}, AS_OF)
    for p in tmp_path.rglob("*"):
        if p.is_file():
            cuerpo = p.read_text(encoding="utf-8", errors="ignore")
            assert iban not in cuerpo and G[1] + " " + G[2] not in cuerpo, p


# ---------------------------------------------------------------- T-120 H-02 · el máximo de lecciones falla cerrado
@pytest.mark.parametrize("valor", [0, -1, -3, LECCIONES_POR_ENCARGO_MAX + 1, 1000, 2.7, 1e3, True, False, "4", [4]])
def test_t120_h02_un_maximo_de_lecciones_mal_formado_falla_al_crear_el_evaluador(tmp_path, valor):
    cfg = config_pruebas(aprendizaje={"lecciones_por_encargo": valor})
    with pytest.raises(ValueError, match="lecciones_por_encargo"):
        lecciones_por_encargo(cfg)
    with pytest.raises(ValueError, match="lecciones_por_encargo"):
        Evaluador(Almacen(tmp_path), None, None, cfg, None)


@pytest.mark.parametrize("valor", [1, 4, LECCIONES_POR_ENCARGO_MAX])
def test_t120_h02_un_maximo_valido_se_acepta(valor):
    assert lecciones_por_encargo(config_pruebas(aprendizaje={"lecciones_por_encargo": valor})) == valor


# ---------------------------------------------------------------- T-113 H-10 y H-12 (A1b) · diccionarios dentro de conjuntos
class _DictConHash(dict):
    """Un diccionario que puede ir dentro de un conjunto (ninguna parte del paquete lo produce hoy)."""
    def __hash__(self):
        return id(self)


SECRETO = _DictConHash({"pass" + "word": "abcdef"})


@pytest.mark.parametrize("valor", [
    {"a": frozenset({SECRETO})},                                 # H-10: un conjunto colgado de un diccionario
    {"a": [{"b": {SECRETO}}]},
    [frozenset({SECRETO})],                                      # A1b: un conjunto colgado de una lista
    (frozenset({SECRETO}),),
    frozenset({SECRETO}),
])
def test_t113_h10_un_diccionario_dentro_de_un_conjunto_se_ve(valor):
    assert contenido_sensible(valor)


def test_t113_h10_sin_secreto_sigue_dando_falso():
    assert not contenido_sensible({"a": frozenset({_DictConHash({"nombre": "abcdef"})}), "b": [1, 2]})


# ---------------------------------------------------------------- T-113 H-12 (B7) · una cola demasiado anidada se quita
def test_t113_h12_una_ultima_linea_demasiado_anidada_se_quita_al_seguir_grabando(tmp_path):
    from bloque_a.herramientas.ht06_indice import acabar_en_salto
    ruta = tmp_path / "cache_resultados.jsonl"
    buena = b'{"clave": "a", "valor": 1}\n'
    ruta.write_bytes(buena + b"[" * 200000 + b"]" * 200000)      # sin salto final y demasiado honda para json.loads
    acabar_en_salto(ruta)
    assert ruta.read_bytes() == buena


# ---------------------------------------------------------------- T-113 H-12 (C1) · lo descartado de la cinta se declara
def test_t113_h12_las_lineas_descartadas_de_la_cinta_se_declaran_al_arrancar(tmp_path, universo):
    from bloque_a.llm import MockClient

    class _ConCinta(MockClient):
        descartadas = 3
    b = nuevo_bloque(tmp_path, universo, cliente=_ConCinta())
    inc = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "grabación del cliente" in e.get("detalle", "")]
    assert len(inc) == 1 and inc[0]["tipo"] == "HERRAMIENTA" and ": 3 línea" in inc[0]["detalle"]
    b2 = nuevo_bloque(tmp_path / "otro", universo)
    assert not [e for e in b2.almacen.leer("HA") if "grabación del cliente" in e.get("detalle", "")]


def test_t113_h12_el_volcado_de_un_conjunto_es_json(tmp_path):
    from bloque_a.llm import _json_por_defecto
    assert json.loads(json.dumps({"a": frozenset({1})}, default=_json_por_defecto)) == {"a": [1]}


def test_t113_h10_un_diccionario_con_claves_que_no_son_texto_dentro_de_un_conjunto_sigue_siendo_error():
    """Como antes de T-113: un diccionario con claves que no son texto es un error del llamador."""
    with pytest.raises(TypeError):
        contenido_sensible({"a": frozenset({_DictConHash({("x", 1): "abcdef"})})})


# ---------------------------------------------------------------- T-122 QA r01 · H-14
@pytest.mark.parametrize("max_n", [0, -1, 11, True, 2.0, "3"])
def test_h14_max_n_explicito_fuera_de_rango_falla_cerrado(tmp_path, max_n):
    ev = Evaluador(Almacen(tmp_path), None, None, config_pruebas(), None)
    with pytest.raises(ValueError):
        ev.lecciones_vigentes(AS_OF, max_n=max_n)


def test_h14_max_n_explicito_valido_se_respeta(tmp_path):
    ev = Evaluador(Almacen(tmp_path), None, None, config_pruebas(), None)
    assert ev.lecciones_vigentes(AS_OF, max_n=1) == [] and ev.lecciones_vigentes(AS_OF, max_n=LECCIONES_POR_ENCARGO_MAX) == []

