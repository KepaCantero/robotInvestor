# T-106 · QA independiente

## Ronda r01

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente Claude; no implementó T-106) · **Ronda:** r01 · **Fecha:** 2026-11-12
- **Commit revisado:** `7064f60` (`develop`). Se formó la opinión con el README del ticket, el código y las fichas del Catálogo antes de leer `analisis-tecnico.md`.

### Reproducción desde limpio

Extracción limpia con `git worktree add --detach <tmp>/wt 7064f60` (y otra del padre `1b8c699` para comparar el ciclo), con el `.venv` del proyecto enlazado y `PYTHONPATH` apuntando a la extracción (comprobado que `bloque_a` se importa de ahí, no del árbol principal). Ambas se borran al terminar.

| Paso | Resultado |
| --- | --- |
| `./tools/check_all.sh` en la extracción limpia | **12/12** (`revisores/r01_00_gate.log`): corpus 695 íntegro, ruff 2908 = cuota, mypy A 109, pytest A **1034** · FX 68 · B 176 |
| `tests/test_fase1_mon_idx.py`, `test_fase1_fon_der.py`, `test_fase1_tcv.py`, `test_t106_motor.py` | 118 · 122 · 101 · 27, en verde |
| Ciclo mock (`bloque-a --cliente mock … backtest --desde 2024-01-05 --hasta 2024-03-29`) en el padre y en `7064f60` | `senales.csv`, `pronosticos.csv` y `metricas.json` **idénticos**; `consumo.csv` solo difiere en la latencia; en RC cambia `artefacto.code_ref` de las fichas antiguas (`bloque_a.motor.operaciones · f_x` → `bloque_a.motor.servicio · f_x`, ahora correcto) y, por eso, la cadena de huellas |
| `r01_05_promocion.py`: promoción desde el Catálogo del padre con el script y el ejecutor del commit | Sale **byte a byte** el Catálogo commiteado; segunda pasada idempotente; el manifiesto solo cambia en la línea del Catálogo (huella padre = manifiesto padre; huella nueva = manifiesto nuevo); ningún `.docx` tocado |

Scripts del revisor (todos aceptan la raíz de una extracción como primer argumento):

```bash
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_01_ataques_datos.py [RAIZ]        # fuzzer: 11 844 mutaciones de datos y parámetros
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_02_valores_independientes.py [RAIZ]  # recálculo con otra implementación
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_03_integracion.py [RAIZ]           # Motor ↔ Catálogo, CT-09, RC, §1.3, corpus
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_04_mutantes.py [RAIZ]              # 41 mutantes propios (≈ 25 min)
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_05_promocion.py [RAIZ] [COMMIT]    # reproducción de la promoción
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_06_ataques_dirigidos.py [RAIZ]     # casos concretos y rendimiento
```

Salidas guardadas en `revisores/r01_0N_salida.log`.

### Fidelidad a las fichas (muestra: 16 de 21, de las cinco familias)

Revisados «Método», «Parámetros», «Salidas», «Verificación» y «Aclaración y rechazo» contra el código, y recalculados con otra implementación (`r01_02`):

| Ficha | Método y valores | Parámetros por defecto | Rechazos | Observaciones |
| --- | --- | --- | --- | --- |
| MON-YLD-001 | Conversiones descuento → P → simple/TAE/MMY, i simple → TAE y cubierto (1 + i·t/base)·S/F recalculados a 1e-14 | sí | sí | — |
| MON-EXP-001 | Recupera exactamente una senda escalonada si los nodos son exactos; **inestable** en cuanto no lo son (H-01) | sí | sí | H-01, H-09, H-10 |
| MON-REAL-001 | Fisher exacto ex ante y ex post; vintages | sí | sí | — |
| MON-FIX-001 | Identidad fijar = renovar con forwards | sí | sí | senda «plana» sin prueba que la fije (H-08) |
| IDX-ERP-001 | Grinold-Kroner a mano con λ = 0,3 y N = 7, y con λ = 1: coincide a 1e-14 | sí | sí | — |
| IDX-CONC-001 | HHI, N_ef, top-n y HHI sectorial con numpy sobre pesos de Dirichlet: a 1e-14 | sí | sí | «pesos suman 1» es tautológico (H-08) |
| IDX-REL-001 | Brechas, log-ratio y momentum correctos con datos mensuales | sí | **no comprueba que la historia sea mensual** (H-07) | H-02 |
| IDX-REB-001 | CAR, BMP, segunda vía | sí | sí | sin IC por defecto (INC-T106-01) |
| FON-LEV-001 | Fórmula y arrastre ½(L² − L)σ²T | sí | sí | H-08 |
| FON-TD-001 | TD por bloques anuales y TE = σ·√252 | sí | sí | H-08 |
| DER-VRP-001 | Réplica VIX recalculada con r = 3,5 %, F = 102 y K₀ = 100 (no los r = 0 y K₀ = F de los casos): a 1e-10; ≈ σ de la sonrisa | sí | sí | H-03, H-08 |
| DER-SKEW-001 | SVI recupera (a, b, ρ, m, σ) de una sonrisa SVI exacta a 1e-6; RR y BF 25Δ por SVI = raíz propia con delta forward a 1e-6; dσ/dk en k = 0 | sí | sí | H-03, H-08 |
| DER-ROLL-001 | Carry ln(F/S)/T, roll (F₁/F₂ − 1)·base/Δd con 365 y 360 y desviación en pb, sobre divisas: a 1e-10 | sí | sí | «suma de componentes = total» es tautológico (H-08) |
| TCV-TP-001 | ACM propio (SVD + VAR(1) de `statsmodels` + regresión de excesos + λ + recursiones) sobre **otra** curva afín de 3 factores con innovaciones gaussianas: prima a 2, 5 y 10 años igual a 1e-6 pb; ajuste < 5 pb | sí | sí | La prima se aparta de la del generador a 10 años (27 frente a 47 pb) por el sesgo de muestra finita del VAR que la propia ficha advierte: no es fallo |
| TCV-CDS-001, TCV-BEI-001 | λ = s/(1 − R), pérdida esperada y 5y5y revisados en código | sí | sí | H-08 (λ) |

Números a mano (regla 2): no se han encontrado fuera de las fichas. Lo que no fija la ficha (HAR 1-5-22, ES al 97,5 %, IC al 95 % en SLOPE, IC ausente en IDX-REB) está declarado en INC-T106-01 como `[PROPUESTO]` y en la deuda (T-57). Las constantes de los módulos son convenciones o unidades (365, 360, 252, 100, 10 000).

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | **no** | 21 manejadores y 50 casos superados y registrados en RC (`r01_03`). Pero el caso de MON-EXP-001 «la senda reproduce los forwards de entrada» no comprueba lo que dice la «Verificación»: excluye los nodos que no fijan tramo, y en el propio caso el nodo a 365 días queda a **144 pb** de la senda (H-01). Además, 22 de 41 mutantes sobreviven a los casos de control (H-08). |
| CA-2 | **no** | En el repo, lo servible = código ∩ IMPLEMENTADO (35 = 35), y sin Catálogo o con él vacío no se sirve nada. Pero un Catálogo con bytes no UTF-8 lanza `UnicodeDecodeError` (H-05), y con el ejecutor movido y `rutas.raiz_paquete` (README) el Motor no encuentra el Catálogo y no sirve **ninguna** ficha, tampoco las 14 del ciclo (H-04). |
| CA-3 | **no** | Determinista en los 50 casos nominales (doble llamada idéntica). Pero 297 de 11 844 mutaciones de datos lanzan excepciones que no son `ErrorFicha` en 14 de las 21 fichas, y por CT-09 llegan al llamador sin RECHAZADO ni entrada en RC (H-02). |
| CA-4 | sí | 21 filas y 21 líneas de madurez en IMPLEMENTADO; §1.3 = 35 + 11 + 35 = 81, cuadra con la tabla y con las 81 fichas; promoción reproducida byte a byte; re-congelado en el mismo commit con el motivo (`r01_03`, `r01_05`). |
| CA-5 | sí | 12/12 en extracción limpia; ruff 2938 → 2908; mypy sin subir. |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `r01_02` (bloque MON-EXP) y el caso de control 2 de MON-EXP-001 | **MON-EXP-001 da sendas inventadas.** Con la curva del propio caso de control (OIS 1,92 → 1,60 % en 12 meses, suave) la senda implícita es 1,80 % → 0,16 % (−6,6 bajadas en abril) → **6,85 % (+26,8 subidas en julio)**, y el nodo a 365 días queda a 144 pb de la senda; el caso pasa porque `error_reproduccion_nodos_max` solo mira los nodos usados. Con una senda escalonada exacta y las cotizaciones redondeadas a 0,1 pb (lo normal en una pantalla), el error de la senda es de **208 pb**; con una curva cotizada plana al tipo vigente, −15 movimientos. Causa: cada nodo fija el tipo de un tramo entero con los pocos días que caen tras la reunión (10–18 días), y el error se amplifica tramo a tramo. Se sirve como SERVED_WITH_LIMITATIONS, con cifras citables. | Rehacer la senda: interpolar la curva de descuento (log-lineal) a las fechas de reunión y derivar el tipo de cada tramo de los forwards entre reuniones, o ajustar por mínimos cuadrados con todos los nodos; exigir que **todos** los nodos se reproduzcan dentro de tolerancia (o rechazar); y que el caso de control lo compruebe con nodos que no caigan en las reuniones y con ruido de cotización. Mientras tanto, devolver MON-EXP-001 a «Documentado» en el Catálogo (re-congelado con motivo) o rechazarla en el Motor. | abierto |
| H-02 | **alta** | `r01_01` (297 excepciones; ejemplos por ficha en la salida) y `r01_03` (CT-09 de punta a punta) | **Excepciones que no son `ErrorFicha`** en 14 fichas (IDX-REL 104, MON-EXP 32, IDX-ERP 30, MON-FIX 24, TCV-TP 22, MON-REAL 19, DER-TERM 18, TCV-BEI 15, TCV-VIXTS 12, TCV-SLOPE 11, FON-LEV, IDX-REB, DER-VRP, MON-YLD): `ValueError`, `TypeError`, `AttributeError`, `OverflowError`, `ZeroDivisionError`, `LinAlgError`, `RuntimeError` de `brentq`. Casos realistas: un múltiplo «n/d» en la historia de IDX-REL-001 (`ValueError`), una divisa sin datos en MON-REAL-001, un escenario dado como número en IDX-ERP-001. `Motor.servir` solo traduce `ErrorFicha` y `NotImplementedError`: la excepción sube al llamador, sin RECHAZADO y **sin entrada en RC**. También salen cifras no finitas servidas como `null` (IDX-REL con un CAPE infinito, DER-VRP/FON-LEV/FON-TD con 1e300) y TCV-TP se cuelga con un plazo de 1,2·10⁸ meses. | Validar tipos y dominios en cada ficha (listas, dicts y números finitos y en rango antes de usarlos) y, como defensa en profundidad, que `servir` capture cualquier excepción del manejador y la convierta en RECHAZADO (`DATOS_INSUFICIENTES` o un motivo de error de cálculo) registrado en RC. Rechazar resultados con números no finitos y acotar los plazos de TCV-TP. Prueba de regresión: el fuzzer `r01_01` sin excepciones. | abierto |
| H-03 | media | `r01_03` (estados CT-09) y `grep -n "lim: list\[str\] = \[" bloque_a/11_Ejecutor/bloque_a/motor/fichas_fon_der.py` | Las 8 fichas FON y DER meten sus «Supuestos y limitaciones» fijos en `limitaciones`, no en `resultado["advertencias"]` (no tienen `ADVERTENCIAS`): con datos perfectos salen **siempre** SERVED_WITH_LIMITATIONS. Contradice el comentario de `_advertencias_aparte` («solo señala problemas de los datos»), `analisis-tecnico.md` y el docstring de `test_las_advertencias_fijas_de_la_ficha_no_son_limitaciones` («como en las demás familias»), que solo prueba TCV. | `ADVERTENCIAS` en `fichas_fon_der.py` (o las advertencias en el resultado, como MON/IDX) y una prueba que lo compruebe en las 21. | abierto |
| H-04 | media | `r01_03` (bloque «ejecutor movido») | `madurez_catalogo()` busca el Catálogo en `BLOQUE_A_RAIZ` o en `DIR_EJECUTOR.parent`, pero ignora `rutas.raiz_paquete` del YAML, que el README del ejecutor ofrece para moverlo. Con el ejecutor movido y `raiz_paquete` bien puesto, los prompts se encuentran y el Motor sirve **0 fichas**: también las 14 del ciclo (ACC-MOM, RISK-DD…), así que el ciclo se queda sin cálculos. Antes de T-106 eso no pasaba. | Resolver la raíz con `configuracion.raiz_paquete(cfg)` (pasar la raíz desde el `Motor`, que tiene `cfg`), con una prueba de ejecutor movido. | abierto |
| H-05 | media | `r01_03` (Catálogo con bytes no UTF-8) | CA-2 dice «sin Catálogo legible, ninguna»; con un Catálogo con bytes no UTF-8 `read_text` lanza `UnicodeDecodeError`, que no es `OSError`: `servible()` y cada `servir()` revientan en lugar de rechazar. | Capturar también `UnicodeDecodeError` / `ValueError` y devolver `{}`; prueba. | abierto |
| H-06 | baja | `r01_03` (fila falsa antes de la tabla; caché) | `_FILA_CATALOGO` toma la **primera** fila del documento que encaja, no la de la tabla del §2: una fila con el mismo formato antes de la tabla manda. Y `lru_cache` no se invalida: un Catálogo ausente al primer uso deja el proceso sin servir nada hasta reiniciar (y un cambio en caliente no se ve). El corpus está congelado, así que el riesgo es bajo. | Leer solo la tabla del §2 (entre su cabecera y el «Total: 81 fichas») y comprobar que hay 81 filas; documentar o acotar la caché. | abierto |
| H-07 | media | `r01_06` (IDX-REL con historia diaria) | IDX-REL-001 pide historias **mensuales**, pero no lo comprueba: con datos diarios sirve un «momentum 12-1» de 12 sesiones y un acarreo de cobertura dividido entre 12 por fila, sin limitación. | Rechazar si la separación entre fechas no es mensual (como hace TCV-TP con la curva). | abierto |
| H-08 | media | `r01_04` | **Casos de control y pruebas que no protegen las fórmulas.** De 41 mutantes del revisor, 22 superan los casos de control (lo que decide la promoción) y 11 superan **también** las pruebas: MON-EXP (probabilidad contra el vigente), MON-FIX (senda plana al último forward), IDX-CONC (top-n con n − 1), FON-DISC (κ complementaria: equivalente con κ = 0,5, pero ninguna prueba usa otro κ), FON-TD (TE × 252 en vez de × √252), DER-VRP (e^{−rT}, término de K₀ sumado, implícita de ayer: los casos usan r = 0, K₀ = F e implícita constante, justo lo que anula esos términos), DER-SKEW (delta con N(d₂), w'' de SVI mal derivada) y DER-ROLL (descomposición). Hay casos tautológicos: «pesos suman 1» (IDX-CONC rechaza si no suman), «suma de componentes = total» (DER-ROLL, el roll es el residuo) y «L = 1 ⇒ arrastre 0» (vale también con L² − 1). Las fórmulas actuales son correctas donde se recalcularon (`r01_02`), pero no tienen red. | Añadir casos con datos que no anulen los términos (r ≠ 0, K₀ ≠ F, implícita variable, κ ≠ 0,5, L = 2 frente a valor a mano), valores a mano de TE, top-n, deltas y senda plana, y sustituir los casos tautológicos por comprobaciones del método. | abierto |
| H-09 | baja | `r01_04` (M05) y la ficha MON-EXP-001 (iii) | La ficha da la probabilidad como (tipo implícito tras la reunión − **tipo vigente**)/Δ; el código usa el cambio respecto a la reunión anterior. Puede ser la lectura correcta, pero es una decisión de método que no está en INC-T106-01 (regla 7) y ninguna prueba la fija. | Declararla en INC-T106-01 `[PROPUESTO]` y fijarla con una prueba de varias reuniones. | abierto |
| H-10 | baja | `r01_06` | MON-EXP-001 con un nodo justo a 12 meses (365 días) no calcula el cambio acumulado a 12 meses («curva sin cobertura a 12 meses»). | Admitir el horizonte igual al último nodo (`d_h > d_fin`, no `>=`). | abierto |
| H-11 | baja | `r01_06` | Una fecha numérica (`20261110`) se acepta como 1970-01-01 (epoch en ns) en MON-YLD-001, y lo mismo en las demás fichas que usan `pd.Timestamp` sin comprobar el tipo. | Aceptar solo texto ISO, `date` o `Timestamp`. | abierto |
| H-12 | baja | `r01_06` (VOL-GARCH-001 sin `arch`) | El detalle del rechazo dice «con código pero «Documentado» en el Catálogo», pero el Catálogo la da por IMPLEMENTADO: falta la dependencia. Viene del cambio de condición `ficha in DOCUMENTADAS_CON_CODIGO` → `ficha in IMPLEMENTADAS`. | Distinguir «Documentado en el Catálogo» de «dependencia opcional no instalada». | abierto |
| H-13 | baja | `r01_03` y lectura | Documentación: `analisis-tecnico.md`, `pruebas.md` y la deuda dicen **53** casos de control; hay **50** (2+2+2+2+2+2+2+3 · 3+2+2+2+3+3+2+3 · 2+2+2+3+4). El cambio de `code_ref` de las 14 fichas antiguas en RC no se menciona. `test_cada_ficha_se_sirve_por_ct09_con_su_primer_caso` acepta `comprobar(...) or "advertencias" in resultado`, que pasa aunque el caso falle. | Corregir el recuento, anotar el cambio de `code_ref` y quitar el `or`. | abierto |

### Invariantes del sistema

- Ningún camino nuevo llega a una orden: las fichas solo se sirven por CT-09; el ciclo no las llama (salidas idénticas al padre).
- Sin LLM en la ruta determinista ni en los casos de control.
- Los controles no se relajan solos; pero la promoción se apoya en casos de control que no bastan (H-01, H-08).
- Falla cerrado: no en todos los caminos (H-02, H-05).
- Números a mano: no; lo que la ficha no fija está en INC-T106-01 `[PROPUESTO]` y en la deuda.
- Sin secretos ni datos personales o financieros reales: solo datos sintéticos.
- Documentación: CLAUDE.md, README del ejecutor, deuda y diario al día, salvo H-03 y H-13.

### Veredicto

**NO APTO.** No se cumplen CA-1, CA-2 ni CA-3, y hay dos hallazgos altos abiertos:
- H-01: MON-EXP-001, ya promovida a IMPLEMENTADO, sirve sendas de tipos inventadas, y su caso de control no comprueba lo que dice la «Verificación»;
- H-02: entradas mal formadas tumban la llamada CT-09 sin RECHAZADO ni registro en RC.

CA-4 (promoción, §1.3 y corpus) y CA-5 (gate 12/12) se cumplen. El ciclo del Bloque A sigue igual. Vuelve a `ri-implementar`. Al corregir, el revisor volverá a ejecutar `r01_01` a `r01_06` y añadirá la ronda r02.

## Ronda r02

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente Claude; no implementó T-106) · **Ronda:** r02 · **Fecha:** 2026-11-13
- **Commit revisado:** `4be8ea6` (`develop`; el código de la r02 de T-106 entró en `e4d13d3`). Opinión formada con el README del ticket, el código y las fichas del Catálogo (leídas por identificador) antes de leer `analisis-tecnico.md` y `pruebas.md`.

### Reproducción desde limpio

Extracción limpia con `git worktree add --detach <scratchpad>/wt 4be8ea6`, con el `.venv` del proyecto enlazado y `PYTHONPATH` apuntando a los tres ejecutores de la extracción (comprobado que `bloque_a`, `bloque_a_forex` y `bloque_b` se importan de ahí). Las copias para mutantes son del `bloque_a` entero sin `.docx`. Extracción y copias borradas al terminar.

| Paso | Resultado |
| --- | --- |
| `./tools/check_all.sh` en la extracción limpia | **12/12**: corpus 695 íntegro, ruff 2908 = cuota, mypy A 109 · FX 174 · B 159 (= cuotas), pytest A **1288** · FX 68 · B 176 |
| Pruebas de T-106 en la copia sin mutar (`test_fase1_*`, `test_t106_motor`, `test_unitarias`, `test_t65_resto_t53`, `test_t87_contratos`, `test_t92_revision`) | 685 en verde |
| Catálogo y corpus | El Catálogo no cambia desde `7064f60` (la r02 no lo toca); huella del manifiesto = huella del archivo; ningún `.docx` tocado desde antes de T-106 |

### Scripts ejecutados

```bash
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_00_reejecutar_r01.py [RAIZ] [--mutantes]   # r01_01 a r01_06 (r01_03 y r01_02 adaptados en memoria)
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r01_04_mutantes.py [RAIZ]                       # los 41 mutantes de la r01
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_01_catalogo_y_rc.py [RAIZ]                  # manda el Catálogo por el Motor, RC, promoción, corpus
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_02_oraculos.py [RAIZ]                       # oráculos de MON-EXP, FON-DISC, FON-FLOW, DER-TERM, TCV-SLOPE, TCV-VIXTS
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_03_ataques.py [RAIZ]                        # entradas hostiles y controles que la petición no debe relajar
.venv/bin/python -I -B .docs/tickets/T-106/revisores/r02_04_mutantes.py [RAIZ] [--solo ID]           # 43 mutantes nuevos (fichas y servicio.py), ≈ 15 min
```

| Script | Resultado |
| --- | --- |
| `r01_01` (fuzzer de la r01, por defecto) | **129/129**: 15 678 mutaciones (13 465 `ErrorFicha`, 2 213 servidas), sin excepciones ajenas, sin cifras no finitas, ninguna llamada > 5 s |
| `r01_02` (sin su bloque MON-EXP, que rechaza a propósito el sistema justo que usaba) | **30/30** |
| `r01_03` (con `_madurez.cache_clear()` y 66 casos) | 19/21. Los dos fallos no son defectos: «ejecutor movido» llama a `servible(f)` sin raíz (la corrección de H-04 va por `Motor.raiz`, comprobada en `r02_01`), y «limitaciones fijas» marca 7 fichas cuyas limitaciones con el primer caso son datos opcionales que faltan (sin superficie, sin historia…), no advertencias fijas: H-03 está corregido |
| `r01_04` (mutantes de la r01) | 40 aplicables, **40 cazados por los casos de control** (M38 ya no se aplica: cambió `_forward`) |
| `r01_05` (promoción) | **7/7** |
| `r01_06` (ataques dirigidos) | **5/5** |
| `r02_01` | **27/27** |
| `r02_02` | **40/40** |
| `r02_03` | **12/29** (H-14, H-15, H-16) |
| `r02_04` | 43 mutantes: 25 sobreviven a los casos de control y **13 sobreviven también a las pruebas** (H-18) |

### Hallazgos de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 | corregido | MON-EXP rehecho: `r02_02` (a)–(f): con nodos en las reuniones los tramos coinciden con los forwards entre reuniones de un oráculo propio a 1e-17; con nodos fuera de ellas (sobredeterminado) recupera la senda; una curva suave no escalonada o redondeada sin precisión declarada se rechaza; con precisión declarada el error real de cada tramo queda dentro de la cota que se publica; tira de futuros correcta. Queda H-16 |
| H-02 | corregido en las fichas | `r01_01` sin excepciones; 1 224 llamadas por el Motor con parámetros hostiles (NaN, ±inf, bool, texto, None, listas, dicts, 1e308) en cada parámetro de las 21: sin excepciones, una entrada en RC por llamada y sin cifras no finitas. Queda la petición mal formada al Motor (H-15) |
| H-03 | corregido | Advertencias de FON y DER en `resultado["advertencias"]`; FON-LEV conserva una limitación declarada (simulación no servida) |
| H-04 | corregido | `r02_01`: ejecutor copiado a otra carpeta con `rutas.raiz_paquete`: el Motor sirve las 35 |
| H-05 | corregido | `r02_01`: bytes no UTF-8, vacío, ausente o una carpeta: nada servible y RECHAZADO, sin excepción |
| H-06 | corregido | Solo la tabla del §4 (filas falsas en el §1 o en el §5 no mandan); relectura por fecha de modificación. Informativo: un cambio que conserva `mtime_ns` (p. ej., `cp -p`) no se ve hasta reiniciar |
| H-07 | corregido | `r01_06` |
| H-08 | corregido para los mutantes de la r01 | 40/40 cazados por los casos de control. Mutantes nuevos vivos: H-18 |
| H-09 | parcial | Docstring, prueba y `probabilidades_acumuladas` con la fórmula literal; pero INC-T106-01 no recoge la decisión (H-19) |
| H-10, H-11 | corregidos | `r01_06` |
| H-12 | corregido | `r01_06`; sin prueba que lo fije (mutante S11 vivo, H-18) |
| H-13 | corregido | 66 casos en el ticket y la deuda; `code_ref` anotado; `or` quitado. Restos menores en H-21 |

### Fidelidad a las fichas: oráculos nuevos (`r02_02`)

| Ficha | Comprobado contra un cálculo propio | Resultado |
| --- | --- | --- |
| MON-EXP-001 | forwards entre reuniones, movimientos por reunión y acumulados, probabilidades, cambio a 6 y 12 meses, sobredeterminado, redondeo, curva suave, futuros | 13/13 |
| FON-DISC-001 | mediana de P/NAV − 1, z a 52 semanas, normalización con κ = 0,3, total con NAV supuesto, AR(1) y vida media en meses | 6/6 |
| FON-FLOW-001 | identidad de AUM, flujo relativo, z a 36 meses, autocorrelaciones 1–3 (`statsmodels.acf`), acumulados, suma, rango | 6/6 |
| DER-TERM-001 | varianza total lineal en T, pendiente, ratio, estado, σ_fwd, movimiento del evento, frecuencia de inversiones | 5/5 |
| TCV-SLOPE-001 | pendiente 2s10s, MCO y HAC de Newey-West (`statsmodels`, sin corrección, L = ⌊4(T/100)^(2/9)⌋), IC al 95 %, pendiente forward a 3 y 6 meses, carry y rolldown neutrales en DV01 | 6/6 |
| TCV-VIXTS-001 | estado, roll, futuro a 30 días y rentabilidad esperada, percentil, frecuencia de contango, ES al 97,5 % | 4/4 |

Con la r01 (16 fichas recalculadas), las 21 tienen ya un oráculo independiente; todas coinciden.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | 21 manejadores, 66 casos superados y registrados en RC: 21 entradas CASOS_CONTROL con todos sus casos, la madurez y `verificar_integridad` en verde; una ficha desconocida o sin casos queda REJECTED; un caso que falla queda marcado (`r02_01`). Observación: H-18 |
| CA-2 | sí | Por el Motor, servible = código ∩ IMPLEMENTADO (35); una ficha degradada en la tabla del §4 se rechaza con su madurez en el detalle y queda en RC; sin Catálogo legible, ninguna (`r02_01`). Observación: ninguna prueba lo fija (mutante S01 vivo, H-18) |
| CA-3 | **no** | Determinista y rechaza las entradas mal formadas de sus datos, pero en las 8 fichas MON e IDX los umbrales de rechazo («Entradas mínimas», «Aclaración y rechazo») y los rangos de los parámetros se pueden bajar desde `parametros` de la petición (H-14, alta). Además, una petición mal formada tumba el CT-09 antes de llegar a la ficha (H-15) |
| CA-4 | sí | §1.3 = tabla del §4: 81 = 35 (14 + 21) + 11 + 35; las 21 en IMPLEMENTADO en su fila y en su ficha; Catálogo intacto desde la r01 y huella del manifiesto correcta (`r02_01`, `r01_05`) |
| CA-5 | sí | 12/12 en extracción limpia; cuotas sin subir |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-14 | **alta** | `r02_03`, bloque 1 | **En MON e IDX, la petición puede relajar los controles de la ficha.** `_params` (`fichas_mon_idx.py`) mezcla `parametros` de la petición sobre `PARAMETROS_POR_DEFECTO`, y ahí viven también los umbrales de rechazo y los rangos. Por CT-09: IDX-ERP-001 con 2 años de historia del múltiplo (rechazo < 10) pasa de RECHAZADO a SERVED_WITH_LIMITATIONS con `anios_historia_min: 1`; N = 3 con `N_rango: [1, 100]` y λ = 2 con `lambda_reversion_rango: [-9, 9]` se sirven; IDX-REL-001 con 3 años de historia y `anios_min: 1`; IDX-CONC-001 con `top_n: 1` y `top_n_rango: [0, 1e6]`; MON-FIX-001 con dos nodos hasta T y `nodos_min: 1`. MON-EXP-001 (`nodos_min`, `meses_nodos`, `anios_convexidad`), MON-REAL-001 (`anios_min`), MON-YLD-001 (`anios_percentil_min`), IDX-REB-001 (`eventos_min`) e IDX-CONC-001 (`anios_precios_min`, `ventana_percentil_min_anios`) leen sus umbrales del mismo diccionario. TCV ya lo resolvió (`UMBRALES` fijos, la petición que los trae se rechaza) y FON/DER tienen `MINIMOS` y `RANGOS` aparte: comprobado que no se bajan. Un control que la petición puede bajar contradice CA-3 y «los controles nunca se relajan solos». | Sacar de `PARAMETROS_POR_DEFECTO` de MON/IDX los umbrales y rangos a un diccionario fijo (como `UMBRALES` de TCV) y rechazar la petición que los traiga; pruebas de regresión con cada clave de `r02_03`. | abierto |
| H-15 | media | `r02_03`, bloque 2 | `Motor.servir` lanza la excepción al llamador, sin RECHAZADO ni entrada en RC, con `datos: [5]`, `datos: [{"valores": 5}]`, `datos: [{"valores": [1, 2]}]`, `parametros: "x"` o `[1, 2]`, un `plan` desconocido, una `fecha_corte` ilegible o una `operacion` no textual: el `_resolver_datos`, el `dict(parametros)`, el `parametro(uc…)` y la comparación con `FICHAS_CATALOGO` quedan fuera del `try` de la r02. La validación de `valores` de las envolturas no llega a ejecutarse. Hoy ningún camino del ciclo envía estas fichas al Motor, por eso no es alta. | Validar la forma de la petición al entrar en `servir` (operación texto, `datos` lista de dicts con `valores` dict, `parametros` dict, plan conocido, fechas legibles) y convertir cualquier fallo en RECHAZADO registrado; pruebas con los ocho casos. | abierto |
| H-16 | media | `r02_03`, bloque 5 (último caso) | MON-EXP-001 con una curva escalonada redondeada a 1 pb y `precision_cotizacion: 5e-5` se sirve como **SERVED, sin limitaciones**, con una incertidumbre de redondeo de hasta 23,4 pb en un tramo (umbral de rechazo: Δ = 25 pb). El error real del último tramo es de 12,8 pb: `movimientos_en_reunion` −0,40 frente a −1 verdadero, así que la probabilidad publicada de esa reunión se aparta 60 puntos de la verdadera. La cota se publica en `incertidumbre_redondeo_pb`, pero nada avisa en `limitaciones`. | Añadir una limitación cuando la incertidumbre de algún tramo sea una fracción relevante de Δ, o un umbral más estricto. El número debe salir de la ficha o de la configuración y quedar declarado `[PROPUESTO]` en INC-T106-01. | abierto |
| H-17 | baja | `r02_03`, bloque 4 | Las cifras no finitas siguen dos políticas: MON, IDX, FON y DER rechazan el resultado entero, y el Motor también (`FASE1`); TCV las cambia por `None` con una limitación (TCV-VIXTS con VIX3M = 1e-320 sale SERVED_WITH_LIMITATIONS con `spot/VIX3M: None`). `analisis-tecnico.md` dice que en las fichas de T-106 una cifra no finita se rechaza. Es defendible, pero no está escrito. | Unificar la política o declarar la de TCV en el análisis e INC-T106-01. | abierto |
| H-18 | media | `r02_04` | **Reglas y fórmulas sin red.** 13 de 43 mutantes sobreviven a los casos de control **y** a las pruebas: S01 (`citable_segun_catalogo` → `bool(estado)`: sirve lo «Documentado»; ninguna prueba degrada una ficha en un Catálogo temporal y comprueba que el Motor deja de servirla, solo se mira el texto de `madurez_catalogo`), S09 (una ficha sin casos de control se da por superada), S10 (los casos de control sin comparar las dos pasadas), S07 (excepciones del Motor: hoy equivalente para las 21, sin prueba con un manejador que lance), S11 (H-12 sin prueba), S06 (equivalente con el Catálogo actual); FON-DISC con media en lugar de mediana (Y01) y vida media en meses de 30 días (Y02); FON-FLOW con el acumulado relativo al AUM del último periodo (Y04), el z frente a 72 meses (Y05) y otra autocorrelación (Y06); MON-EXP sin el redondeo implícito de cada cotización (X04); la envoltura MON/IDX sin el rechazo de no finitos (X11, cubierta por el Motor). Las fórmulas actuales son correctas (`r02_02`), pero un cambio que las rompa pasaría el gate. Otros 12 sobreviven a los casos de control y los cazan las pruebas: aceptable donde la «Verificación» de la ficha no cubre el paso. | Pruebas de regresión: Motor con un Catálogo temporal que degrada una ficha (RECHAZADO), `verificar_casos_control` con una ficha sin casos y con un manejador no determinista, un manejador que lanza `ValueError` por el Motor, GARCH sin `arch` simulado; valores a mano de FON-DISC (mediana con miembros asimétricos, vida media) y FON-FLOW (acumulados, z, autocorrelación); MON-EXP con cotizaciones redondeadas sin `precision_cotizacion`. Volver a pasar `r02_04` sin vivos. | abierto |
| H-19 | baja | Lectura de `docs/incidencias.md` y de `f_mon_exp` | Decisiones de método de MON-EXP-001 que el código da por declaradas y no están en INC-T106-01: la lectura del «tipo vigente» de la r01 (H-09: el docstring dice «INC-T106-01 [PROPUESTO]», pero la incidencia no la recoge), el rechazo del sistema justo con nodos fuera de las reuniones, y la precisión implícita «medio último dígito» de cada cotización (un nodo escrito `0.0` vale ±500 pb y fuerza el rechazo; una curva redondeada sin `precision_cotizacion` se rechaza con «no se puede reproducir con un tramo por reunión», sin sugerir que se declare la precisión). | Añadirlas a INC-T106-01 `[PROPUESTO]` y mejorar el mensaje del rechazo por redondeo. | abierto |
| H-20 | baja | Lectura de `fichas_fon_der.py` (`f_der_vrp`) | DER-VRP-001 toma `nivel_es` de RISK-VAR-001 (INC-T106-01), pero acepta cualquier nivel en (0, 1), mientras que TCV-VIXTS-001 aplica el rango 0,90–0,99 de esa misma ficha. | Aplicar el rango de RISK-VAR-001 también en DER-VRP-001. | abierto |
| H-21 | baja | Lectura | Restos de documentación: el apartado «Implementación» de `analisis-tecnico.md` sigue diciendo «la tabla del §2 (81 filas)» (el índice es el §4, como dice la ronda r02) y la primera tabla de `pruebas.md` dice «53 en 21 fichas». | Corregir o marcar como histórico. | abierto |

### Invariantes del sistema

- Ningún camino nuevo llega a una orden: las 21 fichas solo se sirven por CT-09 y el ciclo no las llama.
- No hay LLM en la ruta determinista ni en los casos de control.
- Los controles no se relajan solos en TCV, FON y DER, pero en MON e IDX los relaja una petición (H-14).
- Falla cerrado en las fichas (fuzzer y parámetros hostiles), pero no en la entrada del Motor (H-15).
- Ningún número a mano nuevo. Lo que la ficha no fija está en INC-T106-01, salvo lo de H-19 y H-20.
- Sin secretos ni datos personales o financieros: solo datos sintéticos.
- Documentación al día salvo H-17, H-19 y H-21.

### Veredicto

**NO APTO.** CA-3 no se cumple y hay un hallazgo alto abierto, H-14: en las 8 fichas MON e IDX, la petición puede bajar los umbrales de rechazo y los rangos que fija la ficha. Los medios (H-15, H-16 y H-18) deberían corregirse en la misma ronda. Los bajos, H-17 y H-19 a H-21, pueden ir a la deuda si no se corrigen.

H-01 a H-13 de la r01 están corregidos; H-09 lo está a falta de declararlo (H-19). CA-1, CA-2, CA-4 y CA-5 se cumplen. Vuelve a `ri-implementar`. Al corregir, el revisor volverá a ejecutar `r02_00` a `r02_04` (y `r01_04`) y añadirá la ronda r03.
