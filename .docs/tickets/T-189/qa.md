# QA · T-189 · PB-10, PB-17 y PB-21

## Ronda r01 · 24-11-2026 · Claude (revisor independiente; implementó Astra)

**Veredicto: NO APTO** (1 alta, 2 medias, 6 bajas).

### Qué se revisó

- Rama `astra/encargos-bloque-a-c38-c47` (PR 3), tip `2d99af6` sobre `develop` `9ce57b2`; commit del ticket `c581a75` (más el arreglo de
  importaciones de `5ef929b`). Worktree propio, sin tocar la copia del coordinador.
- Vara de medir: PB-10, PB-17 y PB-21 del Plan de pruebas V3.0, el «No comprueba» de `docs/evidencias_pruebas_bloque_a.md` en `9ce57b2`
  (INC-T116-01, INC-T116-02 e INC-T116-03), HA 4.6 (AUT-) y 4.8 (INC-), y la regla de seguimiento del Orquestador (EV, CPI, EAC).

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| `test_t189_controles.py`, `test_fase4_huecos.py`, `test_t159_extremo_a_extremo.py`, `test_t191_degradado.py` | 69 pasan (205 s) |
| Las pruebas nuevas fallan sin el cambio (revertido el código de `c581a75` en el worktree) | Sí: fallan las 3 de `test_t189_controles.py` y la de PB-10 de `test_fase4_huecos.py` |
| `mutantes.py` del ticket | Los 3 mutantes, detectados |
| Mutantes propios (`revisores/r01_mutantes.py T-189`) | **10 de 10 vivos** (ver H-02, H-05, H-06 y H-09) |
| Ataques (`revisores/r01_ataques.py`) | 5 hallazgos (ver abajo) |
| ruff y mypy de lo tocado | Sin subida en el tip: ruff 47 y mypy A 102 en `9ce57b2` y en `2d99af6`. En `c581a75`, +1 ruff (I001 en `test_t189_controles.py`), que corrige `5ef929b` |
| Goldens y corpus | `formas_flujos_mock.json` no cambia por este ticket (solo por T-185). R8 de T-177 (`retorno_con_credencial`) no se toca; el rechazo íntegro de la mensajería sigue igual |
| G3-MET-13 | Ningún texto nuevo con la raíz «valid-» |

### Juicio del cambio de `test_fase4_huecos.py`

La aserción nueva (`cambiados == {"P-02"}` y P-03 igual que antes) es más estricta que la anterior y coincide con el criterio del plan
(«F10 cambia solo P-02»). Como prueba es legítima. Pero solo pasa por un cambio del código que estropea otra función (H-01). Cuando se
corrija H-01, la prueba debe expresar la petición del plan sin quitar horizontes que el plan no pide quitar (ver la corrección de H-01).

### Hallazgos

**H-01 · alta · El CT-04 ya no deja cambiar P-03 con las clases por defecto, y descarta horizontes válidos sin decirlo.**
- Reproducción: `r01_ataques.py`, A1 y A2. Con P-02 por defecto (12 clases), un CT-04 `{"horizontes": ["H1","H2","H3","H4"]}` (quitar H5)
  da `REGISTRADA` y P-03 sigue siendo H1–H5. Cada horizonte salvo H3 es «No» para alguna clase (H1: FON, INM y ALT; H2: ALT; H4: DER y
  MON; H5: DER, MON y TCV), así que el Broker solo puede fijar subconjuntos de {H3}. En el caso de PB-10, H3 (válido para todas) tampoco
  se aplica, y ningún rechazo lo dice: la respuesta al Broker solo nombra `horizontes:ALT:H1`.
- Se esperaba: cambiar P-03 es una función de servicio del Broker. R6 y la tabla 8.3 ya impiden activar una celda «No» (la aplicabilidad
  se decide por celda). Ni el plan ni INC-T189-01 piden rechazar la lista entera, y ninguna prueba cubre el caso.
- Corrección: quitar `incompatible`/`if incompatible: continue` en `Bloque.decision` y volver al rechazo por celda (cada celda «No» queda
  en `rechazos` y sigue sin aplicarse). Un parámetro cuyo valor nuevo es igual al vigente no escribe ningún CFG (sin escritura que no cambia
  nada). El caso del plan, «H1 para ALT», se expresa con el formato del ejecutor: la lista vigente con H1 (que ya contiene H1). Así F10
  cambia solo en P-02 y ALT×H1 se rechaza con su motivo. Hay que actualizar INC-T116-01 con esa lectura.
- Prueba de regresión: (a) con las 12 clases, `["H1","H2","H3","H4"]` se aplica en P-03 y deja como rechazos las celdas FON/INM/ALT×H1,
  ALT×H2 y DER/MON×H4; (b) PB-10 con la lista vigente: `cambiados == {"P-02"}`, `horizontes:ALT:H1` rechazado y ningún CFG de P-03 en F10;
  (c) la respuesta nombra todo lo que no se aplica.

**H-02 · media · La prueba de CPI y EAC no comprueba el valor ganado; cinco mutantes de EV viven.**
- Reproducción: `r01_mutantes.py T-189`. Siguen vivos: EV con la fase en curso, EV sin BAC, EV sin pesos, BAC = 1 y «nunca registra las
  fases servidas». Con el último, EV siempre vale 0, el CPI 0 y el EAC `None`, y `test_aut_con_valor_ganado` pasa por la rama `else`.
  La prueba solo comprueba que `cpi == ev/ac` y que el EAC cumple su fórmula con los valores que el propio código registró.
- Se esperaba: que se compruebe EV = fracción de fases completadas × BAC (sistema del Orquestador) con valores conocidos.
- Corrección: añadir una prueba unitaria de `Presupuesto.valor_ganado`: con cribado e investigación servidas, al pedir en prospectiva, EV
  vale `BAC·(reparto.cribado + reparto.investigacion)` leído de la configuración, AC vale `consumido`, y CPI y EAC salen de su fórmula.
  Sin fases servidas, `cpi == 0` y `eac is None`. En el ciclo, al menos una AUT con `ev > 0` y `cpi` no nulo.
- Prueba de regresión: la misma. Los cinco mutantes deben morir.

**H-03 · media · La AUT- AUTORIZADA no lleva `condiciones`.**
- Reproducción: `r01_ataques.py`, C2. En el ciclo MP con 6 UC, la AUT AUTORIZADA (fase prospectiva) no tiene el campo `condiciones`.
- Se esperaba: el plan dice «Primera: AUTORIZADA … con condiciones» y HA 4.6 incluye `condiciones` en la AUT-. El mapa marca PB-17 como
  «Superada» sin ese campo.
- Corrección: escribir `condiciones` en cada AUT- (en la AUTORIZADA, la ampliación concedida en UC y el tope que queda; en la DENEGADA,
  `null` o la lista vacía), con textos que no lleven números a mano: se toman de la configuración y del cálculo.
- Prueba de regresión: en `test_aut_con_valor_ganado`, toda AUT AUTORIZADA lleva `condiciones` no vacío y toda AUT lleva motivo.

**H-04 · baja · El EV ponderado y la regla (c) del Orquestador no están declarados.**
- Reproducción: C. La AUT AUTORIZADA tiene EAC 9,18 con BAC 6, por encima de 1,5·BAC = 9,0. El sistema del Orquestador autoriza solo si
  «el EAC del ciclo con la ampliación no supera 1,5·BAC», y ese número no está en el Anexo A, así que no se puede programar. Además, EV se
  pondera con `presupuesto_uc.reparto_fases` en vez de usar la «fracción de fases completadas».
- Corrección: añadir a INC-T189-01 las dos lecturas, `[PROPUESTO]`: EV ponderado por el reparto, y la regla (c) sin aplicar porque falta el
  número en el Anexo A. Esto último queda como pregunta al operador.
- Prueba de regresión: una prueba que ate lo declarado y cite la incidencia: el EAC queda registrado y no decide la autorización.

**H-05 · baja · La etiqueta TARJETA nunca sale; una tarjeta se registra como CLAVE_API.**
- Reproducción: B «tarjeta». `tarjetas_en_texto` devuelve el número enmascarado, así que al reclasificar el indicio no coincide y cae en
  `CLAVE_API`. El prefijo `ES\d{2}` es un apaño para el IBAN. Viven los mutantes «tarjeta/DNI/correo como clave».
- Corrección: en `tipos_protegidos`, clasificar por el detector que encontró el indicio sobre el texto completo, no reclasificando el
  indicio: `ibanes_en_texto` → IBAN, `tarjetas_en_texto` → TARJETA, `RE_CORREO` → CORREO, `RE_SECRETO`/`sk-`/asignaciones → CLAVE_API,
  documento de identidad. Quitar el apaño de `ES\d{2}`.
- Prueba de regresión: una prueba parametrizada con un caso por tipo (como en B de `r01_ataques.py`) y ninguna fuga del valor en la
  incidencia.

**H-06 · baja · Si el secreto es el nombre de un campo, la incidencia se queda sin campo.**
- Reproducción: un CT-04 con una clave API como nombre de un campo de primer nivel da `campo_afectado = []`. La rama `campo_protegido` no
  tiene prueba (su mutante vive).
- Corrección: `campos = [k for k, v in msg.items() if contiene_credenciales(v) or contiene_credenciales(k)]`, con la máscara
  `campo_protegido` para los nombres. El texto de `DatosSensibles` debe usar también la lista enmascarada.
- Prueba de regresión: un secreto como nombre de campo, en primer nivel y anidado, da un campo no vacío, enmascarado, y cero coincidencias
  en los archivos.

**H-07 · baja · Las demás incidencias de R8 no llevan el tipo de dato, y el campo nuevo no está declarado.**
- `interfaz_broker.py` (CT-23, l. 131; retornos con credencial, l. 533 y 544; CT-25 con valor, l. 591) sigue sin `tipos_dato`. El mapa
  dice «lo mismo en CT-03 y con las credenciales de CT-25». `tipos_dato` no está en el esquema INC- de HA 4.8.
- Corrección: pasar `tipos_dato` en todas las incidencias SEGURIDAD (la de CT-25 con `CREDENCIAL`) y declarar el campo y su vocabulario
  cerrado en INC-T189-01.
- Prueba de regresión: una por cada vía: la incidencia lleva `tipos_dato` y no lleva el valor.

**H-08 · baja · Mapa, evidencias e incidencias imprecisos.**
- La misma frase («CT-04 conserva P-03…; AUT lleva CPI y EAC; R8 registra…») está pegada en las filas de PB-10, PB-17 y PB-21 del mapa y
  de las evidencias. INC-T116-01, INC-T116-02 e INC-T116-03 siguen diciendo «se deja como está» o «no se añaden».
- Corrección: dejar en cada fila solo lo que comprueba, y anotar en las tres INC que T-189 las supera (con la lectura de H-01).
- Prueba de regresión: `test_mapa_plan_pruebas` (o la que compare mapa y evidencias) debe seguir en verde. Revisión a mano en la ronda de
  cierre.

**H-09 · baja · La validación nueva de `horizontes` no tiene prueba y admite repetidos.**
- Reproducción: A3. `[]`, `"H1"` y `None` se rechazan (bien), pero ninguna prueba lo dice (el mutante vive). `["H3","H3"]` se aplica y deja
  P-03 = `["H3","H3"]`.
- Corrección: rechazar los horizontes repetidos con su motivo.
- Prueba de regresión: una prueba parametrizada con `[]`, `"H1"`, `None` y un repetido: P-03 no cambia y queda el rechazo.

### Scripts

- `revisores/r01_ataques.py`: se ejecuta desde `bloque_a/11_Ejecutor` (`python ../../.docs/tickets/T-189/revisores/r01_ataques.py`).
- `revisores/r01_mutantes.py T-189`: se ejecuta desde la raíz.

### Para la ronda r02

Volver a pasar los dos scripts: A1, A2, C2 y los casos de B en «ok», y ningún mutante vivo. Además, las pruebas del ticket, `test_integracion.py::test_peticion_ad_hoc_y_decisiones`
y `goldens_ct.py` (su flujo `decision_broker` manda `horizontes: ["H1","H3"]`).
