"""QA r02 de T-143 · Mutantes de la prosa del Anexo B V5.2 aplicados en memoria a las comprobaciones de las pruebas r02.

Las comprobaciones `_esquemas_de_respuesta_que_difieren`, `_listas_de_la_prosa_que_difieren` y `_opcionales_sin_marca` de
`tests/test_fase3_goldens.py` leen los párrafos del Anexo B y los esquemas derivados escritos a mano (que `--update` no
regenera), así que cambiar un párrafo en memoria equivale a cambiar el Documento 0 y re-congelar. Aquí se buscan los huecos de
esas comprobaciones con cambios de prosa que contradicen el código. Desde la raíz, con el Python del .venv:

    .venv/bin/python .docs/tickets/T-143/revisores/r02_03_prosa_en_memoria.py

Una línea por mutante: «DETECTADO» si alguna de las tres comprobaciones lo ve; «NO DETECTADO» si ninguna. Termina con 0
siempre: lo que no se detecta es un dato para la QA, no un fallo del script (las expectativas están en `esperado`).
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJECUTOR = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path.insert(0, str(EJECUTOR))
sys.path.insert(0, str(EJECUTOR / "tests"))

import goldens_ct as g  # noqa: E402
import test_fase3_goldens as t  # noqa: E402

from bloque_a import contratos  # noqa: E402

# (id, contrato, texto viejo, texto nuevo, esperado, qué representa)
MUTANTES = [
    ("P01", "CT-24", "En el encargo son opcionales `seg_id`, `opp_id`, `frecuencia`, `calendario_personalizado`, `motivo`, "
     "`senales_interes` y `fecha_fin`: solo `accion` es obligatorio, y cada acción lleva lo que necesita.",
     "En el encargo son obligatorios `seg_id`, `opp_id`, `frecuencia`, `calendario_personalizado`, `motivo`, `senales_interes` "
     "y `fecha_fin`, y no solo `accion`.", "detectado", "CT-24: la prosa exige los siete campos (la marca «solo » sigue en la frase)"),
    ("P02", "CT-25", "`credencial_ref` y `caducidad` son opcionales (una respuesta DENEGADA no lleva caducidad).",
     "`credencial_ref` y `caducidad` los lleva toda respuesta, salvo error.", "detectado",
     "CT-25: la prosa exige `credencial_ref` y `caducidad` (la marca «salvo» sigue en la frase)"),
    ("P03", "CT-06", "`nombre`, `nombre_llano`, `tipo_opcion`, `subtipo`,", "`nombre`, `nombre_llano`, `tipo_opcion` (MERCADO | PAIS), `subtipo`,",
     "detectado", "CT-06: la prosa da a `tipo_opcion` de la ficha valores que no son los de TIPOS_OPCION"),
    ("P04", "CT-05", "`memoria` (OPP- vigentes, TND- activas, LEC- aplicables, certificados de horizonte)", "`memoria` (OPP- vigentes)", "?",
     "CT-05: la prosa cambia lo que lleva `memoria`"),
    ("P05", "CT-15", "Los tres entregables y sus rutas los escribe el ejecutor, que mide su legibilidad al validarlos (G3).",
     "El Redactor devuelve además las rutas de los tres entregables y sus métricas de legibilidad.", "?",
     "CT-15: la prosa vuelve a decir que el Redactor devuelve rutas y legibilidad (lo que corrigió H-02)"),
    ("P06", "CT-06", "En la fase SEGUIMIENTO no hay informe del Analista: la revisión la calcula el ejecutor (7.11).",
     "En la fase SEGUIMIENTO el Analista responde con `INFORME_CLASE`.", "?", "CT-06: la prosa da informe del Analista en SEGUIMIENTO"),
    ("P07", "CT-05", "y `insumos_integracion` solo con INTEGRACION", "y `insumos_integracion` en todas las órdenes", "detectado",
     "CT-05: la prosa exige `insumos_integracion` siempre"),
    ("P08", "CT-03", "En la consulta, el Broker no envía `query_id`: lo asigna el bloque al recibirla (QRY-). ",
     "En la consulta, el Broker envía `query_id` (QRY-). ", "?", "CT-03: la prosa vuelve a decir que el Broker envía `query_id`"),
]


def detecta(parrafos: dict[str, str], a_mano) -> list[str]:
    esquemas = a_mano[0]
    vistos = []
    if t._esquemas_de_respuesta_que_difieren(contratos.ESQUEMAS, parrafos, esquemas):
        vistos.append("esquemas de respuesta")
    if t._listas_de_la_prosa_que_difieren(esquemas, parrafos):
        vistos.append("listas de la prosa")
    if t._opcionales_sin_marca(esquemas, parrafos):
        vistos.append("opcionales sin marca")
    return vistos


def main() -> int:
    a_mano = g.leer_a_mano()
    base = g.parrafos_anexo_b()
    print("sin mutar:", detecta(base, a_mano) or "ninguna comprobación ve diferencias")
    for ident, ct, viejo, nuevo, esperado, que in MUTANTES:
        p = copy.deepcopy(base)
        claves = [k for k, v in p.items() if viejo in v]
        if not claves or p[ct].count(viejo) != 1:
            print(f"{ident} · NO APLICA · {que}")
            continue
        for k in claves:   # un párrafo de varios contratos se repite en cada uno
            p[k] = p[k].replace(viejo, nuevo)
        vistos = detecta(p, a_mano)
        estado = "DETECTADO" if vistos else "NO DETECTADO"
        marca = "" if (estado == "DETECTADO") == (esperado == "detectado") or esperado == "?" else "   <-- contra lo esperado"
        print(f"{ident} · {estado} ({', '.join(vistos) or '-'}; esperado {esperado}) · {que}{marca}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
