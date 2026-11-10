# FE03-54 — Atividade: Criando Filtro de Dados

## Objetivo

Praticar `filter` (e o encadeamento com `map`) construindo filtros reais sobre uma coleção de dados — o padrão por trás de todo catálogo, busca e listagem da web.

## Cenário

Temos a base de produtos de uma loja:

```javascript
const produtos = [
  { id: 1, nome: "Notebook", categoria: "eletronicos", preco: 3500, estoque: 4 },
  { id: 2, nome: "Mouse", categoria: "eletronicos", preco: 80, estoque: 0 },
  { id: 3, nome: "Cadeira Gamer", categoria: "moveis", preco: 1200, estoque: 2 },
  { id: 4, nome: "Teclado", categoria: "eletronicos", preco: 150, estoque: 10 },
  { id: 5, nome: "Mesa de Escritório", categoria: "moveis", preco: 900, estoque: 0 },
  { id: 6, nome: "Fone Bluetooth", categoria: "eletronicos", preco: 200, estoque: 7 }
];
```

## Desafio 1 — Produtos em estoque

Liste apenas os produtos disponíveis para venda:

```javascript
const emEstoque = produtos.filter(p => p.estoque > 0);

console.log(emEstoque.length); // 4
```

## Desafio 2 — Filtro por categoria

Crie uma função reutilizável que filtre por qualquer categoria:

```javascript
function filtrarPorCategoria(lista, categoria) {
  return lista.filter(p => p.categoria === categoria);
}

const eletronicos = filtrarPorCategoria(produtos, "eletronicos");
// [Notebook, Mouse, Teclado, Fone Bluetooth]
```

## Desafio 3 — Faixa de preço

Filtre produtos entre dois valores, inclusive:

```javascript
function filtrarPorPreco(lista, min, max) {
  return lista.filter(p => p.preco >= min && p.preco <= max);
}

const acessiveis = filtrarPorPreco(produtos, 50, 300);
// [Mouse, Teclado, Fone Bluetooth]
```

## Desafio 4 — Combinando filtros

Produtos eletrônicos **disponíveis** e abaixo de R$ 500:

```javascript
const resultado = produtos
  .filter(p => p.categoria === "eletronicos")
  .filter(p => p.estoque > 0)
  .filter(p => p.preco < 500);

// [Teclado, Fone Bluetooth]
```

Ou num predicado só — equivalente, e mais performático:

```javascript
const resultado = produtos.filter(
  p => p.categoria === "eletronicos" && p.estoque > 0 && p.preco < 500
);
```

## Desafio 5 — Filtro + formatação para exibição

Gere os cards em texto dos produtos disponíveis, ordenando do mais barato ao mais caro:

```javascript
const vitrine = produtos
  .filter(p => p.estoque > 0)
  .map(p => `${p.nome} — R$ ${p.preco.toFixed(2)}`)
  .sort();

console.log(vitrine);
// ["Cadeira Gamer — R$ 1200.00", "Fone Bluetooth — R$ 200.00", ...]
```

## Desafio 6 — Busca por texto (preview do FE03-59)

Filtre produtos cujo nome contenha um termo digitado, ignorando maiúsculas:

```javascript
function buscar(lista, termo) {
  const t = termo.toLowerCase();
  return lista.filter(p => p.nome.toLowerCase().includes(t));
}

buscar(produtos, "te"); // [Notebook, Teclado]
```

## Critérios de verificação

- Cada `filter` retorna um **novo** array — a lista `produtos` original nunca muda
- Predicados retornam comparações (`===`, `>`, `includes`), nunca atribuições (`=`)
- O encadeamento `filter → map → sort` é lido como uma sequência lógica
- Funções de filtro são reutilizáveis (recebem a lista como parâmetro)

## Erros comuns a evitar

| Erro | Por que falha |
| --- | --- |
| `filter(p => p.estoque = 0)` | `=` atribui; use `===` ou `>` para comparar |
| Usar `map` para filtrar | `map` sempre retorna o mesmo tamanho — seleção é papel do `filter` |
| Modificar `produtos` dentro da callback | Callbacks de `filter` devem ser puras (sem efeitos colaterais) |
| `includes()` com case diferente | Normalize com `.toLowerCase()` nos dois lados |
