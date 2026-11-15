# T-141 · Bloque A: datos reales de divisas del BCE

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | `.docs/scripts/descargar_datos_bce.py`, `.docs/scripts/comprobar_datos_a.py` (`--clases`); pruebas `bloque_a/11_Ejecutor/tests/test_t141_datos_bce.py` |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-15: «Doy el visto bueno a todo lo que depende de mí» (fuente de datos reales: el agente elige por defecto) |
| Deuda técnica | T-141 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Decisión

Fuente elegida por defecto `[PROPUESTO]` (registro de decisiones del operador): los **tipos de cambio de referencia del BCE** (API pública `data-api.ecb.europa.eu`, sin cuenta ni clave). El Bloque A solo tiene activas las divisas (PA-01), y las seis del universo salen de los tipos «unidades por euro» de USD, JPY, GBP, AUD, CHF y MXN. Cuando se activen otros tipos de activo hará falta otra fuente.

## Qué se hace

- `descargar_datos_bce.py <carpeta> [--desde]`: descarga y escribe un CSV por símbolo (`fecha`, `cierre`, `fecha_publicacion`) en el formato de HT-01. Los datos no se suben al repositorio.
- `comprobar_datos_a.py --clases DIV`: comprueba solo los tipos que la fuente cubre.
- Resultado al 15-11-2026: seis series de 3 039 cierres (2015-01-02 a 2026-11-13); 6 de 6 OK en H3 y en H1; un ciclo semanal C1 con el cliente simulado sobre estos datos termina COMPLETO, ENTREGADA, G3 APTO.

## Criterios de aceptación (binarios)

1. CA-1: `tests/test_t141_datos_bce.py` en verde (cruces, datos que faltan o no son positivos, lectura por HT-01).
2. CA-2: con red, la descarga y la comprobación dan 6 de 6 OK; un ciclo mock con esos datos termina ENTREGADA.
3. CA-3: gate 12/12.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN QA · claude · implementado y probado (con red: descarga, comprobación y ciclo mock)
- 2026-11-15 · claude · renumerado de T-138 a T-141: otra sesión usó T-138 y lo subió antes
