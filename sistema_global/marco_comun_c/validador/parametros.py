"""Parámetros del sistema en un solo objeto versionado (T-25; Constitución: «umbrales, pesos y límites viven en configuración
versionada»). Aquí están los valores [PROPUESTO] que antes vivían sueltos en K, D, H y CT-G-14; los del Orquestador y la
política de F siguen en su configuración (CONFIG_DEFECTO), y su huella común la calcula el Orquestador (`huella_configuracion`).

Cambiar un valor exige cambiar VERSION_PARAMETROS: la huella de cada decisión anotada lo delata.
"""
from __future__ import annotations

from types import MappingProxyType

VERSION_PARAMETROS = "PAR-0.4.0"   # 0.2.0 (T-26): licencias admitidas por K. 0.3.0 (T-17): costes y confianza en D. 0.4.0 (V0.67): tope de líneas del diario en el panel

_VALORES = {
    # K — calidad y antigüedad de los datos de corte
    "k_tope_antiguedad_dias_habiles": {"TRADING": 1, "TACTICA": 1, "LARGO_PLAZO": 5},
    "k_min_observaciones": 20,
    "k_rango_max_intradia": 1.5,
    "k_salto_adv_bloq": (0.20, 0.50),          # Q-04
    "k_hueco_adv_bloq": (0.02, 0.10),          # Q-05
    "k_cruce_adv_bloq": (0.001, 0.01),         # Q-09
    "k_ventana_acumulado_obs": 5,              # Q-04
    "k_ajuste_tol_rel": 0.10,                  # tolerancia entre el factor de un ajuste y el salto observado
    "k_licencias_admitidas": ("PROPIA", "INTERMEDIARIO-USO-INTERNO", "CC-BY-4.0", "DOMINIO-PUBLICO"),   # Q-14 (T-26) [PROPUESTO, D-29]
    # D — comparación de candidatos
    "d_peso_evidencia": {"VERIFICADO": 1.0, "ESTIMADO": 0.5, "SUPUESTO": 0.25},
    "d_margen_ajustado": 0.05,
    "d_riesgo_min_pct": 1.0,
    "d_tope_confianza_clase": {"Q": 0.80, "S": 0.60, "K": 0.40},
    "d_exceso_min_pct": 0.10,
    "d_rentabilidad_plausible_pct": (-100.0, 500.0),
    "d_referencia_rango_pct": (-5.0, 50.0),
    "d_coste_suelo_ida_vuelta_pb": {"Q": 2.0, "S": 10.0, "K": 30.0},   # T-17: coste mínimo de entrar y salir que D descuenta si el sobre declara menos [PROPUESTO, D-30]
    "d_coste_suelo_mant_anual_pb": {"Q": 0.0, "S": 0.0, "K": 0.0},     # T-17: coste anual mínimo de mantener [PROPUESTO, D-30]
    "d_factor_tope_sin_doble_analisis": 0.75,                         # T-17: sin doble análisis que la confirme (no hecho o discrepante), la confianza no pasa de esta fracción del tope de la clase, como en V-14 [PROPUESTO, D-30]
    "d_riesgo_sin_stop_largo_pct": 100.0,                             # T-17: sin stop legible, un LARGO sin apalancar puede perderlo todo [PROPUESTO, D-30]
    # H — vigilancia
    "h_max_edad_dato_min": 15,
    "h_salto_max_horas": 72,
    # E y el Orquestador
    "e_max_edad_dimensionado_min": 60,
    # CT-G-14 — declaración manual
    "manual_ventana_declaracion_horas": 72,
    # N — consola. V0.64 lo dejaba escrito en la firma de panel(); V0.67 lo trae aquí (regla 5 del kit)
    "n_lineas_diario_ambar": 1000,   # líneas del diario sin punto de control a partir de las que el panel avisa en ámbar [PROPUESTO]
}


def _congela(x):
    if isinstance(x, dict):
        return MappingProxyType({k: _congela(v) for k, v in x.items()})
    return x


# De solo lectura: un valor solo cambia con otra versión del fichero (y entonces cambia la huella de todo lo que se decida)
PARAMETROS = _congela(_VALORES)


def como_dict(x=PARAMETROS):
    """Copia serializable (para la huella y para configuracion())."""
    if isinstance(x, MappingProxyType):
        return {k: como_dict(v) for k, v in x.items()}
    return list(x) if isinstance(x, tuple) else x
