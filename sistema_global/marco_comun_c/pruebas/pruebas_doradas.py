"""Pruebas doradas (V0.66, pieza 7 del kit 2): las fotos fijas de la jornada y de la semana cuadran con
lo que el código hace hoy, y el aparato que las sostiene (resumen, gemelos, texto JSON y comparador) hace
lo que promete: determinista, nunca lanza, no cambia nada y da informes que se pueden leer.

Sin --regenerar (así lo corre la batería completa): regenera las dos fotos en memoria, las compara con las
entregadas en pruebas/doradas/ y, si hay diferencias, las informa paso a paso (camino, antes y después) y
falla. Con --regenerar: reescribe las fotos de pruebas/doradas/. Eso solo se hace a propósito, y cada
regeneración se explica en el Documento 0 de la pieza que la hizo, con la lista de diferencias aceptadas.

Uso: python3 pruebas/pruebas_doradas.py [--regenerar]
"""
import copy
import json
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

import doradas as do  # noqa: E402
import persistencia as pe  # noqa: E402
from pruebas_orquestador import AHORA, Arnes, nuevo  # noqa: E402
from pruebas_jornada import instante, pasos as pasos_jornada  # noqa: E402
from pruebas_semana import DIAS, pasos_semana  # noqa: E402
from vigilancia import vigilar  # noqa: E402


def _vigila_a_105(o, b):
    """El paso de vigilancia por objetivo de la jornada, con otro precio (1,05 en vez de 1,16): la copia
    del recorrido con la que la batería provoca un cambio. El objetivo ya no llega y el stop sí."""
    b.mover_precio("EURUSD", 1.05, instante(40))
    return vigilar(o, b, {"EURUSD": {"precio": 1.05, "hora": instante(40)}}, instante(40))


def _anidado(n):
    """Una estructura anidada n niveles, como las del generador de mutaciones de robustez."""
    x = "fondo"
    for _ in range(n):
        x = [x]
    return x


def _ciclico():
    """Un diccionario que se contiene a sí mismo: el resumen lo corta por profundidad, no se cuelga."""
    d = {}
    d["yo"] = d
    return d


class _O_Raro:
    """Un «Orquestador» roto a propósito para comprobar que el resumen falla cerrado: nada ilegible
    lanza, todo sale como ILEGIBLE (o como el caso más prudente, el kill activo)."""

    expedientes = None
    posiciones = {"P": {"estado": "ABIERTA", "cantidad": "mucho"}, "Q": None}
    avisos = [{"codigo": "O-19", "acuse": None}, "suelto", {"acuse": {"actor": "OPERADOR"}}]
    cfg = {}
    degradadas = {"TACTICA": {"motivo": "x", "ahora": "2026-11-06T09:00:00+00:00"}}
    kill = 0
    rearmes = None

    def nivel(self, cartera):
        raise ValueError("no sé")


class _O_Avisos_Raros(_O_Raro):
    """Y uno con los avisos en un diccionario: no es la lista que el Orquestador mantiene."""

    avisos = {"O-19": None}


def _sin_clave(x, clave):
    if isinstance(x, dict):
        return clave not in x and all(not _sin_clave(v, clave) for v in x.values())
    if isinstance(x, list):
        return all(not _sin_clave(v, clave) for v in x)
    return True


def _contiene(x, texto):
    if isinstance(x, dict):
        return any(_contiene(v, texto) for v in x.values())
    if isinstance(x, list):
        return any(_contiene(v, texto) for v in x)
    return x == texto


def _con_decimales_de_mas(x):
    if isinstance(x, float):
        return x != round(x, 6)
    if isinstance(x, dict):
        return any(_con_decimales_de_mas(v) for v in x.values())
    if isinstance(x, list):
        return any(_con_decimales_de_mas(v) for v in x)
    return False


def _json_estricto_y_ordenado(texto):
    """¿El texto es JSON estricto (sin NaN ni infinitos) y es exactamente el volcado ordenado e
    indentado de lo que dice? (Así las claves están ordenadas y el indentado es el de la foto.)"""
    try:
        foto = json.loads(texto, parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
    except (ValueError, TypeError):
        return False
    return texto == json.dumps(foto, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"


def _sin_mudar(r, o, instante_base):
    """¿El resumen deja el Orquestador y el resultado tal estaban? (volcado igual y copia igual)."""
    antes = pe.volcar(o, instante_base)
    rc = copy.deepcopy(r)
    do.resumen(r, o)
    return pe.volcar(o, instante_base) == antes and rc == r


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--regenerar" in argv:
        for r, p in sorted(do.generar_fotos().items()):
            n = len(json.loads(p.read_text(encoding="utf-8")))
            print(f"{p}: reescrita ({n} pasos)")
        print("Regeneración a propósito: explica en el Documento 0 de tu pieza las diferencias aceptadas.")
        return 0

    h = Arnes()
    # las fotos de hoy: los dos recorridos completos, regenerados en memoria
    foto_j, foto_s = do.FOTOS["jornada"](), do.FOTOS["semana"]()
    texto_j, texto_s = do.texto_foto(foto_j), do.texto_foto(foto_s)
    texto_entregada_j = (do.CARPETA_FOTOS / "jornada.json").read_text(encoding="utf-8")
    texto_entregada_s = (do.CARPETA_FOTOS / "semana.json").read_text(encoding="utf-8")

    h.chk("las_dos_fotos_regeneradas_coiniden_byte_a_byte_con_las_entregadas",
          texto_j == texto_entregada_j and texto_s == texto_entregada_s,
          (do.describe(do.comparar_fotos(json.loads(texto_entregada_j), foto_j))
           + do.describe(do.comparar_fotos(json.loads(texto_entregada_s), foto_s)))[:8])
    h.chk("la_foto_de_la_jornada_tiene_un_resumen_por_paso_en_el_orden_del_recorrido",
          [e["paso"] for e in foto_j] == [n for n, _ in pasos_jornada()], [e["paso"] for e in foto_j])
    h.chk("la_foto_de_la_semana_tiene_un_resumen_por_paso_en_el_orden_del_recorrido",
          [e["paso"] for e in foto_s] == [n for n, _, _ in pasos_semana()], [e["paso"] for e in foto_s])

    with tempfile.TemporaryDirectory() as tmp:
        b1 = {r: p.read_bytes() for r, p in do.generar_fotos(tmp).items()}
        b2 = {r: p.read_bytes() for r, p in do.generar_fotos(tmp).items()}
        solo = do.generar_fotos(tmp, recorridos=("semana",))   # el parámetro recorridos, ejercitado
        h.chk("regenerar_en_carpeta_temporal_da_el_mismo_fichero_dos_veces_y_el_mismo_que_en_memoria",
              b1 == b2 and b1["jornada"] == texto_j.encode("utf-8") and b1["semana"] == texto_s.encode("utf-8")
              and set(solo) == {"semana"} and solo["semana"].read_bytes() == b1["semana"]
              and do.leer_foto("jornada", tmp) == json.loads(texto_j) and do.leer_foto("semana", tmp) == json.loads(texto_s)
              and do.leer_foto("jornada") == json.loads(texto_entregada_j),
              {r: (len(b1[r]), len(b2[r])) for r in b1})
    h.chk("el_mismo_recorrido_dos_veces_da_la_misma_foto",
          do.FOTOS["jornada"]() == foto_j and do.FOTOS["semana"]() == foto_s, None)

    # un cambio provocado: una copia del recorrido de la jornada con otro precio en su paso de vigilancia
    pasos_mod = [(n, f) if n != "vigilar_objetivo" else ("vigilar_objetivo", _vigila_a_105) for n, f in pasos_jornada()]
    difs = do.comparar_fotos(foto_j, do.FOTOS["jornada"](pasos_mod))
    lineas = do.describe(difs)
    h.chk("un_precio_distinto_en_una_copia_del_recorrido_se_detecta",
          bool(difs) and any("vigilar_objetivo" in d["camino"] and ".acciones" in d["camino"] for d in difs),
          lineas[:6])
    h.chk("el_informe_nombra_el_paso_el_camino_y_los_valores_de_antes_y_despues",
          any("vigilar_objetivo" in l and "->" in l for l in lineas) and all(d["antes"] != d["después"] for d in difs),
          lineas[:4])

    # el comparador, por unidad: tres cambios de estado y de resultado provocados en una copia de la foto
    foto_j2 = copy.deepcopy(foto_j)
    idx4 = f"paso[4] ({foto_j[4]['paso']})"
    foto_j2[4]["estado"]["posiciones"]["POS-EXP-0001"]["cantidad"] = 99.5
    foto_j2[4]["resultado"].pop("posicion_id")
    foto_j2[4]["resultado"]["codigo"] = "O-01"
    caminos = {d["camino"]: (d["antes"], d["después"]) for d in do.comparar_fotos(foto_j, foto_j2)}
    h.chk("el_comparador_senala_el_camino_exacto_de_un_cambio_de_estado_provocado",
          caminos.get(f"{idx4}.estado.posiciones.POS-EXP-0001.cantidad") == (100.0, 99.5)
          and caminos.get(f"{idx4}.resultado.posicion_id") == ("POS-EXP-0001", do.AUSENTE)
          and caminos.get(f"{idx4}.resultado.codigo") == ("OK", "O-01") and len(caminos) == 3,
          sorted(caminos))

    # la forma de los resúmenes
    h.chk("los_resumenes_no_llevan_textos_de_motivo",
          _sin_clave(foto_j, "motivo") and _sin_clave(foto_s, "motivo"), None)

    mudas = []
    foto_j_hook = do.FOTOS["jornada"](observar=lambda n, r, o: mudas.append((n, _sin_mudar(r, o, AHORA))))
    foto_s_hook = do.FOTOS["semana"](observar=lambda n, r, o: mudas.append((n, _sin_mudar(r, o, DIAS["lunes"]))))
    h.chk("el_resumen_no_cambia_el_orquestador_ni_el_resultado_en_ningun_paso",
          len(mudas) == len(foto_j) + len(foto_s) and all(m for _, m in mudas),
          [n for n, m in mudas if not m][:3])
    h.chk("observar_no_perturba_la_foto",
          foto_j_hook == foto_j and foto_s_hook == foto_s, None)

    # lo raro no lanza y es determinista, con un Orquestador de verdad y con uno roto
    raros = [None, 42, "texto", [], {},
             {"ok": None, "codigo": 5, "motivo": "se va", "precio": float("nan"), "cantidad": float("inf"),
              "acciones": "no-es-lista"},
             {"ok": True, "acciones": [{"regla": "H-01", "codigo": "H-01", "ok": False}, "suelto"],
              "profundo": _anidado(500), "ciclico": _ciclico()},
             {"un_set": {"b", "a", 1}, "anidado": [{"frozenset": frozenset({1, 2})}]},
             {"1": "texto", 1: "numero", True: "bool"}]   # 1 y True colisionan tras str(): sale ILEGIBLE
    o_fresco = nuevo({"nivel_autonomia": {"TACTICA": "L2"}})
    try:
        parejas = [(do.resumen(r, o_fresco), do.resumen(r, o_fresco)) for r in raros]
        textos = [do.texto_foto([{"paso": "raros", **s}]) for s, _ in parejas]
        h.chk("el_resumen_aguenta_resultados_raros_sin_lanzar_y_es_determinista",
              all(a == b for a, b in parejas) and all(_json_estricto_y_ordenado(t) for t in textos)
              and all(_contiene(s["resultado"].get("ciclico"), do.CORTADO) for s, _ in parejas
                      if isinstance(s.get("resultado"), dict) and "ciclico" in s["resultado"])
              and parejas[-2][0]["resultado"]["un_set"] == do.ILEGIBLE
              and parejas[-2][0]["resultado"]["anidado"][0]["frozenset"] == do.ILEGIBLE
              and parejas[-1][0]["resultado"]["1"] == do.ILEGIBLE,   # sets y colisiones: ILEGIBLE, fijado
              None)
    except Exception as ex:   # noqa: BLE001 — la promesa es que nunca lanza
        h.chk("el_resumen_aguenta_resultados_raros_sin_lanzar_y_es_determinista", False, f"{type(ex).__name__}: {ex}")
    # el redondeo y los no finitos, fijados por unidad: los recorridos de hoy solo llevan cantidades exactas,
    # así que sin esta comprobación quitar el redondeo no cambiaría ninguna foto (sonda S1)
    nums = do.resumen({"nan": float("nan"), "pos": float("inf"), "neg": float("-inf"), "tercios": 1 / 3,
                       "mas": 0.12345675, "entero": 3, "si": True, "no": None}, o_fresco)["resultado"]
    h.chk("el_redondeo_a_seis_decimales_y_los_no_finitos_son_lo_que_la_foto_promete",
          nums["nan"] == "NaN" and nums["pos"] == "Infinity" and nums["neg"] == "-Infinity"
          and nums["tercios"] == round(1 / 3, 6) and nums["mas"] == round(0.12345675, 6)
          and nums["entero"] == 3 and nums["si"] is True and nums["no"] is None, nums)
    raro = do.resumen(None, _O_Raro())
    h.chk("el_resumen_aguenta_un_orquestador_roto_sin_lanzar_y_falla_cerrado",
          raro["estado"]["expedientes"] == do.ILEGIBLE and raro["estado"]["niveles"] == do.ILEGIBLE
          and raro["estado"]["rearmes"] == do.ILEGIBLE and raro["estado"]["posiciones"]["Q"] == do.ILEGIBLE
          and raro["estado"]["posiciones"]["P"]["cantidad"] == "mucho" and raro["estado"]["avisos"] == ["O-19"]
          and raro["estado"]["kill"] is True and do.resumen(None, _O_Raro()) == raro
          and do.resumen(None, _O_Avisos_Raros())["estado"]["avisos"] == do.ILEGIBLE,
          raro)

    # el formato de las fotos entregadas
    h.chk("las_fotos_son_json_valido_ordenado_e_indentado_y_sin_nan",
          _json_estricto_y_ordenado(texto_entregada_j) and _json_estricto_y_ordenado(texto_entregada_s), None)
    h.chk("las_cantidades_de_las_fotos_no_superan_seis_decimales",
          not _con_decimales_de_mas(foto_j) and not _con_decimales_de_mas(foto_s), None)

    # y las fotos documentan el comportamiento que ya conocemos (no son la foto de nada)
    j = {e["paso"]: e for e in foto_j}
    s = {e["paso"]: e for e in foto_s}
    h.chk("la_foto_marca_los_puntos_de_giro_conocidos_de_los_dos_recorridos",
          j["kill"]["estado"]["kill"] is True and j["kill"]["estado"]["rearmes"] == 0
          and j["rearmar"]["estado"]["kill"] is False and j["rearmar"]["estado"]["rearmes"] == 1
          and j["degradar"]["estado"]["niveles"]["TACTICA"] == "L1"
          and j["cerrar_operador"]["estado"]["posiciones"]["POS-EXP-0001"]["estado"] == "CERRADA"
          and j["ejecutar"]["resultado"]["posicion_id"] == "POS-EXP-0001"
          and s["viernes_kill"]["estado"]["kill"] is True and s["viernes_rearmar"]["estado"]["rearmes"] == 1
          and s["viernes_rearmar"]["estado"]["niveles"] == {"TACTICA": "L1", "TRADING": "L1"}
          and s["jueves_stop"]["estado"]["posiciones"]["POS-EXP-0001"]["estado"] == "CERRADA"
          and s["miercoles_ejecutar"]["estado"]["posiciones"]["POS-EXP-0003"]["cantidad"] == 50.0,
          None)

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO DORADAS:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
