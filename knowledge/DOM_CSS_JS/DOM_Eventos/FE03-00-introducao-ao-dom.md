# FE03-00 — Introdução ao DOM

## O que é o DOM?

**DOM** significa *Document Object Model* (Modelo de Objeto do Documento). É a interface de programação padrão para documentos HTML e XML.

Quando o navegador carrega uma página web, ele processa o texto HTML e constrói em memória uma **árvore hierárquica de nós e objetos** (*DOM Tree*). O JavaScript utiliza o DOM como uma ponte para:

- Ler, alterar ou excluir elementos e textos existentes.
- Criar e inserir novos elementos em tempo real.
- Modificar estilos e classes CSS dinamicamente.
- Escutar e responder a interações do usuário (cliques, digitação, rolagem).

---

## A Árvore do DOM (DOM Tree)

Cada tag HTML é convertida em um **nó de elemento** na árvore:

```text
               WINDOW (Objeto Global do Navegador)
                         |
                      DOCUMENT (A Página Carregada)
                         |
                      <html> (Elemento Raiz)
                     /      \
               <head>        <body>
              /      \       /    \
        <meta>     <title>  <h1>   <p>
```

- **Nós de Elemento:** as tags (`<h1>`, `<button>`, `<div>`).
- **Nós de Texto:** o conteúdo textual dentro das tags.
- **Nós de Atributo:** as propriedades (`id`, `class`, `src`, `href`).

---

## O Objeto `document`

O ponto de entrada de qualquer manipulação de DOM em JavaScript é o objeto global `document`:

```javascript
// Exibe a representação do DOM no console:
console.log(document);

// Acessa o título da página:
console.log(document.title);

// Altera o título da aba do navegador dinamicamente:
document.title = "Novo Título da Aplicação";
```
