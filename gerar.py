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
VERSAO_CSS = "20261004b"
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
        "slug": "no-do-dia-oito-pecas",
        "titulo": "O Nó do dia: oito peças, quatro regras e mais de uma resposta certa",
        "data": "2026-10-04",
        "resumo": (
            "Um tabuleiro de 8 por 8 casas, oito peças para colocar e quatro regras que não mudam. "
            "O jogo confere as regras, não um gabarito, então existe mais de um jeito de acertar."
        ),
        "imagem": "capa-no-do-dia-800.png",
        "imagem_og": "capa-no-do-dia.png",
        "jogo": "https://jogos.ibaestudio.com/jogos/no-do-dia.html",
        "jogo_nome": "O Nó do dia",
        "corpo": """
<p>O Nó do dia é um tabuleiro de 8 por 8 casas dividido em regiões numeradas. A tarefa é
colocar oito peças, e as regras são sempre as mesmas quatro:</p>

<ul>
  <li>uma peça em cada linha;</li>
  <li>uma peça em cada coluna;</li>
  <li>uma peça em cada região numerada;</li>
  <li>nenhuma peça encosta em outra, nem na diagonal.</li>
</ul>

<p>O que muda de um dia para o outro é o desenho das regiões. Um tabuleiro novo por dia, igual
para todo mundo, publicado na virada do dia pelo relógio de Brasília.</p>

<h2>O jogo não guarda a resposta</h2>

<p>Quando alguém fecha o tabuleiro, o jogo confere as quatro regras, e não compara o arranjo
com um gabarito guardado. Se o arranjo passa nas quatro, vence, mesmo que seja diferente
daquele que o gerador tinha em mente ao desenhar o tabuleiro.</p>

<p>Isso não é detalhe de implementação. Contando com um solver, o tabuleiro do primeiro dia, de
28 de setembro de 2026, tem 74 arranjos válidos diferentes. Guardar um só deles como resposta
certa e recusar os outros 73 seria mentir para quem acertou. Quem chega em um deles chegou.</p>

<h2>No celular e no teclado</h2>

<p>No celular, um toque põe a peça e outro toque tira, sem arrastar nada. No computador as setas
andam entre as casas e a barra de espaço põe e tira a peça, para quem prefere resolver sem
tirar a mão do teclado.</p>

<h2>O que o jogo não faz</h2>

<p>Não tem cadastro, não tem ranking e não guarda nada no servidor. A contagem de dias seguidos
fica no armazenamento do próprio navegador, e some se a pessoa limpar os dados do site.</p>

<p>Pedir a resposta existe, para quem travou e não quer sair sem ver a solução. Só que ver a
resposta não é resolver: a sequência de dias seguidos volta ao começo.</p>
""",
    },
    {
        "slug": "conta-do-dia-qualquer-conta",
        "titulo": "A Conta do dia: vale qualquer conta que chegue no alvo",
        "data": "2026-10-04",
        "resumo": (
            "Um número alvo, um limite de caracteres e seis tentativas. O jogo aceita qualquer conta "
            "que chegue no alvo dentro do limite, e o limite do dia tem uma razão de ser."
        ),
        "imagem": "capa-conta-do-dia-800.png",
        "imagem_og": "capa-conta-do-dia.png",
        "jogo": "https://jogos.ibaestudio.com/jogos/conta-do-dia.html",
        "jogo_nome": "A Conta do dia",
        "corpo": """
<p>A Conta do dia dá um número alvo e um limite de caracteres. A pessoa escreve uma conta que
chegue nesse número, dentro do limite, em até seis tentativas. As regras:</p>

<ul>
  <li>use os números de 0 a 9 e as operações + − × ÷;</li>
  <li>a conta precisa caber no limite de caracteres do dia;</li>
  <li>não há parênteses: a conta é lida da esquerda para a direita;</li>
  <li>a divisão só vale quando dá número inteiro;</li>
  <li>são seis tentativas, e qualquer conta que chegue no alvo vence.</li>
</ul>

<h2>O limite do dia não é um número escolhido a esmo</h2>

<p>O limite de caracteres de cada dia é o tamanho da <strong>menor</strong> conta que chega naquele
alvo. Isso faz "no máximo N caracteres" e "exatamente N caracteres" valerem a mesma coisa em
termos de resposta: se existe uma conta menor, o limite do dia é ela.</p>

<p>A primeira conta, de 1º de outubro de 2026, pedia 747 em quatro caracteres. Cabem ali
<code>83×9</code> e <code>9×83</code>, que são contas diferentes na tela e chegam no mesmo
número. No arquivo que cobre os 400 dias do ano, nenhum dia tem uma resposta só: o menor dia
aponta duas, e o maior aponta dez.</p>

<h2>A mesma regra nos dois lados</h2>

<p>Quem gera o conteúdo de um ano é um script em Python. Quem confere o que a pessoa digita é o
navegador, em JavaScript. Se as duas versões da regra divergirem em algum detalhe, o dia fica
injusto: alguém acerta e o jogo recusa.</p>

<p>Por isso a regra mora em um arquivo só, usado pelos dois lados, e existe uma conferência por
execução que compara os dois resultados. A última rodada comparou 12.852 contas.</p>

<h2>O que o jogo não faz</h2>

<p>Não guarda a conta enviada no servidor, não tem cadastro e não tem ranking. As tentativas
ficam na tela do dia: quem escreve uma conta válida vence e o dia acabou.</p>
""",
    },
    {
        "slug": "retangulo-do-dia-grade-sem-sobra",
        "titulo": "O Retângulo do dia: dividir a grade sem deixar casa de fora",
        "data": "2026-10-04",
        "resumo": (
            "O jogo mais novo do catálogo. A mecânica é fácil de explicar e trabalhosa de gerar: "
            "tabuleiro sorteado sem solução é pior que tabuleiro nenhum."
        ),
        "imagem": "capa-retangulo-do-dia-800.png",
        "imagem_og": "capa-retangulo-do-dia.png",
        "jogo": "https://jogos.ibaestudio.com/jogos/retangulo-do-dia.html",
        "jogo_nome": "O Retângulo do dia",
        "corpo": """
<p>O Retângulo do dia é uma grade de 6 por 6 casas com números espalhados. A tarefa é dividir a
grade inteira em retângulos, e o retângulo tem duas obrigações ao mesmo tempo:</p>

<ul>
  <li>fechar sobre exatamente um número;</li>
  <li>ter área igual a esse número.</li>
</ul>

<p>Um retângulo de 2 por 3 tem seis casas, então só vale se o número dentro dele for 6. Nenhuma
casa fica de fora, e nenhum retângulo cobre o número de outro.</p>

<h2>O problema de verdade está em gerar</h2>

<p>Dividir a grade é a parte fácil. Montar um tabuleiro que tenha solução é o trabalho. Se a
grade for preenchida com números escolhidos ao acaso, é questão de tempo até sair um tabuleiro
sem resposta nenhuma, e um quebra-cabeça insolúvel é pior do que não publicar nada naquele dia.</p>

<p>O gerador resolve cada tabuleiro antes de aceitar. A preferência é solução única, e foi o que
saiu nos 400 dias do arquivo: uma resposta por dia, sem margem para uma segunda divisão válida.
Tabuleiro sem solução nenhuma não entra, em dia nenhum.</p>

<p>E a conferência não confia em quem gerou. O gerador escreve em Python, e existe um segundo
solver, escrito de novo em Node, que relê o arquivo do ano inteiro e resolve cada dia por conta
própria. Os dois têm de concordar. Quando não concordam, o problema é do gerador, e o dia não
entra no ar.</p>

<h2>Como se joga no celular</h2>

<p>Arrasta-se de uma casa até o canto oposto do retângulo, com o dedo ou com o mouse. Um toque
em cima de um retângulo já desenhado tira ele, para quem errou a medida. Numa casa sozinha com o
número 1, um toque já fecha o retângulo de uma casa só.</p>

<p>Quando o retângulo não vale, o aviso diz o motivo, e não um erro genérico: se não tem número
dentro, se tem dois, ou se a área não bate com o número. Quem está jogando sabe o que ajustar.</p>

<p>Como nos outros jogos, a conferência é por regra. Qualquer divisão da grade que respeite as
duas obrigações vence.</p>

<h2>O que o jogo não faz</h2>

<p>Não tem cadastro, não guarda o tabuleiro resolvido no servidor e não tem ranking. O cronômetro
é para quem gosta de comparar o próprio tempo com o de ontem, e não vale como placar de ninguém.</p>
""",
    },
    {
        "slug": "como-nascem-os-jogos-diarios",
        "titulo": "Como nascem os jogos diários da IBA",
        "data": "2026-10-04",
        "resumo": (
            "O site é estático, sem cadastro e sem servidor. O dia é lido no fuso de Brasília, e um "
            "ano inteiro de conteúdo é gerado e conferido antes de entrar no ar."
        ),
        "imagem": None,
        "imagem_og": None,
        "jogo": JOGOS,
        "jogo_nome": "os jogos da IBA",
        "corpo": """
<p>Os jogos diários da IBA são três, e todos partem do mesmo desenho. Uma sessão de um a cinco
minutos, um desafio por dia, igual para todo mundo, que troca na virada do dia.</p>

<h2>Site estático, sem cadastro e sem servidor</h2>

<p>Tudo o que a pessoa vê vem de arquivos: HTML, CSS e JavaScript. Não existe conta para criar,
não existe banco de dados guardando o que cada um jogou, e não existe servidor para cair no meio
da partida. Também não existe aplicativo para instalar: abre no navegador do celular e joga.</p>

<p>O lado bom disso é a previsibilidade. O lado ruim é que quase todo o trabalho acontece antes,
na hora de gerar o conteúdo e conferir.</p>

<h2>O dia é o dia do Brasil</h2>

<p>O jogo lê o relógio no fuso de Brasília, e não no relógio do aparelho. Celular com fuso
trocado, ou alguém viajando, veria o desafio de amanhã fora de hora se o jogo confiasse na hora
do aparelho. Como o dia vem do mesmo lugar para todo mundo, o tabuleiro de hoje é o mesmo em
Porto Alegre e em qualquer outra cidade.</p>

<h2>Um ano inteiro gerado antes</h2>

<p>O conteúdo de cada jogo é gerado por ano, de uma vez. Antes de entrar no ar, o arquivo passa
por conferência por execução: no caso do Nó do dia e do Retângulo do dia, um solver resolve os
tabuleiros de novo e compara com o que o gerador tinha calculado. Quando os dois discordam, o
arquivo não vai para o ar.</p>

<p>Gerar com antecedência também evita o pior defeito possível num jogo diário: o dia em que o
gerador falha às 23h59 e não existe desafio para publicar.</p>

<h2>Conferir a regra, e não o gabarito</h2>

<p>Nenhum dos três jogos compara o que a pessoa fez com uma resposta guardada. Eles conferem a
regra. Isso importa porque existe mais de uma resposta certa em todos os casos: o tabuleiro do
primeiro dia do Nó do dia tem 74 arranjos válidos, e a primeira conta do dia aceita 83×9 e 9×83
para chegar em 747.</p>

<p>Validar regra dá mais trabalho na hora de escrever o código, porque obriga a descrever a
solução como uma condição em vez de guardar um resultado. Em troca, o jogo nunca recusa um
acerto.</p>

<h2>O que a pessoa não vê, mas sente</h2>

<p>Alguns cuidados não aparecem na tela e mudam a experiência:</p>

<ul>
  <li><strong>Carimbo de versão no endereço dos arquivos.</strong> O CSS e o JavaScript ficam em
  cache no CDN, e o HTML não. Por isso cada mudança no CSS ou no JavaScript vem com um carimbo no
  endereço do arquivo. Sem o carimbo, quem já tinha aberto o site continua com o arquivo velho, e
  a página quebra de um jeito difícil de enxergar.</li>
  <li><strong>Movimento reduzido.</strong> Quem pede menos animação no sistema operacional recebe
  a tela sem animação nenhuma. Não é preferência estética: é a configuração de acessibilidade da
  pessoa sendo respeitada.</li>
  <li><strong>Contraste medido, não estimado.</strong> O contraste de texto e de interface é
  conferido por um script que lê as cores do arquivo de estilo e calcula a razão: no mínimo 4,5:1
  para texto e 3:1 para forma. Hoje são 34 pares medidos, nos dois temas.</li>
  <li><strong>Teto de JavaScript.</strong> O site inteiro respeita um teto de 120 KB de JavaScript.
  Hoje ele soma 87 KB, sem nenhuma biblioteca de terceiro. Foi o que dispensou uma biblioteca de
  arrastar e obrigou a escrever a interação com os eventos nativos do navegador.</li>
  <li><strong>Capa e identidade.</strong> A arte de cada jogo é gerada por script a partir da capa
  aprovada, com o recorte do mascote idêntico, pixel a pixel. Jogo novo não inventa um rosto novo
  para a marca: fundo branco, Archivo nos títulos, Inter no corpo, laranja apenas em botão, e
  nenhum emoji em nada que o visitante vê.</li>
</ul>

<h2>O que os jogos não fazem</h2>

<p>Não existe ranking, liga ou premiação. Não existe histórico do lado do servidor: a sequência de
dias seguidos fica no navegador de quem joga e desaparece se os dados do site forem limpos. E não
existe cobrança: os três jogos são abertos, sem cadastro e sem anúncio.</p>
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
    print(f"artigos: {len(ARTIGOS)} | um índice, 4 páginas de artigo e o sitemap")


if __name__ == "__main__":
    main()
