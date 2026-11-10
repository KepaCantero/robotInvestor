"""Pruebas de robustez de la infraestructura T-03 (V0.62, Pieza 3 del kit 2). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_robustez_t03.py

Lo mismo que pruebas/pruebas_robustez.py (V0.37) y pruebas/pruebas_robustez_validadores.py (V0.60) pero
para la infraestructura T-03 —persistencia (volcar, guardar, verificar, cargar, cargar_de y la bóveda de
la clave), diario (crear, abrir y las operaciones anotadas), migraciones (migrar y camino), reloj (Reloj,
contrastar, comprobar_estado, rearmar y degradar_por_reloj) y rotación (rotar y rotar_ficheros)—: con
entradas mutadas al azar, con semilla fija (random.Random(20261111), nunca el random global), demuestra
que nunca lanzan (salvo lo documentado), no mutan lo que no deben, son deterministas y fallan cerrado con
la regla correcta del diseño. Una comprobación puede cubrir N casos.

La comprobación r01 (`r01_los_esperados_cubren_todo_lo_que_el_modulo_puede_responder`, añadida al aplicar
la revisión de V0.62) repite los objetivos que tienen `esperados` con 25 semillas NUEVAS (seis casos por
objetivo y semilla, los mismos generadores que los bloques de abajo) y exige que los códigos que los
módulos respondan queden dentro del `esperado` de su objetivo: los esperados deben cubrir todo lo que el
módulo puede responder con el generador de la pieza, no solo lo que la semilla fija sorteó (la entrega
V0.62 admitía cuatro objetivos sin el PE-03 que una cabecera mutada produce y pasó con la semilla
20261111 tras una tirada con alrededor de dos de cada tres probabilidades de salir mal solo por el
objetivo del diario).

El generador de mutaciones (_mutar_en_sitio, _igual_nan) es el de la pieza de robustez del fin de semana
(pruebas/pruebas_robustez.py), importado sin cambiarlo; los fixtures vienen de las baterías de T-03
(pruebas_orquestador, pruebas_reloj_t03), importados sin cambiarlos.

Las cuatro promesas, adaptadas a cada módulo:

- nunca lanzan: `cargar`, `cargar_de`, `verificar`, `guardar`, `diario.crear`, `diario.abrir`, las
  operaciones anotadas del diario, `migrar`, `camino`, `rotar`, `rotar_ficheros`, `escribir_clave`,
  `leer_clave`, `contrastar`, `comprobar_estado`, `rearmar` y `degradar_por_reloj` no lanzan NUNCA, con
  cualquier mutación; los únicos lanzamientos legítimos son los DOCUMENTADOS: `volcar` con un instante
  ilegible, una clave inválida o un estado que JSON no guarda tal cual (`guardar` los convierte en PE-01 o
  PE-07), el constructor de `Reloj` con tolerancias o fuentes imposibles (ValueError) y una operación del
  diario cuyos argumentos el método no acepta (la envoltura la anota como O-00 y el diario sigue sirviendo);
- no mutan lo que no deben: foto con `_igual_nan` del Orquestador tras `volcar`, `verificar` y `cargar`
  (son lectores); del Orquestador tras un `degradar_por_reloj` que responde RL-06 («no cambia nada»); y
  del fichero de estado tras cada `guardar` fallido (la escritura es atómica: el fichero antiguo entero o
  el nuevo entero, nunca uno roto, y sin temporales olvidados);
- son deterministas: dos llamadas con las mismas entradas dan la misma respuesta (el par ok/código);
- fallan cerrado con la regla correcta: toda mutación del ESTADO de un documento sin rehacer su huella da
  PE-02 al cargar (y con clave, PE-06: la firma cubre toda la cabecera y el estado); una mutación de la
  forma o de la cabecera da PE-01, PE-03 o PE-08; una línea del diario tocada da DI-02 (o DI-03/DI-04 si
  la cadena aguanta y el punto no cuadra); el estado tocado no abre el diario (PE-01/PE-02/PE-03: la
  firma no interviene aquí porque el documento va sin firmar, y PE-06 era franquicia muerta); un
  texto firmado tocado no se rota (PE-06, o PE-01/PE-03 si la forma rota antes de la firma; PE-02 nunca
  llega porque la firma se comprueba antes que la huella); un texto sin firmar mutado no se rota
  (PE-01/PE-02/PE-03); un esquema que no está en el registro da MG-01 al migrar; instantes,
  motivos y actores imposibles dan MG-05 o CL-03; una referencia externa o un rearme imposibles dan RL-06
  sin bloquear; una lectura de fuente que no es un número finito plausible da RL-05 y bloquea.

Excepciones por diseño (no son defectos; cada una con su justificación):

- una mutación de la CABECERA que respeta la forma (por ejemplo version_config como otro texto) puede
  cargar bien: la huella cubre el estado, no la cabecera; lo que una cabecera mentirosa produce lo ven las
  comprobaciones de montar (PE-03) o la integridad (O-13 con kill-switch), y en las mutaciones REHECHAS
  (huella rehecha a propósito, como haría quien edita sabiendo cómo) se admite OK/O-13 exigiendo que el
  resultado vuelta a volcar exactamente igual (ida y vuelta) cuando cargó sin kill-switch;
- `migrar` sobre un documento de ESTE código responde ok con «nada que migrar» y el MISMO texto de
  entrada: una mutación que respete la forma puede salir así; la promesa es que no cambie nada;
- los argumentos mutados de una operación del diario que SÍ son aplicables se aplican y se anotan: cada
  operación escribe exactamente cero (DI-01, no se aplica) o dos líneas (OP y RES), nunca una a medias;
- rearmar un reloj sin bloqueo previo es RL-06 por diseño (solo se rearma un incidente).

Defectos reales: ninguno. La pieza no corrige nada: los módulos T-03 ya cumplían las cuatro promesas y la
batería las demuestra y las fija.
"""
from __future__ import annotations

import copy
import json
import os
import random
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

import diario as di  # noqa: E402
import migraciones as mg  # noqa: E402
import persistencia as pe  # noqa: E402
import reloj as rl  # noqa: E402
import rotacion as rt  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, hasta, nuevo  # noqa: E402
from pruebas_reloj_t03 import BASE, iso, nuevo_reloj  # noqa: E402
from pruebas_robustez import _igual_nan, _mutar_en_sitio  # noqa: E402

SEMILLA = 20261111
T = "2026-11-06T09:30:00+00:00"          # el instante de las baterías T-03
TM = "2026-11-07T10:00:00+00:00"         # instante de migración y rotación
MOTIVO = "Actualizo el código del robot a la versión nueva"
K1, K2 = bytes(range(32)), bytes(range(1, 33))
CASOS_PE = 240   # persistencia: 40 por cada uno de los seis objetivos (rotación)
CASOS_DI = 180   # diario: 60 por cada uno de los tres objetivos
CASOS_MG = 150   # migraciones: 30 por cada uno de los cinco objetivos
CASOS_RL = 150   # reloj: 30 por cada uno de los cinco objetivos
CASOS_RT = 150   # rotación: 30 por cada uno de los cinco objetivos
VENENO_RL = [None, "", "x", [], {}, True, 0, -1, 1e308, float("nan"), float("inf"), -float("inf"), "1.1"]


def _texto_doc(doc) -> str:
    # sin allow_nan=False a propósito: el veneno puede dejar NaN o infinitos, y el TEXTO corrupto que
    # resulta (con NaN literal) es exactamente lo que cargar, migrar y rotar deben rechazar (PE-01)
    return json.dumps(doc, ensure_ascii=True, separators=(",", ":"))


def _rehacer(texto) -> str:
    """Rehace atributos y huella del documento (lo que haría quien edita el estado sabiendo cómo).
    Si la mutación dejó el estado sin forma de diccionario, se devuelve el texto tal cual (PE-01/PE-02)."""
    d = json.loads(texto)
    if not isinstance(d.get("estado"), dict):
        return texto
    try:
        d["atributos"] = sorted(d["estado"])
        d["huella"] = pe._huella(d["estado"])
        return pe._texto(d)
    except (ValueError, TypeError):   # la mutación dejó NaN o infinitos: la huella no se puede rehacer
        return json.dumps(d, ensure_ascii=True, separators=(",", ":"))


def _mutar_doc(texto, rng, dentro_estado=False):
    """Una mutación del documento parseado (en su estado o en la raíz), sin rehacer la huella. Captura el
    valor devuelto: una mutación «valor» en la raíz de un escalar devuelve el objeto NUEVO sin tocar el
    original, y aquí la raíz del documento puede quedar sustituida entera por el veneno."""
    d = json.loads(texto)
    if dentro_estado:
        d["estado"], _ = _mutar_en_sitio(d["estado"], rng)
    else:
        raiz, _ = _mutar_en_sitio(d, rng)
        if not isinstance(raiz, (dict, list)):
            return _texto_doc(raiz)   # la raíz entera sustituida por un escalar (o un veneno no JSON)
    return _texto_doc(d)


def _profundo(n):
    v = 0
    for _ in range(n):
        v = [v]
    return v


def main():
    rng = random.Random(SEMILLA)
    h = Arnes()

    # ================================================================ base común
    o_base = nuevo()
    hasta(o_base, "AUTORIZADA", n=1)
    assert o_base.integridad() == [], o_base.integridad()
    t0 = pe.volcar(o_base, T)                 # sin clave
    t1 = pe.volcar(o_base, T, K1)             # firmado con K1
    h.chk("base_valida_sin_y_con_clave", pe.cargar(t0)["ok"] and pe.cargar(t1, K1)["ok"]
          and pe.cargar(t1)["codigo"] == "PE-06" and pe.cargar(t0, K1)["codigo"] == "PE-06",
          (pe.cargar(t0)["codigo"], pe.cargar(t1)["codigo"]))

    # ================================================================ persistencia
    st = {n: {"lanz": 0, "mal": [], "deter": 0, "n": 0}
          for n in ("estado", "cabecera", "raiz", "firmado", "rehecho", "instante")}
    for i in range(CASOS_PE):
        nombre = list(st)[i % 6]
        st[nombre]["n"] += 1
        if nombre == "instante":
            malo, _ = _mutar_en_sitio(T, rng)
            with tempfile.TemporaryDirectory() as td:
                ruta = os.path.join(td, "e.json")
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(t0)
                try:
                    r = pe.guardar(o_base, ruta, malo)
                except Exception as ex:   # noqa: BLE001
                    st[nombre]["lanz"] += 1
                    st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                    continue
                if r["codigo"] != "PE-01":
                    st[nombre]["mal"].append(r["codigo"])
                if open(ruta, encoding="utf-8").read() != t0:
                    st[nombre]["mal"].append("el fichero cambió con un guardado fallido")
                if any(x.startswith(".estado-") for x in os.listdir(td)):
                    st[nombre]["mal"].append("deja temporales")
            continue
        if nombre == "firmado":
            texto = _mutar_doc(t1, rng, dentro_estado=rng.random() < 0.5)
            esperados, admite_ok = {"PE-01", "PE-06"}, False
        elif nombre == "estado":
            texto = _mutar_doc(t0, rng, dentro_estado=True)
            esperados, admite_ok = {"PE-01", "PE-02"}, False   # PE-01 si el veneno deja la huella incanonicalizable
        elif nombre == "cabecera":
            texto = _mutar_doc(t0, rng, dentro_estado=False)
            esperados, admite_ok = {"PE-01", "PE-02", "PE-03", "PE-08"}, True
        elif nombre == "raiz":
            raiz, _ = _mutar_en_sitio(json.loads(t0), rng)
            texto = raiz if isinstance(raiz, str) else _texto_doc(raiz)
            esperados, admite_ok = {"PE-01", "PE-02", "PE-03", "PE-08"}, True
        else:   # rehecho: la huella rehecha a propósito, como quien edita sabiendo cómo
            texto = _rehacer(_mutar_doc(t0, rng, dentro_estado=True))
            esperados, admite_ok = {"OK", "O-13", "PE-01", "PE-02", "PE-03", "PE-04"}, True
        try:
            r = pe.cargar(texto)
            r2 = pe.cargar(texto)
        except Exception as ex:   # noqa: BLE001
            st[nombre]["lanz"] += 1
            st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
            continue
        if (r["ok"], r["codigo"]) != (r2["ok"], r2["codigo"]):
            st[nombre]["deter"] += 1
        if r["codigo"] not in esperados or (r["ok"] and not admite_ok):
            st[nombre]["mal"].append(r["codigo"])
        if nombre == "rehecho" and r["codigo"] == "OK" and pe.volcar(r["orquestador"], T) != texto:
            st[nombre]["mal"].append("el estado cargado no vuelve a volcar igual")
    h.chk("persistencia_cargar_nunca_lanza_en_240_casos", all(v["lanz"] == 0 for v in st.values()),
          [(k, v["mal"][:1]) for k, v in st.items() if v["lanz"]][:4])
    h.chk("persistencia_cargar_determinista_en_200_casos_de_texto", all(v["deter"] == 0 for v in st.values()),
          [(k, v["deter"]) for k, v in st.items() if v["deter"]][:4])
    h.chk("persistencia_falla_cerrado_con_la_regla_correcta_en_240_casos",
          all(not v["mal"] for v in st.values()) and all(v["n"] > 0 for v in st.values()),
          [(k, v["mal"][:2]) for k, v in st.items() if v["mal"]][:6])
    h.chk("persistencia_toda_mutacion_del_estado_sin_rehacer_huella_es_PE02_o_PE01_nunca_ok",
          st["estado"]["n"] > 0 and not st["estado"]["mal"], st["estado"]["mal"][:3])
    h.chk("persistencia_un_documento_firmado_tocado_por_cualquier_sitio_es_PE06_o_PE01",
          st["firmado"]["n"] > 0 and not st["firmado"]["mal"], st["firmado"]["mal"][:3])
    h.chk("persistencia_guardar_con_instante_mutado_PE01_y_no_toca_el_fichero_ni_deja_temporales",
          st["instante"]["n"] > 0 and not st["instante"]["mal"], st["instante"]["mal"][:3])

    # no mutan la entrada: volcar, verificar y cargar son lectores del Orquestador
    foto = copy.deepcopy({k: v for k, v in vars(o_base).items()})
    pe.volcar(o_base, T, K1)
    pe.verificar(t1, K1)
    pe.cargar(t0)
    h.chk("persistencia_volcar_verificar_y_cargar_no_mutan_el_orquestador",
          _igual_nan(foto, {k: v for k, v in vars(o_base).items()}))

    # guardar con ruta imposible: PE-05, sin temporales y sin tocar lo que ya había
    with tempfile.TemporaryDirectory() as td:
        ruta_buena = os.path.join(td, "e.json")
        pe.guardar(o_base, ruta_buena, T)
        antes = open(ruta_buena, encoding="utf-8").read()
        mal = []
        for ruta_mala in [None, "", "a\x00b", os.path.join(td, "no", "existe", "e.json"), td]:
            try:
                r = pe.guardar(o_base, ruta_mala, T)
                if r["codigo"] != "PE-05":
                    mal.append((repr(ruta_mala)[:40], r["codigo"]))
            except Exception as ex:   # noqa: BLE001
                mal.append((repr(ruta_mala)[:40], f"lanza {type(ex).__name__}"))
        if open(ruta_buena, encoding="utf-8").read() != antes:
            mal.append("el fichero bueno cambió")
        if any(x.startswith(".estado-") for x in os.listdir(td)):
            mal.append("deja temporales")
        h.chk("persistencia_guardar_con_rutas_imposibles_PE05_y_todo_queda_como_estaba", not mal, mal[:4])
        r = pe.guardar(o_base, os.path.join(td, "e2.json"), T, clave="corta")
        h.chk("persistencia_guardar_con_clave_invalida_PE07_y_no_escribe",
              r["codigo"] == "PE-07" and not os.path.exists(os.path.join(td, "e2.json")), r)

    # bóveda de la clave: escribir/leer con entradas imposibles (PE-07, nunca lanza, nunca pisa)
    with tempfile.TemporaryDirectory() as td:
        ruta_clave = os.path.join(td, "clave.hex")
        mal = []
        for valor in (None, "corta", bytes(32), 12345, b""):
            try:
                r = pe.escribir_clave(ruta_clave, valor)
                if r["codigo"] != "PE-07":
                    mal.append(("escribir", repr(valor)[:20], r["codigo"]))
            except Exception as ex:   # noqa: BLE001
                mal.append(("escribir", repr(valor)[:20], f"lanza {type(ex).__name__}"))
        if not pe.escribir_clave(ruta_clave, K1)["ok"]:
            mal.append(("escribir K1", "falló"))
        if pe.escribir_clave(ruta_clave, K2)["codigo"] != "PE-07":
            mal.append(("no pisa", "reescribió la clave"))
        try:
            os.chmod(ruta_clave, 0o644)
            if pe.leer_clave(ruta_clave)["codigo"] != "PE-07":
                mal.append(("permisos 0644", "la leyó"))
            os.chmod(ruta_clave, 0o600)
            with open(ruta_clave, "w", encoding="ascii") as f:
                f.write("zz" * 32 + "\n")
            if pe.leer_clave(ruta_clave)["codigo"] != "PE-07":
                mal.append(("no hexadecimal", "la leyó"))
            with open(ruta_clave, "w", encoding="ascii") as f:
                f.write(K1.hex() + "\n")
            r = pe.leer_clave(ruta_clave)
            if not (r["ok"] and r.get("clave") == K1):
                mal.append(("ida y vuelta", r["codigo"]))
        except OSError as ex:
            mal.append(("chmod", str(ex)))
        for ruta in (None, os.path.join(td, "no", "existe"), td):
            try:
                if pe.leer_clave(ruta)["codigo"] != "PE-07":
                    mal.append(("leer", repr(ruta)[:30], "no es PE-07"))
            except Exception as ex:   # noqa: BLE001
                mal.append(("leer", repr(ruta)[:30], f"lanza {type(ex).__name__}"))
        h.chk("persistencia_la_boveda_de_la_clave_falla_cerrado_PE07", not mal, mal[:5])

    # ================================================================ diario
    with tempfile.TemporaryDirectory() as td:
        re_, rd_ = os.path.join(td, "base.e"), os.path.join(td, "base.d")
        d_base = di.crear(nuevo(), re_, rd_, T)["diario"]
        hasta(d_base, "PROPUESTA")
        lineas_puras = open(rd_, encoding="ascii").read()
        estado_puro = open(re_, encoding="ascii").read()
        h.chk("diario_base_creado_y_su_estado_se_carga", len(lineas_puras.splitlines()) >= 2 and pe.cargar(estado_puro)["ok"])

        st = {n: {"lanz": 0, "mal": [], "deter": 0, "n": 0} for n in ("linea", "estado", "args")}
        for i in range(CASOS_DI):
            nombre = list(st)[i % 3]
            st[nombre]["n"] += 1
            if nombre == "linea":
                # se restauran los DOS ficheros: los casos del estado contaminan el de estado
                ls = lineas_puras.splitlines()
                j = rng.randrange(len(ls))
                try:
                    e = json.loads(ls[j])
                    e, _ = _mutar_en_sitio(e, rng)   # capturado: la raíz «valor» devuelve el objeto nuevo
                    ls[j] = _texto_doc(e)
                except (ValueError, TypeError):
                    ls[j] = "{roto"
                with open(re_, "w", encoding="ascii") as f:
                    f.write(estado_puro)
                with open(rd_, "w", encoding="ascii") as f:
                    f.write("\n".join(ls) + "\n")   # siempre con el salto final: el OK de la regla del corte
                # solo llega con un fichero SIN salto final, caso que este objetivo no construye (lo cubre
                # el caso fijo de la línea cortada de abajo) — franquicia muerta retirada (revisión V0.62)
                try:
                    r = di.abrir(re_, rd_)
                    r2 = di.abrir(re_, rd_)
                except Exception as ex:   # noqa: BLE001
                    st[nombre]["lanz"] += 1
                    st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                    continue
                if (r["ok"], r["codigo"]) != (r2["ok"], r2["codigo"]):
                    st[nombre]["deter"] += 1
                esperados = {"DI-02", "DI-03", "DI-04"}
                if r["codigo"] not in esperados or r["ok"]:
                    st[nombre]["mal"].append((f"línea {j + 1}/{len(ls)}", r["codigo"]))
            elif nombre == "estado":
                d_e = json.loads(estado_puro)
                d_e, _ = _mutar_en_sitio(d_e, rng)   # capturado: la raíz «valor» devuelve el objeto nuevo
                with open(re_, "w", encoding="utf-8") as f:
                    f.write(_texto_doc(d_e))
                with open(rd_, "w", encoding="ascii") as f:
                    f.write(lineas_puras)   # restaurados los DOS ficheros (antes quedaba el diario del caso
                                            # «línea» anterior: observación 2 de la revisión de V0.62)
                try:
                    r = di.abrir(re_, rd_)
                except Exception as ex:   # noqa: BLE001
                    st[nombre]["lanz"] += 1
                    st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                    continue
                # el documento va sin firmar: la firma no interviene y PE-06 era franquicia muerta; la
                # cabecera mutada da PE-03 (revisión de V0.62, hallazgos 1 y 3)
                if r["ok"] or r["codigo"] not in {"PE-01", "PE-02", "PE-03"}:
                    st[nombre]["mal"].append(r["codigo"])
            else:   # args: una operación con argumentos mutados, sobre un diario recién creado
                re_i, rd_i = os.path.join(td, f"args{i}.e"), os.path.join(td, f"args{i}.d")
                try:
                    dd = di.crear(nuevo(), re_i, rd_i, T)["diario"]
                    n_antes = len(open(rd_i, encoding="ascii").read().splitlines())
                    arg = {"instrumento": "EURUSD", "valor": 1.1, "fecha_hora": AHORA}
                    arg, _ = _mutar_en_sitio(arg, rng)
                    r = dd.registrar_cotizacion(arg, "G", T)
                    n_despues = len(open(rd_i, encoding="ascii").read().splitlines())
                except Exception as ex:   # noqa: BLE001
                    st[nombre]["lanz"] += 1
                    st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                    continue
                if not isinstance(r.get("codigo"), str):
                    st[nombre]["mal"].append(r)
                if n_despues - n_antes not in (0, 2):
                    st[nombre]["mal"].append(f"escribió {n_despues - n_antes} líneas")
                # una operación aplicada puede responder ok False con razón (un rechazo del Orquestador
                # también se anota y se reproduce): lo que no puede es escribir una línea a medias
        h.chk("diario_abrir_y_las_operaciones_nunca_lanzan_en_180_casos",
              all(v["lanz"] == 0 for v in st.values()),
              [(k, v["mal"][:1]) for k, v in st.items() if v["lanz"]][:4])
        h.chk("diario_abrir_determinista_en_120_casos_de_ficheros_mutados",
              st["linea"]["deter"] == 0, st["linea"]["deter"])
        h.chk("diario_una_linea_tocada_no_se_usa_DI02_o_el_punto_no_cuadra",
              st["linea"]["n"] > 0 and not st["linea"]["mal"], st["linea"]["mal"][:3])
        h.chk("diario_el_estado_tocado_no_abre_PE01_PE02_o_PE03",
              st["estado"]["n"] > 0 and not st["estado"]["mal"], st["estado"]["mal"][:3])
        h.chk("diario_argumentos_mutados_cero_o_dos_lineas_nunca_una_a_medias",
              st["args"]["n"] > 0 and not st["args"]["mal"], st["args"]["mal"][:3])

        # con los ficheros restaurados: dos aperturas llegan al mismo estado
        with open(re_, "w", encoding="ascii") as f:
            f.write(estado_puro)
        with open(rd_, "w", encoding="ascii") as f:
            f.write(lineas_puras)
        a1, a2 = di.abrir(re_, rd_), di.abrir(re_, rd_)
        h.chk("diario_dos_aperturas_del_mismo_par_de_ficheros_llegan_al_mismo_estado",
              a1["ok"] and a2["ok"] and pe.volcar(a1["diario"].orquestador, T) == pe.volcar(a2["diario"].orquestador, T)
              == pe.volcar(d_base.orquestador, T), (a1["codigo"], a2["codigo"]))

        # la última línea cortada a medias se ignora (no es un fallo) y la última entera pero tocada es
        # DI-02, con los DOS ficheros restaurados (los casos del estado dejan el estado corrupto)
        with open(re_, "w", encoding="ascii") as f:
            f.write(estado_puro)
        with open(rd_, "w", encoding="ascii") as f:
            f.write(lineas_puras)
        with open(rd_, "a", encoding="ascii") as f:
            f.write('{"n":99,"tipo":"OP"')
        r = di.abrir(re_, rd_)
        h.chk("diario_una_ultima_linea_cortada_se_ignora_y_se_limpia",
              r["ok"] and r.get("linea_incompleta") and open(rd_, encoding="ascii").read().endswith("\n"), r)
        ls = lineas_puras.splitlines()
        with open(rd_, "w", encoding="ascii") as f:
            f.write("\n".join(ls[:-1] + [_texto_doc({**json.loads(ls[-1]), "resultado": "0" * 64})]) + "\n")
        r = di.abrir(re_, rd_)
        h.chk("diario_la_ultima_linea_entera_pero_tocada_es_DI02", r["codigo"] == "DI-02", r["codigo"])

    # ================================================================ migraciones
    st = {n: {"lanz": 0, "mal": [], "deter": 0, "n": 0} for n in ("texto", "esquema", "registro", "metadatos", "rehecho")}
    for i in range(CASOS_MG):
        nombre = list(st)[i % 5]
        st[nombre]["n"] += 1
        if nombre == "texto":
            texto = _mutar_doc(t0, rng, dentro_estado=rng.random() < 0.5)
            args = (texto, TM, MOTIVO)
            kw = {}
            esperados = {"OK", "PE-01", "PE-02", "PE-03"}   # ok solo «nada que migrar» con una cabecera mutada
            # (PE-03 con el formato tocado por un texto distinto: revisión de V0.62, hallazgo 1)
        elif nombre == "esquema":
            d = json.loads(t0)
            d["esquema"] = "f" * 64   # un esquema que este código no conoce ni está registrado
            texto = pe._texto(d)
            args = (texto, TM, MOTIVO)
            kw = {}
            esperados = {"MG-01"}
        elif nombre == "registro":
            args = (t0, TM, MOTIVO)
            kw = {"registro": rng.choice([None, 7, "x", (), {"mal": None}]),
                  "esquemas": rng.choice([None, 7, [], {"mal": None}, {"f" * 64: "sin parte"}])}
            esperados = {"OK", "MG-01"}   # con el esquema actual el camino no llega a mirar el registro:
            # MG-02 era franquicia muerta (la envoltura no llega a lanzar y _registro_ok no lanza: revisión V0.62)
        elif nombre == "metadatos":
            args = (t0, rng.choice(["ayer", None, 7, "2026-13-45T00:00:00+00:00", TM]),
                    rng.choice(["corto", "x" * 600, None, 7, MOTIVO]))
            kw = {"actor": rng.choice(["G", None, "", 7, "OPERADOR"])}
            esperados = {"OK", "MG-05"}
        else:   # rehecho: estado mutado con huella rehecha; migrar no llega a montarlo (nada que migrar)
            args = (_rehacer(_mutar_doc(t0, rng, dentro_estado=True)), TM, MOTIVO)
            kw = {}
            esperados = {"OK", "PE-01", "PE-02"}
        try:
            r = mg.migrar(*args, **kw)
            r2 = mg.migrar(*args, **kw)
        except Exception as ex:   # noqa: BLE001
            st[nombre]["lanz"] += 1
            st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
            continue
        if (r["ok"], r["codigo"]) != (r2["ok"], r2["codigo"]):
            st[nombre]["deter"] += 1
        if r["codigo"] not in esperados:
            st[nombre]["mal"].append(r["codigo"])
        if r["ok"] and r.get("texto") is not None and r["texto"] != args[0]:
            st[nombre]["mal"].append("una migración sin pasos cambió el texto")
    h.chk("migraciones_migrar_nunca_lanza_en_150_casos", all(v["lanz"] == 0 for v in st.values()),
          [(k, v["mal"][:1]) for k, v in st.items() if v["lanz"]][:4])
    h.chk("migraciones_migrar_determinista_en_150_casos", all(v["deter"] == 0 for v in st.values()),
          [(k, v["deter"]) for k, v in st.items() if v["deter"]][:4])
    h.chk("migraciones_falla_cerrado_con_la_regla_correcta_en_150_casos",
          all(not v["mal"] for v in st.values()) and all(v["n"] > 0 for v in st.values()),
          [(k, v["mal"][:2]) for k, v in st.items() if v["mal"]][:6])
    h.chk("migraciones_un_esquema_no_registrado_es_MG01_y_metadatos_imposibles_MG05",
          st["esquema"]["n"] > 0 and not st["esquema"]["mal"] and st["metadatos"]["n"] > 0
          and not st["metadatos"]["mal"], (st["esquema"]["mal"][:2], st["metadatos"]["mal"][:2]))
    h.chk("migraciones_camino_sin_camino_o_con_registro_roto_da_None_sin_lanzar",
          mg.camino(pe.FORMATO, "f" * 64, pe.esquema_actual(), mg.MIGRACIONES) is None
          and mg.camino("ESTADO-ORQUESTADOR-9.9.9", "f" * 64, pe.esquema_actual(), mg.MIGRACIONES) is None
          and mg.camino(pe.FORMATO, pe.esquema_actual(), pe.esquema_actual(), [{"mal": 1}]) is None)

    # ================================================================ reloj
    st = {n: {"lanz": 0, "mal": [], "deter": 0, "n": 0} for n in ("referencia", "estado", "incidente", "rearme", "tolerancias")}
    for i in range(CASOS_RL):
        nombre = list(st)[i % 5]
        st[nombre]["n"] += 1
        if nombre == "referencia":
            ref, _ = _mutar_en_sitio(AHORA, rng)
            try:
                _, r_ = nuevo_reloj()
                x = r_.contrastar(ref, "INTERMEDIARIO")
                _, r2_ = nuevo_reloj()
                x2 = r2_.contrastar(ref, "INTERMEDIARIO")
            except Exception as ex:   # noqa: BLE001
                st[nombre]["lanz"] += 1
                st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                continue
            if (x["ok"], x["codigo"]) != (x2["ok"], x2["codigo"]):
                st[nombre]["deter"] += 1
            if x["codigo"] not in {"OK", "RL-03", "RL-06"}:
                st[nombre]["mal"].append(x["codigo"])
            if x["codigo"] == "RL-03" and r_.bloqueo is None:
                st[nombre]["mal"].append("RL-03 sin bloqueo")
            if x["codigo"] == "RL-06" and r_.bloqueo is not None:
                st[nombre]["mal"].append("RL-06 bloqueó")
            if x["ok"] and not pe._instante_ok(x.get("ahora")):
                st[nombre]["mal"].append("ok con un instante ilegible")
        elif nombre == "estado":
            estado = type("Estado", (), {})()
            estado.ultimo_ahora, _ = _mutar_en_sitio(AHORA, rng)
            try:
                _, r_ = nuevo_reloj()
                x = r_.comprobar_estado(estado)
                _, r2_ = nuevo_reloj()
                x2 = r2_.comprobar_estado(copy.deepcopy(estado))
            except Exception as ex:   # noqa: BLE001
                st[nombre]["lanz"] += 1
                st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                continue
            if (x["ok"], x["codigo"]) != (x2["ok"], x2["codigo"]):
                st[nombre]["deter"] += 1
            if x["codigo"] not in {"OK", "RL-02"}:
                st[nombre]["mal"].append(x["codigo"])
        elif nombre == "incidente":
            inc, _ = _mutar_en_sitio({"ok": False, "codigo": "RL-01", "motivo": "x", "ahora": None}, rng)
            o_inc = nuevo()
            foto_i = copy.deepcopy({k: v for k, v in vars(o_inc).items()})
            try:
                x = rl.degradar_por_reloj(o_inc, inc)
            except Exception as ex:   # noqa: BLE001
                st[nombre]["lanz"] += 1
                st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                continue
            if x["codigo"] == "RL-06":
                # «no es un incidente: no cambia nada»: el Orquestador queda exactamente como estaba
                if not _igual_nan(foto_i, {k: v for k, v in vars(o_inc).items()}):
                    st[nombre]["mal"].append("RL-06 cambió el Orquestador")
            elif x["ok"]:
                # una mutación que no toca el código del incidente sigue siendo incidente: degrada a L1
                if any(o_inc.nivel(c) != "L1" for c in rl.CARTERAS):
                    st[nombre]["mal"].append("degradó y quedó una cartera por encima de L1")
            else:
                st[nombre]["mal"].append(x["codigo"])
        elif nombre == "rearme":
            actor, _ = _mutar_en_sitio("OPERADOR", rng)
            motivo, _ = _mutar_en_sitio("Revisado: alguien cambió la hora de la máquina por error", rng)
            try:
                _, r_ = nuevo_reloj()
                x = r_.rearmar(actor, motivo)
            except Exception as ex:   # noqa: BLE001
                st[nombre]["lanz"] += 1
                st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                continue
            if x["codigo"] != "RL-06" or r_.bloqueo is not None:
                st[nombre]["mal"].append((x["codigo"], r_.bloqueo))
        else:   # tolerancias del constructor
            kw = rng.choice([{"max_salto_s": rng.choice(VENENO_RL)}, {"max_desfase_s": rng.choice(VENENO_RL)},
                             {"max_sin_contraste_s": rng.choice(VENENO_RL)}])
            try:
                rl.Reloj(**kw)
            except ValueError:
                pass          # documentado: tolerancias imposibles
            except Exception as ex:   # noqa: BLE001
                st[nombre]["lanz"] += 1
                st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
    h.chk("reloj_contrastar_comprobar_rearmar_degradar_y_constructor_nunca_lanzan_en_150_casos",
          all(v["lanz"] == 0 and not v["mal"] for v in st.values()),
          [(k, (v["mal"] or ["lanz"])[0]) for k, v in st.items() if v["lanz"] or v["mal"]][:5])
    h.chk("reloj_determinista_en_las_lecturas_mutadas", all(v["deter"] == 0 for v in st.values()),
          [(k, v["deter"]) for k, v in st.items() if v["deter"]][:4])
    h.chk("reloj_una_referencia_o_un_rearme_imposible_no_bloquea_RL06",
          st["referencia"]["n"] > 0 and st["rearme"]["n"] > 0 and not st["referencia"]["mal"]
          and not st["rearme"]["mal"], (st["referencia"]["mal"][:2], st["rearme"]["mal"][:2]))
    # y los dos caminos que el veneno no alcanza, fijos: referencia válida dentro de la tolerancia y fuera
    _, r_ = nuevo_reloj()
    x_ok = r_.contrastar("2026-11-06T09:00:02+00:00", "INTERMEDIARIO")
    _, r_ = nuevo_reloj()
    x_rl03 = r_.contrastar("2026-11-06T09:00:30+00:00", "INTERMEDIARIO")
    h.chk("reloj_la_referencia_valida_da_OK_y_la_desfasada_RL03_con_bloqueo",
          x_ok["ok"] and x_rl03["codigo"] == "RL-03" and r_.bloqueo is not None, (x_ok, x_rl03["codigo"]))

    # lecturas de fuente imposibles, sobre un reloj ya contrastado: el veneno en la fuente de PARED es
    # siempre RL-05 (ningún valor imposible es plausible); en la MONÓTONA es RL-05 o RL-01 (un valor
    # finito pero descolocado es un salto del monótono); en ambos casos el reloj queda bloqueado
    mal_rl05 = []
    for valor in VENENO_RL:
        try:
            _, r_ = nuevo_reloj()
            r_._pared = lambda v=valor: v
            x = r_.ahora()
            if x["codigo"] != "RL-05" or r_.bloqueo is None:
                mal_rl05.append(("pared", repr(valor)[:20], x["codigo"]))
        except Exception as ex:   # noqa: BLE001
            mal_rl05.append(("pared", repr(valor)[:20], f"lanza {type(ex).__name__}"))
        try:
            _, r_ = nuevo_reloj()
            r_._monotono = lambda v=valor: v
            x = r_.ahora()
            if x["codigo"] not in {"RL-01", "RL-05"} or r_.bloqueo is None:
                mal_rl05.append(("mono", repr(valor)[:20], x["codigo"]))
        except Exception as ex:   # noqa: BLE001
            mal_rl05.append(("mono", repr(valor)[:20], f"lanza {type(ex).__name__}"))
    h.chk("reloj_lecturas_de_fuente_imposibles_fallan_cerrado_RL05_o_RL01_y_bloquean",
          not mal_rl05, mal_rl05[:4])

    # ================================================================ rotación
    with tempfile.TemporaryDirectory() as td_rt:
        st = {n: {"lanz": 0, "mal": [], "deter": 0, "n": 0}
              for n in ("texto", "claves", "metadatos", "ficheros", "sin_firmar")}
        for i in range(CASOS_RT):
            nombre = list(st)[i % 5]
            st[nombre]["n"] += 1
            if nombre == "texto":
                args = (_mutar_doc(t1, rng, dentro_estado=rng.random() < 0.5), TM, MOTIVO, K1, K2)
                esperados, admite_ok = {"PE-01", "PE-03", "PE-06"}, False
                # la firma se comprueba ANTES que la huella: un firmado tocado da PE-06 (o PE-01/PE-03 si la
                # forma rota antes); PE-02 y CL-02 eran franquicias muertas (revisión de V0.62, hallazgos 1 y 3)
            elif nombre == "claves":
                args = (t1, TM, MOTIVO,
                        rng.choice([K1, None, b"corta", bytes(32), "K1", 7]),
                        rng.choice([K2, None, bytes(32), b"corta", 7]))
                esperados, admite_ok = {"OK", "CL-01", "PE-06"}, True
                # _previas da CL-01 para toda clave inválida ANTES de que cargar pudiera dar PE-07, y sin
                # cargar no hay rotación que se caiga: PE-07 y CL-02 eran franquicias muertas (revisión V0.62);
                # PE-06 con clave_vieja None sobre un documento firmado
            elif nombre == "metadatos":
                args = (t1, rng.choice(["ayer", None, 7, TM]),
                        rng.choice(["corto", "x" * 600, None, 7, MOTIVO]),
                        K1, K2, rng.choice(["G", None, "", 7, "OPERADOR"]))
                esperados, admite_ok = {"OK", "CL-01", "CL-03", "PE-06"}, True
            elif nombre == "ficheros":
                ruta_mala = rng.choice([None, "", "a\x00b", os.path.join(td_rt, "no", "e"), td_rt])
                try:
                    x = rt.rotar_ficheros(ruta_mala, os.path.join(td_rt, "d"), TM, MOTIVO, K1, K2)
                except Exception as ex:   # noqa: BLE001
                    st[nombre]["lanz"] += 1
                    st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                    continue
                if x["ok"] or x["codigo"] not in {"PE-05", "CL-04", "CL-01", "CL-03", "PE-01", "PE-07"}:
                    st[nombre]["mal"].append(x["codigo"])
                continue
            else:   # sin_firmar: documento sin firma mutado, con clave_vieja None (primera firma)
                args = (_mutar_doc(t0, rng, dentro_estado=rng.random() < 0.5), TM, MOTIVO, None, K1)
                esperados, admite_ok = {"PE-01", "PE-02", "PE-03"}, False
                # sin firmar, la huella SÍ se alcanza (PE-02) y la cabecera mutada da PE-03 (revisión de
                # V0.62, hallazgo 1); CL-02 era franquicia muerta (hallazgo 3)
            try:
                x = rt.rotar(*args)
                x2 = rt.rotar(*args)
            except Exception as ex:   # noqa: BLE001
                st[nombre]["lanz"] += 1
                st[nombre]["mal"].append(f"{type(ex).__name__}: {ex}")
                continue
            if (x["ok"], x["codigo"]) != (x2["ok"], x2["codigo"]):
                st[nombre]["deter"] += 1
            if x["codigo"] not in esperados or (x["ok"] and not admite_ok):
                st[nombre]["mal"].append(x["codigo"])
            if x["ok"] and nombre == "claves" and not pe.cargar(x["texto"], args[4])["ok"]:
                st[nombre]["mal"].append("una rotación ok no se vuelve a cargar con la clave nueva")
        h.chk("rotacion_rotar_y_rotar_ficheros_nunca_lanzan_en_150_casos",
              all(v["lanz"] == 0 for v in st.values()),
              [(k, v["mal"][:1]) for k, v in st.items() if v["lanz"]][:4])
        h.chk("rotacion_determinista_en_120_casos_de_rotar", all(v["deter"] == 0 for v in st.values()),
              [(k, v["deter"]) for k, v in st.items() if v["deter"]][:4])
        h.chk("rotacion_un_texto_mutado_no_se_rota_y_las_claves_o_metadatos_imposibles_fallan_cerrado",
              all(not v["mal"] for v in st.values()) and all(v["n"] > 0 for v in st.values()),
              [(k, v["mal"][:2]) for k, v in st.items() if v["mal"]][:6])
        r = rt.rotar(t1, TM, MOTIVO, K1, K2)
        h.chk("rotacion_el_camino_feliz_sigue_funcionando",
              r["ok"] and pe.cargar(r["texto"], K2)["ok"] and pe.cargar(r["texto"], K1)["codigo"] == "PE-06",
              r["codigo"])

    # ================================================================ casos fijos: anidado extremo
    # en el ESTADO de un documento (huella rehecha): cargar nunca lanza; si carga sin kill-switch, ida y vuelta
    d_an = json.loads(t0)
    d_an["estado"]["avisos"] = _profundo(500)
    texto_an = _rehacer(pe._texto(d_an))
    try:
        r = pe.cargar(texto_an)
        bien = r["codigo"] in {"OK", "O-13", "PE-03", "PE-04"} and (
            r["codigo"] != "OK" or pe.volcar(r["orquestador"], T) == texto_an)
    except Exception as ex:   # noqa: BLE001
        bien, r = False, f"{type(ex).__name__}: {ex}"
    h.chk("anidado_500_niveles_en_el_estado_cargar_nunca_lanza", bien, r)

    # en el TEXTO crudo (json.loads anidado): PE-01 sin lanzar en quien lo consume
    doc_an = json.loads(t0)
    doc_an["estado"] = _profundo(500)
    doc_an["atributos"] = sorted(doc_an["estado"])
    doc_an["huella"] = pe._huella(doc_an["estado"])
    texto_an = pe._texto(doc_an)
    mal_an = []
    for nombre_fn, fn in (("cargar", lambda: pe.cargar(texto_an)["codigo"]),
                          ("verificar", lambda: pe.verificar(texto_an)[1]["codigo"]),
                          ("migrar", lambda: mg.migrar(texto_an, TM, MOTIVO)["codigo"]),
                          ("rotar", lambda: rt.rotar(texto_an, TM, MOTIVO, None, K1)["codigo"])):
        try:
            if fn() != "PE-01":
                mal_an.append(nombre_fn)
        except Exception as ex:   # noqa: BLE001
            mal_an.append((nombre_fn, f"lanza {type(ex).__name__}"))
    h.chk("anidado_500_niveles_en_el_texto_crudo_PE01_en_cargar_verificar_migrar_y_rotar", not mal_an, mal_an)

    # guardar un estado con un valor anidado que desborda la pila: PE-01 sin lanzar y sin fichero
    o_an = nuevo()
    o_an.degradadas = {"X": _profundo(3000)}
    with tempfile.TemporaryDirectory() as td:
        ruta_an = os.path.join(td, "e.json")
        try:
            r = pe.guardar(o_an, ruta_an, T)
            bien = r["codigo"] == "PE-01" and not os.path.exists(ruta_an)
        except Exception as ex:   # noqa: BLE001
            bien, r = False, f"{type(ex).__name__}: {ex}"
        h.chk("anidado_3000_niveles_guardar_es_PE01_y_no_escribe_nada", bien, r)

    # en una línea del diario: DI-02 sin lanzar
    with tempfile.TemporaryDirectory() as td:
        re_, rd_ = os.path.join(td, "e"), os.path.join(td, "d")
        di.crear(nuevo(), re_, rd_, T)
        ls = open(rd_, encoding="ascii").read().splitlines()
        e = json.loads(ls[0])
        e["estado"] = _profundo(500)
        ls.append(_texto_doc({**e, "n": 2, "tipo": "PUNTO", "fichero": "a" * 64}))
        with open(rd_, "w", encoding="ascii") as f:
            f.write("\n".join(ls) + "\n")
        try:
            r = di.abrir(re_, rd_)
            bien = r["codigo"] == "DI-02"
        except Exception as ex:   # noqa: BLE001
            bien, r = False, f"{type(ex).__name__}: {ex}"
        h.chk("anidado_500_niveles_en_una_linea_del_diario_es_DI02_sin_lanzar", bien, r)

    # ---------------------------------------------------------------- r01 (regresión del hallazgo 1 de la
    # revisión de V0.62): los `esperados` de la batería cubren TODO lo que los módulos pueden responder con
    # los generadores de los objetivos. El resto de la batería corre con su semilla fija; este barrido corto
    # repite los objetivos con `esperados` con 25 semillas NUEVAS (seis casos por objetivo y semilla) y
    # exige que el código observado quede dentro del esperado de su objetivo (y ok solo donde el objetivo
    # lo admite). Unos esperados más estrechos que el contrato real del módulo solo fallan en falso con la
    # semilla equivocada: la entrega V0.62 admitía cuatro objetivos sin el PE-03 que una cabecera mutada
    # produce y pasó con la semilla 20261111 tras una tirada con ~2/3 de probabilidad de salir mal solo por
    # el objetivo del diario. Un lanzamiento aquí también es un fallo: las demás comprobaciones vigilan
    # «nunca lanzan» con su semilla, y r01 no puede dejar pasar una semilla que lance.
    SEMILLAS_R01, CASOS_OBJ_R01 = 25, 6
    mal_r01 = []
    with tempfile.TemporaryDirectory() as td_r01:
        re_r, rd_r = os.path.join(td_r01, "r01.e"), os.path.join(td_r01, "r01.d")
        ls_r01 = lineas_puras.splitlines()

        def g_pe_estado(rng, i):
            return pe.cargar(_mutar_doc(t0, rng, dentro_estado=True))

        def g_pe_cabecera(rng, i):
            return pe.cargar(_mutar_doc(t0, rng, dentro_estado=False))

        def g_pe_raiz(rng, i):
            raiz, _ = _mutar_en_sitio(json.loads(t0), rng)
            return pe.cargar(raiz if isinstance(raiz, str) else _texto_doc(raiz))

        def g_pe_firmado(rng, i):
            return pe.cargar(_mutar_doc(t1, rng, dentro_estado=rng.random() < 0.5))

        def g_pe_rehecho(rng, i):
            return pe.cargar(_rehacer(_mutar_doc(t0, rng, dentro_estado=True)))

        def g_di_linea(rng, i):
            ls = ls_r01[:]
            j = rng.randrange(len(ls))
            try:
                e = json.loads(ls[j])
                e, _ = _mutar_en_sitio(e, rng)
                ls[j] = _texto_doc(e)
            except (ValueError, TypeError):
                ls[j] = "{roto"
            with open(re_r, "w", encoding="ascii") as f:
                f.write(estado_puro)
            with open(rd_r, "w", encoding="ascii") as f:
                f.write("\n".join(ls) + "\n")
            return di.abrir(re_r, rd_r)

        def g_di_estado(rng, i):
            d_e = json.loads(estado_puro)
            d_e, _ = _mutar_en_sitio(d_e, rng)
            with open(re_r, "w", encoding="utf-8") as f:
                f.write(_texto_doc(d_e))
            with open(rd_r, "w", encoding="ascii") as f:
                f.write(lineas_puras)   # restaurados los DOS ficheros, como los casos de arriba
            return di.abrir(re_r, rd_r)

        def g_mg_texto(rng, i):
            return mg.migrar(_mutar_doc(t0, rng, dentro_estado=rng.random() < 0.5), TM, MOTIVO)

        def g_mg_registro(rng, i):
            return mg.migrar(t0, TM, MOTIVO,
                             registro=rng.choice([None, 7, "x", (), {"mal": None}]),
                             esquemas=rng.choice([None, 7, [], {"mal": None}, {"f" * 64: "sin parte"}]))

        def g_mg_metadatos(rng, i):
            return mg.migrar(t0, rng.choice(["ayer", None, 7, "2026-13-45T00:00:00+00:00", TM]),
                             rng.choice(["corto", "x" * 600, None, 7, MOTIVO]),
                             actor=rng.choice(["G", None, "", 7, "OPERADOR"]))

        def g_mg_rehecho(rng, i):
            return mg.migrar(_rehacer(_mutar_doc(t0, rng, dentro_estado=True)), TM, MOTIVO)

        def g_rt_texto(rng, i):
            return rt.rotar(_mutar_doc(t1, rng, dentro_estado=rng.random() < 0.5), TM, MOTIVO, K1, K2)

        def g_rt_claves(rng, i):
            return rt.rotar(t1, TM, MOTIVO,
                            rng.choice([K1, None, b"corta", bytes(32), "K1", 7]),
                            rng.choice([K2, None, bytes(32), b"corta", 7]))

        def g_rt_metadatos(rng, i):
            return rt.rotar(t1, rng.choice(["ayer", None, 7, TM]),
                            rng.choice(["corto", "x" * 600, None, 7, MOTIVO]),
                            K1, K2, rng.choice(["G", None, "", 7, "OPERADOR"]))

        def g_rt_sin_firmar(rng, i):
            return rt.rotar(_mutar_doc(t0, rng, dentro_estado=rng.random() < 0.5), TM, MOTIVO, None, K1)

        objetivos_r01 = (
            (g_pe_estado, {"PE-01", "PE-02"}, False),
            (g_pe_cabecera, {"PE-01", "PE-02", "PE-03", "PE-08"}, True),
            (g_pe_raiz, {"PE-01", "PE-02", "PE-03", "PE-08"}, True),
            (g_pe_firmado, {"PE-01", "PE-06"}, False),
            (g_pe_rehecho, {"OK", "O-13", "PE-01", "PE-02", "PE-03", "PE-04"}, True),
            (g_di_linea, {"DI-02", "DI-03", "DI-04"}, False),
            (g_di_estado, {"PE-01", "PE-02", "PE-03"}, False),
            (g_mg_texto, {"OK", "PE-01", "PE-02", "PE-03"}, True),
            (g_mg_registro, {"OK", "MG-01"}, True),
            (g_mg_metadatos, {"OK", "MG-05"}, True),
            (g_mg_rehecho, {"OK", "PE-01", "PE-02"}, True),
            (g_rt_texto, {"PE-01", "PE-03", "PE-06"}, False),
            (g_rt_claves, {"OK", "CL-01", "PE-06"}, True),
            (g_rt_metadatos, {"OK", "CL-01", "CL-03", "PE-06"}, True),
            (g_rt_sin_firmar, {"PE-01", "PE-02", "PE-03"}, False),
        )
        for s in range(SEMILLAS_R01):
            rng_r = random.Random(SEMILLA + 1 + s)
            for g, esp, ok_ok in objetivos_r01:
                for i in range(CASOS_OBJ_R01):
                    try:
                        r_r = g(rng_r, i)
                    except Exception as ex:   # noqa: BLE001
                        mal_r01.append((g.__name__, f"semilla {SEMILLA + 1 + s}", f"lanza {type(ex).__name__}"))
                        continue
                    if r_r["codigo"] not in esp or (r_r.get("ok") and not ok_ok):
                        mal_r01.append((g.__name__, f"semilla {SEMILLA + 1 + s}", r_r["codigo"]))
    h.chk("r01_los_esperados_cubren_todo_lo_que_el_modulo_puede_responder", not mal_r01, mal_r01[:8])

    # ---------------------------------------------------------------- determinismo de la batería entera
    def tirada():
        g = random.Random(SEMILLA)
        out = []
        for i in range(60):
            out.append(pe.cargar(_mutar_doc(t0, g, dentro_estado=i % 2 == 0))["codigo"])
        return out

    h.chk("bateria_determinista_misma_semilla_mismos_resultados", tirada() == tirada())

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO ROBUSTEZ T-03:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
