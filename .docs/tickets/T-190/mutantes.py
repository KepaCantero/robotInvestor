"""T-190 · mutantes del código nuevo de `cadena_a_b.py` (H-02 de la QA r01 de T-152).

Uso, desde la raíz de la copia de trabajo:
  .venv/bin/python .docs/tickets/T-190/mutantes.py <copia desechable con «t147_mut»> [--grupo FB|CB|CAB|BCE]
Cada mutante cambia un texto que aparece exactamente una vez, ejecuta las pruebas de T-150 y T-149 (y las de T-144 en
FB), restaura el fichero e imprime MUERTO, VIVO o EQUIVALENTE (los que se esperan equivalentes). Termina con 1 si sobrevive
alguno que no se espera equivalente. Sin red ni coste. Los del umbral (H-01) están en
`.docs/tickets/T-152/mutantes.py` (U2, U5 y U6)."""
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
MUTANTES = [   # (grupo, nombre, fichero, texto, sustituto, pruebas[, ¿equivalente esperado?])
    ("CAB", "R1 un paquete anidado sin fin da traza", CAB, "    except RecursionError:\n        raise TypeError(",
     "    except ZeroDivisionError:\n        raise TypeError(", P),
    ("CAB", "R2 un --config-a anidado sin fin da traza", CAB, "    except RecursionError:   # T-190 (QA r01 de T-152, H-02)",
     "    except ZeroDivisionError:   # T-190 (QA r01 de T-152, H-02)", P),
    ("CAB", "R3 sin el respaldo con escapes para un sustituto", CAB, '        texto.encode("utf-8")\n', "        pass\n", P),
    ("CAB", "R4 se escribe directamente, sin temporal", CAB, "        tmp.write_bytes(datos_json)\n        os.replace(tmp, ruta)\n",
     "        ruta.write_bytes(datos_json)\n", P),
    ("CAB", "R5 el temporal no se borra si falla", CAB, "    finally:\n        tmp.unlink(missing_ok=True)\n    return ruta",
     "    finally:\n        pass\n    return ruta", P),
    ("CAB", "R6 la petición que no se escribe da traza", CAB,
     "            except OSError as e:   # T-190 (H-02): sin la petición escrita no se envía (antes, una traza)",
     "            except ZeroDivisionError as e:   # T-190 (H-02): sin la petición escrita no se envía (antes, una traza)", P),
    ("CAB", "R7 la sonda que no se escribe da traza", CAB, "                except OSError as e:   # T-190 (H-02)",
     "                except ZeroDivisionError as e:   # T-190 (H-02)", P),
    ("CAB", "R8 el motivo lleva la ruta (con el opp_id)", CAB,
     "sin la ruta (lleva el `opp_id`).\"\"\"\n    return f\"{type(e).__name__}: {e.strerror or 'sin descripción'}\"",
     "sin la ruta (lleva el `opp_id`).\"\"\"\n    return f\"{type(e).__name__}: {e}\"", P),
    ("CAB", "R9 la salida impresa sin el respaldo con escapes", CAB, "    print(_json(_resumen(w, resumen)))",
     "    print(json.dumps(_resumen(w, resumen), ensure_ascii=False, indent=1))", P),
]
vivos = 0
for grupo, nombre, rel, viejo, nuevo, pruebas, *equiv in MUTANTES:
    equiv = bool(equiv and equiv[0])
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
    vivos += not muerto and not equiv
    estado = "MUERTO" if muerto else ("EQUIVALENTE" if equiv else "VIVO")
    print(f"{grupo:3} {nombre:72} {estado:11} {r.stdout.strip().splitlines()[-1][:60]}", flush=True)
print(f"\n{vivos} vivos (sin contar los equivalentes esperados)")
sys.exit(1 if vivos else 0)
