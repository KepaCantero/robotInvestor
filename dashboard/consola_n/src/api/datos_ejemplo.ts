// Datos de ejemplo del prototipo. Inventados y coherentes entre sí; ninguno es del operador.
// Instrumentos genéricos para que nadie los tome por una recomendación.
import type { Aviso, Cartera, CifraPrincipal, Decision, Informes, Parametro, Posicion, PuntoSerie, Salud } from "./tipos";

const MIN = 60_000;
const DIA = 86_400_000;

function enMinutos(ahora: number, m: number) {
  return new Date(ahora + m * MIN).toISOString();
}

/** Generador pseudoaleatorio con semilla (mulberry32): mismas series en cada carga. */
function aleatorio(semilla: number) {
  let a = semilla >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Serie diaria que termina exactamente en `fin`, con la volatilidad diaria dada. */
export function serieDiaria(semilla: number, fin: number, dias: number, vol: number, hasta: number): PuntoSerie[] {
  const r = aleatorio(semilla);
  const pasos: number[] = [];
  for (let i = 0; i < dias; i++) pasos.push((r() - 0.5) * 2 * vol);
  const valores: number[] = [fin];
  for (let i = dias - 1; i > 0; i--) valores.unshift(valores[0]! / (1 + pasos[i]!));
  return valores.map((v, i) => ({
    fecha: new Date(hasta - (dias - 1 - i) * DIA).toISOString().slice(0, 10),
    valor: Number(v.toFixed(v < 5 ? 4 : 2)),
  }));
}

function posicion(p: Omit<Posicion, "valor" | "resultado"> & { divisa?: boolean }): Posicion {
  const { divisa, ...resto } = p;
  const resultado = divisa
    ? p.cantidad * (p.precio / p.precioEntrada - 1)
    : p.cantidad * (p.precio - p.precioEntrada);
  const valor = divisa ? p.cantidad + resultado : p.cantidad * p.precio;
  return { ...resto, valor: Number(valor.toFixed(2)), resultado: Number(resultado.toFixed(2)) };
}

export function posicionesIniciales(): Posicion[] {
  return [
    posicion({ id: "P-01", cartera: "trading", instrumento: "EUR/USD", clase: "Divisas", cantidad: 1200, precioEntrada: 1.082, precio: 1.0874, rangoMin: 1.071, rangoMax: 1.101, estres: 48, stop: 1.0775, divisa: true }),
    posicion({ id: "P-02", cartera: "trading", instrumento: "USD/JPY", clase: "Divisas", cantidad: 900, precioEntrada: 151.4, precio: 150.62, rangoMin: 147.8, rangoMax: 154.2, estres: 52, stop: 152.9, divisa: true }),
    posicion({ id: "P-03", cartera: "tactica", instrumento: "ETF renta variable europea", clase: "Renta variable", cantidad: 10, precioEntrada: 82.1, precio: 84.35, rangoMin: 76.5, rangoMax: 91.0, estres: 338, stop: 77.0 }),
    posicion({ id: "P-04", cartera: "tactica", instrumento: "ETF oro físico", clase: "Materias primas", cantidad: 20, precioEntrada: 61.2, precio: 63.9, rangoMin: 57.4, rangoMax: 69.8, estres: 255, stop: 58.0 }),
    posicion({ id: "P-05", cartera: "largo", instrumento: "Fondo indexado mundial", clase: "Fondos", cantidad: 34.6, precioEntrada: 268.4, precio: 255.1, rangoMin: 205.0, rangoMax: 330.0, estres: 4410, stop: null, caidaAceptada: 35, caidaActual: 9.8, costeSalida: 0 }),
    posicion({ id: "P-06", cartera: "largo", instrumento: "Fondo indexado bonos euro", clase: "Fondos", cantidad: 160, precioEntrada: 22.1, precio: 22.32, rangoMin: 20.9, rangoMax: 23.6, estres: 390, stop: null, caidaAceptada: 35, caidaActual: 1.2, costeSalida: 0 }),
    posicion({ id: "P-07", cartera: "largo", instrumento: "Fondo indexado emergentes", clase: "Fondos", cantidad: 310, precioEntrada: 11.8, precio: 11.25, rangoMin: 8.4, rangoMax: 15.1, estres: 1520, stop: null, caidaAceptada: 35, caidaActual: 12.4, costeSalida: 0 }),
  ];
}

export function carterasDesde(pos: Posicion[]): Cartera[] {
  const suma = (c: string, k: "valor" | "resultado") =>
    Number(pos.filter((p) => p.cartera === c).reduce((s, p) => s + p[k], 0).toFixed(2));
  return [
    { id: "trading", nombre: "Trading", ritmo: "A diario, si quiere", valor: suma("trading", "valor") + 900, efectivo: 900, resultadoPeriodo: suma("trading", "resultado"), periodo: "Posiciones abiertas" },
    { id: "tactica", nombre: "Táctica", ritmo: "Una vez por semana", valor: suma("tactica", "valor") + 3878.5, efectivo: 3878.5, resultadoPeriodo: suma("tactica", "resultado"), periodo: "Posiciones abiertas" },
    {
      id: "largo",
      nombre: "Largo plazo",
      ritmo: "Una vez al mes",
      valor: suma("largo", "valor") + 310,
      efectivo: 310,
      resultadoPeriodo: suma("largo", "resultado"),
      periodo: "Desde la primera aportación",
      plan: { objetivo: "Jubilación", anosHechos: 2, anosTotales: 25, enCamino: true, nota: "Las caídas de este año están dentro de lo que aceptó por escrito. El plan no cambia." },
    },
  ];
}

export const cifraEjemplo: CifraPrincipal = { euros: 142, rangoMin: -310, rangoMax: 590, nivel: 0.9, desde: "2026-09-01", semanas: 10 };

export function decisionesIniciales(ahora: number): Decision[] {
  return [
    {
      id: "D-0147", tipo: "abrir", cartera: "trading", instrumento: "EUR/USD",
      resumen: "Abrir una posición larga en EUR/USD dentro del mandato",
      cifrasF: { resultado: "aprobado", motivo: "Dentro de todos los límites", importe: 1500, cantidad: 1500, precioRef: 1.0874, stop: 1.079, perdidaMaxima: 11.7 },
      estresM: 61, planBase: "Sin cambio en el plan: la cartera de trading opera con su propio presupuesto de riesgo.",
      venceEn: enMinutos(ahora, 45), limiteTocadoHoy: false, estado: "pendiente", usada: false,
      explicacion: "Se abren 1.500,00 € en EUR/USD con el stop en 1,079. Si salta el stop, la pérdida máxima es de 11,70 €. En una caída como la de 2008, el riesgo de esta posición sería de 61 €.",
    },
    {
      id: "D-0148", tipo: "aumentar", cartera: "tactica", instrumento: "ETF renta variable europea",
      resumen: "Aumentar la posición en el ETF de renta variable europea",
      cifrasF: { resultado: "reducido", motivo: "Pedía 30 participaciones; F lo reduce a 11 por el peso máximo de un activo (30 %)", importe: 927.85, cantidad: 11, precioRef: 84.35, stop: 77, perdidaMaxima: 80.85 },
      estresM: 371, planBase: "Con esta compra, el ETF pesa un 29,5 % de la cartera táctica, justo por debajo del máximo.",
      venceEn: enMinutos(ahora, 80), limiteTocadoHoy: false, estado: "pendiente", usada: false,
      explicacion: "F redujo la compra de 30 a 11 participaciones, 927,85 € en total. Con el stop en 77, la pérdida máxima es de 80,85 €; en una caída como la de 2008 serían 371 €.",
    },
    {
      id: "D-0149", tipo: "aumentar", cartera: "trading", instrumento: "USD/JPY",
      resumen: "Aumentar la posición corta en USD/JPY",
      cifrasF: { resultado: "aprobado", motivo: "Dentro de los límites de la operación", importe: 600, cantidad: 600, precioRef: 150.62, stop: 152.9, perdidaMaxima: 9.1 },
      estresM: 35, planBase: "Sin cambio en el plan.",
      venceEn: enMinutos(ahora, 120), limiteTocadoHoy: true, estado: "pendiente", usada: false,
      explicacion: "El yen suele subir un 3,4 % en semanas como esta, así que aumentar 600,00 € tiene sentido.",
    },
    {
      id: "D-0150", tipo: "reducir", cartera: "tactica", instrumento: "ETF oro físico",
      resumen: "Reducir a la mitad el ETF de oro: H da la tesis por debilitada",
      cifrasF: { resultado: "aprobado", motivo: "Reducir riesgo: solo controles de forma", importe: 639, cantidad: 10, precioRef: 63.9, stop: null, perdidaMaxima: 0 },
      estresM: -128, planBase: "Sin cambio en el plan.",
      venceEn: enMinutos(ahora, 300), limiteTocadoHoy: false, estado: "pendiente", usada: false,
      explicacion: "Se venden 10 participaciones del ETF de oro, 639,00 €. El riesgo en una caída como la de 2008 baja en 128 €.",
    },
    {
      id: "D-0145", tipo: "abrir", cartera: "trading", instrumento: "GBP/USD",
      resumen: "Abrir una posición larga en GBP/USD",
      cifrasF: { resultado: "aprobado", motivo: "Dentro de todos los límites", importe: 1000, cantidad: 1000, precioRef: 1.2741, stop: 1.2655, perdidaMaxima: 6.75 },
      estresM: 44, planBase: "Sin cambio en el plan.", venceEn: enMinutos(ahora, -900), limiteTocadoHoy: false,
      estado: "aprobada", usada: true, explicacion: "",
    },
    {
      id: "D-0144", tipo: "aumentar", cartera: "tactica", instrumento: "ETF oro físico",
      resumen: "Aumentar el ETF de oro",
      cifrasF: { resultado: "aprobado", motivo: "Dentro de los límites", importe: 640, cantidad: 10, precioRef: 64.0, stop: 58, perdidaMaxima: 60 },
      estresM: 128, planBase: "Sin cambio en el plan.", venceEn: enMinutos(ahora, -1500), limiteTocadoHoy: false,
      estado: "caducada", usada: false, explicacion: "",
    },
  ];
}

export function avisosIniciales(ahora: number): Aviso[] {
  return [
    { id: "AV-31", prioridad: "alta", titulo: "Una decisión vence en menos de una hora", detalle: "D-0147 (abrir EUR/USD) caduca si no responde. Si caduca, no pasa nada: el robot no actúa.", fecha: enMinutos(ahora, -12), acusadoEn: null },
    { id: "AV-30", prioridad: "media", titulo: "Stop ejecutado en GBP/USD", detalle: "Se cerró la posición en 1,2655 con una pérdida de 6,75 €, la prevista por F.", fecha: enMinutos(ahora, -190), acusadoEn: null },
    { id: "AV-29", prioridad: "media", titulo: "Dato con retraso: fondo de emergentes", detalle: "El valor liquidativo llegó con un día de retraso. K lo marca como viejo y E no lo usa para dimensionar hasta que llegue el de hoy.", fecha: enMinutos(ahora, -600), acusadoEn: enMinutos(ahora, -540) },
    { id: "AV-28", prioridad: "info", titulo: "Informe semanal listo", detalle: "Semana del 3 al 9 de noviembre: 5 órdenes, 6 abstenciones y 11,05 € de costes.", fecha: enMinutos(ahora, -2880), acusadoEn: enMinutos(ahora, -2700) },
    { id: "AV-27", prioridad: "alta", titulo: "Latido perdido durante 4 minutos", detalle: "El servidor no respondió entre las 03:12 y las 03:16. El vigilante avisó por el canal fuera del chat; las protecciones siguieron en el intermediario.", fecha: enMinutos(ahora, -11520), acusadoEn: enMinutos(ahora, -11490) },
  ];
}

export function informesEjemplo(hasta: number): Informes {
  const robot = serieDiaria(11, 25172, 23, 0.006, hasta - 10 * DIA);
  const sombra = serieDiaria(12, 25040, 23, 0.0055, hasta - 10 * DIA);
  return {
    semanal: {
      semana: "Del 3 al 9 de noviembre de 2026",
      analisis: 38,
      ordenes: 5,
      abstenciones: 6,
      embudo: [
        { etapa: "Oportunidades vistas (A)", cantidad: 214 },
        { etapa: "Estudiadas a fondo (B y C)", cantidad: 38 },
        { etapa: "Con ventaja tras D", cantidad: 11 },
        { etapa: "Aprobadas por F", cantidad: 7 },
        { etapa: "Órdenes enviadas (G)", cantidad: 5 },
      ],
      costeIA: 4.85,
      costeIntermediario: 6.2,
    },
    mensual: {
      mes: "Octubre de 2026",
      robot,
      sombra,
      atribucion: [
        { etapa: "Selección (A, B y C)", euros: 38, rangoMin: -120, rangoMax: 190 },
        { etapa: "Dimensionado (E)", euros: 12, rangoMin: -30, rangoMax: 55 },
        { etapa: "Control de riesgo (F)", euros: -9, rangoMin: -25, rangoMax: 8 },
        { etapa: "Ejecución y costes (G)", euros: -14, rangoMin: -20, rangoMax: -8 },
      ],
      intervenciones: [
        { descripcion: "Venta a mano del ETF de oro el 14 de octubre", euros: -23 },
        { descripcion: "Rechazo de la decisión D-0131", euros: 8 },
      ],
    },
    anual: [
      { pregunta: "¿Sigue valiendo la caída que aceptó por escrito para el largo plazo?", hecho: false },
      { pregunta: "¿Ha cambiado su horizonte, sus ingresos o su colchón de emergencia?", hecho: false },
      { pregunta: "¿Aporta el robot frente a la cartera sombra, con su rango?", hecho: false },
      { pregunta: "¿Qué parámetros quiere revisar con el asesor de configuración?", hecho: false },
      { pregunta: "¿Está al día la carta de instrucciones para la persona de confianza?", hecho: false },
    ],
  };
}

export function saludInicial(ahora: number): Salud {
  const hace = (m: number) => enMinutos(ahora, -m);
  return {
    bloques: [
      { id: "A", nombre: "A · Buscar oportunidades", estado: "ok", ultimoLatido: hace(1), nota: "Ciclo semanal del lunes completo" },
      { id: "B", nombre: "B · Elegir activos", estado: "ok", ultimoLatido: hace(1), nota: "3 encargos atendidos" },
      { id: "C", nombre: "C · Analizar a fondo", estado: "ok", ultimoLatido: hace(2), nota: "Perfil de divisas" },
      { id: "D", nombre: "D · Comparar opciones", estado: "ok", ultimoLatido: hace(1), nota: "" },
      { id: "E", nombre: "E · Dimensionar carteras", estado: "ok", ultimoLatido: hace(1), nota: "" },
      { id: "F", nombre: "F · Control de riesgo", estado: "ok", ultimoLatido: hace(0), nota: "Código, sin IA" },
      { id: "G", nombre: "G · Ejecutar y conciliar", estado: "ok", ultimoLatido: hace(0), nota: "Conciliación de las 08:00 limpia" },
      { id: "K", nombre: "K · Datos", estado: "degradado", ultimoLatido: hace(1), nota: "Un valor liquidativo con un día de retraso" },
      { id: "I", nombre: "I · Evaluar frente a la sombra", estado: "ok", ultimoLatido: hace(3), nota: "" },
      { id: "O", nombre: "Orquestador", estado: "ok", ultimoLatido: hace(0), nota: "" },
    ],
    sellos: [
      { fuente: "Precios de divisas (intermediario)", ultimo: hace(1), estado: "fresco" },
      { fuente: "Cotizaciones de ETF", ultimo: hace(15), estado: "fresco" },
      { fuente: "Valor liquidativo de fondos", ultimo: hace(1500), estado: "viejo" },
      { fuente: "Calendario de eventos", ultimo: hace(240), estado: "fresco" },
    ],
    presupuestoIA: { gastado: 18.4, tope: 40, mes: "Noviembre de 2026" },
    latido: hace(0),
    killSwitch: false,
  };
}

export function parametrosIniciales(): Parametro[] {
  return [
    { id: "riesgo_op", nombre: "Riesgo máximo por operación (trading)", valor: 1.5, porDefecto: 1.5, unidad: "% de la cartera", enEuros: "45 € con una cartera de 3.000 €", justificacion: "Con este valor, diez stops seguidos cuestan unos 420 €: incómodo, pero no cambia el plan.", subeRiesgo: true },
    { id: "perdida_dia", nombre: "Pérdida máxima diaria (trading)", valor: 3, porDefecto: 3, unidad: "% de la cartera", enEuros: "90 € al día", justificacion: "Si se alcanza, el robot deja de abrir posiciones ese día y no se puede subir hasta mañana.", subeRiesgo: true },
    { id: "peso_max", nombre: "Peso máximo de un activo (táctica)", valor: 30, porDefecto: 30, unidad: "% de la cartera", enEuros: "1.800 € con una cartera de 6.000 €", justificacion: "Evita que un solo error pese demasiado en la cartera táctica.", subeRiesgo: true },
    { id: "caida_aceptada", nombre: "Caída aceptada (largo plazo)", valor: 35, porDefecto: 35, unidad: "% desde el máximo", enEuros: "Unos 5.600 € sobre 16.000 €", justificacion: "Es la caída que firmó por escrito. Una crisis como la de 2008 llegó a algo más.", subeRiesgo: true },
    { id: "aportacion", nombre: "Aportación mensual (largo plazo)", valor: 300, porDefecto: 300, unidad: "€ al mes", enEuros: "3.600 € al año", justificacion: "Sale del plan base; la decide usted con el planificador.", subeRiesgo: false },
  ];
}
