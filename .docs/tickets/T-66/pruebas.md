# T-66 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`bloque_a/11_Ejecutor/tests`) | 117 | 185 (`test_t66_propuestas.py`: 46, 13 de la QA · `test_t66_evaluacion.py`: 22) |
| Bloque A Forex y Bloque B | 68 · 141 | 68 · 141 (no se tocan) |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1: cada propuesta aplicada tiene una prueba que falla sin ella | Orquestación: `revisores/mutaciones_orquestacion.sh` (11 mutaciones, las 11 fallan). Evaluación: el segundo agente revirtió cada cambio en una copia (tabla en su informe, resumida en «Regresiones») |
| CA-2: suites y gate completo en verde, línea base subida | A 185 / FX 68 / B 141; gate 12/12; cuotas bajadas: ruff 3120 → 3109 y mypy A 135 → 123 |
| CA-3: lo no aplicado, con motivo y destino | README del ticket («No entra») y deuda técnica T-67 |
| CA-4: el Documento 0 no se toca | `corpus-integridad` en verde; comportamiento documentado en el README del ejecutor y en INC-T66-01 e INC-T66-02 |

## Regresiones

**Orquestación** (`mutaciones_orquestacion.sh`): cada propuesta revertida por separado hace fallar su prueba:
- PA-01: P-02 y el aviso de tipo no activo;
- H-06;
- PA-05: la entrada al Contradictor, resolver sin contrarréplica, no esperar su confirmación y el efecto de una tesis frágil;
- PA-09: la marca y la anonimización automática;
- PA-14;
- PA-21.

**Evaluación:** fallan al revertir su cambio:
- el filtro de admisibles y el de `estado_h5`;
- el estado PROPUESTO y `certificados_vigentes`;
- la validación de `aprobar_certificados`;
- la recalibración como propuesta y la retirada de un PROPUESTO;
- la validación de `solo_endurecer`;
- el criterio con `n_eff`, las fechas, la correlación intraclase y el bootstrap por fechas;
- la métrica del Analista.

**Pruebas anteriores cambiadas:** `test_unitarias.py::test_metricas_de_pronostico_con_pronosticadores_sinteticos` y `test_integracion.py::test_certificado_emitido_con_muestra_suficiente`. Daban a todos los pronósticos la misma fecha, o ninguna, lo que con `n_eff` deja una sola observación efectiva. Ahora cada pronóstico tiene su fecha: el comportamiento nuevo es el correcto.

## Gate

Se ejecutó `.docs/scripts/gate.sh` con `--completo` sobre el resultado ya juntado: 12/12. El registro queda en `.docs/scripts/.logs/`.
