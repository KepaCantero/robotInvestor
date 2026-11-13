# T-102 · Análisis técnico

## Causa

El filtro de T-101 trataba cada texto entero con pocas reglas:
- «opciones» contaba como palabra de probabilidad, y en el Bloque es el nombre de las ideas y el de un derivado;
- el código tras el verbo se cortaba a cinco letras, así que «EURUSD» se leía «EURUS»;
- solo se miraba la primera palabra tras el verbo;
- una frase mala hacía caer todos los textos llanos.

## Implementación (`bloque_a/diseno_v6.py`)

- `frase_prohibida(frase, perm)`, `texto_prohibido(texto, perm)` y `limpiar(texto, perm)`: se divide el texto en frases (`. ; ! ?`) y se juzga cada una.
- **R13:** tres patrones:
  - porcentaje «de probabilidad, posibilidad, confianza u opciones de»;
  - «probabilidad» o «posibilidad» con un enlace corto y una cifra;
  - «probable al N %».
- **R21:**
  - sufijo societario, bono con año de vencimiento y `sintesis._UNITARIA`;
  - un ISIN que no sea una serie del universo;
  - tras un verbo (comprar, vender, adquirir, sobreponderar, invertir en, entrar en, tomar posiciones en, abrir largos o cortos en, la compra de, la venta de), cualquier código que sea un instrumento en los 60 caracteres siguientes, hasta la coma o el siguiente «y + verbo».
- **Qué es un instrumento (`_es_instrumento`):** un código en mayúsculas que no está en `v6.filtro_r21_codigos`, que no es un par de dos divisas permitidas y que no es una serie del universo. Las series son los símbolos con «=», «^», dígitos, guiones o barra, o de más de cinco letras, y los pares «EURUSD=X» también sin el «=X». Un ticker de fondo del universo (GLD, XLK) sí es un instrumento.
- `_aplicar_integracion` quita frases de cada texto de la integración. `_redaccion_segura` lo hace en cada texto llano y, si uno se queda vacío, pone el texto por defecto de ese elemento. Las dos lo declaran en las limitaciones, con cuántas frases se quitaron.

## Límites

- Un nombre propio sin código ni sufijo («entrar en Tesla») no se detecta: lo revisa el Auditor por muestreo.
- La V5 sigue sin filtro en los textos de integración de AG-02 (deuda T-101).

## Ronda r02 (hallazgos H-01 a H-10 de la QA r01)

**Causa.** Las reglas de la r01 enumeraban formas: R13 solo cazaba el enlace pegado a «probabilidad» y no «la probabilidad de que X … es del N %» (H-01); R21 cortaba la ventana en la coma y a los 60 caracteres (H-02, H-08) y tomaba por instrumento cualquier sigla de la ventana (H-03). Enumerar formas de un texto libre no converge (memoria de Claude): cada ronda encuentra formas nuevas. La r02 cambia la dirección de R13 (amplia y con excepciones estrechas, falla cerrado) y la ventana de R21 (toda la frase que depende del verbo).

**Implementación (`bloque_a/diseno_v6.py`).**
- **R13 (`_r13`):** se quita la frase que tiene una palabra de probabilidad («probabilidad», «probable», «posibilidad», «chance»; no «probablemente») y una cifra (porcentaje, decimal 0,xx o «N de cada M»), salvo que esa cifra sea claramente otra cosa:
  - el nivel de un tipo, una tasa o una métrica, con solo palabras de función o nombres propios entre medias («el depósito en el 2 %», «el tipo de la Fed en el 4 %»; no «el tipo de interés baje es del 70 %»);
  - el tope de un movimiento («un recorte de la Fed hasta el 4,25 %»);
  - una frecuencia del historial («el 62 % de las veces») o un peso («un 5 % del capital»).
  Además, «N % de probabilidad, confianza, seguridad, certeza, opciones, riesgo de o de que», con o sin palabra de probabilidad, salvo el «VaR al 95 % de confianza».
- **R21:**
  - la ventana es todo lo que sigue al verbo hasta una subordinada («si», «cuando», «antes de», «según»…) o un verbo coordinado en minúscula («y esperar»), sin cortar en «,» ni «:» (H-02) y sin número de caracteres (H-08);
  - verbos nuevos: apostar por, acumular, ponerse largo o corto en, reforzar, reducir, cerrar o deshacer posiciones en, suscribir, liquidar y deshacerse de;
  - no son instrumentos: los códigos de `filtro_r21_codigos` (ampliada con regiones, bancos centrales, siglas macro, ratios, vehículos, temas, índices, materias primas, segmentos soberanos y divisas), las calificaciones crediticias, los pares de divisas con o sin barra, las series del universo y lo que sigue a una familia de índices («MSCI ACWI», «EURO STOXX 50») (H-03);
  - un símbolo del universo con sufijo de bolsa («XEON.DE») es un fondo, no una serie (H-02);
  - BTC y ETH salen de la lista: un token concreto es un instrumento, igual que SOL (H-09, `[PROPUESTO]` para el operador en T-57);
  - el sufijo societario acotado a siete palabras, con «S.A.», «SA», «FI», «FIL» y «SICAV» (H-04 b, H-07); `sintesis._UNITARIA` acota el nombre a 120 caracteres (H-07).
- **División (H-04):** se protegen las abreviaturas (EE. UU., S.A., p. ej., etc., Inc.…), se divide también por «…» y por saltos de línea, y `limpiar` conserva los separadores: un texto sin nada prohibido sale igual.
- **Declaración:** el glosario quitado cuenta (H-05); en la reescritura se retira la limitación de la respuesta descartada (H-06).

**Medida.** Banco del revisor (`revisores/r01_banco_frases.py`, 107 legítimas y 58 prohibidas): de 15 falsos positivos y 6 falsos negativos (r01) a 0 y 0. Ese banco sirvió para ajustar, así que no mide la generalización. Un banco de control escrito después y no usado para ajustar (25 legítimas y 24 prohibidas, en `tests/test_t102_filtro.py`, grupo r02) dio 0 falsos positivos y 1 falso negativo («la probabilidad de que el tipo de interés baje es del 70 %»), por un fallo real: el nombre propio de la cadena de excepción casaba cualquier palabra con IGNORECASE. Corregido.

**Límites que quedan.**
- Un nombre propio sin código ni sufijo («entrar en Tesla», «comprar Inditex») no se detecta: lo revisa el Auditor por muestreo.
- La lista de siglas permitidas es abierta: una sigla legítima que falte y vaya tras un verbo quita la frase (falla cerrado y se declara).
- R13 quita frases legítimas con una palabra de probabilidad y una cifra que no encaja en las excepciones («la posibilidad de subidas del 0,25 % gana peso»): falla cerrado y se declara.
- Un código tras una subordinada («Comprar RV si sube AAPL») no cuenta como comprado.
- La V5 sigue sin filtro en los textos de integración de AG-02 (deuda T-101).

## Ronda r03: rediseño con marcadores (decisión del operador del 12-11-2026)

**Por qué.** Tres rondas de QA con revisores nuevos encontraron, cada una, formas de redactar que el filtro de patrones no veía: listas con saltos de línea, «recomendamos el ETF X», «la opción preferida es X» o probabilidades en letra. Un filtro que enumera formas de un texto libre no converge. El operador eligió cambiar el diseño: el Sintetizador escribe con marcadores y el código los rellena, de modo que la regla sobre el texto libre puede ser estricta y no depende de la redacción.

**Implementación (`bloque_a/diseno_v6.py`).**
- **Marcadores:** `{opp:OPP-…}` (el `nombre_llano` de la opción), `{tipo:RV}` (`NOMBRE_CLASE`), `{n:RV}`, `{candidatas:RV}`, `{n_ideas}`, `{n_tipos}` y `{n_apuestas}`. `marcadores(paquete)` da sus valores; `rellenar` los sustituye después de filtrar, de modo que lo que pone el código no se filtra.
- **Regla, frase a frase:**
  - MARCADOR: un marcador que no es de este paquete, mal formado o una llave suelta;
  - CIFRA: cualquier dígito, «por ciento», «de cada diez» o una fracción junto a una palabra de probabilidad. Cubre R13 (sin cifras no hay probabilidad numérica) y parte de R21 (ISIN, tickers con números, vencimientos);
  - R21: un sufijo societario o de fondo, `sintesis._UNITARIA`, o cualquier código en mayúsculas que sea un instrumento, esté donde esté y con o sin verbo. Ya no hay verbos, ventanas ni excepciones.
- **Qué no es un instrumento:** `v6.filtro_r21_codigos` (ampliada con siglas del Documento 0: CDS, CLO, ABS, NFT, RWA, ELTIF, HICP…), las calificaciones, los pares de divisas y las series del universo. Un token frente a una divisa (BTC-USD, SOL-USD) es un instrumento (H-17).
- El prompt del Sintetizador (`prompts_v6/`, §4) y `INSTR_SINTESIS` explican la regla y los marcadores; el simulador escribe así.

**Coste aceptado.** Una frase legítima con una cifra se quita, porque las cifras las pone el código; también una sigla legítima que falte en la lista. Falla cerrado y se declara. El prompt pide escribir así, así que con el modelo real debería ser raro; se medirá en el banco con la API.

**Límite que queda.** Un nombre propio sin código ni sufijo («Tesla», «Inditex» sin «la acción de»). Con los marcadores, el Sintetizador no necesita escribir ninguno; lo revisa el Auditor por muestreo.

## Ronda r04 (QA r03 NO APTO, mismo diseño de marcadores)

**Causa.** La regla estricta de la r03 tenía huecos de cobertura, no de diseño:
- «cifra» era `\d`, sin los números Unicode (No, Nl) ni los números en letra (H-20);
- el sufijo no admitía punto y `_INDICE` borraba el ticker que seguía a la familia del índice (H-21);
- se colaban minúsculas tras un vehículo, homoglifos, códigos pegados y colisiones con la lista o con calificaciones (H-22);
- marcadores numéricos compuestos (H-23);
- además de los bajos H-24 a H-30.

**Implementación (`bloque_a/diseno_v6.py`).**
- **CIFRA:**
  - cualquier carácter numérico de Unicode, mirado antes y después de NFKC;
  - «%», «‰» y «por cien(to)»;
  - «N sobre / entre / de cada / en M» con números en letra (también «novecientos», «mil»);
  - una palabra de probabilidad junto a un número en letra o a un marcador numérico. Las palabras de probabilidad son ahora también «confianza», «seguridad», «certeza» y «escenario», porque los pesos de los escenarios son probabilidades.
- **MARCADOR:**
  - dos marcadores numéricos pegados o unidos por «sobre», «entre», «de cada», «/» o «%»;
  - un marcador numérico seguido de «%»;
  - llaves de cualquier escritura («｛ ｝» pasan a «{ }» con NFKC; «❴ ❵» cuentan como llaves sueltas).
- **R21:**
  - el sufijo, también con punto, tras coma o en minúscula (inc, corp, ltd), y los nombres de fondo que acaban en «Fund», «Trust», «ETF» o «UCITS ETF». No tras un artículo o un determinante («Las SICAV», «Varios ETF»);
  - sin `_INDICE`: los nombres de índice se añaden a la lista (ACWI, EAFE, EMU, EURO);
  - una calificación solo lo es junto a «crédito», «rating», «bonos», «deuda»…;
  - cualquier letra griega o cirílica;
  - «$» seguido de letras, un código pegado tras «_», «=», o tras «-» o «.» después de una minúscula;
  - mayúsculas y minúsculas mezcladas («AApl»), salvo los plurales de una sigla («ETFs»);
  - tras un vehículo, una sola letra, o un código en minúscula si el vehículo se nombra por su ticker (ETF, REIT, ticker, «fondo» con ≤ 4 letras).
- **Lista:** ampliada con siglas corrientes que no son instrumentos (OTAN, ONU, OMC, COVID, QE, QT, UK, IVA, IRPF, PYME, CAPE, EBIT…). Salen AI, ETN y UST, que también son tickers (en español: IA, nota cotizada, Tesoro). Los números romanos no son instrumentos («siglo XXI»).
- **Bajos:**
  - el `nombre_llano` que rellena `{opp:…}` pasa la regla y, si la incumple, se pone «esta idea» (H-27);
  - una entrada del glosario que no es texto se quita como FORMATO (H-24);
  - `_SEPARADOR` sin solapes, lineal (H-26);
  - la instrucción del Sintetizador lleva la lista de siglas permitidas (H-25);
  - la prueba de los marcadores calcula los valores aparte (H-29).

**Medida con los scripts de la QA r03** (ajustados contra ellos, así que no miden la generalización):
- `r03_01_ataques.py`: R13, 0 de 26 pasan; R21, 4 de 30 pasan (los cuatro límites de abajo); rendimiento, 0,48 s en total.
- `r03_02_banco_prompt.py`: legítimas quitadas, 1 de 128; prohibidas sin dígitos que pasan sin declararse, 2 de 45, y 2 de 3 límites.

**Límites declarados (R21, los revisa el Auditor por muestreo):**
- un nombre propio sin código ni sufijo («Tesla», «Inditex»);
- un ticker escrito en minúscula o como nombre propio sin un vehículo delante («la opción preferida es nvda», «… Nvda»);
- un ticker que coincide con una sigla legítima de la lista (COP es también el peso colombiano);
- un ticker de una sola letra sin un vehículo delante («Comprar F ya»).

## Ronda r05 (QA r04 NO APTO, mismo diseño de marcadores)

**Causa.** La r04 solo trataba un número en letra como cifra en unas pocas formas («N de cada M») o junto a una palabra de probabilidad. Eso dejaba pasar «una de cada tres», las fracciones y las cuotas (H-31), y a la vez quitaba «a medio plazo es probable» (H-35). Además, un `_SUFIJO` sin tope era cuadrático (H-37) y tomaba por nombre una palabra común delante de «ETF» (H-36).

**Implementación (`bloque_a/diseno_v6.py`).**
- **CIFRA (H-31 y H-35):**
  - cualquier número en letra es cifra, en cualquier frase: «dos», «setenta», «mil», «tercio»;
  - «uno» o «una» solo cuentan en «una de cada…», «uno contra uno» y en las fracciones «un cuarto», «una décima» o «una cuarta parte»;
  - «medio» solo cuenta en «y medio», «un medio», «medio punto» y «media docena»;
  - «mitad» cuenta salvo en «primera/segunda mitad» y «mitad del año, ciclo, mes…»;
  - los ordinales («cuarto trimestre») no cuentan;
  - también son cifra «el doble» o «el triple», y cualquier signo de porcentaje o de por mil de otra escritura («٪»);
  - una palabra de probabilidad solo hace falta ya junto a un marcador numérico.
- **MARCADOR:**
  - dos marcadores numéricos unidos también por «veces de cada», «contra», «a», «en» o «-»;
  - un marcador unido a «uno» o «una» («una de cada {n_ideas}»);
  - el nombre de un marcador fuera de sus llaves («〔n_ideas〕», «[n:RV]»).
- **R21:**
  - más sufijos (H-32): «SpA», «S.p.A.», «Co.», «Limited», «GmbH», «LLC», «N.V.» y «Aktiengesellschaft», y en minúscula con punto («apple inc.»);
  - una palabra común al principio del nombre no es un nombre (H-36): «Cada», «Todos», un infinitivo al abrir la frase («Sobreponderar ETF»). Un nombre que acaba como un infinitivo en mitad de la frase («Comprar Unilever plc») sigue contando;
  - cada palabra del nombre empieza donde no hay otra letra y tiene un tope de 40 caracteres (H-37): 40 000 caracteres de «A.» en 0,1 s;
  - antes de mirar, fuera los caracteres de formato y las marcas combinantes (H-33): espacio de ancho cero, guion blando, unión de palabras;
  - letras de cualquier alfabeto no latino, versalitas e indicadores regionales («ᏚᏢᎩ», «ɴᴠᴅᴀ», «🇳🇻🇩🇦»);
  - tras un vehículo, una palabra con mayúscula inicial y el resto en minúscula es un nombre, no un código (H-36): «acciones de Europa».
- **Instrucción (H-39):** no se ofrecen siglas con cifras («G7», «G20»).
- **Pruebas (H-38):** `test_t102_filtro.py`, ronda r05, con una frase por mutante vivo de las QA r03 y r04. Los valores de los marcadores, el glosario y el historial se comparan con el paquete en una prueba unitaria de `_redaccion_segura`.

**Límites declarados (R21; los revisa el Auditor por muestreo):** los cuatro de la r04, y además (H-34) un ticker en minúscula tras «la acción», «el valor» o «el título» («comprar el valor nvda»). Cazarlo sin quitar «el valor real» o «el valor neto» exige saber qué palabras son españolas, y queda en la deuda (T-109).

**Coste declarado de la regla estricta:** se quitan frases legítimas con un número en letra que no es una probabilidad («Los dos escenarios favorecen al dólar», «en dos de los mercados»). El Sintetizador tiene marcadores para las cuentas y el prompt le pide no escribir cifras.
