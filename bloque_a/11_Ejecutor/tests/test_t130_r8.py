"""T-130 · R8: hallazgos de la QA r02 de T-123 (H-05 a H-10)."""
import hashlib
import random

import pytest
from bloque_a.contratos import ibanes_en_texto, secretos_en_texto, tarjetas_en_texto
from tiempo_cpu import minimos_intercalados

VISA = "4111" + "1111" + "1111" + "1111"            # número de prueba publicado, partido
DE = "DE89" + "370400440532013000"
GB = "GB29" + "NWBK60161331926819"
MT = "MT84" + "MALT011000012345MTLCAST001S"


def _g(s, sep=" "):
    return sep.join(s[i:i + 4] for i in range(0, len(s), 4))


# ---------------------------------------------------------------- H-05 · tras una coma o un punto
@pytest.mark.parametrize("texto", ["cliente,Ana," + VISA + ",12/27", "Visa," + VISA, "pago." + VISA, "fin." + _g(VISA),
                                   "datos," + _g(VISA), "tarjeta;" + VISA])
def test_h05_tarjeta_tras_coma_o_punto(texto):
    assert tarjetas_en_texto(texto) == ["tarjeta …1111"]


def test_h05_pero_no_la_parte_decimal():
    assert tarjetas_en_texto("0." + VISA) == [] and tarjetas_en_texto("12," + VISA) == []


# ---------------------------------------------------------------- H-06 · ISIN, índices y huellas truncadas
def test_h06_isin_e_indices_seguidos_de_palabras_no_son_iban():
    r = random.Random(5)
    palabras = ["el", "la", "los", "con", "para", "por", "que", "y", "o", "sin", "su", "muy", "alza", "bono", "uno", "de"]
    for _ in range(20000):
        pais = r.choice(["LU", "IE", "DE", "FR", "ES", "IT", "NL", "AT", "BE", "GB", "SE"])
        isin = pais + "".join(r.choice("0123456789") for _ in range(10))
        frase = " ".join(r.choice(palabras) for _ in range(10))
        assert ibanes_en_texto(f"ISIN {isin} {frase}") == []
        assert ibanes_en_texto(f"El {pais}{r.randint(10, 600)} {frase}") == []


def test_h06_huellas_truncadas_no_son_iban_ni_tarjeta():
    solo_cifras_marcadas = 0
    for i in range(100000):
        h = hashlib.sha256(str(i).encode()).hexdigest()[:16]
        marcada = secretos_en_texto(f'"huella": "{h}"')
        if h.isdigit():           # 16 cifras con Luhn y prefijo de red: forma de tarjeta, límite declarado (INC-T123-01)
            solo_cifras_marcadas += bool(marcada)
        else:
            assert marcada == [], h
    assert solo_cifras_marcadas <= 3


def test_h06_los_iban_con_letras_de_su_pais_siguen_detectandose():
    assert ibanes_en_texto(_g(GB)) == [GB] and ibanes_en_texto(_g(MT)) == [MT]
    assert ibanes_en_texto("IT60" + "X054 2811 1010 0000 0123 456") == ["IT60X0542811101000000123456"]


def test_h06_un_iban_de_bban_numerico_con_letras_no_se_marca():
    # mismo control mod 97 que un IBAN alemán, pero con letras en el BBAN: Alemania solo usa cifras
    falsos = [c for c in (f"DE{d:02d}37040044ABCD013000" for d in range(100)) if ibanes_en_texto(c)]
    assert falsos == []


# ---------------------------------------------------------------- H-07 · tablas
def test_h07_filas_y_columnas_de_numeros_de_cuatro_cifras():
    r = random.Random(9)
    for _ in range(5000):
        nums = [str(r.randint(1000, 9999)) for _ in range(8)]
        assert tarjetas_en_texto("  ".join(nums)) == []
        assert tarjetas_en_texto("Volumen:\n" + "\n".join(nums)) == []


def test_h07_identificadores_con_guion_bajo():
    r = random.Random(4)
    for _ in range(5000):
        assert tarjetas_en_texto("id_" + "".join(r.choice("0123456789") for _ in range(16))) == []


# ---------------------------------------------------------------- H-08 · coste lineal
@pytest.mark.parametrize("unidad", ["DE12 ", "DE11 " + "1 " * 30, "4111 "])
def test_h08_coste_lineal(unidad):
    """T-199: tiempo de CPU, la mínima de varias medidas intercaladas de cada tamaño (`tiempo_cpu`)."""
    t_corto, t_largo = unidad * (50_000 // len(unidad)), unidad * (200_000 // len(unidad))
    corto, largo = minimos_intercalados(lambda: secretos_en_texto(t_corto), lambda: secretos_en_texto(t_largo))
    assert largo < 3.0 and largo < 10 * max(corto, 0.01)


# ---------------------------------------------------------------- H-09 · IBAN pegado a letras
def test_h09_iban_pegado_a_letras_al_final():
    assert ibanes_en_texto(DE + "EUR") == [DE] and ibanes_en_texto(_g(DE) + "EUR") == [DE]
    assert ibanes_en_texto(DE + "1") == []           # una cifra pegada es otra serie
