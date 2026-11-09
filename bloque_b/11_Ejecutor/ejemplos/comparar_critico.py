"""Experimento pareado con informes ficticios de pedidos de equipos eléctricos.

Desde 11_Ejecutor: PYTHONPATH=. python ejemplos/comparar_critico.py
Con el cliente real: añadir --cliente anthropic --modelo IDENTIFICADOR.
Cada llamada es independiente. Revisar las objeciones y su fuerza: ¿identifican el
origen del incremento y explican qué implica para repetirlo? Una advertencia
genérica sobre el ciclo en ambos informes no distingue los casos.
"""
import argparse
import json

from bloque_b.agentes import Invocador
from bloque_b.configuracion import cargar_config, modelo_de
from bloque_b.llm import crear_cliente
from bloque_b.prompts import CatalogoPrompts

DESGLOSES = {
    "A": "Los 20 millones adicionales corresponden a entregas anuales contratadas durante tres años.",
    "B": "Los 20 millones adicionales corresponden a una entrega puntual ya completada, sin entregas futuras contratadas.",
}


def comparar(cliente, modelo=None):
    cfg = cargar_config()
    if modelo:
        cfg["modelos"]["AG-B14"] = modelo
    resultados = {}
    for caso, desglose in DESGLOSES.items():
        inv = Invocador(cfg, crear_cliente(cliente, cfg), CatalogoPrompts(cfg, cliente), modo="backtest")
        tesis = {
            "enunciado": "La facturación anual de los fabricantes de equipos eléctricos puede mantenerse en 120 millones.",
            "premisas": [{"premisa": "El incremento de ingresos se mantendrá el próximo ejercicio.",
                          "comprobacion": "Informe ficticio al cierre de 2024. La facturación anual pasó de 100 a 120 millones de euros. " + desglose}],
        }
        # Los identificadores de caso y el criterio de evaluación no se envían al agente.
        respuesta = inv.llamar(
            "AG-B14", "CT-B-17", "refutacion",
            {"pet_id": "PET-B-2025-0001", "tesis": tesis, "hipotesis": [], "escenarios": [], "finalistas": []},
            "Refuta la tesis y los finalistas; gradúa las objeciones (fuerte, moderada, débil).",
            {"objeciones": "array", "veredicto_tesis": "string"},
            {"fecha_as_of": "2025-01-31", "lecciones": [], "f10": {"methodology_version": cfg.get("methodology_version")}},
        )
        if respuesta.get("_no_conforme"):
            raise ValueError(f"Respuesta no conforme en el caso {caso}: no se puede evaluar la pareja.")
        resultados[caso] = {"tesis_enviada": tesis, "respuesta": respuesta}
    return {"cliente": cliente, "modelo": modelo_de(cfg, "AG-B14") if cliente != "mock" else None, "casos": resultados}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cliente", choices=("mock", "anthropic"), default="mock")
    parser.add_argument("--modelo", help="Identificador del modelo para el cliente real")
    args = parser.parse_args()
    print(json.dumps(comparar(args.cliente, args.modelo), ensure_ascii=False, indent=2))
