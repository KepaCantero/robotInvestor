"""T-84, QA r01 de la V0.63 (semana simulada): mutaciones dirigidas sobre diario, reloj y persistencia.

Para cada mutación copia validador/, pruebas/, esquemas/ y el LEEME a una carpeta temporal, cambia UNA cadena exacta de un
fichero de la copia (nunca el repositorio), ejecuta pruebas/pruebas_semana.py en la copia y anota si la semana la caza
(sale con fallos o lanza) o la deja VIVA. Con --doradas también ejecuta pruebas/pruebas_doradas.py (la foto fija de la
semana de la V0.66), para separar lo que caza la semana de lo que caza la dorada; con --resto, además, las baterías de T-03 y
la jornada (OTRAS), para saber si lo que la semana deja vivo lo caza alguna otra batería del marco; con --todas, todas las
pruebas/pruebas_*.py del marco en lugar de OTRAS (lento: úsalo con --solo).

Cada mutación lleva lo que se espera de una red de integración: «CAZAR» si la semana dice probarlo (Documento 0 de la V0.63,
§1 a §3) y «FUERA» si es robustez que la semana no pretende cubrir (la cubren las baterías de T-03). El resultado que cuenta
para el informe es la columna «semana» frente a «se espera».

Uso (desde sistema_global/marco_comun_c):
  python3 -I entrega_claude/V0.63_revision/r01_mutaciones_semana.py [--doradas] [--resto | --todas] [--solo ID,ID]
"""
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MARCO = Path(__file__).resolve().parents[2]
PY = sys.executable
EXCLUIR = set()   # baterías que ya fallan en la copia sin mutar (con --todas): no cuentan
OTRAS = ("pruebas_diario_t03.py", "pruebas_reloj_t03.py", "pruebas_persistencia_t03.py", "pruebas_firma_t03.py",
         "pruebas_robustez_t03.py", "pruebas_jornada.py", "pruebas_reloj_diario_t72.py")

# (id, fichero, cadena exacta, sustituta, qué rompe, se espera)
MUTACIONES = [
    # ---------------------------------------------------------------- diario.py
    ("D01", "validador/diario.py",
     'return isinstance(e.get("firma"), str) and hmac.compare_digest(e["firma"], pe.firmar(clave, "robot-investor/diario/" + e["hash"]))',
     'return isinstance(e.get("firma"), str)',
     "abrir acepta cualquier firma en las líneas del diario firmado", "FUERA"),
    ("D02", "validador/diario.py",
     '    if clave is not None:\n        e["firma"] = pe.firmar(clave, "robot-investor/diario/" + e["hash"])',
     '    if False:\n        e["firma"] = pe.firmar(clave, "robot-investor/diario/" + e["hash"])',
     "las líneas del diario no se firman aunque haya clave", "CAZAR"),
    ("D03", "validador/diario.py",
     'if sig["resultado"] != _resultado(res):',
     'if False:',
     "al reabrir no se compara el resultado anotado (DI-04 desactivado)", "FUERA"),
    ("D04", "validador/diario.py",
     "            if ultima and incompleta:\n                return lineas, True, True, None",
     "            if ultima and incompleta:\n                return lineas[:-2], True, True, None",
     "tras una línea a medias se pierde además la última operación completa (OP y RES)", "CAZAR"),
    ("D05", "validador/diario.py",
     "    d = Diario(o, ruta_estado, ruta_diario, lineas[-1][\"hash\"], lineas[-1][\"n\"], clave)\n    if reescribir:",
     "    d = Diario(o, ruta_estado, ruta_diario, lineas[-1][\"hash\"], lineas[-1][\"n\"], clave)\n    if False:",
     "la línea cortada no se limpia antes de seguir escribiendo", "CAZAR"),
    ("D06", "validador/diario.py",
     "            if ultima and incompleta:\n                return lineas, True, True, None",
     "            if True:\n                return lineas, True, True, None",
     "una línea rota en MEDIO del diario se toma por un corte (se trunca en silencio en vez de DI-02)", "FUERA"),
    ("D07", "validador/diario.py",
     "            _escribir_atomico(self._ruta_estado, texto)\n",
     "",
     "el punto de control no guarda el estado (pero sí reduce el diario)", "CAZAR"),
    ("D08", "validador/diario.py",
     "        actual = _huella_viva(self._o)\n        if actual is not None and actual == self._huella:\n            return None",
     "        actual = _huella_viva(self._o)\n        if True:\n            return None",
     "no se detectan los cambios hechos por fuera del diario (DI-06)", "FUERA"),
    ("D09", "validador/diario.py",
     "        if sig is not None:   # una OP sin su RES solo puede ser la última",
     "        if sig is not None and False:   # una OP sin su RES solo puede ser la última",
     "una OP sin RES en medio del diario se acepta", "FUERA"),
    ("D10", "validador/diario.py",
     '            if reescribir:   # se quita la línea cortada (o se cierra la última) antes de seguir escribiendo\n                _reescribir(ruta_diario, lineas)\n            d._anotar({"tipo": "RES", "op": e["n"], "resultado": _resultado(res)})',
     '            if reescribir:   # se quita la línea cortada (o se cierra la última) antes de seguir escribiendo\n                _reescribir(ruta_diario, lineas)\n            pass',
     "una OP sin RES al final se aplica pero su RES no se anota", "FUERA"),
    # ---------------------------------------------------------------- reloj.py
    ("R01", "validador/reloj.py",
     "        if u is not None and not _dentro(_suma(u, -self.max_desfase_s",
     "        if False and u is not None and not _dentro(_suma(u, -self.max_desfase_s",
     "comprobar_estado nunca da RL-02 (el reloj puede arrancar detrás del estado)", "CAZAR"),
    ("R02", "validador/reloj.py",
     "            self._suelo = u if self._suelo is None else max(self._suelo, u)",
     "            pass",
     "comprobar_estado no fija el suelo (el último instante del estado)", "CAZAR"),
    ("R03", "validador/reloj.py",
     "        s = segundos if self._suelo is None else max(segundos, self._suelo)",
     "        s = segundos",
     "el reloj puede dar instantes por debajo del suelo", "CAZAR"),
    ("R04", "validador/reloj.py",
     'ahora=self._dar(max(p, ref.timestamp())), desfase_s=desfase)',
     'ahora=self._dar(ref.timestamp()), desfase_s=desfase)',
     "contrastar da la hora de la referencia, no el mayor de reloj y referencia", "FUERA"),
    ("R05", "validador/reloj.py",
     "        if not _dentro(abs(desfase), self.max_desfase_s):",
     "        if False:",
     "contrastar no compara con la referencia (RL-03 desactivado)", "CAZAR"),
    ("R06", "validador/reloj.py",
     '            if not _dentro(abs(salto), self.max_salto_s):',
     '            if False:',
     "no se vigila el salto de pared frente a monótono (RL-01)", "FUERA"),
    ("R07", "validador/reloj.py",
     '        return _r(True, "OK", "instante", ahora=self._dar(p))',
     '        return _r(False, "RL-04", "roto a propósito", ahora=None)',
     "Reloj.ahora() no da NUNCA un instante", "CAZAR"),
    ("R08", "validador/reloj.py",
     '        if self._contraste is None or not _dentro(m - self._contraste, self.max_sin_contraste_s):',
     '        if False:',
     "ahora() da instantes sin haber contrastado nunca (RL-04)", "CAZAR"),
    ("R09", "validador/reloj.py",
     '        lect, err = self._leer()\n        if err:\n            return {**err, "desfase_s": None}\n        p, m = lect',
     '        lect, err = None, None\n        p, m = ref.timestamp(), 0.0',
     "contrastar no lee el reloj: devuelve la referencia sin más", "CAZAR"),
    # ---------------------------------------------------------------- persistencia.py
    ("P01", "validador/persistencia.py",
     '        if _huella(doc["estado"]) != doc["huella"]:',
     '        if False:',
     "cargar no comprueba la huella del estado (PE-02)", "FUERA"),
    ("P02", "validador/persistencia.py",
     "        if not buena:\n",
     "        if False:\n",
     "cargar acepta un estado con la firma rota (PE-06)", "FUERA"),
    ("P03", "validador/persistencia.py",
     '    return firmar(clave, "robot-investor/estado/" + cabecera + "|" + orden)',
     '    return firmar(clave, "robot-investor/estado/" + cabecera + "|")',
     "la firma del estado no cubre el estado (solo la cabecera)", "FUERA"),
    ("P04", "validador/persistencia.py",
     "        rotos = o.integridad()\n        if rotos:\n            # siempre",
     "        rotos = []\n        if rotos:\n            # siempre",
     "cargar no pasa integridad()", "FUERA"),
    ("P05", "validador/persistencia.py",
     "    estado = {k: v for k, v in vars(o).items()}",
     '    estado = {k: v for k, v in vars(o).items() if k != "manuales"}',
     "volcar no guarda un atributo (manuales)", "CAZAR"),
    ("P06", "validador/persistencia.py",
     '    if clave is not None:\n        doc["clave_id"] = clave_id(clave)',
     '    if False:\n        doc["clave_id"] = clave_id(clave)',
     "volcar con clave no firma el estado", "CAZAR"),
    # ---------------------------------------------------------------- la propia batería
    ("S01", "pruebas/pruebas_semana.py",
     '        f.write("".join(lineas + [lineas[-1][:25]]))',
     '        f.write("".join(lineas))',
     "el corte a medias del miércoles no corta nada", "CAZAR"),
    ("S02", "pruebas/pruebas_semana.py",
     "        ce = self.reloj.comprobar_estado(self.o)\n        assert ce[\"ok\"], (\"comprobar_estado\", ce)",
     "        ce = {\"ok\": True}",
     "la máquina no llama comprobar_estado al arrancar", "CAZAR"),
]


def copia(dest):
    for d in ("validador", "pruebas", "esquemas"):
        shutil.copytree(MARCO / d, dest / d, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copy2(MARCO / "LEEME.md", dest / "LEEME.md")


def ejecuta(raiz, bateria):
    env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        p = subprocess.run([PY, "-I", "-B", bateria], cwd=raiz, env=env, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return True, "TIMEOUT"
    salida = p.stdout + p.stderr
    caza = p.returncode != 0 or "TODAS LAS PRUEBAS PASAN" not in salida
    falla = [x for x in salida.splitlines() if x.startswith("FALLA") or "Error" in x][:2]
    return caza, " | ".join(x[:110] for x in falla)


def una(m, doradas, resto=False):
    mid, fichero, viejo, nuevo, _, _ = m
    with tempfile.TemporaryDirectory(prefix=f"t84-{mid}-") as tmp:
        raiz = Path(tmp) / "marco_comun_c"
        copia(raiz)
        if mid != "BASE":
            f = raiz / fichero
            texto = f.read_text(encoding="utf-8")
            n = texto.count(viejo)
            if n != 1:
                return mid, None, None, f"la cadena aparece {n} veces: mutación no aplicable"
            f.write_text(texto.replace(viejo, nuevo), encoding="utf-8")
        caza_s, det_s = ejecuta(raiz, "pruebas/pruebas_semana.py")
        caza_d, det_d = ejecuta(raiz, "pruebas/pruebas_doradas.py") if doradas else (None, "")
        lista = sorted(x.name for x in (raiz / "pruebas").glob("pruebas_*.py") if x.name != "pruebas_semana.py") if resto == "todas" else OTRAS
        lista = [b for b in lista if b not in EXCLUIR]
        otras = [b.replace("pruebas_", "").replace(".py", "") for b in lista if ejecuta(raiz, "pruebas/" + b)[0]] if resto else None
        return mid, caza_s, caza_d, det_s or det_d, otras


def main():
    doradas = "--doradas" in sys.argv
    solo = None
    if "--solo" in sys.argv:
        solo = set(sys.argv[sys.argv.index("--solo") + 1].split(","))
    resto = "todas" if "--todas" in sys.argv else "--resto" in sys.argv
    base = una(("BASE", "", "", "", "", ""), doradas, resto)
    print(f"BASE (sin mutar): semana {'FALLA' if base[1] else 'pasa'}" + (f", doradas {'FALLA' if base[2] else 'pasa'}" if doradas else ""))
    if base[4] and resto == "todas":   # las que fallan sin mutar (necesitan algo fuera de la copia): se apartan y se dice
        EXCLUIR.update("pruebas_" + b + ".py" for b in base[4])
        print(f"apartadas por fallar ya en la copia sin mutar: {sorted(EXCLUIR)}")
    elif base[4]:
        print(f"fallan ya en la copia sin mutar: {base[4]}")
        return 2
    if base[1] or base[2]:
        print("la copia sin mutar no pasa: no se puede medir nada")
        return 2
    lista = [m for m in MUTACIONES if solo is None or m[0] in solo]
    with ThreadPoolExecutor(max_workers=max(1, (os.cpu_count() or 2))) as ex:
        res = list(ex.map(lambda m: una(m, doradas, resto), lista))
    huecos = 0
    print(f"\n{'ID':4} {'se espera':9} {'semana':7} {'doradas':8} qué rompe")
    for m, (mid, cs, cd, det, otras) in zip(lista, res):
        if cs is None:
            print(f"{mid:4} {'-':9} {'NO APL':7} {'':8} {det}")
            huecos += 1
            continue
        s = "CAZADA" if cs else "VIVA"
        d = "" if cd is None else ("CAZADA" if cd else "VIVA")
        marca = "  <-- HUECO" if m[5] == "CAZAR" and not cs else ""
        huecos += bool(marca)
        print(f"{mid:4} {m[5]:9} {s:7} {d:8} {m[4]}{marca}")
        if det and cs:
            print(f"{'':31}  ({det})")
        if otras is not None:
            print(f"{'':31}  otras que la cazan: {', '.join(otras) if otras else 'NINGUNA'}")
    print(f"\nMutaciones que la semana dice cubrir y deja vivas: {huecos}")
    print("RESULTADO r01:", "LA SEMANA CAZA TODO LO QUE DICE PROBAR" if huecos == 0 else "HAY HUECOS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
