# Memoria de los agentes del Robot Investor

Memoria compartida entre Claude y Astra. Sirve para que cada agente arranque sabiendo lo que el otro y él mismo aprendieron, sin depender del historial de una conversación.

## Estructura

| Carpeta | Quién escribe | Qué guarda |
| --- | --- | --- |
| `.docs/memoria/compartida/` | Los dos agentes y el operador, cada uno con entradas firmadas | Lo que necesitan los dos: estado del proyecto, reglas del operador y convenciones |
| `.docs/memoria/claude/` | Solo Claude | Lecciones y contexto de trabajo propios de Claude |
| `.docs/memoria/<agente>/` (p. ej. `astra`) | Solo ese agente | Igual, para cada agente. **Cada agente crea su carpeta la primera vez**: `.docs/scripts/memoria.sh <agente> …` la crea con su `INDICE.md` |

Cada carpeta tiene un `INDICE.md` con una línea por entrada. **Se lee primero el índice y después solo las entradas necesarias**: la memoria es un almacén indexado, no contexto que se carga entero (regla 6 de `CLAUDE.md`).

## Cuándo leer y cuándo escribir

- **Al empezar una sesión:** este LEEME, el índice de `compartida/`, el de tu carpeta y el de la carpeta del otro agente. Abre las entradas que toquen la tarea.
- **Al terminar una tarea o una sesión:** escribe lo que a tu yo futuro o al otro agente le ahorraría tiempo o errores. No escribas lo que ya está en el código, en la Constitución o en la deuda técnica: enlázalo.
- **Al pasar una tarea al otro agente:** el traspaso va en `handoff.md`, dentro del ticket (`.docs/tickets/T-NN/`), no en la memoria.
- **Lo que pasó cada día** va al diario (`.docs/diario/`); la memoria guarda solo lo que conviene saber siempre.

## Formato de una entrada

Un archivo por entrada: `<AAAA-MM-DD>_<tema-corto>.md`, de como mucho unas 40 líneas. Lo más cómodo es crearla con `.docs/scripts/memoria.sh`, que pone la cabecera, la indexa y, con `--sustituye`, marca la anterior.

```markdown
---
id: <carpeta>/<AAAA-MM-DD>_<tema-corto>
autor: claude | astra | operador
fecha: AAAA-MM-DD
tipo: estado | decision | regla | leccion | convencion | traspaso | contexto
etiquetas: [marco-c, orquestador, …]
fuente: <commit, ruta del repo o enlace que lo respalda>
vigencia: vigente | sustituida por <id> | caduca AAAA-MM-DD
---

<Contenido: el hecho, por qué importa y cómo aplicarlo.>
```

Al crear una entrada, añade su línea al `INDICE.md` de la carpeta: `| id | tipo | resumen de una línea | vigencia |`.

## Reglas

1. **Escribe solo en tu carpeta y en `compartida/`.** Nunca edites ni borres entradas de otro agente.
2. **Las entradas no se reescriben: se sustituyen.** Para corregir una, crea otra con la información nueva, y en la vieja cambia solo `vigencia` a `sustituida por <id>` (si es tuya, o si está en `compartida/`). En el índice, marca la vieja como sustituida.
3. **La memoria no es la fuente de verdad.** Mandan la Constitución, los Documentos 0, el código y la deuda técnica. Si una entrada los contradice, gana la fuente y la entrada se sustituye. Si dos entradas de agentes distintos se contradicen, se anota en `compartida/` y se pregunta al operador.
4. **Lo que dependa del operador va a la deuda técnica**, no a la memoria.
5. **Repositorio público.** Nada de secretos, credenciales, datos personales, ni datos financieros o del perfil inversor del operador.
6. **Poda.** Cuando un índice pase de unas 100 líneas, mueve las entradas sustituidas o caducadas a `archivo/` dentro de la misma carpeta.
