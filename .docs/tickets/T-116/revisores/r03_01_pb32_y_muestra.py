"""QA r03 de T-116 · PB-32 con TODAS las pruebas que el mapa cita ahora, y una muestra de seis filas AUTOMATICA ya leídas.

1. PB-32: los cuatro mutantes de la r02 (P32a a P32d) y cuatro nuevos (Holm sin aplicar en el Evaluador o en el criterio, el
   Evaluador que ignora el criterio, y un certificado por clase y horizonte sin método) contra las pruebas del ejecutor que
   el mapa cita para PB-32 (se leen del mapa: si el mapa cambia, cambia lo que se ejecuta).
2. Muestra (PB-06, PB-14, PB-33, PB-56, PB-60 y PB-64): un mutante por fila que rompe una cláusula del plan y se enfrenta a
   las pruebas del ejecutor que el mapa cita para esa fila. MUERTO = alguna falla; VIVO = todas pasan.
3. PB-60 a mano: con una credencial denegada y un ciclo simulado, ¿declaran los entregables la degradación?

Uso:  python r03_01_pb32_y_muestra.py <copia desechable de bloque_a/11_Ejecutor, con «qa2_mut» en la ruta> [--solo P32e,S60a]
Trabaja solo en la copia; restaura cada fichero al acabar. Termina con 0: es una medida.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
ej = Path(sys.argv[1]).resolve()
assert "qa2_mut" in str(ej) and (ej / "bloque_a" / "almacen.py").exists(), "solo en una copia desechable de 11_Ejecutor"
solo = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
MAPA = json.loads((ej / "tests" / "mapa_plan_pruebas.json").read_text(encoding="utf-8"))


def citadas(pb: str) -> list[str]:
    return [p.split("11_Ejecutor/", 1)[1] for p in MAPA[pb]["pruebas"] if p.startswith("11_Ejecutor/")]


EVA, EVL, ORQ, IB = "bloque_a/motor/evaluacion.py", "bloque_a/evaluador.py", "bloque_a/orquestacion.py", "bloque_a/interfaz_broker.py"
MUT = [
    # ---- PB-32 (los de la r02)
    ("P32a", "PB-32", EVA, "el IC del BSS ya no cuenta", "if ic[0] is None or ic[0] <= 0:", "if False:"),
    ("P32b", "PB-32", EVA, "la calibración frente al nulo ya no cuenta", "if e is None or q90 is None or e > q90:", "if False:"),
    ("P32c", "PB-32", EVA, "el tope de ECE ya no cuenta", "if e is None or e >= ece_max:", "if False:"),
    ("P32d", "PB-32", EVA, "la muestra mínima ya no cuenta", "elif not (math.isfinite(n_eff) and n_eff >= n_min):", "elif False:"),
    # ---- PB-32 (nuevos)
    ("P32e", "PB-32", EVL, "Holm no se aplica: el Evaluador no pasa el umbral corregido",
     'umbrales[etiqueta_celda(k)] if len(metr) > 1 else None)', 'None)'),
    ("P32f", "PB-32", EVA, "Holm no se aplica: el criterio ignora alfa_holm", "    if alfa_holm is not None:\n", "    if False:\n"),
    ("P32g", "PB-32", EVL, "el Evaluador emite certificado aunque el criterio diga que no",
     'if crit["certificable"] and k not in vigentes and k not in propuestos:', 'if k not in vigentes and k not in propuestos:'),
    ("P32h", "PB-32", EVL, "las celdas se agrupan sin el método (un certificado por clase y horizonte)",
     'celdas[(p["clase"], p["horizonte"], p.get("metodo"))].append(p)', 'celdas[(p["clase"], p["horizonte"], None)].append(p)'),
    # ---- muestra
    ("S06", "PB-06", ORQ, "la respuesta N0 lleva una referencia que no existe",
     'refs = [x for x in d.get("referencias", []) if x in conocidos]',
     'refs = [x for x in d.get("referencias", []) if x in conocidos] + ["OPP-2099-9999"]'),
    ("S14", "PB-14", ORQ, "control: el arrastre ya no cierra la opción invalidada (debe morir)",
     "            self._deduplicar_entre_tipos(seleccion)", "            self._deduplicar_entre_tipos(seleccion)"),   # sustituido abajo
    ("S33", "PB-33", EVL, "no se genera la alerta (lección) de sobreconfianza",
     'if cg and cg.get("p_media") is not None and cg["p_media"] - cg["frecuencia"] >= 0.10:', 'if False:'),
    ("S56", "PB-56", ORQ, "el ciclo C1 ya no quita los duplicados entre tipos",
     "            self._deduplicar_entre_tipos(seleccion)\n", "            pass\n"),
    ("S60a", "PB-60", IB, "una credencial denegada no se vuelve a pedir NUNCA (ni con cambio de circunstancias)",
     'if any(c.get("estado") == "DENEGADA" for c in previas) and not cambio_circunstancias:',
     'if any(c.get("estado") == "DENEGADA" for c in previas):'),
    ("S60b", "PB-60", IB, "la denegación ya no deja la limitación en F10 (control: debe morir)",
     '        if estado == "DENEGADA":\n            self.b.almacen.escribir("F10"', '        if False:\n            self.b.almacen.escribir("F10"'),
    ("S64", "PB-64", EVL, "control: la revisión de certificados emite también para H5 (debe morir)",
     'celdas[(p["clase"], p["horizonte"], p.get("metodo"))].append(p)', 'celdas[(p["clase"], p["horizonte"], p.get("metodo"))].append(p)'),
]


def control_s14(texto: str) -> tuple[str, str] | None:
    """S14: el cierre por invalidación se anota con otro motivo (la prueba de PB-14 lo afirma)."""
    viejo = '"INVALIDACION"'
    return (viejo, '"OTRO_MOTIVO"') if texto.count(viejo) >= 1 else None


def main() -> int:
    vivos = []
    for mid, pb, fich, desc, viejo, nuevo in MUT:
        if solo and mid not in solo:
            continue
        ruta = ej / fich
        original = ruta.read_text(encoding="utf-8")
        texto = original
        if mid == "S14":
            par = control_s14(original)
            if par is None:
                print(f"{mid} · NO APLICADO · {desc}")
                continue
            texto = original.replace(*par)
        elif mid == "S64":
            print(f"{mid} · no se ejecuta (la r02 ya leyó PB-64; sin mutante propio) · {desc}")
            continue
        else:
            if original.count(viejo) != 1:
                print(f"{mid} · NO APLICADO ({original.count(viejo)} apariciones) · {desc}", flush=True)
                continue
            texto = original.replace(viejo, nuevo)
        pruebas = citadas(pb)
        try:
            ruta.write_text(texto, encoding="utf-8")
            r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", *pruebas], cwd=ej, capture_output=True, text=True)
            ult = (r.stdout + r.stderr).strip().splitlines()[-1][:90]
            print(f"{mid} · {pb} · {'MUERTO' if r.returncode else 'VIVO  '} · {desc} · {len(pruebas)} citadas · {ult}", flush=True)
            if r.returncode == 0:
                vivos.append(mid)
        finally:
            ruta.write_text(original, encoding="utf-8")
    print("vivos: " + (", ".join(vivos) or "ninguno"))
    if solo is None or "PB60" in solo:
        r = subprocess.run([PY, "-c", PB60], cwd=ej, capture_output=True, text=True)
        print("PB-60 a mano:", (r.stdout + r.stderr).strip()[-600:])
    return 0


PB60 = """
import sys, tempfile
from pathlib import Path
sys.path[:0] = ['.', 'tests']
from conftest import nuevo_bloque, AS_OF
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo
tmp = Path(tempfile.mkdtemp())
b = nuevo_bloque(tmp, cargar_universo(RUTA_UNIVERSO_EJEMPLO))
s = b.credenciales.solicitar('API de crédito privado', 'AG-09', 'Cribado ALT', 'Sin descuentos de secundario', as_of=AS_OF)
b.credenciales.responder({'crd_id': s['crd_id'], 'estado': 'DENEGADA', 'credencial_ref': None}, AS_OF)
r = b.ciclo(AS_OF, alcance={'clases': ['ALT', 'RV']})
textos = {k: Path(v).read_text(encoding='utf-8') for k, v in r['entregables'].items()}
claves = ('crédito privado', 'DEGRADADO', 'denegad', 'credencial', 'CRD-')
en = {k: [c for c in claves if c.lower() in t.lower()] for k, t in textos.items()}
print('limitaciones del paquete:', r['paquete'].get('limitaciones'))
print('menciones de la degradación en cada entregable:', en)
print('F10 la tiene:', any(e.get('tipo_entrada') == 'LIMITACION_SERVICIO' for e in b.almacen.leer('F10')))
print('los entregables declaran la degradación:', any(en.values()))
"""

if __name__ == "__main__":
    raise SystemExit(main())
