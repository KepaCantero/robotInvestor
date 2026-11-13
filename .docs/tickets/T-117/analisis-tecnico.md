# T-117 · Análisis técnico

## Causa raíz o motivo

El GC1 por código de la V6 (T-101) tenía un umbral único, 0,75, pensado para la señal compuesta. La señal compuesta es la media de tres familias; en renta fija, liquidez y tipos, curvas y volatilidad la familia de tendencia suele quedar neutra (0,5), y entonces llegar a 0,75 exige casi el máximo en las otras dos. El análisis de T-101 ya lo decía («apenas deja pasar ámbitos de renta fija, liquidez y tipos») y la QA de T-101 (H-28) añadió que un solo umbral no vale para otras señales. Además, el filtro no comprobaba la concordancia de dos familias que pide el Anexo A.

## Evidencia

Señal compuesta de cada ámbito del universo de ejemplo en 17 fechas (cada cuatro semanas, de julio de 2025 a octubre de 2026), con los datos sintéticos:

| Tipo | Ámbitos | Pasan por fecha con 0,75 | Con 0,65 y dos familias |
| --- | --- | --- | --- |
| RV | 7 | 1,5 | 3,1 |
| RF | 8 | 0,8 | 2,1 |
| DIV | 6 | 1,6 | 2,3 |
| MP | 6 | 1,9 | — |
| IDX | 6 | 1,9 | — |
| FON | 4 | 1,5 | — |
| DER | 3 | 0,7 | 0,9 |
| INM | 3 | 0,8 | — |
| CRI | 3 | 0,6 | — |
| ALT | 2 | 0,9 | — |
| MON | 3 | 0,5 | 1,1 |
| TCV | 6 | 0,9 | 2,1 |

Con 0,75 todos los que pasan tienen ya dos familias concordantes. La tendencia sale «sin tendencia» en 65 de 136 observaciones de RF y en 50 de 102 de TCV.

## Implementación

- Archivos cambiados y por qué:
  - `bloque_a/11_Ejecutor/bloque_a/diseno_v6.py`: `gc1()` lee el umbral del tipo y exige la concordancia; `validar()` rechaza la configuración no válida; `FAMILIAS_SENAL_COMPUESTA = 3`.
  - `bloque_a/11_Ejecutor/config/por_defecto.yaml`: `senal_por_perfil` relleno, `umbral_por_perfil` y `familias_min`.
  - `bloque_a/11_Ejecutor/tests/test_t117_gc1.py`: 43 pruebas.
  - `docs/incidencias.md` (INC-T117-01), la deuda y `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`.
- Decisiones tomadas:
  - señal compuesta en los doce tipos, y no otra señal por tipo: las demás señales del Motor no están en la escala del umbral;
  - 0,65 solo en RF, MON y TCV, los tres tipos que T-101 señaló y que la medida confirma; DER, INM, CRI y ALT tienen dos o tres ámbitos y la medida no permite afinar;
  - sin recuento de familias no se descarta: coherente con «la falta de señal no prueba la falta de oportunidad».
- Límites conocidos:
  - datos sintéticos y universo pequeño: valores provisionales;
  - la configuración se fusiona por claves: para devolver un tipo al umbral general hay que ponerle 0,75, no borrar la clave (dicho en el YAML y probado);
  - el registro de cobertura de HA guarda el umbral y `familias_min`, no los motivos de cada descarte.
- Comandos exactos para probarlo, desde `bloque_a/11_Ejecutor`: `python -m pytest -q tests/test_t117_gc1.py` (43 pruebas) y `python -m pytest -q tests/test_t101_v6.py tests/test_t102_filtro.py tests/test_t113_deuda.py tests/test_t88_consumo.py`.
