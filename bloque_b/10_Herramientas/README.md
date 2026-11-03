# Herramientas deterministas del Bloque B · V2.0 (actualizado V2.1)

**Bloque B · Robot Investor · V2.0 · actualizado V2.1, 03/11/2026** · Subordinado al Documento 0 del Bloque B, óptima V2.1 (secciones 4.4, 7.10, 8.6, 8.7, 9.12, 9.13 y 10.8; Anexos A, A.2 y B) y al catálogo G3 del *Plan de pruebas del Bloque B - V2.0* (actualizado V2.1, sección 3). Las herramientas declaran `VERSION = "2.1"`.

Implementaciones de referencia en Python (≥ 3.10), sin modelo de lenguaje, con su batería de pruebas. El ejecutor `11_Ejecutor/bloque_b` las usa como **copias literales** (`bloque_b/herramientas/referencia/`); una prueba del ejecutor comprueba que no divergen.

Estado de madurez (R26): **implementadas, con pruebas unitarias superadas**. Ninguna está **validada** con datos reales.

| Código | Archivo | Función | Dependencias |
|---|---|---|---|
| HT-02 | `ht02_verificador_enlaces.py` | Verificador de enlaces y contenido de F7, F8, F9 y FM (estado HTTP, redirecciones, DOI, muro de pago, retractaciones, hash y SimHash, Wayback). **Copia del Bloque A V5.0** (solo cambia la cabecera) | estándar (+ HT-07) |
| HT-03 | `ht03_puntuaciones.py` | Estrategia (matriz 8.3 con moduladores y regla de profundidad; horizontes H1–H5; activación de AG-B24), puntuaciones A, E, C y S; **V2.1**: PCB, cuello material, AE y PEM, puertas PV1–PV3 y mejores opciones por eslabón; banda marginal, puertas PA y PC, veredictos del ámbito y del candidato, normalización del universo, top-N, alternativas, diversidad (9.7), GC3, apuestas independientes, relevancia decisional y siguiente paso | estándar |
| HT-07 | `ht07_legibilidad.py` | Fernández-Huerta corregido (Law, 2011), longitud de frases y jerga. **Copia del Bloque A V5.0** (solo cambia la cabecera; fórmula idéntica) | estándar |
| HT-08 | `ht08_monitor_tiempo.py` | Modelo de tiempos (p50/p80 por fase y, V2.1, **por capa**; camino crítico; radar de emergentes y desglose de la cadena), opción `HASTA_PV2`, PT30 previa y en ejecución, PTA con margen, opciones de CT-B-05, política de autorización automática con tope, recordatorio y caducidad, puntos de control con huella, recalibración, cronómetro y órdenes de instancias | estándar |
| HT-09 | `ht09_validador_g3.py` | Validador G3 con el catálogo **G3B-EST/DAT/MET/CON/SEL/TMP/ENT-nn** (107 comprobaciones: 88 de la V2.0 y 19 de la V2.1), en las pasadas PAQUETE_SINTESIS (F8) y FIDELIDAD_ENTREGABLES (F9) y en los perfiles reducidos **PAR** (`validar_informe_parada`) y **CIC** (`validar_informe_seguimiento`) | estándar (+ HT-03, HT-07; `jsonschema` y `openpyxl` opcionales) |
| HT-10 | `ht10_anexo_datos.py` | Anexo de datos y cálculos en XLSX y CSV (V2.1: hojas `Eslabones`, `Opciones_eslabon` y `Emergentes`; `eslabon_id` y `origen_seleccion` en `Encargos_C`); plantilla vacía con `--plantilla` | `openpyxl` |
| HT-11 | `ht11_cribador.py` | Universo invertible por tipo de activo desde CSV y listas, en punto del tiempo (sin sesgo de supervivencia ni de anticipación), con filtros duros de los doce playbooks y del marco 2.7 | estándar |

HT-01 (datos y bóveda), HT-04 (gráficos), HT-05 (planificador) y HT-06 (índice y caché) viven en el ejecutor (`bloque_b/herramientas/`), porque dependen de su almacén y su configuración.

## Pruebas

```bash
cd 10_Herramientas
python3 -m pytest -q tests        # 148 pruebas (+ 38 subpruebas), ≈ 13 s, sin red (HT-02 usa un servidor HTTP local)
```

## Uso por línea de comandos

```bash
# HT-03: estrategia y cálculo completo (orden de cálculo de 9.3)
python3 ht03_puntuaciones.py --estrategia entrada_estrategia.json     # {tipo_objeto, horizonte, tipos_materiales, nivel, desviaciones}
python3 ht03_puntuaciones.py entrada.json --salida salida.json        # A, E, refutación, RE, puertas, candidatos_por_tipo
# HT-08: estimación y puerta previa (código 1 si dispara PT30)
python3 ht08_monitor_tiempo.py ejemplos/plan_ejemplo.json
# HT-09: G3 (0 APTO · 1 APTO_CON_ADVERTENCIAS · 2 BLOQUEADO · 3 error)
python3 ht09_validador_g3.py ejemplos/paquete_analisis_mercado_ejemplo.json \
   --esquema "../06_Plantillas_entregables/Esquema JSON - Paquete de análisis de mercado - Bloque B - V2.0.json" \
   --visual "../06_Plantillas_entregables/Plantilla - Informe visual para el usuario - Bloque B - V2.0.html"
# HT-10: anexo (o --plantilla)
python3 ht10_anexo_datos.py ejemplos/paquete_analisis_mercado_ejemplo.json --salida /tmp/anexo
# HT-11: universo
python3 ht11_cribador.py --tipo RV --csv ejemplos/universo_rv_ejemplo.csv --fecha 2026-10-30 --ambito redes_electricas_europa
# HT-07 y HT-02: igual que en el Bloque A
python3 ht07_legibilidad.py ejemplos/informe_visual_ejemplo.html
python3 ht02_verificador_enlaces.py "../05_Archivos_operativos/Registro de Fuentes para el Analizador de Mercados - V2.0.md" --salida /tmp/enlaces
```

## HT-03: decisiones de implementación

- **Aritmética exacta** con fracciones; los empates exactos de redondeo se resuelven **hacia abajo** (prudencia). A y E se redondean al múltiplo de 5; C y S al entero.
- **Moduladores** (8.3.2–8.3.3): factor del horizonte × media geométrica de los factores de los tipos con peso material; renormalización con enteros por el **método del mayor resto** (A.2: suma 100 antes de la regla de profundidad).
- **Profundidad**: ≥ 12 → P3 · 7–11 → P2 · 4–6 → P1 · ≤ 3 → P0; D9 ≥ P2 y D12 ≥ P1. **N1**: un escalón menos (mínimo P1); D9 y D12 se mantienen en P2 solo si ya lo eran (A.2). **N3**: peso ≥ 9 → P3.
- **C en N1** sin simulación: `RE = None` redistribuye su peso (A.2).
- **Precedencia INVERTIR / ESCALONADO** (A.2): prevalece INVERTIR salvo que el Director active una condición de escalonamiento (`catalizadores_escalonados`, `valoracion_parcialmente_descontada`, `dispersion_alta`).
- **Banda marginal**: con segunda pasada se usa el menor valor; sin ella, PA7 (ámbito) o PC7 (candidato, máximo SECUNDARIO).
- **Diversidad**: el máximo por subclúster es ⌊0,4 × top-N previsto⌋ (mínimo 1); los desplazados pasan a alternativas con su motivo y el candidato frente al que se desplazan.
- **Siguiente paso** (concreción declarada de 7.9): ENVIAR_CANDIDATOS_A_C si INVERTIR/ESCALONADO con prioritarios; PROFUNDIZAR_EN_B si VIGILAR con resultado PARCIAL/NO_CONCLUYENTE o con relevancia ALTA y E < 70; VIGILAR o DESCARTAR en el resto.
- **Métricas por playbook**: `PLAYBOOKS[tipo]["metricas"]` traduce cada componente de S a métricas concretas (las de precio, como `momento_12_1` o `volatilidad_1a`, las calcula el Motor con HT-01). Son la propuesta inicial; el Evaluador las ajusta dentro de bandas y el operador las cambia por tipo 3.

### HT-03: funciones de la V2.1

- `calcular_PCB(sev, pers, rel)` = round(100·sev·pers·rel/125) (empate hacia abajo); `estado_indicador_cuello` aplica los umbrales ámbar/rojo del Anexo A; `severidad_cuello` y `evaluar_cuello` derivan severidad, PCB y `material` (PCB ≥ 30 y ≥ 2 rojos).
- `calcular_AE(componentes, PCB)` con pesos 20/20/15/20/15/10 (el componente «cuello» se deriva del PCB si no viene); eslabón atractivo con AE ≥ 60. `calcular_PEM(criterios)` con pesos 20/25/15/15/15/10 (criterios propuestos por AG-B24; el Motor MC-B07 replica la aritmética y el Director la confirma con HT-03).
- `evaluar_pv1` (eliminatorios y debilidades; dos debilidades detienen), `evaluar_pv2` (A y E provisionales ≥ 50 y tesis viva; si solo falla E, `consulta_previa = CONFIRMACION_SUPUESTO`), `evaluar_pv3` / `eslabon_cualifica` (AE ≥ 60 o cuello material, con opción PC1–PC4 y S ≥ 50; ESL-00 cualifica siempre).
- `mejores_por_eslabon`: hasta 5 por eslabón cualificado (N1: 3, solo el crítico), orden por S y pureza al eslabón, sin duplicar el top-N (`en_top_n_tipo`); `procesar` acepta `eslabones` y `eslabon_critico` y devuelve `mejores_por_eslabon` (las prioritarias adicionales generan encargo propio; si el veredicto final del ámbito no es INVERTIR/ESCALONADO, bajan a SECUNDARIO).
- Horizonte H5: moduladores de la matriz (columna H5), D9 ≥ P2, relevancia de la iliquidez en H4 y H5.

## HT-08: modelo de tiempos inicial

Minutos por nodo (calibrables por el Evaluador con F1): F0 1 · F1 1 + 0,3/tipo · F2 = máximo por especialista de (P1 0,8 · P2 1,6 · P3 2,8 por dimensión) + 0,8 de integración + 30 % de las dimensiones que cubre el Director · F3 1,5 · F4 2,5 (N1 1) ∥ F5 = máximo por tipo de (1 + 0,02 × universo + 0,2 × finalistas) · F6 1,5 + 0,1 × finalistas × tipos (N1 0,8) · F7 1,5 · F8 0,5 + muestreo × (2,5 + 1 × 0,5 vueltas) · F9 2 · F10 0,5; factor de nivel N1 0,5, N3 1,6; p80 = 1,2 × p50. Con estos valores, un N2 de un tipo queda en ≈ 29 min (p80) y uno de tres tipos en ≈ 32 min (dispara PT30). La puerta en ejecución proyecta consumido + p80 restante × desviación observada (acotada a 0,8–2,5). **V2.1**: AG-B24 añade 1,2 min (radar) y el desglose de la cadena 0,4 min; `estimar` devuelve `desglose_por_capa`, su p80 y `minutos_p80_hasta_pv2`; `opciones(..., pv2_pendiente=True)` añade `HASTA_PV2` (capas 0–2) y la versión ≤ 30 min apunta al 90 % del umbral.

Política de autorización automática (`aplicar_politica`): se aplica la primera regla que cubre el caso; condiciones admitidas `relevancia`, `nivel` (valor o lista), `origen`, `siguiente_paso_A`, `puerta`, `minutos_max` (el p80 necesario no supera el valor) y `minutos_p80_min` (el p80 necesario alcanza el valor; POL-3 del Runbook). Acciones `AUTORIZAR_HASTA`, `ELEGIR_OPCION` y `NO_AUTORIZAR`. El tope efectivo es min(tope de F10, 480 min); por encima, la decisión es siempre del Broker.

## HT-09: comprobaciones del catálogo G3B

Las 107 comprobaciones del Plan de pruebas se devuelven siempre, con resultado PASA, FALLA o NO_APLICA (con motivo). Clase B → BLOQUEADO; clase W → APTO_CON_ADVERTENCIAS. G3B-CON-04 es mixta: la parte de campos ausentes es B y la relevancia distinta de la regla de 7.9 es W.

| Situación | Comprobaciones |
|---|---|
| **Deterministas con el paquete** (pasada F8) | EST-01, 03, 05, 06, 07, 09, 10 · DAT-01, 03, 04, 06, 07, 12 · MET-01, 03–12, 14, 16, 17 · CON-01–18 · SEL-01–15 · TMP-01–04 |
| **Con insumos opcionales** | EST-04 y MET-02 (`parametros_f10`) · DAT-02, 05, 10, 13 (`f2`: ids, trazas, dat, evd_estados, calc_estados) · MET-15 (`puntuaciones.cambio_frente_previo`) · EST-08 (`rutas`) · CON-14 completa (`preguntas` de la petición) |
| **Segunda pasada** (F9, entregables) | ENT-01–10 y DAT-08 (informe visual, técnico, memorando y anexo XLSX) |
| **V2.1** (con `mapa_eslabones` y `f1` opcionales) | EST-11, EST-14 · MET-18–22 · CON-20, CON-21 · SEL-16–18 · TMP-05 (F8) · ENT-11, ENT-12 (F9; el texto de las tablas por eslabón del informe visual va dentro de `<section aria-labelledby="t-eslabones">`) |
| **Perfiles reducidos** | PAR (`validar_informe_parada`): EST-05, 06, 12, 14 · MET-18 · CON-15, 16, 19, 21 · DAT-08 · TMP-05 · CIC (`validar_informe_seguimiento`): EST-05, 06, 13 · CON-15, 16, 21 · SEL-16 · DAT-08 · TMP-06. El resto del perfil del Orquestador (5.3 bis) lo verifica él contra F1, F2 y RC |
| **Manuales del Orquestador** (NO_APLICA «manual») | **EST-02** campos comunes de los mensajes · **DAT-09** unidades y divisas · **DAT-11** raíces y corroboración frente a F2 · **DAT-14** discrepancias DSC-B · **MET-13** madurez de los métodos frente a RC y CC |

Limitaciones conocidas: G3B-ENT-02 (fidelidad) comprueba los valores S y las puntuaciones citados y la presencia del veredicto, la fecha de corte y los prioritarios; no compara cada afirmación textual (esa parte queda en la auditoría experta). G3B-ENT-08 comprueba los textos alternativos; la paleta apta para daltonismo se verifica en la plantilla, no en cada informe.

## HT-11: columnas de los CSV

Comunes: `id, isin, nombre, tipo_activo, region_mercado (EEE, UK, CH, US, CA, JP, AU, HK, SG u OTRO), mercado, divisa, emisor, ambitos (lista con «;»), subcluster, sancionado, suspendido, fecha_alta, fecha_baja, fecha_dato`. Por tipo (filtros de 8.5): RV `capitalizacion_meur, volumen_medio_meur, flotante_pct, ejercicios_auditados, salida_bolsa_reciente, opinion_auditoria` · RF `precio_observable, tipo_emisor, saldo_vivo_meur, folleto, impago, vencimiento, calificacion, metricas_credito, denominacion_min_eur` · DIV `controles_capital, instrumento_acceso, instrumento_en_marco` · MP `tipo_instrumento (futuro|etc|etn), mercado_regulado, interes_abierto, colateral_auditado` · IDX `metodologia_publica, replicable_ucits_o_futuro, historial_anos, reconstruccion_documentada` · FON `ucits, kid, cerrado_cotizado, gestion, patrimonio_meur, historial_anos, historial_indice_anos, clase_eur_o_cubierta, en_liquidacion` · DER `tipo_instrumento, mercado_regulado, kid, interes_abierto, perdida_superior_desembolso` · INM `capitalizacion_meur, volumen_medio_meur, nav_frecuencia_meses, cuentas_auditadas, ltv` · CRI `stablecoin, acceso_mica_o_etp, capitalizacion_meur, historial_meses, lavado_detectado, advertencia_regulatoria, es_protocolo, codigo_auditado` · ALT `cotizado_o_eltif, nav_frecuencia_meses, nav_auditado, mecanismo_liquidez, gestor_regulado` · MON `tipo_instrumento, tipo_emisor, calificacion_corto, plazo_dias, mmf_reglamento, kid` · TCV `mercado_regulado, ucits, kid, volumen_medio_meur, interes_abierto, apalancado_o_inverso`. Un filtro no verificable por falta de dato excluye con `DATOS_INSUFICIENTES`. Un vehículo colectivo (`tipo_instrumento` etf, fondo o sicav) fuera del universo FON se excluye con «se asigna a FON» (2.6, regla 2), coherente con G3B-SEL-09. La tabla de 2.6 (filas MON y TCV), 8.5.11 y 8.5.12 citan fondos y ETF dentro de MON y TCV, en contradicción con esa regla; las herramientas aplican la regla 2 (más estricta) hasta que el Documento 0 lo aclare. Los fondos cerrados y ELTIF de ALT no se excluyen.

## Ejemplos (`ejemplos/`)

`paquete_analisis_mercado_ejemplo.json` (copia del ejemplo de `06`, APTO; V2.1: metodología 2.1, `mapa_cadena_valor` con cuatro macro-eslabones y un insumo, opción añadida por cobertura del eslabón con su encargo C.x, capas y puertas, dos consultas al Broker —una con supuesto aplicado— y lista profesional), `universo_rv_ejemplo.csv` (incluye una excotizada, una salida a bolsa futura, una sancionada y un mercado fuera del marco), `plan_ejemplo.json`, `referencias_ejemplo.md`, `informe_visual_ejemplo.html` y `jerga_personalizada.txt`.
