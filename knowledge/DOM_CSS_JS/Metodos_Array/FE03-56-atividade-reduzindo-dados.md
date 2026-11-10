# FE03-56 — Atividade: Reduzindo Dados

## Objetivo

Dominar o `reduce` aplicando-o a problemas reais de consolidação: somatórios, médias, contagens e agrupamentos sobre arrays de objetos.

## Cenário

Vendas de uma loja durante a semana:

```javascript
const vendas = [
  { vendedor: "Ana", valor: 300, categoria: "eletronicos" },
  { vendedor: "Beto", valor: 150, categoria: "moveis" },
  { vendedor: "Ana", valor: 200, categoria: "eletronicos" },
  { vendedor: "Carla", valor: 500, categoria: "eletrodomesticos" },
  { vendedor: "Beto", valor: 80, categoria: "eletronicos" },
  { vendedor: "Carla", valor: 120, categoria: "moveis" }
];
```

## Desafio 1 — Faturamento total

```javascript
const faturamento = vendas.reduce((acc, v) => acc + v.valor, 0);
// 1350
```

## Desafio 2 — Ticket médio

```javascript
const ticketMedio = vendas.reduce((acc, v) => acc + v.valor, 0) / vendas.length;
// 225
```

Ou numa única passada, acessando o array pelo terceiro parâmetro:

```javascript
const ticket = vendas.reduce((acc, v, i, arr) => {
  acc += v.valor;
  return i === arr.length - 1 ? acc / arr.length : acc;
}, 0);
```

## Desafio 3 — Total por vendedor

Consolide o faturamento de cada pessoa num objeto:

```javascript
const porVendedor = vendas.reduce((acc, v) => {
  acc[v.vendedor] = (acc[v.vendedor] || 0) + v.valor;
  return acc;
}, {});

// { Ana: 500, Beto: 230, Carla: 620 }
```

## Desafio 4 — Contagem por categoria

Quantas vendas ocorreram em cada categoria?

```javascript
const porCategoria = vendas.reduce((acc, v) => {
  acc[v.categoria] = (acc[v.categoria] || 0) + 1;
  return acc;
}, {});

// { eletronicos: 3, moveis: 2, eletrodomesticos: 1 }
```

## Desafio 5 — Maior venda

Encontre a venda de maior valor (o objeto inteiro, não só o valor):

```javascript
const maiorVenda = vendas.reduce(
  (acc, v) => (v.valor > acc.valor ? v : acc),
  vendas[0]
);

// { vendedor: "Carla", valor: 500, categoria: "eletrodomesticos" }
```

## Desafio 6 — Relatório completo num reduce só

Gere um objeto-resumo com totais e extremos:

```javascript
const relatorio = vendas.reduce(
  (acc, v) => {
    acc.total += v.valor;
    acc.quantidade += 1;
    if (v.valor > acc.maior) acc.maior = v.valor;
    if (v.valor < acc.menor) acc.menor = v.valor;
    return acc;
  },
  { total: 0, quantidade: 0, maior: -Infinity, menor: Infinity }
);

// { total: 1350, quantidade: 6, maior: 500, menor: 80 }
```

## Desafio 7 — Vendas de eletrônicos por vendedor

Combine `filter` + `reduce`:

```javascript
const eletronicosPorVendedor = vendas
  .filter(v => v.categoria === "eletronicos")
  .reduce((acc, v) => {
    acc[v.vendedor] = (acc[v.vendedor] || 0) + v.valor;
    return acc;
  }, {});

// { Ana: 500, Beto: 80 }
```

## Critérios de verificação

- Toda chamada de `reduce` tem **valor inicial explícito** (`0`, `{}`, `[]`, objeto de configuração)
- O tipo do acumulador é consistente: número para somas, objeto para contagens/agrupamentos
- A callback sempre **retorna o acumulador** — esquecer o `return` é o bug nº 1 do reduce
- `filter` antes de `reduce` para consolidar subconjuntos

## Erros comuns a evitar

| Erro | Sintoma |
| --- | --- |
| Sem valor inicial | `TypeError` em array vazio ou acumulador de tipo errado |
| Esquecer `return acc` | `undefined` na volta seguinte — `NaN` silencioso |
| `acc[v.vendedor] += v.valor` sem inicializar | `NaN`, pois `undefined + número = NaN` — use `(acc[k] \|\| 0)` |
| Reduzir para transformar 1:1 | Isso é `map` — deixe `reduce` para consolidação |
