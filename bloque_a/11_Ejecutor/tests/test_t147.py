"""T-147 · Hallazgos de las QA r01 de T-142 y T-141: R8 en la petición del Broker al Bloque B y en el detector de A
(correos y asignaciones de una clave, T-142 H-02), validación de `tipos_secundarios` (H-01) y de `cadena_b.peticion`
contra el Anexo B.1 del Bloque B (H-03), la sonda sin clave (H-04), `--clases` de la comprobación de datos (T-141 H-01) y
las respuestas raras del BCE (T-141 H-02 y H-03). Sin red ni coste.

Las direcciones de correo de prueba van partidas en dos cadenas (gate de secretos) y son de dominios de ejemplo."""
import copy
import importlib.util
import io
import json
import re
import unicodedata
import urllib.error
from pathlib import Path

import pytest
import yaml
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config, fusionar
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient, contenido_sensible
from bloque_a.orquestacion import Bloque
from conftest import DATOS, config_pruebas

from bloque_a import cadena_b, contratos, llm

EJECUTOR = Path(__file__).resolve().parents[1]
REPO = EJECUTOR.parents[1]
SCRIPTS = REPO / ".docs" / "scripts"
EJEMPLO_A = EJECUTOR.parent / "06_Plantillas_entregables" / "Ejemplo - Paquete de oportunidades - V5.0.json"
OPP = "OPP-2026-9112"                                     # opción MON del ejemplo publicado (ENVIAR_A_BLOQUE_B)
CORREO = "inversor.prueba" + "@example.com"               # partido para el gate de secretos
CORREO_2 = "contacto+ir" + "@empresa-ejemplo.org"
IBAN = "ES91 2100 0418 " + "4502 0005 1332"               # el de ejemplo de las normas, partido
PW, AK = "pass" + "word", "api" + "_key"                   # nombres de credencial partidos (detect-secrets del pre-commit)


def _modulo(nombre):
    spec = importlib.util.spec_from_file_location(nombre, SCRIPTS / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def cfg():
    return fusionar(cargar_config(), {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez_eur"}}})


@pytest.fixture()
def ejemplo():
    return json.loads(EJEMPLO_A.read_text(encoding="utf-8"))


def _entrada(p):
    return next(e for e in p["paquete_para_bloque_B"] if e["opp_id"] == OPP)


def _opcion(p):
    return next(o for c in p["clases"].values() for o in c["opciones"] if o["opp_id"] == OPP)


def _codigo(p, c, **kw):
    try:
        cadena_b.construir_peticion(p, OPP, c, **kw)
    except cadena_b.ErrorCadenaB as e:
        return e
    return None


# ---------------------------------------------------------------- T-142 H-02 · R8 en el detector de A
@pytest.mark.parametrize("texto", [
    f"Contacto: {CORREO}", f"<{CORREO_2}>", f"correo:{CORREO}.", "mailto:" + CORREO,
    AK + "=ABCDEF1234567890", "API-KEY: zz12zz12zz", "X-Api-Key: zzzzzz12", "export SECRET_KEY=abc123def",
    f"'{PW}': 'hunter2'", PW + "=hunter2", "contraseña: Verano2026!", "client_" + "secret = s3cr3t-valor",
    "access_token: abcdefghijklmnopqrstuv", "token: abcdefgh12345678xyz", "secret=Zx9" + "Qw8Er7Ty6Ui5Op4",
])
def test_h02_r8_detecta_correos_y_asignaciones_de_clave(texto):
    assert contratos.secretos_en_texto(texto)
    assert contenido_sensible(texto) and contenido_sensible({"tesis": f"La tesis. {texto}"})
    assert contratos.contiene_credenciales({"a": [texto]})


@pytest.mark.parametrize("texto", [
    "logo@2x.png", "icono@3x.webp", "@usuario en la red social", "precio 1.2@3.4", "a@b", "correo electrónico del BCE",
    "token: Uniswap", "token: ETH", "token: 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", "contraseña: obligatoria",
    PW + ": requerida", "tokens_entrada: 12345678901234567", "clave: el tipo de cambio", "secret: sauce",
    AK + ": <tu clave>", f'"{AK}": null', "key: valor", "Token de gobernanza: UNI (Uniswap)",
    "token=abcdefghijklmnopqrstuvwxyz",   # genérico sin cifras: texto, no una clave
])
def test_h02_r8_falsos_positivos_de_las_formas_nuevas(texto):
    assert not contratos.secretos_en_texto(texto), contratos.secretos_en_texto(texto)


def test_h02_el_correo_se_detecta_aunque_lleve_escapes_de_json():
    assert contenido_sensible(json.dumps({"t": f"línea\n{CORREO}"}))
    assert contenido_sensible(f"\\n{CORREO}")


# ---------------------------------------------------------------- T-142 H-02 · el Broker no envía la petición
@pytest.mark.parametrize("dato", [CORREO, AK + "=ABCDEF1234567890", "token: abcdefgh12345678xyz", IBAN])
@pytest.mark.parametrize("campo", ["tesis", "mecanismo", "x_nota_libre"])
def test_h02_la_peticion_con_datos_protegidos_falla_cerrado(ejemplo, cfg, dato, campo):
    _entrada(ejemplo)[campo] = f"Texto del ámbito monetario. {dato}"
    for exigir in (True, False):
        e = _codigo(copy.deepcopy(ejemplo), cfg, exigir_correspondencia=exigir)
        assert e is not None and e.codigo == "DATOS_PROTEGIDOS"
        assert dato not in str(e) and dato[:6] not in e.detalle             # no reproduce el dato
        assert "paquete_para_bloque_B" in e.detalle                          # nombra el campo


def test_h02_la_peticion_limpia_se_sigue_construyendo(ejemplo, cfg):
    pet = cadena_b.construir_peticion(ejemplo, OPP, cfg)
    assert not contratos.contiene_credenciales(pet)


def test_h02_el_script_no_escribe_ni_devuelve_ct04_de_una_peticion_con_datos_protegidos(tmp_path, ejemplo, monkeypatch):
    """`cadena_a_b.py` con un ciclo simulado de mentira (el ejemplo publicado con un correo en la tesis): la opción queda
    en `no_enviadas` con DATOS_PROTEGIDOS, no se escribe la petición, no se llama al Bloque B ni sale CT-04."""
    mod = _modulo("cadena_a_b")
    _entrada(ejemplo)["tesis"] = f"La tesis. {CORREO}"
    paquete = tmp_path / "paquete.json"
    paquete.write_text(json.dumps(ejemplo, ensure_ascii=False), encoding="utf-8")
    llamadas = []

    def cli(bloque, args):
        llamadas.append((bloque, args[-1]))
        if bloque == "a" and args[-1] == "ciclo":
            return {"run_id": ejemplo["run_id"], "entregables": {"paquete_json": str(paquete)}}
        raise AssertionError(f"no debería llamar a {bloque} {args[-3:]}")
    monkeypatch.setattr(mod, "_cli", cli)
    extra = tmp_path / "extra.yaml"
    extra.write_text(yaml.safe_dump({"cadena_b": {"correspondencia_ambitos": {
        "LETRAS-EUR-12M": "liquidez_eur", "AUDUSD=X": "divisas_materias_primas"}}}), encoding="utf-8")
    w = tmp_path / "w"
    assert mod.main(["--trabajo", str(w), "--config-a", str(extra)]) == 1      # ninguna entrega
    resumen = json.loads((w / "resumen.json").read_text(encoding="utf-8"))
    malas = [n for n in resumen["no_enviadas"] if n["opp_id"] == OPP]
    assert malas and malas[0]["codigo"] == "DATOS_PROTEGIDOS" and CORREO not in json.dumps(resumen)
    assert not (w / "peticiones" / f"{OPP}.json").exists() and not (w / "ct04").exists()
    assert all(b == "a" for b, _ in llamadas) and not resumen["envios"]


# ---------------------------------------------------------------- T-142 H-02 · falsos positivos en el ciclo y los goldens
@pytest.fixture(scope="module")
def textos_del_ciclo(tmp_path_factory):
    """Todo lo que R8 mira en un ciclo C1 simulado con los doce tipos (mensajes, prompts de sistema, encargos y respuestas):
    se registran los hallazgos de las formas nuevas (correos y asignaciones de clave)."""
    hallados, vistos = [], [0]
    orig = contratos.secretos_en_texto

    def espia(texto):
        t = bytes(texto).decode("utf-8", errors="replace") if isinstance(texto, (bytes, bytearray)) else texto
        vistos[0] += 1
        hallados.extend([m.group(0) for m in contratos.RE_CORREO.finditer(t)] + contratos._asignaciones_de_clave(t))
        return orig(texto)
    for mod in (contratos, llm):
        mod.secretos_en_texto = espia
    try:
        tmp = tmp_path_factory.mktemp("t147c")
        b = Bloque(config_pruebas(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
                   tmp / "estado", tmp / "ent")
        r = b.ciclo("2024-03-29")
    finally:
        for mod in (contratos, llm):
            mod.secretos_en_texto = orig
    return hallados, vistos[0], b, r, tmp


def test_h02_ni_un_falso_positivo_en_el_ciclo_simulado_de_los_doce_tipos(textos_del_ciclo):
    hallados, vistos, b, r, tmp = textos_del_ciclo
    assert vistos > 1000 and hallados == []
    assert r["estado"] == "COMPLETO"
    bloqueos = [e for f in ("F5", "HA") for e in b.almacen.leer(f) if "R8" in json.dumps(e, ensure_ascii=False)]
    assert bloqueos == []
    for f in tmp.rglob("*"):                                         # estado y entregables escritos
        if f.is_file() and f.suffix in (".json", ".jsonl", ".md", ".html", ".csv", ".txt"):
            t = f.read_text(encoding="utf-8", errors="replace")
            assert not contratos.RE_CORREO.search(t) and not contratos._asignaciones_de_clave(t), f


def test_h02_ni_un_falso_positivo_en_los_prompts_ni_en_los_goldens():
    carpetas = [EJECUTOR.parent / "02_System_prompts", EJECUTOR / "tests" / "goldens", EJECUTOR.parent / "06_Plantillas_entregables"]
    vistos = 0
    for c in carpetas:
        for f in c.rglob("*"):
            if f.is_file() and f.suffix in (".md", ".json", ".html"):
                t = f.read_text(encoding="utf-8", errors="replace")
                vistos += 1
                assert not contratos.RE_CORREO.search(t) and not contratos._asignaciones_de_clave(t), f
    assert vistos > 30


# ---------------------------------------------------------------- T-142 H-01 · tipos_secundarios
@pytest.mark.parametrize("tipos", ["RF", ["XYZ"], ["RF", "RF"], [None], ["rf"], {"RF": 1}, [["RF"]]])
def test_h01_tipos_secundarios_que_no_cumplen_el_esquema_no_se_envian(ejemplo, cfg, tipos):
    _opcion(ejemplo)["tipos_secundarios"] = tipos
    e = _codigo(ejemplo, cfg)
    assert e is not None and e.codigo == "ENTRADA_B_INVALIDA" and "tipos_secundarios" in e.detalle


@pytest.mark.parametrize("tipos, esperado", [(["RF"], ["MON", "RF"]), ([], ["MON"]), (["MON", "FON"], ["MON", "FON"]),
                                             (None, ["MON"])])
def test_h01_tipos_secundarios_validos(ejemplo, cfg, tipos, esperado):
    if tipos is None:
        _opcion(ejemplo).pop("tipos_secundarios", None)
    else:
        _opcion(ejemplo)["tipos_secundarios"] = tipos
    assert cadena_b.construir_peticion(ejemplo, OPP, cfg)["tipos_activo_admitidos"] == esperado


# ---------------------------------------------------------------- T-142 H-03 · cadena_b.peticion contra B.1
def _b1():
    d = REPO / "bloque_b" / "01_Gobernanza"
    [f] = [p for p in d.iterdir() if unicodedata.normalize("NFC", p.name).startswith("Documento 0") and p.suffix == ".md"]
    texto = f.read_text(encoding="utf-8")
    return json.loads(re.search(r"```json\n(.*?)```", texto[texto.index("### B.1 CT-B-01"):], re.DOTALL).group(1))


def test_h03_las_enumeraciones_son_las_del_anexo_b1_del_bloque_b():
    b1 = _b1()
    assert cadena_b.ENUMERACIONES_B1["nivel"] == tuple(b1["nivel"].split("|"))
    assert cadena_b.ENUMERACIONES_B1["prioridad"] == tuple(b1["prioridad"].split("|"))
    assert cadena_b.ENUMERACIONES_B1["perfil_invertibilidad"] == (b1["marco_invertibilidad"]["perfil"],)
    assert cadena_b.RE_IDIOMA.fullmatch(b1["idioma_usuario"])
    # y la configuración por defecto las cumple
    pet = cargar_config()["cadena_b"]["peticion"]
    assert all(pet[k] in v for k, v in cadena_b.ENUMERACIONES_B1.items())


@pytest.mark.parametrize("cambio", [
    {"cadena_b": {"peticion": {"nivel": "N9"}}}, {"cadena_b": {"peticion": {"nivel": "auto"}}},
    {"cadena_b": {"peticion": {"prioridad": "URGENTISIMA"}}}, {"cadena_b": {"peticion": {"prioridad": 1}}},
    {"cadena_b": {"peticion": {"perfil_invertibilidad": "PROFESIONAL"}}}, {"idioma": 123}, {"idioma": "español"},
    {"idioma": "es_ES"}, {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": " liquidez_eur "}}},
    {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M ": "liquidez_eur"}}},
    {"cadena_b": {"correspondencia_ambitos": {"LETRAS-EUR-12M": "liquidez eur"}}},
])
def test_h03_configuracion_fuera_de_b1_falla_cerrado(ejemplo, cfg, cambio):
    c = fusionar(cfg, cambio)
    if "correspondencia_ambitos" in json.dumps(cambio):
        c["cadena_b"]["correspondencia_ambitos"] = cambio["cadena_b"]["correspondencia_ambitos"]
    for exigir in (True, False):
        e = _codigo(copy.deepcopy(ejemplo), c, exigir_correspondencia=exigir)
        assert e is not None and e.codigo == "CONFIGURACION_CADENA_B", (cambio, e)


def test_h03_peticion_que_no_es_una_tabla(ejemplo, cfg):
    c = copy.deepcopy(cfg)
    c["cadena_b"]["peticion"] = "AUTO"
    assert _codigo(ejemplo, c).codigo == "CONFIGURACION_CADENA_B"


@pytest.mark.parametrize("valores", [{"nivel": "N3", "prioridad": "ALTA"}, {"nivel": "PERS", "prioridad": "BAJA"}])
def test_h03_valores_de_b1_se_aceptan(ejemplo, cfg, valores):
    pet = cadena_b.construir_peticion(ejemplo, OPP, fusionar(cfg, {"cadena_b": {"peticion": valores}, "idioma": "en-GB"}))
    assert (pet["nivel"], pet["prioridad"], pet["idioma_usuario"]) == (valores["nivel"], valores["prioridad"], "en-GB")


# ---------------------------------------------------------------- T-142 H-04 · la sonda no arrastra una clave del paquete
def test_h04_sonda_sin_correspondencia_quita_la_clave_previa(ejemplo, cfg):
    _entrada(ejemplo)["x_clave_universo"] = "cobre"
    _entrada(ejemplo)["indicador_seguimiento"]["simbolo"] = "SIN-FILA"
    pet = cadena_b.construir_peticion(ejemplo, OPP, cfg, exigir_correspondencia=False)
    assert "x_clave_universo" not in pet["paquete_para_bloque_B"] and "clave_universo" not in pet["objeto"]
    assert _entrada(ejemplo)["x_clave_universo"] == "cobre"             # el paquete no cambia


# ---------------------------------------------------------------- T-141 H-01 · comprobar_datos_a.py --clases
@pytest.fixture(scope="module")
def comprobar():
    return _modulo("comprobar_datos_a")


@pytest.mark.parametrize("clases", [["XXX"], ["div"], ["DIV", "RENTA"], []])
def test_t141_h01_clases_que_no_existen_fallan(comprobar, clases, capsys):
    with pytest.raises(SystemExit) as e:
        comprobar.main([str(DATOS), "--as-of", "2024-03-29", "--clases", *clases])
    assert e.value.code == 2
    assert "0 de 0" not in capsys.readouterr().out


def test_t141_h01_universo_sin_simbolos_de_la_clase_falla(comprobar, tmp_path, capsys):
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    u[u["clase"] == "DIV"].to_csv(tmp_path / "solo_div.csv", index=False)
    assert comprobar.main([str(DATOS), "--universo", str(tmp_path / "solo_div.csv"), "--as-of", "2024-03-29",
                           "--clases", "RV"]) == 2
    salida = capsys.readouterr()
    assert "nada que comprobar" in salida.err and "0 de 0" not in salida.out


def test_t141_h01_una_clase_que_existe_sigue_en_verde(comprobar, capsys):
    assert comprobar.main([str(DATOS), "--as-of", "2024-03-29", "--clases", "DIV"]) == 0
    assert "6 de 6 símbolos OK" in capsys.readouterr().out


# ---------------------------------------------------------------- T-141 H-02 y H-03 · descargar_datos_bce.py
CAB = "KEY,FREQ,CURRENCY,CURRENCY_DENOM,EXR_TYPE,EXR_SUFFIX,TIME_PERIOD,OBS_VALUE,OBS_STATUS\n"
VAL = {"USD": 1.1, "JPY": 170.0, "GBP": 0.85, "AUD": 1.7, "CHF": 0.93, "MXN": 20.5}


def _fila(m, d, v):
    return f"EXR.D.{m}.EUR.SP00.A,D,{m},EUR,SP00,A,{d},{v},A\n"


def _cuerpo(quitar=(), valores=None, extra=""):
    v = {**VAL, **(valores or {})}
    return CAB + "".join(_fila(m, d, v[m]) for d in ("2026-11-12", "2026-11-13") for m in VAL if m not in quitar) + extra


@pytest.fixture()
def bce():
    return _modulo("descargar_datos_bce")


def _con_respuesta(bce, monkeypatch, cuerpo):
    class R(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def falso(url, timeout=None):
        if isinstance(cuerpo, Exception):
            raise cuerpo
        return R(cuerpo.encode())
    monkeypatch.setattr(bce.urllib.request, "urlopen", falso)


@pytest.mark.parametrize("nombre, cuerpo", [
    ("solo cabecera", CAB), ("vacío", ""), ("falta MXN", _cuerpo(quitar=("MXN",))),
    ("fila repetida con otro valor", _cuerpo(extra=_fila("USD", "2026-11-13", 9.99))),
    ("fila repetida igual", _cuerpo(extra=_fila("USD", "2026-11-13", 1.1))),
    ("USD sin valores", _cuerpo(valores={"USD": "NaN"})), ("JPY negativo", _cuerpo(valores={"JPY": -170.0})),
    ("HTML con 200", "<html><body>Service unavailable</body></html>"),
    ("HTTP 404", urllib.error.HTTPError("u", 404, "No Results Found", {}, io.BytesIO(b""))),
    ("sin conexión", urllib.error.URLError("sin red")),
])
def test_t141_h03_respuestas_raras_no_escriben_nada(bce, monkeypatch, tmp_path, capsys, nombre, cuerpo):
    _con_respuesta(bce, monkeypatch, cuerpo)
    destino = tmp_path / "datos"
    destino.mkdir()
    (destino / "OTRO.csv").write_text("fecha,cierre\n", encoding="utf-8")     # lo que ya había se queda
    assert bce.main([str(destino)]) == 1, nombre
    assert sorted(p.name for p in destino.iterdir()) == ["OTRO.csv"]
    assert "no se escribe nada" in capsys.readouterr().err


def test_t141_h03_respuesta_normal_escribe_las_seis_series(bce, monkeypatch, tmp_path):
    _con_respuesta(bce, monkeypatch, _cuerpo())
    assert bce.main([str(tmp_path / "nueva")]) == 0
    assert sorted(p.stem for p in (tmp_path / "nueva").iterdir()) == sorted(bce.CRUCES)
    df = (tmp_path / "nueva" / "USDJPY=X.csv").read_text(encoding="utf-8").splitlines()
    assert df[0] == "fecha,cierre,fecha_publicacion" and df[1].startswith("2026-11-12,154.54545455,2026-11-12")


def test_t141_h02_el_docstring_dice_cuando_se_publica():
    texto = " ".join((SCRIPTS / "descargar_datos_bce.py").read_text(encoding="utf-8").split("Uso")[0].split())
    assert "hacia las 16:00 (CET)" in texto and "14:15" in texto and "no el cierre de un mercado" in texto
