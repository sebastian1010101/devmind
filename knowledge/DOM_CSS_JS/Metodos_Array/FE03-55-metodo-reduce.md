# FE03-55 — Método reduce

## O que é

`reduce` pega todos os elementos de um array e os **reduz a um único valor** — que pode ser um número, uma string, um objeto ou até outro array. É o método de array mais poderoso e, de longe, o mais temido por quem está começando.

A analogia: `reduce` é uma bola de neve. Começa com um valor inicial (o acumulador) e cada elemento do array é "adicionado" a ela, transformando-a a cada volta.

```javascript
const numeros = [1, 2, 3, 4];

const soma = numeros.reduce((acumulador, numero) => {
  return acumulador + numero;
}, 0);

console.log(soma); // 10
```

## Sintaxe

```javascript
const resultado = array.reduce((acumulador, elemento, indice, array) => {
  return novoAcumulador;
}, valorInicial);
```

- **acumulador** — o valor que "carrega" o resultado parcial de volta em volta
- **elemento** — o item atual do array
- **valorInicial** — de onde o acumulador começa

## Entendendo a execução passo a passo

```javascript
[10, 20, 30].reduce((acc, n) => acc + n, 0);
```

| Volta | acumulador | elemento | retorna |
| --- | --- | --- | --- |
| 1 | 0 | 10 | 10 |
| 2 | 10 | 20 | 30 |
| 3 | 30 | 30 | 60 |

Resultado final: `60`.

## A importância do valor inicial

**Sempre** forneça o valor inicial. Sem ele, o `reduce` usa o primeiro elemento como acumulador e começa a iterar do segundo — o que quebra em arrays vazios e muda o tipo do acumulador silenciosamente:

```javascript
// ❌ Sem valor inicial — explode em array vazio
[].reduce((acc, n) => acc + n); // TypeError: Reduce of empty array

// ✅ Com valor inicial — retorna 0 com segurança
[].reduce((acc, n) => acc + n, 0); // 0
```

## Casos de uso clássicos

### Somar propriedades de objetos

```javascript
const carrinho = [
  { produto: "Teclado", preco: 150 },
  { produto: "Mouse", preco: 80 },
  { produto: "Mousepad", preco: 40 }
];

const total = carrinho.reduce((acc, item) => acc + item.preco, 0);
// 270
```

O `0` inicial define que o acumulador é um **número** — sem ele, a primeira volta tentaria somar um objeto.

### Contar ocorrências (acumulador objeto)

```javascript
const votos = ["Ana", "Beto", "Ana", "Carla", "Beto", "Ana"];

const contagem = votos.reduce((acc, nome) => {
  acc[nome] = (acc[nome] || 0) + 1;
  return acc;
}, {});

// { Ana: 3, Beto: 2, Carla: 1 }
```

Aqui o valor inicial é `{}` — o acumulador é um objeto que cresce a cada volta.

### Agrupar por propriedade

```javascript
const pessoas = [
  { nome: "Ana", setor: "dev" },
  { nome: "Beto", setor: "design" },
  { nome: "Carla", setor: "dev" }
];

const porSetor = pessoas.reduce((acc, p) => {
  (acc[p.setor] = acc[p.setor] || []).push(p.nome);
  return acc;
}, {});

// { dev: ["Ana", "Carla"], design: ["Beto"] }
```

### Achatar array de arrays

```javascript
const grupos = [[1, 2], [3, 4], [5]];

const achatado = grupos.reduce((acc, grupo) => acc.concat(grupo), []);
// [1, 2, 3, 4, 5]
```

### Encontrar o maior/menor

```javascript
const notas = [7, 9, 4, 8];

const maior = notas.reduce((acc, n) => (n > acc ? n : acc), notas[0]);
// 9
```

## reduce com encadeamento

```javascript
const pedidos = [
  { item: "Café", preco: 12, pago: true },
  { item: "Bolo", preco: 25, pago: false },
  { item: "Suco", preco: 8, pago: true }
];

const totalPago = pedidos
  .filter(p => p.pago)
  .reduce((acc, p) => acc + p.preco, 0);
// 20
```

## Quando NÃO usar reduce

O `reduce` é flexível demais — dá para reescrever `map` e `filter` com ele, mas o código fica menos legível. Prefira o método específico:

| Se o objetivo é... | Use |
| --- | --- |
| Transformar elementos 1:1 | `map` |
| Selecionar elementos | `filter` |
| Encontrar um elemento | `find` |
| Somar, agrupar, consolidar | `reduce` |

Regra prática: se o acumulador muda de *forma* mas não de *tipo de estrutura* (`number` → `number`, `{}` → `{}`), `reduce` é a escolha certa. Se você está montando um array do mesmo tamanho, é um `map` disfarçado.
