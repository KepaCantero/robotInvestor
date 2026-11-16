"""QA r02 de T-157 · ataques a las correcciones de la r02 (H-01, H-02, H-03, H-05, H-06) en copias desechables del corpus real.

1. Determinismo con empates sembrados en todas las clases (CT-01/CT-1, R1/R01, PS1/PS01, F5/F05, RF-0001/RF-1, TA-01/TA-1),
   con cuatro PYTHONHASHSEED en subprocesos.
2. Otras formas de esconder una ficha: el símbolo de una serie declarado en otro archivo, el mismo ID como `serie_ht01` y como
   `ficha_id`, una ficha en un array JSON, con guion U+2011, en negrita, entre comillas invertidas con operador, con otro
   número de cifras, y una de familia desconocida poco parecida.
3. Que las reglas nuevas no creen errores falsos: los mismos contextos legítimos del corpus real, más un rango de funciones
   válido y un código JEL de la lista, siguen siendo INFO; y el corpus real sigue en 2 errores.
4. H-06: un destino cuya carpeta existe pero no admite archivos (/proc) — ¿queda algo escrito a medias?
Imprime una línea por comprobación; sale 1 si alguna falla. El corpus del repositorio no se toca (huellas antes y después).

Uso (desde bloque_a/11_Ejecutor):
    ../../.venv/bin/python ../../.docs/tickets/T-157/revisores/r02_01_ataques.py
"""
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

P_AUDITOR = "02_System_prompts/System prompt - Auditor - Versión óptima V5.0.md"
P_RV = "02_System_prompts/System prompt - Analista de Renta Variable - Versión óptima V5.0.md"
F_AUDITOR = "03_Funciones/Funciones, tareas y cometidos – Auditor – óptima V5.0.md"
RC = "05_Archivos_operativos/Registro de cálculos del Motor (esquema V2.0).md"
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


def niveles(inf: dict, ident: str) -> set[str]:
    return {h["nivel"] for h in inf["hallazgos"] if h["id"] == ident}


def lanzar(raiz: Path, *extra: str, semilla: str | None = None) -> int:
    env = {**os.environ, **({"PYTHONHASHSEED": semilla} if semilla else {})}
    return subprocess.run([sys.executable, "-m", "bloque_a.herramientas.verificador_ids", "--raiz", str(raiz), *extra],
                          cwd=EJ, capture_output=True, text=True, timeout=600, env=env).returncode


antes = huellas()
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)

    # ------------------------------------------------------------------ 1. empates en todas las clases
    r1 = copia(tmp / "empates")
    anadir(r1, P_AUDITOR, "Empates QA: CT-01 y CT-1; R1 y R01; PS1 y PS01; F5 y F05; F2 y F02.")
    anadir(r1, P_RV, "Empates QA: RF-0001 y RF-1; TA-01 y TA-1; TM-01 y TM-1.")
    bytes_ = set()
    for s in ("0", "1", "3", "7"):
        js, md = tmp / f"e{s}.json", tmp / f"e{s}.md"
        lanzar(r1, "--json", str(js), "--md", str(md), semilla=s)
        bytes_.add((js.read_bytes(), md.read_bytes()))
    comprobar("H-01: mismo JSON y Markdown con 4 semillas y empates en CT, R, PS, F, RF, TA y TM", len(bytes_) == 1,
              f"{len(bytes_)} salidas distintas")

    # ------------------------------------------------------------------ 2. otras formas de esconder una ficha
    r2 = copia(tmp / "fichas")
    anadir(r2, RC, '{"datos":[{"simbolo":"FX-TRND-009","fuente":"HT-01"}]}')             # «símbolo» en un ejemplo de RC…
    anadir(r2, P_RV, "Calcula el momento con la ficha FX-TRND-009.")                       # …y la misma cadena como ficha
    anadir(r2, P_RV, '{"serie_ht01":"VOL-GARH-001","operacion":{"ficha_id":"VOL-GARH-001"}}')  # símbolo y ficha a la vez
    anadir(r2, P_RV, '{"fichas":["FX-MOMM-001","ST-DESK-001"]}')                           # array JSON
    anadir(r2, P_RV, "Usa la FX‑CORRR‑001.")                                     # guion U+2011 dentro del ID
    anadir(r2, P_RV, "Usa la **RISK-VARR-001** y `SIM-MCC-001 / 2`.")                       # negrita y fórmula
    anadir(r2, P_RV, "Usa la FX-TREND-01 y la FX-TREND-0001.")                              # otro número de cifras
    anadir(r2, P_RV, "Usa la ficha GARCH-VOL-001.")                                          # familia desconocida
    inf2 = vi.verificar(r2)
    comprobar("H-02: una ficha cuyo texto se declaró «simbolo» en otro archivo → ERROR en la cita de ficha",
              "ERROR" in niveles(inf2, "FX-TRND-009"), f"obtenido {sorted(niveles(inf2, 'FX-TRND-009')) or 'nada'}")
    comprobar("H-02: el mismo ID como serie_ht01 y como ficha_id en la misma línea → ERROR",
              "ERROR" in niveles(inf2, "VOL-GARH-001"), f"obtenido {sorted(niveles(inf2, 'VOL-GARH-001')) or 'nada'}")
    for ident, que in (("FX-MOMM-001", "ficha en un array JSON"), ("ST-DESK-001", "segunda ficha del array"),
                       ("FX-CORRR-001", "ficha con guion U+2011"), ("RISK-VARR-001", "ficha en negrita"),
                       ("SIM-MCC-001", "ficha entre comillas invertidas con operador")):
        comprobar(f"H-02: {que} → ERROR", "ERROR" in niveles(inf2, ident), f"obtenido {sorted(niveles(inf2, ident)) or 'nada'}")
    for ident in ("FX-TREND-01", "FX-TREND-0001"):
        comprobar(f"ficha con otro número de cifras ({ident}) → algún hallazgo", bool(niveles(inf2, ident)),
                  f"obtenido {sorted(niveles(inf2, ident)) or 'nada'}")
    comprobar("H-05: familia desconocida poco parecida (GARCH-VOL-001) → a la vista (INFO o más)",
              bool(niveles(inf2, "GARCH-VOL-001")), f"obtenido {sorted(niveles(inf2, 'GARCH-VOL-001')) or 'nada'}")

    # ------------------------------------------------------------------ 3. que las reglas nuevas no creen errores falsos
    real = vi.verificar(RAIZ)
    comprobar("corpus real: 2 errores (FX-MC10-003 y RF-0123)", real["errores"] == 2
              and {h["id"] for h in real["hallazgos"] if h["nivel"] == "ERROR"} == {"FX-MC10-003", "RF-0123"})
    r3 = copia(tmp / "legitimos")
    anadir(r3, P_RV, "Filtro por código JEL (E43, R30, F31).")                              # lista JEL legítima
    anadir(r3, P_RV, "Pendiente `(F1 − F12) / F12` de la curva.")                           # fórmula legítima
    anadir(r3, F_AUDITOR, "Resultados de AUD-F03 a F12.")                                    # rango con dos extremos del documento
    anadir(r3, P_RV, "Las fases F0–F10 no son archivos; CT-B-28 es del Bloque B.")          # fases y CT de otro bloque
    anadir(r3, P_RV, "El índice IDX-FICT-001 sube.")                                         # serie ya declarada en el corpus
    inf3 = vi.verificar(r3)
    comprobar("sin errores falsos con contextos legítimos (siguen 2 errores)", inf3["errores"] == 2,
              str(sorted({h['id'] for h in inf3['hallazgos'] if h['nivel'] == 'ERROR'})))

    # ------------------------------------------------------------------ 4. H-06: destino que existe pero no admite archivos
    r4 = copia(tmp / "destinos")
    js = tmp / "ok.json"
    aud = tmp / "aud.md"
    aud.write_text(f"x\n{vi.MARCA_INICIO}\n{vi.MARCA_FIN}\n", encoding="utf-8")
    rc = lanzar(r4, "--json", str(js), "--md", "/proc/qa_t157.md", "--auditoria", str(aud))
    comprobar("H-06: --md en una carpeta que no admite archivos → salida 2 y nada escrito",
              rc == 2 and not js.exists() and "Informe" not in aud.read_text(encoding="utf-8"),
              f"rc={rc}, JSON {'escrito' if js.exists() else 'no escrito'}, auditoría "
              f"{'reescrita' if 'Informe' in aud.read_text(encoding='utf-8') else 'intacta'}")
    comprobar("H-06: ningún temporal .*.tmp abandonado", not list(tmp.glob(".*.tmp")))

comprobar("el corpus del repositorio (.md y .docx) no cambia", huellas() == antes)
malos = [q for q, ok, _ in resultados if not ok]
print(f"\n{len(resultados) - len(malos)}/{len(resultados)} bien. Fallan: {malos if malos else 'ninguna'}")
sys.exit(1 if malos else 0)
