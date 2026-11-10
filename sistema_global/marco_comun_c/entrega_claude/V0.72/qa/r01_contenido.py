"""QA r01 de T-83 (V0.72): sondas de contenido de `validador/parametros_doc.py` frente a la Constitución, la deuda y el código.

No cambia nada. Cada sonda imprime HALLAZGO (algo que contradice el diseño o los documentos) u OK, con su evidencia.

Uso (desde sistema_global/marco_comun_c): python3 -I entrega_claude/V0.72/qa/r01_contenido.py
"""
import io
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MARCO = AQUI.parents[2]
SISTEMA = MARCO.parent
REPO = SISTEMA.parent
sys.path.insert(0, str(MARCO / "validador"))
import parametros_doc as pd  # noqa: E402

CONS = (SISTEMA / "constitucion" / "Constitucion_Global.md").read_text(encoding="utf-8")
DEUDA = (SISTEMA / "seguimiento" / "Deuda_tecnica_y_pendientes_del_operador.md").read_text(encoding="utf-8")
hallazgos = 0


def informe(nombre, es_hallazgo, detalle):
    global hallazgos
    hallazgos += bool(es_hallazgo)
    print("HALLAZGO" if es_hallazgo else "OK      ", nombre)
    for linea in detalle:
        print("         ", linea)


def fila(texto, ident):
    m = re.search(rf"^\| {re.escape(ident)} \|[^\n]*", texto, re.MULTILINE)
    return m.group(0) if m else None


# 1. apalancamiento_max: la Constitución ratifica «sin apalancamiento» por defecto (D-16, D-45, §7 «inicialmente cero»)
d16 = fila(CONS, "D-16")
ap = pd.doc("apalancamiento_max", "POLITICA_DEFECTO")
na = pd.doc("nivel_autonomia", "CONFIG_DEFECTO")
cons_45 = "sin apalancamiento" in CONS and "apalancamiento permitido (inicialmente cero)" in CONS
informe("apalancamiento_max_frente_a_D-16_y_D-45",
        d16 and "RATIFICADO" in d16 and cons_45 and ap["estado"] == "PROPUESTO" and "Constitución D-16" not in ap["fuente"],
        [f"Constitución {d16[:150]}…" if d16 else "sin D-16",
         "§9 punto 4 (D-45): «(en simulado, poca autonomía, sin apalancamiento y límites bajos)»; §7: «apalancamiento permitido (inicialmente cero)»",
         f"doc: estado={ap['estado']} fuente={ap['fuente']}",
         f"pregunta: {ap['pregunta']}",
         f"en cambio nivel_autonomia (L1 por D-45) es {na['estado']} con fuente {na['fuente']}"])

# 2. Registros compuestos: las subclaves que la pregunta no deja fijar
tablas = pd.tablas_del_codigo()
compuestos = []
for t in ("CONFIG_DEFECTO",):
    for k, v in tablas[t].items():
        if isinstance(v, dict) and v and k not in ("politica_f",) and all(isinstance(x, str) for x in v) and not set(v) <= {"TRADING", "TACTICA", "LARGO_PLAZO"}:
            compuestos.append((k, sorted(v), pd.doc(k, t)["pregunta"]))
apro = pd.doc("aprobacion", "CONFIG_DEFECTO")
q = apro["pregunta"].lower()
sin_pregunta = [s for s, palabras in (("canales (canal de aprobación y segundo factor, D-19 y P-08)", ("canal", "dónde", "consola", "segundo factor")),
                                       ("enfriamiento_tras_perdida_dia_eur (pérdida que activa la espera, D-18)", ("cuánta pérdida", "qué pérdida", "a partir de"))
                                       ) if not any(p in q for p in palabras)]
informe("aprobacion_subvalores_sin_pregunta", bool(sin_pregunta),
        [f"subclaves: {sorted(tablas['CONFIG_DEFECTO']['aprobacion'])}", f"pregunta: {apro['pregunta']}",
         f"sin pregunta: {sin_pregunta}", f"Deuda {(fila(DEUDA, 'D-18') or '')[:200]}…", f"Deuda {(fila(DEUDA, 'D-19') or '')[:200]}…"]
        + [f"compuesto {k}: {s} -> {p}" for k, s, p in compuestos])

# 3. La justificación de «aprobacion» dice un horario; el código deja aprobar fuera de él con enfriamiento
orq = (MARCO / "validador" / "orquestador.py").read_text(encoding="utf-8")
fuera_espera = '(["fuera de horario"] if fuera else [])' in orq
informe("aprobacion_horario_descrito_como_prohibicion", fuera_espera and "de 07:00 a 21:00 UTC" in apro["justificacion"],
        [f"justificación: {apro['justificacion']}",
         "orquestador.py: fuera de horario solo añade el motivo «fuera de horario» a la espera de enfriamiento_min (no lo prohíbe)"])

# 4. preguntas_pendientes() no valida `tablas` como faltan(): lo que falta sale con valor None sin aviso
otra = {t: dict(tablas[t]) for t in pd.TABLAS}
del otra["POLITICA_DEFECTO"]["valor_min_eur"]
r = [x for x in pd.preguntas_pendientes(otra) if x["clave"] == "valor_min_eur"]
try:
    pd.preguntas_pendientes({})
    exc = "nada"
except Exception as e:   # noqa: BLE001
    exc = type(e).__name__
informe("preguntas_pendientes_sin_validar_tablas", bool(r) and r[0]["valor"] is None,
        [f"con valor_min_eur ausente: valor={r[0]['valor'] if r else '—'} (faltan() lo da como NO_EXISTE)",
         f"preguntas_pendientes({{}}) lanza {exc}; faltan({{}}) lanza ValueError"])

# 5. Números de cada justificación que no aparecen en su valor (heurística: se informa, no se juzga)
def numeros_valor(v, out):
    if isinstance(v, bool):
        return out
    if isinstance(v, (int, float)):
        out |= {round(float(v), 6), round(float(v) * 100, 6), round(abs(float(v)), 6), round(abs(float(v)) * 100, 6)}
    elif hasattr(v, "items"):
        for x in v.values():
            numeros_valor(x, out)
    elif isinstance(v, (list, tuple)):
        for x in v:
            numeros_valor(x, out)
    elif isinstance(v, str):
        for m in re.findall(r"\d+(?:[.,]\d+)?", v):
            out.add(round(float(m.replace(",", ".")), 6))
    return out


PALABRAS = {"uno": 1, "dos": 2, "tres": 3, "cinco": 5, "diez": 10}
raros = []
for t in pd.TABLAS:
    for k in pd.DOC[t]:
        j = pd.DOC[t][k]["justificacion"]
        if k not in tablas[t]:
            continue
        vals = numeros_valor(tablas[t][k], set())
        nums = [round(float(m.replace(".", "").replace(",", ".")), 6) for m in re.findall(r"(?<![\w-])\d[\d.]*(?:,\d+)?", j)]
        nums += [PALABRAS[w] for w in re.findall(r"\b(dos|tres|cinco|diez)\b", j)]
        fuera = [n for n in nums if n not in vals and n not in (1, 24, 100, 7, 2) or (n == 2 and k == "max_reaperturas" and 2 not in vals)]
        if fuera and tablas[t][k] is not tablas["POLITICA_DEFECTO"]:
            raros.append(f"{t}.{k}: {fuera} no está en el valor {str(tablas[t][k])[:80]}")
print("INFO     números de la justificación que no aparecen en el valor (revisados a mano en qa.md):")
for x in raros:
    print("         ", x)

# 6. Esquema del código y valores: HEAD frente al árbol de trabajo
codigo = """
import sys, json, hashlib
sys.path.insert(0, sys.argv[1])
import persistencia, parametros, orquestador, control_f
print(persistencia.esquema_actual(), parametros.VERSION_PARAMETROS, orquestador.CONFIG_DEFECTO['version_config'],
      'parametros_doc' in persistencia.MODULOS_ESQUEMA,
      hashlib.sha256(json.dumps([parametros.como_dict(), orquestador.CONFIG_DEFECTO, control_f.POLITICA_DEFECTO], sort_keys=True,
                                default=lambda x: parametros.como_dict(x) if hasattr(x, 'items') else list(x)).encode()).hexdigest()[:16])
"""
with tempfile.TemporaryDirectory() as td:
    tar = subprocess.run(["git", "-C", str(REPO), "archive", "HEAD", "sistema_global/marco_comun_c/validador"], capture_output=True,
                         check=True).stdout
    tarfile.open(fileobj=io.BytesIO(tar)).extractall(td, filter="data")
    salidas = {}
    for nombre, carpeta in (("HEAD", Path(td) / "sistema_global" / "marco_comun_c" / "validador"), ("árbol", MARCO / "validador")):
        salidas[nombre] = subprocess.run([sys.executable, "-I", "-c", codigo, str(carpeta)], capture_output=True, text=True,
                                         check=True).stdout.strip()
informe("esquema_y_valores_cambian_frente_a_HEAD", salidas["HEAD"] != salidas["árbol"], [f"{k}: {v}" for k, v in salidas.items()])

print(f"\nRESULTADO r01 CONTENIDO T-83: {hallazgos} HALLAZGOS")
