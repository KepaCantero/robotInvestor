"""QA r01 de T-157 · fallos sembrados en copias desechables del corpus real, fallo cerrado, T-143 simulado y determinismo.

Cada escenario copia `bloque_a/` (sin `11_Ejecutor/` ni `99_Historico*`) a una carpeta temporal, la modifica y lanza el
verificador sobre la copia con el código real (o con un `Codigo` retocado para la clase d). El corpus del repositorio no se toca
(se comprueba con las huellas de todos los .md antes y después). Imprime una línea por comprobación; sale 1 si alguna falla.

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r01_02_siembra.py
"""
import dataclasses
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EJ = Path.cwd()
sys.path.insert(0, str(EJ))
RAIZ = EJ.parent
from bloque_a.herramientas import verificador_ids as vi  # noqa: E402

DOC0 = "Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.1.md"
P_AUDITOR = "02_System_prompts/System prompt - Auditor - Versión óptima V5.0.md"
P_RV = "02_System_prompts/System prompt - Analista de Renta Variable - Versión óptima V5.0.md"
F_AUDITOR = "03_Funciones/Funciones, tareas y cometidos – Auditor – óptima V5.0.md"
resultados: list[tuple[str, bool, str]] = []


def comprobar(que: str, ok: bool, detalle: str = "") -> None:
    resultados.append((que, ok, detalle))
    print(f"[{'OK ' if ok else 'MAL'}] {que}" + (f" · {detalle}" if detalle else ""))


def huellas() -> dict[str, str]:
    return {p.relative_to(RAIZ).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(RAIZ.rglob("*")) if p.is_file() and p.suffix in (".md", ".docx") and "11_Ejecutor" not in p.parts}


def copia(base: Path) -> Path:
    destino = base / "bloque_a"
    shutil.copytree(RAIZ, destino, ignore=lambda d, n: [x for x in n if x == "11_Ejecutor" or x.startswith("99_Historico")])
    return destino


def anadir(raiz: Path, rel: str, texto: str) -> None:
    p = raiz / rel
    p.write_text(p.read_text(encoding="utf-8") + "\n" + texto + "\n", encoding="utf-8")


def hallazgos(inf: dict, ident: str) -> list[tuple[str, str, str]]:
    return [(h["clase"], h["nivel"], h["codigo"]) for h in inf["hallazgos"] if h["id"] == ident]


def nivel_de(inf: dict, ident: str) -> set[str]:
    return {n for _, n, _ in hallazgos(inf, ident)}


def lanzar(raiz: Path, *extra: str, env: dict | None = None) -> tuple[int, str]:
    r = subprocess.run([sys.executable, "-m", "bloque_a.herramientas.verificador_ids", "--raiz", str(raiz), *extra],
                       cwd=EJ, capture_output=True, text=True, timeout=600, env=env)
    return r.returncode, r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""


antes = huellas()
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)

    # ------------------------------------------------------------------ 1. un fallo nominal de cada clase (a)–(f)
    r1 = copia(tmp / "s1")
    anadir(r1, P_AUDITOR, "Siembra QA: ver CT-26. Cumple R28. Aplica PS9. Lee RF-9999. Usa la ficha VOL-GARH-001. Catálogo V4.1.")
    anadir(r1, P_RV, "Siembra QA: escribe en F12.")
    real = vi.Codigo.desde_paquete(r1)
    inf = vi.verificar(r1, real)
    comprobar("(a) CT-26 inexistente → ERROR", ("a", "ERROR", "CT_INEXISTENTE") in hallazgos(inf, "CT-26"))
    comprobar("(b) R28 → ERROR", ("b", "ERROR", "R_INEXISTENTE") in hallazgos(inf, "R28"))
    comprobar("(c) F12 en prosa de un prompt → ERROR", ("c", "ERROR", "F_INEXISTENTE") in hallazgos(inf, "F12"),
              str(hallazgos(inf, "F12")))
    comprobar("(e) RF-9999 → ERROR", ("e", "ERROR", "REF_INEXISTENTE") in hallazgos(inf, "RF-9999"))
    comprobar("(f) PS9 → ERROR", ("f", "ERROR", "PS_INEXISTENTE") in hallazgos(inf, "PS9"))
    comprobar("(d) ficha citada VOL-GARH-001 → ERROR", ("d", "ERROR", "FICHA_CITADA_INEXISTENTE") in hallazgos(inf, "VOL-GARH-001"))
    comprobar("(d) mención «Catálogo V4.1» → AVISO", nivel_de(inf, "Catálogo V4.1") == {"AVISO"})
    # (d) con el código retocado: una ficha solo en el código, una del Catálogo sin código y un ID cambiado
    cod = dataclasses.replace(
        real, fichas_catalogo=tuple(x for x in real.fichas_catalogo if x not in ("FX-TREND-001", "FX-MOM-001")) + ("ZZ-SOLO-001",
                                                                                                                  "FX-MOMM-001"),
        manejadores=(real.manejadores - {"FX-TREND-001", "FX-MOM-001"}) | {"ZZ-SOLO-001", "FX-MOMM-001"})
    inf_d = vi.verificar(r1, cod)
    clase = {f["id"]: f["clase"] for f in inf_d["fichas"]["filas"]}
    comprobar("(d) ficha solo en el código → SOLO_CODIGO + ERROR",
              clase.get("ZZ-SOLO-001") == "SOLO_CODIGO" and "ERROR" in nivel_de(inf_d, "ZZ-SOLO-001"))
    comprobar("(d) ficha IMPLEMENTADO del Catálogo sin código → SOLO_CATALOGO + ERROR",
              clase.get("FX-TREND-001") == "SOLO_CATALOGO" and "ERROR" in nivel_de(inf_d, "FX-TREND-001"))
    comprobar("(d) ID cambiado FX-MOMM-001 ↔ FX-MOM-001 → ID_DISTINTO",
              clase.get("FX-MOMM-001") == clase.get("FX-MOM-001") == "ID_DISTINTO", f"{clase.get('FX-MOMM-001')}")

    # ------------------------------------------------------------------ 2. trampas: errores reales en contextos que se excusan
    r2 = copia(tmp / "s2")
    anadir(r2, P_RV, '{"estado_madurez_metodos":"FIR-CARYY-001: implementado"}')     # campo JSON que SÍ lleva fichas
    anadir(r2, P_RV, '{"metodo":"Brier frente a la referencia (FC-EVAL-009)"}')         # prosa dentro de un valor JSON
    anadir(r2, P_RV, "Clasificación JEL de la fuente; el contrato CT-27 manda.")         # JEL en la misma línea
    anadir(r2, P_RV, "Regla de corte: `R29 = R1 + R2`.")                                 # fórmula entre comillas invertidas
    anadir(r2, P_RV, "Usa la ficha GARCH-VOL-001.")                                       # familia que no existe
    anadir(r2, P_RV, "Según el catálogo v4.0 del Motor.")                                 # versión en minúsculas
    anadir(r2, P_RV, "Contrato CT‑28 con guion no separable.")                       # guion U+2011
    anadir(r2, F_AUDITOR, "Siembra QA: el archivo F13 no existe.")                       # documento con AUD-F13
    anadir(r2, P_RV, "Lee RF-123 y RF-00123.")                                            # RF con otro número de cifras
    inf2 = vi.verificar(r2)
    for ident, que in (("FIR-CARYY-001", "ficha inexistente en «estado_madurez_metodos»"),
                       ("FC-EVAL-009", "ficha inexistente en prosa de un valor JSON"),
                       ("CT-27", "CT inexistente en una línea con «JEL»"),
                       ("R29", "R inexistente dentro de una fórmula"),
                       ("F13", "F13 en prosa de un documento con AUD-F13"),
                       ("RF-123", "RF de 3 cifras"), ("RF-00123", "RF de 5 cifras")):
        n = nivel_de(inf2, ident)
        comprobar(f"trampa: {que} → ERROR", "ERROR" in n, f"obtenido {sorted(n) or 'nada'}")
    comprobar("trampa: ficha de una familia que no existe (GARCH-VOL-001) → algún hallazgo",
              bool(hallazgos(inf2, "GARCH-VOL-001")), "no se detecta" if not hallazgos(inf2, "GARCH-VOL-001") else "")
    comprobar("trampa: «catálogo v4.0» en minúsculas → algún hallazgo",
              any(h["codigo"] == "MENCION_OTRA_VERSION" and any(u["archivo"] == P_RV for u in h["ubicaciones"])
                  for h in inf2["hallazgos"]))
    comprobar("trampa: CT con guion U+2011 → algún hallazgo", bool(hallazgos(inf2, "CT-28")))

    # ------------------------------------------------------------------ 3. fallo cerrado (salida 2 y nada escrito)
    def sale_2(nombre: str, preparar) -> None:
        r = copia(tmp / nombre)
        preparar(r)
        js = tmp / f"{nombre}.json"
        rc, err = lanzar(r, "--json", str(js))
        comprobar(f"fallo cerrado: {nombre} → salida 2 sin JSON", rc == 2 and not js.exists(), f"rc={rc} · {err[:110]}")

    gob = "01_Gobernanza"
    sale_2("sin_doc0", lambda r: (r / gob / DOC0).unlink())
    sale_2("dos_doc0", lambda r: shutil.copy(r / gob / DOC0, r / gob / DOC0.replace("V5.1", "V5.2")))
    sale_2("sin_catalogo", lambda r: (r / "04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.0.md").unlink())
    sale_2("dos_catalogos", lambda r: shutil.copy(r / "04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.0.md",
                                                  r / "04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.1.md"))
    sale_2("doc0_no_utf8", lambda r: (r / gob / DOC0).write_bytes(b"\xff\xfe" + (r / gob / DOC0).read_bytes()))
    sale_2("doc0_sin_6_1", lambda r: (r / gob / DOC0).write_text(
        (r / gob / DOC0).read_text(encoding="utf-8").replace("### 6.1 ", "### 6.X "), encoding="utf-8"))
    sale_2("doc0_es_carpeta", lambda r: ((r / gob / DOC0).unlink(), (r / gob / DOC0).mkdir()))
    sale_2("catalogo_sin_indice", lambda r: (p := r / "04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.0.md")
           .write_text(p.read_text(encoding="utf-8").replace("\n## 4. ", "\n## 4bis "), encoding="utf-8"))
    sale_2("sin_raiz", lambda r: shutil.rmtree(r))
    # salida con la carpeta de destino inexistente: ¿2 (fallo cerrado) o una traza con salida 1 («hay errores»)?
    r3 = copia(tmp / "destino")
    aud = tmp / "aud.md"
    aud.write_text(f"x\n{vi.MARCA_INICIO}\n{vi.MARCA_FIN}\n", encoding="utf-8")
    rc, err = lanzar(r3, "--auditoria", str(aud), "--json", str(tmp / "no_existe" / "i.json"))
    comprobar("destino del JSON inexistente → salida 2 y la auditoría sin tocar",
              rc == 2 and vi.MARCA_INICIO + "\n" + vi.MARCA_FIN in aud.read_text(encoding="utf-8"),
              f"rc={rc}, auditoría {'reescrita' if 'Informe' in aud.read_text(encoding='utf-8') else 'intacta'} · {err[:90]}")

    # ------------------------------------------------------------------ 4. T-143 simulado: V5.2 en su sitio, V5.1 al histórico
    for donde in ("99_Historico_V5.1", f"{gob}/99_Historico_V5.1"):
        r = copia(tmp / donde.replace("/", "_"))
        (r / donde).mkdir(parents=True)
        texto = (r / gob / DOC0).read_text(encoding="utf-8")
        for ext in (".md", ".docx"):
            shutil.move(r / gob / DOC0.replace(".md", ext), r / donde / DOC0.replace(".md", ext))
        # la V5.2 simulada: otro título y una regla R28 nueva, con su fila justo tras la R27
        lineas = texto.splitlines(keepends=True)
        i27 = next(i for i, x in enumerate(lineas) if x.startswith("| R27 |"))
        lineas.insert(i27 + 1, "| R28 | Nueva | Regla de la V5.2 |\n")
        v52 = "".join(lineas).replace("Versión óptima V5.1", "Versión óptima V5.2", 1).replace("(R1–R27)", "(R1–R28)", 1)
        (r / gob / DOC0.replace("V5.1", "V5.2")).write_text(v52, encoding="utf-8")
        anadir(r, P_AUDITOR, "Siembra QA: cumple R28.")
        anadir(r / donde, DOC0, "Cita CT-99 en el histórico.")
        inf5 = vi.verificar(r)
        d0 = inf5["entradas"]["documento_0"]
        comprobar(f"T-143 ({donde}): lee la V5.2", (d0["version_nombre"], d0["version_titulo"]) == ("5.2", "5.2"), d0["archivo"])
        comprobar(f"T-143 ({donde}): R28 definida, sin error", "ERROR" not in nivel_de(inf5, "R28")
                  and "R28" in inf5["reglas"]["definidas"])
        comprobar(f"T-143 ({donde}): el histórico no se lee (CT-99)", not hallazgos(inf5, "CT-99"))
        comprobar(f"T-143 ({donde}): mismos 3 errores", inf5["errores"] == 3, str(inf5["errores"]))

    # ------------------------------------------------------------------ 5. determinismo entre procesos (PYTHONHASHSEED)
    huellas_json = set()
    for semilla in ("0", "1", "3", "7"):
        js = tmp / f"det_{semilla}.json"
        lanzar(RAIZ, "--json", str(js), env={**os.environ, "PYTHONHASHSEED": semilla})
        huellas_json.add(hashlib.sha256(js.read_bytes()).hexdigest())
    comprobar("determinismo: el mismo JSON con PYTHONHASHSEED 0, 1, 3 y 7", len(huellas_json) == 1,
              f"{len(huellas_json)} JSON distintos")
    comprobar("el JSON del repositorio coincide con una ejecución nueva",
              (RAIZ.parent / "docs/auditoria_ids_bloque_a.json").read_bytes() in
              {(tmp / f"det_{s}.json").read_bytes() for s in ("0", "1", "3", "7")},
              "solo con algunas semillas" if len(huellas_json) > 1 else "")
    js = json.loads((tmp / "det_0.json").read_text(encoding="utf-8"))
    vi.validar_informe(js)
    comprobar("el JSON escrito valida contra ESQUEMA_INFORME", True)
    comprobar("sin rutas absolutas en el JSON", str(RAIZ) not in json.dumps(js) and "/tmp" not in json.dumps(js))

comprobar("el corpus del repositorio (.md y .docx) no cambia", huellas() == antes)
malos = [q for q, ok, _ in resultados if not ok]
print(f"\n{len(resultados) - len(malos)}/{len(resultados)} bien. Fallan: {malos if malos else 'ninguna'}")
sys.exit(1 if malos else 0)
