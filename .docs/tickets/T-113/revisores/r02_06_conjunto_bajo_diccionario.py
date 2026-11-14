"""QA r02 de T-113 · Caso mínimo de las 3 regresiones y los 4 «OTRO» de `r02_01`: un diccionario que solo se alcanza a través
de un conjunto (o frozenset) que cuelga de otro diccionario. `json.dumps(..., default=str)` del diccionario de arriba convierte
el conjunto con `str`, que da comillas simples, así que el patrón «"clave": "valor"» de RE_SECRETO no lo ve; y
`_diccionarios_de_arriba` no baja por los diccionarios. Antes de T-113 la recursión sí lo serializaba.
Solo cabe en un conjunto un diccionario con `__hash__` (una subclase): ningún camino del paquete lo produce hoy.
Compara la función actual con la de `3a5fbfe^` y con una variante (solo en este script) cuyo `default` convierte los conjuntos
en listas. Uso (desde bloque_a/11_Ejecutor de la copia): python .../r02_06_conjunto_bajo_diccionario.py
La clave falsa va partida."""
import json
import re
import subprocess
import sys

sys.path.insert(0, ".")
from bloque_a import llm  # noqa: E402
from bloque_a.contratos import secretos_en_texto  # noqa: E402

fuente = subprocess.run(["git", "show", "3a5fbfe^:bloque_a/11_Ejecutor/bloque_a/llm.py"], capture_output=True, text=True, check=True).stdout
ns = {"json": json, "secretos_en_texto": secretos_en_texto}
exec(re.search(r"^def contenido_sensible\(valor\).*?(?=^\S)", fuente, re.S | re.M).group(0), ns)  # noqa: S102 — versión anterior del repo
viejo = ns["contenido_sensible"]


class DH(dict):
    def __hash__(self):
        return id(self)


def variante(valor):
    """La actual, pero con los conjuntos serializados como listas (para ver que la corrección sugerida basta)."""
    orig = json.dumps

    def dumps(o, **k):
        k["default"] = lambda x: sorted(x, key=repr) if isinstance(x, (set, frozenset)) else str(x)
        return orig(o, **k)
    llm.json.dumps = dumps
    try:
        return llm.contenido_sensible(valor)
    finally:
        llm.json.dumps = orig


CLAVE = "api" + "_key"
CASOS = {
    "dict > set > DH(par)": {"a": {DH({CLAVE: "abcdef123456"})}},
    "lista > dict > frozenset > DH(par)": [{"a": frozenset([DH({CLAVE: "abcdef123456"})])}],
    "dict > set > tupla > DH(par)": {"a": {(DH({CLAVE: "abcdef123456"}),)}},
    "dict > set > DH(clave tupla) [antes TypeError]": {"a": {DH({("t",): 1})}},
}
fallos = 0
for nombre, v in CASOS.items():
    res = []
    for f in (viejo, llm.contenido_sensible, variante):
        try:
            res.append(str(f(v)))
        except Exception as e:  # noqa: BLE001
            res.append(type(e).__name__)
    mal = res[0] in ("True", "TypeError") and res[1] == "False"
    fallos += mal
    print(f"{'REGRESIÓN' if mal else 'ok       '} antes={res[0]:9s} ahora={res[1]:9s} con la variante={res[2]:9s} {nombre}")
print("regresiones:", fallos)
