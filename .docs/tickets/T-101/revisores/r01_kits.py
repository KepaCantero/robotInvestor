"""QA r01 de T-101 · El kit no pierde ni inventa contenido en los doce perfiles (CA-2).

Para cada Analista compara el prompt V5.0 congelado con lo que recibe en la V6 (núcleo + interfaz + kit), sección a
sección y también la cabecera (lo anterior a la §1), y comprueba que el núcleo es idéntico para los doce.

Uso: python -I r01_kits.py <raiz_repo>
"""
import re
import sys
from pathlib import Path

raiz = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(raiz / "bloque_a" / "11_Ejecutor"))
from bloque_a.configuracion import cargar_config  # noqa: E402
from bloque_a.prompts import (  # noqa: E402
    ANALISTAS_TIPO,
    CatalogoPrompts,
    _sin_comentario,
    _sustituir,
    identidad,
    kit,
    secciones,
)

fallos = []
cfg = cargar_config(extra={"diseno": "v6"})
c = CatalogoPrompts(cfg)
nucleo = c.nucleo()
marco = c._cache["_marco"]
_, sec_nucleo = secciones(nucleo)
_, sec_marco = secciones(_sin_comentario(marco))
nucleos = set()
print(f"{'agente':6} {'ide':28} {'kit_sec':18} {'perdidas(ninguna)':18} cabecera_perdida")
for ag in sorted(ANALISTAS_TIPO):
    esp = c.texto(ag)
    ide = identidad(esp)
    if None in ide.values():
        fallos.append(f"{ag}: identidad incompleta {ide}")
    sistema = "".join(b["text"] for b in c.system(ag, cache=False))
    nucleos.add("".join(b["text"] for b in c.system(ag, cache=False)[:2]))
    cab, se = secciones(esp)
    _, sm = secciones(_sustituir(_sin_comentario(marco), ide))
    _, sk_comp = secciones(kit(esp, marco, "completa"))
    _, sk = secciones(c.kit(ag))
    # 1) cada sección V5.0 está, literal, en el kit o (sustituida) en el marco del núcleo
    perdidas = []
    for n, txt in se.items():
        en_kit = sk.get(n, "").strip() == txt.strip()
        en_marco = sm.get(n, "").strip() == txt.strip() and n in sec_nucleo
        if not (en_kit or en_marco):
            perdidas.append(n)
        if not (sk_comp.get(n, "").strip() == txt.strip() or en_marco):
            fallos.append(f"{ag}: §{n} se pierde incluso con el kit completo")
    # 2) el núcleo no trae secciones que el prompt V5.0 del perfil no tenga (no inventa)
    sobran = sorted(set(sec_nucleo) - set(se), key=int)
    if sobran:
        fallos.append(f"{ag}: el núcleo trae secciones que su prompt V5.0 no tiene: {sobran}")
    # 3) secciones del kit que no son texto literal del V5.0
    for n, txt in sk_comp.items():
        if txt.strip() != se.get(n, "").strip():
            fallos.append(f"{ag}: §{n} del kit no es literal del V5.0")
    # 4) la cabecera del V5.0 (antes de la §1): ¿llega algo de ella al system V6?
    lineas = [ln.strip() for ln in cab.splitlines() if ln.strip() and not ln.startswith("# ")]
    perdida_cab = [ln for ln in lineas if ln not in sistema]
    print(f"{ag:6} {str(ide['codigo'])+'/'+str(ide['perfil']):28} {','.join(sorted(sk, key=int)):18} {','.join(perdidas) or '-':18} "
          f"{len(perdida_cab)} línea(s): {perdida_cab[0][:90] + '…' if perdida_cab else ''}")
    if [p for p in perdidas if p != "10"]:
        fallos.append(f"{ag}: con base_conocimientos=ninguna se pierden secciones distintas de la §10: {perdidas}")
    # 5) duplicados: secciones del núcleo que el kit vuelve a traer (manda la del kit)
    dup = sorted(set(sk) & set(sec_nucleo), key=int)
    if dup:
        print(f"       secciones duplicadas núcleo/kit (manda el kit): {dup}")
if len(nucleos) != 1:
    fallos.append(f"el núcleo no es idéntico para los doce ({len(nucleos)} variantes)")
if "{{" in nucleo:
    fallos.append("quedan marcadores en el núcleo")
print("\nFALLOS:" if fallos else "\nSin fallos de secciones.")
for f in fallos:
    print(" -", f)
sys.exit(1 if fallos else 0)
