// Tipos del prototipo. Imitan lo que N leería de cada bloque; cuando el diseño se cierre se
// generarán de los esquemas reales (regla 3 del proyecto), no a mano.
import type { Comprobacion } from "@/logica/semaforo";
import type { TipoAccion } from "@/logica/friccion";

export type CarteraId = "trading" | "tactica" | "largo";

export interface CifraPrincipal {
  /** Diferencia frente a la cartera sombra, en euros, después de costes, impuestos e inflación (I). */
  euros: number;
  rangoMin: number;
  rangoMax: number;
  nivel: number;
  desde: string;
  semanas: number;
}

/** Resultado de control de F (imita CT-G-08: aprobado, reducido o vetado, con motivo y tipo de acción). */
export interface CifrasF {
  resultado: "aprobado" | "reducido";
  motivo: string;
  importe: number;
  cantidad: number;
  precioRef: number;
  stop: number | null;
  perdidaMaxima: number;
}

export interface Decision {
  id: string;
  tipo: TipoAccion;
  cartera: CarteraId;
  instrumento: string;
  resumen: string;
  cifrasF: CifrasF;
  /** Riesgo en euros de M: pérdida en una caída como la de 2008, para esta operación. */
  estresM: number;
  planBase: string;
  venceEn: string;
  limiteTocadoHoy: boolean;
  explicacion: string;
  estado: "pendiente" | "aprobada" | "rechazada" | "caducada";
  usada: boolean;
}

export interface Posicion {
  id: string;
  cartera: CarteraId;
  instrumento: string;
  clase: string;
  cantidad: number;
  precioEntrada: number;
  precio: number;
  valor: number;
  resultado: number;
  /** Rango esperado de H para el horizonte de la posición, en precio. */
  rangoMin: number;
  rangoMax: number;
  /** Pérdida en euros de M en una caída como la de 2008. */
  estres: number;
  stop: number | null;
  /** Solo largo plazo: caída que el operador aceptó por escrito, en % desde el máximo. */
  caidaAceptada?: number;
  /** Solo largo plazo: caída real desde el máximo, en %. */
  caidaActual?: number;
  costeSalida?: number;
}

export interface Cartera {
  id: CarteraId;
  nombre: string;
  ritmo: string;
  valor: number;
  efectivo: number;
  resultadoPeriodo: number;
  periodo: string;
  /** Largo plazo: avance frente al plan, en lugar de la cifra diaria. */
  plan?: { objetivo: string; anosHechos: number; anosTotales: number; enCamino: boolean; nota: string };
}

export interface Aviso {
  id: string;
  prioridad: "alta" | "media" | "info";
  titulo: string;
  detalle: string;
  fecha: string;
  acusadoEn: string | null;
}

export interface EtapaEmbudo {
  etapa: string;
  cantidad: number;
}

export interface Atribucion {
  etapa: string;
  euros: number;
  rangoMin: number;
  rangoMax: number;
}

export interface PuntoSerie {
  fecha: string;
  valor: number;
}

export interface Informes {
  semanal: {
    semana: string;
    analisis: number;
    ordenes: number;
    abstenciones: number;
    embudo: EtapaEmbudo[];
    costeIA: number;
    costeIntermediario: number;
  };
  mensual: {
    mes: string;
    robot: PuntoSerie[];
    sombra: PuntoSerie[];
    atribucion: Atribucion[];
    intervenciones: { descripcion: string; euros: number }[];
  };
  anual: { pregunta: string; hecho: boolean }[];
}

export interface EstadoBloque {
  id: string;
  nombre: string;
  estado: "ok" | "degradado" | "parado";
  ultimoLatido: string;
  nota: string;
}

export interface SelloDatos {
  fuente: string;
  ultimo: string;
  estado: "fresco" | "viejo" | "dudoso";
}

export interface Salud {
  bloques: EstadoBloque[];
  sellos: SelloDatos[];
  presupuestoIA: { gastado: number; tope: number; mes: string };
  latido: string;
  killSwitch: boolean;
}

export interface Parametro {
  id: string;
  nombre: string;
  valor: number;
  porDefecto: number;
  unidad: string;
  /** Qué significa en euros, para decidir con cifras y no con porcentajes sueltos. */
  enEuros: string;
  justificacion: string;
  /** Si subir el valor sube el riesgo. */
  subeRiesgo: boolean;
}

export interface OperacionExterna {
  instrumento: string;
  lado: "compra" | "venta";
  cantidad: number;
  precio: number;
  fecha: string;
}

export interface Panel {
  comprobaciones: Comprobacion[];
  cifra: CifraPrincipal;
  carteras: Cartera[];
}
