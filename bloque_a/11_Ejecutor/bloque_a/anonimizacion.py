"""Anonimización de símbolos y nombres en lo que ven los agentes (mitigación PARCIAL de la fuga por
conocimiento del modelo en backtest).

Qué hace: sustituye cada símbolo y nombre del universo por un alias neutro por clase («RV03», «Activo RV03»)
en todos los textos enviados a los agentes, reexpresa los niveles de precio en base 100 y deshace la
sustitución en las respuestas (proxy_backtest, umbrales de invalidación, fuentes HT-01).

Límites (declarados en el README): la clase, la región, el sector y el tipo de opción se mantienen (sin ellos
el análisis por clase pierde sentido) y pueden bastar para identificar el activo; las fechas no se desplazan;
la forma de la serie (rentabilidades, caídas, volatilidad) puede delatar episodios conocidos (p. ej., marzo de
2020); el modelo puede razonar con su conocimiento general del periodo aunque no sepa el activo.
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
        for _, f in universo.sort_values(["clase", "simbolo"]).iterrows():
            cont[f["clase"]] = cont.get(f["clase"], 0) + 1
            alias = f"{f['clase']}{cont[f['clase']]:02d}"
            self.a_alias[f["simbolo"]] = alias
            self.de_alias[alias] = f["simbolo"]
            self.nombres[f["nombre"]] = f"Activo {alias}"
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
                s = re.sub(r"(?<![\w-])Activo " + re.escape(a) + r"(?![\w-])", sym, s)
                s = re.sub(r"(?<![\w-])" + re.escape(a) + r"(?![\w-])", sym, s)
            return s
        if isinstance(obj, list):
            return [self.salida(x) for x in obj]
        if isinstance(obj, dict):
            return {k: self.salida(v) for k, v in obj.items()}
        return obj
