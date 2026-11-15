"""T-99 r02 · Mutantes del registro de experimentos: cada uno debe morir ante sus pruebas y las del borrador de CT-G-24.

Trabaja en una copia de `.docs/scripts` en una carpeta temporal (nunca en el árbol principal) y sin la prueba de
integración sobre A, que necesita la raíz del repositorio. Uso: .venv/bin/python -B .docs/tickets/T-99/mutantes_r02.py"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
PY = RAIZ / ".venv" / "bin" / "python"
MUTANTES = {
    "R01 sin ancla en git": ("        if not self.ancla_git:\n            return", "        if True:\n            return"),
    "R02 ancla que no exige prefijo": ("if not texto.encode(\"utf-8\").startswith(en_head.stdout):", "if False:"),
    "R03 sin sello": ("        self._comprobar_sello(out[-1] if out else None)\n", ""),
    "R04 sello que admite que falte": ("            if ultima is not None:\n                raise RegistroError(f\"falta el sello",
                                       "            if False:\n                raise RegistroError(f\"falta el sello"),
    "R05 sin cerrojo": ("            fcntl.flock(fl.fileno(), fcntl.LOCK_EX)", "            pass"),
    "R06 huella del prerregistro sin contrastar": ('if e["huella_prerregistro"] != huella(e["contenido"]):', "if False:"),
    "R07 intento que cita otro prerregistro": ('if e["huella_prerregistro"] != pre[exp]["huella_prerregistro"]:', "if False:"),
    "R08 dentro_del_maximo guardado sin recalcular": ('if e["dentro_del_maximo"] != _dentro(previos, e["variante"], pre[exp]["contenido"]["max_variantes"]):',
                                                      "if False:"),
    "R09 EXP duplicado admitido": ("                if exp in pre:\n                    raise", "                if False:\n                    raise"),
    "R10 intento no correlativo admitido": ('if e["n"] != len(previos) + 1:', "if False:"),
    "R11 tipo desconocido admitido": ('if not isinstance(e, dict) or e.get("tipo") not in TIPOS:', "if not isinstance(e, dict):"),
    "R12 forma sin comprobar": ("    if claves != CAMPOS[tipo]:", "    if False:"),
    "R13 detalle que no es objeto": ('        if not isinstance(e["detalle"], dict):\n            raise RegistroError("«detalle»',
                                     '        if False:\n            raise RegistroError("«detalle»'),
    "R14 instantes como texto": ("_instante(primero[0][\"inicio\"], \"inicio\") >= creado", "primero[0][\"inicio\"] >= pre[\"creado_en\"]"),
    "R15 año del texto": ('anio = _instante(ahora, "ahora").year', "anio = int(ahora[:4])"),
    "R16 cuenta el último resultado de la variante": ("primero = con_veredicto[0] if con_veredicto else None", "primero = con_veredicto[-1] if con_veredicto else None"),
    "R17 contradicciones ignoradas": ('and not d["contradictoria"] and d["dentro_del_maximo"]', 'and d["dentro_del_maximo"]'),
    "R18 «fallido» cuenta como primero": ('if i["n"] in res and res[i["n"]]["veredicto"] != "fallido"]', 'if i["n"] in res]'),
    "R19 variante sin normalizar": ('return unicodedata.normalize("NFC", v)', "return v"),
    "R20 variante vacía admitida": ('    if not isinstance(v, str) or not v.strip():\n        raise RegistroError(f"la variante',
                                    '    if not isinstance(v, str):\n        raise RegistroError(f"la variante'),
    "R21 separadores Unicode sin escapar": ('return txt.replace("\\u2028", "\\\\u2028")', "return txt or txt.replace(\"\\u2028\", \"\\\\u2028\")"),
    "R22 fichero sin salto final admitido": ('        if texto and not texto.endswith("\\n"):\n            raise', '        if False:\n            raise'),
    "R23 lectura con splitlines": ('texto.split("\\n")[:-1] if texto else []', "texto.splitlines()"),
    "R24 NaN admitido en la huella": ("allow_nan=False)\n    except (TypeError, ValueError) as e:   # NaN", "allow_nan=True)\n    except (TypeError, ValueError) as e:   # NaN"),
    "R25 fechas imposibles": ("        return date.fromisoformat(txt)", "        return txt"),
    "R26 datos sin comprobar": ('    _texto(c["datos"], "datos")\n', ""),
    "R27 EXP sin tope": ("            if n > MAX_EXP_POR_ANIO:", "            if False:"),
    "R28 n booleano admitido": ("if isinstance(v, bool) or not isinstance(v, int)", "if not isinstance(v, int)"),
    "R29 main con traza": ("    except Exception as e:   # noqa: BLE001", "    except RegistroError as e:   # noqa: BLE001"),
    "R30 verificar de un registro que no existe": ("            if not r.ruta.exists():\n                raise", "            if False:\n                raise"),
}


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="t99_mut_"))
    try:
        copia = tmp / ".docs" / "scripts"
        shutil.copytree(RAIZ / ".docs" / "scripts", copia, ignore=shutil.ignore_patterns("__pycache__", ".logs"))
        fichero = copia / "registro_experimentos.py"
        original = fichero.read_text(encoding="utf-8")
        vivos = []
        for nombre, (viejo, nuevo) in MUTANTES.items():
            if original.count(viejo) != 1:
                print(f"??    {nombre}: el patrón no aparece una sola vez")
                vivos.append(nombre)
                continue
            fichero.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([str(PY), "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "-k", "not integracion",
                                str(copia / "pruebas_registro_experimentos.py"), str(copia / "pruebas_borradores_contratos.py")], cwd=tmp, capture_output=True, text=True, check=False)
            muerto = r.returncode != 0
            print(("MUERE " if muerto else "VIVO  ") + nombre)
            if not muerto:
                vivos.append(nombre)
        fichero.write_text(original, encoding="utf-8")
        print(f"\n{len(vivos)} vivo(s) de {len(MUTANTES)}: {vivos}")
        return 1 if vivos else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
