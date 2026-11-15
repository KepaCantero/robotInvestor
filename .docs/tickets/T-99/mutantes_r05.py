"""T-99 r05 · Mutantes del registro de experimentos: cada uno debe morir ante sus pruebas y las del borrador de CT-G-24.

Trabaja en una copia de `.docs/scripts` en una carpeta temporal (nunca en el árbol principal) y sin la prueba de
integración sobre A, que necesita la raíz del repositorio. Uso: .venv/bin/python -B .docs/tickets/T-99/mutantes_r05.py"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
PY = RAIZ / ".venv" / "bin" / "python"
MUTANTES = {
    "R01 sin ancla en git": ("        if not self.ancla_git:\n            return", "        if True:\n            return"),
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
    "R18 «fallido» cuenta como primero": ('if i["n"] in res and res[i["n"]]["veredicto"] != "fallido"]', 'if i["n"] in res]'),
    "R20 variante vacía admitida": ('    if not isinstance(v, str) or not v.strip():\n        raise RegistroError(f"la variante',
                                    '    if not isinstance(v, str):\n        raise RegistroError(f"la variante'),
    "R22 fichero sin salto final admitido": ('        if texto and not texto.endswith("\\n"):\n            raise', '        if False:\n            raise'),
    "R23 lectura con splitlines": ('texto.split("\\n")[:-1] if texto else []', "texto.splitlines()"),
    "R24 NaN admitido en la huella": ("allow_nan=False)\n    except (TypeError, ValueError) as e:   # NaN", "allow_nan=True)\n    except (TypeError, ValueError) as e:   # NaN"),
    "R25 fechas imposibles": ("        return date.fromisoformat(txt)", "        return txt"),
    "R26 datos sin comprobar": ('    _texto(c["datos"], "datos")\n', ""),
    "R27 EXP sin tope": ("            if n > MAX_EXP_POR_ANIO:", "            if False:"),
    "R28 n booleano admitido": ("if isinstance(v, bool) or not isinstance(v, int)", "if not isinstance(v, int)"),
    "R29 main con traza": ("    except Exception as e:   # noqa: BLE001", "    except RegistroError as e:   # noqa: BLE001"),
    "R30 verificar de un registro que no existe": ("            if not r.ruta.exists():\n                raise", "            if False:\n                raise"),
    "R16 cuenta el último resultado de la variante": ('primero = con_veredicto[0] if con_veredicto and primero_vivo', 'primero = con_veredicto[-1] if con_veredicto and primero_vivo'),
    "R17 contradicciones ignoradas": ('if d["veredicto"] == "mejor" and not d["contradictoria"] and not d["pendiente"]', 'if d["veredicto"] == "mejor" and not d["pendiente"]'),
    "R19 variante sin normalizar": ('        raise RegistroError(f"la variante tiene que ser un texto no vacío: {v!r}")\n    return unicodedata.normalize("NFC", v)',
                                    '        raise RegistroError(f"la variante tiene que ser un texto no vacío: {v!r}")\n    return v'),
    "R21 separadores Unicode sin escapar": ('    txt = txt.replace("\\u2028", "\\\\u2028")', '    txt = txt or txt.replace("\\u2028", "\\\\u2028")'),
    "S02 registro quitado del repositorio admitido": ('                    raise RegistroError(f"el registro se quitó del repositorio', '                    pass  # raise RegistroError(f"el registro se quitó del repositorio'),
    "U01 fusión anterior cuenta como borrado": ("                if any(version(p) is not None for p in padres):\n                    raise", "                if True:\n                    raise"),
    "U02 fallido tardío por instantes": ('and any(j["_seq"] < res[i["n"]]["_seq"] for j in suyos if j["n"] > i["n"])', 'and any(j["inicio"] < res[i["n"]]["registrado_en"] for j in suyos if j["n"] > i["n"])'),
    "U03 resultado anterior a su intento admitido": ('            if _instante(ahora, "ahora") < _instante(inicio, "inicio"):', "            if False:"),
    "U04 repetir con un intento abierto admitido": ("            if abiertos:   # QA r04, H-40", "            if False:   # QA r04, H-40"),
    "U05 sello junto al registro aunque haya git": ("            if raiz is not None and shutil.which(\"git\") is not None:", "            if False:"),
    "U06 lector sin permiso falla": ("            if compartido:   # H-39: quien solo puede leer", "            if False:   # H-39: quien solo puede leer"),
    "U07 RI_AGENTE no válido cae en claude": ("if AGENTE_VALIDO else None", "if AGENTE_VALIDO else RAIZ / \".docs\" / \"experimentos\" / \"registro_claude.jsonl\""),
    "U08 la marca a mano no se arrastra": ('if a_mano or getattr(self, "sello_a_mano", False):', "if a_mano:"),
    "U09 el escritor suelta el turno antes de esperar": ("                if compartido:   # el lector pasa por el turno y lo suelta enseguida\n", ""),
    "T01 sello por detrás más de uno admitido": ("        if k < len(out) - 1 and not (en_git is not None and texto.encode(\"utf-8\") == en_git):", "        if False:"),
    "T02 sello fuera de la cadena admitido": ("        if not en_cadena:\n            raise RegistroError(f\"el registro no casa con su sello", "        if False:\n            raise RegistroError(f\"el registro no casa con su sello"),
    "T03 sello por delante admitido": ("(1 <= k <= len(out) and out[k - 1][\"_hash\"] == s[\"hash\"])", "(1 <= k and (k > len(out) or out[k - 1][\"_hash\"] == s[\"hash\"]))"),
    "T04 git-dir roto admitido": ("        if dir_git.returncode != 0:   # «.git» vacío", "        if False:   # «.git» vacío"),
    "T05 HEAD ilegible como repositorio vacío": ("        if cabeza.returncode != 0:\n            raise RegistroError(f\"git no puede leer HEAD", "        if cabeza.returncode != 0:\n            return None\n            raise RegistroError(f\"git no puede leer HEAD"),
    "T06 rev-list que falla admitido": ("        if lista.returncode != 0:\n            raise RegistroError(f\"git no puede leer el historial", "        if False:\n            raise RegistroError(f\"git no puede leer el historial"),
    "T07 sin turno para el escritor": ("            self._esperar(turno, fcntl.LOCK_EX, \"esperando turno\")", "            pass"),
    "T08 escritura con cerrojo compartido": ("self._esperar(fl, fcntl.LOCK_SH if compartido else fcntl.LOCK_EX,", "self._esperar(fl, fcntl.LOCK_SH,"),
    "T09 cerrojo sin plazo": ("                if time.monotonic() > limite:", "                if False:"),
    "T10 escribe sin cerrojo fuera de POSIX": ("            if not compartido:\n                raise RegistroError(\"este sistema no tiene cerrojo", "            if False:\n                raise RegistroError(\"este sistema no tiene cerrojo"),
    "T11 pendiente ignorado": ('and not d["contradictoria"] and not d["pendiente"] and not d["fallido_tardio"]', 'and not d["contradictoria"] and not d["fallido_tardio"]'),
    "T12 fallido tardío ignorado": ('and not d["pendiente"] and not d["fallido_tardio"]', 'and not d["pendiente"]'),
    "T13 RI_AGENTE no válido cae en claude": ("            if not AGENTE_VALIDO:\n                raise RegistroError(f\"RI_AGENTE", "            if False:\n                raise RegistroError(f\"RI_AGENTE"),
    "T14 enlace simbólico sin resolver": ("        self.ruta = Path(os.path.realpath(ruta))", "        self.ruta = Path(ruta)"),
    "T15 registro ilegible como traza": ("        except OSError as e:   # un directorio o un fichero ilegible (H-20)", "        except ZeroDivisionError as e:   # un directorio o un fichero ilegible (H-20)"),
    "T16 sellar un registro con sello": ("            if con_sello:\n                raise RegistroError(f\"el registro lo escribió una versión con sello", "            if False:\n                raise RegistroError(f\"el registro lo escribió una versión con sello"),
    "T17 os.replace del sello que falla en silencio": ("        except OSError as ex:\n            raise RegistroError(f\"la anotación está escrita, pero no se pudo poner al día el sello", "        except OSError as ex:\n            return\n            raise RegistroError(f\"la anotación está escrita, pero no se pudo poner al día el sello"),
    "S01 ancla solo en HEAD": ("            for p in padres:\n                anterior = version(p)", "            for p in []:\n                anterior = version(p)"),
    "S03 sin ancla en HEAD": ("        if en_head is not None and not texto.encode(\"utf-8\").startswith(en_head):", "        if False:"),
    "S04 git ausente sin avisar": ("        if shutil.which(\"git\") is None:\n            raise", "        if shutil.which(\"git\") is None:\n            return None\n            raise"),
    "S05 GIT_DIR respetado": ("entorno = {k: v for k, v in os.environ.items() if not k.startswith(\"GIT_\")}", "entorno = dict(os.environ)"),
    "S06 objeto dañado ignorado": ("                    if blob.returncode != 0:\n                        raise", "                    if False:\n                        raise"),
    "S07 sello sin comprobar": ("        self._comprobar_sello(out, texto, en_git)\n", ""),
    "S08 sello que falta admitido siempre": ("            if ultima is None or len(out) == 1 or (en_git is not None and texto.encode(\"utf-8\") == en_git):", "            if True:"),
    "S12 lectores sin cerrojo": ("        with self._cerrojo(compartido=True):\n            return self._leer()", "        return self._leer()"),
    "S15 primero pendiente ignorado": ('primero = con_veredicto[0] if con_veredicto and primero_vivo is not None and primero_vivo["n"] in res else None', 'primero = con_veredicto[0] if con_veredicto else None'),
    "S16 búsqueda fuera del cerrojo": ("        construir = self._construir_prerregistro(datos, autor, ahora)\n        with self._cerrojo():\n            previas = self._leer()", "        construir = self._construir_prerregistro(datos, autor, ahora)\n        with contextlib.nullcontext():\n            previas = self._leer()"),
    "S17 intento sin registro crea carpeta": ("        if not self.ruta.exists():   # no se crea carpeta", "        if False:   # no se crea carpeta"),
    "S18 sello preparado después": ("        temporal = self._preparar_sello(e)   # antes de tocar", "        temporal = None   # antes de tocar"),
    "S19 sustituto en la huella": ("        return hashlib.sha256(txt.encode(\"utf-8\")).hexdigest()\n    except UnicodeEncodeError as e:", "        return hashlib.sha256(txt.encode(\"utf-8\", \"replace\")).hexdigest()\n    except UnicodeEncodeError as e:"),
    "S20 variantes antiguas sin normalizar": ('orden_variantes = list(dict.fromkeys(_nfc(i["variante"]) for i in intentos))', 'orden_variantes = list(dict.fromkeys(i["variante"] for i in intentos))'),
    "S21 sellar dos veces": ("            if self.sello.exists():\n                raise RegistroError(\"el registro ya tiene sello", "            if False:\n                raise RegistroError(\"el registro ya tiene sello"),
    "S22 detalle null en la línea de órdenes": ("            if not isinstance(detalle, dict):\n                raise RegistroError(\"«--detalle»", "            if False:\n                raise RegistroError(\"«--detalle»"),
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
