# Marco común de C y sobre CT-G-02 — V0.1 (provisional, 0.x)

Fecha: 5 de noviembre de 2026. Fase 1 de la Constitución V0.3.

## Contenido

| Carpeta o archivo | Para qué sirve |
| --- | --- |
| `esquemas/ct-g-02_0.1.0.schema.json` | Esquema JSON del sobre común de valoración (forma) |
| `esquemas/generar_esquema.py` | Genera el esquema; se edita aquí, no a mano en el JSON |
| `validador/validar_sobre.py` | Esquema + reglas V-01 a V-23 (código determinista, sin LLM) |
| `pruebas/generar_casos.py` | Genera 3 sobres válidos y 51 inválidos (datos simulados) |
| `pruebas/ejecutar_pruebas.py` | Ejecuta todos los casos y comprueba la regla esperada de cada uno |

El documento explicativo es la Constitución de C: «Marco común de C y sobre CT-G-02 — V0.1».

## Cómo se ejecuta

```
pip install jsonschema
python3 esquemas/generar_esquema.py > esquemas/ct-g-02_0.1.0.schema.json
python3 pruebas/generar_casos.py
python3 pruebas/ejecutar_pruebas.py
python3 validador/validar_sobre.py sobre.json contexto.json
```

Resultado esperado de las pruebas: `TODAS LAS PRUEBAS PASAN`.

## Qué está comprobado y qué no

- Comprobado: el esquema valida, el validador acepta los 3 sobres válidos y rechaza cada
  uno de los 51 inválidos por la regla que rompe.
- No comprobado: ningún sobre real. Los datos de prueba son simulados. Falta pasar un
  sobre real de `C-DIV` (pendiente de que se comparta su desarrollo) y de `C-RV` (Fase 2).
- Valores de partida (no ratificados): topes de confianza Q 0,80, S 0,60, K 0,40; factor
  0,75 si el doble análisis discrepa; los seis episodios de estrés y los ocho factores.
- El esquema sigue en `0.x`: admite cambios compatibles. Se congela en `1.0.0` tras dos
  perfiles reales y su consumo por D.
