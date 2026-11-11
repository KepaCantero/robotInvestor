import { colorPanel, type Comprobacion, type EstadoComprobacion } from "@/logica/semaforo";
import { cn } from "@/lib/utils";

const estilo: Record<EstadoComprobacion | "rojo", string> = {
  verde: "bg-bien",
  ambar: "bg-aviso",
  rojo: "bg-mal",
  sin_dato: "bg-mal",
};
const texto = { verde: "Todo en orden", ambar: "Hay algo que mirar", rojo: "Algo falla o no se puede comprobar" };

export function PuntoEstado({ estado, vivo = false }: { estado: EstadoComprobacion; vivo?: boolean }) {
  return <span aria-hidden className={cn("inline-block size-2.5 shrink-0 rounded-full", estilo[estado], vivo && "punto-vivo")} />;
}

export function PastillaSemaforo({ comprobaciones }: { comprobaciones: Comprobacion[] | undefined }) {
  const c = colorPanel(comprobaciones);
  return (
    <span
      data-testid="semaforo"
      data-color={c}
      className={cn(
        "inline-flex items-center gap-2 rounded-sm border px-2.5 py-1 text-xs font-semibold uppercase tracking-[0.08em]",
        c === "verde" && "border-bien/50 text-bien",
        c === "ambar" && "border-aviso/50 text-aviso",
        c === "rojo" && "border-mal/60 text-mal",
      )}
    >
      <PuntoEstado estado={c} vivo />
      <span className="hidden sm:inline">{texto[c]}</span>
      <span className="sm:hidden">{c === "verde" ? "Bien" : c === "ambar" ? "Mirar" : "Fallo"}</span>
    </span>
  );
}

export function ListaComprobaciones({ comprobaciones }: { comprobaciones: Comprobacion[] }) {
  return (
    <ul className="grid gap-2">
      {comprobaciones.map((c) => (
        <li key={c.id} className="grid grid-cols-[auto_7rem_1fr] items-baseline gap-3 text-sm">
          <PuntoEstado estado={c.estado} />
          <span className="font-medium">{c.nombre}</span>
          <span className="min-w-0 text-tenue">{c.detalle}</span>
        </li>
      ))}
    </ul>
  );
}
