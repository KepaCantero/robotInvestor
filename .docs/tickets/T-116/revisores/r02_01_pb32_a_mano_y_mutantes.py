"""QA r02 de T-116 · PB-32 (certificación de un horizonte), una de las AUTOMATICA que la r01 no leyó, con la regla estricta.

El plan: 60 PRG de RF × H3 con habilidad y 40 de RV × H3 sin habilidad ⇒ «CERT- para RF × H3 (n ≥ 100, IC 90 % del BSS > 0
tras Holm, calibración no rechazada con ECE < 0,15, re-ejecución CT-10 coincidente); NINGUNO para RV × H3»; criterio: «un
certificado; G3-CON-10 PASA en RF y bloquearía en RV».
 1. A mano (lo que el ejecutor hace): celda RF × H3 con habilidad y celda RV × H3 sin habilidad en el mismo almacén.
 2. Mutantes en `motor/evaluacion.py::criterio_certificado` contra las pruebas que el mapa cita para PB-32: ¿alguna
    prueba citada afirma que una celda SIN habilidad no se certifica?
Uso, desde bloque_a/11_Ejecutor:  python <este fichero> [<copia desechable de 11_Ejecutor, con «qa2_mut» en la ruta>]
"""
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "tests")]
import numpy as np
import pandas as pd
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo
from conftest import nuevo_bloque

import bloque_a

print("código:", Path(bloque_a.__file__).resolve().parents[1])
b = nuevo_bloque(Path(tempfile.mkdtemp()), cargar_universo(RUTA_UNIVERSO_EJEMPLO))
rng = np.random.default_rng(1)
b.reloj.fijar("2026-01-02")
k = 0
for clase, habil in (("RF", True), ("RV", False)):
    for i in range(150):
        k += 1
        p = float(rng.choice([0.3, 0.7]))
        o = int(rng.random() < (p if habil else 0.5))
        pid = f"PRG-2026-{k:04d}"
        b.almacen.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": pid, "clase": clase, "horizonte": "H3", "prob_interna": p,
                                           "referencia_ingenua": {"valor_o_prob": 0.5}, "en_informe": True, "sentido": "POSITIVO",
                                           "fecha_emision": "2025-01-02", "estado": "ABIERTO",
                                           "fecha_resolucion": str((pd.Timestamp("2025-07-02") + pd.offsets.BDay(i)).date())})
        b.almacen.escribir("F4", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": pid, "estado": "RESUELTO",
                                           "resolucion": {"resultado_binario": o, "valor_observado": 0.01, "comprobacion_fuga": "SUPERADA",
                                                          "fecha_resuelto": "2025-07-02"}})
res = b.evaluador.revisar_certificados("2026-01-02")
celdas = [c["celda"] for c in res["emitidos"]]
print("[1] a mano · certificados emitidos:", celdas)
print("    el ejecutor cumple el caso del plan (uno para RF × H3, ninguno para RV × H3):",
      celdas == [{"clase": "RF", "horizonte": "H3", "metodo": None}])

if len(sys.argv) > 1:
    copia = Path(sys.argv[1]).resolve()
    assert "qa2_mut" in str(copia)
    PY = "/home/user/robotinvestor/.venv/bin/python"
    CITADAS = ["tests/test_integracion.py::test_certificado_emitido_con_muestra_suficiente",
               "tests/test_unitarias.py::test_metricas_de_pronostico_con_pronosticadores_sinteticos",
               "tests/test_t87_datos.py::test_r13_certificado_por_metodo_en_la_entrega"]
    ruta = copia / "bloque_a/motor/evaluacion.py"
    original = ruta.read_text(encoding="utf-8")
    MUT = [("P32a", "el IC del BSS ya no cuenta (una celda sin habilidad se certifica)", "if ic[0] is None or ic[0] <= 0:", "if False:"),
           ("P32b", "la calibración (ECE frente al nulo) ya no cuenta", "if e is None or q90 is None or e > q90:", "if False:"),
           ("P32c", "el tope de ECE ya no cuenta", "if e is None or e >= ece_max:", "if False:"),
           ("P32d", "la muestra mínima ya no cuenta", "elif not (math.isfinite(n_eff) and n_eff >= n_min):", "elif False:")]
    print("[2] mutantes de `criterio_certificado` contra las tres pruebas del ejecutor que el mapa cita para PB-32")
    for mid, desc, viejo, nuevo in MUT:
        assert original.count(viejo) == 1, mid
        ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        try:
            r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", *CITADAS], cwd=copia, capture_output=True, text=True)
        finally:
            ruta.write_text(original, encoding="utf-8")
        print(f"    {mid} {'MUERTO' if r.returncode else 'VIVO'} · {desc} · {(r.stdout.strip().splitlines() or [''])[-1][:80]}")
