"""QA r01 de T-143 · Afirmaciones del Anexo B V5.2 contrastadas con el ejecutor, una a una, fuera de los goldens.

Se ejecuta desde la raíz del repositorio con el Python del .venv:

    .venv/bin/python .docs/tickets/T-143/revisores/r01_01_anexo_b_contra_codigo.py

Imprime una línea por comprobación (OK o HALLAZGO) y termina con 1 si hay algún hallazgo. No usa red ni la API: solo el
cliente simulado y el Motor local, en una carpeta temporal.
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJECUTOR = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJECUTOR))
sys.path.insert(0, str(EJECUTOR / "tests"))

import conftest
from bloque_a.configuracion import cargar_config

from bloque_a import contratos

DOC0 = next((RAIZ / "bloque_a" / "01_Gobernanza").glob("Documento 0*.md")).read_text(encoding="utf-8")
ANEXO_B = DOC0[DOC0.index("## ANEXO B."):DOC0.index("## ANEXO C.")]
HALLAZGOS: list[str] = []


def parrafo(ct: str) -> str:
    m = re.search(rf"(?ms)^\*\*{ct}\b.*?(?=^\*\*(?:CT-|Esquema)|\Z)", ANEXO_B)
    return m.group(0) if m else ""


def anota(ok: bool, texto: str) -> None:
    print(("OK       " if ok else "HALLAZGO ") + texto)
    if not ok:
        HALLAZGOS.append(texto)


def ct04_sin_los_cuatro_bloques(tmp: Path) -> None:
    """Anexo B, CT-04: «Los cuatro bloques (…) son opcionales (…); un CT-04 sin ninguno se rechaza»."""
    p = parrafo("CT-04")
    anota("un CT-04 sin ninguno se rechaza" in p, "CT-04: el Anexo B dice que un CT-04 sin los cuatro bloques se rechaza")
    b = conftest.nuevo_bloque(tmp / "ct04", conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO))
    try:
        r = b.decision({"aprobar_certificados": ["CERT-2099-9999"]}, conftest.AS_OF)
        admitido = True
    except ValueError:
        r, admitido = None, False
    anota(not admitido, "CT-04 con solo `aprobar_certificados` (ninguno de los cuatro bloques): "
          + (f"Bloque.decision lo admite (estado {r['estado']}, rechazos {len(r['rechazos'])}); el Anexo B dice que se rechaza"
             if admitido else "se rechaza"))
    anota("aprobar_certificados" in ANEXO_B, "CT-04: el Anexo B nombra `aprobar_certificados` (PA-10, la única vía por la que un "
          "certificado de horizonte entra en vigor)" if "aprobar_certificados" in ANEXO_B else
          "CT-04: el Anexo B no nombra `aprobar_certificados`, que Bloque.decision acepta (PA-10, T-66: aprobar certificados de "
          "horizonte, que relajan un control)")


def ct03_escalado_sin_ejecutar(tmp: Path) -> None:
    """Anexo B, CT-03: «si escala, un objeto con `run_id`, `plazo_estimado`, `nivel`, `clases`, `estado_run` y
    `respuesta_provisional`». La CLI tiene `consulta --sin-escalado` (ejecutar_escalado=False)."""
    b = conftest.nuevo_bloque(tmp / "ct03", conftest.cargar_universo(conftest.RUTA_UNIVERSO_EJEMPLO))
    r = b.consulta("¿Qué opinas del oro frente a la plata a 6 meses?", as_of=conftest.AS_OF, ejecutar_escalado=False)
    esc = r.get("escalado")
    nombrados = {"run_id", "plazo_estimado", "nivel", "clases", "estado_run", "respuesta_provisional"}
    if not isinstance(esc, dict):
        anota(True, f"CT-03: la consulta no escaló con el cliente simulado (escalado={esc!r}); no se puede medir")
        return
    falta = sorted(nombrados - set(esc))
    anota(not falta, f"CT-03 con `consulta --sin-escalado`: el `escalado` del retorno lleva {sorted(esc)}"
          + (f"; le falta {falta}, que el Anexo B no marca «si aplica»" if falta else ""))


def ct09_fecha_corte(tmp: Path) -> None:
    """Anexo B, CT-09: «`fecha_corte` (obligatoria siempre: ningún dato posterior)». CT-09 no pasa por la mensajería: lo sirve
    `Motor.servir`, que toma la fecha del proveedor si falta."""
    from bloque_a.almacen import Almacen
    from bloque_a.motor import servicio

    class Proveedor:
        as_of = None
        nombre = "revisor"

    motor = servicio.Motor(Almacen(tmp / "motor"), Proveedor(), cargar_config())
    ficha = next(f for f in sorted(servicio.CASOS_CONTROL) if servicio.servible(f) and f != "VOL-GARCH-001")
    caso = servicio.CASOS_CONTROL[ficha][0]
    r = motor.servir({"operacion": ficha, "datos": caso.get("datos") or [], "parametros": dict(caso.get("parametros") or {})}, "AG-21")
    servido = str(r.get("estado", "")).startswith("SERVED")
    anota("obligatoria siempre" in parrafo("CT-09"), "CT-09: el Anexo B dice que `fecha_corte` es obligatoria siempre")
    anota(not servido, f"CT-09 sin `fecha_corte` y con un proveedor sin fecha: Motor.servir da {r.get('estado')}"
          + (" (lo sirve; solo la mensajería, por la que no pasa ningún CT-09 del ejecutor, la exige)" if servido else ""))


def ct06_prosa_de_los_anidados() -> None:
    """Prosa de los campos anidados de CT-06 frente a INFORME_CLASE, FINALISTA y RESPUESTA_OBJECIONES."""
    p = parrafo("CT-06")
    cribado = contratos.ESQUEMAS["INFORME_CLASE"]["properties"]["cribado"]["items"]["required"]
    anota("señal" not in p.split("`cribado`, por candidata,")[1].split(";")[0] or "senal" in cribado,
          f"CT-06: el Anexo B dice que cada elemento de `cribado` lleva «la señal y el motivo de paso o descarte»; el esquema "
          f"exige {cribado} (ningún campo de señal)")
    fin = set(contratos.FINALISTA["properties"])
    anota("calculos" in fin or "cálculos" not in p.split("`finalistas`,")[1].split(";")[0],
          "CT-06: el Anexo B dice que `finalistas` lleva la ficha «con puntuaciones provisionales, pre-mortem, cálculos y "
          "evidencias»; FINALISTA no tiene campo de cálculos ni de puntuaciones (tiene `dimensiones` y `afirmaciones`)")
    req = contratos.ESQUEMAS["RESPUESTA_OBJECIONES"]["properties"]["respuestas"]["items"]["required"]
    anota("evidencia_citada" in req or "la evidencia citada" not in p,
          f"CT-06: cada elemento de `respuestas` lleva, según el Anexo B, «la evidencia citada»; el esquema solo exige {req} "
          "(`evidencia_citada` es opcional y no se marca «si aplica»)")


def ct15_respuesta() -> None:
    """Anexo B, CT-15: «respuesta: rutas de los tres entregables + métricas de legibilidad». El Redactor (AG-17) responde con
    el esquema REDACCION (y el Sintetizador V6, con SINTESIS): textos, no rutas; las rutas y la legibilidad las pone el código."""
    p = parrafo("CT-15")
    red = contratos.ESQUEMAS["REDACCION"]["required"]
    falso = "rutas de los tres entregables" in p and not any("ruta" in c for c in red)
    anota(not falso, f"CT-15: el Anexo B dice que la respuesta son «rutas de los tres entregables + métricas de legibilidad»; el "
          f"Redactor responde con REDACCION, que exige {red}, y el Anexo B no lo nombra (las frases fijas de los retornos internos "
          "solo cubren CT-06 a CT-08 y CT-11 a CT-14)")


def lotes_y_auditoria() -> None:
    """Sanidad: los campos que el Anexo B V5.2 da a los lotes y a CT-16, CT-17 y CT-19 están en el código que los emite."""
    fuente = "".join((EJECUTOR / "bloque_a" / n).read_text(encoding="utf-8") for n in ("orquestacion.py", "diseno_v6.py"))
    for ct, campos in {"CT-11": ["indice", "fuente", "extracto", "afirmacion", "direccion"],
                       "CT-12": ["ref", "proxy", "opp_id", "tesis", "horizontes", "datos", "catalizadores_conocidos",
                                 "invalidacion_propuesta", "tipo_pronostico", "referencia_indice", "certificado_r13",
                                 "metodos_certificados_por_horizonte"],
                       "CT-13": ["ref", "opp_id", "afirmaciones_verificables", "evidencias", "calculos", "contrarreplicas"],
                       "CT-17": ["nivel_por_clase", "g3", "opciones", "riesgo_1a5", "relevancia_decisional"],
                       "CT-19": ["FIABILIDAD_FUENTES", "fuentes", "informe"]}.items():
        faltan = [c for c in campos if f'"{c}"' not in fuente]
        anota(not faltan and all(f"`{c}`" in parrafo(ct) or c == "FIABILIDAD_FUENTES" for c in campos),
              f"{ct}: los campos que el Anexo B nombra están en el código que lo emite" + (f" (faltan {faltan})" if faltan else ""))


def main() -> int:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        ct04_sin_los_cuatro_bloques(tmp)
        ct03_escalado_sin_ejecutar(tmp)
        ct09_fecha_corte(tmp)
    ct06_prosa_de_los_anidados()
    ct15_respuesta()
    lotes_y_auditoria()
    print(f"\n{len(HALLAZGOS)} hallazgos")
    return 1 if HALLAZGOS else 0


if __name__ == "__main__":
    sys.exit(main())
