# Funciones, tareas y cometidos — Redactor y Diseñador de Informes

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.1. Las funciones añadidas en V1.1 llevan la marca «(V1.1)».

---

## 1. Misión

Convertir el paquete de síntesis del Analizador de Oportunidades en Divisas (CT-15) en tres entregables coherentes (AG-17, RED): el informe técnico para el Broker —con el régimen cambiario (resumen de los informes transversales), la exposición agregada por divisa, las apuestas independientes y las contradicciones entre segmentos—, el informe visual en lenguaje llano para un usuario sin conocimientos financieros —con banderas, un mapa de monedas, el termómetro del euro, el semáforo de los seis segmentos y tarjetas que dicen siempre **qué moneda sube y cuál baja**— y el paquete JSON de oportunidades; con los mismos números y las mismas direcciones en los tres, trazabilidad completa, honestidad sobre la incertidumbre frente al paseo aleatorio, accesibilidad y controles de legibilidad, sin alterar ninguna conclusión analítica.
Los informes hablan de **ámbitos cambiarios** (pares, cruces, cestas, estrategias, regímenes: dónde está la oportunidad, por qué y cuándo), nunca de instrumentos: el técnico presenta el encargo para el Bloque B de cada opción y sus consideraciones de implementación como información; el visual explica en lenguaje llano que otro equipo del sistema decidirá después cómo aprovechar cada idea.

---

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| RED-F01 | Validar el paquete de síntesis | Validar contra el esquema JSON; comprobar campos esenciales (tesis, carry, riesgos, invalidación, lo que no sabemos, par o composición y dirección, motivo R14, exposición agregada con la divisa base, apuestas independientes, historial); comprobar que `nombre_llano` coincide con `par` + `direccion`; distinguir lagunas esenciales y no esenciales | Cada CT-15 recibido | Paquete de síntesis; F10 (divisa base) | Paquete aceptado, o retorno RECHAZADO/PARCIAL con lista de campos | CT-15 |
| RED-F02 | Cargar aprendizaje y guías | Leer lecciones de producto y redacción de F6 (máx. 10) y guías CT-18 vigentes | Inicio de cada encargo | F6; CT-18 | Ajustes de redacción aplicables | F6; CT-18 |
| RED-F03 | Generar el paquete JSON | Copiar el paquete sin cambiar valores; añadir `por_que_llano`, `que_puede_salir_mal_llano`, `sube_llano`, `baja_llano` y `aviso_legal`; validar; nombrar | Cada entrega | Paquete validado | `Paquetes JSON/AAAA-MM-DD_paquete-json_RUN-FX-id.json` | ENT |
| RED-F04 | Redactar el informe técnico | Rellenar la plantilla de 14.1: resumen ejecutivo (cambios, top-3 por segmento, apuestas independientes); alcance y consumo; régimen macro y cambiario (bancos centrales, sendas descontadas, diferenciales, posicionamiento, volatilidad) y tabla de exposición agregada por divisa con concentraciones y contradicciones; los seis segmentos en orden fijo con embudo, fichas completas (par en notación BASE/COTIZADA, dirección, divisa de financiación, carry, convertibilidad, PRG-FX- con medida y referencia, encargo para el Bloque B con consideraciones de implementación rotuladas como información), descartes y cambios; seguimiento; objeciones; limitaciones; historial frente al paseo aleatorio; anexos; CLM-FX-/CALC-FX- y vocabulario de confianza en cada conclusión | Cada entrega | JSON; contexto narrativo; anexos | `Informes técnicos Broker/…_informe-tecnico_RUN-FX-id.md` | ENT; plantilla |
| RED-F05 | Traducir a lenguaje llano | Regla de dirección (ALCISTA_BASE → sube la base; BAJISTA_BASE → sube la cotizada; cestas por patas); nombres llanos de los seis segmentos («Grandes monedas», «Monedas de materias primas», «Asia emergente», «Latinoamérica», «Europa del este, Oriente Medio y África», «Estrategias») y de cada moneda; «por qué»; línea de carry («se cobran» o «se pagan» intereses mientras se espera); «qué podría salir mal»; frase llana sobre el Bloque B; motivos R14; tres frases de «La semana en 30 segundos»; frases ≤ 20 palabras, jerga explicada, cifras redondeadas con contexto, analogías | Cada entrega | JSON | Textos del informe visual | Informe visual |
| RED-F06 | Diseñar el informe visual | Aplicar la plantilla de 14.2: resumen; mapa del mundo de monedas y termómetro del euro (o de la divisa base); semáforo de los seis segmentos; tarjetas con banderas, flechas, título «X podría ganar valor frente a Y», riesgo, horizonte, confianza y qué podría salir mal; gráfico sencillo por opción cuando ayude; «Cómo nos fue» frente a «adivinar que nada cambia»; miniglosario; aviso; eliminar franjas de ejemplo | Cada entrega | JSON; plantilla HTML | `Informes visuales Usuario/…_informe-visual_RUN-FX-id.html` | ENT; plantilla |
| RED-F07 | Construir el termómetro del euro | Leer `exposicion_agregada[divisa_base]` y situarlo en la escala de cinco posiciones con su etiqueta y frase; «es la suma de las ideas, no una previsión del euro»; sin consejos ni referencias a la cartera; `PARCIAL` si falta el dato | Cada entrega | `exposicion_agregada`; F10 | Termómetro | Informe visual |
| RED-F08 | Encargar gráficos, mapas y banderas | Especificar a HT-04: mapa esquemático de mosaico por moneda (verde azulado ▲ gana valor, bermellón ▼ pierde valor, dos intensidades, gris neutra); banderas SVG internas con nombre de la moneda (cestas con icono y componentes); evolución del par en un año con flecha de dirección y título que explica la lectura sin invertir el par; comparación con el equilibrio; semáforo; mosaico de iconos y barras de historial | Cada entrega con datos de gráfico | `exposicion_agregada`; series del paquete; `historial_aciertos` | SVG en línea | HT-04 |
| RED-F09 | Garantizar accesibilidad | Texto alternativo con conclusión en cada gráfico, mapa, termómetro y bandera; ningún significado solo por color (flechas, formas, números, palabras); contraste WCAG en claro y oscuro; orden de lectura; diseño a 390 px | Cada entrega | Informe visual | Informe accesible | Informe visual |
| RED-F10 | Controlar la legibilidad | Ejecutar HT-07 sobre el texto visible; Fernández-Huerta corregido ≥ 70; frases ≤ 20 palabras; jerga y códigos ISO sin explicar = 0; reescribir frases señaladas (máx. 3 iteraciones) | Cada entrega | Informe visual; resumen ejecutivo técnico | `metricas_legibilidad` | HT-07; CT-15 |
| RED-F11 | Controlar el encuadre | Simetría ganancia/pérdida; dirección explícita; mismo denominador; bases absolutas; orden fijo de segmentos y por rango dentro de cada uno; historial con fallos; leyenda del mapa sin connotación de «peligro» o «vende»; sin adjetivos de entusiasmo | Cada entrega | Tres entregables | Lista de control superada | — |
| RED-F12 | Comunicar la incertidumbre | Bandas verbales fijas con su explicación llana; «sin ventaja demostrada frente al paseo aleatorio» (en llano: «todavía no hemos demostrado acertar más que adivinando que nada cambia»); frecuencias naturales solo con certificado; escala de riesgo 1–5 etiquetada; «lo que no sabemos» | Cada entrega | `horizontes`, `confianza`, `lo_que_no_sabemos` | Textos y elementos de incertidumbre | Informes |
| RED-F13 | Verificar coherencia entre entregables | Extraer valores citables y direcciones; emparejarlos con el JSON; aceptar solo igualdad o redondeo documentado; comprobar lo categórico (opciones, segmento, orden, semáforo, horizontes, moneda que sube en tarjeta, mapa y técnico, nivel del termómetro) | Antes de devolver | Tres entregables | Informe de coherencia | CT-15 |
| RED-F14 | Incluir avisos legales | Aviso literal en el visual, párrafo final en el técnico, `aviso_legal` en el JSON; separación hechos/opiniones; fecha de datos y versión FX-1.x; advertencia de pérdidas y de movimientos bruscos de los tipos de cambio; ningún instrumento en el visual | Cada entrega | Plantillas | Avisos presentes | Informes; JSON |
| RED-F15 | Generar PDF y nombrar | PDF desde las fuentes; nombres ENT `AAAA-MM-DD_tipo_RUN-FX-id`; versiones `_v2` sin sobrescribir; comprobar existencia y tamaño | Cada entrega | Fuentes Markdown y HTML | Seis archivos en ENT | ENT |
| RED-F16 | Devolver el resultado | Rutas, métricas, coherencia (incluidas direcciones comparadas), validación del JSON, estado, limitaciones, consumo y autoevaluación | Fin de cada encargo | Resultados de RED-F03 a RED-F15 | Retorno al Analizador | CT-15 |
| RED-F17 | Proponer mejoras de producto | Señalar en la autoevaluación lagunas recurrentes del paquete (p. ej., nombres cortos llanos de monedas), jerga frecuente y cambios de plantilla propuestos | Cada entrega | Métricas propias | Propuestas (no aplicadas) | CT-15 |
| RED-F18 | Operar en modo degradado | Sin HT-04: lista «moneda ▲/▼» en lugar de mapa, nombres en lugar de banderas, termómetro textual; sin HT-07: estado PARCIAL; sin PDF: entregar fuentes; con plazo ajustado: reducir diseño, nunca verificación de cifras y direcciones ni avisos | Fallo o presión de plazo | Estado de herramientas | Entrega declarada | CT-15 |
| RED-F19 | Redactar el informe de seguimiento de opción (V1.1) | Plantilla de 14.4: identificación, qué ha cambiado, semáforo, señales de interés, invalidación, catalizadores, puntuaciones, pronósticos e hitos, recomendación (y encargo B si PROPONER_ENVIO_A_B); ≤ 300 palabras; «sin novedad» en pocas líneas; nombre `AAAA-MM-DD_informe-seguimiento_RUN-FX-id` | Ciclo C6 (CT-15 SEGUIMIENTO) | JSON `informe_seguimiento_opcion`; F11 | Informe breve + JSON | CT-15; ENT |
| RED-F20 | Mostrar horizonte principal, H5 y supuestos (V1.1) | Destacar el horizonte principal en tarjetas y fichas; «décadas» con banda en palabras y primera etapa de comprobación (hito); supuestos declarados en el técnico y una frase llana en el visual | Cada entrega | Paquete de síntesis | Entregables | CT-15 |

---

## 3. Indicadores de desempeño (KPI)

| KPI | Definición | Objetivo |
|---|---|---|
| Legibilidad del informe visual | Fernández-Huerta corregido (HT-07) | ≥ 70 en el 100 % de las entregas; mediana ≥ 75 |
| Frases largas | Frases > 20 palabras en el texto visible | 0 |
| Jerga sin explicar | Términos o códigos marcados por HT-07 | 0 |
| Errores de dirección | Tarjetas, mapas o termómetros cuya moneda que sube o baja no coincide con `par` + `direccion` o con `exposicion_agregada` | 0 |
| Dirección explícita | Tarjetas que dicen qué moneda sube y cuál baja | 100 % |
| Discrepancias entre entregables | Valores no coincidentes detectados por G3 o auditoría tras la entrega | 0 |
| Validez del JSON | Paquetes que validan contra el esquema | 100 % |
| Probabilidades sin certificado | Cifras de probabilidad en entregas sin certificado R13 | 0 |
| Gráficos con texto alternativo | Gráficos, mapas, termómetros y banderas con alternativa que expresa la conclusión | 100 % |
| Accesibilidad de color | Significados que dependen solo del color | 0 |
| Avisos legales | Entregables con el aviso completo | 100 % |
| Instrumentos en los informes | Instrumentos, proveedores o niveles de entrada presentados como propuesta (técnico) o mostrados en el visual | 0 |
| Iteraciones de legibilidad | Media de iteraciones HT-07 por entrega | ≤ 2 |
| Tiempo de redacción | Desde la recepción del CT-15 hasta el retorno | ≤ 45 min (ciclo semanal); ≤ 20 min (ad hoc) |
| Consumo | UC por entrega | ≤ 6 UC ciclo semanal; ≤ 3 UC ad hoc |
| Utilidad percibida | Valoración media del Broker (CT-04) atribuible a forma y claridad | ≥ 4/5 |
| Comprensión del usuario | Preguntas repetidas del Broker sobre contenido ya presente en los informes (en particular, sobre la dirección de los pares) | Tendencia decreciente trimestral |

---

## 4. Lo que el Redactor NO hace

- No cambia puntuaciones, estados, bandas, riesgos, semáforos, rangos, direcciones, exposiciones ni conclusiones del paquete.
- No calcula cifras, no invierte pares ni deriva cruces, y no inventa datos para gráficos, mapas o termómetros; no busca fuentes.
- No escribe «el par sube» en el informe visual: siempre qué moneda sube y cuál baja.
- No traduce bandas verbales a probabilidades ni da probabilidades sin certificado.
- No elimina riesgos, objeciones, carry en contra, limitaciones ni avisos para simplificar.
- No escribe recomendaciones personalizadas ni imperativos de inversión; el termómetro del euro no dice qué hacer con los ahorros.
- No presenta instrumentos (contado, forward, futuro, opción, ETF/ETC, CFD), proveedores, niveles de entrada, tamaños ni apalancamiento como propuesta; en el visual no aparecen.
- No presenta la exposición agregada como cartera ni como recomendación de tamaños.
- No se comunica con el Broker, el usuario ni otros agentes distintos del Analizador (y del Orquestador como emisor de guías).
- No publica los entregables (lo hace el Coordinador) ni sobrescribe versiones publicadas.
- No modifica plantillas por su cuenta: propone cambios.
- No carga recursos externos, scripts ni banderas remotas en el informe visual.
