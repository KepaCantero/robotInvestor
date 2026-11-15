"""T-149 · Hallazgos de las QA r01 de T-144 y T-147: copias de una serie en rejillas que no son potencias de 10 y con un
precio suelto sin redondear (T-144 H-01), errores de la cadena B sin el dato que protege R8 (T-147 H-01), dos trazas de
la descarga del BCE (T-147 H-02) y la pregunta de la QA: sin entrega del Bloque A (G3 BLOQUEADO) no se encarga nada al
Bloque B. Los mutantes que vivían (T-144 H-02, T-147 H-03) se matan en `test_t144.py` y `test_t147.py`, los ficheros
que fija el script de mutantes del revisor. Sin red ni coste.

Los correos y claves de prueba van partidos en dos cadenas (gate de secretos) y son de dominios de ejemplo."""
import copy
import importlib.util
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from bloque_a.configuracion import cargar_config, fusionar
from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor import frontera_b as fb

from bloque_a import cadena_b

EJECUTOR = Path(__file__).resolve().parents[1]
SCRIPTS = EJECUTOR.parents[1] / ".docs" / "scripts"
EJEMPLO_A = EJECUTOR.parent / "06_Plantillas_entregables" / "Ejemplo - Paquete de oportunidades - V5.0.json"
OPP = "OPP-2026-9112"
CORREO = "inversor.prueba" + "@example.com"
AK = "api" + "_key"
FECHAS = pd.bdate_range("2025-06-02", periods=320)


def _modulo(nombre):
    spec = importlib.util.spec_from_file_location(nombre, SCRIPTS / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _paseo(semilla, nivel=50.0, sd=0.01):
    rng = np.random.default_rng(semilla)
    return pd.Series(nivel * np.exp(np.cumsum(rng.normal(0.0005, sd, len(FECHAS)))), index=FECHAS)


def _rejilla(s, paso):
    return (s / paso).round() * paso


def _es_copia(x, y):
    t = pd.DataFrame({"x": x, "y": y}).sort_index()
    g = fb._etiquetas_series_copiadas(t.to_numpy(dtype=float).T, np.asarray((t.index - t.index[0]).days, dtype=float) / fm.DIAS_ANIO,
                                      fb.FRONTERA_B["tolerancia_clon"], 1.0)
    return bool(g[0] == g[1])


def _amplitud(series):
    v = {"composicion": fm._composicion(10, igual=False)}
    res, lim = fm.FICHAS["IDX-CONC-001"]["fn"]({"valores": v, "series": series, "series_rol": {}}, {"top_n": 5})
    return res["amplitud"], lim


A = _paseo(7)


# ---------------------------------------------------------------- T-144 H-01 · otras rejillas y un precio suelto
@pytest.mark.parametrize("nombre, copia", [
    ("paso de 0,05", _rejilla(A, 0.05)), ("paso de 0,25", _rejilla(A, 0.25)), ("paso de 0,02", _rejilla(A, 0.02)),
    ("paso de 0,025", _rejilla(A, 0.025)), ("octavos", _rejilla(A, 1 / 8)), ("dieciseisavos", _rejilla(A, 1 / 16)),
    ("treintaidosavos del doble", _rejilla(A * 2, 1 / 32)), ("1/128 del triple", _rejilla(A * 3, 1 / 128)),
    ("paso de 5 a 100 veces", _rejilla(A * 100, 5.0)), ("paso de 50 a 1000 veces", _rejilla(A * 1000, 50.0)),
    ("dos decimales con un precio sin redondear", pd.concat([A.round(2).iloc[:-1], A.iloc[-1:]])),
    ("paso de 0,05 con tres precios sin redondear", _rejilla(A, 0.05).where(~A.index.isin(A.index[[5, 150, 300]]), A)),
    ("4 cifras significativas cruzando 100", (A * 2.3).apply(lambda v: float(f"{v:.4g}"))),
    ("0,05 y una sesión ausente", _rejilla(A, 0.05).drop(A.index[100])),
])
def test_h01_la_misma_serie_en_otra_rejilla_es_una_copia(nombre, copia):
    base = A * (copia.iloc[0] / A.iloc[0])            # la misma serie a la escala de la copia
    assert _es_copia(base, copia), nombre
    amp, lim = _amplitud({"C00": base, "SECRETA": copia})
    assert amp is None and not any("SECRETA" in x or "C00" in x for x in lim), nombre


def test_h01_paso_de_cada_rejilla():
    filas = [[50.05, 50.15, 50.35], [50.25, 50.75, 51.25], [50.125, 50.375, 51.625], [1 / 32, 3 / 32, 5 / 32],
             [10.02, 10.04, 10.08], [1250.0, 1350.0, 1450.0], [12.34, 12.35, 12.37]]
    x = np.array(filas)
    assert fb._paso_de_precio(x, ~np.isnan(x), 1e-10).tolist() == [0.05, 0.25, 0.125, 1 / 32, 0.02, 50.0, 0.01]


def test_h01_un_precio_suelto_no_hunde_el_paso_pero_una_minoria_grande_si():
    base = np.round(A.to_numpy(), 2)
    hay = np.ones((1, len(base)), dtype=bool)
    suelto = base.copy()
    suelto[-1] = A.iloc[-1]                                # 1 de 320 fuera de la rejilla
    assert fb._paso_de_precio(suelto[None, :], hay, 1e-10).tolist() == [0.01]
    k = int(np.ceil((1 - fb.REJILLAS_PRECIO["fraccion_en_rejilla"]) * len(base))) + 1
    muchos = base.copy()
    muchos[:k] = A.iloc[:k]                                # más de 1 − fraccion_en_rejilla fuera: ya no es una rejilla
    assert fb._paso_de_precio(muchos[None, :], hay, 1e-10)[0] < 1e-6


def test_h01_la_fraccion_en_rejilla_deja_fuera_la_rejilla_siguiente():
    """La mitad de los precios de una rejilla caen por azar en la siguiente más gruesa (los pares de 0,01 en 0,02): la
    fracción exigida tiene que estar bastante por encima, o una serie de 2 decimales tendría paso 0,02."""
    assert 0.5 < fb.REJILLAS_PRECIO["fraccion_en_rejilla"] < 1
    x = np.round(A.to_numpy(), 2)[None, :]
    assert fb._paso_de_precio(x, ~np.isnan(x), 1e-10).tolist() == [0.01]


def test_h01_paso_por_decada_en_cifras_significativas():
    x = np.array([[95.12, 99.87, 101.3, 104.9, 98.76, 100.0]])
    paso = fb._paso_por_decada(x, ~np.isnan(x), 1e-10)
    assert fb._paso_de_precio(x, ~np.isnan(x), 1e-10).tolist() == [0.01]   # la serie entera: el de la parte fina
    assert paso[0, [0, 1, 4]].tolist() == [0.01] * 3 and all(p >= 0.1 for p in paso[0, [2, 3, 5]])
    una = np.array([[12.34, 12.35, 12.37]])
    assert not fb._paso_por_decada(una, ~np.isnan(una), 1e-10).any()        # sin cruzar una década: el de la serie


@pytest.mark.parametrize("paso", [0.05, 0.25, 1 / 8, 1 / 32])
@pytest.mark.parametrize("nivel", [100.0, 12.0])
def test_h01_series_distintas_en_otras_rejillas_no_son_copias(paso, nivel):
    """Dos índices con ρ ≈ 0,995 y un índice y su rentabilidad total, en la misma rejilla: 0 de 100 (con el paso
    decimal, los mismos 0 de T-144; la cota se ensancha hasta el redondeo real de la rejilla y sigue distinguiéndolos)."""
    if paso / nivel > fb.FRONTERA_B["tolerancia_clon"] / 2:
        # 1/8 a 12 (un 1 %): la cota del par llega al tope de los casi clones y dos índices que se separan menos de un 1 %
        # en un año se toman por copias (1 de 300 semillas): límite declarado (falla cerrado), como 0,01 a 0,50 en T-144
        pytest.skip("paso del orden del 1 % del precio: límite declarado")
    juntas = 0
    for s in range(100):
        rng = np.random.default_rng(5000 + s)
        m = rng.normal(0.0003, 0.011, len(FECHAS))
        x = pd.Series(nivel * np.cumprod(1 + m), index=FECHAS)
        y = pd.Series(nivel * np.cumprod(1 + m + rng.normal(0, 0.0011, len(FECHAS))), index=FECHAS)
        rt = pd.Series(nivel * np.cumprod(1 + m + 0.02 / 252), index=FECHAS)
        juntas += _es_copia(_rejilla(x, paso), _rejilla(y, paso)) + _es_copia(_rejilla(x, paso), _rejilla(rt, paso))
    assert juntas == 0


@pytest.mark.parametrize("nombre, copia", [
    ("rejilla de 0,03 (fuera de REJILLAS_PRECIO)", _rejilla(A, 0.03)),
    ("2 decimales y después 1 en la misma década", pd.concat([A.round(2).iloc[:200], A.round(1).iloc[200:]])),
])
def test_h01_limites_declarados_no_se_agrupan(nombre, copia):
    """Límites declarados en INC-T128-01 (ronda T-149): si algún día se agrupan, hay que actualizar la incidencia."""
    assert not _es_copia(A, copia), nombre


# ---------------------------------------------------------------- T-147 H-01 · ningún error copia un dato de R8
@pytest.fixture()
def ejemplo():
    return json.loads(EJEMPLO_A.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def cfg():
    return fusionar(cargar_config(), {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}})


def _entrada(p):
    return next(e for e in p["paquete_para_bloque_B"] if e["opp_id"] == OPP)


def _opcion(p):
    return next(o for c in p["clases"].values() for o in c["opciones"] if o["opp_id"] == OPP)


def _error(p, c, **kw):
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(p, OPP, c, **kw)
    return e.value


def _sin(e, dato):
    texto = f"{e.codigo} {e.detalle} {e}"
    return dato not in texto and dato.split("@")[0].split("=")[-1] not in texto


DATOS = [CORREO, AK + "=ABCDEF1234567890", "ES91 2100 0418 " + "4502 0005 1332"]


@pytest.mark.parametrize("dato", DATOS)
@pytest.mark.parametrize("campo", ["tipo_activo", "tipo_opcion", "horizonte_principal", "relevancia_decisional", "pronosticos"])
def test_h01_un_campo_enumerado_con_el_dato_no_lo_reproduce(ejemplo, cfg, dato, campo):
    _entrada(ejemplo)[campo] = [dato] if campo == "pronosticos" else dato   # PRG- con patrón; los demás, enumerados
    e = _error(ejemplo, cfg)
    assert e.codigo == "ENTRADA_B_INVALIDA" and campo in e.detalle and _sin(e, dato)


@pytest.mark.parametrize("dato", DATOS)
def test_h01_tipos_secundarios_con_el_dato_no_lo_reproducen(ejemplo, cfg, dato):
    _opcion(ejemplo)["tipos_secundarios"] = ["RF", dato]
    e = _error(ejemplo, cfg)
    assert e.codigo == "ENTRADA_B_INVALIDA" and "tipos_secundarios" in e.detalle and _sin(e, dato)


@pytest.mark.parametrize("dato", DATOS)
@pytest.mark.parametrize("cambio", ["nivel", "prioridad", "perfil_invertibilidad", "idioma"])
def test_h01_la_configuracion_con_el_dato_no_lo_reproduce(ejemplo, cfg, dato, cambio):
    c = fusionar(cfg, {"idioma": dato} if cambio == "idioma" else {"cadena_b": {"peticion": {cambio: dato}}})
    for exigir in (True, False):
        e = _error(copy.deepcopy(ejemplo), c, exigir_correspondencia=exigir)
        assert e.codigo == "CONFIGURACION_CADENA_B" and _sin(e, dato)


def test_h01_el_simbolo_sin_correspondencia_con_el_dato_no_lo_reproduce(ejemplo, cfg):
    _entrada(ejemplo)["indicador_seguimiento"]["simbolo"] = CORREO
    e = _error(ejemplo, cfg)
    assert e.codigo == "SIN_CORRESPONDENCIA_AMBITO" and _sin(e, CORREO)


def test_h01_sin_datos_protegidos():
    assert cadena_b.sin_datos_protegidos("tipo_activo: 'RVX' is not one of ['RV']") == "tipo_activo: 'RVX' is not one of ['RV']"
    t = cadena_b.sin_datos_protegidos(f"a: '{CORREO}' is not one of ['RV']")
    assert t == f"a: '{cadena_b.DATO_PROTEGIDO}' is not one of ['RV']"
    escapado = json.dumps({"nota": f"linea\n{'pass' + 'word'}=hunter2x"})          # tras un salto escapado de JSON
    assert "hunter2x" not in cadena_b.sin_datos_protegidos(escapado)
    # un dato que el detector no da por su texto (la tarjeta, enmascarada) no se puede quitar: el aviso entero
    assert cadena_b.sin_datos_protegidos("valor '4111 1111 " + "1111 1111' no admitido") == cadena_b.DETALLE_OMITIDO
    for d in DATOS:
        assert not cadena_b.contiene_credenciales(cadena_b.ErrorCadenaB("X", f"valor {d!r}").detalle)


def test_h01_el_script_no_escribe_ni_imprime_el_dato_de_la_configuracion(tmp_path, ejemplo, monkeypatch, capsys):
    mod = _modulo("cadena_a_b")
    paquete = tmp_path / "paquete.json"
    paquete.write_text(json.dumps(ejemplo, ensure_ascii=False), encoding="utf-8")

    def cli(bloque, args):
        if bloque == "a" and args[-1] == "ciclo":
            return {"run_id": ejemplo["run_id"], "entrega": "ENTREGADA", "g3": "APTO", "entregables": {"paquete_json": str(paquete)}}
        raise AssertionError(f"no debería llamar a {bloque} {args[-3:]}")
    monkeypatch.setattr(mod, "_cli", cli)
    extra = tmp_path / "extra.yaml"
    extra.write_text(json.dumps({"cadena_b": {"peticion": {"nivel": CORREO},
                                              "correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}}), encoding="utf-8")
    w = tmp_path / "w"
    assert mod.main(["--trabajo", str(w), "--config-a", str(extra)]) == 1
    salida = capsys.readouterr()
    resumen = (w / "resumen.json").read_text(encoding="utf-8")
    assert "CONFIGURACION_CADENA_B" in resumen
    for texto in (resumen, salida.out, salida.err):
        assert CORREO not in texto and "inversor.prueba" not in texto


def test_h01_el_script_no_imprime_un_dato_de_la_correspondencia(tmp_path, capsys):
    mod = _modulo("cadena_a_b")
    extra = tmp_path / "extra.yaml"
    extra.write_text(json.dumps({"cadena_b": {"correspondencia_ambitos": {"AUDUSD=X": CORREO}}}), encoding="utf-8")
    assert mod.main(["--trabajo", str(tmp_path / "w"), "--config-a", str(extra)]) == 2
    err = capsys.readouterr().err
    assert "no tiene" in err and CORREO not in err and "inversor.prueba" not in err


# ---------------------------------------------------------------- T-150 (QA r01 de T-149, H-03) · las dos limpiezas
# En este fichero porque es uno de los que fija el script de mutantes del revisor (`T-149/revisores/r01_02_mutantes_qa.py`):
# N21 recortaba el mensaje de `jsonschema` a 200 antes de limpiarlo y N27 imprimía el fallo de un ejecutor sin limpiar.
def test_t150_el_mensaje_de_jsonschema_se_limpia_antes_de_recortarlo(ejemplo, cfg):
    """El correo junto al carácter 200 del mensaje («tipo_activo: 'ZZ… <correo>' is not one of …»): recortado antes, su
    dominio o su parte local quedan cortados, el detector ya no lo ve y su principio llega al detalle."""
    for relleno in range(150, 200):
        p = copy.deepcopy(ejemplo)
        _entrada(p)["tipo_activo"] = "Z" * relleno + " " + CORREO
        e = _error(p, cfg)
        assert e.codigo == "ENTRADA_B_INVALIDA" and "tipo_activo" in e.detalle, relleno
        assert "inversor" not in str(e) and "@example" not in str(e) and not cadena_b.contiene_credenciales(str(e)), relleno


def test_t150_el_script_limpia_el_fallo_de_un_ejecutor_que_imprime(tmp_path, monkeypatch, capsys):
    mod = _modulo("cadena_a_b")

    def cli(bloque, args):
        raise mod.FalloEjecutor(f"bloque A ciclo: código 3\nTraceback …\nValueError: {CORREO} {AK}=ABCDEF1234567890")
    monkeypatch.setattr(mod, "_cli", cli)
    extra = tmp_path / "extra.yaml"
    extra.write_text(json.dumps({"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}}), encoding="utf-8")
    assert mod.main(["--trabajo", str(tmp_path / "w"), "--config-a", str(extra)]) == 2
    err = capsys.readouterr().err
    assert "código 3" in err and cadena_b.DATO_PROTEGIDO in err
    assert "inversor.prueba" not in err and "ABCDEF1234567890" not in err


# ---------------------------------------------------------------- T-147 H-02 · descarga del BCE sin trazas
CAB = "KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE,OBS_STATUS\n"
VAL = {"USD": 1.1, "JPY": 170.0, "GBP": 0.85, "AUD": 1.7, "CHF": 0.93, "MXN": 20.5}


def _fila(m, d, v):
    return f"EXR.D.{m}.EUR.SP00.A,D,{m},EUR,SP00,A,{d},{v},A\n"


def _cuerpo(extra=""):
    return CAB + "".join(_fila(m, d, v) for d in ("2026-11-03", "2026-11-04") for m, v in VAL.items()) + extra


@pytest.fixture()
def bce():
    return _modulo("descargar_datos_bce")


def _con_respuesta(bce, monkeypatch, cuerpo):
    llamadas = []

    class R(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def falso(url, timeout=None):
        llamadas.append(url)
        return R(cuerpo.encode())
    monkeypatch.setattr(bce.urllib.request, "urlopen", falso)
    return llamadas


@pytest.mark.parametrize("repetida", ["2026-11-3", "2026-11-04"])
def test_h02_fecha_repetida_escrita_de_otra_forma(bce, monkeypatch, tmp_path, capsys, repetida):
    _con_respuesta(bce, monkeypatch, _cuerpo(extra=_fila("USD", repetida, 9.99)))
    destino = tmp_path / "datos"
    destino.mkdir()
    assert bce.main([str(destino)]) == 1
    err = capsys.readouterr().err
    assert not list(destino.iterdir()) and "fecha repetida" in err and "Traceback" not in err


def test_h02_una_fecha_sin_ceros_sola_es_valida(bce, monkeypatch, tmp_path):
    _con_respuesta(bce, monkeypatch, _cuerpo().replace("2026-11-03", "2026-11-3"))
    assert bce.main([str(tmp_path / "d")]) == 0
    assert (tmp_path / "d" / "EURUSD=X.csv").read_text(encoding="utf-8").splitlines()[1].startswith("2026-11-03,")


@pytest.mark.parametrize("como", ["fichero", "dentro de un fichero"])
def test_h02_destino_que_no_es_una_carpeta(bce, monkeypatch, tmp_path, capsys, como):
    llamadas = _con_respuesta(bce, monkeypatch, _cuerpo())
    f = tmp_path / "f.txt"
    f.write_text("no tocar", encoding="utf-8")
    destino = f if como == "fichero" else f / "sub"
    assert bce.main([str(destino)]) == 1
    err = capsys.readouterr().err
    assert "no es una carpeta" in err and "no se escribe nada" in err and not llamadas   # ni siquiera descarga
    assert f.read_text(encoding="utf-8") == "no tocar" and sorted(p.name for p in tmp_path.iterdir()) == ["f.txt"]


def test_h02_un_csv_de_destino_que_es_una_carpeta(bce, monkeypatch, tmp_path, capsys):
    _con_respuesta(bce, monkeypatch, _cuerpo())
    destino = tmp_path / "datos"
    (destino / "USDJPY=X.csv").mkdir(parents=True)
    assert bce.main([str(destino)]) == 1
    assert sorted(p.name for p in destino.iterdir()) == ["USDJPY=X.csv"] and "no se escribe nada" in capsys.readouterr().err


def test_h02_un_fallo_al_escribir_da_un_mensaje_y_no_deja_nada(bce, monkeypatch, tmp_path, capsys):
    _con_respuesta(bce, monkeypatch, _cuerpo())
    destino = tmp_path / "datos"

    def sin_espacio(*a, **k):
        raise OSError(28, "No queda espacio en el dispositivo")
    monkeypatch.setattr(pd.DataFrame, "to_csv", sin_espacio)
    assert bce.main([str(destino)]) == 1
    assert "no se escribe nada" in capsys.readouterr().err and not list(destino.iterdir())   # sin la carpeta temporal


# ---------------------------------------------------------------- pregunta de la QA · G3 BLOQUEADO no encarga nada
@pytest.mark.parametrize("estado", [None, "BLOQUEADO", "SIN_RESULTADO", "apto"])
def test_g3_un_paquete_sin_entrega_no_se_encarga(ejemplo, cfg, estado):
    if estado is None:
        ejemplo.pop("estado_g3", None)
    else:
        ejemplo["estado_g3"] = estado
    for exigir in (True, False):
        e = _error(copy.deepcopy(ejemplo), cfg, exigir_correspondencia=exigir)
        assert e.codigo == "ENTREGA_BLOQUEADA_G3"


@pytest.mark.parametrize("estado", ["APTO", "APTO_CON_ADVERTENCIAS"])
def test_g3_un_paquete_entregado_si(ejemplo, cfg, estado):
    ejemplo["estado_g3"] = estado
    assert cadena_b.construir_peticion(ejemplo, OPP, cfg)["pet_ref_broker"].endswith(OPP)


def test_g3_los_estados_son_los_de_la_entrega_ct02():
    """Los mismos que exige el retorno CT-02 en `contratos.py` («se requiere una entrega G3 aprobada») y que admite
    `estado_g3` en el esquema del paquete."""
    texto = (EJECUTOR / "bloque_a" / "contratos.py").read_text(encoding="utf-8")
    assert cadena_b.ESTADOS_G3_ENTREGA == ("APTO", "APTO_CON_ADVERTENCIAS")
    assert 'msg.get("estado_g3") not in ("APTO", "APTO_CON_ADVERTENCIAS")' in texto
    esquema = json.loads((EJECUTOR.parent / "06_Plantillas_entregables" / "Esquema JSON - Paquete de oportunidades - V5.0.json")
                         .read_text(encoding="utf-8"))
    assert tuple(esquema["properties"]["estado_g3"]["enum"]) == cadena_b.ESTADOS_G3_ENTREGA


@pytest.mark.parametrize("ciclo", [
    {"entrega": "BLOQUEADA", "g3": "BLOQUEADO", "entregables": None},                       # G3 de F6
    {"entrega": "BLOQUEADA", "g3": "BLOQUEADO", "entregables": {"paquete_json": "PAQUETE"}},   # G3 de los entregables
    {"entrega": "SIN_RESULTADO", "g3": "SIN_RESULTADO", "entregables": None},
])
def test_g3_el_script_no_envia_nada_sin_entrega(tmp_path, ejemplo, monkeypatch, capsys, ciclo):
    mod = _modulo("cadena_a_b")
    ejemplo.pop("estado_g3", None)                     # el paquete bloqueado no lleva estado G3 (redaccion.py, T-65)
    paquete = tmp_path / "paquete.json"
    paquete.write_text(json.dumps(ejemplo, ensure_ascii=False), encoding="utf-8")
    if ciclo["entregables"]:
        ciclo = {**ciclo, "entregables": {"paquete_json": str(paquete)}}
    llamadas = []

    def cli(bloque, args):
        llamadas.append((bloque, args[-1]))
        if bloque == "a" and args[-1] == "ciclo":
            return {"run_id": ejemplo["run_id"], **ciclo}
        raise AssertionError(f"no debería llamar a {bloque} {args[-3:]}")
    monkeypatch.setattr(mod, "_cli", cli)
    extra = tmp_path / "extra.yaml"
    extra.write_text(json.dumps({"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}}), encoding="utf-8")
    w = tmp_path / "w"
    assert mod.main(["--trabajo", str(w), "--config-a", str(extra)]) == 1
    resumen = json.loads((w / "resumen.json").read_text(encoding="utf-8"))
    assert resumen["sin_envio"]["motivo"] == "ENTREGA_BLOQUEADA_G3" and not resumen["envios"]
    assert llamadas == [("a", "ciclo")] and not (w / "peticiones").exists() and not (w / "ct04").exists()
    assert "no se envía nada" in capsys.readouterr().err
