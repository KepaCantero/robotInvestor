# Notas de deuda — V0.62 (robustez de la infraestructura T-03)

- **Tabla T (pendientes de deuda técnica):** ninguna fila nueva, ninguna resuelta, ninguna cambiada. La
  pieza no encontró ningún defecto real que corregir: los módulos de la infraestructura T-03
  (persistencia, diario, migraciones, reloj y rotación) ya cumplían las cuatro promesas de robustez y la
  batería nueva (`pruebas_robustez_t03.py`) las demuestra y las fija. `Deuda_tecnica.md` queda intacto y
  su contenido sigue viajando resumido en las notas de deuda de cada entrega (desde V0.61, con la cita del
  Documento 0).
- **Tabla D (decisiones del operador):** ninguna fila nueva. La pieza no añade valores de configuración
  ni de parámetros: la batería es prueba, no configuración, y no toca ningún módulo de `validador/`.
- **Tras la revisión independiente (9 de noviembre de 2026):** cuatro hallazgos (uno medio, tres bajos),
  ninguno de producto; ninguno abre ni resuelve filas de deuda. La corrección del hallazgo 1 (los
  `esperados` de la batería al contrato real de los módulos, con el PE-03 admitido en los cuatro objetivos
  que mutan el documento entero y las franquicias muertas retiradas) va con su regresión r01 en la
  batería; los tres bajos son documentales: las frases de no-vacuidad (hallazgo 2), las franquicias
  descritas como activas (hallazgo 3) y las verificaciones no reproducibles desde el ZIP, ahora con el
  manifiesto SHA-256 de los ficheros heredados y `corre_baterias.py` en la raíz (hallazgo 4).
- **Observación para el revisor** (no es deuda): las excepciones por diseño de la batería son las que los
  módulos T-03 documentan — `volcar` lanza ValueError con un instante ilegible, una clave inválida o un
  estado que JSON no guarda tal cual (`guardar` lo convierte en PE-01 o PE-07), el constructor de `Reloj`
  lanza ValueError con tolerancias imposibles, las operaciones del diario con argumentos que el método no
  acepta se anotan como O-00 y el diario sigue sirviendo, una cabecera mutada que respeta la forma puede
  cargar (la huella cubre el estado, no la cabecera), `migrar` sobre un documento de este código responde
  «nada que migrar» con el mismo texto, y `degradar_por_reloj` con un incidente real degrada todas las
  carteras a L1 por diseño. Cada una está justificada en la cabecera de la batería y en el Documento 0
  (§2 punto 3 y §5), y la no-vacuidad quedó demostrada con sondas antes de entregar.
