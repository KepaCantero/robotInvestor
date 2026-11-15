# T-133 · Pruebas (banco de medida)

| Suite | Antes | Después |
| --- | --- | --- |
| `.docs/scripts/pruebas_banco_medida.py` | 87 | 98 en verde |
| Mutantes (`mutantes.py`, esta carpeta) | — | 0 de 68 vivos |
| Simulación nula de T-94 (100 mundos) | 9,5 % y 10,0 % | 10 % y 10 % |

| Hallazgo | Prueba |
| --- | --- |
| H-21 y H-22 | `test_t133_h21_h22_la_fuente_es_el_contenido_de_los_datos` |
| H-23 | `test_t133_h23_verificar_no_se_fia_del_registro_que_cita_la_carpeta` |
| H-24 | `test_t133_h24_una_fecha_fuera_de_la_muestra_no_deja_repetida_a_otra` |
| H-25 | `test_t133_h25_una_neutral_no_gasta_ventana` |
| H-26 | `test_t133_h26_consumo_estricto` |
| H-27 | `test_t133_h27_el_minimo_de_un_experimento_es_el_de_a` |
| H-28 | `test_t133_h28_*` (S04, N19 y C01) |
| H-29 | `test_t133_h29_version` |

Se adaptan cuatro pruebas anteriores por cambios de diseño:
- dos de `verificar` pasan `--registro`, porque sin él se compara con el registro del agente;
- la del mínimo de fechas: el mínimo de un experimento es ahora 10;
- la del consumo: la salida incluye `columnas_ausentes`.
