# T-90 · Análisis técnico

## Causa raíz o motivo

En el bucle de notas del informe dimensional (`bloque_b/11_Ejecutor/bloque_b/orquestacion.py`), una nota con fechas de fuente que no pasaban `fechas_de_fuente` se saltaba con `continue`, sin dejar rastro.

## Implementación

- **Exclusión:** la nota se sigue excluyendo. Cada exclusión se cuenta por (dimensión, especialista, motivo):
  - **fuga:** alguna fecha es posterior al corte;
  - **fechas:** son incompletas, ilegibles o incoherentes.
- **Declaración:** al terminar el bucle, `estados_degradados` gana una entrada por cada clave: «Dn: k nota(s) de AG-… excluida(s) por …».
- **Pruebas:** `tests/test_t90_nota_fuera_de_corte.py`.
- **Límites:** el motivo se deduce de las fechas que trae la nota. Una fecha posterior al corte manda sobre el resto.
