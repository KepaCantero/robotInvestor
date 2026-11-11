import { useEffect, useRef } from "react";
import { ColorType, createChart, LineStyle, type IChartApi } from "lightweight-charts";
import type { PuntoSerie } from "@/api/tipos";
import { color, useTema } from "./tema";

export interface Linea {
  precio: number;
  titulo: string;
  token: "oro" | "mal" | "bien" | "tenue" | "aviso";
  discontinua?: boolean;
}

function opcionesBase() {
  return {
    autoSize: true,
    layout: {
      background: { type: ColorType.Solid, color: color("panel") },
      textColor: color("tenue"),
      fontFamily: "'JetBrains Mono', ui-monospace, monospace",
      fontSize: 11,
    },
    grid: { vertLines: { color: color("rejilla") }, horzLines: { color: color("rejilla") } },
    rightPriceScale: { borderColor: color("linea") },
    timeScale: { borderColor: color("linea") },
    crosshair: { vertLine: { color: color("tenue", 0.5) }, horzLine: { color: color("tenue", 0.5) } },
    localization: {
      locale: "es-ES",
      priceFormatter: (p: number) => p.toLocaleString("es-ES", { maximumFractionDigits: p < 5 ? 4 : 2 }),
    },
  };
}

/** Precio de una posición con su entrada, su stop y el rango esperado de H. */
export function GraficoPrecio({ serie, lineas, alto = 260 }: { serie: PuntoSerie[]; lineas: Linea[]; alto?: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const tema = useTema();
  useEffect(() => {
    if (!ref.current) return;
    const chart: IChartApi = createChart(ref.current, opcionesBase());
    const area = chart.addAreaSeries({
      lineColor: color("oro"),
      topColor: color("oro", 0.28),
      bottomColor: color("oro", 0.02),
      lineWidth: 2,
      priceLineVisible: false,
    });
    area.setData(serie.map((p) => ({ time: p.fecha, value: p.valor })));
    for (const l of lineas)
      area.createPriceLine({
        price: l.precio,
        color: color(l.token),
        lineWidth: 1,
        lineStyle: l.discontinua ? LineStyle.Dashed : LineStyle.Solid,
        axisLabelVisible: true,
        title: l.titulo,
      });
    chart.timeScale().fitContent();
    return () => chart.remove();
  }, [serie, lineas, tema]);
  return <div ref={ref} style={{ height: alto }} className="w-full" data-testid="grafico-precio" />;
}

/** El robot frente a la cartera sombra. */
export function GraficoComparado({ robot, sombra, alto = 240 }: { robot: PuntoSerie[]; sombra: PuntoSerie[]; alto?: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const tema = useTema();
  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, opcionesBase());
    const s = chart.addLineSeries({ color: color("tenue"), lineWidth: 2, lineStyle: LineStyle.Dashed, title: "Sombra", priceLineVisible: false });
    s.setData(sombra.map((p) => ({ time: p.fecha, value: p.valor })));
    const r = chart.addLineSeries({ color: color("oro"), lineWidth: 2, title: "Robot", priceLineVisible: false });
    r.setData(robot.map((p) => ({ time: p.fecha, value: p.valor })));
    chart.timeScale().fitContent();
    return () => chart.remove();
  }, [robot, sombra, tema]);
  return <div ref={ref} style={{ height: alto }} className="w-full" data-testid="grafico-comparado" />;
}
