"""Reloj del sistema (T-03, quinta parte; V0.47). Determinista con fuentes inyectadas, sin red.

Todo el marco recibe el instante como argumento (`ahora`). En marcha tiene que salir del reloj de la máquina, y casi todo depende
de él: frescura, ventanas, caducidades, enfriamientos, pérdidas del día y de la semana, órdenes por hora, fechas de revisión. Este
módulo da ese instante y falla cerrado ante un reloj dudoso:

- `Reloj(pared, monotono)` lee el reloj de pared (segundos desde 1970, UTC; por defecto `time.time`) y uno monótono que no salta
  cuando alguien cambia la hora y sí avanza durante una suspensión de la máquina (por defecto CLOCK_BOOTTIME en Linux;
  `time.monotonic` donde no existe). El de pared debe avanzar lo mismo que el monótono: entre dos lecturas seguidas, con una
  tolerancia (`max_salto_s`), y desde el ancla (la primera lectura o el último rearme), con esa tolerancia más una deriva máxima
  (TASA_MAX, el ajuste lento de la sincronización). Así no se cuelan ni un reloj congelado o acelerado ni muchos saltos pequeños.
- Antes del primer instante, y de nuevo tras un rearme o pasado `max_sin_contraste_s`, el reloj se contrasta con una referencia
  externa (`contrastar`, por ejemplo la hora del intermediario): una máquina que arranca con una fecha equivocada no llega a dar
  instantes ni a escribirlos en el estado.
- `ahora()` da el instante en el formato del marco (ISO 8601, UTC, con microsegundos) y nunca uno anterior a otro ya dado ni al
  último instante del estado (un retroceso pequeño, dentro de la tolerancia, repite el último).
- `comprobar_estado(o)` al arrancar: el reloj no puede ir detrás del último instante que vio el Orquestador cargado; ese instante
  pasa a ser el suelo de los que se den.
- `contrastar(referencia, fuente)` devuelve como instante el mayor entre el reloj y la referencia (si están dentro de la
  tolerancia): así los datos del intermediario nunca son «del futuro» para el Orquestador.
- Ante un incidente el reloj se bloquea: no da más instantes hasta que el operador lo rearma (`rearmar`) y se vuelve a contrastar.
  `degradar_por_reloj(o, r)` baja todas las carteras a L1 con el último instante que vio el Orquestador (el único de fiar).

Códigos (nada lanza; el constructor, ValueError con parámetros imposibles):
  RL-01 salto o deriva del reloj de pared respecto al monótono, el monótono retrocede o el reloj va detrás de lo ya dado: se bloquea.
  RL-02 el reloj va detrás del último instante del estado: se bloquea.
  RL-03 desfase con una referencia externa mayor que `max_desfase_s`: se bloquea.
  RL-04 el reloj está bloqueado (hay que rearmarlo) o aún no se ha contrastado (hay que contrastarlo).
  RL-05 lectura imposible: la fuente falla, no da un número finito o da un instante fuera de lo plausible
        (antes de MINIMO o desde MAXIMO, como una máquina que arranca en 1970): se bloquea.
  RL-06 referencia externa ilegible o fuera de lo plausible, rearme mal pedido o algo que no es un incidente: no cambia nada.
  RL-07 no se pudieron degradar las carteras tras un incidente: quien llama no debe seguir operando.

Límites: no sincroniza el reloj (eso es del sistema operativo) ni sabe si la referencia externa es de fiar; un salto menor que la
tolerancia no se ve; el bloqueo vive en memoria (un reinicio lo quita, pero vuelve a exigir contrastar y `comprobar_estado`); una
cartera que ya estaba degradada no recibe un aviso nuevo por el reloj (el reloj sigue bloqueado hasta que el operador lo rearme).
"""
from __future__ import annotations

import math
import time
from datetime import datetime, timezone

from orquestador import _dt, _motivo_ok

MAX_SALTO_S = 2.0       # [PROPUESTO] diferencia tolerada entre lo que avanzan el reloj de pared y el monótono
MAX_DESFASE_S = 5.0     # [PROPUESTO] diferencia tolerada con una referencia externa (latencia del intermediario incluida)
MAX_SIN_CONTRASTE_S = 24 * 3600.0   # [PROPUESTO] pasado este tiempo sin contrastar, el reloj pide otro contraste
TASA_MAX = 0.0005       # deriva máxima del reloj de pared desde el ancla (500 ppm: lo que corrige la sincronización)
TOPE_SALTO_S, TOPE_DESFASE_S = 60.0, 300.0   # tolerancias mayores desactivarían las comprobaciones
MINIMO = datetime(2026, 1, 1, tzinfo=timezone.utc)   # un instante anterior no es de esta instalación: reloj sin poner en hora
MAXIMO = datetime(2100, 1, 1, tzinfo=timezone.utc)
CARTERAS = ("TRADING", "TACTICA", "LARGO_PLAZO")


def _r(ok, codigo, motivo, **extra):
    return {"ok": ok, "codigo": codigo, "motivo": motivo, **extra}


def _float(x):
    """El número como float finito, o None (también para bool, textos, desbordes y tipos que no se dejan convertir)."""
    if isinstance(x, bool) or not isinstance(x, (int, float)) and type(x).__name__ not in ("float64", "float32"):
        return None
    try:
        v = float(x)
    except (OverflowError, TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def _instante(segundos):
    return datetime.fromtimestamp(segundos, timezone.utc)


def _monotono_por_defecto():
    if hasattr(time, "CLOCK_BOOTTIME"):   # Linux: sigue contando durante una suspensión (revisión de V0.47, hallazgo 7)
        return lambda: time.clock_gettime(time.CLOCK_BOOTTIME)
    return time.monotonic


class Reloj:
    def __init__(self, pared=None, monotono=None, max_salto_s=MAX_SALTO_S, max_desfase_s=MAX_DESFASE_S,
                 max_sin_contraste_s=MAX_SIN_CONTRASTE_S):
        s, d, c = _float(max_salto_s), _float(max_desfase_s), _float(max_sin_contraste_s)
        if not (s and 0 < s <= TOPE_SALTO_S and d and 0 < d <= TOPE_DESFASE_S and c and c > 0):
            raise ValueError(f"tolerancias del reloj imposibles: salto en (0, {TOPE_SALTO_S}], desfase en (0, {TOPE_DESFASE_S}], contraste > 0")
        if (pared is not None and not callable(pared)) or (monotono is not None and not callable(monotono)):
            raise ValueError("las fuentes del reloj deben ser invocables")
        self._pared = pared if pared is not None else time.time
        self._monotono = monotono if monotono is not None else _monotono_por_defecto()
        self.max_salto_s, self.max_desfase_s, self.max_sin_contraste_s = s, d, c
        self._ancla = None         # (pared, monótono) de la primera lectura o del último rearme
        self._ultima = None        # (pared, monótono) de la última lectura buena
        self._suelo = None         # segundos: nunca se da un instante anterior (lo ya dado y el último del estado)
        self._contraste = None     # monótono del último contraste bueno
        self.bloqueo = None        # {"codigo", "motivo"} mientras esté bloqueado
        self.incidentes = []       # [{"codigo", "motivo", "suelo"}] y rearmes [{"codigo": "REARME", "actor", ...}]

    # ------------------------------------------------------------------------------------------------ incidentes
    def _bloquear(self, codigo, motivo, **extra):
        self.bloqueo = {"codigo": codigo, "motivo": motivo}
        self.incidentes.append({"codigo": codigo, "motivo": motivo, "suelo": self._iso_suelo()})
        return _r(False, codigo, motivo, ahora=None, **extra)

    def _iso_suelo(self):
        return _instante(self._suelo).isoformat() if self._suelo is not None else None

    def _leer(self):
        """Lee y comprueba las dos fuentes sin dar el instante: (pared, monótono) o (None, error). Nunca lanza."""
        if self.bloqueo is not None:
            return None, _r(False, "RL-04", f"el reloj está bloqueado ({self.bloqueo['codigo']}: {self.bloqueo['motivo']}): hay que rearmarlo",
                            ahora=None)
        try:
            p, m = _float(self._pared()), _float(self._monotono())
            if p is None or m is None:
                return None, self._bloquear("RL-05", "el reloj no da un número finito")
            t = _instante(p)
        except Exception as ex:   # noqa: BLE001 — una fuente rota es un reloj del que no se puede fiar
            return None, self._bloquear("RL-05", f"no se pudo leer el reloj: {type(ex).__name__}")
        if not MINIMO <= t < MAXIMO:
            return None, self._bloquear("RL-05", f"el reloj da {t.isoformat()}, fuera de lo plausible: no está en hora")
        if self._ultima is not None:
            p0, m0 = self._ultima
            if m < m0:
                return None, self._bloquear("RL-01", "el reloj monótono retrocede: la fuente no es de fiar")
            salto = (p - p0) - (m - m0)
            if abs(salto) > self.max_salto_s:
                return None, self._bloquear("RL-01", f"el reloj de pared saltó {salto:+.1f} s respecto al monótono: alguien cambió la "
                                                     "hora o la sincronización dio un salto")
        if self._ancla is not None:   # hallazgo 1: un reloj congelado, acelerado o con muchos saltos pequeños
            pa, ma = self._ancla
            deriva = (p - pa) - (m - ma)
            if abs(deriva) > self.max_salto_s + TASA_MAX * max(0.0, m - ma):
                return None, self._bloquear("RL-01", f"el reloj de pared se ha separado {deriva:+.1f} s del monótono desde "
                                                     f"{_instante(pa).isoformat()}: va congelado, acelerado o a saltos")
        # el suelo puede ir por delante del reloj hasta max_desfase_s (lo sube un contraste con una referencia adelantada)
        if self._suelo is not None and p < self._suelo - self.max_salto_s - self.max_desfase_s:
            return None, self._bloquear("RL-01", f"el reloj ({t.isoformat()}) va por detrás de un instante ya dado ({self._iso_suelo()})")
        if self._ancla is None:
            self._ancla = (p, m)
        self._ultima = (p, m)
        return (p, m), None

    def _dar(self, segundos):
        """Da el instante (nunca por debajo del suelo) y sube el suelo."""
        s = segundos if self._suelo is None else max(segundos, self._suelo)
        self._suelo = s
        return _instante(s).isoformat()

    # ------------------------------------------------------------------------------------------------ lectura
    def ahora(self) -> dict:
        """{ok, codigo, motivo, ahora}: el instante actual (ISO 8601, UTC), nunca anterior a uno ya dado ni al del estado."""
        lect, err = self._leer()
        if err:
            return err
        p, m = lect
        if self._contraste is None or m - self._contraste > self.max_sin_contraste_s:
            return _r(False, "RL-04", "el reloj no se ha contrastado (o hace demasiado): contrástalo con una referencia externa", ahora=None)
        return _r(True, "OK", "instante", ahora=self._dar(p))

    def comprobar_estado(self, o) -> dict:
        """Al arrancar con un estado cargado: el reloj no puede ir detrás del último instante que vio el Orquestador (RL-02), que
        pasa a ser el suelo. No da ningún instante. {ok, codigo, motivo, ahora: None}."""
        lect, err = self._leer()
        if err:
            return err
        try:
            ultimo = getattr(o, "ultimo_ahora")
            u = None if ultimo is None else _dt(ultimo).timestamp()
        except Exception as ex:   # noqa: BLE001 — un estado con un instante ilegible: no se opera con él
            return self._bloquear("RL-02", f"no se puede comparar con el último instante del estado: {type(ex).__name__}")
        if u is not None:   # el último instante del estado es el suelo, también si el reloj va detrás (revisión, hallazgo 4)
            self._suelo = u if self._suelo is None else max(self._suelo, u)
        if u is not None and lect[0] < u - self.max_desfase_s:   # el estado pudo guardar un instante de una referencia adelantada
            return self._bloquear("RL-02", f"el reloj ({_instante(lect[0]).isoformat()}) va detrás del último instante del estado ({ultimo}): "
                                           "el reloj está atrasado o el estado es de otra máquina")
        return _r(True, "OK", "el reloj no va detrás del estado", ahora=None)

    def contrastar(self, referencia, fuente) -> dict:
        """Compara el reloj con un instante externo (ISO 8601 con zona). Si están dentro de la tolerancia, da como instante el
        mayor de los dos. {ok, codigo, motivo, ahora, desfase_s}: desfase positivo si el reloj va por delante."""
        try:
            ref = _dt(referencia)
            if ref.tzinfo is None or not MINIMO <= ref < MAXIMO or not isinstance(fuente, str) or not fuente.strip():
                raise ValueError("referencia")
        except Exception:   # noqa: BLE001
            return _r(False, "RL-06", "referencia externa ilegible o fuera de lo plausible: no se contrasta", ahora=None, desfase_s=None)
        lect, err = self._leer()
        if err:
            return {**err, "desfase_s": None}
        p, m = lect
        desfase = p - ref.timestamp()
        if abs(desfase) > self.max_desfase_s:
            return self._bloquear("RL-03", f"el reloj difiere {desfase:+.1f} s de {fuente[:40]}", desfase_s=desfase)
        self._contraste = m
        return _r(True, "OK", f"reloj contrastado con {fuente[:40]}", ahora=self._dar(max(p, ref.timestamp())), desfase_s=desfase)

    def rearmar(self, actor, motivo) -> dict:
        """El operador rearma el reloj tras revisar el incidente. La lectura siguiente es la nueva ancla; antes de dar instantes
        hay que volver a contrastar, y nunca se da uno anterior a los ya dados ni al del estado."""
        if not (type(actor) is str and actor == "OPERADOR" and _motivo_ok(motivo)):
            return _r(False, "RL-06", "solo el operador rearma el reloj, con un motivo de 15 a 500 caracteres")
        if self.bloqueo is None:
            return _r(False, "RL-06", "el reloj no está bloqueado")
        self.incidentes.append({"codigo": "REARME", "actor": actor, "motivo": motivo, "antes": self.bloqueo, "suelo": self._iso_suelo()})
        self.bloqueo, self._ultima, self._ancla, self._contraste = None, None, None, None
        return _r(True, "OK", "reloj rearmado: contrástalo antes de usarlo")


def degradar_por_reloj(o, resultado) -> dict:
    """Tras un incidente del reloj, todas las carteras bajan a L1 (Constitución: estado incierto). Usa el último instante que vio
    el Orquestador, porque el del reloj no es de fiar. Nunca lanza. {ok, codigo, motivo, carteras, ya_degradadas}: RL-07 si no
    se pudo (quien llama no debe seguir operando)."""
    try:
        codigo = resultado.get("codigo") if isinstance(resultado, dict) else None
        if not (type(codigo) is str and codigo in ("RL-01", "RL-02", "RL-03", "RL-05")):
            return _r(False, "RL-06", "no es un incidente del reloj", carteras=[], ya_degradadas=[])
        cuando = o.ultimo_ahora
        if cuando is None:
            return _r(False, "RL-07", "el Orquestador no ha visto ningún instante: no hay con qué anotar la degradación", carteras=[], ya_degradadas=[])
        ya = [c for c in CARTERAS if c in o.degradadas]
        motivo = f"reloj del sistema: {codigo} {str(resultado.get('motivo', ''))[:120]}"
        hechas = [c for c in CARTERAS if o.degradar(c, motivo, "ORQUESTADOR", cuando)["ok"]]
    except Exception as ex:   # noqa: BLE001
        return _r(False, "RL-07", f"no se pudo degradar: {type(ex).__name__}", carteras=[], ya_degradadas=[])
    if len(hechas) != len(CARTERAS):
        return _r(False, "RL-07", f"no se pudieron degradar todas las carteras (solo {hechas}): no sigas operando", carteras=hechas, ya_degradadas=ya)
    return _r(True, "OK", f"carteras en L1 por el reloj: {', '.join(hechas)}", carteras=hechas, ya_degradadas=ya)
