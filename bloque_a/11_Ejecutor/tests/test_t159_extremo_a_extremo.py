"""T-159 · Fase 4: casos «Superada en parte» del Plan de pruebas V3.0 cuya cláusula pendiente ya la cumple el ejecutor.

Cada prueba cita su PB-xx, siembra la preparación del plan con el cliente simulado (`MockClient`, sin red ni coste) y sigue
sus pasos de extremo a extremo con `Bloque.ciclo` o con el ciclo C6 de seguimiento. La siembra cambia solo lo que el plan
prepara (lo que devuelve un agente simulado o la serie de un proveedor); el código del ejecutor no se toca.
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from bloque_a.evaluador import contaminacion_posible
from bloque_a.herramientas import ht03, ht07
from bloque_a.herramientas.ht01_datos import ProveedorCSV
from bloque_a.llm import MockClient
from bloque_a.motor import servicio
from bloque_a.orquestacion import Bloque
from conftest import AS_OF, DATOS, config_pruebas, nuevo_bloque

from bloque_a import mock_respuestas
from bloque_a import sintesis as sint


def _todas(nombre: str, valor: int) -> dict:
    return {k: valor for k in ht03.PARAMETROS_POR_DEFECTO["pesos"][nombre]}


def _g3v(b, run_id: str, fase: str = "F6") -> list[dict]:
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V" and e["run_id"] == run_id and e.get("fase") == fase]


def _resultado(g3v: dict, cid: str) -> str:
    return next(c["resultado"] for c in g3v["comprobaciones"] if c["id"] == cid)


def _entregado(r) -> dict:
    return json.loads(Path(r["entregables"]["paquete_json"]).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- PB-02 · top-3 con menos de tres elegibles
# Segunda pasada de E de la candidata marginal: media exacta 57,5 (la «E = 58» del plan), que HT-03 redondea a 55; las
# dimensiones van de 10 en 10, como exige HT-03
SEGUNDA_E_MARGINAL = {**{k: 60 for k in ht03.PARAMETROS_POR_DEFECTO["pesos"]["E"]}, "calidad_raices": 50}


def test_pb02_dos_opciones_y_la_de_banda_marginal_fuera_con_su_segunda_pasada(tmp_path, universo, monkeypatch):
    """PB-02. Preparación del plan: en DIV solo dos candidatas superan E y A; una tercera queda en la banda marginal de E
    (primera pasada en el umbral, segunda con media 57,5) y el resto, lejos. Criterio: exactamente dos opciones, G3-CON-03
    (C03 de HT-09: menos de tres con su motivo) PASA y ninguna opción entregada incumple un umbral."""
    original = mock_respuestas._ficha
    papeles: dict[str, str] = {}

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        if msg["clase"] != "DIV":
            return f
        papel = papeles.setdefault(u["simbolo"], ("BUENA", "BUENA", "MARGINAL")[len(papeles)] if len(papeles) < 3 else "BAJA")
        e = {"BUENA": 80, "MARGINAL": 60, "BAJA": 30}[papel]
        f["dimensiones"] = {**f["dimensiones"], "T": _todas("T", 70), "E": _todas("E", e), "A": _todas("A", 80)}
        f["segunda_pasada"] = {"T": _todas("T", 70), "E": SEGUNDA_E_MARGINAL if papel == "MARGINAL" else _todas("E", e), "A": _todas("A", 80)}
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    assert r["g3"]["dictamen"] == "APTO" and r["g3_entregables"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS") and r["entregables"]
    assert list(papeles.values())[:3] == ["BUENA", "BUENA", "MARGINAL"] and len(papeles) >= 4      # siete candidatas en el plan
    div = _entregado(r)["clases"]["DIV"]
    buenas = {s for s, p in papeles.items() if p == "BUENA"}
    marginal = next(s for s, p in papeles.items() if p == "MARGINAL")
    assert len(div["opciones"]) == 2                                                    # exactamente dos opciones
    assert {o["indicador_seguimiento"]["simbolo"] for o in div["opciones"]} == buenas
    assert marginal not in json.dumps(div["opciones"])                                  # la de la banda marginal no aparece
    # Su segunda pasada está registrada en F3 y es la que decide (E por debajo del umbral)
    f3 = {e["simbolo_seguimiento"]: e for e in b.almacen.estado("F3").values() if e.get("clase") == "DIV" and e.get("simbolo_seguimiento")}
    umbrales = b.params_ht03["umbrales"]
    assert f3[marginal]["segunda_pasada"]["E"] == SEGUNDA_E_MARGINAL and not f3[marginal]["elegible"]
    assert f3[marginal]["puntuaciones_totales"]["E"] < umbrales["E"]
    # El motivo de «menos de tres»: candidatas analizadas, por qué cayó cada una y qué tendría que ocurrir
    motivo = div["menos_de_tres_motivo"]
    assert f"de {div['candidatas_analizadas']} candidatas analizadas" in motivo and f3[marginal]["opp_id"] in motivo and "→" in motivo
    # G3-CON-03 (C03) PASA en la validación del paquete y en la de los entregables
    assert [_resultado(g, "C03") for g in _g3v(b, r["run_id"])] == ["OK"]
    assert _resultado(_g3v(b, r["run_id"], "F7")[0], "C03") == "OK"
    # Ninguna opción entregada con un umbral incumplido
    for o in div["opciones"]:
        pu = o["puntuaciones"]
        assert pu["E"] >= umbrales["E"] and pu["A"] >= umbrales["A"] and pu["T"] >= umbrales["T"]


# ---------------------------------------------------------------- PB-03 · clase sin ninguna opción elegible
def test_pb03_alt_sin_vehiculo_minorista_queda_sin_opciones_y_en_gris(tmp_path, universo, monkeypatch):
    """PB-03. Preparación del plan: las candidatas de ALT no superan PS3 (sin universo invertible para un minorista).
    Criterio: cero opciones ALT; semáforo GRIS, ninguna tarjeta de ALT en el visual y el motivo por candidata en el técnico.
    Que el Auditor no registre hallazgo por ello lo juzga el modelo real."""
    original = mock_respuestas._ficha
    alt: list[str] = []

    def ficha(u, msg, ctx, rng, inyectado):
        f = original(u, msg, ctx, rng, inyectado)
        if msg["clase"] == "ALT":
            f["invertibilidad"] = {"universo_suficiente": False, "nota": "Sin vehículo accesible para un inversor minorista europeo."}
            alt.append(u["simbolo"])
        return f
    monkeypatch.setattr(mock_respuestas, "_ficha", ficha)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["ALT", "RF"]})
    assert alt and r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS") and r["entregables"]
    entregado = _entregado(r)["clases"]
    assert entregado["ALT"]["opciones"] == [] and entregado["ALT"]["estado_semaforo"] == "GRIS"
    assert entregado["RF"]["opciones"]                                                  # el resto del ciclo sigue
    # Cada candidata de ALT cae por PS3 y queda en F3 con su motivo
    f3 = [e for e in b.almacen.estado("F3").values() if e.get("clase") == "ALT" and e.get("simbolo_seguimiento") in alt]
    assert {e["simbolo_seguimiento"] for e in f3} == set(alt)
    for e in f3:
        assert not e["elegible"] and e["puertas"]["PS3"] is False and any("PS3" in m for m in e["motivos_no_elegible"])
    # El técnico detalla el motivo por candidata; el visual no pinta tarjetas de ALT y lo explica en lenguaje llano
    motivo = entregado["ALT"]["menos_de_tres_motivo"]
    assert all(e["opp_id"] in motivo for e in f3) and "PS3" in motivo
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    assert motivo in tecnico
    visual = Path(r["entregables"]["informe_visual"]).read_text(encoding="utf-8")
    assert not any(e["opp_id"] in visual for e in f3)
    assert re.search(r"Miramos \d+ ideas\. Solo 0 pasaron todos los filtros", visual)   # explicación llana del Redactor


# ---------------------------------------------------------------- PB-30 · cifra sin artefacto bloqueada por G3
def test_pb30_la_cifra_sin_artefacto_bloquea_se_retira_y_lo_entregado_no_la_lleva(tmp_path, universo, monkeypatch):
    """PB-30. Preparación del plan: el paquete de síntesis lleva una rentabilidad esperada que cita un CALC- sin artefacto
    en el Registro de cálculos. Pasos: HT-09, CT-14 al Orquestador, corrección y relanzamiento. Criterio: dos G3V- en HA y la
    cifra no aparece en la entrega (o aparece con su CALC-). El tiempo de dictamen (≤ 10 min) es de tiempo real."""
    construir = sint.construir
    sembrada: dict = {}

    def con_cifra_sin_calc(*args, **kwargs):
        paquete, extras = construir(*args, **kwargs)
        op = paquete["clases"]["RV"]["opciones"][0]
        op["valoracion"] = f"{op['valoracion']} Rentabilidad esperada del 12,4 % a doce meses (CALC-2026-9999)."
        op["calculos"] = [*op["calculos"], "CALC-2026-9999"]
        sembrada.update(opp_id=op["opp_id"])
        return paquete, extras
    monkeypatch.setattr(sint, "construir", con_cifra_sin_calc)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert "CALC-2026-9999" not in {e.get("calc_id") for e in b.almacen.leer("RC")}
    g3v = _g3v(b, r["run_id"])
    assert len(g3v) == 2                                                                # dos G3V- en HA
    assert g3v[0]["dictamen_efectivo"] == "BLOQUEADO" and _resultado(g3v[0], "C08") == "BLOQUEO"
    c08 = next(c for c in g3v[0]["comprobaciones"] if c["id"] == "C08")
    assert any("CALC-2026-9999 sin artefacto" in d for d in c08["detalle"])
    assert g3v[0]["excepcion"]["dictamen_orquestador"] == "BLOQUEADO"                    # el Orquestador no lo da por bueno
    ct14 = [m for m in b.mensajeria.registro if m["contrato"] == "CT-14"]
    assert ct14 and ct14[0]["emisor"] == "AG-02" and ct14[0]["receptor"] == "AG-18"
    assert g3v[1]["dictamen_efectivo"] == "APTO" and _resultado(g3v[1], "C08") == "OK"   # tras retirar la cifra, APTO
    assert r["g3"]["dictamen"] == "APTO" and r["entregables"]
    # La cifra no llega a ningún entregable; lo que se entrega cita solo cálculos con artefacto
    for ruta in r["entregables"].values():
        texto = Path(ruta).read_text(encoding="utf-8")
        assert "CALC-2026-9999" not in texto and "12,4 %" not in texto
        sin_avisos = re.sub(r"retiradas por (?:bloqueo|el control) G3: [^.\n\"<]*", "", texto)   # solo se nombra al declararla (T-165 r03: «el control G3»)
        assert sembrada["opp_id"] not in sin_avisos
    entregado = _entregado(r)
    servidos = {e["calc_id"] for e in b.almacen.leer("RC") if e.get("estado") in ("SERVED", "SERVED_WITH_LIMITATIONS")}
    citados = {c for clase in entregado["clases"].values() for o in clase["opciones"] for c in o["calculos"]}
    assert citados and citados <= servidos
    assert sembrada["opp_id"] not in {o["opp_id"] for o in entregado["clases"]["RV"]["opciones"]}
    assert any(sembrada["opp_id"] in x for x in entregado["limitaciones"])            # la retirada se declara


# ---------------------------------------------------------------- PB-39 · informe visual con legibilidad < 70
_JERGA = ("La convexidad implícita de la estructura temporal de volatilidades, condicionada por la heterocedasticidad "
          "autorregresiva generalizada y por la asimetría de la distribución de rendimientos esperados, sugiere una "
          "reasignación táctica de la duración modificada ponderada por la sensibilidad diferencial de los diferenciales "
          "crediticios subordinados frente a la curva soberana interpolada.")


def _redactor_con_jerga(original, siempre: bool):
    def redactor(msg, ctx, rng):
        out = original(msg, ctx, rng)
        if siempre or not msg.get("reescritura"):
            out["frases_30s"] = [_JERGA, _JERGA, _JERGA]
            for t in out["tarjetas"]:
                t.update(por_que_llano=_JERGA[:160], que_puede_salir_mal_llano=_JERGA[:200])
            out["frase_historial"] = _JERGA
        return out
    return redactor


def _visuales(b, run_id):
    return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V" and e["run_id"] == run_id and e.get("fase") == "F7"]


def test_pb39_el_visual_por_debajo_de_70_se_bloquea_y_tras_la_reescritura_se_entrega(tmp_path, universo, monkeypatch):
    """PB-39. Preparación del plan: el Redactor usa frases largas y jerga. Pasos: HT-07, HT-09 (C12, G3-ENT-01) y reescritura.
    Criterio: ningún informe visual entregado con índice < 70."""
    monkeypatch.setattr(mock_respuestas, "_redactor", _redactor_con_jerga(mock_respuestas._redactor, siempre=False))
    cliente = MockClient()
    b = nuevo_bloque(tmp_path, universo, cliente=cliente)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    umbral = config_pruebas()["redaccion"]["umbral_fh"]
    f7 = _visuales(b, r["run_id"])
    assert len(f7) == 2 and [x["agente"] for x in cliente.llamadas].count("AG-17") == 2   # bloqueo y una reescritura
    primero, segundo = f7
    assert primero["dictamen_efectivo"] == "BLOQUEADO" and _resultado(primero, "C12") == "BLOQUEO"
    assert primero["legibilidad"]["fernandez_huerta"] < umbral
    assert segundo["dictamen_efectivo"] != "BLOQUEADO" and segundo["legibilidad"]["fernandez_huerta"] >= umbral
    assert r.get("entrega") != "BLOQUEADA" and r["entregables"]
    visual = Path(r["entregables"]["informe_visual"]).read_text(encoding="utf-8")
    assert _JERGA[:60] not in visual and ht07.analizar(visual, es_html=True)["fernandez_huerta"] >= umbral


def test_pb39_si_la_reescritura_sigue_por_debajo_de_70_no_se_entrega_ningun_visual(tmp_path, universo, monkeypatch):
    monkeypatch.setattr(mock_respuestas, "_redactor", _redactor_con_jerga(mock_respuestas._redactor, siempre=True))
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    umbral = config_pruebas()["redaccion"]["umbral_fh"]
    f7 = _visuales(b, r["run_id"])
    assert len(f7) == 2 and all(x["dictamen_efectivo"] == "BLOQUEADO" and x["legibilidad"]["fernandez_huerta"] < umbral for x in f7)
    assert r["entrega"] == "BLOQUEADA" and r["estado"] == "PARCIAL"
    entregados = [p for p in (tmp_path / "ent").rglob("*informe-visual*") if "_borradores" not in p.parts and "bloque" not in str(p).lower()]
    assert entregados == []                                                             # ningún visual con < 70 en la entrega
    assert not [e for e in b.almacen.leer("F4") if e.get("run_id") == r["run_id"]]     # y nada se congela


# ---------------------------------------------------------------- PB-41 · coherencia entre entregables y entre clases
class ProveedorFactorComun(ProveedorCSV):
    """Las series de RF, INM y RV comparten un factor común (el «factor tipos» del plan): a cada cierre se le suma, en
    logaritmos, la misma marcha aleatoria reproducible, con más volatilidad que la propia de cada serie."""

    def __init__(self, base, simbolos: set[str]) -> None:
        super().__init__(base)
        self.con_factor = set(simbolos)

    def _serie_completa(self, simbolo):
        df = super()._serie_completa(simbolo)
        if simbolo not in self.con_factor:
            return df
        dias = pd.DatetimeIndex(df.index)
        choques = np.array([np.random.default_rng(d.toordinal()).normal(0.0, 0.03) for d in dias])
        df = df.copy()
        df["cierre"] = df["cierre"].astype(float) * np.exp(np.cumsum(choques))
        return df


def test_pb41_el_factor_comun_de_rf_reit_y_rv_queda_en_un_cluster_y_los_tres_entregables_coinciden(tmp_path, universo):
    """PB-41. Preparación del plan: top-3 con RF, inmobiliario cotizado (REIT) y RV expuestos al mismo factor. Criterio:
    G3-ENT-07 PASA (mismas OPP-, en el mismo orden, en el JSON, el técnico y el visual); el clúster común se declara y
    `apuestas_independientes` lo refleja. Que el Auditor no recuente menos apuestas lo juzga el modelo real."""
    clases = ["RF", "INM", "RV"]
    simbolos = set(universo[universo["clase"].isin(clases)]["simbolo"])
    b = Bloque(config_pruebas(), ProveedorFactorComun(DATOS, simbolos), universo, MockClient(),
               tmp_path / "estado", tmp_path / "ent")
    r = b.ciclo(AS_OF, alcance={"clases": clases})
    assert r["g3"]["dictamen"] in ("APTO", "APTO_CON_ADVERTENCIAS") and r["entregables"]
    js = _entregado(r)
    opciones = {o["opp_id"]: c for c in clases for o in js["clases"][c]["opciones"]}
    assert {c for c in opciones.values()} == set(clases)
    # El clúster común reúne opciones de los tres tipos y las apuestas independientes son los clústeres, no las opciones
    comun = [e for e in js["clusteres_exposicion"] if {opciones[o] for o in e["opp_ids"]} == set(clases)]
    assert comun and comun[0]["factor_dominante"]
    assert js["apuestas_independientes"] == len(js["clusteres_exposicion"]) < len(opciones)
    assert sorted(o for e in js["clusteres_exposicion"] for o in e["opp_ids"]) == sorted(opciones)
    # G3-ENT-07: los tres entregables, mismas OPP- y mismo orden; la validación de los entregables no ve incoherencias
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    visual = Path(r["entregables"]["informe_visual"]).read_text(encoding="utf-8")
    orden_json = [o["opp_id"] for c in js["clases"] for o in js["clases"][c]["opciones"]]

    def orden_en(texto):
        return sorted(opciones, key=texto.index)
    assert all(o in tecnico and o in visual for o in opciones)
    assert orden_en(tecnico) == orden_en(visual) == sorted(opciones, key=orden_json.index)
    f7 = _visuales(b, r["run_id"])[-1]
    assert f7["incoherencias"] == [] and f7["dictamen_efectivo"] != "BLOQUEADO" and _resultado(f7, "C14") != "BLOQUEO"
    assert str(js["apuestas_independientes"]) in tecnico and comun[0]["cluster_id"] in tecnico


# ---------------------------------------------------------------- PB-47 · estados de madurez
def test_pb47_un_metodo_documentado_no_se_usa_y_la_entrega_lo_declara(tmp_path, universo, monkeypatch):
    """PB-47. Preparación del plan: un método que el ciclo usa (ML-CLUS-001, los clústeres de exposición) figura como
    DOCUMENTADO en el Catálogo. Criterio: el entregable final no usa el método (o lo declara «documentado»); nada se
    presenta como validado."""
    original = servicio.madurez_catalogo

    def con_documentado(raiz=None):
        return {**original(raiz), "ML-CLUS-001": "DOCUMENTADO"}
    monkeypatch.setattr(servicio, "madurez_catalogo", con_documentado)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
    rc = b.almacen.leer("RC")
    clus = [e for e in rc if (e.get("operacion") or {}).get("ficha_id") == "ML-CLUS-001"]
    assert clus and all(e["estado"] == "REJECTED" and e["motivo_rechazo"] == "METODO_NO_IMPLEMENTADO"
                    and e["madurez_metodo"] == "DOCUMENTADO" and not e.get("resultado") for e in clus)
    assert r["entregables"] and r.get("entrega") != "BLOQUEADA"
    js = _entregado(r)
    servidos = {e["calc_id"]: e for e in rc if e.get("estado") in ("SERVED", "SERVED_WITH_LIMITATIONS")}
    citados = {c for clase in js["clases"].values() for o in clase["opciones"] for c in o["calculos"]}
    assert citados and citados <= set(servidos)                                         # solo cifras de métodos servidos
    assert all(servidos[c]["operacion"]["ficha_id"] != "ML-CLUS-001" for c in citados)  # el método documentado no se usa
    assert any("clústeres de exposición no calculados" in x for x in js["limitaciones"])   # y la entrega lo declara
    for ruta in r["entregables"].values():
        texto = Path(ruta).read_text(encoding="utf-8").lower()
        assert "clústeres de exposición no calculados" in texto or ruta.endswith(".html")
        assert "validado" not in texto                                                 # nada se presenta como validado


# ---------------------------------------------------------------- PB-52 · herramienta caída (lo que sí cumple)
def test_pb52_con_ht09_caido_nunca_hay_apto_por_defecto_ni_entrega(tmp_path, universo, monkeypatch):
    """La caída en F6 deja un bloqueo manual en HA, sin dictamen favorable, entrega ni pronóstico."""

    def caido(*args, **kwargs):
        raise sint.ht09.HerramientaNoDisponible("HT-09 no disponible")
    control = sint.control_con_respaldo
    def observar(*args, **kwargs):
        decision = control(*args, **kwargs)
        assert decision["dictamen"] == "BLOQUEADO"
        return decision

    monkeypatch.setattr(sint, "ht09_validar", caido)
    monkeypatch.setattr(sint, "control_con_respaldo", observar)
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["entrega"] == "BLOQUEADA" and r["g3"]["modo"] == "G3_MANUAL"
    assert not [p for p in (tmp_path / "ent").rglob("*") if p.is_file()]
    assert not [e for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "ALTA"]
    g3v = [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "G3V"]
    assert not any(str(e.get("dictamen_efectivo")).startswith("APTO") for e in g3v)
    assert any(e.get("tipo_control") == "G3_MANUAL" and e["dictamen_efectivo"] == "BLOQUEADO" for e in g3v)


# ---------------------------------------------------------------- PB-67 · el seguimiento propone el envío al Bloque B
def test_pb67_el_ciclo_c6_propone_el_envio_a_b_sin_enviar_nada(tmp_path, universo):
    """PB-67. Preparación del plan: la OPP- vigilada vuelve a superar los umbrales sin objeciones fuertes abiertas y con
    novedad (su catalizador ocurre). Criterio: HT-09 (perfil SEGUIMIENTO) APTO y ningún envío automático."""
    b = nuevo_bloque(tmp_path, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    opp = r["paquete"]["clases"]["RV"]["opciones"][0]["opp_id"]
    alta = b.seguimientos.procesar({"accion": "ALTA", "opp_id": opp, "frecuencia": "SEMANAL", "motivo": "Vigilar"}, AS_OF)
    propuesta = None
    for k in range(1, 13):
        fecha = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7 * k)).date())
        n_msg = len(b.mensajeria.registro)
        res = b.seguimientos.ejecutar(fecha)
        assert len(res) == 1 and res[0]["ejecutado"]
        if res[0]["recomendacion"] == "PROPONER_ENVIO_A_B":
            propuesta, nuevos = res[0], b.mensajeria.registro[n_msg:]
            break
    assert propuesta, "el catalizador de la opción ocurre dentro de las doce semanas"
    inf = propuesta["informe"]
    assert propuesta["g3"] == "APTO" and propuesta["validacion"]["dictamen"] == "APTO" and propuesta["entregado"]
    assert inf["puntuaciones"]["elegible"] and inf["objeciones_fuertes_abiertas"] == [] and not inf["sin_novedad"]
    pb = inf["paquete_para_bloque_B"]
    assert pb["opp_id"] == opp and pb["tesis"] and pb["pronosticos"] and pb["indicador_seguimiento"]
    assert isinstance(inf["sugerir_profundizacion_N3"], bool)
    # Sin envío automático: solo el CT-24 al Broker con la recomendación; la decisión queda en el Broker
    externos = [m for m in nuevos if not str(m["receptor"]).startswith("AG-")]
    assert [(m["contrato"], m["receptor"]) for m in externos] == [("CT-24", "BROKER")]
    assert not [m for m in b.mensajeria.registro if "B-" in str(m["contrato"]) or "BLOQUE_B" in str(m["receptor"]).upper()]
    f3 = b.almacen.estado("F3")[opp]
    assert f3["decision_broker"]["decision"] == "EN_SEGUIMIENTO" and f3["seg_id"] == alta["seg_id"]   # ni ENVIADA ni otra
    assert f3["estado"] == b.almacen.estado("F3", AS_OF)[opp]["estado"]                # el C6 no cambia el estado de la opción


# ---------------------------------------------------------------- PB-44 · historial de aciertos honesto
class ProveedorConCorte(ProveedorCSV):
    """Un símbolo deja de publicar datos desde una fecha: su pronóstico no se puede resolver y acaba NO_RESOLUBLE."""

    def __init__(self, base) -> None:
        super().__init__(base)
        self.cortes: dict[str, pd.Timestamp] = {}

    def _serie_completa(self, simbolo):
        df = super()._serie_completa(simbolo)
        return df[df.index <= self.cortes[simbolo]] if simbolo in self.cortes else df


def test_pb44_el_historial_publicado_es_el_recuento_de_f4_con_su_muestra_y_el_mismo_dato_en_los_informes(tmp_path, universo):
    """PB-44. Preparación del plan (a escala de los datos sintéticos): semanas de ciclos con opciones de horizonte vencido,
    una cerrada por invalidación, una descartada por el Broker y una cuyo PRG queda NO_RESOLUBLE. Criterio: recuento
    verificado contra F4 y F3; `significativo` false con n < 30 y su nota; mismo dato en el técnico y en el visual («Cómo nos
    fue»); G3-CON-18 (historial con su tamaño muestral) PASA."""
    prov = ProveedorConCorte(DATOS)
    b = Bloque(config_pruebas(), prov, universo, MockClient(), tmp_path / "estado", tmp_path / "ent")
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    invalidada, descartada, sin_datos = r["paquete"]["clases"]["RV"]["opciones"][:3]
    sym = invalidada["indicador_seguimiento"]["simbolo"]
    b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": invalidada["opp_id"],          # como en PB-14
                                       "invalidacion_cuantitativa": [{"simbolo": sym, "umbral": b.proveedor.valor_en(sym, AS_OF)[1] * 2,
                                                                      "direccion": "por_debajo"}]})
    b.decision({"decisiones": [{"opp_id": descartada["opp_id"], "decision": "DESCARTADA", "motivo": "no encaja"}]}, AS_OF)
    prov.cortes[sin_datos["indicador_seguimiento"]["simbolo"]] = pd.Timestamp(AS_OF)
    for k in range(1, 9):
        r = b.ciclo(str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7 * k)).date()), alcance={"clases": ["RV"]})
    as_of = r["as_of"]
    assert b.almacen.estado("F3")[invalidada["opp_id"]]["cierre"]["motivo"] == "INVALIDACION"
    assert b.almacen.estado("F3")[descartada["opp_id"]]["decision_broker"]["decision"] == "DESCARTADA"
    hist = r["paquete"]["historial_aciertos"]
    g = hist["global"]
    # Recuento contra F4: PRG del informe resueltos en la ventana, sin fuga, sin hitos ni contaminados
    f4, f3 = b.almacen.estado("F4", as_of), b.almacen.estado("F3", as_of)
    desde = pd.Timestamp(as_of) - pd.Timedelta(weeks=int(hist["ventana"].split()[0]))
    cuentan = [p for p in f4.values() if p.get("estado") == "RESUELTO" and p.get("en_informe") and not p.get("es_hito")
               and p["resolucion"]["comprobacion_fuga"] == "SUPERADA" and not contaminacion_posible(p)
               and pd.Timestamp(p["resolucion"]["fecha_resuelto"]) >= desde]
    assert cuentan and g["n"] == len(cuentan) and g["aciertos"] == sum(int(p["resolucion"]["resultado_binario"]) for p in cuentan)
    assert all(p["opp_id"] in f3 for p in cuentan)                                      # y contra F3: opciones registradas
    por_opp = {p["opp_id"] for p in cuentan}
    assert {invalidada["opp_id"], descartada["opp_id"]} <= por_opp                      # el universo completo, no solo las vigentes
    no_res = [p for p in f4.values() if p.get("estado") == "NO_RESOLUBLE" and p.get("en_informe") and not p.get("es_hito")]
    assert no_res and {p["opp_id"] for p in no_res} == {sin_datos["opp_id"]} and sin_datos["opp_id"] not in por_opp
    assert f"{len(no_res)} no resolubles excluidos y declarados" in hist["nota"]
    # Muestra pequeña: no significativo y con su nota
    assert g["n"] < 30 and g["significativo"] is False and "muestra pequeña" in hist["nota"]
    # El mismo dato en el JSON, el técnico y el visual
    js = _entregado(r)
    assert js["historial_aciertos"]["global"] == g
    tecnico = Path(r["entregables"]["informe_tecnico"]).read_text(encoding="utf-8")
    assert f"| Global | {g['n']} | {g['aciertos']} |" in tecnico and hist["nota"] in tecnico
    visual = Path(r["entregables"]["informe_visual"]).read_text(encoding="utf-8")
    assert "Cómo nos fue" in visual and f"<b>{g['aciertos']} de cada {g['n']}</b>" in visual
    # G3-CON-18: el historial y su tamaño muestral están en el paquete validado (C01 de HT-09 en OK)
    assert all(_resultado(x, "C01") == "OK" for x in _g3v(b, r["run_id"]) + _g3v(b, r["run_id"], "F7"))
