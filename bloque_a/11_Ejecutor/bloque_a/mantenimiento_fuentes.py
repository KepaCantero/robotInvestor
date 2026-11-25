"""Tratamiento de incidencias de HT-02 por los custodios de F7, F8 y F9."""
from __future__ import annotations

import os
import re
import tempfile
from datetime import date
from pathlib import Path

from .configuracion import parametro
from .procedencia import cumple_ps1
from . import sintesis as sint
from .contratos import contiene_credenciales
from .herramientas import ht02
from .referencias import nivel_de_q

CUSTODIOS = {"F7": "AG-14", "F8": "AG-15", "F9": "AG-16"}


def detalle_bajas(lineas, archivo="Registro de bajas"):
    nivel = 0
    for numero, linea in enumerate(lineas, 1):
        titulo = ht02.modulo.RE_TITULO.match(linea)
        if titulo:
            profundidad = len(titulo.group(1))
            if "registro de bajas" in ht02.modulo._norm_clave(linea):
                nivel = profundidad
            elif profundidad <= nivel:
                nivel = 0
        elif nivel and linea.startswith("|"):
            partes = re.split(r"(?<!\\)\|", linea.strip().strip("|"))
            if len(partes) == 5:
                rid, _, motivo, fecha, _ = (p.strip() for p in partes)
                if re.fullmatch(r"[A-Z][A-Z0-9-]*-\d+", rid):
                    try:
                        dia = date.fromisoformat(fecha).isoformat()
                    except ValueError as exc:
                        raise ValueError(f"{archivo}, fila {numero}: fecha de baja inválida {fecha!r}") from exc
                    yield rid.removeprefix("REF-"), dia, motivo.replace(r"\|", "|")


def bajas_registradas(lineas, archivo="Registro de bajas"):
    for rid, dia, _ in detalle_bajas(lineas, archivo):
        yield rid, dia


def _degradar(lineas, ficha, revision, archivo, cfg):
    puntos = revision.get("puntos")
    limites = parametro(cfg, f"referencias.rubricas.{archivo}")
    if not isinstance(puntos, list) or len(puntos) != len(limites) or any(
        type(p) is not int or not 0 <= p <= limite for p, limite in zip(puntos, limites)
    ):
        raise ValueError("La puntuación debe respetar los siete criterios de la rúbrica")
    q = sum(puntos)
    if ficha.q is None or q >= ficha.q:
        raise ValueError("DEGRADAR requiere una reducción de Q")
    nivel = nivel_de_q(q, cfg)
    marca = f"{q} ({nivel})"
    i = ficha.linea_inicio
    lineas[i] = re.sub(r"·\s*Q\s*\d+\s*\([A-D]\)", "· Q " + marca, lineas[i], count=1)
    fijar = ht02.modulo._fijar_campo
    fijar(lineas, ficha, "Calidad Q", marca + " — " + revision["motivo"])
    ficha = next(f for f in ht02.leer_fichas(lineas) if f.id == ficha.id)
    fijar(lineas, ficha, "Revisión de calidad", str(puntos) + " — " + revision["motivo"])


def _sin_copia(r):
    """Una caída del servicio de archivo tampoco demuestra que falte una alternativa."""
    import json
    from urllib.parse import urlencode
    destino = r.get("url") or r.get("url_final")
    if not destino or (r.get("doi") and not isinstance(r.get("doi_codigo_http"), int)):
        return False
    cfg = ht02.Config()
    url = cfg.wayback_api + "?" + urlencode({"url": destino})
    respuesta, _ = ht02.modulo._con_reintentos(url, "GET", cfg)
    if respuesta["codigo"] != 200:
        return False
    try:
        datos = json.loads(respuesta["cuerpo"] or b"")
    except ValueError:
        return False
    return isinstance(datos, dict) and datos.get("archived_snapshots") == {}


def tratar(archivo, original, informe, revisiones, cfg=None):
    """Calcula todo antes de publicar. Cada revisión local identifica la huella examinada."""
    lineas = original.splitlines(keepends=True)
    fecha = date.fromisoformat(informe["fecha"])
    if informe["resumen"]["incidencia_red"]:
        if revisiones:
            raise ValueError("La revisión exige una observación HTTP del barrido")
        return original
    estados = []
    fichas = {f.id: f for f in ht02.leer_fichas(lineas)}
    if set(revisiones) - {r["id"] for r in informe["resultados"]}:
        raise ValueError("Revisión sin referencia en el barrido")
    for r in informe["resultados"]:
        if r.get("codigo_http") is None and r.get("doi_codigo_http") is None:
            if r["id"] in revisiones:
                raise ValueError("La revisión exige una observación HTTP del barrido")
            estados.append(r)
            continue
        ficha = fichas.get(r["id"])
        if ficha is None:
            raise ValueError("La referencia del informe falta en el catálogo")
        rev = revisiones.get(ficha.id)
        baja = None
        codigo = r.get("codigo_http")
        if (r["estado"] == "ROTO" and r["accion"] == "BORRAR" and r.get("confirmado") is True
                and isinstance(codigo, int) and 400 <= codigo < 600 and not r.get("copia_archivada")
                and not ficha.campo("Copia archivada") and not r.get("retractacion") and _sin_copia(r)):
            baja = "Enlace roto confirmado y sin alternativa tras dos barridos"
        if rev:
            motivo = rev.get("motivo")
            if not r.get("hash") or rev.get("hash") != r["hash"] or not isinstance(motivo, str) or not motivo.strip() or len(motivo.splitlines()) != 1:
                raise ValueError("La revisión exige la huella observada y un motivo en una línea")
            if contiene_credenciales(motivo) or any(c in motivo for c in ("<", ">")):
                raise ValueError("Motivo no apto para el registro")
            if rev.get("accion") == "RETRACTADA" and r.get("retractacion"):
                baja = "Retractación confirmada por el custodio: " + motivo
            elif rev.get("accion") == "DEGRADAR" and r["estado"] == "CONTENIDO_CAMBIADO":
                ficha = next(f for f in ht02.leer_fichas(lineas) if f.id == ficha.id)
                _degradar(lineas, ficha, rev, archivo, cfg)
                lineas = ht02.rebasar_contenido(lineas, ficha.id, r)
            elif rev.get("accion") == "REPARAR" and r["estado"] == "CONTENIDO_CAMBIADO":
                url = (r.get("copia_archivada") or {}).get("url", "")
                if not re.match(r"^https?://web\.archive\.org/web/", url) or rev.get("url") != url:
                    raise ValueError("La reparación requiere la copia archivada del barrido")
                url = url.replace("http://", "https://", 1) if url.startswith("http://") else url
                copia = ht02.comprobar_url(url, ht02.Config())
                ficha = next(f for f in ht02.leer_fichas(lineas) if f.id == ficha.id)
                if not copia.get("hash") or copia["hash"] != ficha.campo("Hash de contenido") or copia.get("retractacion"):
                    raise ValueError("La copia no reproduce la referencia original")
                ht02.modulo._fijar_campo(lineas, ficha, "URL", url)
                r = {**r, "estado": "OK", "hash": copia["hash"], "huella": copia["huella"]}
            else:
                raise ValueError("La decisión no corresponde a la incidencia observada")
        if baja:
            lineas, _ = ht02.borrar_ficha(lineas, ficha.id, baja, fecha)
        else:
            estados.append(r)
    return "".join(ht02.aplicar_resultados(lineas, estados))


def publicar(ruta, original, nuevo):
    """Sustitución completa y comparación con la versión observada, bajo el cierre del escritor."""
    if nuevo == original:
        return
    with ruta.with_suffix(".ht02.lock").open("a") as lock:
        if os.name == "nt":
            import msvcrt
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(lock, fcntl.LOCK_EX)
        if ruta.read_text(encoding="utf-8") != original:
            raise ValueError("El catálogo cambió durante la verificación; repetir el barrido")
        with tempfile.NamedTemporaryFile(dir=ruta.parent, delete=False) as fh:
            temporal = Path(fh.name)
        try:
            temporal.write_text(nuevo, encoding="utf-8")
            temporal.chmod(ruta.stat().st_mode)
            os.replace(temporal, ruta)
        finally:
            temporal.unlink(missing_ok=True)


def revisar_bajas(bloque, as_of, run_id):
    """El registro de bajas es la fuente durable. Un reintento completa los pasos pendientes."""
    refs = bloque.referencias
    refs.actualizar()
    fecha = str(as_of)[:10]
    bajas = {(archivo, "REF-" + rid, dia) for archivo, filas in refs.bajas.items() for rid, dia in filas if dia <= fecha}
    motivos = dict(refs.motivos_bajas)
    if refs.registro_bajas_f9 and refs.registro_bajas_f9.exists():
        ruta = refs.registro_bajas_f9
        for rid, dia, motivo in detalle_bajas(ruta.read_text(encoding="utf-8").splitlines(), ruta):
            if dia <= fecha:
                clave = ("F9", "REF-" + rid, dia)
                bajas.add(clave)
                motivos[clave] = motivo
    if not bajas:
        return
    almacen = bloque.almacen
    with almacen._transaccion():
        evds = avisar_curador(almacen, bloque.mensajeria, as_of, run_id, bajas, motivos, bloque.cfg)
        clms = almacen.estado("F2", as_of, clave="clm_id")
        opciones = almacen.estado("F3", as_of)
        meses = {}
        for archivo, ref, dia in sorted(bajas):
            meses.setdefault((archivo, dia[:7]), []).append({"ref_id": ref, "motivo": motivos.get((archivo, ref, dia), "Motivo no consignado")})
        retiradas = {eid for eid, e in evds.items() if e.get("estado_verificacion") == "FUENTE_RETIRADA"}
        for oid, op in opciones.items():
            if op.get("estado") != "VIGENTE":
                continue
            ligadas = {eid for cid in op.get("evidencias", []) for eid in clms.get(cid, {}).get("evidencias", [cid])}
            afectadas = sorted(ligadas & retiradas)
            if not afectadas or afectadas == op.get("revision_bajas", {}).get("evidencias_retiradas"):
                continue
            # Las fichas antiguas pueden carecer de estado de verificación: se conserva su traza de F3.
            candidatas = [evds[eid] for eid in set(op.get("evidencias_ps1", [])) - retiradas if eid in evds]
            raices = sint.raices_de_evidencias(e for e in candidatas if e.get("grado_independencia") == "RAIZ"
                and e.get("direccion") == "FAVORABLE" and e.get("nivel_fuente") in ("A", "B")
                and e.get("estado_verificacion") in (None, "VERIFICADA", "PENDIENTE"))
            mantiene = op.get("ps1") is True and bloque._ps1(raices)
            almacen.escribir("F3", "AG-02", {"tipo_entrada": "ACTUALIZACION", "opp_id": oid,
                "ps1": mantiene, "revision_bajas": {"run_id": run_id, "evidencias_retiradas": afectadas,
                "conclusion": "MANTIENE_RESPALDO" if mantiene else "REQUIERE_REEVALUACION"}})
        emitidos = almacen.estado("HA", as_of, clave="mes_bajas")
        for (archivo, mes), detalle in meses.items():
            clave = archivo + "/" + mes
            referencias = sorted(fila["ref_id"] for fila in detalle)
            if mes < fecha[:7] and referencias != emitidos.get(clave, {}).get("bajas"):
                msg = bloque.mensajeria.crear("CT-21", CUSTODIOS[archivo], "AG-18",
                                              {"periodo": mes, "bajas": detalle}, run_id=run_id)
                almacen.escribir("HA", "AG-18", {"tipo_entrada": "MANTENIMIENTO", "mes_bajas": clave,
                                                 "bajas": referencias, "mensaje": msg})


def avisar_curador(almacen, mensajeria, as_of, run_id, bajas, motivos=None, cfg=None):
    with almacen._transaccion():
        alertas = almacen.estado("F2", as_of, clave="baja_id")
        evds = almacen.estado("F2", as_of, clave="evd_id")
        afectadas = set()
        for archivo, ref, dia in sorted(bajas):
            clave = f"{archivo}/{dia}/{ref}"
            if clave not in alertas:
                motivo = (motivos or {}).get((archivo, ref, dia), "Motivo no consignado")
                msg = mensajeria.crear("CT-11", CUSTODIOS[archivo], "AG-12",
                    {"tipo": "fuente_retirada", "piezas": [{"indice": 0, "fuente": ref, "ref_id": ref, "fecha_baja": dia,
                     "extracto": "", "direccion": "neutra", "afirmacion": f"Fuente retirada de {archivo} el {dia}: {motivo}"}]}, run_id=run_id)
                almacen.escribir("F2", "AG-12", {"tipo_entrada": "ALERTA_PROCEDENCIA", "baja_id": clave, "mensaje": msg})
            for eid, e in evds.items():
                if e.get("ref_id") in (ref, ref.removeprefix("REF-")) and e.get("estado_verificacion") != "FUENTE_RETIRADA":
                    almacen.escribir("F2", "AG-12", {"tipo_entrada": "EVD", "evd_id": eid, "estado_verificacion": "FUENTE_RETIRADA"})
                    e["estado_verificacion"] = "FUENTE_RETIRADA"
                    afectadas.update(e.get("clm_ids", []))
        if afectadas:
            clms = almacen.estado("F2", as_of, clave="clm_id")
            for cid in sorted(afectadas):
                clm = clms.get(cid, {})
                if "evidencias_ps1" in clm:
                    raices = sint.raices_de_clm(clm, evds)
                    almacen.escribir("F2", "AG-12", {"tipo_entrada": "CLM", "clm_id": cid,
                                     "raices_independientes": len(raices), "ps1_cumple": cumple_ps1(raices, cfg)})
        return evds


def retirar_por_manipulacion(bloque, ref_id, as_of, run_id):
    """El registro de explotación pertenece a esta instancia, también durante un backtest."""
    ref = bloque.referencias.por_id(ref_id)
    if not ref or ref["archivo"] != "F9" or not re.fullmatch(r"[A-Z][A-Z0-9-]*-\d+", ref["ref_id"]):
        return
    from .contratos import RE_INYECCION
    if not RE_INYECCION.search(ref["titulo"]):
        return  # una atribución del modelo no demuestra manipulación en la fuente
    almacen = bloque.almacen
    ruta = almacen.carpeta / "F9_bajas.md"
    bloque.referencias.registro_bajas_f9 = ruta
    dia = str(as_of)[:10]
    with almacen._transaccion():
        texto = ruta.read_text(encoding="utf-8") if ruta.exists() else ""
        previa = min((fecha for rid, fecha in bajas_registradas(texto.splitlines()) if rid == ref["ref_id"] and fecha <= dia), default=None)
        if previa is None:
            # El título original puede contener texto externo o datos sensibles.
            linea = f"| {ref['ref_id']} | Título en cuarentena | Manipulación confirmada en F9 | {dia} | — |\n"
            cabecera = "## Registro de bajas\n\n| REF-id | Título | Motivo | Fecha | Sustituta |\n|---|---|---|---|---|\n"
            from tempfile import NamedTemporaryFile
            with NamedTemporaryFile("w", encoding="utf-8", dir=ruta.parent, delete=False) as tmp:
                tmp.write((texto or cabecera) + linea)
            Path(tmp.name).replace(ruta)
        baja = ("F9", ref_id, previa or dia)
        avisar_curador(almacen, bloque.mensajeria, as_of, run_id, {baja}, {baja: "Manipulación confirmada en F9"}, bloque.cfg)
