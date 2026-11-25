"""Mutantes propios de T-205: aplica cada mutación a `bloque_a/seguimiento.py`, corre las pruebas de T-205 (y la de `b_agente`
de T-201) y restaura el fichero. Un mutante muere si alguna prueba falla.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-205/mutantes.py ."""
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
    ("M1 b_agente vuelve al AG-03 por defecto", "    if not clase_admitida(clase):\n        raise ClaseNoAdmitida(\"La clase",
     "    if False:\n        raise ClaseNoAdmitida(\"La clase"),
    ("M2 cualquier cadena es una clase", "return isinstance(clase, str) and clase in AGENTE_CLASE", "return isinstance(clase, str)"),
    ("M3 None y vacía admitidas", "return isinstance(clase, str) and clase in AGENTE_CLASE",
     "return not clase or (isinstance(clase, str) and clase in AGENTE_CLASE)"),
    ("M4 procesar no comprueba antes del CT-24", "            self._exigir_clase_alta(ct24.get(\"opp_id\"), as_of)\n", ""),
    ("M5 _alta no comprueba", "        self._exigir_clase_alta(opp_id, as_of)\n        frec", "        frec"),
    ("M6 el alta nunca rechaza", "if opp_id not in f3 or clase_admitida(f3[opp_id].get(\"clase\")):", "if True:"),
    ("M7 alta: tipo fuera del esquema", "            \"OTRO\", f\"Alta", "            \"DATOS\", f\"Alta"),
    ("M8 alta: sin campo_afectado", "objeto=opp_id, campo_afectado=\"clase\",", "objeto=opp_id,"),
    ("M9 alta: el detalle lleva el valor", "\"falta. No se registra el encargo (T-205)\"",
     "f\"falta. No se registra el encargo (T-205) {f3[opp_id].get('clase')}\""),
    ("M10 alta: escalado_operador falso", "tratamiento=\"rechazada y registrada\", escalado_operador=True",
     "tratamiento=\"rechazada y registrada\", escalado_operador=False"),
    ("M11 C6: vuelve el respaldo de F11", "        clase = opp.get(\"clase\")\n        if not clase_admitida(clase):",
     "        clase = opp.get(\"clase\") or enc.get(\"clase\")\n        if not clase_admitida(clase):"),
    ("M12 C6: sin comprobación", "        if not clase_admitida(clase):\n            return self._c6_clase_no_admitida",
     "        if False:\n            return self._c6_clase_no_admitida"),
    ("M13 C6: sin deduplicar", "            if previas:\n", "            if False:\n"),
    ("M14 C6: la clave no mira los ciclos", ", \"ciclos_encargo\": int(enc.get(\"ciclos\") or 0)}", "}"),
    ("M15 C6: la clave no mira la entrada de F3", "\"f3_seq_clase\": self._seq_clase(opp_id, as_of), ", ""),
    ("M16 C6: sin transacción", "        with b.almacen._transaccion():\n            previas", "        if True:\n            previas"),
    ("M17 _seq_clase cuenta cualquier entrada de F3", "e.get(\"opp_id\") == opp_id and \"clase\" in e)", "e.get(\"opp_id\") == opp_id)"),
    ("M18 C6: tipo fuera del esquema", "                    \"OTRO\", f\"Ciclo C6", "                    \"HERRAMIENTA\", f\"Ciclo C6"),
    ("M19 C6: incidencia_nueva siempre verdadera", "inc_id, nueva = previas[0][\"id\"], False", "inc_id, nueva = previas[0][\"id\"], True"),
    ("M20 C6: escalado_operador falso", "tratamiento=\"ciclo omitido y registrado\", escalado_operador=True",
     "tratamiento=\"ciclo omitido y registrado\", escalado_operador=False"),
    ("M21 C6: sin campo_afectado", "objeto=seg_id, campo_afectado=\"clase\",", "objeto=seg_id,"),
    ("M22 C6: la deduplicación no mira la fase (muere desde test_c6_un_inc_de_otra_fase…)", "e.get(\"tipo_entrada\") == \"INC\" and e.get(\"fase\") == \"C6\"",
     "e.get(\"tipo_entrada\") == \"INC\""),
    # Ronda de cierre de la QA r01: los mutantes vivos Q1 y Q2 del revisor (`revisores/r01_mutantes.py`), con varias sustituciones
    ("Q1 C6: la absorción en C1 va antes que la comprobación de la clase (H-01)", [(CHK + ABS, ABS + CHK)]),
    ("Q2 alta: si el INC- no se escribe, el alta sigue (H-02)", [
        (INC_ALTA, "        try:\n            inc = self.b.almacen.incidencia(\n"),
        ("            f3_seq_clase=self._seq_clase(opp_id, as_of))\n        raise ClaseNoAdmitida",
         "            f3_seq_clase=self._seq_clase(opp_id, as_of))\n        except Exception:\n            return\n        raise ClaseNoAdmitida")]),
    ("Q11 C6: la deduplicación lee HA fuera de la transacción (muere desde test_c6_la_lectura_de_ha_y_el_inc_van_en_la_misma_transaccion)", [
        ("        with b.almacen._transaccion():\n            previas = b.almacen.leer(\"HA\", filtro=lambda e: e.get(\"tipo_entrada\") == \"INC\" and e.get(\"fase\") == \"C6\"\n"
         "                                     and e.get(\"campo_afectado\") == \"clase\" and all(e.get(k) == v for k, v in clave.items()))\n",
         "        previas = b.almacen.leer(\"HA\", filtro=lambda e: e.get(\"tipo_entrada\") == \"INC\" and e.get(\"fase\") == \"C6\"\n"
         "                                 and e.get(\"campo_afectado\") == \"clase\" and all(e.get(k) == v for k, v in clave.items()))\n"
         "        with b.almacen._transaccion():\n")]),
]

ruta = EJ / SEG
original = ruta.read_text(encoding="utf-8")
vivos = []
try:
    for nombre, *cambio in M:
        pares = cambio[0] if len(cambio) == 1 else [tuple(cambio)]   # una sustitución, o una lista de ellas
        texto, aplica = original, True
        for viejo, nuevo in pares:
            if texto.count(viejo) != 1:
                print(f"NO APLICA  {nombre} ({texto.count(viejo)} apariciones)")
                aplica = False
                break
            texto = texto.replace(viejo, nuevo)
        if not aplica:
            vivos.append(nombre)
            continue
        ruta.write_text(texto, encoding="utf-8")
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=EJ,
                           capture_output=True, text=True)
        muerto = r.returncode != 0
        print(f"{'muerto' if muerto else 'VIVO  '}  {nombre}")
        if not muerto:
            vivos.append(nombre)
finally:
    ruta.write_text(original, encoding="utf-8")
print(f"{len(M) - len(vivos)} muertos de {len(M)}; vivos: {vivos}")
sys.exit(1 if vivos else 0)
