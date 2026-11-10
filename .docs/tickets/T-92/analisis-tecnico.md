# T-92 · Análisis técnico

## Cómo se hizo

1. **Revisión de la rama de Astra** (`76b90e6`, base `bc90534`), sobre su propia base. `qa_rama.sh` da 244 pruebas de A en verde. Sondas en `revisores/rama_*.py`: H-01 (R8) y H-02 (sellos).
2. **Fusión de prueba con develop:** 13 ficheros en conflicto, porque develop tiene las cinco rondas de T-65 sobre los mismos ficheros.
3. **`cherry-pick` de `76b90e6` sobre develop** y resolución fichero a fichero:
   - **`evaluador.py`:** `motivo_no_fresca` de T-65 se combina con `_base_conocida`, `bases_cesta` y la base congelada de Astra. `_rentabilidad_serie(simbolo, f0, f1, base)` devuelve también la fecha de la base, que la frescura necesita. Se conservan `fecha_dato_proxy`, `fecha_dato_referencia`, la comprobación de fuga por serie y los parámetros sin literales (T-65, H-05). La fecha de efecto de la degradación de H5 se queda en el mismo ciclo (T-65, H-13), y la composición de O3 se hace con `efectivo_el` igual a esa fecha.
   - **`sintesis.py`:** certificados por (clase, horizonte, método) de Astra, con `parametro()` y las bandas por Evaluador de develop. Se mantiene el control C07 de R13 y `_control_unitarias` (C8).
   - **`contratos.py`:** el `msg_id` externo de CT-01 (Astra) convive con el prefijo por ámbito de develop.
   - **`orquestacion.py` y `consumo.py`:** `autorizar_hasta_tope` (A6), con los dos números leídos de la configuración.
   - **`motor/servicio.py`, `agentes.py` y `README.md`:** manda develop. La lista de 81 fichas de la V5.0 entra limpia desde la rama.
   - **Documentación** (`CLAUDE.md`, la deuda, el diario, las cuotas y el mapa de pruebas): manda develop. Lo de Astra se reescribe en este ticket.
4. **Fuera:** `encargo_b.py`, el subcomando `preparar-encargo-b`, su prueba y su apartado del README (Fase 6).
5. **Correcciones H-01 a H-03** y sus pruebas en `tests/test_t92_revision.py`.

## Lo que cambia de comportamiento frente a develop

- **CESTA:** antes, un miembro que no servía se quitaba. Ahora la CESTA espera y, pasado el plazo, queda NO_RESOLUBLE (D02, ver el README).
- **Certificados:** un certificado sin método ya no autoriza cifras (R13 del Documento 0: clase × horizonte × método). En simulado no hay certificados reales afectados.
- **Ampliación del presupuesto:** el tope es el total (base × 1,50) y no base × 1,75 (INC-T92-01).
- **Almacén:**
  - abrir uno manipulado lanza `ValueError`, y no solo lo señala `verificar_integridad`;
  - las escrituras toman un cerrojo de fichero.
- **CT-01:** reutilizar el `msg_id` recupera la respuesta guardada. Un mensaje fallido se reconcilia a mano.

## Límites que se mantienen (declarados por Astra o por esta revisión)

- **Sellos:** quien pueda reescribir toda la carpeta de estado, sellos y marca incluidos, no se detecta. Hace falta una copia o una firma externas.
- **Almacenes anteriores a los sellos:** un almacén anterior se sella al abrirlo, y no se sabe si ya le faltaba el último registro.
- **R21 (C8):** es un filtro textual acotado; no sustituye a un clasificador de instrumentos.
- **Sello restaurado de una escritura atrás:** no se distingue de un proceso que murió entre el registro y el sello; al abrir se aparta ese registro (confirmado) a `*.no_confirmado.jsonl` con una incidencia. No se pierde: queda en ese fichero (QA r03, `r03_02`, caso 6).
- **Rastro de una recuperación:** si el proceso muere después de reescribir y antes de anotar la incidencia, el rastro es el propio `*.no_confirmado.jsonl` (QA r03, H-29).
- **Reconciliación de CT-01:** depende de que el operador revise F5. El código no puede saber si hubo efectos.

## Diseño de las rondas r02 y r03

- **R8 (claves `sk-`).** Primero un candidato lineal con una expresión regular y después una decisión en Python (`_es_clave_sk`). Dos intentos con una sola expresión fallaron: el primero tenía falsos positivos con «risk-…» y URLs (H-01 y H-07); el segundo, falsos negativos con «_» (H-17). Una sola expresión que lo resolviera todo sería cuadrática. `secretos_en_texto()` es la función común de `contiene_credenciales()` y `llm.contenido_sensible()`.
- **Almacén.** Una escritura añade el registro y después guarda el sello, cada paso con fsync.
  - Si se interrumpe antes del sello, se trunca el registro.
  - Si se interrumpe después, el registro queda confirmado.
  - Si el proceso muere entre los dos, al abrir hay exactamente un registro válido por encima del sello, que se aparta a `*.no_confirmado.jsonl` con una incidencia, una vez validados todos los ficheros.
  - Cualquier otra diferencia es un fallo de integridad y no abre.
  - Una instancia viva no recupera nunca.
- **CT-01.** El `msg_id` del Broker tiene su propio espacio (`MSG-BRK-…`). La reserva guarda la clase del error, y `reconciliar()` deja primero el rastro en HA. La respuesta se devuelve en la forma guardada.
- **CESTA.** La base de cada miembro pasa la validación de HT-01; un miembro inválido o ya parado al emitir queda fuera, porque se sabía al emitir.
- **CT-23.** Un plazo con solo fecha vence a la medianoche local siguiente.

## Ronda r04

- **R8 (claves `sk-`), regla definitiva.** Se detecta todo «sk-» (en mayúsculas o minúsculas) que no está dentro de una palabra y va seguido de 20 caracteres o más. Solo se descarta lo que tiene forma de texto corriente: tramos separados por «-» o «_» que son palabras, siglas, números de hasta 4 cifras o códigos de periodo («Q4», «FY2023», «3Q24», «2024Q4»). También se mira el texto con los escapes de JSON sustituidos y se aceptan `bytes`.
  - Las rondas anteriores intentaban reconocer la forma de una clave y siempre se escapaba alguna.
  - Esta reconoce la forma del texto, que es lo que hay que dejar pasar, y por defecto todo lo demás es una clave.
- **Almacén.**
  - Una sola escritura cortada en todo el almacén; si hay más registros sin sello, falla cerrado.
  - Una última línea a medio escribir también se aparta al abrir.
- **CT-23.** Solo fechas ISO 8601; una medianoche que no existe en la zona pasa a la primera hora válida.
