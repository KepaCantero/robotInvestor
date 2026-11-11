// Parámetros del prototipo. Todos [PROPUESTO] (propuesta de N, §6 y §9): en la consola real
// saldrán de la configuración del robot, no de este fichero.

/** Segundos de espera antes de confirmar un aumento de riesgo. En el prototipo es corto para poder probarlo. */
export const ESPERA_AUMENTO_SEG = 8;

/** Minutos que vale una aprobación pendiente antes de caducar sin actuar. */
export const CADUCIDAD_APROBACION_MIN = 90;

/** Latencia simulada de la API, en milisegundos. */
export const LATENCIA_API_MS = 180;

/** Código de segundo factor de la demostración (en la consola real llega por un canal distinto del chat). */
export const CODIGO_DEMO = "482913";

/** Nivel del rango de la cifra principal (enmienda 5, D-54 [PROPUESTO]). */
export const NIVEL_RANGO = 0.9;
