"""T-87: las cifras de evaluación conservan evidencia y límites de acceso."""
import pandas as pd
import pytest
from test_t53_evaluacion_y_almacen import MotorFalso, _alta, _h5_con_hitos, _resolver

from bloque_a.almacen import Almacen
from bloque_a.backtest import ejecutar_backtest
from bloque_a.evaluador import Evaluador
from bloque_a.herramientas.ht01_datos import DatosNoDisponibles, ProveedorCSV


def _csv(carpeta, nombre, texto):
    (carpeta / (nombre + ".csv")).write_text(texto, encoding="utf-8")


def _evaluador(tmp):
    p = ProveedorCSV(tmp)
    a = Almacen(tmp / "estado")
    a.reloj.fijar("2026-06-05")
    return Evaluador(a, p, MotorFalso(), {}, pd.DataFrame({"simbolo": ["X", "Y"], "clase": ["RV", "RV"]}))


@pytest.mark.parametrize("obsoleta", ["activo", "indice", "cesta"])
def test_no_resuelve_si_una_pata_esta_obsoleta(tmp_path, obsoleta):
    e = _evaluador(tmp_path)
    for sim in ("X", "Y", "I"):
        vieja = (sim, obsoleta) in {("X", "activo"), ("I", "indice"), ("Y", "cesta")}
        _csv(tmp_path, sim, "fecha,cierre\n2026-06-05,100\n" + ("2026-06-08,103\n" if vieja else "2026-07-31,110\n"))
    _alta(e.almacen, "PRG-2026-0001", tipo_pronostico="RELATIVO", variable={"serie_ht01": "X"},
          referencia_indice="CESTA" if obsoleta == "cesta" else "I", nivel_referencia={"valor": 100, "fecha": "2026-06-05"},
          nivel_referencia_indice=100, fecha_resolucion="2026-07-31")
    for corte, esperado in [("2026-07-31", "ABIERTO"), ("2026-08-21", "NO_RESOLUBLE")]:
        e.almacen.reloj.fijar(corte)
        e.proveedor.fijar_as_of(corte)
        e.resolver(corte)
        assert e.almacen.estado("F4")["PRG-2026-0001"]["estado"] == esperado


def test_resolver_conserva_niveles_conocidos_y_congelados(tmp_path):
    e = _evaluador(tmp_path)
    _csv(tmp_path, "X", "fecha,cierre,fecha_publicacion\n2026-06-04,100,2026-06-04\n2026-06-05,200,2026-07-01\n2026-07-31,150,2026-07-31\n")
    _csv(tmp_path, "I", "fecha,cierre\n2026-06-05,400\n2026-07-31,250\n")
    _alta(e.almacen, "PRG-2026-0010", tipo_pronostico="RELATIVO", variable={"serie_ht01": "X"},
          referencia_indice="I", nivel_referencia={"valor": 100, "fecha": "2026-06-04"},
          nivel_referencia_indice=200, fecha_resolucion="2026-07-31")
    e.proveedor.fijar_as_of("2026-08-03")
    e.almacen.reloj.fijar("2026-08-03")
    r, = e.resolver("2026-08-03")
    assert r["resolucion"]["rent_proxy"] == 0.5
    assert r["resolucion"]["rent_referencia"] == 0.25


def test_certificados_separan_metodos(tmp_path):
    e = _evaluador(tmp_path)
    for i in range(100):
        pid = f"PRG-2026-{i:04d}"
        _alta(e.almacen, pid, metodo="MET-A" if i < 50 else "MET-B",
              fecha_resolucion=str((pd.Timestamp("2025-06-01") + pd.Timedelta(days=i)).date()))
        _resolver(e.almacen, pid, i % 2)
    res = e.revisar_certificados("2026-07-31")
    assert set(res["insuficientes"]) == {"RV|H3|MET-A", "RV|H3|MET-B"}
    assert not res["evaluadas"]


def test_no_reutiliza_directorio_de_backtest_con_estado(tmp_path):
    estado = tmp_path / "estado"
    estado.mkdir()
    original = estado / "F4_registro_pronosticos.jsonl"
    original.write_text("estado anterior\n")
    with pytest.raises(FileExistsError, match="salida"):
        ejecutar_backtest({}, "2026-01-01", "2026-01-31", "no-datos", "no-universo", str(tmp_path))
    assert original.read_text() == "estado anterior\n"


def test_huella_incluye_fechas_intermedias(tmp_path):
    huellas = []
    for sub, fecha in [("a", "2026-06-04"), ("b", "2026-06-05")]:
        d = tmp_path / sub
        d.mkdir()
        _csv(d, "X", f"fecha,cierre\n2026-06-01,1\n{fecha},2\n2026-06-09,3\n")
        p = ProveedorCSV(d)
        p.fijar_as_of("2026-06-12")
        huellas.append(p.huella("X"))
    assert huellas[0] != huellas[1]


def test_datos_csv_limites_de_carpeta(tmp_path):
    d = tmp_path / "permitido"
    d.mkdir()
    _csv(tmp_path, "FUERA", "fecha,cierre\n2026-02-01,200\n")
    (d / "ENLACE.csv").symlink_to(tmp_path / "FUERA.csv")
    p = ProveedorCSV(d)
    p.fijar_as_of("2026-02-01")
    for nombre in ("../FUERA", str(tmp_path / "FUERA"), "ENLACE"):
        with pytest.raises(DatosNoDisponibles):
            p.cierres(nombre)


def test_dos_degradaciones_en_misma_fecha_de_efecto(tmp_path):
    a = Almacen(tmp_path)
    a.reloj.fijar("2027-06-04")
    for i, clase in enumerate(("RV", "MP")):
        _h5_con_hitos(a, clase, f"PRG-2026-{901+i:04}", 5, 15)
    e = Evaluador(a, None, None, {"evaluacion": {}, "methodology_version": "5.1"}, None)
    ajustes = e.aplicar_degradacion_h5("2027-06-04")
    assert len(ajustes) == 2 and all(x["tipo_entrada"] == "AJU" for x in ajustes)
    # T-92: con la regla de T-65 (H-13) la degradación rige desde el mismo ciclo; las dos se componen en esa fecha
    siguiente = a.estado("F10", "2027-06-04")
    assert all(siguiente["P-31"]["valor_vigente"][c]["H5"] == "LIMITADO" for c in ("RV", "MP"))
    assert siguiente["P-30"]["valor_vigente"] == "5.3"


def test_cesta_conserva_composicion_y_precios_de_emision(tmp_path):
    e = _evaluador(tmp_path)
    _csv(tmp_path, "X", "fecha,cierre\n2026-06-05,100\n2026-07-31,150\n")
    _csv(tmp_path, "Y", "fecha,cierre,fecha_publicacion\n2026-06-05,200,2026-07-01\n2026-07-31,50,2026-07-31\n")
    e.proveedor.fijar_as_of("2026-06-05")
    bases = e.bases_cesta("RV", "2026-06-05")
    assert set(bases) == {"X"}
    e.proveedor.fijar_as_of("2026-07-31")
    for congelada in (bases, None):
        # Una cesta histórica sin snapshot se reconstruye con información conocible al emitir.
        r, fecha = e.rentabilidad("CESTA", "RV", "2026-06-05", "2026-07-31", base=congelada)
        assert r == 0.5 and fecha == pd.Timestamp("2026-07-31")


def test_r13_certificado_por_metodo_en_la_entrega(tmp_path, universo):
    from conftest import AS_OF, nuevo_bloque

    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    for h, metodo in [("H2", "OTRO-METODO"), ("H3", "ACC-MOM-001"), ("H2", None)]:
        b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT", "id": b.almacen.nuevo_id("CERT"), "estado": "VIGENTE",
                                           "celda": {"clase": "RV", "horizonte": h, "metodo": metodo}})
    r = b.ciclo(AS_OF, alcance={"clases": ["RV"]})
    altas = [p for p in b.almacen.estado("F4").values() if p.get("metodo") == "ACC-MOM-001"]
    assert altas and r["entregables"]
    assert {p["horizonte"] for p in altas} >= {"H2", "H3"}
    for p in altas:
        assert (p["prob_publicada"] is not None) == (p["horizonte"] == "H3")
    for op in r["paquete"]["clases"]["RV"]["opciones"]:
        for h, v in op["horizontes"].items():
            assert (v["prob"] is not None) == (h == "H3")
