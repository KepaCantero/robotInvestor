"""T-120 · Dos hallazgos fuera de ticket de la QA r01 de T-116: el IBAN con separadores (R8) y el máximo de lecciones."""
import pytest
from bloque_a.almacen import Almacen
from bloque_a.configuracion import cargar_config, parametro
from bloque_a.contratos import DatosSensibles, contiene_credenciales, secretos_en_texto
from bloque_a.evaluador import Evaluador
from conftest import AS_OF, config_pruebas, nuevo_bloque

IBAN = "ES91" + "21000418450200051332"       # el IBAN de ejemplo de la documentación bancaria, partido
GRUPOS = [IBAN[i:i + 4] for i in range(0, 24, 4)]


@pytest.mark.parametrize("separador", ["", " ", ".", "-"])
def test_el_iban_se_detecta_con_y_sin_separador_entre_grupos(separador):
    texto = f"cobren en {separador.join(GRUPOS)}, gracias"
    assert secretos_en_texto(texto) and contiene_credenciales({"comentario": texto})
    assert contiene_credenciales({"a": [{"b": texto}]})


@pytest.mark.parametrize("texto", [
    "El índice ES50 cerró en 4 900 puntos.", "ES91 2100 0418 4502 0005", "ES91 2100 0418 4502 0005 133", "ES9 2100 0418 4502 0005 1332",
    "RES91 2100 0418 4502 0005 1332", "ES91  2100  0418  4502  0005  1332", "ES91 2100 0418 4502 0005 13320", "es91 2100 0418 4502 0005 1332",
    "Entre 2100 0418 4502 y 0005 1332 hay series de cuatro cifras.", "ISIN ES0113900J37 y ES0000012B88",
])
def test_lo_que_no_es_un_iban_espanol_no_se_marca(texto):
    assert secretos_en_texto(texto) == []


def test_un_ct04_con_solo_un_iban_con_espacios_se_rechaza_y_no_queda_en_ningun_archivo(tmp_path, universo):
    """Antes se admitía (APLICADA) y el IBAN quedaba en F5."""
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha(AS_OF)
    iban = " ".join(GRUPOS)
    with pytest.raises(DatosSensibles):
        b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": f"cobren en {iban}"}}, AS_OF)
    incs = [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]
    assert len(incs) == 1 and incs[0]["campo_afectado"] == ["valoracion_informe"]
    for p in tmp_path.rglob("*"):
        if p.is_file():
            cuerpo = p.read_text(encoding="utf-8", errors="ignore")
            assert iban not in cuerpo and "2100 0418" not in cuerpo and IBAN not in cuerpo, p


def _con_lecciones(tmp_path, n):
    a = Almacen(tmp_path)
    a.reloj.fijar(AS_OF)
    for i in range(1, n + 1):
        a.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": f"LEC-2026-{i:04d}", "fecha": AS_OF, "ambito": {"clase": "DIV"}, "nivel": "B",
                                   "tipo": "CALIBRACION", "observacion": f"o{i}", "evidencia": [], "recomendacion": f"r{i}",
                                   "fuerza": "recurrente", "n": 30, "caducidad": "2027-06-05", "estado": "VIGENTE", "origen": "DETERMINISTA"})
    return a


def test_el_maximo_de_lecciones_sale_de_la_configuracion(tmp_path):
    assert parametro(cargar_config(), "aprendizaje.lecciones_por_encargo") == 10
    a = _con_lecciones(tmp_path, 14)
    assert len(Evaluador(a, None, None, config_pruebas(), None).lecciones_vigentes(AS_OF, "DIV")) == 10
    assert len(Evaluador(a, None, None, {"evaluacion": {}}, None).lecciones_vigentes(AS_OF, "DIV")) == 10     # configuración parcial
    cuatro = Evaluador(a, None, None, config_pruebas(aprendizaje={"lecciones_por_encargo": 4}), None)
    assert [x["id"] for x in cuatro.lecciones_vigentes(AS_OF, "DIV")] == [f"LEC-2026-{i:04d}" for i in range(1, 5)]
    assert len(cuatro.lecciones_vigentes(AS_OF, "DIV", max_n=12)) == 12                                        # el argumento explícito manda
