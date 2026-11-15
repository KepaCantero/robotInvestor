"""T-146 · mutantes de lo que cambia T-146 (reserva del peor caso petición a petición, cobro de la caché, AG-18/19/20 dentro
del presupuesto, búsquedas en UC, suma de límites). Cada mutante se aplica en la copia, se ejecutan las pruebas y se restaura.

Uso, desde la raíz:  python .docs/tickets/T-146/mutantes_t146.py <copia desechable de la raíz, con «t146_mut» en la ruta>
(la copia necesita al menos `bloque_a/` entero: el ejecutor lee los prompts y las plantillas de la carpeta del bloque)."""
import subprocess
import sys
from pathlib import Path

COPIA = Path(sys.argv[1]).resolve()
assert "t146_mut" in str(COPIA) and (COPIA / "bloque_a" / "11_Ejecutor" / "bloque_a").is_dir()
CO, AG, LL, OR = (f"bloque_a/11_Ejecutor/bloque_a/{f}.py" for f in ("consumo", "agentes", "llm", "orquestacion"))
PRUEBAS = ["tests/test_t146_presupuesto.py", "tests/test_t88_consumo.py"]
MUTANTES = [
    ("M01", "la bolsa no comprueba lo que queda", CO, "if self._limite(clase) - self._ocupado(clase) + 1e-9 >= uc:", "if True:"),
    ("M02", "sin el margen del tokenizador", CO, "tokens = math.ceil(bruto * self.p.factor_de(self.bolsa, self.factor))",
     "tokens = bruto"),
    ("M03", "la entrada no cuenta los mensajes", CO, "    texto += json.dumps(mensajes, ensure_ascii=False, default=_volcar)\n", ""),
    ("M04", "la continuación no reserva", LL, "if guarda is not None and vuelta > 0:", "if False:"),
    ("M05", "la reparación no reserva", AG, "                if guarda is not None:\n                    mt = guarda.reservar(",
     "                if guarda is not None and intento == 0:\n                    mt = guarda.reservar("),
    ("M06", "toda la escritura de caché se aplaza (antes de T-146)", OR, "diferido = min(u.cache_escritura, solo)",
     "diferido = u.cache_escritura"),
    ("M07", "la prima «solo» no se retiene", OR, "diferido, 0 if propio else solo)", "diferido, 0)"),
    ("M08", "las búsquedas no cuentan en UC", CO, "        if uso.busquedas_web:   # T-146", "        if False:   # T-146"),
    ("M09", "AG-19 fuera del presupuesto", OR, "No editas la entrega.\", as_of, run_id,\n                          presupuesto=presupuesto,",
     "No editas la entrega.\", as_of, run_id,\n                          presupuesto=None,"),
    ("M10", "AG-20 fuera del presupuesto", OR, "fuerza.\", as_of, run_id,\n                          presupuesto=presupuesto,",
     "fuerza.\", as_of, run_id,\n                          presupuesto=None,"),
    ("M11", "lo de C5 no pasa a la bolsa del ciclo", OR, "        presupuesto.absorber(pres_c5)\n", ""),
    ("M12", "sin escalar los límites al ciclo", CO, "self._escala = min(1.0, float(tope_total) / total) if", "self._escala = 1.0 if"),
    ("M13", "la ampliación no cuenta lo reservado", CO, "falta = estimado + self._ocupado(clase) - actual",
     "falta = estimado + self.consumido[clase] - actual"),
    ("M14", "sin recorte de la salida", CO, "        if mt >= self.salida_minima:\n", "        if False:\n"),
    ("M15", "sin salida mínima", CO, "        if mt >= self.salida_minima:\n", "        if mt >= 1:\n"),
    ("M16", "los controles no admiten ampliación", OR, "            bolsa, est, control or fase in (", "            bolsa, est, fase in ("),
    ("M17", "lo real no se aparta entre peticiones", CO, "        self.p.retener_real(self.bolsa, real)\n", ""),
    ("M18", "sin factor observado", CO, "            self.p.observar_factor(self.bolsa, entrada / bruto)", "            pass"),
    ("M19", "no pide la ampliación antes de recortar", CO, "self.ampliar is not None and self.ampliar(completo)", "False"),
    ("M20", "cerrar no suelta lo apartado", CO, "        if self._apartado:\n            self.p.liberar(self.bolsa, self._apartado)",
     "        if False:\n            self.p.liberar(self.bolsa, self._apartado)"),
    ("M21", "la liquidación no suelta lo retenido", CO, "            self.retenido.clear()", "            pass"),
    ("M22", "_cargar no usa el prefijo de la primera petición", OR, "        if prefijo is None:\n            prefijo = cacheados",
     "        if True:\n            prefijo = cacheados"),
    ("M23", "la continuación sin presupuesto se repara", AG, "\"contenido_sensible\", \"presupuesto_agotado\")", "\"contenido_sensible\")"),
    ("M24", "la petición negada no cierra la fase", OR, "            presupuesto.cierre_parcial(bolsa, fase or contrato, guarda.negada)\n",
     "            pass\n"),
    ("M25", "G3 (AG-18) sin presupuesto", OR, "Nunca APTO por defecto.\", as_of, run_id,\n                                  presupuesto=presupuesto,",
     "Nunca APTO por defecto.\", as_of, run_id,\n                                  presupuesto=None,"),
    ("M26", "el exceso no se anota", CO, "        if real > w + 1e-4:", "        if False:"),
]


def main() -> int:
    vivos = []
    for mid, que, ruta, viejo, nuevo in MUTANTES:
        f = COPIA / ruta
        original = f.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} NO APLICA ({original.count(viejo)} apariciones): {que}")
            vivos.append(mid)
            continue
        f.write_text(original.replace(viejo, nuevo), encoding="utf-8")
        try:
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS],
                               cwd=COPIA / "bloque_a" / "11_Ejecutor", capture_output=True, text=True, timeout=1800)
        finally:
            f.write_text(original, encoding="utf-8")
        muerto = r.returncode != 0
        print(f"{mid} {'muerto' if muerto else 'VIVO'}: {que}", flush=True)
        if not muerto:
            vivos.append(mid)
    print(f"{len(MUTANTES) - len(vivos)}/{len(MUTANTES)} muertos; vivos: {vivos or 'ninguno'}")
    return 1 if vivos else 0


if __name__ == "__main__":
    sys.exit(main())
