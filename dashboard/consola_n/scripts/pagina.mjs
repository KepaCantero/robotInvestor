// Convierte dist-pagina/index.html (un solo fichero, de vite-plugin-singlefile) en el fragmento que
// se publica como página: sin <!doctype>, <html>, <head> ni <body>, que pone el publicador.
import { readFileSync, writeFileSync } from "node:fs";

const html = readFileSync("dist-pagina/index.html", "utf8");
const cabeza = html.match(/<head>([\s\S]*?)<\/head>/i)?.[1] ?? "";
const cuerpo = html.match(/<body>([\s\S]*?)<\/body>/i)?.[1] ?? "";
const sinMetasBase = cabeza.replace(/<meta charset[^>]*>\s*/i, "").replace(/<meta name="viewport"[^>]*>\s*/i, "");
const scripts = [...sinMetasBase.matchAll(/<script\b[\s\S]*?<\/script>/gi)].map((m) => m[0]);
const resto = sinMetasBase.replace(/<script\b[\s\S]*?<\/script>/gi, "");
const fragmento = `${resto.trim()}\n${cuerpo.replace(/<script\b[\s\S]*?<\/script>/gi, "").trim()}\n${scripts.join("\n")}\n`;
if (!/<title>/.test(fragmento.slice(0, 8192))) throw new Error("El <title> no está en los primeros 8 KB");
writeFileSync("dist-pagina/consola_n.html", fragmento);
console.log(`dist-pagina/consola_n.html · ${(fragmento.length / 1024).toFixed(0)} KB`);
