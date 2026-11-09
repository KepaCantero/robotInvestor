import pytest
from bloque_b.comparacion_azar import comparar_azar, universo_azar


def test_grupos_admisibles_empates_y_cobertura():
    a, b, c, d, e = ({"cand_id": k} for k in "ABCDE")
    a["indice_replicado"] = c["indice_replicado"] = "indice"
    b["subcluster"] = d["subcluster"] = "redes"
    sel = {"top_n": [a, b], "alternativas": [c], "resto_secundarios": [d, e], "top_n_previsto": 2}
    universo = universo_azar(sel, {"C|D": 1})
    filas = [{"cand_id": k, "rent_fwd": v, "en_top_n": k in "AB"} for k, v in zip("ABCDE", [4, 2, 1, 0, 2])]
    # Se descartan AC (índice), BD (subclúster), CD (correlación).
    r = comparar_azar(universo, filas, "RV", 100, "prueba")
    assert (r["azar_metodo"], r["azar_grupos_examinados"], r["azar_grupos_validos"]) == ("exacto", 10, 7)
    assert r["azar_pct_superado"] == pytest.approx(100 * 5 / 7)
    assert r["azar_pct_empate"] == pytest.approx(100 * 2 / 7)
    sorteado = comparar_azar(universo, filas, "RV", 9, "prueba")
    assert sorteado["azar_metodo"] == "muestreo" and sorteado["azar_grupos_examinados"] == 9
    assert sorteado == comparar_azar(universo, filas[::-1], "RV", 9, "prueba")
    filas[-1]["rent_fwd"] = None
    r = comparar_azar(universo, filas, "RV", 100, "prueba")
    assert r["azar_estado"] == "universo_incompleto" and r["azar_pct_superado"] is None


def test_limite_emisor_rf():
    c = [{"cand_id": k, "emisor": "X" if k != "D" else "Y"} for k in "ABCD"]
    u = universo_azar({"top_n": [c[0], c[1], c[3]], "alternativas": [c[2]], "resto_secundarios": [], "top_n_previsto": 3})
    filas = [{"cand_id": k, "en_top_n": k != "C", "rent_fwd": 0} for k in "ABCD"]
    r = comparar_azar(u, filas, "RF", 100, "prueba")
    assert r["azar_grupos_validos"] == 3 and r["azar_pct_empate"] == 100
