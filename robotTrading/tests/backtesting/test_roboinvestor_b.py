from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from scripts.backtest_roboinvestor_b import simular_b


def test_seleccion_fechada_sin_resultados_futuros(tmp_path):
    ranking = tmp_path / "rankings.csv"
    ranking.write_text(
        "fecha_asof,cand_id,tipo_activo,simbolo,nombre,S,en_top_n,fecha_fin_horizonte,pet_id\n"
        "2023-12-29,RV:ENR,RV,RV-ENR,Siemens Energy,52,False,2024-12-17,\n"
        "2024-01-31,RV:ENR,RV,RV-ENR,Siemens Energy,55,True,2025-01-17,\n"
    )
    precios = Path(__file__).resolve().parents[2] / "data/historical"
    with pytest.raises(ValueError, match="no fue seleccionado"):
        simular_b(ranking, "2023-12-29", "RV:ENR", precios)
    r = simular_b(ranking, "2024-01-31", "RV:ENR", precios)
    assert (r["simbolo"], r["entrada"], r["salida"]) == (
        "ENR.DE",
        date(2024, 2, 1),
        date(2025, 1, 17),
    )
    assert (r["apertura_historica"], r["cierre_final"]) == (Decimal("13.85"), Decimal("50.34"))
