"""QA r01 de T-158 · mutantes propios del revisor (G01–G30) sobre `guias.py` y el enganche en `orquestacion.py`.

Uso: python r01_04_mutantes.py <copia desechable con «qa29_» y «_mut» en la ruta y `bloque_a/` entero> [--scripts]
Cada mutante se aplica en la copia, se pasan las pruebas de `PRUEBAS` (con -x) y se restaura. Vivo = ninguna prueba lo
detecta. Con `--scripts`, a cada vivo se le pasa además `r01_02_integracion.py` de esta ronda. Los equivalentes (no cambian
ningún comportamiento observable) se marcan en EQUIVALENTES y su supervivencia no es un hallazgo. Termina con 1 si alguno no
aplica o si vive uno que no es equivalente."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "qa29_" in str(COPIA) and "_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
SCRIPTS = "--scripts" in sys.argv[2:]
AQUI = Path(__file__).resolve().parent
GU, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("guias", "orquestacion"))
PRUEBAS = ["tests/test_t158_guias.py", "tests/test_t126_pb26_pb48.py", "tests/test_t126_r02.py"]
MUTANTES = [
    ("G01", "detector ciego (no lee nada)", GU, 't = _normalizar(item.get("que_cambia", ""))', 't = ""'),
    ("G02", "sin la familia RELAJA_CONTROL", GU, "    if relaja:\n", "    if False:\n"),
    ("G03", "sin la familia TIPO_3", GU, "    if tipo3:\n", "    if False:\n"),
    ("G04", "sin credenciales", GU, "    if cred:\n", "    if False:\n"),
    ("G05", "sin prompt o contrato", GU, "    if pc and cambio:\n", "    if False:\n"),
    ("G06", "sin quitar tildes", GU, '    t = "".join(c for c in t if not unicodedata.combining(c))\n', ""),
    ("G07", "sin minúsculas", GU, 'return re.sub(r"\\s+", " ", t.lower()).strip()', 'return re.sub(r"\\s+", " ", t).strip()'),
    ("G08", "RELAJA sin exigir un control nombrado (más falsos positivos)", GU, "        if tocados:\n", "        if True:\n"),
    ("G09", "el ciclo no revisa en F0 (solo en la primera llamada)", OR, "        self.guias.cargar(as_of, run_id)\n", ""),
    ("G10", "las guías llegan a todos los agentes", OR,
     "guias = self.guias.para(agente, as_of, run_id)",
     "guias = [i for a in sorted(self.guias.cargar(as_of, run_id)) for i in self.guias.para(a, as_of, run_id)]"),
    ("G11", "si la revisión falla, se aplican las guías sin revisar", GU,
     "            aplicables = {}\n            self._por_run[clave] = aplicables",
     "            aplicables = {str(g.get('agente')): [dict(i, guia_id=k) for i in g.get('items', [])] "
     "for k, g in self.vigentes(as_of=hoy).items()}\n            self._por_run[clave] = aplicables"),
    ("G12", "una guía de HA inválida se aplica igual", GU,
     '"motivo": "no cumple el esquema del CT-18"})\n                continue\n', '"motivo": "no cumple el esquema del CT-18"})\n'),
    ("G13", "el ítem en conflicto no se retira (se registra, pero se conserva)", GU,
     'quedan = [it for it in g["items"] if it["item_id"] not in retirados]', 'quedan = list(g["items"])'),
    ("G14", "no se escribe el P3-", GU, '"tipo_entrada": "P3", "id": p3_id,', '"tipo_entrada": "P3X", "id": p3_id,'),
    ("G15", "el P3- nace APROBADA", GU, '"estado": "PENDING_OPERATOR", "decision_operador": None',
     '"estado": "APROBADA", "decision_operador": None'),
    ("G16", "la caducidad es exclusiva (el día de caducidad ya no)", GU, '_dia(it["caducidad"]) >= hoy', '_dia(it["caducidad"]) > hoy'),
    ("G17", "la fecha de aplicación es exclusiva", GU, '_dia(g["fecha_aplicacion"]) > hoy', '_dia(g["fecha_aplicacion"]) >= hoy'),
    ("G18", "emitir no sustituye a la vigente", GU, "            for k in vigentes:\n", "            for k in []:\n"),
    ("G19", "8 ítems ya no caben", GU, 'len(items) > lim["max_items_por_version"]', 'len(items) >= lim["max_items_por_version"]'),
    ("G20", "los hallazgos se cuentan mal (LEC en vez de HAL)", GU, 'if o.startswith("HAL-")}', 'if o.startswith("LEC-")}'),
    ("G21", "F5 no anota las guías aplicadas", OR, '**({"guias_aplicadas": ap} if (ap := self.guias.aplicadas(run_id)) else {})',
     "**({})"),
    ("G22", "la caché de la revisión no depende del run", GU, 'clave = (run_id or "", hoy.isoformat())', 'clave = ("", hoy.isoformat())'),
    ("G23", "sin acuse obligatorio en el esquema", GU, '"acuse_requerido": {"const": True},', '"acuse_requerido": {"type": "boolean"},'),
    ("G24", "sustituye siempre null", GU, "sustituye = max(vigentes, key=lambda k: int(k[-4:])) if vigentes else None", "sustituye = None"),
    ("G25", "se revisan también las SUPERSEDED", GU, 'if v.get("estado") == "ISSUED" and', 'if v.get("estado") in ("ISSUED", "SUPERSEDED") and'),
    ("G26", "la guía sin ítems válidos se queda ISSUED", GU,
     '{"tipo_entrada": "GUI", "id": gid, "estado": "RETIRADA", "motivo": motivo}', '{"tipo_entrada": "GUI", "id": gid, "motivo": motivo}'),
    ("G27", "tipo 3 admitido en el esquema", GU, '"tipo": {"enum": [1, 2]},', '"tipo": {"enum": [1, 2, 3]},'),
    ("G28", "el contexto lleva también el origen", GU,
     'for k in ("item_id", "tipo", "que_cambia", "donde_se_comprueba", "como_se_sabe")}}',
     'for k in ("item_id", "tipo", "que_cambia", "donde_se_comprueba", "como_se_sabe", "origen")}}'),
    ("G29", "COR- sin comunicar al operador", GU, '"comunicado_a": [agente, "AG-18", "OPERADOR"]', '"comunicado_a": [agente, "AG-18"]'),
    ("G30", "la guía de otro agente se acepta (sin comprobar el receptor en guia_id)", GU,
     "(receptor not in TODOS or gid[4:8] != receptor.replace(\"-\", \"\"))", "(receptor not in TODOS)"),
]
# G09 parecía equivalente (`_invocar` llama a `cargar` con el mismo run_id en la primera llamada), pero no lo es: sin la
# revisión del F0, la primera llamada puede ser la de un hilo de Analista y la reemisión de la guía (CT-18, contadores de HA)
# se mezcla con los mensajes de los otros hilos (r01_02, determinismo con hilos). G22: dentro de un proceso, `emitir` vacía
# la caché; solo cambia si alguien escribe en HA sin `emitir` entre dos runs del mismo día (ver qa.md).
EQUIVALENTES: set[str] = set()


def pasar(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=3600).returncode


def main() -> int:
    sin_aplicar, vivos = [], []
    ej = COPIA / "bloque_a" / "11_Ejecutor"
    for mid, que, ruta, viejo, nuevo in MUTANTES:
        f = COPIA / ruta
        original = f.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} NO APLICA ({original.count(viejo)} apariciones): {que}", flush=True)
            sin_aplicar.append(mid)
            continue
        f.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        extra = ""
        try:
            muerto = pasar([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], ej) != 0
            if not muerto and SCRIPTS:
                u = pasar([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", str(AQUI / "r01_02_integracion.py")], ej)
                extra = f" · r01_02 {'lo detecta' if u else 'no'}"
        finally:
            f.write_text(original, encoding="utf-8")
        print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}{extra}", flush=True)
        if not muerto:
            vivos.append(mid)
    malos = [m for m in vivos if m not in EQUIVALENTES]
    print(f"{len(MUTANTES) - len(vivos) - len(sin_aplicar)}/{len(MUTANTES)} muertos; vivos: {', '.join(vivos) or 'ninguno'} "
          f"(no equivalentes: {', '.join(malos) or 'ninguno'}); sin aplicar: {', '.join(sin_aplicar) or 'ninguno'}")
    return 1 if sin_aplicar or malos else 0


if __name__ == "__main__":
    sys.exit(main())
