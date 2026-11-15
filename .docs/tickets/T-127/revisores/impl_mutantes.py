"""Mutantes de las correcciones de T-127. Se aplican en una copia desechable del ejecutor (DESTINO/11_Ejecutor, con el
Catálogo al lado) y se ejecutan `tests/test_t127_hallazgos.py` y `tests/test_t119_r02.py` (-x). MUERTO = alguna prueba
falla.
Uso: python impl_mutantes.py ORIGEN_EJECUTOR DESTINO [--solo ID,ID]   (DESTINO: carpeta desechable fuera del repo, cuya
ruta contenga «t127_mut»; sin --solo se borra al acabar)"""
import shutil
import subprocess
import sys
from pathlib import Path

ORIGEN = Path(sys.argv[1]).resolve()
BASE = Path(sys.argv[2]).resolve()
assert "t127_mut" in str(BASE) and not (BASE / ".git").exists() and BASE != ORIGEN, "DESTINO debe ser una carpeta desechable"
COPIA = BASE / "11_Ejecutor"
SOLO = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
PY = sys.executable
PRUEBAS = ["tests/test_t127_hallazgos.py", "tests/test_t119_r02.py"]
P2, SV, OP, TC, FD, CF = ("bloque_a/motor/fichas_p2.py", "bloque_a/motor/servicio.py", "bloque_a/motor/operaciones.py",
                          "bloque_a/motor/fichas_tcv.py", "bloque_a/motor/fichas_fon_der.py", "bloque_a/configuracion.py")

if BASE.exists():
    shutil.rmtree(BASE)
BASE.mkdir(parents=True)
shutil.copytree(ORIGEN, COPIA, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
shutil.copytree(ORIGEN.parent / "04_Motor_conocimiento_y_catalogo", BASE / "04_Motor_conocimiento_y_catalogo")

M = [
    # H-10 · casi clones
    ("K01", P2, '    "tolerancia_clon": 0.01,', '    "tolerancia_clon": 0.0,', "clones solo exactos (la regla de la r02)"),
    ("K02", P2, "        cerca &= np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(a[:, None], a[None, :])",
     "        cerca &= np.abs(x[:, None] - x[None, :]) < tol * np.maximum(a[:, None], a[None, :])", "tolerancia estricta"),
    ("K03", P2, "        cerca &= np.abs(x[:, None] - x[None, :]) <= tol * np.maximum(a[:, None], a[None, :])",
     "        cerca &= np.abs(x[:, None] - x[None, :]) <= tol * np.minimum(a[:, None], a[None, :])", "tolerancia por el menor"),
    ("K04", P2, "        cerca &= nulo[:, None] == nulo[None, :]\n", "", "un dato ausente igual a un cero"),
    ("K05", P2, "    repetidos = len(firmas) - _grupos_casi_iguales(firmas, tol)", "    repetidos = len(firmas) - len(set(firmas))",
     "vuelve la comparación exacta"),
    # H-10 · dominancia
    ("D01", P2, '    "peso_maximo_componente": 0.95,', '    "peso_maximo_componente": 1.0,', "sin dominancia"),
    ("D02", P2, "        if peso > peso_maximo:", "        if peso >= peso_maximo:", "dominancia en el borde"),
    ("D03", P2, '                  "ffo": col["ffo"]}, f"{F}: componentes", u["peso_maximo_componente"])',
     '                  }, f"{F}: componentes", u["peso_maximo_componente"])', "REI-LEV sin la base del FFO"),
    ("D04", P2, '_sin_dominio({"gav": col["gav"], "deuda": col["deuda"], "ebitda": col["ebitda"], "gastos_financieros": col["gf"],',
     '_sin_dominio({"gav": col["gav"], "deuda": col["deuda"],', "REI-LEV sin EBITDA ni gastos financieros"),
    ("D05", P2, '    _sin_dominio({"deuda": deudas}, f"{F}: componentes", u["peso_maximo_componente"])', "    pass",
     "FIR-CRED sin dominancia"),
    ("D06", P2, "    if not red:   # T-127 (H-10): bases", "    if True:   # T-127 (H-10): bases", "la red también con dominancia"),
    ("D07", P2, '        _sin_dominio({"capitalizacion_circulante": cm, "fdv": fdv}, f"{F}: tokens", u["peso_maximo_componente"])',
     "        pass", "CHR-TOKEN sin dominancia"),
    ("D08", P2, "        a = np.abs(np.asarray(x, dtype=float))", "        a = np.asarray(x, dtype=float)", "dominancia sin valor absoluto"),
    # H-10 · estadísticos de orden
    ("O01", P2, '    "componentes_minimos_orden": len(ESTADISTICOS_ORDEN) + 2,', '    "componentes_minimos_orden": len(ESTADISTICOS_ORDEN) + 1,',
     "orden desde 6"),
    ("O02", P2, '    if len(x) >= u["componentes_minimos_orden"]:', '    if len(x) > u["componentes_minimos_orden"]:', "orden desde 8"),
    ("O03", P2, '    if _orden(a["gav"], u, sin_orden, "la dispersión de los componentes") is not None:   # T-127 (H-10)',
     "    if True:", "REI-LEV con dispersión siempre"),
    ("O04", P2, '    if not red and _orden(a_cm, u, sin_orden, "la dispersión de los tokens") is not None:   # T-127 (H-10)',
     "    if not red:", "CHR-TOKEN con dispersión siempre"),
    ("O05", P2, '            "holgura_ltv_pp": _orden(np.array(holg_ltv), u, sin_orden, "las holguras frente a covenants"),',
     '            "holgura_ltv_pp": _distribucion(np.array(holg_ltv)),', "holgura del LTV con orden siempre"),
    ("O06", P2, '"vencimientos_24m_pct": _distribucion(a["venc"] / a["deuda"] * PCT)}\n    _limitacion_orden(sin_orden, u, lim)',
     '"vencimientos_24m_pct": _distribucion(a["venc"] / a["deuda"] * PCT)}', "REI-LEV no lo declara"),
    # H-10 · subconjuntos
    ("S01", P2, '    if 0 < len(holg_ltv) < u["componentes_minimos"]:', '    if 0 < len(holg_ltv) < 2:', "covenants desde 2"),
    ("S02", P2, '        if not red and (len(pares) < u["tokens_minimos_sector"]', "        if not red and (len(pares) < 1",
     "staking de un token (EQUIVALENTE mientras peso_maximo_componente < 1: un token es el 100 % de su subconjunto)"),
    ("S03", P2, '                        or max(c for c, _ in pares) / peso > u["peso_maximo_componente"]):',
     "                        or False):", "staking dominado"),
    # H-10 · red propia
    ("R01", P2, "        if nativo is None or not isinstance(id_token, str) or id_token.strip().upper() != nativo:",
     "        if nativo is None:", "cualquier token como red"),
    ("R02", P2, "        if nativo is None or not isinstance(id_token, str) or id_token.strip().upper() != nativo:",
     "        if False:", "cualquier ámbito como red (la regla de la r02)"),
    ("R03", P2, '        nativo = u["redes_propias"].get(ambito.strip().casefold())', '        nativo = u["redes_propias"].get(ambito)',
     "nombre de la red sin normalizar"),
    # H-11
    ("C01", SV, '        return {"l" if type(x) is list else "t": [_marcado(v) for v in x]}', '        return {"l": [_marcado(v) for v in x]}',
     "tupla igual que lista"),
    ("C02", SV, "        pares = [[_marcado(k), _marcado(v)] for k, v in x.items()]", "        pares = [[str(k), _marcado(v)] for k, v in x.items()]",
     "clave entera igual que su texto"),
    ("C03", SV, "        return hashlib.sha256(json.dumps(_marcado(partes), sort_keys=True",
     "        return hashlib.sha256(json.dumps(partes, default=_con_tipo, sort_keys=True", "vuelve la firma de la r02"),
    # H-07
    ("A01", SV, '    return any(r == seccion or r.startswith(f"{seccion}.") for r in respaldos)', "    return False",
     "nunca toma nada del fichero"),
    ("A02", SV, '    return any(r == seccion or r.startswith(f"{seccion}.") for r in respaldos)', "    return True",
     "siempre toma algo del fichero (la regla de T-121 sin _cubre)"),
    ("A03", CF, "        if callable(anotar):\n            anotar(ruta_clave)", "        pass", "parametro no apunta"),
    ("A04", SV, '    return any(r == seccion or r.startswith(f"{seccion}.") for r in respaldos)',
     "    return any(r.startswith(seccion) for r in respaldos)", "prefijo sin el punto"),
    # H-08
    ("F01", OP, "    return t if t.tz is None else t.tz_convert(None)", "    return t if t.tz is None else t.tz_localize(None)",
     "día local en vez de UTC"),
    ("F02", TC, "        return d if len(x.strip()) == 10 else dia(pd.Timestamp(x.strip())).date()", "        return d",
     "TCV: los diez primeros caracteres"),
    ("F03", FD, "    return op.sin_zona(t)\n", "    return t\n", "FON: zonas sin convertir"),
    ("F04", TC, "        return dia(x).date()\n    if isinstance(x, datetime):", "        return x.date()\n    if isinstance(x, datetime):",
     "TCV: Timestamp con su día local"),
    # H-09
    ("N01", FD, '        fnav = op.dia(_fecha(mb["fecha_nav"], F, "fecha_nav"))', '        fnav = _fecha(mb["fecha_nav"], F, "fecha_nav")',
     "FON-DISC: NAV con hora"),
]
vivos = []
for mid, mod, a, b, desc in M:
    if SOLO and mid not in SOLO:
        continue
    ruta = COPIA / mod
    orig = ruta.read_text(encoding="utf-8")
    if orig.count(a) != 1:
        print(f"{mid}: el texto aparece {orig.count(a)} veces; no se aplica · {desc}", flush=True)
        vivos.append(f"{mid}?")
        continue
    ruta.write_text(orig.replace(a, b), encoding="utf-8")
    try:
        r = subprocess.run([PY, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *PRUEBAS], cwd=COPIA,
                           capture_output=True, text=True, timeout=1800, check=False)
        muerto = r.returncode != 0
        fallo = next((ln for ln in r.stdout.splitlines() if ln.startswith(("FAILED", "ERROR"))), "")
    finally:
        ruta.write_text(orig, encoding="utf-8")
    print(f"{mid} {'muere' if muerto else 'VIVE '} · {desc} · {fallo[:140]}", flush=True)
    if not muerto:
        vivos.append(mid)
print(f"\n{len([m for m in M if not SOLO or m[0] in SOLO])} mutantes; vivos: {', '.join(vivos) or 'ninguno'}")
if not SOLO:
    shutil.rmtree(BASE)
