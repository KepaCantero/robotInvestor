"""Clientes de modelo de lenguaje.

- `AnthropicClient`: cliente real (SDK `anthropic` 2.x, `messages.create`). El system prompt se envía
  como lista de bloques de texto con `cache_control` (caché de prompts); la herramienta de servidor de
  búsqueda web (`web_search_20260318`) solo se añade cuando el orquestador lo permite (nunca en
  backtest); gestiona `pause_turn` (continuación) y registra tokens de entrada, salida, escritura y
  lectura de caché y búsquedas web. T-151: el SDK no reintenta; reintenta el cliente (`ReglaReintentos`), y cada
  reintento reserva su petición en el presupuesto como las demás.
- `MockClient`: respuestas sintéticas deterministas (semilla) generadas a partir del encargo
  (`bloque_a.mock_respuestas`), válidas frente a los esquemas y sensibles a la entrada.
- `ReplayClient`: graba las respuestas de otro cliente en JSONL y las reproduce exactamente
  (reproducibilidad de backtests con el modelo real).
"""
from __future__ import annotations

import contextlib
import contextvars
import hashlib
import json
import math
import os
import threading
import time
from collections.abc import Callable, Iterator
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .configuracion import parametro
from .contratos import secretos_en_texto


@dataclass
class Uso:
    entrada: int = 0            # tokens de entrada no cacheados
    salida: int = 0
    cache_escritura: int = 0
    cache_lectura: int = 0
    busquedas_web: int = 0

    def sumar(self, otro: Uso) -> None:
        for k in asdict(self):
            setattr(self, k, getattr(self, k) + getattr(otro, k))


@dataclass
class RespuestaLLM:
    texto: str
    uso: Uso
    modelo: str
    stop_reason: str | None = None
    truncada: bool = False
    rechazo: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


def contenido_sensible(valor) -> bool:
    """Aplica R8 tanto al JSON estructurado como a texto libre o JSON incompleto."""
    if isinstance(valor, (bytes, bytearray)):
        valor = bytes(valor).decode("utf-8", errors="replace")
    if isinstance(valor, str):
        # Un valor sensible truncado antes de la comilla final también se descarta.
        return bool(secretos_en_texto(valor + '"'))
    if not isinstance(valor, (dict, list, tuple, set, frozenset)):   # T-93 (H-32): también los conjuntos
        return False
    # T-113 (H-56 de T-104): antes, cada nivel volvía a serializar todo lo que tenía debajo (profundidad × tamaño). Ahora cada
    # diccionario que no cuelga de otro se serializa una sola vez (uno anidado aparece igual dentro) y las hojas de texto se
    # recorren sin recursión, cada una con la comilla final de un valor truncado. r02 (QA r01, H-01): también los
    # diccionarios que cuelgan de una lista, una tupla o un conjunto (antes de la r02 solo se serializaba el de arriba)
    sin_serializar: TypeError | None = None
    try:
        for d in _diccionarios_de_arriba(valor):
            try:
                if secretos_en_texto(json.dumps(d, ensure_ascii=False, default=str)):
                    return True
            except TypeError as exc:   # claves que no son texto: sigue siendo un error del llamador (si el diccionario
                if d is valor:         # cuelga de una lista, después de mirar el resto: un secreto hallado pesa más)
                    raise
                sin_serializar = sin_serializar or exc
    except ValueError:   # r02 (H-01): una estructura que se contiene a sí misma no se puede comprobar: falla cerrado
        return True
    except RecursionError:   # demasiado anidado para serializarlo: no se puede comprobar, así que falla cerrado
        return True
    vistos: set[int] = set()
    pila: list = [valor]
    hay_conjuntos = False
    while pila:
        x = pila.pop()
        if isinstance(x, (dict, list, tuple, set, frozenset)):   # r02 (H-01): cada contenedor, una vez (termina siempre)
            if id(x) in vistos:
                continue
            vistos.add(id(x))
            hay_conjuntos = hay_conjuntos or isinstance(x, (set, frozenset))
        if isinstance(x, (bytes, bytearray)):
            x = bytes(x).decode("utf-8", errors="replace")
        if isinstance(x, str):
            if secretos_en_texto(x + '"'):
                return True
        elif isinstance(x, dict):
            pila.extend(x.values())
        elif isinstance(x, (list, tuple, set, frozenset)):
            pila.extend(x)
    if hay_conjuntos:
        # T-122 (QA r02 de T-113, H-10): con `default=str` un conjunto sale como su representación de Python, y un diccionario
        # dentro de él no casa con los patrones de R8. Se vuelve a mirar con los conjuntos como listas. Solo si hay conjuntos,
        # y además de la primera pasada (que conserva lo que ya se detectaba: un «"api_key": <conjunto>»)
        try:
            for d in _diccionarios_de_arriba(valor):
                try:
                    if secretos_en_texto(json.dumps(d, ensure_ascii=False, default=_json_por_defecto)):
                        return True
                except TypeError as exc:   # claves que no son texto dentro del conjunto: error del llamador, como antes de T-113
                    sin_serializar = sin_serializar or exc
        except (ValueError, RecursionError):
            return True
    if sin_serializar is not None:
        raise sin_serializar
    return False


def _json_por_defecto(o):
    """T-122 (QA r02 de T-113, H-10): un conjunto se vuelca como lista, para que un diccionario dentro de él salga con sus
    pares «"clave": "valor"» y no con la representación de Python, que no casa con los patrones de R8."""
    if isinstance(o, (set, frozenset)):
        return list(o)
    return str(o)


def _diccionarios_de_arriba(valor) -> list[dict]:
    """T-113 r02 (H-01): los diccionarios que no cuelgan de otro diccionario, bajando por listas, tuplas y conjuntos sin
    recursión; cada uno, una vez. Una lista o tupla que se contiene a sí misma es `ValueError` (como el ciclo de un
    diccionario en `json.dumps`); la misma lista en dos sitios no es un ciclo."""
    hallados: list[dict] = []
    vistos: set[int] = set()
    camino: set[int] = set()
    pila: list = [(valor, False)]
    while pila:
        x, salida = pila.pop()
        if salida:
            camino.discard(id(x))
        elif id(x) in camino:
            raise ValueError("estructura cíclica")
        elif id(x) in vistos:
            continue
        elif isinstance(x, dict):
            vistos.add(id(x))
            hallados.append(x)
        elif isinstance(x, (list, tuple, set, frozenset)):
            vistos.add(id(x))
            camino.add(id(x))
            pila.append((x, True))
            pila.extend((v, False) for v in x)
    return hallados


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

    def generar(self, *, agente: str, modelo: str, system: list[dict], mensajes: list[dict], max_tokens: int,
                herramientas: list[dict] | None = None, esquema: dict | None = None) -> RespuestaLLM:
        raise NotImplementedError


# T-146: la reserva de presupuesto de la llamada en curso (`consumo.ReservaLlamada`). La fija `Agentes.invocar` alrededor de
# cada `generar`; el cliente real la usa para reservar cada continuación tras `pause_turn` y pagar cada petición. Cada hilo
# tiene la suya (las variables de contexto no pasan de un hilo a otro).
_GUARDA: contextvars.ContextVar[Any] = contextvars.ContextVar("guarda_presupuesto", default=None)


@contextlib.contextmanager
def con_guarda(guarda: Any) -> Iterator[None]:
    marca = _GUARDA.set(guarda)
    try:
        yield
    finally:
        _GUARDA.reset(marca)


def herramienta_busqueda_web(tipo: str = "web_search_20260318", max_usos: int = 5) -> dict:
    """Definición de la herramienta de servidor de búsqueda web (tipos en anthropic.types.WebSearchTool*Param)."""
    return {"type": tipo, "name": "web_search", "max_uses": int(max_usos)}


# Límites del protocolo HTTP (RFC 9110, §15), no parámetros de ajuste: el menor estado y el primero de la clase 5xx (T-156)
ESTADO_HTTP_MIN, PRIMER_ESTADO_5XX = 100, 500


@dataclass(frozen=True)
class ReglaReintentos:
    """T-151 (QA r01 de T-146, H-09): los reintentos ante un fallo del proveedor, en el cliente y no en el SDK, para que cada
    reintento pase por la reserva del presupuesto (`consumo.ReservaLlamada`). Los números salen de la configuración
    (`llm.max_reintentos_api` y `llm.reintentos.*`, `[PROPUESTO]`, INC-T146-01): los estados que se reintentan, los que el
    servidor rechaza sin ejecutar la petición (no se cobran) y la espera, determinista (la inicial, doblando hasta la
    máxima; o la que pida el servidor con `retry-after`).
    T-154 (QA r01 de T-151, H-01 y H-04): desde `cobro_posible` (la clase 5xx) una petición pudo cobrarse aunque no se
    reintente, salvo las de `sin_cobro`; y no se espera a un `retry-after` mayor que `espera_servidor_max_s` (no se
    reintenta)."""
    maximo: int
    espera_inicial_s: float
    espera_max_s: float
    estados: frozenset[int]
    sin_cobro: frozenset[int]
    espera_servidor_max_s: float
    cobro_posible: int

    @classmethod
    def de_config(cls, cfg: dict) -> ReglaReintentos:
        maximo = parametro(cfg, "llm.max_reintentos_api")
        inicial, tope = parametro(cfg, "llm.reintentos.espera_inicial_s"), parametro(cfg, "llm.reintentos.espera_max_s")
        estados, sin_cobro = parametro(cfg, "llm.reintentos.estados_reintentables"), parametro(cfg, "llm.reintentos.estados_sin_cobro")
        servidor, desde = parametro(cfg, "llm.reintentos.espera_servidor_max_s"), parametro(cfg, "llm.reintentos.cobro_posible_desde")
        if isinstance(maximo, bool) or not isinstance(maximo, int) or maximo < 0:
            raise ValueError("llm.max_reintentos_api debe ser un entero no negativo")
        for nombre, v in (("espera_inicial_s", inicial), ("espera_max_s", tope), ("espera_servidor_max_s", servidor)):
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0:
                raise ValueError(f"llm.reintentos.{nombre} debe ser un número no negativo")
        if inicial > tope:
            raise ValueError("llm.reintentos.espera_inicial_s no puede pasar de espera_max_s")
        for nombre, v in (("estados_reintentables", estados), ("estados_sin_cobro", sin_cobro)):
            if not isinstance(v, list) or any(isinstance(x, bool) or not isinstance(x, int) for x in v):
                raise ValueError(f"llm.reintentos.{nombre} debe ser una lista de estados HTTP enteros")
        if not set(sin_cobro) <= set(estados):
            raise ValueError("llm.reintentos.estados_sin_cobro debe estar dentro de estados_reintentables")
        # T-156 (QA r01 de T-154, H-01): un estado HTTP (RFC 9110, §15: de 100 a 599) y como mucho el primero de la clase
        # 5xx. Con uno mayor, un 5xx por debajo que no se reintenta se soltaría como no cobrado (fallaría abierto); con uno
        # menor se cuentan como cobrados también estados anteriores, que es más prudente.
        if isinstance(desde, bool) or not isinstance(desde, int) or not ESTADO_HTTP_MIN <= desde <= PRIMER_ESTADO_5XX:
            raise ValueError(f"llm.reintentos.cobro_posible_desde debe ser un estado HTTP entero entre {ESTADO_HTTP_MIN} y "
                             f"{PRIMER_ESTADO_5XX} (con uno mayor, un 5xx que no se reintenta se soltaría como no cobrado)")
        return cls(maximo, float(inicial), float(tope), frozenset(estados), frozenset(sin_cobro), float(servidor), desde)

    def espera(self, reintento: int, error: BaseException) -> float | None:
        """Segundos antes del reintento número `reintento` (1, 2…): los que pida el servidor (`retry-after-ms` o
        `retry-after` en segundos, como el SDK) o la espera inicial doblada en cada reintento, sin pasar de la máxima.
        T-154 (H-04): un `retry-after` que no es un número finito y positivo no vale (la espera de la regla); uno mayor que
        `espera_servidor_max_s` da None: no se reintenta (no se inventa una espera más corta que la que pide el servidor)."""
        cabeceras = _cabeceras(error)
        for clave, escala in (("retry-after-ms", 1000.0), ("retry-after", 1.0)):
            crudo = cabeceras.get(clave)
            try:
                v = float(str(crudo)) / escala
            except ValueError:   # ausente («None») o una fecha: no se interpreta
                continue
            if math.isfinite(v) and v > 0:
                return v if v <= self.espera_servidor_max_s else None
        return min(self.espera_inicial_s * 2 ** (reintento - 1), self.espera_max_s)


def _cabeceras(error: BaseException) -> dict[str, Any]:
    """T-154 (QA r01 de T-151, H-04): las cabeceras de la respuesta de un error con el nombre en minúsculas (HTTP no distingue
    mayúsculas en los nombres; las de httpx ya no lo hacen, un diccionario sí)."""
    crudas = getattr(getattr(error, "response", None), "headers", None) or {}
    try:
        return {str(k).lower(): v for k, v in crudas.items()}
    except AttributeError:   # no es un diccionario de cabeceras
        return {}


def clasificar_error(error: BaseException, regla: ReglaReintentos | None) -> tuple[bool, bool]:
    """T-151: (se reintenta, la API pudo cobrarla). Conexión y timeout: la petición pudo llegar y completarse (se reintenta
    y pudo cobrarse). Un estado HTTP: se reintenta si está en `regla.estados` (o si el servidor lo pide con
    `x-should-retry`, como el SDK, sin distinguir mayúsculas) y no se cobró si está en `regla.sin_cobro` o no se reintenta
    (el servidor la rechazó). T-154 (QA r01 de T-151, H-01): un estado de la clase 5xx (desde `regla.cobro_posible`) pudo
    cobrarse aunque no se reintente (501, 520, un 500 con `x-should-retry: false`), salvo los de `regla.sin_cobro`.
    Otro error (no del proveedor): ni se reintenta ni se cobró. Sin regla (un cliente creado sin la configuración) no se
    reintenta nada, y un error del proveedor cuenta como cobrado (prudente: no se sabe qué estados rechaza sin ejecutar)."""
    try:
        import anthropic
    except ImportError:   # pragma: no cover - sin el SDK no hay errores suyos
        return False, False
    if isinstance(error, anthropic.APIConnectionError):   # también APITimeoutError
        return regla is not None, True
    if isinstance(error, anthropic.APIStatusError):
        if regla is None:
            return False, True
        pide = str(_cabeceras(error).get("x-should-retry", "")).lower().strip()
        reintenta = pide == "true" or (pide != "false" and error.status_code in regla.estados)
        if error.status_code >= regla.cobro_posible:   # T-154 (H-01): el servidor pudo ejecutarla, se reintente o no
            return reintenta, error.status_code not in regla.sin_cobro
        return reintenta, reintenta and error.status_code not in regla.sin_cobro
    return False, False


class AnthropicClient(LLMClient):
    nombre = "anthropic"

    def __init__(self, api_key: str | None = None, timeout_s: float = 600, salida_estructurada: bool = False,
                 max_continuaciones: int = 3, sdk: Any = None, reintentos: ReglaReintentos | None = None,
                 dormir: Callable[[float], None] | None = None) -> None:
        """T-151 (QA r01 de T-146, H-09): el SDK no reintenta (`max_retries=0`; uno recibido con `with_options` se pone
        también a 0): reintenta este cliente con `reintentos` (sin regla, ninguno) y cada reintento reserva su petición."""
        if sdk is None:
            import anthropic
            clave = api_key or os.environ.get("ANTHROPIC_API_KEY")
            if not clave:
                raise RuntimeError("Falta ANTHROPIC_API_KEY (variable de entorno). El bloque nunca la guarda en archivos (R8).")
            sdk = anthropic.Anthropic(api_key=clave, max_retries=0, timeout=timeout_s)
        elif callable(getattr(sdk, "with_options", None)):
            sdk = sdk.with_options(max_retries=0)
        self.sdk = sdk
        self.salida_estructurada = salida_estructurada
        self.max_continuaciones = max_continuaciones
        self.reintentos = reintentos
        self.dormir = dormir or time.sleep

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

    def generar(self, *, agente: str, modelo: str, system: list[dict], mensajes: list[dict], max_tokens: int,
                herramientas: list[dict] | None = None, esquema: dict | None = None) -> RespuestaLLM:
        if contenido_sensible([system, mensajes]):
            return RespuestaLLM("", Uso(), modelo, stop_reason="contenido_sensible")
        msgs = list(mensajes)
        kwargs: dict[str, Any] = {"model": modelo, "max_tokens": int(max_tokens), "system": system, "messages": msgs,
                                  "metadata": {"user_id": f"bloque-a-{agente}"}}
        if herramientas:
            kwargs["tools"] = herramientas
        if esquema is not None and self.salida_estructurada:
            kwargs["output_config"] = {"format": {"type": "json_schema", "schema": esquema}}
        uso = Uso()
        textos: list[str] = []
        stop = None
        guarda = _GUARDA.get()
        for vuelta in range(self.max_continuaciones + 1):
            if guarda is not None and vuelta > 0:
                # T-146: cada continuación es una petición más y reserva su peor caso antes de salir (la primera la reservó
                # `Agentes.invocar`, que pasa aquí su `max_tokens`)
                mt = guarda.reservar(system, msgs, herramientas, int(kwargs["max_tokens"]))
                if mt is None:
                    return RespuestaLLM("".join(textos), uso, modelo, stop_reason="presupuesto_agotado")
                kwargs["max_tokens"] = int(mt)
            resp, fallo = self._crear(kwargs, guarda, system, msgs, herramientas)
            if fallo == "presupuesto_agotado":
                return RespuestaLLM("".join(textos), uso, modelo, stop_reason="presupuesto_agotado")
            if fallo is not None:   # agotados los reintentos (los mensajes de excepción pueden contener secretos: no se guardan)
                return RespuestaLLM("", uso, modelo, stop_reason="error_proveedor")
            u = self._uso(getattr(resp, "usage", None))
            uso.sumar(u)
            if guarda is not None:
                guarda.pagar(u)
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

    def _crear(self, kwargs: dict, guarda: Any, system: list[dict], msgs: list[dict],
               herramientas: list[dict] | None) -> tuple[Any, str | None]:
        """Una petición con sus reintentos (T-151, H-09). Cada intento fallido se declara a la guarda (`fallida`: suelta su
        reserva si no se cobró, o la deja para cargarla si pudo cobrarse) y cada reintento reserva la suya antes de salir.
        Devuelve (respuesta, None), (None, "presupuesto_agotado") o (None, "error_proveedor")."""
        reintento = 0
        while True:
            try:
                return self.sdk.messages.create(**kwargs), None
            except Exception as e:
                reintenta, cobro = clasificar_error(e, self.reintentos)
                if guarda is not None:
                    guarda.fallida(cobro, type(e).__name__)
                if not reintenta or self.reintentos is None or reintento >= self.reintentos.maximo:
                    return None, "error_proveedor"
                reintento += 1
                espera = self.reintentos.espera(reintento, e)
                if espera is None:   # T-154 (H-04): el servidor pide esperar más de lo admitido: no se reintenta
                    return None, "error_proveedor"
                self.dormir(espera)
            if guarda is not None:
                mt = guarda.reservar(system, msgs, herramientas, int(kwargs["max_tokens"]))
                if mt is None:
                    return None, "presupuesto_agotado"
                kwargs["max_tokens"] = int(mt)


def _tokens_aprox(texto: str) -> int:
    return max(1, int(len(texto) / 3.6))


class MockClient(LLMClient):
    """Cliente simulado determinista. Los tokens se estiman (≈ 3,6 caracteres por token) y la caché de
    prompts se simula por prefijo, como la API (T-101): cada punto `cache_control` guarda el prefijo hasta él; una llamada lee
    el prefijo guardado más largo y escribe el resto; lo que queda después del último punto, o sin puntos, es entrada."""

    nombre = "mock"
    conocimiento_previo = False   # el simulado no sabe nada del periodo: no hay fuga por memoria (PA-09)

    def __init__(self, semilla: int = 20261102, fallos: dict[str, int] | None = None) -> None:
        self.semilla = int(semilla)
        self._vistos: set = set()
        self._lock = threading.Lock()
        self.llamadas: list[dict] = []
        self.fallos = dict(fallos or {})   # agente -> nº de respuestas inválidas a devolver (pruebas)

    def identidad_cache(self):
        return [super().identidad_cache(), self.semilla]

    def generar(self, *, agente: str, modelo: str, system: list[dict], mensajes: list[dict], max_tokens: int,
                herramientas: list[dict] | None = None, esquema: dict | None = None) -> RespuestaLLM:
        from . import mock_respuestas
        sys_txt = "".join(b.get("text", "") for b in system)
        user_txt = "".join(m["content"] if isinstance(m["content"], str) else json.dumps(m["content"], default=str)
                           for m in mensajes if m["role"] == "user")
        # Caché por prefijo, como la API (T-101, idea 2): cada punto de caché guarda el prefijo hasta él (modelo,
        # herramientas y bloques de system). Se lee el prefijo guardado más largo y se escribe el resto hasta el último punto.
        puntos, acumulado = [], ""
        for b in system:
            acumulado += b.get("text", "")
            if b.get("cache_control"):
                puntos.append((hashlib.sha256((modelo + json.dumps(herramientas, default=str) + acumulado).encode()).hexdigest(),
                               _tokens_aprox(acumulado)))
        with self._lock:
            leido = max((t for k, t in puntos if k in self._vistos), default=0)
            hasta = puntos[-1][1] if puntos else 0
            self._vistos.update(k for k, _ in puntos)
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
        uso = Uso(entrada=_tokens_aprox(user_txt) + max(t_sys - hasta, 0), salida=_tokens_aprox(datos_txt),
                  cache_escritura=max(hasta - leido, 0), cache_lectura=leido,
                  busquedas_web=1 if herramientas else 0)
        return RespuestaLLM(texto=datos_txt, uso=uso, modelo=modelo, stop_reason="end_turn")


class ReplayFaltante(KeyError):
    pass


class ReplayClient(LLMClient):
    """Graba (modo «grabar», envolviendo otro cliente) o reproduce (modo «reproducir») respuestas."""

    nombre = "replay"

    def __init__(self, ruta, modo: str = "reproducir", base: LLMClient | None = None) -> None:
        if modo not in ("grabar", "reproducir"):
            raise ValueError("modo debe ser «grabar» o «reproducir»")
        if modo == "grabar" and base is None:
            raise ValueError("ReplayClient en modo grabar necesita un cliente base")
        self.ruta = Path(ruta)
        self.modo = modo
        self.base = base
        self._lock = threading.Lock()
        self._tabla: dict[str, dict] = {}
        self.descartadas = 0
        if self.ruta.exists():
            # T-113 (H-54 de T-104): una última línea cortada se descarta; otra ilegible da el fichero y la línea
            from .herramientas.ht06_indice import acabar_en_salto, leer_jsonl
            filas, self.descartadas = leer_jsonl(self.ruta)
            for d in filas:
                if not isinstance(d, dict) or not isinstance(d.get("clave"), str):   # r02 (H-06): la clave es un texto
                    raise ValueError(f"{self.ruta}: registro de la grabación sin «clave»")   # noqa: TRY004 — dato, no tipo
                self._tabla[d["clave"]] = d
            if modo == "grabar":   # r02 (QA r01, H-02): para seguir escribiendo; al reproducir no se toca
                acabar_en_salto(self.ruta)
        elif modo == "reproducir":
            raise FileNotFoundError(f"No existe la grabación {self.ruta}")

    def identidad_cache(self):
        return [super().identidad_cache(), str(self.ruta.resolve()), self.modo,
                self.base.identidad_cache() if self.base else None]

    @staticmethod
    def clave(agente: str, modelo: str, system: list[dict], mensajes: list[dict], herramientas) -> str:
        h = hashlib.sha256()
        h.update(json.dumps([agente, modelo, [b.get("text") for b in system], mensajes, herramientas],
                            ensure_ascii=False, sort_keys=True, default=str).encode())
        return h.hexdigest()

    def generar(self, *, agente: str, modelo: str, system: list[dict], mensajes: list[dict], max_tokens: int,
                herramientas: list[dict] | None = None, esquema: dict | None = None) -> RespuestaLLM:
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


def crear_cliente(tipo: str, cfg: dict, replay: str | None = None, replay_modo: str = "reproducir") -> LLMClient:
    llm = cfg.get("llm") or {}
    if tipo == "mock":
        return MockClient(parametro(cfg, "llm.semilla_mock"))
    if tipo == "anthropic":
        return AnthropicClient(timeout_s=parametro(cfg, "llm.timeout_s"), salida_estructurada=llm.get("salida_estructurada", False),
                               max_continuaciones=parametro(cfg, "llm.max_continuaciones_pause_turn"),
                               reintentos=ReglaReintentos.de_config(cfg))
    if tipo == "replay":
        if not replay:
            raise ValueError("--replay RUTA es obligatorio con --cliente replay")
        base = None
        if replay_modo == "grabar":
            base = crear_cliente(os.environ.get("BLOQUE_A_CLIENTE_BASE", "anthropic"), cfg)
        return ReplayClient(replay, replay_modo, base)
    raise ValueError(f"Cliente desconocido {tipo}")
