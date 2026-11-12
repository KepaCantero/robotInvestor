"""T-103: regresiones de H-40 a H-44 de la QA r01 de T-93 (`.docs/tickets/T-93/qa.md`).

Sin red ni claves: las claves de prueba se arman en tiempo de ejecución para que el escáner de secretos del repositorio no
las tome por reales. Los casos son los de `.docs/tickets/T-93/revisores/r01_01_r8_escapes.py`, `r01_02_almacen_legado.py` y
`r01_03_plazos_tipos.py`.
"""
import datetime as dt
import json
import random
import string
import urllib.parse

import pytest
from bloque_a.almacen import Almacen
from bloque_a.contratos import contiene_credenciales
from bloque_a.llm import contenido_sensible
from conftest import nuevo_bloque

SK = "s" + "k-"
CLAVE = SK + "ant-api03-" + "msUpBNeqXSNZ0e2m" * 6 + "AA"


# ---------------------------------------------------------------------------------------------- H-40: escapes dobles y largos
@pytest.mark.parametrize("nombre,texto", [
    ("doble_n", json.dumps({"x": json.dumps({"nota": "línea\n" + CLAVE})})),
    ("doble_t", json.dumps({"x": json.dumps({"nota": "a\t" + CLAVE})})),
    ("doble_r", json.dumps({"x": json.dumps({"nota": "a\r" + CLAVE})})),
    ("doble_barra", json.dumps({"x": json.dumps({"url": "https://a.example/" + CLAVE}).replace("/", "\\/")})),
    ("doble_u00ab", json.dumps({"x": json.dumps({"nota": "«" + CLAVE})})),
    ("doble_nbsp", json.dumps({"x": json.dumps({"nota": "clave:\u00a0" + CLAVE})})),
    ("url_dos_veces", "u=" + urllib.parse.quote(urllib.parse.quote("https://a.example/?key=" + CLAVE, safe=""), safe="")),
    ("barra_literal_ruta", "ruta C:\\\\n" + CLAVE),
    ("ascii_emoji", ascii("🔑" + CLAVE)),
    ("repr_fuera_del_bmp", repr("\U000f0000" + CLAVE)),
    ("escape_javascript", "nota=%u2014" + CLAVE),
    ("octal", "nota \\253" + CLAVE),
])
def test_h40_ningun_escape_doble_o_largo_oculta_la_clave(nombre, texto):
    assert contenido_sensible(texto), nombre


def test_h40_clave_de_dict_con_barra_literal():
    obj = {"nota\\n" + CLAVE: 1}
    assert contenido_sensible(obj) and contiene_credenciales(obj)


# ---------------------------------------------------------------------------------------------- H-41: colas de solo cifras
@pytest.mark.parametrize("n,k", [(5, 5), (6, 4), (8, 4)])
def test_h41_una_cola_de_tramos_de_cifras_es_clave(n, k):
    rnd = random.Random(20261112 + n * k)
    claves = [SK + "-".join("".join(rnd.choice(string.digits) for _ in range(n)) for _ in range(k)) for _ in range(200)]
    assert all(contenido_sensible("clave: " + c) for c in claves)


@pytest.mark.parametrize("texto", [
    "https://www.example.com/news/sk-telecom-q2-2024-earnings",
    "https://www.reuters.com/technology/sk-hynix-q2-profit-jumps-on-ai-chip-demand-2024-07-25/",
    "Descarga: sk-hynix_20240725_earnings_release.pdf",
])
def test_h41_el_texto_con_fechas_sigue_sin_ser_clave(texto):
    assert not contenido_sensible(texto)


# ---------------------------------------------------------------------------------------------- H-44: frozenset
def test_h44_contiene_credenciales_recorre_frozenset():
    assert contiene_credenciales({"x": frozenset({"\n" + CLAVE})}) and contiene_credenciales({"x": frozenset({"«" + CLAVE})})


# ---------------------------------------------------------------------------------------------- H-42: registro sin «\n» final
def _tres(tmp):
    a = Almacen(tmp)
    for k in ("uno", "dos", "tres"):
        a.escribir("F5", "AG-01", {"id": k, "nota": "año «ñ» — fin"})
    return next(tmp.glob("F5*"))


def _quitar_ultimo_salto(f5):
    datos = f5.read_bytes()
    assert datos.endswith(b"\n")
    f5.write_bytes(datos[:-1])


def test_h42_almacen_legado_con_el_ultimo_registro_sin_salto(tmp_path):
    f5 = _tres(tmp_path)
    (tmp_path / "sellos_integridad.json").unlink()
    (tmp_path / "formato_almacen.json").unlink()
    _quitar_ultimo_salto(f5)
    a = Almacen(tmp_path)
    assert list(a.estado("F5")) == ["uno", "dos", "tres"]
    a.escribir("F5", "AG-01", {"id": "cuatro"})
    assert list(Almacen(tmp_path).estado("F5")) == ["uno", "dos", "tres", "cuatro"]


def test_h42_almacen_sellado_con_el_ultimo_registro_sin_salto(tmp_path):
    f5 = _tres(tmp_path)
    _quitar_ultimo_salto(f5)
    a = Almacen(tmp_path)
    a.escribir("F5", "AG-01", {"id": "cuatro"})
    a.escribir("F5", "AG-01", {"id": "cinco"})
    assert list(Almacen(tmp_path).estado("F5")) == ["uno", "dos", "tres", "cuatro", "cinco"]
    assert f5.read_bytes().count(b"\n") == 5 and f5.read_bytes().endswith(b"\n")


# ---------------------------------------------------------------------------------------------- H-43: CNS sin plazo
def test_h43_una_consulta_sin_plazo_vence_con_incidencia(tmp_path, universo):
    """Caso 3b de `r01_03`: un CNS ENVIADA y SALIENTE sin el campo (estado manipulado o de otra versión)."""
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(dt.date(2026, 6, 5))
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS", "id": "CNS-2026-9999", "cns_id": "CNS-2026-9999", "sentido": "SALIENTE",
                                       "estado": "ENVIADA", "modo": "BLOQUEANTE", "clases": ["RV"],
                                       "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}]})
    assert b.consultas.vencer("2026-06-06T09:00") == ["CNS-2026-9999"]
    assert any("CNS-2026-9999" in str(e.get("detalle")) and e.get("tipo") == "DATOS" for e in b.almacen.leer("HA"))
    assert b.consultas.vencer("2026-06-07T09:00") == []
