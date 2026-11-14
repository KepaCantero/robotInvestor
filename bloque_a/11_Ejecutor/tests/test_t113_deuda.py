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


# ================================================================================================== Ronda r02 (QA r01 de T-113)
_SK = "sk-" + "ant-api03-abcdefghijklmnopqrstuvwxyz0123"
_CLAVE = "api" + "_key"


def _sensible_antes(valor) -> bool:
    """`contenido_sensible` tal como era antes de T-113 (recursivo): la referencia del diferencial de H-01."""
    from bloque_a.contratos import secretos_en_texto
    if isinstance(valor, (bytes, bytearray)):
        valor = bytes(valor).decode("utf-8", errors="replace")
    if isinstance(valor, str):
        return bool(secretos_en_texto(valor + '"'))
    if isinstance(valor, dict):
        return (bool(secretos_en_texto(json.dumps(valor, ensure_ascii=False, default=str)))
                or any(_sensible_antes(v) for v in valor.values()))
    if isinstance(valor, (list, tuple, set, frozenset)):
        return any(_sensible_antes(v) for v in valor)
    return False


class _ConTexto:
    def __str__(self):
        return _SK


@pytest.mark.parametrize("valor", [[{_CLAVE: "abcdef"}], [[{"pass" + "word": "valor-de-prueba"}]], ({"sec" + "ret": "x1"},),
                                   {"a": [{"client_" + "secret": "zz"}]}, [{_SK: 1}], [{"a": _ConTexto()}], [{"a": _SK.encode()}],
                                   (frozenset({_SK}),), [[{"type": "text", "text": "hola"}], [{"role": "user", "content": [{_CLAVE: "abcdef"}]}]]],
                         ids=["lista", "lista_lista", "tupla", "dict_lista", "clave_sk", "objeto", "bytes", "frozenset", "mensajes"])
def test_r02_h01_un_diccionario_bajo_una_lista_tupla_o_conjunto_se_sigue_viendo(valor):
    from bloque_a.llm import contenido_sensible
    assert _sensible_antes(valor) and contenido_sensible(valor)


def test_r02_h01_diferencial_con_la_version_anterior():
    """3 000 estructuras al azar (semilla fija): ninguna que antes era sensible deja de serlo, ni al revés."""
    import random

    from bloque_a.llm import contenido_sensible
    rng = random.Random(113)
    hojas = ["hola", _SK, 3, None, 2.5, True, "Bearer " + "a" * 25, "texto normal sk-learn", b"x", _SK.encode(), "AKIA" + "ABCDEFGHIJKLMNOP"]
    claves = ["a", "b", _CLAVE, "pass" + "word", "nota", _SK, "sec" + "ret"]

    def gen(prof):
        r = rng.random()
        if prof <= 0 or r < 0.35:
            return rng.choice(hojas)
        if r < 0.6:
            return {rng.choice(claves): gen(prof - 1) for _ in range(rng.randint(0, 3))}
        if r < 0.8:
            return [gen(prof - 1) for _ in range(rng.randint(0, 3))]
        if r < 0.9:
            return tuple(gen(prof - 1) for _ in range(rng.randint(0, 3)))
        return frozenset(rng.choice(hojas) for _ in range(2))
    casos = [gen(4) for _ in range(3000)]
    distintos = [x for x in casos if _sensible_antes(x) != contenido_sensible(x)]
    assert not distintos, repr(distintos[0])[:200].replace(_SK, "<clave>")
    assert 300 < sum(map(contenido_sensible, casos)) < 2700   # el banco tiene de las dos clases


def test_r02_h01_ciclos_y_demasiado_hondo_fallan_cerrado_y_terminan():
    from bloque_a.llm import contenido_sensible
    lista: list = ["inofensivo"]
    lista.append(lista)
    dic: dict = {"a": "inofensivo"}
    dic["yo"] = [dic]
    con_tupla: list = []
    con_tupla.append((con_tupla,))
    for ciclico in (lista, dic, con_tupla, [1, [2, lista]]):
        assert contenido_sensible(ciclico) is True
    compartida = ["inofensivo", {"a": 1}]
    assert contenido_sensible([compartida, compartida, {"x": compartida}]) is False   # la misma lista dos veces no es un ciclo
    hondo: object = "inofensivo"
    for _ in range(5000):
        hondo = {"a": [hondo]}
    assert contenido_sensible(hondo) is True   # H-56 (mutante M07): no se puede serializar para comprobarlo, falla cerrado
    lista_honda: object = {_CLAVE: "abcdef"}
    for _ in range(5000):
        lista_honda = [lista_honda]
    assert contenido_sensible(lista_honda) is True   # una lista honda no impide ver el diccionario del fondo
    with pytest.raises(TypeError):   # claves que no son texto: como antes, error del llamador (también con un secreto dentro)
        contenido_sensible({(1, 2): "x"})
    with pytest.raises(TypeError):
        contenido_sensible({1: _SK, (1, 2): "x"})
    assert contenido_sensible([_SK, {(1, 2): "x"}]) is True   # pero un secreto hallado pesa más
    with pytest.raises(TypeError):
        contenido_sensible(["inofensivo", {(1, 2): "x"}])


def test_r02_h01_lineal_con_listas_de_diccionarios():
    import time

    from bloque_a.llm import contenido_sensible
    honda: object = ["x" * 1000]
    for _ in range(50000):
        honda = [honda, {"k": "v"}]
    ancha = [{"a": "palabra " * 20, "b": [i, str(i)]} for i in range(20000)]
    t0 = time.perf_counter()
    assert not contenido_sensible(honda) and not contenido_sensible(ancha)
    assert time.perf_counter() - t0 < 20


def test_r02_h01_la_misma_lista_en_muchos_sitios_se_mira_una_vez():
    """Una lista que contiene dos veces a la anterior, 26 veces: 2**26 caminos, pero 27 listas. Cada contenedor se mira una vez."""
    import time

    from bloque_a.llm import contenido_sensible
    for hoja, esperado in (("inofensivo", False), ({"a": "inofensivo"}, False), (_SK, True), ({_CLAVE: "abcdef"}, True)):
        x: object = [hoja]
        for _ in range(26):
            x = [x, x]
        t0 = time.perf_counter()
        assert contenido_sensible(x) is esperado
        assert time.perf_counter() - t0 < 5


def test_r02_h01_la_ultima_puerta_antes_de_la_api_bloquea_el_contenido_estructurado():
    from types import SimpleNamespace

    from bloque_a.llm import AnthropicClient
    enviados: list = []
    c = AnthropicClient.__new__(AnthropicClient)
    c.sdk = SimpleNamespace(messages=SimpleNamespace(create=lambda **k: enviados.append(k)))
    c.salida_estructurada, c.max_continuaciones = False, 0
    for mensajes in ([{"role": "user", "content": [{"type": "tool_result", "content": {_CLAVE: "abcdef123456"}}]}],
                     [{"role": "user", "content": "hola", _CLAVE: "abcdef123456"}]):
        r = c.generar(agente="AG-01", modelo="m", system=[{"type": "text", "text": "s"}], mensajes=mensajes, max_tokens=10)
        assert r.stop_reason == "contenido_sensible" and not enviados


def test_r02_h02_tras_un_corte_se_puede_seguir_grabando_en_la_cache(tmp_path):
    from bloque_a.herramientas.ht06_indice import CacheResultados
    ruta = tmp_path / "cache_resultados.jsonl"
    ruta.write_bytes(b'{"clave": "a", "valor": 1}\n{"clave": "b", "val')
    c = CacheResultados(ruta)
    assert c.descartadas == 1 and ruta.read_bytes() == b'{"clave": "a", "valor": 1}\n'   # la línea cortada se quita
    c.guardar("nuevo", 7)
    c2 = CacheResultados(ruta)
    assert (c2.obtener("a"), c2.obtener("nuevo"), c2.descartadas) == (1, 7, 0)
    ruta.write_bytes(b'{"clave": "a", "valor": 1}\n{"clave": "b", "valor": 2}')   # última línea entera, sin salto: se conserva
    c3 = CacheResultados(ruta)
    c3.guardar("c", 3)
    c4 = CacheResultados(ruta)
    assert (c4.obtener("a"), c4.obtener("b"), c4.obtener("c"), c4.descartadas) == (1, 2, 3, 0)


def test_r02_h02_tras_un_corte_se_puede_seguir_grabando_en_la_cinta(tmp_path):
    from bloque_a.llm import LLMClient, ReplayClient, RespuestaLLM, Uso

    class _Base(LLMClient):
        nombre = "base_pruebas"

        def generar(self, **k):
            return RespuestaLLM('{"ok": true}', Uso(entrada=1, salida=1), k["modelo"], "end_turn")
    ruta = tmp_path / "cinta.jsonl"
    cortada = b'{"clave": "a", "texto": "{}", "uso": {}, "modelo": "m"}\n{"clave": "b", "tex'
    ruta.write_bytes(cortada)
    assert ReplayClient(ruta, "reproducir").descartadas == 1 and ruta.read_bytes() == cortada   # reproducir no escribe
    rc = ReplayClient(ruta, "grabar", _Base())
    assert rc.descartadas == 1
    for texto in ("hola", "adiós"):
        rc.generar(agente="AG-01", modelo="m", system=[{"type": "text", "text": "s"}], mensajes=[{"role": "user", "content": texto}], max_tokens=100)
    rc2 = ReplayClient(ruta, "reproducir")
    assert len(rc2._tabla) == 3 and rc2.descartadas == 0
    ilegible = b'{"clave": "a"}\nno es json\n{"clave": "b", "tex'
    ruta.write_bytes(ilegible)
    with pytest.raises(ValueError, match="cinta.jsonl: línea 2"):
        ReplayClient(ruta, "grabar", _Base())
    assert ruta.read_bytes() == ilegible   # valida antes de mutar: si la lectura falla, el fichero no se toca


def test_r02_h02_las_lineas_descartadas_se_declaran_al_arrancar(tmp_path):
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque
    from conftest import DATOS, config_pruebas

    def incidencias(carpeta):
        b = Bloque(config_pruebas(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(), carpeta, tmp_path / "ent")
        return [e for e in b.almacen.leer("HA") if e.get("tipo_entrada") == "INC" and "cache_resultados.jsonl" in e.get("detalle", "")]
    assert incidencias(tmp_path / "limpio") == []
    (tmp_path / "cortado").mkdir()
    (tmp_path / "cortado" / "cache_resultados.jsonl").write_bytes(b'{"clave": "a", "valor": 1}\nno es json\n{"clave": "b", "val')
    inc = incidencias(tmp_path / "cortado")
    assert len(inc) == 1 and inc[0]["tipo"] == "HERRAMIENTA" and ": 2 línea" in inc[0]["detalle"]


@pytest.mark.parametrize("linea,claves", [(b'{"clave": ["x"], "valor": 1}', 1), (b'{"clave": null, "valor": 1}', 1), (b"[1, 2]", 1),
                                          (b'{"clave": "z"}', 1), (b'{"clave": "z", "valor": ' + b"[" * 100000 + b"]" * 100000 + b"}", 1)],
                         ids=["clave_lista", "clave_nula", "lista", "sin_valor", "anidado"])
def test_r02_h06_la_cache_descarta_un_registro_que_no_vale(tmp_path, linea, claves):
    """H-06 y el mutante M03 de H-54: un registro que no es {clave de texto, valor} se descarta y se cuenta; no impide arrancar."""
    from bloque_a.herramientas.ht06_indice import CacheResultados
    ruta = tmp_path / "cache_resultados.jsonl"
    ruta.write_bytes(b'{"clave": "a", "valor": 1}\n' + linea + b"\n")
    c = CacheResultados(ruta)
    assert (c.obtener("a"), len(c._mem), c.descartadas) == (1, claves, 1)


def test_r02_h06_la_cinta_rechaza_una_clave_que_no_es_texto(tmp_path):
    from bloque_a.llm import ReplayClient
    ruta = tmp_path / "cinta.jsonl"
    ruta.write_bytes(b'{"clave": ["x"], "texto": "{}"}\n')
    with pytest.raises(ValueError, match="sin «clave»"):
        ReplayClient(ruta, "reproducir")


@pytest.mark.parametrize("frase", ["Las IIC españolas ganan peso.", "Las IIC y los fondos pesan.", "Sus IIC ganan.", "Los VIX altos asustan.",
                                   "Los I y los V no cuentan."])
def test_r02_h03_una_sigla_permitida_tras_un_determinante_no_es_una_cifra(perm, frase):
    from bloque_a import diseno_v6 as v6
    assert {"IIC", "VIX"} <= perm["codigos"]
    assert v6.frase_prohibida(frase, perm) is None, frase


@pytest.mark.parametrize("frase", ["Vemos las VII ideas.", "Pesan los III primeros.", "Sus IV opciones pesan.", "Estas XII pesan.", "Son unas XX ideas.",
                                   "Los XXXIX primeros ganan.", "Las IX mayores pesan."])
def test_r02_h03_los_romanos_como_cantidad_siguen_siendo_cifra(perm, frase):
    from bloque_a import diseno_v6 as v6
    assert v6.frase_prohibida(frase, perm) == "CIFRA", frase


def test_r02_h03_un_romano_que_es_sigla_permitida_no_es_cifra(perm):
    from bloque_a import diseno_v6 as v6
    frase = "Las IV altas pesan."
    assert v6.frase_prohibida(frase, perm) == "CIFRA"
    assert v6.frase_prohibida(frase, {**perm, "codigos": perm["codigos"] | {"IV"}}) is None


def test_r02_h07_sin_respuesta_valida_del_sintetizador_se_declara():
    from types import SimpleNamespace

    from bloque_a import diseno_v6 as v6
    bloque, perm0 = SimpleNamespace(redaccion=_Redaccion()), {"codigos": frozenset(), "series": frozenset()}
    paquete = {**_paquete(), "limitaciones": ["Ninguna limitación adicional a las declaradas por opción"]}
    red = v6._redaccion_segura(bloque, paquete, None, perm0)
    assert red == _Redaccion().textos_por_defecto(paquete)
    assert paquete["limitaciones"] == [v6._SIN_SINTESIS] and "no dio una respuesta válida" in v6._SIN_SINTESIS
    v6._redaccion_segura(bloque, paquete, None, perm0)
    assert paquete["limitaciones"] == [v6._SIN_SINTESIS]   # no se repite
    d = {"frases_30s": ["El mercado espera con calma.", "El dólar pesa."], "tarjetas": [], "motivos_llanos": {}, "glosario": [], "frase_historial": "Aún es pronto."}
    v6._redaccion_segura(bloque, paquete, d, perm0)   # una reescritura válida retira el aviso
    assert paquete["limitaciones"] == ["Ninguna limitación adicional a las declaradas por opción"]


def test_r02_h07_cero_o_cuatro_frases_por_el_ciclo_se_declaran(tmp_path, monkeypatch):
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque
    from conftest import AS_OF, DATOS, config_pruebas

    from bloque_a import diseno_v6 as v6
    from bloque_a import mock_respuestas as mr
    orig = mr._sintetizador

    def con_frases(cambio):
        def sintetizador(msg, ctx, rng):
            o = orig(msg, ctx, rng)
            return {**o, "frases_30s": cambio(o["frases_30s"])}
        return sintetizador
    for i, cambio in enumerate((lambda f: [], lambda f: [*f, "Tercera.", "Cuarta."], lambda f: f)):
        monkeypatch.setattr(mr, "_sintetizador", con_frases(cambio))
        b = Bloque(config_pruebas(diseno="v6", perfiles={"activos": ["RV", "DIV"]}), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO),
                   MockClient(), tmp_path / f"e{i}", tmp_path / f"n{i}")
        res = b.ciclo(AS_OF)
        assert res["estado"] == "COMPLETO"
        assert (v6._SIN_SINTESIS in res["paquete"]["limitaciones"]) == (i < 2), res["paquete"]["limitaciones"]


# ---------------------------------------------------------------------------------------------- H-09: los mutantes vivos de la r01
def _curva_escalonada(r0, tasas, cortes, dias, base=360.0):
    import math
    out = []
    for d in dias:
        lg, prev, r = 0.0, 0, r0
        for c, rk in zip(cortes, tasas):
            if c >= d:
                break
            lg += (c - prev) * math.log1p(r / base)
            prev, r = c, rk
        lg += (d - prev) * math.log1p(r / base)
        out.append(math.expm1(lg) * base / d)
    return out


def test_r02_h27_una_curva_escalonada_redondeada_con_su_precision_no_se_rechaza():
    """Oráculo en pequeño (mutante M24): sendas escalonadas conocidas, su curva exacta redondeada a 1 pb o 0,1 pb y la
    precisión declarada (medio último dígito). Ninguna se rechaza por «no se puede reproducir»; con la precisión sola como
    cota (antes de T-113) se rechazaban. Una curva lisa, que no es escalonada, se sigue rechazando."""
    import pandas as pd
    fn = servicio.IMPLEMENTADAS["MON-EXP-001"]["fn"]
    rng = np.random.default_rng(113)
    fecha = pd.Timestamp("2026-11-12")
    inc = 0.0025
    servidas, sin_reproducir, mas_que_la_precision = 0, [], 0
    for _ in range(120):
        n_reu = int(rng.integers(2, 6))
        cortes = sorted(int(x) for x in rng.choice(np.arange(15, 330), size=n_reu, replace=False))
        if min(np.diff([0, *cortes])) < 20:
            continue
        oficial, dif = 0.02 + float(rng.uniform(-0.01, 0.02)), 0.0008
        r0 = oficial - dif
        tasas = list(r0 + np.cumsum(rng.choice([-1, -0.5, 0, 0.3, 0.7, 1.0], size=n_reu) * inc))
        dias = sorted(set(cortes) | {int((a + b) / 2) for a, b in zip(cortes, [*cortes[1:], cortes[-1] + 40])} | {cortes[-1] + 40, 7}
                      | {int(x) for x in rng.integers(10, cortes[-1] + 40, size=3)})
        dec = int(rng.choice([4, 5]))
        prec = 0.5 * 10 ** (-dec)
        v = {"fecha": str(fecha.date()), "base_curva": 360, "tipo_oficial": oficial, "diferencial_estable": dif,
             "reuniones": [str((fecha + pd.Timedelta(days=c)).date()) for c in cortes],
             "curva": [{"dias": d, "tipo": round(t, dec)} for d, t in zip(dias, _curva_escalonada(r0, tasas, cortes, dias))],
             "precision_cotizacion": prec}
        try:
            r, _ = fn({"valores": v, "series": {}, "series_rol": {}}, {})
        except servicio.op.ErrorFicha as e:
            if "no se puede reproducir" in str(e):
                sin_reproducir.append(str(e)[:160])
            continue
        servidas += 1
        mas_que_la_precision += any(abs(n["tipo_senda"] - n["tipo_nodo"]) > prec for n in r["verificacion"]["nodos"])
    assert not sin_reproducir, sin_reproducir[:2]
    assert servidas >= 30
    assert mas_que_la_precision >= 5   # el oráculo ejercita la cota: hay curvas servidas con un nodo a más de la precisión sola
    for pend in (0.004, 0.008, 0.02):
        v = {"fecha": str(fecha.date()), "base_curva": 360, "tipo_oficial": 0.02, "diferencial_estable": 0.0008,
             "reuniones": [str((fecha + pd.Timedelta(days=c)).date()) for c in (35, 125, 215, 305)],
             "curva": [{"dias": d, "tipo": round(0.0192 + pend * (d / 365) ** 2, 4)} for d in (7, 30, 60, 90, 120, 150, 180, 240, 300, 365)],
             "precision_cotizacion": 0.00005}
        with pytest.raises(servicio.op.ErrorFicha, match="no se puede reproducir"):
            fn({"valores": v, "series": {}, "series_rol": {}}, {})


@pytest.mark.parametrize("ficha,cambio", [("IDX-REB-001", {"sesiones_estimacion": 0}), ("IDX-REB-001", {"sesiones_estimacion": -1}),
                                          ("IDX-REB-001", {"sesiones_estimacion": 2.5}), ("IDX-CONC-001", {"ventana_percentil_anios": 0}),
                                          ("IDX-CONC-001", {"ventana_percentil_anios": -1}), ("IDX-CONC-001", {"ventana_percentil_anios": 101})])
def test_r02_h24_sesiones_de_estimacion_y_ventana_del_percentil_con_dominio(ficha, cambio):
    """Los dos parámetros que citaba el origen y no tenían prueba (mutantes M22 y M23)."""
    v, params = _valores(ficha)
    clave = next(iter(cambio))
    with pytest.raises(servicio.op.ErrorFicha, match=f"parámetro {clave} = .* (fuera del rango admitido|no es entero)"):
        servicio.IMPLEMENTADAS[ficha]["fn"]({"valores": v, "series": {}, "series_rol": {}}, {**params, **cambio})


def test_r02_h24_los_parametros_de_dominio_en_su_borde_se_admiten():
    for ficha, dom in fichas_mon_idx.DOMINIOS.items():
        for clave, (tipo, lo, hi) in dom.items():
            if tipo == "entero":
                for borde in (lo, hi):
                    p = {**fichas_mon_idx.PARAMETROS_POR_DEFECTO[ficha], clave: borde}
                    if clave == "momentum_salto_meses":
                        p["momentum_retro_meses"] = max(borde + 1, p["momentum_retro_meses"])
                    elif clave == "momentum_retro_meses":
                        p["momentum_salto_meses"] = 0
                    fichas_mon_idx._dominio(ficha, p)   # no lanza
                    with pytest.raises(servicio.op.ErrorFicha):
                        fichas_mon_idx._dominio(ficha, {**p, clave: lo - 1})


_PRESUPUESTO_JUSTO = 3.0   # UC por tipo: el presupuesto justo de la QA r01 (`r01_09`), que cierra fases en varios tipos


def test_r02_h16_las_limitaciones_no_dependen_del_orden_de_los_cierres(tmp_path, monkeypatch):
    """Por `sintesis.construir` y con los cierres desordenados a propósito (mutante M11b): las limitaciones por presupuesto
    del paquete salen por tipo, fase y motivo."""
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
    from bloque_a.llm import MockClient
    from bloque_a.orquestacion import Bloque
    from conftest import AS_OF, DATOS, config_pruebas

    from bloque_a import sintesis
    orig = sintesis.construir
    vistos: list = []

    def desordenado(*a, **k):
        presupuesto = k.get("presupuesto", a[-1])
        presupuesto.cierres.sort(key=lambda c: (c["clase"], c["fase"], c["motivo"]), reverse=True)
        vistos.append([dict(c) for c in presupuesto.cierres])
        return orig(*a, **k)
    monkeypatch.setattr(sintesis, "construir", desordenado)
    tipos = ["RV", "RF", "DIV", "MP"]
    b = Bloque(config_pruebas(perfiles={"activos": tipos}), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
               tmp_path / "estado", tmp_path / "ent")
    res = b.ciclo(AS_OF, nivel_forzado="N2", presupuesto_override={c: _PRESUPUESTO_JUSTO for c in tipos})
    cierres = vistos[-1]
    assert len({c["clase"] for c in cierres}) >= 2, cierres   # hay cierres de más de un tipo, y llegan al revés
    esperadas = [f"Presupuesto agotado en {c['clase']} (fase {c['fase']}): {c['motivo']}; alcance reducido, controles intactos (R16)"
                 for c in sorted(cierres, key=lambda c: (c["clase"], c["fase"], c["motivo"]))]
    assert [x for x in res["paquete"]["limitaciones"] if x.startswith("Presupuesto agotado")] == esperadas


def test_r02_h15_la_uc_total_sale_de_los_tokens_sumados():
    """Sin hilos (el menor de H-09): dos llamadas cuya UC redondeada, sumada, no es la UC de sus tokens sumados."""
    from bloque_a.consumo import Contabilidad
    from bloque_a.llm import Uso
    c = Contabilidad(cargar_config())
    e = next(e for e in range(1, 100000) if round(2 * c.uc_de(Uso(entrada=e)), 4) != c.uc_de(Uso(entrada=2 * e)))
    for _ in range(2):
        c.registrar("RUN-1", "AG-03", "m", Uso(entrada=e))
    assert c.resumen("RUN-1")["uc_llm"] == c.uc_de(Uso(entrada=2 * e))


def test_r02_h49_la_clave_ajena_quitada_se_declara_y_h50_la_instruccion_pide_exactamente_dos():
    from types import SimpleNamespace

    from bloque_a import diseno_v6 as v6
    paquete = _paquete()
    d = {"frases_30s": ["El mercado espera con calma.", "El dólar pesa."], "tarjetas": [], "glosario": [], "frase_historial": "Aún es pronto.",
         "motivos_llanos": {"RF": "Preferimos esperar.", "ZETA": "No es un tipo.", "RV 2027": "Tampoco."}}
    v6._redaccion_segura(SimpleNamespace(redaccion=_Redaccion()), paquete, d, {"codigos": frozenset(), "series": frozenset()})
    assert paquete["limitaciones"] == ["Frases llanas del Sintetizador quitadas (FORMATO): 2; el resto de sus textos se conserva"]   # M38
    assert "exactamente dos frases" in v6.INSTR_SINTESIS and "la primera, con las cuentas, la escribe el código" not in v6.INSTR_SINTESIS   # M44
