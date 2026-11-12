# T-75 · Análisis técnico

## Causa raíz o motivo

D-22 de la Constitución V0.6 pide el embudo visible y la alarma de sequía a 60 días. La pasada de coherencia de la V0.65 (PC2-03) lo dejó pendiente. La QA r01 encontró que la primera versión (V0.70) tenía tres problemas:
- con una ventana deslizante, la sequía solo se veía durante un intervalo estrecho (H-08);
- el veto de F no dejaba rastro en el expediente (H-01);
- contaba pasos en vez de candidatos (H-03 y H-04).

## Implementación (V0.70 y ronda r02 en la V0.73)

- **`orquestador.py`:**
  - `embudo(desde, hasta)` trabaja sobre el periodo abierto por la izquierda (desde, hasta].
  - Las validadas se cuentan por análisis: la clave es el event_id del sobre, o el `analisis_ref` de un DIRECTA.
  - Las invertidas se cuentan por expediente.
  - Cada salida lleva `bloqueo_previo`, que es el último veto de F. `salen` cuenta las oportunidades distintas que salen.
  - `sequia(ahora, dias)` se cuenta desde la última inversión, o desde el arranque si no la hubo. La condición sigue cierta hasta la siguiente inversión.
  - `barrer()` da un O-40 por cada plazo que dure la sequía y solo informa del cambio si el aviso se añadió.
  - El veto de F en `autorizar()` se anota de PROPUESTA a PROPUESTA, de F, con las reglas que vetan (`MOTIVO_VETO_F`).
- **`consola.py`:** `informe_embudo(o, ahora, dias)` valida los días.
- **Otros archivos:** `parametros.py` (`o_dias_sequia`, `n_dias_embudo`), `catalogo_codigos.py` (O-40), `reloj.py` (T-89) y `migraciones.py` (MIG-007 y, en la r02, MIG-009).

## Ronda r03 (V0.75)

La QA r02 encontró que la corrección del veto solo cubría `autorizar()` y que rompía la propuesta CT-G-06.
- **H-09:** `_anotar_veto_f(e, cf, control_f, ahora)` es el método común. Lo llaman la rama de veto sin anulación de `pantalla_aprobacion()` y la de `autorizar()`. El informe se consume igual que antes.
- **H-10:** `contratos.propuesta()` busca la última transición a PROPUESTA con `desde != "PROPUESTA"`. Así el veto (de PROPUESTA a PROPUESTA) no cambia el emisor, la hora ni el `event_id`. Ningún otro lector de «la última anotación a X» se ve afectado: `orden()` ya filtraba así, y el resto lee por estado.
- **H-11:** las dos ramas devuelven `_no(..., reloj_firme=True)`. Con esa marca, `@_seguro` no devuelve `ultimo_ahora` a su valor anterior: el reloj se queda en el instante del veto y nada anterior a él se admite después (O-16).
- **H-12:** LEEME, Documento 0 (V0.70 y V0.75), deuda y `pruebas.md` al día.
- **H-13:** se mantiene la clave por sobre (un sobre nuevo es un análisis nuevo) y se corrige el docstring.
- **H-14:** la edad se mide desde el primer instante real (`a - (ult or primero) < plazo`). El inicio adelantado 1 µs solo se usa para el embudo.

**Decisiones:**
- La causa de bloqueo que se ve es la del veto de F. Los demás rechazos de `autorizar()` son intentos, no controles del análisis, y quedan como límite: por kill-switch, que el panel ya muestra; por nivel de la cartera; por testigos.
- La sequía se juzga desde la última inversión, la lectura de D-22 que propone la QA.

**Límites:**
- Los rechazos de `autorizar()` distintos del veto de F no salen en el embudo.
- Una inversión en cualquier cartera apaga la alarma de todas.
- Nada llama a `informe_embudo()` cada semana: lo hará N cuando exista.
