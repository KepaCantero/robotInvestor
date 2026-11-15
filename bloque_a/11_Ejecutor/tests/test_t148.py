"""T-148 · Hallazgos de la QA r01 de T-145: la contrarréplica y la respuesta a objeciones en la cota del coste (H-01), lo
que lee cada búsqueda (H-02), los tipos de F10 (H-03), los mutantes vivos del estimador (H-04), la comprobación de datos
con el último cierre inválido (H-05), el borrador del Anexo B (H-06) y INC-T129-01 (H-07). Sin red ni coste.

Ningún identificador de modelo se escribe aquí: los modelos salen de la tarifa y de la configuración."""
import collections
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest
import yaml
from bloque_a.almacen import Almacen
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config, modelo_de
from bloque_a.consumo import Contabilidad, Presupuesto, ReservaLlamada
from bloque_a.contratos import AGENTE_CLASE
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.orquestacion import Bloque
from conftest import DATOS

from bloque_a import llm

EJECUTOR = Path(__file__).resolve().parents[1]
REPO = EJECUTOR.parents[1]
SCRIPTS = REPO / ".docs" / "scripts"
PRECIOS = EJECUTOR / "config" / "precios_anthropic.yaml"
DOCE = ["RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"]


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


@pytest.fixture(scope="module")
def medida(tmp_path_factory):
    """Lo que mide `medir_consumo_a.py` en un ciclo C1 simulado con la configuración por defecto (solo DIV)."""
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
        tmp = tmp_path_factory.mktemp("t148m")
        Bloque(cargar_config(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), llm.MockClient(),
               tmp / "estado", tmp / "ent").ciclo("2024-03-29")
    finally:
        llm.MockClient.generar = orig
    return reg


def _cota(est, medida, tarifa, cfg=None, **kw):
    return est.cota_ciclo(medida, cfg or cargar_config(), tarifa["precios_por_millon"], 10.0, 1.35, **kw)


def _encargo_max(cfg, bolsa_tipo=True, n_tipos=1):
    p, u = cfg["presupuesto_uc"], cfg["uc"]
    amp = max(p["ampliacion_sin_autorizacion"], p["ampliacion_max_autorizable"])
    limite = (1 + amp) * (p["N2"] if bolsa_tipo else max(p["fraccion_minima_comun"] * p["ciclo_semanal_max"],
                                                         p["ciclo_semanal_max"] - n_tipos * p["N1"]))
    r = p["reserva"]   # T-146: la entrada por el margen y, como poco, la salida mínima caben en la bolsa
    return 2 * u["tokens_entrada_por_uc"] * (limite - 0.5 * r["salida_minima_tokens"] / u["tokens_salida_por_uc"]) / r["factor_tokens_entrada"]


# ---------------------------------------------------------------- H-01 · la contrarréplica y la respuesta (S4b)
def test_h01_la_respuesta_y_la_contrarreplica_se_acotan_por_el_presupuesto(est, tarifa, medida):
    cfg = cargar_config()
    c = _cota(est, medida, tarifa)
    por = {x["papel"]: x for x in c["papeles"] if x["tipo"] == "DIV"}
    for papel, agente in (("contrarreplica", "AG-11"), ("respuesta_objeciones", AGENTE_CLASE["DIV"])):
        medido = max(x["user_tok"] for x in medida if x["agente"] == agente)
        assert por[papel]["encargo_tok"] == pytest.approx(medido + _encargo_max(cfg)), papel
        assert por[papel]["encargo_tok"] > medido + por[papel]["lee_tok"]          # S4 no los acotaba
    # los demás papeles siguen con S4: lo medido más lo que leen (el tope del presupuesto no les llega)
    for papel in ("cribado", "prospectiva", "refutacion", "curacion"):
        x = por[papel]
        medido = max([m["user_tok"] for m in medida if m["agente"] == x["agente"]] or [max(m["user_tok"] for m in medida)])
        assert x["encargo_tok"] == medido + x["lee_tok"], papel
    assert c["encargo_max_por_bolsa"]["DIV"] == pytest.approx(_encargo_max(cfg))
    assert c["encargo_max_por_bolsa"]["COMUN"] == pytest.approx(_encargo_max(cfg, False, 1))


def test_h01_con_un_presupuesto_pequeno_el_tope_acota_tambien_a_s4(est, tarifa, medida):
    """Con bolsas de 1 UC, el tope del presupuesto (2·8 000·(1,5 − 0,83) / 1,35 ≈ 7 901 tokens) es menor que lo que S4 da
    a la prospectiva o la refutación: su encargo es lo medido más el tope, no más lo que leen."""
    cfg = cargar_config(extra={"presupuesto_uc": {"N1": 1, "N2": 1}})
    c = _cota(est, medida, tarifa, cfg)
    tope = _encargo_max(cfg)
    assert 0 < tope < 10_000
    for x in c["papeles"]:
        if x["tipo"] == "DIV":
            medido = max([m["user_tok"] for m in medida if m["agente"] == x["agente"]] or [max(m["user_tok"] for m in medida)])
            assert x["encargo_tok"] == pytest.approx(medido + min(x["lee_tok"], tope) if x["papel"] not in
                                                     est.MULTIPLICAN_ENCARGO else medido + tope), x["papel"]
    assert any(x["lee_tok"] > tope for x in c["papeles"] if x["tipo"] == "DIV" and x["papel"] not in est.MULTIPLICAN_ENCARGO)


def test_h01_el_tope_del_encargo_es_el_de_la_reserva_del_codigo(est, tarifa, medida):
    """Integración con T-146: `ReservaLlamada` no deja salir una petición con un mensaje del tamaño del tope (y algo más) en
    la bolsa del tipo entera (N2 con la ampliación máxima), y sí uno algo menor: ningún mensaje admitido pasa del tope. El
    tope del estimador es el mismo."""
    cfg = cargar_config()
    p = cfg["presupuesto_uc"]
    limite = p["N2"] * (1 + max(p["ampliacion_sin_autorizacion"], p["ampliacion_max_autorizable"]))
    tope = _encargo_max(cfg)
    assert _cota(est, medida, tarifa)["encargo_max_por_bolsa"]["DIV"] == pytest.approx(tope)

    def sale(tokens):
        # la base de la bolsa tal que su límite (la base con el margen sin autorización) es el de la ampliación máxima
        base = limite / (1 + p["ampliacion_sin_autorizacion"])
        guarda = ReservaLlamada(Presupuesto({"DIV": base}, cfg), "DIV", Contabilidad(cfg), "AG-11")
        mensaje = [{"role": "user", "content": "a" * int(tokens * 3.6)}]
        return guarda.reservar([], mensaje, None, int(p["reserva"]["salida_minima_tokens"])) is not None
    assert not sale(tope * 1.001)
    assert sale(tope * 0.99)          # el tope es ajustado


def test_h01_la_cota_cubre_el_caso_de_la_qa(est, tarifa, medida):
    """El escenario de la QA (r01_01, N = 150, K = 1): la contrarréplica se admitió con 196 239 tokens de encargo (S4 daba
    53 746) y costó 2,48 USD (5,04 con toda la entrada como escritura y una reparación). La cota de esa llamada pasa de las
    dos cifras y su encargo, de los 222 410 de N = 170."""
    contra = next(x for x in _cota(est, medida, tarifa)["papeles"] if x["papel"] == "contrarreplica")
    assert contra["encargo_tok"] > 222_410 and contra["usd"] > 5.04


def test_h01_la_curacion_se_queda_por_debajo_del_contexto_largo_de_su_tarifa(est, tarifa, medida):
    """S5: la única tarifa con recargo por contexto largo es la del modelo más barato (comentario de la tarifa: por encima de
    100 000 tokens de prompt); su único papel en el ciclo, la curación, no llega con S4 (con el margen y una reparación)."""
    cfg = cargar_config()
    barato = min(tarifa["precios_por_millon"], key=lambda m: tarifa["precios_por_millon"][m]["entrada"])
    assert "100 000 tokens" in PRECIOS.read_text(encoding="utf-8")
    papeles = [x for x in _cota(est, medida, tarifa)["papeles"] if modelo_de(cfg, x["agente"]) == barato]
    assert {x["papel"] for x in papeles} == {"curacion"}
    for x in papeles:
        assert x["encargo_tok"] * 1.35 + cfg["llm"]["reintento_reparacion"] * cfg["max_tokens"]["por_defecto"] < 100_000


# ---------------------------------------------------------------- H-02 · lo que lee cada búsqueda
def test_h02_el_peso_de_lo_que_lee_cada_busqueda(est, tarifa, medida, tmp_path, capsys):
    c = _cota(est, medida, tarifa)
    cfg = cargar_config()
    # la petición de conocimiento (1 por tipo): 2 intentos × 5 búsquedas por petición × (4 + 3 + 2 + 1) lecturas, al precio
    # de escritura de caché de su agente, por cada 1 000 tokens leídos
    pc = next(x for x in c["papeles"] if x["papel"] == "peticion_conocimiento")
    esperado = 2 * 5 * (4 + 3 + 2 + 1) * tarifa["precios_por_millon"][modelo_de(cfg, pc["agente"])]["escritura_cache"] * 1000 / 1e6
    assert c["usd_por_mil_tokens_leidos_por_busqueda"] == pytest.approx(esperado)
    (tmp_path / "m").mkdir()
    (tmp_path / "m" / "llamadas.json").write_text(json.dumps(medida), encoding="utf-8")
    assert est.main([str(tmp_path / "m")]) == 0
    salida = capsys.readouterr().out
    assert "salvo lo que lee cada búsqueda" in salida and "por cada 1 000 tokens leídos" in salida
    assert any(s.startswith("S4b") for s in est.SUPUESTOS)


# ---------------------------------------------------------------- T-146 integrado (aviso de la coordinación)
def test_con_t146_la_cota_por_presupuesto_son_los_limites(est, tarifa, medida, tmp_path, capsys):
    """Con T-146 el presupuesto reserva el peor caso antes de cada petición y todo pasa por él: la cota por presupuesto es
    solo `limites` (sin última llamada, primas, lo de fuera ni las búsquedas aparte); es la de por defecto desde que T-146
    está en el código, y `con_t146=False` da la más holgada de antes."""
    sin = _cota(est, medida, tarifa, con_t146=False)
    con = _cota(est, medida, tarifa)
    p = sin["presupuesto"]
    assert con["cota_presupuesto"] == pytest.approx(p["limites"])
    assert sin["cota_presupuesto"] == pytest.approx(p["limites"] + p["ultima_llamada"] + p["primas_cache"]
                                                    + p["fuera_del_presupuesto"] + sin["busquedas"] * 10.0 / 1000)
    assert con["cota_llamadas"] == sin["cota_llamadas"] and con["cota"] == min(con["cota_llamadas"], con["cota_presupuesto"])
    # si la configuración da las UC de una búsqueda (la clave de T-146) y su precio por UC es el más alto, manda él
    cara = _cota(est, medida, tarifa, cargar_config(extra={"uc": {"uc_por_busqueda_web": 0.01}}))
    assert cara["cota_presupuesto"] == pytest.approx(p["limites"] * (10.0 / 1000 / 0.01) / _usd_por_uc_bolsa(
        est, cargar_config(), tarifa, ["AG-02", "AG-11", "AG-17"]))
    (tmp_path / "m").mkdir()
    (tmp_path / "m" / "llamadas.json").write_text(json.dumps(medida), encoding="utf-8")
    for opciones in ([], ["--con-t146"]):                # la opción vieja se acepta y da lo mismo
        assert est.main([str(tmp_path / "m"), *opciones]) == 0
        assert "con T-146 integrado: solo los límites" in capsys.readouterr().out
    assert est.main([str(tmp_path / "m"), "--sin-t146"]) == 0
    assert "la de antes de T-146, más holgada" in capsys.readouterr().out


# ---------------------------------------------------------------- H-03 · los tipos del ciclo salen de F10 si hay estado
def test_h03_los_tipos_salen_de_f10(est, tarifa, medida, tmp_path):
    estado = tmp_path / "estado"
    al = Almacen(estado)
    al.escribir("F10", "OPERADOR", {"tipo_entrada": "PARAMETRO", "param_id": "P-02", "nombre": "Clases de activo activas",
                                    "valor_inicial": ["DIV"], "valor_vigente": ["DIV", "RV"], "regimen": "SERVICIO"})
    doce = cargar_config(extra={"perfiles": {"activos": DOCE}})
    assert est.tipos_del_estado(str(estado), doce) == ["DIV", "RV"]
    c = _cota(est, medida, tarifa, doce, tipos=est.tipos_del_estado(str(estado), doce))
    assert c["tipos"] == ["DIV", "RV"] and c["llamadas_max"] == 7 * 2 + 7
    vacio = tmp_path / "vacio"
    vacio.mkdir()
    assert est.tipos_del_estado(str(vacio), doce) == DOCE                  # sin F10: lo que F10 tomará al nacer
    with pytest.raises(SystemExit, match="no existe"):
        est.tipos_del_estado(str(tmp_path / "no_hay"), doce)
    assert not (tmp_path / "no_hay").exists()
    for malos in (["XXX"], [], ["DIV", "DIV"]):
        with pytest.raises(SystemExit, match="tipos"):
            _cota(est, medida, tarifa, tipos=malos)


def test_h03_main_con_estado(est, medida, tmp_path, capsys):
    (tmp_path / "m").mkdir()
    (tmp_path / "m" / "llamadas.json").write_text(json.dumps(medida), encoding="utf-8")
    estado = tmp_path / "estado"
    Almacen(estado).escribir("F10", "OPERADOR", {"tipo_entrada": "PARAMETRO", "param_id": "P-02", "valor_vigente": ["DIV", "MON"],
                                                 "regimen": "SERVICIO"})
    assert est.main([str(tmp_path / "m"), "--estado", str(estado)]) == 0
    assert "Tipos de activo: DIV, MON\n" in capsys.readouterr().out


# ---------------------------------------------------------------- H-04 · los mutantes vivos del estimador (R01, R04–R09)
def test_h04_r01_la_integracion_lee_el_cribado(est, tarifa, medida):
    cfg = cargar_config()
    integ = next(x for x in _cota(est, medida, tarifa)["papeles"] if x["papel"] == "integracion")
    medido = max(x["user_tok"] for x in medida if x["agente"] == "AG-02")
    assert integ["lee_tok"] == cfg["max_tokens"][AGENTE_CLASE["DIV"]] and integ["encargo_tok"] == medido + integ["lee_tok"]


def _por_bolsa(c):
    ultima = collections.defaultdict(float)
    for x in c["papeles"]:
        if x["bolsa"]:
            ultima[x["bolsa"]] = max(ultima[x["bolsa"]], x["uc"] / x["llamadas"])
    return ultima


def _usd_por_uc_bolsa(est, cfg, tarifa, agentes):
    return max(est._usd_por_uc(tarifa["precios_por_millon"][modelo_de(cfg, a)], est._uc(cfg)) for a in agentes)


def test_h04_r04_r05_los_limites_del_presupuesto_a_mano(est, tarifa, medida):
    """Los límites, a mano, en dos casos (los modelos salen de la tarifa): tipos baratos y bolsa común cara con el tope de
    siempre (el máximo es con todos los tipos en N1: no basta el reparto todo N2, R05) y tipos caros con un tope pequeño
    (el máximo es todo N2 y la bolsa común se queda en su suelo, la fracción mínima del tope: R04)."""
    pm = tarifa["precios_por_millon"]
    barato, caro = min(pm, key=lambda m: pm[m]["entrada"]), max(pm, key=lambda m: pm[m]["entrada"])
    de_tipo = {AGENTE_CLASE[t] for t in DOCE} | {"AG-10", "AG-11", "AG-12", "AG-14", "AG-16"}
    for tope, m_tipo, m_comun in ((240, barato, caro), (100, caro, barato)):
        cfg = cargar_config(extra={"perfiles": {"activos": DOCE}, "presupuesto_uc": {"ciclo_semanal_max": tope},
                                   "modelos": {**{a: m_tipo for a in de_tipo}, "AG-02": m_comun, "AG-17": m_comun}})
        c = _cota(est, medida, tarifa, cfg)
        p = cfg["presupuesto_uc"]
        pt = _usd_por_uc_bolsa(est, cfg, tarifa, de_tipo)
        pc = _usd_por_uc_bolsa(est, cfg, tarifa, ["AG-02", "AG-17"])
        amp = max(p["ampliacion_sin_autorizacion"], p["ampliacion_max_autorizable"])
        bases = [k * p["N2"] + (12 - k) * p["N1"] for k in range(13)]
        esperado = max((1 + amp) * (pt * b + pc * max(tope - b, p["fraccion_minima_comun"] * tope)) for b in bases)
        assert c["presupuesto"]["limites"] == pytest.approx(esperado), tope
        if tope == 240:
            todos_n2 = (1 + amp) * (pt * bases[-1] + pc * max(tope - bases[-1], p["fraccion_minima_comun"] * tope))
            assert esperado > todos_n2                                           # R05: no basta el reparto todo N2
        else:
            sin_suelo = max((1 + amp) * (pt * b + pc * (tope - b)) for b in bases)
            assert esperado > sin_suelo                                          # R04: el suelo de la común cuenta


def test_h04_r06_r07_ultima_llamada_y_primas_a_mano(est, tarifa, medida):
    cfg = cargar_config()
    c = _cota(est, medida, tarifa)
    agentes = collections.defaultdict(set)
    for x in c["papeles"]:
        if x["bolsa"]:
            agentes[x["bolsa"]].update(x["agentes"])
    precio_uc = {b: _usd_por_uc_bolsa(est, cfg, tarifa, a) for b, a in agentes.items()}
    ultima = _por_bolsa(c)
    assert c["presupuesto"]["ultima_llamada"] > 0
    assert c["presupuesto"]["ultima_llamada"] == pytest.approx(sum(precio_uc[b] * ultima[b] for b in ultima))
    primas = sum(x["prima_uc"] for x in c["papeles"] if x["bolsa"])
    assert primas > 0 and c["presupuesto"]["primas_cache"] == pytest.approx(max(precio_uc.values()) * primas)
    # la prima de una llamada, a mano: por petición, 0,5 · sistema · margen · (1 − factor de lectura) / tokens por UC
    p = {"entrada": 2.0, "salida": 10.0, "escritura_cache": 4.0, "lectura_cache": 0.1}
    w = est.peor_llamada(p, 8000, 1000, 1000, False, 1, 3, 1.35, 5, 10.0, (8000.0, 1500.0, 0.1))
    assert w["peticiones"] == 2 and w["prima_uc"] == pytest.approx(2 * 0.5 * 8000 * 1.35 * 0.9 / 8000)


def test_h04_r08_s3_en_el_borde(est, tarifa, medida):
    """AG-11 puede llamarse 2 veces por tipo (refutación y contrarréplica): el ciclo medido hizo 1; con una más, en el
    borde, vale; con dos más, falla cerrado."""
    a11 = [x for x in medida if x["agente"] == "AG-11"]
    assert len(a11) == 1
    _cota(est, medida + [dict(a11[0])], tarifa)
    with pytest.raises(SystemExit, match="previstas"):
        _cota(est, medida + [dict(a11[0])] * 2, tarifa)


def test_h04_r09_precio_por_uc_con_la_lectura_de_cache(est):
    p = {"entrada": 1.0, "salida": 1.0, "escritura_cache": 1.0, "lectura_cache": 1.0}
    # una UC son 2·8 000 de entrada, 2·1 500 de salida o 2·8 000/0,1 de lectura: la lectura manda en esta tarifa
    assert est._usd_por_uc(p, (8000.0, 1500.0, 0.1)) == pytest.approx(2 * 8000 / 0.1 / 1e6)


# ---------------------------------------------------------------- H-05 · comprobar_datos_a.py, el último cierre inválido
@pytest.mark.parametrize("ultimo", ["n/d", -3, "repetida"])
def test_h05_historia_antigua_invalida_lleva_aviso(tmp_path, ultimo):
    cd = _modulo("comprobar_datos_a")
    cfg = cargar_config()
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    u = u[u["simbolo"] == "EURUSD=X"].reset_index(drop=True)
    filas = [("2026-01-02", 1.1), ("2026-01-05", 1.2)]
    filas.append(("2026-01-05", 1.3) if ultimo == "repetida" else ("2026-01-06", ultimo))
    pd.DataFrame(filas, columns=["fecha", "cierre"]).to_csv(tmp_path / "EURUSD=X.csv", index=False)
    f = cd.comprobar(tmp_path, u, "2030-06-28", "H3", cfg)[0]
    assert f["estado"] == "ANTIGUO" and f["aviso"].startswith("dato inválido en la historia")


def test_h05_historia_antigua_valida_sin_aviso(tmp_path):
    cd = _modulo("comprobar_datos_a")
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    u = u[u["simbolo"] == "EURUSD=X"].reset_index(drop=True)
    pd.DataFrame([("2026-01-02", 1.1), ("2026-01-05", 1.2)], columns=["fecha", "cierre"]).to_csv(tmp_path / "EURUSD=X.csv", index=False)
    f = cd.comprobar(tmp_path, u, "2030-06-28", "H3", cargar_config())[0]
    assert f["estado"] == "ANTIGUO" and f["aviso"] == "" and f["hasta"] == "2026-01-05"


# ---------------------------------------------------------------- H-06 · el borrador del Anexo B
def test_h06_el_borrador_cita_donde_estan_coincide_e_independiente():
    texto = (REPO / ".docs" / "diseno" / "bloque_a" / "borrador_correccion_anexo_b.md").read_text(encoding="utf-8")
    linea = next(x for x in texto.splitlines() if "Lo que el Anexo B deja abierto" in x)
    assert "`motor/servicio.py`" in linea and "_registrar_evidencia_clase" in linea and "esquemas_respuestas.json" not in linea
    r = subprocess.run([sys.executable, str(SCRIPTS / "borrador_anexo_b.py"), "--comprobar"], cwd=REPO, capture_output=True, check=False)
    assert r.returncode == 0


# ---------------------------------------------------------------- H-07 · INC-T129-01 al día
def test_h07_inc_t129_01_limites_del_estimador_al_dia():
    texto = (REPO / "docs" / "incidencias.md").read_text(encoding="utf-8")
    inc = texto[texto.index("**INC-T129-01"):]
    inc = inc[:inc.index("\n\n**INC-")]
    limites = next(x for x in inc.splitlines() if x.startswith("- **Límites del estimador"))
    assert "Cuenta las reparaciones de JSON" in limites and "S4b" in limites
    assert "no cuenta lo que lee cada búsqueda web, reintentos ni reparaciones" not in inc
    assert "Ronda T-148" in inc and "Con T-146 integrado" in inc
