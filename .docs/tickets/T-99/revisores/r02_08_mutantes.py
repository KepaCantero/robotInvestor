"""r02_08 · Mutantes propios del revisor (independientes de mutantes_r02.py del implementador): cada uno cambia una línea del
registro o del banco en una COPIA (un worktree aparte, nunca el árbol principal), ejecuta las pruebas del implementador y dice
si alguna lo mata. Restaura el fichero después de cada mutante.
Uso: python3 r02_08_mutantes.py <worktree desechable>"""
import subprocess
import sys
from pathlib import Path

W = Path(sys.argv[1]).resolve()
assert W != Path("/home/user/robotinvestor").resolve(), "nunca en el árbol principal"
REG = W / ".docs" / "scripts" / "registro_experimentos.py"
BAN = W / ".docs" / "scripts" / "banco_medida.py"
PRUEBAS = [".docs/scripts/pruebas_registro_experimentos.py", ".docs/scripts/pruebas_banco_medida.py",
           ".docs/scripts/pruebas_borradores_contratos.py"]
MUTANTES = [
    ("sello: no se comprueba", REG, "        if not self.sello.exists():\n            if ultima is not None:",
     "        return\n        if not self.sello.exists():\n            if ultima is not None:"),
    ("sello: un registro con anotaciones sin sello se acepta", REG,
     "            if ultima is not None:\n                raise RegistroError(f\"falta el sello",
     "            if False:\n                raise RegistroError(f\"falta el sello"),
    ("ancla: no se comprueba", REG, "        if not self.ancla_git:\n            return", "        if True:\n            return"),
    ("ancla: compara solo la longitud", REG, "if not texto.encode(\"utf-8\").startswith(en_head.stdout):",
     "if len(texto.encode(\"utf-8\")) < len(en_head.stdout):"),
    ("cerrojo: sin flock", REG, "            fcntl.flock(fl.fileno(), fcntl.LOCK_EX)", "            pass"),
    ("cerrojo: se lee fuera del cerrojo", REG,
     "        with self._cerrojo():\n            previas = self.anotaciones()",
     "        previas = self.anotaciones()\n        with self._cerrojo():\n            previas = previas"),
    ("adopción: cuenta el ÚLTIMO resultado", REG, "primero = con_veredicto[0] if con_veredicto else None",
     "primero = con_veredicto[-1] if con_veredicto else None"),
    ("adopción: sin contradicción", REG, "contradictoria = bool(primero) and any(", "contradictoria = False and any("),
    ("adopción: «fallido» cuenta como primer resultado", REG,
     "if i[\"n\"] in res and res[i[\"n\"]][\"veredicto\"] != \"fallido\"]", "if i[\"n\"] in res]"),
    ("adopción: estrictamente después (>)", REG, "_instante(primero[0][\"inicio\"], \"inicio\") >= creado",
     "_instante(primero[0][\"inicio\"], \"inicio\") > creado"),
    ("adopción: compara instantes como texto", REG, "_instante(primero[0][\"inicio\"], \"inicio\") >= creado",
     "primero[0][\"inicio\"] >= pre[\"creado_en\"]"),
    ("lectura: no recalcula dentro_del_maximo", REG,
     "                if e[\"dentro_del_maximo\"] != _dentro(", "                if False and e[\"dentro_del_maximo\"] != _dentro("),
    ("lectura: no contrasta la huella del contenido", REG,
     "        if e[\"huella_prerregistro\"] != huella(e[\"contenido\"]):", "        if False:"),
    ("lectura: no contrasta la huella que cita el intento", REG,
     "                if e[\"huella_prerregistro\"] != pre[exp][\"huella_prerregistro\"]:", "                if False:"),
    ("lectura: admite dos prerregistros con el mismo EXP", REG, "                if exp in pre:\n", "                if False:\n"),
    ("escritura: no escapa U+2028", REG, "return txt.replace(\"\\u2028\", \"\\\\u2028\")", "return txt.replace(\"\\u2028\", \"\\u2028\")"),
    ("escritura: tolera el fichero sin salto final", REG, "        if texto and not texto.endswith(\"\\n\"):", "        if False:"),
    ("variante: sin NFC", REG, "    return unicodedata.normalize(\"NFC\", v)", "    return v"),
    ("instante: sin pasar a UTC el año del EXP", REG, "anio = _instante(ahora, \"ahora\").year", "anio = int(ahora[:4])"),
    ("banco: prerregistro.json fuera del try", BAN,
     "    try:\n        _escribir_json(salida / \"prerregistro.json\", {**prerregistro, \"huella\": h})",
     "    _escribir_json(salida / \"prerregistro.json\", {**prerregistro, \"huella\": h})\n    try:\n        pass"),
    ("banco: --max-variantes distinto se acepta al reutilizar", BAN, "            if prev != max_variantes:", "            if False:"),
    ("banco: --registro vacío se acepta", BAN, "    if getattr(a, \"registro\", None) == \"\":", "    if False:"),
]

vivos = []
for nombre, f, viejo, nuevo in MUTANTES:
    orig = f.read_text(encoding="utf-8")
    if orig.count(viejo) != 1:
        print(f"[NO APLICA] {nombre}: el texto aparece {orig.count(viejo)} veces"); continue
    f.write_text(orig.replace(viejo, nuevo), encoding="utf-8")
    try:
        p = subprocess.run([str(W / ".venv" / "bin" / "python"), "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                           cwd=str(W), capture_output=True, text=True, timeout=900)
        muerto = p.returncode != 0
    finally:
        f.write_text(orig, encoding="utf-8")
    ult = (p.stdout.strip().splitlines() or [""])[-1]
    print(f"[{'MUERTO' if muerto else 'VIVO'}] {nombre} · {ult[:90]}")
    if not muerto:
        vivos.append(nombre)
print(f"\n{len(MUTANTES) - len(vivos)}/{len(MUTANTES)} muertos; vivos: {vivos}")
