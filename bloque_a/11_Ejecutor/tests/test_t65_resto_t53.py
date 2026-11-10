"""T-65 · Resto técnico de la revisión T-53 del Bloque A: CA-14, CA-15, CS-08, CS-10, CS-11, CS-18, CS-19 y CS-23.

Cada prueba falla sin su corrección (ver `.docs/tickets/T-65/pruebas.md`).
"""
import copy
import re
import shutil
import threading
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.almacen import PARAMETROS_CALIBRABLES, PARAMETROS_SERVICIO, Almacen
from bloque_a.configuracion import (
    DIR_EJECUTOR,
    DIR_PAQUETE,
    RUTA_CONFIG_POR_DEFECTO,
    RUTA_UNIVERSO_EJEMPLO,
    cargar_config,
    config_por_defecto,
    parametro,
    sesiones_horizonte,
)
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.herramientas.referencia import ht03_puntuaciones as ht03_ref
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from conftest import AS_OF, DATOS, config_pruebas

from bloque_a import contratos

RAIZ_BLOQUE = DIR_EJECUTOR.parent
SIG = str((pd.Timestamp(AS_OF) + pd.Timedelta(days=7)).date())


def _bloque(tmp_path, cfg=None, datos=DATOS, universo=RUTA_UNIVERSO_EJEMPLO):
    return Bloque(cfg or config_pruebas(), ProveedorCSV(datos), cargar_universo(universo), MockClient(),
                  Path(tmp_path) / "estado", Path(tmp_path) / "ent")


def _capturar_motor(b) -> list[dict]:
    peticiones: list[dict] = []
    servir = b.motor.servir

    def _servir(peticion, *a, **kw):
        peticiones.append(copy.deepcopy(peticion))
        return servir(peticion, *a, **kw)
    b.motor.servir = _servir
    return peticiones


# ---------------------------------------------------------------- CA-14 · números de la configuración
def test_ca14_sesiones_por_horizonte_salen_de_la_configuracion():
    cfg = cargar_config()
    assert {h: sesiones_horizonte(cfg, h) for h in ("H1", "H2", "H3", "H4", "H5")} == \
        {"H1": 5, "H2": 20, "H3": 126, "H4": 252, "H5": 2520}          # los mismos valores que la tabla anterior
    otra = cargar_config(extra={"horizontes": {"H3": {"meses": 3}}, "calendario": {"sesiones_por_mes": 20}})
    assert sesiones_horizonte(otra, "H3") == 60 and sesiones_horizonte(otra, "H4") == 240   # antes: 126 y 252 fijos


def test_ca14_tasa_base_con_parametros_de_la_configuracion(tmp_path):
    b = _bloque(tmp_path, cfg=config_pruebas(tasa_base={"min_ventanas": 10_000, "sin_historia": 0.4}))
    b.fijar_fecha(AS_OF)
    ri = b.evaluador.tasa_base("SPY", "ACWI", "RV", 5, True, AS_OF, "RUN-2026-0001")
    assert ri["valor_o_prob"] == 0.4                               # antes: 0,5 y 5 ventanas escritos en el código
    rc = next(x for x in b.almacen.leer("RC") if x.get("calc_id") == ri["calc_id"])
    assert "menos de 10000 ventanas: tasa base 0,4 por defecto" in rc["limitaciones"][0]
    b2 = _bloque(tmp_path / "b2", cfg=config_pruebas(tasa_base={"recorte": [0.45, 0.55]}))
    b2.fijar_fecha(AS_OF)
    assert 0.45 <= b2.evaluador.tasa_base("SPY", "ACWI", "RV", 5, True, AS_OF, "RUN-2026-0001")["valor_o_prob"] <= 0.55


def test_ca14_zona_de_interes_y_confianza_de_la_configuracion(tmp_path):
    b = _bloque(tmp_path, cfg=config_pruebas(presentacion={"zona_interes": 0.10, "confianza_probable_E": 101}))
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    ops = r["paquete"]["clases"]["RV"]["opciones"]
    assert ops
    for o in ops:
        z = o["minigrafico"]["zona_interes"]
        assert z["max"] / z["min"] == pytest.approx(1.10 / 0.90, rel=1e-4)    # antes: ±5 % fijo
        assert o["confianza"] == "especulativo"                     # E nunca llega a 101


def test_ca14_c6_sin_sigma_trata_el_delta_como_material(tmp_path):
    datos = tmp_path / "datos"
    shutil.copytree(DATOS, datos)
    fechas = pd.bdate_range("2026-05-11", AS_OF)                    # 4 semanas: σ semanal no estimable
    (datos / "USDNEW=X.csv").write_text("fecha,cierre\n" + "".join(f"{d.date()},1.0{i % 9}\n" for i, d in enumerate(fechas)))
    b = _bloque(tmp_path, datos=datos)
    b.fijar_fecha(AS_OF)
    opp = {"opp_id": "OPP-2026-0001", "clase": "DIV", "indicador_seguimiento": {"simbolo": "USDNEW=X"}}
    rev = b.seguimientos._revision({"fecha_alta": "2026-05-29"}, opp, pd.Timestamp(AS_OF))
    assert rev["material"] is True and rev["umbral_material"] is None    # antes: umbral inventado del 5 %
    assert any("σ semanal de USDNEW=X no estimable" in x for x in rev["limitaciones"])


# ---------------------------------------------------------------- CA-15 · determinismo de F5 y de los msg_id del paralelo
def test_ca15_msg_id_del_paralelo_no_dependen_del_orden_de_los_hilos(tmp_path):
    llamadas = iter(range(100))

    def ids(orden: list[str]) -> dict[str, list[str]]:
        m = contratos.Mensajeria(Almacen(tmp_path / f"almacen_{next(llamadas)}"))
        out: dict[str, list[str]] = {}
        turnos = {c: threading.Event() for c in orden}

        def trabajo(clase, siguiente):
            try:
                assert turnos[clase].wait(30)
                with m.ambito(clase):
                    for _ in range(3):
                        cuerpo = {"clase": clase, "fase": "CRIBADO_E_INVESTIGACION", "nivel": "N2", "opciones_vigentes": [],
                                  "lecciones": []}
                        out.setdefault(clase, []).append(
                            m.crear("CT-06", "AG-02", contratos.AGENTE_CLASE[clase], cuerpo, run_id="RUN-2026-0001")["msg_id"])
            finally:
                if siguiente:
                    turnos[siguiente].set()
        hilos = [threading.Thread(target=trabajo, args=(c, orden[i + 1] if i + 1 < len(orden) else None)) for i, c in enumerate(orden)]
        for h in hilos:
            h.start()
        turnos[orden[0]].set()
        for h in hilos:
            h.join(60)
        return out
    a, b = ids(["RV", "DIV"]), ids(["DIV", "RV"])
    assert a == b and len(a["RV"]) == 3                             # antes: MSG-…0001 era de quien llegaba antes
    assert a["RV"][0] == "MSG-RV-2026-000001"


def test_ca15_participantes_de_f5_en_orden_de_agente(tmp_path):
    b = _bloque(tmp_path)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV", "DIV", "MP"]})
    run = next(x for x in b.almacen.leer("F5") if x.get("tipo_entrada") == "RUN" and x.get("id") == r["run_id"])
    agentes = [p["agente"] for p in run["participantes"]]
    assert agentes == sorted(agentes) and len(agentes) > 3


# ---------------------------------------------------------------- CS-08 · fichas «Documentado» del Catálogo
@pytest.mark.parametrize("ficha", ["ACC-ERP-001", "FX-MOM-001", "REI-CAP-001"])
def test_cs08_fichas_documentadas_no_entregan_cifras(tmp_path, ficha):
    b = _bloque(tmp_path)
    b.fijar_fecha(AS_OF)
    r = b.motor.servir({"operacion": ficha, "plan": "PLAN_MIN", "datos": [{"serie": "SPY"}],
                        "valores": {"rent_esperada": 0.06, "rent_libre": 0.02}}, "AG-02", "RUN-2026-0001")
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "METODO_NO_IMPLEMENTADO"   # antes: SERVED
    assert "Documentado" in r["detalle"]


def test_cs08_no_se_ofrece_como_alternativa_una_ficha_que_no_se_sirve(tmp_path):
    b = _bloque(tmp_path)
    b.fijar_fecha(AS_OF)
    for ficha in ("ACC-VAL-001", "REI-NAV-001"):                    # su alternativa era ACC-ERP-001 o REI-CAP-001
        r = b.motor.servir({"operacion": ficha, "plan": "PLAN_MIN", "datos": []}, "AG-02", "RUN-2026-0001")
        assert r["estado"] == "RECHAZADO" and not r.get("alternativa") and "alternativa" not in r["detalle"]
    r = b.motor.servir({"operacion": "RISK-VAR-001", "plan": "PLAN_MIN", "datos": []}, "AG-02", "RUN-2026-0001")
    assert r.get("alternativa") == "RISK-DD-001"


# ---------------------------------------------------------------- CS-10 · resto de números de reglas
def test_cs10_la_resolucion_usa_las_replicas_de_la_configuracion(tmp_path):
    b = _bloque(tmp_path, cfg=config_pruebas(evaluacion={"bootstrap_replicas": 321, "simulaciones_ece": 123}))
    b.fijar_fecha(AS_OF)
    b.almacen.escribir("F4", "AG-10", {
        "tipo_entrada": "ALTA", "prg_id": "PRG-2026-0901", "opp_id": "OPP-1", "clase": "RV", "horizonte": "H2", "estado": "ABIERTO",
        "prob_interna": 0.65, "sentido": "POSITIVO", "umbral": 0.0, "tipo_pronostico": "ABSOLUTO", "referencia_indice": None,
        "variable": {"serie_ht01": "SPY"}, "fecha_emision": "2026-04-03", "fecha_resolucion": "2026-05-01",
        "nivel_referencia": {"valor": 1.0, "fecha": "2026-04-03"}, "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True})
    peticiones = _capturar_motor(b)
    assert b.evaluador.resolver(AS_OF, "RUN-2026-0001")
    fc = [p for p in peticiones if p.get("operacion") == "FC-EVAL-001"]
    assert fc and all(p["parametros"] == {"replicas": 321, "simulaciones": 123} for p in fc)   # antes: 200 y 200


@pytest.mark.parametrize("celdas", [1, 3])
def test_cs10_celdas_de_rotacion_exploratoria_de_la_configuracion(tmp_path, celdas):
    b = _bloque(tmp_path, cfg=config_pruebas(seleccion={"rotacion_exploratoria_celdas": celdas}))
    b.ciclo(AS_OF, alcance={"clases": ["RF"]})
    cuerpos: list[dict] = []
    crear = b.mensajeria.crear

    def _crear(contrato, emisor, receptor, cuerpo, **kw):
        if contrato == "CT-06" and cuerpo.get("fase") == "REVISION_VIGENTES":
            cuerpos.append(copy.deepcopy(cuerpo))
        return crear(contrato, emisor, receptor, cuerpo, **kw)
    b.mensajeria.crear = _crear
    b.ciclo(SIG, tipo="AD_HOC", alcance={"clases": ["RF"]}, nivel_forzado="N1")
    assert cuerpos and len(cuerpos[0]["rotacion_exploratoria"]) == celdas    # antes: siempre 2


def test_cs10_todas_las_claves_leidas_existen_en_por_defecto():
    """Toda ruta que el paquete lee con `parametro(...)` está en `por_defecto.yaml` (si faltara, el ciclo fallaría cerrado)."""
    rutas = set()
    for f in DIR_PAQUETE.rglob("*.py"):
        rutas |= set(re.findall(r'parametro\([^,()]+, f?"([a-zA-Z_0-9.]+)"\)', f.read_text(encoding="utf-8")))
    assert len(rutas) > 40
    faltan = []
    for r in sorted(rutas):
        try:
            parametro({}, r)
        except KeyError:
            faltan.append(r)
    assert not faltan, faltan
    for r in ("ps1.raices_min", "pregunta_repetida.veces", "evaluacion.recalibracion_rk", "seleccion.rotacion_exploratoria_celdas"):
        assert r in rutas or r.rsplit(".", 1)[0] in rutas


# ---------------------------------------------------------------- CS-11 · parámetros de HT-03 y regímenes de F10
def test_cs11_parametros_ht03_del_yaml_iguales_al_corpus():
    yaml_p = config_por_defecto()["parametros_ht03"]
    for k, v in yaml_p.items():
        assert v == ht03_ref.PARAMETROS_POR_DEFECTO[k], k
    assert set(ht03_ref.PARAMETROS_POR_DEFECTO) - set(yaml_p) == {"tipos_activo", "puertas_obligatorias"}


def test_cs11_parametros_ht03_se_leen_de_la_seccion_del_yaml(tmp_path):
    b = _bloque(tmp_path, cfg=config_pruebas(parametros_ht03={"umbrales": {"E": 61}}))
    assert b.params_ht03["umbrales"]["E"] == 61 and b.params_ht03["umbrales"]["A"] == 55   # antes: se ignoraba
    assert b.f10()["P-09"]["E"] == 61


def test_cs11_regimenes_de_f10_completos_segun_el_esquema():
    esquema = (RAIZ_BLOQUE / "05_Archivos_operativos" / "Configuración y parámetros del bloque (esquema V3.0).md").read_text(encoding="utf-8")
    filas = re.findall(r"^\| (P-\d\d) \| [^|]+ \| [^|]+ \| ([^|]+) \|", esquema, re.MULTILINE)
    assert len(filas) == 44
    calibrables = {p for p, reg in filas if reg.strip().startswith("CALIBRABLE")}
    servicio = {p for p, reg in filas if reg.strip().startswith("SERVICIO")}
    assert PARAMETROS_CALIBRABLES == calibrables                    # antes: faltaban P-35, P-36, P-39 y P-40
    assert PARAMETROS_SERVICIO == servicio                          # antes: faltaban P-34, P-38 y P-44


def test_cs11_p30_sin_respaldo_4_0(tmp_path):
    cfg = config_pruebas()
    del cfg["methodology_version"]
    b = _bloque(tmp_path, cfg=cfg)
    assert b.f10()["P-30"] == config_por_defecto()["methodology_version"]   # antes: «4.0»


# ---------------------------------------------------------------- CS-18 · ventana de ML-CLUS-001
@pytest.mark.parametrize("semanas", [156, 104])
def test_cs18_la_ventana_de_clusteres_sale_de_la_configuracion(tmp_path, semanas):
    b = _bloque(tmp_path, cfg=config_pruebas(clusteres={"ventana_semanas": semanas}))
    b.fijar_fecha(AS_OF)
    peticiones = _capturar_motor(b)
    analisis = {"DIV": {"finalistas": [{"proxy": p, "_gc3": True} for p in ("EURUSD=X", "USDJPY=X", "AUDUSD=X")]}}
    b._clusteres(analisis, AS_OF, "RUN-2026-0001")
    p = next(x for x in peticiones if x["operacion"] == "ML-CLUS-001")
    assert p["parametros"]["ventana_semanas"] == semanas
    inicio = (pd.Timestamp(AS_OF) - pd.Timedelta(weeks=semanas + 2)).normalize()
    assert {d["inicio"] for d in p["datos"]} == {str(inicio.date())}   # antes: siempre 2 años + 14 días


def test_cs18_por_defecto_la_ventana_del_catalogo():
    assert cargar_config()["clusteres"]["ventana_semanas"] == 156   # Catálogo, ML-CLUS-001: ≥ 3 años semanales


# ---------------------------------------------------------------- CS-19 · mapa de pruebas al día
def test_cs19_mapa_cubre_las_67_pruebas_del_plan():
    plan = (RAIZ_BLOQUE / "09_Pruebas" / "Plan de pruebas del Bloque A - V3.0.md").read_text(encoding="utf-8")
    mapa = (DIR_EJECUTOR / "tests" / "MAPA_PLAN_DE_PRUEBAS.md").read_text(encoding="utf-8")
    pb_plan = sorted(set(re.findall(r"^### (PB-\d\d)", plan, re.MULTILINE)))
    assert len(pb_plan) == 67
    pb_mapa = set(re.findall(r"\bPB-\d\d\b", mapa))
    assert not set(pb_plan) - pb_mapa, sorted(set(pb_plan) - pb_mapa)
    assert "Plan de pruebas V3.0" in mapa.splitlines()[0] and "67 pruebas" in mapa
    funciones = set()
    for f in (DIR_EJECUTOR / "tests").glob("test_*.py"):
        funciones |= set(re.findall(r"^def (test_\w+)", f.read_text(encoding="utf-8"), re.MULTILINE))
    modulos = {f.stem for f in (DIR_EJECUTOR / "tests").glob("test_*.py")}
    citadas = []
    for cita in re.findall(r"`([^`]+)`", mapa):
        if cita.startswith("10_Herramientas/"):
            assert (RAIZ_BLOQUE / cita.split("::")[0]).exists(), cita
            continue
        citadas += re.findall(r"\btest_\w+", cita)
    rotas = [c for c in citadas if c not in funciones and c not in modulos]
    assert citadas and not rotas, rotas


# ---------------------------------------------------------------- CS-23 · la prueba citada existe
def test_cs23_herramientas_cita_una_prueba_que_existe():
    doc = (DIR_PAQUETE / "herramientas" / "__init__.py").read_text(encoding="utf-8")
    citas = re.findall(r"`(test_\w+\.py)(?:::(test_\w+))?`", doc)
    assert citas
    for archivo, funcion in citas:
        ruta = DIR_EJECUTOR / "tests" / archivo
        assert ruta.exists(), archivo                                # antes: test_herramientas.py, que no existe
        assert not funcion or f"def {funcion}(" in ruta.read_text(encoding="utf-8")


def test_yaml_sin_claves_duplicadas_en_las_secciones_nuevas():
    texto = RUTA_CONFIG_POR_DEFECTO.read_text(encoding="utf-8")
    for clave in ("calendario:", "tasa_base:", "presentacion:", "senales:", "ps1:", "pregunta_repetida:", "parametros_ht03:",
                  "redaccion:"):
        assert len(re.findall(rf"^{clave}", texto, re.MULTILINE)) == 1, clave
