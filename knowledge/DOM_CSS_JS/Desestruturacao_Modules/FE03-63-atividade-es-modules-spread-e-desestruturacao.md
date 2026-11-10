# FE03-63 — Atividade: ES Modules, Spread e Desestruturação

## Objetivo

Integrar os três conceitos do bloco — **módulos ES6**, **desestruturação** e **spread** — num mini-projeto de carrinho de compras modularizado.

## Estrutura do projeto

```text
carrinho/
├── index.html
├── app.js              ← ponto de entrada
├── data/
│   └── produtos.js     ← dados do catálogo
├── services/
│   └── carrinho.js     ← lógica do carrinho
└── utils/
    └── format.js       ← formatadores
```

## Arquivo 1 — dados (named export de array)

```javascript
// data/produtos.js
export const produtos = [
  { id: 1, nome: "Teclado", preco: 150, categoria: "perifericos" },
  { id: 2, nome: "Mouse", preco: 80, categoria: "perifericos" },
  { id: 3, nome: "Monitor", preco: 900, categoria: "monitores" },
  { id: 4, nome: "Mousepad", preco: 40, categoria: "perifericos" }
];
```

## Arquivo 2 — utilitários (named exports + desestruturação)

```javascript
// utils/format.js
export function formatarMoeda(valor) {
  return `R$ ${valor.toFixed(2)}`;
}

export function resumir({ nome, preco }) {
  return `${nome} — ${formatarMoeda(preco)}`;
}
```

## Arquivo 3 — lógica do carrinho (spread + imutabilidade)

```javascript
// services/carrinho.js
let itens = [];

export function adicionar(produto) {
  // ✅ Imutável — novo array, sem mutar 'itens' por fora
  itens = [...itens, { ...produto, quantidade: 1 }];
  return itens;
}

export function remover(id) {
  itens = itens.filter(item => item.id !== id);
  return itens;
}

export function total() {
  return itens.reduce((acc, { preco, quantidade }) => acc + preco * quantidade, 0);
}

export function listar() {
  return [...itens]; // devolve cópia — protege o estado interno
}
```

## Arquivo 4 — ponto de entrada

```javascript
// app.js
import { produtos } from "./data/produtos.js";
import { formatarMoeda, resumir } from "./utils/format.js";
import { adicionar, remover, total, listar } from "./services/carrinho.js";

// Desestruturação do primeiro produto
const [primeiro, ...resto] = produtos;

console.log(resumir(primeiro)); // "Teclado — R$ 150.00"

adicionar(primeiro);
adicionar(resto[0]); // Mouse

console.log(formatarMoeda(total())); // "R$ 230.00"
console.log(listar().length);        // 2

remover(primeiro.id);
console.log(formatarMoeda(total())); // "R$ 80.00"
```

## HTML — ativando o módulo

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Carrinho</title>
</head>
<body>
  <h1>Carrinho</h1>
  <ul id="itens"></ul>
  <script type="module" src="app.js"></script>
</body>
</html>
```

## Desafios extras

### Desafio A — agrupar por categoria

Em `app.js`, desestruture e agrupe os produtos:

```javascript
const porCategoria = produtos.reduce((acc, p) => {
  const { categoria } = p;
  acc[categoria] = [...(acc[categoria] || []), p];
  return acc;
}, {});
```

### Desafio B — produto mais caro com desestruturação

```javascript
const maisCaro = produtos.reduce((a, b) => (b.preco > a.preco ? b : a));
const { nome, preco } = maisCaro;
console.log(`${nome}: ${formatarMoeda(preco)}`);
```

### Desafio C — configuração com defaults

```javascript
function criarCarrinho({ desconto = 0, frete = 20 } = {}) {
  return { desconto, frete };
}

const config1 = criarCarrinho();                    // { desconto: 0, frete: 20 }
const config2 = criarCarrinho({ desconto: 0.1 });   // { desconto: 0.1, frete: 20 }
```

## Critérios de verificação

- Cada arquivo tem **uma responsabilidade** (dados, lógica, formatação, orquestração)
- `type="module"` no `<script>` e servidor local funcionando
- Named exports com `import { nome }` e default com `import Nome`
- Spread usado para **cópias imutáveis** — nenhuma mutação direta de estado
- Desestruturação em parâmetros e extrações — sem `obj.prop` repetido

## Erros comuns a evitar

| Erro | Correção |
| --- | --- |
| `import` sem `.js` no caminho | Navegador exige extensão: `"./utils.js"` |
| `{...produto}` compartilhando referência | Spread é raso — objetos aninhados ainda são referências |
| `itens = [...itens]` fora do módulo | O array interno de `carrinho.js` é privado — use `listar()` |
| `file://` no lugar de `localhost` | Módulos exigem HTTP — use Live Server ou `python3 -m http.server` |
