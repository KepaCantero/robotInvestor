# T-114 · Análisis técnico

## Causa raíz o motivo

Los formatos de los contratos CT del Bloque A vivían solo en el código (`bloque_a/contratos.py`) y en el Anexo B del Documento 0. Un cambio en una tabla de canales, en un campo mínimo o en un esquema de respuesta podía pasar sin que fallara ninguna prueba. La Fase 3 del plan de fases pide congelarlos en goldens comparados byte a byte, antes de la cadena A→B (Fase 6), que se apoya en ellos.

## Evidencia

- Antes de T-114 no había ningún fichero esperado de contratos: `grep -rn golden bloque_a/11_Ejecutor tools` no daba nada.
- Con los goldens, cinco mutaciones hechas a mano en una copia desechable se detectan (salida en `pruebas.md`, «Mutación a mano»).
- Al derivar los esquemas del Anexo B y medir con el ejecutor aparecieron diferencias que nadie tenía listadas: INC-T114-01 y INC-T114-02 en `docs/incidencias.md`.

## Implementación

- Archivos nuevos y por qué:
  - `bloque_a/11_Ejecutor/tests/goldens_ct.py`: genera el texto de cada golden, lo compara con el congelado y re-congela con motivo. Es a la vez módulo de las pruebas y orden de línea.
  - `bloque_a/11_Ejecutor/tests/test_fase3_goldens.py`: 51 pruebas, agrupadas por criterio de aceptación.
  - `bloque_a/11_Ejecutor/tests/goldens/`: seis goldens generados, dos ficheros escritos a mano (`anexo_b_esquemas.json`, 32 esquemas; `anexo_b_ejemplos.json`, 32 ejemplos), `README.md` con la regla de re-congelado y `REGISTRO.md`.
- Archivos cambiados: `docs/incidencias.md` (INC-T114-01 y 02), la deuda técnica (T-114 y T-115), `.docs/README.md` (tabla de scripts), `bloque_a/11_Ejecutor/README.md` (una línea en la estructura) y `docs/AVANCE.md`.
- No cambia: nada de `bloque_a/11_Ejecutor/bloque_a/`, del Documento 0 ni de `06_Plantillas_entregables`.
- Decisiones tomadas:
  - Los esquemas derivados viven con las pruebas y no en `06_Plantillas_entregables`, que es corpus congelado de la entrega.
  - Las diferencias con el Anexo B se **miden con el ejecutor**, no se deducen de las tablas: se crea el mensaje del ejemplo con `Mensajeria.crear` y se repite quitando cada campo obligatorio. Motivo: las tablas engañan; por ejemplo, `CAMPOS_MINIMOS["CT-02"]` no se aplica a la entrega, que es un retorno y tiene su comprobación propia en `validar`.
  - Del ciclo simulado se congelan formas (emisores, receptores, claves y valores de las listas cerradas), no mensajes enteros: los textos del simulador pueden cambiar sin que cambie un formato.
  - Los ejemplos del Anexo B se envían por el primer canal del contrato; el retorno vuelve por él si el canal lo admite. Los campos del sobre que el Anexo B pone en el cuerpo (`run_id`, `query_id`, `presupuesto`, `consumo`) se pasan por su sitio, como hace el ejecutor.
- Desviaciones del plan:
  - CA-5 decía que los dos ejemplos publicados cumplen sus esquemas. El del informe de seguimiento no lo cumple por la clave `x_aviso_ejemplo` (INC-T114-02). La prueba congela el hecho: ese es el único incumplimiento y sin la clave lo cumple. No se toca la entrega.
  - `divergencias_anexo_b.json` usa las claves `el_ejecutor_rechaza_el_ejemplo_del_anexo_b`, `el_ejecutor_admite_que_falte` y `el_ejecutor_exige_y_el_anexo_b_no_nombra`, más precisas que las dos que nombraba el plan.
  - `formas_ciclo_mock.json` añade `valores_de_listas_cerradas`: así se ve que CT-06 emite fases que el Anexo B no lista.
- Límites conocidos:
  - Los esquemas derivados solo llegan al primer nivel de campos, y a un segundo nivel donde el Anexo B trae un bloque JSON. No fijan tipos.
  - El ciclo simulado emite 8 de los 25 contratos por la mensajería (CT-02, 05, 06, 08, 11, 12, 13 y 15). De los demás se congelan las tablas y el mensaje de ejemplo, no una forma observada.
  - Los retornos internos (CT-06 a CT-14) no pasan por `Mensajeria`: su formato real lo fijan los esquemas de `ESQUEMAS`, congelados en `esquemas_respuestas.json`.
  - CT-16 a CT-22 no tienen cuerpo congelado: el Anexo B no da sus campos.
  - El Bloque A Forex queda para T-115.
- Comandos exactos para probarlo, desde `bloque_a/11_Ejecutor` y con el `.venv` del proyecto:
  - `python -m pytest -q tests/test_fase3_goldens.py` (51 pruebas, unos 20 s);
  - `python tests/goldens_ct.py` (comprueba; 0 si coincide, 1 si difiere);
  - `python tests/goldens_ct.py --update` (debe terminar con 2 y no escribir nada).
