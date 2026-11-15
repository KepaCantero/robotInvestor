"""Simula una oportunidad NUEVA/LARGO del Bloque A con precios diarios locales.

Desde robotTrading: python -m scripts.backtest_roboinvestor CARPETA_SALIDA OPP-ID H2
La carpeta debe contener senales.csv y pronosticos.csv. Se aplican los costes simulados por robotTrading.
"""

import argparse
import csv
import json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from app.backtesting.engine import BacktestEngine
from app.backtesting.models import BacktestConfig
from app.domain.models.market_data import Quote
from app.domain.models.signal import Signal, SignalSource, SignalStrength, SignalType


def filas(archivo):
    with archivo.open(encoding="utf-8-sig", newline="") as entrada:
        yield from csv.DictReader(entrada)


def unica(filas_elegidas, descripcion):
    filas_elegidas = list(filas_elegidas)
    if len(filas_elegidas) != 1:
        raise ValueError(f"Se esperaba una {descripcion}, se encontraron {len(filas_elegidas)}.")
    return filas_elegidas[0]


def simular(carpeta, oportunidad, horizonte, historicos, graficas=None):
    idea = unica(
        (
            r
            for r in filas(carpeta / "senales.csv")
            if r["opp_id"] == oportunidad and r["vigente_nueva"] == "NUEVA"
        ),
        "señal NUEVA",
    )
    simbolo = idea["proxy_backtest"]
    if idea["direccion"] != "LARGO" or not simbolo or Path(simbolo).name != simbolo:
        raise ValueError("Esta prueba requiere una señal LARGO con un símbolo de histórico local.")
    pronostico = unica(
        (
            r
            for r in filas(carpeta / "pronosticos.csv")
            if r["run_id"] == idea["run_id"]
            and r["opp_id"] == oportunidad
            and r["fecha_emision"] == idea["fecha_asof"]
            and r["simbolo"] == simbolo
            and r["horizonte"] == horizonte
        ),
        "previsión para ese horizonte",
    )
    inicio = date.fromisoformat(idea["fecha_asof"])
    fin = date.fromisoformat(pronostico["fecha_resolucion"])
    resultado = simular_compra(
        historicos,
        simbolo,
        inicio,
        fin,
        oportunidad,
        idea["run_id"],
        float(idea["prob_interna"]) * 100,
        float(idea["RK"]), graficas=graficas,
    )
    return {
        "oportunidad": oportunidad,
        "run_id": idea["run_id"],
        "horizonte": horizonte,
        **resultado,
    }


def simular_compra(
    historicos, simbolo, inicio, fin, identificador, ejecucion, confianza, prioridad, graficas=None, moneda="unid."
):
    """Compra en la siguiente apertura y cierre de la posición al final del periodo."""
    barras = []
    for r in filas(historicos / f"{simbolo}.csv"):
        dia = date.fromisoformat(r["date"])
        if inicio <= dia <= fin:
            cierre = Decimal(r["Close"])
            barras.append(
                Quote(
                    symbol=simbolo,
                    timestamp=datetime.combine(dia, datetime.min.time()),
                    open=Decimal(r["Open"]),
                    high=Decimal(r["High"]),
                    low=Decimal(r["Low"]),
                    close=cierre,
                    last=cierre,
                    bid=cierre,
                    ask=cierre,
                    volume=Decimal(r["Volume"]),
                )
            )
    barras.sort(key=lambda b: b.timestamp)
    if (
        len(barras) < 2
        or barras[0].timestamp.date() != inicio
        or barras[-1].timestamp.date() != fin
        or len({b.timestamp for b in barras}) != len(barras)
    ):
        raise ValueError(
            "Se requieren sesiones únicas, con cotización en la emisión y el vencimiento."
        )
    primera = barras[0]
    # La probabilidad describe el pronóstico. El dimensionamiento usa las reglas del motor.
    senal = Signal(
        signal_id=identificador,
        symbol=simbolo,
        signal_type=SignalType.BUY,
        strength=SignalStrength.MODERATE,
        confidence=confianza,
        liquidity_score=50.0,
        priority_score=prioridad,
        source=SignalSource.FUNDAMENTAL,
        price=primera.close,
        volume=Decimal(0),
        timestamp=primera.timestamp,
        metadata={"strategy": "roboinvestor", "run_id": ejecucion},
    )
    config = BacktestConfig(strategy_name="roboinvestor", next_day_execution=True)
    resultado = BacktestEngine(config, strategy_name="roboinvestor").run_backtest(barras, [senal])
    compra = unica((t for t in resultado.trades if t.side == "buy"), "compra")
    operacion = unica((t for t in resultado.trades if t.side == "sell"), "venta")
    if operacion.entry_time != barras[1].timestamp or operacion.exit_time != barras[-1].timestamp:
        raise ValueError("Las fechas ejecutadas difieren de las sesiones previstas.")
    if abs(resultado.final_capital - config.initial_capital - operacion.pnl) > Decimal("0.01"):
        raise ValueError("El resultado de la operación no cuadra con el capital final.")
    grafica = {}
    if graficas is not None:
        from scripts.grafica_ganancias import curva_semanal, dibujar
        destino = graficas / f"{simbolo}_{inicio}_{fin}.png"
        grafica["grafica_semanal"] = dibujar({simbolo: curva_semanal(barras, compra, operacion)}, destino, moneda)
    return {
        **grafica,
        "simbolo": simbolo,
        "entrada": operacion.entry_time.date(),
        "salida": operacion.exit_time.date(),
        "precio_entrada": operacion.entry_price,
        "cierre_final": operacion.exit_price,
        "unidades": operacion.quantity,
        "capital_inicial": config.initial_capital,
        "capital_final": resultado.final_capital,
        "rentabilidad_cartera_pct": resultado.total_return,
        "apertura_historica": barras[1].open,
        "variacion_precio_sin_costes_pct": (barras[-1].close / barras[1].open - 1) * 100,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("carpeta", type=Path)
    parser.add_argument("oportunidad")
    parser.add_argument("horizonte")
    parser.add_argument("--historicos", type=Path, default=Path("data/historical"))
    parser.add_argument("--graficas", type=Path, default=Path("resultados/graficas"))
    args = parser.parse_args()
    try:
        print(
            json.dumps(
                simular(args.carpeta, args.oportunidad, args.horizonte, args.historicos, args.graficas),
                indent=2,
                default=str,
                ensure_ascii=False,
            )
        )
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Error de simulación: {exc}\n")
