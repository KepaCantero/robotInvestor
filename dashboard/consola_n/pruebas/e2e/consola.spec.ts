import { expect, test, type Page } from "@playwright/test";

const PANTALLAS = ["inicio", "decisiones", "carteras", "avisos", "informes", "salud", "configuracion"];

// Las fuentes de Google no se pueden descargar en el entorno de pruebas; el resto de errores sí cuentan.
function vigilarErrores(page: Page) {
  const errores: string[] = [];
  page.on("pageerror", (e) => errores.push(e.message));
  page.on("console", (m) => {
    if (m.type() === "error" && !/Failed to load resource/.test(m.text())) errores.push(m.text());
  });
  return errores;
}

test("CA-2: las siete pantallas se abren por el menú y por su enlace, sin errores", async ({ page }) => {
  const errores = vigilarErrores(page);
  await page.goto("/");
  for (const p of PANTALLAS) {
    await page.getByTestId(`menu-${p}`).click();
    await expect(page).toHaveURL(new RegExp(`#${p}$`));
    await expect(page.locator("main h1")).toBeVisible();
  }
  for (const p of PANTALLAS) {
    await page.goto(`/#${p}`);
    await expect(page.getByTestId(`menu-${p}`)).toHaveAttribute("aria-current", "page");
  }
  expect(errores).toEqual([]);
});

test("CA-3: la cifra principal dice que todavía no se sabe", async ({ page }) => {
  await page.goto("/#inicio");
  const c = page.getByTestId("cifra-principal");
  await expect(c).toHaveAttribute("data-veredicto", "no_se_sabe");
  await expect(c).toContainText("Todavía no se puede saber si el robot aporta");
  await expect(page.getByTestId("plan-largo")).toContainText("Sin cifra diaria");
});

test("CA-4: abrir pide el importe exacto y vale una sola vez", async ({ page }) => {
  await page.goto("/#decisiones");
  await page.getByTestId("item-D-0147").click();
  const d = page.getByTestId("detalle-D-0147");
  await expect(d.getByTestId("aprobar")).toBeDisabled();
  await d.getByLabel("Teclee el importe exacto, al céntimo").fill("1.500,01");
  await expect(d.getByTestId("aprobar")).toBeDisabled();
  await d.getByLabel("Teclee el importe exacto, al céntimo").fill("1.500,00");
  await d.getByTestId("aprobar").click();
  await expect(d.getByTestId("estado-cerrada")).toContainText("Cada aprobación vale una sola vez");
});

test("CA-4: aumentar pide además código y espera", async ({ page }) => {
  await page.goto("/#decisiones");
  await page.getByTestId("item-D-0148").click();
  const d = page.getByTestId("detalle-D-0148");
  await d.getByLabel("Teclee el importe exacto, al céntimo").fill("927,85");
  await expect(d.getByTestId("aprobar")).toBeDisabled();
  await d.getByTestId("pedir-codigo").click();
  await d.getByLabel(/Código/).fill("482913");
  await expect(d.getByTestId("espera")).toContainText("Espera obligatoria");
  await expect(d.getByTestId("aprobar")).toBeDisabled();
  await expect(d.getByTestId("espera")).toContainText("Espera cumplida", { timeout: 15_000 });
  await d.getByTestId("aprobar").click();
  await expect(d.getByTestId("estado-cerrada")).toBeVisible();
});

test("CA-4 y CA-6: aumentar el día de un límite está bloqueado y la explicación inventada se retira", async ({ page }) => {
  await page.goto("/#decisiones");
  await page.getByTestId("item-D-0149").click();
  const d = page.getByTestId("detalle-D-0149");
  await expect(d.getByTestId("limite-hoy")).toBeVisible();
  await expect(d.getByTestId("aprobar")).toBeDisabled();
  await expect(d.getByTestId("explicacion-retirada")).toContainText("3,4");
  await page.getByTestId("item-D-0147").click();
  await expect(page.getByTestId("explicacion")).toBeVisible();
});

test("CA-5: reducir es un toque y el kill-switch también", async ({ page }) => {
  await page.goto("/#decisiones");
  await page.getByTestId("item-D-0150").click();
  await page.getByTestId("reducir-ahora").click();
  await expect(page.getByTestId("detalle-D-0150").getByTestId("estado-cerrada")).toContainText("Aprobada");
  await page.getByTestId("kill-switch").click();
  await expect(page.getByTestId("banda-kill")).toBeVisible();
  await page.getByTestId("item-D-0147").click();
  await expect(page.getByTestId("detalle-D-0147")).toContainText("Kill-switch activo");
  await page.getByTestId("reactivar").click();
  await page.getByLabel("Código de segundo factor").fill("482913");
  await page.getByRole("button", { name: "Reactivar", exact: true }).click();
  await expect(page.getByTestId("banda-kill")).toBeHidden();
});

test("CA-5: vender en caída el largo plazo muestra antes la caída aceptada y deja vender", async ({ page }) => {
  await page.goto("/#carteras");
  await page.getByRole("tab", { name: "Largo plazo" }).click();
  await page.getByTestId("tabla-posiciones").getByText("Fondo indexado mundial").click();
  await page.getByTestId("vender").click();
  const ap = page.getByTestId("antipanico");
  await expect(ap).toContainText("Caída que aceptó por escrito");
  await expect(ap).toContainText("−35 %");
  await expect(ap).toContainText("−9,8 %");
  await expect(ap).toContainText("plan base");
  await ap.getByTestId("vender-igualmente").click();
  await expect(page.getByTestId("tabla-posiciones")).not.toContainText("Fondo indexado mundial");
});

test("CA-7: acusar un aviso no lo borra", async ({ page }) => {
  await page.goto("/#avisos");
  const a = page.getByTestId("aviso-AV-31");
  await a.getByTestId("acusar").click();
  await expect(a).toBeHidden();
  await page.getByRole("tab", { name: "Historial completo" }).click();
  await expect(page.getByTestId("aviso-AV-31").getByTestId("acusado")).toBeVisible();
});

test("CA-8: si la API no responde, el semáforo pasa a rojo y no se muestran cifras", async ({ page }) => {
  await page.goto("/#salud");
  await expect(page.getByTestId("semaforo")).toHaveAttribute("data-color", "ambar");
  await page.getByTestId("simular-fallo").click();
  await expect(page.getByTestId("semaforo")).toHaveAttribute("data-color", "rojo");
  await expect(page.getByRole("alert").first()).toContainText("La API del robot no responde");
  await expect(page.getByTestId("bloques")).toHaveCount(0);
  await page.getByTestId("simular-fallo").click();
  await expect(page.getByTestId("bloques")).toBeVisible();
});

test("subir un límite desde Configuración crea una decisión con fricción", async ({ page }) => {
  await page.goto("/#configuracion");
  const f = page.getByTestId("param-peso_max");
  await f.getByLabel("Valor nuevo").fill("40");
  await f.getByTestId("proponer-peso_max").click();
  await expect(page).toHaveURL(/#decisiones$/);
  await expect(page.locator("[data-testid^='detalle-D-']")).toContainText("Subir «Peso máximo de un activo (táctica)»");
});

for (const [nombre, ancho, tema] of [["móvil claro", 400, "light"], ["escritorio oscuro", 1280, "dark"]] as const) {
  test(`CA-9: sin desplazamiento horizontal (${nombre})`, async ({ page }) => {
    await page.emulateMedia({ colorScheme: tema });
    await page.setViewportSize({ width: ancho, height: 860 });
    for (const p of PANTALLAS) {
      await page.goto(`/#${p}`);
      await page.waitForTimeout(400);
      const ancho_doc = await page.evaluate(() => document.documentElement.scrollWidth);
      expect(ancho_doc, p).toBeLessThanOrEqual(ancho);
    }
  });
}
