"""T-133 · Mutantes del banco de medida (los de la r03 de T-94, al día, y los de T-133): cada uno debe morir ante `pruebas_banco_medida.py`.

Trabaja en una copia de `.docs/scripts` en una carpeta temporal (nunca en el árbol principal) y sin la prueba de
integración sobre A, que necesita la raíz del repositorio. Uso: .venv/bin/python -B .docs/tickets/T-133/banco_medida/mutantes.py"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
PY = RAIZ / ".venv" / "bin" / "python"
MUTANTES = {
    "M01 borde del cero": ("if lo > 0:", "if lo >= 0:"),
    "M02 sin signo en el exceso": ("SIGNO[direccion] * (r - float(np.mean(cesta)))", "(r - float(np.mean(cesta)))"),
    "M03 sin precio final se estima con el último": ("if serie.empty or serie.index.max() < fin:", "if serie.empty:"),
    "M04 nivel ignorado": ("cola = (1.0 - nivel) / 2.0", "cola = 0.05"),
    "M05 azar sin semilla por fecha y clase": ('rng = random.Random(f"{semilla}|{fecha}|{clase}")', "rng = random.Random(semilla)"),
    "M06 momento CORTO elige como LARGO": ('candidatos = orden if f["direccion"] != "CORTO" else list(reversed(orden))', "candidatos = orden"),
    "M07 repeticiones contadas": ("elif clave in abiertas and abiertas[clave][0] > ini:", "elif False:"),
    "M08 la repetida alarga la ventana": ('motivo=f"repetida: la misma apuesta sigue abierta desde el {abiertas[clave][1]}")',
                                          ('motivo=f"repetida: la misma apuesta sigue abierta desde el {abiertas[clave][1]}")\n'
                                           "            abiertas[clave] = (max(fin, abiertas[clave][0]), abiertas[clave][1])")),
    "M09 orden de entrada en vez del canónico": ("for i in sorted(range(len(selecciones)), key=orden):", "for i in range(len(selecciones)):"),
    "M10 remuestreo sin grupos": ("    if grupos is None:\n        idx = rng.integers(0, len(x), size=(n, len(x)))",
                                  "    if True:\n        idx = rng.integers(0, len(x), size=(n, len(x)))"),
    "M11 efectivas = n": ("return len(x) if grupos is None else len(set(grupos))", "return len(x)"),
    "M12 sin mínimo de efectivas": ("if min(efectivas) < min_efectivas:", "if False:"),
    "M13 mínimo mirando el lado con más fechas": ("if min(efectivas) < min_efectivas:", "if max(efectivas) < min_efectivas:"),
    "M14 sin muestra de fechas sin solape": ("dentro = [f for f in filas if _fecha(f) in muestra]", "dentro = list(filas)"),
    "M15 fechas solapadas en la muestra": ("        if d >= cierre:\n            elegidas.add(d)", "        if True:\n            elegidas.add(d)"),
    "M16 la ventana más corta de una fecha manda": ("fin_por_fecha[d] = max(fin_por_fecha.get(d, fin), fin)", "fin_por_fecha[d] = fin"),
    "M17 grupos por símbolo": ("[_fecha(f) for f in puntuadas]", '[f.get("simbolo") for f in puntuadas]'),
    "M18 grupos sin normalizar la fecha": ('return fila.get("fecha_corte") or pd.Timestamp(fila["fecha_asof"]).strftime("%Y-%m-%d")',
                                           'return str(fila["fecha_asof"])'),
    "M19 cierres no positivos admitidos": ("malos = ~np.isfinite(v) | (v <= 0)", "malos = ~np.isfinite(v)"),
    "M20 no finitos admitidos": ("malos = ~np.isfinite(v) | (v <= 0)", "malos = v <= 0"),
    "M21 fechas repetidas admitidas": ("if fechas.duplicated().any():", "if False:"),
    "M22 columnas repetidas admitidas": ("        if repetidas:\n            raise", "        if False:\n            raise"),
    "M23 fichero sin filas admitido": ("if df.empty:", "if False:"),
    "M24 clase ajena admitida": ("if clase not in miembros:", "if False:"),
    "M25 símbolo de otra clase admitido": ("if clase_de.get(sim) != clase:", "if False:"),
    "M26 dirección desconocida admitida": ("if direccion not in DIRECCIONES:", "if False:"),
    "M27 zona horaria admitida": ("if serie.index.tz is not None:", "if False:"),
    "M28 universo con símbolos repetidos": ("if not dup.empty:", "if False:"),
    "M29 horizonte desconocido sin BancoError": ('except (KeyError, ValueError, TypeError) as e:\n            raise BancoError(f"horizonte',
                                                 'except ZeroDivisionError as e:\n            raise BancoError(f"horizonte'),
    "M30 resolución no posterior admitida": ("if not fin > ini:", "if False:"),
    "M31 azar recorta en silencio": ("if len(pool) < len(filas):", "if False:"),
    "M32 momento recorta en silencio": ("if len(puntos) < len(filas):", "if False:"),
    "M33 fuga sin efecto": ('if sin_veredicto and c["veredicto"] in ("mejor", "peor"):', "if False:"),
    "M34 fuga solo rebaja «mejor»": ('c["veredicto"] in ("mejor", "peor")', 'c["veredicto"] == "mejor"'),
    "M35 fuga solo con el simulado": ('a.cliente != "mock" and', 'a.cliente == "mock" and'),
    "M36 caché fuera del coste": ('CAMPOS_ENTEROS = ("llamadas", "tokens_entrada", "tokens_salida", "tokens_cache_escritura", "tokens_cache_lectura")',
                                  'CAMPOS_ENTEROS = ("llamadas", "tokens_entrada", "tokens_salida")'),
    "M37 consumo negativo admitido": ("if not math.isfinite(v) or v < 0:", "if not math.isfinite(v):"),
    "M38 coste parcial como total": ('if filas and not consumo["filas_sin_coste"]:', "if filas:"),
    "M39 coste cero como sin dato": ("None if coste is None else round(coste / resueltas, 4)", "None if not coste else round(coste / resueltas, 4)"),
    "M41 aviso de otra hipótesis desde dos": ("        if otros_misma:\n", "        if otros_misma > 1:\n"),
    "M42 experimento ajeno admitido": ("        if distinto:\n            raise", "        if False:\n            raise"),
    "M40 un experimento por fuente ignorado": ('and c.get("objeto") == "BLOQUE" and c.get("fuente_banco") == fuente,', 'and c.get("objeto") == "BLOQUE",'),
    "M43 RegistroError sin traducir": ("        except rx.RegistroError as e:\n            raise BancoError(f\"registro de experimentos: {e}\") from e\n    try:",
                                       "        except ZeroDivisionError as e:\n            raise BancoError(f\"registro de experimentos: {e}\") from e\n    try:"),
    "B01 fuente con las huellas (otro experimento)": ('        "fuente": f"cliente {a.cliente}",', '        "fuente": f"cliente {a.cliente}, datos {huella_d[:16]}, universo {huella_u[:16]}",'),
    "B02 huella sin el contenido": ('b"\\0" + _huella_fichero(f))', 'b"\\0")'),
    "B09 verificar con el registro citado": ("            registro = rx.REGISTRO_DEFECTO\n", "            registro = citado\n"),
    "B10 sin aviso de otro registro": ('            avisos.append("experimento.json cita otro registro', '            pass  # avisos.append("experimento.json cita otro registro'),
    "B12 huella con subcarpetas": ('ficheros = sorted(ruta.glob("*.csv"), key=', 'ficheros = sorted(ruta.rglob("*.csv"), key='),
    "B13 huella sin ordenar": ('ficheros = sorted(ruta.glob("*.csv"), key=lambda f: unicodedata.normalize("NFC", f.name))', 'ficheros = list(ruta.glob("*.csv"))[::-1]'),
    "B14 huella con la ruta entera": ('h.update(unicodedata.normalize("NFC", f.name).encode(', 'h.update(unicodedata.normalize("NFC", str(f)).encode('),
    "B15 huella del universo con el nombre del fichero": ('            h.update(unicodedata.normalize("NFC", f"{sim}\\t{clase}\\n").encode("utf-8"))', '            h.update(unicodedata.normalize("NFC", f"{ruta.name}{sim}\\t{clase}\\n").encode("utf-8"))'),
    "B16 huella sin NFC": ('h.update(unicodedata.normalize("NFC", f.name).encode(', 'h.update((f.name).encode('),
    "B17 datos cambiados durante la ejecución admitidos": ('        if (huella_datos(tit["datos"], universo["simbolo"].tolist()), huella_datos(tit["universo"])) != (huella_d, huella_u):', '        if False:'),
    "B18 celda vacía en una obligatoria admitida": ('                if k in ("llamadas", "tokens_entrada", "tokens_salida") and (f.get(k) is None or not str(f.get(k)).strip()):', '                if False:'),
    "B19 columna ausente como 0": ('        return "sin dato" if k in ausentes else t.get(k, defecto)', '        return t.get(k, defecto)'),
    "B20 sin la plantilla en el informe md": ('if inf.get("plantilla") else []),', 'if False else []),'),
    "B21 nivel 0,80 admitido": ("NIVEL_MIN, NIVEL_MAX = 0.90, 0.99", "NIVEL_MIN, NIVEL_MAX = 0.80, 0.99"),
    "B22 fechas de la plantilla sin normalizar": ('if pd.Timestamp(s["fecha_asof"]).strftime("%Y-%m-%d") in muestra]', 'if s["fecha_asof"] in muestra]'),
    "B03 repetidas fuera de la muestra": ('        plantilla = [s for s in plantilla_total if pd.Timestamp(s["fecha_asof"]).strftime("%Y-%m-%d") in muestra]', '        plantilla = plantilla_total'),
    "B04 NEUTRAL gasta ventana": ('        if f.get("direccion") == "NEUTRAL":   # T-133 (H-25)', '        if False:   # T-133 (H-25)'),
    "B05 decimales en los recuentos": ("                if v != int(v):   # un recuento", "                if False:   # un recuento"),
    "B06 columnas que faltan admitidas": ("        if faltan:\n            raise BancoError(f\"a {Path(fichero).name} le faltan las columnas", "        if False:\n            raise BancoError(f\"a {Path(fichero).name} le faltan las columnas"),
    "B07 columnas repetidas en consumo": ("        if repetidas:   # T-133 (H-26)", "        if False:   # T-133 (H-26)"),
    "B08 mínimo de 5 fechas": ("MIN_EFECTIVAS_MIN = MIN_EFECTIVAS", "MIN_EFECTIVAS_MIN = 5"),
    "B11 máximo de experimento.json sin comparar": ('    elif e.get("dentro_del_maximo") != it["dentro_del_maximo"]:', '    elif False:'),
    "M44 fallo tras el titular sin anotar": ("    except BaseException as e:\n        if reg is not None:",
                                             "    except BancoError as e:\n        if reg is not None:"),
    "M45 verificar sin huella": ('if pre.get("huella") != h:', "if False:"),
    "M46 verificar sin informe.md": ("if md != informe_md(", "if False and md != informe_md("),
    "M47 verificar sin experimento.json no se queja": ("    if not fe.exists():\n        problemas.append", "    if False:\n        problemas.append"),
    "M48 verificar sin la huella del informe": ('rs["detalle"].get("huella_informe") != huella(inf)', "False"),
    "M49 no se borra el experimento.json anterior": ('(salida / "experimento.json").unlink(missing_ok=True)', "pass"),
    "M50 cotas de nivel de un experimento": ("    if not NIVEL_MIN <= nivel <= NIVEL_MAX:\n        raise BancoError(f\"«nivel» de un experimento",
                                             "    if False:\n        raise BancoError(f\"«nivel» de un experimento"),
    "M56 cotas de un veredicto": ("    if not NIVEL_MIN <= nivel <= NIVEL_MAX:\n        raise BancoError(f\"«nivel» de un veredicto",
                                  "    if False:\n        raise BancoError(f\"«nivel» de un veredicto"),
    "M57 cota de remuestreos de un veredicto": ('_entero("remuestreos", remuestreos, minimo=REMUESTREOS_MIN), _nivel(nivel)',
                                                '_entero("remuestreos", remuestreos), _nivel(nivel)'),
    "M51 cota de remuestreos de un experimento": ('getattr(a, "remuestreos", REMUESTREOS), minimo=REMUESTREOS_MIN)',
                                                  'getattr(a, "remuestreos", REMUESTREOS), minimo=1)'),
    "M52 cota de fechas efectivas de un experimento": ('getattr(a, "min_efectivas", MIN_EFECTIVAS), minimo=MIN_EFECTIVAS_MIN)',
                                                       'getattr(a, "min_efectivas", MIN_EFECTIVAS), minimo=1)'),
    "M53 semilla negativa admitida": ('getattr(a, "semilla", SEMILLA), minimo=0)', 'getattr(a, "semilla", SEMILLA), minimo=-(2 ** 63))'),
    "M54 aviso de cliente siempre": ('    if cliente == "mock":\n        partes.append', '    if True:\n        partes.append'),
    "M55 huella citada de otro contenido": ("h = huella(prerregistro)", 'h = huella({**prerregistro, "tarde": True})'),
}


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="t94_mut_"))
    try:
        copia = tmp / ".docs" / "scripts"
        shutil.copytree(RAIZ / ".docs" / "scripts", copia, ignore=shutil.ignore_patterns("__pycache__", ".logs"))
        fichero = copia / "banco_medida.py"
        original = fichero.read_text(encoding="utf-8")
        vivos = []
        for nombre, (viejo, nuevo) in MUTANTES.items():
            if original.count(viejo) != 1:
                print(f"??    {nombre}: el patrón no aparece una sola vez")
                vivos.append(nombre)
                continue
            fichero.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            r = subprocess.run([str(PY), "-B", "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "-k", "not integracion",
                                str(copia / "pruebas_banco_medida.py")], cwd=tmp, capture_output=True, text=True, check=False)
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
