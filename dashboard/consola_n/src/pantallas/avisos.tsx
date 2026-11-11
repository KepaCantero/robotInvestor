import { useState } from "react";
import { CheckCheck } from "lucide-react";
import { useAcusar, useAvisos } from "@/api/consultas";
import type { Aviso } from "@/api/tipos";
import { ConDatos } from "@/componentes/estado_consulta";
import { Badge } from "@/componentes/ui/badge";
import { Button } from "@/componentes/ui/button";
import { Tabs, TabsList, TabsTrigger } from "@/componentes/ui/tabs";
import { fechaHora, hora } from "@/logica/formato";
import { cn } from "@/lib/utils";

const PRIORIDAD = {
  alta: { nombre: "Alta · exige actuar", variante: "mal", franja: "bg-mal", canal: "Móvil y correo, nunca el chat" },
  media: { nombre: "Media · conviene saber", variante: "aviso", franja: "bg-aviso", canal: "Resumen diario" },
  info: { nombre: "Información", variante: "neutro", franja: "bg-border", canal: "Resumen semanal" },
} as const;

function Tarjeta({ a }: { a: Aviso }) {
  const acusar = useAcusar();
  const p = PRIORIDAD[a.prioridad];
  return (
    <li data-testid={`aviso-${a.id}`} className="relative grid gap-2 overflow-hidden rounded-md border bg-card p-4 pl-5">
      <span aria-hidden className={cn("absolute inset-y-0 left-0 w-1", p.franja)} />
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant={p.variante}>{p.nombre}</Badge>
        <span className="cifra text-xs text-tenue">{fechaHora(a.fecha)}</span>
        <span className="text-xs text-tenue">· {p.canal}</span>
      </div>
      <p className="font-semibold">{a.titulo}</p>
      <p className="text-sm text-tenue">{a.detalle}</p>
      {a.acusadoEn ? (
        <p className="flex items-center gap-1.5 text-xs text-bien" data-testid="acusado">
          <CheckCheck className="size-3.5" /> Acusado a las {hora(a.acusadoEn)}. Sigue en el historial.
        </p>
      ) : (
        <Button size="sm" variant="outline" className="justify-self-start" data-testid="acusar" onClick={() => acusar.mutate(a.id)} disabled={acusar.isPending}>
          Acusar recibo
        </Button>
      )}
    </li>
  );
}

export function Avisos() {
  const q = useAvisos();
  const [vista, setVista] = useState<"pendientes" | "todos">("pendientes");
  return (
    <div className="grid gap-4">
      <p className="max-w-prose text-sm text-tenue">
        Pocos avisos, y fuera del chat: solo lo que exige actuar llega al móvil, con acuse y escalado. Acusar no borra: todo queda en el historial.
        Presupuesto de avisos: como mucho uno alto por semana de media antes de revisar por qué.
      </p>
      <Tabs value={vista} onValueChange={(v) => setVista(v as typeof vista)}>
        <TabsList>
          <TabsTrigger value="pendientes">Sin acusar</TabsTrigger>
          <TabsTrigger value="todos">Historial completo</TabsTrigger>
        </TabsList>
      </Tabs>
      <ConDatos q={q}>
        {(as) => {
          const lista = vista === "pendientes" ? as.filter((a) => !a.acusadoEn) : as;
          if (!lista.length) return <p className="text-sm text-tenue">Nada sin acusar.</p>;
          return <ul className="grid gap-3">{lista.map((a) => <Tarjeta key={a.id} a={a} />)}</ul>;
        }}
      </ConDatos>
    </div>
  );
}
