"""Línea de comandos `bloque-b` (Documento 0 del Bloque B V2.1, 18.4): analizar, autorizar, consulta, decision,
seguimiento (CT-B-29: alta, modificar, pausar, reanudar, cancelar, ciclo, pendientes, listar), consulta-broker (CT-B-28:
responder, aporte, revisar, listar), vigia (ronda del Vigía, fase F11), evaluar, estado, verificar-enlaces, backtest y
generar-sinteticos. La salida es JSON por stdout (integrable con n8n)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Sequence

from .configuracion import cargar_config


def _entorno(a, modo: Optional[str] = None):
    from .entorno import Entorno
    cfg = cargar_config(a.config)
    return Entorno(cfg, estado=a.estado, salida=a.salida, datos=a.datos, cliente=a.cliente, replay=a.replay, replay_modo=a.replay_modo,
                   as_of=a.as_of, modo=modo, boveda=a.boveda)


def _json(ruta: str):
    return json.loads(Path(ruta).read_text(encoding="utf-8"))


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="bloque-b", description="Ejecutor del Bloque B (Robot Investor) · V1.1 (Bloque B V2.1)")
    ap.add_argument("--config", help="YAML que se fusiona con config/por_defecto.yaml")
    ap.add_argument("--cliente", default="mock", choices=("mock", "anthropic", "replay"))
    ap.add_argument("--replay", help="Archivo JSONL de grabación (cliente replay)")
    ap.add_argument("--replay-modo", default="reproducir", choices=("grabar", "reproducir"))
    ap.add_argument("--datos", help="Carpeta de CSV por símbolo (HT-01); sin ella, series sintéticas en memoria")
    ap.add_argument("--estado", default="./estado_bloque_b", help="Directorio de F1–F6, F10, RC, HA y puntos de control")
    ap.add_argument("--salida", default="./entregables", help="Carpeta ENT de entregables y alertas")
    ap.add_argument("--as-of", help="Fecha de corte (AAAA-MM-DD); por defecto, hoy")
    ap.add_argument("--boveda", help="Archivo de la bóveda simulada (permisos 600); alternativa: BLOQUE_B_BOVEDA_<ALIAS>")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("analizar", help="Petición de análisis (CT-B-01)")
    s.add_argument("--json", required=True)
    s = sub.add_parser("autorizar", help="Decisión del Broker sobre una autorización pendiente (CT-B-05)")
    s.add_argument("--aut", required=True)
    s.add_argument("--opcion", required=True, choices=("CONTINUAR", "VERSION_30_MIN", "DIVIDIR_EN_FASES", "HASTA_PV2", "CANCELAR"))
    s.add_argument("--minutos", type=float)
    s.add_argument("--decidido-por", default="BROKER", choices=("BROKER", "USUARIO_VIA_BROKER"))
    s.add_argument("--motivo")
    s = sub.add_parser("consulta", help="Consulta N0 (CT-B-03)")
    s.add_argument("pregunta")
    s.add_argument("--contexto", help="REC-B o PET-B de referencia")
    s = sub.add_parser("decision", help="Decisiones, resultados, configuración, credenciales y forzar continuación (CT-B-04, CT-B-06)")
    s.add_argument("--json", required=True)
    s = sub.add_parser("seguimiento", help="Seguimiento encargado por el Broker (CT-B-29, archivo F11, ciclos N1-SEG)")
    s.add_argument("accion", choices=("alta", "modificar", "pausar", "reanudar", "cancelar", "ciclo", "pendientes", "listar"))
    s.add_argument("--json", help="Encargo CT-B-29 (alta o modificar)")
    s.add_argument("--seg", help="SEG-B del seguimiento")
    s.add_argument("--motivo")
    s = sub.add_parser("consulta-broker", help="Consultas del bloque al Broker y aportes (CT-B-28)")
    s.add_argument("accion", choices=("responder", "aporte", "revisar", "listar"))
    s.add_argument("--cns", help="CNS-B de la consulta")
    s.add_argument("--respuesta")
    s.add_argument("--forzar-continuacion", action="store_true", help="La respuesta ordena forzar la continuación tras PV2")
    s.add_argument("--motivo")
    s.add_argument("--json", help="Aporte entrante del Broker (pet_id o seg_id, naturaleza, contenido)")
    s.add_argument("--pet")
    sub.add_parser("vigia", help="Ronda del Vigía sobre las REC-B entregadas (fase F11; solo alertas, R32)")
    sub.add_parser("evaluar", help="Resolución de pronósticos y rankings vencidos, métricas y lecciones (F12)")
    s = sub.add_parser("estado", help="Estado del servicio")
    s.add_argument("--pet")
    s.add_argument("--config", dest="ver_config", action="store_true")
    s = sub.add_parser("verificar-enlaces", help="Barrido HT-02 de F7, F8, F9 y FM (F13)")
    s.add_argument("--aplicar", action="store_true")
    s.add_argument("--con-red", action="store_true", help="Comprueba los enlaces en la red (por defecto solo lee las fichas)")
    s.add_argument("--max-fichas", type=int)
    s = sub.add_parser("backtest", help="Backtest de rankings y pronósticos sin anticipación")
    s.add_argument("--peticion", required=True)
    s.add_argument("--desde", required=True)
    s.add_argument("--hasta", required=True)
    s.add_argument("--frecuencia", default="mensual", choices=("mensual", "semanal", "diaria"))
    s.add_argument("--solo-seleccion", action="store_true", help="Solo la selección determinista (HT-11, Motor, HT-03), sin agentes")
    s = sub.add_parser("generar-sinteticos", help="Escribe las series sintéticas de los universos y ámbitos de ejemplo en CSV")
    s.add_argument("--salida", dest="salida_sint", required=True)
    s.add_argument("--semilla", type=int, default=None)
    a = ap.parse_args(argv)
    if a.cmd == "generar-sinteticos":
        from .entorno import proveedor_sintetico
        prov = proveedor_sintetico(cargar_config(a.config), semilla=a.semilla)
        rutas = prov.escribir_csv(a.salida_sint)
        print(json.dumps({"series": len(rutas), "carpeta": a.salida_sint, "aviso": "Series ficticias: solo para pruebas"}, ensure_ascii=False))
        return 0
    from .orquestacion import Coordinador
    ent = _entorno(a, "backtest" if a.cmd == "backtest" else None)
    coord = Coordinador(ent)
    if a.cmd == "analizar":
        res = coord.recibir(_json(a.json))
    elif a.cmd == "autorizar":
        res = coord.autorizar(a.aut, a.opcion, a.minutos, a.decidido_por, a.motivo)
    elif a.cmd == "consulta":
        from .broker import consulta
        res = consulta(ent, coord, a.pregunta, a.contexto)
    elif a.cmd == "decision":
        from .broker import decision
        res = decision(ent, _json(a.json), coord)
    elif a.cmd == "seguimiento":
        from . import seguimiento as sg
        if a.accion == "alta":
            res = sg.encargo(ent, coord, dict(_json(a.json), accion="ALTA"))
        elif a.accion == "modificar":
            d = _json(a.json)
            res = sg.encargo(ent, coord, dict(d, accion="MODIFICACION", seg_id=a.seg or d.get("seg_id")))
        elif a.accion in ("pausar", "reanudar", "cancelar"):
            acc = {"pausar": "PAUSA", "reanudar": "REANUDACION", "cancelar": "CANCELACION"}[a.accion]
            res = sg.encargo(ent, coord, {"accion": acc, "seg_id": a.seg, "motivo": a.motivo})
        elif a.accion == "ciclo":
            res = sg.ciclo(ent, coord, a.seg)
        elif a.accion == "pendientes":
            res = sg.pendientes(ent, coord)
        else:
            res = sg.listar(ent)
    elif a.cmd == "consulta-broker":
        if a.accion == "responder":
            res = coord.responder_consulta(a.cns, a.respuesta or "", a.forzar_continuacion, a.motivo)
        elif a.accion == "aporte":
            res = coord.aporte_broker(_json(a.json))
        elif a.accion == "revisar":
            res = {"cerradas_por_plazo": coord.revisar_consultas()}
        else:
            res = {"consultas": [{k: e.get(k) for k in ("id", "pet_id", "seg_id", "sentido", "tipo", "modo", "estado", "plazo", "supuesto", "efecto")}
                                 for e in ent.alm.estado("F1", tipo="CONSULTA_BROKER").values() if not a.pet or e.get("pet_id") == a.pet]}
    elif a.cmd == "vigia":
        from .vigia import ronda
        res = ronda(ent, coord)
    elif a.cmd == "evaluar":
        from .evaluador import evaluar
        res = evaluar(ent, coord)
    elif a.cmd == "estado":
        from .broker import estado
        res = estado(ent, coord, a.pet, a.ver_config)
    elif a.cmd == "verificar-enlaces":
        from .broker import verificar_enlaces
        res = verificar_enlaces(ent, coord, a.aplicar, not a.con_red, a.max_fichas)
    elif a.cmd == "backtest":
        from .backtest import backtest
        res = backtest(ent, coord, _json(a.peticion), a.desde, a.hasta, a.frecuencia, a.solo_seleccion, a.salida)
    else:  # pragma: no cover
        ap.error("subcomando desconocido")
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
