"""r03_08 · Mutantes propios del revisor sobre lo nuevo del registro 0.3.0 y del banco (ancla en el historial, sello tolerante,
cerrojo de lectores, pendientes, búsqueda atómica, RI_AGENTE, rutas públicas). CAMBIA FICHEROS: solo sobre un worktree
desechable. Cada mutante se aplica, se pasan las pruebas del implementador del fichero tocado y se deshace.
Uso: .venv/bin/python -B r03_08_mutantes.py <worktree desechable>"""
import subprocess
import sys
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
assert WT != Path("/home/user/robotinvestor"), "nunca sobre el repositorio principal"
PY = "/home/user/robotinvestor/.venv/bin/python"
REG = WT / ".docs/scripts/registro_experimentos.py"
BAN = WT / ".docs/scripts/banco_medida.py"
P_REG = ".docs/scripts/pruebas_registro_experimentos.py"
P_BAN = ".docs/scripts/pruebas_banco_medida.py"

M = [
    ("M01 ancla: no compara cada commit con sus padres", REG,
     "if anterior is not None and not actual.startswith(anterior):", "if False:"),
    ("M02 ancla: un commit sin el registro no falla", REG,
     'raise RegistroError(f"el registro se quitó del repositorio en el commit {commit[:8]}")', "continue"),
    ("M03 ancla: solo HEAD (no recorre la historia)", REG,
     'for linea in lista.stdout.decode("utf-8", "replace").splitlines():', "for linea in []:"),
    ("M04 ancla: rev-list que falla se toma como «sin ancla»", REG,
     'raise RegistroError(f"git no puede leer el historial del registro', 'return None; raise RegistroError(f"'),
    ("M05 ancla: sin comparar el fichero de trabajo con HEAD", REG,
     'if en_head is not None and not texto.encode("utf-8").startswith(en_head):', "if False:"),
    ("M06 ancla: sin git instalado, sin ancla", REG,
     'raise RegistroError("el registro está en un repositorio git y git no está instalado', 'return None; raise RegistroError("'),
    ("M07 ancla: hereda GIT_DIR y compañía", REG, 'if not k.startswith("GIT_")}', "if True}"),
    ("M08 sello: admite un sello por delante (truncado)", REG,
     "if s != esperado and s != un_corte:",
     'if s != esperado and s != un_corte and not (isinstance(s, dict) and isinstance(s.get("seq"), int) and s["seq"] > esperado["seq"]):'),
    ("M09 sello: sin tolerancia a un corte (como la r02)", REG, "if s != esperado and s != un_corte:", "if s != esperado:"),
    ("M10 sello: sin sello, siempre vale", REG,
     'if ultima is None or len(out) == 1 or (en_git is not None and texto.encode("utf-8") == en_git):', "if True:"),
    ("M11 sello: un clon sin sello no se lee", REG,
     'if ultima is None or len(out) == 1 or (en_git is not None and texto.encode("utf-8") == en_git):',
     "if ultima is None or len(out) == 1:"),
    ("M12 sello: se prepara después de escribir la línea", REG,
     "temporal = self._preparar_sello(e)   # antes", "temporal = None   # antes"),
    ("M13 sello: un fallo de os.replace sale como OSError", REG,
     'raise RegistroError(f"la anotación está escrita', 'raise ex; raise RegistroError(f"la anotación está escrita'),
    ("M14 sellar: vuelve a sellar aunque ya haya sello", REG, "if self.sello.exists():\n                raise", "if False:\n                raise"),
    ("M15 cerrojo: los lectores no lo cogen", REG, "with self._cerrojo(compartido=True):", "with contextlib.nullcontext():"),
    ("M16 cerrojo: espera sin límite", REG, "if time.monotonic() > limite:", "if False:"),
    ("M17 cerrojo: un intento rechazado crea carpeta y cerrojo", REG,
     "if not self.ruta.exists():   # no se crea carpeta", "if False:   # no se crea carpeta"),
    ("M18 adopción: un intento pendiente no bloquea", REG, 'and not d["pendiente"]', ""),
    ("M19 adopción: pendiente solo si es el primero", REG,
     'pendiente = any(i["n"] not in res for i in suyos)', 'pendiente = bool(suyos) and suyos[0]["n"] not in res'),
    ("M20 buscar_o_prerregistrar: busca fuera del cerrojo", REG,
     "        with self._cerrojo():\n            previas = self._leer()\n            for x in previas:\n"
     "                if x[\"tipo\"] == \"PRERREGISTRO\" and coincide(x[\"contenido\"]):\n                    return x, False\n"
     "            return self._escribir(previas, construir(previas)), True",
     "        for x in self.anotaciones():\n            if x[\"tipo\"] == \"PRERREGISTRO\" and coincide(x[\"contenido\"]):\n"
     "                return x, False\n        import time as _t; _t.sleep(0.2)\n        return self._anexar(construir), True"),
    ("M21 RI_AGENTE ignorado", REG, 'AGENTE = os.environ.get("RI_AGENTE", "claude")', 'AGENTE = "claude"'),
    ("M22 banco: rutas absolutas en el registro", BAN, "return p.relative_to(RAIZ.resolve()).as_posix()", "return str(p)"),
    ("M23 banco: rutas externas con su carpeta", BAN, 'return f"«externa»/{p.name}', 'return f"{p}'),
    ("M24 banco: otro máximo de variantes al reutilizar no se rechaza", BAN, "if prev != max_variantes:", "if False:"),
    ("M25 banco: decide reutilizar con la lectura de fuera", BAN,
     "encontrado, _nuevo = reg.buscar_o_prerregistrar(", "encontrado, _nuevo = (lambda *a, **k: (next((x for x in previos if a[0](x['contenido'])), None) or reg.prerregistrar(a[1], k['autor']), False))("),
]

vivos = []
for nombre, f, viejo, nuevo in M:
    orig = f.read_text(encoding="utf-8")
    if orig.count(viejo) != 1:
        print(f"[NO APLICA] {nombre}: el texto aparece {orig.count(viejo)} veces")
        vivos.append(nombre + " (no aplica)")
        continue
    f.write_text(orig.replace(viejo, nuevo), encoding="utf-8")
    pruebas = [P_REG] if f == REG else [P_BAN]
    if f == REG and "banco" in nombre:
        pruebas.append(P_BAN)
    try:
        p = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas], cwd=WT, capture_output=True,
                           text=True, timeout=300)
        muerto, cola = p.returncode != 0, (p.stdout.strip().splitlines() or ["?"])[-1]
    except subprocess.TimeoutExpired:
        muerto, cola = True, "tiempo agotado (300 s)"
    finally:
        f.write_text(orig, encoding="utf-8")
    print(f"[{'MUERTO' if muerto else 'VIVO'}] {nombre} · {cola[:120]}", flush=True)
    if not muerto:
        vivos.append(nombre)
print(f"\n{len(M) - len(vivos)}/{len(M)} mutantes muertos; vivos: {vivos}")
