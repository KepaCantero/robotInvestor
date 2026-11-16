"""T-150 · Hallazgos bajos de la QA r01 de T-149: dos datos protegidos pegados (H-01), el error de un ejecutor recortado
antes de limpiarlo (H-02), un `opp_id` con un correo en el resumen (H-04), copias truncadas en IDX-CONC-001 (H-05), dos
respuestas raras del BCE (H-06) y las observaciones de la QA (un `paquete_json` o un `--config-a` que no se leen, el
mensaje de un traslado a medias, un destino que es un enlace roto). Las pruebas de las dos limpiezas que mutó el revisor
(H-03) están en `test_t149.py`, uno de los ficheros que fija su script de mutantes. Sin red ni coste.

Los correos y claves de prueba van partidos en dos cadenas (gate de secretos) y son de dominios de ejemplo."""
import http.client
import importlib.util
import io
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest
from bloque_a.contratos import secretos_en_texto
from bloque_a.motor import fichas_mon_idx as fm
from bloque_a.motor import frontera_b as fb

from bloque_a import cadena_b

EJECUTOR = Path(__file__).resolve().parents[1]
SCRIPTS = EJECUTOR.parents[1] / ".docs" / "scripts"
EJEMPLO_A = EJECUTOR.parent / "06_Plantillas_entregables" / "Ejemplo - Paquete de oportunidades - V5.0.json"
OPP = "OPP-2026-9112"
CORREO = "inversor.prueba" + "@example.com"
CLAVE = "api" + "_key=ABCDEF1234567890"
IBAN = "ES91 2100 0418 " + "4502 0005 1332"
SK = "sk-" + "ant-api03-" + "Q" * 30 + "x9Z"
PWD = '"pass' + 'word": "Hunter2-Secreto"'
# cada dato con un trozo suyo que no puede quedar en el texto limpio
DATOS = {"correo": (CORREO, "inversor.prueba"), "clave": (CLAVE, "ABCDEF1234567890"), "iban": (IBAN, "0418 4502 0005 1332"),
         "sk": (SK, "Q" * 20), "password": (PWD, "Hunter2-Secreto")}
FECHAS = pd.bdate_range("2025-06-02", periods=320)
ANIOS = np.asarray((FECHAS - FECHAS[0]).days, dtype=float) / fm.DIAS_ANIO


def _modulo(nombre):
    spec = importlib.util.spec_from_file_location(nombre, SCRIPTS / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _limpio(texto, trozo):
    return not secretos_en_texto(texto) and not cadena_b.contiene_credenciales(texto) and trozo not in texto


# ---------------------------------------------------------------- H-01 · dos datos pegados
PARES = [(a, b) for a in DATOS for b in DATOS if a != b]


@pytest.mark.parametrize("primero, segundo", PARES)
def test_h01_dos_datos_pegados_no_dejan_rastro(primero, segundo):
    """Cada dato está también suelto en el texto, así que el detector lo ve; pegado al otro, la coincidencia que abarca
    los dos ya no se come el principio del segundo."""
    (d1, k1), (d2, k2) = DATOS[primero], DATOS[segundo]
    for texto in (f"{d1} {d2} y {d2}{d1}", f"{d1}{d2} · {d2} · {d1}", f"valor '{d1}{d2}' is not one of ['{d2}', '{d1}']",
                  f"{d2}\n{d1}{d2}{d1}\n{d1}"):
        r = cadena_b.sin_datos_protegidos(texto)
        assert _limpio(r, k1) and _limpio(r, k2), (texto[:40], r[:80])


def test_h01_lo_que_el_detector_no_ve_pegado_tampoco_se_quita():
    """Límite de INC-T123-01 (observación O-03 de la QA r01 de T-149), no de la sustitución: un IBAN pegado detrás de una
    clave «sk-…» no es un IBAN para el detector (empieza tras una letra) y lo que no ve no se quita."""
    texto = SK + IBAN
    assert not any("0418" in s for s in secretos_en_texto(texto))
    assert "0418 4502 0005 1332" in cadena_b.sin_datos_protegidos(texto)


def test_h01_el_correo_pegado_a_la_clave_era_el_caso_de_la_qa():
    """El detector da una coincidencia que abarca los dos («…@example.comapi»): antes, sustituida primero, dejaba
    ««dato protegido por R8»_key=» y el valor de la clave."""
    texto = f"x {CLAVE} y {CORREO}{CLAVE}"
    assert any(CORREO + "api" == s for s in secretos_en_texto(texto))
    r = cadena_b.sin_datos_protegidos(texto)
    assert r == f"x {cadena_b.DATO_PROTEGIDO} y {cadena_b.DATO_PROTEGIDO}"


def test_h01_tramos_que_se_solapan_o_se_tocan_se_unen_y_el_resto_queda():
    assert cadena_b._sin_tramos("abcdefgh", ["bcd", "cdef"]) == f"a{cadena_b.DATO_PROTEGIDO}gh"
    assert cadena_b._sin_tramos("abcdefgh", ["bc", "de"]) == f"a{cadena_b.DATO_PROTEGIDO}fgh"        # se tocan
    assert cadena_b._sin_tramos("ab-ab-ab", ["ab"]) == "-".join([cadena_b.DATO_PROTEGIDO] * 3)        # cada aparición
    assert cadena_b._sin_tramos("aaaa", ["aaa"]) == cadena_b.DATO_PROTEGIDO                            # solapadas
    assert cadena_b._sin_tramos("sin nada", ["otro", ""]) == "sin nada"


def test_h01_un_texto_corriente_no_cambia_y_lo_que_no_se_localiza_se_omite():
    assert cadena_b.sin_datos_protegidos("tipo_activo: 'RVX' is not one of ['RV']") == "tipo_activo: 'RVX' is not one of ['RV']"
    # el detector ve la tarjeta solo enmascarada: no tiene tramo y el texto entero cambia por el aviso (como en T-149)
    assert cadena_b.sin_datos_protegidos("valor '4111 1111 " + "1111 1111' no admitido") == cadena_b.DETALLE_OMITIDO


# ---------------------------------------------------------------- H-02 · el fallo de un ejecutor: limpiar y recortar
def _fallo_de(mod, monkeypatch, codigo, stdout="", stderr=""):
    monkeypatch.setattr(mod, "subprocess", SimpleNamespace(
        run=lambda *a, **k: SimpleNamespace(returncode=codigo, stdout=stdout, stderr=stderr)))
    with pytest.raises(mod.FalloEjecutor) as e:
        mod._cli("a", ["--estado", "x", "ciclo"])
    return str(e.value)


@pytest.mark.parametrize("nombre", list(DATOS))
def test_h02_el_stderr_se_limpia_antes_de_recortarlo(monkeypatch, nombre):
    mod = _modulo("cadena_a_b")
    dato, trozo = DATOS[nombre]
    for corte in range(2, len(dato) - 3):                 # el corte de 2000 cae dentro del dato
        stderr = "inicio " + dato + " " + "y" * (2000 - (len(dato) - corte) - 1)
        msg = _fallo_de(mod, monkeypatch, 3, stderr=stderr)
        assert "código 3" in msg and dato[corte:] not in msg and trozo[-8:] not in msg, (nombre, corte)


@pytest.mark.parametrize("nombre", ["correo", "clave", "iban"])
def test_h02_la_salida_que_no_es_json_se_limpia_antes_de_recortarla(monkeypatch, nombre):
    mod = _modulo("cadena_a_b")
    dato, trozo = DATOS[nombre]
    for corte in range(2, len(dato) - 3, 2):
        stdout = "no es JSON " + dato + " " + "y" * (1000 - (len(dato) - corte) - 1)
        msg = _fallo_de(mod, monkeypatch, 0, stdout=stdout)
        assert "no es JSON" in msg and dato[corte:] not in msg and trozo[-8:] not in msg, (nombre, corte)


# ---------------------------------------------------------------- H-04 y O-04 · el resumen y el paquete
@pytest.fixture()
def ejemplo():
    return json.loads(EJEMPLO_A.read_text(encoding="utf-8"))


def _extra(tmp_path, contenido=None):
    extra = tmp_path / "extra.yaml"
    extra.write_text(contenido if contenido is not None else
                     json.dumps({"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}}), encoding="utf-8")
    return extra


def _cli_ciclo(ruta_paquete, llamadas):
    def cli(bloque, args):
        llamadas.append((bloque, args[-1]))
        if bloque == "a" and args[-1] == "ciclo":
            return {"run_id": "RUN-X", "entrega": "ENTREGADA", "g3": "APTO", "entregables": {"paquete_json": str(ruta_paquete)}}
        raise AssertionError(f"no debería llamar a {bloque} {args[-3:]}")
    return cli


def test_h04_un_opp_id_con_un_correo_no_llega_al_resumen_ni_a_la_salida(tmp_path, ejemplo, monkeypatch, capsys):
    mod = _modulo("cadena_a_b")
    for o in (o for c in ejemplo["clases"].values() for o in c["opciones"]):
        if o["opp_id"] == OPP:
            o["opp_id"] = CORREO
    for e in ejemplo["paquete_para_bloque_B"]:
        if e["opp_id"] == OPP:
            e["opp_id"] = CORREO
    paquete = tmp_path / "paquete.json"
    paquete.write_text(json.dumps(ejemplo, ensure_ascii=False), encoding="utf-8")
    llamadas = []
    monkeypatch.setattr(mod, "_cli", _cli_ciclo(paquete, llamadas))
    w = tmp_path / "w"
    assert mod.main(["--trabajo", str(w), "--config-a", str(_extra(tmp_path))]) == 1
    salida = capsys.readouterr()
    resumen = (w / "resumen.json").read_text(encoding="utf-8")
    assert cadena_b.DATO_PROTEGIDO in json.loads(resumen)["opciones_enviables"]
    for texto in (resumen, salida.out, salida.err):
        assert "inversor.prueba" not in texto and not cadena_b.contiene_credenciales(texto)
    assert llamadas == [("a", "ciclo")] and not (w / "peticiones").exists()


def test_h04_el_resumen_entero_pasa_por_la_limpieza():
    mod = _modulo("cadena_a_b")
    r = mod._sin_datos({"a": [CORREO, 1, None, {CORREO: (IBAN, 2.5)}], "b": "sin nada"})
    assert r == {"a": [cadena_b.DATO_PROTEGIDO, 1, None, {cadena_b.DATO_PROTEGIDO: [cadena_b.DATO_PROTEGIDO, 2.5]}],
                 "b": "sin nada"}


@pytest.mark.parametrize("como", ["no existe", "no es JSON", "una lista", "un texto con un correo"])
def test_o04_un_paquete_que_no_se_lee_da_un_mensaje_y_1(tmp_path, monkeypatch, capsys, como):
    mod = _modulo("cadena_a_b")
    paquete = tmp_path / "paquete.json"
    if como == "no es JSON":
        paquete.write_text('{"clases": ' + CORREO, encoding="utf-8")
    elif como == "una lista":
        paquete.write_text("[1, 2]", encoding="utf-8")
    elif como == "un texto con un correo":
        paquete.write_text(json.dumps(CORREO), encoding="utf-8")
    llamadas = []
    monkeypatch.setattr(mod, "_cli", _cli_ciclo(paquete, llamadas))
    w = tmp_path / "w"
    assert mod.main(["--trabajo", str(w), "--config-a", str(_extra(tmp_path))]) == 1
    err = capsys.readouterr().err
    assert "no se lee" in err and "no se envía nada" in err and "Traceback" not in err and "inversor" not in err
    resumen = json.loads((w / "resumen.json").read_text(encoding="utf-8"))
    assert resumen["sin_envio"]["motivo"] == "PAQUETE_ILEGIBLE" and "inversor" not in json.dumps(resumen)
    assert llamadas == [("a", "ciclo")] and not (w / "peticiones").exists()


# ---------------------------------------------------------------- O-06 · un --config-a que no se lee
@pytest.mark.parametrize("como, contenido", [
    ("YAML roto con un correo", "cadena_b:\n  peticion: {nivel: " + CORREO + "\n  otra: [\n"),
    ("YAML roto con una clave", "cadena_b: [" + CLAVE + "\n  x: {\n"),
    ("una lista", "- " + CORREO + "\n- b\n"),
    ("cadena_b que no es un diccionario", "cadena_b: 3\n"),
    ("correspondencia que no es un diccionario", "cadena_b:\n  correspondencia_ambitos: [" + CORREO + "]\n"),
    ("no existe", None),
])
def test_o06_un_config_a_que_no_se_lee_da_un_mensaje_y_1(tmp_path, monkeypatch, capsys, como, contenido):
    mod = _modulo("cadena_a_b")
    monkeypatch.setattr(mod, "_cli", lambda *a: (_ for _ in ()).throw(AssertionError("no debería ejecutar nada")))
    ruta = tmp_path / "no_existe.yaml" if contenido is None else _extra(tmp_path, contenido)
    w = tmp_path / "w"
    assert mod.main(["--trabajo", str(w), "--config-a", str(ruta)]) == 1
    err = capsys.readouterr().err
    assert "--config-a no se puede leer" in err and "Traceback" not in err
    assert "inversor" not in err and "ABCDEF1234567890" not in err and not (w / "resumen.json").exists()


def test_o06_el_yaml_roto_da_la_posicion_y_no_la_linea(tmp_path, capsys):
    mod = _modulo("cadena_a_b")
    ruta = _extra(tmp_path, "a: 1\ncadena_b:\n  peticion: {nivel: " + CORREO + "\n  otra: [\n")
    assert mod.main(["--trabajo", str(tmp_path / "w"), "--config-a", str(ruta)]) == 1
    err = capsys.readouterr().err
    assert "en la línea" in err and "columna" in err and "peticion" not in err


# ---------------------------------------------------------------- H-05 · copias truncadas en IDX-CONC-001
def _paseo(semilla, nivel=50.0, sd=0.01):
    rng = np.random.default_rng(semilla)
    return nivel * np.exp(np.cumsum(rng.normal(0.0005, sd, len(FECHAS))))


def _juntas(x, y):
    g = fb._etiquetas_series_copiadas(np.vstack([x, y]), ANIOS, fb.FRONTERA_B["tolerancia_clon"], 1.0)
    return bool(g[0] == g[1])


def _trunc(x, q):
    return np.floor(x / q) * q


def _amplitud(x, y):
    series = {"C00": pd.Series(x, index=FECHAS), "SECRETA": pd.Series(y, index=FECHAS)}
    res, lim = fm.FICHAS["IDX-CONC-001"]["fn"]({"valores": {"composicion": fm._composicion(10, igual=False)}, "series": series,
                                                 "series_rol": {}}, {"top_n": 5})
    return res["amplitud"], lim


A = _paseo(7)                                           # 36,6 … 50,2: cambia bastante de precio (la vía de la QA)
SIG4 = _paseo(9, 99.0, 0.006)                           # alrededor de 100: 4 cifras significativas cambian de paso


def _sig_trunc(x, k):
    e = np.floor(np.log10(x)) - (k - 1)
    return np.floor(x / 10.0 ** e) * 10.0 ** e


@pytest.mark.parametrize("nombre, x, copia", [
    ("0,05 truncado (la vía de la QA)", A, _trunc(A, 0.05)),
    ("2 decimales truncados (la vía de la QA)", A, _trunc(A, 0.01)),
    ("0,25 truncado", A, _trunc(A, 0.25)),
    ("1/8 truncado", A, _trunc(A, 1 / 8)),
    ("0,05 truncado frente a la misma a 2 decimales", np.round(A, 2), _trunc(A, 0.05)),
    ("0,05 truncado frente a la misma truncada a 0,001", _trunc(A, 0.001), _trunc(A, 0.05)),
    ("0,05 truncado a otra escala (×1000)", A, _trunc(A * 1000, 50.0)),
    ("4 cifras significativas truncadas cruzando 100", SIG4, _sig_trunc(SIG4, 4)),
])
def test_h05_una_copia_truncada_es_una_copia(nombre, x, copia):
    assert _juntas(x, copia), nombre
    amp, lim = _amplitud(x, copia)
    assert amp is None and not any("SECRETA" in t or "C00" in t for t in lim), nombre


def test_h05_antes_no_se_agrupaba_y_solo_con_la_hipotesis_truncada():
    """La vía de la QA no cabe en la cota de medio paso centrada en el precio truncado: solo con la hipótesis truncada."""
    t = _trunc(A, 0.05)
    L = np.log(A) - np.log(t)
    b = -np.log1p(-0.05 / (2 * t)) + fb.FRONTERA_B["tolerancia_numerica_copias"]
    assert np.max(L - b) > np.min(L + b)                 # redondeada: no hay constante que quepa
    Lt = np.log(A) - np.log(t + 0.025)
    bt = -np.log1p(-0.025 / (t + 0.025)) + fb.FRONTERA_B["tolerancia_numerica_copias"]
    assert np.max(Lt - bt) <= np.min(Lt + bt)            # truncada: sí


@pytest.mark.parametrize("semilla, paso", [(9020, 0.25), (9031, 0.25), (9040, 0.25), (9031, 0.05), (9031, 1 / 8), (9000, 0.25)])
def test_h05_un_precio_con_paso_grande_no_quita_la_hipotesis_al_resto(semilla, paso):
    """El desplazamiento es por precio: una serie truncada que cruza 100 y pasa pocas sesiones en una de sus décadas,
    donde el paso de la década puede salir grueso (más del 1 % del precio), se sigue agrupando. Con la hipótesis por
    serie (ningún precio con paso grande), estas semillas no se agrupaban (3 de 200 a 0,25; la 9000, control)."""
    x = 100.0 * np.cumprod(1 + np.random.default_rng(semilla).normal(0.0003, 0.011, len(FECHAS)))
    assert _juntas(x, _trunc(x, paso))


@pytest.mark.parametrize("nivel, paso", [(100.0, 0.05), (100.0, 0.25), (12.0, 0.05), (100.0, 1 / 32), (2.0, 0.001)])
def test_h05_series_distintas_truncadas_no_son_copias(nivel, paso):
    juntas = 0
    for s in range(40):
        rng = np.random.default_rng(7000 + s)
        m = rng.normal(0.0003, 0.011, len(FECHAS))
        x = nivel * np.cumprod(1 + m)
        y = nivel * np.cumprod(1 + m + rng.normal(0, 0.0011, len(FECHAS)))
        rt = x * 1.02 ** ANIOS
        juntas += _juntas(np.round(x / paso) * paso, _trunc(y, paso)) + _juntas(_trunc(x, paso), _trunc(y, paso))
        juntas += _juntas(np.round(x / paso) * paso, _trunc(rt, paso))
    assert juntas == 0


def test_h05_un_paso_grande_frente_al_precio_no_se_desplaza():
    """Un monetario casi siempre a 1,00 (paso 1: q/p = 100 %) y otro distinto que crece un 1 %/año a 4 decimales: no son
    copias (con el desplazamiento también en los pasos grandes, 90 de 100 se agrupaban)."""
    juntas = 0
    for s in range(20):
        rng = np.random.default_rng(7000 + s)
        x = np.ones(len(FECHAS))
        x[rng.random(len(FECHAS)) < 0.08] = 1.01
        y = np.round(1.01 ** (np.arange(len(FECHAS)) / 252) * (1 + rng.normal(0, 0.0002, len(FECHAS))), 4)
        juntas += _juntas(x, y)
    assert juntas == 0


def test_h05_pares_por_hipotesis():
    con_paso = np.array([True, False, True])
    pares = [(i.tolist(), k.tolist()) for i, k in fb._pares_por_hipotesis(3, 100, con_paso)]
    # (r, r) todos; (t, r) solo con la primera con paso; (r, t) solo con la segunda con paso; (t, t) las dos
    assert pares == [([0, 0, 1], [1, 2, 2]), ([3, 3], [1, 2]), ([0, 1], [5, 5]), ([3], [5])]


@pytest.mark.parametrize("nombre, copia", [
    ("redondeada hacia arriba (⌈p/q⌉·q)", np.ceil(A / 0.05) * 0.05),
    ("tabla de paso por tramo de precio (0,01 bajo 40 y 0,05 encima, como MiFID II)",
     np.where(A < 40.0, np.round(A, 2), np.round(A / 0.05) * 0.05)),
])
def test_h05_limites_declarados_no_se_agrupan(nombre, copia):
    """Límites declarados en INC-T127-01 (rondas T-149 y T-150): si algún día se agrupan, hay que actualizar la incidencia."""
    assert not _juntas(A, copia), nombre


# ---------------------------------------------------------------- H-06 y O-05 · descarga del BCE
CAB = "KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE,OBS_STATUS\n"
VAL = {"USD": 1.1, "JPY": 170.0, "GBP": 0.85, "AUD": 1.7, "CHF": 0.93, "MXN": 20.5}


def _fila(m, d, v):
    return f"EXR.D.{m}.EUR.SP00.A,D,{m},EUR,SP00,A,{d},{v},A\n"


def _cuerpo(extra=""):
    return CAB + "".join(_fila(m, d, v) for d in ("2026-11-03", "2026-11-04") for m, v in VAL.items()) + extra


@pytest.fixture()
def bce():
    return _modulo("descargar_datos_bce")


def _con_respuesta(bce, monkeypatch, cuerpo=None, fallo=None):
    llamadas = []

    class R(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self, *a):
            if fallo is not None:
                raise fallo
            return super().read(*a)

    def falso(url, timeout=None):
        llamadas.append(url)
        return R((cuerpo or "").encode())
    monkeypatch.setattr(bce.urllib.request, "urlopen", falso)
    return llamadas


@pytest.mark.parametrize("fila", [_fila("USD", "", 1.2), _fila("JPY", "", "")])
def test_h06_una_fila_sin_fecha_da_un_mensaje_y_no_escribe_nada(bce, monkeypatch, tmp_path, capsys, fila):
    _con_respuesta(bce, monkeypatch, _cuerpo(extra=fila))
    destino = tmp_path / "datos"
    destino.mkdir()
    assert bce.main([str(destino)]) == 1
    err = capsys.readouterr().err
    assert "sin fecha" in err and "no se escribe nada" in err and "Traceback" not in err and not list(destino.iterdir())


@pytest.mark.parametrize("fallo", [http.client.IncompleteRead(b"KEY,FR"), http.client.BadStatusLine("x"),
                                   http.client.RemoteDisconnected("cerrada")])
def test_h06_una_lectura_cortada_da_un_mensaje_y_no_escribe_nada(bce, monkeypatch, tmp_path, capsys, fallo):
    _con_respuesta(bce, monkeypatch, fallo=fallo)
    destino = tmp_path / "datos"
    assert bce.main([str(destino)]) == 1
    err = capsys.readouterr().err
    assert type(fallo).__name__ in err and "no se escribe nada" in err and not destino.exists()


def test_o05_un_traslado_a_medias_dice_que_csv_quedaron(bce, monkeypatch, tmp_path, capsys):
    _con_respuesta(bce, monkeypatch, _cuerpo())
    destino = tmp_path / "datos"
    reales = bce.os.replace
    cuenta = {"n": 0}

    def replace(a, b):
        cuenta["n"] += 1
        if cuenta["n"] == 3:
            raise OSError(5, "Error de E/S")
        return reales(a, b)
    monkeypatch.setattr(bce.os, "replace", replace)
    assert bce.main([str(destino)]) == 1
    err = capsys.readouterr().err
    escritos = sorted(p.name for p in destino.iterdir())
    assert escritos == ["EURUSD=X.csv", "USDJPY=X.csv"]                     # sin la carpeta temporal
    assert "no se escribe nada" not in err and all(e in err for e in escritos) and "Repite la descarga" in err


def test_o05_el_primer_traslado_que_falla_sigue_diciendo_que_no_se_escribe_nada(bce, monkeypatch, tmp_path, capsys):
    _con_respuesta(bce, monkeypatch, _cuerpo())
    destino = tmp_path / "datos"

    def replace(a, b):
        raise OSError(5, "Error de E/S")
    monkeypatch.setattr(bce.os, "replace", replace)
    assert bce.main([str(destino)]) == 1
    assert "no se escribe nada" in capsys.readouterr().err and not list(destino.iterdir())


@pytest.mark.parametrize("donde", ["destino", "carpeta de la ruta"])
def test_o05_un_destino_que_es_un_enlace_roto_no_se_descarga(bce, monkeypatch, tmp_path, capsys, donde):
    llamadas = _con_respuesta(bce, monkeypatch, _cuerpo())
    roto = tmp_path / "enlace_roto"
    roto.symlink_to(tmp_path / "no_existe")
    destino = roto if donde == "destino" else roto / "sub"
    assert bce.main([str(destino)]) == 1
    err = capsys.readouterr().err
    assert "enlace simbólico roto" in err and not llamadas and not (tmp_path / "no_existe").exists()


def test_h06_una_respuesta_valida_sigue_escribiendo_los_seis(bce, monkeypatch, tmp_path):
    _con_respuesta(bce, monkeypatch, _cuerpo())
    destino = tmp_path / "datos"
    assert bce.main([str(destino)]) == 0
    assert sorted(p.name for p in destino.iterdir()) == sorted(f"{s}.csv" for s in bce.CRUCES)


# ================================================================ T-152 · hallazgos de la QA r01 de T-150
# Van en este fichero porque es el que ejecuta el script de mutantes del revisor (`T-150/revisores/r01_04_mutantes_qa.py`).
DATO = cadena_b.DATO_PROTEGIDO


def test_t152_h01_un_tramo_contenido_en_otro_no_acorta_la_union():
    """Mutante Y01: la unión de un tramo con otro que cabe dentro no se acorta al final del de dentro."""
    assert cadena_b._sin_tramos("abcdef", ["abcdef", "cd"]) == DATO
    assert cadena_b._sin_tramos("xabcdefy", ["abcdef", "bc"]) == f"x{DATO}y"
    assert cadena_b._sin_tramos("xabcdefy", ["bc", "abcdef", "de"]) == f"x{DATO}y"


def test_t152_h01_un_correo_dentro_de_una_contrasena_no_deja_su_cola():
    """El caso del revisor: el detector da la contraseña entera y, dentro, el correo; la cola de la contraseña
    («/ZZZZ1234567») no la ve la comprobación final si queda suelta."""
    texto = "password=x/" + CORREO + "/ZZZZ1234567"
    tramos = secretos_en_texto(texto)
    assert CORREO in tramos and any(t.endswith("ZZZZ1234567") and len(t) > len(CORREO) for t in tramos)
    r = cadena_b.sin_datos_protegidos(texto)
    assert "ZZZZ1234567" not in r and "inversor" not in r and "x/" not in r


def test_t152_h01_el_aviso_de_sin_entrega_se_limpia(tmp_path, monkeypatch, capsys):
    """Mutante Z03: el aviso «Sin entrega del Bloque A (entrega …, G3 …)» copia lo que dice el ciclo; se limpia."""
    mod = _modulo("cadena_a_b")
    llamadas = []

    def cli(bloque, args):
        llamadas.append((bloque, args[-1]))
        return {"run_id": "RUN-X", "entrega": f"NO_ENTREGADA {CORREO}", "g3": f"BLOQUEADO {CLAVE}", "entregables": {}}
    monkeypatch.setattr(mod, "_cli", cli)
    w = tmp_path / "w"
    assert mod.main(["--trabajo", str(w), "--config-a", str(_extra(tmp_path))]) == 1
    salida = capsys.readouterr()
    assert "Sin entrega del Bloque A" in salida.err and DATO in salida.err
    resumen = (w / "resumen.json").read_text(encoding="utf-8")
    assert json.loads(resumen)["sin_envio"]["motivo"] == "ENTREGA_BLOQUEADA_G3"
    for texto in (salida.out, salida.err, resumen):
        assert "inversor" not in texto and "ABCDEF1234567890" not in texto
    assert llamadas == [("a", "ciclo")] and not (w / "peticiones").exists()


@pytest.mark.parametrize("falla", [2, 3, 4, 6])
def test_t152_h01_el_traslado_a_medias_nombra_solo_los_escritos(bce, monkeypatch, tmp_path, capsys, falla):
    """Mutante W01: el mensaje nombra exactamente los CSV que quedaron escritos, no el que falló ni los que no se movieron."""
    _con_respuesta(bce, monkeypatch, _cuerpo())
    destino = tmp_path / "datos"
    reales = bce.os.replace
    cuenta = {"n": 0}

    def replace(a, b):
        cuenta["n"] += 1
        if cuenta["n"] == falla:
            raise OSError(5, "Error de E/S")
        return reales(a, b)
    monkeypatch.setattr(bce.os, "replace", replace)
    assert bce.main([str(destino)]) == 1
    err = capsys.readouterr().err
    escritos = {p.name for p in destino.iterdir()}
    assert escritos == {f"{s}.csv" for s in list(bce.CRUCES)[:falla - 1]}
    assert {f"{s}.csv" for s in bce.CRUCES if f"{s}.csv" in err} == escritos


def _en_tramo(lo, hi, semilla):
    """Un paseo aleatorio llevado al tramo [lo, hi]: el precio cambia sin salir de un tramo de q/p (ni de su década)."""
    u = np.cumsum(np.random.default_rng(semilla).normal(0, 0.03, len(FECHAS)))
    return lo + (hi - lo) * (u - u.min()) / (u.max() - u.min())


@pytest.mark.parametrize("lo, hi, agrupa", [(5.15, 5.45, True), (5.06, 5.45, True), (4.6, 4.9, False), (4.55, 4.95, False)])
def test_t152_h02_el_umbral_del_desplazamiento_esta_en_q_p_del_1_por_ciento(lo, hi, agrupa):
    """H-02: el umbral `[PROPUESTO]` de INC-T127-01 (ronda T-150): un precio se desplaza a la hipótesis truncada solo si
    su paso entero no pasa de `tolerancia_clon` (q/p ≤ 1 %). Con 0,05 entre 5,06 y 5,45 (q/p de 0,92 a 0,99 %), la
    copia truncada se agrupa; entre 4,55 y 4,95 (de 1,01 a 1,10 %), no (el límite declarado de los pasos grandes).
    Con el umbral al 2 % (mutante X01) se agruparía también la segunda; a la mitad, ninguna de las dos (medido en
    `.docs/tickets/T-152/medir_umbral.py`). Resolución medida: mata un umbral un 5 % más bajo o un 10 % más alto; más cerca
    del 1 %, con precios de tramo estrecho, la hipótesis redondeada ya agrupa o no según el camino, sea cual sea el
    umbral (`T-152/analisis-tecnico.md`). Si el operador cambia el umbral (T-57), esta prueba cambia con él."""
    assert fb.FRONTERA_B["tolerancia_clon"] == 0.01
    qp = 0.05 / np.array([hi, lo])
    assert ((qp <= 0.01).all() if agrupa else (qp > 0.01).all())
    juntas = [_juntas(x, _trunc(x, 0.05)) for x in (_en_tramo(lo, hi, s) for s in range(12))]
    assert juntas == [agrupa] * 12


def test_t152_o01_un_cambio_de_metodo_a_mitad_de_la_historia_no_se_agrupa():
    """Observación O-01: una copia redondeada a 0,05 la primera mitad y truncada después no se agrupa (cada par elige una
    hipótesis para toda la serie). Límite declarado en INC-T127-01 (ronda T-152): si algún día se agrupa, hay que
    actualizar la incidencia."""
    mitad = len(A) // 2
    copia = np.concatenate([np.round(A[:mitad] / 0.05) * 0.05, _trunc(A[mitad:], 0.05)])
    assert not _juntas(A, copia)
    assert _juntas(A, np.round(A / 0.05) * 0.05) and _juntas(A, _trunc(A, 0.05))    # cada mitad sola, sí


@pytest.mark.parametrize("como, contenido", [
    ("un símbolo con una lista", "cadena_b:\n  correspondencia_ambitos:\n    LETRAS-EUR-12M: [" + CORREO + "]\n"),
    ("un símbolo con un diccionario", "cadena_b:\n  correspondencia_ambitos:\n    LETRAS-EUR-12M: {" + CORREO + ": 1}\n"),
    ("un número y un texto", "cadena_b:\n  correspondencia_ambitos: {A: 1, B: " + CORREO + ", C: contenido-xyz}\n"),
    ("un símbolo que es un número", "cadena_b:\n  correspondencia_ambitos: {1: liquidez_eur}\n"),
])
def test_t152_o02_una_correspondencia_que_no_son_textos_da_un_mensaje_y_1(tmp_path, monkeypatch, capsys, como, contenido):
    """O-02: un `--config-a` que se lee pero no tiene la forma (antes, una traza de `TypeError` al ordenar)."""
    mod = _modulo("cadena_a_b")
    monkeypatch.setattr(mod, "_cli", lambda *a: (_ for _ in ()).throw(AssertionError("no debería ejecutar nada")))
    w = tmp_path / "w"
    assert mod.main(["--trabajo", str(w), "--config-a", str(_extra(tmp_path, contenido))]) == 1, como
    err = capsys.readouterr().err
    assert "--config-a no se puede leer" in err and "no son textos" in err and "Traceback" not in err
    assert "inversor" not in err and "contenido-xyz" not in err and not (w / "resumen.json").exists()


MARCA = "contenido-del-paquete-xyz"   # sin datos de R8: si sale en un mensaje, el mensaje copia el contenido


def _sin_forma(paquete, como):
    clases = paquete["clases"]
    primera = next(iter(clases.values()))
    if como == "clases es una lista":
        paquete["clases"] = list(clases.values()) + [MARCA]
    elif como == "una clase que es un texto":
        clases[next(iter(clases))] = f"{CORREO} {MARCA}"
    elif como == "opciones que no son una lista":
        primera["opciones"] = {CORREO: MARCA}
    elif como == "una opción sin opp_id":
        del primera["opciones"][0]["opp_id"]
        primera["opciones"][0]["nota"] = MARCA
    elif como == "un opp_id que no es un texto":
        primera["opciones"][0]["opp_id"] = [CORREO, MARCA]
    elif como == "paquete_para_bloque_B que no es una lista":
        paquete["paquete_para_bloque_B"] = {CORREO: MARCA}
    return paquete


@pytest.mark.parametrize("como", ["clases es una lista", "una clase que es un texto", "opciones que no son una lista",
                                  "una opción sin opp_id", "un opp_id que no es un texto",
                                  "paquete_para_bloque_B que no es una lista"])
def test_t152_o02_un_paquete_sin_la_forma_da_paquete_ilegible(tmp_path, ejemplo, monkeypatch, capsys, como):
    """O-02: un `paquete_json` que se lee pero no tiene la forma que se recorre (antes, `KeyError` o `AttributeError`)."""
    mod = _modulo("cadena_a_b")
    paquete = tmp_path / "paquete.json"
    paquete.write_text(json.dumps(_sin_forma(ejemplo, como), ensure_ascii=False), encoding="utf-8")
    llamadas = []
    monkeypatch.setattr(mod, "_cli", _cli_ciclo(paquete, llamadas))
    w = tmp_path / "w"
    assert mod.main(["--trabajo", str(w), "--config-a", str(_extra(tmp_path))]) == 1, como
    err = capsys.readouterr().err
    assert "no se lee" in err and "Traceback" not in err and "inversor" not in err and MARCA not in err
    resumen = json.loads((w / "resumen.json").read_text(encoding="utf-8"))
    assert resumen["sin_envio"]["motivo"] == "PAQUETE_ILEGIBLE"
    assert "inversor" not in json.dumps(resumen) and MARCA not in json.dumps(resumen)
    assert llamadas == [("a", "ciclo")] and not (w / "peticiones").exists()


def test_t152_o02_el_paquete_de_ejemplo_tiene_la_forma(ejemplo):
    _modulo("cadena_a_b")._forma_paquete(ejemplo)
