"""T-142 · Cadena de encargos A → B (Fase 6): la petición CT-B-01 que el Broker construye desde una opción del paquete
de oportunidades (`bloque_a/cadena_b.py`), la correspondencia de ámbitos `[PROPUESTO]` (INC-T142-01) y la vuelta CT-04.

Del Bloque B solo se leen ficheros como datos (su Documento 0, su ejemplo de petición desde el Bloque A y sus ámbitos de
ejemplo); no se importa su código. Que su ejecutor admita las peticiones lo comprueba `.docs/scripts/cadena_a_b.py`."""
import copy
import importlib.util
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd
import pytest
import yaml
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO, cargar_config, fusionar
from bloque_a.herramientas.ht01_datos import ProveedorCSV, cargar_universo
from bloque_a.llm import MockClient
from bloque_a.orquestacion import Bloque
from conftest import DATOS

from bloque_a import cadena_b

EJECUTOR = Path(__file__).resolve().parents[1]
REPO = EJECUTOR.parents[1]
BLOQUE_B = REPO / "bloque_b"
EJEMPLO_A = EJECUTOR.parent / "06_Plantillas_entregables" / "Ejemplo - Paquete de oportunidades - V5.0.json"
AS_OF = "2024-03-29"
TIPOS = {"RV", "RF", "DIV", "MP", "IDX", "FON", "DER", "INM", "CRI", "ALT", "MON", "TCV"}


def _doc0(carpeta: Path) -> str:
    [f] = [p for p in carpeta.iterdir() if unicodedata.normalize("NFC", p.name).startswith("Documento 0") and p.suffix == ".md"]
    return f.read_text(encoding="utf-8")


def _bloque_json(texto: str, titulo: str) -> dict:
    """El primer bloque ```json que sigue al título dado (los campos mínimos de un contrato en un Anexo B)."""
    resto = texto[texto.index(titulo):]
    m = re.search(r"```json\n(.*?)```", resto, re.DOTALL)
    assert m, titulo
    return json.loads(m.group(1))


@pytest.fixture(scope="module")
def b1():
    """Anexo B.1 del Documento 0 del Bloque B: campos mínimos de CT-B-01 (`peticion`)."""
    return _bloque_json(_doc0(BLOQUE_B / "01_Gobernanza"), "### B.1 CT-B-01")


@pytest.fixture(scope="module")
def cfg():
    return cargar_config()


@pytest.fixture(scope="module")
def ejemplo():
    return json.loads(EJEMPLO_A.read_text(encoding="utf-8"))


def _cfg_ejemplo(cfg, tabla=None):
    """Configuración con una tabla para los símbolos del ejemplo publicado (no son del universo de ejemplo)."""
    return fusionar(cfg, {"cadena_b": {"correspondencia_ambitos": tabla if tabla is not None else {"LETRAS-EUR-12M": "liquidez_eur"}}})


@pytest.fixture(scope="module")
def ciclo(tmp_path_factory):
    """Un ciclo C1 simulado con la configuración por defecto (solo divisas), como el de `cadena_a_b.py`."""
    tmp = tmp_path_factory.mktemp("t142")
    b = Bloque(cargar_config(), ProveedorCSV(DATOS), cargar_universo(RUTA_UNIVERSO_EJEMPLO), MockClient(),
               tmp / "estado", tmp / "ent")
    r = b.ciclo(AS_OF)
    return b, r["paquete"]


# ---------------------------------------------------------------- CA-1 · la petición, campo a campo frente a B.1 y §6.1
def test_peticion_campo_a_campo_frente_al_anexo_b1_del_bloque_b(ciclo, cfg, b1):
    _, paquete = ciclo
    pet = cadena_b.construir_peticion(paquete, "OPP-2024-0002", cfg)
    assert set(pet) == set(b1)                                   # ni un campo inventado ni uno de menos
    assert pet["origen"] == "BLOQUE_A" and pet["origen"] in b1["origen"].split("|")
    assert pet["pet_ref_broker"] == f"{paquete['run_id']}/OPP-2024-0002"
    entrada = next(e for e in paquete["paquete_para_bloque_B"] if e["opp_id"] == "OPP-2024-0002")
    assert pet["paquete_para_bloque_B"] == {**entrada, "x_clave_universo": "divisas_materias_primas"}   # tal cual + x_
    # objeto: los campos de B.1 más `clave_universo` (extensión documentada en el README del ejecutor de B, 3)
    assert set(pet["objeto"]) == set(b1["objeto"]) | {"clave_universo"}
    assert pet["objeto"]["clave_universo"] == "divisas_materias_primas"
    assert pet["objeto"]["ambito"] == entrada["ambito"] and set(pet["objeto"]["ambito"]) == set(b1["objeto"]["ambito"])
    assert pet["objeto"]["descripcion"] == entrada["nombre"]
    assert pet["objeto"]["tipo_objeto_sugerido"] is None                # B.1 admite null: lo encuadra el Director de B
    assert pet["tipos_activo_admitidos"] == ["DIV"] and set(pet["tipos_activo_admitidos"]) <= TIPOS
    assert pet["horizontes"] == entrada["horizontes"] and set(pet["horizontes"]) <= {"H1", "H2", "H3", "H4", "H5"}
    assert pet["preguntas"] == []                                        # las de A van en paquete_para_bloque_B.preguntas_para_B
    assert pet["nivel"] == "AUTO" and pet["nivel"] in b1["nivel"].split("|")
    assert pet["prioridad"] == "NORMAL" and pet["prioridad"] in b1["prioridad"].split("|")
    assert pet["limite"] == {k: None for k in b1["limite"]}
    assert pet["marco_invertibilidad"] == {"perfil": "MINORISTA_UE_DEFECTO"}
    assert set(pet["marco_invertibilidad"]) <= set(b1["marco_invertibilidad"])
    assert pet["marco_invertibilidad"]["perfil"] == b1["marco_invertibilidad"]["perfil"]
    assert (pet["top_n"], pet["alto_impacto"], pet["referencia_previa"], pet["fecha_objetivo"]) == (None, False, None, None)
    assert pet["idioma_usuario"] == cfg["idioma"] == b1["idioma_usuario"]
    json.dumps(pet, allow_nan=False)                                     # JSON estricto


def test_paquete_para_b_cubre_los_campos_que_el_bloque_b_espera(ciclo, cfg, b1):
    """El encargo de A trae los campos de B.1 salvo `puntuaciones_A`, que el esquema V5.0 del Bloque A no tiene
    (INC-T142-01); A añade los suyos (horizonte principal, nombre…), que B trata como pista (R31)."""
    _, paquete = ciclo
    pet = cadena_b.construir_peticion(paquete, "OPP-2024-0002", cfg)
    falta = set(b1["paquete_para_bloque_B"]) - set(pet["paquete_para_bloque_B"])
    assert falta == {"puntuaciones_A"}


def test_las_dos_claves_van_donde_las_pone_el_ejemplo_del_bloque_b(ciclo, cfg):
    ej = json.loads((BLOQUE_B / "11_Ejecutor" / "ejemplos" / "peticiones" / "peticion_redes_bloque_a.json").read_text(encoding="utf-8"))
    _, paquete = ciclo
    pet = cadena_b.construir_peticion(paquete, "OPP-2024-0002", cfg)
    assert ej["origen"] == pet["origen"] == "BLOQUE_A"
    assert ej["paquete_para_bloque_B"]["x_clave_universo"] == ej["objeto"]["clave_universo"]
    assert pet["paquete_para_bloque_B"]["x_clave_universo"] == pet["objeto"]["clave_universo"]
    assert set(ej) - {"fecha_objetivo"} <= set(pet)


def test_no_muta_el_paquete(ciclo, cfg):
    _, paquete = ciclo
    antes = copy.deepcopy(paquete)
    cadena_b.construir_peticion(paquete, "OPP-2024-0002", cfg)
    with pytest.raises(cadena_b.ErrorCadenaB):
        cadena_b.construir_peticion(paquete, "OPP-2024-0001", cfg)
    assert paquete == antes


def test_tipos_secundarios_de_la_opcion_entran_en_los_admitidos(ejemplo, cfg):
    p = copy.deepcopy(ejemplo)
    opcion = next(o for o in p["clases"]["MON"]["opciones"] if o["opp_id"] == "OPP-2026-9112")
    opcion["tipos_secundarios"] = ["RF", "MON"]
    pet = cadena_b.construir_peticion(p, "OPP-2026-9112", _cfg_ejemplo(cfg))
    assert pet["tipos_activo_admitidos"] == ["MON", "RF"]
    assert pet["objeto"]["clave_universo"] == "liquidez_eur"


# ---------------------------------------------------------------- Broker: qué opciones se envían
def test_opciones_enviables_son_las_de_enviar_a_b(ejemplo, ciclo):
    esperado = [o["opp_id"] for c in ejemplo["clases"].values() for o in c["opciones"]
                if o["siguiente_paso_sugerido"] == "ENVIAR_A_BLOQUE_B"]
    assert cadena_b.opciones_enviables(ejemplo) == esperado and len(esperado) == 7
    _, paquete = ciclo
    assert cadena_b.opciones_enviables(paquete) == ["OPP-2024-0001", "OPP-2024-0002", "OPP-2024-0003"]


# ---------------------------------------------------------------- correspondencia de ámbitos [PROPUESTO]
def test_correspondencia_por_defecto_casa_con_los_dos_universos(cfg):
    tabla = cfg["cadena_b"]["correspondencia_ambitos"]
    ambitos_b = yaml.safe_load((BLOQUE_B / "11_Ejecutor" / "config" / "ambitos_ejemplo.yaml").read_text(encoding="utf-8"))
    universo = pd.read_csv(RUTA_UNIVERSO_EJEMPLO).set_index("simbolo")
    assert tabla and set(tabla.values()) <= set(ambitos_b)              # cada clave existe en el Bloque B
    for simbolo, clave in tabla.items():
        assert simbolo in universo.index                                 # cada ámbito existe en el Bloque A
        assert universo.loc[simbolo, "clase"] in ambitos_b[clave]["tipos_activo"]   # y del mismo tipo de activo


def test_sin_correspondencia_falla_cerrado(ciclo, cfg):
    _, paquete = ciclo
    for opp in ("OPP-2024-0001", "OPP-2024-0003"):                       # USD/JPY y USD/MXN: sin ámbito en B
        with pytest.raises(cadena_b.ErrorCadenaB) as e:
            cadena_b.construir_peticion(paquete, opp, cfg)
        assert e.value.codigo == "SIN_CORRESPONDENCIA_AMBITO"


def test_sin_simbolo_no_hay_correspondencia(ejemplo, cfg):
    p = copy.deepcopy(ejemplo)
    for e in p["paquete_para_bloque_B"]:
        if e["opp_id"] == "OPP-2026-9112":
            e["indicador_seguimiento"]["simbolo"] = None
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(p, "OPP-2026-9112", _cfg_ejemplo(cfg))
    assert e.value.codigo == "SIN_CORRESPONDENCIA_AMBITO"


@pytest.mark.parametrize("seccion", [None, "no es una tabla", {"correspondencia_ambitos": ["LETRAS-EUR-12M"]},
                                     {"correspondencia_ambitos": {"LETRAS-EUR-12M": ""}},
                                     {"correspondencia_ambitos": {"LETRAS-EUR-12M": 7}}])
def test_configuracion_ausente_o_mal_formada_falla_cerrado(ejemplo, cfg, seccion):
    c = {k: v for k, v in cfg.items() if k != "cadena_b"}
    if seccion is not None:
        c["cadena_b"] = seccion
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(ejemplo, "OPP-2026-9112", c)
    assert e.value.codigo == "CONFIGURACION_CADENA_B"


@pytest.mark.parametrize("falta", ["nivel", "prioridad", "perfil_invertibilidad"])
def test_sin_valor_por_defecto_de_la_peticion_falla_cerrado(ejemplo, cfg, falta):
    c = _cfg_ejemplo(cfg)
    c["cadena_b"]["peticion"] = {k: v for k, v in c["cadena_b"]["peticion"].items() if k != falta}
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(ejemplo, "OPP-2026-9112", c)
    assert e.value.codigo == "CONFIGURACION_CADENA_B" and falta in e.value.detalle


def test_sonda_sin_correspondencia_no_lleva_clave(ciclo, cfg):
    _, paquete = ciclo
    pet = cadena_b.construir_peticion(paquete, "OPP-2024-0001", cfg, exigir_correspondencia=False)
    assert "x_clave_universo" not in pet["paquete_para_bloque_B"] and "clave_universo" not in pet["objeto"]
    c = {k: v for k, v in cfg.items() if k != "cadena_b"}                # los demás fallos siguen cerrando
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(paquete, "OPP-2024-0001", c, exigir_correspondencia=False)
    assert e.value.codigo == "CONFIGURACION_CADENA_B"


# ---------------------------------------------------------------- el paquete de A se valida antes de construir
def test_opcion_desconocida_o_duplicada(ejemplo, cfg):
    c = _cfg_ejemplo(cfg)
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(ejemplo, "OPP-2026-0000", c)
    assert e.value.codigo == "OPCION_DESCONOCIDA"
    p = copy.deepcopy(ejemplo)
    p["paquete_para_bloque_B"].append(copy.deepcopy(next(x for x in p["paquete_para_bloque_B"] if x["opp_id"] == "OPP-2026-9112")))
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(p, "OPP-2026-9112", c)
    assert e.value.codigo == "OPCION_DUPLICADA"
    p = copy.deepcopy(ejemplo)                                           # opción sin encargo para B
    p["paquete_para_bloque_B"] = [x for x in p["paquete_para_bloque_B"] if x["opp_id"] != "OPP-2026-9112"]
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(p, "OPP-2026-9112", c)
    assert e.value.codigo == "OPCION_DESCONOCIDA"


@pytest.mark.parametrize("estropear", [lambda e: e.pop("tesis"), lambda e: e.update(horizontes=[]),
                                       lambda e: e.update(tipo_activo="ACCIONES"), lambda e: e.update(campo_nuevo=1)])
def test_encargo_que_no_cumple_el_esquema_de_a_no_se_envia(ejemplo, cfg, estropear):
    p = copy.deepcopy(ejemplo)
    estropear(next(x for x in p["paquete_para_bloque_B"] if x["opp_id"] == "OPP-2026-9112"))
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(p, "OPP-2026-9112", _cfg_ejemplo(cfg))
    assert e.value.codigo == "ENTRADA_B_INVALIDA"


@pytest.mark.parametrize("paquete", [[], {"clases": {}}, {"run_id": "", "clases": {}}])
def test_paquete_invalido(cfg, paquete):
    with pytest.raises(cadena_b.ErrorCadenaB) as e:
        cadena_b.construir_peticion(paquete, "OPP-2026-9112", cfg)
    assert e.value.codigo == "PAQUETE_INVALIDO"


# ---------------------------------------------------------------- la vuelta: CT-04 al Bloque A (7.7 y Anexo B)
RESPUESTA_B = {"pet_id": "PET-B-2024-0001", "rec_id": "REC-B-2024-0001", "estado_peticion": "ENTREGADA",
               "resumen": {"veredicto": "VIGILAR", "resultado_del_analisis": "CONCLUYENTE"},
               "acuse_inmediato": {"pet_id": "PET-B-2024-0001", "admision": "ADMITIDA"}}


def test_ct04_de_vuelta_con_los_campos_del_anexo_b_de_a():
    ct04_doc = _bloque_json(_doc0(EJECUTOR.parent / "01_Gobernanza"), "**CT-04 Retroalimentación y configuración**")
    ct04 = cadena_b.ct04_desde_respuesta_b("OPP-2024-0002", RESPUESTA_B)
    assert set(ct04) <= set(ct04_doc)
    [d] = ct04["decisiones"]
    assert set(d) == set(ct04_doc["decisiones"][0])
    assert d["decision"] == "ENVIADA_A_BLOQUE_B" and d["decision"] in ct04_doc["decisiones"][0]["decision"].split("|")
    assert set(ct04["resultado_comunicado"]) == set(ct04_doc["resultado_comunicado"])
    texto = ct04["resultado_comunicado"]["texto"]
    for trozo in ("PET-B-2024-0001", "ADMITIDA", "ENTREGADA", "REC-B-2024-0001", "VIGILAR", "CONCLUYENTE"):
        assert trozo in texto


def test_ct04_solo_con_lo_que_devuelve_b():
    ct04 = cadena_b.ct04_desde_respuesta_b("OPP-2024-0002", {"pet_id": "PET-B-2024-0002", "admision": "RECHAZADA",
                                                             "motivo": "AMBITO_INDETERMINADO"})
    assert ct04["resultado_comunicado"]["texto"] == "Bloque B PET-B-2024-0002; admisión RECHAZADA; motivo AMBITO_INDETERMINADO"
    for mala in (None, {}, {"pet_id": ""}, ["PET-B-2024-0001"]):
        with pytest.raises(cadena_b.ErrorCadenaB) as e:
            cadena_b.ct04_desde_respuesta_b("OPP-2024-0002", mala)
        assert e.value.codigo == "RESPUESTA_B_INVALIDA"


def test_ct04_lo_registra_el_bloque_a(ciclo):
    b, _ = ciclo
    r = b.decision(cadena_b.ct04_desde_respuesta_b("OPP-2024-0002", RESPUESTA_B), AS_OF)
    assert r["estado"] == "APLICADA"
    f3 = [e for e in b.almacen.leer("F3") if e.get("tipo_entrada") == "DECISION_BROKER" and e.get("opp_id") == "OPP-2024-0002"]
    assert f3 and f3[-1]["decision_broker"]["decision"] == "ENVIADA_A_BLOQUE_B"
    f5 = [e for e in b.almacen.leer("F5") if e.get("tipo_entrada") == "RET" and e.get("id") == r["ret_id"]]
    assert f5 and "REC-B-2024-0001" in f5[-1]["resultado_comunicado"]["texto"]
    assert all(b.almacen.verificar_integridad().values())                # cadena de hash intacta


# ---------------------------------------------------------------- el script de punta a punta falla cerrado
def test_script_rechaza_una_correspondencia_con_claves_que_b_no_tiene(tmp_path):
    spec = importlib.util.spec_from_file_location("cadena_a_b", REPO / ".docs" / "scripts" / "cadena_a_b.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    extra = tmp_path / "extra.yaml"
    extra.write_text("cadena_b:\n  correspondencia_ambitos:\n    AUDUSD=X: no_existe_en_b\n", encoding="utf-8")
    assert mod.main(["--trabajo", str(tmp_path / "w"), "--config-a", str(extra)]) == 2
    assert not (tmp_path / "w" / "a").exists()                           # no llegó a ejecutar ningún bloque
