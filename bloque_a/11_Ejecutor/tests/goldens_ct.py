"""T-114 · Fase 3: goldens de los contratos CT-01 a CT-25 del Bloque A.

Genera el texto exacto de cada golden a partir del código (`bloque_a/contratos.py`), de los esquemas derivados del
Anexo B (`goldens/anexo_b_esquemas.json`, escritos a mano) y de un ciclo semanal simulado. Las pruebas
(`test_fase3_goldens.py`) comparan ese texto, byte a byte, con los ficheros de `goldens/`.

Uso, desde `bloque_a/11_Ejecutor`:
    python tests/goldens_ct.py                          comprueba; termina con 1 si algo difiere
    python tests/goldens_ct.py --update --motivo "…"    re-congela (solo deliberado) y lo anota en REGISTRO.md

La regla de re-congelado está en `goldens/README.md`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import jsonschema

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent                 # bloque_a/11_Ejecutor
BLOQUE = RAIZ.parent               # bloque_a
for _ruta in (str(RAIZ), str(AQUI)):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

from bloque_a.almacen import Almacen, Reloj

from bloque_a import contratos

CARPETA = AQUI / "goldens"
A_MANO = ("anexo_b_esquemas.json", "anexo_b_ejemplos.json")
GENERADOS = ("tablas_contratos.json", "esquemas_respuestas.json", "mensajes_ejemplo.json", "formas_ciclo_mock.json",
             "divergencias_anexo_b.json", "huellas.json")
DOCUMENTOS = ("README.md", "REGISTRO.md")
MARCA = "derivado del Anexo B"
RUN_EJEMPLO = "RUN-2026-0001"
# Campos comunes de todo mensaje (primer párrafo del Anexo B y `Mensajeria.crear`): no cuentan como diferencia
SOBRE = frozenset({"msg_id", "contrato", "version_contrato", "emisor", "receptor", "run_id", "query_id", "timestamp", "tipo_mensaje",
                   "presupuesto", "consumo", "estado", "limitaciones", "autoevaluacion", "consultas_broker",
                   "solicitudes_credenciales", "supuestos_declarados"})


def texto(obj) -> str:
    """Forma canónica de un golden: claves ordenadas, sangría de un espacio, UTF-8 sin escapes y salto final."""
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def _canales(tabla: dict) -> dict:
    return {ct: [{"emisores": sorted(em), "receptores": sorted(rc)} for em, rc in pares] for ct, pares in tabla.items()}


def tablas() -> dict:
    """Las tablas de `contratos.py` que definen qué contratos hay, por dónde viajan y qué campos exigen."""
    return {"version_contrato": contratos.VERSION_CONTRATO, "estados": list(contratos.ESTADOS),
            "campo_estado": dict(contratos.CAMPO_ESTADO),
            "estados_especificos": {k: list(v) for k, v in contratos.ESTADOS_ESPECIFICOS.items()},
            "canales": _canales(contratos.CANALES), "canales_v6": _canales(contratos.CANALES_V6),
            "campos_minimos": {k: list(v) for k, v in contratos.CAMPOS_MINIMOS.items()},
            "campos_retorno": {k: list(v) for k, v in contratos.CAMPOS_RETORNO.items()}}


def esquemas_respuestas() -> dict:
    return json.loads(json.dumps(contratos.ESQUEMAS))


def leer_a_mano(carpeta: Path = CARPETA) -> tuple[dict, dict]:
    esquemas = json.loads((carpeta / A_MANO[0]).read_text(encoding="utf-8"))
    ejemplos = json.loads((carpeta / A_MANO[1]).read_text(encoding="utf-8"))
    return esquemas, ejemplos


def sin_campos_en_anexo_b(esquemas: dict) -> list[str]:
    """Contratos en vigor para los que el Anexo B no da campos (los remite a los prompts de sistema)."""
    con = {clave.split(".")[0] for clave in esquemas}
    return sorted(set(contratos.CANALES) - con)


def _canal(ct: str, sentido: str) -> tuple[str, str]:
    """Emisor y receptor del ejemplo: el primer canal del contrato; el retorno vuelve por él si el canal lo permite."""
    emisores, receptores = contratos.CANALES[ct][0]
    em, rc = min(emisores), min(receptores)
    if sentido == "RETORNO" and contratos.canal_permitido(ct, rc, em):
        return rc, em
    return em, rc


def _mensajeria(carpeta: Path, fecha: str):
    reloj = Reloj()
    reloj.fijar(fecha)
    return contratos.Mensajeria(Almacen(carpeta, reloj))


def _crear(mensajeria, clave: str, cuerpo: dict) -> dict:
    """Crea el mensaje de un cuerpo del Anexo B por el canal del contrato. Los campos del sobre que el Anexo B pone en el
    cuerpo (`run_id`, `query_id`, `presupuesto`, `consumo`) se pasan por su sitio, como hace el ejecutor."""
    ct, sentido = clave.split(".")
    em, rc = _canal(ct, sentido)
    run_id = cuerpo.get("run_id") or (None if cuerpo.get("query_id") else RUN_EJEMPLO)
    try:
        msg = mensajeria.crear(ct, em, rc, cuerpo, run_id=run_id, query_id=cuerpo.get("query_id"),
                               presupuesto=cuerpo.get("presupuesto"), consumo=cuerpo.get("consumo"), tipo_mensaje=sentido)
        return {"mensaje": msg}
    except (ValueError, PermissionError) as e:
        return {"rechazo": {"clase": type(e).__name__, "motivo": str(e)}}


def mensajes_ejemplo(ejemplos: dict, carpeta_tmp: Path, fecha: str) -> dict:
    """El mensaje que `Mensajeria.crear` construye con cada ejemplo del Anexo B, o la clase de su rechazo."""
    mensajeria = _mensajeria(Path(carpeta_tmp) / "estado_mensajes", fecha)
    return {clave: _crear(mensajeria, clave, ejemplos[clave]) for clave in sorted(ejemplos)}


def capturar_ciclo(carpeta_tmp: Path, fecha: str) -> list[dict]:
    """Los mensajes que crea un ciclo semanal simulado (MockClient, los doce perfiles de las pruebas)."""
    import conftest
    from bloque_a.configuracion import RUTA_UNIVERSO_EJEMPLO
    from bloque_a.herramientas.ht01_datos import cargar_universo

    bloque = conftest.nuevo_bloque(carpeta_tmp, cargar_universo(RUTA_UNIVERSO_EJEMPLO))
    capturados: list[dict] = []
    crear = bloque.mensajeria.crear

    def crear_y_anotar(*args, **kwargs):
        msg = crear(*args, **kwargs)
        capturados.append(json.loads(json.dumps(msg, default=str)))
        return msg

    bloque.mensajeria.crear = crear_y_anotar
    bloque.ciclo(fecha)
    return capturados


def formas(capturados: list[dict], esquemas: dict | None = None) -> dict:
    """Por contrato y tipo de mensaje: quién emite, quién recibe, qué claves van siempre y cuáles a veces, y los valores
    vistos en los campos que el Anexo B cierra con una lista."""
    esquemas = esquemas or {}
    grupos: dict[str, list[dict]] = {}
    for msg in capturados:
        grupos.setdefault(f"{msg['contrato']}.{msg['tipo_mensaje']}", []).append(msg)
    salida = {}
    for clave in sorted(grupos):
        mensajes = grupos[clave]
        siempre = set.intersection(*(set(m) for m in mensajes))
        todas = set.union(*(set(m) for m in mensajes))
        salida[clave] = {"emisores": sorted({m["emisor"] for m in mensajes}), "receptores": sorted({m["receptor"] for m in mensajes}),
                         "claves_siempre": sorted(siempre), "claves_a_veces": sorted(todas - siempre)}
        cerrados = sorted(c for c, p in esquemas.get(clave, {}).get("properties", {}).items() if "enum" in p)
        if cerrados:
            salida[clave]["valores_de_listas_cerradas"] = {c: sorted({str(m[c]) for m in mensajes if c in m}) for c in cerrados}
    return salida


def _errores(esquema: dict, instancia: dict) -> list[str]:
    validador = jsonschema.Draft202012Validator(esquema)
    return sorted({f"{'/'.join(str(p) for p in e.absolute_path) or '(raíz)'}: {e.validator} {e.validator_value!r}"
                   if e.validator != "required" else f"{'/'.join(str(p) for p in e.absolute_path) or '(raíz)'}: {e.message}"
                   for e in validador.iter_errors(instancia)})


def divergencias(esquemas: dict, ejemplos: dict, capturados: list[dict], carpeta_tmp: Path, fecha: str) -> dict:
    """Dónde difieren el Anexo B (esquemas derivados) y el ejecutor, medido con el propio ejecutor. Se congela: una
    diferencia nueva hace fallar la suite.

    - `el_ejecutor_rechaza_el_ejemplo_del_anexo_b`: el ejemplo cumple el esquema derivado y `Mensajeria.crear` no lo admite;
    - `el_ejecutor_admite_que_falte`: campos obligatorios en el Anexo B sin los cuales `Mensajeria.crear` admite el mensaje;
    - `el_ejecutor_exige_y_el_anexo_b_no_nombra`: campos mínimos del ejecutor que el Anexo B no nombra;
    - los mensajes de un ciclo simulado que no cumplen el esquema derivado, con el motivo."""
    mensajeria = _mensajeria(Path(carpeta_tmp) / "estado_divergencias", fecha)
    campos: dict[str, dict] = {}
    for clave in sorted(esquemas):
        ct, sentido = clave.split(".")
        tabla = contratos.CAMPOS_MINIMOS if sentido == "ENCARGO" else contratos.CAMPOS_RETORNO
        d: dict = {}
        sobra = sorted(set(tabla.get(ct, [])) - set(esquemas[clave].get("properties", {})) - SOBRE)
        if sobra:
            d["el_ejecutor_exige_y_el_anexo_b_no_nombra"] = sobra
        entero = _crear(mensajeria, clave, ejemplos[clave])
        if "rechazo" in entero:
            d["el_ejecutor_rechaza_el_ejemplo_del_anexo_b"] = entero["rechazo"]
        else:
            falta = [c for c in sorted(set(esquemas[clave].get("required", [])) - SOBRE)
                     if "mensaje" in _crear(mensajeria, clave, {k: v for k, v in ejemplos[clave].items() if k != c})]
            if falta:
                d["el_ejecutor_admite_que_falte"] = falta
        if d:
            campos[clave] = d
    ciclo: dict[str, list[str]] = {}
    for msg in capturados:
        clave = f"{msg['contrato']}.{msg['tipo_mensaje']}"
        if clave in esquemas:
            errores = _errores(esquemas[clave], msg)
            if errores:
                ciclo[clave] = sorted(set(ciclo.get(clave, [])) | set(errores))
    return {"por_contrato": campos, "mensajes_del_ciclo_simulado_que_no_cumplen_el_anexo_b": dict(sorted(ciclo.items())),
            "contratos_sin_campos_en_el_anexo_b": sin_campos_en_anexo_b(esquemas)}


def _sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def huellas(carpeta: Path = CARPETA) -> dict:
    """Huellas de lo que no se genera: el Documento 0, los esquemas publicados y los dos ficheros escritos a mano."""
    doc0 = sorted((BLOQUE / "01_Gobernanza").glob("Documento 0*.md"))
    publicados = sorted((BLOQUE / "06_Plantillas_entregables").glob("Esquema JSON*.json"))
    salida = {f"{r.parent.name}/{r.name}": _sha(r) for r in doc0 + publicados}
    salida.update({f"goldens/{n}": _sha(carpeta / n) for n in A_MANO})
    return salida


def generar(carpeta: Path = CARPETA, fecha: str | None = None) -> dict[str, str]:
    """Nombre de cada golden generado → su texto. No escribe nada en `carpeta`."""
    if fecha is None:
        import conftest
        fecha = conftest.AS_OF
    esquemas, ejemplos = leer_a_mano(carpeta)
    with tempfile.TemporaryDirectory() as tmp:
        capturados = capturar_ciclo(Path(tmp) / "ciclo", fecha)
        mensajes = mensajes_ejemplo(ejemplos, Path(tmp), fecha)
        difieren = divergencias(esquemas, ejemplos, capturados, Path(tmp), fecha)
    return {"tablas_contratos.json": texto(tablas()), "esquemas_respuestas.json": texto(esquemas_respuestas()),
            "mensajes_ejemplo.json": texto(mensajes), "formas_ciclo_mock.json": texto(formas(capturados, esquemas)),
            "divergencias_anexo_b.json": texto(difieren), "huellas.json": texto(huellas(carpeta))}


def comparar(generados: dict[str, str], carpeta: Path = CARPETA) -> list[str]:
    """Diferencias entre lo generado y lo congelado; lista vacía si coincide todo, byte a byte."""
    problemas = []
    for nombre in sorted(generados):
        ruta = carpeta / nombre
        if not ruta.is_file():
            problemas.append(f"{nombre}: falta el golden")
        elif ruta.read_bytes() != generados[nombre].encode("utf-8"):
            problemas.append(f"{nombre}: difiere del golden congelado{_primera_diferencia(ruta, generados[nombre])}")
    esperados = set(generados) | set(A_MANO) | set(DOCUMENTOS)
    presentes = {p.name for p in carpeta.iterdir()} if carpeta.is_dir() else set()
    problemas += [f"{n}: fichero que no es un golden conocido" for n in sorted(presentes - esperados)]
    problemas += [f"{n}: falta" for n in sorted(esperados - presentes - set(generados))]
    return problemas


def _primera_diferencia(ruta: Path, nuevo: str) -> str:
    viejas = ruta.read_text(encoding="utf-8", errors="replace").splitlines()
    nuevas = nuevo.splitlines()
    for n, (a, b) in enumerate(zip(viejas, nuevas), start=1):
        if a != b:
            return f" (línea {n}: congelado «{a.strip()}», generado «{b.strip()}»)"
    return f" (congelado {len(viejas)} líneas, generado {len(nuevas)})"


def recongelar(motivo: str, carpeta: Path = CARPETA, generados: dict[str, str] | None = None, hoy: str | None = None) -> list[str]:
    """Re-congelado deliberado: exige motivo, escribe los goldens que cambian y lo anota en REGISTRO.md."""
    if not isinstance(motivo, str) or not motivo.strip():
        raise ValueError("el re-congelado exige un motivo (--motivo)")
    generados = generar(carpeta) if generados is None else generados
    cambiados = [n for n in sorted(generados)
                 if not (carpeta / n).is_file() or (carpeta / n).read_bytes() != generados[n].encode("utf-8")]
    for nombre in cambiados:
        (carpeta / nombre).write_bytes(generados[nombre].encode("utf-8"))
    if cambiados:
        linea = f"- {hoy or dt.date.today().isoformat()} · {', '.join(cambiados)} · {' '.join(motivo.split())}\n"
        with (carpeta / "REGISTRO.md").open("a", encoding="utf-8") as fh:
            fh.write(linea)
    return cambiados


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Goldens de los contratos CT del Bloque A (T-114).")
    ap.add_argument("--update", action="store_true", help="re-congela; exige --motivo")
    ap.add_argument("--motivo", default="", help="por qué cambia el formato (va a REGISTRO.md)")
    args = ap.parse_args(argv)
    if args.update:
        if not args.motivo.strip():
            print("ERROR: el re-congelado exige un motivo: --update --motivo \"…\"", file=sys.stderr)
            return 2
        cambiados = recongelar(args.motivo)
        print("re-congelados: " + (", ".join(cambiados) if cambiados else "ninguno (ya coincidían)"))
        return 0
    problemas = comparar(generar())
    for p in problemas:
        print("DIFERENCIA · " + p, file=sys.stderr)
    print("goldens de contratos: " + ("coinciden" if not problemas else f"{len(problemas)} diferencias"))
    return 1 if problemas else 0


if __name__ == "__main__":
    raise SystemExit(main())
