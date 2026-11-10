# FE03-04 — Atividade: Criando Elementos

## Objetivo da Atividade

Construir dinamicamente componentes de interface no DOM a partir de dados estruturados (arrays de objetos), aplicando `createElement`, manipulação de textos, atributos e montagem com `appendChild`.

---

## Enunciado do Desafio

Dado o array de produtos abaixo:

```javascript
const listaProdutos = [
  { nome: "Teclado Mecânico", preco: 250.00, categoria: "Periféricos" },
  { nome: "Headset Gamer", preco: 180.00, categoria: "Áudio" },
  { nome: "Mouse Sem Fio", preco: 95.00, categoria: "Periféricos" }
];
```

Crie uma função `renderizarCatalogo(produtos)` que:
1. Seleciona o container com o ID `#vitrine-produtos`.
2. Para cada produto da lista:
   - Cria uma tag `<article>` com a classe `.card-produto`.
   - Cria um título `<h3>` com o nome do produto.
   - Cria um parágrafo `<p>` formatando o preço em reais.
   - Cria uma etiqueta `<span>` com a categoria.
   - Cria um botão com o texto `"Comprar"`.
   - Monta a hierarquia inserindo todos os filhos dentro do `<article>` e, por fim, insere o `<article>` no container `#vitrine-produtos`.

---

## Solução de Referência

```javascript
function renderizarCatalogo(produtos) {
  const containerVitrine = document.querySelector("#vitrine-produtos");
  if (!containerVitrine) return;

  // Limpa o container antes de renderizar
  containerVitrine.innerHTML = "";

  for (const produto of produtos) {
    // 1. Cria os nós na memória
    const card = document.createElement("article");
    card.classList.add("card-produto");

    const titulo = document.createElement("h3");
    titulo.innerText = produto.nome;

    const preco = document.createElement("p");
    preco.innerText = `R$ ${produto.preco.toFixed(2)}`;

    const categoria = document.createElement("span");
    categoria.classList.add("badge-categoria");
    categoria.innerText = produto.categoria;

    const botaoComprar = document.createElement("button");
    botaoComprar.innerText = "Comprar";
    botaoComprar.classList.add("btn-comprar");

    // 2. Monta a árvore interna do card
    card.append(categoria, titulo, preco, botaoComprar);

    // 3. Insere o card pronto na tela
    containerVitrine.appendChild(card);
  }
}

// Invocação da renderização:
renderizarCatalogo(listaProdutos);
```
