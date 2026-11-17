"""QA r03 de T-143 · El Anexo B V5.2 (texto de la r03) contrastado de nuevo con el ejecutor, contrato a contrato.

Sustituye a `r02_01`, anclado al texto de la r02 (busca «`memoria` (…)» y pedía los anidados de la ficha con la ruta
`INFORME_CLASE.finalistas[].x`; la r03 los describe con «En `FINALISTA`, …», como fija la introducción del anexo, y este script
lee esa notación). Desde la raíz del repositorio, con el Python del .venv:

    .venv/bin/python .docs/tickets/T-143/revisores/r03_01_anexo_b_contra_codigo.py

El analizador de la prosa es propio (no el de `test_fase3_goldens.py`). Las comprobaciones:

1. Qué esquema de respuesta valida el ejecutor en cada contrato (código y flujos simulados V5 y V6) frente a los que el Anexo B
   describe con «con `ESQUEMA`, que exige …» (ahora también CT-17 con AUDITORIA).
2. De cada esquema: primer nivel, anidados (los de la ficha, bajo «En `FINALISTA`, …») y la regla de lectura «un campo con
   lista cerrada lleva sus valores entre paréntesis», también para los opcionales que la frase nombra.
3. CT-05 (r03): las claves de `memoria` y la forma de `delta_gc0` de cada tipo de orden, frente a la frase de cada tipo, y la
   nota del V6 («no hay orden INTEGRACION»), también con `v6.sintetizador` desactivado.
4. Lo que el ejecutor lee de una respuesta además de lo que el esquema exige: BUSQUEDA (r03) y AUDITORIA (r03).
5. Cobertura del V6 por defecto: qué retornos internos con esquema deja de pedir el diseño V6 y si el párrafo lo dice.
6. CT-03, CT-04, CT-09, CT-01 y CT-24, como en la r02.

Imprime una línea por comprobación (OK o HALLAZGO) y termina con 1 si hay algún hallazgo. Sin red ni API: cliente simulado y
Motor local, en una carpeta temporal.
"""
from __future__ import annotations

import inspect
import json
import re
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJECUTOR = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJECUTOR))
sys.path.insert(0, str(EJECUTOR / "tests"))

import conftest  # noqa: E402

from bloque_a import contratos, diseno_v6, orquestacion  # noqa: E402

DOC0 = next((RAIZ / "bloque_a" / "01_Gobernanza").glob("Documento 0*.md")).read_text(encoding="utf-8")
ANEXO_B = DOC0[DOC0.index("## ANEXO B."):DOC0.index("## ANEXO C.")]
FUENTE = "".join((EJECUTOR / "bloque_a" / n).read_text(encoding="utf-8") for n in ("orquestacion.py", "diseno_v6.py", "seguimiento.py"))
HALLAZGOS: list[str] = []
COMUNES = {"estado", "autoevaluacion"}


def anota(ok: bool, texto: str) -> None:
    print(("OK       " if ok else "HALLAZGO ") + texto)
    if not ok:
        HALLAZGOS.append(texto)


def parrafos() -> dict[str, str]:
    salida: dict[str, str] = {}
    for trozo in re.split(r"(?m)^(?=\*\*)", ANEXO_B):
        m = re.match(r"\*\*(CT-\d\d)(?: (a|/) (CT-\d\d))?", trozo)
        if not m:
            continue
        a, union, b = m.groups()
        nums = range(int(a[3:]), int(b[3:]) + 1) if union == "a" else [int(x[3:]) for x in (a, b) if x]
        for n in nums:
            salida[f"CT-{n:02d}"] = salida.get(f"CT-{n:02d}", "") + trozo
    return salida


P = parrafos()


def nombres(texto: str | None) -> list[str]:
    return re.findall(r"`([^`]+)`", texto or "")


def frases(texto: str) -> list[str]:
    return [f for f in re.split(r"(?<=\.)\s+(?=[A-ZÁÉÍÓÚ«`(])", texto.replace("\n", " ")) if f]


# --------------------------------------------------------------------------------------------- 1. qué esquema en cada contrato
def esquemas_del_codigo() -> dict[str, set[str]]:
    """(contrato → esquemas) de cada llamada `_invocar` del código, con los dos casos que no son literales (CT-06 por fase y
    CT-07/CT-08 por tipo)."""
    pares: dict[str, set[str]] = {}
    for m in re.finditer(r'_invocar\(\s*[^,]+,\s*"(CT-\d\d|C\d)",\s*[^,]+,\s*"([A-Z_0-9]+)"', FUENTE):
        pares.setdefault(m.group(1), set()).add(m.group(2))
    if '"INFORME_CLASE" if fase == "CRIBADO_E_INVESTIGACION" else "REVISION_VIGENTES"' in FUENTE:
        pares.setdefault("CT-06", set()).update({"INFORME_CLASE", "REVISION_VIGENTES"})
    if re.search(r'_invocar\(agente, tipo, msg, "BUSQUEDA"', FUENTE):
        pares.setdefault("CT-07", set()).add("BUSQUEDA")
        pares.setdefault("CT-08", set()).add("BUSQUEDA")
    return pares


class Espia:
    """Las llamadas a agentes (`_invocar`) y los mensajes de la mensajería de un Bloque."""

    def __init__(self, b):
        self.invocaciones: list[tuple] = []
        self.mensajes: list[dict] = []
        orig_inv, orig_crear = b._invocar, b.mensajeria.crear

        def inv(agente, contrato, mensaje, esquema, *a, **k):
            self.invocaciones.append((agente, contrato, esquema, json.loads(json.dumps(mensaje, default=str))))
            return orig_inv(agente, contrato, mensaje, esquema, *a, **k)

        def crear(contrato, emisor, receptor, cuerpo, **k):
            msg = orig_crear(contrato, emisor, receptor, cuerpo, **k)
            self.mensajes.append(json.loads(json.dumps(msg, default=str)))
            return msg

        b._invocar, b.mensajeria.crear = inv, crear


def flujos(tmp: Path) -> dict[str, Espia]:
    universo = conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO)
    out = {}
    for nombre, cfg in (("v5", conftest.config_pruebas(auditoria={"en_backtest": True})),
                        ("v6", conftest.config_pruebas(diseno="v6", auditoria={"en_backtest": True})),
                        ("v6_sin_sintetizador", conftest.config_pruebas(diseno="v6", v6={"sintetizador": False},
                                                                        auditoria={"en_backtest": True}))):
        b = conftest.nuevo_bloque(tmp / nombre, universo, cfg=cfg)
        e = Espia(b)
        r = b.ciclo(conftest.AS_OF, alcance={"clases": ["RV", "MP"]})
        if nombre == "v5":   # un seguimiento encargado (C6) sobre una opción del ciclo
            opps = [o["opp_id"] for d in r["paquete"]["clases"].values() for o in d["opciones"]]
            if opps:
                b.seguimientos.procesar({"accion": "ALTA", "opp_id": opps[0], "frecuencia": "SEMANAL"}, conftest.AS_OF)
                b.seguimientos.ejecutar("2026-06-12")
        out[nombre] = e
    return out


def descritos(ct: str) -> dict[str, re.Match]:
    return {m.group(1): m for m in re.finditer(r"con `([A-Z_0-9]+)`, que exige ([^;.]*)(?:; admite además ([^;.]*))?\.", P.get(ct, ""))}


def comprueba_que_esquema(pares: dict[str, set[str]], vistos: dict[str, set[str]]) -> None:
    for ct in sorted(set(pares) | set(vistos)):
        if not ct.startswith("CT-"):
            continue
        usados = pares.get(ct, set()) | vistos.get(ct, set())
        if ct == "CT-03":   # el retorno CT-03 pasa por la mensajería; el Anexo B describe ese retorno, no el de CONSULTA
            props = set(contratos.ESQUEMAS["CONSULTA"]["properties"])
            json_ret = set(re.findall(r'"([a-z_]+)":', P["CT-03"].split("\n")[3] if P["CT-03"].count("\n") > 3 else ""))
            anota(json_ret - {"query_id"} <= props, f"CT-03: los campos del retorno del Anexo B están en CONSULTA ({sorted(json_ret)})")
            continue
        faltan = sorted(e for e in usados if e not in descritos(ct))
        anota(not faltan, f"{ct}: el ejecutor valida la respuesta con {sorted(usados)}; el Anexo B la describe con la frase fija"
              + (f" salvo {faltan} (el párrafo dice: «{_cola(ct)}»)" if faltan else ""))


def _cola(ct: str) -> str:
    p = P.get(ct, "").replace("\n", " ")
    i = p.find("espuesta")
    return p[max(0, i - 1):i + 140].strip() if i >= 0 else p[:140]


# --------------------------------------------------------------------------------------------- 2. campos, anidados y valores
def enum_de(prop: dict) -> list | None:
    if "enum" in prop:
        return prop["enum"]
    it = prop.get("items")
    return it.get("enum") if isinstance(it, dict) else None


def anidados(esq: dict, ruta: str = ""):
    for campo, prop in esq.get("properties", {}).items():
        if not ruta and campo in COMUNES:
            continue
        sub = prop.get("items", prop)
        if isinstance(sub, dict) and ("required" in sub or "properties" in sub):
            yield f"{ruta}{campo}", sub
            yield from anidados(sub, f"{ruta}{campo}[].")


def frases_anidadas(ct: str) -> dict[tuple[str, str], tuple[str, str | None]]:
    out = {}
    for m in re.finditer(r"En ((?:`[A-Z_0-9]+`(?:, | y )?)+), (?:cada elemento de )?`([a-z_\[\].0-9]+)` lleva ([^;.]*)(?:; admite además ([^;.]*))?\.",
                         P.get(ct, "")):
        for clave in re.findall(r"`([A-Z_0-9]+)`", m.group(1)):
            out[(clave, m.group(2))] = (m.group(3), m.group(4))
    return out


def valores_en(texto: str) -> dict[str, set[str]]:
    return {c: {v.strip() for v in vs.split("|")} for c, vs in re.findall(r"`([^`]+)` \(([^)]*)\)", texto or "")}


def _valores_que_faltan(texto: str, esq: dict, donde: str) -> list[str]:
    """Campos con lista cerrada (en el campo o en sus elementos) que la frase nombra sin sus valores, o con otros."""
    dados, out = valores_en(texto), []
    for campo in nombres(texto):
        e = enum_de(esq.get("properties", {}).get(campo, {}))
        if e is not None and dados.get(campo) != set(e):
            out.append(f"{donde}.{campo} (código {e}; Anexo B {sorted(dados.get(campo, []))})")
    return out


def _compara_anidado(ct, etiqueta, frase, sub, sin_valores) -> bool:
    lleva, ademas = frase
    if lleva.startswith("lo mismo que"):
        return False
    req = set(sub.get("required", []))
    opc = set(sub.get("properties", {})) - req
    anota(set(nombres(lleva)) == req and set(nombres(ademas)) == opc,
          f"{ct} · {etiqueta}: lleva {sorted(req)}, admite {sorted(opc)}; el Anexo B dice {sorted(nombres(lleva))} / {sorted(nombres(ademas))}")
    sin_valores += _valores_que_faltan(f"{lleva} {ademas or ''}", sub, f"{ct} · {etiqueta}")
    return True


def comprueba_campos(pares: dict[str, set[str]]) -> None:
    """Primer nivel, anidados y valores. La ficha de las finalistas se busca, por dentro, bajo «En `FINALISTA`, …»."""
    sin_valores: list[str] = []
    sin_describir: list[str] = []
    for ct in sorted(p for p in pares if p.startswith("CT-") and p != "CT-03"):
        fa = frases_anidadas(ct)
        for clave in sorted(pares[ct]):
            m = descritos(ct).get(clave)
            if not m:
                continue
            esq = contratos.ESQUEMAS[clave]
            exige = set(esq.get("required", [])) - COMUNES
            admite = set(esq.get("properties", {})) - set(esq.get("required", [])) - COMUNES
            anota(set(nombres(m.group(2))) == exige and set(nombres(m.group(3))) == admite,
                  f"{ct} · {clave}: exige {sorted(exige)} y admite {sorted(admite)}; el Anexo B dice "
                  f"{sorted(nombres(m.group(2)))} / {sorted(nombres(m.group(3)))}")
            sin_valores += _valores_que_faltan(f"{m.group(2)} {m.group(3) or ''}", esq, f"{ct} · {clave}")
            dentro_de_ficha: list[str] = []
            for ruta, sub in anidados(esq):
                if any(ruta.startswith(r + "[].") for r in dentro_de_ficha):
                    continue   # dentro de la ficha: se mira abajo con «En `FINALISTA`, …»
                frase = fa.get((clave, ruta))
                if frase is None:
                    sin_describir.append(f"{ct} · {clave}.{ruta}")
                    continue
                comparado = _compara_anidado(ct, f"{clave}.{ruta}", frase, sub, sin_valores)
                if sub is contratos.FINALISTA:
                    dentro_de_ficha.append(ruta)
                    if comparado:
                        for rel, sub2 in anidados(contratos.FINALISTA):
                            f2 = fa.get(("FINALISTA", rel))
                            if f2 is None:
                                sin_describir.append(f"{ct} · FINALISTA.{rel}")
                            else:
                                _compara_anidado(ct, f"FINALISTA.{rel}", f2, sub2, sin_valores)
    anota(not sin_valores, "Regla de lectura («En esas frases, un campo con lista cerrada lleva sus valores entre paréntesis»), "
          "también en los opcionales nombrados: " + ("se cumple" if not sin_valores else "sin sus valores o con otros: "
                                                     + "; ".join(sorted(set(sin_valores)))))
    anota(not sin_describir, "Campos anidados de los esquemas descritos (con la notación «En `FINALISTA`, …» dentro de la ficha): "
          + ("todos descritos" if not sin_describir else "sin frase: " + "; ".join(sorted(set(sin_describir)))))


# --------------------------------------------------------------------------------------------- 3. CT-05
def _forma_delta(d) -> str:
    if not d:
        return "vacío"
    vals = list(d.values())
    if all(isinstance(v, dict) and "cambio_material" in v for v in vals):
        return "GC0 por tipo"
    if all(isinstance(v, list) for v in vals):
        return "motivos por tipo"
    return f"otra ({type(vals[0]).__name__})"


def comprueba_ct05(f: dict[str, Espia]) -> None:
    p = P["CT-05"].replace("\n", " ")
    esperado = {}
    for m in re.finditer(r"En (la orden del ciclo \(([^)]*)\)|SEGUIMIENTO|INTEGRACION), `memoria` lleva ([^.]*?), y `delta_gc0`(,? [^.]*)\.", p):
        tipos = [x.strip() for x in re.split(r",| o ", m.group(2))] if m.group(2) else [m.group(1)]
        memoria = set(re.findall(r"`([a-z_0-9]+)`", m.group(3).split(" (")[0]))
        delta = "vacío" if "vacío" in m.group(4) else ("motivos por tipo" if "motivos" in m.group(4) else "GC0 por tipo")
        for tp in tipos:
            if tp:
                esperado[tp] = (memoria, delta)
    anota(set(esperado) >= {"PERIODICO", "SEGUIMIENTO", "INTEGRACION"}, f"CT-05: el Anexo B describe `memoria` y `delta_gc0` de {sorted(esperado)}")
    vistos: dict[str, list[tuple[set, str]]] = {}
    for nombre in ("v5", "v6"):
        for m in f[nombre].mensajes:
            if m["contrato"] == "CT-05" and m["tipo_mensaje"] == "ENCARGO":
                vistos.setdefault(m["tipo"], []).append((set(m.get("memoria") or {}), _forma_delta(m.get("delta_gc0"))))
        for _a, ct, _e, msg in f[nombre].invocaciones:
            if ct == "CT-05":
                vistos.setdefault(msg.get("tipo"), []).append((set(msg.get("memoria") or {}), _forma_delta(msg.get("delta_gc0"))))
    for tipo, lst in sorted(vistos.items()):
        for memoria, delta in {(frozenset(a), b) for a, b in lst}:
            e = esperado.get(tipo)
            anota(e is not None and set(memoria) == e[0] and delta == e[1],
                  f"CT-05 tipo {tipo}: `memoria` {sorted(memoria)}, `delta_gc0` {delta}; el Anexo B dice "
                  + (f"{sorted(e[0])}, {e[1]}" if e else "nada para este tipo"))
    integ = {n: [x for x in f[n].invocaciones if x[1] == "CT-05"] for n in f}
    dice = "En el diseño V6 no hay orden INTEGRACION ni su retorno" in p
    anota(dice and not integ["v6"], f"CT-05 V6 por defecto: {len(integ['v6'])} órdenes INTEGRACION; el Anexo B dice que no hay")
    anota(not integ.get("v6_sin_sintetizador"),
          "CT-05 V6 con `v6.sintetizador: false`: " + (f"el ejecutor emite {len(integ['v6_sin_sintetizador'])} orden(es) "
          "INTEGRACION a AG-02 (y CT-15 con REDACCION), y el Anexo B dice «En el diseño V6 no hay orden INTEGRACION» sin "
          "condición" if integ.get("v6_sin_sintetizador") else "sin orden INTEGRACION"))
    v5 = {x[2] for x in f["v5"].invocaciones if x[1] == "CT-15"}
    v6 = {x[2] for x in f["v6"].invocaciones if x[1] == "CT-15"}
    anota(v5 == {"REDACCION"} and v6 == {"SINTESIS"}, f"CT-15: V5 responde con {sorted(v5)} y V6 con {sorted(v6)}")


def comprueba_v6(f: dict[str, Espia], pares: dict[str, set[str]]) -> None:
    """Retornos internos con esquema que el diseño V6 por defecto no pide al agente, y si el párrafo menciona el V6."""
    v5 = {x[1] for x in f["v5"].invocaciones}
    v6 = {x[1] for x in f["v6"].invocaciones}
    for ct in sorted(c for c in pares if c.startswith("CT-") and c in v5 and c not in v6):
        anota("V6" in P.get(ct, ""), f"{ct}: el V5 pide la respuesta del agente ({sorted(pares[ct])}) y el V6 por defecto no "
              f"(sin invocación en el ciclo V6); el párrafo {'menciona' if 'V6' in P.get(ct, '') else 'no menciona'} el V6")


# --------------------------------------------------------------------------------------------- 4. otros contratos
def comprueba_ct03(tmp: Path) -> None:
    universo = conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO)
    b = conftest.nuevo_bloque(tmp / "ct03", universo)
    sin = b.consulta("¿Qué opinas del oro frente a la plata a 6 meses?", as_of=conftest.AS_OF, ejecutar_escalado=False)["escalado"]
    anota(isinstance(sin, dict) and "estado_run" not in sin and sin["run_id"] is None
          and set(sin) == {"run_id", "plazo_estimado", "nivel", "clases", "respuesta_provisional"},
          f"CT-03 sin ejecutar el análisis: `escalado` lleva {sorted(sin) if isinstance(sin, dict) else sin}, `run_id` {sin.get('run_id') if isinstance(sin, dict) else '-'}")
    b.cfg.setdefault("perfiles", {})["activos"] = ["MP"]
    con = b.consulta("¿Qué opinas del oro frente a la plata a 6 meses?", contexto={"clases": ["MP"]}, as_of=conftest.AS_OF)["escalado"]
    anota(isinstance(con, dict) and "estado_run" in con and con.get("run_id"),
          f"CT-03 con el análisis ejecutado: `escalado` lleva {sorted(con) if isinstance(con, dict) else con}")


def comprueba_ct04(tmp: Path) -> None:
    p = P["CT-04"]
    cinco = ("decisiones", "valoracion_informe", "configuracion", "resultado_comunicado", "aprobar_certificados")
    anota(all(f"`{k}`" in p for k in cinco) and "sin ninguno de los cinco se rechaza" in p, "CT-04: el Anexo B nombra los cinco bloques")
    codigo = re.search(r'if not any\(k in ct04 for k in \(([^)]*)\)\)', inspect.getsource(orquestacion.Bloque.decision)).group(1)
    anota(set(re.findall(r'"([a-z_]+)"', codigo)) == set(cinco), f"CT-04: `Bloque.decision` mira {codigo}")
    b = conftest.nuevo_bloque(tmp / "ct04", conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO))
    try:
        b.decision({"otra_cosa": 1}, conftest.AS_OF)
        rechazado = False
    except ValueError:
        rechazado = True
    anota(rechazado, "CT-04 con solo un bloque que no es de los cinco: " + ("se rechaza" if rechazado else "se admite"))
    r = b.decision({"aprobar_certificados": ["CERT-2099-9999"]}, conftest.AS_OF)
    anota(r["estado"] in ("REGISTRADA", "APLICADA_PARCIALMENTE", "APLICADA"), f"CT-04 con solo `aprobar_certificados`: {r['estado']}")


def comprueba_ct09(tmp: Path) -> None:
    from bloque_a.almacen import Almacen
    from bloque_a.configuracion import cargar_config
    from bloque_a.motor import servicio
    import pandas as pd

    class SinFecha:
        as_of = None
        nombre = "revisor"

    class ConFecha(SinFecha):
        as_of = pd.Timestamp("2029-12-31")

    ficha = next(f for f in sorted(servicio.CASOS_CONTROL) if servicio.servible(f) and f != "VOL-GARCH-001")
    caso = servicio.CASOS_CONTROL[ficha][0]
    pet = {"operacion": ficha, "datos": caso.get("datos") or [], "parametros": dict(caso.get("parametros") or {})}
    r1 = servicio.Motor(Almacen(tmp / "m1"), SinFecha(), cargar_config()).servir(dict(pet), "AG-21")
    al = Almacen(tmp / "m2")
    r2 = servicio.Motor(al, ConFecha(), cargar_config()).servir(dict(pet), "AG-21")
    rc = [e for e in al.leer("RC") if e.get("id") == r2.get("calc_id") or e.get("calc_id") == r2.get("calc_id")]
    usa = json.dumps(rc, default=str).count("2029-12-31") > 0
    anota(str(r1.get("estado", "")).startswith("SERVED") and str(r2.get("estado", "")).startswith("SERVED") and usa,
          f"CT-09 sin `fecha_corte`: proveedor sin fecha → {r1.get('estado')}; proveedor con fecha → {r2.get('estado')}, "
          f"y el registro de cálculos {'usa' if usa else 'no muestra'} la fecha del proveedor")
    anota("la exige la mensajería" in P["CT-09"] and "fecha_corte" in contratos.CAMPOS_MINIMOS["CT-09"], "CT-09: la mensajería exige `fecha_corte`")


def comprueba_ct01() -> None:
    src = inspect.getsource(orquestacion.Bloque.ciclo)
    anota('(alcance or {}).get("clases") or activas' in src and "dentro de `alcance` todo es opcional" in P["CT-01"],
          "CT-01: sin `alcance.clases`, el ciclo usa los tipos activos, y el Anexo B lo dice")
    anota(isinstance(contratos.CAMPOS_MINIMOS["CT-01"], list) and "alcance" in contratos.CAMPOS_MINIMOS["CT-01"],
          "CT-01: la mensajería exige `alcance` (un objeto, aunque esté vacío)")


def comprueba_busqueda() -> None:
    """r03: «De cada referencia lee además, si los trae, …»: lo que lee `_peticion_conocimiento`, sus valores por defecto y
    cuántas referencias toma."""
    src = inspect.getsource(orquestacion.Bloque._peticion_conocimiento)
    leidos = set(re.findall(r'ref\.get\("([a-z_]+)"', src)) | ({"pronostico_fuente"} if "_bloque_pronostico_fuente(ref)" in src else set())
    leidos -= {"ref_id"}
    m = re.search(r"De cada referencia lee además, si los trae, ([^:]*):", P["CT-07"])
    dice = set(nombres(m.group(1))) if m else set()
    anota(dice == leidos, f"CT-07/CT-08: el ejecutor lee de cada referencia {sorted(leidos)} además de `ref_id`; el Anexo B nombra {sorted(dice)}")
    anota('ref.get("afirmacion") or datos.get("sintesis"' in src and "sin `afirmacion`, la pieza toma la síntesis" in P["CT-07"]
          and 'ref.get("direccion", "neutra")' in src and "sin `direccion`, neutra" in P["CT-07"],
          "CT-07/CT-08: los valores por defecto (síntesis y neutra) son los del código")
    anota('if self.modo == "backtest" and str(ref.get("ref_id")) not in ofrecidas' in src and "En backtest solo cuentan las referencias" in P["CT-07"],
          "CT-07/CT-08: en backtest solo cuentan las referencias ofrecidas")
    tope = re.search(r'datos\.get\("referencias", \[\]\)\[:(\d+)\]', src)
    anota(not tope or re.search(r"(tres|3) (primeras )?referencias", P["CT-07"]) is not None,
          "CT-07/CT-08: " + (f"el ejecutor solo toma las {tope.group(1)} primeras referencias de la respuesta (`[:{tope.group(1)}]`, "
                             "igual que `max_fuentes` del encargo) y el Anexo B no lo dice" if tope else "sin tope de referencias"))


def comprueba_ct17(pares: dict[str, set[str]]) -> None:
    """r03: CT-17 con AUDITORIA, y lo que `_auditar` lee de cada hallazgo además de lo exigido."""
    src = inspect.getsource(orquestacion.Bloque._auditar)
    leidos = set(re.findall(r'h\.get\("([a-z_]+)"', src))
    esq = contratos.ESQUEMAS["AUDITORIA"]["properties"]["hallazgos"]["items"]
    fuera = sorted(leidos - set(esq.get("properties", {})) - set(esq["required"]))
    m = re.search(r"En `AUDITORIA`, cada elemento de `hallazgos` lleva ([^.;]*)(?:; admite además ([^.]*))?\.", P["CT-17"])
    dice = set(nombres(m.group(2))) if m and m.group(2) else set()
    anota(not [c for c in fuera if c not in dice and c not in P["CT-17"]],
          f"CT-17: `_auditar` lee de cada hallazgo {sorted(leidos)} además de lo exigido"
          + (f"; {fuera} no está en el esquema ni en el Anexo B (con valor por defecto el run)" if fuera else ""))


def comprueba_ct24() -> None:
    p = P["CT-24"]
    bloque = p.split("```json")[1].split("```")[0].splitlines()
    claves = set(re.findall(r'"([a-z_]+)":', "".join(bloque[:4])))
    m = re.search(r"En el encargo son opcionales ([^:]*):", p)
    dice = set(nombres(m.group(1))) if m else set()
    anota(dice == claves - {"accion"}, f"CT-24: opcionales {sorted(dice)} frente a las claves del encargo {sorted(claves)}")


def main() -> int:
    pares = esquemas_del_codigo()
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        f = flujos(tmp)
        vistos: dict[str, set[str]] = {}
        for e in f.values():
            for _agente, ct, esq, _msg in e.invocaciones:
                vistos.setdefault(ct, set()).add(esq)
        print("Esquemas por contrato (código):", {k: sorted(v) for k, v in sorted(pares.items())})
        print("Esquemas por contrato (flujos):", {k: sorted(v) for k, v in sorted(vistos.items())})
        comprueba_que_esquema(pares, vistos)
        comprueba_campos(pares)
        comprueba_ct17(pares)
        comprueba_ct05(f)
        comprueba_v6(f, pares)
        comprueba_ct03(tmp)
        comprueba_ct04(tmp)
        comprueba_ct09(tmp)
    comprueba_ct01()
    comprueba_busqueda()
    comprueba_ct24()
    print(f"\n{len(HALLAZGOS)} hallazgos")
    return 1 if HALLAZGOS else 0


if __name__ == "__main__":
    sys.exit(main())
