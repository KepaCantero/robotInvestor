const nfEuros = new Intl.NumberFormat("es-ES", { style: "currency", currency: "EUR", maximumFractionDigits: 0 });
const nfEurosCent = new Intl.NumberFormat("es-ES", { style: "currency", currency: "EUR", minimumFractionDigits: 2 });
const nfNum = new Intl.NumberFormat("es-ES", { maximumFractionDigits: 4 });

/** Fuerza el separador de miles también en números de cuatro cifras (Intl en español no lo pone: «1500 €»). */
function milesSiempre(texto: string): string {
  return texto.replace(/(^|[^\d,])(\d)(\d{3})(?=[^\d]|$)/g, "$1$2.$3");
}

export const euros = (n: number) => milesSiempre(nfEuros.format(n));
export const eurosCent = (n: number) => milesSiempre(nfEurosCent.format(n));
export const eurosConSigno = (n: number) => (n > 0 ? "+" : n < 0 ? "−" : "") + euros(Math.abs(n));
export const numero = (n: number) => milesSiempre(nfNum.format(n));
export const pct = (n: number, dec = 1) =>
  `${n > 0 ? "+" : n < 0 ? "−" : ""}${Math.abs(n).toFixed(dec).replace(".", ",")} %`;

export function hora(iso: string): string {
  return new Date(iso).toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Madrid" });
}
export function fecha(iso: string): string {
  return new Date(iso).toLocaleDateString("es-ES", { day: "numeric", month: "short", year: "numeric", timeZone: "Europe/Madrid" });
}
export function fechaHora(iso: string): string {
  return `${fecha(iso)}, ${hora(iso)}`;
}
export function minutosRestantes(iso: string, ahora: number = Date.now()): number {
  return Math.round((new Date(iso).getTime() - ahora) / 60000);
}
