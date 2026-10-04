# Blog da IBA (`blog.ibaestudio.com`)

Site estático, sem framework, sem JavaScript próprio e sem build: HTML, CSS e as capas dos jogos.
Foi montado no padrão dos jogos da casa (fundo branco, Archivo nos títulos, Inter no corpo, laranja
só em botão, sem emoji) e os artigos são escritos aqui dentro, em `gerar.py`.

**Nada foi publicado.** Não existe projeto no Vercel, não existe registro de DNS e nada foi
empurrado para o GitHub. Os passos que faltam estão no fim deste arquivo.

## Como mexer

```bash
# escreve (ou muda) o artigo dentro de gerar.py e regenera as páginas
python3 gerar.py

# confere tudo: arquivo que falta, link quebrado, metatag, travessão, emoji, sitemap e contraste
node verificar.mjs

# olha com o olho, em http://localhost:8095
python3 -m http.server 8095
```

O `gerar.py` é sensor também: ele **recusa** artigo com travessão, com emoji, com data fora do
padrão `AAAA-MM-DD`, com `<h1>` repetido no corpo ou com tique de texto gerado ("Além disso",
"Descubra como", "É importante ressaltar"). Texto que quebra a régua da casa não chega a virar
página.

## O que tem aqui

| Arquivo | O que é |
| --- | --- |
| `gerar.py` | Todo o conteúdo e o casco das páginas. É a fonte da verdade do blog. |
| `index.html` | Lista de artigos. Gerado. |
| `sitemap.xml` | Gerado junto com as páginas, uma URL por artigo. |
| `verificar.mjs` | Sensor: arquivos, links internos, metatags, travessão, emoji, sitemap e contraste. |
| `styles.css` | Folha única. Nenhum arquivo JS. |
| `vercel.json` | Cabeçalhos de cache e de segurança. Sem build, sem rewrite. |

### Artigos

1. `artigos/no-do-dia-oito-pecas.html`: O Nó do dia, as quatro regras e por que o jogo confere
   regra em vez de guardar gabarito.
2. `artigos/conta-do-dia-qualquer-conta.html`: A Conta do dia, o limite de caracteres e a regra
   que mora em um arquivo só.
3. `artigos/retangulo-do-dia-grade-sem-sobra.html`: O Retângulo do dia, o jogo mais novo, e o
   problema de gerar tabuleiro que tenha solução.
4. `artigos/como-nascem-os-jogos-diarios.html`: o processo da linha inteira, do fuso ao carimbo de
   versão no CSS.

Nenhum número dos artigos foi estimado: os que aparecem (74 arranjos válidos no tabuleiro do
primeiro dia, 400 dias com solução única, 12.852 contas conferidas, 34 pares de contraste, teto de
120 KB de JavaScript) saíram de execução, e a maior parte deles saiu de arquivo que está no
repositório dos jogos, não da memória de quem escreveu.

**Dependência:** o terceiro artigo fala do Retângulo do dia e linka a página do jogo. Blog e jogo
sobem na mesma rodada. Se o jogo não subir, esse artigo sai do `ARTIGOS` no `gerar.py` antes de
publicar o blog.

## Passos que faltam para publicar (dependem da palavra da Isis)

1. **Subir o repositório dos jogos** (`/opt/data/staging-gametools`): o commit local com o jogo
   novo está pronto e não foi empurrado. Sem o push, não existe deploy e o link do terceiro artigo
   dá 404.
2. **Criar o repositório e o projeto do blog.** Caminho mais curto, que não exige credencial nova
   no servidor: criar o projeto no Vercel apontando para a pasta `/opt/data/blog-iba` (framework
   "Other", sem build, sem comando de build, sem variável de ambiente), pelo PC, e depois criar o
   repositório no GitHub a partir dessa pasta.
3. **Dizer ao Vercel que este projeto atende `blog.ibaestudio.com`**: Vercel, projeto do blog,
   Settings, Domains, Add, `blog.ibaestudio.com`. O Vercel informa na tela o registro que ele espera.
4. **Registro de DNS no Cloudflare** (só com a palavra dela):

   | Campo | Valor |
   | --- | --- |
   | Tipo | `CNAME` |
   | Nome | `blog` |
   | Destino | `cname.vercel-dns.com` |
   | Proxy | ligado (nuvem laranja), igual aos outros subdomínios da casa |
   | TTL | automático |

   O destino é o valor que o Vercel mostrar no passo 3. Hoje o Vercel recomenda
   `cname.vercel-dns.com` para subdomínio, mas quem manda é a tela dele.

   **Cuidado medido:** `ibaestudio.com` tem um registro curinga (`*`) que já responde para qualquer
   subdomínio, inclusive para um nome inventado. Um `blog.ibaestudio.com` criado por engano só no
   curinga responde, mas pode servir o conteúdo errado, e o erro fica escondido. Por isso o registro
   do `blog` precisa ser explícito, e não herdar o curinga.

5. **Conferir depois do DNS**: `curl -sI https://blog.ibaestudio.com/` tem de responder `200` com
   `server: cloudflare` e o HTML do blog, e não a página de outro projeto.

Não mexi no DNS do e-mail: nenhum registro de MX, SPF ou DKIM é tocado por este passo, que mexe
apenas no nome `blog`.

## O que já foi conferido

- `node verificar.mjs`: 0 problemas (arquivos, links internos, metatags, travessão, emoji, sitemap).
- Contraste medido por script, nos pares de texto e de forma: todos acima do piso da casa (4,5:1
  para texto, 3:1 para forma).
- Páginas abertas no navegador em 390 px de largura e em 1280 px, sem erro de console, sem rolagem
  horizontal e sem imagem quebrada.
- Nenhum arquivo de JavaScript no blog: o site é HTML e CSS.
