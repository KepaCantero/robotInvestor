"""Mutantes propios de T-206: aplica cada mutación, corre tests/test_t206_tipo_incidencia.py y restaura.
Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-206/mutantes.py ."""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
ALM, BRK, ORQ, F9 = "bloque_a/almacen.py", "bloque_a/interfaz_broker.py", "bloque_a/orquestacion.py", "bloque_a/fiabilidad_f9.py"
CHECK = "        self._comprobar_tipo_incidencia(tipo, extra)   # T-206: falla cerrado antes de pedir el id (sin contador ni entrada)\n"


def revertir(prefijo: str) -> tuple[str, str]:
    """El sitio vuelve a escribir `tipo` DATOS, como antes de T-206."""
    return f"incidencia_de_datos({prefijo}", f"incidencia(\"DATOS\", {prefijo}"


M = [
 ("M1 incidencia sin validar el tipo", ALM, CHECK, ""),
 ("M2 _incidencia_interna sin validar el tipo", ALM, "        self._comprobar_tipo_incidencia(tipo)   # T-206: antes de pedir el id\n", ""),
 ("M3 valida después de gastar el contador", ALM, CHECK,
  "        self.nuevo_id(\"INC\")\n        self._comprobar_tipo_incidencia(tipo, extra)\n"),
 ("M4 sin comprobar que es texto", ALM, "        if type(tipo) is not str or tipo not in TIPOS_INCIDENCIA:",
  "        if tipo not in TIPOS_INCIDENCIA:"),
 ("M4b isinstance en vez del tipo exacto (cierre H-02)", ALM, "        if type(tipo) is not str or tipo not in TIPOS_INCIDENCIA:",
  "        if not isinstance(tipo, str) or tipo not in TIPOS_INCIDENCIA:"),
 ("M5 el enumerado admite DATOS", ALM, "                    \"OTRO\")\n", "                    \"OTRO\", \"DATOS\")\n"),
 ("M6 el enumerado pierde ESCRITURA", ALM, "\"HERRAMIENTA\", \"ESCRITURA\",\n", "\"HERRAMIENTA\",\n"),
 ("M7 los de datos como HERRAMIENTA", ALM, "TIPO_INCIDENCIA_DATOS = \"OTRO\"", "TIPO_INCIDENCIA_DATOS = \"HERRAMIENTA\""),
 ("M8 sin categoria DATOS", ALM, "severidad, categoria=CATEGORIA_DATOS, **extra)", "severidad, **extra)"),
 ("M9 el lector no reconoce las antiguas", ALM, "    return (entrada.get(\"tipo\") == CATEGORIA_DATOS\n", "    return (False\n"),
 ("M10 el lector no reconoce las nuevas", ALM, "or entrada.get(\"categoria\") == CATEGORIA_DATOS)", "or False)"),
 ("M11 el lector no mira tipo_entrada", ALM, "    if entrada.get(\"tipo_entrada\") != \"INC\" or entrada.get(\"tipo\") not in",
  "    if entrada.get(\"tipo\") not in"),
 # cierre de la QA r01 (H-03): la categoría DATOS solo con OTRO
 ("M21 el lector toma cualquier tipo con categoria DATOS", ALM,
  " not in (CATEGORIA_DATOS, TIPO_INCIDENCIA_DATOS):\n        return False", " is None:\n        return False"),
 ("M22 incidencia no comprueba la categoría", ALM,
  "        if extra is not None and \"categoria\" in extra:", "        if False:"),
 ("M23 la categoría se admite con cualquier tipo", ALM, " or cat != CATEGORIA_DATOS or tipo != TIPO_INCIDENCIA_DATOS:",
  " or cat != CATEGORIA_DATOS:"),
 ("M24 la categoría se admite con cualquier valor", ALM, " or cat != CATEGORIA_DATOS or tipo != TIPO_INCIDENCIA_DATOS:",
  " or tipo != TIPO_INCIDENCIA_DATOS:"),
 ("M25 categoría sin tipo exacto", ALM, "            if type(cat) is not str or cat != CATEGORIA_DATOS",
  "            if cat != CATEGORIA_DATOS"),
 ("M26 incidencia no pasa la categoría a la comprobación", ALM, CHECK,
  "        self._comprobar_tipo_incidencia(tipo)\n"),
 # cierre de la QA r01 (H-04): la escritura genérica
 ("M27 escribir no comprueba una INC- de HA", ALM, "        if archivo == \"HA\" and tipo == \"INC\":", "        if False:"),
 ("M28 escribir no comprueba la categoría de una INC-", ALM,
  "                self._comprobar_tipo_incidencia(entrada.get(\"tipo\"), entrada)",
  "                self._comprobar_tipo_incidencia(entrada.get(\"tipo\"))"),
 # cierre de la QA r01 (H-06): la vista del operador
 ("M29 estado no enseña la categoría", "bloque_a/orquestacion.py", "**({\"categoria\": e[\"categoria\"]} if \"categoria\" in e else {})", ""),
 ("M30 estado enseña categoria en todas", "bloque_a/orquestacion.py",
  "**({\"categoria\": e[\"categoria\"]} if \"categoria\" in e else {})", "\"categoria\": e.get(\"categoria\")"),
 # cierre de la QA r01 (H-05): los diez mutantes vivos del revisor (Q6, Q14, Q15, Q16, Q18, Q20, Q21, Q22, Q24 y Q25)
 ("Q6 incidencia_de_datos cambia la severidad por omisión", ALM,
  "    def incidencia_de_datos(self, detalle: str, objeto: str = \"\", severidad: str = \"Material\"",
  "    def incidencia_de_datos(self, detalle: str, objeto: str = \"\", severidad: str = \"Operativa\""),
 ("Q14 broker C2 sin alcance pierde su tratamiento", BRK,
  "tratamiento=f\"revisar a mano el alcance de la revisión C2 de {cns_id}\", escalado_operador=True)",
  "escalado_operador=True)"),
 ("Q15 broker plazo ilegible cambia de objeto", BRK,
  "\"se da por vencida y el análisis sigue con el supuesto declarado\", \"AG-01\")",
  "\"se da por vencida y el análisis sigue con el supuesto declarado\", \"AG-18\")"),
 ("Q16 referencia inválida cambia de severidad", ORQ,
  "\"tipo no analizado en este ciclo\", ref, severidad=\"Operativa\",", "\"tipo no analizado en este ciclo\", ref, severidad=\"Menor\","),
 ("Q18 datos inválidos de un símbolo cambia de severidad", ORQ,
  "s, severidad=\"Operativa\", tratamiento=\"símbolo excluido", "s, severidad=\"Menor\", tratamiento=\"símbolo excluido"),
 ("Q20 CT-19 no atendido cambia de severidad", ORQ,
  "\"se reintenta en el ciclo siguiente\", \"AG-16\", severidad=\"Operativa\", run_id=run_id)",
  "\"se reintenta en el ciclo siguiente\", \"AG-16\", severidad=\"Material\", run_id=run_id)"),
 ("Q21 pronóstico no registrable pierde run_id", ORQ,
  "                                severidad=\"Menor\", run_id=run_id)\n        return \"PREVISION\"",
  "                                severidad=\"Menor\")\n        return \"PREVISION\""),
 ("Q22 F9 sin fichas cambia de severidad", F9,
  "\"reintentan en el ciclo siguiente\", \"AG-16\", severidad=\"Operativa\", run_id=run_id,",
  "\"reintentan en el ciclo siguiente\", \"AG-16\", severidad=\"Material\", run_id=run_id,"),
 ("Q24 F9 fuente fuera cambia de severidad", F9,
  "\"incorporar y no se vuelve a enviar al Buscador\", \"AG-16\", severidad=\"Operativa\", run_id=run_id,",
  "\"incorporar y no se vuelve a enviar al Buscador\", \"AG-16\", severidad=\"Material\", run_id=run_id,"),
 ("Q25 F9 fuente fuera pierde su tratamiento", F9,
  "fue_no_atendible=f.get(\"fue_id\"), tratamiento=\"declarada una vez; excluida de los CT-19 siguientes\")",
  "fue_no_atendible=f.get(\"fue_id\"))"),
 ("M12 broker: revisión C2 sin alcance escribe DATOS", BRK, *revertir("f\"La revisión C2 de {cns_id} no tiene")),
 ("M13 broker: plazo ilegible escribe DATOS", BRK, *revertir("f\"Consulta CT-23 {k} con un plazo")),
 ("M14 orquestación: referencia inválida escribe DATOS", ORQ, *revertir("f\"HT-01: referencia de comparación")),
 ("M15 orquestación: datos inválidos escribe DATOS", ORQ, *revertir("f\"HT-01: datos inválidos de")),
 ("M16 orquestación: CT-19 no atendido escribe DATOS", ORQ, *revertir("f\"CT-19 {msg['msg_id']} no atendido")),
 ("M17 orquestación: pronóstico no registrable escribe DATOS", ORQ, *revertir("f\"Pronóstico de fuente no registrable")),
 ("M18 F9: sin fichas escribe DATOS", F9, *revertir("f\"F9 no se pudo leer")),
 ("M19 F9: fuente fuera de F9 escribe DATOS", F9, *revertir("f\"{f.get('fue_id')}: la fuente")),
 ("M20 F9: la marca antigua no cuenta", F9, "if isinstance(e.get(\"fue_no_atendible\"), str)}",
  "if isinstance(e.get(\"fue_no_atendible\"), str) and e.get(\"tipo\") != \"DATOS\"}"),
]
# Cierre de la QA r01 (H-02): M4 no era equivalente (un objeto o una subclase de str con == permisivo pasaba); ahora la
# comprobación es del tipo exacto y M4 y M4b tienen que morir. No queda ningún equivalente.
EQUIVALENTES: set[str] = set()
vivos = []
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "tests/test_t206_tipo_incidencia.py"],
                           cwd=EJ, capture_output=True, text=True, check=False)
    finally:
        p.write_text(orig, encoding="utf-8")
    muerto = r.returncode != 0
    print(f"{nombre}: {'MUERTO' if muerto else ('VIVO (equivalente)' if nombre in EQUIVALENTES else 'VIVO')}", flush=True)
    if not muerto and nombre not in EQUIVALENTES:
        vivos.append(nombre)
print("vivos:", vivos)
sys.exit(1 if vivos else 0)
