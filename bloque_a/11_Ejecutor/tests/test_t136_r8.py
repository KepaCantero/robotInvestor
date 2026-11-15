"""T-136 · R8: hallazgos de la QA r01 de T-130. Estructura del BBAN de cada país (H-01 y H-03), filas de tabla de números
de cuatro cifras (H-02), decimales tras un ISIN (H-05) y misma caja en el IBAN."""
import random
import re

import pytest
from bloque_a.contratos import (
    BBAN_NUMERICO,
    ESTRUCTURA_BBAN,
    LONGITUD_IBAN,
    _iban_valido,
    ibanes_en_texto,
    tarjetas_en_texto,
)


def _iban(pais, bban):
    num = "".join(str(int(c, 36)) for c in bban + pais + "00")
    return f"{pais}{98 - int(num) % 97:02d}{bban}"


def _g(s, sep=" "):
    return sep.join(s[i:i + 4] for i in range(0, len(s), 4))


def _bban_de(estructura, r):
    trozos = {"n": "0123456789", "a": "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "c": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    return "".join("".join(r.choice(trozos[k]) for _ in range(int(n))) for n, k in re.findall(r"(\d+)([nac])", estructura))


def test_h01_las_estructuras_cuadran_con_la_longitud_de_cada_pais():
    assert set(ESTRUCTURA_BBAN) == set(LONGITUD_IBAN)
    for p, e in ESTRUCTURA_BBAN.items():
        assert 4 + sum(int(n) for n in re.findall(r"(\d+)[nac]", e)) == LONGITUD_IBAN[p], p


def test_h01_un_iban_con_la_estructura_de_su_pais_se_detecta_en_los_42():
    r = random.Random(13)
    for p, e in ESTRUCTURA_BBAN.items():
        for _ in range(20):
            iban = _iban(p, _bban_de(e, r))
            assert _iban_valido(iban)
            assert ibanes_en_texto(f"cuenta {_g(iban)} gracias") == [iban], iban
            assert ibanes_en_texto(iban) == [iban], iban


@pytest.mark.parametrize("iban", ["RO49" + "AAAA1B31007593840000", "LV80" + "BANK0000435195001", "GB29" + "NWBK60161331926819",
                                  "MT84" + "MALT011000012345MTLCAST001S", "IT60" + "X0542811101000000123456"])
def test_h01_ejemplos_del_registro_con_letras(iban):
    assert ibanes_en_texto(_g(iban)) == [iban] and ibanes_en_texto(_g(iban).lower()) == [iban]


def test_h01_letras_donde_el_pais_pide_cifras_no_es_un_iban():
    r = random.Random(2)
    for p in sorted(BBAN_NUMERICO):
        bban = list(_bban_de(ESTRUCTURA_BBAN[p], r))
        bban[len(bban) // 2] = "X"
        assert ibanes_en_texto(_iban(p, "".join(bban))) == [], p


def test_h03_bban_numerico_tiene_los_21_paises_con_va():
    assert len(BBAN_NUMERICO) == 21 and "VA" in BBAN_NUMERICO


def test_h02_filas_de_numeros_de_cuatro_cifras():
    r = random.Random(8)
    # T-140 (QA r01 de T-136, H-02): una fila de 8 se marca solo si son dos tarjetas válidas seguidas (en torno al 0,6 % con
    # números de 4000 a 5999, que casi siempre tienen prefijo de red); antes se exigía 0 y eso dejaba sin detectar dos
    # tarjetas seguidas o una tarjeta con su caducidad MMAA
    marcadas = sum(bool(tarjetas_en_texto(" ".join(str(r.randint(4000, 5999)) for _ in range(8)))) for _ in range(5000))
    assert marcadas <= 50
    assert tarjetas_en_texto(_g("4111" + "1111" + "1111" + "1111")) == ["tarjeta …1111"]   # cuatro grupos sí


def test_h05_isin_seguido_de_decimales_con_punto():
    r = random.Random(6)
    for _ in range(20000):
        pais = r.choice(["DE", "FR", "IT", "LU", "IE", "NL", "BE", "AT", "ES"])
        isin = pais + "".join(r.choice("0123456789") for _ in range(10))
        texto = f"ISIN {isin} " + " ".join(f"{r.randint(1, 99)}.{r.randint(0, 9)}" for _ in range(6))
        assert ibanes_en_texto(texto) == [], texto


def test_misma_caja_palabras_tras_un_isin():
    r = random.Random(3)
    palabras = ["la", "de", "por", "con", "que", "y", "o", "sin", "muy", "bono", "alza", "para"]
    marcados = 0
    for _ in range(20000):
        isin = r.choice(["LU", "IE", "FR", "IT", "CY", "GR"]) + "".join(r.choice("0123456789") for _ in range(10))
        marcados += bool(ibanes_en_texto(f"ISIN {isin} " + " ".join(r.choice(palabras) for _ in range(10))))
    assert marcados == 0
