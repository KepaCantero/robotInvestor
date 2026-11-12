# T-97 · Análisis técnico

## Causa raíz o motivo

Los valores por defecto del marco se fijaron versión a versión (T-22, T-42, D-05…) antes de que existieran los diseños de los bloques y la tanda 2 de decisiones. Al preparar el cuestionario se vio que no cuadraban: un tope diario de 50 € de análisis sin tope anual, el importe del día y la pérdida de la semana de F solo en euros, y un 3 % de tolerancia del tipo de cambio igual para el euro-dólar que para una divisa poco líquida.

## Evidencia

- `validador/orquestador.py` (V0.73): `CONFIG_DEFECTO["dia_coste_max_eur"] = 50.0` y ningún tope anual; `tolerancia_tipo_k_rel = 0.03` única.
- `validador/control_f.py` (V0.73): F-14 con `importe_max_dia_eur` (50.000 €) y F-16 semana con `perdida_semana_max_eur` (5.000 €), sin porcentaje. F-04, F-07 y F-08 ya eran porcentajes del capital (el §8 del cuestionario lo exageraba; corregido).
- `validador/motor.py` no tiene ningún cálculo de oscilación o volatilidad, y `Orquestador.registrar_senal` recalcula la alerta de pérdida con `cfg["alerta_perdida_pct"]` (R-07): por eso H1 no cabe en este ticket (T-98).

## Implementación

- `validador/orquestador.py`:
  - `CONFIG_DEFECTO`: `tope_anual_gasto_pct_capital` (0,5), `capital_referencia_eur` (None), `tolerancia_tipo_k_rel_principales` (0,005), `divisas_principales` (USD, GBP, JPY, CHF) y `version_config` `CFG-0.12.0`; su validación en `_valida_config` (principales nunca más laxa que la general, divisas ISO sin euro ni repetidas, tope en (0, 10], capital None o positivo).
  - `_gasto_anio(a)`: gasto del año natural UTC, reservas vivas y tope en euros (capital de la última foto de G o, si no hay, el declarado; None si ninguno).
  - `emitir_encargo`: tras el tope diario, rechaza con O-43 si el encargo no cabe en el anual o no hay capital (solo encargos con coste).
  - `registrar_gasto`: aviso O-43 al llegar al tope.
  - `tolerancia_tipo_k(divisa)` y su uso en el contraste con K; `_pct_tol` para escribir «0.5%» en el motivo.
  - `_f_al_enviar`: pasa el capital de la autorización a `controles_de_contexto`.
  - `PRIORIDAD_AVISO["O-43"] = "ALTA"`.
- `validador/control_f.py`: `POLITICA_DEFECTO` con `importe_max_dia_pct` (25) y `perdida_semana_max_pct_*` (4, 5, 5), `SEMANA_PCT`, validación ≤ 100; F-14 con el mínimo de euros y %; F-16 semana con el mínimo cuando hay capital; `controles_de_contexto(..., cap=None)` falla cerrado con un capital no válido; `VERSION_REGLAS` F-0.4.0.
- `validador/catalogo_codigos.py`: O-43.
- `validador/migraciones.py`: `ESQUEMA_V0_74`, `_v074` y MIG-010 con su lista `cambia`; esquema de V0.74 registrado en `esquemas_codigo.json`.
- `validador/parametros_doc.py`: los ocho registros nuevos y `version_config` al día.
- `pruebas/pruebas_tanda2_t97.py` (nueva, 49 comprobaciones).
- Pruebas existentes ajustadas (datos, no lo que comprueban):
  - `pruebas_orquestador.py` (configuración de mecánica): tope anual al 10 %, capital declarado de 100.000 € y holgura del tipo de cambio también en las principales;
  - `pruebas_k_t26.py`, `pruebas_cartera.py` y `pruebas_libres_t33.py`: donde daban holgura al tipo de cambio, la misma en las principales;
  - `pruebas_control_f_t22.py`: la prueba del tope del día en euros usa una política con el 100 % para aislarlo; versión de reglas F-0.4.0;
  - `pruebas_integracion_v053.py`: CFG ≥ 0.11.0, cadena hasta MIG-010 y comprobación de V0.74 (una más: 37);
  - `pruebas_catalogo_codigos.py`: 44 avisos.
- `LEEME.md` y Documento 0 V0.74.

**Desviaciones del plan:** H1 fuera (T-98); en F solo lo que faltaba; el largo plazo conserva el 2 % diario de F-08 (quitarlo relajaría); capital declarado para el tope anual sin foto.

**Límites conocidos:** el capital es el de la cuenta (una cartera en la Fase 1); el tope anual va por año natural UTC; la lista de divisas principales es `[PROPUESTO]`.

**Comandos:**

```bash
.docs/scripts/pruebas_marco.sh
```

```bash
.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c
```

```bash
cd sistema_global/marco_comun_c && ../../.venv/bin/python pruebas/pruebas_tanda2_t97.py
```
