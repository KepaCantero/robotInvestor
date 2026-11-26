"""T-206 · El `tipo` de una incidencia (INC-) de HA es el del esquema de HA V2.0 (4.8).

Hasta T-206 el ejecutor escribía `tipo` DATOS en ocho sitios (`interfaz_broker.py` 2, `orquestacion.py` 4, `fiabilidad_f9.py`
2), que el esquema no admite, y `Almacen.incidencia` no comprobaba el tipo. Ahora `incidencia` falla cerrado ante un tipo
fuera del enumerado, sin escribir nada; los problemas de datos son OTRO con `categoria` DATOS (INC-T206-01 [PROPUESTO]) y
`es_incidencia_de_datos` reconoce también las entradas de antes (`tipo` DATOS) de los almacenes existentes.
"""
import ast
import datetime as dt
import re
import types
import unicodedata
from pathlib import Path

import jsonschema
import pytest
from bloque_a.almacen import (
    ARCHIVOS,
    CATEGORIA_DATOS,
    TIPOS_INCIDENCIA,
    Almacen,
    EscrituraFueraDeReserva,
    Reloj,
    TipoIncidenciaNoAdmitido,
    es_incidencia_de_datos,
)
from bloque_a.configuracion import cargar_config
from bloque_a.fiabilidad_f9 import FiabilidadNoAtendible
from bloque_a.herramientas.ht01_datos import DatosInvalidos
from conftest import AS_OF, RAIZ, config_pruebas, nuevo_bloque
from test_t125_fiabilidad_fuentes import _sembrar

from bloque_a import fiabilidad_f9

ESQUEMA_HA = RAIZ.parent / "05_Archivos_operativos" / unicodedata.normalize("NFC", "Historial de auditorías (esquema V2.0).md")
PAQUETE = RAIZ / "bloque_a"
FUENTE = "REF-RF-0001"     # fuente de F9 (corpus)


def _tipos_del_esquema() -> list[str]:
    """El enumerado de `tipo` de la INC- tal como lo escribe el esquema de HA (4.8), leído del corpus congelado."""
    (linea,) = [x for x in ESQUEMA_HA.read_text(encoding="utf-8").splitlines() if x.startswith("- `INC-`:")]
    (lista,) = re.findall(r"`tipo` \(([^)]*)\)", linea)
    return [t.strip() for t in lista.split("·")]


def _esquema_inc() -> dict:
    """Esquema JSON de una INC- hecho del esquema de HA (no hay un esquema JSON de HA en el corpus): `tipo` del enumerado
    de 4.8, los campos de 4.8 que escribe el ejecutor y, si la lleva, `categoria` DATOS (INC-T206-01)."""
    return {"type": "object",
            "required": ["tipo_entrada", "id", "tipo", "severidad", "objeto", "tratamiento"],
            "properties": {"tipo_entrada": {"const": "INC"}, "id": {"type": "string", "pattern": r"^INC-\d{4}-\d{4}$"},
                           "tipo": {"enum": _tipos_del_esquema()}, "severidad": {"type": "string"},
                           "objeto": {"type": "string"}, "tratamiento": {"type": "string"},
                           "categoria": {"const": CATEGORIA_DATOS}}}


def _incs(almacen) -> list[dict]:
    return [e for e in almacen.leer("HA") if e.get("tipo_entrada") == "INC"]


def _comprobar_de_datos(nuevas: list[dict], texto: str) -> dict:
    """Una sola INC- nueva con `texto`, de un tipo del esquema, de datos y conforme al esquema JSON de la INC-."""
    (inc,) = [e for e in nuevas if texto in str(e.get("detalle"))]
    assert inc["tipo"] in _tipos_del_esquema() and inc["tipo"] == "OTRO"
    assert inc["categoria"] == CATEGORIA_DATOS and es_incidencia_de_datos(inc)
    jsonschema.validate(inc, _esquema_inc())
    return inc


def _estado_en_disco(carpeta: Path) -> dict:
    return {p.name: p.read_bytes() for p in sorted(carpeta.iterdir()) if p.is_file()}


# ---------------------------------------------------------------- CA-1 · el enumerado es el del esquema, en un solo sitio
def test_ca1_el_enumerado_del_codigo_es_el_del_esquema_de_ha():
    assert list(TIPOS_INCIDENCIA) == _tipos_del_esquema()
    assert "DATOS" not in TIPOS_INCIDENCIA and "OTRO" in TIPOS_INCIDENCIA


def test_ca1_el_enumerado_solo_se_escribe_en_almacen():
    """Ningún otro módulo del paquete repite la lista (un único sitio que cita el esquema): ninguna tupla, lista o conjunto
    literal con tres o más tipos del enumerado fuera de `almacen.py`."""
    con_la_lista = set()
    for p in sorted(PAQUETE.rglob("*.py")):
        for nodo in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
            if isinstance(nodo, (ast.Tuple, ast.List, ast.Set)):
                tipos = {e.value for e in nodo.elts if isinstance(e, ast.Constant) and e.value in TIPOS_INCIDENCIA}
                if len(tipos) >= 3:
                    con_la_lista.add(p.relative_to(PAQUETE).as_posix())
    assert con_la_lista == {"almacen.py"}


def test_ca1_todas_las_llamadas_del_paquete_usan_un_tipo_del_esquema():
    """Lectura estática de cada `incidencia(…)` y `_incidencia_interna(…)` del paquete: el tipo es un literal del enumerado
    (o la constante de los de datos) y ninguna escribe DATOS."""
    vistos, fuera = set(), []
    for p in sorted(PAQUETE.rglob("*.py")):
        for nodo in ast.walk(ast.parse(p.read_text(encoding="utf-8"))):
            if not (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute)
                    and nodo.func.attr in ("incidencia", "_incidencia_interna")):
                continue
            arg = nodo.args[0] if nodo.args else None
            if isinstance(arg, ast.Constant) and arg.value in TIPOS_INCIDENCIA:
                vistos.add(arg.value)
            elif isinstance(arg, ast.Name) and arg.id == "TIPO_INCIDENCIA_DATOS" and p.name == "almacen.py":
                vistos.add("OTRO")
            else:
                fuera.append(f"{p.name}:{nodo.lineno}")
    assert fuera == []
    assert {"CANAL_NO_PREVISTO", "HERRAMIENTA", "MANIPULACION", "OTRO", "SEGURIDAD", "ACCESO_FUERA_DE_MATRIZ",
            "ESCRITURA"} <= vistos


# ---------------------------------------------------------------- CA-2 · un tipo fuera del enumerado falla cerrado
class _Permisivo:
    """Cierre de la QA r01 (H-02): un objeto cuyo == da siempre True pasa `in TIPOS_INCIDENCIA`."""

    def __eq__(self, otro):
        return True

    __hash__ = object.__hash__


class _TextoPermisivo(str):
    """Cierre de la QA r01 (H-02): una subclase de str con == permisivo pasa `isinstance` y `in`."""

    def __eq__(self, otro):
        return True

    __hash__ = str.__hash__


@pytest.mark.parametrize("tipo", ["DATOS", "", None, "otro", "OTRO ", " SEGURIDAD", "HERRAMIENTAS", 7, ["OTRO"], ("OTRO",),
                                  _Permisivo(), _TextoPermisivo("DATOS")])
def test_ca2_un_tipo_fuera_del_esquema_falla_cerrado_sin_escribir_nada(tmp_path, tipo):
    alm = Almacen(tmp_path, Reloj())
    alm.reloj.fijar(AS_OF)
    alm.incidencia("OTRO", "una previa")
    antes = _estado_en_disco(tmp_path)
    with pytest.raises(TipoIncidenciaNoAdmitido, match="fuera del esquema de HA"):
        alm.incidencia(tipo, "no debe quedar", "AG-18", severidad="Operativa", run_id="RUN-2026-0001")
    with pytest.raises(TipoIncidenciaNoAdmitido):
        alm._incidencia_interna(tipo, "tampoco", "AG-18")
    assert _estado_en_disco(tmp_path) == antes                       # ni la entrada, ni el contador de INC-, ni el sello
    assert len(_incs(Almacen(tmp_path, Reloj()))) == 1
    assert alm.nuevo_id("INC") == "INC-2026-0002"                     # el contador no se gastó


def test_ca2_el_rechazo_es_un_error_propio_y_no_cita_mas_que_el_tipo(tmp_path):
    alm = Almacen(tmp_path, Reloj())
    alm.reloj.fijar(AS_OF)
    with pytest.raises(TipoIncidenciaNoAdmitido) as e:
        alm.incidencia("DATOS", "detalle con algo que no debe salir en el error")
    assert isinstance(e.value, ValueError) and "detalle" not in str(e.value) and "'DATOS'" in str(e.value)
    assert not (tmp_path / ARCHIVOS["HA"]).exists() or _incs(alm) == []


@pytest.mark.parametrize("tipo", TIPOS_INCIDENCIA)
def test_ca2_cada_tipo_del_esquema_se_escribe(tmp_path, tipo):
    alm = Almacen(tmp_path, Reloj())
    alm.reloj.fijar(AS_OF)
    inc = alm.incidencia(tipo, "detalle", "AG-18")
    assert inc["tipo"] == tipo and "categoria" not in inc
    jsonschema.validate(inc, _esquema_inc())


def test_ca2_la_de_datos_no_admite_otra_categoria(tmp_path):
    alm = Almacen(tmp_path, Reloj())
    alm.reloj.fijar(AS_OF)
    with pytest.raises(TypeError):
        alm.incidencia_de_datos("detalle", "AG-18", categoria="OTRA")
    assert not (tmp_path / ARCHIVOS["HA"]).exists() or _incs(alm) == []
    inc = alm.incidencia_de_datos("detalle", "AG-18", severidad="Operativa", tratamiento="t", run_id="RUN-2026-0001")
    assert (inc["tipo"], inc["categoria"], inc["severidad"], inc["objeto"], inc["tratamiento"], inc["run_id"]) == (
        "OTRO", "DATOS", "Operativa", "AG-18", "t", "RUN-2026-0001")


@pytest.mark.parametrize("tipo, categoria", [("SEGURIDAD", "DATOS"), ("HERRAMIENTA", "DATOS"), ("OTRO", "OTRA"), ("OTRO", "datos"),
                                             ("OTRO", None), ("OTRO", _TextoPermisivo("DATOS")), ("OTRO", _Permisivo())])
def test_ca2_categoria_solo_en_la_pareja_otro_datos_falla_cerrado_sin_escribir_nada(tmp_path, tipo, categoria):
    """Cierre de la QA r01 (H-03): `categoria` solo va con la pareja OTRO + DATOS; cualquier otra combinación se rechaza
    antes de pedir el id."""
    alm = Almacen(tmp_path, Reloj())
    alm.reloj.fijar(AS_OF)
    alm.incidencia("OTRO", "una previa")
    antes = _estado_en_disco(tmp_path)
    with pytest.raises(TipoIncidenciaNoAdmitido, match="Categoría"):
        alm.incidencia(tipo, "no debe quedar", "AG-18", categoria=categoria)
    assert _estado_en_disco(tmp_path) == antes
    assert alm.nuevo_id("INC") == "INC-2026-0002"
    assert alm.incidencia("OTRO", "la pareja sí", "AG-18", categoria="DATOS")["categoria"] == "DATOS"


@pytest.mark.parametrize("entrada", [{"tipo": "DATOS"}, {}, {"tipo": None}, {"tipo": "otro"}, {"tipo": _TextoPermisivo("DATOS")},
                                     {"tipo": "SEGURIDAD", "categoria": "DATOS"}, {"tipo": "OTRO", "categoria": "OTRA"}])
def test_ca2_escribir_rechaza_una_inc_montada_a_mano_fuera_del_esquema(tmp_path, entrada):
    """Cierre de la QA r01 (H-04): la escritura genérica también comprueba el tipo (y la categoría) de una INC- de HA, sin
    escribir nada; las demás entradas de HA no cambian."""
    alm = Almacen(tmp_path, Reloj())
    alm.reloj.fijar(AS_OF)
    alm.incidencia("OTRO", "una previa")
    antes = _estado_en_disco(tmp_path)
    base = {"tipo_entrada": "INC", "id": "INC-2026-0099", "severidad": "Menor", "objeto": "x", "tratamiento": "registrada"}
    with pytest.raises(EscrituraFueraDeReserva):
        alm.escribir("HA", "AG-18", {**base, **entrada})
    assert _estado_en_disco(tmp_path) == antes
    assert alm.escribir("HA", "AG-18", {**base, "tipo": "OTRO", "categoria": "DATOS"})["tipo"] == "OTRO"
    assert alm.escribir("HA", "AG-18", {"tipo_entrada": "GUI", "id": "GUI-AG02-0001", "estado": "RETIRADA"})["_autor"] == "AG-18"


# ---------------------------------------------------------------- CA-3 · los ocho caminos escriben un tipo del esquema
def _conserva(inc: dict, objeto, severidad, tratamiento, run_id=None, **marcas) -> None:
    """Cierre de la QA r01 (H-05): cada camino conserva el objeto, la severidad, el tratamiento, el run_id y sus marcas de
    develop (los que no lleva, ausentes)."""
    esperado = {"objeto": objeto, "severidad": severidad, "tratamiento": tratamiento, "run_id": run_id,
                "escalado_operador": marcas.get("escalado_operador"), "fue_no_atendible": marcas.get("fue_no_atendible")}
    assert {k: inc.get(k) for k in esperado} == esperado


def test_ca3_broker_revision_c2_sin_tipos_que_revisar(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    cns = b.consultas.enviar({"tipo": "ACLARACION_ALCANCE", "modo": "NO_BLOQUEANTE", "clases": [],
                              "preguntas": [{"texto": "¿Incluimos stablecoins?", "supuesto_declarado": "No se incluyen",
                                             "efecto_si_falso": "Se ampliaría el cribado de CRI"}]}, AS_OF)["cns_id"]
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "RUN", "id": "RUN-2026-0900", "entrega": "ENTREGADA", "supuestos_cns": [cns]})
    antes = len(_incs(b.almacen))
    out = b.consultas.responder(cns, [{"indice": 0, "texto": "Sí"}], as_of=AS_OF)
    assert out["revision_c2"]["estado"] == "SIN_ALCANCE"
    inc = _comprobar_de_datos(_incs(b.almacen)[antes:], "no tiene tipos de activo que revisar")
    _conserva(inc, "AG-01", "Material", f"revisar a mano el alcance de la revisión C2 de {cns}", escalado_operador=True)


def test_ca3_broker_consulta_con_plazo_ilegible(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(dt.date(2026, 6, 5))
    b.almacen.escribir("F5", "AG-01", {"tipo_entrada": "CNS", "id": "CNS-2026-9999", "cns_id": "CNS-2026-9999", "sentido": "SALIENTE",
                                       "estado": "ENVIADA", "modo": "BLOQUEANTE", "clases": ["RV"],
                                       "preguntas": [{"texto": "¿RV?", "supuesto_declarado": "esperar"}]})
    antes = len(_incs(b.almacen))
    assert b.consultas.vencer("2026-06-06T09:00") == ["CNS-2026-9999"]
    inc = _comprobar_de_datos(_incs(b.almacen)[antes:], "CNS-2026-9999 con un plazo que no se puede leer")
    _conserva(inc, "AG-01", "Material", "registrada")


def test_ca3_orquestacion_referencia_de_comparacion_invalida(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    monkeypatch.setattr(b, "_referencia_invalida", lambda ref, ini, as_of: "cierre no positivo simulado")
    with pytest.raises(DatosInvalidos, match="referencia de comparación"):
        b.senales_clase("RV", AS_OF, "RUN-2026-0001")
    inc = _comprobar_de_datos(_incs(b.almacen), "referencia de comparación")
    ref = b._referencia("RV")
    assert ref and f"referencia de comparación {ref} de RV" in inc["detalle"]
    _conserva(inc, ref, "Operativa", "tipo de activo PARCIAL y declarado", "RUN-2026-0001")


def test_ca3_orquestacion_datos_invalidos_de_un_simbolo(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    valor_en = b.proveedor.valor_en

    def malo(simbolo, fecha):
        if simbolo == "EURUSD=X":
            raise DatosInvalidos("HT-01: cierre no positivo simulado")
        return valor_en(simbolo, fecha)
    monkeypatch.setattr(b.proveedor, "valor_en", malo)
    sen, _ = b.senales_clase("DIV", AS_OF, "RUN-2026-0001")
    assert "EURUSD=X" not in sen and sen
    inc = _comprobar_de_datos(_incs(b.almacen), "HT-01: datos inválidos de EURUSD=X")
    _conserva(inc, "EURUSD=X", "Operativa", "símbolo excluido y declarado como laguna del tipo", "RUN-2026-0001")


def test_ca3_orquestacion_ct19_no_atendido_por_el_buscador(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas())
    b.fijar_fecha(AS_OF)
    _sembrar(b, FUENTE, 20, 5)
    b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")

    def no_cuadra(msg, f6, referencias, as_of=None):
        raise FiabilidadNoAtendible("prueba")
    monkeypatch.setattr(fiabilidad_f9, "comprobar_ct19", no_cuadra)
    antes = len(_incs(b.almacen))
    assert b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0001") == []
    inc = _comprobar_de_datos(_incs(b.almacen)[antes:], "no atendido por el Buscador")
    _conserva(inc, "AG-16", "Operativa", "registrada", "RUN-2026-0001")


def test_ca3_orquestacion_pronostico_de_fuente_no_registrable(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    pieza = {"pronostico_fuente": {"ref_id": FUENTE}, "fuente": FUENTE, "afirmacion": "SPY sube", "origen": "AG-03"}
    assert b._tipo_con_pronostico_fuente("PRONOSTICO_FUENTE", pieza, AS_OF, "RUN-2026-0001") == "PREVISION"
    inc = _comprobar_de_datos(_incs(b.almacen), "Pronóstico de fuente no registrable")
    _conserva(inc, "AG-03", "Menor", "registrada", "RUN-2026-0001")


def test_ca3_fiabilidad_f9_sin_fichas_de_f9(tmp_path):
    alm = Almacen(tmp_path, Reloj())
    alm.reloj.fijar(AS_OF)
    refs = types.SimpleNamespace(fichas={"F9": []})
    assert fiabilidad_f9.apartar_no_atendibles(alm, [{"fue_id": "FUE-2026-0001", "ref_id": FUENTE}], refs, "RUN-2026-0002") == []
    inc = _comprobar_de_datos(_incs(alm), "F9 no se pudo leer")
    _conserva(inc, "AG-16", "Operativa", "sin marca; reintento en el ciclo siguiente", "RUN-2026-0002")
    assert fiabilidad_f9.no_atendibles(alm) == set()


def test_ca3_fiabilidad_f9_fuente_que_ya_no_es_de_f9(tmp_path):
    alm = Almacen(tmp_path, Reloj())
    alm.reloj.fijar(AS_OF)
    refs = types.SimpleNamespace(fichas={"F9": [{"ref_id": "REF-RF-0003"}]}, por_id=lambda r: None)
    assert fiabilidad_f9.apartar_no_atendibles(alm, [{"fue_id": "FUE-2026-0001", "ref_id": FUENTE}], refs, "RUN-2026-0002") == []
    inc = _comprobar_de_datos(_incs(alm), "ya no es de F9")
    _conserva(inc, "AG-16", "Operativa", "declarada una vez; excluida de los CT-19 siguientes", "RUN-2026-0002",
              fue_no_atendible="FUE-2026-0001")
    assert fiabilidad_f9.no_atendibles(alm) == {"FUE-2026-0001"}


# ---------------------------------------------------------------- CA-4 · un HA de antes de T-206, con DATOS, se sigue leyendo
def _sin_comprobar_tipo(monkeypatch):
    """Cierre de la QA r01 (H-04): `escribir` ya no admite una INC- con DATOS; para montar un almacén como lo dejaba el
    ejecutor de antes de T-206 se desactiva la comprobación solo mientras se monta (el contexto lo deshace al salir)."""
    ctx = monkeypatch.context()
    m = ctx.__enter__()
    m.setattr(Almacen, "_comprobar_tipo_incidencia", staticmethod(lambda tipo, extra=None: None))
    return ctx


def _ha_antiguo(carpeta: Path, monkeypatch) -> None:
    """Un almacén escrito por el ejecutor de antes de T-206: incidencias con `tipo` DATOS."""
    ctx = _sin_comprobar_tipo(monkeypatch)
    try:
        alm = Almacen(carpeta, Reloj())
        alm.reloj.fijar("2026-05-29")
        for n, extra in ((1, {"fue_no_atendible": "FUE-2026-0001", "run_id": "RUN-2026-0001"}),
                         (2, {"escalado_operador": True, "tratamiento": "revisar a mano el alcance de la revisión C2 de CNS-2026-0001"})):
            alm.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": alm.nuevo_id("INC"), "tipo": "DATOS", "severidad": "Operativa",
                                         "objeto": "AG-16" if n == 1 else "AG-01", "detalle": f"incidencia de datos antigua {n}",
                                         "tratamiento": "registrada", **extra})
    finally:
        ctx.__exit__(None, None, None)


def test_ca4_un_ha_antiguo_con_datos_se_abre_integro_y_se_reconoce(tmp_path, monkeypatch):
    _ha_antiguo(tmp_path, monkeypatch)
    alm = Almacen(tmp_path, Reloj())
    alm.reloj.fijar(AS_OF)
    with pytest.raises(EscrituraFueraDeReserva):          # la comprobación vuelve a estar activa
        alm.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": "INC-2026-0099", "tipo": "DATOS"})
    assert all(alm.verificar_integridad().values())
    alm.incidencia_de_datos("incidencia de datos nueva", "AG-16", severidad="Operativa", fue_no_atendible="FUE-2026-0002")
    alm.incidencia("HERRAMIENTA", "otra que no es de datos", "AG-20")
    de_datos = [e["detalle"] for e in alm.leer("HA") if es_incidencia_de_datos(e)]
    assert de_datos == ["incidencia de datos antigua 1", "incidencia de datos antigua 2", "incidencia de datos nueva"]
    assert [e["tipo"] for e in _incs(alm)] == ["DATOS", "DATOS", "OTRO", "HERRAMIENTA"]   # lo antiguo no se reescribe
    assert fiabilidad_f9.no_atendibles(alm) == {"FUE-2026-0001", "FUE-2026-0002"}
    assert all(Almacen(tmp_path, Reloj()).verificar_integridad().values())


def test_ca4_el_lector_no_toma_otras_entradas_por_de_datos():
    assert not es_incidencia_de_datos({"tipo_entrada": "INC", "tipo": "OTRO"})
    assert not es_incidencia_de_datos({"tipo_entrada": "INC", "tipo": "OTRO", "categoria": "OTRA"})
    assert not es_incidencia_de_datos({"tipo_entrada": "INC", "tipo": "HERRAMIENTA", "categoria": "OTRA"})
    assert not es_incidencia_de_datos({"tipo_entrada": "INC", "tipo": "SEGURIDAD", "categoria": "DATOS"})   # H-03
    assert not es_incidencia_de_datos({"tipo_entrada": "INC", "tipo": "HERRAMIENTA", "categoria": "DATOS"})
    assert not es_incidencia_de_datos({"tipo_entrada": "INC", "categoria": "DATOS"})
    assert not es_incidencia_de_datos({"tipo_entrada": "HAL", "tipo": "DATOS"})
    assert not es_incidencia_de_datos({"tipo_entrada": "G3V", "categoria": "DATOS"})
    assert es_incidencia_de_datos({"tipo_entrada": "INC", "tipo": "DATOS"})
    assert es_incidencia_de_datos({"tipo_entrada": "INC", "tipo": "OTRO", "categoria": "DATOS"})


def test_ca4_las_fue_marcadas_en_un_ha_antiguo_no_vuelven_al_ct19(tmp_path, universo, monkeypatch):
    """La deduplicación de `fiabilidad_f9` (marca `fue_no_atendible`) sigue valiendo con una marca escrita antes de T-206."""
    b = nuevo_bloque(tmp_path, universo, cfg=config_pruebas())
    b.fijar_fecha(AS_OF)
    _sembrar(b, FUENTE, 20, 5)
    (fue,) = b.evaluador.fiabilidad_fuentes(AS_OF, "RUN-2026-0001")
    ctx = _sin_comprobar_tipo(monkeypatch)
    try:
        b.almacen.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": b.almacen.nuevo_id("INC"), "tipo": "DATOS",
                                           "severidad": "Operativa", "objeto": "AG-16", "detalle": "antigua",
                                           "tratamiento": "declarada una vez; excluida de los CT-19 siguientes",
                                           "fue_no_atendible": fue["fue_id"]})
    finally:
        ctx.__exit__(None, None, None)
    assert fiabilidad_f9.por_comunicar(b.almacen, AS_OF) == []
    assert b._comunicar_fiabilidad(b.reloj.fecha, "RUN-2026-0002") == []
    assert not [m for m in b.mensajeria.registro if m["contrato"] == "CT-19" and m["receptor"] == "AG-16"]


def test_ca4_el_estado_del_operador_muestra_las_escaladas_antiguas_y_las_nuevas(tmp_path, universo, monkeypatch):
    _ha_antiguo(tmp_path / "estado", monkeypatch)
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    b.almacen.incidencia_de_datos("nueva escalada", "AG-01", escalado_operador=True)
    b.almacen.incidencia("HERRAMIENTA", "escalada que no es de datos", "AG-01", escalado_operador=True)
    esc = b.estado()["incidencias_escaladas"]
    assert [(e["tipo"], e["detalle"]) for e in esc] == [
        ("DATOS", "incidencia de datos antigua 2"), ("OTRO", "nueva escalada"), ("HERRAMIENTA", "escalada que no es de datos")]
    # cierre de la QA r01 (H-06): la categoría llega al operador solo cuando la INC- la lleva
    assert [e.get("categoria", "—") for e in esc] == ["—", "DATOS", "—"]


def test_ca4_la_documentacion_ya_no_habla_de_incidencias_datos():
    """Cierre de la QA r01 (H-06): el README del ejecutor y el código no describen el tipo antiguo como el actual."""
    for f in (RAIZ / "README.md", PAQUETE / "orquestacion.py", PAQUETE / "fiabilidad_f9.py"):
        assert "incidencia DATOS" not in f.read_text(encoding="utf-8"), f.name


# ---------------------------------------------------------------- CA-5 · regresión: ciclo simulado con la configuración por defecto
def test_ca5_ciclo_mock_por_defecto_con_un_dato_invalido_solo_deja_tipos_del_esquema(tmp_path, universo, monkeypatch):
    b = nuevo_bloque(tmp_path, universo, cfg=cargar_config())
    valor_en = b.proveedor.valor_en

    def malo(simbolo, fecha, **criterios_publicacion):
        if simbolo == "EURUSD=X":
            raise DatosInvalidos("HT-01: cierre no positivo simulado")
        return valor_en(simbolo, fecha, **criterios_publicacion)
    monkeypatch.setattr(b.proveedor, "valor_en", malo)
    r = b.ciclo(AS_OF)
    assert r["paquete"]["clases"]["DIV"]["opciones"]
    incs = _incs(b.almacen)
    assert incs and all(e["tipo"] in _tipos_del_esquema() for e in incs)
    for e in incs:
        jsonschema.validate(e, _esquema_inc())
    _comprobar_de_datos(incs, "HT-01: datos inválidos de EURUSD=X")
    assert all(b.almacen.verificar_integridad().values())
