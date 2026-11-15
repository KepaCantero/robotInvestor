"""T-154 · mutantes de lo que cambia T-154 (cobro de los 5xx, lo de AG-19 en F5, reparto de las primas con una petición sin
respuesta, `retry-after` y `x-should-retry`). Cada mutante se aplica en la copia, se pasan las pruebas (con -x) y se
restaura. Vivo = ninguna prueba lo detecta.

Uso, desde la raíz:  python .docs/tickets/T-154/mutantes_t154.py <copia desechable de la raíz, con «t154_mut» en la ruta>
(la copia necesita al menos `bloque_a/` entero). Termina con 1 si alguno queda vivo o no aplica."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t154_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "copia desechable"
CO, LL, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("consumo", "llm", "orquestacion"))
PRUEBAS = ["tests/test_t154.py", "tests/test_t151_reintentos.py", "tests/test_t88_consumo.py"]
MUTANTES = [
    ("P01", "H-01: un 5xx que no se reintenta no se carga", LL, "        if error.status_code >= regla.cobro_posible:",
     "        if False:"),
    ("P02", "H-01: un 5xx de los sin cobro (529) se carga", LL, "            return reintenta, error.status_code not in regla.sin_cobro\n",
     "            return reintenta, True\n"),
    ("P03", "H-01: el primer estado con cobro escrito a mano", LL, "frozenset(sin_cobro), float(servidor), desde)",
     "frozenset(sin_cobro), float(servidor), 500)"),
    ("P04", "H-04: sin tope a la espera del servidor", LL, "                return v if v <= self.espera_servidor_max_s else None\n",
     "                return v\n"),
    ("P05", "H-04: con la espera de más, se reintenta igual", LL, "                if espera is None:", "                if False:"),
    ("P06", "H-04: el nombre de la cabecera distingue mayúsculas", LL, "{str(k).lower(): v for k, v in crudas.items()}",
     "{str(k): v for k, v in crudas.items()}"),
    ("P07", "H-04: el valor de x-should-retry con espacios", LL, "\"x-should-retry\", \"\")).lower().strip()",
     "\"x-should-retry\", \"\")).lower()"),
    ("P08", "H-04: espera_servidor_max_s sin validar", LL, ", (\"espera_servidor_max_s\", servidor)):", "):"),
    ("P09", "H-01: cobro_posible_desde sin validar", LL,
     "        if isinstance(desde, bool) or not isinstance(desde, int) or desde < 0:", "        if False:"),
    ("P10", "H-03: el grupo con un fallo reparte lo escrito que se vio", CO,
     "                if grupo in self._grupos_sin_respuesta:\n                    reales = total\n", ""),
    ("P11", "H-03: la liquidación no suelta los grupos marcados", CO, "            self._grupos_sin_respuesta.clear()\n", ""),
    ("P12", "H-03: la petición sin respuesta no marca su grupo", OR,
     "            presupuesto.grupo_sin_respuesta(grupo_primas(self.v6, agente))", "            pass"),
    ("P13", "H-03: el grupo de un analista V6 es él mismo (marca y reparte otro grupo)", OR,
     "    return \"ANALISTAS\" if (v6 and agente in set(AGENTE_CLASE.values())) else agente", "    return agente"),
    ("P14", "H-02: lo de AG-19 no se escribe en F5", OR, "        self._registrar_f9(run_id, presupuesto, marca)\n", ""),
    ("P15", "H-02: la marca, después de la auditoría", OR,
     "        marca = presupuesto.marca()\n        self._auditar(resultado, tipo, nivel, as_of, run_id, presupuesto=presupuesto)\n",
     "        self._auditar(resultado, tipo, nivel, as_of, run_id, presupuesto=presupuesto)\n        marca = presupuesto.marca()\n"),
    ("P16", "H-02: el tramo no empieza en la marca", CO, "list(getattr(self, k)[marca.get(k, 0):])", "list(getattr(self, k))"),
    ("P17", "H-02: la entrada F9 se escribe aunque no haya nada", OR, "        if not tramo.algo():\n            return\n", ""),
    ("P18", "H-02: la entrada F9 con el id del RUN", OR, "\"id\": self.almacen.nuevo_id(\"F5F9\"), \"run_id\": run_id,",
     "\"id\": run_id, \"run_id\": run_id,"),
]


def main() -> int:
    malos = []
    for mid, que, ruta, viejo, nuevo in MUTANTES:
        f = COPIA / ruta
        original = f.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} NO APLICA ({original.count(viejo)} apariciones): {que}", flush=True)
            malos.append(mid)
            continue
        f.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                               cwd=COPIA / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, timeout=3600)
            muerto = r.returncode != 0
        finally:
            f.write_text(original, encoding="utf-8")
        print(f"{mid} {'muerto' if muerto else 'VIVO  '} · {que}", flush=True)
        if not muerto:
            malos.append(mid)
    print(f"{len(MUTANTES) - len(malos)}/{len(MUTANTES)} muertos; vivos o sin aplicar: {', '.join(malos) or 'ninguno'}")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
