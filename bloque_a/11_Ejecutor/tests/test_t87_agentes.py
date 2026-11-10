"""T-87: pruebas adversariales sobre caché, coste, evidencia y adaptador de modelos. Sin red."""
import json
from types import SimpleNamespace

import pytest
from bloque_a.agentes import Agentes
from bloque_a.almacen import Almacen
from bloque_a.consumo import Contabilidad, Presupuesto
from bloque_a.herramientas.ht06_indice import CacheResultados
from bloque_a.llm import AnthropicClient, MockClient, ReplayClient, ReplayFaltante
from bloque_a.referencias import Referencias
from conftest import config_pruebas, nuevo_bloque

C5 = {"agente": "AG-20", "contrato": "C5", "mensaje": {"resueltos_hoy": 1, "metricas_por_celda": {}},
          "esquema_clave": "APRENDIZAJE", "instrucciones": "Resume", "contexto": {"fecha_as_of": "2024-01-05", "modo": "backtest"}}
VALIDA = '{"resumen":"control","lecciones":[]}'


class SDK:
    def __init__(self, texto=VALIDA, stop="end_turn"):
        self.texto, self.stop = texto, stop
        self.messages = self
        self.llamadas = []

    def create(self, **kwargs):
        self.llamadas.append(kwargs)
        if isinstance(self.texto, Exception):
            raise self.texto
        return SimpleNamespace(stop_reason=self.stop, usage=SimpleNamespace(input_tokens=50, output_tokens=20),
                               content=[SimpleNamespace(type="text", text=self.texto)])


def agentes(tmp, cliente, cache=None, **extra):
    cfg = config_pruebas(**extra)
    return Agentes(cfg, cliente, Almacen(tmp / "estado"), Contabilidad(cfg), cache=cache)


def test_separa_cache_por_cliente_prompt_y_limite(tmp_path):
    cache = CacheResultados(tmp_path / "cache.jsonl")
    assert agentes(tmp_path, MockClient(), cache).invocar(**C5).estado == "COMPLETO"
    sdk = SDK()
    real = agentes(tmp_path, AnthropicClient(sdk=sdk), cache)
    r = real.invocar(**C5)
    assert r.datos == json.loads(VALIDA) and not r.cache_hit
    assert real.invocar(**C5).cache_hit
    real.prompts._cache["AG-20"] += "\nNueva política."
    assert not real.invocar(**C5).cache_hit
    real.cfg["max_tokens"]["AG-20"] = 99
    assert not real.invocar(**C5).cache_hit
    assert len(sdk.llamadas) == 3


@pytest.mark.parametrize("formato", ["json", "texto", "malformado", "truncado"])
def test_r8_no_reenvia_ni_persiste(tmp_path, formato):
    marcador = "MARCADOR-FICTICIO-DE-QA"
    dato = '{"password":"' + marcador + '"}'
    texto = {"json": '{"resumen":' + dato + ',"lecciones":[]}', "texto": "respuesta " + dato,
             "truncado": '{"password":"' + marcador, "malformado": '{"resumen":' + dato}[formato]
    sdk = SDK(texto, "pause_turn")
    graba = ReplayClient(tmp_path / "cinta.jsonl", "grabar", AnthropicClient(sdk=sdk))
    a = agentes(tmp_path, graba, CacheResultados(tmp_path / "cache.jsonl"))
    r = a.invocar(**C5)
    assert r.estado == "PARCIAL" and len(sdk.llamadas) == 1 and r.uso.salida == 20
    assert all(marcador not in p.read_text() for p in tmp_path.rglob("*.jsonl"))
    assert agentes(tmp_path, ReplayClient(tmp_path / "cinta.jsonl")).invocar(**C5).estado == "PARCIAL"
    assert a.invocar(**{**C5, "mensaje": {"password": marcador}}).estado == "PARCIAL"
    assert len(sdk.llamadas) == 1


@pytest.mark.parametrize("stop", ["pause_turn", "refusal", "max_tokens"])
def test_turno_incompleto_es_parcial_en_directo_y_replay(tmp_path, stop):
    sdk = SDK(stop=stop)
    cinta = tmp_path / "cinta.jsonl"
    graba = ReplayClient(cinta, "grabar", AnthropicClient(sdk=sdk, max_continuaciones=0))
    assert agentes(tmp_path, graba).invocar(**C5).estado == "PARCIAL"
    assert agentes(tmp_path, ReplayClient(cinta)).invocar(**C5).estado == "PARCIAL"
    assert agentes(tmp_path, AnthropicClient(sdk=SDK())).invocar(**C5).estado == "COMPLETO"
    a = agentes(tmp_path, ReplayClient(cinta))
    a.cfg["max_tokens"]["AG-20"] = 101
    with pytest.raises(ReplayFaltante):
        a.invocar(**C5)


def test_limite_total_de_ampliacion(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    b.fijar_fecha("2026-06-05")
    p = Presupuesto({"RV": 10}, b.cfg)
    p.cargar("RV", 12.5)
    assert not b._solicitar_ampliacion(p, "RV", 5, "RUN-2026-0001", "refutacion")
    assert b._solicitar_ampliacion(p, "RV", 2.5, "RUN-2026-0001", "refutacion")
    assert not b._solicitar_ampliacion(p, "RV", 3, "RUN-2026-0001", "refutacion")
    assert p.disponible("RV") == 2.5


def test_transporte_agotado_cierra_run_parcial_con_incidencia(tmp_path, universo):
    sdk = SDK(RuntimeError("Fallo simulado"))
    b = nuevo_bloque(tmp_path, universo, cliente=AnthropicClient(sdk=sdk))
    run = b.ciclo("2026-06-05", alcance={"clases": ["RV", "RF"]}, nivel_forzado="N2")
    assert run["estado"] == "PARCIAL"
    assert any("error_proveedor" in str(i) for i in b.almacen.leer("HA"))
    assert any(f["id"] == run["run_id"] for f in b.almacen.leer("F5") if f["tipo_entrada"] == "RUN")


def test_referencia_no_ofrecida_no_llega_a_f2(tmp_path, universo):
    sdk = SDK()
    b = nuevo_bloque(tmp_path, universo, cliente=AnthropicClient(sdk=sdk), anonimizar=False)
    corte = b.fijar_fecha("2000-06-05")
    futura = "REF-ANA-DOC-0280"
    assert b.referencias.por_id(futura)["anio"] == 2023
    sdk.texto = json.dumps({"referencias": [{"ref_id": futura}], "sintesis": "test", "lagunas": []})
    pet = b._peticion_conocimiento("RV", {"proxy":"XLV"}, {"tipo":"CT-08"}, [], corte, "RUN-2000-0001", None)
    assert pet["estado"] == "SIN_RESULTADO" and not pet["piezas"]
    assert futura not in str(sdk.llamadas[0]["messages"])


def test_referencia_con_solo_anio_disponible_al_terminar_el_anio():
    ref = Referencias.__new__(Referencias)
    ref.fichas = {"F7": [{"ref_id":"prueba", "titulo":"prueba", "q":1, "nivel":"A", "tematica":"TA-05", "anio":2025}]}
    def consultar(fecha):
        return ref.para_clase("RV", fecha, "backtest", archivos=("F7",))["referencias"]
    assert not consultar("2025-12-30") and consultar("2025-12-31")


def test_cita_inventada_no_es_evidencia_verificada(tmp_path, universo):
    b = nuevo_bloque(tmp_path, universo)
    fecha = b.fijar_fecha("2026-06-05")
    senales, _ = b.senales_clase("RV", fecha, "RUN-2026-0001")
    proxy = next(iter(senales))
    def pieza(origen):
        return {"afirmacion":"Se multiplicará por mil", "fuente":origen, "direccion":"favorable", "extracto":"sin datos", "origen":"AG-03"}
    f = {"proxy":proxy, "senales":senales[proxy], "_piezas":[pieza("CALC-2026-9999"), pieza("HT-01:INEXISTENTE"),
         pieza("HT-01:"+proxy), pieza("REF-ANA-DOC-0280")]}
    b._registrar_evidencia_clase({"clase":"RV","nivel":"N1","finalistas":[f]},fecha,"RUN-2026-0001")
    ev, = [x for x in b.almacen.leer("F2") if x["tipo_entrada"] == "EVD"]
    assert ev["estado_verificacion"] == "PENDIENTE" and not f["_ps1"] and not f["_raices"]
    s = senales[proxy]
    f["_piezas"] = [{"afirmacion": f"La señal compuesta de {proxy} es {s['senal_compuesta']:.2f} con tendencia «{s['tendencia_26s']}» a 26 semanas",
                     "direccion": "favorable" if s["senal_compuesta"] >= 0.5 else "contraria", "fuente": "HT-01:"+proxy, "origen":"AG-03"}]
    b._registrar_evidencia_clase({"clase":"RV","nivel":"N1","finalistas":[f]},fecha,"RUN-2026-0001")
    assert any(x.get("estado_verificacion") == "VERIFICADA" and x["ref_id"] == "HT-01:"+proxy for x in b.almacen.leer("F2"))



def test_cinta_anterior_recupera_truncamiento(tmp_path):
    mensajes = [{"role": "user", "content": "encargo anterior"}]
    system = [{"type": "text", "text": "sistema"}]
    cinta = tmp_path / "anterior.jsonl"
    clave = ReplayClient.clave("AG-20", "modelo", system, mensajes, None)
    cinta.write_text(json.dumps({"clave": clave, "agente": "AG-20", "modelo": "modelo", "texto": VALIDA,
                                 "uso": {"salida": 4}, "stop_reason": "max_tokens"}) + "\n")
    r = ReplayClient(cinta).generar(agente="AG-20", modelo="modelo", system=system, mensajes=mensajes, max_tokens=20)
    assert r.truncada and r.uso.salida == 4
