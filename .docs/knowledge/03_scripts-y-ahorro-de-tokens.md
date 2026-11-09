# 03 · Scripts: hacerlo una vez, ejecutarlo siempre

**La regla.** Todo lo que un agente hace más de una vez se convierte en un script de `.docs/scripts/`. La primera vez cuesta tokens pensarlo y escribirlo; las siguientes, basta con ejecutarlo. Además, un script hace siempre lo mismo, mientras que un agente puede hacerlo distinto cada vez.

**Cuándo crear uno.**

- Vas a repetir una secuencia de órdenes (probar, comprobar, generar, publicar, migrar, contar).
- Has tenido que razonar varios pasos para algo mecánico.
- Otra persona o el otro agente va a necesitar lo mismo.

**Cómo escribirlo.**

1. Empieza por `source "$(dirname "$0")/common.sh"`: así tienes modo estricto, la raíz del repositorio en `$RAIZ`, el Python del proyecto en `$PY` y las variables de `.env`.
2. Los secretos, solo desde `.env` (con `requiere_var NOMBRE`). Nunca escritos en el script ni en sus argumentos.
3. Cabecera con qué hace y cómo se usa; mensajes de error claros; que falle cerrado (si algo no cuadra, para y lo dice).
4. Que no destruya nada: crea, añade o comprueba; no borra ni sobrescribe sin que se le pida.
5. Pruébalo en una copia antes de usarlo en el repositorio.
6. Apúntalo en la tabla de scripts de `.docs/README.md`.

**Cuándo no.** Una tarea única o que exige juicio en cada paso (diseñar, revisar, decidir). Ahí el script, como mucho, prepara los datos.
