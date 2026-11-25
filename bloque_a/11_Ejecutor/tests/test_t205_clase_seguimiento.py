"""T-205: el seguimiento encargado (CT-24, ciclo C6) no manda al AG-03 una opción de F3 con una clase desconocida o vacía.

Antes, `b_agente` mandaba al AG-03, sin ningún aviso, el CT-06 de una opción cuya clase no estaba en `AGENTE_CLASE` (o
faltaba): `_alta` no comprobaba la clase, el C6 registraba un CT-05 con `{"XYZ": "N1"}` y presupuesto y un CT-06 de AG-02 a
AG-03, y no dejaba ninguna incidencia en HA; solo lo paraba después G3, porque el esquema del informe rechaza `tipo_activo`
(QA r01 de T-201, 25-11-2026). Ahora el alta y el C6 se rechazan antes de escribir nada y dejan un INC- de tipo OTRO con
`campo_afectado` «clase» y sin el valor (INC-T205-01); en el C6 la opción se salta con su incidencia (una sola mientras nada
cambie) y el resto del ciclo sigue igual. Sin red ni claves: cliente simulado y datos sintéticos.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from bloque_a.almacen import Almacen
from bloque_a.contratos import AGENTE_CLASE
from bloque_a.seguimiento import ClaseNoAdmitida, Seguimientos, b_agente, clase_admitida
from conftest import AS_OF, RAIZ, nuevo_bloque

from bloque_a import seguimiento

SEMANA_SIG = "2026-06-12"
MALAS = [("XYZ", "desconocida"), ("", "vacia"), (None, "none")]
AUSENTE = object()   # la ficha de F3 no lleva la clave `clase`


# ------------------------------------------------------------------------------------------------ preparación
@pytest.fixture(scope="module")
def base(tmp_path_factory, universo):
    """Un ciclo C1 de RV (cliente simulado): sus opciones, con su clase en F3, son las de las pruebas."""
    tmp = tmp_path_factory.mktemp("t205")
    b = nuevo_bloque(tmp, universo)
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    opps = [o["opp_id"] for o in r["paquete"]["clases"]["RV"]["opciones"]]
    assert len(opps) >= 3, opps
    return tmp, opps


def _copia(base, destino, universo):
    """Un Bloque nuevo sobre una copia del estado del ciclo base (la mensajería empieza vacía)."""
    tmp, _ = base
    for carpeta in ("estado", "ent"):
        if (tmp / carpeta).exists():
            shutil.copytree(tmp / carpeta, destino / carpeta)
    b = nuevo_bloque(destino, universo)
    mensajes: list[dict] = []
    crear = b.mensajeria.crear

    def espia(contrato, emisor, receptor, cuerpo, **kw):
        m = crear(contrato, emisor, receptor, cuerpo, **kw)
        mensajes.append(m)
        return m

    b.mensajeria.crear = espia
    return b, mensajes


def _poner_clase(b, opp_id, valor, fecha=AS_OF):
    """F3 manipulado o migrado: la ficha de la opción pasa a tener otra clase (escrita por su propietario, AG-02)."""
    b.fijar_fecha(fecha)
    b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": opp_id, "clase": valor})


def _opp_sin_clase(b, opp_id="OPP-2026-0901"):
    b.fijar_fecha(AS_OF)
    b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ALTA", "opp_id": opp_id, "estado": "DESCARTADA", "horizonte_principal": "H3",
                                       "indicador_seguimiento": {"simbolo": "EURUSD=X"}})
    assert "clase" not in b.almacen.estado("F3")[opp_id]
    return opp_id


def _foto(b):
    """Contenido de todos los ficheros del estado (F3, F5, F6, F10, F11, HA, contadores, sellos…)."""
    return {p.name: p.read_bytes() for p in sorted(b.almacen.carpeta.iterdir()) if p.is_file() and p.suffix in (".jsonl", ".json")}


def _incs(b, desde=0):
    """Los INC- de la clase (el ciclo base deja otros INC- en HA, ajenos a T-205)."""
    return [e for e in b.almacen.leer("HA")[desde:] if e.get("tipo_entrada") == "INC" and e.get("campo_afectado") == "clase"]


def _alta(b, opp_id, fecha=AS_OF):
    return b.seguimientos.procesar({"accion": "ALTA", "opp_id": opp_id, "frecuencia": "SEMANAL", "motivo": "T-205",
                                    "senales_interes": ["Momentum relativo"]}, fecha)


def _de(mensajes, seg_id, opp_id):
    return [m for m in mensajes if m["contrato"] in ("CT-05", "CT-06") and (m.get("seg_id") == seg_id or m.get("opp_id") == opp_id)]


# ------------------------------------------------------------------------------------------------ b_agente
@pytest.mark.parametrize("clase", ["XYZ", "", None, "rv", " RV", 3, ["RV"]], ids=repr)
def test_b_agente_falla_con_una_clase_que_no_es_uno_de_los_doce_tipos(clase):
    """CA-1: desconocida, vacía, None, otra grafía u otro tipo → ClaseNoAdmitida (antes, AG-03 sin aviso)."""
    with pytest.raises(ClaseNoAdmitida):
        b_agente(clase)
    assert not clase_admitida(clase)


def test_b_agente_da_el_analista_de_cada_uno_de_los_doce_tipos():
    """CA-1: las doce clases siguen yendo a su Analista; ClaseNoAdmitida es un ValueError (los que ya lo capturan siguen)."""
    assert {c: b_agente(c) for c in AGENTE_CLASE} == AGENTE_CLASE and len(AGENTE_CLASE) == 12
    assert issubclass(ClaseNoAdmitida, ValueError)


# ------------------------------------------------------------------------------------------------ alta (CT-24 ALTA)
@pytest.mark.parametrize(("valor", "_id"), MALAS + [(AUSENTE, "ausente")], ids=[i for _, i in MALAS] + ["ausente"])
def test_alta_con_clase_no_admitida_se_rechaza_sin_escribir_nada_mas_que_su_inc(base, tmp_path, universo, valor, _id):
    """CA-2: el alta se rechaza antes de escribir nada (ni F11, ni F3, ni F5, ni el CT-24 de entrada, ni SEG- o MSG-) y deja un
    INC- OTRO con campo_afectado «clase», sin el valor."""
    b, mensajes = _copia(base, tmp_path, universo)
    if valor is AUSENTE:
        opp = _opp_sin_clase(b)
    else:
        opp = base[1][0]
        _poner_clase(b, opp, valor)
        assert b.almacen.estado("F3")[opp]["clase"] == valor
    antes, n_ha, cont = _foto(b), len(b.almacen.leer("HA")), json.loads((b.almacen.carpeta / "contadores.json").read_text())
    with pytest.raises(ClaseNoAdmitida) as exc:
        _alta(b, opp)
    despues = _foto(b)
    assert {k for k in antes.keys() | despues.keys() if antes.get(k) != despues.get(k)} <= {"HA_historial_auditorias.jsonl", "contadores.json",
                                                                                           "sellos_integridad.json"}
    cont2 = json.loads((b.almacen.carpeta / "contadores.json").read_text())
    assert {k for k in cont.keys() | cont2.keys() if cont.get(k) != cont2.get(k)} == {"INC-2026"}     # ni SEG- ni MSG- ni F5SEG
    assert mensajes == [] and b.mensajeria.registro == []                                                # ni el CT-24 de entrada
    [inc] = _incs(b, n_ha)
    assert len(b.almacen.leer("HA")) == n_ha + 1 and exc.value.inc_id == inc["id"]
    assert (inc["tipo"], inc["campo_afectado"], inc["fase"], inc["objeto"], inc["opp_id"]) == ("OTRO", "clase", "ALTA", opp, opp)
    assert inc["escalado_operador"] is True and inc["tratamiento"] == "rechazada y registrada"
    if valor == "XYZ":
        assert "XYZ" not in json.dumps(inc, ensure_ascii=False)                                         # sin el valor
    assert not [e for e in b.seguimientos.encargos().values() if e["opp_id"] == opp]
    assert "seg_id" not in b.almacen.estado("F3")[opp]


def test_alta_con_clase_buena_sigue_igual_y_cada_alta_rechazada_deja_su_inc(base, tmp_path, universo):
    """CA-2 (regresión): con su clase, el alta es la de siempre; dos altas rechazadas son dos peticiones y dos INC-."""
    b, mensajes = _copia(base, tmp_path, universo)
    a = _alta(b, base[1][0])
    assert a["estado"] == "ACTIVO" and a["proximo_ciclo"] == SEMANA_SIG
    assert [m["contrato"] for m in mensajes] == ["CT-24", "CT-24"] and not _incs(b)
    assert b.seguimientos.encargos()[a["seg_id"]]["clase"] == "RV"
    _poner_clase(b, base[1][1], "XYZ")
    for _ in range(2):
        with pytest.raises(ClaseNoAdmitida):
            _alta(b, base[1][1])
    assert len(_incs(b)) == 2


def test_alta_de_una_opp_que_no_esta_en_f3_sigue_siendo_keyerror_sin_inc(base, tmp_path, universo):
    """CA-2 (límite): una OPP- inexistente no es un problema de clase: el KeyError de siempre, sin INC-."""
    b, _ = _copia(base, tmp_path, universo)
    with pytest.raises(KeyError):
        _alta(b, "OPP-2026-9999")
    assert not _incs(b)


def test_alta_con_ha_rota_sube_el_error_de_ha_y_solo_cambia_el_contador_de_inc(base, tmp_path, universo):
    """CA-5 en el alta (ronda de cierre de la QA r01, H-02; modelo: A6 de r01_02): si no se puede escribir el INC- en HA, sube
    el error de HA (no `ClaseNoAdmitida` ni un acuse) y solo cambia el contador de INC-: ni mensajes, ni F11, ni F3, ni F5."""
    b, mensajes = _copia(base, tmp_path, universo)
    opp = base[1][0]
    _poner_clase(b, opp, "XYZ")
    antes = _foto(b)
    escribir = b.almacen.escribir

    def roto(archivo, *a, **k):
        if archivo == "HA":
            raise OSError("disco lleno")
        return escribir(archivo, *a, **k)

    b.almacen.escribir = roto
    try:
        with pytest.raises(OSError, match="disco lleno"):
            _alta(b, opp)
    finally:
        b.almacen.escribir = escribir
    despues = _foto(b)
    assert {k for k in antes.keys() | despues.keys() if antes.get(k) != despues.get(k)} <= {"contadores.json"}
    assert mensajes == [] and b.mensajeria.registro == []
    assert not [e for e in b.seguimientos.encargos().values() if e["opp_id"] == opp] and not _incs(b)


def test_alta_directa_tambien_comprueba_la_clase(base, tmp_path, universo):
    """CA-2: `_alta` comprueba la clase aunque se llame sin `procesar` (la clase cambia entre la comprobación y el alta)."""
    b, _ = _copia(base, tmp_path, universo)
    opp = base[1][0]
    _poner_clase(b, opp, "XYZ")
    n_f11 = len(b.almacen.leer("F11"))
    with pytest.raises(ClaseNoAdmitida):
        b.seguimientos._alta({"opp_id": opp, "frecuencia": "SEMANAL"}, b.fijar_fecha(AS_OF))
    assert len(b.almacen.leer("F11")) == n_f11 and len(_incs(b)) == 1


# ------------------------------------------------------------------------------------------------ ciclo C6
def _tres_encargos(b, opps):
    """Tres encargos con su clase; el tercero (el último SEG-) es el que se estropea."""
    return [_alta(b, o)["seg_id"] for o in opps[:3]]


def _norma(obj, *raices):
    """JSON canónico sin las carpetas de cada copia (las rutas de los entregables) ni los sellos de tiempo de los mensajes."""
    t = json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)
    for r in raices:
        t = t.replace(str(r), "<copia>")
    return t


@pytest.mark.parametrize(("valor", "_id"), MALAS, ids=[i for _, i in MALAS])
def test_c6_salta_la_opcion_con_clase_no_admitida_y_el_resto_del_ciclo_sigue_igual(base, tmp_path, universo, valor, _id):
    """CA-3: la opción se salta con su INC- (OTRO, «clase», sin el valor), sin CT-05 ni CT-06, sin RUN-, F5, G3V ni informe, y
    F11 no avanza; las otras dos dan exactamente lo mismo que sin la opción estropeada (gemelo sin estropear)."""
    (tmp_path / "mal").mkdir()
    (tmp_path / "bien").mkdir()
    b, mensajes = _copia(base, tmp_path / "mal", universo)
    g, mensajes_g = _copia(base, tmp_path / "bien", universo)
    segs, segs_g = _tres_encargos(b, base[1]), _tres_encargos(g, base[1])
    assert segs == segs_g
    malo, opp_malo = segs[2], base[1][2]
    _poner_clase(b, opp_malo, valor)
    _poner_clase(g, opp_malo, "RV")      # el gemelo escribe la misma entrada de F3, con su clase de siempre
    del mensajes[:], mensajes_g[:]
    n_ha, n_f5 = len(b.almacen.leer("HA")), len(b.almacen.leer("F5"))
    enc_antes = b.seguimientos.encargos()[malo]
    res, res_g = b.seguimientos.ejecutar(SEMANA_SIG), g.seguimientos.ejecutar(SEMANA_SIG)
    assert [r["seg_id"] for r in res] == segs and [r["seg_id"] for r in res_g] == segs
    # la opción estropeada: omitida, con su INC-
    r = res[2]
    assert r["ejecutado"] is False and r["incidencia_nueva"] is True and "run_id" not in r
    [inc] = [e for e in _incs(b, n_ha)]
    assert inc["id"] == r["inc_id"] and (inc["tipo"], inc["campo_afectado"], inc["fase"], inc["objeto"], inc["opp_id"]) == \
        ("OTRO", "clase", "C6", malo, opp_malo)
    assert inc["escalado_operador"] is True and inc["ciclos_encargo"] == 0
    if valor == "XYZ":
        assert "XYZ" not in json.dumps(inc, ensure_ascii=False)
    assert _de(mensajes, malo, opp_malo) == []                                                      # ni CT-05 ni CT-06
    assert not [m for m in mensajes if m["contrato"] == "CT-24" and m.get("seg_id") == malo]
    assert not [m for m in mensajes if "XYZ" in json.dumps(m.get("nivel_por_clase") or {})]
    assert b.seguimientos.encargos()[malo] == enc_antes                                              # F11 no avanza
    assert not [e for e in b.almacen.leer("F5")[n_f5:] if e.get("seg_id") == malo]
    assert not [e for e in b.almacen.leer("HA")[n_ha:] if e.get("tipo_entrada") == "G3V" and e.get("run_id") not in
                {x["run_id"] for x in res[:2]}]
    # el resto del ciclo, igual que en el gemelo (los mismos RUN-, informes, mensajes y entradas de F11 y F5)
    raices = (tmp_path / "mal", tmp_path / "bien")
    for x, y in zip(res[:2], res_g[:2]):
        assert x["ejecutado"] and x["entregado"] and _norma(x, *raices) == _norma(y, *raices)
        assert Path(x["rutas"]["json"]).read_bytes() == Path(y["rutas"]["json"]).read_bytes()
    assert res_g[2]["ejecutado"]
    buenos = [m for m in mensajes if m.get("seg_id") in segs[:2] or m.get("run_id") in {x["run_id"] for x in res[:2]}]
    buenos_g = [m for m in mensajes_g if m.get("seg_id") in segs[:2] or m.get("run_id") in {x["run_id"] for x in res_g[:2]}]

    def sin_tiempo(ms):
        return _norma([{k: v for k, v in m.items() if k not in ("timestamp", "msg_id")} for m in ms], *raices)

    assert [m["contrato"] for m in buenos] == ["CT-05", "CT-06", "CT-24"] * 2 and sin_tiempo(buenos) == sin_tiempo(buenos_g)
    for s in segs[:2]:
        assert _norma(b.seguimientos.encargos()[s], *raices) == _norma(g.seguimientos.encargos()[s], *raices)


def test_c6_una_opcion_vigente_con_clase_no_admitida_no_se_omite_cubierta_en_c1(base, tmp_path, universo):
    """CA-3 (ronda de cierre de la QA r01, H-01; modelo: A4 de r01_02): la clase se comprueba antes que la absorción en C1. Una
    opción VIGENTE con la clase estropeada se salta con su INC-, sin CICLO_OMITIDO, y F11 no cambia."""
    b, mensajes = _copia(base, tmp_path, universo)
    opp = base[1][0]
    seg = _alta(b, opp)["seg_id"]
    b.fijar_fecha(AS_OF)
    b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": opp, "clase": "XYZ", "estado": "VIGENTE"})
    assert b.almacen.estado("F3")[opp]["estado"] == "VIGENTE"
    del mensajes[:]
    n_f11, enc_antes = len(b.almacen.leer("F11")), b.seguimientos.encargos()[seg]
    [r] = b.seguimientos.ejecutar(SEMANA_SIG)
    assert r["ejecutado"] is False and r["inc_id"] and r["motivo"] != "cubierto en C1"
    assert [e["id"] for e in _incs(b)] == [r["inc_id"]] and _incs(b)[0]["fase"] == "C6"
    assert not [e for e in b.almacen.leer("F11") if e.get("tipo_entrada") == "CICLO_OMITIDO"]
    assert len(b.almacen.leer("F11")) == n_f11 and b.seguimientos.encargos()[seg] == enc_antes and mensajes == []


def test_c6_de_un_encargo_cuya_opp_no_esta_en_f3_tambien_se_salta(base, tmp_path, universo):
    """CA-3 (límite, clase ausente): un encargo de F11 sin su OPP- en F3 ya no toma la clase de F11; se salta con su INC-."""
    b, mensajes = _copia(base, tmp_path, universo)
    b.fijar_fecha(AS_OF)
    b.almacen.escribir("F11", "AG-01", {"tipo_entrada": "ALTA", "seg_id": "SEG-2026-0900", "opp_id": "OPP-2026-0900", "clase": "RV",
                                         "estado": "ACTIVO", "frecuencia": "SEMANAL", "fecha_alta": AS_OF, "ciclos": 0,
                                         "proximo_ciclo": SEMANA_SIG})
    [r] = b.seguimientos.ejecutar(SEMANA_SIG)
    assert r["ejecutado"] is False and r["inc_id"] and mensajes == []
    [inc] = _incs(b)
    assert inc["f3_seq_clase"] is None and inc["objeto"] == "SEG-2026-0900"


def test_c6_forzado_tambien_se_salta(base, tmp_path, universo):
    """CA-3: `ejecutar(seg_id, forzar=True)` pasa por la misma comprobación."""
    b, mensajes = _copia(base, tmp_path, universo)
    seg = _alta(b, base[1][0])["seg_id"]
    _poner_clase(b, base[1][0], "")
    del mensajes[:]
    [r] = b.seguimientos.ejecutar(AS_OF, seg, forzar=True)
    assert r["ejecutado"] is False and _de(mensajes, seg, base[1][0]) == [] and len(_incs(b)) == 1


def test_c6_una_sola_incidencia_mientras_nada_cambie(base, tmp_path, universo):
    """CA-4: los ciclos vencidos siguientes citan el mismo INC-; otra entrada de F3 con la clase (otro valor no admitido) o un
    ciclo hecho entre medias abren otro."""
    b, mensajes = _copia(base, tmp_path, universo)
    opp = base[1][0]
    seg = _alta(b, opp)["seg_id"]
    _poner_clase(b, opp, "XYZ")
    [r1] = b.seguimientos.ejecutar(SEMANA_SIG)
    [r2] = b.seguimientos.ejecutar(SEMANA_SIG)
    [r3] = b.seguimientos.ejecutar("2026-06-13")                         # al día siguiente sigue vencido (F11 no avanzó)
    assert r1["incidencia_nueva"] and not r2["incidencia_nueva"] and not r3["incidencia_nueva"]
    assert r1["inc_id"] == r2["inc_id"] == r3["inc_id"] and len(_incs(b)) == 1
    # una actualización de F3 que no toca la clase no cambia nada
    b.almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": opp, "nota": "otra cosa"})
    [r4] = b.seguimientos.ejecutar("2026-06-13")
    assert r4["inc_id"] == r1["inc_id"] and len(_incs(b)) == 1
    # otro valor no admitido: otra entrada de F3 que fija la clase → otro INC-
    _poner_clase(b, opp, "ABC", "2026-06-13")
    [r5] = b.seguimientos.ejecutar("2026-06-13")
    assert r5["incidencia_nueva"] and r5["inc_id"] != r1["inc_id"] and len(_incs(b)) == 2
    # se corrige: el ciclo se hace y F11 avanza; si se vuelve a estropear con el mismo valor, es otro episodio
    _poner_clase(b, opp, "RV", "2026-06-13")
    del mensajes[:]
    [r6] = b.seguimientos.ejecutar("2026-06-13")
    assert r6["ejecutado"] and len(_de(mensajes, seg, opp)) == 2
    enc = b.seguimientos.encargos()[seg]
    assert enc["ciclos"] == 1 and enc["proximo_ciclo"] == "2026-06-20"
    _poner_clase(b, opp, "ABC", "2026-06-20")
    [r7] = b.seguimientos.ejecutar("2026-06-20")
    assert r7["incidencia_nueva"] and len(_incs(b)) == 3 and _incs(b)[-1]["ciclos_encargo"] == 1


def test_c6_un_inc_de_otra_fase_con_la_misma_clave_no_tapa_el_del_c6(base, tmp_path, universo):
    """CA-4 (límite): la deduplicación solo cuenta los INC- del propio C6; otro INC- de la clase con la misma clave pero de otra
    fase (escrito a mano o por otra pieza) no evita el del ciclo."""
    b, _ = _copia(base, tmp_path, universo)
    opp = base[1][0]
    seg = _alta(b, opp)["seg_id"]
    _poner_clase(b, opp, "XYZ")
    clave = {"seg_id": seg, "f3_seq_clase": b.seguimientos._seq_clase(opp, SEMANA_SIG), "ciclos_encargo": 0}
    ajena = b.almacen.incidencia("OTRO", "otra pieza", objeto=seg, campo_afectado="clase", fase="REVISION", **clave)
    [r] = b.seguimientos.ejecutar(SEMANA_SIG)
    assert r["incidencia_nueva"] and r["inc_id"] != ajena["id"] and _incs(b)[-1]["fase"] == "C6"


def test_c6_un_fallo_al_escribir_la_incidencia_no_deja_nada_a_medias(base, tmp_path, universo, monkeypatch):
    """CA-5 (falla cerrado): si no se puede escribir el INC-, el error sube y no queda ni CT-05/CT-06, ni RUN-, ni F11, ni F5."""
    b, mensajes = _copia(base, tmp_path, universo)
    seg = _alta(b, base[1][0])["seg_id"]
    _poner_clase(b, base[1][0], "XYZ")
    del mensajes[:]
    antes = _foto(b)

    class Roto(Exception):
        pass

    def roto(*a, **k):
        raise Roto("disco lleno")

    monkeypatch.setattr(b.almacen, "incidencia", roto)
    with pytest.raises(Roto):
        b.seguimientos.ejecutar(SEMANA_SIG)
    assert _foto(b) == antes and mensajes == [] and b.seguimientos.encargos()[seg]["ciclos"] == 0


# ------------------------------------------------------------------------------------------------ concurrencia
PROCESOS = 6
RONDAS = 5
TRABAJADOR = r"""
import sys
from types import SimpleNamespace
sys.path.insert(0, sys.argv[1])
from bloque_a.almacen import Almacen
from bloque_a.seguimiento import Seguimientos
for linea in sys.stdin:
    carpeta = linea.strip()
    if not carpeta:
        break
    al = Almacen(carpeta)
    al.reloj.fijar("2026-06-12")
    # sin mensajería ni proveedor: si el ciclo intentara un CT-05 o un CT-06, fallaría con AttributeError
    s = Seguimientos(SimpleNamespace(almacen=al, cfg={}))
    enc = s.encargos()["SEG-2026-0001"]
    print("listo", flush=True)
    sys.stdin.readline()
    try:
        r = s.ciclo_c6(enc, "2026-06-12")
        print("ok " + r["inc_id"] + " " + str(r["incidencia_nueva"]), flush=True)
    except BaseException as e:
        print("fallo " + type(e).__name__ + ": " + str(e).replace("\n", " "), flush=True)
"""


def test_c6_la_lectura_de_ha_y_el_inc_van_en_la_misma_transaccion(tmp_path):
    """CA-4 (concurrencia, determinista; ronda de cierre de la QA r01, mutante Q11 del revisor): justo después de que el C6 lea
    HA para deduplicar, otra instancia del almacén (otro «proceso») intenta el mismo C6. Si la lectura y la escritura van en la
    misma transacción, la otra espera al cerrojo y encuentra el INC- ya escrito; si no, las dos escriben el suyo."""
    import threading

    def preparar():
        al = Almacen(tmp_path)
        al.reloj.fijar(AS_OF)
        al.escribir("F3", "AG-02", {"tipo_entrada": "ALTA", "opp_id": "OPP-2026-0001", "clase": "XYZ", "estado": "DESCARTADA"})
        al.escribir("F11", "AG-01", {"tipo_entrada": "ALTA", "seg_id": "SEG-2026-0001", "opp_id": "OPP-2026-0001", "clase": "RV",
                                      "estado": "ACTIVO", "frecuencia": "SEMANAL", "ciclos": 0, "proximo_ciclo": SEMANA_SIG})

    def seguimientos():
        al = Almacen(tmp_path)
        al.reloj.fijar(SEMANA_SIG)
        return Seguimientos(SimpleNamespace(almacen=al, cfg={}))

    preparar()
    s1, s2 = seguimientos(), seguimientos()
    resultado_2: list = []
    otro = threading.Thread(target=lambda: resultado_2.append(s2.ciclo_c6(s2.encargos()["SEG-2026-0001"], SEMANA_SIG)))
    leer = s1.b.almacen.leer

    def leer_y_ceder(archivo, *a, **k):
        out = leer(archivo, *a, **k)
        if archivo == "HA" and not otro.is_alive() and not resultado_2:
            otro.start()
            otro.join(timeout=2)     # con la transacción, el otro sigue esperando al cerrojo
        return out

    s1.b.almacen.leer = leer_y_ceder
    r1 = s1.ciclo_c6(s1.encargos()["SEG-2026-0001"], SEMANA_SIG)
    otro.join()
    [r2] = resultado_2
    incs = [e for e in Almacen(tmp_path).leer("HA") if e.get("tipo_entrada") == "INC"]
    assert len(incs) == 1 and r1["inc_id"] == r2["inc_id"] == incs[0]["id"]
    assert (r1["incidencia_nueva"], r2["incidencia_nueva"]) == (True, False)


def test_c6_varios_procesos_a_la_vez_dejan_una_sola_incidencia(tmp_path):
    """CA-4 (concurrencia): seis procesos omiten a la vez el C6 del mismo encargo; un solo INC- y todos lo citan."""
    trabajadores = [subprocess.Popen([sys.executable, "-c", TRABAJADOR, str(RAIZ)], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, text=True, bufsize=1) for _ in range(PROCESOS)]
    fallos = []
    try:
        for ronda in range(RONDAS):
            carpeta = tmp_path / f"almacen_{ronda}"
            al = Almacen(carpeta)
            al.reloj.fijar(AS_OF)
            al.escribir("F3", "AG-02", {"tipo_entrada": "ALTA", "opp_id": "OPP-2026-0001", "clase": "XYZ", "estado": "DESCARTADA"})
            al.escribir("F11", "AG-01", {"tipo_entrada": "ALTA", "seg_id": "SEG-2026-0001", "opp_id": "OPP-2026-0001", "clase": "RV",
                                          "estado": "ACTIVO", "frecuencia": "SEMANAL", "ciclos": 0, "proximo_ciclo": SEMANA_SIG})
            for t in trabajadores:
                t.stdin.write(f"{carpeta}\n")
            assert [t.stdout.readline().strip() for t in trabajadores] == ["listo"] * PROCESOS
            for t in trabajadores:
                t.stdin.write("ya\n")
            respuestas = [t.stdout.readline().strip().split() for t in trabajadores]
            incs = [e for e in Almacen(carpeta).leer("HA") if e.get("tipo_entrada") == "INC"]
            if any(r[0] != "ok" for r in respuestas) or len(incs) != 1 or {r[1] for r in respuestas} != {incs[0]["id"]} \
                    or sorted(r[2] for r in respuestas) != ["False"] * (PROCESOS - 1) + ["True"]:
                fallos.append((ronda, respuestas, [e["id"] for e in incs]))
    finally:
        for t in trabajadores:
            t.stdin.close()
        for t in trabajadores:
            t.wait(timeout=60)
    assert not fallos, fallos


# ------------------------------------------------------------------------------------------------ sin el cambio
def test_el_defecto_de_la_qa_r01_de_t201_ya_no_se_reproduce(base, tmp_path, universo):
    """CA-6 (regresión de la QA r01 de T-201): con «XYZ» en F3 tras el alta, antes salían un CT-05 con {"XYZ": "N1"} y un CT-06
    AG-02 → AG-03 sin incidencia; ahora no sale ninguno de los dos y queda el INC-."""
    b, mensajes = _copia(base, tmp_path, universo)
    seg = _alta(b, base[1][0])["seg_id"]
    _poner_clase(b, base[1][0], "XYZ")
    del mensajes[:]
    b.seguimientos.ejecutar(SEMANA_SIG)
    assert not [m for m in mensajes if m["contrato"] == "CT-06" and m["receptor"] == "AG-03"]
    assert not [m for m in mensajes if (m.get("nivel_por_clase") or {}).get("XYZ")]
    assert [e["objeto"] for e in _incs(b)] == [seg]
    assert seguimiento.Seguimientos is Seguimientos
