"""HT-04 · Generador de gráficos SVG (minigráficos, mosaico de aciertos, líneas de métricas).

Paleta accesible (azul/naranja, apta para daltonismo); todos los gráficos llevan texto alternativo.
"""
from __future__ import annotations

from html import escape
from typing import Dict, List, Optional, Sequence, Tuple


def _escala(valores: Sequence[float], alto: float, margen: float, vmin=None, vmax=None) -> Tuple[float, float]:
    lo = min(valores) if vmin is None else vmin
    hi = max(valores) if vmax is None else vmax
    if hi - lo < 1e-12:
        hi, lo = lo + 1.0, lo - 1.0
    return lo, hi


def puntos_polyline(valores: Sequence[float], ancho: float = 280, alto: float = 72, margen_inf: float = 14,
                    margen_sup: float = 6, n_puntos: int = 12, vmin=None, vmax=None) -> Tuple[str, Tuple[float, float]]:
    """Reduce la serie a `n_puntos` y devuelve los puntos del polyline y el último punto (x, y)."""
    vals = list(valores)
    if not vals:
        return "", (0.0, 0.0)
    if len(vals) > n_puntos:
        idx = [round(i * (len(vals) - 1) / (n_puntos - 1)) for i in range(n_puntos)]
        vals = [vals[i] for i in idx]
    lo, hi = _escala(vals, alto, margen_inf, vmin, vmax)
    util = alto - margen_inf - margen_sup
    paso = (ancho - 14) / max(len(vals) - 1, 1)
    pts = []
    for i, v in enumerate(vals):
        x = 2 + i * paso
        y = margen_sup + (hi - v) / (hi - lo) * util
        pts.append((round(x, 1), round(y, 1)))
    return " ".join(f"{x},{y}" for x, y in pts), pts[-1]


def y_de(valor: float, lo: float, hi: float, alto: float = 72, margen_inf: float = 14, margen_sup: float = 6) -> float:
    util = alto - margen_inf - margen_sup
    return round(margen_sup + (hi - valor) / (hi - lo) * util, 1)


def minigrafico_precio(valores: Sequence[float], zona: Optional[Tuple[float, float]], titulo_alt: str, pie: str,
                       id_svg: str) -> str:
    """Minigráfico de precio de 12 meses con zona de interés (clases CSS de la plantilla)."""
    vals = list(valores)
    lo = min(vals + ([zona[0]] if zona else []))
    hi = max(vals + ([zona[1]] if zona else []))
    if hi - lo < 1e-12:
        hi, lo = lo + 1, lo - 1
    pts, (xh, yh) = puntos_polyline(vals, vmin=lo, vmax=hi)
    zona_svg = ""
    if zona:
        y1, y2 = y_de(zona[1], lo, hi), y_de(zona[0], lo, hi)
        zona_svg = (f'<rect class="zona" x="0" y="{y1}" width="280" height="{round(max(y2 - y1, 2), 1)}"/>'
                    f'<line class="zona-borde" x1="0" y1="{y1}" x2="280" y2="{y1}"/>'
                    f'<line class="zona-borde" x1="0" y1="{y2}" x2="280" y2="{y2}"/>')
    return (f'<figure class="spark" style="margin:0"><svg viewBox="0 0 280 72" role="img" aria-labelledby="{id_svg}">'
            f'<title id="{id_svg}">{escape(titulo_alt)}</title>{zona_svg}'
            f'<polyline class="lin" points="{pts}"/><circle class="hoy" cx="{xh}" cy="{yh}" r="4.5"/>'
            f'<text x="2" y="70">hace 1 año</text><text x="243" y="70">hoy</text></svg>'
            f'<figcaption>{escape(pie)}</figcaption></figure>')


def mosaico_aciertos(aciertos: int, n: int, max_casillas: int = 30) -> str:
    """Mosaico de casillas (10 por fila): acertadas con class="ok"."""
    n_vis = min(n, max_casillas)
    ok_vis = round(aciertos * n_vis / n) if n else 0
    filas = max((n_vis + 9) // 10, 1)
    rects = []
    for i in range(n_vis):
        x, y = (i % 10) * 33, (i // 10) * 33
        cls = ' class="ok"' if i < ok_vis else ""
        rects.append(f'<rect{cls} x="{x}" y="{y}" width="28" height="28" rx="5"/>')
    alt = (f"De {n} ideas ya evaluadas, {aciertos} lo hicieron mejor que su referencia y {n - aciertos} peor."
           if n else "Todavía no hay ideas con el plazo terminado.")
    return (f'<svg viewBox="0 0 330 {filas * 33}" role="img" aria-labelledby="mos-t"><title id="mos-t">{escape(alt)}</title>'
            f'<g>{"".join(rects)}</g></svg>')


def grafico_lineas(series: Dict[str, List[float]], etiquetas_x: List[str], titulo: str, ancho: int = 640,
                   alto: int = 260) -> str:
    """Gráfico de líneas sencillo (para metricas y el informe técnico en HTML)."""
    colores = ["#1f6fb2", "#d9822b", "#5b8c3a", "#8a4fb0"]
    todos = [v for s in series.values() for v in s if v is not None]
    if not todos:
        return f'<svg viewBox="0 0 {ancho} {alto}" role="img"><title>{escape(titulo)}: sin datos</title></svg>'
    lo, hi = min(todos), max(todos)
    if hi - lo < 1e-12:
        hi, lo = lo + 1, lo - 1
    m = 30
    n = max(len(s) for s in series.values())
    def xy(i, v):
        return m + i * (ancho - 2 * m) / max(n - 1, 1), alto - m - (v - lo) / (hi - lo) * (alto - 2 * m)
    partes = [f'<svg viewBox="0 0 {ancho} {alto}" role="img"><title>{escape(titulo)}</title>']
    for k, (nombre, s) in enumerate(series.items()):
        pts = " ".join(f"{round(xy(i, v)[0], 1)},{round(xy(i, v)[1], 1)}" for i, v in enumerate(s) if v is not None)
        partes.append(f'<polyline fill="none" stroke="{colores[k % 4]}" stroke-width="2" points="{pts}"/>')
        partes.append(f'<text x="{m + 4}" y="{16 + 14 * k}" font-size="12" fill="{colores[k % 4]}">{escape(nombre)}</text>')
    if etiquetas_x:
        partes.append(f'<text x="{m}" y="{alto - 8}" font-size="11">{escape(etiquetas_x[0])}</text>')
        partes.append(f'<text x="{ancho - m - 70}" y="{alto - 8}" font-size="11">{escape(etiquetas_x[-1])}</text>')
    partes.append("</svg>")
    return "".join(partes)
