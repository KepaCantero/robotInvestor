// Consultas y mutaciones con TanStack Query sobre el puerto. Las pantallas solo usan estos ganchos.
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ApiSimulada } from "./simulada";
import type { ConsolaApi } from "./puerto";
import type { OperacionExterna } from "./tipos";

export const api: ConsolaApi & { fallo?: boolean } = new ApiSimulada();

const cada = { refetchInterval: 15_000 } as const;

export const useComprobaciones = () => useQuery({ queryKey: ["comprobaciones"], queryFn: () => api.comprobaciones(), ...cada });
export const useCifra = () => useQuery({ queryKey: ["cifra"], queryFn: () => api.cifraPrincipal() });
export const useCarteras = () => useQuery({ queryKey: ["carteras"], queryFn: () => api.carteras() });
export const usePosiciones = () => useQuery({ queryKey: ["posiciones"], queryFn: () => api.posiciones() });
export const useSerie = (id: string | null) =>
  useQuery({ queryKey: ["serie", id], queryFn: () => api.serie(id!), enabled: !!id });
export const useDecisiones = () => useQuery({ queryKey: ["decisiones"], queryFn: () => api.decisiones(), ...cada });
export const useAvisos = () => useQuery({ queryKey: ["avisos"], queryFn: () => api.avisos(), ...cada });
export const useInformes = () => useQuery({ queryKey: ["informes"], queryFn: () => api.informes() });
export const useSalud = () => useQuery({ queryKey: ["salud"], queryFn: () => api.salud(), ...cada });
export const useParametros = () => useQuery({ queryKey: ["parametros"], queryFn: () => api.parametros() });

function useMutacion<A, R>(fn: (a: A) => Promise<R>) {
  const qc = useQueryClient();
  return useMutation({ mutationFn: fn, onSettled: () => qc.invalidateQueries() });
}

export const usePedirCodigo = () => useMutacion((id: string) => api.pedirCodigo(id));
export const useAprobar = () =>
  useMutacion((a: { id: string; importe: string; codigo: string }) => api.aprobar(a.id, a.importe, a.codigo));
export const useRechazar = () => useMutacion((id: string) => api.rechazar(id));
export const useVender = () => useMutacion((a: { id: string; cantidad: number }) => api.vender(a.id, a.cantidad));
export const useAcusar = () => useMutacion((id: string) => api.acusar(id));
export const useActivarKill = () => useMutacion((_: void) => api.activarKillSwitch());
export const useDesactivarKill = () => useMutacion((codigo: string) => api.desactivarKillSwitch(codigo));
export const useProponerParametro = () =>
  useMutacion((a: { id: string; valor: number }) => api.proponerParametro(a.id, a.valor));
export const useDeclarar = () => useMutacion((op: OperacionExterna) => api.declararOperacion(op));

/** Solo para la demostración del fallo cerrado (pantalla de salud). */
export function useSimularFallo() {
  const qc = useQueryClient();
  return (activo: boolean) => {
    api.fallo = activo;
    void qc.invalidateQueries();
  };
}
