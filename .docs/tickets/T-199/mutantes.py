"""Mutantes de T-199: un mutante de coste (cuadrático, o el defecto que vigila la prueba) por cada prueba de tiempo.

Cada mutante cambia el código de producción en la copia, ejecuta solo su prueba y lo restaura. MUERTO: la prueba falla por
su aserción de tiempo o, en ST-INF-001, de recuento (se muestra la línea). Con `--originales` ejecuta además las doce pruebas sin mutar (tienen que pasar).
Para la prueba con carga, se lanza antes `carga.sh` (ver `pruebas.md`).

Uso (desde bloque_a/11_Ejecutor): ../../.venv/bin/python ../../.docs/tickets/T-199/mutantes.py . [--originales] [M01 M02 …]
"""
import subprocess
import sys
import time
from pathlib import Path

EJ = Path(sys.argv[1])
CON, LLM, HT9 = "bloque_a/contratos.py", "bloque_a/llm.py", "bloque_a/herramientas/ht09.py"
V6 = "bloque_a/diseno_v6.py"
F_FRASE = "def frase_prohibida(t: str, perm, marcas: dict | None = None) -> str | None:\n"
F_TEXTO = "def texto_prohibido(t, permitidos=None, marcas: dict | None = None) -> str | None:\n"
RIE, SER, FRB = "bloque_a/motor/fichas_riesgo.py", "bloque_a/motor/fichas_series.py", "bloque_a/motor/frontera_b.py"


def r8_reescaneo(bloque: int) -> list[tuple[str, str]]:
    """R8 cuadrático: antes de mirar el texto, vuelve a mirar desde el principio el prefijo cada `bloque` caracteres
    (el tipo de defecto de H-26/H-37 de T-102: cada tramo nuevo repasa todo lo anterior). `bloque` es fijo: coste n²/2·bloque."""
    return [("def secretos_en_texto(texto) -> list[str]:\n",
             "def secretos_en_texto(texto) -> list[str]:\n"
             "    if isinstance(texto, str):\n"
             f"        for _i in range({bloque}, len(texto), {bloque}):\n"
             "            _secretos_sin_mutar(texto[:_i])\n"
             "    return _secretos_sin_mutar(texto)\n\n\n"
             "def _secretos_sin_mutar(texto) -> list[str]:\n")]


def ht09_reescaneo(bloque: int) -> list[tuple[str, str]]:
    """G3-MET-13 cuadrático: cada texto se vuelve a comprobar desde el principio cada `bloque` caracteres."""
    firma = "(textos: Iterable[tuple[str, str, str]], madurez: Mapping[str, str], sirve: Callable[[str], bool],\n"
    return [(f"def comprobar_madurez{firma}",
             "def comprobar_madurez(textos, madurez, sirve, fichas=()):\n"
             "    textos = list(textos)\n"
             "    for ruta, crudo, sev in textos:\n"
             "        if isinstance(crudo, str):\n"
             f"            for _i in range({bloque}, len(crudo), {bloque}):\n"
             "                _comprobar_sin_mutar([(ruta, crudo[:_i], sev)], madurez, sirve, fichas)\n"
             "    return _comprobar_sin_mutar(textos, madurez, sirve, fichas)\n\n\n"
             f"def _comprobar_sin_mutar{firma}")]


T123 = "tests/test_t123_r8_iban_y_tarjetas.py::test_el_coste_es_lineal"
T92 = "tests/test_t92_revision.py::test_r02_h17_r8_sin_retroceso_cuadratico"
T103 = "tests/test_t103_r8_y_bajos.py::test_r02_h47_r8_lineal_con_un_tramo_largo_de_barras"
T130 = "tests/test_t130_r8.py::test_h08_coste_lineal"
T113A = "tests/test_t113_deuda.py::test_h56_contenido_sensible_lineal_con_mucho_anidamiento"
T113B = "tests/test_t113_deuda.py::test_r02_h01_lineal_con_listas_de_diccionarios"
T113C = "tests/test_t113_deuda.py::test_r02_h01_la_misma_lista_en_muchos_sitios_se_mira_una_vez"
T165 = "tests/test_t165_g3_met13.py::test_coste_lineal_en_una_frase_larga_y_en_muchas_fichas_por_parrafo"
T144 = "tests/test_t144.py::test_h03_indice_grande_con_salida_y_exclusion_sin_fechas_comunes"
TMC = "tests/test_fase2_riesgo.py::test_la_ficha_mas_cara_en_su_cota_cabe_en_tiempo"
TCOTA = "tests/test_fase2_series.py::test_cota_de_cada_parametro_de_tamano[TEM-DIFF-001:B]"
TINF = "tests/test_fase2_series.py::test_st_inf_n_minimo_de_potencia_acotado"
TINF_CUENTA = "tests/test_fase2_series.py::test_st_inf_la_busqueda_del_n_minimo_empieza_en_la_aproximacion"   # r02 (H-02)
T102 = ["tests/test_t102_filtro.py::" + n for n in ("test_textos_largos_en_tiempo_lineal", "test_r04_muchos_espacios_en_tiempo_lineal",
        "test_r05_h37_sufijo_en_tiempo_lineal", "test_r06_h45_marcador_y_muchos_espacios_en_tiempo_lineal")]   # r02 (H-04)

# (nombre, fichero, [(antes, después)], prueba). Los bloques de re-escaneo son la centésima parte del texto más corto de
# la prueba (unas 50 veces el coste lineal a ese tamaño); en las de razón, la del texto largo.
M = [
    ("M01 R8 re-escanea el prefijo (bloque 15 600)", CON, r8_reescaneo(15_600), T123),
    ("M02 R8 re-escanea el prefijo (bloque 1 200)", CON, r8_reescaneo(1_200), T92),
    ("M03 R8 re-escanea el prefijo (bloque 1 000)", CON, r8_reescaneo(1_000), T103),
    ("M04 R8 re-escanea el prefijo (bloque 2 000)", CON, r8_reescaneo(2_000), T130),
    ("M05 H-56: cada nivel vuelve a serializar lo de debajo (profundidad × tamaño)", LLM,
     [("        for d in _diccionarios_de_arriba(valor):\n            try:\n"
       "                if secretos_en_texto(json.dumps(d, ensure_ascii=False, default=str)):",
       "        _todos, _p = [], list(_diccionarios_de_arriba(valor))\n"
       "        while _p:\n"
       "            _d = _p.pop()\n"
       "            _todos.append(_d)\n"
       "            _p.extend(v for v in _d.values() if isinstance(v, dict))\n"
       "        for d in _todos:\n            try:\n"
       "                if secretos_en_texto(json.dumps(d, ensure_ascii=False, default=str)):")], T113A),
    ("M06 el camino de la lista como lista (profundidad²)", LLM,
     [("    camino: set[int] = set()\n", "    camino: list[int] = []\n"),
      ("            camino.discard(id(x))\n", "            camino.remove(id(x))\n"),
      ("            camino.add(id(x))\n", "            camino.append(id(x))\n")], T113B),
    ("M07 H-01: cada contenedor tantas veces como caminos (exponencial)", LLM,
     [("            if id(x) in vistos:\n                continue\n            vistos.add(id(x))\n"
       "            hay_conjuntos", "            hay_conjuntos")], T113C),
    ("M08 G3-MET-13 re-comprueba el prefijo (bloque 2 400)", HT9, ht09_reescaneo(2_400), T165),
    ("M09 H-03 de T-144: un par solo sale cuando salen todos (n²·T)", FRB,
     [("            vivos = vivos[~(distinta[vivos] & (lo[vivos] > hi[vivos]))]\n",
       "            if (distinta[vivos] & (lo[vivos] > hi[vivos])).all():\n                vivos = vivos[:0]\n")], T144),
    ("M10 SIM-MC suma de nuevo todas las innovaciones en cada paso (horizonte² × trayectorias)", RIE,
     [("    res: dict[int, np.ndarray] = {}\n", "    res: dict[int, np.ndarray] = {}\n    _incs: list = []\n"),
      ("            x = x + din[\"mu\"] + din[\"sigma\"] * normales()\n",
       "            _incs.append(din[\"mu\"] + din[\"sigma\"] * normales())\n            x = np.sum(_incs, axis=0)\n")], TMC),
    ("M11 TEM-DIFF-001: la cota de B se comprueba después del bootstrap", SER,
     [("        p[\"B\"] = _entero(p[\"B\"], f\"{F}: B\", 1, u[\"B_maximo\"])\n",
       "        p[\"B_pedido\"], p[\"B\"] = p[\"B\"], u[\"B_maximo\"]\n"),
      ("    if not sims:\n        raise ErrorFicha(f\"{F}: CONVERGENCIA: ninguna réplica del bootstrap converge\")\n",
       "    _entero(p.get(\"B_pedido\", p[\"B\"]), f\"{F}: B\", 1, UMBRALES[F][\"B_maximo\"])\n"
       "    if not sims:\n        raise ErrorFicha(f\"{F}: CONVERGENCIA: ninguna réplica del bootstrap converge\")\n")], TCOTA),
    ("M12 ST-INF-001: búsqueda desde 2 que en cada paso vuelve a mirar los anteriores (cota²)", SER,
     [("        m = max(2, math.ceil(aprox)) if aprox <= tope else tope + 1\n", "        m = 2\n"),
      ("        while m <= tope and pm(m) < objetivo:\n",
       "        while m <= tope and all(pm(k) < objetivo for k in range(2, m + 1)):\n")], (TINF_CUENTA, TINF)),
    ("M13 ST-INF-001: búsqueda lineal desde 2, sin la aproximación (r02, H-02: la mata el recuento)", SER,
     [("        m = max(2, math.ceil(aprox)) if aprox <= tope else tope + 1\n", "        m = 2\n")], (TINF_CUENTA, TINF)),
    # r02 (QA r01, H-01): lineal + cuadrático con el término cuadrático pequeño, que el tope de 16 dejaba vivo
    ("M14 G3-MET-13 re-comprueba el prefijo (bloque 120 000)", HT9, ht09_reescaneo(120_000), T165),
    ("M15 G3-MET-13 re-comprueba el prefijo (bloque 160 000)", HT9, ht09_reescaneo(160_000), T165),
    # r02 (QA r01, H-04): las cuatro de T-102, con los mutantes de retroceso Q4, Q1 y Q2 de la QA r01 de T-168
    ("M16 texto_prohibido con retroceso ((?:\\w+[ ,]+)+;)", V6, [(F_TEXTO, F_TEXTO + "    re.search(r\"(?:\\w+[ ,]+)+;\", t) if isinstance(t, str) else None\n")], T102[0]),
    ("M17 frase_prohibida con retroceso en los blancos del final ([ \\t]+$)", V6, [(F_FRASE, F_FRASE + "    re.search(r\"[ \\t]+$\", t)\n")], T102[1]),
    ("M18 frase_prohibida con retroceso en el sufijo ((?:[A-Z]\\.)+[a-z])", V6, [(F_FRASE, F_FRASE + "    re.search(r\"(?:[A-Z]\\.)+[a-z]\", t)\n")], T102[2]),
    ("M19 frase_prohibida con retroceso en los blancos del final, contra r06", V6, [(F_FRASE, F_FRASE + "    re.search(r\"[ \\t]+$\", t)\n")], T102[3]),
]
ORIGINALES = [T123, T92, T103, T130, T113A, T113B, T113C, T165, T144, TMC, TCOTA, TINF, TINF_CUENTA, *T102]


def pytest(nodo: str | tuple[str, ...]) -> tuple[bool, str, float]:
    t0 = time.monotonic()
    nodos = [nodo] if isinstance(nodo, str) else list(nodo)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *nodos],
                       cwd=EJ, capture_output=True, text=True, check=False)
    motivo = next((ln.strip() for ln in r.stdout.splitlines() if ln.lstrip().startswith("E ")), "")
    return r.returncode == 0, motivo[:160], time.monotonic() - t0


def main() -> int:
    elegidos = [a for a in sys.argv[2:] if not a.startswith("--")]
    malos = 0
    if "--originales" in sys.argv:
        for nodo in ORIGINALES:
            ok, motivo, seg = pytest(nodo)
            malos += not ok
            print(f"ORIGINAL {nodo.split('::')[1]}: {'PASA' if ok else 'FALLA ' + motivo} ({seg:.0f} s de reloj)", flush=True)
    for nombre, f, cambios, nodo in M:
        if elegidos and nombre.split()[0] not in elegidos:
            continue
        p = EJ / f
        orig = p.read_text(encoding="utf-8")
        mut = orig
        for a, b in cambios:
            assert mut.count(a) == 1, (nombre, a[:60], mut.count(a))
            mut = mut.replace(a, b)
        p.write_text(mut, encoding="utf-8")
        try:
            ok, motivo, seg = pytest(nodo)
        finally:
            p.write_text(orig, encoding="utf-8")
        malos += ok
        print(f"{nombre}: {'VIVO' if ok else 'MUERTO'} ({seg:.0f} s de reloj) {motivo}", flush=True)
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
