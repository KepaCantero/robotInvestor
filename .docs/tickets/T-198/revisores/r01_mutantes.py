"""QA r01 de T-198: mutantes propios del revisor (lo esencial que no cubren los 34 del implementador).
Aplica cada mutación sobre una COPIA de bloque_a/11_Ejecutor, corre tests/test_t198_buscador_ct19.py y restaura.
Uso: python r01_mutantes.py <copia de 11_Ejecutor>"""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
FIA, ORQ = "bloque_a/fiabilidad_f9.py", "bloque_a/orquestacion.py"
M = [
    ("R1 F2 sin as_of (fuga en pronosticos_registrados)", FIA,
     "    for clm in almacen.estado(\"F2\", as_of, clave=\"clm_id\").values():",
     "    for clm in almacen.estado(\"F2\", None, clave=\"clm_id\").values():"),
    ("R2 F6 sin as_of al atender (fuga)", FIA,
     "    with almacen._transaccion():\n        f6 = _fue_de_f6(almacen, as_of)",
     "    with almacen._transaccion():\n        f6 = _fue_de_f6(almacen, None)"),
    ("R3 sin métrica", FIA, "\"metrica\": fue.get(\"metodo\"),", "\"metrica\": None,"),
    ("R4 el ciclo sin cerrojo (dos procesos)", ORQ,
     "        with self.almacen._transaccion():\n            fue = fiabilidad_f9.por_comunicar(self.almacen, as_of)",
     "        if True:\n            fue = fiabilidad_f9.por_comunicar(self.almacen, as_of)"),
    ("R5 el CT-07 del ciclo con fuga (sin as_of)", ORQ,
     "        fiabilidad_f9.anotar_candidatas(self.almacen, as_of, cand[\"referencias\"])",
     "        fiabilidad_f9.anotar_candidatas(self.almacen, None, cand[\"referencias\"])"),
    ("R6 registrados de cualquier tipo de afirmación", FIA,
     "        if clm.get(\"tipo_afirmacion\") == \"PRONOSTICO_FUENTE\" and isinstance(pf, dict)",
     "        if isinstance(pf, dict)"),
    ("R7 run_id del mensaje en vez del ciclo", FIA, "\"run_id\": run_id,", "\"run_id\": None,"),
    ("R8 fecha_ct19 sin el mensaje", FIA, "        fecha = str(msg.get(\"timestamp\") or \"\")[:10] or str(as_of)[:10]",
     "        fecha = \"2000-01-01\""),
    ("R9 periodo de otra fuente", FIA, "\"periodo\": f[\"periodo\"],", "\"periodo\": None,"),
]
vivos = []
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t198_buscador_ct19.py"],
                           cwd=EJ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else 'VIVO'}", flush=True)
    if not muerto:
        vivos.append(nombre)
print(f"{len(M) - len(vivos)} de {len(M)} muertos" + (f"; vivos: {vivos}" if vivos else ""))
sys.exit(1 if vivos else 0)
