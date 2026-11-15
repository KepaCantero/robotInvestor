"""QA r02 de T-94 · Simulación nula propia, distinta de la de r01: oportunidades DISTINTAS con ventanas solapadas entre fechas.

La regla de la ronda r02 cuenta una vez la apuesta repetida (mismo activo, clase y dirección) y remuestrea fechas de corte
enteras. Esta simulación no repite nunca la misma apuesta mientras está abierta: cada semana elige otro activo. Si las
elecciones de fechas distintas comparten un factor (un «tema»: activos del mismo subsector), sus excesos sobre ventanas
solapadas están correlados entre fechas, y el remuestreo por fechas los trata como independientes.

Mundo nulo (sin ninguna habilidad, sin deriva): una clase de 24 activos en 4 subsectores de 6; rentabilidad semanal
logarítmica = factor del subsector + ruido propio, ambos de media cero. 104 fechas de corte semanales, horizonte de 26
semanas (ventanas solapadas 25 de 26 semanas entre fechas consecutivas). Escenarios:
  I) control: el titular elige cada semana un activo al azar de la clase que no tenga ya una apuesta abierta (sin tema);
  T) tema: el titular elige al empezar un subsector al azar y cada semana un activo de ese subsector sin apuesta abierta
     (si todos están abiertos, repite uno, que el banco marca como repetido);
  P) pares: clases de 2 activos; el titular alterna LARGO del primero y CORTO del segundo, que con una cesta de dos es la
     MISMA apuesta (exceso idéntico) aunque la clave (activo, clase, dirección) sea distinta.
Contra la referencia del banco `azar` (y `momento` con 13 semanas en I y T). Con un rango del 90 % honesto, sin habilidad,
«mejor» o «peor» debería salir ~10 % de las veces.

Uso: .venv/bin/python -B .docs/tickets/T-94/revisores/r02_02_nula_solapada.py [<carpeta de banco_medida.py>] [n_sim] [sd_factor] [escenarios]
(por defecto 200 simulaciones, factor semanal 0,02 frente a 0,03 de ruido propio, escenarios ITP)
Imprime la tasa de veredictos firmes por escenario y comparación; sale con 1 si alguna supera el 16 %."""
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
CARPETA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3] / "scripts"
NSIM = int(sys.argv[2]) if len(sys.argv) > 2 else 200
SD_FACTOR = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02     # desviación semanal del factor del subsector
ESCENARIOS = sys.argv[4] if len(sys.argv) > 4 else "ITP"
sys.path.insert(0, str(CARPETA))
import banco_medida as bm

SEMANAS = pd.date_range("2023-01-06", periods=260, freq="7D")        # viernes, cinco años de historia
CORTES = list(SEMANAS[60:164])                                        # 104 cortes; las ventanas de 26 semanas caben
H = 26
FIN = lambda ini, h: pd.Timestamp(ini) + pd.Timedelta(weeks=H)        # noqa: E731
CONSUMO = {"llamadas": 0, "tokens_entrada": 0, "tokens_salida": 0, "coste_estimado": None}
SUB = {f"S{i:02d}": i // 6 for i in range(24)}


def precios_factor(rng, sd_propio=0.03):
    sd_factor = SD_FACTOR
    f = rng.normal(0, sd_factor, size=(4, len(SEMANAS)))
    return {s: pd.Series(100 * np.exp(np.cumsum(f[g] + rng.normal(0, sd_propio, len(SEMANAS)))), index=SEMANAS)
            for s, g in SUB.items()}


def plantilla_sin_repetir(candidatos_por_fecha, r):
    abiertas: dict[str, pd.Timestamp] = {}
    out = []
    for c, cands in zip(CORTES, candidatos_por_fecha):
        libres = [s for s in cands if abiertas.get(s, c) <= c]
        s = r.choice(libres) if libres else r.choice(cands)
        if libres:
            abiertas[s] = FIN(c, "H")
        out.append({"fecha_asof": c.strftime("%Y-%m-%d"), "clase": "C", "simbolo": s, "direccion": "LARGO", "horizonte": "H"})
    return out


def informe(pl, precios, universo, seed, con_momento=True):
    cont = {"titular": bm.evaluar(pl, precios, universo, FIN),
            "azar": bm.evaluar(bm.azar(pl, universo, seed), precios, universo, FIN)}
    if con_momento:
        cont["momento"] = bm.evaluar(bm.momento(pl, universo, precios, 13), precios, universo, FIN)
    return bm.construir_informe(cont, CONSUMO, 500, seed, None, "h")


def escenario(nombre, seed):
    rng, r = np.random.default_rng(seed), random.Random(seed)
    if nombre in ("I", "T"):
        precios = precios_factor(rng)
        universo = pd.DataFrame({"simbolo": list(SUB), "clase": ["C"] * len(SUB)})
        if nombre == "I":
            cands = [list(SUB)] * len(CORTES)
        else:
            tema = r.randrange(4)
            cands = [[s for s, g in SUB.items() if g == tema]] * len(CORTES)
        return informe(plantilla_sin_repetir(cands, r), precios, universo, seed)
    # P: 6 clases de 2 activos independientes; LARGO del primero y CORTO del segundo, alternos
    sims = {f"P{k}{x}": f"K{k}" for k in range(6) for x in "ab"}
    precios = {s: pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.03, len(SEMANAS)))), index=SEMANAS) for s in sims}
    universo = pd.DataFrame({"simbolo": list(sims), "clase": list(sims.values())})
    pl = []
    for i, c in enumerate(CORTES):
        for k in range(6):
            if i < 2 * k:   # cada clase empieza dos semanas después que la anterior: fechas efectivas distintas
                continue
            largo = (i - 2 * k) % 2 == 0
            pl.append({"fecha_asof": c.strftime("%Y-%m-%d"), "clase": f"K{k}", "simbolo": f"P{k}{'a' if largo else 'b'}",
                       "direccion": "LARGO" if largo else "CORTO", "horizonte": "H"})
    return informe(pl, precios, universo, seed, con_momento=False)


def main():
    peor = 0.0
    for nombre in ESCENARIOS:
        firmes: dict[str, int] = {}
        efectivas = []
        for k in range(NSIM):
            inf = escenario(nombre, 70_000 + k)
            efectivas.append(inf["contendientes"]["titular"]["efectivas"])
            for comp, c in inf["comparaciones"].items():
                firmes[comp] = firmes.get(comp, 0) + (c["veredicto"] in ("mejor", "peor"))
        for comp, n in firmes.items():
            tasa = n / NSIM
            peor = max(peor, tasa)
            print(f"{'OK   ' if tasa <= 0.16 else 'FALLO'} escenario {nombre}, {comp}: {tasa:.1%} de veredictos firmes sin habilidad "
                  f"(nominal 10 %); fechas efectivas del titular: mediana {int(np.median(efectivas))}", flush=True)
    sys.exit(1 if peor > 0.16 else 0)


if __name__ == "__main__":
    main()
