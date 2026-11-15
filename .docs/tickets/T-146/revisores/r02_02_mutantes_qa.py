"""QA r02 de T-146 · mutantes propios del revisor sobre los arreglos de la r02 (distintos de M01–M35 de `mutantes_t146.py` y
de Q01–Q12 de `r01_05_mutantes_qa.py`).

Uso: python r02_02_mutantes_qa.py <copia desechable con «qa21_» y «_mut» en la ruta y `bloque_a/` entero>
Cada mutante se aplica, se pasan `tests/test_t146_presupuesto.py`, `tests/test_t88_consumo.py` y `tests/test_fase4_huecos.py`
(con -x) y se restaura. Vivo = ninguna prueba lo detecta. Termina con 1 si alguno no aplica (texto no encontrado una vez)."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa21_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
CO, AG, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("consumo", "agentes", "orquestacion"))
PRUEBAS = ["tests/test_t146_presupuesto.py", "tests/test_t88_consumo.py", "tests/test_fase4_huecos.py"]
MUT = [
    ("V01", "H-02: el exceso se compara con lo real con la lectura (depende del orden de los hilos)", CO,
     "        if real > w + 1e-4:", "        if self.cont.uc_de(uso) > w + 1e-4:"),
    ("V02", "H-03: el peor reparto de C5 toma el nivel de menos presupuesto", OR,
     "            n = max((\"N1\", \"N2\"), key=", "            n = min((\"N1\", \"N2\"), key="),
    ("V03", "H-05: la llamada que se cae no suelta su reserva", OR,
     "                presupuesto.cargar(bolsa, guarda.apartado)\n                guarda.cerrar()\n",
     "                presupuesto.cargar(bolsa, guarda.apartado)\n"),
    ("V04", "H-05: solo las Exception cargan lo pagado (no KeyboardInterrupt)", OR, "        except BaseException:\n            if guarda",
     "        except Exception:\n            if guarda"),
    ("V05", "H-05: R8 sin comprobar por lo anidado deja pasar (falla abierto)", AG,
     "        except RecursionError:   # T-146 r02 (H-05): demasiado anidado para comprobarlo: falla cerrado\n"
     "                    con_credenciales = True",
     "        except RecursionError:   # T-146 r02 (H-05): demasiado anidado para comprobarlo: falla cerrado\n"
     "                    con_credenciales = False"),
    ("V06", "H-01/H-04: el exceso no dice cuántas búsquedas hizo", CO, ",\n                                      \"busquedas_web\": int(uso.busquedas_web)})",
     "})"),
    ("V07", "H-04: lectura por búsqueda negativa aceptada", CO, "        if self.lectura_por_busqueda < 0:", "        if False:"),
    ("V08", "H-06: F5 sin escala_presupuesto", OR, "if presupuesto.escala < 1 else {}),   # T-146 r02 (H-06)",
     "if False else {}),   # T-146 r02 (H-06)"),
    ("V09", "H-02: el prefijo de la primera petición solo cuenta lo escrito (depende del orden)", CO,
     "            self.prefijo = uso.cache_lectura + uso.cache_escritura", "            self.prefijo = uso.cache_escritura"),
    ("V10", "H-03: la bolsa de C5 es la base del peor reparto aunque pase del mínimo de antes", OR,
     "        return min(minimo, peor.base(\"COMUN\"))", "        return peor.base(\"COMUN\")"),
]

vivos, no_aplica = [], []
for mid, desc, rel, viejo, nuevo in MUT:
    f = COPIA / rel
    orig = f.read_text(encoding="utf-8")
    if orig.count(viejo) != 1:
        print(f"{mid} NO APLICA ({orig.count(viejo)} apariciones) · {desc}", flush=True)
        no_aplica.append(mid)
        continue
    f.write_text(orig.replace(viejo, nuevo), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=COPIA / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, timeout=3600)
        muerto = r.returncode != 0
    finally:
        f.write_text(orig, encoding="utf-8")
    print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {desc}", flush=True)
    if not muerto:
        vivos.append(mid)
print(f"{len(MUT) - len(vivos) - len(no_aplica)}/{len(MUT)} muertos; vivos: {', '.join(vivos) or 'ninguno'}; "
      f"no aplican: {', '.join(no_aplica) or 'ninguno'}")
sys.exit(1 if no_aplica else 0)
