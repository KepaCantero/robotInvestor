"""T-113 · deuda técnica del Bloque A: T-104, T-107, T-108, T-109 y T-110."""
import copy
import json
from pathlib import Path

import numpy as np
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config
from bloque_a.motor import fichas_mon_idx, servicio


class _Proveedor:
    as_of = None
    nombre = "pruebas"


def _motor(tmp_path):
    return servicio.Motor(Almacen(Path(tmp_path)), _Proveedor(), cargar_config())


def _valores(ficha, i=0):
    caso = servicio.CASOS_CONTROL[ficha][i]
    return {k: v for d in caso["datos"] for k, v in (d.get("valores") or {}).items()}, dict(caso.get("parametros") or {})


# ================================================================================================== T-108
def test_h23_la_cota_de_cada_reunion_acota_su_probabilidad():
    """Perturbaciones al azar dentro de la precisión declarada: el cambio de la probabilidad de cada reunión (movimientos en
    la reunión) y de la acumulada no pasa de su cota publicada. Con la cota anterior (la del tipo), se pasaba hasta 1,35 veces."""
    v, params = _valores("MON-EXP-001")
    prec = 2e-6
    v = {**v, "precision_cotizacion": prec}
    fn = servicio.IMPLEMENTADAS["MON-EXP-001"]["fn"]
    base, _ = fn({"valores": copy.deepcopy(v), "series": {}, "series_rol": {}}, dict(params))
    rng = np.random.default_rng(20261113)
    peor_r = peor_a = 0.0
    for _ in range(300):
        w = copy.deepcopy(v)
        for n in w["curva"]:
            n["tipo"] += float(rng.choice([-1.0, 1.0])) * prec * float(rng.uniform(0.5, 1.0))
        try:
            r, _ = fn({"valores": w, "series": {}, "series_rol": {}}, dict(params))
        except Exception:   # noqa: BLE001, S112 — una perturbación que la ficha rechaza no cuenta
            continue
        for s0, s1 in zip(base["senda"], r["senda"]):
            dr = abs(s1["movimientos_en_reunion"] - s0["movimientos_en_reunion"])
            da = abs(s1["movimientos_acumulados"] - s0["movimientos_acumulados"])
            assert dr <= s0["incertidumbre_probabilidad"] * (1 + 1e-6) + 1e-12
            assert da <= s0["incertidumbre_probabilidad_acumulada"] * (1 + 1e-6) + 1e-12
            peor_r = max(peor_r, dr / max(s0["incertidumbre_probabilidad"], 1e-300))
            peor_a = max(peor_a, da / max(s0["incertidumbre_probabilidad_acumulada"], 1e-300))
    assert peor_r > 0.3 and peor_a > 0.3   # las cotas no son triviales: las perturbaciones se acercan a ellas


@pytest.mark.parametrize("cambio", [{"momentum_retro_meses": -20}, {"momentum_retro_meses": 2.5}, {"momentum_salto_meses": 12},
                                    {"momentum_corto_meses": 0}, {"ventana_anios": 10 ** 9}])
def test_h24_idx_rel_ventanas_con_dominio(cambio):
    v, params = _valores("IDX-REL-001")
    with pytest.raises(servicio.op.ErrorFicha):
        servicio.IMPLEMENTADAS["IDX-REL-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {**params, **cambio})


@pytest.mark.parametrize("ficha,cambio", [("MON-EXP-001", {"diferencial_estable_dias": 0}), ("MON-EXP-001", {"diferencial_estable_dias": -1}),
                                          ("MON-EXP-001", {"diferencial_estable_dias": 2.5}), ("MON-EXP-001", {"incremento_pb": 0}),
                                          ("MON-EXP-001", {"meses_cambio_acumulado": [6, 10 ** 6]}),
                                          ("IDX-CONC-001", {"media_amplitud": 0}), ("IDX-CONC-001", {"meses_diferencial": []}),
                                          ("IDX-REB-001", {"ventana_post_sesiones": -5}), ("MON-YLD-001", {"plazos_meses": [1, 1.5]}),
                                          ("MON-REAL-001", {"plazo_meses": 0}), ("MON-FIX-001", {"escenarios_pb": [float("inf")]}),
                                          ("MON-FIX-001", {"escenarios_pb": list(range(21))})])
def test_h24_ventanas_plazos_y_listas_de_mon_e_idx_con_dominio(ficha, cambio):
    v, params = _valores(ficha)
    with pytest.raises(servicio.op.ErrorFicha, match="parámetro|momentum"):
        servicio.IMPLEMENTADAS[ficha]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {**params, **cambio})


def test_h25_n02_los_recomendados_son_umbrales_fijos():
    for f, claves in fichas_mon_idx.UMBRALES.items():
        assert {k for k in fichas_mon_idx.PARAMETROS_POR_DEFECTO[f] if k.endswith("_recomendados")} <= claves
    v, params = _valores("MON-REAL-001")
    with pytest.raises(servicio.op.ErrorFicha, match="umbrales fijos"):
        servicio.IMPLEMENTADAS["MON-REAL-001"]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {**params, "anios_recomendados": 1})


def test_h25_n10_una_serie_con_fin_ilegible_es_un_rechazo(tmp_path):
    r = _motor(tmp_path).servir({"operacion": "ST-DESC-001", "datos": [{"serie": "SPY", "fin": "mañana"}], "fecha_corte": "2026-11-12"}, "AG-03")
    assert r["estado"] == "RECHAZADO" and r["motivo"] in ("DATOS_INCOHERENTES", "DATOS_NO_DISPONIBLES")


@pytest.mark.parametrize("extra", [{"plan": ["PLAN_MIN"]}, {"plan": {"a": 1}}, {"parametros": {1: "a", "b": 2}},
                                   {"perfil": [{(1, 2): 3}]}, {"clase": {1: 2, "x": 3}}])
def test_h22_campos_no_serializables_son_un_rechazo_en_rc(tmp_path, extra):
    m = _motor(tmp_path)
    r = m.servir({"operacion": "ST-DESC-001", "datos": [], "fecha_corte": "2026-11-12", **extra}, "AG-03")
    assert r["estado"] == "RECHAZADO" and r["motivo"] == "DATOS_INCOHERENTES" and m.almacen.leer("RC")[-1]["tipo_entrada"] == "RECHAZO"


# ================================================================================================== T-104
def test_h54_una_linea_cortada_en_la_cache_no_impide_arrancar(tmp_path):
    from bloque_a.herramientas.ht06_indice import CacheResultados
    ruta = tmp_path / "cache_resultados.jsonl"
    ruta.write_bytes(json.dumps({"clave": "a", "valor": 1}).encode() + b"\n{\"clave\": \"b\", \"val" + "é".encode()[:1])
    c = CacheResultados(ruta)
    assert c.obtener("a") == 1 and c.descartadas == 1


def test_h54_la_cache_tolera_una_linea_ilegible_en_medio(tmp_path):
    from bloque_a.herramientas.ht06_indice import CacheResultados
    ruta = tmp_path / "cache_resultados.jsonl"
    ruta.write_bytes(b'{"clave": "a", "valor": 1}\nno es json\n{"clave": "b", "valor": 2}\n')
    c = CacheResultados(ruta)
    assert c.obtener("a") == 1 and c.obtener("b") == 2 and c.descartadas == 1


def test_h54_la_grabacion_descarta_la_ultima_cortada_y_nombra_el_fichero_si_no(tmp_path):
    from bloque_a.llm import MockClient, ReplayClient
    ruta = tmp_path / "cinta.jsonl"
    ruta.write_bytes(b'{"clave": "a", "respuesta": {}}\n{"clave": "b", "resp')
    assert ReplayClient(ruta, "reproducir").descartadas == 1
    ruta.write_bytes(b'{"clave": "a"}\nno es json\n{"clave": "b"}\n')
    with pytest.raises(ValueError, match="cinta.jsonl: línea 2"):
        ReplayClient(ruta, "grabar", MockClient())


def test_h55_la_version_de_python_declarada_es_la_que_hace_falta():
    texto = (Path(servicio.DIR_EJECUTOR) / "pyproject.toml").read_text(encoding="utf-8")
    assert 'requires-python = ">=3.12"' in texto


def test_h56_contenido_sensible_lineal_con_mucho_anidamiento():
    import time

    from bloque_a.llm import contenido_sensible
    d: object = "x" * (1 << 20)
    for _ in range(400):
        d = {"a": d}
    t0 = time.perf_counter()
    assert not contenido_sensible(d)
    assert time.perf_counter() - t0 < 5
    assert contenido_sensible({"a": {"b": [{"c": "sk-" + "ant-api03-abcdefghijklmnopqrstuvwxyz0123"}]}})
    profundo: object = "sk-" + "ant-api03-abcdefghijklmnopqrstuvwxyz0123"
    for _ in range(5000):
        profundo = {"a": [profundo]}
    assert contenido_sensible(profundo)   # el secreto al fondo de 5 000 niveles se encuentra


# ================================================================================================== T-107
def _ciclo(tmp, diseno="v5", cierres=None):
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque
    from conftest import AS_OF, DATOS, config_pruebas
    b = Bloque(config_pruebas(diseno=diseno, perfiles={"activos": ["RV", "RF", "DIV", "MP", "IDX", "FON"]}, paralelismo={"hilos_analistas": 6}),
               ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), tmp / "estado", tmp / "ent")
    res = b.ciclo(AS_OF)
    return b, res


def test_h14_la_curacion_de_ag12_se_carga_a_la_bolsa_de_su_tipo(tmp_path, monkeypatch):
    from bloque_a.orquestacion import Bloque
    vistas = []
    orig = Bloque._invocar

    def espia(self, agente, contrato, mensaje, esquema, instrucciones, as_of, run_id, clase=None, fase=None, presupuesto=None, *a, **k):
        if agente == "AG-12" and fase == "investigacion":
            vistas.append((clase, presupuesto is not None))
        return orig(self, agente, contrato, mensaje, esquema, instrucciones, as_of, run_id, clase, fase, presupuesto, *a, **k)
    monkeypatch.setattr(Bloque, "_invocar", espia)
    _ciclo(tmp_path)
    assert vistas and all(con for _, con in vistas) and all(c for c, _ in vistas)   # antes iban sin presupuesto


def test_h15_el_consumo_total_del_run_es_el_mismo_con_hilos(tmp_path):
    vistos = set()
    for k in range(3):
        b, _ = _ciclo(tmp_path / str(k))
        run = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RUN"][-1]
        vistos.add(json.dumps({x: run["consumo"][x] for x in ("uc", "uc_llm", "entrada", "salida")}, sort_keys=True))
    assert len(vistos) == 1, vistos


def test_h16_las_limitaciones_por_presupuesto_salen_ordenadas(monkeypatch):
    from types import SimpleNamespace

    from bloque_a import sintesis
    cierres = [{"clase": "RV", "fase": "F2", "motivo": "b"}, {"clase": "IDX", "fase": "F1", "motivo": "a"}, {"clase": "RV", "fase": "F1", "motivo": "a"}]
    fuente = Path(sintesis.__file__).read_text(encoding="utf-8")
    assert 'sorted(presupuesto.cierres, key=lambda c: (c["clase"], c["fase"], c["motivo"]))' in fuente
    orden = sorted(cierres, key=lambda c: (c["clase"], c["fase"], c["motivo"]))
    assert [c["clase"] + c["fase"] for c in orden] == ["IDXF1", "RVF1", "RVF2"] and SimpleNamespace


# ================================================================================================== T-109 y T-110 (filtro del Sintetizador)
@pytest.fixture(scope="module")
def perm(tmp_path_factory):
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque
    from conftest import DATOS, config_pruebas

    from bloque_a import diseno_v6 as v6
    t = tmp_path_factory.mktemp("perm")
    b = Bloque(config_pruebas(diseno="v6"), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), t / "e", t / "n")
    return v6.permitidos_r21(b)


LEGITIMAS_T113 = ["El IPC sube por un quinto mes consecutivo.", "El ETF sube.", "El ETF cae.", "Comprar el ETF usd no tiene sentido.",
                  "Basilea III endurece el capital de los bancos.", "Es el gran tema del siglo XXI.", "El valor real del activo baja.",
                  "Según la AIE, la demanda de petróleo cae.", "El INE publica la EPA el jueves.", "La TAE de los depósitos sube.",
                  "El BID financia infraestructuras."]
PROHIBIDAS_T113 = [("CIFRA", "Sube un cuarto."), ("CIFRA", "The odds are seventy to thirty."), ("CIFRA", "There are a thousand reasons."),
                   ("R21", "Compre 🅝🅥🅓🅐 ya."), ("R21", "Comprar NVDAs ya."), ("R21", "Comprar N·V·D·A ya."), ("R21", "Comprar N.V.D.A ya."),
                   ("CIFRA", "Vemos las VII ideas de la semana.")]


@pytest.mark.parametrize("frase", LEGITIMAS_T113)
def test_t113_frases_legitimas(perm, frase):
    from bloque_a import diseno_v6 as v6
    assert v6.frase_prohibida(frase, perm) is None, frase


@pytest.mark.parametrize("regla,frase", PROHIBIDAS_T113)
def test_t113_frases_prohibidas(perm, regla, frase):
    from bloque_a import diseno_v6 as v6
    assert v6.frase_prohibida(frase, perm) == regla, frase


def test_h34_un_ticker_del_universo_en_minuscula_tras_el_valor(perm):
    from bloque_a import diseno_v6 as v6
    t = next(x for x in sorted(perm["tickers"]) if x.isalpha() and len(x) >= 3 and x.lower() not in v6._PALABRA_COMUN)
    for vehiculo in ("la acción", "el valor", "el título"):
        assert v6.frase_prohibida(f"Comprar {vehiculo} {t.lower()} ya.", perm) == "R21", (vehiculo, t)


class _Redaccion:
    def textos_por_defecto(self, paquete):
        from bloque_a.redaccion import Redaccion
        return Redaccion.textos_por_defecto(None, paquete)


def _paquete():
    return {"clases": {"RV": {"opciones": [{"opp_id": "OPP-1", "nombre_llano": "la renta variable"}], "candidatas_analizadas": 1},
                       "RF": {"opciones": [], "candidatas_analizadas": 3}},
            "apuestas_independientes": 1, "limitaciones": []}


@pytest.mark.parametrize("frases,esperadas", [(["Una."], 2), (["Una.", "Dos.", "Tres."], 2), (["Una.", "Dos."], 2)])
def test_h50_una_o_tres_frases_de_30s_se_normalizan_y_se_declaran(frases, esperadas):
    from types import SimpleNamespace

    from bloque_a.contratos import ESQUEMAS

    from bloque_a import diseno_v6 as v6
    f = ESQUEMAS["SINTESIS"]["properties"]["frases_30s"]
    assert (f["minItems"], f["maxItems"]) == (1, 3)
    paquete = _paquete()
    d = {"frases_30s": frases, "tarjetas": [], "motivos_llanos": {}, "glosario": [], "frase_historial": "Aún es pronto."}
    red = v6._redaccion_segura(SimpleNamespace(redaccion=_Redaccion()), paquete, d, {"codigos": frozenset(), "series": frozenset()})
    assert len(red["frases_30s"]) == 3 and red["frases_30s"][1] == frases[0]
    declarado = any("FORMATO" in x for x in paquete["limitaciones"])
    assert declarado == (len(frases) != esperadas)


def test_h49_cuentas_en_singular_motivos_solo_de_tipos_del_paquete_y_mayuscula():
    from types import SimpleNamespace

    from bloque_a import diseno_v6 as v6
    paquete = _paquete()
    defecto = _Redaccion().textos_por_defecto(paquete)
    assert defecto["frases_30s"][0] == "Esta semana vemos 1 idea en 1 tipo de inversión."
    assert v6._cuenta_motivo(paquete, "RV").startswith("De 1 idea de ") and "analizada, 1 pasó" in v6._cuenta_motivo(paquete, "RV")
    d = {"frases_30s": ["Una.", "Dos."], "tarjetas": [], "glosario": [], "frase_historial": "Aún es pronto.",
         "motivos_llanos": {"RF": "Preferimos esperar.", "ZETA": "No es un tipo."}}
    red = v6._redaccion_segura(SimpleNamespace(redaccion=_Redaccion()), paquete, d, {"codigos": frozenset(), "series": frozenset()})
    assert set(red["motivos_llanos"]) == {"RF"}
    limpio, reglas = v6.limpiar("Hay un 70 % de subida; el dólar pesa.", {"codigos": frozenset(), "series": frozenset()}, {})
    assert reglas == ["CIFRA"] and limpio == "El dólar pesa."
