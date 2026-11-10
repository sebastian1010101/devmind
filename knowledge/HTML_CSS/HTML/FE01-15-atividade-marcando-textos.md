# FE01-15 — Atividade: Marcando Textos

## Objetivo da Atividade

Consolidar a aplicação prática de semântica HTML, organização de conteúdos textuais, listas, links e imagens em uma página de artigo temática.

---

## Enunciado do Desafio

Crie um arquivo chamado `artigo.html` que represente a publicação de um artigo de blog sobre tecnologia, contemplando:

1. Estrutura semântica com `<header>`, `<main>`, `<article>` e `<footer>`.
2. No `<header>`:
   - Um título com o nome do blog.
   - Um menu `<nav>` com três links não ordenados (`Home`, `Artigos`, `Contato`).
3. No `<main>` dentro de `<article>`:
   - Título principal do artigo (`h1`).
   - Dados de publicação: autor e data usando `<small>`.
   - Uma imagem ilustrativa com texto alternativo descritivo (`alt`) e dimensões declaradas.
   - Dois parágrafos de texto com destaques em `<strong>` e termos em `<em>`.
   - Um subtítulo (`h2`) introduzindo uma lista de tópicos essenciais.
   - Uma lista não ordenada (`<ul>`) com pelo menos três itens.
   - Um link para uma fonte externa com `target="_blank"` e `rel="noopener noreferrer"`.
4. No `<footer>`:
   - Um parágrafo com o aviso de direitos autorais e ano corrente.

---

## Solução de Referência

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Por que Aprender HTML Semântico em 2026? - DevBlog</title>
  </head>
  <body>
    <header>
      <h1>DevBlog Kenzie</h1>
      <nav>
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#artigos">Artigos</a></li>
          <li><a href="#contato">Contato</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <article>
        <h1>Por que Aprender HTML Semântico em 2026?</h1>
        <p><small>Publicado por <strong>Lucas Dev</strong> em 15 de Fevereiro de 2026</small></p>

        <figure>
          <img 
            src="https://images.unsplash.com/photo-1542838132-92c53300491e?w=800" 
            alt="Código HTML aberto em tela de computador" 
            width="800" 
            height="400"
            loading="lazy"
          >
          <figcaption>A base de toda aplicação web moderna começa no HTML bem estruturado.</figcaption>
        </figure>

        <p>
          O <em>HTML semântico</em> vai muito além da aparência visual. Ele garante que qualquer pessoa, independente das suas condições físicas ou dos dispositivos que utiliza, consiga navegar pelo conteúdo com clareza.
        </p>

        <p>
          Além disso, robôs de indexação como o Google conseguem classificar seu site com maior relevância quando a hierarquia de tags como <code>&lt;header&gt;</code>, <code>&lt;main&gt;</code> e <code>&lt;article&gt;</code> é respeitada.
        </p>

        <h2>Principais Benefícios da Semântica</h2>
        <ul>
          <li>Acessibilidade para leitores de tela</li>
          <li>Otimização para motores de busca (SEO)</li>
          <li>Facilidade de manutenção do código em equipe</li>
        </ul>

        <p>
          Saiba mais consultando a documentação oficial na 
          <a href="https://developer.mozilla.org/pt-BR/docs/Glossary/Semantics" target="_blank" rel="noopener noreferrer">MDN Web Docs</a>.
        </p>
      </article>
    </main>

    <footer>
      <p>&copy; 2026 DevBlog Kenzie. Todos os direitos reservados.</p>
    </footer>
  </body>
</html>
```
