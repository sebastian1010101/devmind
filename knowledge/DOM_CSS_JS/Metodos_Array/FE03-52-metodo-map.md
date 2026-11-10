# FE03-52 — Método map

## O que é

`map` **transforma** cada elemento de um array e retorna um **novo array** com os resultados — sempre com exatamente o mesmo número de itens do original.

A analogia clássica: `map` é uma esteira de produção. Cada item entra, a callback o transforma, e o item transformado sai na mesma posição do novo array.

```javascript
const numeros = [1, 2, 3, 4];

const dobrados = numeros.map(n => n * 2);

console.log(dobrados); // [2, 4, 6, 8]
console.log(numeros);  // [1, 2, 3, 4] — original intacto
```

## Sintaxe

```javascript
const novoArray = array.map((elemento, indice, arrayOriginal) => {
  return valorTransformado;
});
```

Com arrow function de retorno implícito (o padrão mais comum):

```javascript
const novoArray = array.map(elemento => valorTransformado);
```

## Regra fundamental: 1 pra 1

O array resultante tem **sempre** o mesmo tamanho do original. Se entraram 10 elementos, saem 10 — transformados, mas 10. Para remover elementos, o método certo é `filter`.

```javascript
const precos = [100, 200, 300];

const comDesconto = precos.map(preco => preco * 0.9);
// [90, 180, 270] — 3 entraram, 3 saíram
```

## Casos de uso clássicos

### Extrair uma propriedade de objetos

Provavelmente o uso mais frequente em código real:

```javascript
const usuarios = [
  { nome: "Ana", idade: 25 },
  { nome: "Beto", idade: 30 },
  { nome: "Carla", idade: 28 }
];

const nomes = usuarios.map(u => u.nome);
// ["Ana", "Beto", "Carla"]
```

### Transformar formato de dados

```javascript
const datas = ["2024-01-15", "2024-02-20"];

const formatadas = datas.map(d => {
  const [ano, mes, dia] = d.split("-");
  return `${dia}/${mes}/${ano}`;
});
// ["15/01/2024", "20/02/2024"]
```

### Gerar elementos de UI

```javascript
const produtos = [
  { nome: "Teclado", preco: 150 },
  { nome: "Mouse", preco: 80 }
];

const html = produtos.map(p => `
  <li class="produto">
    <span>${p.nome}</span>
    <strong>R$ ${p.preco}</strong>
  </li>
`).join("");
```

### Usando o índice

```javascript
const alunos = ["Ana", "Beto", "Carla"];

const chamada = alunos.map((nome, i) => `${i + 1}. ${nome}`);
// ["1. Ana", "2. Beto", "3. Carla"]
```

## A armadilha do retorno esquecido

Com `function` tradicional ou arrow com chaves `{}`, esquecer o `return` gera um array de `undefined`:

```javascript
// ❌ Chaves exigem return explícito
const errado = numeros.map(n => {
  n * 2; // calcula, mas não retorna nada
});
// [undefined, undefined, undefined, undefined]

// ✅ Correto
const certo = numeros.map(n => {
  return n * 2;
});
```

## map + encadeamento

```javascript
const pedidos = [
  { item: "Café", preco: 12, pago: true },
  { item: "Bolo", preco: 25, pago: false },
  { item: "Suco", preco: 8, pago: true }
];

const resumoPagos = pedidos
  .filter(p => p.pago)                        // só os pagos
  .map(p => `${p.item}: R$ ${p.preco}`);      // formata a descrição

// ["Café: R$ 12", "Suco: R$ 8"]
```

## map vs forEach

| Pergunta | `map` | `forEach` |
| --- | --- | --- |
| Quero um novo array? | Sim | — |
| Só quero executar efeitos? | — | Sim |
| Posso encadear o resultado? | Sim | Não (retorna `undefined`) |

Se você está fazendo `array.forEach(item => novoArray.push(...))`, pare — isso é um `map` disfarçado.
