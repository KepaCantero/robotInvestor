"""QA r04 de T-116 (revisor sin contexto): mutantes contra las pruebas que el mapa cita para cada fila.

Uso:  python .docs/tickets/T-116/revisores/r04_01_mutantes_clausulas.py <copia desechable de bloque_a, con «_mut» en la ruta>
Para cada mutante: aplica el cambio en la copia, ejecuta las pruebas que el mapa cita para su fila (del ejecutor y de
10_Herramientas) y la deja como estaba. MUERTO = alguna citada falla; VIVO = todas pasan con el mutante.
"""
import json
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "_mut" in str(COPIA) and (COPIA / "11_Ejecutor" / "bloque_a").is_dir(), "hace falta una copia desechable de bloque_a con «_mut»"
MAPA = json.loads((COPIA / "11_Ejecutor" / "tests" / "mapa_plan_pruebas.json").read_text(encoding="utf-8"))
PY = sys.executable

# (id, fila, qué rompe, archivo relativo a bloque_a, texto original, texto mutado)
MUTANTES = [
    ("M31", "PB-31", "la banda verbal de cada horizonte publicado deja de seguir a la probabilidad interna (siempre «incierto»)",
     "11_Ejecutor/bloque_a/sintesis.py",
     '"banda": bloque.evaluador.banda_publicable(d["prob_interna"]), "prob": d["prob_interna"] if cert else None',
     '"banda": "incierto", "prob": d["prob_interna"] if cert else None'),
    ("M37a", "PB-37", "el Evaluador deja de resolver las correcciones (PRG con version_de)",
     "11_Ejecutor/bloque_a/evaluador.py",
     'pendientes = [p for p in abiertos if pd.Timestamp(p["fecha_resolucion"]) <= as_of and p.get("prob_interna") is not None]',
     'pendientes = [p for p in abiertos if pd.Timestamp(p["fecha_resolucion"]) <= as_of and p.get("prob_interna") is not None and not p.get("version_de")]'),
    ("M37b", "PB-37", "el Evaluador deja de resolver el original de un PRG corregido",
     "11_Ejecutor/bloque_a/evaluador.py",
     'pendientes = [p for p in abiertos if pd.Timestamp(p["fecha_resolucion"]) <= as_of and p.get("prob_interna") is not None]',
     'pendientes = [p for p in abiertos if pd.Timestamp(p["fecha_resolucion"]) <= as_of and p.get("prob_interna") is not None and p["prg_id"] not in {x.get("version_de") for x in abiertos}]'),
    ("M22", "PB-22", "la incidencia de canal no previsto deja de marcarse como escalada (corrección r04)",
     "11_Ejecutor/bloque_a/contratos.py",
     'tratamiento="rechazada y registrada", escalado_operador=True)\n            raise CanalNoPrevisto(f"{msg[\'emisor\']}',
     'tratamiento="rechazada y registrada")\n            raise CanalNoPrevisto(f"{msg[\'emisor\']}'),
    ("M60a", "PB-60", "los entregables dejan de declarar la degradación (corrección r04)",
     "11_Ejecutor/bloque_a/interfaz_broker.py",
     '        as_of = pd.Timestamp(as_of)\n        por_servicio: dict[str, dict] = {}',
     '        return []\n        as_of = pd.Timestamp(as_of)\n        por_servicio: dict[str, dict] = {}'),
    ("M60b", "PB-60", "con cambio de circunstancias tampoco se vuelve a pedir",
     "11_Ejecutor/bloque_a/interfaz_broker.py",
     'if any(c.get("estado") == "DENEGADA" for c in previas) and not cambio_circunstancias:',
     'if any(c.get("estado") == "DENEGADA" for c in previas):'),
    ("M58", "PB-58", "una solicitud pendiente deja de declararse como degradada (solo las denegadas)",
     "11_Ejecutor/bloque_a/interfaz_broker.py",
     'if c.get("estado") in ("SOLICITADA", "APLAZADA") and c.get("servicio"):',
     'if False and c.get("servicio"):'),
    ("M56", "PB-56", "el C1 deja de llamar a la regla de duplicados entre tipos (S56 de la r03)",
     "11_Ejecutor/bloque_a/orquestacion.py",
     "            self._deduplicar_entre_tipos(seleccion)\n        if self.v6:",
     "            pass\n        if self.v6:"),
    ("M33", "PB-33", "no se genera la alerta de sobreconfianza (S33 de la r03)",
     "11_Ejecutor/bloque_a/evaluador.py",
     'f"Sobreconfianza en {c}×{h}: probabilidad',
     'f"Calibración de {c}×{h}: probabilidad'),
]


def citadas(fila):
    out = {"11_Ejecutor": [], "10_Herramientas": []}
    for p in MAPA[fila]["pruebas"]:
        raiz, resto = p.split("/", 1)
        out[raiz].append(resto)
    return out


def ejecutar(fila):
    fallos = 0
    for raiz, pruebas in citadas(fila).items():
        if not pruebas:
            continue
        r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", *pruebas], cwd=COPIA / raiz,
                           capture_output=True, text=True)
        if r.returncode not in (0, 1):
            print(r.stdout[-2000:], r.stderr[-2000:])
            raise SystemExit(f"error al ejecutar las pruebas de {fila} en {raiz}")
        if r.returncode == 1:
            fallos += sum(int(x.split()[0]) for x in r.stdout.splitlines()[-1].split(", ") if "failed" in x) or 1
    return fallos


for mid, fila, que, rel, viejo, nuevo in MUTANTES:
    ruta = COPIA / rel
    original = ruta.read_text(encoding="utf-8")
    assert original.count(viejo) == 1, f"{mid}: el texto original no aparece exactamente una vez en {rel}"
    ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
    try:
        n = ejecutar(fila)
    finally:
        ruta.write_text(original, encoding="utf-8")
    total = sum(len(v) for v in citadas(fila).values())
    print(f"{mid} | {fila} | {que} | citadas {total} | {'MUERTO (' + str(n) + ' fallan)' if n else 'VIVO'}", flush=True)
