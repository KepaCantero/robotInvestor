"""T-176 · Mutantes de PB-36 (ajustes de F10, revisión trimestral, elevación por CT-19) y PB-33 (Novedades de F6).

Copia `bloque_a/11_Ejecutor` a una carpeta temporal, aplica cada mutante (sustitución de texto que debe aparecer una sola vez)
y ejecuta `tests/test_t176_pb36_pb33.py`; el mutante debe morir (alguna prueba falla).

Uso, desde la raíz y con el Python del `.venv`: .venv/bin/python .docs/tickets/T-176/mutantes.py
Termina con 1 si alguno no aplica o vive.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
EV, OR = "bloque_a/evaluador.py", "bloque_a/orquestacion.py"
PRUEBAS = ["tests/test_t176_pb36_pb33.py"]
MUTANTES = [
    ("M01", "no comprueba CALIBRABLE", EV, "        if param_id not in PARAMETROS_CALIBRABLES:\n            raise", "        if False:\n            raise"),
    ("M02", "sin banda pasa como dentro", EV, 'if not banda or banda.get("estado") != "DEFINIDA":', "if not banda:"),
    ("M03", "banda trimestral sin lo del trimestre", EV, "fuera = abs(delta) + en_trimestre > b_trim", "fuera = abs(delta) > b_trim"),
    ("M04", "sin banda total", EV, " or abs(objetivo - ini) > b_tot + 1e-9", ""),
    ("M05", "límite estricto en la banda trimestral", EV, "en_trimestre > b_trim + 1e-9", "en_trimestre >= b_trim"),
    ("M06", "el AJU- no se marca propuesto", EV, '"estado": "PROPUESTO", "aplicado_en_produccion": False, "propuesta": True, "fecha"',
     '"estado": "EN_SOMBRA", "aplicado_en_produccion": False, "propuesta": True, "fecha"'),
    ("M07", "ajuste_en_sombra coge cualquier parámetro", EV, 'and a.get("parametro", "P-11") == "P-11":', ":"),
    ("M08", "Youden sin empate al vigente", EV, "clave = (round(j, 12), -abs(t - vig), t)", "clave = (round(j, 12), t, 0)"),
    ("M09", "Youden con J ≤ 0 propone", EV, "        if j <= 0:\n", "        if j < -1:\n"),
    ("M10", "sin muestra mínima", EV, "        if len(res) < n_min:\n            return {**base, \"motivo\"",
     "        if len(res) < 1:\n            return {**base, \"motivo\""),
    ("M11", "revisión sin registro único", EV, '        if rid in self.almacen.estado("F6", as_of, clave="id"):\n            return None\n', ""),
    ("M12", "RTR- también sin evidencia", EV, "        if not con_objetivo:\n            return", "        if False:\n            return"),
    ("M13", "la P3- no queda ENVIADA", EV, '"run_id": run_id, "estado": "ENVIADA", "elevada_via": None}',
     '"run_id": run_id, "estado": "PENDIENTE", "elevada_via": None}'),
    ("M14", "P3- sin plan de reversión", EV, '"plan_reversion": f"Si se aprueba', '"_plan_reversion": f"Si se aprueba'),
    ("M15", "propuesta repetida (r02: la línea de H-03)", EV,
     '            if (a.get("tipo_entrada") == "P3" and a.get("estado") == "ENVIADA") or (',
     '            if False and (a.get("tipo_entrada") == "P3" and a.get("estado") == "ENVIADA") or ('),
    ("M16", "elevación no comprueba HA", OR, '            if p["id"] not in en_ha:\n                self.almacen.escribir("HA"',
     '            if True:\n                self.almacen.escribir("HA"'),
    ("M17", "elevación no anota elevada_via", OR, '{"tipo_entrada": "P3", "id": p["id"], "elevada_via": msg["msg_id"]}',
     '{"tipo_entrada": "P3", "id": p["id"]}'),
    ("M18", "HA sin PENDING_OPERATOR", OR, '"recibida_via": msg["msg_id"], "estado": "PENDING_OPERATOR"',
     '"recibida_via": msg["msg_id"], "estado": "ENVIADA"'),
    ("M19", "ciclo sin elevar", OR, "            self.elevar_propuestas_tipo3(as_of, run_id)   # T-176", "            pass   # T-176"),
    ("M20", "CT-19 a otro receptor", OR, '"CT-19", "AG-20", "AG-18", {"tipo": "PROPUESTA_TIPO_3"', '"CT-19", "AG-20", "AG-02", {"tipo": "PROPUESTA_TIPO_3"'),
    ("M21", "Novedades sin corte de la anterior", EV, "        desde = max((int(e.get(\"hasta_seq\") or 0) for e in previas), default=0)\n",
     "        desde = 0\n"),
    ("M22", "la primera sección sin el lunes", EV, "        if not previas:   # la primera", "        if False:   # la primera"),
    ("M23", "Novedades repite cambios de estado", EV, "or (tipo, ident) in vistos:", ":"),
    ("M24", "Novedades con lecciones no vigentes", EV, '            if tipo == "LEC" and e.get("estado") != "VIGENTE":\n                continue\n', ""),
    ("M25", "Novedades vacía se publica", EV, "        if not any(apartados.values()):\n            return None\n", ""),
    ("M26", "ciclo sin Novedades", EV, "novedades = self.publicar_novedades(as_of, run_id)", "novedades = None"),
    ("M27", "ciclo sin revisión trimestral", EV, "revision_trimestral = self.revision_trimestral(as_of, run_id)", "revision_trimestral = None"),
    ("M28", "revocación fuera de Novedades", EV, '"CERT_REVOCACION": "revocaciones", ', ""),
    # r02 (QA r01, H-01 a H-06)
    ("M29", "H-01 recalibrar repite la P3- de P-11", EV, "            if abierta:\n                return", "            if False:\n                return"),
    ("M30", "H-01 la P3- de P-11 sin parametro", EV, '"objeto": "P-11 pesos de RK", "parametro": "P-11",', '"objeto": "P-11 pesos de RK",'),
    ("M31", "H-02 la P3- de P-11 sin plan de reversión", EV, '"plan_reversion": "Si se aprueba y aplica, un CFG- nuevo con revierte_a devuelve P-11',
     '"_plan_reversion": "Si se aprueba y aplica, un CFG- nuevo con revierte_a devuelve P-11'),
    ("M32", "H-03 la P3- abierta solo bloquea el mismo objetivo", EV,
     'if (a.get("tipo_entrada") == "P3" and a.get("estado") == "ENVIADA") or (',
     'if (a.get("tipo_entrada") == "P3" and a.get("estado") == "ENVIADA" and a.get("a") == objetivo) or ('),
    ("M33", "H-04 proponer_ajuste sin transacción", EV,
     "        with self.almacen._transaccion():\n            return self._proponer_ajuste(",
     "        if True:\n            return self._proponer_ajuste("),
    ("M34", "H-04 revisión sin transacción", EV, "        with self.almacen._transaccion():\n            return self._revision_trimestral(",
     "        if True:\n            return self._revision_trimestral("),
    ("M35", "H-04 elevación sin transacción", OR, "        with self.almacen._transaccion():\n            return self._elevar_propuestas_tipo3(",
     "        if True:\n            return self._elevar_propuestas_tipo3("),
    ("M36", "H-05 sin las específicas de R18", EV, ', *parametro(cfg, "evaluacion.regresion_r18")]', "]"),
    ("M38", "H-07 recalibrar sin transacción", EV, "        with self.almacen._transaccion():\n            return self._recalibrar(",
     "        if True:\n            return self._recalibrar("),
    ("M37", "H-06 la que tiene elevada_via no se mira en HA", OR, '(not p.get("elevada_via") or p["id"] not in en_ha)',
     '(not p.get("elevada_via"))'),
]


def main() -> int:
    malos = []
    with tempfile.TemporaryDirectory(prefix="t176_mut_") as tmp:
        copia = Path(tmp) / "11_Ejecutor"
        shutil.copytree(EJ, copia, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".mypy_cache"))
        for mid, desc, rel, viejo, nuevo in MUTANTES:
            f = copia / rel
            orig = f.read_text(encoding="utf-8")
            if orig.count(viejo) != 1:
                print(f"{mid} NO APLICA ({orig.count(viejo)} apariciones): {desc}")
                malos.append(mid)
                continue
            f.write_text(orig.replace(viejo, nuevo), encoding="utf-8")
            try:
                r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=copia,
                                   capture_output=True, text=True, timeout=900)
            finally:
                f.write_text(orig, encoding="utf-8")
            vive = r.returncode == 0
            print(f"{mid} {'VIVE' if vive else 'muere'}: {desc}")
            if vive:
                malos.append(mid)
    print(f"{len(MUTANTES) - len(malos)}/{len(MUTANTES)} muertos" + (f"; fallan: {', '.join(malos)}" if malos else ""))
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
