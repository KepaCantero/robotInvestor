"""Pruebas de T-83 (V0.72): cada valor por defecto con su estado, su fuente, su justificación y su pregunta del cuestionario como
datos (Constitución V0.6, D-44 y D-45; PC3-07 de la V0.67). Módulo `validador/parametros_doc.py`.

Comprueba la cobertura en los dos sentidos de `PARAMETROS`, `CONFIG_DEFECTO` y `POLITICA_DEFECTO`; estados, fuentes (que
existen en la Constitución, en la deuda técnica o en documentos_0), justificaciones y preguntas; que las marcas [RATIFICADO] y
[PROPUESTO] de los comentarios del código (análisis del fuente con `ast` y `tokenize`) coinciden con el estado documentado; y,
con una copia del código en una carpeta temporal y esta misma batería en un subproceso, que añadir un parámetro sin documentar
o cambiar una marca la hace fallar.

Uso: python3 pruebas/pruebas_parametros_doc_t83.py
(La variable de entorno T83_VALIDADOR, que usa la propia batería en sus subprocesos, apunta a otra carpeta `validador`.)
"""
import ast
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MARCO = AQUI.parent
SISTEMA = MARCO.parent
COPIA = os.environ.get("T83_VALIDADOR")
VALIDADOR = Path(COPIA).resolve() if COPIA else MARCO / "validador"
sys.path.insert(0, str(VALIDADOR))
import parametros_doc as pd  # noqa: E402
from control_f import POLITICA_DEFECTO  # noqa: E402
from orquestador import CONFIG_DEFECTO  # noqa: E402
from parametros import PARAMETROS, como_dict  # noqa: E402
from persistencia import MODULOS_ESQUEMA  # noqa: E402

CONSTITUCION = SISTEMA / "constitucion" / "Constitucion_Global.md"
DEUDA = SISTEMA / "seguimiento" / "Deuda_tecnica_y_pendientes_del_operador.md"
DOCUMENTOS_0 = SISTEMA / "documentos_0"
RE_MARCA = re.compile(r"\[(PROPUESTO|RATIFICADO)\b")
RE_LECTURA = re.compile(r"(?:\b_P|\bPARAMETROS)\[[\"'](\w+)[\"']\]")
FUENTE_TABLA = {"PARAMETROS": "parametros.py", "CONFIG_DEFECTO": "orquestador.py", "POLITICA_DEFECTO": "control_f.py"}


class Arnes:
    """El arnés de `pruebas_orquestador.py` (solo `chk`): se copia para no importar el Orquestador desde otra carpeta en los
    subprocesos con T83_VALIDADOR."""

    def __init__(self):
        self.ok = True
        self.n = 0

    def chk(self, nombre, cond, detalle=""):
        self.n += 1
        print(("OK   " if cond else "FALLA"), nombre, "" if cond else detalle)
        self.ok &= bool(cond)


# ---------------------------------------------------------------------- análisis del fuente
def comentarios(texto):
    """{línea: [comentarios]} de un fuente Python, con tokenize (solo comentarios de verdad, no textos ni docstrings)."""
    out = {}
    for tok in tokenize.generate_tokens(io.StringIO(texto).readline):
        if tok.type == tokenize.COMMENT:
            out.setdefault(tok.start[0], []).append(tok.string)
    return out


def marcas_de_dict(texto, nombre):
    """{clave: {marcas}} de las claves de primer nivel del diccionario literal asignado a `nombre`. A una clave le tocan los
    comentarios de las líneas que ocupa (de la clave al final de su valor) y los de las líneas de solo comentario que la
    preceden inmediatamente. Solo aparecen las claves con alguna marca."""
    arbol = ast.parse(texto)
    nodos = [n.value for n in ast.walk(arbol) if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict)
             and any(isinstance(t, ast.Name) and t.id == nombre for t in n.targets)]
    if len(nodos) != 1:
        raise ValueError(f"{nombre}: {len(nodos)} asignaciones de diccionario literal")
    lineas, com, out = texto.splitlines(), comentarios(texto), {}
    for k, v in zip(nodos[0].keys, nodos[0].values):
        if not (isinstance(k, ast.Constant) and isinstance(k.value, str)):
            continue
        textos = [c for n in range(k.lineno, v.end_lineno + 1) for c in com.get(n, [])]
        n = k.lineno - 1
        while n >= 1 and lineas[n - 1].strip().startswith("#"):
            textos += com.get(n, [])
            n -= 1
        m = set(RE_MARCA.findall(" ".join(textos)))
        if m:
            out[k.value] = m
    return out


def lecturas_con_marca(carpeta):
    """[(fichero, línea, clave, {marcas})] de las líneas de `validador/` que leen `_P["clave"]` o `PARAMETROS["clave"]` y llevan
    una marca en su comentario (fuera de parametros.py y parametros_doc.py)."""
    out = []
    for ruta in sorted(Path(carpeta).glob("*.py")):
        if ruta.stem in ("parametros", "parametros_doc"):
            continue
        texto = ruta.read_text(encoding="utf-8")
        com = comentarios(texto)
        for n, linea in enumerate(texto.splitlines(), 1):
            if n not in com:
                continue
            codigo = linea.split("#", 1)[0]
            m = set(RE_MARCA.findall(" ".join(com[n])))
            for clave in RE_LECTURA.findall(codigo):
                if m:
                    out.append((ruta.name, n, clave, m))
    return out


def discrepancias(marcas, tabla):
    """Claves cuya marca de comentario no coincide con su estado documentado (o que no están documentadas)."""
    return sorted((k, sorted(m), pd.DOC[tabla][k]["estado"] if k in pd.DOC[tabla] else None)
                  for k, m in marcas.items() if k not in pd.DOC[tabla] or m != {pd.DOC[tabla][k]["estado"]})


def tiene_numeros(v):
    if isinstance(v, bool):
        return False
    if isinstance(v, (int, float)):
        return True
    if isinstance(v, dict) or hasattr(v, "items"):
        return any(tiene_numeros(x) for x in v.values())
    if isinstance(v, (list, tuple, set)):
        return any(tiene_numeros(x) for x in v)
    return False


def canon(x):
    return json.dumps(como_dict(x) if hasattr(x, "items") and not isinstance(x, dict) else x, sort_keys=True, default=list)


# ---------------------------------------------------------------------- mutaciones en una copia del código
MUTACIONES = (
    ("parametros_sin_documentar", "parametros.py", "_VALORES = {\n", '_VALORES = {\n    "x_t83_sin_documentar": 1,\n',
     "cobertura_PARAMETROS_sin_documentar"),
    ("config_sin_documentar", "orquestador.py", 'CONFIG_DEFECTO = {"max_reintentos": 3,',
     'CONFIG_DEFECTO = {"x_t83_sin_documentar": 1, "max_reintentos": 3,', "cobertura_CONFIG_DEFECTO_sin_documentar"),
    ("politica_sin_documentar", "control_f.py", 'POLITICA_DEFECTO = {"riesgo_max_pct": 1.0,',
     'POLITICA_DEFECTO = {"x_t83_sin_documentar": 1.0, "riesgo_max_pct": 1.0,', "cobertura_POLITICA_DEFECTO_sin_documentar"),
    ("marca_cambiada", "parametros.py", "[RATIFICADO] (D-22: «N muestra cada semana»)", "[PROPUESTO] (D-22: «N muestra cada semana»)",
     "marcas_coinciden_PARAMETROS"),
    ("propuesto_sin_pregunta", "parametros_doc.py", '"¿Qué índice mundial quieres usar como inversión pasiva con la que comparar al robot?"',
     "None", "propuesto_con_pregunta"),
)


def correr_con(carpeta):
    r = subprocess.run([sys.executable, "-I", str(Path(__file__).resolve())], cwd=AQUI, check=False, capture_output=True, text=True,
                       timeout=300, env={**os.environ, "T83_VALIDADOR": str(carpeta)})
    fallan = [l.split()[1] for l in r.stdout.splitlines() if l.startswith("FALLA") and len(l.split()) > 1]
    return r.returncode, fallan, r.stdout + r.stderr


def mutaciones(h):
    ign = shutil.ignore_patterns("__pycache__", "*.pyc")
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "limpia"
        shutil.copytree(MARCO / "validador", base / "validador", ignore=ign)
        shutil.copytree(MARCO / "esquemas", base / "esquemas", ignore=ign)
        rc, fallan, sal = correr_con(base / "validador")
        h.chk("mutacion_la_copia_sin_cambios_pasa", rc == 0 and not fallan and "TODAS LAS PRUEBAS PASAN" in sal, (rc, fallan, sal[-600:]))
        for nombre, fichero, antes, despues, esperada in MUTACIONES:
            d = Path(td) / nombre
            shutil.copytree(base, d, ignore=ign)
            ruta = d / "validador" / fichero
            texto = ruta.read_text(encoding="utf-8")
            if texto.count(antes) != 1:
                h.chk(f"mutacion_{nombre}_hace_fallar_la_bateria", False, f"no encuentro una vez {antes!r} en {fichero}")
                continue
            ruta.write_text(texto.replace(antes, despues), encoding="utf-8")
            rc, fallan, sal = correr_con(d / "validador")
            h.chk(f"mutacion_{nombre}_hace_fallar_la_bateria", rc != 0 and esperada in fallan and "HAY FALLOS" in sal,
                  (rc, fallan, sal[-600:]))


# ---------------------------------------------------------------------- la batería
def main():
    h = Arnes()
    tablas = pd.tablas_del_codigo()
    todos = [(t, k, v) for t in pd.TABLAS for k, v in pd.DOC[t].items()]
    antes = {t: canon(tablas[t]) for t in pd.TABLAS}

    # ------------------------------------------------------------------ cobertura en los dos sentidos
    h.chk("las_tablas_son_las_del_codigo", tablas["PARAMETROS"] is PARAMETROS and tablas["CONFIG_DEFECTO"] is CONFIG_DEFECTO
          and tablas["POLITICA_DEFECTO"] is POLITICA_DEFECTO and set(pd.DOC) == set(pd.TABLAS))
    h.chk("politica_f_es_la_politica_de_F", CONFIG_DEFECTO["politica_f"] is POLITICA_DEFECTO)
    fal = pd.faltan()
    for t in pd.TABLAS:
        h.chk(f"cobertura_{t}_sin_documentar", not [x for x in fal if x[0] == t and x[2] == "SIN_DOCUMENTAR"], fal)
        h.chk(f"cobertura_{t}_documentadas_que_no_existen", not [x for x in fal if x[0] == t and x[2] == "NO_EXISTE"], fal)
    h.chk("faltan_vacio_con_el_codigo_de_hoy", fal == [], fal)
    h.chk("cobertura_cuenta_las_claves_del_codigo", len(todos) == sum(len(tablas[t]) for t in pd.TABLAS) and len(todos) >= 85,
          (len(todos), {t: len(tablas[t]) for t in pd.TABLAS}))

    # ------------------------------------------------------------------ forma de cada registro
    h.chk("defectos_de_forma_ninguno", pd.defectos() == [], pd.defectos()[:5])
    h.chk("registros_con_los_cuatro_campos", all(set(v) == set(pd.CAMPOS) for _, _, v in todos))
    h.chk("estado_valido_en_todos", all(v["estado"] in ("RATIFICADO", "PROPUESTO", "TECNICO") for _, _, v in todos),
          [(t, k, v["estado"]) for t, k, v in todos if v["estado"] not in pd.ESTADOS])
    mal = [(t, k) for t, k, v in todos if not (isinstance(v["fuente"], tuple) and v["fuente"]
                                               and all(isinstance(f, str) and pd.RE_FUENTE.match(f) for f in v["fuente"]))]
    h.chk("fuente_no_vacia_y_bien_formada", not mal, mal)
    cons, deuda = CONSTITUCION.read_text(encoding="utf-8"), DEUDA.read_text(encoding="utf-8")
    filas_c = set(re.findall(r"^\| ([DP]-\d{2}) \|", cons, re.MULTILINE))
    filas_d = set(re.findall(r"^\| ([DT]-\d{2}) \|", deuda, re.MULTILINE))
    versiones = {p.name.split("_", 1)[0] for p in DOCUMENTOS_0.glob("V0.*_*.md")}

    def existe(f):
        doc_, _, ident = f.partition(" ")
        return (ident in filas_c if doc_ == "Constitución" else ident in filas_d if doc_ == "Deuda" else f in versiones)
    mal = sorted({f for _, _, v in todos for f in v["fuente"] if not existe(f)})
    h.chk("fuente_existe_en_su_documento", not mal and len(filas_c) > 40 and len(filas_d) > 40, mal)
    h.chk("fuente_inventada_no_existe", not any(existe(f) for f in ("Constitución D-99", "Constitución P-99", "Deuda D-99", "V0.99"))
          and existe("Constitución D-45") and existe("Deuda T-83") and existe("V0.71"))
    ratificadas = set(re.findall(r"^\| (D-\d{2}) \|[^\n]*\| RATIFICADO \|", cons, re.MULTILINE))
    mal = [(t, k) for t, k, v in todos if v["estado"] == "RATIFICADO"
           and not any(f.startswith("Constitución D-") and f.split()[1] in ratificadas for f in v["fuente"])]
    h.chk("ratificado_cita_una_decision_ratificada_de_la_constitucion", not mal and len(ratificadas) > 20, mal)
    h.chk("los_ratificados_son_los_de_la_constitucion", set(pd.por_estado("RATIFICADO")) == {
        ("PARAMETROS", "o_dias_sequia"), ("PARAMETROS", "n_dias_embudo"), ("PARAMETROS", "i_meses_juicio_sombra"),
        ("CONFIG_DEFECTO", "nivel_autonomia")}, pd.por_estado("RATIFICADO"))
    mal = [(t, k) for t, k, v in todos if not (isinstance(v["justificacion"], str) and 20 <= len(v["justificacion"]) <= 400
                                               and v["justificacion"].endswith(".")
                                               and len(re.findall(r"[.!?](?:\s|$)", v["justificacion"])) <= 2)]
    h.chk("justificacion_de_una_o_dos_frases", not mal, mal)
    for est in ("PROPUESTO", "RATIFICADO"):
        mal = [(t, k) for t, k, v in todos if v["estado"] == est and not (isinstance(v["pregunta"], str) and v["pregunta"].strip())]
        h.chk(f"{est.lower()}_con_pregunta", not mal, mal)
    mal = [(t, k) for t, k, v in todos if v["estado"] == "TECNICO" and v["pregunta"] is not None]
    h.chk("tecnico_sin_pregunta", not mal, mal)
    preguntas = [v["pregunta"] for _, _, v in todos if v["pregunta"] is not None]
    nombres = {k for t in pd.TABLAS for k in tablas[t] if "_" in k}
    mal = [q for q in preguntas if not ("¿" in q and q.endswith("?") and len(q) <= 250 and "_" not in q
                                        and not any(n in q for n in nombres))]
    h.chk("pregunta_en_lenguaje_sencillo", not mal, mal)
    h.chk("preguntas_distintas", len(preguntas) == len(set(preguntas)))
    mal = [(t, k) for t, k, v in todos if v["estado"] == "TECNICO"
           and not (t == "CONFIG_DEFECTO" and k in tablas[t] and (tablas[t][k] is POLITICA_DEFECTO or not tiene_numeros(tablas[t][k])))]
    h.chk("tecnico_solo_sin_numeros_y_en_la_configuracion", not mal, mal)
    h.chk("politica_f_tecnico_porque_sus_limites_van_uno_a_uno", pd.DOC["CONFIG_DEFECTO"]["politica_f"]["estado"] == "TECNICO"
          and all(pd.DOC["POLITICA_DEFECTO"].get(k, {}).get("estado") in ("PROPUESTO", "RATIFICADO") for k in POLITICA_DEFECTO))
    docstrings = {m: ast.get_docstring(ast.parse((VALIDADOR / f"{m}.py").read_text(encoding="utf-8"))) or ""
                  for m in ("parametros", "k_calidad", "orquestador", "control_f")}
    h.chk("los_modulos_declaran_sus_valores_de_partida_propuestos", all("[PROPUESTO]" in d for d in docstrings.values()),
          {m: "[PROPUESTO]" in d for m, d in docstrings.items()})

    # ------------------------------------------------------------------ marcas de los comentarios frente al estado
    marcas = {t: marcas_de_dict((VALIDADOR / FUENTE_TABLA[t]).read_text(encoding="utf-8"), t if t != "PARAMETROS" else "_VALORES")
              for t in pd.TABLAS}
    for t in pd.TABLAS:
        h.chk(f"marcas_coinciden_{t}", not discrepancias(marcas[t], t), discrepancias(marcas[t], t))
    h.chk("el_analisis_ve_las_marcas", sum(1 for m in marcas["PARAMETROS"].values() if m == {"RATIFICADO"}) >= 3
          and len(marcas["PARAMETROS"]) >= 8 and len(marcas["CONFIG_DEFECTO"]) >= 10 and len(marcas["POLITICA_DEFECTO"]) >= 3,
          {t: len(m) for t, m in marcas.items()})
    h.chk("el_analisis_ve_un_comentario_de_la_linea_anterior", marcas["CONFIG_DEFECTO"].get("umbral_l2_eur") == {"PROPUESTO"}
          and marcas["POLITICA_DEFECTO"].get("importe_max_activo_eur") == {"PROPUESTO"}, marcas["CONFIG_DEFECTO"].get("umbral_l2_eur"))
    texto_par = (VALIDADOR / "parametros.py").read_text(encoding="utf-8")
    girado = marcas_de_dict(texto_par.replace("[RATIFICADO] (D-22", "[PROPUESTO] (D-22"), "_VALORES")
    h.chk("el_analisis_ve_una_marca_cambiada", "[RATIFICADO] (D-22" in texto_par
          and [x[0] for x in discrepancias(girado, "PARAMETROS")] == ["n_dias_embudo"], discrepancias(girado, "PARAMETROS"))
    h.chk("el_analisis_ignora_marcas_dentro_de_textos", marcas_de_dict('X = {"a": "[RATIFICADO]",  # nada\n "b": 2}\n', "X") == {}
          and marcas_de_dict('X = {"a": 1,  # [PROPUESTO]\n # [RATIFICADO]\n "b": 2}\n', "X") == {"a": {"PROPUESTO"}, "b": {"RATIFICADO"}})
    lect = lecturas_con_marca(VALIDADOR)
    mal = [x for x in lect if x[2] not in pd.DOC["PARAMETROS"] or x[3] != {pd.DOC["PARAMETROS"][x[2]]["estado"]}]
    h.chk("marcas_de_las_lecturas_de_PARAMETROS_coinciden", not mal and len(lect) >= 15, (mal, len(lect)))
    leidas = {c for ruta in VALIDADOR.glob("*.py") if ruta.stem not in ("parametros", "parametros_doc")
              for c in RE_LECTURA.findall(ruta.read_text(encoding="utf-8"))}
    h.chk("toda_clave_leida_esta_documentada", leidas and leidas <= set(pd.DOC["PARAMETROS"]), sorted(leidas - set(pd.DOC["PARAMETROS"])))

    # ------------------------------------------------------------------ doc()
    r = pd.doc("o_dias_sequia")
    h.chk("doc_devuelve_el_registro_con_tabla_y_clave", r["tabla"] == "PARAMETROS" and r["clave"] == "o_dias_sequia"
          and r["estado"] == "RATIFICADO" and "Constitución D-27" in r["fuente"] and r["pregunta"], r)
    h.chk("doc_con_su_tabla", pd.doc("riesgo_max_pct", "POLITICA_DEFECTO")["estado"] == "PROPUESTO"
          and pd.doc("version_config", "CONFIG_DEFECTO")["pregunta"] is None)
    r["estado"] = "TECNICO"
    h.chk("doc_devuelve_copia", pd.doc("o_dias_sequia")["estado"] == "RATIFICADO")
    try:
        pd.DOC["PARAMETROS"]["o_dias_sequia"]["estado"] = "TECNICO"
        solo_lectura = False
    except TypeError:
        solo_lectura = True
    h.chk("doc_registros_de_solo_lectura", solo_lectura and pd.DOC["PARAMETROS"]["o_dias_sequia"]["estado"] == "RATIFICADO")

    def lanza(fn, exc):
        try:
            fn()
        except exc:
            return True
        except Exception:   # noqa: BLE001  otra excepción tampoco vale
            return False
        return False
    h.chk("doc_sin_documentar_es_KeyError", lanza(lambda: pd.doc("no_existe_t83"), KeyError) and lanza(lambda: pd.doc(None), KeyError)
          and lanza(lambda: pd.doc(["o_dias_sequia"]), KeyError))
    h.chk("doc_en_otra_tabla_es_KeyError", lanza(lambda: pd.doc("o_dias_sequia", "CONFIG_DEFECTO"), KeyError))
    h.chk("doc_tabla_desconocida_es_ValueError", lanza(lambda: pd.doc("o_dias_sequia", "OTRA"), ValueError))
    original = pd.DOC
    try:
        dup = {t: dict(original[t]) for t in pd.TABLAS}
        dup["POLITICA_DEFECTO"]["o_dias_sequia"] = original["PARAMETROS"]["o_dias_sequia"]
        pd.DOC = pd._congela(dup)
        ambigua = lanza(lambda: pd.doc("o_dias_sequia"), ValueError) and pd.doc("o_dias_sequia", "PARAMETROS")["tabla"] == "PARAMETROS"
    finally:
        pd.DOC = original
    h.chk("doc_ambigua_es_ValueError_y_con_tabla_responde", ambigua)

    # ------------------------------------------------------------------ por_estado() y faltan()
    grupos = {e: pd.por_estado(e) for e in pd.ESTADOS}
    h.chk("por_estado_es_una_particion", sorted(x for g in grupos.values() for x in g) == sorted((t, k) for t, k, _ in todos)
          and sum(len(g) for g in grupos.values()) == len(todos))
    h.chk("por_estado_en_el_orden_del_codigo", grupos["PROPUESTO"] == [(t, k) for t in pd.TABLAS for k in pd.DOC[t]
                                                                       if pd.DOC[t][k]["estado"] == "PROPUESTO"]
          and [k for t, k in grupos["TECNICO"]] == ["version_config", "contradictor_desactivado_motivo", "politica_f", "divisas_cotizacion"],
          grupos["TECNICO"])
    h.chk("por_estado_desconocido_es_ValueError", lanza(lambda: pd.por_estado("PENDIENTE"), ValueError)
          and lanza(lambda: pd.por_estado(None), ValueError))
    otra = {t: dict(tablas[t]) for t in pd.TABLAS}
    otra["PARAMETROS"]["x_t83_nuevo"] = 1
    del otra["POLITICA_DEFECTO"]["riesgo_max_pct"]
    h.chk("faltan_detecta_sin_documentar_y_no_existe", pd.faltan(otra) == [("PARAMETROS", "x_t83_nuevo", "SIN_DOCUMENTAR"),
                                                                            ("POLITICA_DEFECTO", "riesgo_max_pct", "NO_EXISTE")], pd.faltan(otra))
    h.chk("faltan_con_tablas_incompletas_es_ValueError", lanza(lambda: pd.faltan({"PARAMETROS": PARAMETROS}), ValueError)
          and lanza(lambda: pd.faltan([]), ValueError))

    # ------------------------------------------------------------------ preguntas_pendientes() (para T-57)
    pend = pd.preguntas_pendientes()
    h.chk("preguntas_pendientes_son_las_de_los_propuestos", [(x["tabla"], x["clave"]) for x in pend] == grupos["PROPUESTO"]
          and all(x["pregunta"] and x["estado"] == "PROPUESTO" for x in pend))
    mal = [(x["tabla"], x["clave"]) for x in pend if x["clave"] not in tablas[x["tabla"]] or canon(x["valor"]) != canon(tablas[x["tabla"]][x["clave"]])]
    h.chk("preguntas_pendientes_con_el_valor_de_partida_del_codigo", not mal, mal)
    h.chk("preguntas_pendientes_serializables", json.loads(json.dumps(pend, ensure_ascii=False)) is not None)
    for x in pend:
        if isinstance(x["valor"], dict):
            x["valor"]["x_t83"] = 0
    pend[0]["pregunta"] = "otra"
    h.chk("preguntas_pendientes_devuelve_copias", {t: canon(tablas[t]) for t in pd.TABLAS} == antes
          and pd.preguntas_pendientes()[0]["pregunta"] != "otra")

    # ------------------------------------------------------------------ no cambia nada más
    h.chk("no_cambia_el_esquema_del_codigo", "parametros_doc" not in MODULOS_ESQUEMA)
    imps = [n for n in ast.parse((VALIDADOR / "parametros_doc.py").read_text(encoding="utf-8")).body
            if isinstance(n, (ast.Import, ast.ImportFrom))]
    h.chk("no_cambia_al_importar_solo_biblioteca_estandar", {a.name for n in imps if isinstance(n, ast.Import) for a in n.names}
          <= {"copy", "re"} and {n.module for n in imps if isinstance(n, ast.ImportFrom)} <= {"__future__", "types"})
    h.chk("no_cambia_ningun_valor", {t: canon(tablas[t]) for t in pd.TABLAS} == antes)

    # ------------------------------------------------------------------ añadir un parámetro sin documentar hace fallar la batería
    if COPIA is None:
        mutaciones(h)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO PARÁMETROS DOCUMENTADOS T-83:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
