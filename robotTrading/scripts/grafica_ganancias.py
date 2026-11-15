"""Ganancias semanales por posición para simulaciones de compra y mantenimiento."""
from pathlib import Path

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter


def curva_semanal(barras, compra, venta):
    semanas = {}
    for barra in barras:
        if barra.symbol == compra.symbol and compra.entry_time <= barra.timestamp <= venta.exit_time:
            dia = barra.timestamp.date()
            ganancia = compra.quantity * (barra.close - compra.entry_price) - compra.all_in_cost
            semanas[dia.isocalendar()[:2]] = (dia, float(venta.pnl if barra.timestamp == venta.exit_time else ganancia))
    return list(semanas.values())


def dibujar(curvas, destino, moneda):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    nombres = sorted(curvas, key=lambda n: max(abs(v) for _, v in curvas[n]), reverse=True)
    ampliar = len(nombres) >= 3 and max(abs(v) for _, v in curvas[nombres[0]]) > 3 * max(abs(v) for _, v in curvas[nombres[1]])
    fig = Figure(figsize=(10, 7 if ampliar else 4.8), layout="constrained")
    FigureCanvasAgg(fig)
    paneles = fig.subplots(2 if ampliar else 1, sharex=True, squeeze=False).ravel()
    colores = dict(zip(nombres, ["#12645b", "#2564ab", "#bc502b", "#795b91", "#8b690b"]))
    fig.suptitle("Ganancia acumulada por empresa", fontsize=21, weight="bold")
    for i, ax in enumerate(paneles):
        ax.set_title("Detalle de las posiciones de menor amplitud" if i else "Último cierre semanal y resultado de la venta · sin dividendos", loc="left", fontsize=11)
        for n in (nombres[1:] if i else nombres):
            dias, valores = zip(*curvas[n])
            saldo = f"{valores[-1]:+,.2f}".translate(str.maketrans(",.", ".,"))
            ax.plot(dias, valores, color=colores.get(n), lw=2, label=f"{n}   {saldo} {moneda}")
            ax.scatter(dias[-1], valores[-1], s=18, color=ax.lines[-1].get_color())
        ax.axhline(0, color="#738184", lw=.8)
        ax.grid(axis="y", alpha=.25)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_ylabel(f"Ganancia ({moneda})")
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}".replace(",", ".")))
        ax.legend(frameon=False)
    locator = AutoDateLocator(minticks=4, maxticks=8)
    paneles[-1].xaxis.set_major_locator(locator)
    paneles[-1].xaxis.set_major_formatter(ConciseDateFormatter(locator))
    fig.savefig(destino, dpi=165)
    return str(destino.resolve())
