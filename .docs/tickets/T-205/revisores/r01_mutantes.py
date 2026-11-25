"""QA r01 de T-205 (revisor): mutantes propios de lo esencial de `bloque_a/seguimiento.py`, distintos de los 22 del
implementador. Aplica cada mutación, corre las pruebas de T-205 y la de `b_agente` de T-201, y restaura el fichero. Un mutante
muere si alguna prueba falla. Ejecútese en una copia que no use nadie más (reescribe `seguimiento.py`).
Uso (desde bloque_a/11_Ejecutor de esa copia): ../../.venv/bin/python <ruta>/r01_mutantes.py ."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
SEG = "bloque_a/seguimiento.py"
PRUEBAS = ["tests/test_t205_clase_seguimiento.py", "tests/test_t201_cuotas.py::test_b_agente_da_el_analista_de_su_clase_o_falla"]
ABS = ("        # Absorción en C1 (7.11.5): si la opción vuelve a estar VIGENTE en el top-3, el ciclo se omite\n"
       "        if opp.get(\"estado\") == \"VIGENTE\":\n"
       "            b.almacen.escribir(\"F11\", \"AG-01\", {\"tipo_entrada\": \"CICLO_OMITIDO\", \"seg_id\": seg_id, \"fecha\": str(as_of.date()),\n"
       "                                                 \"motivo\": \"cubierto en C1: la opción está en el top-3\", \"proximo_ciclo\": self._proximo(enc, as_of)})\n"
       "            return {\"seg_id\": seg_id, \"ejecutado\": False, \"motivo\": \"cubierto en C1\"}\n")
CHK = ("        clase = opp.get(\"clase\")\n"
       "        if not clase_admitida(clase):\n"
       "            return self._c6_clase_no_admitida(enc, opp_id, as_of)\n")
INC_ALTA = "        inc = self.b.almacen.incidencia(\n"
M = [
    # Orden declarado en el README («la clase se comprueba antes que la absorción en C1»)
    ("Q1 C6: la absorción en C1 va antes que la comprobación de la clase", CHK + ABS, ABS + CHK),
    # Fallo cerrado del alta: si el INC- no se puede escribir, el alta no debe seguir
    ("Q2 alta: si el INC- no se escribe, el alta sigue",
     INC_ALTA, "        try:\n            inc = self.b.almacen.incidencia(\n"),
    # (se completa abajo: cierra el try)
    ("Q3 C6: comprobación por verdad y no por los doce tipos", "        if not clase_admitida(clase):\n            return self._c6_clase_no_admitida",
     "        if not clase:\n            return self._c6_clase_no_admitida"),
    ("Q4 C6: la clase sale de F11 y no de F3", "        clase = opp.get(\"clase\")\n        if not clase_admitida(clase):",
     "        clase = enc.get(\"clase\")\n        if not clase_admitida(clase):"),
    ("Q5 C6: el detalle del INC- lleva el valor", "\"activo, o falta. Sin CT-05 ni CT-06; F11 no avanza (T-205)\"",
     "f\"activo, o falta. Sin CT-05 ni CT-06; F11 no avanza (T-205) {enc.get('clase')}{(b.almacen.estado('F3', as_of).get(opp_id) or {}).get('clase')}\""),
    ("Q6 C6: cerrojo solo entre hilos (no entre procesos)", "        with b.almacen._transaccion():\n            previas",
     "        with b.almacen._lock:\n            previas"),
    ("Q7 _seq_clase toma la primera entrada y no la última", "return con_clase[-1].get(\"_seq\") if con_clase else None",
     "return con_clase[0].get(\"_seq\") if con_clase else None"),
    ("Q8 clase_admitida sin distinguir mayúsculas", "return isinstance(clase, str) and clase in AGENTE_CLASE",
     "return isinstance(clase, str) and clase.strip().upper() in AGENTE_CLASE"),
    ("Q9 C6: F11 avanza al omitir", "        b, seg_id = self.b, enc[\"seg_id\"]\n        clave =",
     "        b, seg_id = self.b, enc[\"seg_id\"]\n        b.almacen.escribir(\"F11\", \"AG-01\", {\"tipo_entrada\": \"CICLO_OMITIDO\", \"seg_id\": seg_id, \"proximo_ciclo\": self._proximo(enc, as_of)})\n        clave ="),
    ("Q10 alta: el INC- no lleva el opp_id", "escalado_operador=True, fase=\"ALTA\", opp_id=opp_id,", "escalado_operador=True, fase=\"ALTA\","),
    ("Q11 C6: la deduplicación lee HA fuera de la transacción",
     "        with b.almacen._transaccion():\n            previas = b.almacen.leer(\"HA\", filtro=lambda e: e.get(\"tipo_entrada\") == \"INC\" and e.get(\"fase\") == \"C6\"\n"
     "                                     and e.get(\"campo_afectado\") == \"clase\" and all(e.get(k) == v for k, v in clave.items()))\n",
     "        previas = b.almacen.leer(\"HA\", filtro=lambda e: e.get(\"tipo_entrada\") == \"INC\" and e.get(\"fase\") == \"C6\"\n"
     "                                 and e.get(\"campo_afectado\") == \"clase\" and all(e.get(k) == v for k, v in clave.items()))\n"
     "        with b.almacen._transaccion():\n"),
]

ruta = EJ / SEG
original = ruta.read_text(encoding="utf-8")


def aplicar(nombre, viejo, nuevo):
    if original.count(viejo) != 1:
        return None
    texto = original.replace(viejo, nuevo)
    if nombre.startswith("Q2"):   # cierra el try: si incidencia falla, se sale sin rechazar
        texto = texto.replace("            f3_seq_clase=self._seq_clase(opp_id, as_of))\n        raise ClaseNoAdmitida",
                              "            f3_seq_clase=self._seq_clase(opp_id, as_of))\n        except Exception:\n            return\n        raise ClaseNoAdmitida", 1)
        texto = texto.replace("            inc = self.b.almacen.incidencia(\n            \"OTRO\", f\"Alta",
                              "            inc = self.b.almacen.incidencia(\n                \"OTRO\", f\"Alta", 1)
    return texto


vivos = []
# Ronda de cierre: sin mutar, las pruebas tienen que pasar; si no (p. ej. un nombre de prueba que ya no existe), los mutantes
# «morirían» sin ejecutar nada
if subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *PRUEBAS], cwd=EJ, capture_output=True).returncode:
    sys.exit("las pruebas no pasan sin mutar (¿PRUEBAS cita una prueba que no existe?): no se ejecutan los mutantes")
try:
    for nombre, viejo, nuevo in M:
        texto = aplicar(nombre, viejo, nuevo)
        if texto is None:
            print(f"NO APLICA  {nombre}")
            vivos.append(nombre)
            continue
        ruta.write_text(texto, encoding="utf-8")
        ok = subprocess.run([sys.executable, "-c", f"import ast,sys; ast.parse(open({str(ruta)!r}).read())"]).returncode == 0
        if not ok:
            print(f"SINTAXIS  {nombre}")
            vivos.append(nombre)
            continue
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=EJ,
                           capture_output=True, text=True)
        muerto = r.returncode != 0
        print(f"{'muerto' if muerto else 'VIVO  '}  {nombre}", flush=True)
        if not muerto:
            vivos.append(nombre)
finally:
    ruta.write_text(original, encoding="utf-8")
print(f"{len(M) - len(vivos)} muertos de {len(M)}; vivos: {vivos}")
sys.exit(1 if vivos else 0)
