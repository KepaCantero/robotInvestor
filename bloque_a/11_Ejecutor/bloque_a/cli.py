"""CLI «bloque-a»: ciclo, peticion, consulta, decision, evaluar, estado, verificar-enlaces, backtest, generar-sinteticos;
V5.1: seguimiento (CT-24, ciclo C6, F11), consulta-broker (CT-23) y credencial (CT-25, bóveda de HT-01)."""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

import pandas as pd

from .configuracion import DIR_EJECUTOR, RUTA_UNIVERSO_EJEMPLO, cargar_config, ruta


def _resumen_run(r: dict) -> dict:
    return {"run_id": r["run_id"], "as_of": r["as_of"], "estado": r["estado"], "entrega": r.get("entrega", "ENTREGADA"),
            "nivel_por_clase": r["nivel_por_clase"], "g3": (r.get("g3_entregables") or r["g3"]).get("dictamen"),
            "top3_por_clase": {c: [o["opp_id"] for o in d["opciones"]] for c, d in r["paquete"]["clases"].items()},
            "entregables": r.get("entregables"), "consumo_uc": (r.get("consumo") or {}).get("uc")}


def _bloque(a, cfg):
    from .herramientas.ht01_datos import ProveedorCSV, ProveedorYahoo, cargar_universo
    from .llm import crear_cliente
    from .orquestacion import Bloque
    uni = cargar_universo(a.universo)
    if a.proveedor == "yahoo":
        prov = ProveedorYahoo(list(uni["simbolo"]), cfg.get("modo", "vivo"))
    else:
        if not a.datos:
            sys.exit("Falta --datos CARPETA (CSV por símbolo) o --proveedor yahoo")
        prov = ProveedorCSV(a.datos)
    cli = crear_cliente(a.cliente, cfg, a.replay, a.replay_modo)
    return Bloque(cfg, prov, uni, cli, a.estado or (cfg["rutas"]["almacen"]), a.salida or cfg["rutas"]["entregables"], anonimizar=a.anonimizar)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bloque-a", description="Ejecutor programático del Bloque A (Robot Investor)")
    ap.add_argument("--config", help="YAML que se fusiona sobre config/por_defecto.yaml")
    ap.add_argument("--datos", help="Carpeta de datos CSV (HT-01)")
    ap.add_argument("--universo", default=str(RUTA_UNIVERSO_EJEMPLO))
    ap.add_argument("--proveedor", choices=["csv", "yahoo"], default="csv")
    ap.add_argument("--cliente", choices=["mock", "anthropic", "replay"], default="mock")
    ap.add_argument("--replay", help="Archivo JSONL de grabación (cliente replay)")
    ap.add_argument("--replay-modo", choices=["grabar", "reproducir"], default="reproducir")
    ap.add_argument("--estado", help="Carpeta del estado del bloque (F1–F6, F10, RC, HA)")
    ap.add_argument("--salida", help="Carpeta de salida / entregables")
    ap.add_argument("--as-of", help="Fecha as_of (AAAA-MM-DD); por defecto hoy")
    ap.add_argument("--anonimizar", action="store_true", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ciclo", help="Ciclo periódico C1")
    p = sub.add_parser("peticion", help="Petición ad hoc CT-01")
    p.add_argument("--json", required=True)
    p = sub.add_parser("consulta", help="Consulta CT-03")
    p.add_argument("texto")
    p.add_argument("--sin-escalado", action="store_true")
    p = sub.add_parser("decision", help="Decisiones y configuración CT-04")
    p.add_argument("--json", required=True)
    sub.add_parser("evaluar", help="C5: resolución de pronósticos, métricas, certificados y lecciones")
    sub.add_parser("estado", help="Colas, consumo y últimos runs")
    p = sub.add_parser("alta-referencias", help="Incorpora un lote de fichas a su catálogo temático")
    p.add_argument("--archivo", choices=("F7", "F8", "F9"), required=True)
    p.add_argument("--json", required=True)
    p = sub.add_parser("verificar-enlaces", help="HT-02 sobre F7, F8, F9 y FM")
    p.add_argument("--revisiones", help="JSON de decisiones del custodio por archivo e identificador (T-181)")
    p.add_argument("--aplicar", action="store_true", help="Escribe los estados en los archivos (por defecto solo informe)")
    p = sub.add_parser("reconciliar-mensaje", help="CT-01: liberar la reserva de un mensaje fallido o interrumpido (tras revisar F5)")
    p.add_argument("--msg-id", required=True)
    p.add_argument("--motivo", required=True)
    p = sub.add_parser("backtest", help="Backtest sobre fechas as_of")
    p.add_argument("--desde", required=True)
    p.add_argument("--hasta", required=True)
    p.add_argument("--frecuencia", choices=["diaria", "semanal", "quincenal", "mensual"])
    p.add_argument("--clases", help="Lista separada por comas (RV,RF,…)")
    p.add_argument("--sin-resolucion-final", action="store_true")
    # V5.1 · Seguimiento encargado de opción (CT-24, ciclo C6, F11)
    p = sub.add_parser("seguimiento", help="CT-24: alta, modificar, pausar, reanudar, cancelar, ejecutar (ciclo C6), responder, listar")
    p.add_argument("accion", choices=["alta", "modificar", "pausar", "reanudar", "cancelar", "ejecutar", "responder", "listar"])
    p.add_argument("--seg", help="SEG- del encargo (todas las acciones salvo alta, ejecutar y listar)")
    p.add_argument("--json", help="JSON del CT-24 (alta: opp_id, frecuencia, motivo, senales_interes, fecha_fin; modificar: campos)")
    p.add_argument("--forzar", action="store_true", help="ejecutar: lanza el ciclo C6 del encargo aunque no haya vencido")
    p.add_argument("--decision", help="responder: decisión del Broker sobre la última recomendación (p. ej., ACEPTADA, RECHAZADA)")
    # V5.1 · Consultas del bloque al Broker (CT-23)
    p = sub.add_parser("consulta-broker", help="CT-23: enviar (saliente), responder, entrante, vencer, listar, revisiones (C2 "
                                               "pendientes), relanzar (revisiones C2 interrumpidas, pendientes o fallidas)")
    p.add_argument("accion", choices=["enviar", "responder", "entrante", "vencer", "listar", "revisiones", "relanzar"])
    p.add_argument("--json", help="enviar: {tipo, modo, preguntas[{texto, supuesto_declarado, efecto_si_falso}], clases, run_id}; "
                                   "responder: {respuestas, estado}; entrante: {contenido, referencia}")
    p.add_argument("--cns", help="CNS- (responder; en relanzar, solo las de esa consulta)")
    p.add_argument("--incluir-en-curso", action="store_true",
                   help="relanzar: también las EN_CURSO (solo si el proceso que las lanzó ya no corre; T-174)")
    # V5.1 · Credenciales (CT-25, bóveda simulada de HT-01)
    p = sub.add_parser("credencial", help="CT-25: solicitar, depositar (Broker, fuera de banda), responder, estado, recordatorios")
    p.add_argument("accion", choices=["solicitar", "depositar", "responder", "estado", "recordatorios", "c4"],
                   help="c4: mantenimiento C4 del BFA (revisa la bóveda de sus servicios y emite los CT-25 que falten, T-177)")
    p.add_argument("--servicio")
    p.add_argument("--solicitante", default="AG-16")
    p.add_argument("--uso", default="Fuente de datos para el análisis")
    p.add_argument("--impacto", default="Servicio degradado: fuente alternativa con calidad declarada")
    p.add_argument("--crd", help="CRD- de la solicitud")
    p.add_argument("--valor-desde-entorno", help="depositar: nombre de la variable de entorno con la clave (si falta, se pide sin eco)")
    p.add_argument("--caducidad")
    p.add_argument("--respuesta", dest="estado_credencial", choices=["PROVISTA", "DENEGADA", "APLAZADA"],
                   help="responder: estado que comunica el Broker (sin valores)")
    # T-158 · Guías de mejora del Orquestador (CT-18)
    p = sub.add_parser("guia", help="CT-18: emitir (el Orquestador, con el esquema del cuerpo) o listar las guías y su estado")
    p.add_argument("accion", choices=["emitir", "listar"])
    p.add_argument("--receptor", help="emitir: agente receptor (AG-nn)")
    p.add_argument("--json", help="emitir: {items: [{tipo, origen, que_cambia, donde_se_comprueba, como_se_sabe, caducidad}], "
                                   "fecha_aplicacion}")
    p.add_argument("--simular-fallo-del-emisor", action="store_true",
                   help="emitir (solo con --cliente mock): deja pasar el control doble del emisor para ejercer PB-48 (T-161)")
    p = sub.add_parser("generar-sinteticos", help="Escribe precios sintéticos (CSV) para el universo")
    p.add_argument("--desde", default="2022-01-03")
    p.add_argument("--hasta", default="2026-10-30")
    p.add_argument("--semilla", type=int, default=7)
    a = ap.parse_args(argv)
    cfg = cargar_config(a.config)

    if a.cmd == "generar-sinteticos":
        from .herramientas.ht01_datos import ProveedorSintetico, cargar_universo
        u = cargar_universo(a.universo)
        dest = a.salida or str(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos")
        ProveedorSintetico(dict(zip(u.simbolo, u.clase)), a.semilla, a.desde, a.hasta).escribir_csv(dest)
        print(json.dumps({"salida": dest, "simbolos": len(u)}, ensure_ascii=False))
        return 0
    if a.cmd == "backtest":
        from .backtest import ejecutar_backtest
        if not a.datos or not a.salida:
            sys.exit("backtest necesita --datos y --salida")
        r = ejecutar_backtest(cfg, a.desde, a.hasta, a.datos, a.universo, a.salida, a.frecuencia,
                              a.clases.split(",") if a.clases else None, tipo_cliente=a.cliente, replay=a.replay,
                              replay_modo=a.replay_modo, anonimizar=a.anonimizar, resolver_al_final=not a.sin_resolucion_final,
                              progreso=lambda res: print(f"{res['as_of']} {res['run_id']} {res['estado']}", file=sys.stderr))
        r.pop("bloque")
        r.pop("metricas")
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "alta-referencias":
        from .altas_referencias import incorporar
        from .referencias import ARCHIVOS_REF, localizar
        incorporar(localizar(ruta(cfg, "archivos_operativos"), ARCHIVOS_REF[a.archivo]), a.archivo, json.loads(Path(a.json).read_text(encoding="utf-8")))
        return 0
    if a.cmd == "verificar-enlaces":
        from .herramientas import ht02
        from .referencias import ARCHIVOS_REF, localizar
        base = ruta(cfg, "archivos_operativos")
        out = Path(a.salida or ".")
        out.mkdir(parents=True, exist_ok=True)
        codigo = 0
        from .almacen import Almacen, Reloj
        from .contratos import Mensajeria
        from .diseno_v6 import validar
        from .mantenimiento_fuentes import (
            CUSTODIOS,
            avisar_curador,
            bajas_registradas,
            publicar,
            tratar,
        )
        revisiones = json.loads(Path(a.revisiones).read_text(encoding="utf-8")) if a.revisiones else {}
        for k, nombre in ARCHIVOS_REF.items():
            archivo = localizar(base, nombre)
            informe = out / f"ht02_{k}.json"
            original = archivo.read_text(encoding="utf-8") if a.aplicar and k in CUSTODIOS and archivo.exists() else None
            args = [str(archivo), "--salida-json", str(informe)]
            if a.as_of:
                args.extend(["--fecha", a.as_of])
            if a.aplicar and k == "FM":
                args.append("--aplicar")
            resultado = ht02.main(args) or 0
            codigo = max(codigo, resultado)
            if resultado == 0 and original is not None:
                datos = json.loads(informe.read_text(encoding="utf-8"))
                nuevo = tratar(k, original, datos, revisiones.get(k, {}))
                publicar(archivo, original, nuevo)
                bajas = {(k, "REF-" + rid, dia) for rid, dia in bajas_registradas(nuevo.splitlines()) if dia <= datos["fecha"]}
                if bajas:
                    reloj = Reloj(cfg["zona_horaria"])
                    reloj.fijar(datos["fecha"])
                    almacen = Almacen(a.estado or cfg["rutas"]["almacen"], reloj)
                    avisar_curador(almacen, Mensajeria(almacen, validar(cfg)), datos["fecha"], almacen.nuevo_id("RUN"), bajas)
        return codigo
    bloque = _bloque(a, cfg)
    as_of = pd.Timestamp(a.as_of) if a.as_of else pd.Timestamp.now(tz=bloque.reloj.zona).tz_localize(None)
    if a.cmd == "ciclo":
        print(json.dumps(_resumen_run(bloque.ciclo(as_of)), ensure_ascii=False, indent=1))
    elif a.cmd == "peticion":
        r = bloque.peticion(json.loads(Path(a.json).read_text(encoding="utf-8")), as_of)
        print(json.dumps({**_resumen_run(r), "acuse": r["acuse"]}, ensure_ascii=False, indent=1, default=str))
    elif a.cmd == "consulta":
        r = bloque.consulta(a.texto, as_of=as_of, ejecutar_escalado=not a.sin_escalado)
        print(json.dumps(r, ensure_ascii=False, indent=1, default=str))
    elif a.cmd == "decision":
        print(json.dumps(bloque.decision(json.loads(Path(a.json).read_text(encoding="utf-8")), as_of), ensure_ascii=False, indent=1))
    elif a.cmd == "evaluar":
        bloque.fijar_fecha(as_of)
        r = bloque.evaluador.ciclo(as_of)
        print(json.dumps({"resueltos": r["resueltos"], "no_resolubles": r["no_resolubles"], "celdas": list(r["metricas"]),
                          "certificados_emitidos": [c["id"] for c in r["certificados"]["emitidos"]],
                          "lecciones_nuevas": [l["id"] for l in r["lecciones_nuevas"]]}, ensure_ascii=False, indent=1))
    elif a.cmd == "estado":
        print(json.dumps(bloque.estado(), ensure_ascii=False, indent=1, default=str))
    elif a.cmd == "reconciliar-mensaje":
        print(json.dumps(bloque.mensajeria.reconciliar(a.msg_id, a.motivo), ensure_ascii=False, indent=1))
    elif a.cmd == "seguimiento":
        print(json.dumps(_seguimiento(bloque, a, as_of), ensure_ascii=False, indent=1, default=str))
    elif a.cmd == "consulta-broker":
        print(json.dumps(_consulta_broker(bloque, a, as_of), ensure_ascii=False, indent=1, default=str))
    elif a.cmd == "credencial":
        print(json.dumps(_credencial(bloque, a, as_of), ensure_ascii=False, indent=1, default=str))
    elif a.cmd == "guia":
        print(json.dumps(_guia(bloque, a, as_of), ensure_ascii=False, indent=1, default=str))
    return 0


def _json(a) -> dict:
    if not a.json:
        return {}
    p = Path(a.json)
    return json.loads(p.read_text(encoding="utf-8") if p.exists() else a.json)


def _seguimiento(bloque, a, as_of) -> object:
    s = bloque.seguimientos
    acciones = {"alta": "ALTA", "modificar": "MODIFICACION", "pausar": "PAUSA", "reanudar": "REANUDACION", "cancelar": "CANCELACION"}
    if a.accion in acciones:
        ct24 = {**_json(a), "accion": acciones[a.accion]}
        if a.seg:
            ct24["seg_id"] = a.seg
        return s.procesar(ct24, as_of)
    if a.accion == "ejecutar":
        return [{k: v for k, v in r.items() if k not in ("informe", "validacion")} for r in s.ejecutar(as_of, a.seg, a.forzar)]
    if a.accion == "responder":
        if not (a.seg and a.decision):
            sys.exit("responder necesita --seg y --decision")
        return s.respuesta_broker(a.seg, a.decision, as_of=as_of)
    return {k: {c: v.get(c) for c in ("opp_id", "estado", "frecuencia", "proximo_ciclo", "ciclos", "ultima_recomendacion", "fecha_fin")}
            for k, v in s.encargos().items()}


def _consulta_broker(bloque, a, as_of) -> object:
    c = bloque.consultas
    if a.accion == "enviar":
        return c.enviar(_json(a), as_of)
    if a.accion == "responder":
        d = _json(a)
        return c.responder(a.cns or d.get("cns_id"), d.get("respuestas", []), d.get("estado", "RESPONDIDA"), as_of)
    if a.accion == "entrante":
        d = _json(a)
        return c.entrante(d.get("contenido", ""), d.get("referencia"), as_of)
    if a.accion == "vencer":
        bloque.fijar_fecha(as_of)
        return {"vencidas": c.vencer(as_of)}
    if a.accion == "revisiones":   # T-174 r02 (H-06): revisiones C2 que no han llegado al Broker
        return c.revisiones_pendientes()
    if a.accion == "relanzar":
        estados = ("INTERRUMPIDA", "PENDIENTE", "FALLIDA") + (("EN_CURSO",) if a.incluir_en_curso else ())
        return c.relanzar_revisiones(as_of, cns_id=a.cns, estados=estados)
    return {k: {x: v.get(x) for x in ("sentido", "tipo", "modo", "estado", "plazo_respuesta", "run_id", "clases")} for k, v in c._todas().items()}


def _guia(bloque, a, as_of) -> object:
    bloque.fijar_fecha(as_of)
    if a.accion == "emitir":
        d = _json(a)
        if not a.receptor or not isinstance(d, dict):
            sys.exit("emitir necesita --receptor y --json con {items, fecha_aplicacion}")
        from .contratos import MensajeInvalido
        try:   # T-161 (H-05): un cuerpo inválido o un ítem en conflicto no se emite y la orden termina con el motivo
            return bloque.guias.emitir(a.receptor, d.get("items"), as_of=as_of, fecha_aplicacion=d.get("fecha_aplicacion"),
                                       simular_fallo_del_emisor=a.simular_fallo_del_emisor)
        except MensajeInvalido as e:
            sys.exit(f"guia emitir: no se emite: {e}")
    return {k: {c: v.get(c) for c in ("agente", "version", "estado", "fecha_aplicacion", "sustituye", "sustituida_por", "motivo")}
            for k, v in bloque.guias.todas().items()}


def _credencial(bloque, a, as_of) -> object:
    c = bloque.credenciales
    if a.accion == "solicitar":
        if not a.servicio:
            sys.exit("solicitar necesita --servicio")
        return c.solicitar(a.servicio, a.solicitante, a.uso, a.impacto, as_of=as_of)
    if a.accion == "depositar":
        # Simula el procedimiento seguro del Broker: el valor nunca se escribe en mensajes, archivos del bloque ni salidas
        valor = os.environ.get(a.valor_desde_entorno) if a.valor_desde_entorno else getpass.getpass("Credencial (sin eco): ")
        if not valor:
            sys.exit("Sin valor de credencial")
        return c.depositar(a.crd, valor, a.caducidad, as_of)
    if a.accion == "responder":
        return c.responder({"crd_id": a.crd, "estado": a.estado_credencial, "credencial_ref": None}, as_of)
    if a.accion == "c4":
        from .mantenimiento_c4 import mantenimiento_c4
        return mantenimiento_c4(bloque, as_of)
    if a.accion == "recordatorios":
        bloque.fijar_fecha(as_of)
        return {"recordatorios": c.recordatorios(as_of)}
    bloque.fijar_fecha(as_of)
    return c.estado(a.servicio)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
