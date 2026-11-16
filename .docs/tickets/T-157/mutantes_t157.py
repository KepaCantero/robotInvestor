"""Mutantes de T-157: cada uno quita una protección del verificador y la prueba citada debe fallar; el nulo es el control.
Se ejecuta desde bloque_a/11_Ejecutor: ../../.venv/bin/python ../../.docs/tickets/T-157/mutantes_t157.py"""
import subprocess, sys
MUT = {
  "nulo (control)": ("pass", "test_a_contratos"),
  "lee 99_Historico": ("vi.PREFIJO_HISTORICO = 'ZZZ'", "test_no_lee_historico_ni_ejecutor"),
  "sin contextos (r02: _contexto_r)": ("vi._contexto_r = lambda x, c: None", "test_contextos_que_no_son_citas"),
  "sin ID_DISTINTO": ("vi._mas_parecido = lambda x, c: None", "test_d_fichas_cuatro_clases"),
  "sin validar esquema": ("vi.validar_informe = lambda i: None", "test_informe_que_no_valida_no_se_escribe"),
  "Doc 0 sin unicidad": ("_u = vi._unico\nvi._unico = lambda r, c, p, q: sorted(x for x in (r/c).iterdir() if x.is_file() and p.match(vi._nfc(x.name)))[0]", "test_dos_documentos_0_fallan_cerrado"),
  "canal_permitido ignorado": ("import dataclasses\n_v = vi.verificar\nvi.verificar = lambda r, c=None: _v(r, dataclasses.replace(c, canales_admitidos=c.canales) if c else c)", "test_a_contratos"),
  # r02: las reglas nuevas de la QA r01 (H-02, H-03, H-05, H-06)
  "r02 cualquier campo JSON declara símbolo": ("import re\nvi.RE_SIMBOLO_SERIE = re.compile(r'\"(\\w+)\"\\s*:\\s*\"([A-Z][^\":]*)')", "test_r02_contextos_no_excusan_de_mas"),
  "r02 «JEL» excusa la línea entera": ("vi._en_lista_jel = lambda c: 'JEL' in c.texto", "test_r02_contextos_no_excusan_de_mas"),
  "r02 la fórmula excusa también las R": ("_r = vi._contexto_r\nvi._contexto_r = lambda x, c: 'formula' if vi._en_formula(c) else _r(x, c)", "test_r02_contextos_no_excusan_de_mas"),
  "r02 sin normalizar guiones": ("vi.GUIONES = {}", "test_r02_contextos_no_excusan_de_mas"),
  "r02 menciones con mayúsculas": ("import re\nvi.RE_MENCION_CATALOGO = re.compile(vi.RE_MENCION_CATALOGO.pattern)", "test_r02_contextos_no_excusan_de_mas"),
  "r02 sin familias desconocidas": ("import re\nvi.RE_FORMA_FICHA = re.compile(r'(?!x)x')", "test_r02_contextos_no_excusan_de_mas"),
  "r02 destinos sin comprobar": ("vi._escribir_todo = lambda s: [r.write_text(t, encoding='utf-8') for r, t in s]", "test_r02_destino_imposible_sale_2_y_no_escribe_nada"),
}
for nombre, (parche, prueba) in MUT.items():
    conf = f"import bloque_a.herramientas.verificador_ids as vi\n{parche}\n"
    open("tests/conftest_mutante.py", "w").write(conf)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "tests.conftest_mutante",
                        f"tests/test_t157_verificador_ids.py::{prueba}"], capture_output=True, text=True)
    print(f"{nombre:42s} -> {'MATADO' if r.returncode else 'VIVO'} ({prueba})")
import os; os.remove("tests/conftest_mutante.py")
