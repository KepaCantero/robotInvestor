import { describe, expect, it } from "vitest";
import { ApiSimulada } from "@/api/simulada";
import { CODIGO_DEMO, ESPERA_AUMENTO_SEG } from "@/config/prototipo";

function api() {
  let t = Date.parse("2026-11-11T10:00:00Z");
  const a = new ApiSimulada({ ahora: () => t, latenciaMs: 0 });
  return { a, avanzar: (seg: number) => (t += seg * 1000) };
}

describe("API simulada: el servidor vuelve a comprobarlo todo", () => {
  it("aprobar con el importe exacto funciona una sola vez", async () => {
    const { a } = api();
    await expect(a.aprobar("D-0147", "1.500,01", "")).rejects.toThrow(/importe exacto/);
    const d = await a.aprobar("D-0147", "1.500,00", "");
    expect(d.estado).toBe("aprobada");
    await expect(a.aprobar("D-0147", "1.500,00", "")).rejects.toThrow(/una sola vez/);
  });

  it("aumentar exige código y espera cumplida", async () => {
    const { a, avanzar } = api();
    await expect(a.aprobar("D-0148", "927,85", CODIGO_DEMO)).rejects.toThrow(/cuenta atrás/);
    await a.pedirCodigo("D-0148");
    await expect(a.aprobar("D-0148", "927,85", "000000")).rejects.toThrow(/código/);
    await expect(a.aprobar("D-0148", "927,85", CODIGO_DEMO)).rejects.toThrow(/cuenta atrás/);
    avanzar(ESPERA_AUMENTO_SEG);
    expect((await a.aprobar("D-0148", "927,85", CODIGO_DEMO)).estado).toBe("aprobada");
  });

  it("aumentar el día en que se tocó un límite se rechaza", async () => {
    const { a, avanzar } = api();
    await a.pedirCodigo("D-0149");
    avanzar(ESPERA_AUMENTO_SEG);
    await expect(a.aprobar("D-0149", "600,00", CODIGO_DEMO)).rejects.toThrow(/hasta mañana/);
  });

  it("una decisión caduca sin actuar", async () => {
    const { a, avanzar } = api();
    avanzar(46 * 60);
    const ds = await a.decisiones();
    expect(ds.find((d) => d.id === "D-0147")?.estado).toBe("caducada");
    await expect(a.aprobar("D-0147", "1.500,00", "")).rejects.toThrow(/caducó/);
  });

  it("reducir es un toque y baja la posición", async () => {
    const { a } = api();
    await a.aprobar("D-0150", "", "");
    const p = (await a.posiciones()).find((x) => x.instrumento === "ETF oro físico");
    expect(p?.cantidad).toBe(10);
  });

  it("con el kill-switch activo no se abre ni aumenta, pero se puede reducir", async () => {
    const { a } = api();
    await a.activarKillSwitch();
    await expect(a.aprobar("D-0147", "1.500,00", "")).rejects.toThrow(/Kill-switch/);
    expect((await a.aprobar("D-0150", "", "")).estado).toBe("aprobada");
    await expect(a.desactivarKillSwitch("1")).rejects.toThrow(/código/);
    expect((await a.desactivarKillSwitch(CODIGO_DEMO)).killSwitch).toBe(false);
  });

  it("vender más de lo que se tiene se veta (abriría riesgo)", async () => {
    const { a } = api();
    await expect(a.vender("P-04", 21)).rejects.toThrow(/más de lo que se tiene/);
    expect((await a.vender("P-04", 20)).cantidad).toBe(0);
  });

  it("acusar un aviso no lo borra (CA-7)", async () => {
    const { a } = api();
    const antes = (await a.avisos()).length;
    await a.acusar("AV-31");
    const despues = await a.avisos();
    expect(despues.length).toBe(antes);
    expect(despues.find((x) => x.id === "AV-31")?.acusadoEn).not.toBeNull();
  });

  it("bajar un límite se aplica; subirlo crea una decisión pendiente", async () => {
    const { a } = api();
    expect(await a.proponerParametro("peso_max", 25)).toEqual({ aplicado: true });
    const r = await a.proponerParametro("peso_max", 40);
    expect(r.aplicado).toBe(false);
    const d = (await a.decisiones()).find((x) => x.id === r.decisionId);
    expect(d?.tipo).toBe("subir_limite");
    expect(d?.estado).toBe("pendiente");
  });

  it("si la API falla, todas las llamadas fallan (CA-8)", async () => {
    const { a } = api();
    a.fallo = true;
    await expect(a.comprobaciones()).rejects.toThrow(/no responde/);
    await expect(a.cifraPrincipal()).rejects.toThrow(/no responde/);
  });
});
