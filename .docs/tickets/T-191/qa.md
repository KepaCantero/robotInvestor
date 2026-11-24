# QA · T-191 · PB-52, modo degradado de HT-09

## Ronda r01 · 24-11-2026 · Claude (revisor independiente; implementó Astra)

**Veredicto: NO APTO** (1 alta, 1 media, 3 bajas).

### Qué se revisó

- Rama `astra/encargos-bloque-a-c38-c47` (PR 3), tip `2d99af6` sobre `9ce57b2`; commit del ticket `f9e16b7` (`5ef929b` solo cambia el
  estilo en `redaccion.py` y `sintesis.py`).
- Vara de medir: PB-52 del Plan V3.0; el «No comprueba» de `9ce57b2` («sin CT-14 al Orquestador, sin G3 manual con etiqueta y sin el RUN-
  ni la incidencia en el historial»); el sistema del Orquestador para «HT-09 caído» (elevar por CT-14, comprobaciones B a mano, etiqueta
  «G3 manual», BLOQUEADO con motivo si no se completan, nunca APTO por defecto); y CT-14 en el Anexo B.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| `test_t191_degradado.py` y la prueba de PB-52 de `test_t159_extremo_a_extremo.py` (con las vecinas, 69 pasan) | En verde |
| Fallan sin el cambio (revertido el código de `f9e16b7`) | Sí: las 3 |
| `mutantes.py` del ticket | El único mutante, detectado |
| Mutantes propios (`revisores/r01_mutantes.py T-191`) | **7 de 8 vivos** (H-02) |
| Ataques (`revisores/r01_ataques.py`) | Caso nominal bien: CT-14 de AG-02 a AG-18, incidencia HERRAMIENTA ligada a su `msg_id`, G3V `G3_MANUAL` BLOQUEADO, RUN- `PARCIAL` con la entrega `BLOQUEADA` y la limitación, nada en las carpetas de entrega. Además, 3 hallazgos |
| ruff y mypy | Sin subida en el tip (ruff 47 y mypy A 102 en los ficheros tocados, igual que en `9ce57b2`) |
| G3-MET-13 y números | Ningún texto con «valid-» ni ningún número a mano |

### Juicio del cambio de `test_t159_extremo_a_extremo.py`

Es legítimo que la prueba deje de esperar la excepción, porque el plan pide continuidad segura, no un ciclo que se cae. También es
legítimo que admita un G3V `G3_MANUAL`. Pero al quitar `assert not [G3V]` se pierde la única aserción que respaldaba su nombre («nunca
hay APTO por defecto»), y no se pone otra en su lugar (H-04). La prueba nueva (`test_t191_degradado.py`) cubre CT-14 (solo el receptor),
el G3V manual BLOQUEADO, el RUN- en F5 y que no haya pronósticos. No cubre la incidencia del historial, que el encargo pide expresamente,
ni el emisor ni el contenido de la CT-14, ni la etiqueta `dictamen_ht09`, ni la limitación declarada (H-02).

### Hallazgos

**H-01 · alta · El respaldo hace pasar un fallo de integridad, o un error de control, por «herramienta caída».**
- Reproducción: `r01_ataques.py`, casos 2 y 3. `control_con_respaldo` captura `RuntimeError, OSError, ValueError, KeyError, TypeError`
  en torno a `ht09_validar`, que además lee el almacén (F2, RC) y corre controles propios del ejecutor (raíces, EST-06, unitarias, C07,
  G3-MET-13). Si se manipula F2 durante el control, el almacén lanza `ValueError("Fallo de integridad en F2, registro 1")`. Antes de
  T-191 eso paraba el ciclo (comprobado revirtiendo el cambio). Ahora el ciclo termina `BLOQUEADA` con una incidencia HERRAMIENTA y sigue
  escribiendo en F5 y en HA. Pasa lo mismo con `DatosSensibles` y `EscrituraFueraDeReserva`, que son `PermissionError` y por tanto
  `OSError`, con `MensajeInvalido`, `FugaDeInformacion`, `ReplayFaltante`, `PresupuestoAgotado` y con los fallos de programación.
- Se esperaba: la regla vigente (`respuesta_final.para_la_consulta`, T-166 y T-169) dice que un fallo de integridad o un error de control
  para el ciclo. El modo degradado es solo para la herramienta no disponible.
- Corrección: envolver solo la llamada a `ht09.validar`, no los controles del ejecutor, y tratar como caída solo la indisponibilidad de
  la herramienta (una excepción propia `HerramientaNoDisponible` que lance el envoltorio de HT-09 ante `ImportError` u `OSError` de la
  herramienta, sin contar `PermissionError`). Todo lo demás se relanza, y siempre se relanza si
  `respuesta_final.para_la_consulta(almacen, e)` es verdad o si `verificar_integridad()` no está entero.
- Prueba de regresión: (a) F2 manipulado durante el control: el ciclo para con «Fallo de integridad» y no queda ninguna incidencia
  HERRAMIENTA ni CT-14; (b) `DatosSensibles`, `EscrituraFueraDeReserva`, `KeyError` y `TypeError` dentro del control se relanzan;
  (c) la caída simulada (`HerramientaNoDisponible`) sigue dando el modo degradado.

**H-02 · media · Las pruebas no matan casi nada de lo que pide el plan; siete mutantes viven.**
- Reproducción: `r01_mutantes.py T-191`. Viven: sin incidencia HERRAMIENTA; `except Exception`; la fase mal atribuida (F6 en lugar de
  F7); sin la limitación en el paquete; G3V de F6 sin `dictamen_ht09 = NO_DISPONIBLE`; G3V de F7 con el dictamen de la herramienta; CT-14
  sin la fase. Solo muere «G3V F7 sin etiqueta».
- Corrección: en `test_t191_degradado.py`, para cada `fallo`: la incidencia HERRAMIENTA con `fase` igual a F6 o F7 y el `msg_id` de la
  CT-14; la CT-14 con emisor AG-02, receptor AG-18 y `resultado_ht09.fase`; el G3V `G3_MANUAL` con `dictamen_ht09 == "NO_DISPONIBLE"`;
  la limitación con el motivo en el RUN- de F5 o en el paquete; `r["g3"]["modo"] == "G3_MANUAL"`. Con H-01: una excepción que no es de
  disponibilidad no entra en el modo degradado.
- Prueba de regresión: las mismas aserciones. Los ocho mutantes deben morir.

**H-03 · baja · El mapa da por cumplido «el Orquestador ejecuta G3 manual», y el caso combinado del plan no se prueba.**
- El ejecutor no hace ninguna comprobación B a mano: siempre bloquea (INC-T191-01 lo declara, y «bloqueo justificado» cumple el criterio
  de aprobación). Aun así, el mapa y las evidencias ponen «Superada» con `no_comprueba` vacío. INC-T159-01 sigue contando PB-52 entre las
  funciones que faltan. La preparación del plan (HT-09 caído y HT-01 sin datos de una clase en el mismo C1) no se prueba junta.
- Corrección: poner en `no_comprueba` que el G3 manual es un bloqueo justificado sin comprobaciones B (INC-T191-01), actualizar
  INC-T159-01 y añadir el caso combinado.
- Prueba de regresión: un ciclo con dos clases, una sin datos de HT-01, y HT-09 caído: la clase sin datos se cierra con alcance reducido
  declarado (PS2), la entrega queda BLOQUEADA, no hay ningún G3V APTO y no sale ninguna cifra.

**H-04 · baja · `test_pb52_con_ht09_caido_nunca_hay_apto_por_defecto_ni_entrega` ya no comprueba que no haya APTO.**
- Corrección: añadir `assert not [e for e in HA if e.get("tipo_entrada") == "G3V" and str(e.get("dictamen_efectivo")).startswith("APTO")]`
  y que el G3V `G3_MANUAL` esté BLOQUEADO. Corregir el docstring para que diga lo que comprueba.
- Prueba de regresión: la misma aserción. Un mutante que devuelva APTO en el respaldo debe morir también en esta prueba.

**H-05 · baja · La CT-14 del modo degradado no lleva el paquete y añade un campo que el Anexo B no describe.**
- `paquete_sintesis` es `{"run_id": …}`, no el paquete que el Orquestador revisaría. `resultado_ht09` no está en el CT-14 del Anexo B: el
  esquema derivado lo admite porque no cierra las propiedades, pero no está documentado.
- Corrección: mandar el paquete (o su referencia, como en el CT-14 normal) y declarar `resultado_ht09` en INC-T191-01 y en el registro de
  divergencias del Anexo B, o llevarlo dentro de `paquete_sintesis`. El golden `formas_flujos_mock.json` no captura este flujo, así que no
  hay que volver a congelarlo.
- Prueba de regresión: la CT-14 degradada valida contra `CT-14.ENCARGO` y lleva el `paquete_sintesis` del run.

### Scripts

- `revisores/r01_ataques.py`: se ejecuta desde `bloque_a/11_Ejecutor`.
- `revisores/r01_mutantes.py T-191`: se ejecuta desde la raíz del worktree.

### Para la ronda r02

Volver a pasar los dos scripts. Los casos 2 y 3 deben salir «ok» (excepción relanzada y ninguna incidencia HERRAMIENTA), salvo los fallos
de programación si se declara otra cosa, y ningún mutante debe quedar vivo.
