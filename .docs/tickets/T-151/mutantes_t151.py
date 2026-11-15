"""T-151 · mutantes de lo que cambia T-151 (factor en las continuaciones de una generación que buscó, RUN sin análisis con el
presupuesto de C5, reintentos en el cliente con su reserva). Cada mutante se aplica en la copia, se pasan las pruebas
(con -x) y se restaura. Vivo = ninguna prueba lo detecta.

Uso, desde la raíz:  python .docs/tickets/T-151/mutantes_t151.py <copia desechable de la raíz, con «t151_mut» en la ruta>
(la copia necesita al menos `bloque_a/` entero). Termina con 1 si alguno queda vivo o no aplica."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t151_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir(), "copia desechable"
CO, LL, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("consumo", "llm", "orquestacion"))
PRUEBAS = ["tests/test_t151_reintentos.py", "tests/test_t146_presupuesto.py"]
MUTANTES = [
    ("N01", "H-11: se observa en la continuación de una generación que buscó", CO, " and not ya_busco:", ":"),
    ("N02", "H-11: la generación no recuerda que buscó", CO, "        ya_busco = self._pagado.busquedas_web > 0\n",
     "        ya_busco = False\n"),
    ("N03", "H-12: el RUN sin análisis sin el presupuesto de C5", OR,
     "prioridad,\n                                          pres_c5)", "prioridad,\n                                          None)"),
    ("N04", "H-09: el SDK reintenta por su cuenta", LL, "anthropic.Anthropic(api_key=clave, max_retries=0,",
     "anthropic.Anthropic(api_key=clave, max_retries=4,"),
    ("N05", "H-09: un SDK recibido conserva sus reintentos", LL, "        elif callable(getattr(sdk, \"with_options\", None)):",
     "        elif False:"),
    ("N06", "H-09: lo que pudo cobrarse suelta su reserva", CO, "        if not cobro_posible:\n", "        if True:\n"),
    ("N07", "H-09: lo que no se cobró se carga", CO, "        if not cobro_posible:\n", "        if False:\n"),
    ("N08", "H-09: cerrar no carga lo sin respuesta", CO, "            self.p.cargar(self.bolsa, self._sin_respuesta)\n", ""),
    ("N09", "H-09: el reintento no reserva", LL,
     "            if guarda is not None:\n                mt = guarda.reservar(system, msgs, herramientas, int(kwargs[\"max_tokens\"]))\n"
     "                if mt is None:\n                    return None, \"presupuesto_agotado\"",
     "            if False:\n                mt = guarda.reservar(system, msgs, herramientas, int(kwargs[\"max_tokens\"]))\n"
     "                if mt is None:\n                    return None, \"presupuesto_agotado\""),
    ("N10", "H-09: no se reintenta", LL, "reintento >= self.reintentos.maximo:", "True:"),
    ("N11", "H-09: un 429/529 cuenta como cobrado", LL, "return reintenta, reintenta and error.status_code not in regla.sin_cobro",
     "return reintenta, reintenta"),
    ("N12", "H-09: la espera empieza doblada", LL, "self.espera_inicial_s * 2 ** (reintento - 1)", "self.espera_inicial_s * 2 ** reintento"),
    ("N13", "H-09: F5 sin las peticiones sin respuesta", OR, "               if presupuesto.sin_respuesta else {})}",
     "               if False else {})}"),
    ("N14", "H-09: absorber no pasa lo sin respuesta de C5", CO, "            self.sin_respuesta.extend(sin_respuesta)\n", ""),
    ("N15", "H-09: estados sin cobro fuera de los reintentables", LL, "        if not set(sin_cobro) <= set(estados):", "        if False:"),
    ("N16", "H-09: sin x-should-retry", LL,
     "reintenta = pide == \"true\" or (pide != \"false\" and error.status_code in regla.estados)",
     "reintenta = error.status_code in regla.estados"),
    ("N17", "H-09: sin retry-after", LL, "            if math.isfinite(v) and v > 0:\n                return v", "            if False:\n                return v"),
    ("N18", "H-09: sin regla, un timeout no cuenta como cobrado", LL, "        return regla is not None, True",
     "        return regla is not None, regla is not None"),
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
