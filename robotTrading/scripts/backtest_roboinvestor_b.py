"""Simula una acción elegida por el Bloque B en una fecha concreta."""

import argparse
import json
from datetime import date
from pathlib import Path

from scripts.backtest_roboinvestor import filas, simular_compra, unica

# Ficha del universo RV: Siemens Energy, ISIN DE000ENER6Y0, XETR, EUR.
SIMBOLOS = {("RV", "RV-ENR", "Siemens Energy"): "ENR.DE"}


def simular_b(ranking, fecha, candidato, historicos, graficas=None):
    fila = unica(
        (r for r in filas(ranking) if r["fecha_asof"] == fecha and r["cand_id"] == candidato),
        "fila de candidato en la fecha solicitada",
    )
    if fila["en_top_n"] != "True":
        raise ValueError("El candidato no fue seleccionado en esa fecha.")
    simbolo = SIMBOLOS.get((fila["tipo_activo"], fila["simbolo"], fila["nombre"]))
    if simbolo is None:
        raise ValueError("El instrumento no tiene una equivalencia verificada en robotTrading.")
    # B entrega una puntuación, no una probabilidad. Confianza fija del piloto para dimensionar.
    resultado = simular_compra(
        historicos,
        simbolo,
        date.fromisoformat(fecha),
        date.fromisoformat(fila["fecha_fin_horizonte"]),
        candidato,
        fila["pet_id"] or f"ranking-{fecha}",
        100.0,
        float(fila["S"]), graficas=graficas, moneda="€",
    )
    return {
        "candidato": candidato,
        "activo": fila["nombre"],
        "fecha_seleccion": fecha,
        "simbolo_b": fila["simbolo"],
        "confianza_simulacion": 100.0,
        **resultado,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ranking", type=Path)
    parser.add_argument("fecha")
    parser.add_argument("candidato")
    parser.add_argument("--historicos", type=Path, default=Path("data/historical"))
    parser.add_argument("--graficas", type=Path, default=Path("resultados/graficas"))
    args = parser.parse_args()
    try:
        print(
            json.dumps(
                simular_b(args.ranking, args.fecha, args.candidato, args.historicos, args.graficas),
                indent=2,
                default=str,
                ensure_ascii=False,
            )
        )
    except (OSError, KeyError, ValueError) as exc:
        parser.exit(1, f"Error de simulación: {exc}\n")
