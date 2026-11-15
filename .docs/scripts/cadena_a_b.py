"""Cadena de encargos A → B de punta a punta con el cliente simulado en los dos bloques (T-142, Fase 6). Coste cero.

1. Bloque A: un ciclo C1 (`bloque-a ciclo`) con los datos sintéticos y el universo de ejemplo.
2. Broker (código del lado A, `bloque_a/cadena_b.py`, sin modelo): elige las opciones con siguiente paso
   `ENVIAR_A_BLOQUE_B` y escribe una petición CT-B-01 por cada una; una opción sin correspondencia de ámbito, o cuya
   petición lleva credenciales o datos personales (R8, `DATOS_PROTEGIDOS`, T-147), no se envía (falla cerrado), no se
   escribe ni lleva CT-04 de vuelta, y queda en el resumen con su código.
3. Bloque B: `bloque-b analizar --json` por petición. Si la puerta de tiempo la detiene (EN_PAUSA con `aut_id`), el
   Broker autoriza con la opción que recomienda el propio Bloque B (`autorizar --decidido-por BROKER`), hasta
   `--max-autorizaciones` veces; una pausa por consulta bloqueante no se responde y queda en el resumen.
4. Valida el paquete JSON de cada entrega del Bloque B contra su esquema publicado.
5. Vuelta: CT-04 al Bloque A (`bloque-a decision`) con `ENVIADA_A_BLOQUE_B` y el `resultado_comunicado` (7.7 del
   Documento 0 del Bloque A).
6. Con `--sonda-sin-correspondencia`, envía también a un Bloque B aparte una opción sin correspondencia **sin clave** y
   anota qué hace el Bloque B V2.1 con ella (admisión y clave que elige); es solo evidencia para INC-T142-01.

Los dos ejecutores corren como `python -m bloque_x.cli` desde el `11_Ejecutor` de esta copia (no las CLI instaladas,
que pueden apuntar a otro árbol). El script importa solo el código del Bloque A (el papel del Broker vive allí); el
Bloque B se usa por su línea de comandos y sus ficheros se leen como datos.

Uso (desde la raíz):
  .venv/bin/python .docs/scripts/cadena_a_b.py [--trabajo DIR] [--as-of 2024-03-29] [--config-a YAML]
                                              [--max-autorizaciones 3] [--sonda-sin-correspondencia]
Deja en DIR (por defecto, una carpeta temporal nueva) los estados, entregables, peticiones, CT-04 y `resumen.json`.
Termina con 0 si hay al menos una entrega del Bloque B y todas validan contra su esquema; con 1 si no; con 2 si falla
un ejecutor o la configuración no casa con los ámbitos del Bloque B.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema
import yaml

RAIZ = Path(__file__).resolve().parents[2]
EJ_A = RAIZ / "bloque_a" / "11_Ejecutor"
EJ_B = RAIZ / "bloque_b" / "11_Ejecutor"
ESQUEMA_B = RAIZ / "bloque_b" / "06_Plantillas_entregables" / "Esquema JSON - Paquete de análisis de mercado - Bloque B - V2.0.json"
AMBITOS_B = EJ_B / "config" / "ambitos_ejemplo.yaml"
sys.path.insert(0, str(EJ_A))

from bloque_a.configuracion import cargar_config

from bloque_a import cadena_b


class FalloEjecutor(RuntimeError):
    pass


def _cli(bloque: str, args: list[str]) -> dict:
    cwd = EJ_A if bloque == "a" else EJ_B
    r = subprocess.run([sys.executable, "-m", f"bloque_{bloque}.cli", "--cliente", "mock", *args], cwd=cwd,
                       capture_output=True, text=True, check=False)
    if r.returncode != 0:
        raise FalloEjecutor(f"bloque {bloque.upper()} {' '.join(args[-3:])}: código {r.returncode}\n{r.stderr[-2000:]}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError as e:
        raise FalloEjecutor(f"bloque {bloque.upper()}: la salida no es JSON ({e})\n{r.stdout[-1000:]}") from e


def _escribir(ruta: Path, datos: dict) -> Path:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    return ruta


def _errores_esquema_b(ruta_paquete: str) -> list[str]:
    esquema = json.loads(ESQUEMA_B.read_text(encoding="utf-8"))
    validador = jsonschema.validators.validator_for(esquema)(esquema, format_checker=jsonschema.FormatChecker())
    paquete = json.loads(Path(ruta_paquete).read_text(encoding="utf-8"))
    return [f"{'/'.join(map(str, e.absolute_path))}: {e.message}"[:200] for e in validador.iter_errors(paquete)]


def _analizar_b(base_b: list[str], ruta_pet: Path, max_aut: int) -> tuple[dict, list[dict]]:
    """CT-B-01 al Bloque B y, si la puerta de tiempo pausa, autorizaciones del Broker con la recomendación del B."""
    res = _cli("b", base_b + ["analizar", "--json", str(ruta_pet)])
    acuse = res.get("acuse_inmediato") or {"pet_id": res.get("pet_id"), "admision": res.get("admision")}
    autorizaciones: list[dict] = []
    while res.get("aut_id") and res.get("requiere_autorizacion") and len(autorizaciones) < max_aut:
        opcion = (res.get("recomendacion") or {}).get("opcion")
        if not opcion:
            break
        autorizaciones.append({"aut_id": res["aut_id"], "puerta": res.get("puerta"), "opcion": opcion})
        res = _cli("b", base_b + ["autorizar", "--aut", res["aut_id"], "--opcion", opcion, "--decidido-por", "BROKER",
                                  "--motivo", "Cadena T-142 (simulada): el Broker sigue la recomendación del Bloque B"])
    res.setdefault("acuse_inmediato", acuse)
    return res, autorizaciones


def _clave_elegida_por_b(estado_b: Path, pet_id: str) -> str | None:
    f1 = estado_b / "F1_registro_peticiones_ejecuciones.jsonl"
    if not f1.exists():
        return None
    clave = None
    for linea in f1.read_text(encoding="utf-8").splitlines():
        e = json.loads(linea)
        if e.get("id") == pet_id and e.get("clave_universo"):
            clave = e["clave_universo"]
    return clave


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--trabajo", help="carpeta de trabajo (se crea; por defecto, una temporal nueva)")
    ap.add_argument("--as-of", default="2024-03-29", help="fecha de corte de los dos bloques (datos sintéticos)")
    ap.add_argument("--config-a", help="YAML que se fusiona sobre la configuración del Bloque A (p. ej., para activar tipos)")
    ap.add_argument("--max-autorizaciones", type=int, default=3, help="autorizaciones del Broker por petición")
    ap.add_argument("--sonda-sin-correspondencia", action="store_true",
                    help="envía además, a un Bloque B aparte, una opción sin correspondencia sin clave (evidencia)")
    a = ap.parse_args(argv)
    w = Path(a.trabajo).resolve() if a.trabajo else Path(tempfile.mkdtemp(prefix="cadena_a_b_"))
    w.mkdir(parents=True, exist_ok=True)
    cfg = cargar_config(a.config_a)
    ambitos_b = yaml.safe_load(AMBITOS_B.read_text(encoding="utf-8")) or {}
    ajenas = sorted({v for v in ((cfg.get("cadena_b") or {}).get("correspondencia_ambitos") or {}).values()} - set(ambitos_b))
    if ajenas:
        print(f"La correspondencia de ámbitos cita claves que el Bloque B no tiene: {ajenas}", file=sys.stderr)
        return 2
    config_a = ["--config", str(Path(a.config_a).resolve())] if a.config_a else []
    base_a = config_a + ["--datos", "ejemplos/datos_sinteticos", "--universo", "config/universo_ejemplo.csv",
                         "--estado", str(w / "a" / "estado"), "--salida", str(w / "a" / "salida"), "--as-of", a.as_of]
    base_b = ["--estado", str(w / "b" / "estado"), "--salida", str(w / "b" / "salida"), "--as-of", a.as_of]
    resumen: dict = {"trabajo": str(w), "as_of": a.as_of, "envios": [], "no_enviadas": []}
    try:
        ciclo = _cli("a", base_a + ["ciclo"])
        resumen["bloque_a"] = {k: ciclo.get(k) for k in ("run_id", "estado", "entrega", "g3", "top3_por_clase")}
        paquete = json.loads(Path(ciclo["entregables"]["paquete_json"]).read_text(encoding="utf-8"))
        enviables = cadena_b.opciones_enviables(paquete)
        resumen["opciones_enviables"] = enviables
        for opp_id in enviables:
            try:
                pet = cadena_b.construir_peticion(paquete, opp_id, cfg)
            except cadena_b.ErrorCadenaB as e:
                resumen["no_enviadas"].append({"opp_id": opp_id, "codigo": e.codigo, "detalle": e.detalle})
                continue
            ruta_pet = _escribir(w / "peticiones" / f"{opp_id}.json", pet)
            res, auts = _analizar_b(base_b, ruta_pet, a.max_autorizaciones)
            envio = {"opp_id": opp_id, "clave_universo": pet["objeto"]["clave_universo"], "peticion": str(ruta_pet),
                     "pet_id": res.get("pet_id"), "admision": (res.get("acuse_inmediato") or {}).get("admision"),
                     "autorizaciones": auts, "estado_peticion": res.get("estado_peticion"), "rec_id": res.get("rec_id"),
                     "veredicto": (res.get("resumen") or {}).get("veredicto"),
                     "resultado_del_analisis": (res.get("resumen") or {}).get("resultado_del_analisis"),
                     "estado_g3": res.get("estado_g3")}
            ruta_paq_b = (res.get("entregables") or {}).get("paquete_json")
            if ruta_paq_b:
                errores = _errores_esquema_b(ruta_paq_b)
                envio["paquete_b"] = ruta_paq_b
                envio["paquete_b_valido"] = not errores
                envio["errores_esquema_b"] = errores[:10]
            ct04 = cadena_b.ct04_desde_respuesta_b(opp_id, res)
            ruta_ct04 = _escribir(w / "ct04" / f"{opp_id}.json", ct04)
            vuelta = _cli("a", base_a + ["decision", "--json", str(ruta_ct04)])
            envio["vuelta_a"] = {"ct04": str(ruta_ct04), "ret_id": vuelta.get("ret_id"), "estado": vuelta.get("estado"),
                                 "resultado_comunicado": ct04["resultado_comunicado"]["texto"]}
            resumen["envios"].append(envio)
        if a.sonda_sin_correspondencia:
            sin = next((n for n in resumen["no_enviadas"] if n["codigo"] == "SIN_CORRESPONDENCIA_AMBITO"), None)
            try:   # T-147: la sonda pasa los mismos filtros (R8, configuración) que el envío; si no, se anota
                pet = cadena_b.construir_peticion(paquete, sin["opp_id"], cfg, exigir_correspondencia=False) if sin else None
            except cadena_b.ErrorCadenaB as e:
                resumen["sonda_sin_correspondencia"] = {"opp_id": sin["opp_id"], "codigo": e.codigo, "detalle": e.detalle}
                pet = None
            if pet is not None:
                ruta_pet = _escribir(w / "sonda" / f"{sin['opp_id']}_sin_clave.json", pet)
                estado_sonda = w / "b_sonda" / "estado"
                res = _cli("b", ["--estado", str(estado_sonda), "--salida", str(w / "b_sonda" / "salida"), "--as-of", a.as_of,
                                 "analizar", "--json", str(ruta_pet)])
                acuse = res.get("acuse_inmediato") or res
                resumen["sonda_sin_correspondencia"] = {
                    "opp_id": sin["opp_id"], "ambito_a": pet["paquete_para_bloque_B"]["ambito"],
                    "admision": acuse.get("admision"), "motivo": acuse.get("motivo"),
                    "estado_peticion": res.get("estado_peticion") or res.get("estado"),
                    "clave_elegida_por_b": _clave_elegida_por_b(estado_sonda, acuse.get("pet_id") or ""),
                    "nota": "Sin clave, el Bloque B V2.1 no responde AMBITO_INDETERMINADO: su Director encuadra con los ámbitos "
                            "de su configuración (INC-T142-01). Por eso el Broker falla cerrado."}
    except FalloEjecutor as e:
        print(str(e), file=sys.stderr)
        _escribir(w / "resumen.json", resumen)
        return 2
    entregadas = [e for e in resumen["envios"] if e.get("estado_peticion") == "ENTREGADA"]
    resumen["veredicto_cadena"] = {"entregadas": len(entregadas),
                                   "todas_validas": all(e.get("paquete_b_valido") for e in entregadas),
                                   "vueltas_registradas": sum(1 for e in resumen["envios"] if (e.get("vuelta_a") or {}).get("ret_id"))}
    _escribir(w / "resumen.json", resumen)
    print(json.dumps(resumen, ensure_ascii=False, indent=1))
    return 0 if entregadas and resumen["veredicto_cadena"]["todas_validas"] else 1


if __name__ == "__main__":
    sys.exit(main())
