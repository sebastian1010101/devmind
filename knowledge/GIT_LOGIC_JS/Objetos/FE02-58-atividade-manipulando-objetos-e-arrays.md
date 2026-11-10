# FE02-58 — Atividade: Manipulando Objetos e Arrays

## A Estrutura Mais Comum na Web: Arrays de Objetos

Na grande maioria das aplicações reais (e-commerces, redes sociais, dashboards), os dados que chegam de APIs e bancos de dados são organizados como **uma lista (array) contendo múltiplos registros estruturados (objetos)**:

```javascript
const catalogo = [
  { id: 1, titulo: "Camiseta Dev", preco: 59.90, categoria: "Vestuário" },
  { id: 2, titulo: "Caneca Kenzie", preco: 35.00, categoria: "Acessórios" },
  { id: 3, titulo: "Adesivo JS", preco: 5.00, categoria: "Acessórios" }
];
```

---

## Enunciado do Desafio

Crie um módulo de operações de loja virtual implementando as funções:

1. `filtrarPorCategoria(produtos, categoriaDesejada)`:
   - Retorna um novo array contendo apenas os objetos cuja categoria corresponda à informada.
2. `calcularTotalEstoque(produtos)`:
   - Cada produto agora possui `preco` e `quantidadeEstoque`.
   - Calcule e retorne o patrimônio financeiro total do estoque (`soma de preco * quantidadeEstoque`).
3. `buscarPorId(produtos, idBusca)`:
   - Localiza e retorna o objeto do produto com o ID especificado, ou `null` caso não exista.

---

## Solução de Referência

```javascript
const produtosLoja = [
  { id: 101, nome: "Notebook Gamer", preco: 4500.00, estoque: 4, categoria: "Informática" },
  { id: 102, nome: "Mouse Óptico", preco: 90.00, estoque: 20, categoria: "Periféricos" },
  { id: 103, nome: "Teclado Sem Fio", preco: 220.00, estoque: 8, categoria: "Periféricos" },
  { id: 104, nome: "Monitor 27 Pol", preco: 1400.00, estoque: 5, categoria: "Informática" }
];

// 1. Filtrar por categoria
function filtrarPorCategoria(produtos, categoriaDesejada) {
  const filtrados = [];
  for (const item of produtos) {
    if (item.categoria.toLowerCase() === categoriaDesejada.toLowerCase()) {
      filtrados.push(item);
    }
  }
  return filtrados;
}

// 2. Calcular valor total do estoque
function calcularTotalEstoque(produtos) {
  let total = 0;
  for (const item of produtos) {
    total += item.preco * item.estoque;
  }
  return total;
}

// 3. Buscar produto por ID único
function buscarPorId(produtos, idBusca) {
  for (const item of produtos) {
    if (item.id === idBusca) {
      return item;
    }
  }
  return null;
}

// Testes:
console.log("Periféricos encontrados:", filtrarPorCategoria(produtosLoja, "periféricos"));
console.log("Valor total do inventário: R$", calcularTotalEstoque(produtosLoja)); // R$ 37.960
console.log("Busca ID 103:", buscarPorId(produtosLoja, 103));
```
