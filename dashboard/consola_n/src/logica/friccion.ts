export type TipoAccion = "abrir" | "aumentar" | "reducir" | "cerrar" | "proteger" | "subir_limite";

export const SUBE_RIESGO: ReadonlySet<TipoAccion> = new Set(["abrir", "aumentar", "subir_limite"]);

export interface Requisitos {
  /** Reducir, cerrar o proteger: un toque, sin más. */
  unToque: boolean;
  importeTecleado: boolean;
  segundoFactor: boolean;
  esperaSeg: number;
}

/**
 * Fricción asimétrica (propuesta de N, §6). Bajar el riesgo es inmediato; subirlo cuesta.
 * «abrir» dentro del mandato pide importe tecleado; «aumentar» y «subir_limite» piden además
 * segundo factor y espera.
 */
export function requisitos(tipo: TipoAccion, esperaSeg: number): Requisitos {
  if (!SUBE_RIESGO.has(tipo)) return { unToque: true, importeTecleado: false, segundoFactor: false, esperaSeg: 0 };
  if (tipo === "abrir") return { unToque: false, importeTecleado: true, segundoFactor: false, esperaSeg: 0 };
  return { unToque: false, importeTecleado: true, segundoFactor: true, esperaSeg };
}

/**
 * Lee un importe tecleado en formato español («1.234,56», «1234,56», «1234») y lo devuelve en céntimos.
 * Devuelve null si no es un importe válido. No acepta el punto como decimal: «12.50» es ambiguo.
 */
export function importeACentimos(texto: string): number | null {
  const t = texto.trim().replace(/\s|€/g, "");
  if (!/^\d{1,3}(\.\d{3})*(,\d{1,2})?$|^\d+(,\d{1,2})?$/.test(t)) return null;
  const [entero = "", dec = ""] = t.replace(/\./g, "").split(",");
  return Number(entero) * 100 + Number(dec.padEnd(2, "0"));
}

export interface EstadoAprobacion {
  usada: boolean;
  venceEn: string;
  limiteTocadoHoy: boolean;
}

export type MotivoBloqueo =
  | "usada"
  | "caducada"
  | "limite_hoy"
  | "importe_distinto"
  | "falta_codigo"
  | "codigo_erroneo"
  | "en_espera";

export interface Comprobar {
  tipo: TipoAccion;
  importeEsperadoCent: number;
  importeTecleado: string;
  codigo: string;
  codigoValido: string;
  esperaRestanteSeg: number;
  estado: EstadoAprobacion;
  ahora?: number;
}

/** Devuelve el primer motivo que impide confirmar, o null si se puede confirmar. */
export function motivoBloqueo(c: Comprobar): MotivoBloqueo | null {
  if (c.estado.usada) return "usada";
  if (new Date(c.estado.venceEn).getTime() <= (c.ahora ?? Date.now())) return "caducada";
  const r = requisitos(c.tipo, 0);
  if (r.unToque) return null;
  if (SUBE_RIESGO.has(c.tipo) && c.tipo !== "abrir" && c.estado.limiteTocadoHoy) return "limite_hoy";
  if (importeACentimos(c.importeTecleado) !== c.importeEsperadoCent) return "importe_distinto";
  if (r.segundoFactor) {
    if (c.codigo.trim() === "") return "falta_codigo";
    if (c.codigo.trim() !== c.codigoValido) return "codigo_erroneo";
    if (c.esperaRestanteSeg > 0) return "en_espera";
  }
  return null;
}

export const textoBloqueo: Record<MotivoBloqueo, string> = {
  usada: "Esta aprobación ya se usó. Cada aprobación vale una sola vez.",
  caducada: "Esta aprobación caducó sin actuar. Si sigue haciendo falta, el robot la volverá a proponer.",
  limite_hoy: "Hoy se alcanzó un límite: aumentar el riesgo no se puede hasta mañana.",
  importe_distinto: "Teclee el importe exacto, al céntimo, tal como aparece en las cifras de F.",
  falta_codigo: "Falta el código de segundo factor.",
  codigo_erroneo: "El código no es correcto.",
  en_espera: "Espere a que termine la cuenta atrás antes de confirmar.",
};
