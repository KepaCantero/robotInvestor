// Estado de la interfaz (Zustand): qué pantalla se ve y qué está seleccionado.
// Los datos del robot no viven aquí: vienen de la API con TanStack Query.
import { create } from "zustand";
import type { CarteraId } from "@/api/tipos";

export const PANTALLAS = ["inicio", "decisiones", "carteras", "avisos", "informes", "salud", "configuracion"] as const;
export type Pantalla = (typeof PANTALLAS)[number];

export function pantallaDeHash(hash: string): Pantalla {
  const h = hash.replace(/^#/, "");
  return (PANTALLAS as readonly string[]).includes(h) ? (h as Pantalla) : "inicio";
}

interface EstadoUI {
  pantalla: Pantalla;
  decisionSeleccionada: string | null;
  cartera: CarteraId;
  posicionSeleccionada: string | null;
  ir: (p: Pantalla) => void;
  fijarPantalla: (p: Pantalla) => void;
  seleccionarDecision: (id: string | null) => void;
  fijarCartera: (c: CarteraId) => void;
  seleccionarPosicion: (id: string | null) => void;
}

export const useUI = create<EstadoUI>((set) => ({
  pantalla: typeof window === "undefined" ? "inicio" : pantallaDeHash(window.location.hash),
  decisionSeleccionada: null,
  cartera: "trading",
  posicionSeleccionada: null,
  ir: (p) => {
    if (typeof window !== "undefined" && window.location.hash !== `#${p}`) window.location.hash = p;
    set({ pantalla: p });
  },
  fijarPantalla: (p) => set({ pantalla: p }),
  seleccionarDecision: (id) => set({ decisionSeleccionada: id }),
  fijarCartera: (c) => set({ cartera: c, posicionSeleccionada: null }),
  seleccionarPosicion: (id) => set({ posicionSeleccionada: id }),
}));
