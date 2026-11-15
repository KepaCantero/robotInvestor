"""T-123 r02 · Hallazgos de la QA r01: huellas y UUID no son tarjetas (H-02), el dato se ve con lo que lo acompaña (H-01)
e importes con espacio de miles y listas de números no se marcan (H-04)."""
import hashlib
import random
import uuid

import pytest
from bloque_a.contratos import ibanes_en_texto, secretos_en_texto, tarjetas_en_texto

VISA = "4111" + "1111" + "1111" + "1111"            # número de prueba publicado, partido
AMEX = "3782" + "822463" + "10005"
IBAN_DE = "DE89" + "370400440532013000"
IBAN_IT = "IT60" + "X0542811101000000123456"


def _grupos(s, n=4, sep=" "):
    return sep.join(s[i:i + n] for i in range(0, len(s), n))


# ---------------------------------------------------------------- H-02 · huellas y UUID
def test_h02_huellas_sha256_no_son_tarjetas():
    for i in range(20000):
        h = hashlib.sha256(str(i).encode()).hexdigest()
        assert tarjetas_en_texto(h) == [] and tarjetas_en_texto(h.upper()) == [], h


def test_h02_la_huella_del_revisor_no_se_marca():
    # una huella que antes daba «tarjeta …3400»: el tramo de cifras va entre letras
    h = "5d8f6cce" + "a" + VISA[:15] + "4" + "b" + "d5518a86"
    assert tarjetas_en_texto(h) == []
    assert secretos_en_texto(f"comentario: ver huella {h}") == []


def test_h02_uuid_no_son_tarjetas():
    r = random.Random(7)
    for _ in range(3000):
        u = str(uuid.UUID(int=r.getrandbits(128)))
        assert tarjetas_en_texto(u) == [], u


def test_h02_la_tarjeta_pegada_a_una_letra_no_se_marca_pero_suelta_si():
    assert tarjetas_en_texto("x" + VISA) == [] and tarjetas_en_texto(VISA + "x") == []
    assert tarjetas_en_texto("tarjeta:" + VISA) == ["tarjeta …1111"]


# ---------------------------------------------------------------- H-01 · lo que acompaña al dato
@pytest.mark.parametrize("texto", [
    _grupos(VISA) + " 12/27", _grupos(VISA) + " 123", VISA + " 12/27", _grupos(VISA, sep="-") + " 123",
    "cvv 123 " + _grupos(VISA), "4222 2222 2222 2", "4222 2222 2222 2 05/28", "la " + _grupos(AMEX[:4]) + " " + AMEX[4:10] + " " + AMEX[10:] + " 1234",
])
def test_h01_tarjeta_con_caducidad_o_cvv(texto):
    assert tarjetas_en_texto(texto), texto


@pytest.mark.parametrize("texto", [
    "IBAN " + _grupos(IBAN_DE) + " 15 de noviembre", _grupos(IBAN_IT) + " 3 cuotas", IBAN_DE + " 2 recibos",
    "Ref AB12 " + _grupos(IBAN_DE), "ID QA42 " + IBAN_DE, _grupos(IBAN_DE, sep="   "), _grupos(IBAN_DE).lower(),
])
def test_h01_iban_con_cifra_o_codigo_al_lado(texto):
    assert ibanes_en_texto(texto), texto


def test_h01_lo_que_ya_no_es_un_iban_sigue_sin_marcarse():
    assert ibanes_en_texto(IBAN_DE + "1") == []                    # una cifra pegada: es otra serie
    assert ibanes_en_texto(_grupos(IBAN_DE, sep="    ")) == []     # cuatro separadores
    assert ibanes_en_texto(_grupos(IBAN_DE)[:-1]) == []            # una de menos


# ---------------------------------------------------------------- H-04 · importes y listas
def test_h04_importes_con_espacio_de_miles_y_listas_no_se_marcan():
    r = random.Random(3)
    for _ in range(3000):
        importe = f"{r.randint(10**14, 10**15 - 1):,} €".replace(",", " ")
        lista = " ".join(str(r.randint(1, 99)) for _ in range(11))
        assert tarjetas_en_texto(importe) == [] and tarjetas_en_texto(lista) == [], (importe, lista)
    assert tarjetas_en_texto("372 436 879 280 739 €") == []


def test_r02_decimales_siguen_sin_marcarse():
    assert tarjetas_en_texto("0." + VISA) == [] and tarjetas_en_texto(VISA + ",5") == []
