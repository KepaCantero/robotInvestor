import { MessageSquareText, ShieldOff } from "lucide-react";
import { cifrasAjenas, explicacionValida } from "@/logica/cifras";
import { numero } from "@/logica/formato";

/**
 * Explicación del Broker junto a las cifras, nunca en su lugar. Antes de mostrarla se comprueba
 * que cada cifra del texto está en la pantalla; si no, se retira (propuesta de N, §4).
 */
export function Explicacion({ texto, cifrasPantalla }: { texto: string; cifrasPantalla: number[] }) {
  if (!texto) return null;
  if (!explicacionValida(texto, cifrasPantalla)) {
    const ajenas = cifrasAjenas(texto, cifrasPantalla);
    return (
      <div data-testid="explicacion-retirada" className="flex gap-3 rounded-md border border-dashed border-aviso/60 p-3 text-sm">
        <ShieldOff className="mt-0.5 size-4 shrink-0 text-aviso" />
        <p className="text-tenue">
          <span className="font-semibold text-aviso">Explicación retirada.</span> El texto del Broker citaba{" "}
          {ajenas.length === 1 ? "una cifra" : "cifras"} que no está en pantalla ({ajenas.map((n) => numero(n)).join(", ")}). Decida con las cifras de F.
        </p>
      </div>
    );
  }
  return (
    <div data-testid="explicacion" className="flex gap-3 rounded-md bg-muted p-3 text-sm">
      <MessageSquareText className="mt-0.5 size-4 shrink-0 text-oro" />
      <div>
        <p className="etiqueta mb-1">Explicación del Broker</p>
        <p>{texto}</p>
      </div>
    </div>
  );
}
