"""Anonimización de códigos y nombres de los indicadores en lo que ven los agentes (mitigación PARCIAL de la fuga
por conocimiento del modelo en backtest).

Qué hace: sustituye cada código y nombre del universo por un alias neutro por segmento («G10N03», «Ámbito G10N03»)
en todos los textos enviados a los agentes, reexpresa los niveles del indicador en base 100 y deshace la sustitución
en las respuestas (indicador de seguimiento, umbrales de invalidación, fuentes HT-01).

Límites (declarados en el README): en divisas la mitigación es todavía más débil que en otros mercados, porque el
segmento, el tipo de opción, el par y la composición (códigos ISO 4217) se mantienen —sin ellos no hay análisis
cambiario— y bastan para identificar el ámbito; las fechas no se desplazan; los tipos de interés de cada divisa
delatan el periodo; la forma de la serie puede delatar episodios conocidos (p. ej., la ruptura del suelo del franco
suizo en 2015 o el desplome de la libra en 2022).
"""
from __future__ import annotations

import re
from typing import Any, Dict

import pandas as pd


class Anonimizador:
    def __init__(self, universo: pd.DataFrame) -> None:
        self.a_alias: Dict[str, str] = {}
        self.de_alias: Dict[str, str] = {}
        self.nombres: Dict[str, str] = {}
        cont: Dict[str, int] = {}
        for _, f in universo.sort_values(["segmento", "simbolo"]).iterrows():
            cont[f["segmento"]] = cont.get(f["segmento"], 0) + 1
            alias = f"{f['segmento']}{cont[f['segmento']]:02d}"
            self.a_alias[f["simbolo"]] = alias
            self.de_alias[alias] = f["simbolo"]
            if f["nombre"] and f["nombre"] != f.get("simbolo") and "/" not in f["nombre"]:
                self.nombres[f["nombre"]] = f"Ámbito {alias}"
        pares = [(s, a) for s, a in self.a_alias.items()] + list(self.nombres.items())
        pares.sort(key=lambda kv: -len(kv[0]))
        self._ida = [(re.compile(r"(?<![\w-])" + re.escape(k) + r"(?![\w-])"), v) for k, v in pares]
        self._vuelta = sorted(self.de_alias.items(), key=lambda kv: -len(kv[0]))
        self.factores: Dict[str, float] = {}   # símbolo -> factor de rebase (100 / precio as_of)

    def texto(self, s: str) -> str:
        for rx, v in self._ida:
            s = rx.sub(v, s)
        return s

    def entrada(self, obj: Any) -> Any:
        if isinstance(obj, str):
            return self.texto(obj)
        if isinstance(obj, list):
            return [self.entrada(x) for x in obj]
        if isinstance(obj, dict):
            return {k: self.entrada(v) for k, v in obj.items()}
        return obj

    def simbolo(self, alias_o_simbolo: str) -> str:
        return self.de_alias.get(alias_o_simbolo, alias_o_simbolo)

    def salida(self, obj: Any) -> Any:
        if isinstance(obj, str):
            if obj in self.de_alias:
                return self.de_alias[obj]
            s = obj
            for a, sym in self._vuelta:
                s = re.sub(r"(?<![\w-])Ámbito " + re.escape(a) + r"(?![\w-])", sym, s)
                s = re.sub(r"(?<![\w-])" + re.escape(a) + r"(?![\w-])", sym, s)
            return s
        if isinstance(obj, list):
            return [self.salida(x) for x in obj]
        if isinstance(obj, dict):
            return {k: self.salida(v) for k, v in obj.items()}
        return obj
