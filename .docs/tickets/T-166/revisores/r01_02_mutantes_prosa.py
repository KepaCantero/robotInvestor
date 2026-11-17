"""QA r01 de T-166 · mutantes de prosa propios contra `_final_que_difiere` de test_t166_entrega_corpus.py.

Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python -I ../../.docs/tickets/T-166/revisores/r01_02_mutantes_prosa.py
Cada mutante cambia el sentido de una frase del párrafo «Respuesta final (V5.3)»; «VIVE» = la prueba no lo nota.
"""
import sys
from pathlib import Path

EJ = Path(__file__).resolve().parents[4] / "bloque_a" / "11_Ejecutor"
sys.path[:0] = [str(EJ), str(EJ / "tests")]
import goldens_ct as g  # noqa: E402
import test_t166_entrega_corpus as t  # noqa: E402

MUTANTES = [
    ("con opciones, la más baja de las suyas en F3", "con opciones, la más alta de las suyas en F3"),
    ("que queda registrado en F5)", "que queda registrado en F3)"),
    ("`escalado` (el mismo que la provisional)", "`escalado` (distinto del de la provisional)"),
    ("de una consulta de ruta ANALITICA", "de una consulta de ruta N0"),
    ("(o falla, no entrega o no se lanzó)", "(solo si entrega)"),
    ("las de su top-3", "las de su top-3"),  # control: no cambia nada (debe dar «sin cambio»)
    ("Coordinador envía otro CT-03", "Evaluador envía otro CT-03"),
    ("con estado RESPONDIDA_FINAL", "con estado RESPONDIDA_ANALITICA"),
    ("ENTREGADO, COMPLETO;", "ENTREGADO, PARCIAL;"),
    ("sin llamar al modelo", "con el modelo"),
    ("`provisional_msg_id` (el `msg_id` de la provisional, MSG-,", "`provisional_msg_id` (el `query_id` de la consulta, MSG-,"),
]


def main() -> int:
    p = g.parrafos_anexo_b()["CT-03"]
    c = t._codigo()
    assert t._final_que_difiere(p, c) == []
    vivos = 0
    for viejo, nuevo in MUTANTES:
        if viejo == nuevo or viejo not in p:
            print(f"sin cambio · {viejo!r}")
            continue
        muerto = t._final_que_difiere(p.replace(viejo, nuevo, 1), c) != []
        vivos += not muerto
        print(f"{'muerto' if muerto else 'VIVE  '} · {viejo!r} → {nuevo!r}")
    print(f"vivos: {vivos}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
