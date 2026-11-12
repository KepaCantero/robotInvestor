"""Registro de experimentos (T-99; decisión 5 de la tanda 1, D-53 propuesta): toda prueba que pueda cambiar cómo decide o cuánto
cuesta el robot se prerregistra y se sella ANTES de ejecutarse, y cuentan todos sus intentos, también los fallidos.

Fichero de solo anexar, una línea JSON por anotación, encadenada por huellas (`_seq`, `_hash_prev`, `_hash`): reescribir o
quitar una línea rompe la cadena y `verificar()` lo dice. Tres tipos de anotación:
- PRERREGISTRO: hipótesis, objeto, métrica, datos, fechas, semilla, criterio de éxito, máximo de variantes y su huella;
- INTENTO: una ejecución de una variante del experimento (cuenta aunque no llegue a dar resultado);
- RESULTADO: lo que dio un intento, con su veredicto («mejor», «peor», «todavía no se sabe» o «fallido»).
No hay intento sin prerregistro ni resultado sin intento. Un resultado solo sirve para adoptar un cambio (`adoptable`) si el
experimento se prerregistró antes de su primer intento, el intento está dentro del máximo de variantes y el veredicto es «mejor».
El formato definitivo lo fijará el contrato CT-G-24 (borrador en `.docs/diseno/contratos/`) cuando se cierre el diseño de J.

Uso (desde la raíz):
  python3 .docs/scripts/registro_experimentos.py prerregistrar <prerregistro.json> [--registro R] [--autor A]
  python3 .docs/scripts/registro_experimentos.py intento <EXP-…> [--variante V] [--registro R]
  python3 .docs/scripts/registro_experimentos.py resultado <EXP-…> <n> <veredicto> [--detalle JSON] [--registro R]
  python3 .docs/scripts/registro_experimentos.py ver [<EXP-…>] [--registro R]
  python3 .docs/scripts/registro_experimentos.py verificar [--registro R]
Solo biblioteca estándar.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone, UTC
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
REGISTRO_DEFECTO = RAIZ / ".docs" / "experimentos" / "registro.jsonl"
VERSION = "0.1.0"
OBJETOS = ("RECORTE", "INSTRUCCION", "MODELO", "ESTRATEGIA", "PARAMETRO", "BLOQUE", "OTRO")
VEREDICTOS = ("mejor", "peor", "todavía no se sabe", "fallido")
CAMPOS_PRERREGISTRO = ("hipotesis", "objeto", "metrica", "datos", "desde", "hasta", "semilla", "criterio_exito", "max_variantes")
RE_EXP = re.compile(r"^EXP-\d{4}-\d{4}\Z")
RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}\Z")


class RegistroError(ValueError):
    """Anotación que el registro no admite, o cadena rota. Nunca se escribe nada en ese caso."""


def huella(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def _ahora() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class Registro:
    def __init__(self, ruta: Path | str = REGISTRO_DEFECTO):
        self.ruta = Path(ruta)

    # ------------------------------------------------------------------ lectura y verificación
    def anotaciones(self) -> list[dict]:
        if not self.ruta.exists():
            return []
        out = []
        prev = "0" * 64
        for i, linea in enumerate(self.ruta.read_text(encoding="utf-8").splitlines(), 1):
            if not linea.strip():
                continue
            try:
                e = json.loads(linea)
            except ValueError as ex:
                raise RegistroError(f"línea {i} no es JSON: el registro está dañado") from ex
            cuerpo = {k: v for k, v in e.items() if k != "_hash"} if isinstance(e, dict) else None
            if not isinstance(e, dict) or e.get("_seq") != len(out) + 1 or e.get("_hash_prev") != prev or e.get("_hash") != huella(cuerpo):
                raise RegistroError(f"cadena rota en la anotación {len(out) + 1}: alguien la reescribió o la quitó")
            out.append(e)
            prev = e["_hash"]
        return out

    def verificar(self) -> int:
        return len(self.anotaciones())

    def _anexar(self, cuerpo: dict) -> dict:
        previas = self.anotaciones()   # falla cerrado si la cadena ya está rota
        e = {**cuerpo, "_seq": len(previas) + 1, "_hash_prev": previas[-1]["_hash"] if previas else "0" * 64}
        e["_hash"] = huella(e)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ruta, "a", encoding="utf-8") as f:
            f.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
            f.flush()
            os.fsync(f.fileno())
        return e

    def experimento(self, exp_id: str) -> dict:
        """El prerregistro, los intentos y los resultados de un experimento."""
        a = self.anotaciones()
        pre = next((x for x in a if x["tipo"] == "PRERREGISTRO" and x["exp_id"] == exp_id), None)
        if pre is None:
            raise RegistroError(f"{exp_id} no está prerregistrado")
        return {"prerregistro": pre, "intentos": [x for x in a if x["tipo"] == "INTENTO" and x["exp_id"] == exp_id],
                "resultados": [x for x in a if x["tipo"] == "RESULTADO" and x["exp_id"] == exp_id]}

    # ------------------------------------------------------------------ escritura
    def prerregistrar(self, datos: dict, autor: str, ahora: str | None = None) -> dict:
        falta = [k for k in CAMPOS_PRERREGISTRO if k not in datos]
        if falta:
            raise RegistroError(f"al prerregistro le faltan {falta}")
        if datos["objeto"] not in OBJETOS:
            raise RegistroError(f"objeto {datos['objeto']!r} no válido ({', '.join(OBJETOS)})")
        for k in ("hipotesis", "metrica", "criterio_exito"):
            if not (isinstance(datos[k], str) and len(datos[k].strip()) >= 10):
                raise RegistroError(f"«{k}» tiene que decirse con palabras (10 caracteres o más)")
        if not (isinstance(datos["max_variantes"], int) and not isinstance(datos["max_variantes"], bool) and 1 <= datos["max_variantes"] <= 1000):
            raise RegistroError("«max_variantes» es un entero entre 1 y 1000")
        if not (isinstance(datos["semilla"], int) and not isinstance(datos["semilla"], bool)):
            raise RegistroError("«semilla» es un entero")
        if not all(isinstance(datos[k], str) and RE_FECHA.match(datos[k]) for k in ("desde", "hasta")) or datos["desde"] > datos["hasta"]:
            raise RegistroError("«desde» y «hasta» son fechas AAAA-MM-DD, en orden")
        if not (isinstance(autor, str) and autor.strip()):
            raise RegistroError("falta el autor")
        ahora = ahora or _ahora()
        anio = ahora[:4]
        n = sum(1 for x in self.anotaciones() if x["tipo"] == "PRERREGISTRO" and x["exp_id"].startswith(f"EXP-{anio}-")) + 1
        contenido = {k: datos[k] for k in sorted(datos)}
        return self._anexar({"tipo": "PRERREGISTRO", "exp_id": f"EXP-{anio}-{n:04d}", "autor": autor, "creado_en": ahora,
                             "version_registro": VERSION, "contenido": contenido, "huella_prerregistro": huella(contenido)})

    def intento(self, exp_id: str, variante: str = "única", ahora: str | None = None) -> dict:
        exp = self.experimento(exp_id)   # sin prerregistro no hay intento
        n = len(exp["intentos"]) + 1
        orden = list(dict.fromkeys([x["variante"] for x in exp["intentos"]] + [str(variante)]))   # variantes en el orden en que aparecen
        dentro = orden.index(str(variante)) < exp["prerregistro"]["contenido"]["max_variantes"]
        return self._anexar({"tipo": "INTENTO", "exp_id": exp_id, "n": n, "variante": str(variante), "inicio": ahora or _ahora(),
                             "huella_prerregistro": exp["prerregistro"]["huella_prerregistro"], "dentro_del_maximo": dentro})

    def resultado(self, exp_id: str, n: int, veredicto: str, detalle: dict | None = None, ahora: str | None = None) -> dict:
        exp = self.experimento(exp_id)
        if veredicto not in VEREDICTOS:
            raise RegistroError(f"veredicto {veredicto!r} no válido ({', '.join(VEREDICTOS)})")
        if not any(x["n"] == n for x in exp["intentos"]):
            raise RegistroError(f"{exp_id} no tiene el intento {n}")
        if any(x["n"] == n for x in exp["resultados"]):
            raise RegistroError(f"el intento {n} de {exp_id} ya tiene resultado: no se reescribe")
        return self._anexar({"tipo": "RESULTADO", "exp_id": exp_id, "n": n, "veredicto": veredicto, "detalle": detalle or {},
                             "registrado_en": ahora or _ahora()})

    # ------------------------------------------------------------------ lo que dice el registro
    def resumen(self, exp_id: str) -> dict:
        exp = self.experimento(exp_id)
        pre = exp["prerregistro"]
        res = {x["n"]: x for x in exp["resultados"]}
        intentos = exp["intentos"]
        adoptables = [i["n"] for i in intentos if i["dentro_del_maximo"] and res.get(i["n"], {}).get("veredicto") == "mejor"
                      and i["inicio"] >= pre["creado_en"]]
        return {"exp_id": exp_id, "hipotesis": pre["contenido"]["hipotesis"], "objeto": pre["contenido"]["objeto"],
                "max_variantes": pre["contenido"]["max_variantes"], "intentos": len(intentos),
                "variantes": len({i["variante"] for i in intentos}), "sin_resultado": [i["n"] for i in intentos if i["n"] not in res],
                "fuera_del_maximo": [i["n"] for i in intentos if not i["dentro_del_maximo"]],
                "veredictos": {str(n): r["veredicto"] for n, r in sorted(res.items())}, "adoptables": adoptables,
                "adoptable": bool(adoptables)}

    def adoptable(self, exp_id: str) -> bool:
        return self.resumen(exp_id)["adoptable"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--registro", default=str(REGISTRO_DEFECTO))
    sub = ap.add_subparsers(dest="orden", required=True)
    p = sub.add_parser("prerregistrar"); p.add_argument("fichero"); p.add_argument("--autor", default="operador")
    p = sub.add_parser("intento"); p.add_argument("exp_id"); p.add_argument("--variante", default="única")
    p = sub.add_parser("resultado"); p.add_argument("exp_id"); p.add_argument("n", type=int); p.add_argument("veredicto")
    p.add_argument("--detalle", default="{}")
    p = sub.add_parser("ver"); p.add_argument("exp_id", nargs="?")
    sub.add_parser("verificar")
    a = ap.parse_args(argv)
    r = Registro(a.registro)
    try:
        if a.orden == "prerregistrar":
            e = r.prerregistrar(json.loads(Path(a.fichero).read_text(encoding="utf-8")), a.autor)
            print(f"{e['exp_id']} prerregistrado; huella {e['huella_prerregistro'][:16]}…")
        elif a.orden == "intento":
            e = r.intento(a.exp_id, a.variante)
            print(f"{a.exp_id}: intento {e['n']}" + ("" if e["dentro_del_maximo"] else " (FUERA del máximo de variantes prerregistrado)"))
        elif a.orden == "resultado":
            r.resultado(a.exp_id, a.n, a.veredicto, json.loads(a.detalle))
            print(f"{a.exp_id}: resultado del intento {a.n} registrado")
        elif a.orden == "ver":
            ids = [a.exp_id] if a.exp_id else sorted({x["exp_id"] for x in r.anotaciones() if x["tipo"] == "PRERREGISTRO"})
            print(json.dumps([r.resumen(i) for i in ids], ensure_ascii=False, indent=1))
        else:
            print(f"registro íntegro: {r.verificar()} anotaciones")
    except (RegistroError, OSError, ValueError) as e:
        print(f"registro de experimentos: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
