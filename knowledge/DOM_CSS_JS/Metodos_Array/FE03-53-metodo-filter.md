# FE03-53 — Método filter

## O que é

`filter` cria um **novo array** contendo apenas os elementos que passam num teste — ou seja, os elementos para os quais a callback retorna `true`.

A analogia: `filter` é uma peneira. Tudo que passa pelo teste fica; o resto é descartado.

```javascript
const numeros = [1, 2, 3, 4, 5, 6];

const pares = numeros.filter(n => n % 2 === 0);

console.log(pares);   // [2, 4, 6]
console.log(numeros); // [1, 2, 3, 4, 5, 6] — original intacto
```

## Sintaxe

```javascript
const novoArray = array.filter((elemento, indice, arrayOriginal) => {
  return condicao; // true → entra no novo array; false → descartado
});
```

A callback é chamada de **predicado**: uma função que responde uma pergunta de sim/não sobre cada elemento.

## Pontos-chave

- O novo array tem tamanho **menor ou igual** ao original (pode até ficar vazio)
- O array original **nunca** é modificado
- A callback deve retornar um valor *truthy* ou *falsy* — o retorno decide a entrada, não o valor em si

## Casos de uso clássicos

### Filtrar objetos por propriedade

```javascript
const produtos = [
  { nome: "Teclado", preco: 150, estoque: 5 },
  { nome: "Mouse", preco: 80, estoque: 0 },
  { nome: "Monitor", preco: 900, estoque: 3 }
];

const disponiveis = produtos.filter(p => p.estoque > 0);
// [Teclado, Monitor]

const baratos = produtos.filter(p => p.preco < 100);
// [Mouse]
```

### Filtrar strings

```javascript
const palavras = ["sol", "javascript", "lua", "programação", "mar"];

const longas = palavras.filter(p => p.length > 5);
// ["javascript", "programação"]
```

### Remover valores falsy

Truque elegante usando o próprio `Boolean` como predicado:

```javascript
const misto = [0, "oi", "", null, "tchau", undefined, 42];

const limpos = misto.filter(Boolean);
// ["oi", "tchau", 42] — todos os falsy removidos
```

### Filtrar com o índice

```javascript
const letras = ["a", "b", "c", "d", "e"];

const posicoesPares = letras.filter((_, i) => i % 2 === 0);
// ["a", "c", "e"] — elementos nas posições 0, 2, 4
```

O `_` é a convenção para "parâmetro que preciso declarar mas não vou usar".

## A armadilha da comparação errada

```javascript
const usuarios = [
  { nome: "Ana", ativo: true },
  { nome: "Beto", ativo: false }
];

// ❌ Retorna o objeto — sempre truthy, nada é filtrado
usuarios.filter(u => u.ativo = true); // atribuição, não comparação!

// ✅ Correto
usuarios.filter(u => u.ativo === true);
// ou simplesmente:
usuarios.filter(u => u.ativo);
```

## Encadeamento: filter + map

O combo mais comum do JavaScript moderno — primeiro selecione, depois transforme:

```javascript
const alunos = [
  { nome: "Ana", nota: 8 },
  { nome: "Beto", nota: 4 },
  { nome: "Carla", nota: 9 },
  { nome: "Diego", nota: 5 }
];

const aprovados = alunos
  .filter(a => a.nota >= 6)   // ["Ana", "Carla"]
  .map(a => a.nome);          // extrai só os nomes

// ["Ana", "Carla"]
```

A ordem importa: filtrar **antes** de mapear economiza trabalho — o `map` só processa quem passou.

## filter vs find vs some

| Método | Pergunta respondida | Retorno |
| --- | --- | --- |
| `filter` | "Quais passam no teste?" | Array com todos que passam |
| `find` | "Qual é o primeiro que passa?" | O elemento (ou `undefined`) |
| `some` | "Existe algum que passa?" | `boolean` |

```javascript
const numeros = [3, 7, 10, 14];

numeros.filter(n => n > 5); // [7, 10, 14] — todos
numeros.find(n => n > 5);   // 7 — só o primeiro
numeros.some(n => n > 5);   // true — existe pelo menos um
```
