# Auditoría de identificadores del Bloque A (Fase 0, T-157)

Qué está desincronizado entre el corpus vigente del Bloque A y el código del ejecutor, medido con un comando. El informe de
abajo lo genera el verificador; nada de él está escrito a mano. Las decisiones del final eran **propuestas**: ninguna se aplicó
en esta fase (D-1 la aplicó T-160 y D-2 a D-4, la entrega del corpus de T-166, 17-11-2026), y cada una tiene su entrada en `docs/incidencias.md` (INC-T157-01 a INC-T157-05).

## Cómo se repite

Desde `bloque_a/11_Ejecutor`:

```bash
../../.venv/bin/python -m bloque_a.herramientas.verificador_ids \
  --json ../../docs/auditoria_ids_bloque_a.json --auditoria ../../docs/auditoria_ids_bloque_a.md
```

Sin opciones escribe el Markdown por la salida estándar. Sale con 0 si no hay errores, 1 si los hay y 2 si falla cerrado (falta
el Documento 0 o el Catálogo, hay más de uno, o falta una sección que necesita). `--auditoria` solo sustituye lo que va entre
las marcas `INFORME:INICIO` e `INFORME:FIN`; este texto y las decisiones se conservan. El JSON completo, con todas las
ubicaciones, está en `docs/auditoria_ids_bloque_a.json`.

El Documento 0 y el Catálogo se buscan por patrón (el informe dice qué versión leyó y su huella SHA-256), así que el comando
sigue valiendo cuando llegue otra versión del Documento 0. No se lee `11_Ejecutor/` como corpus ni ninguna carpeta
`99_Historico*`.

<!-- INFORME:INICIO -->

## Informe de consistencia de identificadores del Bloque A

Generado por `bloque_a/herramientas/verificador_ids.py` 1.1.0 (T-157). Todo dato sale del corpus y del código escaneados; las huellas permiten comprobar que se leyó exactamente esto.

### Entradas

| Entrada | Archivo | Versión | SHA-256 |
|---|---|---|---|
| Documento 0 | `01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.3.md` | V5.3 (título: V5.3) | `12cc5182ca4fb2cb9ca1cbbe43c1286985add017f1dff10582c70dd9f721cf74` |
| Catálogo | `04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.0.md` | V5.0 | `16fdb3b30833c7d7a2bece5c0c1628a7327b38fdeaa11a82b5bdca31062bd66f` |
| Código | `bloque_a/contratos.py` | — | `424c5bf521087627babcb2e1028ecd28837ca7f0276f118806f5fad415425910` |
| Código | `bloque_a/motor/servicio.py` | — | `d5bf9d7ab758f2226ae4d64cd042481c95653563525c7821ecbc289997e55945` |
| Corpus | 88 `.md` (sin 11_Ejecutor/, 99_Historico*/) | — | `7649e725c1ac338b75d20c75aeeb01d675cd5dbc9f85982d7bf5f5f806f4c851` |

Secciones del Documento 0 leídas (línea del título): §1 l. 25, §5.1 l. 263, §6.1 l. 296, §7.3 (solo el título) l. 370, §9.3 l. 556.

### Resumen

| Clase | Errores | Avisos | Info |
|---|---|---|---|
| Entradas | 0 | 0 | 0 |
| a · Contratos CT | 0 | 0 | 0 |
| b · Reglas R | 0 | 0 | 1 |
| c · Archivos F | 0 | 0 | 9 |
| d · Fichas del Catálogo | 0 | 0 | 2 |
| e · Referencias de los archivos operativos | 0 | 1 | 0 |
| f · Puertas PS | 0 | 0 | 0 |

**Total de errores: 0.**

### (a) Contratos CT

§6.1: «6.1 Contratos en vigor (CT-01 a CT-25)». Definidos en §6.1: 25; con canal en `contratos.py`: 25.

| CT | §6.1 | CANALES | canal_permitido | CANALES_V6 | CAMPOS_MINIMOS | Citas | Archivos |
|---|---|---|---|---|---|---|---|
| CT-01 | sí | sí | sí | no | sí | 38 | 11 |
| CT-02 | sí | sí | sí | no | sí | 30 | 8 |
| CT-03 | sí | sí | sí | no | sí | 47 | 7 |
| CT-04 | sí | sí | sí | no | no | 48 | 13 |
| CT-05 | sí | sí | sí | no | sí | 93 | 12 |
| CT-06 | sí | sí | sí | no | sí | 332 | 33 |
| CT-07 | sí | sí | sí | sí | sí | 98 | 38 |
| CT-08 | sí | sí | sí | sí | sí | 94 | 38 |
| CT-09 | sí | sí | sí | no | sí | 192 | 52 |
| CT-10 | sí | sí | sí | no | sí | 98 | 25 |
| CT-11 | sí | sí | sí | no | sí | 87 | 42 |
| CT-12 | sí | sí | sí | no | sí | 49 | 12 |
| CT-13 | sí | sí | sí | no | sí | 109 | 41 |
| CT-14 | sí | sí | sí | no | sí | 37 | 8 |
| CT-15 | sí | sí | sí | sí | sí | 47 | 14 |
| CT-16 | sí | sí | sí | no | no | 36 | 8 |
| CT-17 | sí | sí | sí | no | no | 52 | 8 |
| CT-18 | sí | sí | sí | no | no | 67 | 23 |
| CT-19 | sí | sí | sí | no | no | 97 | 32 |
| CT-20 | sí | sí | sí | no | no | 41 | 9 |
| CT-21 | sí | sí | sí | no | no | 62 | 20 |
| CT-22 | sí | sí | sí | no | no | 67 | 12 |
| CT-23 | sí | sí | sí | no | sí | 152 | 50 |
| CT-24 | sí | sí | sí | no | sí | 87 | 16 |
| CT-25 | sí | sí | sí | no | sí | 175 | 44 |

Sin hallazgos.

### (b) Reglas R

§1: «1. REGLAS CRÍTICAS (R1–R27)». Definidas: 27.

| Regla | §1 | Citas | Archivos |
|---|---|---|---|
| R1 | sí | 27 | 14 |
| R2 | sí | 27 | 20 |
| R3 | sí | 17 | 13 |
| R4 | sí | 39 | 24 |
| R5 | sí | 35 | 23 |
| R6 | sí | 19 | 15 |
| R7 | sí | 76 | 54 |
| R8 | sí | 47 | 29 |
| R9 | sí | 64 | 48 |
| R10 | sí | 34 | 26 |
| R11 | sí | 20 | 13 |
| R12 | sí | 35 | 25 |
| R13 | sí | 141 | 58 |
| R14 | sí | 50 | 32 |
| R15 | sí | 40 | 29 |
| R16 | sí | 46 | 34 |
| R17 | sí | 21 | 13 |
| R18 | sí | 13 | 7 |
| R19 | sí | 23 | 13 |
| R20 | sí | 14 | 10 |
| R21 | sí | 141 | 45 |
| R22 | sí | 70 | 47 |
| R23 | sí | 19 | 15 |
| R24 | sí | 20 | 14 |
| R25 | sí | 62 | 41 |
| R26 | sí | 31 | 20 |
| R27 | sí | 47 | 24 |
| R30 | no | 1 | 1 |

| Nivel | Código | ID | Motivo | Dónde |
|---|---|---|---|---|
| INFO | CITA_EN_CONTEXTO_AJENO | R30 | R30 aparece como código JEL de clasificación de la literatura económica: no se cuenta como cita | `02_System_prompts/System prompt - Documentador para el Analizador - Versión óptima V5.0.md:368` |

### (c) Archivos F

Mapa código de §5.1 → archivo real de `05_Archivos_operativos`, por su H1 (la numeración no coincide con el nombre del archivo):

| Código | Nombre en §5.1 | Archivo real (por H1) | Nombre en el H1 |
|---|---|---|---|
| CC | Catálogo de cálculos, Perfiles de clase y Mapa de conocimientos del Motor | — | — |
| ENT | Carpetas de entregables | — | — |
| F1 | Registro maestro de tendencias | `05_Archivos_operativos/Registro maestro de tendencias (esquema V2.0).md` | Registro maestro de tendencias |
| F2 | Registro de evidencia y afirmaciones | `05_Archivos_operativos/Registro de evidencia y afirmaciones (esquema V2.0).md` | Registro de evidencia y afirmaciones |
| F3 | Registro de oportunidades | `05_Archivos_operativos/Registro de oportunidades (esquema V3.0).md` | Registro de oportunidades |
| F4 | Registro de pronósticos congelados | `05_Archivos_operativos/Registro de pronósticos congelados (esquema V2.0).md` | Registro de pronósticos congelados |
| F5 | Historial de análisis | `05_Archivos_operativos/Historial de análisis (esquema V2.0).md` | Historial de análisis |
| F6 | Memoria de aprendizaje | `05_Archivos_operativos/Memoria de aprendizaje (esquema V2.0).md` | Memoria de aprendizaje |
| F7 | Documentación para el Analizador de Tendencias de Inversión | `05_Archivos_operativos/Documentación para el Analizador de Tendencias de Inversión - V3.2.md` | Documentación para el Analizador de Tendencias de Inversión |
| F8 | Documentación para el Motor de Cálculo Avanzado | `05_Archivos_operativos/Documentación para el Motor de Cálculo Avanzado - V3.2.md` | Documentación para el Motor de Cálculo Avanzado |
| F9 | Registro de Fuentes para el Analizador de Tendencias de Inversión | `05_Archivos_operativos/Registro de Fuentes para el Analizador de Tendencias de Inversión - V3.2.md` | Registro de Fuentes para el Analizador de Tendencias de Inversión |
| F10 | Configuración y parámetros del bloque | `05_Archivos_operativos/Configuración y parámetros del bloque (esquema V3.0).md` | Configuración y parámetros del bloque |
| F11 | Registro de seguimientos encargados | `05_Archivos_operativos/Registro de seguimientos encargados (esquema V1.0).md` | Registro de seguimientos encargados |
| FM | Fondo metodológico bibliográfico | `05_Archivos_operativos/Fondo Metodológico Bibliográfico - V3.1.md` | Fondo Metodológico Bibliográfico |
| HA | Historial de auditorías | `05_Archivos_operativos/Historial de auditorías (esquema V2.0).md` | Historial de auditorías |
| RC | Registro de cálculos del Motor | `05_Archivos_operativos/Registro de cálculos del Motor (esquema V2.0).md` | Registro de cálculos del Motor |

Las fases salen del título de §7.3 («7.3 Fases de un análisis (F0–F8) y fases asíncronas (F9–F10)»): F0, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10. Una cita «F3» puede ser el archivo o la fase; solo es error si no es ninguna de las dos.

| F | Archivo de §5.1 | Fase de §7.3 | Citas | Archivos |
|---|---|---|---|---|
| F0 | no | sí | 39 | 26 |
| F1 | sí | sí | 218 | 57 |
| F02 | no | no | 2 | 2 |
| F2 | sí | sí | 235 | 55 |
| F3 | sí | sí | 222 | 53 |
| F4 | sí | sí | 176 | 64 |
| F05 | no | no | 1 | 1 |
| F5 | sí | sí | 210 | 48 |
| F6 | sí | sí | 294 | 63 |
| F7 | sí | sí | 236 | 59 |
| F8 | sí | sí | 158 | 43 |
| F9 | sí | sí | 250 | 63 |
| F10 | sí | sí | 239 | 62 |
| F11 | sí | no | 90 | 27 |
| F12 | no | no | 6 | 3 |
| F31 | no | no | 1 | 1 |

| Nivel | Código | ID | Motivo | Dónde |
|---|---|---|---|---|
| INFO | CODIGO_FUERA_DE_05 | CC | CC («Catálogo de cálculos, Perfiles de clase y Mapa de conocimientos del Motor») no es un archivo de 05_Archivos_operativos/ | `01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.3.md:263` |
| INFO | CODIGO_FUERA_DE_05 | ENT | ENT («Carpetas de entregables») no es un archivo de 05_Archivos_operativos/ | `01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.3.md:263` |
| INFO | CITA_EN_CONTEXTO_AJENO | F02 | F02 aparece como abreviatura de la función AUD-F02 del mismo documento, en el rango F02–F12: no se cuenta como cita | `03_Funciones/Funciones, tareas y cometidos – Auditor – óptima V5.0.md:30` |
| INFO | CITA_EN_CONTEXTO_AJENO | F02 | F02 aparece como abreviatura de la función PROS-F02 del mismo documento, en el rango F02–F12: no se cuenta como cita | `03_Funciones/Funciones, tareas y cometidos – Analista de Prospectiva y Horizontes – óptima V5.0.md:31` |
| INFO | CITA_EN_CONTEXTO_AJENO | F05 | F05 aparece como abreviatura de la función ORQ-F05 del mismo documento, en el rango ORQ-F03 a F05: no se cuenta como cita | `03_Funciones/Funciones, tareas y cometidos – Orquestador técnico – óptima V5.0.md:23` |
| INFO | CITA_EN_CONTEXTO_AJENO | F12 | F12 aparece como abreviatura de la función AUD-F12 del mismo documento, en el rango F02–F12: no se cuenta como cita | `03_Funciones/Funciones, tareas y cometidos – Auditor – óptima V5.0.md:30` |
| INFO | CITA_EN_CONTEXTO_AJENO | F12 | F12 aparece como abreviatura de la función PROS-F12 del mismo documento, en el rango F02–F12: no se cuenta como cita | `03_Funciones/Funciones, tareas y cometidos – Analista de Prospectiva y Horizontes – óptima V5.0.md:31` |
| INFO | CITA_EN_CONTEXTO_AJENO | F12 | F12 aparece como notación dentro de una fórmula: no se cuenta como cita | `02_System_prompts/System prompt - Analista de Materias Primas - Versión óptima V5.0.md:81`, `02_System_prompts/System prompt - Analista de Materias Primas - Versión óptima V5.0.md:81`, `02_System_prompts/System prompt - Analista de Materias Primas - Versión óptima V5.0.md:111`, `02_System_prompts/System prompt - Analista de Materias Primas - Versión óptima V5.0.md:111` |
| INFO | CITA_EN_CONTEXTO_AJENO | F31 | F31 aparece como código JEL de clasificación de la literatura económica: no se cuenta como cita | `02_System_prompts/System prompt - Documentador para el Analizador - Versión óptima V5.0.md:368` |

### (d) Fichas del Catálogo

`CATALOG_VERSION` del código: 5.0; `catalog_version` del Catálogo: 5.0; nombre del archivo: V5.0. Encabezados `### ID`: 81 (el Catálogo declara 81); filas del índice §4: 81; `FICHAS_CATALOGO`: 81; manejadores CT-09 (`IMPLEMENTADAS`): 80; servicios CT-10 (`SERVICIOS_CT10`): AUD-REX-001.

Clases: IMPLEMENTADO 81, SOLO_CATALOGO 0, SOLO_CODIGO 0, ID_DISTINTO 0.

Fichas por sección del Catálogo (las de secciones con «V5.0» en el título son las nuevas de esa versión: 21; las demás, 60):

| Sección | Fichas | Nueva en V5.0 |
|---|---|---|
| 6. Fichas heredadas de la línea V3.0 | 17 | no |
| 7. Fichas nuevas — núcleo transversal | 15 | no |
| 8. Fichas nuevas — renta variable (PERF-ACC) | 4 | no |
| 9. Fichas nuevas — renta fija y crédito (PERF-FIR) | 5 | no |
| 10. Fichas nuevas — divisas (PERF-FX) | 2 | no |
| 11. Fichas nuevas — materias primas (PERF-CMD) | 4 | no |
| 12. Fichas nuevas — inmobiliario cotizado (PERF-REI) | 4 | no |
| 13. Fichas nuevas — criptoactivos (PERF-CHR) | 4 | no |
| 14. Fichas nuevas — alternativos y mercados privados (PERF-PRV, PERF-ALT) | 5 | no |
| 15. Fichas nuevas V5.0 — índices bursátiles (PERF-IDX) | 4 | sí |
| 16. Fichas nuevas V5.0 — fondos y vehículos de inversión colectiva (PERF-ETF) | 4 | sí |
| 17. Fichas nuevas V5.0 — derivados financieros (PERF-DER) | 4 | sí |
| 18. Fichas nuevas V5.0 — instrumentos monetarios y liquidez (PERF-MON) | 4 | sí |
| 19. Fichas nuevas V5.0 — tipos de interés, crédito y volatilidad (PERF-TCV) | 5 | sí |

Menciones a otra versión del Catálogo:

Ninguna.

Ficha a ficha:

| Ficha | Clase | Madurez (índice §4) | FICHAS_CATALOGO | Manejador | servible() | Parecida a |
|---|---|---|---|---|---|---|
| ACC-ERP-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| ACC-FACT-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| ACC-MOM-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| ACC-VAL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| ALT-AUC-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| ALT-DESMOOTH-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| ALT-HF-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| AUD-REX-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-10 | no | — |
| BIB-MET-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| BT-DSR-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| BT-PBO-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| BT-VAR-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| CHR-FLOW-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| CHR-FUND-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| CHR-ONCHAIN-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| CHR-TOKEN-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| CMD-CURVE-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| CMD-INV-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| CMD-REAL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| CMD-RETDEC-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| DEC-VOI-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| DER-OPT-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| DER-ROLL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| DER-SKEW-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| DER-TERM-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| DER-VRP-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| FC-CAL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| FC-EVAL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| FIN-CAGR-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| FIR-CARRY-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FIR-CRED-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| FIR-CURVE-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FIR-PRICE-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FIR-SPREAD-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FON-DISC-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| FON-FLOW-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| FON-LEV-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| FON-TD-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| FX-BEER-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| FX-BRK-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FX-CARRY-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| FX-COINT-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FX-CORR-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| FX-MOM-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FX-PPA-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FX-REGIME-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FX-STL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| FX-TREND-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| FX-VOL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| IDX-CONC-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| IDX-ERP-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| IDX-REB-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| IDX-REL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| ML-CAL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| ML-CLUS-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| ML-PRED-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| MON-EXP-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| MON-FIX-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| MON-REAL-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| MON-YLD-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| PRV-CF-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| PRV-PME-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| REG-HMM-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| REI-CAP-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| REI-FFO-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| REI-LEV-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-119)) | sí | CT-09 | sí | — |
| REI-NAV-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| RISK-DD-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| RISK-VAR-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| SCN-H-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| SCORE-RK-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| SIM-MC-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| ST-DESC-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |
| ST-INF-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| TCV-BEI-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| TCV-CDS-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| TCV-SLOPE-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| TCV-TP-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| TCV-VIXTS-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-106)) | sí | CT-09 | sí | — |
| TEM-DIFF-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor, casos de control registrados (T-112)) | sí | CT-09 | sí | — |
| VOL-GARCH-001 | IMPLEMENTADO | IMPLEMENTADO (ejecutor V1.0, pruebas unitarias) | sí | CT-09 | sí | — |

| Nivel | Código | ID | Motivo | Dónde |
|---|---|---|---|---|
| INFO | CITA_EN_CONTEXTO_AJENO | IDX-FICT-001 | IDX-FICT-001 aparece como símbolo de una serie (valor de «serie_ht01» en 05_Archivos_operativos/Registro de cálculos del Motor (esquema V2.0).md:94), no una ficha: no se cuenta como cita | `05_Archivos_operativos/Registro de cálculos del Motor (esquema V2.0).md:94`, `05_Archivos_operativos/Registro de oportunidades (esquema V3.0).md:130`, `05_Archivos_operativos/Registro de oportunidades (esquema V3.0).md:130`, `05_Archivos_operativos/Registro de pronósticos congelados (esquema V2.0).md:132`, `05_Archivos_operativos/Registro de pronósticos congelados (esquema V2.0).md:133` |
| INFO | FAMILIA_DESCONOCIDA | WI-METH-001 | WI-METH-001 tiene forma de ficha y su familia (WI) no es la de ninguna ficha del Catálogo ni del código: probablemente es otro identificador | `05_Archivos_operativos/Registro de Fuentes para el Analizador de Tendencias de Inversión - V3.2.md:5594` |

### (e) Referencias de los archivos operativos

Citadas en `02_System_prompts/`, `03_Funciones/`; entradas en `05_Archivos_operativos`: 1473 (más 15 en los Registros de bajas). Dónde se definen: ANA-DOC en `05_Archivos_operativos/Documentación para el Analizador de Tendencias de Inversión - V3.2.md`; DOC-MOT en `05_Archivos_operativos/Documentación para el Motor de Cálculo Avanzado - V3.2.md`; RF en `05_Archivos_operativos/Registro de Fuentes para el Analizador de Tendencias de Inversión - V3.2.md`; TA en `05_Archivos_operativos/Documentación para el Analizador de Tendencias de Inversión - V3.2.md`; TF en `05_Archivos_operativos/Registro de Fuentes para el Analizador de Tendencias de Inversión - V3.2.md`; TM en `05_Archivos_operativos/Documentación para el Motor de Cálculo Avanzado - V3.2.md`.

| Prefijo | Citas | ID distintos | Existen | De baja | No existen | Otra forma |
|---|---|---|---|---|---|---|
| DOC-MOT | 4 | 4 | 4 | 0 | 0 | 0 |
| RF | 2 | 2 | 1 | 0 | 0 | 1 |
| TA | 146 | 23 | 23 | 0 | 0 | 0 |
| TF | 125 | 19 | 19 | 0 | 0 | 0 |
| TM | 107 | 18 | 18 | 0 | 0 | 0 |

| Nivel | Código | ID | Motivo | Dónde |
|---|---|---|---|---|
| AVISO | REF_FORMA_DISTINTA | RF-1 | RF-1 no tiene la forma de las entradas RF- (4 cifras): probablemente es otro identificador | `02_System_prompts/System prompt - Auditor - Versión óptima V5.0.md:459` |

### (f) Puertas PS

§9.3: «9.3 Puertas de selección PS1–PS8». Definidas: 8.

| Puerta | §9.3 | Citas | Archivos |
|---|---|---|---|
| PS1 | sí | 50 | 26 |
| PS2 | sí | 39 | 26 |
| PS3 | sí | 68 | 30 |
| PS4 | sí | 5 | 3 |
| PS5 | sí | 5 | 3 |
| PS6 | sí | 4 | 2 |
| PS7 | sí | 7 | 5 |
| PS8 | sí | 39 | 15 |

Sin hallazgos.
<!-- INFORME:FIN -->

## Lectura del informe

- **El desfase V4.0 ↔ V5.0 del Catálogo está resuelto en el código.** El verificador lo comprueba con el corpus y el código, no
  lo da por hecho: `CATALOG_VERSION` es 5.0 como el nombre y el `catalog_version` del Catálogo; las 81 fichas con encabezado
  `### ID` están en el índice §4 y en `FICHAS_CATALOGO`, 80 tienen manejador CT-09 y AUD-REX-001 se sirve por la re-ejecución
  CT-10 (`SERVICIOS_CT10`), así que las 81 salen IMPLEMENTADO y ninguna SOLO_CATALOGO, SOLO_CODIGO o ID_DISTINTO; la madurez que
  lee `madurez_catalogo()` coincide fila a fila con el índice §4. De las 81, 21 están en secciones «V5.0» del Catálogo y 60 en
  las anteriores: el «60 frente a 81» del desfase.
- **Desde T-166 (17-11-2026) no queda ninguna mención a la versión 4.0 del Catálogo, ni ficha o RF inexistente:** el informe
  de arriba da 0 errores y solo el AVISO de «RF-1» (la tarjeta del Auditor). Antes de esa entrega quedaban textos del corpus
  con la versión 4.0: seis menciones en los prompts MC-01 a MC-05 (una en
  prosa y cinco en ejemplos JSON) y una línea de las funciones del Motor (D-2), más el ejemplo del Registro de cálculos, la
  octava mención, que va con su ficha inexistente en D-3. El literal `catalog_version` 4.0 que el código escribía en
  `evaluador.py` y el docstring de `motor/operaciones.py` (D-1) los corrigió T-160: el escaneo de los `.py` del paquete ya no
  encuentra ninguna versión distinta de la vigente.
- **Contratos (a), reglas (b), archivos (c) y puertas (f): sin errores.** Las 25 CT de §6.1 tienen canal en `contratos.py` y
  `canal_permitido` admite al menos un par en cada una; no se cita ninguna CT, regla, archivo o puerta inexistente. El mapa de
  (c) da el archivo real de cada F por su H1. Los INFO de (b) y (c) son códigos de la lista JEL del Documentador, notación de una
  fórmula de futuros y rangos de funciones de cada documento de `03_Funciones` («F02–F12» por `PROS-F02` a `PROS-F12`,
  «ORQ-F03 a F05»): el informe dice cuál y dónde. Los INFO de (d) son IDX-FICT-001, que el corpus declara como símbolo de una
  serie (`serie_ht01`), y WI-METH-001, con forma de ficha pero de una familia que no existe y sin parecido con ninguna.
- **(e) referencias:** las 23 TA, 18 TM y 19 TF citadas en prompts y funciones existen en `05_Archivos_operativos`; de las RF,
  la del ejemplo del prompt del Evaluador existe desde T-166 (RF-0046; antes, `RF-0123`, sin entrada), y «RF-1» del prompt del Auditor es una tarjeta del
  informe visual, no una referencia (AVISO, sin acción).

## Decisiones propuestas

Solo lo que estaba desincronizado al medir. La Fase 0 no aplica ninguna; D-1 la aplicó después T-160, y D-2 a D-4, T-166. Las cuatro están en el
registro de decisiones del Bloque A (`sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`, §6).

| # | Qué está desincronizado (hallazgo del informe) | Decisión propuesta | Por qué | Quién la decide y cuándo | Incidencia |
| --- | --- | --- | --- | --- | --- |
| D-1 | El código escribe `catalog_version` 4.0 en la entrada del Registro de cálculos de la tasa base RI-TB (FC-EVAL-001), y el docstring de `motor/operaciones.py` dice «Catálogo de cálculos V4.0» (CATALOG_VERSION_LITERAL, MENCION_OTRA_VERSION_CODIGO) | Escribir `servicio.CATALOG_VERSION` en lugar del literal y corregir el docstring | Una re-ejecución CT-10 usa la versión del artefacto (§1.1 del Catálogo); un artefacto que declara 4.0 cita un Catálogo que ya no es el vigente. Con la constante, el próximo cambio de versión no deja literales atrás | El agente, por defecto (`compartida/2026-11-13_decide-el-agente-por-defecto`). **Aplicada por T-160** (16-11-2026): `evaluador.py` escribe `servicio.CATALOG_VERSION` y el informe ya no da CATALOG_VERSION_LITERAL ni MENCION_OTRA_VERSION_CODIGO | INC-T157-02 |
| D-2 | Seis menciones de los prompts MC-01 a MC-05 y una línea de las funciones del Motor citan el «Catálogo V4.0» (MENCION_OTRA_VERSION) | Dejar el corpus como está en esta entrega; en la próxima, «Catálogo V5.0» (o la versión vigente) | Es corpus congelado: no se edita en una fase de código. Los prompts son datos en tiempo de ejecución y el código no lee de ellos la versión: el Registro de cálculos lleva `CATALOG_VERSION` en los servicios del Motor, así que el texto no cambia ningún cálculo | El operador, en la próxima entrega del corpus del Bloque A (re-congelado deliberado). **Conviene antes de la Fase 5** (modo sombra con la API real, ya autorizada): con la API, «la ficha VIGENTE del Catálogo V4.0» llega tal cual al modelo. **Decidida por delegación del operador (16-11-2026) y aplicada por T-166** (17-11-2026): «Catálogo V5.0» en los seis sitios de los prompts y en MOTOR-F05 | INC-T157-03 |
| D-3 | El ejemplo del Registro de cálculos (`05_Archivos_operativos`, RC) cita la ficha `FX-MC10-003`, que no existe en el Catálogo V5.0, con `catalog_version` 4.0 (FICHA_CITADA_INEXISTENTE) | En la próxima entrega, citar una ficha vigente del MC-10 con su versión: FC-EVAL-001 es la que el ejecutor usa para la tasa base RI-TB (`evaluador.py`) | El ejemplo es ficticio, pero es la plantilla de una entrada de RC: quien lo copie cita una ficha que el Motor rechazaría con `OPERACION_SIN_FICHA` | El operador, en la próxima entrega del corpus. **Decidida por delegación del operador (16-11-2026) y aplicada por T-166** (17-11-2026): FC-EVAL-001 con `catalog_version` 5.0 | INC-T157-04 |
| D-4 | El ejemplo del prompt del Evaluador cita `RF-0123`, sin entrada en F9 ni en su Registro de bajas (REF_INEXISTENTE) | En la próxima entrega, citar una RF que exista en F9 o marcarla como ficticia | Un ejemplo con una referencia inexistente enseña a citar fuentes que el bloque no tiene registradas (R7) | El operador, en la próxima entrega del corpus. **Decidida por delegación del operador (16-11-2026) y aplicada por T-166** (17-11-2026): RF-0046 (Goldman Sachs Global Investment Research, TF-05) | INC-T157-05 |

Los criterios técnicos del propio verificador (qué cuenta como «ID parecido» y qué contextos no son citas) son INC-T157-01.
