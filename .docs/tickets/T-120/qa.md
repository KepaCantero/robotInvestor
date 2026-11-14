# T-120 · QA independiente

- **Revisor:** un revisor nuevo sin el contexto de la implementación (subagente de Claude; la implementación es de Claude). Retoma la sesión de otro revisor que se cortó después de escribir `r01_01` y `r01_02` y antes de escribir aquí · **Ronda:** r01 · 2026-11-14

Orden de lectura: `README.md` → el diff de `6b9f916` en `contratos.py`, `evaluador.py`, `por_defecto.yaml` y `tests/test_t120_r8_y_lecciones.py` → solo al final `analisis-tecnico.md` y `pruebas.md`.

## Reproducción desde limpio

Copia propia: un `git worktree` con HEAD separado en `b4601c3` (contiene `6b9f916`), con el entorno del proyecto (`/home/user/robotinvestor/.venv`, Python 3.12). Máquina de 4 núcleos compartida con la batería de mutantes de T-113: los tiempos llevan ese margen. «Ejecutado» quiere decir que la evidencia es una salida mía; «leído», que lo deduzco del código.

```
cd bloque_a/11_Ejecutor
python -m pytest -q -p no:cacheprovider tests/test_t113_deuda.py tests/test_t120_r8_y_lecciones.py     # 122 passed en 44,6 s (16 de T-120)
python -m pytest -q -p no:cacheprovider tests/test_t102_filtro.py tests/test_t101_v6.py tests/test_unitarias.py \
       tests/test_t87_contratos.py tests/test_fase3_goldens.py                                         # 464 passed en 251,7 s
cd ../..
python tools/corpus_integridad.py; python tools/refs_vivas.py; python tools/secrets_scan.py; python tools/nfc_check.py   # los cuatro, código 0
ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l         # 2902 = cuota
mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l                                  # 109 = cuota
```

**No lanzados, por indicación de quien encarga la QA:** el gate completo (pasó 12/12 al subir `6b9f916`) y la suite completa de A (media hora; pasó en ese gate).

### Scripts (`revisores/`)

Desde `bloque_a/11_Ejecutor` de la copia, con `QA_TMP=<carpeta> python ../../.docs/tickets/T-120/revisores/<script>`.

| Script | Qué ataca | Resultado |
| --- | --- | --- |
| `r01_01_iban_banco.py` (del revisor anterior) | 69 textos: 22 IBAN que deben marcarse (junto, espacios, puntos, guiones, mezclados, pegado a «IBAN:», entre comillas, en JSON y en JSON dos veces, escapados, en bytes, dos seguidos…), 18 que no (ISIN, NIF, CIF, ES50, cuatro grupos, último grupo de tres, una cifra de más, importes, años, fechas, número de serie, IBAN alemán, palabra acabada en «ES», teléfono…) y 29 observaciones; diferencial con el patrón de `6b9f916^`; 200 000 textos al azar; y el camino real con cinco formas por CT-04 (comentario y anidado), CT-03 (pregunta y contexto) y CT-23 (envío, respuesta, entrante) | **0 fallos.** 22/22 marcados (y por `contenido_sensible`), 18/18 sin marcar, nada que antes se marcara deja de marcarse; 0 falsos positivos al azar de otra regla; las 35 llamadas del camino real se rechazan con una incidencia SEGURIDAD cada una y el dato no queda en ningún archivo |
| `r01_02_lecciones_config.py` (del revisor anterior) | `lecciones_por_encargo` con 20 valores raros, configuraciones parciales, el argumento explícito y el orden | ver CA-4 y H-02 |
| `r01_03_iban_fuera_de_lo_declarado.py` (mío) | formas corrientes del IBAN fuera de lo declarado (espacio duro, tabulador, dos espacios, formato CCC impreso, minúsculas) por CT-04, CT-03 y CT-23 | 12 de 15 admitidas y guardadas: H-01 |
| `../../T-113/revisores/r02_04_mutantes.py` (F1–F6, G1–G2) | ocho mutantes de T-120 | ver «Mutantes» |

Coste del patrón (ejecutado): textos de 1 a 1,6 MB con «ES12» y cifras repetidas, 0,15–0,23 s; no hay retroceso catastrófico (cuantificadores acotados).

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 IBAN junto y con espacio, punto o guion, también en listas y diccionarios | **sí** (para los separadores declarados) | Ejecutado, `r01_01`: 22/22, también mezclados, en JSON, en bytes y en `[{"a": (iban,)}]`. Fuera de lo declarado: H-01 |
| CA-2 un CT-04 con solo un IBAN con espacios se rechaza y no queda en ningún archivo | **sí** | Ejecutado, `r01_01`: rechazado, +1 incidencia SEGURIDAD sin el valor, ningún archivo de la carpeta del bloque contiene «2100…0418». Igual en CT-04 anidado, CT-03 (pregunta y contexto) y CT-23 (envío, respuesta y entrante), y con puntos, guiones, junto y mezclado |
| CA-3 los diez textos legítimos no se marcan | **sí** | Ejecutado: la prueba del paquete (10 casos) pasa, y mi banco añade 8 más sin marcar. Observación: «ES24 2021 2022 2023 2024 2025» (ES, dos cifras y cinco años) se marca; es la forma de un IBAN y es improbable en un mensaje: no lo cuento |
| CA-4 el máximo es el de la configuración, también con configuración parcial, y cambia al cambiarla | **sí** | Ejecutado, `r01_02`: 10 → 10, 4 → 4, 1 → 1, 0 → 0; sección `aprendizaje` vacía, `None` o configuración `{}` → 10 (el de `por_defecto.yaml`); `None` en la clave → `KeyError` (falla cerrado); el argumento explícito manda (12, 0, 100); con 4 salen las cuatro «estadistica». Los valores raros: H-02 |
| CA-5 suites de contratos, secretos y goldens en verde; gate 12/12 | **sí, por partes** | Ejecutado: `test_t87_contratos`, `test_unitarias`, `test_fase3_goldens` y `test_t120_r8_y_lecciones` en verde; secretos, corpus, refs y NFC en verde; ruff 2902 y mypy 109 (las cuotas). Leído: `RE_SECRETO` no está en las tablas congeladas y `test_fase3_goldens` pasa sin re-congelar. El gate completo no lo he lanzado (consta 12/12 al subir el commit) |

## Mutantes

`python .docs/tickets/T-113/revisores/r02_04_mutantes.py <copia> <carpeta> todos` (F1–F6 y G1–G2), uno a uno en copias desechables, borradas al acabar. **7 de 8 mueren con `test_t120_r8_y_lecciones.py`:** F1 (solo junto), F2 (sin punto ni guion), F3 (varios separadores seguidos: lo mata el caso legítimo «con dos espacios»), F4 (sin límite de palabra al final), F5 (cuatro grupos bastan), G1 (el literal 10 vuelve) y G2 (el argumento explícito deja de mandar). **F6** (separador también tras «ES») sobrevive al ticket y a 97 vecinas: es más estricto, no deshace nada.

## Hallazgos

Órdenes desde `bloque_a/11_Ejecutor` de la copia, con `R=../../.docs/tickets/T-120/revisores`.

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `QA_TMP=<carpeta> python $R/r01_03_iban_fuera_de_lo_declarado.py`. A mano: `secretos_en_texto(" ".join(["ES91","2100","0418","4502","0005","1332"]))` → vacío | **Esperado:** un IBAN español que se escribe como se suele escribir se rechaza, o la forma que no se cubre está declarada como límite. **Obtenido:** con espacio duro (U+00A0, el que trae un IBAN copiado de una web o de un PDF) y en el formato impreso de la cuenta (`ES91 2100 0418 45 0200051332`, entidad-oficina-DC-cuenta) el mensaje se admite por CT-04, CT-03 y CT-23 y el IBAN queda en `F5_historial_analisis.jsonl` (y en `cache_resultados.jsonl` en CT-03 y CT-23): 6 de 6. Ninguna de las dos formas está declarada: el README dice «espacio, punto o guion» y sus límites («No entra») son tarjetas y otros países. Con dos espacios y en minúsculas pasa lo mismo (6 de 6 más), pero esas dos sí están declaradas (la primera, como texto legítimo de CA-3, lo que es discutible: es un IBAN). Con tabulador se rechaza (por el camino de `RE_ESCAPES`) | Normalizar antes del patrón los espacios Unicode (`\s` con `re.UNICODE`, U+00A0, U+202F) y admitir entre cifras hasta dos separadores, por ejemplo `\bES\d{2}(?:[\s.\-]{0,2}\d){20}\b` (cubre grupos de cuatro, el formato impreso y dos espacios); o declarar estas formas como límite en el README y en la deuda. Prueba con las tres formas | abierto |
| H-02 | baja | `QA_TMP=<carpeta> python $R/r01_02_lecciones_config.py` | **Esperado:** un máximo mal configurado falla cerrado (error al cargar o al usarlo), como `None`. **Obtenido:** con `-1` salen 13 de 14 lecciones y con `-3`, 11 (`lst[:max_n]` con un negativo quita por el final): más que el máximo del 12.3 del Documento 0. `1e3` y `10**30` dan todas (sin tope); `2.7` → 2, `True` → 1, `"4"` → 4, `False` → 0, en silencio. Sí fallan (con excepción): `"diez"`, `""`, NaN, infinito, lista, dict. Hace falta un YAML mal escrito por el operador; no llega desde un mensaje | Validar el parámetro: entero (no `bool`) y `>= 0` (y, si se quiere, `<=` el del Documento 0), o `ValueError` al usarlo. Una prueba con `-1` | abierto |

Observaciones, sin ID: **O-1** el mismo patrón antiguo sigue en el Forex (declarado en «No entra»). **O-2** `Evaluador(..., cfg=None).lecciones_vigentes` da `AttributeError` antes de llegar al parámetro: es anterior a T-120 y ningún camino real pasa `None`.

## Sin comprobar

- El gate completo y la suite completa de A (no lanzados, ver arriba).
- La API real: todo con el cliente simulado.
- IBAN de otros países y números de tarjeta (fuera de alcance, declarados).

## Veredicto

**APTO.** Los cinco criterios se cumplen (CA-5 por partes: el gate completo consta 12/12 al subir el commit y no lo he relanzado), 7 de 8 mutantes mueren y el octavo no deshace nada. No queda ningún hallazgo crítico ni alto. H-01 (media: el IBAN con espacio duro o en el formato impreso de la cuenta se admite y se guarda, sin estar declarado) y H-02 (baja: un máximo negativo o no entero no falla cerrado) pasan a la deuda técnica con su ID; H-01 conviene antes del modo sombra.
