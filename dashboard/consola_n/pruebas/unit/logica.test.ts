import { describe, expect, it } from "vitest";
import { veredictoRango } from "@/logica/veredicto";
import { importeACentimos, motivoBloqueo, requisitos, type Comprobar } from "@/logica/friccion";
import { cifrasAjenas, explicacionValida, extraerCifras } from "@/logica/cifras";
import { colorPanel, type Comprobacion } from "@/logica/semaforo";
import { euros, eurosCent } from "@/logica/formato";

describe("veredicto de la cifra principal (CA-3)", () => {
  it("rango que cruza el cero: todavía no se sabe", () => {
    expect(veredictoRango(-310, 590)).toBe("no_se_sabe");
    expect(veredictoRango(0, 10)).toBe("no_se_sabe");
    expect(veredictoRango(-10, 0)).toBe("no_se_sabe");
  });
  it("rango entero por encima o por debajo", () => {
    expect(veredictoRango(5, 90)).toBe("aporta");
    expect(veredictoRango(-20, -8)).toBe("resta");
  });
  it("datos imposibles: no se sabe (falla cerrado)", () => {
    expect(veredictoRango(NaN, 5)).toBe("no_se_sabe");
    expect(veredictoRango(10, 5)).toBe("no_se_sabe");
  });
});

describe("importe tecleado al céntimo (CA-4)", () => {
  it("formatos españoles válidos", () => {
    expect(importeACentimos("1.500,00")).toBe(150000);
    expect(importeACentimos("1500,00")).toBe(150000);
    expect(importeACentimos("1500")).toBe(150000);
    expect(importeACentimos("927,85 €")).toBe(92785);
    expect(importeACentimos("927,8")).toBe(92780);
  });
  it("formatos ambiguos o mal escritos: no valen", () => {
    expect(importeACentimos("12.50")).toBeNull();
    expect(importeACentimos("1,500.00")).toBeNull();
    expect(importeACentimos("1.50,00")).toBeNull();
    expect(importeACentimos("abc")).toBeNull();
    expect(importeACentimos("")).toBeNull();
    expect(importeACentimos("1,234")).toBeNull();
  });
});

describe("fricción asimétrica (CA-4, CA-5)", () => {
  const futuro = new Date(Date.now() + 3_600_000).toISOString();
  const base: Comprobar = {
    tipo: "abrir",
    importeEsperadoCent: 150000,
    importeTecleado: "1.500,00",
    codigo: "",
    codigoValido: "482913",
    esperaRestanteSeg: 0,
    estado: { usada: false, venceEn: futuro, limiteTocadoHoy: false },
  };
  it("reducir, cerrar y proteger: un toque, sin importe ni código", () => {
    for (const tipo of ["reducir", "cerrar", "proteger"] as const) {
      expect(requisitos(tipo, 8)).toEqual({ unToque: true, importeTecleado: false, segundoFactor: false, esperaSeg: 0 });
      expect(motivoBloqueo({ ...base, tipo, importeTecleado: "" })).toBeNull();
    }
  });
  it("reducir no se bloquea aunque se haya tocado un límite hoy", () => {
    expect(motivoBloqueo({ ...base, tipo: "reducir", importeTecleado: "", estado: { ...base.estado, limiteTocadoHoy: true } })).toBeNull();
  });
  it("abrir: importe exacto, sin segundo factor", () => {
    expect(motivoBloqueo(base)).toBeNull();
    expect(motivoBloqueo({ ...base, importeTecleado: "1.500,01" })).toBe("importe_distinto");
    expect(motivoBloqueo({ ...base, importeTecleado: "1500" })).toBeNull();
  });
  it("aumentar: importe, código correcto y espera cumplida", () => {
    const a: Comprobar = { ...base, tipo: "aumentar" };
    expect(motivoBloqueo(a)).toBe("falta_codigo");
    expect(motivoBloqueo({ ...a, codigo: "111111" })).toBe("codigo_erroneo");
    expect(motivoBloqueo({ ...a, codigo: "482913", esperaRestanteSeg: 3 })).toBe("en_espera");
    expect(motivoBloqueo({ ...a, codigo: "482913" })).toBeNull();
  });
  it("aumentar o subir un límite nunca el día en que se tocó un límite", () => {
    const e = { ...base.estado, limiteTocadoHoy: true };
    expect(motivoBloqueo({ ...base, tipo: "aumentar", codigo: "482913", estado: e })).toBe("limite_hoy");
    expect(motivoBloqueo({ ...base, tipo: "subir_limite", codigo: "482913", estado: e })).toBe("limite_hoy");
  });
  it("una aprobación vale una vez y caduca sin actuar", () => {
    expect(motivoBloqueo({ ...base, estado: { ...base.estado, usada: true } })).toBe("usada");
    expect(motivoBloqueo({ ...base, estado: { ...base.estado, venceEn: new Date(Date.now() - 1000).toISOString() } })).toBe("caducada");
    expect(motivoBloqueo({ ...base, tipo: "reducir", estado: { ...base.estado, usada: true } })).toBe("usada");
  });
});

describe("explicación del Broker sin cifras inventadas (CA-6)", () => {
  const pantalla = [1500, 1.079, 11.7, 61, 2008];
  it("extrae cifras en formato español", () => {
    expect(extraerCifras("1.500,00 € y 1,079 con 11,70 € y −310 en 2008")).toEqual([1500, 1.079, 11.7, -310, 2008]);
    expect(extraerCifras("un 2,5 % de 90")).toEqual([2.5, 90]);
  });
  it("todas las cifras en pantalla: se muestra", () => {
    expect(explicacionValida("Se abren 1.500,00 € con el stop en 1,079. Pierde como mucho 11,70 €; en 2008, 61 €.", pantalla)).toBe(true);
  });
  it("una cifra que no está en pantalla: se retira", () => {
    const t = "El yen suele subir un 3,4 % en semanas como esta; se abren 1.500,00 €.";
    expect(explicacionValida(t, pantalla)).toBe(false);
    expect(cifrasAjenas(t, pantalla)).toEqual([3.4]);
  });
  it("acepta el valor absoluto de una cifra negativa en pantalla", () => {
    expect(explicacionValida("La pérdida sería de 310 €.", [-310])).toBe(true);
  });
  it("un texto sin cifras se muestra", () => {
    expect(explicacionValida("Conviene esperar al cierre.", [])).toBe(true);
  });
});

describe("semáforo del panel (CA-8)", () => {
  const c = (estado: Comprobacion["estado"]): Comprobacion => ({ id: "datos", nombre: "x", estado, detalle: "" });
  it("verde solo si las cinco están en verde", () => {
    expect(colorPanel([c("verde"), c("verde"), c("verde"), c("verde"), c("verde")])).toBe("verde");
    expect(colorPanel([c("verde"), c("ambar"), c("verde"), c("verde"), c("verde")])).toBe("ambar");
  });
  it("rojo si una no se puede calcular, si faltan o si no hay datos", () => {
    expect(colorPanel([c("verde"), c("sin_dato"), c("verde"), c("verde"), c("verde")])).toBe("rojo");
    expect(colorPanel([c("verde"), c("verde")])).toBe("rojo");
    expect(colorPanel(undefined)).toBe("rojo");
    expect(colorPanel([])).toBe("rojo");
  });
});

describe("formato español", () => {
  it("separa los miles también con cuatro cifras", () => {
    expect(euros(1500).replace(/\s/g, " ")).toBe("1.500 €");
    expect(eurosCent(1500).replace(/\s/g, " ")).toBe("1.500,00 €");
    expect(eurosCent(927.85).replace(/\s/g, " ")).toBe("927,85 €");
    expect(euros(16195).replace(/\s/g, " ")).toBe("16.195 €");
  });
});
