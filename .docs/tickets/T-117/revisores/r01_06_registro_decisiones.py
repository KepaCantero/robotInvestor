"""QA r01 (común a T-114, T-116 y T-117) · Muestreo del registro `Decisiones_del_operador_Bloque_A.md`: la clave que cita cada
fila existe en `por_defecto.yaml` y vale lo que dice. Uso, desde la raíz:  python <este fichero>"""
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[4]
cfg = yaml.safe_load((RAIZ / "bloque_a/11_Ejecutor/config/por_defecto.yaml").read_text(encoding="utf-8"))
registro = (RAIZ / "sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md").read_text(encoding="utf-8")


def valor(clave):
    o = cfg
    for parte in clave.split("."):
        if not isinstance(o, dict) or parte not in o:
            return "<<NO EXISTE>>"
        o = o[parte]
    return o


# (clave citada en la columna «Dónde», lo que dice la columna «Valor hoy», valor esperado en el yaml)
MUESTRA = [
    ("diseno", "V5", "v5"),
    ("perfiles.activos", "Solo divisas (DIV)", ["DIV"]),
    ("seleccion.umbral_senal_gc1", "0,75", 0.75),
    ("v6.gc1.umbral_por_perfil", "0,65 en RF, MON y TCV", {"RF": 0.65, "MON": 0.65, "TCV": 0.65}),
    ("v6.gc1.senal_por_perfil", "la compuesta en los doce", None),
    ("v6.gc1.familias_min", "2", 2),
    ("v6.gc1.exploracion_celdas", "2 por tipo", 2),
    ("seleccion.max_candidatas", "8", 8),
    ("seleccion.max_finalistas", "5", 5),
    ("parametros_ht03.max_opciones_por_clase", "3", 3),
    ("parametros_ht03.max_por_cluster", "(cita la clave)", None),
    ("parametros_ht03.diversidad_margen_rk", "10 puntos", 10),
    ("seleccion.siguiente_paso", "E 70; A 65", None),
    ("seleccion.semaforo", "(cita la clave)", None),
    ("presentacion.confianza_probable_E", "70", 70),
    ("seleccion.rotacion_exploratoria_celdas", "2", 2),
    ("ps1.raices_min", "2", 2),
    ("contrarias.moderadas_para_fragil", "2", 2),
    ("presupuesto_uc", "N0 1, N1 5, N2 18, N3 50; semanal 240", None),
    ("presupuesto_uc.ampliacion_sin_autorizacion", "+25 %", 0.25),
    ("presupuesto_uc.ampliacion_max_autorizable", "+50 %", 0.5),
    ("presupuesto_uc.reparto_fases", "35/20/15/20/10 %", None),
    ("v6.auditoria_fraccion", "25 %", 0.25),
    ("aprendizaje.solo_endurecer", "Sí", True),
    ("evaluacion.ece_revocacion", "0,12", 0.12),
    ("evaluacion.recalibracion_rk", "pasos 0,05; ±0,05; ±0,15; tres meses", None),
    ("pregunta_repetida", "3 veces en 4 semanas", None),
    ("backtest.anonimizar", "se anonimiza", None),
    ("backtest.fecha_corte_modelo", "(cita la clave)", None),
    ("ps2_antiguedad_maxima_dias", "(cita la clave)", None),
    ("ps2_festivos", "(cita la clave)", None),
]
mal = 0
for clave, dice, esperado in MUESTRA:
    citada = f"`{clave}`" in registro or f"`{clave.rsplit('.', 1)[0]}" in registro
    v = valor(clave)
    estado = "OK"
    if v == "<<NO EXISTE>>":
        estado = "!! LA CLAVE NO EXISTE EN EL YAML"
    elif esperado is not None and v != esperado:
        estado = f"!! EL VALOR NO COINCIDE (esperado {esperado!r})"
    mal += estado != "OK"
    print(f"{estado:<34} {clave:<45} registro: {dice:<38} yaml: {str(v)[:110]}{'' if citada else '  (clave no citada tal cual)'}")
print(f"{len(MUESTRA)} filas comprobadas, {mal} con problema")
sys.exit(0)
