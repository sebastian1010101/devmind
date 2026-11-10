# FE01-38-1 — Projeto: Blog Kenzie

## Visão Geral do Projeto

O **Projeto Blog Kenzie** é a primeira entrega prática integradora do módulo, consolidando todo o conhecimento acumulado em estruturação semântica HTML5, modelos de caixa, estilizações de fontes e cores, posicionamentos e boas práticas de CSS sem frameworks externos.

---

## Requisitos do Projeto

### 1. Estrutura HTML Semântica

- `<header>` contendo o logotipo do blog e uma barra de navegação `<nav>` com links de categorias.
- `<main>` contendo:
  - Uma seção `<section class="destaque">` com o post principal em evidência.
  - Uma seção `<section class="recentes">` com uma grade de artigos secundários estruturados como `<article>`.
  - Uma barra lateral `<aside>` com perfil do autor e links de tópicos populares.
- `<footer>` com créditos, redes sociais e direitos autorais.

### 2. Estilização CSS

- Utilização de arquivo `reset.css` dedicado para padronização entre navegadores.
- Arquivo `style.css` com separação por classes reutilizáveis.
- Aplicação estrita de `box-sizing: border-box`.
- Tipografia escalável utilizando unidades relativas (`rem`).
- Efeitos visuais em estados interativos (`:hover` em botões e links de artigos).

---

## Estrutura de Código de Referência

### `index.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Kenzie - Notícias de Tecnologia</title>
    <link rel="stylesheet" href="reset.css">
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <header class="cabecalho">
      <div class="container nav-wrapper">
        <h1 class="logo">Kenzie<span>Blog</span></h1>
        <nav>
          <ul class="nav-links">
            <li><a href="#">Início</a></li>
            <li><a href="#">Front-End</a></li>
            <li><a href="#">Carreira</a></li>
          </ul>
        </nav>
      </div>
    </header>

    <main class="container layout-principal">
      <div class="conteudo-artigos">
        <!-- Post Destaque -->
        <article class="post-destaque">
          <img src="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800" alt="Notebook com código de programação">
          <div class="destaque-info">
            <span class="tag">Front-End</span>
            <h2>Como Construir uma Carreira Sólida em Desenvolvimento Web</h2>
            <p>Descubra as principais competências e fundamentos necessários para ingressar no mercado de tecnologia em 2026.</p>
            <a href="#" class="btn-ler">Ler Artigo Completo</a>
          </div>
        </article>

        <!-- Grade de Artigos -->
        <section class="posts-grade">
          <article class="card-artigo">
            <span class="tag">HTML5</span>
            <h3>Guia Prático de Semântica</h3>
            <p>Entenda o porquê de utilizar tags estruturais corretas melhora acessibilidade e SEO.</p>
            <a href="#" class="link-artigo">Continuar lendo &rarr;</a>
          </article>

          <article class="card-artigo">
            <span class="tag">CSS3</span>
            <h3>Dominando o Box Model</h3>
            <p>Aprenda a controlar margens, paddings e dimensões sem quebrar seu layout.</p>
            <a href="#" class="link-artigo">Continuar lendo &rarr;</a>
          </article>
        </section>
      </div>

      <!-- Barra Lateral -->
      <aside class="barra-lateral">
        <div class="widget-autor">
          <h3>Sobre o Autor</h3>
          <p>Equipe de instrutores e especialistas da Kenzie Academy Brasil compartilhando conteúdo técnico semanal.</p>
        </div>
      </aside>
    </main>

    <footer class="rodape">
      <p>&copy; 2026 Blog Kenzie Academy. Todos os direitos reservados.</p>
    </footer>
  </body>
</html>
```

### `style.css`

```css
body {
  font-family: system-ui, -apple-system, sans-serif;
  background-color: #f8fafc;
  color: #1e293b;
  line-height: 1.6;
}

.container {
  max-width: 1140px;
  margin: 0 auto;
  padding: 0 16px;
}

.cabecalho {
  background-color: #0f172a;
  color: #ffffff;
  padding: 16px 0;
}

.logo {
  font-size: 24px;
}

.logo span {
  color: #3b82f6;
}

.nav-links li {
  display: inline-block;
  margin-left: 16px;
}

.nav-links a:hover {
  color: #3b82f6;
}

.layout-principal {
  margin-top: 32px;
  margin-bottom: 48px;
}

.post-destaque {
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 32px;
}

.destaque-info {
  padding: 24px;
}

.tag {
  display: inline-block;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 12px;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
}

.btn-ler {
  display: inline-block;
  margin-top: 16px;
  background-color: #3b82f6;
  color: #ffffff;
  padding: 10px 18px;
  border-radius: 6px;
  font-weight: 600;
}

.btn-ler:hover {
  background-color: #2563eb;
}

.card-artigo {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 16px;
}

.link-artigo {
  color: #3b82f6;
  font-weight: 600;
  display: inline-block;
  margin-top: 8px;
}

.rodape {
  background: #0f172a;
  color: #94a3b8;
  text-align: center;
  padding: 24px 0;
}
```
