"""QA r01 de T-116 · Tres filas AUTOMATICA del mapa, ejecutadas como dice el plan y no como las pruebas citadas.

PB-21 (CT-04 con una clave API y un IBAN en el comentario; búsqueda del valor en TODOS los archivos),
PB-45 (¿se ve con el cliente simulado la aplicación de la lección?) y PB-06 (≥ 1 referencia por afirmación).
Uso, desde bloque_a/11_Ejecutor:  python <este fichero>.  Solo usa carpetas temporales. No es un gate (termina con 0).
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "tests")]
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
from bloque_a.herramientas.ht01_datos import cargar_universo
from conftest import AS_OF, nuevo_bloque

U = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
TMP = Path(tempfile.mkdtemp())


def buscar(carpeta: Path, textos: list[str]) -> dict:
    hallados = {}
    for p in carpeta.rglob("*"):
        if p.is_file():
            cuerpo = p.read_text(encoding="utf-8", errors="ignore")
            for t in textos:
                if t in cuerpo:
                    hallados.setdefault(t, []).append(p.name)
    return hallados


print("== PB-21 · CT-04 del Broker con una clave API y un IBAN en el comentario")
CLAVE, IBAN_ESP, IBAN_JUNTO = "sk-ant-abcdefghijklmnopqrstuvwxyz123456", "ES91 2100 0418 4502 0005 1332", "ES9121000418450200051332"
for nombre, comentario in (("clave + IBAN con espacios (caso del plan)", f"mi clave es {CLAVE} y mi IBAN {IBAN_ESP}"),
                           ("solo IBAN con espacios", f"cobren en {IBAN_ESP}"), ("solo IBAN sin espacios", f"cobren en {IBAN_JUNTO}")):
    d = TMP / nombre.replace(" ", "_")
    b = nuevo_bloque(d, U)
    b.fijar_fecha(AS_OF)
    try:
        r = b.decision({"valoracion_informe": {"run_id": "RUN-2026-0001", "utilidad": 1, "comentario": comentario}}, AS_OF)
        fin = f"ADMITIDO (estado {r.get('estado')})"
    except Exception as e:  # noqa: BLE001
        fin = f"rechazado con {type(e).__name__}"
    incs = [e for e in b.almacen.leer("HA") if e.get("tipo") == "SEGURIDAD"]
    hall = buscar(d, [CLAVE, IBAN_ESP, IBAN_JUNTO, "2100 0418"])
    print(f"  {nombre}: {fin}; incidencias SEGURIDAD={len(incs)} campo={[e.get('campo_afectado') for e in incs]}; "
          f"valor en archivos: {hall or 'cero coincidencias'}{'  !! el dato personal queda en los archivos' if hall else ''}")

print("== PB-45 · ¿cambia algo observable en el ciclo simulado cuando hay una lección de calibración vigente?")
probs = {}
for con in (False, True):
    b = nuevo_bloque(TMP / f"pb45_{con}", U)
    b.fijar_fecha(AS_OF)
    if con:
        b.almacen.escribir("F6", "AG-20", {"tipo_entrada": "LEC", "id": "LEC-2026-0001", "fecha": AS_OF, "ambito": {"clase": "DIV", "horizonte": "H2"},
                                           "nivel": "B", "tipo": "CALIBRACION", "observacion": "o", "evidencia": [], "recomendacion": "r",
                                           "fuerza": "estadistica", "n": 30, "caducidad": "2027-06-05", "estado": "VIGENTE", "origen": "DETERMINISTA"})
    b.ciclo(AS_OF, alcance={"clases": ["DIV"]})
    probs[con] = sorted({e.get("prob_interna") for e in b.almacen.leer("F4") if e.get("tipo_entrada") == "ALTA" and e.get("prob_interna") is not None})
print(f"  probabilidades internas de los PRG de DIV sin lección: {probs[False]} · con lección de calibración: {probs[True]}")
print("  " + ("!! la aplicación de la lección SÍ es observable con el cliente simulado (probabilidades más prudentes) y ninguna prueba citada la afirma"
              if probs[False] != probs[True] else "sin diferencia observable: la aplicación es solo del modelo real"))

print("== PB-06 · consulta N0: ¿las pruebas pueden afirmar «≥ 1 referencia por afirmación»?")
b = nuevo_bloque(TMP / "pb06", U)
b.ciclo(AS_OF, alcance={"clases": ["RV", "RF"]})
q = b.consulta("¿Por qué no aparece ninguna opción nueva de renta fija esta semana?", as_of=AS_OF)
print(f"  ruta={q['ruta']} · respuesta={q['respuesta'][:160]!r}")
print(f"  referencias={q['referencias']}")
ids = set()
for a in ("F1", "F2", "F3", "F4", "F5", "F6", "RC"):
    for e in b.almacen.leer(a):
        ids |= {str(v) for k, v in e.items() if k in ("id", "opp_id", "prg_id", "tnd_id", "clm_id", "calc_id", "run_id", "evd_id")}
print(f"  referencias que existen en los archivos: {[x for x in q['referencias'] if x in ids]} de {len(q['referencias'])}")

print("== PB-23 · los tres intentos del plan, uno a uno, con la huella de F4 antes y después")
import hashlib

from bloque_a.almacen import Almacen

alm = Almacen(TMP / "pb23")
alm.reloj.fijar("2026-01-02")
alm.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0001", "estado": "ABIERTO", "prob_interna": 0.6, "afirmacion": "x"})
f4 = TMP / "pb23" / "F4_registro_pronosticos.jsonl"
antes = hashlib.sha256(f4.read_bytes()).hexdigest()
for nombre, autor, entrada in (("Analizador escribe en F4", "AG-02", {"tipo_entrada": "ALTA", "prg_id": "PRG-2026-0002"}),
                               ("Prospectiva escribe un campo de resolución", "AG-10", {"tipo_entrada": "RESOLUCION", "prg_id": "PRG-2026-0001", "estado": "RESUELTO", "resolucion": {"x": 1}}),
                               ("Evaluador modifica la afirmación de un PRG", "AG-20", {"tipo_entrada": "RESOLUCION", "prg_id": "PRG-2026-0001", "afirmacion": "otra"})):
    try:
        alm.escribir("F4", autor, entrada)
        fin = "ADMITIDO  !!"
    except Exception as e:  # noqa: BLE001
        fin = f"rechazado ({type(e).__name__})"
    print(f"  {nombre}: {fin}; huella de F4 {'sin cambios' if hashlib.sha256(f4.read_bytes()).hexdigest() == antes else 'CAMBIADA  !!'}")
print(f"  incidencias: {[e.get('tipo') for e in alm.leer('HA') if e.get('tipo_entrada') == 'INC']}")

print("== PB-49 · ¿detecta `verificar_integridad` una entrada BORRADA (no solo modificada)?")
for caso in ("la del medio", "la última"):
    d = TMP / f"pb49_{caso.split()[-1]}"
    a = Almacen(d)
    a.reloj.fijar("2026-01-02")
    for i in range(3):
        a.escribir("F4", "AG-10", {"tipo_entrada": "ALTA", "prg_id": f"PRG-2026-000{i + 1}", "estado": "ABIERTO", "prob_interna": 0.6})
    ruta = d / "F4_registro_pronosticos.jsonl"
    lineas = ruta.read_text(encoding="utf-8").splitlines(keepends=True)
    ruta.write_text("".join(lineas[:1] + lineas[2:] if caso == "la del medio" else lineas[:-1]), encoding="utf-8")
    try:
        ok = Almacen(d).verificar_integridad("F4")["F4"]
        print(f"  borrar {caso}: verificar_integridad → {'ÍNTEGRO  !! no lo detecta' if ok else 'no íntegro (lo detecta)'}")
    except Exception as e:  # noqa: BLE001
        print(f"  borrar {caso}: {type(e).__name__}: {str(e)[:90]} (lo detecta)")
