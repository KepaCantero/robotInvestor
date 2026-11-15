"""Ejecuta un backtest de RoboInvestor con el motor incluido de robotTrading."""

import argparse
from pathlib import Path
import os
import subprocess
import sys


RAIZ = Path(__file__).resolve().parent
MOTOR = RAIZ / "robotTrading"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    grupos = parser.add_subparsers(dest="bloque", required=True)
    a = grupos.add_parser("a", help="Simular una oportunidad NUEVA/LARGO")
    a.add_argument("--salida", type=Path, default=RAIZ / "bloque_a/11_Ejecutor/ejemplos/salida_backtest_simulado")
    a.add_argument("--oportunidad", default="OPP-2026-0002")
    a.add_argument("--horizonte", default="H2")
    b = grupos.add_parser("b", help="Simular una selección del ranking")
    b.add_argument("--ranking", type=Path, default=RAIZ / "bloque_b/11_Ejecutor/ejemplos/backtest_simulado/solo_seleccion/rankings.csv")
    b.add_argument("--fecha", default="2024-01-31")
    b.add_argument("--candidato", default="RV:ENR")
    for grupo in (a, b):
        grupo.add_argument("--historicos", type=Path, default=MOTOR / "data/historical")
        grupo.add_argument("--graficas", type=Path, default=MOTOR / "resultados/graficas")

    args = parser.parse_args()
    if args.bloque == "a":
        modulo = "scripts.backtest_roboinvestor"
        entrada = [str(args.salida.resolve()), args.oportunidad, args.horizonte]
    else:
        modulo = "scripts.backtest_roboinvestor_b"
        entrada = [str(args.ranking.resolve()), args.fecha, args.candidato]
    comando = [sys.executable, "-m", modulo, *entrada, "--historicos",
               str(args.historicos.resolve()), "--graficas", str(args.graficas.resolve())]
    entorno = os.environ.copy()
    entorno.setdefault("NUMBA_ENFORCE", "0")
    return subprocess.run(comando, cwd=MOTOR, env=entorno).returncode


if __name__ == "__main__":
    sys.exit(main())
