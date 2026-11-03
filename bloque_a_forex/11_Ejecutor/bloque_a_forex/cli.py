"""CLI «bloque-a-forex»: ciclo, peticion, consulta, decision, evaluar, estado, verificar-enlaces, backtest, generar-sinteticos y,
desde V1.1, seguimiento (CT-24, ciclo C6, F11), consulta-broker (CT-23) y credencial (CT-25, bóveda simulada de HT-01)."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Optional

import pandas as pd

from .configuracion import RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR, cargar_config, ruta


def _resumen_run(r: dict) -> dict:
    return {"run_id": r["run_id"], "as_of": r["as_of"], "estado": r["estado"], "entrega": r.get("entrega", "ENTREGADA"),
            "nivel_por_segmento": r["nivel_por_segmento"], "g3": (r.get("g3_entregables") or r["g3"]).get("dictamen"),
            "top3_por_segmento": {c: [o["opp_id"] for o in d["opciones"]] for c, d in r["paquete"]["segmentos"].items()},
            "entregables": r.get("entregables"), "consumo_uc": (r.get("consumo") or {}).get("uc")}


def _bloque(a, cfg):
    from .herramientas.ht01_datos import ProveedorCSV, ProveedorYahoo, cargar_universo
    from .llm import crear_cliente
    from .orquestacion import Bloque
    uni = cargar_universo(a.universo)
    if a.proveedor == "yahoo":
        from .herramientas.ht01_datos import simbolos_sinteticos
        prov = ProveedorYahoo(list(simbolos_sinteticos(uni)), cfg.get("modo", "vivo"))
    else:
        if not a.datos:
            sys.exit("Falta --datos CARPETA (CSV por símbolo) o --proveedor yahoo")
        prov = ProveedorCSV(a.datos)
    cli = crear_cliente(a.cliente, cfg, a.replay, a.replay_modo)
    return Bloque(cfg, prov, uni, cli, a.estado or (cfg["rutas"]["almacen"]), a.salida or cfg["rutas"]["entregables"], anonimizar=a.anonimizar)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="bloque-a-forex", description="Ejecutor programático del Bloque A Forex (Robot Investor)")
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
    p = sub.add_parser("ciclo", help="Ciclo periódico C1")
    p.add_argument("--segmentos", help="Segmentos separados por comas (G10N,G10M,EMAS,EMLA,EMEA,ESTR); por defecto, los activos en F10")
    p = sub.add_parser("peticion", help="Petición ad hoc CT-01")
    p.add_argument("--json", required=True)
    p = sub.add_parser("consulta", help="Consulta CT-03")
    p.add_argument("texto")
    p.add_argument("--sin-escalado", action="store_true")
    p = sub.add_parser("decision", help="Decisiones y configuración CT-04")
    p.add_argument("--json", required=True)
    sub.add_parser("evaluar", help="C5: resolución de pronósticos, métricas, certificados y lecciones")
    sub.add_parser("estado", help="Colas, consumo y últimos runs")
    p = sub.add_parser("verificar-enlaces", help="HT-02 sobre F7, F8, F9 y FM")
    p.add_argument("--aplicar", action="store_true", help="Escribe los estados en los archivos (por defecto solo informe)")
    p = sub.add_parser("backtest", help="Backtest sobre fechas as_of")
    p.add_argument("--desde", required=True)
    p.add_argument("--hasta", required=True)
    p.add_argument("--frecuencia", choices=["diaria", "semanal", "quincenal", "mensual"])
    p.add_argument("--segmentos", help="Segmentos separados por comas (G10N,G10M,EMAS,EMLA,EMEA,ESTR)")
    p.add_argument("--sin-resolucion-final", action="store_true")
    # --- V1.1 ---------------------------------------------------------------------------------
    p = sub.add_parser("seguimiento", help="CT-24: encargos de seguimiento de opción (F11) y ciclos C6")
    ss = p.add_subparsers(dest="accion", required=True)
    q = ss.add_parser("alta", help="Alta de un encargo (Broker → Coordinador)")
    q.add_argument("--opp-id", required=True)
    q.add_argument("--frecuencia", default="SEMANAL", help="DIARIA, SEMANAL, QUINCENAL, MENSUAL, TRIMESTRAL o PERSONALIZADA")
    q.add_argument("--calendario", help="PERSONALIZADA: fechas AAAA-MM-DD separadas por comas, o un número de días")
    q.add_argument("--motivo", default="Seguimiento encargado por el Broker")
    q.add_argument("--senal", action="append", default=[], help="Señal de interés (repetible), p. ej. «USDJPY por debajo de 140»")
    q.add_argument("--fecha-fin")
    for nombre, ayuda in (("modificar", "Modificación"), ("pausar", "Pausa"), ("reanudar", "Reanudación"),
                          ("cancelar", "Cancelación (efecto inmediato)")):
        q = ss.add_parser(nombre, help=ayuda)
        q.add_argument("--seg-id", required=True)
        q.add_argument("--motivo")
        if nombre == "modificar":
            q.add_argument("--frecuencia")
            q.add_argument("--calendario")
            q.add_argument("--senal", action="append")
            q.add_argument("--fecha-fin")
    q = ss.add_parser("ejecutar", help="Ciclo C6 con informe de seguimiento de opción")
    g = q.add_mutually_exclusive_group(required=True)
    g.add_argument("--seg-id")
    g.add_argument("--pendientes", action="store_true", help="Todos los encargos activos con ciclo vencido (HT-05)")
    q.add_argument("--forzar", action="store_true", help="Ejecuta aunque la opción sea VIGENTE en el top-3")
    q = ss.add_parser("responder", help="Respuesta del Broker a la recomendación de un ciclo (CT-22 DECISION_SEGUIMIENTO)")
    q.add_argument("--seg-id", required=True)
    q.add_argument("--run-id", required=True)
    q.add_argument("--decision", required=True)
    q.add_argument("--comentario")
    ss.add_parser("listar", help="Encargos de F11")
    p = sub.add_parser("consulta-broker", help="CT-23: consultas del bloque al Broker y aportaciones del Broker")
    ss = p.add_subparsers(dest="accion", required=True)
    q = ss.add_parser("crear", help="Consulta saliente (ya filtrada y agrupada por el Analizador)")
    q.add_argument("--tipo", default="ACLARACION_ALCANCE",
                   help="ACLARACION_ALCANCE, DATO_O_DOCUMENTO, PREFERENCIA_O_CRITERIO, CONFIRMACION_SUPUESTO u OTRA")
    q.add_argument("--modo", default="NO_BLOQUEANTE", choices=["BLOQUEANTE", "NO_BLOQUEANTE"])
    q.add_argument("--pregunta", required=True)
    q.add_argument("--supuesto", required=True, help="Supuesto declarado que se aplica si no hay respuesta (R26)")
    q.add_argument("--efecto", help="Efecto si el supuesto fuera falso")
    q.add_argument("--origen", default="AG-02")
    q.add_argument("--run-id")
    q.add_argument("--seg-id")
    q.add_argument("--segmento", help="Segmento que se pausa si la consulta es BLOQUEANTE (punto de control)")
    q.add_argument("--punto-control")
    q = ss.add_parser("responder", help="Respuesta del Broker")
    q.add_argument("--cns-id", required=True)
    q.add_argument("--respuesta", required=True)
    q.add_argument("--parcial", action="store_true")
    ss.add_parser("vencer", help="Marca vencidas las consultas fuera de plazo (se aplica el supuesto declarado)")
    q = ss.add_parser("entrante", help="Aportación espontánea del Broker (dato, documento o preferencia)")
    q.add_argument("--contenido", required=True)
    q.add_argument("--run-id")
    q.add_argument("--opp-id")
    q.add_argument("--seg-id")
    ss.add_parser("listar")
    p = sub.add_parser("credencial", help="CT-25: solicitud y provisión de credenciales (bóveda simulada de HT-01)")
    ss = p.add_subparsers(dest="accion", required=True)
    q = ss.add_parser("solicitar")
    q.add_argument("--servicio", required=True)
    q.add_argument("--uso", required=True)
    q.add_argument("--solicitante", default="AG-16")
    q.add_argument("--impacto", required=True)
    q.add_argument("--urgencia", default="NORMAL", choices=["ALTA", "NORMAL"])
    q.add_argument("--forzar", action="store_true", help="Volver a pedir una credencial denegada (cambio de circunstancias)")
    q = ss.add_parser("responder", help="Respuesta del Broker: PROVISTA (deposita en la bóveda), DENEGADA o APLAZADA")
    q.add_argument("--crd-id", required=True)
    q.add_argument("--respuesta", required=True, choices=["PROVISTA", "DENEGADA", "APLAZADA"])
    q.add_argument("--valor-env", help="Variable de entorno con la clave (nunca en la línea de órdenes ni en un mensaje)")
    q.add_argument("--caducidad")
    q = ss.add_parser("estado")
    q.add_argument("--servicio")
    ss.add_parser("recordatorios")
    p = sub.add_parser("generar-sinteticos", help="Escribe tipos de cambio, índices y tipos de interés sintéticos (CSV) del universo")
    p.add_argument("--desde", default="2022-01-03")
    p.add_argument("--hasta", default="2026-10-30")
    p.add_argument("--semilla", type=int, default=7)
    a = ap.parse_args(argv)
    cfg = cargar_config(a.config)

    if a.cmd == "generar-sinteticos":
        from .herramientas.ht01_datos import ProveedorSintetico, cargar_universo
        from .herramientas.ht01_datos import simbolos_sinteticos
        u = cargar_universo(a.universo)
        dest = a.salida or str(DIR_EJECUTOR / "ejemplos" / "datos_sinteticos")
        sims = simbolos_sinteticos(u)
        ProveedorSintetico(sims, a.semilla, a.desde, a.hasta).escribir_csv(dest)
        print(json.dumps({"salida": dest, "simbolos": len(u), "tipos_de_interes": sum(1 for k in sims if k.startswith("TIPO-"))},
                         ensure_ascii=False))
        return 0
    if a.cmd == "backtest":
        from .backtest import ejecutar_backtest
        if not a.datos or not a.salida:
            sys.exit("backtest necesita --datos y --salida")
        r = ejecutar_backtest(cfg, a.desde, a.hasta, a.datos, a.universo, a.salida, a.frecuencia,
                              [x.strip().upper() for x in a.segmentos.split(",")] if a.segmentos else None, tipo_cliente=a.cliente, replay=a.replay,
                              replay_modo=a.replay_modo, anonimizar=a.anonimizar, resolver_al_final=not a.sin_resolucion_final,
                              progreso=lambda res: print(f"{res['as_of']} {res['run_id']} {res['estado']}", file=sys.stderr))
        r.pop("bloque")
        r.pop("metricas")
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "verificar-enlaces":
        from .herramientas import ht02
        from .referencias import ARCHIVOS_REF, localizar
        base = ruta(cfg, "archivos_operativos")
        out = Path(a.salida or ".")
        out.mkdir(parents=True, exist_ok=True)
        codigo = 0
        for k, nombre in ARCHIVOS_REF.items():
            args = [str(localizar(base, nombre)), "--salida-json", str(out / f"ht02_{k}.json")] + (["--aplicar"] if a.aplicar else [])
            codigo = max(codigo, ht02.main(args) or 0)
        return codigo
    bloque = _bloque(a, cfg)
    as_of = pd.Timestamp(a.as_of) if a.as_of else pd.Timestamp.today().normalize()
    if a.cmd == "ciclo":
        alcance = {"segmentos": [x.strip().upper() for x in a.segmentos.split(",")]} if a.segmentos else None
        print(json.dumps(_resumen_run(bloque.ciclo(as_of, alcance=alcance)), ensure_ascii=False, indent=1))
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
    elif a.cmd == "seguimiento":
        print(json.dumps(_seguimiento(bloque, a, as_of), ensure_ascii=False, indent=1, default=str))
    elif a.cmd == "consulta-broker":
        print(json.dumps(_consulta_broker(bloque, a, as_of), ensure_ascii=False, indent=1, default=str))
    elif a.cmd == "credencial":
        print(json.dumps(_credencial(bloque, a, as_of), ensure_ascii=False, indent=1, default=str))
    return 0


def _calendario(txt):
    if not txt:
        return None
    return {"dias": int(txt)} if str(txt).isdigit() else [x.strip() for x in str(txt).split(",") if x.strip()]


def _seguimiento(bloque, a, as_of) -> dict:
    s = bloque.seguimientos
    if a.accion == "alta":
        return s.tramitar({"accion": "ALTA", "opp_id": a.opp_id, "frecuencia": a.frecuencia.upper(), "motivo": a.motivo,
                           "calendario_personalizado": _calendario(a.calendario), "senales_interes": a.senal,
                           "fecha_fin": a.fecha_fin}, as_of)
    if a.accion in ("modificar", "pausar", "reanudar", "cancelar"):
        accion = {"modificar": "MODIFICACION", "pausar": "PAUSA", "reanudar": "REANUDACION", "cancelar": "CANCELACION"}[a.accion]
        ct = {"accion": accion, "seg_id": a.seg_id, "motivo": a.motivo}
        if a.accion == "modificar":
            for k, v in (("frecuencia", a.frecuencia and a.frecuencia.upper()), ("calendario_personalizado", _calendario(a.calendario)),
                         ("senales_interes", a.senal), ("fecha_fin", a.fecha_fin)):
                if v:
                    ct[k] = v
        return s.tramitar(ct, as_of)
    if a.accion == "ejecutar":
        if a.pendientes:
            return {"ciclos": [{k: v for k, v in r.items() if k != "informe_json"} for r in s.ejecutar_pendientes(as_of)]}
        r = s.ejecutar(a.seg_id, as_of, forzar=a.forzar)
        return {k: v for k, v in r.items() if k != "informe_json"}
    if a.accion == "responder":
        return s.responder(a.seg_id, a.run_id, a.decision, as_of, a.comentario)
    return {k: {x: e.get(x) for x in ("opp_id", "estado", "frecuencia", "proximo_ciclo", "ciclos", "aviso")} for k, e in s.encargos(as_of).items()}


def _consulta_broker(bloque, a, as_of) -> dict:
    c = bloque.consultas
    if a.accion == "crear":
        r = c.crear([{"texto": a.pregunta, "origen": a.origen, "supuesto_declarado": a.supuesto,
                      "efecto_si_falso": a.efecto or "Habría que revisar las conclusiones que dependen de este supuesto"}],
                    a.tipo, a.modo, as_of, run_id=a.run_id, seg_id=a.seg_id, segmento=a.segmento, punto_control=a.punto_control)
        r.pop("mensaje", None)
        return r
    if a.accion == "responder":
        return c.responder(a.cns_id, [{"indice": 0, "texto": a.respuesta}], as_of, parcial=a.parcial)
    if a.accion == "vencer":
        return {"vencidas": c.vencer(as_of)}
    if a.accion == "entrante":
        return c.entrante(a.contenido, as_of, run_id=a.run_id, opp_id=a.opp_id, seg_id=a.seg_id)
    return {k: {x: v.get(x) for x in ("sentido", "tipo", "modo", "estado", "run_id", "segmento", "plazo_respuesta")}
            for k, v in c.todas(as_of).items()}


def _credencial(bloque, a, as_of) -> dict:
    c = bloque.credenciales
    if a.accion == "solicitar":
        return c.solicitar(a.servicio, a.uso, a.solicitante, a.impacto, a.urgencia, as_of, forzar=a.forzar)
    if a.accion == "responder":
        valor = os.environ.get(a.valor_env) if a.valor_env else None
        if a.valor_env and not valor:
            sys.exit(f"La variable de entorno {a.valor_env} está vacía")
        return c.responder(a.crd_id, a.respuesta, as_of, valor=valor, caducidad=a.caducidad)
    if a.accion == "estado":
        if a.servicio:
            return c.estado_servicio(a.servicio)
        return {k: {x: v.get(x) for x in ("servicio", "estado", "credencial_ref", "solicitante")} for k, v in c.todas(as_of).items()}
    return {"recordatorios": c.recordatorios(as_of)}


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
