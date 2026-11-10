# FE03-50 — Métodos de Array no ES6

## Panorama geral

O ES6 consolidou um conjunto de métodos de array que mudaram a forma de escrever JavaScript. Em vez de criar laços `for` manuais com variáveis de índice e acumuladores, passamos a descrever **o que** queremos fazer com cada elemento — não **como** percorrê-los.

Esses métodos são chamados de **Higher-Order Functions** (funções de ordem superior) porque recebem outra função como argumento — a famosa *callback* — e a executam para cada item do array.

## O mapa dos métodos

| Método | O que faz | Retorna |
| --- | --- | --- |
| `forEach` | Executa uma ação para cada elemento | `undefined` |
| `map` | Transforma cada elemento | Novo array, mesmo tamanho |
| `filter` | Seleciona elementos que passam num teste | Novo array, mesmo tamanho ou menor |
| `find` | Busca o primeiro elemento que passa no teste | Elemento ou `undefined` |
| `reduce` | Acumula os elementos num único valor | Qualquer valor (número, objeto, array) |
| `some` | Verifica se **algum** elemento passa no teste | `boolean` |
| `every` | Verifica se **todos** passam no teste | `boolean` |
| `includes` | Verifica se um valor existe no array | `boolean` |
| `indexOf` | Posição da primeira ocorrência de um valor | `number` (ou `-1`) |
| `splice` | Insere/remove elementos **alterando o original** | Array com os removidos |

## Imutáveis vs Mutáveis

Distinção essencial para evitar bugs:

### Métodos imutáveis (não alteram o array original)

```javascript
const numeros = [1, 2, 3];

const dobrados = numeros.map(n => n * 2);

console.log(dobrados); // [2, 4, 6]
console.log(numeros);  // [1, 2, 3] — intacto
```

### Métodos mutáveis (alteram o array original)

```javascript
const frutas = ["maçã", "banana", "uva"];

frutas.splice(1, 1); // remove "banana"

console.log(frutas); // ["maçã", "uva"] — o original mudou
```

Métodos mutáveis: `splice`, `push`, `pop`, `shift`, `unshift`, `sort`, `reverse`. Em código moderno e em paradigmas como React, a imutabilidade é preferida — sempre que possível, use métodos que retornam arrays novos.

## A assinatura padrão da callback

Quase todos esses métodos passam até 3 argumentos para a callback:

```javascript
array.metodo((elemento, indice, arrayOriginal) => {
  // elemento      → o item atual
  // indice        → a posição do item (0, 1, 2...)
  // arrayOriginal → referência ao array completo
});
```

Na prática, quase sempre só o primeiro parâmetro é usado. Os outros existem para quando você precisa da posição ou de comparações com o array inteiro.

## Declarativo vs Imperativo

### Imperativo (o "como")

```javascript
const nomes = [];
for (let i = 0; i < usuarios.length; i++) {
  nomes.push(usuarios[i].nome.toUpperCase());
}
```

### Declarativo (o "quê")

```javascript
const nomes = usuarios.map(u => u.nome.toUpperCase());
```

O estilo declarativo é mais curto, mais legível e elimina classes inteiras de bugs (índices errados, `off-by-one`, variáveis de controle esquecidas).

## Encadeamento (Chaining)

Como `map`, `filter` e companhia retornam arrays, eles podem ser encadeados — um padrão onipresente em código profissional:

```javascript
const resultado = produtos
  .filter(p => p.preco < 100)    // só os baratos
  .map(p => p.nome)              // extrai os nomes
  .sort();                       // ordena alfabeticamente
```

Lido da esquerda para a direita, o código conta uma história: *"filtre os baratos, pegue os nomes, ordene"*. Esse encadeamento será explorado em cada método individual nos próximos tópicos.
