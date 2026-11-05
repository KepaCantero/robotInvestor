# Marco común de C, sobres CT-G-02 y CT-G-01, K (datos de corte), Orquestador, Contradictor, consola N y control de riesgo F y ejecución G y vigilancia H — V0.9 (provisional, 0.x)

Fecha: 5 de noviembre de 2026 (V0.9: añade H, la vigilancia de posiciones, y el cierre de posiciones en G; V0.8 añadió G, la ejecución con intermediario simulado, y su conciliación; V0.7 añadió F). Fase 1 de la Constitución V0.3.

## Contenido

| Carpeta o archivo | Para qué sirve |
| --- | --- |
| `esquemas/ct-g-02_0.1.0.schema.json` | Esquema JSON del sobre común de valoración (forma) |
| `esquemas/generar_esquema.py` | Genera el esquema; se edita aquí, no a mano en el JSON |
| `validador/validar_sobre.py` | Esquema + reglas V-01 a V-23 (código determinista, sin LLM) |
| `pruebas/generar_casos.py` | Genera 3 sobres válidos y 51 inválidos (datos simulados) |
| `pruebas/ejecutar_pruebas.py` | Ejecuta los casos del sobre CT-G-02 y comprueba la regla esperada de cada uno |
| `esquemas/ct-g-01_0.1.0.schema.json` y `esquemas/generar_esquema_encargo.py` | Esquema del encargo CT-G-01 |
| `validador/validar_encargo.py` | Reglas E-01 a E-15 del encargo y R-00 a R-10 (el sobre responde al encargo) |
| `pruebas/pruebas_encargo.py` | Genera, guarda en `pruebas/encargos/` y ejecuta los casos del encargo |
| `esquemas/k-sello_0.1.0.schema.json` y `esquemas/generar_esquema_sello.py` | Esquema del sello de corte de K |
| `validador/k_calidad.py` | K: reglas de calidad Q-01 a Q-13, emisión del sello, validación del sello (S-01 a S-13) y caducidad |
| `pruebas/pruebas_k.py` | Casos de K (sellos válidos, entradas inválidas, sellos alterados, caducidad); guarda en `pruebas/k/` |
| `validador/orquestador.py` | Orquestador: máquina de estados de expedientes y posiciones, presupuestos, idempotencia, historial encadenado por hash (códigos O-00 a O-16) |
| `esquemas/ct-g-03_0.1.0.schema.json` y `esquemas/generar_esquema_contradictor.py` | Esquema del informe del Contradictor CT-G-03 |
| `validador/validar_contradictor.py` | Reglas C-01 a C-10 del informe |
| `pruebas/pruebas_contradictor.py` | 37 comprobaciones del informe |
| `validador/control_f.py` | F: control de riesgo (reglas F-01 a F-11), informe CT-G-08 y su verificación por recálculo (CF-01 a CF-08) |
| `pruebas/pruebas_control_f.py` | 75 comprobaciones de F y de su integración en el Orquestador |
| `validador/consola.py` | N mínimo: panel verde/ámbar/rojo, cola de decisiones del operador y avisos pendientes (solo lectura) |
| `pruebas/pruebas_consola.py` | 41 comprobaciones de la consola |
| `pruebas/pruebas_orquestador.py` | 176 comprobaciones del Orquestador (transiciones, actores, caducidad, presupuesto, reloj, integridad) |

El documento explicativo es la Constitución de C: «Marco común de C y sobre CT-G-02».

## Cómo se ejecuta

```
pip install jsonschema
python3 esquemas/generar_esquema.py > esquemas/ct-g-02_0.1.0.schema.json
python3 pruebas/generar_casos.py
python3 pruebas/ejecutar_pruebas.py
python3 esquemas/generar_esquema_encargo.py > esquemas/ct-g-01_0.1.0.schema.json
python3 pruebas/pruebas_encargo.py
python3 esquemas/generar_esquema_sello.py > esquemas/k-sello_0.1.0.schema.json
python3 pruebas/pruebas_k.py
python3 esquemas/generar_esquema_contradictor.py > esquemas/ct-g-03_0.1.0.schema.json
python3 pruebas/pruebas_contradictor.py
python3 pruebas/pruebas_orquestador.py
python3 pruebas/pruebas_consola.py
python3 pruebas/pruebas_control_f.py
python3 pruebas/pruebas_ejecucion_g.py
python3 pruebas/pruebas_vigilancia.py
python3 validador/validar_sobre.py sobre.json contexto.json
```

Resultado esperado de cada script de pruebas: `TODAS LAS PRUEBAS PASAN`.

## Qué está comprobado y qué no

- Comprobado en H (`validador/vigilancia.py`) y en el cierre de G (`cerrar`): 41 comprobaciones con intermediario simulado; reglas H-01 a H-09. H aplica solo condiciones de salida ya declaradas, no cierra con un precio ausente o viejo (avisa) y el cierre lleva a cero la posición neta real del intermediario antes de pasar a CERRADA. Límites: solo cierre total (la reducción parcial sigue pendiente, T-12); solo condiciones sobre el precio; H no tiene reloj propio; el cierre a mercado no es de solo reducción en el simulador; umbrales de 15 min y 72 h [PROPUESTO].

- Comprobado en G (`validador/ejecucion_g.py`): 50 comprobaciones con un intermediario simulado; códigos OK, G-01..G-06, G-08. Tras enviar órdenes, cualquier fallo se trata como estado incierto (G-08) con aviso, nunca como «sin efectos»; una posición sin stop se cierra o se alerta. `conciliar` compara Orquestador e intermediario (cantidad, sentido, activo, stop, stop huérfano). Límites: una posición por instrumento; no hay reducir/cerrar posiciones ni redimensionar el stop; sin conversión de divisa; el disparo del stop no se simula; el intermediario es simulado y los actores no se autentican (ver deuda técnica).

- Comprobado en CT-G-01: 4 encargos válidos, 46 inválidos y 21 comprobaciones de respuesta; el cruce valida antes ambos mensajes y contrasta con el sello de K (E-16, R-11, R-12).
- Comprobado en el Orquestador: 176 comprobaciones con datos simulados; códigos O-00 a O-17 (O-17: objeción del Contradictor). Límites: la cadena de hashes del historial detecta alteración pero no está anclada fuera (use `cabezas()` y un registro de solo añadir); no hay reloj real ni persistencia; el Contradictor (CT-G-03) no se exige por defecto y su independencia es declarada, no comprobada; las condiciones de reapertura de `observar` no se verifican solas; el resultado de F no se verifica de forma independiente; todos los umbrales son [PROPUESTO].
- Comprobado en K: 7 sellos válidos, 82 entradas inválidas, 38 comprobaciones del sello y 16 de caducidad. Datos simulados; no hay proveedor de datos elegido.
- Límites de K: `hash_sello` detecta alteración pero no es una firma; la inmutabilidad real exige un registro de solo añadir. Q-10 no compara valores; `sello_id` no es único por sí mismo.
- Comprobado: el esquema valida, el validador acepta los 3 sobres válidos y rechaza cada
  uno de los 51 inválidos por la regla que rompe.
- No comprobado: ningún sobre real. Los datos de prueba son simulados. Falta pasar un
  sobre real de `C-DIV` (pendiente de que se comparta su desarrollo) y de `C-RV` (Fase 2).
- Valores de partida (no ratificados): topes de confianza Q 0,80, S 0,60, K 0,40; factor
  0,75 si el doble análisis discrepa; los seis episodios de estrés y los ocho factores.
- El esquema sigue en `0.x`: admite cambios compatibles. Se congela en `1.0.0` tras dos
  perfiles reales y su consumo por D.
