# Seguridad y operación (SC-7): que el robot no se rompa ni lo rompan (propuesta de diseño de Claude)

De: Claude, 11-11-2026. Estado: **PROPUESTA PARA DISCUTIR**. No hay nada que implementar: el operador está decidiendo la arquitectura de los bloques antes de construir (relevo de Astra, §0 bis). Copia en el repositorio del documento que el operador revisó con Claude.

## 1. Respuesta corta

SC-7 pone en práctica las once reglas de seguridad de la Constitución (§12) y añade lo que ningún diseño cubre: dónde corre el robot, cómo se vigila, cómo se actualiza y cómo se recupera. Hoy existen el estado guardado con huella y firma (V0.42 a V0.49) y la detección de secretos del repositorio. Faltan la autenticación real (T-01), el bloqueo de órdenes reales en L0 (T-30), la bóveda, las copias y los simulacros.

Idea central: **que un fallo nunca llegue al dinero sin pasar por algo que no depende del robot:** los stops nativos, los topes de la clave en la entidad y un vigilante en otra máquina. Se propone:

1. **Cuatro zonas de confianza:**
    - lectores aislados;
    - inteligencia;
    - control;
    - bóveda e intermediario.

    Cada zona solo puede tocar lo de la siguiente por un camino cerrado.
2. **Dónde corre, con dinero real:** un servidor en la UE para el robot y el vigilante en otro sitio, para que no caigan juntos.
3. **Claves solo en la bóveda,** usadas por referencia, con topes fijados en la propia entidad.
4. **Copias cifradas y restauración probada** cada mes; el intermediario es la verdad de lo que se tiene.
5. **Simulacros trimestrales y una carta de instrucciones** para la persona de confianza y los herederos.

## 2. Amenazas y fallos que cuestan dinero

| Amenaza | Ejemplo | Qué la frena |
| --- | --- | --- |
| Robo de la clave de operación | La clave queda en un fichero, un registro o un chat | Bóveda; topes de importe y frecuencia en la entidad; lista de direcciones permitidas si la entidad la ofrece; rotación |
| Instrucciones escondidas en texto externo | Una noticia o un PDF que dice «vende todo» | Lectores aislados con esquema cerrado (SC-11); el texto externo nunca llega como instrucción (§12) |
| Agente confundido o manipulado | Propone una orden absurda | F en código, límites nominales y aprobación con las cifras de F |
| Suplantación del operador | Alguien aprueba en su nombre | Autenticación y segundo factor por un canal distinto del chat (T-01) |
| Caída de la máquina | Disco roto, corte de luz o de red | Stops nativos; vigilante en otra máquina; copias |
| Estado dañado | Un fichero corrupto o manipulado | Estado con huella y firma; integridad comprobada al cargar; restauración probada |
| Actualización con fallo | Versión nueva que rompe algo | Gates del repositorio, entorno de pruebas, ventana fuera de mercado y vuelta atrás |
| Proveedor de IA caído o encarecido | El modelo no responde o sube de precio | Adaptador intercambiable, ruta determinista y presupuesto duro |
| Fuga de datos personales | Algo personal acaba en el repositorio público | Nada personal en el repositorio (D-47) y detección de secretos en cada commit |
| Operador ausente | Enfermedad o fallecimiento | Hibernación, persona de confianza y carta de instrucciones |

## 3. Qué hay hoy y qué falta

**Decidido en la Constitución (§12):**

- Credenciales en la bóveda, usadas por referencia y nunca en el contexto de un agente.
- Claves separadas con topes.
- Entornos aislados.
- Lectores aislados.
- La inyección detectada es un incidente.
- Aprobaciones con segundo factor.
- Límites que no dependen de agentes.
- Registro que no se puede reescribir.
- Copias y restauración probada, con exportación en formatos abiertos (D-40).
- Persona de confianza solo de lectura.
- Nada personal en el repositorio (D-47).

**En código:**

- Estado guardado con huella (V0.42) y firmado con clave (V0.45), con rotación de la clave (V0.49).
- Jornada con reinicios (V0.44).
- Detección de secretos en el repositorio.
- Secretos de desarrollo solo en un fichero local fuera del repositorio.

**Falta:**

- Dónde corre y cómo se separa el vigilante.
- La bóveda real.
- Autenticación de actores (T-01) y bloqueo de órdenes reales en L0 (T-30).
- Copias y su prueba.
- Vigilancia, actualizaciones y simulacros.
- Qué pasa si el operador falta.

## 4. Dónde corre el robot

| Opción | A favor | En contra |
| --- | --- | --- |
| El ordenador personal del operador | Sin coste | Se apaga, se usa para otras cosas y puede infectarse; depende de la luz y la red de casa |
| Un miniordenador dedicado en casa | Barato y solo para el robot | Sigue dependiendo de la luz y la red de casa; sin copia fuera si no se prepara |
| Un servidor alquilado en la UE | Encendido siempre; dirección fija, que permite a la entidad aceptar solo esa dirección; copias sencillas | Coste mensual; los datos están en un tercero y hay que cifrarlos |

**Propuesta [PROPUESTO].**

- **Fases 1 y 2, sin dinero real:** donde se desarrolla, con entornos separados.
- **Desde la Fase 3:**
    - el robot en un servidor en la UE, con disco cifrado y acceso solo por un canal cifrado con clave;
    - el vigilante en otro sitio (el miniordenador de casa o un segundo proveedor), para que una sola caída no se lleve a los dos;
    - N, accesible solo desde la red privada del operador o por ese canal cifrado.

El coste estimado va de unos pocos euros a unas decenas al mes. Lo mide I como parte del coste del robot.

## 5. Zonas de confianza

Diagrama del documento («Cada zona solo toca la siguiente por un camino cerrado»):

1. **Lectores aislados (SC-11):** leen web, PDF y noticias, sin cartera, sin claves y sin herramientas de acción. Pasan a la zona 2 solo datos con esquema cerrado.
2. **Inteligencia (agentes y Broker conversacional):** proponen y explican, sin claves y sin enviar órdenes. Pasan propuestas a la zona 3.
3. **Control (Orquestador, F, G y kill-switch):** código determinista, sin IA en la ruta de decisión. Solo G usa la clave de operación, que recibe por referencia de la bóveda.
4. **Bóveda** (claves cifradas, nunca en prompts ni registros) **e intermediario** (stops nativos y topes de la clave; protege aunque el robot caiga). Al intermediario solo le llegan órdenes con tope.

Por fuera, el operador entra en la zona de control con segundo factor y por un canal fuera del chat. El vigilante, desde otra máquina, vigila el latido de esa zona.

## 6. Claves, credenciales y accesos

| Clave | Quién la usa | Límites | Cuándo se cambia |
| --- | --- | --- | --- |
| Operación del intermediario | Solo G, por referencia | Importe por orden y órdenes por día fijados en la entidad; solo desde la dirección del servidor si la entidad lo admite | Periódicamente y tras cualquier incidente |
| Lectura del intermediario | G, F y K | Solo lectura | Periódicamente |
| Proveedores de IA | Adaptador de SC-10 | Tope de gasto en el propio proveedor | Periódicamente |
| Datos | K | Las de su licencia | Al renovar |
| Firma del estado y del diario | Orquestador | — | Con el procedimiento de rotación ya existente (V0.49) |
| Canal de avisos | Orquestador y vigilante | Solo enviar | Periódicamente |
| Acceso del operador a N | Operador | Segundo factor | Si se pierde el dispositivo |
| Persona de confianza | Ella | Solo lectura, revocable | Cuando el operador lo decida |

**La bóveda.** Un almacén de secretos cifrado cuya clave maestra no vive en el mismo disco: el gestor de secretos del proveedor del servidor o uno cifrado localmente [PROPUESTO]. Las herramientas reciben una referencia, nunca el secreto.

**Lo que nunca contiene un secreto:** el repositorio, la configuración, los prompts, los registros, los avisos ni el chat. Si aparece en uno de ellos, se da por comprometido y se cambia (§12).

## 7. Copias, recuperación y continuidad

**Qué se copia:**

- el estado firmado;
- el diario;
- los libros operativo y fiscal;
- SC-1 (perfil, mandatos y política personal);
- los expedientes;
- la configuración;
- el almacén de K, lo que no se pueda volver a descargar.

**Cómo:** tres copias, en dos soportes distintos y una fuera del servidor, todas cifradas [PROPUESTO]. Se copia cada día y antes de cada actualización.

**Cuánto se puede perder:**

- **Datos:** como mucho un día. Lo que se tiene de verdad está en el intermediario, así que tras restaurar se concilia con él y se recupera el resto.
- **Tiempo:** volver a funcionar en horas. Mientras tanto, los stops nativos protegen y la cartera está en L1.

**Prueba:** cada mes se restaura la última copia en el entorno de pruebas y se comprueba la integridad. La exportación en formatos abiertos se prueba igual (D-40).

**Si el operador falta.**

- **Temporalmente:** hibernación (nada nuevo, protecciones intactas) y aviso a la persona de confianza (D-32).
- **Para siempre:** una **carta de instrucciones**, en papel o en un lugar seguro y nunca en el repositorio. Dice qué entidades guardan el dinero, cómo apagar el robot sin tocar las posiciones y a quién llamar. Los herederos tratan con las entidades, no con el robot.

## 8. Operación diaria

**Vigilancia.**

- El latido del plano de control lo comprueba el vigilante desde otra máquina.
- El panel de salud de N muestra cada bloque, los sellos de K, el presupuesto y el espacio en disco.
- Lo que exige actuar sale por el canal fuera del chat (diseño de N).

**Actualizaciones.**

1. Pasan los gates del repositorio y la batería de pruebas en el entorno de pruebas.
2. Se instalan en una ventana sin mercado abierto para las carteras activas, con el kill-switch de entradas puesto y las protecciones intactas.
3. Antes, una copia. Si algo falla, se vuelve a la versión anterior con su estado compatible (migraciones).
4. Las bibliotecas van con versiones fijadas, y cada mes se revisan sus avisos de seguridad.

**Simulacros trimestrales [PROPUESTO].**

| Simulacro | Qué se comprueba |
| --- | --- |
| Kill-switch | Cancela entradas, no toca protecciones y se rehabilita con la lista de la Constitución |
| Caída del servidor | El vigilante avisa, los stops siguen en la entidad y se recupera en el tiempo fijado |
| Restauración | La copia vuelve y concilia con el intermediario |
| Clave comprometida | Se revoca y se cambia sin perder protecciones |
| Proveedor de IA caído | La ruta determinista sigue y lo demás espera o baja a L1 |

**Incidentes:** cada uno se registra con causa y autopsia; los de seguridad disparan el kill-switch (§11).

## 9. Precisión, coste y orden

**Cómo se sabe que funciona:**

- simulacros superados;
- tiempo real de restauración frente al fijado;
- tiempo sin servicio;
- incidentes y su causa;
- secretos encontrados en el repositorio o en los registros (objetivo: cero);
- avisos de seguridad de bibliotecas sin atender.

N los muestra en el panel de salud.

**Coste:** el servidor y las copias, de unos pocos euros a unas decenas al mes. Cero tokens.

**Orden:**

- **Fases 1 y 2:** entornos separados, estado firmado (ya existe), bóveda local, copias cifradas con prueba mensual y detección de secretos (ya existe).
- **Antes de la Fase 3:**
    - autenticación (T-01) y bloqueo de órdenes reales en L0 (T-30);
    - servidor en la UE y vigilante en otra máquina;
    - topes de la clave y lista de direcciones en la entidad;
    - primer ciclo de simulacros;
    - carta de instrucciones.
- **Fase 3:** simulacros cada trimestre.

## 10. Preguntas para el operador

Todas son [PROPUESTO]; ninguna se decide sin el operador.

1. **Dónde corre con dinero real:** servidor en la UE y vigilante en otro sitio.
2. **La bóveda:** gestor de secretos del proveedor del servidor o uno cifrado localmente.
3. **Topes de la clave de operación y lista de direcciones permitidas** en la entidad, si los ofrece.
4. **Copias diarias, tres copias cifradas** y prueba de restauración mensual.
5. **Carta de instrucciones** para la persona de confianza y los herederos, fuera del repositorio.
6. **Simulacros cada trimestre** desde la Fase 3.
