"""Pruebas de robustez de los seis validadores que faltaban (V0.60, Pieza 1 del kit 2). Datos SIMULADOS.

Uso: python3 pruebas/pruebas_robustez_validadores.py

Lo mismo que pruebas/pruebas_robustez.py (V0.37) pero para validar_sobre.validar, validar_encargo.validar_encargo,
validar_contradictor.validar_informe, k_calidad.validar_sello, dimensionar (dimensionado) y vigilar (vigilancia):
con entradas mutadas al azar, con semilla fija (random.Random(20261110), nunca el random global), demuestra que
nunca lanzan, no mutan la entrada, son deterministas y fallan cerrado. Una comprobación puede cubrir N casos.

El generador de mutaciones (caminos, mutar, _mutar_en_sitio, _es_forma, _igual_nan) es el de la pieza de
robustez del fin de semana (pruebas/pruebas_robustez.py), importado sin cambiarlo. La separación «de forma» y
«de valor» que exige la pieza se adapta aquí al contrato JSON con _forma_real (ver abajo); el generador queda
tal cual.

Excepciones por diseño (no son defectos; cada una tiene su justificación, y las del calendario y del permiso de
apalancamiento tienen además comprobaciones fijas que acotan lo que sí se exige):

- borrar un ELEMENTO DE LISTA no rompe la forma del esquema JSON MIENTRAS la lista siga en su mínimo: la
  longitud es legal y lo que dispara, si algo, es una regla de contenido (en el sello, S-12: el hash ya no
  cuadra). Si el borrado deja la lista VACÍA o POR DEBAJO de su minItems del esquema (tabla _MIN_ITEMS,
  con los mínimos de los cuatro esquemas de esta batería), el documento YA NO conforma: se reclasifica
  como «de forma» en los objetivos MENSAJE y exige la regla de esquema (regresión r03, hallazgo 3 de la
  revisión independiente);
- sc3 y sello_encargo son claves del contexto del sobre que el Orquestador pasa SIEMPRE (orquestador.py):
  la vista del registro del Motor se reconstruye fiel para cada base (_vista_sc3_de) y sello_encargo es
  None (sin encargo vivo). Mutarlas cae en V-01 (vista o sello ilegibles) o V-26 (vista legible que ya no
  respalda las citas); None y una vista legible se admiten sin regla (el validador no puede verlas). El
  informe también recibe autoria_c y autoria_contradictor cuando el Orquestador las tiene configuradas:
  casos fijos r02 (hallazgo 2 de la revisión);
- el campo `estado` del sello está EXCLUIDO del hash por diseño (hash_del_sello lo deja fuera «porque
  cambia en la vida del sello»): VIGENTE<->CADUCADO respeta la forma, deja el sello VÁLIDO y sin S-12, y
  el consumidor lo ve con el E-16 del encargo (regresión r04, hallazgo 4 de la revisión; excepción
  declarada en Documento 0 y LEEME, no corregida);
- dimensionar y vigilar también llevan foto de NO MUTAR sus entradas (r01, hallazgo 1 de la revisión):
  las cuatro de dimensionar y el `ahora` (T1) de vigilar, además de los datos que ya se cubrían;
- sobre: una mutación del contexto que no toca lo que ESTE sobre consulta puede dejarlo válido: el validador
  solo lee el perfil citado (V-02), la ratificación de la clase de ESE perfil (V-06) y la bandera de
  apalancamiento si el sobre declara capital con apalancamiento distinto de 1 (V-15); una ratificación de otro
  perfil o de más no es dato roto para este sobre (todas las bases declaran apalancamiento 1, así que la
  bandera jamás cambia el resultado). En el MENSAJE, las claves que el esquema deja opcionales y una regla
  semántica exige por condición dan esa regla, no V-01: modelo_ref y motor_id de una cifra → V-08 (o V-20);
- encargo: mismo principio. E-16 solo valida el sello citado en sello_corte_ref (mutar otro sello del contexto
  no afecta); las claves opcionales del contrato 0.2.0 (controles y motivo de resultado_politica) pueden
  borrarse sin efecto (E-14 solo exige el resultado); cada restricción del encargo es opcional por separado y
  solo estrecha (borrar una deja las demás; si no queda ninguna, E-01); los mandatos del contexto declaran
  apalancamiento_max 1, así que la bandera de apalancamiento no cambia nada; el validador ignora las claves de
  más del calendario y de sellos que no cita;
- calendario (encargo y sello): el calendario del contexto se RECOMPUTA, no se firma: una mutación que no toca
  lo que se consulta (la versión, la raíz de mercados, la estructura de un mercado declarado o el año
  consultado de su lista `anios`) no puede discrepar con lo declarado en el sello; quitar un festivo solo hace
  la recomputación más permisiva. Lo que sí se exige, con casos fijos: sin version, sin mercados, anios con
  texto u hora_cierre_utc mal formada → S-01;
- informe: mutar el sobre que viaja en el contexto da C-02 por diseño (el informe ya no refiere ese sobre) en
  vez de C-01;
- vigilar: con datos que siguen frescos tras la mutación (un precio enorme, una clave extra en la raíz) H puede
  actuar con normalidad (cerrar por objetivo, por ejemplo): solo se exige la promesa «no cierra ni envía nada»
  para los datos rotos, que es lo que la pieza pide («con datos rotos»);
- dimensionar: E-01 es la regla de FORMA de la solicitud (campos exactos, política, precios, paso); una
  mutación de forma de una HOJA semántica da la regla que el diseño le asigna: divisa de cotización o tipo de
  cambio roto → E-03 (F vetaría, F-12); dirección o stop incoherentes → E-02. Lo que se exige a toda mutación
  de forma es fallar cerrado: ok False con un código E-01 a E-04 y cantidad 0.

Defecto real corregido en esta pieza (defecto_01): validar_sobre trataba CUALQUIER valor verdadero de
ctx["apalancamiento_permitido"] ("x", NaN, [1]) como permiso para apalancar; el encargo CT-G-01 ya exige
`is True` (mandato_ok). Corregido en validador/validar_sobre.py (V-15 solo se salta con True) y fijado con dos
comprobaciones: con permiso ajeno y apalancamiento 2 → V-15; con permiso True y apalancamiento 2 → válido.
"""
from __future__ import annotations

import copy
import json
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "validador"))
sys.path.insert(0, str(AQUI))

from control_f import POLITICA_DEFECTO  # noqa: E402
from dimensionado import dimensionar  # noqa: E402
from k_calidad import validar_sello  # noqa: E402
import motor  # noqa: E402
from validar_contradictor import validar_informe  # noqa: E402
from validar_encargo import validar_encargo  # noqa: E402
from validar_sobre import cargar_json, validar  # noqa: E402
from vigilancia import MAX_EDAD_MIN, _dato_fresco, vigilar  # noqa: E402
from pruebas_robustez import _es_forma, _igual_nan, _mutar_en_sitio, caminos, mutar  # noqa: E402
from pruebas_orquestador import Arnes  # noqa: E402

SEMILLA = 20261110
CASOS = 300        # por validador de mensajes (rotando entre sus entradas y sus bases válidas)
CASOS_E = 500      # dimensionar (rotando entre sus cuatro entradas)
CASOS_H = 200      # vigilar (mutando datos; Orquestador e intermediario nuevos en cada caso)
REGISTRO = {"regla", "ruta", "mensaje"}

# Reglas que se admite que dé una mutación «de forma» que afecta a lo consultado (falla cerrado con la
# regla correcta del diseño; la pieza solo fija la regla de forma del MENSAJE: V-01, E-01, C-01 y S-01).
ADMITE_SOBRE = {"sobre": {"V-01", "V-08", "V-20"}, "ahora": {"V-01"}, "fecha_corte_encargo": {"V-01"},
                "perfiles_activos": {"V-01", "V-02"}, "clases_ratificadas": {"V-01", "V-06"},
                "apalancamiento_permitido": {"V-01", "V-15"},
                "sc3": {"V-01", "V-26"}, "sello_encargo": {"V-01", "V-26"}}
ADMITE_ENC = {"msg": {"E-01"}, "ahora": {"E-01"}, "fecha_corte_vigente": {"E-01"},
              "perfiles_activos": {"E-01", "E-02"}, "apalancamiento_permitido": {"E-01"},
              "sellos": {"E-01", "E-16"}, "mandatos": {"E-01", "E-05", "E-07", "E-10", "E-17"},
              "calendario": {"E-01", "E-16"}}
ADMITE_INF = {"msg": {"C-01"}, "ahora": {"C-01"}, "sobre": {"C-01", "C-02"}}
ADMITE_E = {"E-01", "E-02", "E-03", "E-04"}   # ver la excepción de dimensionar en la cabecera


# Mínimos (minItems) de las listas de los cuatro esquemas de esta batería (esquemas/ct-g-02, ct-g-01,
# ct-g-03 y k-sello, todos 0.2.0), POR MENSAJE: un borrado que deja la lista vacía o por debajo de su
# mínimo rompe la forma del esquema (hallazgo 3 de la revisión). Ojo: la misma clave puede tener mínimo
# en un esquema y no en otro (data_refs lo tiene en el sobre y en el encargo, pero no en el informe).
_MIN_ITEMS = {
    "sobre": {"data_refs": 1, "cartera_compatible": 1, "incertidumbre": 1},
    "encargo": {"data_refs": 1, "exclusiones": 1},
    "informe": {"revisadas": 1, "escenarios_fallo": 1, "evid_refs": 1},
    "sello": {"mercados": 1, "fuentes": 1, "resultado_reglas": 15, "instrumentos": 1},
}


def _bajo_minimos(info, mutado, minimos):
    """True si la mutación fue borrar un ELEMENTO de una lista y la lista ha quedado vacía o por debajo de
    su minItems del esquema de ESTE mensaje (tabla por mensaje, por el nombre de la clave que la
    sostiene): entonces el documento YA NO conforma y la mutación es «de forma»."""
    if not info["ruta"] or not isinstance(info["ruta"][-1], int) or len(info["ruta"]) < 2:
        return False
    clave = info["ruta"][-2]
    if not isinstance(clave, str):
        return False
    minimo = minimos.get(clave)
    if minimo is None:
        return False
    try:
        x = mutado
        for p in info["ruta"][:-1]:
            x = x[p]
        return isinstance(x, list) and len(x) < minimo
    except (KeyError, IndexError, TypeError):
        return False


def _forma_real(info, mutado=None, minimos=None):
    """True si la mutación es «de forma» en sentido del esquema JSON: clave de más, clave requerida de
    menos (en un dict) o tipo cambiado; y también el borrado de un ELEMENTO que deja su lista vacía o por
    debajo de su minItems (_bajo_minimos), que es donde el documento deja de conformar (hallazgo 3 de la
    revisión; solo en objetivos MENSAJE, con la tabla de mínimos de SU esquema). Borrar un elemento sin
    bajar del mínimo no cambia la forma: el documento sigue conformando y lo que dispara, si algo, es una
    regla de contenido (en el sello, S-12: el hash ya no cuadra). Reclasifica el generador importado, que
    cuenta todo `borrar` como forma; para todo lo demás usa la clasificación importada tal cual."""
    if info["op"] == "borrar":
        if isinstance(info["ruta"][-1], int):
            return minimos is not None and _bajo_minimos(info, mutado, minimos)   # lista: forma solo bajo su mínimo
        return True                                                   # dict → clave de menos (forma)
    return _es_forma(info)   # extra → forma; valor/fecha → forma solo si cambia el tipo


def _vista_ilegible(v):
    """Copia del criterio de motor.vista_ok (misma condición, aquí para clasificar): True si la vista del
    registro del Motor no es None (no configurada) ni un registro legible {id: {modelo_ref, fecha_corte,
    sello_ref}} de textos. Una vista None o legible puede dejarla la mutación sin que el validador pueda
    verlo (el calendario del contexto se recomputa, no se firma, y aquí pasa lo mismo): no se exige regla;
    una vista ilegible da V-01."""
    if v is None:
        return False
    if not isinstance(v, dict):
        return True
    for k, x in v.items():
        if not (isinstance(k, str) and isinstance(x, dict)
                and {"modelo_ref", "fecha_corte", "sello_ref"} <= set(x)
                and all(isinstance(x[c], str) for c in ("modelo_ref", "fecha_corte", "sello_ref"))):
            return True
    return False


def _vista_sc3_de(sobre):
    """La vista del registro del Motor que el Orquestador pasaría para ESTE sobre (_vista_sc3): una entrada
    por cada artefacto citado (referencias.artefactos_motor y los motor_id de las cifras VERIFICADO o
    ESTIMADO), con el modelo que cada cifra declara y fecha de corte igual a la del sobre. Con ella las
    bases siguen válidas y el camino V-26 queda cubierto al mutar la clave (hallazgo 2 de la revisión)."""
    p = sobre["payload"]
    corte = p["identificacion"]["fecha_corte"]
    modelo_por_id = {}
    for _ruta, c in motor._cifras(p):
        aid = c.get("motor_id")
        if isinstance(aid, str):
            modelo_por_id.setdefault(aid, c.get("modelo_ref"))
    citados = (p.get("referencias") or {}).get("artefactos_motor") or []
    ids = list(citados) + [a for a in modelo_por_id if a not in citados]
    return {aid: {"modelo_ref": modelo_por_id.get(aid) or "modelo-de-referencia",
                  "fecha_corte": corte, "sello_ref": "SC-3-fixture-bateria"} for aid in ids}


def _perfil_sobre(sobre):
    return sobre["payload"]["identificacion"]["perfil"]


def _afecta_sobre(nombre, info, sobre, mutado=None):
    """True si la mutación del contexto toca algo que ESTE sobre consulta. El validador del sobre lee:
    ahora y fecha_corte_encargo (siempre), el perfil citado (V-02), la ratificación de la clase de ese perfil
    (V-06), la bandera de apalancamiento cuando el sobre declara capital con apalancamiento ≠ 1 (V-15) y,
    con el registro del Motor en el contexto, sc3 y sello_encargo (V-26; el Orquestador los pasa siempre,
    hallazgo 2 de la revisión)."""
    r = info["ruta"]
    if nombre == "sobre":
        if info["op"] == "borrar" and len(r) == 2 and r[0] == "resultado_politica" \
                and r[1] in ("controles", "motivo"):
            return False   # claves opcionales del contrato 0.2.0 (solo se exigen resultado y version_politica)
        return True
    if nombre in ("ahora", "fecha_corte_encargo"):
        return True
    if nombre == "perfiles_activos":
        if not r:
            return True                       # la lista entera sustituida: list() falla → V-01
        return info["antes"] == _perfil_sobre(sobre)
    if nombre == "clases_ratificadas":
        if info["op"] == "extra":
            return False                      # una ratificación de más no afecta a este sobre
        if not r:
            return True
        return r[0] == _perfil_sobre(sobre)
    if nombre == "apalancamiento_permitido":
        cap = sobre["payload"].get("capital")
        if not isinstance(cap, dict):
            return False
        a = cap.get("apalancamiento") or {}
        return a.get("estado") == "NO_ESTIMABLE" or a.get("valor") != 1
    if nombre == "sc3":
        return _vista_ilegible(mutado)   # None o vista legible: el validador no puede discrepar; ilegible → V-01
    if nombre == "sello_encargo":
        return mutado is not None        # None es «sin encargo vivo»; cualquier otra cosa exige V-01 o V-26
    return True


def _anios_consultados(sello):
    """Años del calendario que validar_sello consulta para ESTE sello: el del corte y los de las últimas
    observaciones de fuentes disponibles (es_habil y dias_habiles solo miran esas fechas)."""
    anios = set()
    try:
        anios.add(int(str(sello["fecha_corte"])[:4]))
        for x in sello.get("fuentes", []):
            if x.get("estado") == "DISPONIBLE":
                anios.add(int(str(x["ultima_observacion"])[:4]))
    except (KeyError, TypeError, ValueError, IndexError):
        pass
    return anios


def _calendario_afecta(info, sello):
    """True si la mutación del calendario (contexto) toca lo que validar_sello consulta para ESTE sello:
    la versión, la raíz de mercados, la estructura de un mercado DECLARADO o el año consultado de su lista
    `anios`. Los mercados no declarados no se consultan; quitar un festivo solo hace la recomputación más
    permisiva (no puede discrepar con lo declarado); las claves de más no se leen."""
    r = info["ruta"]
    if info["op"] == "extra":
        return False
    if not r or r[0] != "mercados":
        return True                           # version o la raíz de mercados: siempre se consultan
    declarados = {m["mercado"] for m in sello.get("mercados", []) if isinstance(m, dict)}
    if r[1] not in declarados:
        return False
    if len(r) >= 3 and r[2] == "festivos":
        return False   # la lista entera, un elemento o su tipo: sin esos festivos la recomputación no puede
                       # discrepar a favor del sello (solo hacerse más permisiva), y si el constructor
                       # lanza el validador responde por sí solo; se deja cubierto por las promesas generales
    if len(r) >= 4 and r[2] == "anios" and isinstance(r[3], int):
        return info["antes"] in _anios_consultados(sello)
    return True


def _afecta_encargo(nombre, info, msg, sellos_ctx):
    """True si la mutación del contexto toca algo que ESTE encargo consulta. E-16 solo valida el sello
    citado en sello_corte_ref; las claves opcionales del contrato 0.2.0 (controles y motivo) y cada
    restricción por separado pueden faltar sin efecto; los mandatos del contexto declaran
    apalancamiento_max 1, así que la bandera de apalancamiento no cambia nada."""
    r = info["ruta"]
    if nombre == "msg":
        if info["op"] == "borrar" and len(r) == 2 and r[0] == "resultado_politica" \
                and r[1] in ("controles", "motivo"):
            return False   # claves opcionales del contrato 0.2.0; E-14 solo exige el resultado
        if info["op"] == "borrar" and len(r) == 3 and r[0] == "payload" and r[1] == "restricciones":
            return False   # cada restricción es opcional por separado; solo estrechan
        return True
    if nombre in ("ahora", "fecha_corte_vigente"):
        return True
    if nombre == "perfiles_activos":
        if not r:
            return True
        return info["antes"] in (msg["consumer"], msg["payload"]["candidato"]["perfil"])
    if nombre == "apalancamiento_permitido":
        return False                          # mandatos con apalancamiento_max 1: la bandera no cambia nada
    if nombre == "sellos":
        if not r:
            return True                       # el diccionario entero: isinstance falla → E-01
        return r[0] == msg["payload"]["sello_corte_ref"]
    if nombre == "calendario":
        return _calendario_afecta(info, sellos_ctx.get(msg["payload"]["sello_corte_ref"], {}))
    return True                               # mandatos: set(m) == CLAVES, todo se valida


def _carga(ruta):
    return json.loads(ruta.read_text(encoding="utf-8"))


def _resumen(x):
    """Huella de un resultado para comparar dos llamadas (independiente del orden de la lista)."""
    return json.dumps(x, sort_keys=True, ensure_ascii=False, default=str)


def _resumenes(r):
    return sorted(_resumen(x) for x in r)


def _reglas(r):
    return sorted({x.get("regla") for x in r})


def _enlista(nombre, nbase, info, detalle, st):
    st[nombre]["mal"].append((nbase, info["ruta"], info["op"], detalle))


def main():
    rng = random.Random(SEMILLA)
    h = Arnes()

    # ---------------------------------------------------------------- fixtures
    sobres = [(p.name, cargar_json(p.read_text(encoding="utf-8")))
              for p in sorted((AQUI / "validos").glob("*.json"))]
    CTX_SOBRE = _carga(AQUI / "contexto.json")
    encargos = [(p.name, _carga(p)) for p in sorted((AQUI / "encargos" / "validos").glob("*.json"))]
    sellos = [(p.name, _carga(p)) for p in sorted((AQUI / "k").glob("valido_*.sello.json"))]
    from pruebas_encargo import CTX as CTX_ENC          # noqa: E402
    from pruebas_contradictor import AHORA as AHORA_CTR, informe as informe_ctr, sobre_base  # noqa: E402
    from pruebas_k import CAL                            # noqa: E402
    from pruebas_dimensionado import AHORA as AHORA_E, CART, SOL  # noqa: E402

    # ---------------------------------------------------------------- el generador, importado sin cambiarlo
    d = {"a": 1, "b": [10, {"c": None}]}
    h.chk("generador_caminos_importado_y_completo",
          set(caminos(d)) == {(), ("a",), ("b",), ("b", 0), ("b", 1), ("b", 1, "c")},
          sorted(map(str, caminos(d))))
    m1 = [repr(mutar(d, rng)) for _ in range(30)]
    h.chk("generador_mutar_importado_da_copia_y_variedad",
          all(mutar(d, random.Random(SEMILLA)) != d for _ in range(20)) and len(set(m1)) > 5, len(set(m1)))

    # ================================================================ validar_sobre.validar
    CLAVES_CTX_SOBRE = ("ahora", "fecha_corte_encargo", "perfiles_activos", "clases_ratificadas",
                        "apalancamiento_permitido", "sc3", "sello_encargo")

    def ctx_sobre(s=None):
        """El contexto que pasa el Orquestador para el sobre `s`: las claves del fixture más la vista del
        registro del Motor (sc3) reconstruida para ESE sobre y el sello de K del encargo vivo (None si no
        lo hay): son claves que el Orquestador pasa SIEMPRE (hallazgo 2 de la revisión)."""
        c = copy.deepcopy(CTX_SOBRE)
        if s is not None:
            c["sc3"] = _vista_sc3_de(s)
            c["sello_encargo"] = None
        return c

    for n, s in sobres:
        h.chk(f"sobre_base_valido_{n.replace('valido_', '').replace('.json', '')}",
              validar(s, ctx_sobre(s)) == [], _resumenes(validar(s, ctx_sobre(s))))
    st = {k: {"lanz": 0, "forma": 0, "mal": [], "sinreg": 0, "muta": 0, "deter": 0}
          for k in ("sobre",) + CLAVES_CTX_SOBRE}
    for i in range(CASOS):
        nombre, (nbase, base) = list(st)[i % 8], sobres[i % len(sobres)]
        s, c = copy.deepcopy(base), ctx_sobre(base)
        objetivo = s if nombre == "sobre" else c[nombre]
        objetivo, info = _mutar_en_sitio(objetivo, rng)
        if nombre == "sobre":
            s = objetivo
        else:
            c[nombre] = objetivo
        mutado = objetivo
        foto = copy.deepcopy({"sobre": s, "contexto": c})
        try:
            r = validar(s, c)
        except Exception as ex:   # noqa: BLE001
            st[nombre]["lanz"] += 1
            _enlista(nombre, nbase, info, f"{type(ex).__name__}: {ex}", st)
            continue
        if not (isinstance(r, list) and all(isinstance(x, dict) and REGISTRO <= set(x) for x in r)):
            st[nombre]["sinreg"] += 1
            continue
        if not _igual_nan(foto, {"sobre": s, "contexto": c}):
            st[nombre]["muta"] += 1
            continue
        if _resumenes(validar(copy.deepcopy(s), copy.deepcopy(c))) != _resumenes(r):
            st[nombre]["deter"] += 1
            continue
        if _forma_real(info, mutado, _MIN_ITEMS["sobre"] if nombre == "sobre" else None):
            st[nombre]["forma"] += 1
            reglas = _reglas(r)
            if not r:
                if _afecta_sobre(nombre, info, s, mutado):
                    _enlista(nombre, nbase, info, "lista vacía", st)
            elif not (set(reglas) & ADMITE_SOBRE[nombre]):
                _enlista(nombre, nbase, info, reglas, st)
    h.chk("sobre_nunca_lanza_en_300_casos", all(v["lanz"] == 0 for v in st.values()),
          [(k, x) for k, v in st.items() for x in v["mal"][:1] if v["lanz"]][:3])
    h.chk("sobre_devuelve_registros_con_regla_ruta_mensaje", all(v["sinreg"] == 0 for v in st.values()),
          [(k, v["sinreg"]) for k, v in st.items() if v["sinreg"]])
    h.chk("sobre_no_muta_la_entrada_en_300_casos", all(v["muta"] == 0 for v in st.values()),
          [(k, v["muta"]) for k, v in st.items() if v["muta"]])
    h.chk("sobre_dos_llamadas_dan_lo_mismo_en_300_casos", all(v["deter"] == 0 for v in st.values()),
          [(k, v["deter"]) for k, v in st.items() if v["deter"]])
    h.chk("sobre_forma_da_V01_o_la_regla_del_contexto_con_las_excepciones_de_diseno",
          all(v["forma"] > 0 and not v["mal"] for v in st.values()),
          [(k, v["mal"][:2]) for k, v in st.items() if v["mal"]][:4])

    # ---------------------------------------------------------------- defecto_01: permiso de apalancamiento ajeno
    s_d = copy.deepcopy(sobres[0][1])
    s_d["payload"]["capital"]["apalancamiento"]["valor"] = 2
    ctx_x = ctx_sobre(s_d)
    ctx_x["apalancamiento_permitido"] = "x"
    h.chk("defecto_01_permiso_ajeno_no_habilita_apalancamiento_V15",
          "V-15" in _reglas(validar(s_d, ctx_x)), _reglas(validar(s_d, ctx_x)))
    ctx_t = ctx_sobre(s_d)
    ctx_t["apalancamiento_permitido"] = True
    h.chk("defecto_01_permiso_verdadero_habilita_apalancamiento_2x",
          validar(s_d, ctx_t) == [], _resumenes(validar(s_d, ctx_t)))

    # ================================================================ validar_encargo.validar_encargo
    CLAVES_CTX_ENC = ("ahora", "fecha_corte_vigente", "perfiles_activos", "apalancamiento_permitido",
                      "sellos", "mandatos", "calendario")

    def ctx_enc():
        return copy.deepcopy(CTX_ENC)

    for n, e in encargos:
        h.chk(f"encargo_base_valido_{n.replace('valido_', '').replace('.json', '')}",
              validar_encargo(e, ctx_enc()) == [], _resumenes(validar_encargo(e, ctx_enc())))
    st = {k: {"lanz": 0, "forma": 0, "mal": [], "sinreg": 0, "muta": 0, "deter": 0}
          for k in ("msg",) + CLAVES_CTX_ENC}
    for i in range(CASOS):
        nombre, (nbase, base) = list(st)[i % 8], encargos[i % len(encargos)]
        m, c = copy.deepcopy(base), ctx_enc()
        objetivo = m if nombre == "msg" else c[nombre]
        objetivo, info = _mutar_en_sitio(objetivo, rng)
        if nombre == "msg":
            m = objetivo
        else:
            c[nombre] = objetivo
        mutado = objetivo
        foto = copy.deepcopy({"msg": m, "contexto": c})
        try:
            r = validar_encargo(m, c)
        except Exception as ex:   # noqa: BLE001
            st[nombre]["lanz"] += 1
            _enlista(nombre, nbase, info, f"{type(ex).__name__}: {ex}", st)
            continue
        if not (isinstance(r, list) and all(isinstance(x, dict) and REGISTRO <= set(x) for x in r)):
            st[nombre]["sinreg"] += 1
            continue
        if not _igual_nan(foto, {"msg": m, "contexto": c}):
            st[nombre]["muta"] += 1
            continue
        if _resumenes(validar_encargo(copy.deepcopy(m), copy.deepcopy(c))) != _resumenes(r):
            st[nombre]["deter"] += 1
            continue
        if _forma_real(info, mutado, _MIN_ITEMS["encargo"] if nombre == "msg" else None):
            st[nombre]["forma"] += 1
            reglas = _reglas(r)
            if not r:
                if _afecta_encargo(nombre, info, m, CTX_ENC["sellos"]):
                    _enlista(nombre, nbase, info, "lista vacía", st)
            elif not (set(reglas) & ADMITE_ENC[nombre]):
                _enlista(nombre, nbase, info, reglas, st)
    h.chk("encargo_nunca_lanza_en_300_casos", all(v["lanz"] == 0 for v in st.values()),
          [(k, x) for k, v in st.items() for x in v["mal"][:1] if v["lanz"]][:3])
    h.chk("encargo_devuelve_registros_con_regla_ruta_mensaje", all(v["sinreg"] == 0 for v in st.values()),
          [(k, v["sinreg"]) for k, v in st.items() if v["sinreg"]])
    h.chk("encargo_no_muta_la_entrada_en_300_casos", all(v["muta"] == 0 for v in st.values()),
          [(k, v["muta"]) for k, v in st.items() if v["muta"]])
    h.chk("encargo_dos_llamadas_dan_lo_mismo_en_300_casos", all(v["deter"] == 0 for v in st.values()),
          [(k, v["deter"]) for k, v in st.items() if v["deter"]])
    h.chk("encargo_forma_da_E01_o_la_regla_del_contexto_con_las_excepciones_de_diseno",
          all(v["forma"] > 0 and not v["mal"] for v in st.values()),
          [(k, v["mal"][:2]) for k, v in st.items() if v["mal"]][:4])

    # ================================================================ validar_contradictor.validar_informe
    sobre_ctr = sobre_base()
    h.chk("informe_base_valido_sin_fallos",
          validar_informe(informe_ctr(sobre_base()), {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_ctr)}) == [],
          _resumenes(validar_informe(informe_ctr(sobre_base()), {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_ctr)})))
    st = {k: {"lanz": 0, "forma": 0, "mal": [], "sinreg": 0, "muta": 0, "deter": 0} for k in ("msg", "ahora", "sobre")}
    for i in range(CASOS):
        nombre = list(st)[i % 3]
        m = informe_ctr(sobre_base())
        c = {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_ctr)}
        objetivo = m if nombre == "msg" else c[nombre]
        objetivo, info = _mutar_en_sitio(objetivo, rng)
        if nombre == "msg":
            m = objetivo
        else:
            c[nombre] = objetivo
        mutado = objetivo
        foto = copy.deepcopy({"msg": m, "contexto": c})
        try:
            r = validar_informe(m, c)
        except Exception as ex:   # noqa: BLE001
            st[nombre]["lanz"] += 1
            _enlista(nombre, nombre, info, f"{type(ex).__name__}: {ex}", st)
            continue
        if not (isinstance(r, list) and all(isinstance(x, dict) and REGISTRO <= set(x) for x in r)):
            st[nombre]["sinreg"] += 1
            continue
        if not _igual_nan(foto, {"msg": m, "contexto": c}):
            st[nombre]["muta"] += 1
            continue
        if _resumenes(validar_informe(copy.deepcopy(m), copy.deepcopy(c))) != _resumenes(r):
            st[nombre]["deter"] += 1
            continue
        if _forma_real(info, mutado, _MIN_ITEMS["informe"] if nombre == "msg" else None):
            st[nombre]["forma"] += 1
            reglas = _reglas(r)
            if not r:
                _enlista(nombre, nombre, info, "lista vacía", st)
            elif not (set(reglas) & ADMITE_INF[nombre]):
                _enlista(nombre, nombre, info, reglas, st)
    h.chk("informe_nunca_lanza_en_300_casos", all(v["lanz"] == 0 for v in st.values()),
          [(k, x) for k, v in st.items() for x in v["mal"][:1] if v["lanz"]][:3])
    h.chk("informe_devuelve_registros_con_regla_ruta_mensaje", all(v["sinreg"] == 0 for v in st.values()),
          [(k, v["sinreg"]) for k, v in st.items() if v["sinreg"]])
    h.chk("informe_no_muta_la_entrada_en_300_casos", all(v["muta"] == 0 for v in st.values()),
          [(k, v["muta"]) for k, v in st.items() if v["muta"]])
    h.chk("informe_dos_llamadas_dan_lo_mismo_en_300_casos", all(v["deter"] == 0 for v in st.values()),
          [(k, v["deter"]) for k, v in st.items() if v["deter"]])
    h.chk("informe_forma_da_C01_y_C02_para_el_sobre_del_contexto",
          all(v["forma"] > 0 and not v["mal"] for v in st.values()),
          [(k, v["mal"][:2]) for k, v in st.items() if v["mal"]][:4])

    # ---------------------------------------------------------------- r02: la autoría que pasa el Orquestador (hallazgo 2)
    # El Orquestador pasa autoria_c y autoria_contradictor cuando están configuradas (orquestador.py); el
    # contexto del fixture no las trae, así que se cubren con casos fijos. Con la autoría de C coherente
    # con la diversidad declarada el informe sigue válido; una autoria_c o autoria_contradictor de forma
    # rota (lista) se queda SIN comprobación en silencio (diversidad() las trata como desconocidas; el
    # Orquestador valida su configuración con _autoria_ok, así que no hay camino práctico: lo investigó el
    # revisor y lo deja anotado para una pieza futura); un dict mal formado lanza por dentro y el
    # envoltorio lo convierte en C-01 (falla cerrado); y una autoria_contradictor bien formada de otro
    # modelo dispara la C-11 que sí existe.
    inf_r02 = informe_ctr(sobre_base())
    a_r02 = inf_r02["payload"]["autoria"]
    if a_r02["diversidad"] == "MISMO_MODELO":
        aut_c_r02 = {"modelo": a_r02["modelo"], "proveedor": a_r02["proveedor"]}
    elif a_r02["diversidad"] == "OTRO_MODELO":
        aut_c_r02 = {"modelo": "ZZZ-otro-modelo", "proveedor": a_r02["proveedor"]}
    else:   # OTRO_PROVEEDOR: modelo y proveedor distintos (un mismo modelo revendido es MISMO_MODELO)
        aut_c_r02 = {"modelo": "ZZZ-otro-modelo", "proveedor": "ZZZ-otro-proveedor"}
    ctx_r02 = {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_ctr), "autoria_c": aut_c_r02,
               "autoria_contradictor": {"modelo": a_r02["modelo"], "proveedor": a_r02["proveedor"]}}
    h.chk("r02_informe_valido_con_la_autoria_que_pasa_el_orquestador",
          validar_informe(inf_r02, copy.deepcopy(ctx_r02)) == [],
          _resumenes(validar_informe(inf_r02, copy.deepcopy(ctx_r02))))
    c_r02 = copy.deepcopy(ctx_r02)
    c_r02["autoria_c"] = {"modelo": 17, "proveedor": None}
    h.chk("r02_autoria_c_mal_formada_la_diversidad_se_queda_sin_comprobacion_en_silencio",
          validar_informe(inf_r02, c_r02) == [], _resumenes(validar_informe(inf_r02, c_r02)))
    c_r02 = copy.deepcopy(ctx_r02)
    c_r02["autoria_contradictor"] = ["no", "es", "dict"]
    h.chk("r02_autoria_contradictor_de_forma_rota_tambien_se_queda_sin_comprobacion",
          validar_informe(inf_r02, c_r02) == [], _resumenes(validar_informe(inf_r02, c_r02)))
    c_r02 = copy.deepcopy(ctx_r02)
    c_r02["autoria_contradictor"] = {"modelo": 17, "proveedor": None}
    h.chk("r02_autoria_contradictor_con_dict_mal_formado_falla_cerrado_C01",
          "C-01" in _reglas(validar_informe(inf_r02, c_r02)), _reglas(validar_informe(inf_r02, c_r02)))
    c_r02 = copy.deepcopy(ctx_r02)
    c_r02["autoria_contradictor"] = {"modelo": "otro-modelo", "proveedor": "otro-proveedor"}
    h.chk("r02_autoria_contradictor_de_otro_modelo_dispara_C11",
          "C-11" in _reglas(validar_informe(inf_r02, c_r02)), _reglas(validar_informe(inf_r02, c_r02)))

    # ================================================================ k_calidad.validar_sello
    for n, s in sellos:
        h.chk(f"sello_base_valido_{n.replace('valido_', '').replace('.sello.json', '')}",
              validar_sello(s, {"calendario": CAL}) == [], _resumenes(validar_sello(s, {"calendario": CAL})))

    # ---------------------------------------------------------------- el calendario del contexto, con casos fijos
    # (el calendario se recomputa, no se firma: estos cuatro casos fijan lo que sí se exige; lo que no toca
    # lo consultado queda cubierto por las promesas generales de los casos aleatorios de abajo)
    cal0 = copy.deepcopy(CAL)
    del cal0["version"]
    h.chk("calendario_sin_version_da_S01_falla_cerrado",
          _reglas(validar_sello(sellos[0][1], {"calendario": cal0})) == ["S-01"],
          _reglas(validar_sello(sellos[0][1], {"calendario": cal0})))
    cal1 = copy.deepcopy(CAL)
    cal1["mercados"] = 0
    h.chk("calendario_sin_mercados_da_S01_falla_cerrado",
          _reglas(validar_sello(sellos[0][1], {"calendario": cal1})) == ["S-01"],
          _reglas(validar_sello(sellos[0][1], {"calendario": cal1})))
    cal2 = copy.deepcopy(CAL)
    primer_mercado = next(iter(cal2["mercados"]))
    cal2["mercados"][primer_mercado]["anios"] = ["texto"]
    h.chk("calendario_con_anios_de_texto_da_S01_falla_cerrado",
          _reglas(validar_sello(sellos[0][1], {"calendario": cal2})) == ["S-01"],
          _reglas(validar_sello(sellos[0][1], {"calendario": cal2})))
    cal3 = copy.deepcopy(CAL)
    cal3["mercados"][primer_mercado]["hora_cierre_utc"] = "25:00"
    h.chk("calendario_con_hora_cierre_mal_formada_da_S01_falla_cerrado",
          _reglas(validar_sello(sellos[0][1], {"calendario": cal3})) == ["S-01"],
          _reglas(validar_sello(sellos[0][1], {"calendario": cal3})))

    st = {"sello": {"lanz": 0, "forma": 0, "mal": [], "valor": 0, "valor_mal": [], "sinreg": 0, "muta": 0, "deter": 0},
          "calendario": {"lanz": 0, "forma": 0, "mal": [], "valor": 0, "valor_mal": [], "sinreg": 0, "muta": 0, "deter": 0}}
    rotacion_sello = ("sello", "sello", "sello", "sello", "calendario")
    for i in range(CASOS):
        nombre, (nbase, base) = rotacion_sello[i % 5], sellos[i % len(sellos)]
        s, c = copy.deepcopy(base), {"calendario": copy.deepcopy(CAL)}
        objetivo = s if nombre == "sello" else c["calendario"]
        objetivo, info = _mutar_en_sitio(objetivo, rng)
        if nombre == "sello":
            s = objetivo
        else:
            c["calendario"] = objetivo
        mutado = objetivo
        foto = copy.deepcopy({"sello": s, "contexto": c})
        try:
            r = validar_sello(s, c)
        except Exception as ex:   # noqa: BLE001
            st[nombre]["lanz"] += 1
            _enlista(nombre, nbase, info, f"{type(ex).__name__}: {ex}", st)
            continue
        if not (isinstance(r, list) and all(isinstance(x, dict) and REGISTRO <= set(x) for x in r)):
            st[nombre]["sinreg"] += 1
            continue
        if not _igual_nan(foto, {"sello": s, "contexto": c}):
            st[nombre]["muta"] += 1
            continue
        if _resumenes(validar_sello(copy.deepcopy(s), copy.deepcopy(c))) != _resumenes(r):
            st[nombre]["deter"] += 1
            continue
        reglas = _reglas(r)
        if _forma_real(info, mutado, _MIN_ITEMS["sello"] if nombre == "sello" else None):
            st[nombre]["forma"] += 1
            if nombre == "sello" and ("S-01" not in reglas or not r):
                _enlista(nombre, nbase, info, reglas, st)
        elif "S-01" not in reglas:
            st[nombre]["valor"] += 1
            if nombre == "sello" and "S-12" not in reglas:
                st[nombre]["valor_mal"].append((nbase, info["ruta"], reglas))
    h.chk("sello_nunca_lanza_en_300_casos", all(v["lanz"] == 0 for v in st.values()),
          [(k, x) for k, v in st.items() for x in v["mal"][:1] if v["lanz"]][:3])
    h.chk("sello_devuelve_registros_con_regla_ruta_mensaje", all(v["sinreg"] == 0 for v in st.values()),
          [(k, v["sinreg"]) for k, v in st.items() if v["sinreg"]])
    h.chk("sello_no_muta_la_entrada_en_300_casos", all(v["muta"] == 0 for v in st.values()),
          [(k, v["muta"]) for k, v in st.items() if v["muta"]])
    h.chk("sello_dos_llamadas_dan_lo_mismo_en_300_casos", all(v["deter"] == 0 for v in st.values()),
          [(k, v["deter"]) for k, v in st.items() if v["deter"]])
    h.chk("sello_forma_da_S01", st["sello"]["forma"] > 0 and not st["sello"]["mal"],
          st["sello"]["mal"][:2])
    h.chk("sello_valor_que_respeta_la_forma_da_S12",
          st["sello"]["valor"] > 0 and not st["sello"]["valor_mal"], st["sello"]["valor_mal"][:3])

    # ---------------------------------------------------------------- r03 y r04: hallazgos 3 y 4 de la revisión
    # r03: un borrado que deja la lista VACÍA o por debajo de su minItems rompe la forma del esquema: se
    # reclasifica como «de forma» (_forma_real con el mutado, solo en objetivos MENSAJE) y exige la regla
    # de esquema; aquí quedan fijados los casos de las listas con mínimo de los cuatro mensajes (tabla
    # _MIN_ITEMS, de los esquemas 0.2.0).
    # r04: `estado` del sello está excluido del hash por diseño («cambia en la vida del sello»): alterarlo
    # dentro del enum respeta la forma, deja el sello VÁLIDO y sin S-12; el consumidor lo ve con el E-16
    # del encargo. Excepción declarada en Documento 0 y LEEME; el comportamiento real, fijado aquí.
    def _sin_lista(msg, ruta):
        x = msg
        for p in ruta:
            x = x[p]
        x.clear()
        return msg

    mal_r03 = []

    def _prueba_min(modulo, nombre_caso, msg, esperada):
        if modulo == "sobre":
            r = validar(msg, ctx_sobre(msg))
        elif modulo == "encargo":
            r = validar_encargo(msg, ctx_enc())
        elif modulo == "informe":
            r = validar_informe(msg, {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_ctr)})
        else:
            r = validar_sello(msg, {"calendario": copy.deepcopy(CAL)})
        if esperada not in _reglas(r):
            mal_r03.append((modulo, nombre_caso, _reglas(r) or "VÁLIDO"))

    s_mr = copy.deepcopy(sobres[0][1])
    if s_mr.get("data_refs"):
        _prueba_min("sobre", "data_refs", _sin_lista(s_mr, ("data_refs",)), "V-01")
    for n_mr, s_mr in sobres:
        if len(s_mr["payload"]["identificacion"]["cartera_compatible"]) == 1:
            _prueba_min("sobre", f"{n_mr}: cartera_compatible",
                        _sin_lista(copy.deepcopy(s_mr), ("payload", "identificacion", "cartera_compatible")), "V-01")
            break
    if len(sobres[0][1].get("incertidumbre", [])) == 1:
        _prueba_min("sobre", "incertidumbre",
                    _sin_lista(copy.deepcopy(sobres[0][1]), ("incertidumbre",)), "V-01")
    e_mr = copy.deepcopy(encargos[0][1])
    if e_mr.get("data_refs"):
        _prueba_min("encargo", "data_refs", _sin_lista(e_mr, ("data_refs",)), "E-01")
    _prueba_min("informe", "revisadas",
                _sin_lista(informe_ctr(sobre_base()), ("payload", "cobertura", "revisadas")), "C-01")
    _prueba_min("informe", "escenarios_fallo",
                _sin_lista(informe_ctr(sobre_base()), ("payload", "escenarios_fallo")), "C-01")
    inf_ev = informe_ctr(sobre_base())
    if inf_ev["payload"]["escenarios_fallo"][0].get("evid_refs"):
        _prueba_min("informe", "evid_refs",
                    _sin_lista(inf_ev, ("payload", "escenarios_fallo", 0, "evid_refs")), "C-01")
    for n_mr, k_mr in sellos:
        if len(k_mr.get("mercados", [])) == 1:
            _prueba_min("sello", f"{n_mr}: mercados", _sin_lista(copy.deepcopy(k_mr), ("mercados",)), "S-01")
            break
    if sellos[0][1].get("fuentes"):
        _prueba_min("sello", "fuentes", _sin_lista(copy.deepcopy(sellos[0][1]), ("fuentes",)), "S-01")
    k_rr = copy.deepcopy(sellos[0][1])
    if len(k_rr.get("resultado_reglas", [])) == 15:
        del k_rr["resultado_reglas"][7]
        _prueba_min("sello", "resultado_reglas 15->14", k_rr, "S-01")
    k_ev = copy.deepcopy(sellos[0][1])
    if k_ev.get("eventos") and k_ev["eventos"][0].get("instrumentos"):
        _prueba_min("sello", "eventos[0].instrumentos",
                    _sin_lista(k_ev, ("eventos", 0, "instrumentos")), "S-01")
    h.chk("r03_borrados_que_dejan_la_lista_bajo_su_minItems_dan_la_regla_de_esquema",
          not mal_r03, mal_r03[:4])

    k_est = copy.deepcopy(sellos[0][1])
    k_est["estado"] = "CADUCADO" if k_est["estado"] == "VIGENTE" else "VIGENTE"
    r_est = validar_sello(k_est, {"calendario": copy.deepcopy(CAL)})
    h.chk("r04_sello_con_estado_alterado_en_el_enum_sin_S12_el_hash_lo_excluye",
          r_est == [] and "S-12" not in _reglas(r_est), _reglas(r_est) or "VÁLIDO")
    from pruebas_encargo import encargo_div  # noqa: E402
    enc_est = encargo_div()
    enc_est["payload"]["sello_corte_ref"] = k_est["sello_id"]
    ct_est = copy.deepcopy(CTX_ENC)
    ct_est["sellos"] = dict(CTX_ENC["sellos"])
    ct_est["sellos"][k_est["sello_id"]] = k_est
    h.chk("r04_el_encargo_ve_el_estado_alterado_del_sello_con_E16",
          "E-16" in _reglas(validar_encargo(enc_est, ct_est)),
          _reglas(validar_encargo(enc_est, ct_est)))

    # ================================================================ dimensionado.dimensionar
    def entradas_e():
        return {"sol": copy.deepcopy(SOL), "cart": copy.deepcopy(CART),
                "pol": copy.deepcopy(POLITICA_DEFECTO), "ahora": AHORA_E}

    r0 = dimensionar(SOL, CART, POLITICA_DEFECTO, AHORA_E, paso=1.0)
    h.chk("dimensionar_base_ok_y_limitada_por_F04", r0["ok"] and r0["limitada_por"] == "F-04", r0)
    st = {k: {"lanz": 0, "cant": 0, "forma": 0, "forma_mal": [], "deter": 0, "muta": 0, "det": ""}
          for k in ("sol", "cart", "pol", "ahora")}
    for i in range(CASOS_E):
        nombre = list(st)[i % 4]
        fuentes = entradas_e()
        fuentes[nombre], info = _mutar_en_sitio(fuentes[nombre], rng)
        foto_e = copy.deepcopy(fuentes)
        try:
            r = dimensionar(fuentes["sol"], fuentes["cart"], fuentes["pol"], fuentes["ahora"])
        except Exception as ex:   # noqa: BLE001
            st[nombre]["lanz"] += 1
            st[nombre]["det"] = f"{info['ruta']}: {type(ex).__name__}: {ex}"
            continue
        tocada = next((k for k in fuentes if not _igual_nan(foto_e[k], fuentes[k])), None)
        if tocada:
            st[nombre]["muta"] += 1
            st[nombre]["det"] = f"{info['ruta']}: mutó la entrada {tocada}"
            continue
        q = r.get("cantidad")
        if not (isinstance(q, (int, float)) and not isinstance(q, bool) and q >= 0):
            st[nombre]["cant"] += 1
            st[nombre]["det"] = f"{info['ruta']}: cantidad no finita o negativa: {q!r}"
            continue
        if (not r["ok"]) and q != 0.0:
            st[nombre]["cant"] += 1
            st[nombre]["det"] = f"{info['ruta']}: sin ok con cantidad {q!r}"
            continue
        r2 = dimensionar(copy.deepcopy(fuentes["sol"]), copy.deepcopy(fuentes["cart"]),
                         copy.deepcopy(fuentes["pol"]), fuentes["ahora"])
        if _resumen(r2) != _resumen(r):
            st[nombre]["deter"] += 1
            continue
        if _forma_real(info, fuentes[nombre], None):   # sin esquema JSON: los mínimos no aplican aquí
            st[nombre]["forma"] += 1
            if r["ok"] or r["codigo"] not in ADMITE_E:
                st[nombre]["forma_mal"].append((info["ruta"], info["op"], r["codigo"]))
    h.chk("dimensionar_nunca_lanza_en_500_casos", all(v["lanz"] == 0 for v in st.values()),
          [(k, v["det"]) for k, v in st.items() if v["lanz"]][:3])
    h.chk("r01_dimensionar_no_muta_ninguna_de_sus_cuatro_entradas_en_500_casos",
          all(v["muta"] == 0 for v in st.values()), [(k, v["det"]) for k, v in st.items() if v["muta"]][:3])
    h.chk("dimensionar_cantidad_siempre_finita_no_negativa_y_cero_si_no_ok",
          all(v["cant"] == 0 for v in st.values()), [(k, v["det"]) for k, v in st.items() if v["det"]][:3])
    h.chk("dimensionar_dos_llamadas_dan_lo_mismo_en_500_casos", all(v["deter"] == 0 for v in st.values()),
          [(k, v["deter"]) for k, v in st.items() if v["deter"]][:3])
    h.chk("dimensionar_forma_falla_cerrado_con_E01_a_E04",
          any(v["forma"] > 0 for v in st.values()) and all(not v["forma_mal"] for v in st.values()),
          [(k, v["forma_mal"][:2]) for k, v in st.items() if v["forma_mal"]][:4])

    # ================================================================ vigilancia.vigilar
    from pruebas_vigilancia import T1, abierta, datos as datos_h  # noqa: E402

    o0, b0 = abierta()
    pid = next(iter(o0.posiciones))
    r0 = vigilar(o0, b0, datos_h(1.10), T1)
    h.chk("vigilar_base_sin_novedad_concilia_e_integridad_vacia", r0["acciones"] == [] and r0["conciliacion_ok"]
          and o0.posiciones[pid]["estado"] == "ABIERTA" and o0.integridad() == [], r0)

    st = {"lanz": 0, "cierra_roto": [], "ordenes": [], "integ": [], "muta_datos": 0, "muta_ahora": 0,
          "rotos": 0, "frescos": 0, "det": ""}
    base_datos = datos_h(1.10)
    for i in range(CASOS_H):
        o, b = abierta()   # Orquestador e intermediario de nuevo en cada caso
        dm, info = _mutar_en_sitio(copy.deepcopy(base_datos), rng)
        antes = copy.deepcopy(dm)
        antes_ahora = copy.deepcopy(T1)
        ordenes = list(b.ordenes)
        try:
            vigilar(o, b, dm, T1)
        except Exception as ex:   # noqa: BLE001
            st["lanz"] += 1
            st["det"] = f"{info['ruta']}: {type(ex).__name__}: {ex}"
            continue
        if not _igual_nan(dm, antes):   # llano daría falso positivo con NaN: nan != nan
            st["muta_datos"] += 1
        if not _igual_nan(antes_ahora, T1):   # hoy es una cadena inmutable; la foto queda si el tipo cambia
            st["muta_ahora"] += 1
        if o.integridad() != []:
            st["integ"].append((i, info["ruta"], o.integridad()))
        roto = not _dato_fresco(dm.get("EURUSD") if isinstance(dm, dict) else None, T1, MAX_EDAD_MIN)
        if roto:
            st["rotos"] += 1
            if o.posiciones[pid]["estado"] != "ABIERTA":
                st["cierra_roto"].append((i, info["ruta"], o.posiciones[pid]["estado"]))
            elif list(b.ordenes) != ordenes:
                st["ordenes"].append((i, info["ruta"], "órdenes nuevas"))
        else:
            st["frescos"] += 1
    h.chk("vigilar_nunca_lanza_en_200_casos", st["lanz"] == 0, st["det"])
    h.chk("vigilar_no_muta_los_datos", st["muta_datos"] == 0, st["muta_datos"])
    h.chk("r01_vigilar_no_muta_ahora_en_200_casos", st["muta_ahora"] == 0, st["muta_ahora"])
    h.chk("vigilar_integridad_vacia_tras_cada_caso", not st["integ"], st["integ"][:2])
    h.chk("vigilar_con_datos_rotos_la_posicion_sigue_abierta",
          st["rotos"] >= 50 and not st["cierra_roto"], [(n, r) for n, r, _ in st["cierra_roto"][:2]])
    h.chk("vigilar_con_datos_rotos_el_intermediario_no_recibe_ordenes", not st["ordenes"], st["ordenes"][:2])
    h.chk("vigilar_cubre_casos_rotos_y_frescos", st["rotos"] >= 50 and st["frescos"] >= 1, (st["rotos"], st["frescos"]))

    # ---------------------------------------------------------------- anidado a 500 niveles (casos fijos)
    # La lista de mutaciones de la pieza incluye «anidar un valor 500 niveles ([[[…]]])»; el generador del
    # fin de semana no la trae, así que se fija aquí aparte, un caso por validador: nunca lanza (los
    # envoltorios de los cuatro validadores de mensajes atrapan RecursionError y vigilar captura Exception)
    # y falla cerrado. Cada caso construye SU estructura anidada fresca: deepcopy de una estructura así
    # desbordaría la pila de la propia batería (~3 fotogramas de copia por nivel).
    def _profundo():
        v = 0
        for _ in range(500):
            v = [v]
        return v

    s_an = copy.deepcopy(sobres[0][1])
    s_an["data_refs"][0] = _profundo()
    r_an = validar(s_an, ctx_sobre())
    h.chk("anidado_500_niveles_sobre_no_lanza_y_da_V01", "V-01" in _reglas(r_an), _reglas(r_an))

    m_an = copy.deepcopy(encargos[0][1])
    m_an["data_refs"][0] = _profundo()
    r_an = validar_encargo(m_an, ctx_enc())
    h.chk("anidado_500_niveles_encargo_no_lanza_y_da_E01", "E-01" in _reglas(r_an), _reglas(r_an))

    m_an = informe_ctr(sobre_base())
    m_an["payload"]["cobertura"]["revisadas"][0] = _profundo()
    r_an = validar_informe(m_an, {"ahora": AHORA_CTR, "sobre": copy.deepcopy(sobre_ctr)})
    h.chk("anidado_500_niveles_informe_no_lanza_y_falla_cerrado", r_an != [], _reglas(r_an))

    s_an = copy.deepcopy(sellos[0][1])
    s_an["fuentes"][0]["fuente_id"] = _profundo()
    r_an = validar_sello(s_an, {"calendario": CAL})
    h.chk("anidado_500_niveles_sello_no_lanza_y_da_S01", "S-01" in _reglas(r_an), _reglas(r_an))

    sol_an = copy.deepcopy(SOL)
    sol_an["instrumento"] = _profundo()
    r_an = dimensionar(sol_an, CART, POLITICA_DEFECTO, AHORA_E)
    h.chk("anidado_500_niveles_dimensionar_no_lanza_y_falla_cerrado",
          (not r_an["ok"]) and r_an["codigo"] in ADMITE_E, r_an)

    o_an, b_an = abierta()
    d_an = copy.deepcopy(datos_h(1.10))
    d_an["EURUSD"] = _profundo()
    ordenes_an = list(b_an.ordenes)
    try:
        vigilar(o_an, b_an, d_an, T1)
        sin_lanzar = True
    except Exception as ex:   # noqa: BLE001
        sin_lanzar, r_an = False, f"{type(ex).__name__}: {ex}"
    h.chk("anidado_500_niveles_vigilar_no_lanza_posicion_abierta_y_sin_ordenes",
          sin_lanzar and o_an.posiciones[pid]["estado"] == "ABIERTA"
          and list(b_an.ordenes) == ordenes_an and o_an.integridad() == [],
          r_an if not sin_lanzar else "")

    # ---------------------------------------------------------------- determinismo de la batería entera
    def tirada_e():
        g2, out2 = random.Random(SEMILLA), []
        for i in range(200):
            nombre = ("sol", "cart", "pol", "ahora")[i % 4]
            fuentes = entradas_e()
            fuentes[nombre], _ = _mutar_en_sitio(fuentes[nombre], g2)
            r = dimensionar(fuentes["sol"], fuentes["cart"], fuentes["pol"], fuentes["ahora"])
            out2.append((r["ok"], r["codigo"], r["cantidad"]))
        return out2

    h.chk("bateria_determinista_misma_semilla_mismos_resultados", tirada_e() == tirada_e())

    print(f"\n{h.n} comprobaciones")
    print("RESULTADO ROBUSTEZ VALIDADORES:", "TODAS LAS PRUEBAS PASAN" if h.ok else "HAY FALLOS")
    return 0 if h.ok else 1


if __name__ == "__main__":
    sys.exit(main())
