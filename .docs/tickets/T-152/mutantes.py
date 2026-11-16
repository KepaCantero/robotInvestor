"""T-152 · mutantes del código nuevo de `cadena_a_b.py` (O-02 de la QA r01 de T-150) y de los bordes que fijan sus pruebas.

Uso, desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-152/mutantes.py <copia desechable con «t147_mut»> [--grupo FB|CB|CAB|BCE]
Cada mutante cambia un texto que aparece exactamente una vez, ejecuta las pruebas de T-150 y T-149 (y las de T-144 en
FB), restaura el fichero e imprime MUERTO o VIVO. Termina con 1 si alguno sobrevive. Sin red ni coste. Los mutantes del
revisor (Y01, Z03, W01, X01) están en `.docs/tickets/T-150/revisores/r01_04_mutantes_qa.py`; estos son otros."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t147_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "copia desechable"
SOLO = sys.argv[sys.argv.index("--grupo") + 1] if "--grupo" in sys.argv else None
A = "bloque_a/11_Ejecutor/bloque_a/"
FB, CB = A + "motor/frontera_b.py", A + "cadena_b.py"
CAB, BCE = ".docs/scripts/cadena_a_b.py", ".docs/scripts/descargar_datos_bce.py"
P_FB = ["tests/test_t150.py", "tests/test_t149.py", "tests/test_t144.py"]
P = ["tests/test_t150.py", "tests/test_t149.py"]
MUTANTES = [   # (grupo, nombre, fichero, texto, sustituto, pruebas)
    ("FB", "U1 el umbral a la mitad (q/p ≤ 0,5 %)", FB, "    desplaza = 2 * rel <= tol\n", "    desplaza = 4 * rel <= tol\n", P_FB),
    ("FB", "U2 el umbral un 10 % más alto (la resolución medida de la prueba)", FB, "    desplaza = 2 * rel <= tol\n",
     "    desplaza = 2 * rel <= 1.10 * tol\n", P_FB),
    ("FB", "U2b el umbral un 5 % más bajo (la resolución medida de la prueba)", FB, "    desplaza = 2 * rel <= tol\n",
     "    desplaza = 2 * rel <= 0.95 * tol\n", P_FB),
    ("CB", "U3 una unión que toca la anterior empieza otra vez", CB, "            unidos[-1][1] = max(unidos[-1][1], final)",
     "            unidos[-1][1] = max(unidos[-1][1], final) if final > unidos[-1][1] else unidos[-1][0]", P),
    ("CAB", "K1 sin mirar la forma del paquete", CAB, "            _forma_paquete(paquete)   # T-152", "            pass   # T-152", P),
    ("CAB", "K2 sin mirar «clases»", CAB, "    if clases is not None and not isinstance(clases, dict):", "    if False:", P),
    ("CAB", "K3 sin mirar cada clase", CAB, "        if clase is not None and not isinstance(clase, dict):", "        if False:", P),
    ("CAB", "K4 sin mirar las opciones", CAB, "        if opciones is not None and not isinstance(opciones, list):",
     "        if False:", P),
    ("CAB", "K5 un opp_id ausente se admite", CAB, 'if isinstance(o, dict) and not isinstance(o.get("opp_id"), str):',
     'if isinstance(o, dict) and "opp_id" in o and not isinstance(o["opp_id"], (str, list)):', P),
    ("CAB", "K6 sin mirar paquete_para_bloque_B", CAB, "    if entradas is not None and not isinstance(entradas, list):",
     "    if False:", P),
    ("CAB", "K7 sin mirar los textos de la correspondencia", CAB, "    if raros:\n", "    if False:\n", P),
    ("CAB", "K8 solo los valores de la correspondencia, no los símbolos", CAB,
     "for kv in (corr or {}).items() for x in kv if not isinstance(x, str)",
     "for x in (corr or {}).values() if not isinstance(x, str)", P),
    ("CAB", "K9 el motivo de la forma con el contenido", CAB,
     'raise TypeError(f"«paquete_para_bloque_B» no es una lista sino {type(entradas).__name__}")',
     'raise TypeError(f"«paquete_para_bloque_B» no es una lista sino {entradas}")', P),
    ("CAB", "K10 el TypeError de la forma deja de ser motivo de PAQUETE_ILEGIBLE", CAB,
     "        except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError) as e:",
     "        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:", P),
    ("BCE", "B1 el traslado a medias no nombra el último que se escribió", BCE,
     "                    raise EscrituraIncompleta(movidos, e) from e", "                    raise EscrituraIncompleta(movidos[:-1] or movidos, e) from e",
     P),
]
vivos = 0
for grupo, nombre, rel, viejo, nuevo, pruebas in MUTANTES:
    if SOLO and grupo != SOLO:
        continue
    ruta = COPIA / rel
    original = ruta.read_text(encoding="utf-8")
    assert original.count(viejo) == 1, f"{nombre}: el texto aparece {original.count(viejo)} veces"
    ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas],
                           cwd=COPIA / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, check=False)
    finally:
        ruta.write_text(original, encoding="utf-8")
    assert r.returncode in (0, 1), r.stdout[-1500:] + r.stderr[-1500:]
    muerto = r.returncode == 1
    vivos += not muerto
    print(f"{grupo:3} {nombre:72} {'MUERTO' if muerto else 'VIVO':7} {r.stdout.strip().splitlines()[-1][:60]}", flush=True)
print(f"\n{vivos} vivos")
sys.exit(1 if vivos else 0)
