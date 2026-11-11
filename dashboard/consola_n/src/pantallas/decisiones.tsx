import { useEffect, useMemo, useState } from "react";
import { Check, Clock, KeyRound, ShieldCheck, X } from "lucide-react";
import { useAprobar, useDecisiones, usePedirCodigo, useRechazar, useSalud } from "@/api/consultas";
import { importeEsperado } from "@/api/simulada";
import type { Decision } from "@/api/tipos";
import { CODIGO_DEMO, ESPERA_AUMENTO_SEG } from "@/config/prototipo";
import { ConDatos } from "@/componentes/estado_consulta";
import { Explicacion } from "@/componentes/explicacion";
import { Badge } from "@/componentes/ui/badge";
import { Button } from "@/componentes/ui/button";
import { Card, CardContent, CardHeader } from "@/componentes/ui/card";
import { Input } from "@/componentes/ui/input";
import { extraerCifras } from "@/logica/cifras";
import { eurosCent, minutosRestantes, numero } from "@/logica/formato";
import { motivoBloqueo, requisitos, SUBE_RIESGO, textoBloqueo, type TipoAccion } from "@/logica/friccion";
import { cn } from "@/lib/utils";
import { useUI } from "@/estado/tienda";

const NOMBRE_TIPO: Record<TipoAccion, string> = {
  abrir: "Abrir",
  aumentar: "Aumentar",
  reducir: "Reducir",
  cerrar: "Cerrar",
  proteger: "Proteger",
  subir_limite: "Subir un límite",
};
const NOMBRE_CARTERA = { trading: "Trading", tactica: "Táctica", largo: "Largo plazo" } as const;
const ESTADO = { pendiente: "Pendiente", aprobada: "Aprobada", rechazada: "Rechazada", caducada: "Caducó sin actuar" } as const;

function useAhora(cadaMs = 500) {
  const [t, setT] = useState(Date.now());
  useEffect(() => {
    const i = setInterval(() => setT(Date.now()), cadaMs);
    return () => clearInterval(i);
  }, [cadaMs]);
  return t;
}

function Fila({ etiqueta, valor, tono }: { etiqueta: string; valor: string; tono?: "mal" | "bien" }) {
  return (
    <div className="flex items-baseline justify-between gap-4 border-b border-dashed py-1.5 last:border-0">
      <dt className="text-sm text-tenue">{etiqueta}</dt>
      <dd className={cn("cifra text-right text-sm font-medium", tono === "mal" && "text-mal", tono === "bien" && "text-bien")}>{valor}</dd>
    </div>
  );
}

function Detalle({ d, killSwitch }: { d: Decision; killSwitch: boolean }) {
  const ahora = useAhora();
  const req = requisitos(d.tipo, ESPERA_AUMENTO_SEG);
  const pedir = usePedirCodigo();
  const aprobar = useAprobar();
  const rechazar = useRechazar();
  const [importe, setImporte] = useState("");
  const [codigo, setCodigo] = useState("");
  const [esperaHasta, setEsperaHasta] = useState<number | null>(null);
  const esperado = importeEsperado(d);
  const esLimite = d.tipo === "subir_limite";

  const cifrasPantalla = useMemo(
    () => [d.cifrasF.importe, d.cifrasF.cantidad, d.cifrasF.precioRef, d.cifrasF.stop ?? 0, d.cifrasF.perdidaMaxima, d.estresM, 2008, ...extraerCifras(d.cifrasF.motivo)],
    [d],
  );
  const restante = esperaHasta ? Math.max(0, Math.ceil((esperaHasta - ahora) / 1000)) : ESPERA_AUMENTO_SEG;
  const motivo = motivoBloqueo({
    tipo: d.tipo,
    importeEsperadoCent: Math.round(esperado * 100),
    importeTecleado: importe,
    codigo,
    codigoValido: codigo, // la pantalla no conoce el código: lo comprueba el servidor
    esperaRestanteSeg: req.segundoFactor ? (esperaHasta ? restante : Number.POSITIVE_INFINITY) : 0,
    estado: { usada: d.usada, venceEn: d.venceEn, limiteTocadoHoy: d.limiteTocadoHoy },
    ahora,
  });
  const bloqueoKill = killSwitch && SUBE_RIESGO.has(d.tipo);
  const cerrada = d.estado !== "pendiente";
  const m = minutosRestantes(d.venceEn, ahora);

  return (
    <Card data-testid={`detalle-${d.id}`}>
      <CardHeader className="gap-2">
        <div className="flex flex-wrap items-center gap-2">
          <span className="cifra text-xs text-tenue">{d.id}</span>
          <Badge variant={SUBE_RIESGO.has(d.tipo) ? "default" : "bien"}>
            {NOMBRE_TIPO[d.tipo]} · {SUBE_RIESGO.has(d.tipo) ? "sube el riesgo" : "baja el riesgo"}
          </Badge>
          <Badge variant="neutro">{NOMBRE_CARTERA[d.cartera]}</Badge>
          {!cerrada && (
            <span className={cn("cifra ml-auto flex items-center gap-1 text-xs", m < 60 ? "text-aviso" : "text-tenue")}>
              <Clock className="size-3.5" /> caduca en {m} min
            </span>
          )}
        </div>
        <h2 className="text-lg font-semibold">{d.resumen}</h2>
      </CardHeader>
      <CardContent className="grid gap-5">
        <div className="grid gap-5 md:grid-cols-2">
          <div>
            <p className="etiqueta mb-1">Cifras de F (las únicas que valen)</p>
            <dl>
              <Fila etiqueta="Resultado del control" valor={d.cifrasF.resultado === "reducido" ? "Reducido" : "Aprobado"} tono={d.cifrasF.resultado === "reducido" ? undefined : "bien"} />
              {esLimite ? (
                <>
                  <Fila etiqueta="Valor actual" valor={numero(d.cifrasF.precioRef)} />
                  <Fila etiqueta="Valor nuevo" valor={numero(d.cifrasF.cantidad)} />
                </>
              ) : (
                <>
                  <Fila etiqueta="Importe" valor={eurosCent(d.cifrasF.importe)} />
                  <Fila etiqueta="Cantidad" valor={numero(d.cifrasF.cantidad)} />
                  <Fila etiqueta="Precio de referencia" valor={numero(d.cifrasF.precioRef)} />
                  <Fila etiqueta="Stop en el intermediario" valor={d.cifrasF.stop ? numero(d.cifrasF.stop) : "—"} />
                  <Fila etiqueta="Pérdida máxima si salta el stop" valor={d.cifrasF.perdidaMaxima ? `−${eurosCent(d.cifrasF.perdidaMaxima)}` : "—"} tono="mal" />
                </>
              )}
            </dl>
            <p className="mt-2 text-xs text-tenue">{d.cifrasF.motivo}.</p>
          </div>
          <div className="grid content-start gap-4">
            {!esLimite && (
              <div>
                <p className="etiqueta mb-1">Riesgo en euros (M)</p>
                <p className="cifra text-xl font-semibold">{d.estresM < 0 ? `baja ${eurosCent(-d.estresM)}` : `−${eurosCent(d.estresM)}`}</p>
                <p className="text-xs text-tenue">en una caída como la de 2008, solo esta operación</p>
              </div>
            )}
            <div>
              <p className="etiqueta mb-1">Plan base</p>
              <p className="text-sm">{d.planBase}</p>
            </div>
          </div>
        </div>

        <Explicacion texto={d.explicacion} cifrasPantalla={cifrasPantalla} />

        {cerrada ? (
          <p data-testid="estado-cerrada" className="rounded-md bg-muted p-3 text-sm">
            <span className="font-semibold">{ESTADO[d.estado]}.</span>{" "}
            {d.estado === "caducada" ? "No se hizo nada. Si sigue haciendo falta, el robot la volverá a proponer." : "Cada aprobación vale una sola vez."}
          </p>
        ) : req.unToque ? (
          <div className="flex flex-wrap gap-2">
            <Button data-testid="reducir-ahora" onClick={() => aprobar.mutate({ id: d.id, importe: "", codigo: "" })} disabled={aprobar.isPending}>
              <Check /> {NOMBRE_TIPO[d.tipo]} ahora
            </Button>
            <Button variant="ghost" onClick={() => rechazar.mutate(d.id)}>
              <X /> No, dejarlo como está
            </Button>
            <p className="w-full text-xs text-tenue">Bajar el riesgo no pide más: un toque.</p>
          </div>
        ) : (
          <div className="grid gap-4 rounded-md border p-4" data-testid="aprobacion">
            {bloqueoKill && <p className="text-sm font-medium text-mal">Kill-switch activo: no se abren ni aumentan posiciones.</p>}
            {d.limiteTocadoHoy && (
              <p className="text-sm font-medium text-aviso" data-testid="limite-hoy">
                {textoBloqueo.limite_hoy}
              </p>
            )}
            <label className="grid gap-1.5 text-sm" htmlFor={`importe-${d.id}`}>
              {esLimite ? "Teclee el valor nuevo" : "Teclee el importe exacto, al céntimo"}
              <Input
                id={`importe-${d.id}`}
                inputMode="decimal"
                placeholder={esLimite ? numero(esperado) : eurosCent(esperado).replace(/\s?€/, "")}
                value={importe}
                onChange={(e) => setImporte(e.target.value)}
                disabled={d.limiteTocadoHoy || bloqueoKill}
                className="cifra max-w-56"
              />
            </label>
            {req.segundoFactor && (
              <div className="grid gap-2">
                {esperaHasta === null ? (
                  <Button
                    variant="outline"
                    className="justify-self-start"
                    data-testid="pedir-codigo"
                    disabled={d.limiteTocadoHoy || bloqueoKill || pedir.isPending}
                    onClick={() => pedir.mutate(d.id, { onSuccess: (r) => setEsperaHasta(new Date(r.esperaHasta).getTime()) })}
                  >
                    <KeyRound /> Pedir el código de segundo factor
                  </Button>
                ) : (
                  <>
                    <label className="grid gap-1.5 text-sm" htmlFor={`codigo-${d.id}`}>
                      Código (llega al móvil, nunca al chat)
                      <Input id={`codigo-${d.id}`} inputMode="numeric" autoComplete="one-time-code" value={codigo} onChange={(e) => setCodigo(e.target.value)} className="cifra max-w-40" />
                      <span className="text-xs text-tenue">En el prototipo, el código es {CODIGO_DEMO}.</span>
                    </label>
                    <p className="cifra text-sm" data-testid="espera">
                      {restante > 0 ? `Espera obligatoria: ${restante} s` : "Espera cumplida"}
                    </p>
                  </>
                )}
              </div>
            )}
            {motivo && importe !== "" && motivo !== "en_espera" && !d.limiteTocadoHoy && (
              <p className="text-xs text-tenue">{textoBloqueo[motivo]}</p>
            )}
            {aprobar.isError && (
              <p className="text-sm text-mal" role="alert">
                {(aprobar.error as Error).message}
              </p>
            )}
            <div className="flex flex-wrap gap-2">
              <Button
                data-testid="aprobar"
                disabled={!!motivo || bloqueoKill || aprobar.isPending}
                onClick={() => aprobar.mutate({ id: d.id, importe, codigo })}
              >
                <ShieldCheck /> Aprobar una vez
              </Button>
              <Button variant="ghost" data-testid="rechazar" onClick={() => rechazar.mutate(d.id)}>
                <X /> Rechazar
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function Decisiones() {
  const q = useDecisiones();
  const salud = useSalud();
  const { decisionSeleccionada, seleccionarDecision } = useUI();
  return (
    <ConDatos q={q}>
      {(ds) => {
        const pend = ds.filter((d) => d.estado === "pendiente").sort((a, b) => a.venceEn.localeCompare(b.venceEn));
        const hist = ds.filter((d) => d.estado !== "pendiente");
        const sel = ds.find((d) => d.id === decisionSeleccionada) ?? pend[0] ?? hist[0];
        const item = (d: Decision) => (
          <li key={d.id}>
            <button
              onClick={() => {
                seleccionarDecision(d.id);
                // En el móvil la lista va encima del detalle: se baja hasta él.
                if (window.innerWidth < 1024)
                  setTimeout(() => document.getElementById("detalle-decision")?.scrollIntoView({ behavior: "smooth", block: "start" }), 50);
              }}
              data-testid={`item-${d.id}`}
              aria-current={sel?.id === d.id ? "true" : undefined}
              className={cn(
                "grid w-full gap-1 rounded-md border p-3 text-left text-sm hover:bg-muted",
                sel?.id === d.id && "border-oro/60 bg-muted",
              )}
            >
              <span className="flex items-center gap-2">
                <span className="cifra text-xs text-tenue">{d.id}</span>
                <span className={cn("ml-auto text-[11px] font-semibold uppercase tracking-[0.08em]", SUBE_RIESGO.has(d.tipo) ? "text-oro" : "text-bien")}>
                  {SUBE_RIESGO.has(d.tipo) ? "Sube riesgo" : "Baja riesgo"}
                </span>
              </span>
              <span>{d.resumen}</span>
              {d.estado !== "pendiente" && <span className="text-xs text-tenue">{ESTADO[d.estado]}</span>}
            </button>
          </li>
        );
        return (
          <div className="grid gap-5 lg:grid-cols-[20rem_1fr]">
            <div className="grid content-start gap-4">
              <div>
                <p className="etiqueta mb-2">Pendientes, por vencimiento</p>
                {pend.length ? <ul className="grid gap-2">{pend.map(item)}</ul> : <p className="text-sm text-tenue">Nada pendiente.</p>}
              </div>
              <div>
                <p className="etiqueta mb-2">Historial</p>
                <ul className="grid gap-2">{hist.map(item)}</ul>
              </div>
            </div>
            <div id="detalle-decision" className="min-w-0 scroll-mt-[calc(var(--cabecera,80px)+12px)]">{sel && <Detalle key={sel.id} d={sel} killSwitch={salud.data?.killSwitch ?? false} />}</div>
          </div>
        );
      }}
    </ConDatos>
  );
}
