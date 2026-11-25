"""QA r01 de T-181 (Claude). Ataques al tratamiento de HT-02 y a la propagación de las bajas.

Ejecutar desde la raíz del repositorio con la venv: `.venv/bin/python .docs/tickets/T-181/revisores/r01_ataques.py`.
Cada comprobación imprime OK o HALLAZGO; el programa termina con código 1 si hay algún HALLAZGO.
Trabaja en directorios temporales: no escribe en el repositorio.
"""
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
EJ = RAIZ / "bloque_a" / "11_Ejecutor"
sys.path[:0] = [str(EJ), str(EJ / "tests")]

import pandas as pd  # noqa: E402
from conftest import nuevo_bloque  # noqa: E402

from bloque_a import mantenimiento_fuentes as mf  # noqa: E402
from bloque_a.herramientas.ht01_datos import cargar_universo  # noqa: E402
from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO  # noqa: E402

RID = "ANA-DOC-0001"
FICHA = f"#### {RID} · Q 90 (A) — Título\n- **Calidad Q:** 90 (A)\n- **URL:** https://example.org/doc\n"
DIA = "2026-06-05"
fallos = []


def informe(**extra):
    fila = {"id": RID, "estado": "ROTO", "accion": "BORRAR", "confirmado": True, "codigo_http": 404,
            "fecha_verificacion": DIA, **extra}
    return {"fecha": DIA, "resumen": {"incidencia_red": False}, "resultados": [fila]}


def comprobar(nombre, condicion, detalle=""):
    print(("OK       " if condicion else "HALLAZGO ") + nombre + ("" if condicion else f" · {detalle}"))
    if not condicion:
        fallos.append(nombre)


def lanza(f):
    try:
        f()
    except ValueError:
        return True
    return False


# ------------------------------------------------------------------ 1. revisión del custodio: entradas hostiles
cambio = informe(estado="CONTENIDO_CAMBIADO", accion="DEGRADAR", hash="h1", huella="x", codigo_http=200)
base = {"accion": "DEGRADAR", "hash": "h1", "puntos": [20, 10, 15, 5, 8, 7, 10], "motivo": "Método modificado"}
for nombre, rev in [
    ("motivo con salto de línea", {**base, "motivo": "uno\ndos"}),
    ("motivo con «<»", {**base, "motivo": "<script>"}),
    ("motivo con credencial ficticia", {**base, "motivo": "clave AKIA" + "ABCDEFGHIJKLMNOP"}),
    ("puntos con booleano", {**base, "puntos": [True, 10, 15, 5, 8, 7, 10]}),
    ("puntos negativos", {**base, "puntos": [-1, 10, 15, 5, 8, 7, 10]}),
    ("puntos por encima del criterio", {**base, "puntos": [26, 10, 15, 5, 8, 7, 10]}),
    ("seis criterios", {**base, "puntos": [20, 10, 15, 5, 8, 7]}),
    ("Q igual a la anterior", {**base, "puntos": [25, 20, 15, 10, 10, 5, 5]}),
    ("acción desconocida", {**base, "accion": "BORRAR"}),
]:
    comprobar(f"rechaza {nombre}", lanza(lambda rev=rev: mf.tratar("F8", FICHA, cambio, {RID: rev})))

# Niveles en los bordes del Documento 0 §13.3 (A ≥ 80, B 65–79, C 50–64, D < 50)
ficha_alta = FICHA.replace("Q 90 (A)", "Q 100 (A)").replace("90 (A)", "100 (A)")
for puntos, esperado in [([25, 20, 15, 10, 10, 0, 0], "80 (A)"), ([25, 20, 15, 10, 9, 0, 0], "79 (B)"),
                         ([25, 20, 15, 5, 0, 0, 0], "65 (B)"), ([25, 20, 15, 4, 0, 0, 0], "64 (C)"),
                         ([25, 20, 5, 0, 0, 0, 0], "50 (C)"), ([25, 20, 4, 0, 0, 0, 0], "49 (D)")]:
    texto = mf.tratar("F8", ficha_alta, cambio, {RID: {**base, "puntos": puntos}})
    comprobar(f"nivel {esperado}", f"Q {esperado}" in texto)

# Un «|» en el motivo de una retractación no rompe la fila del registro (la baja sigue siendo legible)
retr = informe(retractacion=["retracted"], hash="e1", codigo_http=200)
texto = mf.tratar("F8", FICHA, retr, {RID: {"accion": "RETRACTADA", "hash": "e1", "motivo": "Nota | del editor"}})
comprobar("motivo con «|» en la baja", list(mf.bajas_registradas(texto.splitlines())) == [(RID, DIA)])

# La retractación exige el indicio de HT-02: el custodio no retracta una ficha sin aviso del editor
ok = informe(estado="OK", accion="NINGUNA", hash="e1", codigo_http=200)
comprobar("RETRACTADA sin indicio de HT-02 se rechaza",
          lanza(lambda: mf.tratar("F8", FICHA, ok, {RID: {"accion": "RETRACTADA", "hash": "e1", "motivo": "x"}})))

# Una ficha con copia archivada registrada no se borra por enlace roto
orig = mf._sin_copia
mf._sin_copia = lambda r: True
con_copia = FICHA + "- **Copia archivada:** https://web.archive.org/web/2026/https://example.org/doc\n"
comprobar("ficha con copia archivada se conserva", "####" in mf.tratar("F7", con_copia, informe(), {}))
# Pérdida de red: el informe con incidencia de red no cambia nada
red = informe()
red["resumen"]["incidencia_red"] = True
comprobar("incidencia de red no toca el catálogo", mf.tratar("F7", FICHA, red, {}) == FICHA)
mf._sin_copia = orig

# Una revisión para una ficha que el barrido no pudo comprobar (sin código HTTP) no se descarta en silencio
sin_respuesta = informe(codigo_http=None, estado="CONTENIDO_CAMBIADO", hash="h1")
try:
    salida = mf.tratar("F8", FICHA, sin_respuesta, {RID: base})
    comprobar("revisión de una ficha sin respuesta HTTP no se pierde en silencio", False,
              "tratar() devuelve el catálogo sin aplicar la decisión ni avisar")
except ValueError:
    comprobar("revisión de una ficha sin respuesta HTTP no se pierde en silencio", True)

# Un registro de bajas con una fecha imposible no debe tumbar la lectura del catálogo entero
roto = FICHA + "\n## Registro de bajas\n\n| REF-id | Título | Motivo | Fecha | Sustituta |\n|---|---|---|---|---|\n" \
               "| ANA-DOC-0009 | T | M | 2026-13-45 | — |\n"
try:
    list(mf.bajas_registradas(roto.splitlines()))
    comprobar("fecha imposible en el registro", True)
except ValueError as e:
    comprobar("fecha imposible en el registro no bloquea el ejecutor", False, f"ValueError sin contexto: {e}")

# Un encabezado que borrar_ficha reconoce («Registro de bajas» con texto añadido) debe leerse también
from bloque_a.herramientas import ht02  # noqa: E402
variante = FICHA + "\n## Registro de bajas (R24)\n\n| REF-id | Título | Motivo | Fecha | Sustituta |\n|---|---|---|---|---|\n"
lineas, _ = ht02.borrar_ficha(variante.splitlines(keepends=True), RID, "m", pd.Timestamp(DIA).date())
comprobar("la baja escrita por HT-02 bajo un encabezado con sufijo se lee",
          list(mf.bajas_registradas("".join(lineas).splitlines())) == [(RID, DIA)],
          "bajas_registradas exige el encabezado exacto; HT-02 escribe en cualquiera que contenga «registro de bajas»")


# ------------------------------------------------------------------ 2. propagación: revisar_bajas
def bloque_con_baja(tmp):
    universo = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    b = nuevo_bloque(tmp, universo)
    ruta = Path(tmp) / "F7.md"
    mf._sin_copia = lambda r: True
    ruta.write_text(mf.tratar("F7", FICHA, informe(), {}))
    mf._sin_copia = orig
    b.referencias.rutas = {"F7": ruta}
    b.referencias._firmas.clear()
    b.fijar_fecha("2026-06-01")
    return b


def evd(alm, eid, ref, nivel="A", tipo="PRIMARIA"):
    alm.escribir("F2", "AG-12", {"tipo_entrada": "EVD", "evd_id": eid, "ref_id": ref, "direccion": "FAVORABLE",
                                 "grado_independencia": "RAIZ", "nivel_fuente": nivel, "tipo_fuente": tipo})


with tempfile.TemporaryDirectory() as tmp:
    b = bloque_con_baja(tmp)
    alm = b.almacen
    evd(alm, "EVD-1", "REF-" + RID)                      # la que se retira: raíz A primaria
    evd(alm, "EVD-2", "REF-ANA-DOC-0002", "B", "SECUNDARIA")
    evd(alm, "EVD-3", "REF-ANA-DOC-0003", "B", "SECUNDARIA")
    # OPP-A: su única raíz suficiente es la retirada → debe quedar en reevaluación
    alm.escribir("F3", "AG-02", {"opp_id": "OPP-A", "estado": "VIGENTE", "evidencias": ["EVD-1", "EVD-2"],
                                 "evidencias_ps1": ["EVD-1", "EVD-2"], "ps1": True})
    # OPP-B: VIGENTE pero ya sin PS1; la baja no puede devolverle PS1
    alm.escribir("F3", "AG-02", {"opp_id": "OPP-B", "estado": "VIGENTE", "evidencias": ["EVD-1", "EVD-2", "EVD-3"],
                                 "evidencias_ps1": ["EVD-2", "EVD-3"], "ps1": False})
    # OPP-C: no vigente; no se revisa
    alm.escribir("F3", "AG-02", {"opp_id": "OPP-C", "estado": "DESCARTADA", "evidencias": ["EVD-1"],
                                 "evidencias_ps1": ["EVD-1"], "ps1": True})
    for _ in range(3):
        b.fijar_fecha(DIA)
        mf.revisar_bajas(b, DIA, "RUN-QA")
    f3 = alm.estado("F3")
    comprobar("la raíz retirada deja de contar (OPP-A)", f3["OPP-A"]["ps1"] is False
              and f3["OPP-A"]["revision_bajas"]["conclusion"] == "REQUIERE_REEVALUACION")
    comprobar("una baja nunca devuelve PS1 a una opción sin él (OPP-B)", f3["OPP-B"]["ps1"] is False,
              f"ps1 pasa a {f3['OPP-B']['ps1']} con conclusión {f3['OPP-B'].get('revision_bajas', {}).get('conclusion')}")
    comprobar("no se revisa una opción no vigente", "revision_bajas" not in f3["OPP-C"])
    revisiones = [e for e in alm.leer("F3") if e.get("revision_bajas")]
    comprobar("idempotente: una revisión por opción en tres pasadas", len(revisiones) == 2, f"{len(revisiones)} revisiones")
    marcas = [e for e in alm.leer("F2") if e.get("evd_id") == "EVD-1" and e.get("estado_verificacion") == "FUENTE_RETIRADA"]
    comprobar("idempotente: la EVD se marca una sola vez", len(marcas) == 1, f"{len(marcas)} marcas")
    comprobar("CT-21 no sale antes del cierre del mes", not [e for e in alm.leer("HA") if e.get("mes_bajas")])
    b.fijar_fecha("2026-07-03")
    mf.revisar_bajas(b, "2026-07-03", "RUN-QA2")
    ct21 = [e for e in alm.leer("HA") if e.get("mes_bajas")]
    comprobar("CT-21 del mes cerrado, una vez", len(ct21) == 1 and ct21[0]["bajas"] == ["REF-" + RID])


# ------------------------------------------------------------------ 3. evidencias_ps1 de una opción arrastrada
with tempfile.TemporaryDirectory() as tmp:
    universo = cargar_universo(RUTA_UNIVERSO_EJEMPLO)
    b = nuevo_bloque(tmp, universo)
    b.ciclo(DIA)   # las propuestas del primer ciclo pasan a VIGENTE (arrastradas) en el segundo
    antes = {k: v.get("evidencias_ps1") for k, v in b.almacen.estado("F3").items() if v.get("estado") == "PROPUESTA"}
    b.ciclo(str((pd.Timestamp(DIA) + pd.Timedelta(days=7)).date()))
    despues = {k: v.get("evidencias_ps1") for k, v in b.almacen.estado("F3").items() if v.get("estado") == "VIGENTE"}
    perdidas = [k for k in antes if antes[k] and k in despues and not despues[k]]
    comprobar("una opción vigente arrastrada conserva sus evidencias_ps1", antes and not perdidas,
              f"propuestas del ciclo 1: {len(antes)}; vigentes con la lista vaciada en el ciclo 2: {len(perdidas)}")
    # Consecuencia: la baja de una sola fuente quita PS1 a la opción aunque sobrevivan dos raíces A/B suyas
    evds = b.almacen.estado("F2", clave="evd_id")
    elegida = None
    for oid in perdidas:
        lista = [evds[e] for e in antes[oid] if e in evds]
        refs = [e for e in lista if str(e.get("ref_id", "")).startswith("REF-")]
        resto = [e for e in lista if e not in refs[:1] and e.get("nivel_fuente") in ("A", "B")]
        if refs and len({e.get("origen_documental") for e in resto}) >= 2:
            elegida = (oid, refs[0]["ref_id"])
            break
    if elegida:
        oid, ref = elegida
        dia2 = str((pd.Timestamp(DIA) + pd.Timedelta(days=8)).date())
        b.referencias.actualizar = lambda: None
        b.referencias.bajas = {"F7": [(ref.removeprefix("REF-"), dia2)]}
        b.fijar_fecha(dia2)
        mf.revisar_bajas(b, dia2, "RUN-QA3")
        rev = b.almacen.estado("F3")[oid].get("revision_bajas", {})
        comprobar("con dos raíces A/B supervivientes la revisión mantiene el respaldo",
                  rev.get("conclusion") == "MANTIENE_RESPALDO",
                  f"{oid}: baja de {ref} y conclusión {rev.get('conclusion')}, ps1 {b.almacen.estado('F3')[oid].get('ps1')}")
    else:
        print("         (sin opción con dos raíces supervivientes en el ciclo mock: comprobación 3b no aplicable)")

print(f"\n{len(fallos)} hallazgos")
sys.exit(1 if fallos else 0)
