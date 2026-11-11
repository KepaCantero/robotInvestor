import { useState } from "react";
import { useInformes } from "@/api/consultas";
import { ConDatos } from "@/componentes/estado_consulta";
import { GraficoComparado } from "@/componentes/grafico";
import { Badge } from "@/componentes/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/componentes/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/componentes/ui/tabs";
import { eurosCent, eurosConSigno, numero } from "@/logica/formato";
import { veredictoRango } from "@/logica/veredicto";

const VEREDICTO = {
  aporta: { t: "Aporta", v: "bien" },
  resta: { t: "Resta", v: "mal" },
  no_se_sabe: { t: "Todavía no se sabe", v: "neutro" },
} as const;

export function InformesVista() {
  const q = useInformes();
  const [hechas, setHechas] = useState<Record<number, boolean>>({});
  return (
    <ConDatos q={q}>
      {(inf) => {
        const max = inf.semanal.embudo[0]?.cantidad ?? 1;
        const total = inf.mensual.atribucion.reduce((s, a) => s + a.euros, 0);
        return (
          <Tabs defaultValue="semanal">
            <TabsList>
              <TabsTrigger value="semanal">Semanal</TabsTrigger>
              <TabsTrigger value="mensual">Mensual</TabsTrigger>
              <TabsTrigger value="anual">Anual</TabsTrigger>
            </TabsList>

            <TabsContent value="semanal" className="grid gap-5">
              <p className="text-sm text-tenue">{inf.semanal.semana}</p>
              <div className="grid gap-5 sm:grid-cols-3">
                {[
                  ["Análisis a fondo", numero(inf.semanal.analisis)],
                  ["Órdenes enviadas", numero(inf.semanal.ordenes)],
                  ["Costes de la semana", eurosCent(inf.semanal.costeIA + inf.semanal.costeIntermediario)],
                ].map(([e, v]) => (
                  <Card key={e}>
                    <CardHeader>
                      <CardTitle>{e}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="cifra text-3xl font-semibold">{v}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
              <Card>
                <CardHeader>
                  <CardTitle>Embudo de abstención</CardTitle>
                  <p className="text-sm text-tenue">Dónde decide el robot no hacer nada. Abstenerse también es una decisión, y suele ser la buena.</p>
                </CardHeader>
                <CardContent>
                  <ol className="grid gap-2" data-testid="embudo">
                    {inf.semanal.embudo.map((e) => (
                      <li key={e.etapa} className="grid grid-cols-[minmax(0,13rem)_1fr_3rem] items-center gap-3 text-sm">
                        <span className="min-w-0">{e.etapa}</span>
                        <span className="h-3 rounded-sm bg-muted">
                          <span className="block h-full rounded-sm bg-oro" style={{ width: `${Math.max(2, (e.cantidad / max) * 100)}%` }} />
                        </span>
                        <span className="cifra text-right">{numero(e.cantidad)}</span>
                      </li>
                    ))}
                  </ol>
                  <p className="mt-3 text-xs text-tenue">
                    IA: {eurosCent(inf.semanal.costeIA)} · intermediario: {eurosCent(inf.semanal.costeIntermediario)} · {inf.semanal.abstenciones} señales con
                    ventaja que no se ejecutaron.
                  </p>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="mensual" className="grid gap-5">
              <Card>
                <CardHeader>
                  <CardTitle>El robot frente a la cartera sombra · {inf.mensual.mes}</CardTitle>
                  <p className="text-sm text-tenue">Valor total en euros. La sombra es la cartera pasiva de referencia: lo que tendría sin hacer nada.</p>
                </CardHeader>
                <CardContent>
                  <GraficoComparado robot={inf.mensual.robot} sombra={inf.mensual.sombra} />
                  <div className="mt-2 flex gap-4 text-xs text-tenue">
                    <span className="flex items-center gap-1.5">
                      <span className="inline-block h-0.5 w-5 bg-oro" /> Robot
                    </span>
                    <span className="flex items-center gap-1.5">
                      <span className="inline-block h-0.5 w-5 border-t-2 border-dashed border-tenue" /> Sombra
                    </span>
                  </div>
                </CardContent>
              </Card>
              <div className="grid gap-5 lg:grid-cols-2">
                <Card>
                  <CardHeader>
                    <CardTitle>Atribución por etapa (I)</CardTitle>
                  </CardHeader>
                  <CardContent className="overflow-x-auto">
                    <table className="w-full text-sm" data-testid="atribucion">
                      <thead>
                        <tr className="text-left">
                          <th className="etiqueta pb-2 font-semibold">Etapa</th>
                          <th className="etiqueta pb-2 text-right font-semibold">Euros</th>
                          <th className="etiqueta pb-2 text-right font-semibold">Rango del 90 %</th>
                          <th className="etiqueta pb-2 text-right font-semibold">Veredicto</th>
                        </tr>
                      </thead>
                      <tbody>
                        {inf.mensual.atribucion.map((a) => {
                          const v = VEREDICTO[veredictoRango(a.rangoMin, a.rangoMax)];
                          return (
                            <tr key={a.etapa} className="border-t border-dashed">
                              <td className="py-2 pr-2">{a.etapa}</td>
                              <td className="cifra py-2 text-right">{eurosConSigno(a.euros)}</td>
                              <td className="cifra whitespace-nowrap py-2 text-right text-tenue">
                                {eurosConSigno(a.rangoMin)} a {eurosConSigno(a.rangoMax)}
                              </td>
                              <td className="py-2 text-right">
                                <Badge variant={v.v}>{v.t}</Badge>
                              </td>
                            </tr>
                          );
                        })}
                        <tr className="border-t">
                          <td className="py-2 font-semibold">Total del mes</td>
                          <td className="cifra py-2 text-right font-semibold">{eurosConSigno(total)}</td>
                          <td colSpan={2} />
                        </tr>
                      </tbody>
                    </table>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Sus intervenciones</CardTitle>
                    <p className="text-sm text-tenue">Frente a lo que habría hecho el robot. Es información para usted, no un reproche.</p>
                  </CardHeader>
                  <CardContent>
                    <ul className="grid gap-2">
                      {inf.mensual.intervenciones.map((i) => (
                        <li key={i.descripcion} className="flex items-baseline justify-between gap-4 border-b border-dashed pb-2 text-sm last:border-0">
                          <span>{i.descripcion}</span>
                          <span className="cifra shrink-0">{eurosConSigno(i.euros)}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="anual">
              <Card>
                <CardHeader>
                  <CardTitle>Revisión guiada del año</CardTitle>
                  <p className="text-sm text-tenue">Una vez al año, con calma. Lo que cambie pasa por el Broker y por la fricción de la configuración.</p>
                </CardHeader>
                <CardContent>
                  <ul className="grid gap-2">
                    {inf.anual.map((p, i) => (
                      <li key={p.pregunta}>
                        <label className="flex items-start gap-3 text-sm" htmlFor={`anual-${i}`}>
                          <input
                            id={`anual-${i}`}
                            type="checkbox"
                            className="mt-0.5 size-4 accent-[rgb(var(--oro))]"
                            checked={hechas[i] ?? p.hecho}
                            onChange={(e) => setHechas((h) => ({ ...h, [i]: e.target.checked }))}
                          />
                          {p.pregunta}
                        </label>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        );
      }}
    </ConDatos>
  );
}
