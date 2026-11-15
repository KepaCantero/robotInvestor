"""Estima el coste en USD de un ciclo del Bloque A con la API real, sin gastar nada (T-129).

Lee el `llamadas.json` que deja `medir_consumo_a.py` (una fila por llamada del cliente simulado) y le aplica una tarifa
(`bloque_a/11_Ejecutor/config/precios_anthropic.yaml` u otra con las mismas claves). Da tres cifras:
- **suelo:** la entrada que mide el simulador (prompts de sistema y encargos, con su caché) y la salida simulada, que es
  mucho más corta que la de un modelo y no lleva el razonamiento adaptativo, que se cobra como salida. No es un valor
  central: el coste real queda por encima (T-136, H-02);
- **peor caso de las llamadas medidas** (T-136, H-01, y T-140): la entrada multiplicada por `factor_tokens_cota` y pagada
  entera como escritura de caché, toda la salida hasta `max_tokens` (que incluye el razonamiento), cada intento (el
  original y cada reparación de JSON, `llm.reintento_reparacion`) y cada continuación de `pause_turn` de los agentes con
  búsqueda como una petición que reenvía lo ya generado y paga su `max_tokens` y sus búsquedas. **No es una cota del
  ciclo** (T-145, QA r01 de T-140, H-01): solo mira las llamadas que hizo el cliente simulado;
- **cota superior del ciclo** (T-145): la menor de dos cotas, cada una con sus supuestos (`SUPUESTOS`):
  · *por llamadas:* las llamadas que el código de un ciclo C1 de la V5 puede hacer como mucho (`LLAMADAS_POR_TIPO` y
    `LLAMADAS_DEL_CICLO`, sacadas de `orquestacion.py`: también las que dependen de la respuesta del modelo, como las
    peticiones de conocimiento, la contrarréplica, la reescritura de AG-17 o el segundo dictamen G3), cada una en su peor
    caso, y en el encargo de los agentes que leen lo que escriben otros, además, la salida máxima de esos otros;
  · *por presupuesto:* el presupuesto en UC del ciclo con la ampliación máxima, al peor precio por UC de los agentes de
    cada bolsa. Con T-146 (por defecto) es solo eso: cada petición reserva su peor caso antes de salir y todo (AG-18,
    AG-19, AG-20 y las búsquedas incluidos) pasa por el presupuesto. Con `--sin-t146`, la de antes de T-146, más lo que
    aquel presupuesto dejaba pasar: la última llamada de cada bolsa, la escritura de caché cargada como lectura hasta
    `liquidar_primas`, las llamadas fuera del presupuesto (AG-18, AG-19 y AG-20) y las búsquedas, que no contaban en UC.
  Lo que se lee en una búsqueda se cobra como entrada y no se puede saber sin la API: queda fuera de las dos cotas, también
  con T-146 (T-148 r02, QA r01 de T-148, H-01: la reserva de T-146 no lo cubre mientras
  `presupuesto_uc.reserva.tokens_lectura_por_busqueda` sea 0), y la salida da su peso en la cota que manda; también queda
  fuera lo que la entrada real pase del margen de S1 (`factor_tokens_cota`, el mismo 1,35 de la reserva).

Uso (desde la raíz):
  .venv/bin/python .docs/scripts/estimar_coste_ciclo_a.py <carpeta de medir_consumo_a> [--precios yaml] [--config yaml]
`--config` es la misma configuración adicional que se pasó a `medir_consumo_a.py` (los tipos activos, los agentes con
búsqueda, las reparaciones, los presupuestos…).
"""
import argparse
import collections
import json
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
EJECUTOR = RAIZ / "bloque_a" / "11_Ejecutor"


def _config(extra: str | None) -> dict:
    sys.path.insert(0, str(EJECUTOR))
    from bloque_a.configuracion import cargar_config
    return cargar_config(extra)


def _coste(p: dict, entrada: float, salida: float, escr: float, lect: float) -> float:
    return (entrada * p["entrada"] + salida * p["salida"] + escr * p["escritura_cache"] + lect * p["lectura_cache"]) / 1e6


def estimar(llamadas: list[dict], precios: dict, precio_busqueda_mil: float, agentes_busqueda: set[str],
            max_usos: int, factor_tokens: float = 1.0, continuaciones: int = 0, reparaciones: int = 0) -> dict:
    tot = {"estimacion": 0.0, "cota_superior": 0.0, "busquedas_cota": 0}
    por_modelo: dict[str, dict] = collections.defaultdict(lambda: {"llamadas": 0, "estimacion": 0.0, "cota_superior": 0.0})
    for x in llamadas:
        p = precios.get(x["modelo"])
        if p is None or any(p.get(k) is None for k in ("entrada", "salida", "escritura_cache", "lectura_cache")):
            raise SystemExit(f"sin tarifa para {x['modelo']}: añádala al fichero de precios")
        escr, lect = x.get("cache_escr", 0), x.get("cache_lect", 0)
        entrada = max(0, x["sys_tok"] + x["user_tok"] - escr - lect)      # lo que no sale de la caché ni se escribe en ella
        est = _coste(p, entrada, x["out_tok"], escr, lect)
        entrada_cota = (x["sys_tok"] + x["user_tok"]) * factor_tokens     # toda como escritura de caché, sin lecturas
        vueltas = 1 + (continuaciones if x["agente"] in agentes_busqueda else 0)
        # T-140 (QA r01 de T-136, H-01): cada intento (el original y cada reparación de JSON) y cada continuación de
        # `pause_turn` es una petición nueva: reenvía la entrada y lo ya generado, puede gastar todo su `max_tokens` y,
        # en un agente con búsqueda, hacer sus búsquedas
        cota = 0.0
        for r in range(1 + reparaciones):
            for v in range(vueltas):
                cota += _coste(p, 0, x["max_tokens"], entrada_cota + (r * vueltas + v) * x["max_tokens"], 0)
                if x["agente"] in agentes_busqueda:
                    tot["busquedas_cota"] += max_usos
                    cota += max_usos * precio_busqueda_mil / 1000
        tot["estimacion"] += est
        tot["cota_superior"] += cota
        m = por_modelo[x["modelo"]]
        m["llamadas"] += 1
        m["estimacion"] += est
        m["cota_superior"] += cota
    tot["llamadas"] = len(llamadas)
    tot["por_modelo"] = dict(sorted(por_modelo.items()))
    return tot


# --------------------------------------------------------------------------------------------------------------------
# T-145 (QA r01 de T-140, H-01) · cota del ciclo
# --------------------------------------------------------------------------------------------------------------------
# Llamadas que puede hacer como mucho un ciclo periódico C1 de la V5 (`orquestacion.Bloque.ciclo`). Por cada tipo de
# activo, en orden: (papel, agentes posibles, máximo por tipo (un número o la clave de la configuración), con búsqueda).
# «ANALISTA» es el Analista del tipo. Con nivel N1 hay menos (sin refutación ni curación): la tabla es la de N2.
LLAMADAS_POR_TIPO = (
    ("cribado", ("ANALISTA",), 1, False),                       # _analizar_clase: CT-06
    ("peticion_conocimiento", ("AG-14", "AG-16"), "seleccion.peticiones_conocimiento_por_clase", True),   # CT-07/CT-08
    ("prospectiva", ("AG-10",), 1, False),                      # _prospectiva: CT-12, si hay finalistas
    ("refutacion", ("AG-11",), 1, False),                       # _refutacion: CT-13
    ("respuesta_objeciones", ("ANALISTA",), 1, False),          # CT-06, si hay objeciones fuertes o moderadas
    ("contrarreplica", ("AG-11",), 1, False),                   # CT-13, si el Analista da una fuerte por resuelta
    ("curacion", ("AG-12",), 1, False),                         # _registrar_evidencia_clase: CT-11
)
# Una vez por ciclo, en orden: (papel, agente, máximo, bolsa del presupuesto o None si no pasa por él, salidas que puede
# llevar su encargo: los papeles de los tipos que lee, o «*», todas las anteriores). None es el código de antes de T-146
# (`--sin-t146`): con T-146 (por defecto), AG-20, AG-18 y AG-19 pagan de la COMÚN, como en `orquestacion.py`, y `cota_ciclo`
# los pone ahí (T-148 r02, QA r01 de T-148, H-03)
LLAMADAS_DEL_CICLO = (
    ("informe_aprendizaje", "AG-20", 1, None, ()),              # _informe_aprendizaje (C5), antes del análisis: métricas
    ("integracion", "AG-02", 1, "COMUN", ("cribado",)),         # _integrar: régimen, nombres y lagunas de cada Analista
    ("dictamen_g3", "AG-18", 2, None, "*"),                     # _validar_g3: hasta dos intentos, con las incidencias de HT-09
    ("redaccion", "AG-17", 2, "COMUN", "*"),                    # _redactar: la redacción y la reescritura por C12
    ("auditoria", "AG-19", 1, None, "*"),                       # _auditar: CT-17
)
# Mensaje de una reparación de JSON (`agentes.Agentes.invocar`): hasta 15 errores de hasta 300 caracteres y el texto fijo
ERRORES_REPARACION, CARACTERES_POR_ERROR, CARACTERES_FIJOS_REPARACION = 15, 300, 120
# T-148 (QA r01 de T-145, H-01): papeles cuyo encargo copia, por cada objeción, datos de las llamadas anteriores
# (`Bloque._refutacion`): la respuesta a objeciones lleva en cada objeción pendiente su argumento, las dimensiones E de la
# opción y la lista de su evidencia citable; la contrarréplica, en cada objeción fuerte dada por resuelta, el contenido de
# cada evidencia citada (`_contenido_evidencia`), que puede citarse varias veces. Su encargo crece con objeciones ×
# evidencias y solo lo acota la reserva del presupuesto (S4b)
MULTIPLICAN_ENCARGO = ("respuesta_objeciones", "contrarreplica")
# Desde T-146 (`consumo.ReservaLlamada`), una petición con bolsa solo sale si su peor caso cabe en lo que queda de la bolsa:
# toda su entrada (system, mensajes y herramientas, a 3,6 caracteres por token) por `presupuesto_uc.reserva.
# factor_tokens_entrada` y, como poco, `presupuesto_uc.reserva.salida_minima_tokens` de salida. `tests/test_t148.py`
# comprueba contra `ReservaLlamada` que el tope del encargo es ese (integración de T-148 con T-146, 15-11-2026). Desde la r02
# de T-146 la reserva suma además `presupuesto_uc.reserva.tokens_lectura_por_busqueda` por búsqueda posible (hoy 0): con un
# valor mayor, el encargo que cabe en una llamada con búsqueda es menor, así que este tope sigue siendo una cota por encima
SUPUESTOS = (
    "S1 · tokens: como mucho `factor_tokens_cota` veces los que aproxima el simulador (3,6 caracteres por token)",
    ("S2 · cada petición, en su peor caso: toda la entrada como escritura de caché, `max_tokens` de salida y `max_usos` "
    "búsquedas; cada reparación reenvía lo generado y el mensaje de errores; cada continuación de `pause_turn`, lo generado"),
    "S3 · el número de llamadas, el de las tablas `LLAMADAS_POR_TIPO` y `LLAMADAS_DEL_CICLO` (ciclo C1 de la V5, nivel N2)",
    ("S4 · el encargo de cada llamada: lo que mide el ciclo simulado para ese agente (el mayor de los medidos si no se llamó) "
    "más la salida máxima de cada llamada anterior que puede leer (las de su tipo; en las del ciclo, las de su columna "
    "«lee» de `LLAMADAS_DEL_CICLO`), copiada una vez; salvo en la respuesta a objeciones y la contrarréplica (S4b)"),
    ("S4b · (T-148) la respuesta a objeciones y la contrarréplica copian datos anteriores por cada objeción (la "
    "contrarréplica, el contenido de cada evidencia citada): su encargo crece con objeciones × evidencias y se toma el "
    "mayor que admite la reserva del presupuesto de su bolsa (T-146: la entrada con el margen y la salida mínima ≤ el "
    "límite de la bolsa con la ampliación máxima), sumado a lo medido; en toda llamada con bolsa, el encargo es como mucho ese, aunque S4 dé más"),
    ("S5 · fuera: lo que lee cada búsqueda (se cobra como entrada en su petición y en cada continuación de `pause_turn` "
    "que la reenvía; la salida da su peso por cada 1 000 tokens leídos), lo que añade la API por la herramienta, los "
    "reintentos del SDK, la tarifa de contexto largo (los 5.5 de Opus y Sonnet no la tienen; Haiku 5.5, por encima de "
    "100 000 tokens, sí, y su único papel, la curación, se queda por debajo con S4) y lo que el encargo trae de ciclos "
    "anteriores (opciones vigentes) más allá de lo medido desde un estado vacío"),
)


def _uc(cfg: dict) -> tuple[float, float, float]:
    from bloque_a.configuracion import parametro
    return (float(parametro(cfg, "uc.tokens_entrada_por_uc")), float(parametro(cfg, "uc.tokens_salida_por_uc")),
            float(parametro(cfg, "uc.factor_lectura_cache")))


def _usd_por_uc(p: dict, uc: tuple[float, float, float]) -> float:
    """USD que cuesta como mucho una UC: `Contabilidad.uc_de` = 0,5·entrada/T_e + 0,5·salida/T_s, así que una UC es
    2·T_e tokens de entrada (al precio más alto: escritura de caché) o 2·T_s de salida; la lectura de caché, que cuenta
    `factor_lectura_cache`, es más barata por UC en las tarifas de la API."""
    return max(2 * uc[0] * max(p["entrada"], p["escritura_cache"]), 2 * uc[1] * p["salida"],
               2 * uc[0] * p["lectura_cache"] / uc[2]) / 1e6


def peor_llamada(p: dict, sys_tok: float, user_tok: float, max_tokens: int, web: bool, reparaciones: int,
                 continuaciones: int, factor: float, max_usos: int, precio_busqueda_mil: float,
                 uc: tuple[float, float, float], tok_reparacion: float = 0.0) -> dict:
    """Peor caso de una llamada (S2): USD, UC, peticiones, búsquedas y la prima de caché que el presupuesto carga como
    lectura hasta `liquidar_primas` (la escritura cabe en el prefijo con `cache_control`, el prompt de sistema).
    En la reparación `r`, `agentes.invocar` reenvía el texto de la última petición de cada intento anterior y su mensaje
    de errores; en la continuación `v`, `AnthropicClient.generar` reenvía las `v` respuestas pausadas de ese intento (lo
    que traen de la búsqueda queda fuera, S5). Cada respuesta escribe como mucho `max_tokens`."""
    vueltas = 1 + (continuaciones if web else 0)
    r_ = {"usd": 0.0, "uc": 0.0, "peticiones": 0, "busquedas": 0, "prima_uc": 0.0}
    for r in range(1 + reparaciones):
        for v in range(vueltas):
            entrada = (sys_tok + user_tok) * factor + (r + v) * max_tokens + r * tok_reparacion
            r_["usd"] += _coste(p, 0, max_tokens, entrada, 0)
            r_["uc"] += 0.5 * entrada / uc[0] + 0.5 * max_tokens / uc[1]
            r_["prima_uc"] += 0.5 * sys_tok * factor * (1 - uc[2]) / uc[0]
            r_["peticiones"] += 1
            if web:
                r_["busquedas"] += max_usos
                r_["usd"] += max_usos * precio_busqueda_mil / 1000
    return r_


def _sistema_del_catalogo(cfg: dict, agente: str) -> int:
    from bloque_a.llm import _tokens_aprox
    from bloque_a.prompts import CatalogoPrompts
    return _tokens_aprox("".join(b["text"] for b in CatalogoPrompts(cfg).system(agente, cache=False)))


def cota_ciclo(llamadas: list[dict], cfg: dict, precios: dict, precio_busqueda_mil: float, factor_tokens: float,
               sistema=None, tipos: list[str] | None = None, con_t146: bool = True) -> dict:
    """Cota superior del coste de un ciclo C1 (T-145): la menor de la cota por llamadas y la cota por presupuesto, con los
    supuestos de `SUPUESTOS`. `sistema(agente)` da los tokens del prompt de sistema de un agente que no se llamó en el
    ciclo medido (por defecto, el del catálogo). `tipos` son los tipos de activo que analiza el ciclo (T-148, QA r01 de
    T-145, H-03: los de F10, P-02, si el estado ya existe; por defecto, `perfiles_activos`, que es lo que F10 toma al
    nacer). Falla cerrado si el diseño no es el V5, si un tipo no es de los doce o si el ciclo medido hizo una llamada
    que las tablas no prevén.

    `con_t146` (T-148, aviso de la coordinación del 15-11-2026; por defecto desde que T-146 está en el código): con T-146, el presupuesto en UC reserva el peor
    caso antes de cada petición (entrada con el margen como escritura de caché, `max_tokens` de salida y las búsquedas al
    máximo, que cuentan en UC), AG-18, AG-19 y AG-20 pagan de la bolsa común y la suma del ciclo no pasa del tope con la
    ampliación máxima. Entonces todo lo gastado pasa por el presupuesto y ninguna bolsa supera su límite por lo que la
    reserva cubre: la cota por presupuesto es solo `limites` (sin la última llamada de cada bolsa, la caché cargada como
    lectura, lo de fuera del presupuesto ni las búsquedas aparte), salvo lo que lee cada búsqueda y lo que la entrada pase
    del margen (T-148 r02, QA r01 de T-148, H-01): eso no se reserva y puede dejar una bolsa por encima de su límite en la
    petición que lo cruza (después no sale ninguna más). Su peso por cada 1 000 tokens leídos por búsqueda es, en la cota
    por presupuesto, la lectura de una petición en cada bolsa con búsqueda (`max_usos` búsquedas en cada vuelta de
    `pause_turn`, que reenvía las anteriores), aunque `presupuesto_uc.reserva.tokens_lectura_por_busqueda` reserve una
    parte (se dice en la salida). El precio por UC de cada bolsa incluye entonces el de una búsqueda si la
    configuración da sus UC (`uc.uc_por_busqueda_web`, la clave de T-146; si no está, no se añade). Con
    `con_t146=False`, la cota más holgada que valía antes de T-146, cuando el presupuesto no cortaba antes de cada
    petición: se mantiene para comparar y sigue siendo una cota superior."""
    from bloque_a.configuracion import (
        max_tokens_de,
        modelo_de,
        parametro,
        perfiles_activos,
    )
    from bloque_a.contratos import AGENTE_CLASE
    if (cfg.get("diseno") or "v5") != "v5":
        raise SystemExit("la cota por llamadas está hecha para el diseño V5 (`diseno: v5`); la V6 tiene otras llamadas")
    sistema = sistema or (lambda a: _sistema_del_catalogo(cfg, a))
    tipos = list(perfiles_activos(cfg)) if tipos is None else list(tipos)
    if not tipos or any(c not in AGENTE_CLASE for c in tipos) or len(set(tipos)) < len(tipos):
        raise SystemExit(f"tipos de activo no válidos para la cota: {tipos}")
    reparaciones = int(parametro(cfg, "llm.reintento_reparacion"))
    continuaciones = int(parametro(cfg, "llm.max_continuaciones_pause_turn"))
    bw = cfg.get("busqueda_web") or {}
    con_busqueda = set(bw.get("agentes") or []) if bw.get("habilitada_en_vivo") else set()
    max_usos = int(parametro(cfg, "busqueda_web.max_usos_por_llamada")) if con_busqueda else 0
    uc = _uc(cfg)
    tok_rep = (ERRORES_REPARACION * (CARACTERES_POR_ERROR + 3) + CARACTERES_FIJOS_REPARACION) / 3.6

    def maximo(n):
        return int(parametro(cfg, n)) if isinstance(n, str) else int(n)

    # S3: el ciclo medido no puede haber hecho más llamadas de un agente que las que prevén las tablas
    previstas: collections.Counter = collections.Counter()
    for c in tipos:
        for _papel, agentes, n, _web in LLAMADAS_POR_TIPO:
            for a in agentes:
                previstas[AGENTE_CLASE[c] if a == "ANALISTA" else a] += maximo(n)
    for _papel, a, n, _bolsa, _lee in LLAMADAS_DEL_CICLO:
        previstas[a] += n
    medidas = collections.Counter(x["agente"] for x in llamadas)
    fuera = sorted(a for a, k in medidas.items() if k > previstas.get(a, 0))
    if fuera:
        raise SystemExit(f"el ciclo medido llama más veces de las previstas a {', '.join(fuera)}: revise LLAMADAS_POR_TIPO")
    user_max = max((x["user_tok"] for x in llamadas), default=0)

    def encargo(a):
        return max((x["user_tok"] for x in llamadas if x["agente"] == a), default=user_max)

    def sistema_de(a):
        return max([x["sys_tok"] for x in llamadas if x["agente"] == a] + [sistema(a)])

    def precio(a):
        m = modelo_de(cfg, a)
        p = precios.get(m)
        if p is None or any(p.get(k) is None for k in ("entrada", "salida", "escritura_cache", "lectura_cache")):
            raise SystemExit(f"sin tarifa para {m}: añádala al fichero de precios")
        return p

    # Presupuesto del ciclo: el límite de cada bolsa con la ampliación máxima (autorizada o no). Desde T-146, una petición
    # con bolsa solo sale si su peor caso (la entrada por el margen, como poco la salida mínima) cabe en lo que queda de la
    # bolsa, así que el mensaje de una llamada con bolsa no pasa de lo que deja el límite entero (S4b, T-148)
    factor_reserva = float(parametro(cfg, "presupuesto_uc.reserva.factor_tokens_entrada"))
    salida_minima = float(parametro(cfg, "presupuesto_uc.reserva.salida_minima_tokens"))
    amp = max(float(parametro(cfg, "presupuesto_uc.ampliacion_sin_autorizacion")),
              float(parametro(cfg, "presupuesto_uc.ampliacion_max_autorizable")))
    tope = float(parametro(cfg, "presupuesto_uc.ciclo_semanal_max"))
    minimo_comun = float(parametro(cfg, "presupuesto_uc.fraccion_minima_comun")) * tope
    niveles = sorted({float(parametro(cfg, "presupuesto_uc.N1")), float(parametro(cfg, "presupuesto_uc.N2"))})
    limite_max = {c: (1 + amp) * niveles[-1] for c in tipos}
    limite_max["COMUN"] = (1 + amp) * max(minimo_comun, tope - len(tipos) * niveles[0])

    def encargo_max(bolsa):
        """Tokens de encargo (del simulador) que admite como mucho la reserva en una bolsa vacía: sin contar el system
        prompt ni las herramientas, que también entran en la reserva, así que es una cota por encima."""
        return max(0.0, 2 * uc[0] * (limite_max[bolsa] - 0.5 * salida_minima / uc[1]) / factor_reserva)

    def peor(a, leido, web, bolsa=None, multiplica=False):
        tok = encargo(a) + leido
        if bolsa is not None:   # S4b: el presupuesto acota el encargo; en la respuesta y la contrarréplica, es la cota
            tok = encargo(a) + encargo_max(bolsa) if multiplica else min(tok, encargo(a) + encargo_max(bolsa))
        return peor_llamada(precio(a), sistema_de(a), tok, max_tokens_de(cfg, a), web, reparaciones,
                            continuaciones, factor_tokens, max_usos, precio_busqueda_mil, uc, tok_rep), tok

    papeles, bolsas = [], collections.defaultdict(lambda: {"usd_por_uc": 0.0, "ultima_uc": 0.0})
    salida_papel: collections.Counter = collections.Counter()   # salida máxima de cada papel, sumada en todos los tipos
    for c in tipos:
        leido = 0          # S4: la salida máxima de las llamadas anteriores de su tipo
        for papel, agentes, n, web in LLAMADAS_POR_TIPO:
            ags = [AGENTE_CLASE[c] if a == "ANALISTA" else a for a in agentes]
            casos = [(peor(a, leido, web and a in con_busqueda, c, papel in MULTIPLICAN_ENCARGO), a) for a in ags]
            (w, tok), a = max(casos, key=lambda x: x[0][0]["usd"])
            k = maximo(n)
            papeles.append({"tipo": c, "papel": papel, "agente": a, "agentes": ags, "llamadas": k, "bolsa": c,
                            "encargo_tok": max(x[0][1] for x in casos), "lee_tok": leido,
                            **{q: v * k for q, v in w.items()}})
            b = bolsas[c]
            b["usd_por_uc"] = max([b["usd_por_uc"]] + [_usd_por_uc(precio(x), uc) for x in ags])
            b["ultima_uc"] = max(b["ultima_uc"], w["uc"])
            salida = k * max(max_tokens_de(cfg, x) for x in ags)
            leido += salida
            salida_papel[papel] += salida
    for papel, a, n, bolsa, lee in LLAMADAS_DEL_CICLO:
        bolsa = bolsa or ("COMUN" if con_t146 else None)   # T-148 r02 (H-03): con T-146, AG-18/19/20 pagan de la COMÚN
        for _i in range(n):   # la segunda llamada del mismo papel puede leer la primera (la reescritura, el 2.º dictamen)
            leido = sum(v for q, v in salida_papel.items() if lee == "*" or q in lee)
            w, tok = peor(a, leido, a in con_busqueda, bolsa)
            papeles.append({"tipo": None, "papel": papel, "agente": a, "agentes": [a], "llamadas": 1, "bolsa": bolsa,
                            "encargo_tok": tok, "lee_tok": leido, **w})
            if bolsa:
                b = bolsas[bolsa]
                b["usd_por_uc"] = max(b["usd_por_uc"], _usd_por_uc(precio(a), uc))
                b["ultima_uc"] = max(b["ultima_uc"], w["uc"])
            salida_papel[papel] += max_tokens_de(cfg, a)
    cota_llamadas = sum(x["usd"] for x in papeles)
    busquedas = sum(x["busquedas"] for x in papeles)

    # Cota por presupuesto. Con T-146, `consumo.ReservaLlamada` reserva el peor caso de cada petición antes de que salga, así
    # que una bolsa acaba, como mucho, en su límite con la ampliación máxima (salvo lo que no se reserva: S5 y el margen).
    # Con `--sin-t146`, el código de antes (una estimación previa con `Presupuesto.puede` y lo real cargado después): cada
    # llamada admitida empezaba con lo consumido ≤ límite − estimado, y la bolsa acababa, como mucho, en su límite más su
    # última llamada (con el encargo acotado por S4b)
    p_tipos = max(bolsas[c]["usd_por_uc"] for c in tipos)
    p_comun = bolsas["COMUN"]["usd_por_uc"]
    limites = 0.0
    for k in range(len(tipos) + 1):   # k tipos en el nivel alto y el resto en el bajo (el ciclo C1 asigna N1 o N2)
        base = k * niveles[-1] + (len(tipos) - k) * niveles[0]
        limites = max(limites, (1 + amp) * (p_tipos * base + p_comun * max(tope - base, minimo_comun)))
    ultimas = sum(b["usd_por_uc"] * b["ultima_uc"] for b in bolsas.values())
    primas = max(b["usd_por_uc"] for b in bolsas.values()) * sum(x["prima_uc"] for x in papeles if x["bolsa"])
    fuera_presupuesto = sum(x["usd"] - x["busquedas"] * precio_busqueda_mil / 1000 for x in papeles if not x["bolsa"])
    if con_t146:   # T-146 integrado: todo pasa por el presupuesto (ninguna bolsa pasa de su límite salvo S5 y el margen)
        uc_busqueda = (cfg.get("uc") or {}).get("uc_por_busqueda_web")
        if uc_busqueda:   # una búsqueda cuesta en UC lo suyo: su precio por UC puede ser el más alto
            p_busq = precio_busqueda_mil / 1000 / float(uc_busqueda)
            cota_presupuesto = limites * max(p_busq / p_tipos, p_busq / p_comun, 1.0)
        else:
            cota_presupuesto = limites
    else:
        cota_presupuesto = limites + ultimas + primas + fuera_presupuesto + busquedas * precio_busqueda_mil / 1000
    # S5 (T-148, H-02): lo que lee cada búsqueda entra como entrada en su petición y en cada continuación posterior del mismo
    # intento, que reenvía el contenido pausado. Por cada 1 000 tokens leídos por búsqueda, al precio de escritura de caché
    vueltas = 1 + continuaciones

    def lectura_llamadas(x):   # todas las peticiones de las llamadas del papel, cada una con lo leído hasta ella
        return (x["llamadas"] * (1 + reparaciones) * max_usos * vueltas * (vueltas + 1) / 2
                * precio(x["agente"])["escritura_cache"] * 1000 / 1e6)
    lecturas = sum(lectura_llamadas(x) for x in papeles if x["busquedas"])
    # T-148 r02 (QA r01 de T-148, H-01): en la cota por presupuesto, lo leído (que la reserva de T-146 no cubre) solo puede
    # pasar el límite de una bolsa en la petición que lo cruza, porque después ya no cabe ninguna: por bolsa, la mayor
    # lectura de una petición (la última vuelta de `pause_turn` reenvía las búsquedas de las anteriores). Sin descontar lo
    # que reserve `tokens_lectura_por_busqueda` (más holgado). Con `--sin-t146`, la de una llamada entera por bolsa y las
    # llamadas fuera del presupuesto, enteras
    por_bolsa: dict = collections.defaultdict(float)
    lecturas_presupuesto = 0.0
    for x in papeles:
        if not x["busquedas"]:
            continue
        if x["bolsa"]:   # sin T-146 la comprobación era por llamada, no por petición: una llamada entera
            una = (max_usos * vueltas * precio(x["agente"])["escritura_cache"] * 1000 / 1e6 if con_t146
                   else lectura_llamadas(x) / x["llamadas"])
            por_bolsa[x["bolsa"]] = max(por_bolsa[x["bolsa"]], una)
        else:
            lecturas_presupuesto += lectura_llamadas(x)
    lecturas_presupuesto += sum(por_bolsa.values())
    reservado = float(((cfg.get("presupuesto_uc") or {}).get("reserva") or {}).get("tokens_lectura_por_busqueda") or 0)
    manda_presupuesto = cota_presupuesto < cota_llamadas
    return {"tipos": tipos,
            "usd_por_mil_tokens_leidos_por_busqueda": lecturas_presupuesto if manda_presupuesto else lecturas,
            "usd_por_mil_leidos_cota_llamadas": lecturas, "usd_por_mil_leidos_cota_presupuesto": lecturas_presupuesto,
            "manda": "presupuesto" if manda_presupuesto else "llamadas",
            "tokens_lectura_reservados_por_busqueda": reservado if con_t146 else 0.0,
            "encargo_max_por_bolsa": {b: encargo_max(b) for b in limite_max},"llamadas_max": sum(x["llamadas"] for x in papeles), "peticiones_max": sum(x["peticiones"] for x in papeles),
            "busquedas": busquedas, "cota_llamadas": cota_llamadas, "cota_presupuesto": cota_presupuesto,
            "cota": min(cota_llamadas, cota_presupuesto), "presupuesto": {
                "limites": limites, "ultima_llamada": ultimas, "primas_cache": primas, "fuera_del_presupuesto": fuera_presupuesto},
            "papeles": papeles}


def tipos_del_estado(estado: str, cfg: dict) -> list[str]:
    """T-148 (QA r01 de T-145, H-03): los tipos que analizará el ciclo con ese estado del Bloque A: los de F10 (P-02), como
    `Bloque.ciclo`; si F10 aún no existe, los de la configuración (`perfiles_activos`, lo que F10 toma al nacer). Una
    carpeta que no existe falla cerrado (el estado no se crea para leerlo)."""
    from bloque_a.almacen import Almacen
    from bloque_a.configuracion import perfiles_activos
    if not Path(estado).is_dir():
        raise SystemExit(f"no existe la carpeta del estado del Bloque A {estado}")
    p02 = (Almacen(estado).estado("F10").get("P-02") or {}).get("valor_vigente")
    return list(p02) if p02 else list(perfiles_activos(cfg))


def calcular(carpeta: str, precios: str, config: str | None, estado: str | None = None, con_t146: bool = True) -> dict:
    llamadas = json.loads((Path(carpeta) / "llamadas.json").read_text(encoding="utf-8"))
    tarifa = yaml.safe_load(Path(precios).read_text(encoding="utf-8"))
    cfg = _config(config)
    bw = cfg.get("busqueda_web") or {}
    agentes = set(bw.get("agentes") or []) if bw.get("habilitada_en_vivo") else set()
    pb, factor = float(tarifa["precio_busqueda_web_por_mil"]), float(tarifa.get("factor_tokens_cota", 1.0))
    r = estimar(llamadas, tarifa["precios_por_millon"], pb, agentes, int(bw.get("max_usos_por_llamada", 0)), factor,
                int((cfg.get("llm") or {}).get("max_continuaciones_pause_turn", 0)),
                int((cfg.get("llm") or {}).get("reintento_reparacion", 0)))
    r["ciclo"] = cota_ciclo(llamadas, cfg, tarifa["precios_por_millon"], pb, factor,
                            tipos=tipos_del_estado(estado, cfg) if estado else None, con_t146=con_t146)
    return r


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("carpeta")
    ap.add_argument("--precios", default=str(EJECUTOR / "config" / "precios_anthropic.yaml"))
    ap.add_argument("--config", default=None)
    ap.add_argument("--estado", default=None, help="estado del Bloque A con el que correrá el ciclo: los tipos salen de F10 "
                                                   "(P-02), como en el ciclo (T-148)")
    t146 = ap.add_mutually_exclusive_group()   # T-148 r02 (QA r01 de T-148, H-03): una u otra, no las dos
    t146.add_argument("--con-t146", action="store_true", help="se acepta por compatibilidad: desde que T-146 está en el "
                                                               "código, la cota por presupuesto es siempre la de los límites")
    t146.add_argument("--sin-t146", action="store_true", help="la cota más holgada de antes de T-146 (para comparar)")
    a = ap.parse_args(argv)
    con_t146 = not a.sin_t146
    r = calcular(a.carpeta, a.precios, a.config, a.estado, con_t146)
    c = r["ciclo"]
    print(f"{r['llamadas']} llamadas medidas · suelo {r['estimacion']:.2f} USD · peor caso de esas llamadas "
          f"{r['cota_superior']:.2f} USD (no es una cota del ciclo: faltan las llamadas que dependen del modelo)")
    for m, v in r["por_modelo"].items():
        print(f"  {m:20} llamadas {v['llamadas']:3} · suelo {v['estimacion']:.3f} · peor caso {v['cota_superior']:.3f}")
    p = c["presupuesto"]
    print(f"Tipos de activo: {', '.join(c['tipos'])}" + ("" if a.estado else " (de la configuración; con un estado que ya "
          "tiene F10, el ciclo usa P-02: pase --estado)"))
    # T-148 r02 (QA r01 de T-148, H-01): también con T-146 la cota es «salvo lo que lee cada búsqueda»: la reserva no lo cubre
    salvo = "salvo lo que lee cada búsqueda (S5) y lo que la entrada real pase del margen de S1"
    print(f"Cota superior del ciclo: {c['cota']:.2f} USD {salvo}, la menor de:\n"
          f"  por llamadas   {c['cota_llamadas']:7.2f} USD (hasta {c['llamadas_max']} llamadas, {c['peticiones_max']} peticiones "
          f"y {c['busquedas']} búsquedas web)\n"
          + (f"  por presupuesto {c['cota_presupuesto']:6.2f} USD (con T-146 integrado: solo los límites de las bolsas)"
             if con_t146 else
             f"  por presupuesto {c['cota_presupuesto']:6.2f} USD (límites {p['limites']:.2f} + última llamada de cada bolsa "
             f"{p['ultima_llamada']:.2f} + caché cargada como lectura {p['primas_cache']:.2f} + fuera del presupuesto "
             f"{p['fuera_del_presupuesto']:.2f} + búsquedas; la de antes de T-146, más holgada)"))
    reservado = c["tokens_lectura_reservados_por_busqueda"]
    reserva = ("" if not con_t146 else
               f"; la reserva de T-146 aparta {reservado:.0f} tokens por búsqueda (`presupuesto_uc.reserva."
               "tokens_lectura_por_busqueda`), que el peso no descuenta" if reservado else
               "; la reserva de T-146 no lo cubre (`presupuesto_uc.reserva.tokens_lectura_por_busqueda` = 0)")
    print(f"Lo que lee cada búsqueda (S5): por cada 1 000 tokens leídos en cada búsqueda, la cota que manda (por {c['manda']}) "
          f"sube {c['usd_por_mil_tokens_leidos_por_busqueda']:.2f} USD (la cota por llamadas, "
          f"{c['usd_por_mil_leidos_cota_llamadas']:.2f}; la cota por presupuesto, {c['usd_por_mil_leidos_cota_presupuesto']:.2f})"
          f"{reserva}")
    print("Supuestos:\n" + "\n".join("  " + s for s in SUPUESTOS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
