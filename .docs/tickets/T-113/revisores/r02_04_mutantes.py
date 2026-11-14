"""QA r02 de T-113 (y r01 de T-120) · Mutantes propios sobre las correcciones de la r02 y sobre T-120.
Mismo método que `r01_11_mutantes.py`: copia `bloque_a/` de la raíz dada a una carpeta por mutante, aplica UNA mutación textual
(que debe aparecer una sola vez) y ejecuta las pruebas del ticket; si sobrevive, las vecinas. Uno detrás de otro.
Uso: python r02_04_mutantes.py <raíz de una copia> <carpeta_mutantes> [ids separados por comas | todos]"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ, DEST = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
SOLO = set(sys.argv[3].split(",")) if len(sys.argv) > 3 and sys.argv[3] != "todos" else None
PY = "/home/user/robotinvestor/.venv/bin/python"
E = "bloque_a/"
T113 = ["tests/test_t113_deuda.py"]
T120 = ["tests/test_t120_r8_y_lecciones.py"]
VEC113 = ["tests/test_t102_filtro.py", "tests/test_t103_r8_y_bajos.py", "tests/test_t93_hallazgos.py", "tests/test_t92_revision.py",
          "tests/test_t101_v6.py"]
VEC120 = ["tests/test_t87_contratos.py", "tests/test_unitarias.py", "tests/test_t103_r8_y_bajos.py", "tests/test_t93_hallazgos.py",
          "tests/test_t116_aprendizaje.py"]
ROM = '(X{1,3}(?:IX|IV|V?I{0,3})|IX|IV|VI{0,3}|I{2,3})\\b", libre)):'
# (id, fichero, original, mutado, qué se deshace, pruebas, vecinas)
M = [
    ("A1", E + "llm.py", "            hallados.append(x)\n        elif isinstance(x, (list, tuple, set, frozenset)):",
     "            hallados.append(x)\n        elif isinstance(x, (list, set, frozenset)):", "H-01: no se baja por las tuplas", T113, VEC113),
    ("A1b", E + "llm.py", "            hallados.append(x)\n        elif isinstance(x, (list, tuple, set, frozenset)):",
     "            hallados.append(x)\n        elif isinstance(x, (list, tuple)):", "H-01: no se baja por los conjuntos", T113, VEC113),
    ("A2", E + "llm.py", '            raise ValueError("estructura cíclica")', "            continue", "H-01: una lista cíclica ya no falla cerrado", T113, VEC113),
    ("A4", E + "llm.py", "    except ValueError:   # r02 (H-01): una estructura que se contiene a sí misma no se puede comprobar: falla cerrado\n        return True",
     "    except ValueError:\n        return False", "H-01: un ciclo da False", T113, VEC113),
    ("A6", E + "llm.py", "    if sin_serializar is not None:\n        raise sin_serializar\n", "", "H-01: un diccionario que no se pudo serializar bajo una lista se da por limpio", T113, VEC113),
    ("A7", E + "llm.py", "            camino.discard(id(x))", "            pass", "H-01: la misma lista en dos sitios se toma por un ciclo", T113, VEC113),
    ("A9", E + "llm.py", "        for d in _diccionarios_de_arriba(valor):", "        for d in _diccionarios_de_arriba(valor)[:1]:", "H-01: solo se serializa el primer diccionario", T113, VEC113),
    ("A10", E + "llm.py", "        for d in _diccionarios_de_arriba(valor):", "        for d in _diccionarios_de_arriba(valor)[-1:]:", "H-01: solo se serializa el último diccionario hallado", T113, VEC113),
    ("A11", E + "llm.py", "                sin_serializar = sin_serializar or exc", "                raise", "H-01: una clave no texto bajo una lista corta antes de mirar el resto", T113, VEC113),
    ("B1", E + "herramientas/ht06_indice.py", "            fh.truncate(len(datos) - len(cola))", '            fh.write(b"\\n")', "H-02: la línea cortada no se quita, se le pone un salto", T113, VEC113),
    ("B2", E + "herramientas/ht06_indice.py", '            json.loads(cola.decode("utf-8"))\n            fh.write(b"\\n")', '            json.loads(cola.decode("utf-8"))',
     "H-02: a una última línea entera sin salto no se le pone", T113, VEC113),
    ("B3", E + "herramientas/ht06_indice.py", "            acabar_en_salto(self.ruta)   # r02 (H-02)\n", "", "H-02: la caché no se deja acabada en salto", T113, VEC113),
    ("B4", E + "llm.py", '            if modo == "grabar":   # r02 (QA r01, H-02): para seguir escribiendo; al reproducir no se toca', "            if True:",
     "H-02: al reproducir también se toca el fichero", T113, VEC113),
    ("B5", E + "llm.py", "                acabar_en_salto(self.ruta)\n", "                pass\n", "H-02: la cinta no se deja acabada en salto", T113, VEC113),
    ("B6", E + "herramientas/ht06_indice.py", "        except (ValueError, RecursionError) as exc:   # UnicodeDecodeError", "        except ValueError as exc:   # UnicodeDecodeError",
     "H-06: una línea demasiado anidada vuelve a romper el arranque", T113, VEC113),
    ("B7", E + "herramientas/ht06_indice.py", "        except (ValueError, RecursionError):\n            fh.truncate", "        except ValueError:\n            fh.truncate",
     "H-06: acabar_en_salto con una cola demasiado anidada lanza", T113, VEC113),
    ("B8", E + "llm.py", 'if not isinstance(d, dict) or not isinstance(d.get("clave"), str):', 'if not isinstance(d, dict) or "clave" not in d:',
     "H-06: la cinta admite una clave que no es texto", T113, VEC113),
    ("C1", E + "orquestacion.py", '("grabación del cliente", getattr(cliente, "descartadas", 0))):', '("grabación del cliente", 0)):',
     "H-02: lo descartado de la cinta no se declara", T113, VEC113),
    ("C2", E + "orquestacion.py", '(("cache_resultados.jsonl", self.cache.descartadas),', '(("cache_resultados.jsonl", 0),', "H-02: lo descartado de la caché no se declara", T113, VEC113),
    ("D1", E + "diseno_v6.py", 'if any(m.group(1) not in perm["codigos"] for m in re.finditer(', "if any(True for m in re.finditer(",
     "H-03: un romano que es sigla permitida vuelve a ser cifra", T113, VEC113),
    ("D3", E + "diseno_v6.py", ROM, '(IX|IV|VI{0,3}|I{2,3})\\b", libre)):', "H-03: los romanos de X en adelante dejan de ser cifra", T113, VEC113),
    ("D4", E + "diseno_v6.py", ROM, '(X{1,2}(?:IX|IV|V?I{0,3})|IX|IV|VI{0,3}|I{2,3})\\b", libre)):', "H-03: de XXX a XXXIX dejan de ser cifra", T113, VEC113),
    ("D5", E + "diseno_v6.py", ROM, '(X{0,3}(?:IX|IV|V?I{0,3}))\\b", libre)):', "H-03: vuelve la coincidencia vacía (con la anticipación nueva)", T113, VEC113),
    ("D6", E + "diseno_v6.py", '            r"(?=[IVX]{2,}\\b)(X{1,3}', '            r"(?=[IVXLC]{2,}\\b)(X{1,3}', "H-03: la anticipación vuelve a admitir L y C (equivalente si el grupo exige romano entero)", T113, VEC113),
    ("E1", E + "diseno_v6.py", "and x != _SIN_SINTESIS] + [_SIN_SINTESIS]", "and x != _SIN_SINTESIS]", "H-07: sin respuesta válida no se declara", T113, VEC113),
    ("E2", E + "diseno_v6.py", "if not x.startswith(previa) and x != _SIN_SINTESIS]", "if not x.startswith(previa)]",
     "H-07: la limitación se queda aunque una respuesta posterior valga", T113, VEC113),
    ("E3", E + "diseno_v6.py", 'if not x.startswith("Ninguna limitación")\n                                   and x != _SIN_SINTESIS]', "if x != _SIN_SINTESIS]",
     "H-07: «Ninguna limitación…» convive con la limitación nueva", T113, VEC113),
    ("F1", E + "contratos.py", "(?:[ .\\-]?\\d{4}){5}", "(?:\\d{4}){5}", "T-120: el IBAN solo se ve junto", T120, VEC120),
    ("F2", E + "contratos.py", "(?:[ .\\-]?\\d{4}){5}", "(?:[ ]?\\d{4}){5}", "T-120: ni punto ni guion", T120, VEC120),
    ("F3", E + "contratos.py", "(?:[ .\\-]?\\d{4}){5}", "(?:[ .\\-]*\\d{4}){5}", "T-120: varios separadores seguidos (más estricto; ¿lo fija alguna prueba?)", T120, VEC120),
    ("F4", E + "contratos.py", "(\\bES\\d{2}(?:[ .\\-]?\\d{4}){5}\\b)", "(\\bES\\d{2}(?:[ .\\-]?\\d{4}){5})", "T-120: sin límite de palabra al final", T120, VEC120),
    ("F5", E + "contratos.py", "(\\bES\\d{2}(?:[ .\\-]?\\d{4}){5}\\b)", "(\\bES\\d{2}(?:[ .\\-]?\\d{4}){4,5}\\b)", "T-120: basta con cuatro grupos", T120, VEC120),
    ("F6", E + "contratos.py", "(\\bES\\d{2}(?:[ .\\-]?\\d{4}){5}\\b)", "(\\bES[ .\\-]?\\d{2}(?:[ .\\-]?\\d{4}){5}\\b)", "T-120: separador también tras ES (más estricto)", T120, VEC120),
    ("G1", E + "evaluador.py", 'max_n = int(parametro(self.cfg, "aprendizaje.lecciones_por_encargo"))', "max_n = 10", "T-120: el máximo vuelve a ser un literal", T120, VEC120),
    ("G2", E + "evaluador.py", "        if max_n is None:\n            max_n = int(parametro", "        if True:\n            max_n = int(parametro",
     "T-120: el argumento explícito deja de mandar", T120, VEC120),
]


def pytest(ej, ficheros):
    r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *ficheros], cwd=ej, capture_output=True, text=True)
    fallida = next((ln for ln in r.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))), "")
    return r.returncode, (fallida or (r.stdout.strip().splitlines() or [""])[-1])[:150]


def correr(m):
    mid, fich, viejo, nuevo, desc, pruebas, vecinas = m
    tmp = DEST / f"m_{mid}"
    shutil.rmtree(tmp, ignore_errors=True)
    try:
        shutil.copytree(RAIZ / "bloque_a", tmp / "bloque_a", ignore=shutil.ignore_patterns("*.docx", "*.png", "__pycache__", "estado_bloque_a"))
        ej = tmp / "bloque_a" / "11_Ejecutor"
        p = ej / fich
        s = p.read_text(encoding="utf-8")
        if s.count(viejo) != 1:
            return mid, desc, f"NO APLICA ({s.count(viejo)} apariciones)", "", ""
        p.write_text(s.replace(viejo, nuevo), encoding="utf-8")
        c1, d1 = pytest(ej, pruebas)
        if c1 not in (0, 1):
            return mid, desc, f"ERROR (código {c1})", d1, ""
        if c1 == 1:
            return mid, desc, "MATADO por las pruebas del ticket", d1, ""
        existentes = [v for v in vecinas if (ej / v).exists()]
        c2, d2 = pytest(ej, existentes)
        return mid, desc, ("SOBREVIVE al ticket; MATADO por las vecinas" if c2 == 1 else "SOBREVIVE al ticket y a las vecinas"), d1, d2
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    vivos = []
    for m in M:
        if SOLO and m[0] not in SOLO:
            continue
        mid, desc, estado, d1, d2 = correr(m)
        print(f"[{estado}] {mid} {desc} · {d1}" + (f" · vecinas: {d2}" if d2 else ""), flush=True)
        if estado.startswith("SOBREVIVE"):
            vivos.append(mid)
    print("VIVOS frente a las pruebas del ticket:", vivos)
