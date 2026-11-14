"""T-113 r02 · Mutantes de las correcciones de la ronda r02 (H-01, H-02, H-03, H-06 y H-07): deshace cada una y comprueba que
`tests/test_t113_deuda.py` lo detecta. Mismo método que `revisores/r01_11_mutantes.py`: una copia de `bloque_a/` por mutante,
una sola mutación textual (que debe aparecer una vez), uno detrás de otro.
Uso: python r02_mutantes_propios.py <raíz de una copia> <carpeta_mutantes> [ids separados por comas]"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ, DEST = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
SOLO = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
E = "bloque_a/"
M = [
    ("R01", E + "llm.py", "for d in _diccionarios_de_arriba(valor):", "for d in ([valor] if isinstance(valor, dict) else []):",
     "H-01: solo se serializa el diccionario de arriba (la r01)"),
    ("R02", E + "llm.py", '        elif id(x) in camino:\n            raise ValueError("estructura cíclica")\n', "", "H-01: una lista cíclica no falla cerrado"),
    ("R03", E + "llm.py", "    except ValueError:   # r02 (H-01): una estructura que se contiene a sí misma no se puede comprobar: falla cerrado\n        return True",
     "    except ValueError:\n        pass", "H-01: un diccionario cíclico no falla cerrado"),
    ("R04", E + "llm.py", "            if id(x) in vistos:\n                continue\n            vistos.add(id(x))\n", "            vistos.add(id(x))\n", "H-01: las hojas de una lista repetida se miran cada vez"),
    ("R05", E + "llm.py", "        elif id(x) in vistos:\n            continue\n", "", "H-01: los diccionarios de una lista repetida se buscan cada vez"),
    ("R06", E + "llm.py", "                if d is valor:         # cuelga de una lista, después de mirar el resto: un secreto hallado pesa más)\n                    raise\n", "",
     "H-01: el diccionario de arriba con claves que no son texto ya no es TypeError si hay un secreto"),
    ("R07", E + "llm.py", "    if sin_serializar is not None:\n        raise sin_serializar\n", "", "H-01: claves que no son texto bajo una lista, en silencio"),
    ("R08", E + "herramientas/ht06_indice.py", "            acabar_en_salto(self.ruta)   # r02 (H-02)\n", "", "H-02: la caché no deja el fichero acabado en salto"),
    ("R09", E + "llm.py", '            if modo == "grabar":   # r02', '            if False:   # r02', "H-02: la cinta no deja el fichero acabado en salto"),
    ("R10", E + "llm.py", '            if modo == "grabar":   # r02', '            if True:   # r02', "H-02: reproducir también escribe en la cinta"),
    ("R11", E + "herramientas/ht06_indice.py", '            json.loads(cola.decode("utf-8"))\n            fh.write(b"\\n")', '            json.loads(cola.decode("utf-8"))',
     "H-02: a una última línea entera sin salto no se le pone"),
    ("R12", E + "herramientas/ht06_indice.py", "            fh.truncate(len(datos) - len(cola))", '            fh.write(b"\\n")', "H-02: la línea cortada no se quita, se le pone un salto"),
    ("R13", E + "herramientas/ht06_indice.py", "        except (ValueError, RecursionError) as exc:   # UnicodeDecodeError", "        except ValueError as exc:   # UnicodeDecodeError",
     "H-06: una línea demasiado anidada vuelve a lanzar"),
    ("R14", E + "herramientas/ht06_indice.py", 'if isinstance(d, dict) and not isinstance(d.get("clave"), str):', "if False:", "H-06: una clave que no es texto vuelve a lanzar"),
    ("R15", E + "llm.py", 'if not isinstance(d, dict) or not isinstance(d.get("clave"), str):', 'if not isinstance(d, dict) or "clave" not in d:', "H-06: la cinta, TypeError"),
    ("R16", E + "orquestacion.py", '            if n:\n                self.almacen.incidencia("HERRAMIENTA", f"{fichero}:', '            if False:\n                self.almacen.incidencia("HERRAMIENTA", f"{fichero}:',
     "H-02: las líneas descartadas no se declaran"),
    ("R17", E + "diseno_v6.py", 'if any(m.group(1) not in perm["codigos"] for m in re.finditer(', "if any(True for m in re.finditer(", "H-03: una sigla permitida que es un romano es cifra"),
    ("R18", E + "diseno_v6.py", 'r"(?=[IVX]{2,}\\b)(X{1,3}', 'r"(X{1,3}', "H-03: una letra sola («los V») es cifra"),
    ("R19", E + "diseno_v6.py", "(X{1,3}(?:IX|IV|V?I{0,3})|IX|IV|VI{0,3}|I{2,3})\\b", "((?:X{0,3})(?:IX|IV|V?I{0,3}))\\b", "H-03: la expresión vuelve a admitir la coincidencia vacía"),
    ("R20", E + "diseno_v6.py", "                                   and x != _SIN_SINTESIS] + [_SIN_SINTESIS]\n", "                                   and x != _SIN_SINTESIS]\n",
     "H-07: sin respuesta válida no se declara"),
    ("R21", E + "diseno_v6.py", "if not x.startswith(previa) and x != _SIN_SINTESIS]", "if not x.startswith(previa)]", "H-07: el aviso no se retira con una reescritura válida"),
]


def correr(m):
    mid, fich, viejo, nuevo, desc = m
    tmp = DEST / f"m_{mid}"
    shutil.rmtree(tmp, ignore_errors=True)
    try:
        shutil.copytree(RAIZ / "bloque_a", tmp / "bloque_a", ignore=shutil.ignore_patterns("*.docx", "*.png", "__pycache__", "estado_bloque_a"))
        ej = tmp / "bloque_a" / "11_Ejecutor"
        p = ej / fich
        s = p.read_text(encoding="utf-8")
        if s.count(viejo) != 1:
            return f"NO APLICA ({s.count(viejo)} apariciones)", ""
        p.write_text(s.replace(viejo, nuevo), encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t113_deuda.py"], cwd=ej,
                           capture_output=True, text=True, timeout=1200)
        fallida = next((ln for ln in r.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))), "")
        return ("MATADO" if r.returncode == 1 else "SOBREVIVE" if r.returncode == 0 else f"ERROR (código {r.returncode})"), fallida[:150]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    vivos = []
    for m in M:
        if SOLO and m[0] not in SOLO:
            continue
        estado, detalle = correr(m)
        print(f"[{estado}] {m[0]} {m[4]} · {detalle}", flush=True)
        if not estado.startswith("MATADO"):
            vivos.append(m[0])
    print("NO MATADOS:", vivos)
