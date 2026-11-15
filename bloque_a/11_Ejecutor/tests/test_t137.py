"""T-137 · Hallazgos de las QA r02 de T-131, r01 de T-136 y r01 de T-134."""
import importlib.util
import random
import shutil
from pathlib import Path

import pandas as pd
import pytest
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.contratos import ibanes_en_texto, tarjetas_en_texto
from bloque_a.evaluador import (
    _fecha_de_calendario,
    motivo_pronostico_fuente_no_registrable,
)
from bloque_a.herramientas.ht01_datos import cargar_universo
from conftest import AS_OF, DATOS
from test_t125_r02 import FUENTE_A, _bloque, _clm, _pf, _valor

SCRIPTS = Path(__file__).resolve().parents[3] / ".docs" / "scripts"
V, M = "4111 1111 1111 1111", "5555 5555 5555 4444"   # números de prueba publicados


def _modulo(nombre):
    spec = importlib.util.spec_from_file_location(nombre, SCRIPTS / f"{nombre}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- T-136 H-02 · tarjeta junto a otro número de 4 cifras
@pytest.mark.parametrize("texto,esperado", [
    (V + " 0128", ["tarjeta …1111"]), ("2027 " + V, ["tarjeta …1111"]), ("4111-1111-1111-1111-0128", ["tarjeta …1111"]),
    (V + " " + M, ["tarjeta …1111", "tarjeta …4444"]), (V + " 1999", ["tarjeta …1111"]),
])
def test_h02_tarjeta_con_caducidad_ano_o_otra_tarjeta(texto, esperado):
    assert tarjetas_en_texto(texto) == esperado


def test_c12_cinco_grupos_que_no_son_fecha_no_se_marcan():
    # límite declarado (INC-T123-01): una tarjeta seguida de un número de 4 cifras que no es una fecha se toma por una fila
    assert tarjetas_en_texto(V + " 9999") == []
    r = random.Random(4)
    assert not any(tarjetas_en_texto(" ".join(str(r.randint(4000, 5999)) for _ in range(5))) for _ in range(5000))


# ---------------------------------------------------------------- T-136 H-04 · mutante C03 (palabra de más de 4 letras)
def _iban(pais, bban):
    num = "".join(str(int(c, 36)) for c in bban + pais + "00")
    return f"{pais}{98 - int(num) % 97:02d}{bban}"


def test_c03_una_palabra_en_mayusculas_no_es_un_tramo_de_iban():
    iban = _iban("LU", "123" + "ABCDE" + "12345678")          # LU: 3n13c; «ABCDE» cabe en el tramo alfanumérico
    assert ibanes_en_texto(iban) == [iban]                       # junto sí (forma válida)
    assert ibanes_en_texto(f"{iban[:4]} 123 ABCDE 12345678") == []   # en grupos, «ABCDE» es una palabra


# ---------------------------------------------------------------- T-136 H-01 · cota con reparaciones
def test_h01_la_cota_suma_las_reparaciones_peticion_a_peticion():
    est = _modulo("estimar_coste_ciclo_a")
    precios = {"m": {"entrada": 2.0, "salida": 10.0, "escritura_cache": 4.0, "lectura_cache": 0.1}}
    ll = [{"agente": "AG-03", "modelo": "m", "sys_tok": 900_000, "user_tok": 100_000, "out_tok": 0, "max_tokens": 100_000,
           "cache_escr": 0, "cache_lect": 0}]
    sin = est.estimar(ll, precios, 10.0, set(), 5)["cota_superior"]
    con = est.estimar(ll, precios, 10.0, set(), 5, reparaciones=1)["cota_superior"]
    assert sin == pytest.approx(1.0 * 4 + 1.0)                   # 1 M como escritura + 0,1 M de salida
    assert con == pytest.approx(sin + (1.0 + 0.1) * 4 + 1.0)     # la reparación reenvía la salida anterior


# ---------------------------------------------------------------- T-131 H-05 · la ventana del ciclo
@pytest.fixture(scope="module")
def comprobar():
    return _modulo("comprobar_datos_a").comprobar


def _carpeta_con_dato_malo(tmp_path, fecha):
    u = cargar_universo(RUTA_UNIVERSO_EJEMPLO).head(1)
    d = tmp_path / "datos"
    d.mkdir()
    s = u["simbolo"].iloc[0]
    shutil.copy(Path(DATOS) / f"{s}.csv", d / f"{s}.csv")
    df = pd.read_csv(d / f"{s}.csv")
    df["cierre"] = df["cierre"].astype(object)
    fechas = pd.to_datetime(df["fecha"])
    df.loc[fechas == fechas[fechas >= fecha].min(), "cierre"] = "n/d"
    df.to_csv(d / f"{s}.csv", index=False)
    return d, u


def test_h05_un_dato_malo_anterior_a_la_ventana_deja_ok_con_aviso(tmp_path, comprobar):
    d, u = _carpeta_con_dato_malo(tmp_path, "2022-06-01")
    f = comprobar(d, u, "2026-06-30")[0]
    assert f["estado"] == "OK" and "anterior a la ventana" in f["aviso"]


def test_h05_un_dato_malo_dentro_de_la_ventana_es_invalido(tmp_path, comprobar):
    d, u = _carpeta_con_dato_malo(tmp_path, "2025-06-02")
    assert comprobar(d, u, "2026-06-30")[0]["estado"] == "INVALIDO"


# ---------------------------------------------------------------- T-134 H-19 · año 0
class _Refs:
    def por_id(self, ref_id):
        return {"archivo": "F9"} if ref_id.startswith("REF-RF-") else None


def test_h19_una_fecha_fuera_del_calendario_no_se_lee_ni_se_registra():
    with pytest.raises(ValueError):
        _fecha_de_calendario("0000-01-01")
    pf = {"ref_id": "REF-RF-0001", "variable": "cierre", "serie_ht01": "SPY", "fecha_objetivo": "2026-09-30",
          "umbral_o_rango": 100.0, "direccion": "por_encima", "probabilidad": 0.7, "fecha_emision": "0000-01-01"}
    assert motivo_pronostico_fuente_no_registrable(pf, "REF-RF-0001", "2026-06-05", _Refs(), ["cierre"]) is not None


def test_h19_en_f2_no_hace_perder_los_demas(tmp_path, universo):
    b = _bloque(tmp_path, universo)
    f = "2025-03-03"
    _clm(b, "CLM-2025-0941", _pf(FUENTE_A, f, _valor(b, f) - 1))
    malo = _pf(FUENTE_A, "2025-03-04", 1.0, emision="2025-02-01")
    _clm(b, "CLM-2025-0942", malo)
    malo2 = dict(malo, fecha_emision="0000-01-01")
    _clm(b, "CLM-2025-0943", malo2, registro="2025-02-01")
    assert [p["clm_id"] for p in b.evaluador.pronosticos_de_fuentes(AS_OF)][:1] == ["CLM-2025-0941"]
