# Goldens de los contratos CT del Bloque A (T-114, Fase 3)

Ficheros esperados que congelan el formato de los contratos CT-01 a CT-25. La suite (`tests/test_fase3_goldens.py`) vuelve a generarlos con `tests/goldens_ct.py` y los compara **byte a byte**: si un formato cambia, una prueba falla y dice qué fichero y qué línea.

| Fichero | Qué congela | Cómo se obtiene |
| --- | --- | --- |
| `tablas_contratos.json` | Versión, estados, canales (V5 y V6) y campos mínimos de encargo y de retorno | Generado de `bloque_a/contratos.py` |
| `esquemas_respuestas.json` | Los esquemas JSON de las respuestas de los agentes (`ESQUEMAS`) | Generado de `bloque_a/contratos.py` |
| `mensajes_ejemplo.json` | El mensaje completo que `Mensajeria.crear` construye con cada ejemplo del Anexo B, o la clase de su rechazo | Generado con el ejecutor, reloj fijo |
| `formas_ciclo_mock.json` | Por contrato y tipo de mensaje de un ciclo semanal simulado: emisores, receptores y claves | Generado con el ejecutor y `MockClient` |
| `divergencias_anexo_b.json` | Dónde difieren el Anexo B y el ejecutor (INC-T114-01) | Calculado |
| `huellas.json` | SHA-256 del Documento 0, de los esquemas publicados y de los dos ficheros escritos a mano | Calculado |
| `anexo_b_esquemas.json` | Un esquema JSON por contrato y sentido, **derivado solo del Anexo B** del Documento 0 V5.1 | Escrito a mano |
| `anexo_b_ejemplos.json` | Un ejemplo por esquema derivado | Escrito a mano |
| `REGISTRO.md` | Una línea por re-congelado: fecha, ficheros y motivo | Lo escribe `--update` |

## Cómo se derivan los esquemas del Anexo B

- Son obligatorios los campos que el Anexo B nombra sin marcarlos como opcionales o condicionales («opcional», «solo en…», «cuando aplica»).
- Las listas cerradas del Anexo B (`A|B|C`) son `enum`.
- No se añade ningún tipo, patrón ni límite que el Anexo B no diga, y los campos de más se admiten: el §6.2.3 dice que los campos son el mínimo común y que el esquema del operador puede ampliarlos.
- Cada esquema lleva en `$comment` la marca «derivado del Anexo B» y, si hace falta, la nota de lo que el Anexo B deja abierto.
- CT-16 a CT-22 no tienen campos en el Anexo B (los remite a los prompts de sistema): de ellos solo se congela el canal.

## Regla de re-congelado

**Re-congelar solo es deliberado.** Un golden cambia únicamente cuando se ha decidido cambiar un formato, y entonces:

1. desde `bloque_a/11_Ejecutor`: `python tests/goldens_ct.py --update --motivo "por qué cambia el formato"`. Sin motivo, termina con error y no escribe nada;
2. el golden regenerado, la línea nueva de `REGISTRO.md` y el cambio de código que lo causa van en **el mismo commit**, con el motivo también en el mensaje del commit;
3. si cambia `anexo_b_esquemas.json`, `anexo_b_ejemplos.json`, el Documento 0 o un esquema publicado, `huellas.json` deja de coincidir: se revisa que los esquemas derivados siguen diciendo lo que dice el Anexo B y se re-congela con el motivo.

Nunca se regenera un golden para que una prueba pase sin entender por qué falló. Es la misma regla que la del corpus (`tools/corpus_integridad.py --update`).

Para comprobar sin escribir: `python tests/goldens_ct.py` (termina con 1 si algo difiere).
