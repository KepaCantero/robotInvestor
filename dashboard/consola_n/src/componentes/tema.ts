import { useEffect, useState } from "react";

/** Lee un token de color de la hoja de estilos («11 13 18») y lo devuelve como «rgb(11, 13, 18)». */
export function color(token: string, alfa = 1): string {
  const v = getComputedStyle(document.documentElement).getPropertyValue(`--${token}`).trim();
  const [r = "0", g = "0", b = "0"] = v.split(/\s+/);
  return alfa === 1 ? `rgb(${r}, ${g}, ${b})` : `rgba(${r}, ${g}, ${b}, ${alfa})`;
}

/** Cambia cuando cambia el tema (preferencia del sistema o data-theme del visor), para repintar los gráficos. */
export function useTema(): number {
  const [v, setV] = useState(0);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: light)");
    const subir = () => setV((x) => x + 1);
    mq.addEventListener("change", subir);
    const obs = new MutationObserver(subir);
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    return () => {
      mq.removeEventListener("change", subir);
      obs.disconnect();
    };
  }, []);
  return v;
}
