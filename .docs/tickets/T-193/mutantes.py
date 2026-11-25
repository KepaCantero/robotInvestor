"""Ronda r02 de T-193: mutantes portados del revisor de lo esencial de PB-18.

Cada mutante se aplica en una copia temporal de bloque_a y se pasan las pruebas del ticket. Un mutante VIVO (las pruebas
siguen en verde) que cambia el comportamiento es un hallazgo. Uso, con la venv del repo y desde la raíz del worktree:
    python -I .docs/tickets/T-193/revisores/r01_mutantes_revisor.py [--hilos 3]
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
EJ = Path("bloque_a/11_Ejecutor")
PRUEBAS = ["tests/test_t193_ingesta.py", "tests/test_t53_evaluacion_y_almacen.py::test_monitor_abre_instancias_de_los_analistas_nuevos",
           "tests/test_unitarias.py::test_ht04_y_ht06_y_ht08"]
HT, OR = "bloque_a/herramientas/ht08_monitor.py", "bloque_a/orquestacion.py"
MUTANTES = [
    ("Sin apertura por tiempo", HT, "if lenta or q > self.umbral_cola:", "if q > self.umbral_cola:"),
    ("Cierre una lectura tarde", HT, "if self._lecturas_vacias[ag] >= self.lecturas_cierre:",
     "if self._lecturas_vacias[ag] > self.lecturas_cierre:"),
    ("M01 cierre sin la condición ρ < 0,30", HT,
     "libre = q == 0 and rho is not None and rho < self.rho_cierre", "libre = q == 0"),
    ("M02 cierre con la cola sin vaciar", HT,
     "libre = q == 0 and rho is not None and rho < self.rho_cierre", "libre = rho is not None and rho < self.rho_cierre"),
    ("M03 disparo por tiempo a 1× el objetivo", HT,
     "media > self.factor_tiempo * self.objetivo_ingesta_s", "media > 1 * self.objetivo_ingesta_s"),
    ("M04 dimensionado sin la utilización objetivo 0,75", HT,
     "c = math.ceil(tasa * media / self.rho_objetivo)", "c = math.ceil(tasa * media)"),
    ("M05 λ acumulada entre lecturas", HT,
     "                self._llegadas[ag] = 0\n", ""),
    ("M06 W acumulado desde el arranque (sin restar la lectura previa)", HT,
     "                self._previos[ag] = self.completados[ag], self.tiempo_total[ag]\n", ""),
    ("M07 la ventana no avanza entre lecturas", HT,
     "            self._ultima_lectura = ahora\n", ""),
    ("M08 cierra más de una instancia de golpe", HT,
     "                        self.instancias[ag] -= 1", "                        self.instancias[ag] = 1"),
    ("M09 la histéresis no se reinicia con una lectura ocupada", HT,
     "self._lecturas_vacias[ag] = self._lecturas_vacias[ag] + 1 if libre else 0",
     "self._lecturas_vacias[ag] = self._lecturas_vacias[ag] + 1 if libre else self._lecturas_vacias[ag]"),
    ("M10 F2 sin transacción por lote (vuelta a 9ce57b2)", OR,
     "        with self.almacen._transaccion():\n            self._guardar_lote_evidencia(finales, clasif, clase, as_of, run_id)",
     "        self._guardar_lote_evidencia(finales, clasif, clase, as_of, run_id)"),
    ("M11 la ingesta no se mide", OR,
     "        self.monitor.encolar(\"AG-12\")\n        t0 = self.monitor.inicio(\"AG-12\")",
     "        t0 = self.monitor.inicio(\"AG-12\")"),
]


def correr(carpeta):
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=carpeta / EJ,
                          text=True, capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


def uno(m):
    nombre, ruta, antes, despues = m
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp)
        shutil.copytree(RAIZ / "bloque_a", copia / "bloque_a", ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        archivo = copia / EJ / ruta
        txt = archivo.read_text(encoding="utf-8")
        if txt.count(antes) != 1:
            return nombre, "NO APLICA (texto no único)"
        archivo.write_text(txt.replace(antes, despues), encoding="utf-8")
        r = correr(copia)
        return nombre, "MUERTO" if r.returncode == 1 and " failed" in r.stdout else "VIVO"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--hilos", type=int, default=3)
    a = ap.parse_args()
    resultado = correr(RAIZ)
    if resultado.returncode:
        raise SystemExit(resultado.stdout + resultado.stderr)
    fallos = []
    with ThreadPoolExecutor(a.hilos) as ex:
        for nombre, estado in ex.map(uno, MUTANTES):
            print(f"{estado:6} {nombre}", flush=True)

            if estado != "MUERTO":
                fallos.append(nombre)
    sys.exit(bool(fallos))
