import { useEffect, useRef } from "react";
import { Bell, FileBarChart2, Gauge, HeartPulse, House, ListChecks, Settings2, Wallet } from "lucide-react";
import { useAvisos, useComprobaciones, useDecisiones, useSalud } from "@/api/consultas";
import { BotonKillSwitch } from "@/componentes/kill_switch";
import { PastillaSemaforo } from "@/componentes/semaforo";
import { cn } from "@/lib/utils";
import { pantallaDeHash, useUI, type Pantalla } from "@/estado/tienda";
import { Inicio } from "@/pantallas/inicio";
import { Decisiones } from "@/pantallas/decisiones";
import { Carteras } from "@/pantallas/carteras";
import { Avisos } from "@/pantallas/avisos";
import { InformesVista } from "@/pantallas/informes";
import { SaludVista } from "@/pantallas/salud";
import { Configuracion } from "@/pantallas/configuracion";

const MENU: { id: Pantalla; nombre: string; pregunta: string; icono: typeof House }[] = [
  { id: "inicio", nombre: "Inicio", pregunta: "¿Va todo bien y qué espera de mí?", icono: House },
  { id: "decisiones", nombre: "Decisiones", pregunta: "¿Qué apruebo?", icono: ListChecks },
  { id: "carteras", nombre: "Carteras", pregunta: "¿Qué tengo?", icono: Wallet },
  { id: "avisos", nombre: "Avisos", pregunta: "¿Qué no he visto?", icono: Bell },
  { id: "informes", nombre: "Informes", pregunta: "¿Aporta el robot?", icono: FileBarChart2 },
  { id: "salud", nombre: "Salud", pregunta: "¿Funciona el robot?", icono: HeartPulse },
  { id: "configuracion", nombre: "Configuración", pregunta: "¿Cambio algo?", icono: Settings2 },
];

function Contador({ n, tono }: { n: number; tono: "oro" | "mal" }) {
  if (!n) return null;
  return (
    <span
      className={cn(
        "cifra ml-auto min-w-5 rounded-sm px-1 text-center text-[11px] font-semibold",
        tono === "mal" ? "bg-mal text-[rgb(var(--sobre-oro))]" : "bg-oro text-primary-foreground",
      )}
    >
      {n}
    </span>
  );
}

export function App() {
  const { pantalla, ir, fijarPantalla } = useUI();
  const comprobaciones = useComprobaciones();
  const decisiones = useDecisiones();
  const avisos = useAvisos();
  const salud = useSalud();

  useEffect(() => {
    const alCambiar = () => fijarPantalla(pantallaDeHash(window.location.hash));
    window.addEventListener("hashchange", alCambiar);
    return () => window.removeEventListener("hashchange", alCambiar);
  }, [fijarPantalla]);

  useEffect(() => {
    window.scrollTo({ top: 0 });
  }, [pantalla]);

  // Alto real de la barra superior, para que el menú lateral quede pegado debajo (cambia con la banda del kill-switch).
  const cabecera = useRef<HTMLElement>(null);
  useEffect(() => {
    const el = cabecera.current;
    if (!el) return;
    const ro = new ResizeObserver(() => document.documentElement.style.setProperty("--cabecera", `${el.offsetHeight}px`));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const pendientes = decisiones.data?.filter((d) => d.estado === "pendiente").length ?? 0;
  const sinAcuse = avisos.data?.filter((a) => !a.acusadoEn && a.prioridad !== "info").length ?? 0;
  const actual = MENU.find((m) => m.id === pantalla)!;

  return (
    <div className="flex min-h-full flex-col">
      <header ref={cabecera} className="sticky top-[env(safe-area-inset-top,0px)] z-40 border-b bg-card">
        <div className="canal flex items-center gap-3 py-2.5">
          <span className="rotulo-led shrink-0 rounded-sm px-2 py-1 text-[11px] sm:text-xs">Consola N</span>
          <span className="hidden text-xs text-tenue md:inline">Robot Investor · consola del operador</span>
          <div className="ml-auto flex items-center gap-2">
            <PastillaSemaforo comprobaciones={comprobaciones.isError ? undefined : comprobaciones.data} />
            <BotonKillSwitch />
          </div>
        </div>
        <div className="canal flex flex-wrap items-center gap-x-3 gap-y-1 border-t border-dashed border-oro/40 bg-oro/10 py-1 text-[11px] font-semibold uppercase tracking-[0.1em] text-oro">
          <span>Prototipo · datos de ejemplo</span>
          <span className="font-normal normal-case tracking-normal text-tenue">
            No está conectado al robot. Ninguna cifra es suya ni es una recomendación.
          </span>
        </div>
        {salud.data?.killSwitch && (
          <div role="status" data-testid="banda-kill" className="canal border-t border-mal/50 bg-mal/15 py-1.5 text-xs font-medium text-mal">
            Kill-switch activo: el robot no abre ni aumenta posiciones. No vende nada por su cuenta; los stops siguen en el intermediario.
          </div>
        )}
      </header>

      <div className="flex flex-1">
        <nav aria-label="Pantallas" className="sticky top-[calc(var(--cabecera,80px)+env(safe-area-inset-top,0px))] hidden h-[calc(100vh-var(--cabecera,80px)-env(safe-area-inset-top,0px))] w-60 self-start shrink-0 flex-col gap-1 border-r bg-card p-3 lg:flex">
          {MENU.map((m) => (
            <button
              key={m.id}
              onClick={() => ir(m.id)}
              aria-current={pantalla === m.id ? "page" : undefined}
              data-testid={`menu-${m.id}`}
              className={cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-left text-sm transition-colors",
                pantalla === m.id ? "bg-muted font-semibold text-foreground shadow-[inset_2px_0_0_rgb(var(--oro))]" : "text-tenue hover:bg-muted/60 hover:text-foreground",
              )}
            >
              <m.icono className="size-4 shrink-0" />
              <span>{m.nombre}</span>
              {m.id === "decisiones" && <Contador n={pendientes} tono="oro" />}
              {m.id === "avisos" && <Contador n={sinAcuse} tono="mal" />}
            </button>
          ))}
          <div className="mt-auto flex items-center gap-2 rounded-md border border-dashed p-3 text-xs text-tenue">
            <Gauge className="size-4 shrink-0 text-oro" />
            N gasta cero tokens: es código, sin IA.
          </div>
        </nav>

        <main className="canal min-w-0 flex-1 pb-24 pt-5 lg:pb-10">
          <div className="mx-auto grid max-w-6xl gap-5">
            <div>
              <h1 className="text-2xl font-semibold">{actual.nombre}</h1>
              <p className="text-sm text-tenue">{actual.pregunta}</p>
            </div>
            {pantalla === "inicio" && <Inicio />}
            {pantalla === "decisiones" && <Decisiones />}
            {pantalla === "carteras" && <Carteras />}
            {pantalla === "avisos" && <Avisos />}
            {pantalla === "informes" && <InformesVista />}
            {pantalla === "salud" && <SaludVista />}
            {pantalla === "configuracion" && <Configuracion />}
          </div>
        </main>
      </div>

      <nav
        aria-label="Pantallas"
        className="fixed inset-x-0 bottom-0 z-40 grid grid-cols-7 border-t bg-card pb-[env(safe-area-inset-bottom,0px)] lg:hidden"
      >
        {MENU.map((m) => (
          <button
            key={m.id}
            onClick={() => ir(m.id)}
            aria-current={pantalla === m.id ? "page" : undefined}
            aria-label={m.nombre}
            data-testid={`menu-movil-${m.id}`}
            className={cn("relative flex flex-col items-center gap-0.5 py-2 text-[10px]", pantalla === m.id ? "text-oro" : "text-tenue")}
          >
            <m.icono className="size-5" />
            <span className="max-w-full truncate px-0.5">{m.nombre === "Configuración" ? "Ajustes" : m.nombre}</span>
            {m.id === "decisiones" && pendientes > 0 && <span className="absolute right-2 top-1.5 size-2 rounded-full bg-oro" />}
            {m.id === "avisos" && sinAcuse > 0 && <span className="absolute right-2 top-1.5 size-2 rounded-full bg-mal" />}
          </button>
        ))}
      </nav>
    </div>
  );
}
