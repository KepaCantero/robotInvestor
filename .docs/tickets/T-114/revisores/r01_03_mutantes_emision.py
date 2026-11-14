"""QA r01 de T-114 · Mutantes de lo que el ejecutor EMITE (no de `contratos.py`): ¿los ven los goldens? ¿y la suite?

Cambios de formato en los cuerpos que construye el ejecutor: una clave nueva de primer nivel, una clave anidada, un cambio de
tipo de un valor, y cuerpos de contratos que el ciclo semanal simulado no emite (CT-03, CT-16, CT-22, CT-24, CT-25).
Uso:  python r01_03_mutantes_emision.py <copia_desechable> [--solo E02,E03] [--suite "rutas de pytest"]
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PY = "/home/user/robotinvestor/.venv/bin/python"
O, S, I = "bloque_a/orquestacion.py", "bloque_a/seguimiento.py", "bloque_a/interfaz_broker.py"
MUTANTES = [
    ("E01", O, "CT-06 del ciclo: clave nueva de primer nivel", '"rotacion_exploratoria": rot, "calculos_disponibles": calcs,', '"rotacion_exploratoria": rot, "extra_qa": 1, "calculos_disponibles": calcs,'),
    ("E02", O, "CT-06 del ciclo: `lecciones` pasa de lista de identificadores a lista de objetos",
     '"opciones_vigentes": vig_msg, "lecciones": [l["id"] for l in self.evaluador.lecciones_vigentes(as_of, clase)],',
     '"opciones_vigentes": vig_msg, "lecciones": [l for l in self.evaluador.lecciones_vigentes(as_of, clase)],'),
    ("E03", O, "CT-12 del ciclo: clave nueva DENTRO de cada encargo", '"tipo_pronostico": tipo_p, "horizontes": hs,', '"tipo_pronostico": tipo_p, "extra_qa": 1, "horizontes": hs,'),
    ("E04", O, "CT-02 del ciclo: clave nueva DENTRO de `resumen`", '"apuestas_independientes": paquete["apuestas_independientes"]},', '"apuestas_independientes": paquete["apuestas_independientes"], "extra_qa": 1},'),
    ("E05", O, "CT-02 del ciclo: `top3_por_clase` pasa de listas a un recuento",
     '"top3_por_clase": {c: [o["opp_id"] for o in paquete["clases"][c]["opciones"]] for c in paquete["clases"]},',
     '"top3_por_clase": {c: len(paquete["clases"][c]["opciones"]) for c in paquete["clases"]},'),
    ("E06", O, "CT-03 (consulta): `urgencia` renombrada a `prisa`", '{"pregunta": texto, "contexto": contexto or {}, "urgencia": urgencia}', '{"pregunta": texto, "contexto": contexto or {}, "prisa": urgencia}'),
    ("E07", O, "CT-16: `paquete_auditoria` renombrado", '"CT-16", "AG-01", "AG-18", {"paquete_auditoria":', '"CT-16", "AG-01", "AG-18", {"paquete":'),
    ("E08", O, "CT-22 (decisiones): `ret_id` renombrado", '{"tipo": "DECISIONES_BROKER", "ret_id": ret_id,', '{"tipo": "DECISIONES_BROKER", "ret": ret_id,'),
    ("E09", S, "CT-24 retorno FINALIZADO: sin `proximo_ciclo`", '{"seg_id": k, "estado": "FINALIZADO", "proximo_ciclo": None,', '{"seg_id": k, "estado": "FINALIZADO",'),
    ("E10", I, "CT-25 solicitud: sin `herramienta`", 'cuerpo = {"crd_id": crd_id, "servicio": servicio, "herramienta": "HT-01", "uso_previsto"', 'cuerpo = {"crd_id": crd_id, "servicio": servicio, "uso_previsto"'),
    ("E11", I, "CT-23 respuesta: `respuestas` renombrada", '{"cns_id": cns_id, "estado": estado, "respuestas": respuestas}', '{"cns_id": cns_id, "estado": estado, "contestaciones": respuestas}'),
]


def ejecutar(orden, cwd):
    r = subprocess.run(orden, cwd=cwd, capture_output=True, text=True, timeout=1800)
    sal = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode, sal[-1][:140] if sal else ""


def main() -> int:
    copia = Path(sys.argv[1]).resolve()
    assert "qa_f3_mut" in str(copia), "solo en la copia desechable"
    suite = sys.argv[sys.argv.index("--suite") + 1].split() if "--suite" in sys.argv else None
    ej = copia / "bloque_a" / "11_Ejecutor"
    vivos = []
    solo = set(sys.argv[sys.argv.index("--solo") + 1].split(",")) if "--solo" in sys.argv else None
    for mid, fich, desc, viejo, nuevo in MUTANTES:
        if solo and mid not in solo:
            continue
        ruta = ej / fich
        original = ruta.read_text(encoding="utf-8")
        if original.count(viejo) != 1:
            print(f"{mid} · NO APLICADO ({original.count(viejo)} apariciones) · {desc}"); continue
        try:
            ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
            rc, _ = ejecutar([PY, "tests/goldens_ct.py"], ej)
            linea = f"{mid} · goldens_ct rc={rc} ({'DETECTADO' if rc else 'NO DETECTADO'}) · {desc}"
            if rc == 0 and suite:
                rs, us = ejecutar([PY, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *suite], ej)
                linea += f" · suite rc={rs} ({'DETECTADO' if rs else 'VIVO'}): {us}"
                if rs == 0:
                    vivos.append(mid)
            elif rc == 0:
                vivos.append(mid)
            print(linea, flush=True)
        finally:
            ruta.write_text(original, encoding="utf-8")
    print("no detectados por lo ejecutado: " + (", ".join(vivos) or "ninguno"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
