---
name: ri-probar
description: Fase 3 de 4 del flujo de trabajo del Robot Investor. Úsala después de implementar, o cuando pidan «prueba», «testea», «ejecuta las suites», para completar y ejecutar las pruebas (nominales, límites, fallo cerrado, regresión, migración, integración), pasar los gates del repo y dejar el informe en .docs/tickets/T-NN/pruebas.md.
---

# Probar una tarea del Robot Investor

Fase 3 de 4. Antes: `ri-implementar`. Después: `ri-qa`.

Nada cuenta como hecho sin pruebas (regla 5 de `CLAUDE.md`). Esta fase la hace quien implementó; la QA independiente viene después.

## Qué tipos de prueba hacen falta

| Tipo | Qué comprueba | Ejemplo |
| --- | --- | --- |
| Nominal | El caso normal produce lo esperado | Un encargo válido genera su expediente |
| Límite | Bordes exactos: cero, mínimo, máximo, redondeos, fin de una ventana temporal | Una cantidad que es exactamente el paso; una cotización con la antigüedad máxima permitida |
| Fallo cerrado | Entrada ausente, caducada o inválida → error con su código y **estado sin cambios** | Sin tipo de cambio no se reduce (G-06) y el estado es idéntico al de antes |
| Regresión | Cada fallo corregido tiene su prueba, que **falla sin la corrección** | Revierte la corrección, comprueba que la prueba falla y restáurala |
| Migración | Los estados guardados de versiones anteriores migran y siguen siendo íntegros | `estado_V0_50.json` → versión actual |
| Contrato | Los mensajes validan contra su esquema JSON, y los inválidos fallan con la regla esperada | Casos `inv_Vnn_…` del sobre CT-G-02 |
| Determinismo | Misma entrada, misma semilla → misma salida | Dos ejecuciones dan la misma huella |
| Integración | El recorrido de extremo a extremo con datos simulados | Detección → … → cierre en el simulador |

## Reglas

- Las líneas base nunca bajan: A ≥ 103, A-Forex ≥ 68, B ≥ 141 (las de `tools/cuotas.txt`) y todas las suites del marco común de C. Quitar pruebas no es arreglar nada.
- Sin red y con la hora fija: las pruebas no dependen del momento en que se ejecutan.
- Cada criterio de aceptación del plan tiene al menos una prueba.

## Cómo se ejecuta

- Marco común de C: `.docs/scripts/pruebas_marco.sh`, que ejecuta todas las suites de la sección «Cómo se ejecuta» de `sistema_global/marco_comun_c/LEEME.md` y avisa de las que falten en ella.
- Bloques: `pytest -q` en el `11_Ejecutor` de cada bloque tocado (ver `CLAUDE.md`).
- Gate del repo: `.docs/scripts/gate.sh` (rápido) mientras trabajas y el mismo con `--completo` antes de cerrar; los dos llaman a `./tools/check_all.sh` y guardan el log.

## Informe

Escribe `.docs/tickets/T-NN/pruebas.md` con:

- recuento de pruebas antes y después, por suite;
- la matriz criterio de aceptación → prueba;
- para cada regresión, la confirmación de que falla sin la corrección;
- el resultado de `./tools/check_all.sh`;
- los comandos exactos usados.

## Puerta de salida

- [ ] Todas las suites en verde y recuentos iguales o mayores que antes.
- [ ] `./tools/check_all.sh` en verde.
- [ ] Cada criterio de aceptación cubierto por al menos una prueba.
- [ ] `pruebas.md` escrito; si otro agente hará la QA, commit y push con `[pendiente QA]` y `handoff.md` en el ticket.

## Scripts: lo repetible, automatizado

Antes de hacer algo a mano, mira `.docs/scripts/` (tabla en `.docs/README.md`). Si vas a hacer algo que se repetirá, escríbelo como script, guárdalo ahí y apúntalo en esa tabla: la próxima vez se ejecuta y no se gastan otra vez los mismos tokens. Cómo: `.docs/knowledge/03_scripts-y-ahorro-de-tokens.md`. Los secretos, solo desde `.env` a través de `.docs/scripts/common.sh`.

