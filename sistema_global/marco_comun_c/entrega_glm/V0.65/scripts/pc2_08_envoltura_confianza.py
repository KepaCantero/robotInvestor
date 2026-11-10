"""PC2-08 — la envoltura común de la §5 pide confianza e incertidumbre que los contratos no llevan.

La Constitución (§5, «Sobre de mensaje (obligatorio en todo contrato)») fija la envoltura de todo
contrato con estos campos: event_id, correlation_id, expediente_id, producer, consumer, tipo_mensaje,
version_esquema, emitido_en, valid_until, data_refs, payload, confianza, incertidumbre y
resultado_politica.

El código: los cinco contratos con envoltura común plena (CT-G-01 0.2.0, CT-G-02 0.2.0, CT-G-03 0.2.0,
CT-G-08 0.3.0 y CT-G-14 0.2.0) llevan la envoltura, pero CT-G-02 solo lleva incertidumbre (la confianza
está en su capa 3 del payload) y CT-G-01, CT-G-03, CT-G-08 y CT-G-14 no llevan ni confianza ni
incertidumbre; CT-G-03 y CT-G-14 tampoco llevan resultado_politica. El registro de contratos
(esquemas/registro_contratos.json) marca todas como «envoltura: COMPLETA» con un criterio propio, así que
la §5 y el registro dicen cosas distintas.

Uso: python3 entrega_glm/V0.65/scripts/pc2_08_envoltura_confianza.py   (desde la carpeta marcoC)
Imprime FALLA mientras la envoltura vigente no coincida con la §5; OK cuando coincidan.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "validador"))

CONTRATOS = ("ct-g-01_0.2.0.schema.json", "ct-g-02_0.2.0.schema.json", "ct-g-03_0.2.0.schema.json",
             "ct-g-08_0.3.0.schema.json", "ct-g-14_0.2.0.schema.json")
ENVOLTURA_5 = {"event_id", "correlation_id", "expediente_id", "producer", "consumer", "tipo_mensaje",
               "version_esquema", "emitido_en", "valid_until", "data_refs", "payload", "confianza",
               "incertidumbre", "resultado_politica"}

mal = []
for nombre in CONTRATOS:
    esq = json.loads((RAIZ / "esquemas" / nombre).read_text(encoding="utf-8"))
    raiz = set(esq.get("properties", {}))
    faltan = sorted(ENVOLTURA_5 - raiz)
    sobran = sorted(raiz - ENVOLTURA_5)
    print(f"INFO   {nombre}: faltan {faltan if faltan else 'nada'} de la §5; fuera de la §5: {sobran if sobran else 'nada'}")
    if faltan:
        mal_faltan = faltan
        # la divergencia existe: no hacemos nada (mal solo se llena si TODO cuadra)
    else:
        mal.append(f"{nombre} ya lleva la envoltura completa de la §5")

registro = json.loads((RAIZ / "esquemas" / "registro_contratos.json").read_text(encoding="utf-8"))
marcadas = [c["tipo"] for c in registro["contratos"] if isinstance(c, dict) and c.get("envoltura") == "COMPLETA"]
print(f"INFO   registro_contratos.json: {len(marcadas)} contratos marcados «envoltura: COMPLETA» -> {marcadas}")

if len(mal) == len(CONTRATOS):
    print("OK     la divergencia está resuelta:")
    for m in mal:
        print("       -", m)
    print("RESULTADO PC2-08: OK")
else:
    print("FALLA  la envoltura de los contratos vigentes no coincide con la §5: confianza e incertidumbre")
    print("       no viajan como campos (CT-G-02 solo incertidumbre, con la confianza en su capa 3), y")
    print("       CT-G-03 y CT-G-14 no llevan resultado_politica; el registro las marca «COMPLETA» igualmente")
    print("RESULTADO PC2-08: FALLA")
