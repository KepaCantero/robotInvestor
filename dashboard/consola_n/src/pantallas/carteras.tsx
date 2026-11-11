import { useMemo, useState } from "react";
import { FilePlus2, TrendingDown } from "lucide-react";
import { useCarteras, useDeclarar, usePosiciones, useSerie, useVender } from "@/api/consultas";
import type { CarteraId, Posicion } from "@/api/tipos";
import { ConDatos } from "@/componentes/estado_consulta";
import { GraficoPrecio, type Linea } from "@/componentes/grafico";
import { TablaPosiciones } from "@/componentes/tabla_posiciones";
import { Badge } from "@/componentes/ui/badge";
import { Button } from "@/componentes/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/componentes/ui/card";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/componentes/ui/dialog";
import { Input } from "@/componentes/ui/input";
import { Tabs, TabsList, TabsTrigger } from "@/componentes/ui/tabs";
import { euros, eurosConSigno, numero, pct } from "@/logica/formato";
import { useUI } from "@/estado/tienda";

/** Contra la venta de pánico, sin bloquearla (propuesta de N, §6): se muestra antes, sin espera. */
function AntesDeVender({ p, alVender, alMantener, enviando }: { p: Posicion; alVender: () => void; alMantener: () => void; enviando: boolean }) {
  return (
    <div data-testid="antipanico" className="grid gap-4 rounded-md border border-aviso/60 bg-aviso/5 p-4">
      <div className="flex items-center gap-2">
        <TrendingDown className="size-5 text-aviso" />
        <p className="font-semibold">Antes de vender en una caída</p>
      </div>
      <dl className="grid gap-3 sm:grid-cols-3">
        <div>
          <dt className="etiqueta">Caída que aceptó por escrito</dt>
          <dd className="cifra text-2xl font-semibold">{pct(-(p.caidaAceptada ?? 0), 0)}</dd>
        </div>
        <div>
          <dt className="etiqueta">Caída real desde el máximo</dt>
          <dd className="cifra text-2xl font-semibold text-aviso">{pct(-(p.caidaActual ?? 0))}</dd>
        </div>
        <div>
          <dt className="etiqueta">Coste de salir</dt>
          <dd className="cifra text-2xl font-semibold">{euros(p.costeSalida ?? 0)}</dd>
          <dd className="text-xs text-tenue">de comisión; la pérdida de {euros(Math.abs(p.resultado))} se hace real</dd>
        </div>
      </dl>
      <p className="text-sm">
        <span className="font-semibold">Lo que dice el plan base:</span> mantener el fondo y seguir aportando cada mes. Vender ahora fija la pérdida y deja fuera
        la recuperación, si llega.
      </p>
      <div className="flex flex-wrap gap-2">
        <Button variant="outline" onClick={alMantener}>
          Mantener, como dice el plan
        </Button>
        <Button variant="destructive" data-testid="vender-igualmente" onClick={alVender} disabled={enviando}>
          Vender igualmente
        </Button>
      </div>
      <p className="text-xs text-tenue">Nunca se le impide reducir riesgo. Esto solo se muestra una vez, antes de vender.</p>
    </div>
  );
}

function DetallePosicion({ p }: { p: Posicion }) {
  const serie = useSerie(p.id);
  const vender = useVender();
  const [aviso, setAviso] = useState(false);
  const lineas = useMemo<Linea[]>(
    () => [
      { precio: p.precioEntrada, titulo: "Entrada", token: "tenue" },
      ...(p.stop ? [{ precio: p.stop, titulo: "Stop", token: "mal" as const }] : []),
      { precio: p.rangoMax, titulo: "H máx.", token: "bien", discontinua: true },
      { precio: p.rangoMin, titulo: "H mín.", token: "aviso", discontinua: true },
    ],
    [p.precioEntrada, p.stop, p.rangoMax, p.rangoMin],
  );
  const enCaida = p.cartera === "largo" && (p.caidaActual ?? 0) > 0;
  const venderTodo = () => vender.mutate({ id: p.id, cantidad: p.cantidad }, { onSuccess: () => setAviso(false) });

  return (
    <Card data-testid="detalle-posicion">
      <CardHeader className="gap-2">
        <div className="flex flex-wrap items-center gap-2">
          <h2 className="text-lg font-semibold">{p.instrumento}</h2>
          <Badge variant="neutro">{p.clase}</Badge>
          <span className={`cifra ml-auto text-sm ${p.resultado < 0 ? "text-mal" : "text-bien"}`}>{eurosConSigno(p.resultado)}</span>
        </div>
      </CardHeader>
      <CardContent className="grid gap-4">
        <ConDatos q={serie} alto={260}>
          {(s) => <GraficoPrecio serie={s} lineas={lineas} />}
        </ConDatos>
        <p className="text-xs text-tenue">
          Líneas: precio de entrada, stop en el intermediario y rango esperado de H para su horizonte (entre {numero(p.rangoMin)} y {numero(p.rangoMax)}). En una
          caída como la de 2008, esta posición perdería unos {euros(p.estres)} (M).
        </p>
        {p.cantidad === 0 ? (
          <p className="text-sm text-tenue">Posición cerrada.</p>
        ) : aviso && enCaida ? (
          <AntesDeVender p={p} alVender={venderTodo} alMantener={() => setAviso(false)} enviando={vender.isPending} />
        ) : (
          <div className="flex flex-wrap items-center gap-2">
            <Button variant="outline" data-testid="vender" onClick={() => (enCaida ? setAviso(true) : venderTodo())} disabled={vender.isPending}>
              Vender todo
            </Button>
            <Button variant="ghost" onClick={() => vender.mutate({ id: p.id, cantidad: Number((p.cantidad / 2).toFixed(4)) })} disabled={vender.isPending || enCaida}>
              Vender la mitad
            </Button>
            <span className="text-xs text-tenue">Reducir riesgo: un toque, sin aprobación.</span>
          </div>
        )}
        {vender.isError && <p className="text-sm text-mal">{(vender.error as Error).message}</p>}
      </CardContent>
    </Card>
  );
}

function Declarar() {
  const declarar = useDeclarar();
  const [abierto, setAbierto] = useState(false);
  const [instrumento, setInstrumento] = useState("");
  const [lado, setLado] = useState<"compra" | "venta">("compra");
  const [cantidad, setCantidad] = useState("");
  const [precio, setPrecio] = useState("");
  const [fecha, setFecha] = useState(new Date().toISOString().slice(0, 10));
  const num = (s: string) => Number(s.replace(/\./g, "").replace(",", "."));
  return (
    <Dialog open={abierto} onOpenChange={setAbierto}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm" data-testid="declarar">
          <FilePlus2 /> Declarar una operación hecha fuera del robot
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Operación hecha fuera del robot</DialogTitle>
          <DialogDescription>Si compró o vendió por su cuenta, declárelo: si no, G la verá como una discrepancia al conciliar.</DialogDescription>
        </DialogHeader>
        <form
          className="grid gap-3"
          onSubmit={(e) => {
            e.preventDefault();
            declarar.mutate(
              { instrumento, lado, cantidad: num(cantidad), precio: num(precio), fecha },
              { onSuccess: () => setAbierto(false) },
            );
          }}
        >
          <label className="grid gap-1.5 text-sm" htmlFor="op-instrumento">
            Instrumento
            <Input id="op-instrumento" value={instrumento} onChange={(e) => setInstrumento(e.target.value)} required />
          </label>
          <div className="grid grid-cols-2 gap-3">
            <label className="grid gap-1.5 text-sm" htmlFor="op-lado">
              Compra o venta
              <select id="op-lado" value={lado} onChange={(e) => setLado(e.target.value as "compra" | "venta")} className="h-9 rounded-md border bg-background px-2 text-sm">
                <option value="compra">Compra</option>
                <option value="venta">Venta</option>
              </select>
            </label>
            <label className="grid gap-1.5 text-sm" htmlFor="op-fecha">
              Fecha
              <Input id="op-fecha" type="date" value={fecha} onChange={(e) => setFecha(e.target.value)} required />
            </label>
            <label className="grid gap-1.5 text-sm" htmlFor="op-cantidad">
              Cantidad
              <Input id="op-cantidad" inputMode="decimal" value={cantidad} onChange={(e) => setCantidad(e.target.value)} required className="cifra" />
            </label>
            <label className="grid gap-1.5 text-sm" htmlFor="op-precio">
              Precio
              <Input id="op-precio" inputMode="decimal" value={precio} onChange={(e) => setPrecio(e.target.value)} required className="cifra" />
            </label>
          </div>
          {declarar.isError && <p className="text-sm text-mal">{(declarar.error as Error).message}</p>}
          <DialogFooter>
            <Button type="submit" disabled={declarar.isPending}>
              Declarar
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

export function Carteras() {
  const pos = usePosiciones();
  const cart = useCarteras();
  const { cartera, fijarCartera, posicionSeleccionada, seleccionarPosicion } = useUI();
  return (
    <div className="grid gap-5">
      <div className="flex flex-wrap items-center gap-3">
        <Tabs value={cartera} onValueChange={(v) => fijarCartera(v as CarteraId)}>
          <TabsList>
            <TabsTrigger value="trading">Trading</TabsTrigger>
            <TabsTrigger value="tactica">Táctica</TabsTrigger>
            <TabsTrigger value="largo">Largo plazo</TabsTrigger>
          </TabsList>
        </Tabs>
        <div className="ml-auto">
          <Declarar />
        </div>
      </div>
      <ConDatos q={cart}>
        {(cs) => {
          const c = cs.find((x) => x.id === cartera)!;
          return (
            <div className="flex flex-wrap gap-x-8 gap-y-2 text-sm">
              <span>
                <span className="etiqueta mr-2">Valor</span>
                <span className="cifra font-semibold">{euros(c.valor)}</span>
              </span>
              <span>
                <span className="etiqueta mr-2">Efectivo</span>
                <span className="cifra">{euros(c.efectivo)}</span>
              </span>
              <span>
                <span className="etiqueta mr-2">Mirarla</span>
                {c.ritmo.toLowerCase()}
              </span>
            </div>
          );
        }}
      </ConDatos>
      <ConDatos q={pos}>
        {(ps) => {
          const filas = ps.filter((p) => p.cartera === cartera && p.cantidad > 0);
          const sel = filas.find((p) => p.id === posicionSeleccionada) ?? filas[0];
          return (
            <div className="grid gap-5">
              <Card>
                <CardHeader>
                  <CardTitle>Posiciones</CardTitle>
                </CardHeader>
                <CardContent className="overflow-x-auto">
                  <TablaPosiciones filas={filas} seleccion={sel?.id ?? null} alElegir={seleccionarPosicion} />
                </CardContent>
              </Card>
              {sel && <DetallePosicion key={sel.id} p={sel} />}
            </div>
          );
        }}
      </ConDatos>
    </div>
  );
}
