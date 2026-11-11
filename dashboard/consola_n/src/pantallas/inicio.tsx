import { ArrowRight, Clock } from "lucide-react";
import { useAvisos, useCarteras, useCifra, useComprobaciones, useDecisiones } from "@/api/consultas";
import { ConDatos } from "@/componentes/estado_consulta";
import { CifraPrincipalVista } from "@/componentes/cifra_principal";
import { ListaComprobaciones } from "@/componentes/semaforo";
import { Badge } from "@/componentes/ui/badge";
import { Button } from "@/componentes/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/componentes/ui/card";
import { euros, eurosConSigno, minutosRestantes } from "@/logica/formato";
import { SUBE_RIESGO } from "@/logica/friccion";
import { useUI } from "@/estado/tienda";

export function Inicio() {
  const cifra = useCifra();
  const comprobaciones = useComprobaciones();
  const decisiones = useDecisiones();
  const carteras = useCarteras();
  const avisos = useAvisos();
  const { ir, seleccionarDecision, fijarCartera } = useUI();

  return (
    <div className="grid gap-5">
      <Card className="border-oro/40">
        <CardHeader>
          <CardTitle>La cifra principal</CardTitle>
        </CardHeader>
        <CardContent className="pb-8">
          <ConDatos q={cifra}>{(c) => <CifraPrincipalVista c={c} />}</ConDatos>
        </CardContent>
      </Card>

      <div className="grid gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Qué espera de usted</CardTitle>
          </CardHeader>
          <CardContent>
            <ConDatos q={decisiones}>
              {(ds) => {
                const pend = ds.filter((d) => d.estado === "pendiente").sort((a, b) => a.venceEn.localeCompare(b.venceEn));
                if (!pend.length) return <p className="text-sm text-tenue">Nada pendiente. No hace falta mirar más.</p>;
                return (
                  <ul className="grid gap-2">
                    {pend.map((d) => {
                      const m = minutosRestantes(d.venceEn);
                      return (
                        <li key={d.id}>
                          <button
                            onClick={() => {
                              seleccionarDecision(d.id);
                              ir("decisiones");
                            }}
                            className="flex w-full items-center gap-3 rounded-md border p-3 text-left hover:bg-muted"
                          >
                            <span className="cifra text-xs text-tenue">{d.id}</span>
                            <span className="min-w-0 flex-1 text-sm">{d.resumen}</span>
                            <Badge variant={SUBE_RIESGO.has(d.tipo) ? "default" : "bien"}>{SUBE_RIESGO.has(d.tipo) ? "Sube riesgo" : "Baja riesgo"}</Badge>
                            <span className={`cifra flex items-center gap-1 text-xs ${m < 60 ? "text-aviso" : "text-tenue"}`}>
                              <Clock className="size-3.5" /> {m} min
                            </span>
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                );
              }}
            </ConDatos>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Cinco comprobaciones</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-3">
            <ConDatos q={comprobaciones}>{(cs) => <ListaComprobaciones comprobaciones={cs} />}</ConDatos>
            <ConDatos q={avisos}>
              {(as) => {
                const n = as.filter((a) => !a.acusadoEn && a.prioridad !== "info").length;
                return n ? (
                  <Button variant="outline" size="sm" className="justify-self-start" onClick={() => ir("avisos")}>
                    {n} {n === 1 ? "aviso" : "avisos"} sin acusar <ArrowRight />
                  </Button>
                ) : null;
              }}
            </ConDatos>
          </CardContent>
        </Card>
      </div>

      <ConDatos q={carteras}>
        {(cs) => (
          <div className="grid gap-5 md:grid-cols-3">
            {cs.map((c) => (
              <Card key={c.id}>
                <CardHeader>
                  <CardTitle>{c.nombre}</CardTitle>
                  <p className="text-xs text-tenue">Mirarla: {c.ritmo.toLowerCase()}</p>
                </CardHeader>
                <CardContent className="grid gap-2">
                  <p className="cifra text-2xl font-semibold">{euros(c.valor)}</p>
                  {c.plan ? (
                    <div className="grid gap-1.5" data-testid="plan-largo">
                      <div className="h-1.5 w-full rounded-sm bg-muted">
                        <div className="h-full rounded-sm bg-oro" style={{ width: `${(c.plan.anosHechos / c.plan.anosTotales) * 100}%` }} />
                      </div>
                      <p className="text-sm">
                        <span className="font-medium text-bien">{c.plan.enCamino ? "En camino" : "Fuera del plan"}</span> · año {c.plan.anosHechos} de{" "}
                        {c.plan.anosTotales} hacia «{c.plan.objetivo}»
                      </p>
                      <p className="text-xs text-tenue">{c.plan.nota} Sin cifra diaria: se mira en su horizonte.</p>
                    </div>
                  ) : (
                    <p className="text-sm">
                      <span className={`cifra ${c.resultadoPeriodo < 0 ? "text-mal" : "text-bien"}`}>{eurosConSigno(c.resultadoPeriodo)}</span>{" "}
                      <span className="text-tenue">· {c.periodo.toLowerCase()}</span>
                    </p>
                  )}
                  <Button
                    variant="link"
                    className="h-auto justify-self-start p-0"
                    onClick={() => {
                      fijarCartera(c.id);
                      ir("carteras");
                    }}
                  >
                    Ver posiciones <ArrowRight />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </ConDatos>
    </div>
  );
}
