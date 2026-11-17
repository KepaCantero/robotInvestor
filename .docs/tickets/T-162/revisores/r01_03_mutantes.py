"""QA r01 de T-162 (revisor) · mutantes propios de `respuesta_final.py` y del cambio de `orquestacion.consulta`.

Uso, desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-162/revisores/r01_03_mutantes.py <copia desechable con «t162_mut»> [M01 M02 …]
La copia desechable se prepara así (desde la raíz): `git archive HEAD bloque_a | tar -x -C <copia>`, con `.venv` enlazado y
este directorio de revisores copiado en `<copia>/.docs/tickets/T-162/revisores/`.
Cada mutante cambia un texto que aparece exactamente una vez, ejecuta primero `tests/test_t162_respuesta_final.py` y, si
sobrevive, las sondas del revisor (`r01_01_sondas.py`); restaura el fichero e imprime MUERTO (T-162), MUERTO (sondas) o VIVO.
Los que se esperan equivalentes o de pura defensa llevan «(equiv.)». Termina con 1 si vive alguno no esperado. Sin red ni coste.
"""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t162_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "copia desechable"
SOLO = set(sys.argv[2:])
EJ = COPIA / "bloque_a" / "11_Ejecutor"
RF, OR = "bloque_a/respuesta_final.py", "bloque_a/orquestacion.py"
T162 = ["tests/test_t162_respuesta_final.py"]
SONDAS = [str(COPIA / ".docs" / "tickets" / "T-162" / "revisores" / "r01_01_sondas.py")]
MUTANTES = [   # (id, descripción, fichero, texto, sustituto, ¿equivalente o de defensa?)
    ("M01", "confianza: la más alta en vez de la más baja", RF, "return min(valores, key=CONFIANZAS.index)",
     "return max(valores, key=CONFIANZAS.index)", False),
    ("M02", "PRG- de cualquier RUN- de la opción", RF, 'if x.get("tipo_entrada") == "ALTA" and x.get("run_id") == run_id',
     'if x.get("tipo_entrada") == "ALTA"', False),
    ("M03", "sin idempotencia", RF, '        if previa is not None:\n            return {**previa, "repetido": True}',
     '        if False:\n            return {**previa, "repetido": True}', False),
    ("M04", "sin la transacción del almacén (carrera entre hilos y procesos)", RF,
     "with almacen._transaccion():   # comprobar", "with __import__('contextlib').nullcontext():   # comprobar", False),
    ("M05", "la incidencia copia el texto del error", OR, "fallo = type(e).__name__   #", 'fallo = f"{type(e).__name__}: {e}"   #', False),
    ("M06", "un RUN- que falla se da por COMPLETO", OR, 'escalado["estado_run"] = "FALLIDO"', 'escalado["estado_run"] = "COMPLETO"', False),
    ("M07", "tras el fallo no se busca el RUN- registrado", OR, 'escalado["run_id"] = next((x["id"] for x',
     'escalado["run_id"] = None and next((x["id"] for x', False),
    ("M08", "la excepción del RUN- se relanza (comportamiento anterior)", OR, '                    escalado["estado_run"] = "FALLIDO"\n',
     '                    escalado["estado_run"] = "FALLIDO"\n                    raise\n', False),
    ("M09", "referencias sin comprobar que existen", RF, "referencias = [x for x in vistas if x in existentes]",
     "referencias = list(vistas)", False),
    ("M10", "OPP- del top-3 sin mirar `existentes` (F3 ya lo cubre)", RF, "if o is None or opp not in existentes:", "if o is None:", True),
    ("M11", "ENTREGADO_PARCIAL con estado COMPLETO", RF, '"ENTREGADO_PARCIAL": "PARCIAL"', '"ENTREGADO_PARCIAL": "COMPLETO"', False),
    ("M12", "un RUN- PARCIAL se da por completo", RF, 'return "ENTREGADO" if run.get("estado") == "COMPLETO" else "ENTREGADO_PARCIAL"',
     'return "ENTREGADO"', False),
    ("M13", "solo BLOQUEADA cuenta como sin entrega", RF, 'run.get("entrega", "ENTREGADA") != "ENTREGADA"',
     'run.get("entrega") == "BLOQUEADA"', False),
    ("M14", "validar no mira la coherencia del estado", RF,
     'if RESULTADOS[cuerpo["respuesta_final"]["resultado_analisis"]] != estado:', "if False:", False),
    ("M15", "esquema sin las reglas resultado → referencias (defensa)", RF, '    "allOf": [', '    "x_allOf": [', True),
    ("M16", "confianza no válida en F3 → establecido", RF, 'in CONFIANZAS else "especulativo"', 'in CONFIANZAS else "establecido"', False),
    ("M17", "la consulta N0 también envía final", OR, "as_of, fallo) if escalado is not None else None", "as_of, fallo)", False),
    ("M18", "el RUN- candidato aunque no conste en F5 (lo filtra `existentes`)", RF,
     "candidatas: list[str] = [run_id] if run_id and run is not None else []", "candidatas: list[str] = [run_id] if run_id else []", True),
    ("M19", "F5 marca RESPONDIDA_FINAL también sin resultado", RF, '"estado": ESTADO_F5[estado]', '"estado": "RESPONDIDA_FINAL"', False),
    ("M20", "el sobre lleva el RUN- aunque no conste en F5", RF, "return cuerpo, (run_id if run is not None else None),",
     "return cuerpo, run_id,", False),
    ("M21", "las limitaciones del RUN- no pasan a la final", RF, 'limitaciones = [x for x in (run or {}).get("limitaciones", [])',
     "limitaciones = [x for x in []", False),
    ("M22", "provisional_msg_id inventado", RF, '"respuesta_final": {"provisional_msg_id": provisional_msg_id,',
     '"respuesta_final": {"provisional_msg_id": "MSG-0",', False),
    ("M23", "sin validar contra el esquema", RF, "        validar(cuerpo, estado)\n", "", False),
    ("M24", "TND- y CLM- de la opción no se citan", RF,
     "candidatas += [opp, *(o.get(\"tnd_ids\") or [o.get(\"tnd_id\")]), *[x for x in o.get(\"evidencias\") or [] if isinstance(x, str)]]",
     "candidatas += [opp]", False),
    ("M25", "sin la incidencia en HA cuando falla el RUN-", OR,
     '                    self.almacen.incidencia("HERRAMIENTA", f"El análisis escalado de {qry_id} falló ({fallo})", "AG-01")\n', "", False),
]


def pytest(pruebas) -> bool:
    r = subprocess.run([str(COPIA / ".venv" / "bin" / "python"), "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "-W", "ignore",
                        *pruebas], cwd=EJ, capture_output=True, text=True, timeout=3000, check=False)
    return r.returncode == 0


vivos_inesperados = []
for mid, desc, fichero, texto, sustituto, equiv in MUTANTES:
    if SOLO and mid not in SOLO:
        continue
    ruta = EJ / fichero
    original = ruta.read_text(encoding="utf-8")
    assert original.count(texto) == 1, f"{mid}: el texto aparece {original.count(texto)} veces"
    ruta.write_text(original.replace(texto, sustituto), encoding="utf-8")
    try:
        if not pytest(T162):
            veredicto = "MUERTO (T-162)"
        elif not pytest(SONDAS):
            veredicto = "MUERTO (sondas)"
        else:
            veredicto = "VIVO"
            if not equiv:
                vivos_inesperados.append(mid)
    finally:
        ruta.write_text(original, encoding="utf-8")
    print(f"{mid} {veredicto:16} {desc}{' (equiv.)' if equiv else ''}", flush=True)
print("vivos no esperados:", vivos_inesperados)
sys.exit(1 if vivos_inesperados else 0)
