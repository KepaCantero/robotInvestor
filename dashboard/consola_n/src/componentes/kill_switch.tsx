import { useState } from "react";
import { OctagonX, Power } from "lucide-react";
import { useActivarKill, useDesactivarKill, useSalud } from "@/api/consultas";
import { CODIGO_DEMO } from "@/config/prototipo";
import { Button } from "@/componentes/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/componentes/ui/dialog";
import { Input } from "@/componentes/ui/input";

/** Activar es un toque (baja el riesgo). Desactivar lo vuelve a subir: pide segundo factor. */
export function BotonKillSwitch() {
  const salud = useSalud();
  const activar = useActivarKill();
  const desactivar = useDesactivarKill();
  const [abierto, setAbierto] = useState(false);
  const [codigo, setCodigo] = useState("");
  const activo = salud.data?.killSwitch ?? false;

  if (!activo)
    return (
      <Button
        variant="destructive"
        size="sm"
        data-testid="kill-switch"
        onClick={() => activar.mutate()}
        disabled={activar.isPending}
        title="Para el robot: no abre ni aumenta posiciones. No vende nada; los stops siguen en el intermediario."
      >
        <OctagonX /> <span className="hidden sm:inline">Kill-switch</span>
      </Button>
    );

  return (
    <>
      <Button variant="outline" size="sm" data-testid="reactivar" onClick={() => setAbierto(true)}>
        <Power /> <span className="hidden sm:inline">Reactivar el robot</span>
      </Button>
      <Dialog open={abierto} onOpenChange={setAbierto}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Reactivar el robot</DialogTitle>
            <DialogDescription>
              Volver a abrir posiciones sube el riesgo, así que pide el código que llega por el canal fuera del chat.
            </DialogDescription>
          </DialogHeader>
          <label className="grid gap-1.5 text-sm" htmlFor="codigo-kill">
            Código de segundo factor
            <Input id="codigo-kill" inputMode="numeric" autoComplete="one-time-code" value={codigo} onChange={(e) => setCodigo(e.target.value)} />
            <span className="text-xs text-tenue">En el prototipo, el código es {CODIGO_DEMO}.</span>
          </label>
          {desactivar.isError && <p className="text-sm text-mal">{(desactivar.error as Error).message}</p>}
          <DialogFooter>
            <Button variant="ghost" onClick={() => setAbierto(false)}>
              Seguir parado
            </Button>
            <Button
              onClick={() =>
                desactivar.mutate(codigo, {
                  onSuccess: () => {
                    setAbierto(false);
                    setCodigo("");
                  },
                })
              }
              disabled={desactivar.isPending}
            >
              Reactivar
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
