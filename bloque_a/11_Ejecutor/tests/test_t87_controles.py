"""Controles operativos incluidos en el diagnóstico del 9 de noviembre."""
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import pytest
from bloque_a.almacen import ARCHIVOS, Almacen, EscrituraFueraDeReserva
from bloque_a.contratos import DatosSensibles
from conftest import AS_OF, nuevo_bloque


def test_dos_escritores_comparten_contadores_y_cadena(tmp_path):
    clientes = [Almacen(tmp_path), Almacen(tmp_path)]
    def registrar(i):
        a = clientes[i % 2]
        clave = a.nuevo_id("OBS")
        a.escribir("F5", "AG-01", {"id": clave})
        return clave
    with ThreadPoolExecutor(4) as pool:
        ids = list(pool.map(registrar, range(20)))
    assert len(set(ids)) == 20
    assert set(clientes[0].estado("F5")) == set(ids)
    assert Almacen(tmp_path).verificar_integridad("F5")["F5"]


def test_fallo_al_escribir_no_crea_alta_fantasma(tmp_path):
    a = Almacen(tmp_path)
    e = {"prg_id": "P", "tipo_entrada": "ALTA"}
    with patch("builtins.open", side_effect=OSError("disco")), pytest.raises(OSError):
        a.escribir("F4", "AG-10", e)
    assert a.leer("F4") == []
    a.escribir("F4", "AG-10", e)
    assert a.verificar_integridad("F4")["F4"]


def test_truncado_despues_de_reabrir(tmp_path):
    a = Almacen(tmp_path)
    for k in ("uno", "dos"):
        a.escribir("F5", "AG-01", {"id": k})
    p = tmp_path / ARCHIVOS["F5"]
    p.write_bytes(p.read_bytes().splitlines(keepends=True)[0])
    assert not a.verificar_integridad("F5")["F5"]
    with pytest.raises(ValueError, match="integridad"):
        Almacen(tmp_path)


def test_reserva_f10_y_fecha_de_efecto(tmp_path):
    a = Almacen(tmp_path)
    a.reloj.fijar(AS_OF)
    with pytest.raises(EscrituraFueraDeReserva):
        a.escribir("F10", "AG-01", {"tipo_entrada": "OTRO", "param_id": "P-32", "valor_vigente": "x"})
    a.escribir("F10", "OPERADOR", {"tipo_entrada": "PARAMETRO", "param_id": "P-02", "valor_vigente": ["DIV"]})
    a.escribir("F10", "AG-01", {"tipo_entrada": "CFG", "param_id": "P-02",
                                "valor_vigente": ["RV"], "fecha_efecto": "2026-06-06"})
    assert a.estado("F10", AS_OF)["P-02"]["valor_vigente"] == ["DIV"]
    assert a.estado("F10", "2026-06-06")["P-02"]["valor_vigente"] == ["RV"]


def test_plazo_intradía(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    c = b.consultas.enviar({"tipo":"OTRA", "modo":"BLOQUEANTE", "clases":["RV"],
                            "preguntas":[{"texto":"¿RV?", "supuesto_declarado":"esperar"}],
                            "plazo_respuesta":"2026-06-05T10:00+02:00"}, AS_OF)
    assert not b.consultas.vencer("2026-06-05T07:59Z")
    assert b.consultas.vencer("2026-06-05T08:00Z") == [c["cns_id"]]


def test_seg_fin_forzado_y_respuesta_sensible(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    b.almacen.escribir("F11","AG-01",{"seg_id":"SEG-X","opp_id":"OPP-X","estado":"ACTIVO",
                                       "clase":"RV","fecha_fin":"2026-06-06","frecuencia":"DIARIA"})
    marcador = "sk-" + "x"*21
    with pytest.raises(DatosSensibles):
        b.seguimientos.respuesta_broker("SEG-X", marcador, as_of=AS_OF)
    assert marcador not in str(b.almacen.leer("F11"))
    b.seguimientos.ejecutar("2026-06-12","SEG-X",forzar=True)
    assert b.seguimientos.encargos()["SEG-X"]["estado"] == "FINALIZADO"


def test_sello_legacy_y_disco_sin_espacio_al_confirmar(tmp_path):
    a = Almacen(tmp_path)
    a.escribir("F5", "AG-01", {"id": "primero"})
    ruta = tmp_path / ARCHIVOS["F5"]
    original = ruta.read_bytes()
    (tmp_path / "sellos_integridad.json").unlink()  # simula un directorio anterior a T-87
    (tmp_path / "formato_almacen.json").unlink()    # T-92: un directorio anterior tampoco tiene la marca de formato
    a = Almacen(tmp_path)
    assert ruta.read_bytes() == original
    with patch.object(a, "_guardar_json", side_effect=OSError("sin espacio")), pytest.raises(OSError):
        a.escribir("F5", "AG-01", {"id": "fallido"})
    assert ruta.read_bytes() == original
    assert list(Almacen(tmp_path).estado("F5")) == ["primero"]


def test_dos_procesos_asignan_ids_y_escriben_el_mismo_registro(tmp_path):
    import subprocess
    import sys
    from pathlib import Path
    ejecutor = Path(__file__).resolve().parents[1]
    programa = """from bloque_a.almacen import Almacen
import sys
a = Almacen(sys.argv[1])
print('listo', flush=True)
input()
for _ in range(12):
    a.escribir('F5', 'AG-01', {'id': a.nuevo_id('PET')})
"""
    procesos = [subprocess.Popen([sys.executable, "-c", programa, str(tmp_path)], cwd=ejecutor,
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True) for _ in range(2)]
    try:
        for proc in procesos:
            assert proc.stdout.readline().strip() == "listo"
        for proc in procesos:
            proc.stdin.write("seguir\n")
            proc.stdin.flush()
        for proc in procesos:
            assert proc.wait(timeout=30) == 0
    finally:
        for proc in procesos:
            if proc.poll() is None:
                proc.kill()
            proc.communicate()
    a = Almacen(tmp_path)
    assert len(a.estado("F5")) == len(a.leer("F5")) == 24
    assert a.verificar_integridad("F5")["F5"]
