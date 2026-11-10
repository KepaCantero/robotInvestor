"""Pruebas doradas de la jornada y de la semana (V0.66, pieza 7 del kit 2). Solo pruebas y datos de
prueba: nada en validador/.

Una prueba dorada guarda una foto fija de lo que hace cada paso de un recorrido y avisa de cualquier
diferencia; la acepta o la rechaza una persona, a propósito y por escrito (con --regenerar en
pruebas_doradas.py, y cada regeneración se explica en el Documento 0 de la pieza que la hizo).

- resumen(resultado, o): la foto de UN paso. Del resultado: ok, codigo, las listas de acciones
  proyectadas a (condicion, codigo, expediente, ok, posicion, regla), las cantidades redondeadas a 6
  decimales y los identificadores; sin los textos de motivo, que cambian demasiado. Del estado: el estado
  de cada expediente y de cada posición con su cantidad, los códigos de los avisos sin acusar (ordenados),
  el nivel de cada cartera, si hay kill-switch y el número de rearmes. Nunca lanza: lo ilegible sale como
  el texto "ILEGIBLE" (falla cerrado).
- foto_jornada(pasos=None, observar=None) y foto_semana(pasos=None, observar=None): recorren un gemelo
  en memoria de cada recorrido (los pasos de pruebas_jornada.py y de pruebas_semana.py, con el mismo
  instante del Reloj en la semana) y devuelven la lista de resúmenes, paso a paso.
- texto_foto(foto): el JSON de la foto: claves ordenadas e indentado, sin NaN, con salto final.
- generar_fotos(carpeta=None): escribe jornada.json y semana.json en pruebas/doradas/ (o en la carpeta
  que se le dé).
- comparar_fotos(antigua, nueva): las diferencias, cada una {camino, antes, después}, y describe()
  las pinta una por línea: "camino: antes -> después".

Determinismo: sin azar ni reloj del sistema; claves ordenadas al escribir; las listas conservan su orden,
que es semántico; dos ejecuciones dan el mismo fichero byte a byte, en cualquier carpeta y máquina.
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

CARPETA_FOTOS = AQUI / "doradas"
PROFUNDIDAD_TOPE = 60          # anidado más profundo que esto se representa "(...)" [PROPUESTO]
DECIMALES = 6                  # las cantidades de la foto se redondean a este número de decimales
ILEGIBLE = "ILEGIBLE"          # lo que no se puede leer del estado (falla cerrado, nunca lanza)
AUSENTE = "(ausente)"          # la marca de una clave que aparece o desaparece en el comparador
CORTADO = "(...)"              # la marca de un anidado más profundo que PROFUNDIDAD_TOPE

def _num(x):
    """Un float de la foto: redondeado a DECIMALES; los no finitos, como texto (la foto es JSON estricto)."""
    if x != x:
        return "NaN"
    if x == float("inf"):
        return "Infinity"
    if x == float("-inf"):
        return "-Infinity"
    return round(x, DECIMALES)


def _limpia(x, prof=0):
    """La copia limpia de un resultado: sin clave «motivo» a cualquier profundidad, con las listas de
    «acciones» proyectadas a (condicion, codigo, expediente, ok, posicion, regla), los float redondeados
    y el anidado profundo cortado. Un set o frozenset (su orden varía entre procesos) y una clave que
    colisiona tras str() (p. ej. 1 y "1") salen ILEGIBLE: visibles, nunca fundidos ni no deterministas."""
    if prof > PROFUNDIDAD_TOPE:
        return CORTADO
    if isinstance(x, dict):
        d = {}
        for k, v in x.items():
            ks = str(k)
            if ks == "motivo":
                continue
            if ks in d:   # colisión tras str(k): la entrada fundida en silencio se vería como una sola
                d[ks] = ILEGIBLE
                continue
            d[ks] = _acciones(v, prof) if ks == "acciones" else _limpia(v, prof + 1)
        return d
    if isinstance(x, (list, tuple)):
        return [_limpia(v, prof + 1) for v in x]
    if x is None or isinstance(x, (bool, int, str)):
        return x
    if isinstance(x, float):
        return _num(x)
    if isinstance(x, (set, frozenset)):   # sin orden estable entre procesos: no es representable
        return ILEGIBLE
    return str(x)   # fechas, decimales u otros objetos: su representación, que es estable


def _acciones(xs, prof=0):
    """Una lista de acciones de H proyectada a (condicion, codigo, expediente, ok, posicion, regla): lo
    que la jornada y la semana ya exigen de ellas en sus ESPERADO (regla, codigo, condicion) más ok,
    posicion y expediente, que ninguna prueba mira (hallazgo 1 de la revisión independiente: sin ellos,
    una regresión que cambiara el ok o la posicion informados pasaba en silencio por todo el lote). Lo
    que no sea un diccionario se deja limpio tal cual."""
    if not isinstance(xs, list):
        return _limpia(xs, prof + 1)
    out = []
    for a in xs:
        if isinstance(a, dict):
            out.append({"condicion": _limpia(a.get("condicion"), prof + 1), "codigo": _limpia(a.get("codigo"), prof + 1),
                        "expediente": _limpia(a.get("expediente"), prof + 1), "ok": _limpia(a.get("ok"), prof + 1),
                        "posicion": _limpia(a.get("posicion"), prof + 1), "regla": _limpia(a.get("regla"), prof + 1)})
        else:
            out.append(_limpia(a, prof + 1))
    return out


def _estado(o):
    """La mitad de estado del resumen: expedientes, posiciones con su cantidad, avisos sin acusar
    (códigos ordenados, con duplicados), niveles de cada cartera, kill-switch y número de rearmes.
    Cada bloque en su try: lo ilegible no rompe la foto."""
    e = {}
    try:
        e["expedientes"] = {str(k): (_limpia(v.get("estado")) if isinstance(v, dict) else ILEGIBLE)
                            for k, v in o.expedientes.items()}
    except Exception:   # noqa: BLE001 — un expediente ilegible no se pinta de verde
        e["expedientes"] = ILEGIBLE
    try:
        pos = {}
        for k, v in o.posiciones.items():
            pos[str(k)] = ({"cantidad": _limpia(v.get("cantidad")), "estado": _limpia(v.get("estado"))}
                           if isinstance(v, dict) else ILEGIBLE)
        e["posiciones"] = pos
    except Exception:   # noqa: BLE001
        e["posiciones"] = ILEGIBLE
    try:
        if not isinstance(o.avisos, (list, tuple)):
            raise ValueError("los avisos no son una lista")
        e["avisos"] = sorted(str(_limpia(a.get("codigo"))) for a in o.avisos if isinstance(a, dict) and a.get("acuse") is None)
    except Exception:   # noqa: BLE001
        e["avisos"] = ILEGIBLE
    try:
        carteras = sorted(str(c) for c in set(o.cfg.get("nivel_autonomia", {}) or {}) | set(getattr(o, "degradadas", {}) or {}))
        e["niveles"] = {c: _limpia(o.nivel(c)) for c in carteras}
    except Exception:   # noqa: BLE001
        e["niveles"] = ILEGIBLE
    try:
        e["kill"] = o.kill is not None
    except Exception:   # noqa: BLE001
        e["kill"] = ILEGIBLE
    try:
        e["rearmes"] = len(o.rearmes)
    except Exception:   # noqa: BLE001
        e["rearmes"] = ILEGIBLE
    return e


def resumen(resultado, o):
    """La foto de UN paso: {"resultado": …, "estado": …}. Nunca lanza y no cambia nada (lo comprueba
    la batería con el volcado del Orquestador y con una copia del resultado)."""
    return {"estado": _estado(o), "resultado": _limpia(resultado)}


def foto_jornada(pasos=None, observar=None):
    """El gemelo en memoria de la jornada (el `g` de pruebas_jornada.py: nuevo(CFG) y su broker), los
    mismos pasos, y tras cada uno su resumen. Sin diario: los cortes y los reinicios son infraestructura
    de la batería y no cambian el estado del Orquestador. Devuelve la lista de resúmenes."""
    from pruebas_jornada import CFG as CFG_J, broker as broker_j, pasos as pasos_j
    from pruebas_orquestador import nuevo
    o, b = nuevo(CFG_J), broker_j()
    foto = []
    for nombre, paso in (pasos_j() if pasos is None else pasos):
        r = paso(o, b)
        if observar is not None:
            observar(nombre, r, o)
        foto.append({"paso": nombre, **resumen(r, o)})
    return foto


def foto_semana(pasos=None, observar=None):
    """El gemelo en memoria de la semana (el `g` de pruebas_semana.py: nuevo(CFG_SEMANA, sellos=(S2,)) y
    su broker), los mismos pasos y la misma secuencia de instantes (la clase Maquina de la propia batería:
    los mismos deltas, las noches de 120 s y los arranques de la mañana con reloj nuevo). La cfg se IMPORTA
    de la batería (hallazgo 2 de la revisión independiente): un cambio de escenario cambia también la foto.
    Sin diario: el punto de control y el reinicio tampoco cambian el estado. Devuelve la lista de resúmenes."""
    import pruebas_semana as sm
    from pruebas_orquestador import nuevo
    o = nuevo(sm.CFG_SEMANA, sellos=(sm.S2,))
    b = sm.broker()
    m = sm.Maquina(o, [b], sm.DIAS["lunes"])
    dia_actual, t_prev = "lunes", m.instante()
    foto = []
    for nombre, paso, delta in (sm.pasos_semana() if pasos is None else pasos):
        dia = nombre.split("_")[0]
        if dia != dia_actual:   # ---- noche: pasa el tiempo y arranca la mañana con reloj nuevo
            m.pasar(120)
            m.instante()
            m.para()
            m = sm.Maquina(o, [b], sm.DIAS[dia])
            dia_actual, t_prev = dia, m.instante()
        m.pasar(delta)
        t = m.instante()
        r = paso(o, b, t, t_prev)
        if observar is not None:
            observar(nombre, r, o)
        foto.append({"paso": nombre, **resumen(r, o)})
        t_prev = t
    m.para()
    return foto


FOTOS = {"jornada": foto_jornada, "semana": foto_semana}


def texto_foto(foto):
    """El texto JSON de una foto: claves ordenadas e indentado (para que las diferencias se lean bien),
    sin NaN y con el salto de línea final. Dos ejecuciones dan el mismo texto byte a byte."""
    return json.dumps(foto, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"


def generar_fotos(carpeta=None, recorridos=("jornada", "semana")):
    """Recorre los gemelos y escribe sus fotos; devuelve {recorrido: ruta escrita}. Con `carpeta` escribe
    fuera de pruebas/doradas/ (así la batería comprueba la regeneración en una carpeta temporal)."""
    carpeta = Path(carpeta) if carpeta is not None else CARPETA_FOTOS
    carpeta.mkdir(parents=True, exist_ok=True)
    hechas = {}
    for r in recorridos:
        p = carpeta / f"{r}.json"
        p.write_text(texto_foto(FOTOS[r]()), encoding="utf-8")
        hechas[r] = p
    return hechas


def leer_foto(recorrido, carpeta=None):
    """La foto entregada de un recorrido, como estructura."""
    carpeta = Path(carpeta) if carpeta is not None else CARPETA_FOTOS
    return json.loads((carpeta / f"{recorrido}.json").read_text(encoding="utf-8"))


def _dif(a, b, camino, prof=0):
    """Las diferencias entre dos valores ya limpios, cada una {antes, camino, después}."""
    if prof > PROFUNDIDAD_TOPE:
        return [{"antes": a, "camino": camino, "después": b}] if a != b else []
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append({"antes": AUSENTE, "camino": f"{camino}.{k}", "después": b[k]})
            elif k not in b:
                out.append({"antes": a[k], "camino": f"{camino}.{k}", "después": AUSENTE})
            else:
                out.extend(_dif(a[k], b[k], f"{camino}.{k}", prof + 1))
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return [{"antes": len(a), "camino": f"{camino} (longitud)", "después": len(b)},
                    {"antes": a, "camino": camino, "después": b}]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out.extend(_dif(x, y, f"{camino}[{i}]", prof + 1))
        return out
    return [{"antes": a, "camino": camino, "después": b}] if a != b else []


def comparar_fotos(antigua, nueva):
    """Las diferencias entre dos fotos, emparejando los pasos por posición. Cada una lleva el paso, el
    camino completo y los dos valores; una clave que aparece o desaparece se marca con "(ausente)"."""
    if not isinstance(antigua, list) or not isinstance(nueva, list):
        return [{"antes": _limpia(antigua), "camino": "foto (no es una lista de pasos)",
                 "después": _limpia(nueva)}]
    out = []
    if len(antigua) != len(nueva):
        out.append({"antes": len(antigua), "camino": "pasos (número)", "después": len(nueva)})
    for i in range(min(len(antigua), len(nueva))):
        A, B = antigua[i], nueva[i]
        base = f"paso[{i}] ({A.get('paso') if isinstance(A, dict) else A})"
        out.extend(_dif(A, B, base))
    return out


def _corto(v):
    """Un valor del informe, en una línea corta: los compuestos en JSON y los escalares con repr."""
    if isinstance(v, (dict, list)):
        t = json.dumps(v, ensure_ascii=False, sort_keys=True, allow_nan=False)
    else:
        t = repr(v)
    return t if len(t) <= 120 else t[:117] + "..."


def describe(diferencias):
    """El informe de diferencias, una línea por diferencia: "camino: antes -> después"."""
    return [f"{d['camino']}: {_corto(d['antes'])} -> {_corto(d['después'])}" for d in diferencias]
