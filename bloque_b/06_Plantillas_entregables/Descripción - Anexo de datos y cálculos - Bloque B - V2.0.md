# Descripción · Anexo de datos y cálculos · Bloque B · V2.0

> **Bloque B · Robot Investor · V2.0 · actualizado V2.1, 03/11/2026.** Subordinada al Documento 0 del Bloque B, óptima V2.1 (secciones 9.12, 9.13, 14.5 y 14.6). Acompaña a `Plantilla - Anexo de datos y cálculos - Bloque B - V2.0.xlsx`, generada por **HT-10** (`10_Herramientas/ht10_anexo_datos.py --plantilla`).

## Finalidad

El anexo es el entregable 5. Permite a un tercero **rehacer cada cifra y cada ranking** del análisis: toda cifra del informe técnico, del memorando, del paquete JSON y del mapa de oportunidades por eslabón (entregable 6) figura aquí con su fuente, su fecha, su etiqueta epistémica, su clase de cifra y su artefacto (DAT-B o CALC-B), y todo el universo cribado aparece con sus métricas, sus componentes de S y su veredicto o motivo de exclusión. Desde la V2.1 también permite **reconstruir PCB, AE y PEM por eslabón** con HT-03 (`calcular_PCB`, `calcular_AE`, `calcular_PEM`).

- **Generador:** HT-10, invocado por AG-B17 (y por AG-B12 y AG-B02 en seco). Sin modelo de lenguaje.
- **Formatos:** XLSX (una hoja por bloque) y CSV (un archivo por hoja, UTF-8 con BOM, en la carpeta `<nombre>_csv/`).
- **Nombre de publicación:** `AAAA-MM-DD_anexo-datos_PET-B-AAAA-NNNN.xlsx` en `Anexos de datos/`.
- **Retención:** 5 años (Anexo A).
- **Fecha de corte:** la misma `data_cutoff` que los otros cinco entregables (hoja Leeme).

## Hojas

| Hoja | Contenido | Columnas |
|---|---|---|
| **Leeme** | Identificación (PET-B, RUN-B, REC-B, fecha, `data_cutoff`, metodología, ámbito, tipo de objeto, veredicto) y descripción de cada hoja | campo, valor |
| **Puntuaciones** | Componentes de A (asimetría 25 · valoración frente a expectativas 20 · calidad del crecimiento 15 · ventaja estructural 10 · catalizadores 10 · momento y flujos 10 · riesgos 10) y de E (raíces 25 · cobertura 15 · metodología 15 · trazabilidad 15 · actualidad 10 · discrepancias 10 · hipótesis 10); RF, RE, C (fórmula y tope) y veredicto | puntuacion, componente, valor, peso, nota |
| **Cifras** | Cada cifra entregada | id, descripcion, valor, unidad, fecha, fuente, dat_calc, etiqueta, clase_cifra, dimension |
| **Fuentes** | Referencias de F7 (TB-), F8 (TMB-) y F9 (TFB-) y fuentes de datos usadas | ref_id, nombre, archivo, tematica, nivel, q, url, fecha_consulta, uso |
| **Universo_‹TIPO›** | Una hoja por tipo de activo aplicable (en la plantilla, `Universo_RV` como modelo). **Todos** los activos del universo bruto en la fecha del universo, invertibles o no | tipo_activo, cand_id, id, nombre, isin, ticker, mercado, divisa, subcluster, emisor, invertible, motivo_exclusion, detalle_exclusion, pureza, pureza_metodo, fecha_dato, comp_PE…comp_CO, S, ic90_S_inf, ic90_S_sup, rango, ic90_rango_inf, ic90_rango_sup, frontera, veredicto, en_top_n, alternativa, alertas y, a continuación, las métricas brutas del playbook (p. ej., roic, deuda_neta_ebitda, momento_12_1, volatilidad_1a…) |
| **Escenarios** | Base, favorable y adverso | nombre, premisas, regimen, probabilidad, base_probabilidad, banda, resultado_vs_referencia, disparadores |
| **Sensibilidades** | Variables críticas | variable, valor_base, valor_bajo, valor_alto, efecto_bajo, efecto_alto, unidad, calc_id |
| **Pronosticos** | PRG-B congelados en F4 | prg_id, tipo, afirmacion, horizonte, fecha_emision, fecha_resolucion, criterio, referencia, banda, probabilidad_publicada |
| **Artefactos** | Índice de artefactos reproducibles del Motor | calc_id, metodo, modulo, perfil, plan_calculo, semilla, fecha_corte, huella_datos, insumos, como_reproducir |
| **Encargos_C** | Resumen de los `paquete_para_bloque_C`, con su eslabón y su origen (`TOP_N` o `MEJORES_POR_ESLABON`) | bloque_c, cand_id, tipo_activo, nombre, isin, S, rango, veredicto, eslabon_id, origen_seleccion, preguntas_para_C |
| **Eslabones** (V2.1) | Desglose de la cadena por eslabón (8.7.1): métricas, indicadores de cuello en semáforo, severidad, persistencia, relevancia, **PCB**, cuello material y componentes de **AE** (9.12) | eslabon_id, padre, nivel, nombre, papel_ambito, tamano, unidad, crecimiento_anual, margen_bruto, margen_operativo, poder_negociacion, hhi, concentracion_pais, es_cuello, indicadores_rojo, indicadores_ambar, indicadores, severidad, persistencia, relevancia_valor, PCB, cuello_material, senal_resolucion, AE_crecimiento, AE_margen_roic, AE_poder_negociacion, AE_cuello, AE_expectativas_inv, AE_sustitucion_inv, AE, calc_cuello, calc_AE |
| **Opciones_eslabon** (V2.1) | Hasta cinco mejores opciones por eslabón con AE ≥ 60 o cuello material, adicionales al top-N (9.13) | eslabon_id, rango, cand_id, nombre, tipo_activo, rol_en_eslabon, pureza_eslabon, S, ic90_S_inf, ic90_S_sup, veredicto, en_top_n_tipo, motivo |
| **Emergentes** (V2.1) | Radar de AG-B24 por eslabón: criterios de PEM (tecnología 20 · tracción 25 · equipo 15 · financiación 15 · posición en la cadena 15 · vía de exposición 10), PEM y vía de exposición (8.7.3) | eslabon_id, emg_id, nombre, tipo, financiacion_importe, financiacion_divisa, ultima_ronda, tecnologia_o_ventaja, senales_traccion, via_exposicion, instrumento, cand_id, fuera_de_filtros, crit_tecnologia … crit_via_exposicion, PEM, etiqueta |

## Reglas

1. **Valores vacíos.** «NA» (no aplica en el playbook) y «NE» (no evaluable, 0 puntos) se escriben como celda vacía en `comp_*` y se explican en `detalle_exclusion` o en la hoja Puntuaciones.
2. **Probabilidades.** `probabilidad_publicada` solo se rellena con certificado (R13). La probabilidad interna de F4 **no** se publica en el anexo.
3. **Reproducibilidad del ranking.** Con las métricas brutas de `Universo_‹TIPO›`, los pesos del playbook (perfil SEL-) y HT-03 (`normalizar_universo` + `calcular_S` + `seleccionar`) se reconstruyen S, el orden, el top-N, las alternativas y las sustituciones por diversidad. El IC del rango procede del bootstrap del Motor (MC-B07), con la semilla de la hoja Artefactos.
4. **Sin datos personales ni claves** (R10, R11). Los alias de credenciales no aparecen en el anexo.
5. **Universo en punto del tiempo.** Incluye los activos dados de baja después de la fecha del universo (sin sesgo de supervivencia).
6. **Reproducibilidad por eslabón (V2.1).** PCB = round(100 · severidad · persistencia · relevancia / 125), con la severidad derivada de los indicadores en semáforo (umbrales de VC-BOT-001); AE = suma ponderada de sus seis componentes (20/20/15/20/15/10); PEM = suma ponderada de sus seis criterios. HT-09 recalcula PCB y AE (G3B-MET-19) y PEM (G3B-SEL-18) y comprueba que el entregable 6 coincide con el paquete (G3B-ENT-11).
7. **Informe de parada.** Una parada en PV1 o PV2 no genera anexo; las cifras que cita el informe de parada llevan su DAT-B o CALC-B en el propio JSON `informe_parada`.
