"""T-145 · Hallazgos de la QA r01 de T-140: la cota del coste de un ciclo (H-01), filas de tabla con una fecha delante
(H-02), falsos negativos de tarjetas (H-03), la comprobación de datos (H-04), el borrador del Anexo B (H-05) y los
mutantes vivos (H-06). Sin red ni coste: el cliente real se prueba con un SDK falso."""
import importlib.util
import json
import random
import shutil
import types
from pathlib import Path

import pandas as pd
import pytest
import yaml
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config
from bloque_a.contratos import _luhn, tarjetas_en_texto
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.orquestacion import Bloque
from conftest import DATOS

from bloque_a import llm, mock_respuestas, redaccion

SCRIPTS = Path(__file__).resolve().parents[3] / ".docs" / "scripts"
PRECIOS = Path(__file__).resolve().parents[1] / "config" / "precios_anthropic.yaml"
V = "4111 1111 " + "1111 1111"      # números de prueba publicados, partidos en dos cadenas para el gate de secretos
M = "5555 5555 " + "5555 4444"
AS_OF_MEDIDA = "2024-03-29"          # el de `medir_consumo_a.py`


def _modulo(nombre):
    spec = importlib.util.spec_from_file_location(nombre, SCRIPTS / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def est():
    return _modulo("estimar_coste_ciclo_a")


@pytest.fixture(scope="module")
def tarifa():
    return yaml.safe_load(PRECIOS.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- H-01 · la cota del coste de un ciclo
def _bloque(tmp, cliente, cfg=None):
    return Bloque(cfg or cargar_config(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), cliente,
                  Path(tmp) / "estado", Path(tmp) / "ent")


@pytest.fixture(scope="module")
def medida(tmp_path_factory):
    """Lo que mide `medir_consumo_a.py`: un ciclo C1 con el cliente simulado y la configuración por defecto (solo DIV)."""
    reg = []
    orig = llm.MockClient.generar

    def espia(self, **kw):
        r = orig(self, **kw)
        reg.append({"agente": kw["agente"], "modelo": kw["modelo"],
                    "sys_tok": llm._tokens_aprox("".join(b.get("text", "") for b in kw["system"])),
                    "user_tok": llm._tokens_aprox(json.dumps(kw["mensajes"], ensure_ascii=False, default=str)),
                    "out_tok": r.uso.salida, "max_tokens": kw["max_tokens"], "cache_lect": r.uso.cache_lectura,
                    "cache_escr": r.uso.cache_escritura})
        return r
    llm.MockClient.generar = espia
    try:
        _bloque(tmp_path_factory.mktemp("t145m"), llm.MockClient()).ciclo(AS_OF_MEDIDA)
    finally:
        llm.MockClient.generar = orig
    return reg


class _SDKPeorCaso:
    """SDK falso (sin red ni coste) que cobra lo que supone la cota en cada petición: la entrada con `factor_tokens_cota`
    como escritura de caché, lo que escribió el modelo reenviado y `max_tokens` de salida. El primer intento de cada llamada
    no es JSON (se paga la reparación) y el segundo es la respuesta del simulado (como `r01_02` de la QA de T-140)."""

    def __init__(self, est, tarifa):
        self.messages, self.est, self.tarifa, self.usd = self, est, tarifa, 0.0

    def create(self, **kw):
        tok = llm._tokens_aprox
        agente = kw["metadata"]["user_id"].removeprefix("bloque-a-")
        msgs, salida = kw["messages"], int(kw["max_tokens"])
        propio = [m for m in msgs if m["role"] == "user"]
        entrada = int((tok("".join(b["text"] for b in kw["system"])) + tok(json.dumps(propio, ensure_ascii=False)))
                      * float(self.tarifa["factor_tokens_cota"])) + salida * (len(msgs) - len(propio))
        self.usd += self.est._coste(self.tarifa["precios_por_millon"][kw["model"]], 0, salida, entrada, 0)
        texto = "análisis " * 200 if len(propio) == 1 else json.dumps(mock_respuestas.responder(agente, msgs[:1], 20261102),
                                                                       ensure_ascii=False)
        uso = types.SimpleNamespace(input_tokens=0, output_tokens=salida, cache_creation_input_tokens=entrada,
                                    cache_read_input_tokens=0, server_tool_use=None)
        return types.SimpleNamespace(stop_reason="end_turn", usage=uso, content=[types.SimpleNamespace(type="text", text=texto)])


@pytest.fixture(scope="module")
def peor_camino(tmp_path_factory, est, tarifa):
    """El peor caso pasado por el cliente real y el presupuesto del ciclo, con G3 bloqueando la primera redacción por
    legibilidad (C12): el ciclo pide la reescritura a AG-17, una llamada que el simulado no hace."""
    sdk = _SDKPeorCaso(est, tarifa)
    gen = redaccion.Redaccion.generar
    veces = {"n": 0}

    def generar(self, *a, **k):
        entreg, g3b = gen(self, *a, **k)
        veces["n"] += 1
        return entreg, (dict(g3b, dictamen="BLOQUEADO", bloqueos=["C12"], legibilidad=60, frases_largas=[])
                        if veces["n"] == 1 else g3b)
    redaccion.Redaccion.generar = generar
    try:
        b = _bloque(tmp_path_factory.mktemp("t145p"), llm.AnthropicClient(sdk=sdk, salida_estructurada=False))
        r = b.ciclo(AS_OF_MEDIDA)
    finally:
        redaccion.Redaccion.generar = gen
    return sdk.usd, r, b


def test_h01_la_tabla_de_llamadas_del_ciclo(est, tarifa, medida):
    cfg = cargar_config()
    c = est.cota_ciclo(medida, cfg, tarifa["precios_por_millon"], 10.0, 1.35)
    # 7 por tipo de activo (cribado, petición, prospectiva, refutación, respuesta, contrarréplica, curación) y 7 del ciclo
    # (aprendizaje, integración, dos dictámenes G3, redacción y reescritura, auditoría)
    assert c["llamadas_max"] == 7 + 7 > len(medida)
    # la petición de conocimiento (con búsqueda): 2 intentos × 4 peticiones (3 continuaciones) × 5 búsquedas
    # y las otras 13 llamadas, 2 peticiones cada una (el intento y la reparación)
    assert c["busquedas"] == 1 * 2 * 4 * 5 and c["peticiones_max"] == 13 * 2 + 1 * 2 * 4
    assert {x["papel"] for x in c["papeles"]} >= {"peticion_conocimiento", "contrarreplica", "dictamen_g3", "informe_aprendizaje"}
    doce = cargar_config(extra={"perfiles": {"activos": ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT",
                                                         "MON", "TCV"]}})
    assert est.cota_ciclo(medida, doce, tarifa["precios_por_millon"], 10.0, 1.35)["llamadas_max"] == 7 * 12 + 7
    assert c["cota"] == min(c["cota_llamadas"], c["cota_presupuesto"])
    # S4: la contrarréplica lee la salida máxima de las cinco llamadas anteriores de su tipo (cribado y respuesta del
    # Analista, 12 000 cada una; petición, 8 000; prospectiva y refutación, 10 000 cada una)
    contra = next(x for x in c["papeles"] if x["papel"] == "contrarreplica")
    assert contra["encargo_tok"] == max(x["user_tok"] for x in medida if x["agente"] == "AG-11") + 52_000
    # el presupuesto del ciclo (240 UC) con la ampliación máxima (+50 %), al peor precio por UC (Opus: 16 000 tokens de
    # entrada como escritura de caché a 8 USD por millón) en las dos bolsas
    assert c["presupuesto"]["limites"] == pytest.approx(240 * 1.5 * 16_000 * 8.0 / 1e6)


def test_h01_la_cota_cubre_el_peor_camino_con_el_cliente_real(est, tarifa, medida, peor_camino):
    usd, _r, _b = peor_camino
    cfg = cargar_config()
    viejo = est.estimar(medida, tarifa["precios_por_millon"], 10.0, set(), 5, 1.35, 3, 1)["cota_superior"]
    nueva = est.cota_ciclo(medida, cfg, tarifa["precios_por_millon"], 10.0, 1.35)["cota"]
    # T-146: antes, este camino costaba más que la cifra de T-140 (la reescritura la pasaba) y eso mostraba que no era una
    # cota; con el presupuesto que reserva el peor caso antes de cada petición, el camino se corta antes y la comparación
    # con la cifra vieja deja de tener sentido. Queda lo que importa: el coste real no pasa de la cota
    assert viejo > 0
    assert usd <= nueva


def test_h01_el_presupuesto_se_pasa_y_la_cota_por_presupuesto_lo_cuenta(peor_camino):
    """Hallazgo de T-145: `Bloque._invocar` compara una estimación (2 500 de salida, sin reparación) con lo disponible y
    carga lo real después, y la escritura de caché de los agentes compartidos se carga como lectura hasta
    `liquidar_primas`. La bolsa acaba por encima de su límite, pero no de lo que suma la cota por presupuesto: el límite con
    la ampliación máxima, su mayor llamada y la caché cargada como lectura."""
    _usd, r, b = peor_camino
    cfg = b.cfg
    amp = max(cfg["presupuesto_uc"]["ampliacion_sin_autorizacion"], cfg["presupuesto_uc"]["ampliacion_max_autorizable"])
    pasadas = 0
    for bolsa, v in r["presupuesto"].items():
        ll = [x for x in b.contabilidad.llamadas if (x["clase"] or "COMUN") == bolsa]
        limite = v["asignado"] * (1 + cfg["presupuesto_uc"]["ampliacion_sin_autorizacion"]) + v["ampliado"]
        pasadas += v["consumido"] > limite
        primas = sum(0.5 * x["cache_escritura"] * (1 - cfg["uc"]["factor_lectura_cache"]) / cfg["uc"]["tokens_entrada_por_uc"]
                     for x in ll)
        assert v["consumido"] <= v["asignado"] * (1 + amp) + max(x["uc"] for x in ll) + primas + 1e-6
    # T-146: el presupuesto reserva el peor caso antes de cada petición, así que ninguna bolsa pasa ya de su límite (antes
    # de T-146 esta prueba exigía al menos una bolsa pasada, que era el hallazgo)
    assert pasadas == 0


def test_h01_falla_cerrado(est, tarifa, medida):
    with pytest.raises(SystemExit, match="V5"):
        est.cota_ciclo(medida, cargar_config(extra={"diseno": "v6"}), tarifa["precios_por_millon"], 10.0, 1.35)
    de_mas = medida + [dict(medida[0])] * 3      # más llamadas de un agente que las que permite el código
    with pytest.raises(SystemExit, match="previstas"):
        est.cota_ciclo(de_mas, cargar_config(), tarifa["precios_por_millon"], 10.0, 1.35)
    with pytest.raises(SystemExit, match="tarifa"):
        est.cota_ciclo(medida, cargar_config(), {}, 10.0, 1.35)


def test_h01_peor_llamada_reenvia_y_paga_cada_peticion(est):
    p = {"entrada": 2.0, "salida": 10.0, "escritura_cache": 4.0, "lectura_cache": 0.1}
    uc = (8000.0, 1500.0, 0.1)
    w = est.peor_llamada(p, 900_000, 100_000, 100_000, True, 1, 1, 1.0, 5, 10.0, uc, tok_reparacion=10_000)
    # reparación 0: vueltas 0 y 1 (reenvía 0 y 1 salidas); reparación 1: reenvía 1 y 2 salidas y el mensaje de errores
    entradas = [1.0, 1.1, 1.11, 1.21]   # millones de tokens
    assert w["peticiones"] == 4 and w["busquedas"] == 20
    assert w["usd"] == pytest.approx(sum(e * 4 + 1.0 for e in entradas) + 20 * 0.01)
    assert w["uc"] == pytest.approx(sum(0.5 * e * 1e6 / 8000 + 0.5 * 100_000 / 1500 for e in entradas))


def test_h06_k04_main_lee_las_reparaciones_de_la_configuracion(tmp_path, est, medida, capsys):
    (tmp_path / "m").mkdir()
    (tmp_path / "m" / "llamadas.json").write_text(json.dumps(medida), encoding="utf-8")
    cifras = []
    for rep in (0, 1):
        cfg = tmp_path / f"rep{rep}.yaml"
        cfg.write_text(yaml.safe_dump({"llm": {"reintento_reparacion": rep}}), encoding="utf-8")
        assert est.main([str(tmp_path / "m"), "--config", str(cfg)]) == 0
        salida = capsys.readouterr().out
        cifras.append([float(x.split()[0]) for x in salida.split("peor caso de esas llamadas ")[1:2]]
                      + [float(salida.split("Cota superior del ciclo: ")[1].split()[0])])
    assert cifras[1][0] > cifras[0][0] and cifras[1][1] > cifras[0][1]


# ---------------------------------------------------------------- H-02 · filas de tabla con una fecha delante
def _nivel(r):
    return str(r.randint(4000, 5999))      # niveles de un índice (prefijo de Visa o de Mastercard)


def _anio(r):
    return str(r.randint(2015, 2026))


def _mmdd(r):
    return f"{r.randint(1, 12):02d}{r.randint(1, 28):02d}"


@pytest.mark.parametrize("nombre,fila", [
    ("año y cuatro niveles", lambda r: [_anio(r)] + [_nivel(r) for _ in range(4)]),
    ("cuatro niveles y el año", lambda r: [_nivel(r) for _ in range(4)] + [_anio(r)]),
    ("fecha MMDD y cuatro niveles", lambda r: [_mmdd(r)] + [_nivel(r) for _ in range(4)]),
    ("año y cuatro precios del oro", lambda r: [_anio(r)] + [str(r.randint(1800, 2700)) for _ in range(4)]),
    ("dos años y cuatro niveles", lambda r: [_anio(r), _anio(r)] + [_nivel(r) for _ in range(4)]),
    ("año y ocho niveles", lambda r: [_anio(r)] + [_nivel(r) for _ in range(8)]),
])
@pytest.mark.parametrize("sep", [" ", "-"])
def test_h02_una_fila_con_la_fecha_delante_no_es_una_tarjeta(nombre, fila, sep):
    r = random.Random(nombre)
    assert not any(tarjetas_en_texto(sep.join(fila(r))) for _ in range(3000))


def test_h02_limite_declarado_la_fecha_detras_de_cuatro_niveles():
    # INC-T123-01 (T-145): «cuatro niveles + MMDD» tiene la forma de «tarjeta + caducidad» y se marca cuando los cuatro
    # niveles pasan Luhn con prefijo de red (~7 %); es el precio de detectar la tarjeta con su caducidad
    r = random.Random(7)
    n = sum(bool(tarjetas_en_texto(" ".join([_nivel(r) for _ in range(4)] + [_mmdd(r)]))) for _ in range(5000))
    assert 0 < n <= 500


# ---------------------------------------------------------------- H-03 · lo que va detrás de la tarjeta
def _tarjeta(r, prefijo="4"):
    while True:
        c = prefijo + "".join(str(r.randint(0, 9)) for _ in range(15 - len(prefijo)))
        for d in "0123456789":
            if _luhn(c + d):
                return " ".join((c + d)[i:i + 4] for i in range(0, 16, 4))


@pytest.mark.parametrize("forma", ["{a} 0128 {b}", "{a} 0128 {b} 0329", "{a} {b} 1230", "{a} 1299 {b}"])
def test_h03_tarjetas_con_su_caducidad_detras(forma):
    r = random.Random(forma)
    for _ in range(300):
        a, b = _tarjeta(r), _tarjeta(r, r.choice(["51", "52", "53", "54", "55"]))
        assert tarjetas_en_texto(forma.format(a=a, b=b)) == ["tarjeta …" + a[-4:], "tarjeta …" + b[-4:]]


@pytest.mark.parametrize("forma", ["2027 {a} 0128", "0128 {a} 2028", "{a} 0128 4321", "{a} 2027", "2027 {a}"])
def test_h03_limites_declarados(forma):
    # INC-T123-01 (T-145): lo que va delante de la tarjeta (un año, una fecha) y lo que va detrás sin forma de caducidad
    # (un año de cuatro cifras, un PIN tras la caducidad) hace que la serie se lea como una fila de tabla
    r = random.Random(forma)
    assert not any(tarjetas_en_texto(forma.format(a=_tarjeta(r))) for _ in range(300))


# ---------------------------------------------------------------- H-06 · T06 y T07: mes «00» y meses 13–19
@pytest.mark.parametrize("cola,detecta", [("0028", False), ("1300", False), ("1500", False), ("1999", False),
                                          ("0128", True), ("1228", True)])
def test_h06_t06_t07_solo_un_mes_de_01_a_12_es_caducidad(cola, detecta):
    assert tarjetas_en_texto(f"{V} {cola}") == (["tarjeta …1111"] if detecta else [])
    assert tarjetas_en_texto(f"{V} {cola} {M}") == (["tarjeta …1111", "tarjeta …4444"] if detecta else [])


# ---------------------------------------------------------------- H-04 · símbolo que dejó de cotizar antes de la ventana
@pytest.fixture(scope="module")
def comprobar():
    return _modulo("comprobar_datos_a").comprobar


def _carpeta(tmp_path, hasta=None, quitar=False):
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO).head(1)
    d = tmp_path / "datos"
    d.mkdir()
    s = u["simbolo"].iloc[0]
    if not quitar:
        df = pd.read_csv(Path(DATOS) / f"{s}.csv")
        if hasta:
            df = df[pd.to_datetime(df["fecha"]) <= pd.Timestamp(hasta)]
        df.to_csv(d / f"{s}.csv", index=False)
    return d, u


def test_h04_datos_que_acaban_antes_de_la_ventana_son_antiguo(tmp_path, comprobar):
    d, u = _carpeta(tmp_path, hasta="2022-06-30")
    f = comprobar(d, u, "2026-06-30")[0]
    assert f["estado"] == "ANTIGUO" and f["hasta"].startswith("2022-06") and "anterior a la ventana" in f["motivo"]
    assert f["desde"] is None and f["filas"] == 0 and f["mayor_hueco_dias"] is None   # las cifras son las de la ventana


def test_h04_sin_archivo_sigue_siendo_falta(tmp_path, comprobar):
    d, u = _carpeta(tmp_path, quitar=True)
    assert comprobar(d, u, "2026-06-30")[0]["estado"] == "FALTA"


def test_h04_el_docstring_dice_que_las_cifras_son_de_la_ventana():
    doc = _modulo("comprobar_datos_a").__doc__
    assert "de la ventana del ciclo" in doc and "ANTIGUO" in doc


# ---------------------------------------------------------------- H-06 · V02: el margen de 30 días de `senales`
def test_h06_v02_un_dato_malo_en_el_margen_de_senales_es_invalido(tmp_path, comprobar):
    # `senales`: 3 años y 30 días; `tasa_base`: 3 años. Un dato malo entre los dos bordes está dentro de la ventana
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO).head(1)
    d = tmp_path / "datos"
    d.mkdir()
    s = u["simbolo"].iloc[0]
    shutil.copy(Path(DATOS) / f"{s}.csv", d / f"{s}.csv")
    df = pd.read_csv(d / f"{s}.csv")
    df["cierre"] = df["cierre"].astype(object)
    fechas = pd.to_datetime(df["fecha"])
    df.loc[fechas == fechas[fechas >= "2023-06-15"].min(), "cierre"] = "n/d"
    df.to_csv(d / f"{s}.csv", index=False)
    assert comprobar(d, u, "2026-06-30")[0]["estado"] == "INVALIDO"


# ---------------------------------------------------------------- H-05 · el §1 del borrador del Anexo B
def test_h05_el_borrador_separa_los_retornos_del_motor():
    mod = _modulo("borrador_anexo_b")
    texto = mod.generar()
    assert mod.SALIDA.read_text(encoding="utf-8") == texto
    generales = [ln for ln in texto.splitlines() if ln.startswith("- **Retornos")]
    assert any(ln.startswith("- **Retornos internos (CT-06 a CT-08 y CT-11 a CT-14).**") and "ESQUEMAS" in ln for ln in generales)
    assert any(ln.startswith("- **Retornos del Motor (CT-09 y CT-10).**") and "motor/servicio.py" in ln for ln in generales)
    assert not any("CT-06 a CT-14" in ln for ln in generales)
    assert mod._tramos({"CT-01", "CT-03", "CT-04"}) == "CT-01, CT-03 y CT-04" and mod._tramos({"CT-05"}) == "CT-05"
