import { useState } from "react";
import { Unplug } from "lucide-react";
import { useSalud, useSimularFallo } from "@/api/consultas";
import { ConDatos } from "@/componentes/estado_consulta";
import { PuntoEstado } from "@/componentes/semaforo";
import { Button } from "@/componentes/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/componentes/ui/card";
import { eurosCent, fechaHora, hora } from "@/logica/formato";

const ESTADO_BLOQUE = { ok: "verde", degradado: "ambar", parado: "rojo" } as const;
const ESTADO_SELLO = { fresco: "verde", viejo: "ambar", dudoso: "rojo" } as const;
const TEXTO_SELLO = { fresco: "Al día", viejo: "Con retraso", dudoso: "Dudoso" } as const;

export function SaludVista() {
  const q = useSalud();
  const simular = useSimularFallo();
  const [fallo, setFallo] = useState(false);
  const alternar = () => {
    simular(!fallo);
    setFallo(!fallo);
  };
  return (
    <div className="grid gap-5">
      <Card className="border-dashed">
        <CardContent className="flex flex-wrap items-center gap-3 pt-4">
          <Unplug className="size-5 text-tenue" />
          <p className="min-w-0 flex-1 text-sm text-tenue">
            Prueba del fallo cerrado: si la API del robot deja de responder, cada pantalla lo dice, el semáforo pasa a rojo y no se muestran cifras viejas.
          </p>
          <Button variant={fallo ? "default" : "outline"} size="sm" data-testid="simular-fallo" onClick={alternar}>
            {fallo ? "Volver a conectar la API" : "Simular que la API no responde"}
          </Button>
        </CardContent>
      </Card>
      <ConDatos q={q}>
        {(s) => {
          const usado = s.presupuestoIA.gastado / s.presupuestoIA.tope;
          return (
            <>
              <div className="grid gap-5 md:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle>Latido del servidor</CardTitle>
                  </CardHeader>
                  <CardContent className="flex items-center gap-3">
                    <PuntoEstado estado="verde" vivo />
                    <span className="cifra text-2xl font-semibold">{hora(s.latido)}</span>
                    <span className="text-sm text-tenue">El vigilante, en otra máquina, avisa si se pierde.</span>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Presupuesto de IA · {s.presupuestoIA.mes}</CardTitle>
                  </CardHeader>
                  <CardContent className="grid gap-2">
                    <p className="cifra text-2xl font-semibold">
                      {eurosCent(s.presupuestoIA.gastado)} <span className="text-base font-normal text-tenue">de {eurosCent(s.presupuestoIA.tope)}</span>
                    </p>
                    <div className="h-2 rounded-sm bg-muted" role="meter" aria-valuemin={0} aria-valuemax={s.presupuestoIA.tope} aria-valuenow={s.presupuestoIA.gastado} aria-label="Presupuesto de IA usado">
                      <div className={`h-full rounded-sm ${usado > 0.9 ? "bg-mal" : "bg-oro"}`} style={{ width: `${Math.min(100, usado * 100)}%` }} />
                    </div>
                    <p className="text-xs text-tenue">Al llegar al tope, el robot sigue sin IA (solo código) hasta el mes siguiente.</p>
                  </CardContent>
                </Card>
              </div>
              <Card>
                <CardHeader>
                  <CardTitle>Estado por bloque</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="grid gap-x-6 gap-y-2 md:grid-cols-2" data-testid="bloques">
                    {s.bloques.map((b) => (
                      <li key={b.id} className="grid grid-cols-[auto_1fr_auto] items-baseline gap-3 border-b border-dashed py-1.5 text-sm">
                        <PuntoEstado estado={ESTADO_BLOQUE[b.estado]} />
                        <span className="min-w-0">
                          <span className="font-medium">{b.nombre}</span>
                          {b.nota && <span className="block text-xs text-tenue">{b.nota}</span>}
                        </span>
                        <span className="cifra text-xs text-tenue">{hora(b.ultimoLatido)}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Sellos de datos (K)</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="grid gap-2">
                    {s.sellos.map((x) => (
                      <li key={x.fuente} className="grid grid-cols-[auto_1fr_auto] items-baseline gap-3 text-sm">
                        <PuntoEstado estado={ESTADO_SELLO[x.estado]} />
                        <span className="min-w-0">{x.fuente}</span>
                        <span className="cifra text-right text-xs text-tenue">
                          {TEXTO_SELLO[x.estado]} · {fechaHora(x.ultimo)}
                        </span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </>
          );
        }}
      </ConDatos>
    </div>
  );
}
