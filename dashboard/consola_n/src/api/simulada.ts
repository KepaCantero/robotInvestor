// API simulada en memoria. Vuelve a comprobar en el «servidor» todo lo que comprueba la pantalla:
// la consola no es la que protege, solo informa (falla cerrado).
import { CADUCIDAD_APROBACION_MIN, CODIGO_DEMO, ESPERA_AUMENTO_SEG, LATENCIA_API_MS } from "@/config/prototipo";
import { motivoBloqueo, SUBE_RIESGO, textoBloqueo } from "@/logica/friccion";
import type { Comprobacion } from "@/logica/semaforo";
import { eurosCent, numero } from "@/logica/formato";
import {
  avisosIniciales,
  carterasDesde,
  cifraEjemplo,
  decisionesIniciales,
  informesEjemplo,
  parametrosIniciales,
  posicionesIniciales,
  saludInicial,
  serieDiaria,
} from "./datos_ejemplo";
import { ErrorApi, type ConsolaApi } from "./puerto";
import type { Aviso, Decision, Informes, OperacionExterna, Parametro, Posicion, Salud } from "./tipos";

const copia = <T>(x: T): T => structuredClone(x);

/** Lo que el operador debe teclear: el importe de la orden o, si sube un límite, el valor nuevo. */
export function importeEsperado(d: Decision): number {
  return d.tipo === "subir_limite" ? d.cifrasF.cantidad : d.cifrasF.importe;
}

export class ApiSimulada implements ConsolaApi {
  private ahora: () => number;
  private latencia: number;
  private posicionesE: Posicion[];
  private decisionesE: Decision[];
  private avisosE: Aviso[];
  private saludE: Salud;
  private parametrosE: Parametro[];
  private informesE: Informes;
  private esperas = new Map<string, number>();
  private siguiente = 151;
  /** Para probar el fallo cerrado: con esto activo, todas las llamadas fallan. */
  fallo = false;

  constructor(opciones: { ahora?: () => number; latenciaMs?: number } = {}) {
    this.ahora = opciones.ahora ?? (() => Date.now());
    this.latencia = opciones.latenciaMs ?? LATENCIA_API_MS;
    const t = this.ahora();
    this.posicionesE = posicionesIniciales();
    this.decisionesE = decisionesIniciales(t);
    this.avisosE = avisosIniciales(t);
    this.saludE = saludInicial(t);
    this.parametrosE = parametrosIniciales();
    this.informesE = informesEjemplo(t);
  }

  private async responder<T>(f: () => T): Promise<T> {
    if (this.latencia > 0) await new Promise((r) => setTimeout(r, this.latencia));
    if (this.fallo) throw new ErrorApi("La API del robot no responde.");
    return copia(f());
  }

  private caducar() {
    const t = this.ahora();
    for (const d of this.decisionesE)
      if (d.estado === "pendiente" && new Date(d.venceEn).getTime() <= t) d.estado = "caducada";
  }

  private decision(id: string): Decision {
    const d = this.decisionesE.find((x) => x.id === id);
    if (!d) throw new ErrorApi(`No existe la decisión ${id}.`);
    return d;
  }

  comprobaciones() {
    return this.responder<Comprobacion[]>(() => {
      this.caducar();
      const t = this.ahora();
      const altasSinAcuse = this.avisosE.filter((a) => a.prioridad === "alta" && !a.acusadoEn).length;
      const pronto = this.decisionesE.filter(
        (d) => d.estado === "pendiente" && new Date(d.venceEn).getTime() - t < 60 * 60_000,
      ).length;
      const pendientes = this.decisionesE.filter((d) => d.estado === "pendiente").length;
      const viejos = this.saludE.sellos.filter((s) => s.estado !== "fresco").length;
      const p = this.saludE.presupuestoIA;
      return [
        { id: "integridad", nombre: "Integridad", estado: this.saludE.killSwitch ? "ambar" : "verde", detalle: this.saludE.killSwitch ? "Kill-switch activo: no se abren posiciones" : "Conciliación con el intermediario limpia" },
        { id: "datos", nombre: "Datos", estado: viejos ? "ambar" : "verde", detalle: viejos ? `${viejos} fuente con retraso` : "Todas las fuentes al día" },
        { id: "presupuesto", nombre: "Presupuesto", estado: p.gastado / p.tope > 0.9 ? "ambar" : "verde", detalle: `${eurosCent(p.gastado)} de ${eurosCent(p.tope)} este mes` },
        { id: "avisos", nombre: "Avisos", estado: altasSinAcuse ? "ambar" : "verde", detalle: altasSinAcuse ? `${altasSinAcuse} aviso alto sin acusar` : "Nada urgente sin acusar" },
        { id: "decisiones", nombre: "Decisiones", estado: pronto ? "ambar" : "verde", detalle: pronto ? `${pronto} vence en menos de una hora` : `${pendientes} pendientes, sin prisa` },
      ];
    });
  }

  cifraPrincipal() {
    return this.responder(() => cifraEjemplo);
  }
  carteras() {
    return this.responder(() => carterasDesde(this.posicionesE));
  }
  posiciones() {
    return this.responder(() => this.posicionesE);
  }
  serie(posicionId: string) {
    return this.responder(() => {
      const i = this.posicionesE.findIndex((p) => p.id === posicionId);
      const p = this.posicionesE[i];
      if (!p) throw new ErrorApi(`No existe la posición ${posicionId}.`);
      const vol = p.clase === "Divisas" ? 0.004 : p.clase === "Fondos" ? 0.009 : 0.011;
      return serieDiaria(100 + i, p.precio, 120, vol, this.ahora());
    });
  }
  decisiones() {
    return this.responder(() => {
      this.caducar();
      return this.decisionesE;
    });
  }
  avisos() {
    return this.responder(() => this.avisosE);
  }
  informes() {
    return this.responder(() => this.informesE);
  }
  salud() {
    return this.responder(() => ({ ...this.saludE, latido: new Date(this.ahora()).toISOString() }));
  }
  parametros() {
    return this.responder(() => this.parametrosE);
  }

  pedirCodigo(decisionId: string) {
    return this.responder(() => {
      this.decision(decisionId);
      const hasta = this.ahora() + ESPERA_AUMENTO_SEG * 1000;
      this.esperas.set(decisionId, hasta);
      return { esperaHasta: new Date(hasta).toISOString() };
    });
  }

  aprobar(decisionId: string, importeTecleado: string, codigo: string) {
    return this.responder(() => {
      this.caducar();
      const d = this.decision(decisionId);
      if (this.saludE.killSwitch && SUBE_RIESGO.has(d.tipo))
        throw new ErrorApi("Kill-switch activo: no se abren ni aumentan posiciones.");
      const hasta = this.esperas.get(decisionId) ?? Number.POSITIVE_INFINITY;
      const motivo = motivoBloqueo({
        tipo: d.tipo,
        importeEsperadoCent: Math.round(importeEsperado(d) * 100),
        importeTecleado,
        codigo,
        codigoValido: CODIGO_DEMO,
        esperaRestanteSeg: Math.max(0, (hasta - this.ahora()) / 1000),
        estado: { usada: d.usada, venceEn: d.venceEn, limiteTocadoHoy: d.limiteTocadoHoy },
        ahora: this.ahora(),
      });
      if (motivo) throw new ErrorApi(textoBloqueo[motivo]);
      d.usada = true;
      d.estado = "aprobada";
      if (d.tipo === "reducir") {
        const p = this.posicionesE.find((x) => x.instrumento === d.instrumento && x.cartera === d.cartera);
        if (p) this.reducirPosicion(p, d.cifrasF.cantidad);
      }
      return d;
    });
  }

  rechazar(decisionId: string) {
    return this.responder(() => {
      const d = this.decision(decisionId);
      if (d.estado !== "pendiente") throw new ErrorApi("Esta decisión ya está cerrada.");
      d.estado = "rechazada";
      d.usada = true;
      return d;
    });
  }

  private reducirPosicion(p: Posicion, cantidad: number) {
    const c = Math.min(cantidad, p.cantidad);
    const f = (p.cantidad - c) / p.cantidad;
    p.cantidad = Number((p.cantidad - c).toFixed(4));
    p.valor = Number((p.valor * f).toFixed(2));
    p.resultado = Number((p.resultado * f).toFixed(2));
    p.estres = Math.round(p.estres * f);
  }

  vender(posicionId: string, cantidad: number) {
    return this.responder(() => {
      const p = this.posicionesE.find((x) => x.id === posicionId);
      if (!p) throw new ErrorApi(`No existe la posición ${posicionId}.`);
      if (!(cantidad > 0)) throw new ErrorApi("La cantidad tiene que ser mayor que cero.");
      // Asimetría de F (enmienda 5, D-52): vender más de lo que se tiene abriría riesgo, así que se veta.
      if (cantidad > p.cantidad) throw new ErrorApi("No se puede vender más de lo que se tiene: eso abriría una posición nueva.");
      this.reducirPosicion(p, cantidad);
      this.avisosE.unshift({
        id: `AV-${this.siguiente++}`,
        prioridad: "info",
        titulo: `Venta enviada: ${numero(cantidad)} de ${p.instrumento}`,
        detalle: "Reducir riesgo no necesita aprobación. G la ejecuta y la concilia.",
        fecha: new Date(this.ahora()).toISOString(),
        acusadoEn: null,
      });
      return p;
    });
  }

  acusar(avisoId: string) {
    return this.responder(() => {
      const a = this.avisosE.find((x) => x.id === avisoId);
      if (!a) throw new ErrorApi(`No existe el aviso ${avisoId}.`);
      a.acusadoEn ??= new Date(this.ahora()).toISOString();
      return a;
    });
  }

  activarKillSwitch() {
    return this.responder(() => {
      this.saludE.killSwitch = true;
      this.avisosE.unshift({
        id: `AV-${this.siguiente++}`,
        prioridad: "alta",
        titulo: "Kill-switch activado por el operador",
        detalle: "No se abren ni aumentan posiciones. Los stops siguen en el intermediario y no se vende nada sin su orden.",
        fecha: new Date(this.ahora()).toISOString(),
        acusadoEn: new Date(this.ahora()).toISOString(),
      });
      return this.saludE;
    });
  }

  desactivarKillSwitch(codigo: string) {
    return this.responder(() => {
      if (codigo.trim() !== CODIGO_DEMO) throw new ErrorApi("El código no es correcto.");
      this.saludE.killSwitch = false;
      return this.saludE;
    });
  }

  proponerParametro(id: string, valor: number) {
    return this.responder(() => {
      const p = this.parametrosE.find((x) => x.id === id);
      if (!p) throw new ErrorApi(`No existe el parámetro ${id}.`);
      if (!Number.isFinite(valor) || valor < 0) throw new ErrorApi("El valor no es válido.");
      const sube = p.subeRiesgo && valor > p.valor;
      if (!sube) {
        p.valor = valor;
        return { aplicado: true };
      }
      const decisionId = `D-0${this.siguiente++}`;
      const limiteHoy = id === "riesgo_op" || id === "perdida_dia";
      this.decisionesE.unshift({
        id: decisionId,
        tipo: "subir_limite",
        cartera: id === "peso_max" ? "tactica" : id === "caida_aceptada" ? "largo" : "trading",
        instrumento: p.nombre,
        resumen: `Subir «${p.nombre}» de ${numero(p.valor)} a ${numero(valor)} ${p.unidad}`,
        cifrasF: { resultado: "aprobado", motivo: "Cambio de límite: lo aprueba el operador con segundo factor y espera", importe: 0, cantidad: valor, precioRef: p.valor, stop: null, perdidaMaxima: 0 },
        estresM: 0,
        planBase: "El asesor de configuración lo explicará en euros si se lo pide al Broker.",
        venceEn: new Date(this.ahora() + CADUCIDAD_APROBACION_MIN * 60_000).toISOString(),
        limiteTocadoHoy: limiteHoy,
        explicacion: "",
        estado: "pendiente",
        usada: false,
      });
      return { aplicado: false, decisionId };
    });
  }

  declararOperacion(op: OperacionExterna) {
    return this.responder(() => {
      if (!op.instrumento.trim() || !(op.cantidad > 0) || !(op.precio > 0)) throw new ErrorApi("Faltan datos de la operación.");
      const a: Aviso = {
        id: `AV-${this.siguiente++}`,
        prioridad: "info",
        titulo: `Operación declarada: ${op.lado} de ${numero(op.cantidad)} ${op.instrumento}`,
        detalle: `A ${numero(op.precio)} el ${op.fecha}. G la tendrá en cuenta al conciliar; sin declararla sería una discrepancia.`,
        fecha: new Date(this.ahora()).toISOString(),
        acusadoEn: null,
      };
      this.avisosE.unshift(a);
      return a;
    });
  }
}
