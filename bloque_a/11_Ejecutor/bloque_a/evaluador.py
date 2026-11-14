"""Evaluador de Previsiones y Aprendizaje (AG-20) en el ejecutor: parte determinista.

- Resuelve los PRG- de F4 cuya fecha de resolución es <= as_of, con datos HT-01 vistos con ese as_of
  (sin look-ahead) y el criterio congelado; escribe solo campos de resolución (matriz 5.1).
- Métricas por clase × horizonte (FC-EVAL-001 / FC-CAL-001) y rentabilidad relativa del top-3.
- Certificados de horizonte con el criterio del Anexo A (n ≥ 100, IC 90 % del BSS > 0 con Holm, ECE ≤ q90
  del nulo y < 0,15); revocación por deterioro.
- Lecciones LEC- (predictivas, de calibración y de producto) y recalibración de pesos de RK dentro de
  bandas en modo sombra (o propuesta de tipo 3 si se sale de bandas).
- T-66: PA-09 (los PRG con `contaminacion_posible` se resuelven y registran, pero no cuentan para certificados,
  recalibración, lecciones, degradación de H5 ni historial publicado); PA-10 (`aprendizaje.solo_endurecer`: el
  aprendizaje automático solo endurece; certificados PROPUESTO hasta CT-04 y recalibración siempre como propuesta);
  PA-03 (certificados con muestra efectiva n_eff por conglomerados de fecha); PA-21 (Brier del Analista frente al de
  Prospectiva, solo informativo).
"""
from __future__ import annotations

import copy
import math
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from scipy import stats

from .calendario import _sesiones_entre, validar_festivos_ps2
from .configuracion import CLASES, TABLA_HORIZONTES, parametro, parametros_ht03
from .herramientas.ht01_datos import DatosNoDisponibles
from .herramientas.ht05_planificador import dias_habiles_entre
from .motor import evaluacion as ev

CADUCIDAD_MESES = {"anecdotica": 3, "recurrente": 6, "estadistica": 12}
# Escalón inferior de aplicabilidad de un horizonte (12.2): «Sí» → «Limitado» → «No»
ESCALON_INFERIOR = {"SI": "LIMITADO", "LIMITADO": "NO"}


def _coma(x) -> str:
    """Número con coma decimal para los textos en español (QA r01 de T-65, H-11)."""
    return str(x).replace(".", ",")


def contaminacion_posible(p: dict) -> bool:
    """PA-09: el PRG puede estar contaminado por el conocimiento del modelo (backtest con un modelo real antes de su
    fecha de corte). Sin el campo o con null (registros anteriores a T-66): false. Cualquier otro valor distinto de
    false cuenta como contaminado (ante la duda, se marca)."""
    v = p.get("contaminacion_posible")
    return not (v is None or v is False)


def _prob_valida(v) -> bool:
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v) and 0.0 <= float(v) <= 1.0


def _version_menor_siguiente(v) -> str:
    """12.2: todo ajuste se aplica con una versión menor nueva (p. ej., 5.1 → 5.2)."""
    try:
        mayor, menor = str(v).split(".")[:2]
        return f"{int(mayor)}.{int(menor) + 1}"
    except ValueError:
        return str(v)


# Tabla única de bandas verbales. Valores por defecto = Documento 0 V5.1, Anexo A, «Bandas verbales y probabilidad
# interna» (Calibrable): Muy probable 80–95 % (85 %) · Más probable que no 60–75 % (65 %) · Incierto 45–55 % (50 %) ·
# Poco probable 25–40 % (35 %) · Muy poco probable 5–20 % (15 %). `codigo` es el valor de F4 (`banda_verbal`) y
# `texto` el del esquema JSON del paquete (`$defs.vista_horizonte.banda`). Se puede sustituir con la clave de
# configuración `bandas_verbales` (misma estructura); `validar_bandas` la valida y falla cerrado si no es coherente.
# T-65 (QA de T-53, H-07): la tabla de la configuración vive en cada `Evaluador` (`self.bandas`), no en el módulo: dos
# instancias con tablas distintas no se pisan. Las funciones del módulo usan siempre la tabla del Anexo A.
BANDAS_VERBALES_POR_DEFECTO = (
    {"codigo": "MUY_PROBABLE", "texto": "muy probable", "min": 0.80, "max": 0.95, "prob_interna": 0.85},
    {"codigo": "MAS_PROBABLE_QUE_NO", "texto": "más probable que no", "min": 0.60, "max": 0.75, "prob_interna": 0.65},
    {"codigo": "INCIERTO", "texto": "incierto", "min": 0.45, "max": 0.55, "prob_interna": 0.50},
    {"codigo": "POCO_PROBABLE", "texto": "poco probable", "min": 0.25, "max": 0.40, "prob_interna": 0.35},
    {"codigo": "MUY_POCO_PROBABLE", "texto": "muy poco probable", "min": 0.05, "max": 0.20, "prob_interna": 0.15},
)
_CODIGOS_BANDA: dict[str, str] = {str(b["codigo"]): str(b["texto"]) for b in BANDAS_VERBALES_POR_DEFECTO}   # vocabulario fijo (F4 y esquema)


def validar_bandas(tabla=None) -> list[dict]:
    """Valida una tabla de bandas (None = valores del Anexo A) y la devuelve ordenada, sin efectos. Exige los cinco códigos
    del vocabulario, intervalos dentro de [0, 1], disjuntos, y probabilidad interna dentro de su intervalo."""
    filas = [dict(b) for b in (tabla if tabla is not None else BANDAS_VERBALES_POR_DEFECTO)]
    try:
        for b in filas:
            b["min"], b["max"], b["prob_interna"] = float(b["min"]), float(b["max"]), float(b["prob_interna"])
    except (KeyError, TypeError, ValueError) as e:
        raise ValueError(f"bandas_verbales: fila incompleta o no numérica ({e})") from e
    if sorted(str(b.get("codigo")) for b in filas) != sorted(_CODIGOS_BANDA):
        raise ValueError(f"bandas_verbales: se esperan exactamente las bandas {sorted(_CODIGOS_BANDA)}")
    for b in filas:
        if b.get("texto") != _CODIGOS_BANDA[b["codigo"]]:
            raise ValueError(f"bandas_verbales: el texto de {b['codigo']} debe ser «{_CODIGOS_BANDA[b['codigo']]}» (esquema del paquete)")
        if not (0.0 <= b["min"] <= b["prob_interna"] <= b["max"] <= 1.0):
            raise ValueError(f"bandas_verbales: intervalo o probabilidad interna incoherentes en {b['codigo']}")
    filas.sort(key=lambda b: b["min"])
    if any(a["max"] >= s["min"] for a, s in zip(filas, filas[1:])):
        raise ValueError("bandas_verbales: los intervalos se solapan")
    return filas


# Tabla del Anexo A (solo lectura) y probabilidad representativa de cada banda verbal: solo para uso interno cuando un PRG
# H5 no registra probabilidad interna (V5.1: en H5 solo se registra la banda)
_BANDAS: tuple = tuple(validar_bandas())
PROB_DE_BANDA: dict[str, float] = {b["codigo"]: b["prob_interna"] for b in _BANDAS}


def _distancia_a_50(b: dict) -> float:
    return 0.0 if b["min"] <= 0.5 <= b["max"] else min(abs(b["min"] - 0.5), abs(b["max"] - 0.5))


def _banda(p: float, bandas=None) -> dict:
    """Banda de una probabilidad interna. Dentro de un intervalo, esa banda; en un hueco entre dos bandas, la más
    cercana a 50 % (prudencia: prompt de Prospectiva, 6.5); por encima o por debajo de todas, la extrema. `bandas` es una
    tabla ya validada (la de un Evaluador); None = la del Anexo A."""
    tabla = _BANDAS if bandas is None else bandas
    try:
        p = float(p)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Probabilidad interna no numérica: {p!r}") from e
    if not math.isfinite(p) or not 0.0 <= p <= 1.0:
        raise ValueError(f"Probabilidad interna fuera de [0, 1]: {p!r}")
    for b in tabla:
        if b["min"] <= p <= b["max"]:
            return b
    if p < tabla[0]["min"]:
        return tabla[0]
    if p > tabla[-1]["max"]:
        return tabla[-1]
    inf, sup = next((a, s) for a, s in zip(tabla, tabla[1:]) if a["max"] < p < s["min"])
    return min((inf, sup), key=_distancia_a_50)


def banda_de(p: float, bandas=None) -> str:
    """Código de banda verbal (F4, `banda_verbal`) a partir de la probabilidad interna."""
    return _banda(p, bandas)["codigo"]


def banda_publicable(p: float, bandas=None) -> str:
    """Banda tal como la escribe el esquema JSON del paquete (`vista_horizonte.banda`): cinco valores."""
    return _banda(p, bandas)["texto"]


def etiqueta_celda(clave):
    """Conserva el identificador de los informes antiguos para el grupo sin método."""
    clase, horizonte, metodo = clave
    return f"{clase}|{horizonte}|{metodo}" if metodo else f"{clase}|{horizonte}"


class Evaluador:
    def __init__(self, almacen, proveedor, motor, cfg: dict, universo: pd.DataFrame) -> None:
        self.almacen = almacen
        self.proveedor = proveedor
        self.motor = motor
        self.cfg = cfg
        # Tabla 8.3 de partida (la de la configuración o la estática), fijada al crear el Evaluador: si F10 no tiene P-31
        # vigente, se vuelve a ella y no a la última tabla aplicada en memoria (T-53, QA r02 H-12)
        self._tabla_base = copy.deepcopy(cfg.get("_tabla_horizontes") or TABLA_HORIZONTES)
        self.universo = universo
        # Tabla de bandas verbales de la configuración (None = Anexo A), propia de esta instancia (T-65, H-07); falla
        # cerrado si es incoherente
        self.bandas = tuple(validar_bandas(cfg.get("bandas_verbales")))
        # T-91 (QA r05 de T-65, H-26): las sesiones de H1 se cuentan con los mismos festivos que PS2 al emitir
        self._festivos_ps2 = validar_festivos_ps2(parametro(cfg, "ps2_festivos"))
        self.prob_de_banda = {b["codigo"]: b["prob_interna"] for b in self.bandas}
        # T-66: claves nuevas validadas al crear el Evaluador (falla cerrado si no son válidas)
        self.solo_endurecer()
        self._min_conglomerados()

    def banda_de(self, p: float) -> str:
        return banda_de(p, self.bandas)

    def banda_publicable(self, p: float) -> str:
        return banda_publicable(p, self.bandas)

    def _clave(self, seccion: str, clave: str):
        return parametro(self.cfg, f"{seccion}.{clave}")

    def solo_endurecer(self) -> bool:
        """PA-10 (`aprendizaje.solo_endurecer`, [PROPUESTO]): el aprendizaje automático solo endurece."""
        v = self._clave("aprendizaje", "solo_endurecer")
        if not isinstance(v, bool):
            raise ValueError(f"aprendizaje.solo_endurecer debe ser true o false, no {v!r}")
        return v

    def _min_conglomerados(self) -> int:
        v = self._clave("evaluacion", "min_conglomerados_bootstrap")
        if isinstance(v, bool) or not isinstance(v, int) or v < 2:
            raise ValueError(f"evaluacion.min_conglomerados_bootstrap debe ser un entero ≥ 2, no {v!r}")
        return v

    @staticmethod
    def _fechas_conglomerado(lst: list[dict]) -> list[str] | None:
        """PA-03: fecha del conglomerado de cada PRG (`fecha_resolucion`; si falta, `fecha_emision`). None si alguna
        falta o no se puede interpretar: entonces no hay n_eff y la celda no certifica (falla cerrado)."""
        out = []
        for x in lst:
            f = x.get("fecha_resolucion") or x.get("fecha_emision")
            if not f:
                return None
            try:
                ts = pd.Timestamp(f)
            except (ValueError, TypeError):
                return None
            if pd.isna(ts):
                return None
            out.append(str(ts.date()))
        return out

    # ------------------------------------------------------------------------------------
    # Rentabilidades y referencia ingenua
    # ------------------------------------------------------------------------------------
    def simbolos_clase(self, clase: str) -> list[str]:
        return [s for s in self.universo[self.universo["clase"] == clase]["simbolo"] if self.proveedor.tiene(s)]

    def _edad_ps2(self, desde, hasta, horizonte: str | None) -> int:
        """Antigüedad de un dato como la mide PS2 (Anexo A, P-13): en H1, sesiones sin los festivos de `ps2_festivos`
        (T-91, QA r05 de T-65, H-26: antes, sesiones hábiles sin festivos); en el resto, días naturales."""
        return _sesiones_entre(desde, hasta, self._festivos_ps2) if horizonte == "H1" else (pd.Timestamp(hasta) - pd.Timestamp(desde)).days

    def motivo_no_fresca(self, d0, d1, f1, horizonte: str) -> str | None:
        """T-65 (QA r03, H-16; QA r04, H-24): una serie sirve para resolver un pronóstico de horizonte `horizonte` solo si
        tiene un dato posterior al de la emisión (`d1 > d0`) y su último dato no es más antiguo, a la fecha de resolución
        `f1`, que la antigüedad máxima de PS2 de ese horizonte (Anexo A, P-13: `ps2_antiguedad_maxima_dias`; H1 en sesiones
        hábiles, el resto en días naturales). Devuelve el motivo, o None si sirve."""
        d0, d1, f1 = pd.Timestamp(d0), pd.Timestamp(d1), pd.Timestamp(f1)
        if d1 <= d0:
            return f"sin dato posterior a la emisión (último del {d1.date()})"
        lim = int(parametro(self.cfg, "ps2_antiguedad_maxima_dias")[horizonte])
        edad = self._edad_ps2(d1, f1, horizonte)
        if edad > lim:
            unidad = "sesiones" if horizonte == "H1" else "días"
            return f"último dato del {d1.date()}, {edad} {unidad} antes de la resolución (máximo {lim} en {horizonte})"
        return None

    def _base_conocida(self, simbolo, fecha):
        """T-92 (auditoría de Astra, D01): el nivel inicial es el que se conocía al emitir (corte de conocimiento de HT-01),
        no el que el proveedor publica después (una revisión posterior no mueve la base)."""
        serie = self.proveedor.serie(simbolo, fin=fecha, conocido_el=fecha)
        if serie.empty:
            raise DatosNoDisponibles(f"{simbolo}: falta el dato conocido al emitir")
        # T-92 (QA r01, H-06): el cierre de la base pasa la misma validación que cualquier cierre de HT-01 (no positivo, no
        # finito, booleano o fecha repetida → `DatosInvalidos`, que es un `DatosNoDisponibles`)
        ult = self.proveedor._validar_cierres(simbolo, serie[serie.index == serie.index.max()])
        return {"valor": float(ult.iloc[-1]), "fecha": str(ult.index[-1].date())}

    def bases_cesta(self, clase, fecha, horizonte: str | None = None):
        """T-92 (D02): los miembros de la CESTA observables al emitir, con su nivel inicial. Se congelan en F4 al emitir; para
        pronósticos antiguos sin ellos se reconstruyen con el corte de conocimiento de la emisión. Con `horizonte`, queda fuera
        el miembro cuyo último dato ya era, al emitir, más antiguo que la antigüedad de PS2 de ese horizonte (T-65, H-24):
        eso se sabía al emitir, así que no es información posterior."""
        bases = {}
        lim = int(parametro(self.cfg, "ps2_antiguedad_maxima_dias")[horizonte]) if horizonte else None
        for simbolo in self.simbolos_clase(clase):
            try:
                base = self._base_conocida(simbolo, fecha)
            except DatosNoDisponibles:
                continue
            if lim is not None:
                if self._edad_ps2(base["fecha"], fecha, horizonte) > lim:
                    continue
            bases[simbolo] = base
        return bases

    def _rentabilidad_serie(self, simbolo: str, f0, f1, base=None) -> tuple[float, pd.Timestamp, pd.Timestamp]:
        """Rentabilidad entre la base (la congelada en F4 si la hay; si no, la conocida al emitir) y el cierre en f1, con la
        fecha de la base y la del cierre. Falla cerrado con una base no numérica, nula, no finita o posterior a la emisión."""
        if base is None:
            base = self._base_conocida(simbolo, f0)
        try:
            if isinstance(base, dict):
                v0 = base.get("valor")
                d0 = pd.Timestamp(base["fecha"]) if base.get("fecha") else self.proveedor.valor_en(simbolo, f0)[0]
            else:   # registros antiguos con el nivel como número suelto
                v0, d0 = base, self.proveedor.valor_en(simbolo, f0)[0]
        except (ValueError, TypeError, OverflowError) as e:   # T-92 (QA r01, H-14): una fecha ilegible no tumba C5
            raise DatosNoDisponibles(f"{simbolo}: fecha de la base ilegible ({type(e).__name__})") from None
        if pd.isna(d0) or d0 > pd.Timestamp(f0):
            raise DatosNoDisponibles(f"{simbolo}: base posterior a la emisión")
        d1, v1 = self.proveedor.valor_en(simbolo, f1)
        # T-92 (QA r01, H-06): una base no positiva tampoco vale (los cierres de HT-01 son precios > 0)
        if (isinstance(v0, bool) or not isinstance(v0, (float, int)) or not math.isfinite(v0) or v0 <= 0
                or not math.isfinite(v1)):
            raise DatosNoDisponibles(f"HT-01: base o cierre no válido de {simbolo}")
        return v1 / v0 - 1, d0, d1

    def rentabilidad(self, simbolo: str, clase: str, f0, f1, horizonte: str | None = None, *,
                     base=None, hasta=None) -> tuple[float, pd.Timestamp]:
        """Rentabilidad de `simbolo` entre f0 y f1 y la fecha de su último dato. Con `horizonte` (la resolución lo pasa
        siempre), falla (`DatosNoDisponibles`) si la serie no sirve para ese horizonte (`motivo_no_fresca`); sin él, si no
        tiene un dato posterior a la base. En la CESTA cuentan los mismos miembros que al emitir (`base`, los congelados en
        F4): T-92 (D02) sustituye la regla de T-65 de dejar fuera al miembro que no sirve, porque saber al resolver que un
        miembro dejó de publicarse es información posterior a la emisión (sesgo de supervivencia). Si un miembro no sirve,
        la CESTA entera no sirve (el pronóstico espera y, pasado el plazo, queda NO_RESOLUBLE). Nunca entra un 0. La fecha
        devuelta es la más antigua de los miembros."""
        if simbolo == "CESTA":
            bases = self.bases_cesta(clase, f0, horizonte) if base is None else base
            if not isinstance(bases, dict) or not bases:
                raise DatosNoDisponibles(f"Cesta {clase} sin niveles iniciales")
            patas = [self.rentabilidad(s, clase, f0, f1, horizonte, base=b, hasta=hasta) for s, b in sorted(bases.items())]
            # T-91 (QA r05 de T-65, H-27): todos los miembros se miden hasta la misma fecha, la más antigua de las que sirven;
            # cada uno vuelve a pasar la frescura frente a la fecha de resolución (QA r01 de T-91, H-01). Se repite hasta que
            # coinciden (QA r02, H-05): con un hueco en la fecha común, un miembro queda en una fecha anterior. Cada vuelta baja
            # la fecha común, así que acaba: o coinciden, o un miembro deja de ser fresco y el pronóstico espera
            previo = None
            while len({f for _, f in patas}) > 1:
                corte = min(f for _, f in patas)
                if previo is not None and corte >= previo:   # la fecha común no baja: no se puede alinear (falla cerrado)
                    raise DatosNoDisponibles(f"Cesta {clase}: los miembros no se alinean en una fecha común")
                previo = corte
                patas = [self.rentabilidad(s, clase, f0, f1, horizonte, base=b, hasta=corte) for s, b in sorted(bases.items())]
            return float(np.mean([v for v, _ in patas])), min(f for _, f in patas)
        r, d0, d1 = self._rentabilidad_serie(simbolo, f0, f1 if hasta is None else hasta, base)
        motivo = self.motivo_no_fresca(d0, d1, f1, horizonte) if horizonte else (
            f"sin dato posterior a la emisión (último del {d1.date()})" if d1 <= d0 else None)
        if motivo:
            raise DatosNoDisponibles(f"HT-01: {simbolo} no sirve para resolver: {motivo}")
        return r, d1

    def tasa_base(self, proxy: str, referencia: str | None, clase: str, sesiones: int, sentido_positivo: bool,
                  as_of, run_id: str | None = None) -> dict:
        """RI-TB: frecuencia histórica (ventanas no solapadas de 3 años hasta as_of) del suceso pronosticado."""
        tb = parametro(self.cfg, "tasa_base")   # T-65 (CA-14 de T-53): ventana, mínimo, valor sin historia y recorte
        ini = pd.Timestamp(as_of) - pd.DateOffset(years=int(tb["ventana_anios"]))
        s = self.proveedor.cierres(proxy, ini, as_of)
        serie = s.pct_change(sesiones).iloc[sesiones::sesiones] if len(s) > sesiones else pd.Series(dtype=float)
        excluidos_cesta: list[str] = []
        if referencia and referencia != proxy:
            if referencia == "CESTA":
                # Como en `rentabilidad`: los miembros sin datos en [ini, as_of] (p. ej., aún no cotizan) se excluyen
                # y se declaran; falla cerrado solo si no queda ninguno
                comp = []
                for x in self.simbolos_clase(clase):
                    try:
                        comp.append(self.proveedor.cierres(x, ini, as_of).pct_change(sesiones))
                    except DatosNoDisponibles:
                        excluidos_cesta.append(x)
                if not comp:
                    raise DatosNoDisponibles(f"Cesta {clase} sin datos entre {ini.date()} y {pd.Timestamp(as_of).date()}")
                ref = pd.concat(comp, axis=1).mean(axis=1)
            else:
                ref = self.proveedor.cierres(referencia, ini, as_of).pct_change(sesiones)
            serie = (serie - ref.reindex(serie.index)).dropna()
        serie = serie.dropna()
        min_v, (lo, hi) = int(tb["min_ventanas"]), (float(x) for x in tb["recorte"])
        if len(serie) < min_v:
            p = float(tb["sin_historia"])
        else:
            p = float(np.mean(serie > 0)) if sentido_positivo else float(np.mean(serie < 0))
        p = min(max(p, lo), hi)
        # Registro en RC (operación de la familia FC-EVAL-001: referencia RI-TB)
        calc_id = self.almacen.nuevo_id("CALC")
        self.almacen.escribir("RC", "AG-13", {
            "tipo_entrada": "SERVICIO", "calc_id": calc_id, "contrato": "CT-09", "run_id": run_id, "solicitante": "AG-10",
            "operacion": {"method_id": "RI-TB", "ficha_id": "FC-EVAL-001", "ficha_version": "1.0", "catalog_version": "4.0",
                          "op_sin_ficha": False}, "perfil": ["TRANSVERSAL"], "clase": clase, "modo": "SYNC_CALC",
            "plan": "PLAN_MIN", "as_of": str(pd.Timestamp(as_of).date()), "estado": "SERVED",
            "datos": [{"serie_ht01": proxy, "fecha_dato": str(s.index[-1].date()) if len(s) else None, "n": len(s)},
                      {"serie_ht01": referencia}],
            "parametros": {"sesiones": sesiones, "sentido_positivo": sentido_positivo, "ventana": f"{tb['ventana_anios']} años, no solapadas"},
            "semilla": None, "resultado": {"forma": "VALOR", "payload": {"tasa_base": p, "n_ventanas": len(serie)}},
            "clase_cifra": "ESTADISTICA", "referencia_ingenua": {"tipo": "RI-TB"}, "madurez_metodo": "IMPLEMENTADO",
            "consumo_uc": 0.0, "limitaciones": ([] if len(serie) >= min_v else [f"menos de {min_v} ventanas: tasa base {_coma(tb['sin_historia'])} por defecto"])
            + ([f"cesta de {clase}: excluidos por falta de datos en la ventana: {', '.join(excluidos_cesta)}"] if excluidos_cesta else [])})
        return {"tipo": "TASA_BASE", "valor_o_prob": round(p, 4), "calc_id": calc_id, "n_ventanas": len(serie)}

    # ------------------------------------------------------------------------------------
    # Resolución
    # ------------------------------------------------------------------------------------
    def resolver(self, as_of, run_id: str | None = None) -> list[dict]:
        as_of = pd.Timestamp(as_of).normalize()
        abiertos = [p for p in self.almacen.estado("F4", as_of).values() if p.get("estado") == "ABIERTO"]
        # V5.1: los PRG H5 (sin probabilidad interna) no se puntúan con Brier: se evalúan por sus hitos HIT-,
        # que son pronósticos ordinarios de su propio horizonte y se resuelven aquí como los demás
        pendientes = [p for p in abiertos if pd.Timestamp(p["fecha_resolucion"]) <= as_of and p.get("prob_interna") is not None]
        resueltos: list[dict] = []
        filas: list[tuple[dict, dict | None]] = []
        for p in sorted(pendientes, key=lambda x: x["prg_id"]):
            f0, f1 = pd.Timestamp(p["fecha_emision"]), pd.Timestamp(p["fecha_resolucion"])
            try:
                # T-65 (QA r03, H-16; QA r04, H-24): cada serie (proxy, referencia y cada miembro de la CESTA) debe tener un
                # dato posterior al de la emisión y no más antiguo que la antigüedad de PS2 del horizonte; si no, el
                # pronóstico espera y, pasado el plazo, queda NO_RESOLUBLE. Nunca se resuelve con una rentabilidad 0.
                # T-92 (D01): la base de cada serie es la congelada en F4 al emitir
                hz = p["horizonte"]
                rp, d1 = self.rentabilidad(p["variable"]["serie_ht01"], p["clase"], f0, f1, hz, base=p.get("nivel_referencia"))
                rr, d1b = None, None
                if p["tipo_pronostico"] == "RELATIVO":
                    base_ref = p.get("bases_cesta") if p["referencia_indice"] == "CESTA" else p.get("nivel_referencia_indice")
                    if base_ref is not None and not isinstance(base_ref, dict) and p.get("fecha_nivel_referencia_indice"):
                        base_ref = {"valor": base_ref, "fecha": p["fecha_nivel_referencia_indice"]}
                    if base_ref is None and p["referencia_indice"] == "CESTA":
                        base_ref = self.bases_cesta(p["clase"], f0, hz)
                    rr, d1b = self.rentabilidad(p["referencia_indice"], p["clase"], f0, f1, hz, base=base_ref)
                    previo_corte = None
                    while d1b != d1:
                        # T-91 (QA r05 de T-65, H-27; `[PROPUESTO]`, INC-T91-01): las dos series sirven, pero el suceso
                        # pronosticado se mide sobre la misma ventana: las dos hasta la fecha más antigua de las dos, y cada una
                        # vuelve a pasar la frescura frente a f1 (QA r01 de T-91, H-01). Se repite hasta que coinciden (QA r02,
                        # H-05: un hueco o un festivo en la fecha común); cada vuelta baja la fecha común, así que acaba
                        corte = min(d1, d1b)
                        if previo_corte is not None and corte >= previo_corte:   # no baja: no se alinean (falla cerrado)
                            raise DatosNoDisponibles(f"{p['prg_id']}: proxy y referencia no se alinean en una fecha común")
                        previo_corte = corte
                        rp, d1 = self.rentabilidad(p["variable"]["serie_ht01"], p["clase"], f0, f1, hz, base=p.get("nivel_referencia"),
                                                   hasta=corte)
                        rr, d1b = self.rentabilidad(p["referencia_indice"], p["clase"], f0, f1, hz, base=base_ref, hasta=corte)
                x = rp - rr if rr is not None else rp
                # Falla cerrado: un valor no finito (cierre NaN, nivel inicial 0…) es un dato no disponible,
                # nunca un resultado (antes, int(nan > 0) = 0 daba NO_OCURRIDO)
                if not all(math.isfinite(v) for v in (rp, x) + ((rr,) if rr is not None else ())):
                    raise DatosNoDisponibles(f"{p['prg_id']}: rentabilidad no finita con los datos de HT-01")
            except DatosNoDisponibles:
                if dias_habiles_entre(f1, as_of) >= int(parametro(self.cfg, "evaluacion.dias_habiles_no_resoluble")):
                    filas.append((p, None))
                continue
            positivo = p["sentido"] == "POSITIVO"
            o = int((x > p.get("umbral", 0.0)) if positivo else (x < -p.get("umbral", 0.0)))
            # T-91 (QA r01, H-04): un registro antiguo con el nivel como número suelto no tiene fecha; su base es la última
            # sesión ≤ la emisión (`_rentabilidad_serie`), así que no puede ser posterior
            nr = p.get("nivel_referencia")
            f_base = pd.Timestamp(nr["fecha"]) if isinstance(nr, dict) and nr.get("fecha") else f0
            fuga_ok = (f_base <= f0 and d1 <= as_of and f1 <= as_of)
            fuga_ok = fuga_ok and (d1b is None or d1b <= as_of)
            filas.append((p, {"rent_proxy": rp, "rent_referencia": rr, "exceso": x, "o": o,
                              "fecha_dato": max(d1, d1b) if d1b is not None else d1, "fecha_dato_proxy": d1,
                              "fecha_dato_referencia": d1b, "fuga": "SUPERADA" if fuga_ok else "FALLIDA"}))
        if not filas:
            return []
        validas = [(p, r) for p, r in filas if r is not None]
        calc_id = None
        if validas:
            res = self.motor.servir({"operacion": "FC-EVAL-001", "plan": "PLAN_MIN", "datos": [{"valores": {
                "p": [p["prob_interna"] for p, _ in validas], "o": [r["o"] for _, r in validas],
                "p_ref": [p["referencia_ingenua"]["valor_o_prob"] for p, _ in validas]}}],
                # T-65 (CS-10 de T-53): réplicas y simulaciones de la configuración (antes, 200 escritas aquí)
                "parametros": {"replicas": int(parametro(self.cfg, "evaluacion.bootstrap_replicas")),
                               "simulaciones": int(parametro(self.cfg, "evaluacion.simulaciones_ece"))},
                "fecha_corte": str(as_of.date())}, "AG-20", run_id)
            calc_id = res.get("calc_id")
        for p, r in filas:
            if r is None:
                e = {"prg_id": p["prg_id"], "tipo_entrada": "RESOLUCION", "estado": "NO_RESOLUBLE",
                     "resolucion": {"fecha_resuelto": str(as_of.date()), "motivo_no_resoluble": f"sin dato tras {int(parametro(self.cfg, 'evaluacion.dias_habiles_no_resoluble'))} días hábiles",
                                    "comprobacion_fuga": "SUPERADA", "fallback_aplicado": False}}
            else:
                pi, pr = float(p["prob_interna"]), float(p["referencia_ingenua"]["valor_o_prob"])
                o = r["o"]
                e = {"prg_id": p["prg_id"], "tipo_entrada": "RESOLUCION", "estado": "RESUELTO",
                     "resolucion": {"fecha_resuelto": str(as_of.date()), "fecha_dato": str(r["fecha_dato"].date()),
                                    # T-65 (QA r04, H-24): la fecha de cada serie, no solo la más reciente
                                    "fecha_dato_proxy": str(r["fecha_dato_proxy"].date()),
                                    "fecha_dato_referencia": None if r["fecha_dato_referencia"] is None
                                    else str(r["fecha_dato_referencia"].date()),
                                    "valor_observado": round(r["exceso"], 8), "rent_proxy": round(r["rent_proxy"], 8),
                                    "rent_referencia": None if r["rent_referencia"] is None else round(r["rent_referencia"], 8),
                                    "unidad": "tanto por uno", "fuente_usada": f"HT-01:{self.proveedor.nombre}",
                                    "vintage": str(as_of.date()), "fallback_aplicado": False,
                                    "resultado": "OCURRIDO" if o else "NO_OCURRIDO", "resultado_binario": o,
                                    "puntuaciones": {"brier": (pi - o) ** 2, "log": -math.log(min(max(pi if o else 1 - pi, 0.01), 0.99)),
                                                     "brier_ref": (pr - o) ** 2,
                                                     "log_ref": -math.log(min(max(pr if o else 1 - pr, 0.01), 0.99))},
                                    "calc_id": calc_id, "comprobacion_fuga": r["fuga"]}}
            self.almacen.escribir("F4", "AG-20", e)
            resueltos.append({**p, **e})
        self.almacen.escribir("F6", "AG-20", {"tipo_entrada": "RES", "id": f"RES-{as_of.date()}-{self.almacen.nuevo_id('RESL')[-4:]}",
                                              "fecha": str(as_of.date()),
                                              "prg_resueltos": [x["prg_id"] for x in resueltos if x["estado"] == "RESUELTO"],
                                              "prg_no_resolubles": [x["prg_id"] for x in resueltos if x["estado"] == "NO_RESOLUBLE"],
                                              "calc_id": calc_id,
                                              "comprobacion_fuga": "SUPERADA" if all(r is None or r["fuga"] == "SUPERADA" for _, r in filas) else "FALLIDA"})
        return resueltos

    # ------------------------------------------------------------------------------------
    # Métricas
    # ------------------------------------------------------------------------------------
    def resueltos(self, as_of=None, solo_informe: bool = False, admisibles: bool = True) -> list[dict]:
        """Pronósticos ordinarios resueltos sin fuga. Excluye los hitos HIT- de los H5 (`es_hito`): no son pronósticos
        independientes de la celda en la que se registran (8.3, 12.1); se evalúan aparte, por tipo × H5, en `estado_h5`.
        Así no cuentan en métricas, certificados, historial publicado ni recalibración.
        `admisibles` (PA-09): excluye los PRG con `contaminacion_posible`; False los devuelve todos."""
        out = [p for p in self.almacen.estado("F4", as_of).values()
               if p.get("estado") == "RESUELTO" and not p.get("es_hito")
               and (p.get("resolucion") or {}).get("comprobacion_fuga") == "SUPERADA"]
        if admisibles:
            out = [p for p in out if not contaminacion_posible(p)]
        return [p for p in out if p.get("en_informe")] if solo_informe else out

    def excluidos_contaminacion(self, as_of=None, solo_informe: bool = False) -> dict:
        """PA-09: cuántos PRG resueltos se excluyen de la evaluación por `contaminacion_posible`, en total y por celda."""
        ex = [p for p in self.resueltos(as_of, solo_informe, admisibles=False) if contaminacion_posible(p)]
        por = Counter(f"{p['clase']}|{p['horizonte']}" for p in ex)
        return {"total": len(ex), "por_celda": dict(sorted(por.items()))}

    @staticmethod
    def _analista_vs_prospectiva(lst: list[dict]) -> dict | None:
        """PA-21 (solo informativo): Brier de la probabilidad propia del Analista (`prob_analista`) frente al de
        Prospectiva (`prob_interna`) sobre los mismos PRG. Un `prob_analista` no numérico o fuera de [0, 1] no entra y
        se cuenta como inválido."""
        con = [x for x in lst if x.get("prob_analista") is not None]
        if not con:
            return None
        val = [x for x in con if _prob_valida(x["prob_analista"])]
        oo = [int(x["resolucion"]["resultado_binario"]) for x in val]
        b_a = ev.brier([float(x["prob_analista"]) for x in val], oo) if val else None
        b_p = ev.brier([float(x["prob_interna"]) for x in val], oo) if val else None
        return {"n": len(val), "brier_analista": b_a, "brier_prospectiva": b_p,
                "diferencia": None if b_a is None or b_p is None else b_a - b_p, "invalidos": len(con) - len(val),
                "nota": "PA-21, solo informativo: diferencia < 0, el Analista acierta más que Prospectiva; no cambia ninguna decisión"}

    def metricas(self, as_of=None, completas: bool = False, solo_informe: bool = False, admisibles: bool = True) -> dict:
        """Métricas por clase × horizonte. `completas` añade bootstrap del BSS, ECE con nulo y DM-HLN.
        T-66: sin los PRG con `contaminacion_posible` (PA-09; `excluidos_contaminacion` dice cuántos), con la muestra
        efectiva `n_eff` (PA-03) y, si hay `prob_analista`, el Brier del Analista frente al de Prospectiva (PA-21)."""
        celdas: dict[tuple[str, str], list[dict]] = defaultdict(list)
        for p in self.resueltos(as_of, solo_informe, admisibles):
            celdas[(p["clase"], p["horizonte"])].append(p)
        excl = self.excluidos_contaminacion(as_of, solo_informe)["por_celda"] if admisibles else {}
        out = {}
        for (c, h), lst in sorted(celdas.items()):
            lst.sort(key=lambda x: (x["fecha_emision"], x["prg_id"]))
            pp = [float(x["prob_interna"]) for x in lst]
            oo = [int(x["resolucion"]["resultado_binario"]) for x in lst]
            pr = [float(x["referencia_ingenua"]["valor_o_prob"]) for x in lst]
            tasa_base = float(np.mean(pr))
            fechas = self._fechas_conglomerado(lst)
            if completas:
                m = ev.evaluar_celda(pp, oo, pr, tasa_base, int(parametro(self.cfg, "evaluacion.bootstrap_replicas")),
                                     int(parametro(self.cfg, "evaluacion.simulaciones_ece")), float(parametro(self.cfg, "evaluacion.nivel_ic")),
                                     fechas=fechas, min_conglomerados=self._min_conglomerados())
            else:
                m = {"n": len(lst), "brier": ev.brier(pp, oo), "brier_ref": ev.brier(pr, oo),
                     "acierto": ev.acierto_direccional(oo, tasa_base), "calibracion_global": {"p_media": float(np.mean(pp)), "frecuencia": float(np.mean(oo))},
                     "bss": {"valor": (1 - ev.brier(pp, oo) / ev.brier(pr, oo)) if ev.brier(pr, oo) > 0 else None, "ic": [None, None]}}
                muestra = ev.n_efectiva(fechas, np.asarray(oo, float) - np.asarray(pp, float)) if fechas is not None else None
                m["n_eff"] = muestra["n_eff"] if muestra else None
                m["muestra_efectiva"] = muestra
            m["excluidos_contaminacion"] = int(excl.get(f"{c}|{h}", 0))
            analista = self._analista_vs_prospectiva(lst)
            if analista is not None:
                m["analista_vs_prospectiva"] = analista
            informe = [x for x in lst if x.get("en_informe")]
            rel = [x["resolucion"]["valor_observado"] * (1 if x["sentido"] == "POSITIVO" else -1) for x in informe]
            m["rentabilidad_relativa_media_top3"] = float(np.mean(rel)) if rel else None
            m["n_top3"] = len(informe)
            m["referencia"] = lst[0].get("referencia_indice")
            out[f"{c}|{h}"] = m
        return out

    def historial_aciertos(self, as_of, semanas: int = 12) -> dict:
        """Historial publicable (R13 · 11): opciones del informe resueltas en la ventana, con tamaño muestral."""
        lim = pd.Timestamp(as_of) - pd.Timedelta(weeks=semanas)
        lst = [p for p in self.resueltos(as_of, solo_informe=True) if pd.Timestamp(p["resolucion"]["fecha_resuelto"]) >= lim]
        # PA-09: los PRG con contaminación posible no entran en el historial publicado (se declaran en la nota)
        n_contaminados = sum(1 for p in self.resueltos(as_of, solo_informe=True, admisibles=False)
                             if contaminacion_posible(p) and pd.Timestamp(p["resolucion"]["fecha_resuelto"]) >= lim)
        no_res = [p for p in self.almacen.estado("F4", as_of).values()
                  if p.get("estado") == "NO_RESOLUBLE" and p.get("en_informe") and not p.get("es_hito")
                  and not contaminacion_posible(p)]
        def celda(xs, ref_txt):
            n = len(xs)
            k = sum(int(x["resolucion"]["resultado_binario"]) for x in xs)
            pr = float(np.mean([x["referencia_ingenua"]["valor_o_prob"] for x in xs])) if xs else 0.5
            sig = bool(n >= 30 and stats.binomtest(k, n, pr, alternative="greater").pvalue < 0.10) if n else False
            ph = defaultdict(lambda: {"n": 0, "aciertos": 0})
            for x in xs:
                ph[x["horizonte"]]["n"] += 1
                ph[x["horizonte"]]["aciertos"] += int(x["resolucion"]["resultado_binario"])
            return {"n": n, "aciertos": k, "tasa_acierto": round(k / n, 4) if n else None, "referencia": ref_txt,
                    "tasa_esperada_azar": round(pr, 4), "significativo": sig, "por_horizonte": dict(ph)}
        por_clase = {}
        for c in CLASES:
            xs = [x for x in lst if x["clase"] == c]
            if xs:
                por_clase[c] = celda(xs, f"Tasa base sin fuga del mismo suceso (RI-TB) frente a {xs[0].get('referencia_indice') or 'el propio activo'}")
        g = celda(lst, "Tasa base sin fuga (RI-TB) de cada pronóstico")
        nota = (f"Ventana de {semanas} semanas; {g['n']} pronósticos de opciones publicadas resueltos"
                + (f"; {len(no_res)} no resolubles excluidos y declarados" if no_res else "")
                + (f"; {n_contaminados} con contaminación posible por el conocimiento del modelo excluidos y declarados"
                   if n_contaminados else "")
                + ("; muestra pequeña (< 30): la diferencia frente al azar puede deberse a la suerte" if g["n"] < 30 else ""))
        return {"ventana": f"{semanas} semanas", "global": g, "por_clase": por_clase, "nota": nota}

    # ------------------------------------------------------------------------------------
    # Certificados, lecciones y recalibración
    # ------------------------------------------------------------------------------------
    def estado_h5(self, as_of=None) -> dict[str, dict]:
        """V5.1 (12.1): estado de cada PRG H5 a partir de sus hitos resueltos y tasa de hitos cumplidos por celda tipo × H5.
        EN_CURSO_CONFORME: como mucho un hito fallado y no el último; DESVIADO: dos o más fallados o el último fallado;
        INVALIDADO: falla un hito marcado como necesario.
        PA-09: los hitos con `contaminacion_posible` (o los de un H5 que la tenga) cuentan para el estado de su PRG,
        pero no para la tasa de la celda ni, por tanto, para la degradación."""
        f4 = self.almacen.estado("F4", as_of)
        out: dict[str, dict] = {}
        celdas: dict[str, list[int]] = defaultdict(list)
        ids_celda: dict[str, list[str]] = defaultdict(list)
        excluidos: dict[str, int] = defaultdict(int)
        # Anexo A, «Degradación automática de H5 (12.2)» (Calibrable, P-42): tasa < 50 % con ≥ 20 hitos resueltos
        tasa_min = float(parametro(self.cfg, "evaluacion.degradacion_h5_tasa_min"))
        min_hitos = int(parametro(self.cfg, "evaluacion.degradacion_h5_min_hitos"))
        for p in f4.values():
            if p.get("horizonte") != "H5" or p.get("es_hito"):
                continue
            hitos = sorted((f4.get(h) or {} for h in p.get("hit_ids", [])), key=lambda x: str(x.get("fecha_resolucion")))
            res = [int(h["resolucion"]["resultado_binario"]) for h in hitos if h.get("estado") == "RESUELTO" and h.get("resolucion")]
            fallos = res.count(0)
            if any(h.get("necesario") and h.get("estado") == "RESUELTO" and not (h.get("resolucion") or {}).get("resultado_binario")
                   for h in hitos):
                est = "INVALIDADO"
            elif fallos >= 2 or (res and res[-1] == 0):
                est = "DESVIADO"
            else:
                est = "EN_CURSO_CONFORME"
            out[p["prg_id"]] = {"estado": est, "hitos_resueltos": len(res), "hitos_cumplidos": sum(res), "hitos_totales": len(hitos)}
            resueltos_h = [h for h in hitos if h.get("estado") == "RESUELTO" and h.get("resolucion")]
            admis = [h for h in resueltos_h if not (contaminacion_posible(p) or contaminacion_posible(h))]
            celdas[p["clase"]].extend(int(h["resolucion"]["resultado_binario"]) for h in admis)
            ids_celda[p["clase"]].extend(h["prg_id"] for h in admis)
            excluidos[p["clase"]] += len(resueltos_h) - len(admis)
        resumen = {c: {"n": len(v), "tasa_cumplidos": round(sum(v) / len(v), 4) if v else None,
                       "degradar": bool(len(v) >= min_hitos and sum(v) / len(v) < tasa_min),
                       "hitos_resueltos_ids": sorted(ids_celda[c]), "excluidos_contaminacion": excluidos[c]}
                   for c, v in celdas.items()}
        return {"pronosticos": out, "celdas": resumen, "umbral": {"tasa_min": tasa_min, "min_hitos": min_hitos}}

    def _matriz_aplicabilidad(self, as_of) -> dict[str, dict[str, str]]:
        """Matriz de aplicabilidad vigente (P-31): la de F10 si AG-20 ya la ajustó; si no, la tabla 8.3 de la configuración."""
        vig = (self.almacen.estado("F10", as_of).get("P-31") or {}).get("valor_vigente")
        return copy.deepcopy(vig or self._tabla_base)

    def aplicar_degradacion_h5(self, as_of, run_id: str | None = None) -> list[dict]:
        """12.2 y Anexo A (P-42): si la tasa de hitos cumplidos de una celda tipo × H5 queda bajo el umbral con muestra
        suficiente, su aplicabilidad baja un escalón. Se registra en F6 la lección (evidencia: los HIT- resueltos) y:
        - «Sí» → «Limitado»: ajuste AJU- en F6 y cambio CFG- de P-31 (y de P-30, versión menor nueva) en F10 (AG-20,
          régimen CALIBRABLE_RESTRINGIDO de P-31: «Sí» ↔ «Limitado» automático);
        - «Limitado» → «No»: propuesta de tipo 3 (P3-EVAL-) en F6, porque P-31 exige tipo 3 para todo cambio hacia o desde
          «No» (esquema F10, 4.4; R23: manda la regla más restrictiva). No se escribe en F10.
        Como mucho un escalón por celda y trimestre (esquema F10, regla 7), y nunca con una P3 de la celda pendiente.
        Volver a subir exige tipo 3 (12.2): este método nunca sube un escalón."""
        as_of = pd.Timestamp(as_of).normalize()
        est = self.estado_h5(as_of)
        trimestre = f"{as_of.year}-T{(as_of.month - 1) // 3 + 1}"
        hechos: list[dict] = []
        # T-65 (H-13): la degradación se aplica desde este mismo ciclo; T-92 (O3) compone con lo ya registrado para esa fecha
        fecha_efecto = str(as_of.date())
        for clase, celda in sorted(est["celdas"].items()):
            if not celda["degradar"]:
                continue
            f6 = list(self.almacen.estado("F6", as_of, clave="id").values())
            ambito = {"clase": clase, "horizonte": "H5"}
            if any(a.get("parametro") == "P-31" and a.get("celda") == ambito
                   and (a.get("trimestre") == trimestre or (a.get("tipo_entrada") == "P3" and a.get("estado") == "ENVIADA"))
                   for a in f6):
                continue
            # Componer con acuerdos ya registrados que entrarán en vigor el mismo día, sin abrir el corte de conocimiento.
            f10 = self.almacen.estado("F10", as_of, efectivo_el=fecha_efecto)
            matriz = (f10.get("P-31") or {}).get("valor_vigente") or self._tabla_base
            actual = (matriz.get(clase) or {}).get("H5")
            nuevo = ESCALON_INFERIOR.get(actual) if actual is not None else None
            if nuevo is None:          # ya «No» (o valor desconocido): nada que bajar
                continue
            n, tasa = celda["n"], celda["tasa_cumplidos"]
            umbral = est["umbral"]
            evidencia_ids = celda["hitos_resueltos_ids"]
            obs = (f"Tasa de hitos cumplidos de {clase}×H5 {tasa:.0%} con {n} hitos resueltos, por debajo del umbral "
                   f"{umbral['tasa_min']:.0%} (mínimo {umbral['min_hitos']} hitos; Anexo A, P-42).")
            rec = (f"Aplicabilidad de H5 en {clase}: «{actual}» → «{nuevo}». Prospectiva rebaja la banda y exige hitos más "
                   "verificables en esta celda; volver a subir exige un cambio de tipo 3.")
            lec = self._nueva_leccion(as_of, ambito, "PREDICTIVA", obs, rec, "estadistica", evidencia_ids, n)
            lec_id = lec["id"] if lec else next((l["id"] for l in f6 if l.get("tipo_entrada") == "LEC" and l.get("estado") == "VIGENTE"
                                                 and l.get("tipo") == "PREDICTIVA" and l.get("ambito") == ambito), None)
            evid = {"objetivo": "tasa de hitos cumplidos tipo × H5", "tasa_cumplidos": tasa, "n_hitos": n,
                    "umbral": umbral, "hitos": evidencia_ids, "lec_id": lec_id}
            if nuevo == "NO":
                p3 = {"tipo_entrada": "P3", "id": self.almacen.nuevo_id("P3-EVAL"), "objeto": f"P-31 aplicabilidad de H5 en {clase}",
                      "parametro": "P-31", "celda": ambito, "de": actual, "a": nuevo, "trimestre": trimestre,
                      "motivo": "cambio hacia o desde «No»", "evidencia": evid,
                      "impacto_esperado": f"H5 deja de ofrecerse en {clase}", "pruebas_regresion": ["PB-64"],
                      "plan_reversion": "cambio de tipo 3 que restituya «Limitado»", "estado": "ENVIADA"}
                self.almacen.escribir("F6", "AG-20", p3)
                hechos.append(p3)
                continue
            mv_de = str((f10.get("P-30") or {}).get("valor_vigente") or parametro(self.cfg, "methodology_version"))
            mv = {"de": mv_de, "a": _version_menor_siguiente(mv_de)}
            nueva = copy.deepcopy(matriz)
            nueva[clase]["H5"] = nuevo
            aju = {"tipo_entrada": "AJU", "id": self.almacen.nuevo_id("AJU"), "parametro": "P-31", "celda": ambito,
                   "de": actual, "a": nuevo, "trimestre": trimestre,
                   "banda": {"regla": "«Sí» ↔ «Limitado» automático (12.2, P-31); hacia «No», tipo 3"},
                   "evidencia": evid, "methodology_version": mv, "efecto_desde": fecha_efecto,
                   "sombra_hasta": None, "estado": "CONFIRMADO", "aplicado_en_produccion": True,
                   "nota": "degradación automática de 12.2: se aplica desde este mismo ciclo (la lectura de F10 es por fecha de "
                           "registro; T-65, H-13) y no se revierte sola (volver a subir exige tipo 3)"}
            self.almacen.escribir("F6", "AG-20", aju)
            comun = {"tipo_entrada": "CFG", "autor": "AG-20", "origen": aju["id"], "methodology_version": mv,
                     "fecha_registro": str(as_of.date()), "fecha_efecto": aju["efecto_desde"], "revierte_a": None}
            self.almacen.escribir("F10", "AG-20", {**comun, "cfg_id": self.almacen.nuevo_id("CFG"), "param_id": "P-31",
                                                   "de": matriz, "a": nueva, "valor_vigente": nueva,
                                                   "regimen": "CALIBRABLE_RESTRINGIDO", "motivo": obs})
            self.almacen.escribir("F10", "AG-20", {**comun, "cfg_id": self.almacen.nuevo_id("CFG"), "param_id": "P-30",
                                                   "de": mv["de"], "a": mv["a"], "valor_vigente": mv["a"], "regimen": "CALIBRABLE",
                                                   "motivo": f"ajuste {aju['id']} (P-31, {clase}×H5)"})
            hechos.append(aju)
        return hechos

    def certificados_vigentes(self, as_of=None) -> list[dict]:
        """Certificados VIGENTE (los únicos que habilitan probabilidades numéricas). Un PROPUESTO (PA-10) no lo es hasta
        su CERT_APROBACION."""
        return [c for c in self.almacen.estado("F6", as_of, clave="id").values()
                if c.get("tipo_entrada") in ("CERT", "CERT_REVOCACION", "CERT_APROBACION") and c.get("estado") == "VIGENTE"]

    def certificados_propuestos(self, as_of=None) -> list[dict]:
        """PA-10: certificados que pasan el criterio y esperan la aprobación del operador (CT-04)."""
        return [c for c in self.almacen.estado("F6", as_of, clave="id").values()
                if c.get("tipo_entrada") == "CERT" and c.get("estado") == "PROPUESTO"]

    def aprobar_certificados(self, ids, as_of, autor: str = "BROKER") -> list[dict]:
        """PA-10 (CT-04): el operador aprueba certificados PROPUESTO. Escribe en F6 una entrada CERT_APROBACION por id y
        el certificado queda VIGENTE. Valida todos los ids antes de escribir nada (falla cerrado: ValueError con el
        motivo y F6 sin cambios)."""
        if isinstance(ids, str) or not isinstance(ids, (list, tuple)):
            raise ValueError("aprobar_certificados: se espera una lista de identificadores CERT-")
        ids = list(ids)
        if not ids:
            raise ValueError("aprobar_certificados: la lista de certificados está vacía")
        if len(set(ids)) != len(ids):
            raise ValueError("aprobar_certificados: hay identificadores repetidos")
        if not isinstance(autor, str) or not autor.strip():
            raise ValueError("aprobar_certificados: falta el autor de la aprobación")
        as_of = pd.Timestamp(as_of).normalize()
        f6 = self.almacen.estado("F6", as_of, clave="id")
        vigentes = {(c["celda"]["clase"], c["celda"]["horizonte"], c["celda"].get("metodo")) for c in self.certificados_vigentes(as_of) if c.get("celda")}
        for i in ids:
            c = f6.get(i)
            if c is None or not any(h.get("tipo") == "CERT" for h in c.get("_historial", [])):
                raise ValueError(f"aprobar_certificados: no existe ningún certificado {i!r} en F6")
            if c.get("estado") != "PROPUESTO":
                raise ValueError(f"aprobar_certificados: {i} está {c.get('estado')}, no PROPUESTO")
            celda = c.get("celda") or {}
            if (celda.get("clase"), celda.get("horizonte"), celda.get("metodo")) in vigentes:
                raise ValueError(f"aprobar_certificados: la celda {celda.get('clase')}|{celda.get('horizonte')} de {i} ya "
                                 "tiene un certificado VIGENTE")
            vigentes.add((celda.get("clase"), celda.get("horizonte"), celda.get("metodo")))
        hechos = []
        for i in ids:
            e = {"tipo_entrada": "CERT_APROBACION", "id": i, "estado": "VIGENTE", "aprobado_por": autor.strip(),
                 "contrato": "CT-04", "fecha_aprobacion": str(as_of.date()), "estado_anterior": "PROPUESTO"}
            self.almacen.escribir("F6", "AG-20", e)
            hechos.append(e)
        return hechos

    def revisar_certificados(self, as_of, run_id: str | None = None) -> dict:
        """Certificados de horizonte (Anexo A). T-66: solo con PRG admisibles (PA-09); el mínimo de muestra se exige a
        n_eff (PA-03); con `aprendizaje.solo_endurecer` el certificado nace PROPUESTO (PA-10). Revocar un VIGENTE y
        retirar un PROPUESTO que ya no cumple el criterio endurecen: son automáticos."""
        n_cert = int(parametro(self.cfg, "evaluacion.min_certificar"))
        min_cong = self._min_conglomerados()
        solo_endurecer = self.solo_endurecer()
        celdas = defaultdict(list)
        for p in self.resueltos(as_of):
            celdas[(p["clase"], p["horizonte"], p.get("metodo"))].append(p)
        candidatas = {k: v for k, v in celdas.items() if len(v) >= n_cert}
        vigentes = {(c["celda"]["clase"], c["celda"]["horizonte"], c["celda"].get("metodo")): c for c in self.certificados_vigentes(as_of)}
        propuestos = {(c["celda"]["clase"], c["celda"]["horizonte"], c["celda"].get("metodo")): c for c in self.certificados_propuestos(as_of)}
        emitidos, revocados, retirados, evaluadas = [], [], [], {}
        if candidatas:
            metr = {k: ev.evaluar_celda([float(x["prob_interna"]) for x in v], [int(x["resolucion"]["resultado_binario"]) for x in v],
                                        [float(x["referencia_ingenua"]["valor_o_prob"]) for x in v],
                                        float(np.mean([x["referencia_ingenua"]["valor_o_prob"] for x in v])),
                                        int(parametro(self.cfg, "evaluacion.bootstrap_replicas")), int(parametro(self.cfg, "evaluacion.simulaciones_ece")),
                                        fechas=self._fechas_conglomerado(v), min_conglomerados=min_cong)
                    for k, v in candidatas.items()}
            # Holm escalonado (Anexo A, certificado R13): en cuanto una celda no supera su umbral, ninguna de las
            # siguientes (de p mayor) lo supera. α: clave evaluacion.alfa_holm (0,10, coherente con el IC 90 % del criterio)
            umbrales = ev.holm({etiqueta_celda(k): (m["dm_hln"]["p_unilateral"] if m["dm_hln"]["p_unilateral"] is not None else 1.0)
                                for k, m in metr.items()}, float(parametro(self.cfg, "evaluacion.alfa_holm")))
            for k, m in metr.items():
                crit = ev.criterio_certificado(m, n_cert, float(parametro(self.cfg, "evaluacion.ece_max")),
                                               umbrales[etiqueta_celda(k)] if len(metr) > 1 else None)
                evaluadas[etiqueta_celda(k)] = crit
                if crit["certificable"] and k not in vigentes and k not in propuestos:
                    muestra = m.get("muestra_efectiva") or {}
                    cert = {"tipo_entrada": "CERT", "id": self.almacen.nuevo_id("CERT"),
                            "estado": "PROPUESTO" if solo_endurecer else "VIGENTE",
                            "celda": {"clase": k[0], "horizonte": k[1], "metodo": k[2]}, "n": m["n"], "n_eff": m["n_eff"],
                            "muestra_efectiva": {c: muestra.get(c) for c in ("conglomerados", "m_medio", "rho", "efecto_diseno")},
                            "brier": m["brier"], "brier_ref": m["brier_ref"], "bss": m["bss"]["valor"], "bss_ic90": m["bss"]["ic"],
                            "bss_ic_metodo": m["bss"].get("metodo"),
                            "holm_superado": True, "ece": m["calibracion"]["ece"], "ece_nulo_q90": m["ece_nulo"]["q90"],
                            "methodology_version": parametro(self.cfg, "methodology_version"), "emitido": str(pd.Timestamp(as_of).date())}
                    if solo_endurecer:
                        cert["pendiente"] = ("aprobación del operador por CT-04 (aprobar_certificados); hasta entonces no "
                                             "habilita probabilidades numéricas (PA-10, aprendizaje.solo_endurecer)")
                    self.almacen.escribir("F6", "AG-20", cert)
                    emitidos.append(cert)
                elif k in propuestos and not crit["certificable"]:
                    c = propuestos[k]
                    self.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT_REVOCACION", "id": c["id"], "estado": "REVOCADO",
                                                          "motivo_cambio": "propuesta retirada: la celda ya no cumple el criterio ("
                                                          + "; ".join(crit["motivos"]) + ")",
                                                          "fecha": str(pd.Timestamp(as_of).date())})
                    retirados.append(c["id"])
                elif k in vigentes:
                    bssv = m["bss"]["valor"]
                    ece_m = m["calibracion"]["ece"]
                    # Umbral de revocación por deterioro: clave evaluacion.ece_revocacion (0,12; no figura en el Anexo A)
                    ece_rev = float(parametro(self.cfg, "evaluacion.ece_revocacion"))
                    # ECE = 0 es calibración perfecta (no revoca); ECE ausente no permite comprobar la calibración: revoca
                    if (bssv is not None and bssv <= 0) or ece_m is None or ece_m >= ece_rev:
                        c = vigentes[k]
                        self.almacen.escribir("F6", "AG-20", {"tipo_entrada": "CERT_REVOCACION", "id": c["id"], "estado": "REVOCADO",
                                                              "motivo_cambio": f"deterioro: BSS ≤ 0, ECE no disponible o ECE ≥ {ece_rev}",
                                                              "fecha": str(pd.Timestamp(as_of).date())})
                        revocados.append(c["id"])
        no_cert = {etiqueta_celda(k): f"n = {len(v)} < {n_cert}" for k, v in celdas.items() if k not in candidatas}
        return {"emitidos": emitidos, "revocados": revocados, "propuestas_retiradas": retirados, "evaluadas": evaluadas,
                "insuficientes": no_cert, "excluidos_contaminacion": self.excluidos_contaminacion(as_of)}

    def lecciones_vigentes(self, as_of, clase: str | None = None, max_n: int | None = None) -> list[dict]:
        """Lecciones vigentes del tipo, las de más fuerza primero. T-120: el máximo por encargo (12.3 del Documento 0) sale
        de la configuración (`aprendizaje.lecciones_por_encargo`), no de un literal."""
        if max_n is None:
            max_n = int(parametro(self.cfg, "aprendizaje.lecciones_por_encargo"))
        orden = {"estadistica": 0, "recurrente": 1, "anecdotica": 2}
        lst = []
        for l in self.almacen.estado("F6", as_of, clave="id").values():
            if l.get("tipo_entrada") != "LEC" or l.get("estado") != "VIGENTE":
                continue
            if pd.Timestamp(l["caducidad"]) < pd.Timestamp(as_of):
                continue
            amb = l.get("ambito") or {}
            if clase and amb.get("clase") not in (None, clase):
                continue
            lst.append(l)
        lst.sort(key=lambda l: (orden.get(l["fuerza"], 3), l["id"]))
        return [{k: l.get(k) for k in ("id", "ambito", "tipo", "observacion", "recomendacion", "fuerza", "fecha")} for l in lst[:max_n]]

    def _nueva_leccion(self, as_of, ambito: dict, tipo: str, obs: str, rec: str, fuerza: str, evidencia: list[str], n: int,
                       origen: str = "DETERMINISTA") -> dict | None:
        for l in self.almacen.estado("F6", as_of, clave="id").values():
            if l.get("tipo_entrada") == "LEC" and l.get("estado") == "VIGENTE" and l.get("tipo") == tipo \
                    and l.get("ambito") == ambito and pd.Timestamp(l["caducidad"]) >= pd.Timestamp(as_of):
                return None
        cad = pd.Timestamp(as_of) + pd.DateOffset(months=CADUCIDAD_MESES.get(fuerza, 3))
        lec = {"tipo_entrada": "LEC", "id": self.almacen.nuevo_id("LEC"), "fecha": str(pd.Timestamp(as_of).date()), "ambito": ambito,
               "nivel": "B" if tipo in ("PREDICTIVA", "CALIBRACION") else "A", "tipo": tipo, "observacion": obs, "evidencia": evidencia,
               "recomendacion": rec, "fuerza": fuerza, "n": n, "caducidad": str(cad.date()), "estado": "VIGENTE", "origen": origen}
        self.almacen.escribir("F6", "AG-20", lec)
        return lec

    def extraer_lecciones(self, as_of, metricas: dict) -> list[dict]:
        nuevas = []
        for celda, m in metricas.items():
            c, h = celda.split("|")
            n = m["n"]
            if n < 10:
                continue
            tasa = (m.get("acierto") or {}).get("tasa")
            fuerza = "estadistica" if n >= int(parametro(self.cfg, "evaluacion.min_calibrar")) else "recurrente"
            if tasa is not None and tasa < 0.45:
                l = self._nueva_leccion(as_of, {"clase": c, "horizonte": h}, "PREDICTIVA",
                                        f"Acierto {tasa:.0%} en {n} pronósticos de {c}×{h}, por debajo de la tasa base.",
                                        "Rebajar un nivel la banda verbal y exigir catalizador fechado antes de proponer en esta celda.",
                                        fuerza, [f"MET:{celda}"], n)
                if l:
                    nuevas.append(l)
            cg = m.get("calibracion_global") or {}
            if cg and cg.get("p_media") is not None and cg["p_media"] - cg["frecuencia"] >= 0.10:
                l = self._nueva_leccion(as_of, {"clase": c, "horizonte": h}, "CALIBRACION",
                                        f"Sobreconfianza en {c}×{h}: probabilidad media {cg['p_media']:.2f} frente a frecuencia {cg['frecuencia']:.2f} (n = {n}).",
                                        "Acercar la probabilidad interna a la tasa base (máximo 0,60) hasta que la calibración mejore.",
                                        fuerza, [f"MET:{celda}"], n)
                if l:
                    nuevas.append(l)
        return nuevas

    def leccion_producto(self, as_of, tema: str, qry_ids: list[str]) -> dict | None:
        return self._nueva_leccion(as_of, {"clase": None, "horizonte": None, "agente": ["AG-17", "AG-02"]}, "PRODUCTO",
                                   f"La pregunta «{tema}» se ha repetido {len(qry_ids)} veces en 4 semanas.",
                                   "Incorporar esa información al informe por defecto (sección de lectura del conjunto).",
                                   "recurrente", qry_ids, len(qry_ids))

    def recalibrar(self, as_of, run_id: str | None = None) -> dict | None:
        """Propuesta de ajuste de pesos de RK dentro de bandas (modo sombra) a partir de la capacidad
        ordenadora (IC de Spearman) de A y E frente al resultado de las opciones publicadas."""
        res = self.resueltos(as_of, solo_informe=True)
        n_min = int(parametro(self.cfg, "evaluacion.min_calibrar"))
        if len(res) < n_min:
            return None
        f6 = self.almacen.estado("F6", as_of, clave="id").values()
        if any(a.get("tipo_entrada") == "AJU" and a.get("estado") == "EN_SOMBRA" for a in f6):
            return None
        A = [x.get("puntuaciones_opcion", {}).get("A") for x in res]
        E = [x.get("puntuaciones_opcion", {}).get("E") for x in res]
        y = [x["resolucion"]["valor_observado"] * (1 if x["sentido"] == "POSITIVO" else -1) for x in res]
        if any(v is None for v in A + E) or len(set(A)) < 2 or len(set(E)) < 2:
            return None
        ic_a = float(stats.spearmanr(A, y).statistic)
        ic_e = float(stats.spearmanr(E, y).statistic)
        rr = parametro(self.cfg, "evaluacion.recalibracion_rk")   # Anexo A, P-11 (T-65, CS-10 de T-53)
        if abs(ic_a - ic_e) <= float(rr["dif_ic_min"]):
            return None
        sube, baja = ("A", "E") if ic_a > ic_e else ("E", "A")
        trimestre = f"{pd.Timestamp(as_of).year}-T{(pd.Timestamp(as_of).month - 1) // 3 + 1}"
        acumulado = sum(abs(a.get("delta", 0)) for a in f6 if a.get("tipo_entrada") == "AJU" and a.get("parametro") == "P-11"
                        and a.get("estado") in ("EN_SOMBRA", "CONFIRMADO"))
        trimestral = sum(abs(a.get("delta", 0)) for a in f6 if a.get("tipo_entrada") == "AJU" and a.get("parametro") == "P-11"
                         and a.get("trimestre") == trimestre)
        delta, b_trim, b_tot = float(rr["paso"]), float(rr["banda_trimestral"]), float(rr["banda_total"])
        if trimestral + delta > b_trim + 1e-9 or acumulado + delta > b_tot + 1e-9:
            p3 = {"tipo_entrada": "P3", "id": self.almacen.nuevo_id("P3-EVAL"), "objeto": "P-11 pesos de RK",
                  "motivo": "fuera de banda", "evidencia": {"ic_A": ic_a, "ic_E": ic_e, "n": len(res)},
                  "impacto_esperado": f"Mayor peso de {sube}", "pruebas_regresion": ["PB-35", "PB-36"], "estado": "ENVIADA"}
            self.almacen.escribir("F6", "AG-20", p3)
            return p3
        pesos = dict(parametros_ht03(self.cfg)["pesos_rk"])
        nuevos = dict(pesos)
        nuevos[sube] = round(nuevos[sube] + delta, 4)
        nuevos[baja] = round(nuevos[baja] - delta, 4)
        aju = {"tipo_entrada": "AJU", "id": self.almacen.nuevo_id("AJU"), "parametro": "P-11", "de": pesos, "a": nuevos,
               "delta": delta, "trimestre": trimestre, "banda": {"trimestral": b_trim, "total": b_tot}, "acumulado_vs_inicial": acumulado + delta,
               "evidencia": {"objetivo": "capacidad ordenadora de RK", "ic_A": ic_a, "ic_E": ic_e, "n": len(res)},
               "methodology_version": {"de": parametro(self.cfg, "methodology_version"), "a": _version_menor_siguiente(parametro(self.cfg, "methodology_version"))},
               "efecto_desde": str(pd.Timestamp(as_of).date()), "sombra_hasta": str((pd.Timestamp(as_of) + pd.DateOffset(months=int(rr["meses_sombra"]))).date()),
               "estado": "EN_SOMBRA", "aplicado_en_produccion": bool(parametro(self.cfg, "evaluacion.aplicar_recalibracion")),
               "propuesta": False}
        if self.solo_endurecer():
            # PA-10: la recalibración de pesos nunca pasa sola a producción, aunque evaluacion.aplicar_recalibracion sea true
            aju.update({"aplicado_en_produccion": False, "propuesta": True,
                        "nota": "aprendizaje.solo_endurecer: propuesta de recalibración; solo pasa a producción con la "
                                "aprobación del operador"})
        self.almacen.escribir("F6", "AG-20", aju)
        return aju

    def ajuste_en_sombra(self, as_of) -> dict | None:
        for a in self.almacen.estado("F6", as_of, clave="id").values():
            if a.get("tipo_entrada") == "AJU" and a.get("estado") == "EN_SOMBRA":
                return a
        return None

    def ciclo(self, as_of, run_id: str | None = None) -> dict:
        """C5: resolución de vencidos, métricas, certificados, lecciones y recalibración (nunca bloquea C1–C3)."""
        resueltos = self.resolver(as_of, run_id)
        metr = self.metricas(as_of)
        excl = self.excluidos_contaminacion(as_of)
        if metr or excl["total"]:
            self.almacen.escribir("F6", "AG-20", {"tipo_entrada": "MET", "id": f"MET-{pd.Timestamp(as_of).date()}",
                                                  "ventana": f"hasta {pd.Timestamp(as_of).date()}", "metricas": metr,
                                                  "excluidos_contaminacion": excl,
                                                  "comprobacion_fuga": "SUPERADA", "madurez": "implementado"})
        certs = self.revisar_certificados(as_of, run_id)
        lecciones = self.extraer_lecciones(as_of, metr)
        aju = self.recalibrar(as_of, run_id)
        degradacion_h5 = self.aplicar_degradacion_h5(as_of, run_id)
        return {"resueltos": len([r for r in resueltos if r["estado"] == "RESUELTO"]),
                "no_resolubles": len([r for r in resueltos if r["estado"] == "NO_RESOLUBLE"]),
                "metricas": metr, "certificados": certs, "lecciones_nuevas": lecciones, "ajuste": aju,
                "degradacion_h5": degradacion_h5, "excluidos_contaminacion": excl}
