# T-142 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; implementó otra sesión) · **Ronda:** r01 · 2026-11-15
- **Copia:** git desconectada en HEAD `a9f402f` («wip local: T-142»). El plan y el código se leyeron antes que `analisis-tecnico.md`.

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| `pytest -q -p no:cacheprovider tests/test_t142_cadena_b.py` (A) | 30 pasan |
| Suite completa de A (una vez, `python -m pytest -q -p no:cacheprovider` en `bloque_a/11_Ejecutor`) | 6 122 pasan, 0 fallan (20 min), por encima de la línea base |
| `pytest -q bloque_b/11_Ejecutor` | 176 pasan (línea base 174); el Bloque B no se tocó (`git show --stat HEAD`) |
| `.venv/bin/python .docs/scripts/cadena_a_b.py --trabajo <dir> --sonda-sin-correspondencia` | código 0: 3 enviables, 1 enviada (OPP-2024-0002 → `divisas_materias_primas`, PT30 autorizada con la opción de B, ENTREGADA, VIGILAR), paquete de B **válido** contra su esquema V2.0, vuelta CT-04 registrada (RET-2024-0001, APLICADA); 2 no enviadas por `SIN_CORRESPONDENCIA_AMBITO` (USD/JPY, USD/MXN). Sonda: B V2.1 admite la petición sin clave y su Director elige `divisas_materias_primas` para USD/JPY |
| `revisores/r02_cadena_doce_tipos.sh` (los doce tipos activos en A) | código 0: 30 enviables, 2 enviadas (AUD/USD y ETH-USD), las dos ENTREGADA y válidas, 2 RET; 28 sin correspondencia, todas cerradas con su código |
| Importaciones cruzadas | ninguna: `grep` de `import`/`sys.path` de `bloque_b` en `bloque_a/11_Ejecutor` y al revés, vacío; `cadena_a_b.py` importa solo `bloque_a` y usa B por `python -m bloque_b.cli` y sus ficheros como datos (regla 8) |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | La petición tiene exactamente las claves de primer nivel del Anexo B.1 (lectura propia del bloque ```json de B.1 en `r01`); `objeto` ⊆ B.1 + `clave_universo` (la extensión del ejemplo de B); `marco_invertibilidad` ⊆ B.1; `origen`, `nivel` y `prioridad` dentro de sus enumeraciones; encargo tal cual + `x_clave_universo`. El ejecutor de B la admite (`cadena_a_b.py`, `r02`). Sin correspondencia no se envía (`SIN_CORRESPONDENCIA_AMBITO`): cambia lo previsto en el plan («B responde AMBITO_INDETERMINADO»), porque la sonda muestra que B V2.1 no lo hace y elegiría un ámbito por su cuenta; está documentado como `[PROPUESTO]` en INC-T142-01 y en el registro de decisiones del operador. La clave no se inventa (mutante `clave_inventada` muerto) |
| CA-2 | sí | `cadena_a_b.py` termina con 1 paquete de B ENTREGADO y válido; con doce tipos, 2 |
| CA-3 | sí | 30 pruebas nuevas en A; B sin tocar y 176 ≥ 174; ruff 2838 ≤ 2838, mypy A 109 ≤ 109, mypy B 159 ≤ 159, goldens CT coinciden, gates ligeros (secretos, refs vivas, NFC, corpus 695) en verde. `./tools/check_all.sh` no se lanzó por instrucción (lo pasa la sesión coordinadora) |

## Ataques (`revisores/`)

- `r01_ataques_peticion.py` (41 casos, 27 OK y 14 observaciones): B.1 campo a campo, determinismo, campos de más (un campo no `x_` se rechaza por el esquema de A; las `x_` viajan), `x_clave_universo` previa, tipos de activo, horizontes (H5 viaja; H6 se rechaza), datos protegidos R8 en la tesis, paquetes rotos (clases lista o `None`, opciones dict, `run_id` entero, NaN, opción duplicada en otra clase: todos cierran con `ErrorCadenaB`), configuración rota, no mutación, CT-04, y envío de las peticiones raras al ejecutor de B por su CLI.
- `r02_cadena_doce_tipos.sh`: la cadena con los doce tipos activos.
- `r03_mutantes.py` (copia desechable `qa17_mut`, ya borrada): 10 mutantes; 9 muertos y 1 vivo (`muta_paquete`, ver H-05).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01`, casos «tipos_secundarios…»: en la opción, `tipos_secundarios = "RF"` o `["XYZ", "RF", "RF", None]` | Esperado: falla cerrado o solo tipos de los doce, sin repetir. Obtenido: `["MON", "R", "F"]` (el texto se trocea en letras) y `["MON", "XYZ", "RF", "RF", None]`. El ejecutor de B admite la petición con `["M", "O", "N"]` y la lleva hasta DETENIDA_EN_PUERTA. Solo se valida el `paquete_para_bloque_B`, no la parte de la opción que entra en la petición | Validar `tipos_secundarios` (lista, `codigo_clase` del esquema de A, sin repetir) o validar la opción contra su `$defs` antes de usarla; si no, `ENTRADA_B_INVALIDA` | abierto |
| H-02 | media | `r01`, casos «R8 (correo / clave / IBAN) en la tesis» | Esperado (R8 del Documento 0 de A: ningún mensaje lleva credenciales ni datos personales): el Broker no construye ni escribe la petición. Obtenido: se construye y `cadena_a_b.py` la escribiría en `peticiones/`; el Bloque B la rechaza íntegra (DATOS_SENSIBLES, incidencia de seguridad) y el CT-04 de vuelta queda como ENVIADA_A_BLOQUE_B. Además, `contenido_sensible` de A no detecta el correo ni `api_key=…` (solo el IBAN), así que A no lo frena antes | Comprobar la petición con `contenido_sensible` antes de devolverla (código propio, p. ej. `DATOS_PROTEGIDOS`) y no escribirla; anotar para T-57 que los detectores de A y de B no cubren lo mismo | abierto |
| H-03 | media | `r01`, casos «Configuración rota»: `cadena_b.peticion.nivel: N9`, `prioridad: URGENTISIMA`, `idioma: 123`, clave `" liquidez_eur "` | Esperado: falla cerrado (`CONFIGURACION_CADENA_B`), como cuando falta el valor. Obtenido: se construye con los valores tal cual; el ejecutor de B admite `nivel: N9` y sigue (EN_PAUSA_PUNTO_CONTROL) | Validar `nivel`, `prioridad` y `perfil_invertibilidad` contra las enumeraciones de B.1 (en la configuración, con su origen), `idioma` como texto, y las claves de la tabla sin espacios | abierto |
| H-04 | baja | `r01`, caso «Sonda sin correspondencia…»: encargo de A con `x_clave_universo: "cobre"` y símbolo sin fila, `exigir_correspondencia=False` | Esperado (docstring: «ni `x_clave_universo` ni `objeto.clave_universo`, nunca una clave supuesta»): sin clave. Obtenido: la petición de la sonda arrastra `x_clave_universo: "cobre"` del paquete | En la rama sin clave, quitar `x_clave_universo` del encargo copiado | abierto |
| H-05 | baja | `r03_mutantes.py`, mutante `muta_paquete` (`encargo = entrada`, sin copia) | Esperado: lo mata `test_no_muta_el_paquete`. Obtenido: sobrevive, porque el fixture `ciclo` es de módulo y las pruebas anteriores ya han dejado la clave en el paquete cuando la prueba toma su copia de «antes» (con el mutante, el paquete sí se muta) | En esa prueba, usar una copia propia del paquete (`copy.deepcopy(paquete)`) antes de la primera llamada | abierto |
| H-06 | baja | `grep -n "T-142" sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` | La fila dice «Pendiente» con el ticket en QA, y la pregunta para el operador de INC-T142-01 («¿quiere que el Bloque A aprenda de los veredictos del Bloque B?») no figura en la deuda | Al cerrar: fila de T-142 al día, la pregunta en los pendientes del operador (T-57) y los medios de esta QA con su ID | abierto |

**Observaciones (no son hallazgos):**

- El CT-04 de una petición que B rechaza sigue siendo `ENVIADA_A_BLOQUE_B`. Es correcto (el Broker la envió) y el texto lleva «admisión RECHAZADA; motivo …».
- Un `paquete_para_bloque_B` con elementos que no son objetos se tolera: se ignoran y se usa el de la opción. No es un fallo abierto.
- `horizonte_principal` que no está en `horizontes` se reenvía: es el esquema de A (HT-09 C17–C19) el que debe impedirlo, no el Broker. B elige su horizonte dominante con su ámbito y, si no está en la petición, toma el primero de `horizontes`, que no tiene por qué ser el principal de A. Poner el principal el primero sería una mejora sin coste, pero B.1 no la pide.
- Los códigos de los ámbitos de la tabla se comprueban frente a `ambitos_ejemplo.yaml` de B solo en `cadena_a_b.py` (código 2), no en el módulo. Es coherente con la regla 8.

## Veredicto

**APTO** (r01). Se cumplen CA-1 a CA-3 y no hay hallazgos críticos ni altos. El cambio frente al plan (sin correspondencia no se envía) está justificado con la sonda y registrado como `[PROPUESTO]`. H-01 a H-03 (medios) y H-04 a H-06 (bajos) pasan a la deuda técnica con su ID si no se corrigen antes de cerrar. El cierre (estado, deuda, diario, commit) lo hace la sesión coordinadora: este revisor no hace commit.
