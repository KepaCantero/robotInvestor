import { useState } from "react";
import { ArrowDown, ArrowUp, RotateCcw } from "lucide-react";
import { useParametros, useProponerParametro } from "@/api/consultas";
import type { Parametro } from "@/api/tipos";
import { ConDatos } from "@/componentes/estado_consulta";
import { Badge } from "@/componentes/ui/badge";
import { Button } from "@/componentes/ui/button";
import { Card, CardContent } from "@/componentes/ui/card";
import { Input } from "@/componentes/ui/input";
import { numero } from "@/logica/formato";
import { useUI } from "@/estado/tienda";

function FilaParametro({ p }: { p: Parametro }) {
  const proponer = useProponerParametro();
  const { ir, seleccionarDecision } = useUI();
  const [valor, setValor] = useState(numero(p.valor));
  const [resultado, setResultado] = useState<string | null>(null);
  const n = Number(valor.replace(/\./g, "").replace(",", "."));
  const sube = p.subeRiesgo && n > p.valor;
  const cambiado = Number.isFinite(n) && n !== p.valor;

  return (
    <li data-testid={`param-${p.id}`} className="grid gap-3 border-b border-dashed py-4 last:border-0 md:grid-cols-[1fr_14rem]">
      <div className="min-w-0">
        <div className="flex flex-wrap items-center gap-2">
          <p className="font-medium">{p.nombre}</p>
          {p.valor !== p.porDefecto && <Badge variant="aviso">Distinto del valor por defecto</Badge>}
        </div>
        <p className="cifra mt-1 text-sm">
          {numero(p.valor)} {p.unidad} <span className="text-tenue">· {p.enEuros}</span>
        </p>
        <p className="mt-1 text-sm text-tenue">{p.justificacion}</p>
        <p className="mt-1 text-xs text-tenue">
          Por defecto: {numero(p.porDefecto)} {p.unidad}.
        </p>
      </div>
      <div className="grid content-start gap-2">
        <label className="grid gap-1 text-xs text-tenue" htmlFor={`valor-${p.id}`}>
          Valor nuevo
          <Input id={`valor-${p.id}`} value={valor} onChange={(e) => setValor(e.target.value)} inputMode="decimal" className="cifra" />
        </label>
        {cambiado && (
          <Button
            size="sm"
            variant={sube ? "default" : "outline"}
            data-testid={`proponer-${p.id}`}
            disabled={proponer.isPending}
            onClick={() =>
              proponer.mutate(
                { id: p.id, valor: n },
                {
                  onSuccess: (r) => {
                    if (r.aplicado) setResultado("Aplicado. Bajar el riesgo no pide más.");
                    else {
                      setResultado(null);
                      seleccionarDecision(r.decisionId ?? null);
                      ir("decisiones");
                    }
                  },
                },
              )
            }
          >
            {sube ? <ArrowUp /> : <ArrowDown />}
            {sube ? "Proponer la subida" : "Aplicar ahora"}
          </Button>
        )}
        {cambiado && sube && <p className="text-xs text-tenue">Sube el riesgo: pasa a Decisiones con segundo factor y espera, y nunca el día en que se tocó un límite.</p>}
        {p.valor !== p.porDefecto && (
          <Button size="sm" variant="ghost" onClick={() => setValor(numero(p.porDefecto))}>
            <RotateCcw /> Volver al valor por defecto
          </Button>
        )}
        {resultado && <p className="text-xs text-bien">{resultado}</p>}
        {proponer.isError && <p className="text-xs text-mal">{(proponer.error as Error).message}</p>}
      </div>
    </li>
  );
}

export function Configuracion() {
  const q = useParametros();
  return (
    <div className="grid gap-4">
      <p className="max-w-prose text-sm text-tenue">
        Cada parámetro con su valor por defecto y lo que significa en euros. Bajar el riesgo se aplica al momento; subirlo se convierte en una decisión con
        su fricción. En la consola real, el asesor de configuración del Broker explica cada cambio antes de pedirlo.
      </p>
      <Card>
        <CardContent className="pt-2">
          <ConDatos q={q}>{(ps) => <ul>{ps.map((p) => <FilaParametro key={p.id} p={p} />)}</ul>}</ConDatos>
        </CardContent>
      </Card>
    </div>
  );
}
