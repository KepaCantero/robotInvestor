"""La señal del viernes se ejecuta el lunes aunque siga vigente."""

from datetime import date
from decimal import Decimal
from pathlib import Path

from scripts.backtest_roboinvestor import simular


def test_una_entrada_en_la_apertura_siguiente(tmp_path):
    (tmp_path / "senales.csv").write_text(
        "opp_id,vigente_nueva,proxy_backtest,direccion,run_id,fecha_asof,prob_interna,RK\n"
        "op,NUEVA,XLU,LARGO,run,2026-07-31,0.65,74\n"
        "op,VIGENTE,XLU,LARGO,otro,2026-08-07,0.65,74\n"
    )
    (tmp_path / "pronosticos.csv").write_text(
        "opp_id,run_id,fecha_emision,simbolo,horizonte,fecha_resolucion\n"
        "op,run,2026-07-31,XLU,H2,2026-08-28\n"
    )
    historicos = Path(__file__).resolve().parents[2] / "data/historical"
    r = simular(tmp_path, "op", "H2", historicos)
    assert (r["entrada"], r["salida"]) == (date(2026, 8, 3), date(2026, 8, 28))
    assert r["apertura_historica"] == Decimal("43.917082")
    assert r["cierre_final"] == Decimal("42.418102")
    assert r["capital_final"] < r["capital_inicial"]
