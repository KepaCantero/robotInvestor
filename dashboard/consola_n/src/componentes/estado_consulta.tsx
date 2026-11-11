import { AlertTriangle, Loader2 } from "lucide-react";
import type { ReactNode } from "react";
import type { UseQueryResult } from "@tanstack/react-query";

/**
 * Muestra los datos solo si la última consulta salió bien. Si falla, lo dice y no enseña
 * cifras viejas como si fueran actuales (falla cerrado).
 */
export function ConDatos<T>({ q, children, alto = 120 }: { q: UseQueryResult<T>; children: (d: T) => ReactNode; alto?: number }) {
  if (q.isError)
    return (
      <div role="alert" className="flex items-start gap-3 rounded-md border border-mal/50 bg-mal/10 p-4 text-sm">
        <AlertTriangle className="mt-0.5 size-4 shrink-0 text-mal" />
        <div>
          <p className="font-semibold text-mal">Sin datos: {(q.error as Error).message}</p>
          <p className="text-tenue">No se muestran cifras anteriores para no hacerlas pasar por actuales. Se reintentará sola.</p>
        </div>
      </div>
    );
  if (q.isPending || q.data === undefined)
    return (
      <div className="flex items-center gap-2 text-sm text-tenue" style={{ minHeight: alto }}>
        <Loader2 className="size-4 animate-spin" /> Cargando…
      </div>
    );
  return <>{children(q.data)}</>;
}
