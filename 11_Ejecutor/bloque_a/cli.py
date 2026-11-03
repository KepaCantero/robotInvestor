"""CLI «bloque-a»: ciclo, peticion, consulta, decision, evaluar, estado, verificar-enlaces, backtest, generar-sinteticos."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

import pandas as pd

from .configuracion import RUTA_UNIVERSO_EJEMPLO, DIR_EJECUTOR, cargar_config, ruta


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


def main(argv: Optional[List[str]] = None) -> int:
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
    p = sub.add_parser("verificar-enlaces", help="HT-02 sobre F7, F8, F9 y FM")
    p.add_argument("--aplicar", action="store_true", help="Escribe los estados en los archivos (por defecto solo informe)")
    p = sub.add_parser("backtest", help="Backtest sobre fechas as_of")
    p.add_argument("--desde", required=True)
    p.add_argument("--hasta", required=True)
    p.add_argument("--frecuencia", choices=["diaria", "semanal", "quincenal", "mensual"])
    p.add_argument("--clases", help="Lista separada por comas (RV,RF,…)")
    p.add_argument("--sin-resolucion-final", action="store_true")
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
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
