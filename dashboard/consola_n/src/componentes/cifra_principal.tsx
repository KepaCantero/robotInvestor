import type { CifraPrincipal } from "@/api/tipos";
import { euros, eurosConSigno, fecha } from "@/logica/formato";
import { textoVeredicto, veredictoRango } from "@/logica/veredicto";
import { Badge } from "@/componentes/ui/badge";
import { cn } from "@/lib/utils";

/** Barra del rango con el cero marcado: deja ver de un vistazo si el rango cruza el cero. */
export function BarraRango({ min, max, valor }: { min: number; max: number; valor: number }) {
  const lo = Math.min(min, 0) * 1.15;
  const hi = Math.max(max, 0) * 1.15;
  const x = (v: number) => `${((v - lo) / (hi - lo)) * 100}%`;
  return (
    <div className="relative h-8 w-full" aria-hidden>
      <div className="absolute inset-x-0 top-3.5 h-px bg-border" />
      <div className="absolute top-2 h-4 rounded-sm bg-oro/20 ring-1 ring-inset ring-oro/50" style={{ left: x(min), width: `calc(${x(max)} - ${x(min)})` }} />
      <div className="absolute top-0 h-8 w-px bg-tenue" style={{ left: x(0) }} />
      <div className="absolute top-1 size-6 -translate-x-1/2 rounded-full border-2 border-oro bg-background" style={{ left: x(valor) }} />
      <span className="cifra absolute -bottom-4 -translate-x-1/2 text-[11px] text-tenue" style={{ left: x(0) }}>
        0 €
      </span>
    </div>
  );
}

export function CifraPrincipalVista({ c, grande = true }: { c: CifraPrincipal; grande?: boolean }) {
  const v = veredictoRango(c.rangoMin, c.rangoMax);
  return (
    <div className="grid gap-4" data-testid="cifra-principal" data-veredicto={v}>
      <div className="flex flex-wrap items-end gap-x-4 gap-y-2">
        <p className={cn("cifra font-semibold leading-none", grande ? "text-5xl sm:text-6xl" : "text-3xl", c.euros >= 0 ? "text-foreground" : "text-mal")}>
          {eurosConSigno(c.euros)}
        </p>
        <p className="cifra pb-1 text-sm text-tenue">
          entre {eurosConSigno(c.rangoMin)} y {eurosConSigno(c.rangoMax)} · rango del {Math.round(c.nivel * 100)} %
        </p>
      </div>
      <BarraRango min={c.rangoMin} max={c.rangoMax} valor={c.euros} />
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <Badge variant={v === "aporta" ? "bien" : v === "resta" ? "mal" : "neutro"}>{textoVeredicto[v]}</Badge>
        <span className="text-xs text-tenue">
          Frente a no hacer nada (cartera sombra), desde el {fecha(c.desde)}, {c.semanas} semanas, después de costes, impuestos e
          inflación. Con un rango de {euros(c.rangoMax - c.rangoMin)}, aún es pronto.
        </span>
      </div>
    </div>
  );
}
