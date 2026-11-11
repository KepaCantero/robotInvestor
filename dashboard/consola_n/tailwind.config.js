import animate from "tailwindcss-animate";

const token = (n) => `rgb(var(--${n}) / <alpha-value>)`;

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: token("fondo"),
        foreground: token("texto"),
        card: { DEFAULT: token("panel"), foreground: token("texto") },
        popover: { DEFAULT: token("panel"), foreground: token("texto") },
        muted: { DEFAULT: token("panel-2"), foreground: token("tenue") },
        secondary: { DEFAULT: token("panel-2"), foreground: token("texto") },
        accent: { DEFAULT: token("panel-2"), foreground: token("texto") },
        primary: { DEFAULT: token("oro"), foreground: token("sobre-oro") },
        destructive: { DEFAULT: token("mal"), foreground: token("sobre-oro") },
        border: token("linea"),
        input: token("linea"),
        ring: token("oro"),
        oro: token("oro"),
        bien: token("bien"),
        aviso: token("aviso"),
        mal: token("mal"),
        tenue: token("tenue"),
      },
      fontFamily: {
        sans: ["'IBM Plex Sans'", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
        rotulo: ["'Silkscreen'", "'JetBrains Mono'", "ui-monospace", "monospace"],
      },
      borderRadius: { lg: "4px", md: "3px", sm: "2px" },
    },
  },
  plugins: [animate],
};
