export type EstadoComprobacion = "verde" | "ambar" | "rojo" | "sin_dato";

export interface Comprobacion {
  id: "integridad" | "datos" | "presupuesto" | "avisos" | "decisiones";
  nombre: string;
  estado: EstadoComprobacion;
  detalle: string;
}

export type Color = "verde" | "ambar" | "rojo";

/**
 * Color del panel (N V0.06): rojo si alguna comprobación está en rojo o no se puede calcular,
 * o si faltan comprobaciones; ámbar si alguna lo está; verde solo si las cinco lo están.
 */
export function colorPanel(comprobaciones: readonly Comprobacion[] | undefined | null, esperadas = 5): Color {
  if (!comprobaciones || comprobaciones.length < esperadas) return "rojo";
  if (comprobaciones.some((c) => c.estado === "rojo" || c.estado === "sin_dato")) return "rojo";
  if (comprobaciones.some((c) => c.estado === "ambar")) return "ambar";
  return "verde";
}
