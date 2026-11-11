export type Veredicto = "aporta" | "resta" | "no_se_sabe";

/**
 * Veredicto de una cifra con su rango (propuesta de N, §4; enmienda 5, D-54 [PROPUESTO]).
 * Si el rango incluye el umbral (por defecto, el cero), no se puede decir si aporta o resta.
 */
export function veredictoRango(min: number, max: number, umbral = 0): Veredicto {
  if (!Number.isFinite(min) || !Number.isFinite(max) || min > max) return "no_se_sabe";
  if (min > umbral) return "aporta";
  if (max < umbral) return "resta";
  return "no_se_sabe";
}

export const textoVeredicto: Record<Veredicto, string> = {
  aporta: "El robot aporta frente a no hacer nada",
  resta: "El robot resta frente a no hacer nada",
  no_se_sabe: "Todavía no se puede saber si el robot aporta",
};
