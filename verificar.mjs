/*
 * Sensor do blog da IBA, sem dependencia nenhuma.
 *
 * Confere o que o olho nao confere sozinho: arquivo que falta, link interno que aponta para
 * lugar nenhum, artigo que nao aparece no indice, metatag faltando, travessao no texto,
 * emoji, sitemap desalinhado e contraste abaixo do piso da casa.
 *
 * Rodar:  node verificar.mjs      (sai 1 se algo reprovar)
 */
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const RAIZ = dirname(fileURLToPath(import.meta.url));
const PAGINAS = [
  "index.html",
  "artigos/jogos-iba-tres-jogos-diarios.html",
];
const OBRIGATORIOS = [...PAGINAS, "styles.css", "sitemap.xml", "robots.txt", "favicon.ico",
  "assets/img/logo-iba.png", "assets/img/favicon-32.png",
  "assets/fonts/archivo-latin-wght-normal.woff2", "assets/fonts/inter-latin-wght-normal.woff2"];

let falhas = 0;
let metatagsConferidas = 0;
let linksConferidos = 0;
const linhas = [];
const ok = (nome, detalhe = "") => linhas.push(`  ok      ${nome}${detalhe ? " | " + detalhe : ""}`);
const erro = (nome, detalhe) => { falhas += 1; linhas.push(`  REPROVA ${nome} | ${detalhe}`); };

// ------------------------------------------------------------------ 1. arquivos
for (const rel of OBRIGATORIOS) {
  if (existsSync(join(RAIZ, rel))) ok(`arquivo ${rel}`);
  else erro(`arquivo ${rel}`, "nao existe");
}

// ------------------------------------------------------------------ 2. html
const RE_EMOJI = /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}]/u;
const htmls = new Map();

for (const rel of PAGINAS) {
  const caminho = join(RAIZ, rel);
  if (!existsSync(caminho)) continue;
  const html = readFileSync(caminho, "utf8");
  htmls.set(rel, html);
  const exigidos = [
    ['lang="pt-BR"', "idioma"],
    ['<meta charset="utf-8"', "charset"],
    ['name="viewport"', "viewport"],
    ["<title>", "title"],
    ['name="description"', "description"],
    ['rel="canonical"', "canonical"],
    ['property="og:title"', "og:title"],
    ['property="og:description"', "og:description"],
    ['property="og:url"', "og:url"],
    ['name="twitter:card"', "twitter:card"],
  ];
  for (const [marca, nome] of exigidos) {
    metatagsConferidas += 1;
    if (!html.includes(marca)) erro(`${rel}: ${nome}`, "metatag ausente");
  }
  const h1 = html.match(/<h1[\s>]/g) || [];
  if (h1.length !== 1) erro(`${rel}: h1`, `esperado 1, encontrado ${h1.length}`);
  if (html.includes("\u2014")) erro(`${rel}: travessao`, "a casa nao usa travessao");
  if (RE_EMOJI.test(html)) erro(`${rel}: emoji`, "a casa nao usa emoji");
  if (html.includes("<script")) erro(`${rel}: javascript`, "o blog e um site estatico sem JS proprio");
  if (!/<main[\s>]/.test(html)) erro(`${rel}: main`, "sem <main>");
}

// ------------------------------------------------------------------ 3. links e assets internos
for (const [rel, html] of htmls) {
  const refs = [...html.matchAll(/(?:href|src)="([^"]+)"/g)].map((m) => m[1]);
  for (const ref of refs) {
    if (!ref.startsWith("/")) continue;
    linksConferidos += 1;
    const alvo = ref.split("?")[0].split("#")[0];
    const caminho = alvo.endsWith("/") ? join(RAIZ, alvo, "index.html") : join(RAIZ, alvo);
    if (!existsSync(caminho)) erro(`${rel}: link ${ref}`, "nao existe no site gerado");
  }
}

// ------------------------------------------------------------------ 4. indice lista todos os artigos
const indice = htmls.get("index.html") || "";
for (const rel of PAGINAS.filter((p) => p.startsWith("artigos/"))) {
  const alvo = "/" + rel;
  if (!indice.includes(alvo)) erro("indice", `artigo fora da lista: ${alvo}`);
}

// ------------------------------------------------------------------ 5. sitemap
const sitemap = readFileSync(join(RAIZ, "sitemap.xml"), "utf8");
const noMapa = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
const esperado = PAGINAS.map((p) => (p === "index.html" ? "https://blog.ibaestudio.com/" : `https://blog.ibaestudio.com/${p}`));
for (const url of esperado) if (!noMapa.includes(url)) erro("sitemap", `falta ${url}`);
for (const url of noMapa) if (!esperado.includes(url)) erro("sitemap", `sobra ${url}`);

// ------------------------------------------------------------------ 6. css: acessibilidade
const css = readFileSync(join(RAIZ, "styles.css"), "utf8");
if (!css.includes("prefers-reduced-motion: reduce")) erro("styles.css", "sem bloco de movimento reduzido");
if (!css.includes("Archivo")) erro("styles.css", "sem fonte Archivo nos titulos");
if (!css.includes("Inter")) erro("styles.css", "sem fonte Inter no corpo");
if (/var\(--color-accent\)/.test(css) && /\.btn-acao/.test(css)) ok("laranja restrito a botao");

// ------------------------------------------------------------------ 7. contraste (WCAG)
const tokens = {};
{
  const abre = css.indexOf(":root {");
  const inicio = css.indexOf("{", abre) + 1;
  let nivel = 1;
  let i = inicio;
  while (i < css.length && nivel > 0) {
    if (css[i] === "{") nivel += 1;
    else if (css[i] === "}") nivel -= 1;
    i += 1;
  }
  const corpo = css.slice(inicio, i - 1);
  for (const m of corpo.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;]+);/gi)) {
    tokens[m[1]] = m[2].trim();
  }
}

function luminancia(hex) {
  const n = hex.replace("#", "");
  const canais = [0, 2, 4].map((i) => parseInt(n.slice(i, i + 2), 16) / 255);
  const [r, g, b] = canais.map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function contraste(a, b) {
  const la = luminancia(a);
  const lb = luminancia(b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

function cor(valor) {
  let atual = String(valor).trim();
  for (let i = 0; i < 4; i += 1) {
    if (atual.startsWith("var(")) atual = tokens[atual.slice(4, atual.indexOf(")")).trim()];
    else if (atual.startsWith("--")) atual = tokens[atual];
    else break;
  }
  if (!/^#[0-9a-f]{6}$/i.test(atual)) throw new Error(`token sem cor: ${valor} -> ${atual}`);
  return atual.toLowerCase();
}

const PARES = [
  ["texto do corpo", "--color-ink", "--color-surface-page", 4.5],
  ["texto secundario", "--color-ink-muted", "--color-surface-page", 4.5],
  ["texto secundario em superficie", "--color-ink-muted", "--color-surface", 4.5],
  ["texto discreto", "--color-ink-soft", "--color-surface-page", 4.5],
  ["link", "--color-brand-dark", "--color-surface-page", 4.5],
  ["link em cima do rato", "--color-brand", "--color-surface-page", 4.5],
  ["selo do topo", "--color-brand-dark", "--color-brand-soft-alt", 4.5],
  ["botao com acao", "--color-ink", "--color-accent", 4.5],
  ["botao principal", "#ffffff", "--color-brand", 4.5],
  ["data do cartao", "--color-ink-muted", "--color-surface-page", 4.5],
  ["fonte de exemplo", "--color-ink", "--color-surface", 4.5],
  ["borda de campo (forma)", "--color-border-strong", "--color-surface-page", 3],
  ["filete separador (decorativo)", "--color-border", "--color-surface-page", 1.2],
];

const medidas = [];
for (const [nome, frente, fundo, minimo] of PARES) {
  const razao = contraste(cor(frente), cor(fundo));
  medidas.push({ nome, razao, minimo });
  if (razao < minimo) {
    erro(`contraste: ${nome}`, `${razao.toFixed(2)}:1, piso ${minimo}:1`);
  }
}

// ------------------------------------------------------------------ saida
console.log("Sensor do blog da IBA\n");
console.log(linhas.join("\n"));
console.log(`\ncontraste medido (${medidas.length} pares):`);
for (const m of medidas) {
  const marca = m.razao >= m.minimo ? "ok  " : "BAIXO";
  console.log(`  ${marca} ${m.razao.toFixed(2).padStart(6)}:1  (piso ${m.minimo})  ${m.nome}`);
}
console.log(`\nresumo: ${PAGINAS.length} páginas | ${metatagsConferidas} metatags | ${linksConferidos} links internos | ${medidas.length} pares de contraste | problemas: ${falhas}`);
process.exit(falhas === 0 ? 0 : 1);
