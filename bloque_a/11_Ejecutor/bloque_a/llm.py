"""Clientes de modelo de lenguaje.

- `AnthropicClient`: cliente real (SDK `anthropic` 2.x, `messages.create`). El system prompt se envía
  como lista de bloques de texto con `cache_control` (caché de prompts); la herramienta de servidor de
  búsqueda web (`web_search_20260318`) solo se añade cuando el orquestador lo permite (nunca en
  backtest); gestiona `pause_turn` (continuación) y registra tokens de entrada, salida, escritura y
  lectura de caché y búsquedas web.
- `MockClient`: respuestas sintéticas deterministas (semilla) generadas a partir del encargo
  (`bloque_a.mock_respuestas`), válidas frente a los esquemas y sensibles a la entrada.
- `ReplayClient`: graba las respuestas de otro cliente en JSONL y las reproduce exactamente
  (reproducibilidad de backtests con el modelo real).
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .configuracion import parametro
from .contratos import secretos_en_texto


@dataclass
class Uso:
    entrada: int = 0            # tokens de entrada no cacheados
    salida: int = 0
    cache_escritura: int = 0
    cache_lectura: int = 0
    busquedas_web: int = 0

    def sumar(self, otro: "Uso") -> None:
        for k in asdict(self):
            setattr(self, k, getattr(self, k) + getattr(otro, k))


@dataclass
class RespuestaLLM:
    texto: str
    uso: Uso
    modelo: str
    stop_reason: Optional[str] = None
    truncada: bool = False
    rechazo: bool = False
    extra: Dict[str, Any] = field(default_factory=dict)


def contenido_sensible(valor) -> bool:
    """Aplica R8 tanto al JSON estructurado como a texto libre o JSON incompleto."""
    if isinstance(valor, (bytes, bytearray)):
        valor = bytes(valor).decode("utf-8", errors="replace")
    if isinstance(valor, str):
        # Un valor sensible truncado antes de la comilla final también se descarta.
        return bool(secretos_en_texto(valor + '"'))
    if isinstance(valor, dict):
        return (bool(secretos_en_texto(json.dumps(valor, ensure_ascii=False, default=str)))
                or any(contenido_sensible(v) for v in valor.values()))
    if isinstance(valor, (list, tuple)):
        return any(contenido_sensible(v) for v in valor)
    return False


def respuesta_segura(r: RespuestaLLM) -> RespuestaLLM:
    if contenido_sensible(r.texto):
        return RespuestaLLM("", r.uso, r.modelo, stop_reason="contenido_sensible")
    return r


class LLMClient:
    nombre = "base"
    # PA-09 (T-66): ¿el modelo pudo aprender el periodo de un backtest? Por defecto sí (prudente); el simulado, no
    conocimiento_previo = True

    def identidad_cache(self):
        return [type(self).__module__, type(self).__qualname__, self.nombre]

    def generar(self, *, agente: str, modelo: str, system: List[Dict], mensajes: List[Dict], max_tokens: int,
                herramientas: Optional[List[Dict]] = None, esquema: Optional[Dict] = None) -> RespuestaLLM:
        raise NotImplementedError


def herramienta_busqueda_web(tipo: str = "web_search_20260318", max_usos: int = 5) -> Dict:
    """Definición de la herramienta de servidor de búsqueda web (tipos en anthropic.types.WebSearchTool*Param)."""
    return {"type": tipo, "name": "web_search", "max_uses": int(max_usos)}


class AnthropicClient(LLMClient):
    nombre = "anthropic"

    def __init__(self, api_key: Optional[str] = None, max_reintentos: int = 4, timeout_s: float = 600,
                 salida_estructurada: bool = False, max_continuaciones: int = 3, sdk: Any = None) -> None:
        if sdk is None:
            import anthropic
            clave = api_key or os.environ.get("ANTHROPIC_API_KEY")
            if not clave:
                raise RuntimeError("Falta ANTHROPIC_API_KEY (variable de entorno). El bloque nunca la guarda en archivos (R8).")
            sdk = anthropic.Anthropic(api_key=clave, max_retries=max_reintentos, timeout=timeout_s)
        self.sdk = sdk
        self.salida_estructurada = salida_estructurada
        self.max_continuaciones = max_continuaciones

    def identidad_cache(self):
        return [super().identidad_cache(), self.salida_estructurada, self.max_continuaciones]

    @staticmethod
    def _uso(u: Any) -> Uso:
        if u is None:
            return Uso()
        stu = getattr(u, "server_tool_use", None)
        return Uso(entrada=int(getattr(u, "input_tokens", 0) or 0), salida=int(getattr(u, "output_tokens", 0) or 0),
                   cache_escritura=int(getattr(u, "cache_creation_input_tokens", 0) or 0),
                   cache_lectura=int(getattr(u, "cache_read_input_tokens", 0) or 0),
                   busquedas_web=int(getattr(stu, "web_search_requests", 0) or 0) if stu is not None else 0)

    def generar(self, *, agente: str, modelo: str, system: List[Dict], mensajes: List[Dict], max_tokens: int,
                herramientas: Optional[List[Dict]] = None, esquema: Optional[Dict] = None) -> RespuestaLLM:
        if contenido_sensible([system, mensajes]):
            return RespuestaLLM("", Uso(), modelo, stop_reason="contenido_sensible")
        msgs = list(mensajes)
        kwargs: Dict[str, Any] = {"model": modelo, "max_tokens": int(max_tokens), "system": system, "messages": msgs,
                                  "metadata": {"user_id": f"bloque-a-{agente}"}}
        if herramientas:
            kwargs["tools"] = herramientas
        if esquema is not None and self.salida_estructurada:
            kwargs["output_config"] = {"format": {"type": "json_schema", "schema": esquema}}
        uso = Uso()
        textos: List[str] = []
        stop = None
        for _ in range(self.max_continuaciones + 1):
            try:
                resp = self.sdk.messages.create(**kwargs)
            except Exception:
                # El SDK ya ha agotado sus reintentos. Los mensajes de excepción pueden contener secretos.
                return RespuestaLLM("", uso, modelo, stop_reason="error_proveedor")
            uso.sumar(self._uso(getattr(resp, "usage", None)))
            stop = getattr(resp, "stop_reason", None)
            contenido = list(getattr(resp, "content", []) or [])
            textos = [getattr(b, "text", "") for b in contenido if getattr(b, "type", None) == "text"]
            if contenido_sensible("".join(textos)) or any(
                    contenido_sensible(b.model_dump() if hasattr(b, "model_dump") else vars(b)) for b in contenido):
                return RespuestaLLM("", uso, modelo, stop_reason="contenido_sensible")
            if stop == "pause_turn":
                # Turno pausado por una herramienta de servidor: se devuelve el contenido y se continúa.
                msgs = msgs + [{"role": "assistant", "content": contenido}]
                kwargs["messages"] = msgs
                continue
            break
        return RespuestaLLM(texto="".join(textos), uso=uso, modelo=modelo, stop_reason=stop,
                            truncada=(stop == "max_tokens"), rechazo=(stop == "refusal"))


def _tokens_aprox(texto: str) -> int:
    return max(1, int(len(texto) / 3.6))


class MockClient(LLMClient):
    """Cliente simulado determinista. Los tokens se estiman (≈ 3,6 caracteres por token) y la caché de
    prompts se simula: la primera llamada de cada (agente, modelo, system) escribe caché y las demás la leen."""

    nombre = "mock"
    conocimiento_previo = False   # el simulado no sabe nada del periodo: no hay fuga por memoria (PA-09)

    def __init__(self, semilla: int = 20261102, fallos: Optional[Dict[str, int]] = None) -> None:
        self.semilla = int(semilla)
        self._vistos: set = set()
        self._lock = threading.Lock()
        self.llamadas: List[Dict] = []
        self.fallos = dict(fallos or {})   # agente -> nº de respuestas inválidas a devolver (pruebas)

    def identidad_cache(self):
        return [super().identidad_cache(), self.semilla]

    def generar(self, *, agente: str, modelo: str, system: List[Dict], mensajes: List[Dict], max_tokens: int,
                herramientas: Optional[List[Dict]] = None, esquema: Optional[Dict] = None) -> RespuestaLLM:
        from . import mock_respuestas
        sys_txt = "".join(b.get("text", "") for b in system)
        user_txt = "".join(m["content"] if isinstance(m["content"], str) else json.dumps(m["content"], default=str)
                           for m in mensajes if m["role"] == "user")
        clave_sys = hashlib.sha256((agente + modelo + sys_txt).encode()).hexdigest()
        with self._lock:
            primera = clave_sys not in self._vistos
            self._vistos.add(clave_sys)
            self.llamadas.append({"agente": agente, "modelo": modelo, "herramientas": herramientas})
            falla = self.fallos.get(agente, 0) > 0
            if falla:
                self.fallos[agente] -= 1
        if falla:
            datos_txt = '{"respuesta": "no conforme"}'
        else:
            datos = mock_respuestas.responder(agente, mensajes, self.semilla)
            datos_txt = json.dumps(datos, ensure_ascii=False)
        t_sys = _tokens_aprox(sys_txt)
        uso = Uso(entrada=_tokens_aprox(user_txt), salida=_tokens_aprox(datos_txt),
                  cache_escritura=t_sys if primera else 0, cache_lectura=0 if primera else t_sys,
                  busquedas_web=1 if herramientas else 0)
        return RespuestaLLM(texto=datos_txt, uso=uso, modelo=modelo, stop_reason="end_turn")


class ReplayFaltante(KeyError):
    pass


class ReplayClient(LLMClient):
    """Graba (modo «grabar», envolviendo otro cliente) o reproduce (modo «reproducir») respuestas."""

    nombre = "replay"

    def __init__(self, ruta, modo: str = "reproducir", base: Optional[LLMClient] = None) -> None:
        if modo not in ("grabar", "reproducir"):
            raise ValueError("modo debe ser «grabar» o «reproducir»")
        if modo == "grabar" and base is None:
            raise ValueError("ReplayClient en modo grabar necesita un cliente base")
        self.ruta = Path(ruta)
        self.modo = modo
        self.base = base
        self._lock = threading.Lock()
        self._tabla: Dict[str, Dict] = {}
        if self.ruta.exists():
            for l in self.ruta.read_text(encoding="utf-8").splitlines():
                if l.strip():
                    d = json.loads(l)
                    self._tabla[d["clave"]] = d
        elif modo == "reproducir":
            raise FileNotFoundError(f"No existe la grabación {self.ruta}")

    def identidad_cache(self):
        return [super().identidad_cache(), str(self.ruta.resolve()), self.modo,
                self.base.identidad_cache() if self.base else None]

    @staticmethod
    def clave(agente: str, modelo: str, system: List[Dict], mensajes: List[Dict], herramientas) -> str:
        h = hashlib.sha256()
        h.update(json.dumps([agente, modelo, [b.get("text") for b in system], mensajes, herramientas],
                            ensure_ascii=False, sort_keys=True, default=str).encode())
        return h.hexdigest()

    def generar(self, *, agente: str, modelo: str, system: List[Dict], mensajes: List[Dict], max_tokens: int,
                herramientas: Optional[List[Dict]] = None, esquema: Optional[Dict] = None) -> RespuestaLLM:
        antigua = self.clave(agente, modelo, system, mensajes, herramientas)
        k = hashlib.sha256(json.dumps([antigua, system, max_tokens, esquema], ensure_ascii=False,
                                      sort_keys=True).encode()).hexdigest()
        if self.modo == "reproducir":
            d = self._tabla.get(k) or self._tabla.get(antigua)
            if d is None:
                raise ReplayFaltante(f"Respuesta no grabada para {agente} (clave {k[:12]}…)")
            stop = d.get("stop_reason")
            return respuesta_segura(RespuestaLLM(d["texto"], Uso(**d["uso"]), d["modelo"], stop,
                                                 d.get("truncada", stop == "max_tokens"),
                                                 d.get("rechazo", stop == "refusal")))
        assert self.base is not None  # validado al abrir en modo grabar
        r = self.base.generar(agente=agente, modelo=modelo, system=system, mensajes=mensajes, max_tokens=max_tokens,
                              herramientas=herramientas, esquema=esquema)
        r = respuesta_segura(r)
        d = {"truncada": r.truncada, "rechazo": r.rechazo, "clave": k, "agente": agente, "modelo": modelo, "texto": r.texto, "uso": asdict(r.uso), "stop_reason": r.stop_reason}
        with self._lock:
            self._tabla[k] = d
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ruta, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(d, ensure_ascii=False) + "\n")
        return r


def crear_cliente(tipo: str, cfg: Dict, replay: Optional[str] = None, replay_modo: str = "reproducir") -> LLMClient:
    llm = cfg.get("llm") or {}
    if tipo == "mock":
        return MockClient(parametro(cfg, "llm.semilla_mock"))
    if tipo == "anthropic":
        return AnthropicClient(max_reintentos=parametro(cfg, "llm.max_reintentos_api"), timeout_s=parametro(cfg, "llm.timeout_s"),
                               salida_estructurada=llm.get("salida_estructurada", False),
                               max_continuaciones=parametro(cfg, "llm.max_continuaciones_pause_turn"))
    if tipo == "replay":
        if not replay:
            raise ValueError("--replay RUTA es obligatorio con --cliente replay")
        base = None
        if replay_modo == "grabar":
            base = crear_cliente(os.environ.get("BLOQUE_A_CLIENTE_BASE", "anthropic"), cfg)
        return ReplayClient(replay, replay_modo, base)
    raise ValueError(f"Cliente desconocido {tipo}")
