# QA · T-184 · Clasificación temática y orden por calidad (PB-26)

## Ronda r01 · 24-11-2026 · Claude (revisor independiente; implementó Astra)

**Veredicto: NO APTO.** Dos hallazgos medios (H-01 y H-05) y cinco bajos (H-02, H-03, H-04, H-06 y H-07).

### Qué se revisó

- El código del PR 3: la rama `astra/encargos-bloque-a-c38-c47`, en la punta `2d99af6`, sobre `develop` `9ce57b2`. Es el commit `94c6a06`, con `altas_referencias.py`, el comando `alta-referencias` de `cli.py` y `test_t184_altas.py`, más el orden de imports de `5ef929b`. Se revisó en un worktree limpio.
- La vara de medir:
  - el plan para PB-26: preparación con «altas de 30 referencias de calidades variadas en TA-06, TM-11 y TF-04»; resultado esperado «… nivel D marcado como candidato a baja salvo única fuente de un dato»; criterio «0 inversiones; 100 % con temática válida»;
  - el Documento 0 V5.3, §13.3 (rúbrica, niveles), §13.4 (estados iniciales) y §13.5 (Registro de bajas).
- F7, F8 y F9 solo se recorren con `ht02.leer_fichas` y por sección; las altas se hacen sobre copias en `tmp_path`.

### Reproducción

| Comprobación | Resultado |
|---|---|
| `tests/test_t184_altas.py` y las de PB-26 de T-126 (`test_t126_pb26_pb48.py`, `test_t126_r02.py`) | Verde |
| La prueba nueva sin el cambio (sin `altas_referencias.py` y sin el comando de la CLI) | Falla, como debe |
| `.docs/tickets/T-184/mutantes.py`, el de Astra | Sus 2 mutantes mueren |
| `revisores/r01_mutantes.py`, 14 mutantes propios | **Viven los 14** (H-05) |
| `revisores/r01_ataques_altas.py`, 23 casos | 16 en verde y 7 en rojo (H-01 a H-04) |
| Cuotas sobre lo tocado, frente a `9ce57b2` | No suben: ruff con la configuración del gate da 0 en `altas_referencias.py`, `cli.py` y `test_t184_altas.py`; mypy de A da 102, igual que antes |
| Esquemas, corpus y R8 | Esquemas y corpus intactos. El comando escribe en el directorio operativo de la configuración, como `verificar-enlaces --aplicar` |

Lo que sí funciona:

- Treinta altas de calidades A a D, con los bordes 80, 65 y 50, sobre copias de los F7, F8 y F9 entregados cumplen PB-26 (b01): cada ficha en su sección, 0 inversiones de Q, desempate por año, nivel coherente y la D marcada.
- Un lote inválido a mitad no toca el catálogo real (b02).
- Rechaza inyección en el título, credenciales en la URL, Q booleana, real o fuera de rango, prefijo ajeno, temática mal formada, título multilínea o vacío y fecha imposible (b06).
- No duplica al repetir un lote (b07).
- Si otro escritor cambia el catálogo a mitad, el alta se rechaza y el cambio ajeno se conserva (b08).

Cómo reproducirlo, desde `bloque_a/11_Ejecutor`:

```bash
../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-184/revisores/r01_ataques_altas.py
```

Y, desde la raíz del repo:

```bash
.venv/bin/python .docs/tickets/T-184/revisores/r01_mutantes.py
```

### Hallazgos

#### H-01 · media · El alta reutiliza un REF-id dado de baja

- **Qué pasa.** `incorporar` solo mira los identificadores de las fichas vivas. Un id que figura en el «Registro de bajas» del mismo archivo (§13.5) se acepta. Desde ese momento, la ficha nueva queda a la sombra de la baja:
  - `_guardar_lote_evidencia` descarta sus piezas (`continue` por la baja);
  - `para_clase` la retira, si la baja es de F9.

  Es decir, la referencia se incorpora y el ejecutor la ignora en silencio.
- **Cómo reproducirlo.** Ataque b03.
- **Corrección exacta.**
  - En `incorporar`, `ids |= {rid for rid, _ in mantenimiento_fuentes.bajas_registradas(lineas)}`.
  - En F9, también los del registro de bajas de la instancia (`F9_bajas.md` del almacén) si existe.
  - El mensaje de error dice «identificador dado de baja».
- **Prueba de regresión.** b03.

#### H-02 · baja · Validación de entrada incompleta

- **Qué pasa.**
  - Admite una `fecha_publicacion` futura (2099-01-01): entra con «Año: 2099», que además `RE_ANIO` no lee (b04).
  - Admite enlaces con espacios, paréntesis o «<», que se escriben tal cual en el Markdown y lo convierten en otro enlace (b05).
- **Corrección exacta.**
  - Rechazar una fecha posterior al día de la instancia (`--as-of` o el reloj del bloque).
  - Exigir `re.fullmatch(r"https?://[^\s<>()\[\]\"'`]+", url)` además de `urlsplit`.
- **Prueba de regresión.** b04 y b05, con sus tres URL.

#### H-03 · baja · La D que es única fuente de un dato no se puede declarar

- **Qué pasa.** El §13.3 y el resultado esperado de PB-26 dicen que la D es «candidata a baja salvo que sea la única fuente de un dato necesario, declarado». El lote no tiene forma de declararlo, así que toda D sale «candidata a baja» (b09).
- **Corrección exacta.** Campo opcional `unica_fuente_de`: una cadena de una línea, no vacía, saneada como el título. Con él se escribe «- **Seguimiento:** única fuente de un dato necesario: …» en lugar de «candidata a baja». Solo es válido en nivel D. Se declara en INC-T184-01.
- **Prueba de regresión.** b09, más un rechazo de `unica_fuente_de` en una ficha que no es D.

#### H-04 · baja · La ficha de alta no trae la tipología ni el desglose de Q

- **Qué pasa.** El ejecutor decide PRIMARIA o SECUNDARIA por la «Tipología». Una fuente primaria dada de alta no puede declararlo, así que nunca da la vía de PS1 «1 fuente primaria de nivel A». Además, Q entra como un número suelto: el §13.3 la define como la suma de la rúbrica, y `_degradar` ya exige los siete puntos (b10).
- **Corrección exacta.**
  - Exigir `puntos`: siete enteros dentro de `RUBRICAS[archivo]`, la misma validación que `_degradar`.
  - Calcular Q como la suma y rechazar el lote si trae una `q` distinta.
  - Escribir el desglose en «Calidad Q».
  - Admitir `tipologia` en la lista cerrada {primaria, secundaria, terciaria} y escribir «- **Tipología:**».
- **Prueba de regresión.** b10, más el rechazo de unos puntos que no suman la `q` declarada o que superan su criterio.

#### H-05 · media · La prueba del ticket no mata ningún mutante propio, y PB-26 sale «Superada» sin probar el criterio entero

- **Qué pasa.**
  - Con `test_t184_altas.py` viven los 14 mutantes de `revisores/r01_mutantes.py`:
    - los umbrales A, B y C (N1–N3);
    - un id repetido (N4);
    - una sección ambigua (N5);
    - sin filtro de inyección (N6), de esquema (N7) ni de credenciales (N8);
    - el desempate de las fichas existentes por fecha y por año (N9 y N12);
    - Q booleana, real o fuera de rango (N10 y N14);
    - escritura sin comparar con lo leído (N11);
    - título multilínea (N13).
  - Las 30 altas de la prueba son todas de nivel D (Q 41–45), así que «calidades variadas» y «niveles A/B/C coherentes» no se prueban, y el alta nunca se ejerce sobre los catálogos reales.
  - Aun así, el mapa pone PB-26 en AUTOMATICA con `no_comprueba` vacío, y las evidencias la dan por «Superada».
- **Corrección exacta.**
  - Llevar a `tests/test_t184_altas.py` b01 (sobre copias de los tres catálogos entregados), b06, b07 y b08.
  - Añadir una prueba de empate de Q con fichas existentes de años distintos (mata N9 y N12) y una de sección duplicada (N5).
  - Volver a pasar `revisores/r01_mutantes.py` hasta que mueran todos.
  - Citar las pruebas nuevas en `mapa_plan_pruebas.json` y regenerar las evidencias.
- **Prueba de regresión.** Las citadas.

#### H-06 · baja · Umbrales de nivel escritos a mano, por triplicado

- **Qué pasa.** Los umbrales 80, 65 y 50 están escritos a mano en `altas_referencias.py:47`, en `mantenimiento_fuentes.py:42` (T-181) y en la prueba de T-126. Su fuente es el §13.3, que no es el Anexo A ni la configuración (regla 2).
- **Corrección exacta.**
  - Una sola función `nivel_de_q`, en `referencias.py`, que lea `referencias.niveles_q: {A: 80, B: 65, C: 50}` de `config/por_defecto.yaml`. La clave lleva el comentario «transcripción del §13.3» y se declara en INC-T184-01.
  - La usan los dos módulos.
- **Prueba de regresión.** b01 (mata N1–N3) y una prueba de que la configuración manda: con otro umbral, cambia el nivel.

#### H-07 · baja · Decisiones del alta sin declarar

- **Qué pasa.**
  - El §13.4 reserva `PENDIENTE_VERIFICACION_ALTA` para las «referencias semilla incorporadas sin verificación completa». Para un enlace nuevo aún sin barrido, el estado del §13.4 es `PENDIENTE_BARRIDO`.
  - El formato del lote JSON tampoco está declarado.
  - La tercera frase de INC-T184-01 («Usar la configuración de la instancia…») es una instrucción, no una decisión.
- **Corrección exacta.**
  - Escribir `PENDIENTE_BARRIDO`, o declarar la elección como `[PROPUESTO]` con su motivo.
  - Describir en INC-T184-01 los campos del lote y sus reglas, incluidos los de H-03 y H-04.
  - Quitar la frase operativa y pasarla al `handoff.md`.
- **Prueba de regresión.** Una aserción sobre el estado del enlace de la ficha nueva en b01.

### Observación fuera del alcance (para el coordinador)

- **O-01**, también en el `qa.md` de T-183. Las fichas en `PENDIENTE_*` cuentan hoy para PS1, en contra del §13.4. Las altas de este ticket nacen en ese estado y cuentan desde el primer ciclo. Propongo un ticket propio.
