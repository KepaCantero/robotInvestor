"""QA r01 de T-206 (revisor independiente): mutantes propios de lo esencial.

Uso (desde bloque_a/11_Ejecutor de una copia de trabajo desechable): ../../.venv/bin/python ../../.docs/tickets/T-206/revisores/r01_02_mutantes.py .
Primero corre tests/test_t206_tipo_incidencia.py; si el mutante sobrevive, corre además los ocho ficheros de pruebas que
cambian y las vecinas de los caminos (broker, F9). Un mutante vivo tras las dos etapas es un hallazgo, salvo que se declare
equivalente con su motivo.
"""
import subprocess
import sys
from pathlib import Path

EJ = Path(sys.argv[1])
ALM, BRK, ORQ, F9 = "bloque_a/almacen.py", "bloque_a/interfaz_broker.py", "bloque_a/orquestacion.py", "bloque_a/fiabilidad_f9.py"
ETAPA1 = ["tests/test_t206_tipo_incidencia.py"]
ETAPA2 = ETAPA1 + [f"tests/{n}" for n in (
    "test_t198_buscador_ct19.py", "test_t125_r02.py", "test_t65_qa_r01.py", "test_t65_qa_r02.py", "test_t65_qa_r03.py",
    "test_t65_hallazgos.py", "test_t103_r8_y_bajos.py", "test_t116_r05.py", "test_t174_pb61_revision_c2.py",
    "test_t93_hallazgos.py")]

M = [
    # validación
    ("Q1 _incidencia_interna valida después de gastar el contador", ALM,
     "        self._comprobar_tipo_incidencia(tipo)   # T-206: antes de pedir el id\n        self.escribir(\"HA\", \"AG-18\", {\"tipo_entrada\": \"INC\", \"id\": self.nuevo_id(\"INC\"),",
     "        _i = self.nuevo_id(\"INC\")\n        self._comprobar_tipo_incidencia(tipo)\n        self.escribir(\"HA\", \"AG-18\", {\"tipo_entrada\": \"INC\", \"id\": _i,"),
    ("Q2 el error es un ValueError genérico", ALM,
     "            raise TipoIncidenciaNoAdmitido(f\"Tipo de incidencia", "            raise ValueError(f\"Tipo de incidencia"),
    ("Q3 el error cita el detalle (no solo el tipo)", ALM,
     "fuera del esquema de HA (4.8: \"", "fuera del esquema de HA {tipo!r} (4.8: \""),
    ("Q4 la comprobación normaliza mayúsculas y espacios", ALM,
     "        if type(tipo) is not str or tipo not in TIPOS_INCIDENCIA:",   # cierre (H-02): anclaje nuevo
     "        if type(tipo) is not str or tipo.strip().upper() not in TIPOS_INCIDENCIA:"),
    ("Q5 la comprobación con tipo de str (no isinstance) y la pertenencia", ALM,
     "        if type(tipo) is not str or tipo not in TIPOS_INCIDENCIA:",   # cierre (H-02): anclaje nuevo
     "        if tipo not in TIPOS_INCIDENCIA:"),
    # incidencia_de_datos: lo que conserva cada camino
    ("Q6 incidencia_de_datos cambia la severidad por omisión", ALM,
     "    def incidencia_de_datos(self, detalle: str, objeto: str = \"\", severidad: str = \"Material\"",
     "    def incidencia_de_datos(self, detalle: str, objeto: str = \"\", severidad: str = \"Operativa\""),
    ("Q7 incidencia_de_datos pierde el objeto", ALM,
     "self.incidencia(TIPO_INCIDENCIA_DATOS, detalle, objeto, severidad,", "self.incidencia(TIPO_INCIDENCIA_DATOS, detalle, \"\", severidad,"),
    ("Q8 incidencia_de_datos pierde la severidad pedida", ALM,
     "self.incidencia(TIPO_INCIDENCIA_DATOS, detalle, objeto, severidad,", "self.incidencia(TIPO_INCIDENCIA_DATOS, detalle, objeto, \"Material\","),
    ("Q9 incidencia_de_datos pierde las marcas extra", ALM,
     "severidad, categoria=CATEGORIA_DATOS, **extra)", "severidad, categoria=CATEGORIA_DATOS)"),
    ("Q10 categoria con otro valor", ALM, "CATEGORIA_DATOS = \"DATOS\"", "CATEGORIA_DATOS = \"DATO\""),
    # lector
    ("Q11 el lector toma cualquier categoria", ALM,
     "or entrada.get(\"categoria\") == CATEGORIA_DATOS)", "or bool(entrada.get(\"categoria\")))"),
    ("Q12 el lector toma cualquier OTRO", ALM,
     "or entrada.get(\"categoria\") == CATEGORIA_DATOS)", "or entrada.get(\"tipo\") == \"OTRO\")"),
    # caminos: severidad, objeto y marcas de cada uno (CA-3: «conservan su objeto, severidad, tratamiento y marcas»)
    ("Q13 broker C2 sin alcance pierde escalado_operador", BRK,
     "tratamiento=f\"revisar a mano el alcance de la revisión C2 de {cns_id}\", escalado_operador=True)",
     "tratamiento=f\"revisar a mano el alcance de la revisión C2 de {cns_id}\")"),
    ("Q14 broker C2 sin alcance pierde su tratamiento", BRK,
     "tratamiento=f\"revisar a mano el alcance de la revisión C2 de {cns_id}\", escalado_operador=True)",
     "escalado_operador=True)"),
    ("Q15 broker plazo ilegible cambia de objeto", BRK,
     "\"se da por vencida y el análisis sigue con el supuesto declarado\", \"AG-01\")",
     "\"se da por vencida y el análisis sigue con el supuesto declarado\", \"AG-18\")"),
    ("Q16 referencia inválida cambia de severidad", ORQ,
     "\"tipo no analizado en este ciclo\", ref, severidad=\"Operativa\",", "\"tipo no analizado en este ciclo\", ref, severidad=\"Menor\","),
    ("Q17 datos inválidos de un símbolo pierde run_id", ORQ,
     "tratamiento=\"símbolo excluido y declarado como laguna del tipo\",\n                                    run_id=run_id)",
     "tratamiento=\"símbolo excluido y declarado como laguna del tipo\")"),
    ("Q18 datos inválidos de un símbolo cambia de severidad", ORQ,
     "s, severidad=\"Operativa\", tratamiento=\"símbolo excluido", "s, severidad=\"Menor\", tratamiento=\"símbolo excluido"),
    ("Q19 CT-19 no atendido pierde run_id", ORQ,
     "\"se reintenta en el ciclo siguiente\", \"AG-16\", severidad=\"Operativa\", run_id=run_id)",
     "\"se reintenta en el ciclo siguiente\", \"AG-16\", severidad=\"Operativa\")"),
    ("Q20 CT-19 no atendido cambia de severidad", ORQ,
     "\"se reintenta en el ciclo siguiente\", \"AG-16\", severidad=\"Operativa\", run_id=run_id)",
     "\"se reintenta en el ciclo siguiente\", \"AG-16\", severidad=\"Material\", run_id=run_id)"),
    ("Q21 pronóstico no registrable pierde run_id", ORQ,
     "                                severidad=\"Menor\", run_id=run_id)\n        return \"PREVISION\"",
     "                                severidad=\"Menor\")\n        return \"PREVISION\""),
    ("Q22 F9 sin fichas cambia de severidad", F9,
     "\"reintentan en el ciclo siguiente\", \"AG-16\", severidad=\"Operativa\", run_id=run_id,",
     "\"reintentan en el ciclo siguiente\", \"AG-16\", severidad=\"Material\", run_id=run_id,"),
    ("Q23 F9 sin fichas pierde run_id", F9,
     "\"reintentan en el ciclo siguiente\", \"AG-16\", severidad=\"Operativa\", run_id=run_id,",
     "\"reintentan en el ciclo siguiente\", \"AG-16\", severidad=\"Operativa\","),
    ("Q24 F9 fuente fuera cambia de severidad", F9,
     "\"incorporar y no se vuelve a enviar al Buscador\", \"AG-16\", severidad=\"Operativa\", run_id=run_id,",
     "\"incorporar y no se vuelve a enviar al Buscador\", \"AG-16\", severidad=\"Material\", run_id=run_id,"),
    ("Q25 F9 fuente fuera pierde su tratamiento", F9,
     "fue_no_atendible=f.get(\"fue_id\"), tratamiento=\"declarada una vez; excluida de los CT-19 siguientes\")",
     "fue_no_atendible=f.get(\"fue_id\"))"),
]
# Q3 es equivalente (mal planteado): `_comprobar_tipo_incidencia` no recibe el detalle, así que el mutante solo repite el tipo
# en el mensaje; la prueba que exige que el error no cite el detalle ya la cubre test_ca2_el_rechazo_es_un_error_propio_….
EQUIVALENTES: dict[str, str] = {"Q3 el error cita el detalle (no solo el tipo)": "solo repite el tipo"}


def correr(pruebas):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *pruebas],
                       cwd=EJ, capture_output=True, text=True, check=False)
    return r.returncode != 0


# Opcional: QA_DESDE=Q15 empieza en ese mutante (para retomar una ejecución cortada)
import os

_desde = os.environ.get("QA_DESDE")
if _desde:
    M = M[[n.split()[0] for n, *_ in M].index(_desde):]
vivos = []
for nombre, f, a, b in M:
    p = EJ / f
    orig = p.read_text(encoding="utf-8")
    assert orig.count(a) == 1, (nombre, orig.count(a))
    p.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        etapa = "1"
        muerto = correr(ETAPA1)
        if not muerto:
            etapa = "2"
            muerto = correr(ETAPA2)
    finally:
        p.write_text(orig, encoding="utf-8")
    estado = "MUERTO" if muerto else ("VIVO (equivalente)" if nombre in EQUIVALENTES else "VIVO")
    print(f"{nombre}: {estado} (etapa {etapa})", flush=True)
    if not muerto and nombre not in EQUIVALENTES:
        vivos.append(nombre)
print("vivos:", vivos)
sys.exit(1 if vivos else 0)
