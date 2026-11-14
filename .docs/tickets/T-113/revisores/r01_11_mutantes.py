"""QA r01 de T-113 · Mutantes: deshace una a una las correcciones de T-113 (y repite los mutantes vivos de H-25 y H-51) y
comprueba que alguna prueba del paquete lo detecta.

Método (el de las rondas de T-102): copia `bloque_a/` de la raíz dada (sin docx, png ni cachés) a una carpeta por mutante bajo
<carpeta_mutantes>, aplica UNA mutación textual (que debe aparecer una sola vez) y ejecuta `tests/test_t113_deuda.py`. Si
sobrevive, ejecuta además las baterías vecinas (segunda columna de resultado). Uno detrás de otro, sin paralelismo.

Uso: python r01_11_mutantes.py <raíz de una copia> <carpeta_mutantes> [ids separados por comas | todos]"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RAIZ, DEST = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
SOLO = set(sys.argv[3].split(",")) if len(sys.argv) > 3 and sys.argv[3] != "todos" else None
PY = "/home/user/robotinvestor/.venv/bin/python"
E = "bloque_a/"
VECINAS = ["tests/test_t102_filtro.py", "tests/test_t106_r03.py", "tests/test_t103_r8_y_bajos.py", "tests/test_t93_hallazgos.py",
           "tests/test_t92_revision.py", "tests/test_t101_v6.py"]

# (id, fichero, original, mutado, qué se deshace)
M = [
    ("M01", E + "herramientas/ht06_indice.py", "ultima_cortada = i == len(trozos) - 1 and not datos.endswith(b\"\\n\")", "ultima_cortada = False",
     "H-54: la última línea cortada ya no se descarta (caché y cinta)"),
    ("M02", E + "herramientas/ht06_indice.py", "leer_jsonl(self.ruta, tolerar_todas=True)", "leer_jsonl(self.ruta)", "H-54: la caché no tolera una línea ilegible en medio"),
    ("M03", E + "herramientas/ht06_indice.py", 'if isinstance(d, dict) and "clave" in d and "valor" in d:', "if True:", "H-54: la caché no descarta un registro que no es {clave, valor}"),
    ("M04", E + "herramientas/ht06_indice.py", 'raise ValueError(f"{ruta}: línea {i + 1} ilegible ({type(exc).__name__}: {str(exc)[:120]})") from exc', "raise",
     "H-54: el error de la cinta no dice fichero ni línea"),
    ("M05", "pyproject.toml", 'requires-python = ">=3.12"', 'requires-python = ">=3.10"', "H-55: vuelve a declarar 3.10"),
    ("M06", E + "llm.py", "    pila: list = [valor]\n", "    if isinstance(valor, dict):\n        return any(contenido_sensible(v) for v in valor.values())\n    return any(contenido_sensible(v) for v in valor)\n    pila: list = [valor]\n",
     "H-56: vuelve a ser recursivo (profundidad × tamaño)"),
    ("M07", E + "llm.py", "    except RecursionError:   # demasiado anidado para serializarlo: no se puede comprobar, así que falla cerrado\n        return True",
     "    except RecursionError:\n        pass", "H-56: demasiado profundo no falla cerrado (pasa a recorrer hojas)"),
    ("M08", E + "llm.py", "            if secretos_en_texto(x + '\"'):\n                return True\n        elif isinstance(x, dict):", "            pass\n        elif isinstance(x, dict):",
     "H-56: las hojas de texto no se miran"),
    ("M09", E + "orquestacion.py", 'as_of, run_id, clase, "investigacion", presupuesto)   # T-113', 'as_of, run_id, clase, "investigacion")   # T-113', "H-14: la curación vuelve a ir sin presupuesto"),
    ("M10", E + "consumo.py", 'tot["uc_llm"] = self.uc_de(Uso(**sumados)) if ll else 0.0', 'tot["uc_llm"] = round(sum(c["uc"] for c in ll), 4)', "H-15: la UC total vuelve a sumar cifras redondeadas"),
    ("M11", E + "sintesis.py", 'for cz in sorted(presupuesto.cierres, key=lambda c: (c["clase"], c["fase"], c["motivo"])):', "for cz in presupuesto.cierres:", "H-16: limitaciones en el orden de los hilos"),
    ("M11b", E + "sintesis.py", 'for cz in sorted(presupuesto.cierres, key=lambda c: (c["clase"], c["fase"], c["motivo"])):',
     'for cz in (sorted(presupuesto.cierres, key=lambda c: (c["clase"], c["fase"], c["motivo"])) and presupuesto.cierres):', "H-16: igual, pero dejando el texto `sorted(...)` en la fuente"),
    ("M12", E + "motor/servicio.py", 'if not isinstance(peticion.get("plan", "PLAN_MIN"), str):', "if False:", "H-22: `plan` lista o dict vuelve a lanzar"),
    ("M13", E + "motor/servicio.py", "        except (TypeError, ValueError, RecursionError) as exc:\n            return f\"«parametros», «perfil», «clase» o «semilla» no serializables ({type(exc).__name__})\"",
     "        except ZeroDivisionError as exc:\n            return str(exc)", "H-22: campos no serializables vuelven a lanzar"),
    ("M14", E + "motor/fichas_mon_idx.py", '"incertidumbre_probabilidad": min(1.0, cota_mov[k - 1] / incremento),', '"incertidumbre_probabilidad": min(1.0, cota_r[k - 1] / incremento),',
     "H-23: la cota de la reunión vuelve a ser la del tipo"),
    ("M15", E + "motor/fichas_mon_idx.py", "    p.update(params or {})\n    _dominio(ficha, p)", "    p.update(params or {})", "H-24: sin dominios"),
    ("M16", E + "motor/fichas_mon_idx.py", 'if ficha == "IDX-REL-001" and p["momentum_salto_meses"] >= p["momentum_retro_meses"]:', 'if False:', "H-24: salto ≥ retro se sirve"),
    ("M17", E + "motor/fichas_mon_idx.py", 'if tipo in ("entero", "lista_entera") and float(e) != int(e):', "if False:", "H-24: 2,5 vuelve a valer como ventana"),
    ("M18", E + "motor/fichas_mon_idx.py", "if not (lo < float(e) <= hi if tipo == \"real_positivo\" else lo <= float(e) <= hi):", "if not (lo <= float(e) <= hi):", "H-24: incremento_pb = 0 pasa el dominio"),
    ("M19", E + "motor/fichas_mon_idx.py", "not x or len(x) > _MAX_LISTA.get(clave, 12):", "not x:", "H-24: listas sin tope de tamaño"),
    ("M20", E + "motor/fichas_mon_idx.py", '"diferencial_estable_dias": ("entero", 1, 252)', '"diferencial_estable_dias": ("entero", -5, 252)', "H-24: diferencial_estable_dias 0 y −1 valen"),
    ("M21", E + "motor/fichas_mon_idx.py", '"media_amplitud": ("entero", 1, _SESIONES_H5)', '"media_amplitud": ("entero", -5, _SESIONES_H5)', "H-24: media_amplitud 0 vale"),
    ("M22", E + "motor/fichas_mon_idx.py", '"sesiones_estimacion": ("entero", 1, _SESIONES_H5)', '"sesiones_estimacion": ("entero", -5, _SESIONES_H5)', "H-24: sesiones_estimacion 0 y negativos valen"),
    ("M23", E + "motor/fichas_mon_idx.py", '"ventana_percentil_anios": ("entero", 1, _ANIOS_HISTORIA)', '"ventana_percentil_anios": ("entero", -5, _ANIOS_HISTORIA)', "H-24: ventana_percentil_anios 0 vale"),
    ("M24", E + "motor/fichas_mon_idx.py", "cota_nodo = math.exp(float(lg_m)) * base / d * float(c_log)", "cota_nodo = 0.0", "H-27: vuelve a exigir la precisión sola"),
    ("M25", E + "motor/fichas_mon_idx.py", 'k.endswith(("_min", "_rango", "_min_anios", "_recomendados"))', 'k.endswith(("_min", "_rango", "_min_anios"))', "H-25 N02: «_recomendados» deja de ser umbral fijo"),
    ("M26", E + "motor/fichas_mon_idx.py", '"incertidumbre_probabilidad_acumulada": min(1.0, cota_r[k - 1] / incremento)})', '"incertidumbre_probabilidad_acumulada": min(1.0, 0.5 * cota_r[k - 1] / incremento)})',
     "H-25 N05: la incertidumbre acumulada, a la mitad"),
    ("M27", E + "motor/fichas_mon_idx.py", '"incertidumbre_probabilidad": min(1.0, cota_mov[k - 1] / incremento),', '"incertidumbre_probabilidad": min(1.0, 0.5 * cota_mov[k - 1] / incremento),',
     "H-25 N05: la incertidumbre de la reunión, a la mitad"),
    ("M28", E + "diseno_v6.py", 'if m.group(1).upper() in perm.get("tickers", ()) and m.group(1) not in _PALABRA_COMUN:', "if False:", "H-34: ticker en minúscula tras «la acción» pasa"),
    ("M29", E + "diseno_v6.py", 'if m.group(1).upper() in perm.get("tickers", ()) and m.group(1) not in _PALABRA_COMUN:', 'if m.group(1) not in _PALABRA_COMUN:',
     "H-34: caza cualquier palabra, no solo las del universo («el valor real»)"),
    ("M30", E + "diseno_v6.py", "        return \"CIFRA\"\n    for m in _VEHICULO.finditer(libre):", "        pass\n    for m in _VEHICULO.finditer(libre):", "T-109: romanos como cantidad pasan"),
    ("M31", E + "contratos.py", '"frases_30s": {"type": "array", "minItems": 1, "maxItems": 3, "items": TXT}',
     '"frases_30s": {"type": "array", "minItems": 2, "maxItems": 2, "items": TXT}', "H-50: el esquema vuelve a exigir dos"),
    ("M32", E + "diseno_v6.py", "    if len(escritas) != huecos:\n        quitadas.append(\"FORMATO\")", "    if False:\n        pass", "H-50: una o tres frases no se declaran"),
    ("M33", E + "diseno_v6.py", "escritas = (escritas + [\"\"] * huecos)[:huecos]", "escritas = (escritas + [\"\"] * huecos)", "H-50: la tercera frase no se descarta"),
    ("M34", E + "redaccion.py", "{'idea' if n == 1 else 'ideas'} en {nc} {'tipo' if nc == 1 else 'tipos'}", "ideas en {nc} tipos", "H-49: frase por defecto sin singular"),
    ("M35", E + "diseno_v6.py", 'ideas = "idea" if cand == 1 else "ideas"', 'ideas = "ideas"', "H-49: «De 1 ideas»"),
    ("M36", E + "diseno_v6.py", 'analizadas = "analizada" if cand == 1 else "analizadas"', 'analizadas = "analizadas"', "H-49: «1 idea … analizadas»"),
    ("M37", E + "diseno_v6.py", "if k in clases_paquete and isinstance(v, str) and (v2 := _uno(v, \"\").strip())}", "if isinstance(v, str) and (v2 := _uno(v, \"\").strip())}", "H-49: motivos de claves ajenas vuelven"),
    ("M38", E + "diseno_v6.py", '    quitadas.extend("FORMATO" for _ in ajenas)\n', "", "H-49: la clave ajena quitada no se declara"),
    ("M39", E + "diseno_v6.py", "    if reglas and salida[:1].islower():", "    if False:", "H-49: minúscula tras quitar la frase de delante"),
    ("M40", "config/por_defecto.yaml", "                       AIE, INE, EPA, TAE, BID]", "                       ZZZQ]", "H-52: AIE, INE, EPA, TAE y BID salen de la lista"),
    ("M41", "config/por_defecto.yaml", "ASEAN, BRICS, OCDE,", "ASEAN, BRICS, G7, G10, G20, OCDE,", "H-52: G7, G10 y G20 vuelven a la lista"),
    ("M42", E + "diseno_v6.py", "[\\s_\\u2800·‧∙•.\\-/]", "[\\s_\\u2800]", "H-53: el punto medio y el punto no separan letras sueltas"),
    ("M43", E + "diseno_v6.py", "[\\s_\\u2800·‧∙•.\\-/]", "[\\s_\\u2800·‧∙•.]", "H-53: el guion y la barra no separan letras sueltas"),
    ("M44", E + "diseno_v6.py", "exactamente dos frases para «la semana en 30 segundos»: el código pone delante una tercera, con las cuentas;",
     "dos frases de «la semana en 30 segundos»: la primera, con las cuentas, la escribe el código;", "H-50: la instrucción vuelve a ser ambigua"),
    # H-51: los mutantes vivos de la QA de T-102, con sus mismos textos
    ("S16", E + "diseno_v6.py", r'_FIN_CANTIDAD = r"(?=\s+(?:del?|al|en|por|m[aá]s|menos|sobre)\b|\s*[.,;:)]|\s*$)"', '_FIN_CANTIDAD = r""', "H-51 S16"),
    ("S17", E + "diseno_v6.py", r"sobre)\b|\s*[.,;:)]|\s*$)", r"sobre)\b|\s*$)", "H-51 S17"),
    ("S19", E + "diseno_v6.py", r'r"two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"', r'r"qqqq|"', "H-51 S19"),
    ("S20", E + "diseno_v6.py", r'r"thousand|percent|fifty-fifty)")', r'r"qqqq)")', "H-51 S20"),
    ("S34", E + "diseno_v6.py", '"sube", "suben", "cae", "caen"', '"suben", "caen"', "H-51 S34"),
    ("S41", E + "diseno_v6.py", '"CIRCLED LATIN", "PARENTHESIZED LATIN"', '"PARENTHESIZED LATIN"', "H-51 S41"),
    ("W25", E + "diseno_v6.py", 'm.group(2) == "s" and m.group(1) in perm["codigos"]', 'm.group(2) == "s"', "H-51 W25"),
    ("W37", E + "diseno_v6.py", 'if c.upper() not in perm["codigos"] and (', "if True and (", "H-51 W37"),
    # H-25 N10: el except de los datos
    ("N10", E + "motor/servicio.py", None, None, "H-25 N10 (se localiza abajo)"),
]


def pytest(cwd, pruebas):
    r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas], cwd=cwd, capture_output=True, text=True, timeout=3000)
    fallida = next((ln for ln in r.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))), "")
    return r.returncode, (fallida or (r.stdout.strip().splitlines() or [""])[-1])[:150]


def correr(m):
    mid, fich, viejo, nuevo, desc = m
    tmp = DEST / f"m_{mid}"
    shutil.rmtree(tmp, ignore_errors=True)
    try:
        shutil.copytree(RAIZ / "bloque_a", tmp / "bloque_a", ignore=shutil.ignore_patterns("*.docx", "*.png", "__pycache__", "estado_bloque_a"))
        ej = tmp / "bloque_a" / "11_Ejecutor"
        p = ej / fich
        s = p.read_text(encoding="utf-8")
        if mid == "N10":
            import re
            hallado = re.search(r"        except \(TypeError, ValueError, OverflowError\) as (\w+):\n(?=.*\n?.*DATOS_INCOHERENTES)", s)
            cand = [x for x in re.finditer(r"except \(TypeError, ValueError, OverflowError\)", s)]
            print(f"   N10: {len(cand)} `except (TypeError, ValueError, OverflowError)` en servicio.py; se muta el de los datos si es único tras «_resolver_datos(»")
            i = s.find("self._resolver_datos(")
            j = s.find("except (TypeError, ValueError, OverflowError)", i)
            if i < 0 or j < 0 or j - i > 1500:
                return mid, desc, "NO APLICA", "no se localiza el except de los datos", ""
            s2 = s[:j] + "except ZeroDivisionError" + s[j + len("except (TypeError, ValueError, OverflowError)"):]
        else:
            if s.count(viejo) != 1:
                return mid, desc, f"NO APLICA ({s.count(viejo)} apariciones)", "", ""
            s2 = s.replace(viejo, nuevo)
        p.write_text(s2, encoding="utf-8")
        c1, d1 = pytest(ej, ["tests/test_t113_deuda.py"])
        if c1 not in (0, 1):
            return mid, desc, f"ERROR (código {c1})", d1, ""
        if c1 == 1:
            return mid, desc, "MATADO por test_t113_deuda", d1, ""
        c2, d2 = pytest(ej, VECINAS)
        return mid, desc, ("SOBREVIVE a t113; MATADO por las vecinas" if c2 == 1 else "SOBREVIVE a t113 y a las vecinas"), d1, d2
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
    print("VIVOS frente a test_t113_deuda.py:", vivos)
