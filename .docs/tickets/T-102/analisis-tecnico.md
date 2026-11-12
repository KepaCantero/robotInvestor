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
