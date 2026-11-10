"""T-53 · Revisión del Bloque A (9-11-2026): regresiones de selección, validación, entrega, pausas y datos.

Cada prueba falla con el código anterior a la corrección y pasa con ella (ver `.docs/tickets/T-53/pruebas.md`).
"""
import json
import shutil
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.configuracion import (
    CLASES,
    DIR_EJECUTOR,
    RUTA_UNIVERSO_EJEMPLO,
    aplicabilidad,
    cargar_config,
)
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.herramientas.referencia import ht03_puntuaciones as ht03
from bloque_a.herramientas.referencia import ht09_validador_g3 as ht09
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque

from bloque_a import mock_respuestas as mr
from bloque_a import redaccion, sintesis

DATOS = DIR_EJECUTOR / "ejemplos" / "datos_sinteticos"
AS_OF = "2026-06-05"


def _bloque(tmp_path, modo="backtest", datos=DATOS, universo=RUTA_UNIVERSO_EJEMPLO):
    return Bloque(cargar_config(extra={"modo": modo, "perfiles": {"activos": list(CLASES)}}), ProveedorCSV(datos), cargar_universo(universo), MockClient(),
                  tmp_path / "estado", tmp_path / "entregables")


def _ev(oid, rk, vigente=False, cluster=None):
    return {"opp_id": oid, "vigente": vigente, "elegible": True, "cluster": cluster, "riesgo_cola": 1,
            "puntuaciones": {"RK": rk, "E": 70}, "motivos_no_elegible": []}


# ---------------------------------------------------------------- CA-01 · continuidad (9.6.4 y 9.6.5)
def test_vigente_sin_proteccion_ocupa_un_puesto_libre():
    r = ht03.seleccionar_top3([_ev("N1", 85), _ev("N2", 62), _ev("V1", 70, vigente=True)], ht03.PARAMETROS_POR_DEFECTO)
    assert [t["opp_id"] for t in r["top3"]] == ["N1", "V1", "N2"]
    assert r["menos_de_tres_motivo"] is None and not [d for d in r["decisiones"] if d["decision"] == "SUSTITUIDA"]


def test_vigente_sin_proteccion_se_sustituye_si_tres_mejores_ocupan_los_puestos():
    r = ht03.seleccionar_top3([_ev("N1", 85), _ev("N2", 80), _ev("N3", 78), _ev("V1", 70, vigente=True)],
                              ht03.PARAMETROS_POR_DEFECTO)
    assert [t["opp_id"] for t in r["top3"]] == ["N1", "N2", "N3"]
    assert [d["decision"] for d in r["decisiones"] if d["opp_id"] == "V1"] == ["SUSTITUIDA"]


# ---------------------------------------------------------------- CA-11 · hitos H5 distintos (8.3)
def test_h5_tres_copias_del_mismo_hito_bloquea():
    hito = {"hit_id": "HIT-2026-0001", "fecha": "2027-06-01", "indicador": "X", "criterio": "Y"}
    R = ht09.Registro()
    ht09._validar_h5(R, "op.H5", {"prob": None, "banda": "muy probable", "hitos": [dict(hito) for _ in range(3)]}, "2026-06-05")
    detalles = " ".join(str(x) for x in vars(R).values())
    assert "repetidos" in detalles and "distintas" in detalles


def test_h5_tres_hitos_distintos_no_bloquea_por_repeticion():
    hitos = [{"hit_id": f"HIT-2026-000{i}", "fecha": f"{2027 + i}-06-01", "indicador": "X", "criterio": "Y"} for i in range(3)]
    R = ht09.Registro()
    ht09._validar_h5(R, "op.H5", {"prob": None, "banda": "muy probable", "hitos": hitos}, "2026-06-05")
    detalles = " ".join(str(x) for x in vars(R).values())
    assert "repetidos" not in detalles and "distintas" not in detalles


# ---------------------------------------------------------------- CA-03 · lo bloqueado no se entrega (7.3 G3)
def test_entregable_bloqueado_no_llega_a_las_carpetas_de_entrega(tmp_path, monkeypatch):
    monkeypatch.setattr(redaccion, "coherencia", lambda rutas, js: ["incoherencia simulada entre entregables"])
    b = _bloque(tmp_path, modo="vivo")
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["g3_entregables"]["dictamen"] == "BLOQUEADO"
    ent = tmp_path / "entregables"
    for carpeta in ("Informes técnicos Broker", "Informes visuales Usuario", "Paquetes JSON"):
        assert not (ent / carpeta).exists() or not list((ent / carpeta).glob("*"))
    bloqueados = list((ent / "_bloqueados").rglob("*.json"))
    assert bloqueados and "estado_g3" not in json.loads(bloqueados[0].read_text(encoding="utf-8"))


def test_entregable_apto_llega_a_su_carpeta_y_cita_las_rutas_de_entrega(tmp_path):
    b = _bloque(tmp_path, modo="vivo")
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    assert r["g3_entregables"]["dictamen"] != "BLOQUEADO"
    ent = tmp_path / "entregables"
    js = list((ent / "Paquetes JSON").glob("*.json"))
    md = list((ent / "Informes técnicos Broker").glob("*.md"))
    assert js and md and not (ent / "_borradores").exists()
    assert "_borradores" not in md[0].read_text(encoding="utf-8")


# ---------------------------------------------------------------- CA-04 · consulta BLOQUEANTE (7.9, R26)
PREGUNTA = [{"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No", "efecto_si_falso": "cambia el ámbito"}]


def test_bloqueante_sobre_todo_el_alcance_pausa_y_deja_el_run_parcial(tmp_path):
    b = _bloque(tmp_path)
    b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": "BLOQUEANTE", "clases": ["CRI"], "preguntas": PREGUNTA}, AS_OF)
    r = b.ciclo(AS_OF, alcance={"clases": ["CRI"]})
    assert "CRI" not in r["paquete"]["clases"] and r["estado"] == "PARCIAL"
    assert any("pausado" in x for x in r["paquete"]["limitaciones"])


def test_bloqueante_sin_tipos_pausa_todo_el_alcance(tmp_path):
    b = _bloque(tmp_path)
    b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": "BLOQUEANTE", "clases": [], "preguntas": PREGUNTA}, AS_OF)
    assert set(b.consultas.clases_pausadas(AS_OF, ["RV", "RF"])) == {"RV", "RF"}


# ---------------------------------------------------------------- CA-05 · PS1 corrobora las afirmaciones del Analista (9.3)
def test_ps1_no_se_supera_solo_con_la_pieza_automatica_de_momentum(tmp_path):
    b = _bloque(tmp_path)
    b.fijar_fecha(AS_OF)
    f = {"proxy": "SPY", "tesis": "Corrección bajista", "_piezas": [
        {"afirmacion": "Momentum 12-1 de SPY: +12.00% (percentil 80% de la clase) a 2026-06-05", "fuente": "HT-01:SPY",
         "direccion": "favorable", "extracto": "serie de cierres HT-01", "origen": "AG-13", "tipo_afirmacion": "DATO"}]}
    an = {"clase": "RV", "nivel": "N1", "finalistas": [f], "peticiones": [], "hallazgos_r9": []}
    b._registrar_evidencia_clase(an, pd.Timestamp(AS_OF), "RUN-2026-0001")
    assert f["_ps1"] is False and f["_raices"] == {}


# ---------------------------------------------------------------- CA-06 · símbolo sin historia (R14, R16, PS2)
def test_un_simbolo_sin_historia_no_vacia_su_tipo(tmp_path):
    datos = tmp_path / "datos"
    shutil.copytree(DATOS, datos)
    fechas = pd.bdate_range("2026-09-01", "2026-10-30")      # empieza a cotizar después de as_of
    (datos / "USDNEW=X.csv").write_text("fecha,cierre\n" + "\n".join(f"{d.date()},1.0{i % 9}" for i, d in enumerate(fechas)) + "\n")
    uni = Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + \
        "\nUSDNEW=X,DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/NEW,\n"
    (tmp_path / "u.csv").write_text(uni, encoding="utf-8")
    b = _bloque(tmp_path, datos=datos, universo=tmp_path / "u.csv")
    r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    assert r["paquete"]["clases"]["DIV"]["opciones"]          # antes: 0 opciones y estado COMPLETO, sin laguna
    assert r["estado"] == "PARCIAL"
    assert b._sin_historia[("DIV", r["run_id"])] == ["USDNEW=X"]


# ---------------------------------------------------------------- CA-14 · PS2 en H1 (Anexo A: 1 día)
@pytest.mark.parametrize("as_of, dato, esperado", [
    ("2026-06-08", "2026-06-05", True),     # lunes con dato del viernes: una sesión
    ("2026-06-10", "2026-06-07", False),    # miércoles con dato del domingo: más de una sesión
])
def test_ps2_h1_cuenta_sesiones_habiles(tmp_path, as_of, dato, esperado):
    b = _bloque(tmp_path)
    puertas = b._puertas({"senales": {"fecha_dato": dato}}, "N1", as_of, ["H1"])
    assert puertas["PS2"] is esperado


# ---------------------------------------------------------------- CS-17 · semáforo y siguiente paso (prompt AG-02, 6.15-6.16)
UMB = {"E_enviar": 70, "A_profundizar": 65}


def _op(E, A, rel="MEDIA", cat="2026-07-01", fin="2026-12-01", moderada=False):
    return {"puntuaciones": {"E": E, "A": A, "RK": 80}, "relevancia_decisional": rel, "horizonte_principal": "H3",
            "horizontes": {"H3": {"fecha_resolucion": fin}}, "catalizadores": [{"fecha": cat}] if cat else [],
            "objeciones": [{"fuerza": "moderada", "estado": "SIN_RESOLVER"}] if moderada else []}


@pytest.mark.parametrize("op, esperado", [
    (_op(72, 70), "ENVIAR_A_BLOQUE_B"),
    (_op(65, 80), "PROFUNDIZAR_EN_A"),           # antes: ENVIAR con E < 70 si RK ≥ 65
    (_op(72, 70, moderada=True), "VIGILAR"),
    (_op(72, 70, cat=None), "VIGILAR"),
    (_op(72, 70, cat="2027-03-01"), "VIGILAR"),  # catalizador fuera del horizonte principal
])
def test_siguiente_paso_sigue_al_prompt_del_analizador(op, esperado):
    assert sintesis._siguiente_paso(op, UMB) == esperado


# ---------------------------------------------------------------- CS-01 · horizonte principal del Analista (8.3)
def test_esquema_finalista_admite_horizonte_principal_y_justificacion():
    from bloque_a.contratos import FINALISTA
    assert {"horizonte_principal", "justificacion_horizonte"} <= set(FINALISTA["properties"])


# ================================================================ T-53 · QA ronda 1 (H-01 a H-05)


def _con_simbolo_extra(tmp_path, fechas):
    datos = tmp_path / "datos"
    shutil.copytree(DATOS, datos)
    (datos / "USDNEW=X.csv").write_text("fecha,cierre\n" + "\n".join(f"{d.date()},1.0{i % 9}" for i, d in enumerate(fechas)) + "\n")
    uni = Path(RUTA_UNIVERSO_EJEMPLO).read_text(encoding="utf-8").rstrip("\n") + \
        "\nUSDNEW=X,DIV,Dólar frente a nueva divisa,ESTRATEGIA,GLB,G10,USD,SOLO EJEMPLO,Pares,Par nuevo,Otros cruces,USD/NEW,\n"
    (tmp_path / "u.csv").write_text(uni, encoding="utf-8")
    return _bloque(tmp_path, datos=datos, universo=tmp_path / "u.csv")


# ---------------------------------------------------------------- H-01 · símbolo deslistado antes de la ventana
def test_h01_simbolo_deslistado_no_vacia_su_tipo(tmp_path):
    b = _con_simbolo_extra(tmp_path, pd.bdate_range("2020-01-01", "2021-12-31"))
    r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    assert r["paquete"]["clases"]["DIV"]["opciones"]          # antes: 0 opciones, fichas del Motor rechazadas
    assert r["estado"] == "PARCIAL"
    assert "USDNEW=X" in b._sin_historia[("DIV", r["run_id"])]


def test_h01_historia_corta_tambien_queda_declarada(tmp_path):
    b = _con_simbolo_extra(tmp_path, pd.bdate_range("2026-05-22", "2026-06-05"))
    r = b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    assert r["paquete"]["clases"]["DIV"]["opciones"]
    rechazadas = b._fichas_rechazadas.get(("DIV", r["run_id"])) or []
    lagunas = " ".join(r["paquete"]["limitaciones"])
    assert not rechazadas or "rechazadas" in lagunas          # si el Motor rechaza fichas, se declara
    # antes: ML-CLUS-001 rechazado en silencio, run COMPLETO. T-65 (H-16): el proxy corto se excluye y se declara, y el resto
    # se agrupa (antes de T-65 se declaraba «no calculados» para todos)
    assert "clústeres de exposición sin medir para USDNEW=X" in lagunas
    assert r["estado"] == "PARCIAL"


# ---------------------------------------------------------------- H-02 / H-03 · horizonte principal del Analista (CS-01, C17)
def _ciclo_con_parche(tmp_path, monkeypatch, parche):
    orig = mr._ficha

    def _f(u, msg, ctx, rng, iny):
        out = orig(u, msg, ctx, rng, iny)
        parche(out)
        return out
    monkeypatch.setattr(mr, "_ficha", _f)
    b = _bloque(tmp_path)
    return b.ciclo(AS_OF, alcance={"clases": ["RV"]})


def test_h03_se_usan_el_horizonte_y_la_justificacion_del_analista(tmp_path, monkeypatch):
    r = _ciclo_con_parche(tmp_path, monkeypatch, lambda o: o.update(horizonte_principal="H2", naturaleza_inversion="TACTICA",
                                                                    justificacion_horizonte="Catalizador trimestral"))
    ops = r["paquete"]["clases"]["RV"]["opciones"]
    con_h2 = [o for o in ops if "H2" in o["horizontes"]]
    assert con_h2                                              # antes: el ejecutor elegía H3 e ignoraba la justificación
    assert all(o["horizonte_principal"] == "H2" and o["justificacion_horizonte"] == "Catalizador trimestral" for o in con_h2)


def test_h02_h5_declarado_sin_naturaleza_no_se_bloquea_por_la_naturaleza_por_defecto(tmp_path, monkeypatch):
    def parche(o):
        o["horizonte_principal"] = "H5"
        o.pop("naturaleza_inversion", None)
    r = _ciclo_con_parche(tmp_path, monkeypatch, parche)
    ops = r["paquete"]["clases"]["RV"]["opciones"]
    assert ops                                                 # antes: CICLICA por defecto, C17 y el tipo vacío
    assert all(o["horizonte_principal"] == "H5" and o["naturaleza_inversion"] == "ESTRUCTURAL" for o in ops)
    assert "C17" not in json.dumps(r["g3"].get("bloqueos"), ensure_ascii=False)


def test_h02_horizonte_no_ofrecido_se_declara_como_limitacion(tmp_path, monkeypatch):
    r = _ciclo_con_parche(tmp_path, monkeypatch, lambda o: o.update(horizonte_principal="H1", naturaleza_inversion="TACTICA"))
    ops = r["paquete"]["clases"]["RV"]["opciones"]
    assert ops and all("H1" not in o["horizontes"] for o in ops)   # H1 no se ofrece en RV con estos datos
    assert any("(H1)" in x and "no está entre los ofrecidos" in x for x in r["paquete"]["limitaciones"])   # antes: en silencio


@pytest.mark.parametrize("opciones, esperado", [
    ([_op(72, 70)], "VERDE"),
    ([_op(65, 80), _op(60, 60)], "AMBAR"),
    ([], "GRIS"),
])
def test_h03_semaforo(opciones, esperado):
    assert sintesis._semaforo(opciones, UMB) == esperado


# ---------------------------------------------------------------- H-04 · festivos de mercado en PS2 de H1
@pytest.mark.parametrize("as_of, dato, esperado", [
    ("2026-04-04", "2026-04-02", True),     # sábado tras Viernes Santo, dato del jueves
    ("2025-12-27", "2025-12-24", True),     # sábado tras Navidad y San Esteban, dato del 24
    ("2026-06-06", "2026-06-05", True),     # sábado normal, dato del viernes
    ("2026-06-10", "2026-06-07", False),    # control: más de una sesión
])
def test_h04_ps2_h1_descuenta_festivos(tmp_path, as_of, dato, esperado):
    b = _bloque(tmp_path)
    assert b._puertas({"senales": {"fecha_dato": dato}}, "N1", as_of, ["H1"])["PS2"] is esperado


# ---------------------------------------------------------------- H-05 · la degradación de H5 se aplica en el ciclo siguiente (CS-12)
def _sembrar_degradacion_h5(a):
    a.reloj.fijar("2026-06-01")
    ids = []
    for i, o in enumerate([1] * 5 + [0] * 15):
        hid = f"HIT-2025-{i + 1:04d}"
        ids.append(hid)
        a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": hid, "opp_id": "OPP-X", "clase": "RV", "horizonte": "H4",
                                   "prob_interna": 0.65, "sentido": "POSITIVO", "en_informe": True, "es_hito": True,
                                   "prg_padre": "PRG-2025-0999", "fecha_emision": "2025-06-05", "fecha_resolucion": "2026-05-29",
                                   "referencia_ingenua": {"valor_o_prob": 0.5}, "estado": "ABIERTO"})
        a.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": hid, "estado": "RESUELTO",
                                   "resolucion": {"resultado_binario": o, "comprobacion_fuga": "SUPERADA", "fecha_resuelto": "2026-05-29"}})
    a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2025-0999", "opp_id": "OPP-X", "clase": "RV", "horizonte": "H5",
                               "prob_interna": None, "hit_ids": ids, "fecha_emision": "2025-06-05", "fecha_resolucion": "2045-06-05",
                               "estado": "ABIERTO"})


def test_h05_degradacion_h5_cambia_la_tabla_del_ciclo_siguiente(tmp_path):
    b = _bloque(tmp_path)
    _sembrar_degradacion_h5(b.almacen)
    antes = aplicabilidad(b.cfg, "RV", "H5")
    r = b.ciclo("2026-06-05", alcance={"clases": ["RV"]})
    assert (r["evaluacion"] or {}).get("degradacion_h5")
    b.ciclo("2026-06-12", alcance={"clases": ["RV"]})
    assert antes == "SI" and aplicabilidad(b.cfg, "RV", "H5") == "LIMITADO"


# ---------------------------------------------------------------- H-12 · la tabla vigente no pasa entre instancias
def test_h12_dos_bloques_con_la_misma_configuracion_no_comparten_la_tabla_de_horizontes(tmp_path):
    cfg = cargar_config(extra={"modo": "backtest", "perfiles": {"activos": list(CLASES)}})
    uni = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    a = Bloque(cfg, ProveedorCSV(DATOS), uni, MockClient(), tmp_path / "ea", tmp_path / "sa")
    b = Bloque(cfg, ProveedorCSV(DATOS), uni, MockClient(), tmp_path / "eb", tmp_path / "sb")
    _sembrar_degradacion_h5(a.almacen)
    a.ciclo("2026-06-05", alcance={"clases": ["RV"]})
    a.ciclo("2026-06-12", alcance={"clases": ["RV"]})
    assert aplicabilidad(a.cfg, "RV", "H5") == "LIMITADO"
    assert "_tabla_horizontes" not in cfg                      # antes: el ciclo escribía en el dict del llamador
    r = b.ciclo("2026-06-12", alcance={"clases": ["RV"]})
    assert aplicabilidad(b.cfg, "RV", "H5") == "SI"
    assert any("H5" in o["horizontes"] for o in r["paquete"]["clases"]["RV"]["opciones"])
