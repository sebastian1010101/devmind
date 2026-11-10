# FE01-14 — Tags Semânticas

## O que é Semântica no HTML?

HTML Semântico é a prática de utilizar tags que descrevem com precisão o **significado e o papel** do conteúdo tanto para o desenvolvedor quanto para navegadores, robôs de busca (Google, Bing) e tecnologias assistivas (leitores de tela).

Antes do HTML5, páginas inteiras eram construídas apenas com `<div>` genéricas:

```html
<!-- Padrão Antigo Não-Semântico -->
<div class="header">...</div>
<div class="nav">...</div>
<div class="content">...</div>
<div class="footer">...</div>
```

Com o HTML5, utilizamos tags que expressam diretamente a intenção estrutural da página.

---

## Principais Tags Estruturais do HTML5

```text
+-------------------------------------------------------+
|                       <header>                        |
|                         <nav>                         |
+-------------------------------------------------------+
|                       <main>                          |
|  +--------------------------------+  +-------------+  |
|  |           <section>            |  |   <aside>   |  |
|  |  +--------------------------+  |  | (barra      |  |
|  |  |        <article>         |  |  |  lateral    |  |
|  |  +--------------------------+  |  |  ou links)  |  |
|  +--------------------------------+  +-------------+  |
+-------------------------------------------------------+
|                       <footer>                        |
+-------------------------------------------------------+
```

| Tag Semântica | Quando Utilizar |
| --- | --- |
| `<header>` | Cabeçalho introdutório da página ou de uma seção específica. Frequentemente contém logotipo e menu. |
| `<nav>` | Bloco contendo os principais links de navegação da página ou do site. |
| `<main>` | O conteúdo principal e exclusivo do documento. Deve existir apenas um por página. |
| `<section>` | Uma seção temática genérica do documento (ex: "Sobre", "Serviços", "Depoimentos"). Geralmente possui um título próprio (`<h2>`). |
| `<article>` | Um conteúdo autônomo, independente e que faça sentido completo por si só fora da página (ex: post de blog, notícia, comentário). |
| `<aside>` | Conteúdo tangencial ou complementar ao redor (ex: barras laterais, banners de aviso, links relacionados). |
| `<footer>` | Rodapé da página ou de uma seção. Costuma conter direitos autorais, links secundários e contatos. |

---

## Elementos Genéricos: Quando Usar `<div>` e `<span>`?

- Utilize `<div>` e `<span>` apenas quando nenhuma tag semântica representar o significado do conteúdo e você precisar de um container puramente estilístico para aplicar CSS ou manipulações em JavaScript.
  - `<div>`: elemento de bloco genérico.
  - `<span>`: elemento em linha genérico para trechos de texto.
