"""T-123 · R8: IBAN de otros países y números de tarjeta, validados con su dígito de control (hueco menor de la deuda)."""
import random

import pytest
from bloque_a.contratos import (
    LONGITUD_IBAN,
    DatosSensibles,
    _iban_valido,
    _luhn,
    contiene_credenciales,
    ibanes_en_texto,
    secretos_en_texto,
    tarjetas_en_texto,
)
from conftest import AS_OF, nuevo_bloque
from tiempo_cpu import cpu

# IBAN y tarjetas de ejemplo publicados por los bancos y las redes para pruebas (ninguno es una cuenta real)
IBAN = {"DE": "DE89" + "370400440532013000", "GB": "GB82" + "WEST12345698765432", "FR": "FR14" + "20041010050500013M02606",
        "IT": "IT60" + "X0542811101000000123456", "NL": "NL91" + "ABNA0417164300", "BE": "BE68" + "539007547034",
        "PT": "PT50" + "000201231234567890154", "CH": "CH93" + "00762011623852957"}
TARJETAS = {"visa": "4111" + "111111111111", "mastercard": "5500" + "000000000004", "amex": "3782" + "82246310005",
            "mastercard_2": "2223" + "000048400011", "discover": "6011" + "111111111117"}


def _agrupado(s, n=4, sep=" "):
    return sep.join(s[i:i + n] for i in range(0, len(s), n))


@pytest.mark.parametrize("pais", sorted(IBAN))
@pytest.mark.parametrize("forma", ["junto", "espacios", "espacio duro", "guiones"])
def test_el_iban_de_otro_pais_se_detecta(pais, forma):
    iban = IBAN[pais]
    texto = {"junto": iban, "espacios": _agrupado(iban), "espacio duro": _agrupado(iban, sep=" "),
             "guiones": _agrupado(iban, sep="-")}[forma]
    assert ibanes_en_texto(f"cobren en {texto}, gracias") == [iban]
    assert ibanes_en_texto(f"{texto} EUR") == [iban] and ibanes_en_texto(f"{texto}7") == []
    assert contiene_credenciales({"comentario": f"cuenta {texto}"})


@pytest.mark.parametrize("pais", sorted(IBAN))
def test_un_iban_con_el_control_mal_no_se_marca(pais):
    iban = IBAN[pais]
    roto = iban[:-1] + ("0" if iban[-1] != "0" else "1")
    assert not _iban_valido(roto) and ibanes_en_texto(roto) == []


@pytest.mark.parametrize("nombre", sorted(TARJETAS))
@pytest.mark.parametrize("sep", ["", " ", "-"])
def test_la_tarjeta_se_detecta_y_se_devuelve_enmascarada(nombre, sep):
    num = TARJETAS[nombre]
    texto = _agrupado(num, sep=sep) if sep else num
    hallados = tarjetas_en_texto(f"pago con {texto} ayer")
    assert hallados == ["tarjeta …" + num[-4:]] and num not in str(hallados)
    assert contiene_credenciales({"nota": texto})


@pytest.mark.parametrize("texto", [
    "1234 5678 9012 3456", "4111 1111 1111 1112", "El 2024, 2025, 2026 y 2027 fueron buenos.", "Pedido 2024202520262027.",
    "ISIN ES0113900J37 y US0378331005", "Teléfono +34 912 345 678", "Serie 0000 0000 0000 0000", "CUSIP 037833100",
    "DE89 3704 0044 0532 0130 01", "XX89370400440532013000", "La rentabilidad fue del 4,1 % en 1111 sesiones.",
    '"mdd": 0.4903529406787125, "drawdown_actual": 0.4228715933084759', '"pct": 0.6507936507936508',   # decimales del ciclo
    "1,4111111111111111", "-0.4111111111111111",   # T-130: «4111111111111111.5» sí se marca (INC-T123-01)
])
def test_lo_que_no_es_una_cuenta_ni_una_tarjeta_no_se_marca(texto):
    assert ibanes_en_texto(texto) == [] and tarjetas_en_texto(texto) == []


def test_pocos_falsos_positivos_en_series_de_cifras_al_azar():
    rng = random.Random(123)
    positivos = 0
    for _ in range(20000):
        n = rng.choice([13, 15, 16, 19])
        cifras = str(rng.choice([1, 7, 8, 9])) + "".join(str(rng.randint(0, 9)) for _ in range(n - 1))
        positivos += bool(tarjetas_en_texto(cifras))
    assert positivos == 0                                   # sin el prefijo de una red, nunca
    con_red = sum(bool(tarjetas_en_texto("4" + "".join(str(rng.randint(0, 9)) for _ in range(15)))) for _ in range(20000))
    assert 1500 < con_red < 2500                            # con prefijo Visa, solo las que pasan Luhn (≈ 1 de 10)


def test_el_coste_es_lineal(tmp_path):
    texto = ("Cifras 1234 5678 9012 y DE89 algo más. " * 40000)
    assert cpu(lambda: secretos_en_texto(texto)) < 10   # T-199: tiempo de CPU, no de reloj


def test_luhn_y_longitudes():
    assert _luhn("79927398713") and not _luhn("79927398710")
    assert LONGITUD_IBAN["ES"] == 24 and LONGITUD_IBAN["DE"] == 22 and len(LONGITUD_IBAN) >= 40


def test_un_ct04_con_una_tarjeta_o_un_iban_extranjero_se_rechaza_y_no_queda_en_ningun_archivo(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    for dato in (_agrupado(TARJETAS["visa"]), _agrupado(IBAN["DE"])):
        with pytest.raises(DatosSensibles):
            b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": f"cobren en {dato}"}}, AS_OF)
    for p in tmp_path.rglob("*"):
        if p.is_file():
            cuerpo = p.read_text(encoding="utf-8", errors="ignore")
            assert TARJETAS["visa"][4:12] not in cuerpo.replace(" ", "") and IBAN["DE"][4:] not in cuerpo.replace(" ", ""), p
