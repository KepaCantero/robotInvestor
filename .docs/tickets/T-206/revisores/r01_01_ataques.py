"""QA r01 de T-206 (revisor independiente): ataques al tipo de las incidencias de HA.

Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-206/revisores/r01_01_ataques.py
Cada línea dice OK (se comporta como se espera) o HALLAZGO (no). Termina con 1 si hay algún HALLAZGO.
"""
import json
import multiprocessing as mp
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, ".")
from bloque_a.almacen import (
    ARCHIVOS,
    TIPOS_INCIDENCIA,
    Almacen,
    Reloj,
    TipoIncidenciaNoAdmitido,
    es_incidencia_de_datos,
)

AS_OF = "2026-06-05"
hallazgos = []


def informe(nombre, ok, detalle=""):
    print(f"{'OK      ' if ok else 'HALLAZGO'} {nombre}{(': ' + detalle) if detalle else ''}", flush=True)
    if not ok:
        hallazgos.append(nombre)


def alm(carpeta):
    a = Almacen(carpeta, Reloj())
    a.reloj.fijar(AS_OF)
    return a


def disco(carpeta):
    return {p.name: p.read_bytes() for p in sorted(Path(carpeta).iterdir()) if p.is_file()}


def incs(a):
    return [e for e in a.leer("HA") if e.get("tipo_entrada") == "INC"]


# ---------------------------------------------------------------- 1. valores hostiles como tipo
class Permisivo:
    """Objeto cuyo == da siempre True: pasa `in TIPOS_INCIDENCIA`."""
    def __eq__(self, otro):
        return True

    __hash__ = object.__hash__


class TextoPermisivo(str):
    """Subclase de str con == permisivo: pasa isinstance y `in`; json la escribe con su valor."""
    def __eq__(self, otro):
        return True

    __hash__ = str.__hash__


# ---------------------------------------------------------------- 5. concurrencia: el rechazo no gasta contador ni entre procesos


def _trabajo(carpeta, k, n):
    a = Almacen(carpeta, Reloj())
    a.reloj.fijar(AS_OF)
    for i in range(n):
        a.incidencia_de_datos(f"p{k} {i}", "AG-16")
        try:
            a.incidencia("DATOS", "no")
        except TipoIncidenciaNoAdmitido:
            pass
        try:
            a._incidencia_interna(None, "no", "AG-18")
        except TipoIncidenciaNoAdmitido:
            pass


def secciones_1_a_4():
    for nombre, tipo in [("nan", float("nan")), ("inf", float("inf")), ("bytes", b"OTRO"), ("dict", {"OTRO": 1}),
                         ("bool", True), ("NFD/ancho completo", "ＯＴＲＯ"), ("cero ancho", "OTRO\u200b"),
                         ("objeto con == permisivo", Permisivo()), ("str con == permisivo y valor DATOS", TextoPermisivo("DATOS"))]:
        with tempfile.TemporaryDirectory() as d:
            a = alm(d)
            a.incidencia("OTRO", "previa")
            antes = disco(d)
            try:
                a.incidencia(tipo, "hostil")
                rechazo = False
            except TipoIncidenciaNoAdmitido:
                rechazo = True
            except Exception as e:   # otro error: ¿dejó algo a medias?
                rechazo = f"otro error {type(e).__name__}"
            escritos = [e.get("tipo") for e in incs(Almacen(d, Reloj()))]
            informe(f"1 tipo {nombre} rechazado sin escribir", rechazo is True and disco(d) == antes,
                    f"rechazo={rechazo}; tipos en HA={escritos}")

    # ---------------------------------------------------------------- 2. lector: solo las de datos (CA-4 «y solo esas»)
    # Ronda de cierre (implementador, T-206 H-03): la corrección que pide el qa.md hace que `incidencia` rechace la categoría
    # con otro tipo (TipoIncidenciaNoAdmitido, sin escribir nada); este bloque acepta ese rechazo como OK y el lector se
    # prueba con la entrada montada a mano. Las comprobaciones no cambian.
    with tempfile.TemporaryDirectory() as d:
        a = alm(d)
        a.incidencia("OTRO", "previa")
        antes = disco(d)
        try:
            e = a.incidencia("SEGURIDAD", "credencial en un mensaje", "AG-18", categoria="DATOS")
        except TipoIncidenciaNoAdmitido:
            e = None
        informe("2 incidencia() acepta categoria DATOS con un tipo que no es OTRO", (e is None and disco(d) == antes)
                or (e is not None and "categoria" not in e),
                "rechazada sin escribir" if e is None else f"escrita tipo={e['tipo']} categoria={e.get('categoria')}")
        e = {"tipo_entrada": "INC", "tipo": "SEGURIDAD", "categoria": "DATOS"}
        informe("2 el lector no toma una SEGURIDAD por incidencia de datos", not es_incidencia_de_datos(e),
                f"es_incidencia_de_datos={es_incidencia_de_datos(e)}")

    # ---------------------------------------------------------------- 3. escritura genérica (límite declarado)
    with tempfile.TemporaryDirectory() as d:
        a = alm(d)
        try:
            a.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": a.nuevo_id("INC"), "tipo": "DATOS", "severidad": "Menor",
                                       "objeto": "x", "tratamiento": "registrada"})
            escrito = True
        except Exception:
            escrito = False
        informe("3 escribir() rechaza una INC- montada a mano con tipo DATOS", not escrito,
                "se escribe" if escrito else "")

    # ---------------------------------------------------------------- 4. HA antiguo: abrir, sellar, añadir, reabrir
    # Ronda de cierre (implementador, T-206 H-04): `escribir` ya rechaza una INC- con DATOS; el HA antiguo se monta como lo
    # dejaba el ejecutor de antes de T-206, con la comprobación desactivada solo mientras se monta.
    with tempfile.TemporaryDirectory() as d:
        a = alm(d)
        _comprobar = Almacen.__dict__["_comprobar_tipo_incidencia"]
        Almacen._comprobar_tipo_incidencia = staticmethod(lambda tipo, extra=None: None)
        try:
            for i in range(3):
                a.escribir("HA", "AG-18", {"tipo_entrada": "INC", "id": a.nuevo_id("INC"), "tipo": "DATOS", "severidad": "Operativa",
                                           "objeto": "AG-16", "detalle": f"antigua {i}", "tratamiento": "registrada",
                                           **({"fue_no_atendible": "FUE-2026-0001"} if i == 0 else {})})
        finally:
            Almacen._comprobar_tipo_incidencia = _comprobar
        b = alm(d)
        ok_abre = all(b.verificar_integridad().values())
        b.incidencia_de_datos("nueva", "AG-16")
        c = Almacen(d, Reloj())
        ok_reabre = all(c.verificar_integridad().values())
        tipos = [e["tipo"] for e in incs(c)]
        informe("4 HA antiguo con DATOS se abre, se amplía y se reabre íntegro", ok_abre and ok_reabre
                and tipos == ["DATOS", "DATOS", "DATOS", "OTRO"] and sum(map(es_incidencia_de_datos, incs(c))) == 4, f"{tipos}")
        # manipulación: cambiar el tipo de una antigua a OTRO en el fichero debe romper la integridad
        ruta = Path(d) / ARCHIVOS["HA"]
        lineas = ruta.read_text(encoding="utf-8").splitlines()
        e0 = json.loads(lineas[0])
        e0["tipo"] = "OTRO"
        lineas[0] = json.dumps(e0, ensure_ascii=False)
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        try:
            detecta = not all(Almacen(d, Reloj()).verificar_integridad().values())
        except ValueError:
            detecta = True
        informe("4 un HA antiguo con el tipo reescrito a mano se detecta", detecta)



if __name__ == "__main__":
    secciones_1_a_4()
    with tempfile.TemporaryDirectory() as d:
        Almacen(d, Reloj())
        ctx = mp.get_context("spawn")
        ps = [ctx.Process(target=_trabajo, args=(d, k, 10)) for k in range(4)]
        for p in ps:
            p.start()
        for p in ps:
            p.join()
        a = alm(d)
        ids = sorted(e["id"] for e in incs(a))
        esperados = [f"INC-2026-{i:04d}" for i in range(1, 41)]
        informe("5 cuatro procesos: 40 INC- de datos, ids contiguos, ningún contador gastado por los rechazos",
                ids == esperados and all(e["tipo"] == "OTRO" and e["categoria"] == "DATOS" for e in incs(a))
                and all(a.verificar_integridad().values()) and all(p.exitcode == 0 for p in ps), f"{len(ids)} INC-, último {ids[-1:]}")

    # ---------------------------------------------------------------- 6. el enumerado no se puede mutar en ejecución
    informe("6 TIPOS_INCIDENCIA es inmutable (tupla)", isinstance(TIPOS_INCIDENCIA, tuple))

    print(f"\nhallazgos: {len(hallazgos)}: {hallazgos}")
    sys.exit(1 if hallazgos else 0)
