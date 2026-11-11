// Puerto de la consola: lo único que las pantallas saben de la API. La implementación simulada
// (simulada.ts) se cambiará por la real (el Orquestador) sin tocar las pantallas.
import type { Comprobacion } from "@/logica/semaforo";
import type {
  Aviso,
  Cartera,
  CifraPrincipal,
  Decision,
  Informes,
  OperacionExterna,
  Parametro,
  Posicion,
  PuntoSerie,
  Salud,
} from "./tipos";

export interface ConsolaApi {
  comprobaciones(): Promise<Comprobacion[]>;
  cifraPrincipal(): Promise<CifraPrincipal>;
  carteras(): Promise<Cartera[]>;
  posiciones(): Promise<Posicion[]>;
  serie(posicionId: string): Promise<PuntoSerie[]>;
  decisiones(): Promise<Decision[]>;
  avisos(): Promise<Aviso[]>;
  informes(): Promise<Informes>;
  salud(): Promise<Salud>;
  parametros(): Promise<Parametro[]>;

  /** Envía el código de segundo factor por el canal fuera del chat y empieza la espera. */
  pedirCodigo(decisionId: string): Promise<{ esperaHasta: string }>;
  aprobar(decisionId: string, importeTecleado: string, codigo: string): Promise<Decision>;
  rechazar(decisionId: string): Promise<Decision>;
  /** Reducir riesgo: un toque. */
  vender(posicionId: string, cantidad: number): Promise<Posicion>;
  acusar(avisoId: string): Promise<Aviso>;
  activarKillSwitch(): Promise<Salud>;
  desactivarKillSwitch(codigo: string): Promise<Salud>;
  /** Bajar el riesgo se aplica al momento; subirlo crea una decisión pendiente. */
  proponerParametro(id: string, valor: number): Promise<{ aplicado: boolean; decisionId?: string }>;
  declararOperacion(op: OperacionExterna): Promise<Aviso>;
}

export class ErrorApi extends Error {}
