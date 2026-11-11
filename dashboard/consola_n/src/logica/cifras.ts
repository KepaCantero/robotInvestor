/**
 * Comprobación de cifras de una explicación del Broker (propuesta de N, §4):
 * antes de mostrarla, cada cifra del texto tiene que estar en la pantalla. Si alguna no está,
 * la explicación no se muestra.
 */

/** Extrae los números de un texto en formato español: «1.234,56 €», «2,5 %», «−310», «90». */
export function extraerCifras(texto: string): number[] {
  const encontrados = texto.match(/[−-]?\d{1,3}(?:\.\d{3})+(?:,\d+)?|[−-]?\d+(?:,\d+)?/g) ?? [];
  return encontrados.map((s) => Number(s.replace("−", "-").replace(/\./g, "").replace(",", ".")));
}

const iguales = (a: number, b: number) => Math.abs(a - b) < 1e-6;

/**
 * true si cada cifra del texto aparece entre las cifras de la pantalla (también en valor absoluto,
 * porque el texto puede decir «cae 310 €» de una cifra que en pantalla es −310 €).
 */
export function explicacionValida(texto: string, cifrasPantalla: readonly number[]): boolean {
  const permitidas = cifrasPantalla.flatMap((n) => [n, Math.abs(n)]);
  return extraerCifras(texto).every((c) => permitidas.some((p) => iguales(p, c)));
}

/** Cifras del texto que no están en la pantalla (para explicar por qué se retiró). */
export function cifrasAjenas(texto: string, cifrasPantalla: readonly number[]): number[] {
  const permitidas = cifrasPantalla.flatMap((n) => [n, Math.abs(n)]);
  return extraerCifras(texto).filter((c) => !permitidas.some((p) => iguales(p, c)));
}
