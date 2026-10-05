# Blog da IBA (`blog.ibaestudio.com`)

Site estático, sem framework, sem JavaScript próprio e sem build: HTML, CSS e as capas dos jogos.
Foi montado no padrão dos jogos da casa (fundo branco, Archivo nos títulos, Inter no corpo, laranja
só em botão, sem emoji) e os artigos são escritos aqui dentro, em `gerar.py`.

**No ar desde 04/10/2026** em `https://blog.ibaestudio.com` (projeto `blog-iba` na Vercel, ligado a
este repositório: push no `main` publica sozinho). O DNS é um `CNAME blog` na Cloudflare. O link
"Blog" do site principal (`ibaestudio-site`) aponta para cá, e o `/blog` de lá redireciona.

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

Regra da Isis (04/10/2026): **um artigo por tema**. Os quatro textos da estreia (um por jogo e um
sobre o processo) viraram um só, porque eram quatro artigos sobre o mesmo assunto. Os endereços
antigos redirecionam para o artigo único (`vercel.json`).

1. `artigos/jogos-iba-tres-jogos-diarios.html`: o site de jogos inteiro, os três jogos, a
   conferência por regra, o ano gerado antes e os cuidados que não aparecem na tela.

Nenhum número dos artigos foi estimado: os que aparecem (74 arranjos válidos no tabuleiro do
primeiro dia, 400 dias com solução única, 12.852 contas conferidas, 34 pares de contraste, teto de
120 KB de JavaScript) saíram de execução, e a maior parte deles saiu de arquivo que está no
repositório dos jogos, não da memória de quem escreveu.

## Como foi publicado (04/10/2026)

1. Projeto `blog-iba` criado na Vercel pela CLI logada no PC (`vercel link`, `vercel git connect`),
   preset **Other**, sem build, sem variável de ambiente.
2. `vercel domains add blog.ibaestudio.com blog-iba`. A Vercel pediu um CNAME próprio do projeto
   (`5fe355496f8cc7a5.vercel-dns-017.com`), e não o genérico `cname.vercel-dns.com`.
3. Registro `CNAME blog` na Cloudflare. **Cuidado medido:** `ibaestudio.com` tem um curinga (`*`);
   o registro do `blog` precisa ser explícito para não servir conteúdo de outro projeto.
4. Conferência: `curl -s https://blog.ibaestudio.com/` devolve o título do blog.

## O que já foi conferido

- `node verificar.mjs`: 0 problemas (arquivos, links internos, metatags, travessão, emoji, sitemap).
- Contraste medido por script, nos pares de texto e de forma: todos acima do piso da casa (4,5:1
  para texto, 3:1 para forma).
- Páginas abertas no navegador em 390 px de largura e em 1280 px, sem erro de console, sem rolagem
  horizontal e sem imagem quebrada.
- Nenhum arquivo de JavaScript no blog: o site é HTML e CSS.
