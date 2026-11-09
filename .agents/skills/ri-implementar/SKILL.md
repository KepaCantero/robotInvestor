---
name: ri-implementar
description: Fase 2 de 4 del flujo de trabajo del Robot Investor. Úsala para escribir o cambiar código, esquemas JSON, migraciones o configuración a partir de un plan aprobado (.docs/tickets/T-NN/README.md), o cuando pidan «implementa», «programa», «corrige este hallazgo». Aplica las reglas de código del proyecto: determinista, falla cerrado, esquema primero, números de configuración, mock antes que API.
---

# Implementar una tarea del Robot Investor

Fase 2 de 4. Antes: `ri-planificar`. Después: `ri-probar`.

**Requisito:** existe `.docs/tickets/T-NN/README.md` con su puerta superada. Si no existe, vuelve a `ri-planificar`. Si vienes a corregir hallazgos de QA, el requisito es `qa.md` con los hallazgos abiertos.

## Reglas de código (innegociables)

1. **Determinista.** Python sin LLM en la ruta de decisión, control o ejecución. Los agentes de IA proponen; el código valida, limita y ejecuta.
2. **Falla cerrado.** Ante un dato ausente, caducado, inválido o ambiguo: error explícito o rechazo con motivo. Nunca un valor inventado ni un «por defecto» silencioso.
3. **Valida antes de mutar.** Si cualquier comprobación falla, el estado queda exactamente como estaba.
4. **Ningún número a mano.** Umbrales, tolerancias y presupuestos salen de la configuración o del Documento 0.
5. **El esquema es la definición.** Primero el esquema JSON del contrato, después el código que se valida contra él; nunca al revés.
6. **Mock antes que API.** Nada de red en las pruebas; la hora se inyecta, no se lee del reloj.
7. **Historiales encadenados por hash.** Solo se añaden entradas; jamás se reescriben.
8. **Repo público.** Ni secretos, ni credenciales, ni datos personales o financieros del operador.
9. **Cambio mínimo y de una sola pieza.** No reformatees código ajeno. Los paquetes entregados de los bloques solo se tocan en la fase que los trabaja.
10. **Las cuotas de ruff y mypy solo bajan** (`tools/cuotas.txt`).

## Específico del marco común de C (`sistema_global/marco_comun_c/`)

- Si cambias algo que entra en la huella del esquema del estado (constantes importadas, atributos, estructuras), registra la versión con `python3 validador/migraciones.py --registrar-esquema V0.xx` y añade una migración MIG-xxx con su lista `cambia`. Nunca toques las rutas `PROHIBIDAS` (por ejemplo `cfg.nivel_autonomia`).
- Las versiones se comparan como tuplas de enteros, no como texto.
- Las operaciones que mutan el estado llevan el decorador `@_seguro`; `integridad()` tiene que seguir pasando.
- Cada error nuevo tiene código propio (O-xx, G-xx, H-xx…) registrado en el LEEME.

## Procedimiento

1. Lee el plan y solo los archivos que vas a tocar.
2. Escribe primero las pruebas de los criterios de aceptación y comprueba que fallan; después el código.
3. Avanza en pasos pequeños y ejecuta las pruebas del módulo tras cada paso.
4. Si el plan resulta inviable o tienes que desviarte, anótalo. Si la desviación cambia el alcance o una decisión del operador, para y pregunta.
5. Actualiza el LEEME o README de la pieza (tabla de archivos, códigos de error, comandos).
6. Escribe `.docs/tickets/T-NN/analisis-tecnico.md`:
   - archivos cambiados y por qué;
   - decisiones tomadas y desviaciones del plan;
   - límites conocidos;
   - comandos exactos para probarlo.

## Puerta de salida

- [ ] Las pruebas del módulo pasan.
- [ ] `analisis-tecnico.md` escrito.
- [ ] Si otro agente hará la QA: commit en `develop` con mensaje en español, prefijo de área (`motor:`, `contratos:`, `docs:`…) y `[pendiente QA]` al final del título (`.docs/scripts/commit.sh` hace gate, commit y push); `handoff.md` en el ticket; estado `EN QA`.

## Scripts: lo repetible, automatizado

Antes de hacer algo a mano, mira `.docs/scripts/` (tabla en `.docs/README.md`). Si vas a hacer algo que se repetirá, escríbelo como script, guárdalo ahí y apúntalo en esa tabla: la próxima vez se ejecuta y no se gastan otra vez los mismos tokens. Cómo: `.docs/knowledge/03_scripts-y-ahorro-de-tokens.md`. Los secretos, solo desde `.env` a través de `.docs/scripts/common.sh`.

