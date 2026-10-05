#!/usr/bin/env python3
"""Gera o blog da IBA (blog.ibaestudio.com) a partir dos artigos escritos aqui dentro.

O casco das páginas (cabeçalho, rodapé, canônico, cartões do índice) sai de um lugar só,
então artigo novo não inventa estrutura nova nem esquece metatag. O gerador também é
sensor: ele RECUSA publicar texto com travessão, com emoji ou com data fora do padrão.

Rodar:  python3 gerar.py
Conferir depois:  node verificar.mjs
"""
from __future__ import annotations

import html
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
DOMINIO = "https://blog.ibaestudio.com"
VERSAO_CSS = "20261004c"
JOGOS = "https://jogos.ibaestudio.com/"
ESTUDIO = "https://www.ibaestudio.com/"
CONTATO = "contato@ibaestudio.com"
WHATSAPP = "https://wa.me/5551993307386"

MESES = {
    1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril", 5: "maio", 6: "junho",
    7: "julho", 8: "agosto", 9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro",
}


def por_extenso(iso: str) -> str:
    ano, mes, dia = (int(parte) for parte in iso.split("-"))
    return f"{dia} de {MESES[mes]} de {ano}"


ARTIGOS = [
    {
        "slug": "jogos-iba-tres-jogos-diarios",
        "titulo": "Jogos IBA: três jogos diários, abertos e sem cadastro",
        "data": "2026-10-04",
        "resumo": (
            "O Nó do dia, a Conta do dia e o Retângulo do dia: um desafio novo por dia, igual para "
            "todo mundo, que abre no navegador. Como cada um funciona e o que existe por trás."
        ),
        "imagem": None,
        "imagem_og": "capa-retangulo-do-dia.png",
        "jogo": JOGOS,
        "jogo_nome": "os jogos da IBA",
        "corpo": """
<p>O Jogos IBA é o site de jogos do estúdio, em <a href="https://jogos.ibaestudio.com/">jogos.ibaestudio.com</a>.
São três jogos curtos, de um a cinco minutos cada, com um desafio novo por dia, igual para todo
mundo, que troca na virada do dia pelo relógio de Brasília. Não tem cadastro, não tem aplicativo
para instalar e não tem anúncio: abre no navegador do celular e joga.</p>

<h2>O Nó do dia</h2>

<figure>
  <img src="/assets/img/capa-no-do-dia-800.png" alt="Capa do jogo O Nó do dia" width="800" height="450" loading="lazy" />
</figure>

<p>Um tabuleiro de 8 por 8 casas dividido em regiões numeradas. A tarefa é colocar oito peças:
uma em cada linha, uma em cada coluna, uma em cada região, e nenhuma encostando em outra, nem na
diagonal. As regras são sempre essas quatro; o que muda de um dia para o outro é o desenho das
regiões.</p>

<p>No celular, um toque põe a peça e outro tira. No computador, as setas andam entre as casas e a
barra de espaço põe e tira a peça.</p>

<h2>A Conta do dia</h2>

<figure>
  <img src="/assets/img/capa-conta-do-dia-800.png" alt="Capa do jogo A Conta do dia" width="800" height="450" loading="lazy" />
</figure>

<p>Um número alvo, um limite de caracteres e seis tentativas para escrever uma conta que chegue
no alvo. Valem os números de 0 a 9 e as operações + − × ÷, sem parênteses: a conta é lida da
esquerda para a direita, e a divisão só vale quando dá número inteiro.</p>

<p>O limite do dia não é escolhido a esmo. Ele é o tamanho da menor conta que chega naquele alvo,
então "no máximo N caracteres" e "exatamente N caracteres" dão no mesmo. A primeira conta, de 1º
de outubro de 2026, pedia 747 em quatro caracteres, e cabem ali <code>83×9</code> e
<code>9×83</code>.</p>

<h2>O Retângulo do dia</h2>

<figure>
  <img src="/assets/img/capa-retangulo-do-dia-800.png" alt="Capa do jogo O Retângulo do dia" width="800" height="450" loading="lazy" />
</figure>

<p>O mais novo do catálogo. Uma grade de 6 por 6 casas com números espalhados, que precisa ser
dividida inteira em retângulos. Cada retângulo fecha sobre exatamente um número e tem área igual
a ele: um retângulo de 2 por 3 só vale se o número dentro for 6. Arrasta-se de uma casa até o
canto oposto, com o dedo ou com o mouse, e um toque em cima de um retângulo já desenhado tira ele.
Quando o retângulo não vale, o aviso diz o motivo: sem número dentro, com dois números, ou com a
área errada.</p>

<h2>O jogo confere a regra, não um gabarito</h2>

<p>Nenhum dos três compara o que a pessoa fez com uma resposta guardada. Eles conferem a regra, e
qualquer resposta que respeite as regras vence. Isso importa porque quase sempre existe mais de
uma resposta certa. Contando com um solver, o tabuleiro do primeiro dia do Nó do dia, de 28 de
setembro de 2026, tem 74 arranjos válidos. Guardar um só como resposta e recusar os outros 73 seria
dizer a quem acertou que errou.</p>

<p>Na Conta do dia, a regra roda em dois lugares: o script em Python que gera o ano e o navegador,
em JavaScript, que confere o que a pessoa digita. Se as duas versões divergissem em algum detalhe,
alguém acertaria e o jogo recusaria. Por isso a regra mora em um arquivo só, usado pelos dois
lados, e uma conferência por execução compara os resultados. A última rodada comparou 12.852
contas.</p>

<h2>Um ano inteiro gerado e conferido antes</h2>

<p>O conteúdo de cada jogo é gerado por ano, de uma vez, e conferido antes de entrar no ar. Isso
evita o pior defeito de um jogo diário: o dia em que o gerador falha às 23h59 e não há desafio
para publicar.</p>

<p>No Retângulo do dia, gerar é a parte difícil. Grade preenchida ao acaso cedo ou tarde sai sem
solução, e quebra-cabeça insolúvel é pior que dia nenhum. O gerador resolve cada tabuleiro antes
de aceitar, e nos 400 dias do arquivo saiu solução única em todos. Depois, um segundo solver,
escrito de novo em Node, relê o ano inteiro e resolve cada dia por conta própria. Se os dois
discordam, o dia não vai para o ar.</p>

<p>O dia também vem de um lugar só: o jogo lê o relógio no fuso de Brasília, e não o do aparelho.
Celular com fuso trocado veria o desafio de amanhã fora de hora; assim, o tabuleiro de hoje é o
mesmo em Porto Alegre e em qualquer outra cidade.</p>

<h2>O que a pessoa não vê, mas sente</h2>

<ul>
  <li><strong>Site estático.</strong> Tudo vem de arquivos: HTML, CSS e JavaScript. Não há banco de
  dados guardando o que cada um jogou, nem servidor para cair no meio da partida.</li>
  <li><strong>Leve.</strong> O site respeita um teto de 120 KB de JavaScript e hoje soma 87 KB, sem
  biblioteca de terceiro. O arrastar do Retângulo foi escrito com os eventos nativos do navegador
  por causa disso.</li>
  <li><strong>Contraste medido.</strong> Um script lê as cores do arquivo de estilo e calcula a
  razão de contraste: no mínimo 4,5:1 para texto e 3:1 para forma. São 34 pares medidos, nos dois
  temas.</li>
  <li><strong>Movimento reduzido.</strong> Quem pede menos animação no sistema recebe a tela sem
  animação nenhuma.</li>
  <li><strong>Carimbo de versão.</strong> Cada mudança no CSS ou no JavaScript muda o endereço do
  arquivo, para ninguém ficar preso a uma versão velha guardada em cache.</li>
</ul>

<h2>O que os jogos não fazem</h2>

<p>Não existe ranking, liga ou premiação, e nada do que a pessoa joga vai para um servidor. A
sequência de dias seguidos fica no navegador de quem joga e some se os dados do site forem
limpos. No Nó do dia, pedir a resposta existe, para quem travou, mas ver a resposta não é
resolver: a sequência volta ao começo.</p>
""",
    },
]


# --------------------------------------------------------------------------
# Checagens (o gerador é sensor: texto que quebra a regra da casa não é publicado)
# --------------------------------------------------------------------------
TRAVESSAO = "\u2014"


def conferir_artigo(artigo: dict) -> None:
    texto = artigo["titulo"] + " " + artigo["resumo"] + " " + artigo["corpo"]
    if TRAVESSAO in texto:
        raise SystemExit(f"[{artigo['slug']}] travessão no texto (a casa não usa)")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", artigo["data"]):
        raise SystemExit(f"[{artigo['slug']}] data fora do padrão AAAA-MM-DD")
    emoji = re.findall(
        "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2190-\u21FF\u2B00-\u2BFF\uFE0F]",
        texto,
    )
    if emoji:
        raise SystemExit(f"[{artigo['slug']}] emoji no texto: {emoji}")
    for tique in ("É importante ressaltar", "Vale destacar", "Nesse sentido", "Em suma",
                  "Além disso", "Por fim,", "Descubra como"):
        if tique.lower() in texto.lower():
            raise SystemExit(f"[{artigo['slug']}] tique de texto gerado: {tique}")
    if "<h1" in artigo["corpo"]:
        raise SystemExit(f"[{artigo['slug']}] o título já vem do casco: não repetir <h1> no corpo")


# --------------------------------------------------------------------------
# Casco das páginas
# --------------------------------------------------------------------------
def cabecalho(titulo: str, descricao: str, caminho: str, imagem: str | None,
              tipo: str = "article") -> str:
    og_imagem = (
        f'\n  <meta property="og:image" content="{DOMINIO}/assets/img/{imagem}" />'
        if imagem else ""
    )
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(titulo)}</title>
  <meta name="description" content="{html.escape(descricao)}" />
  <link rel="canonical" href="{DOMINIO}/{caminho}" />

  <meta name="theme-color" content="#185cb6" />
  <meta property="og:type" content="{tipo}" />
  <meta property="og:site_name" content="Blog da IBA" />
  <meta property="og:locale" content="pt_BR" />
  <meta property="og:title" content="{html.escape(titulo)}" />
  <meta property="og:description" content="{html.escape(descricao)}" />
  <meta property="og:url" content="{DOMINIO}/{caminho}" />{og_imagem}
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(titulo)}" />
  <meta name="twitter:description" content="{html.escape(descricao)}" />

  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png" />
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/img/favicon-192.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/img/apple-touch-icon.png" />

  <link rel="preload" href="/assets/fonts/archivo-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="stylesheet" href="/styles.css?v={VERSAO_CSS}" />
</head>
<body>
  <a class="skip-link" href="#conteudo">Ir para o conteúdo</a>

  <header class="header">
    <div class="container nav">
      <a class="marca" href="/">
        <img src="/assets/img/logo-iba.png" alt="IBA Estúdios" width="216" height="72" />
        <span>Blog</span>
      </a>
      <nav aria-label="Navegação principal">
        <a href="/"{' aria-current="page"' if caminho == '' else ''}>Artigos</a>
        <a href="{JOGOS}">Jogos</a>
        <a href="{ESTUDIO}">Estúdio</a>
      </nav>
    </div>
  </header>
"""


RODAPE = f"""  <footer class="footer">
    <div class="container footer-conteudo">
      <p>
        Blog da IBA Estúdios, em Porto Alegre.
        Contato: <a href="mailto:{CONTATO}">{CONTATO}</a>
        · <a href="{WHATSAPP}">WhatsApp</a>
      </p>
      <p>Os jogos diários ficam em <a href="{JOGOS}">jogos.ibaestudio.com</a>.</p>
    </div>
  </footer>
</body>
</html>
"""


def pagina_artigo(artigo: dict) -> str:
    caminho = f"artigos/{artigo['slug']}.html"
    cartao_chamada = f"""
      <div class="jogar">
        <p>O jogo fica no catálogo, aberto e sem cadastro.</p>
        <a class="btn btn-acao" href="{artigo['jogo']}">Jogar {artigo['jogo_nome']}</a>
      </div>
"""
    return (
        cabecalho(artigo["titulo"], artigo["resumo"], caminho, artigo["imagem_og"])
        + f"""
  <main id="conteudo" class="container artigo">
    <div class="artigo-cabeca">
      <p class="artigo-data"><time datetime="{artigo['data']}">{por_extenso(artigo['data'])}</time></p>
      <h1>{html.escape(artigo['titulo'])}</h1>
    </div>

    <div class="prosa">
{artigo['corpo'].strip()}
      <hr />
      <p><a href="/">Voltar para a lista de artigos</a></p>
    </div>
{cartao_chamada}  </main>

"""
        + RODAPE
    )


def cartao(artigo: dict) -> str:
    if artigo["imagem"]:
        capa = (
            f'\n        <img src="/assets/img/{artigo["imagem"]}" '
            f'alt="Capa do jogo {html.escape(artigo["jogo_nome"])}" width="800" height="450" loading="lazy" />'
        )
    else:
        # Artigo sem capa de jogo: mesmo bloco de imagem dos outros cartões, com a marca no lugar
        # da arte, para o ritmo interno da grade não quebrar.
        capa = (
            '\n        <span class="cartao-capa-marca">'
            '<img src="/assets/img/logo-iba.png" alt="IBA Estúdios" width="216" height="72" loading="lazy" />'
            "</span>"
        )
    return f"""      <li>
        <a class="cartao" href="/artigos/{artigo['slug']}.html">{capa}
          <span class="cartao-corpo">
            <span class="cartao-data"><time datetime="{artigo['data']}">{por_extenso(artigo['data'])}</time></span>
            <strong>{html.escape(artigo['titulo'])}</strong>
            <span>{html.escape(artigo['resumo'])}</span>
            <span class="cartao-ler">Ler o artigo</span>
          </span>
        </a>
      </li>"""


def pagina_indice() -> str:
    descricao = (
        "Artigos sobre os jogos diários da IBA: como cada um funciona, por que a conferência é "
        "por regra e o que existe por trás de um tabuleiro novo por dia."
    )
    cartoes = "\n".join(cartao(a) for a in ARTIGOS)
    return (
        cabecalho("Blog da IBA: os jogos diários e como eles são feitos", descricao, "", None, "website")
        + f"""
  <main id="conteudo">
    <div class="container">
      <section class="abertura">
        <span class="selo">Jogos diários</span>
        <h1>Como os jogos diários da IBA funcionam</h1>
        <p>
          A IBA faz jogos curtos, de um a cinco minutos, com um desafio novo por dia e sem cadastro.
          Aqui a gente escreve sobre eles: a mecânica de cada um, as decisões que ficaram por trás e
          o que a construção desses jogos ensinou.
        </p>
      </section>

      <ul class="lista">
{cartoes}
      </ul>
    </div>
  </main>

"""
        + RODAPE
    )


def sitemap() -> str:
    urls = [("", "weekly", "1.0")] + [
        (f"artigos/{a['slug']}.html", "monthly", "0.8") for a in ARTIGOS
    ]
    linhas = "\n".join(
        f"""  <url>
    <loc>{DOMINIO}/{caminho}</loc>
    <lastmod>{ARTIGOS[0]['data']}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{prio}</priority>
  </url>""" for caminho, freq, prio in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{linhas}
</urlset>
"""


def main() -> None:
    for artigo in ARTIGOS:
        conferir_artigo(artigo)

    slugs = [a["slug"] for a in ARTIGOS]
    if len(slugs) != len(set(slugs)):
        raise SystemExit("slug repetido na lista de artigos")

    (RAIZ / "artigos").mkdir(exist_ok=True)
    escritos = []

    indice = RAIZ / "index.html"
    indice.write_text(pagina_indice(), encoding="utf-8")
    escritos.append(indice)

    for artigo in ARTIGOS:
        destino = RAIZ / "artigos" / f"{artigo['slug']}.html"
        destino.write_text(pagina_artigo(artigo), encoding="utf-8")
        escritos.append(destino)

    mapa = RAIZ / "sitemap.xml"
    mapa.write_text(sitemap(), encoding="utf-8")
    escritos.append(mapa)

    for arquivo in escritos:
        print(f"escrito: {arquivo.relative_to(RAIZ)} ({arquivo.stat().st_size} bytes)")
    print(f"artigos: {len(ARTIGOS)} | um índice, {len(ARTIGOS)} página(s) de artigo e o sitemap")


if __name__ == "__main__":
    main()
