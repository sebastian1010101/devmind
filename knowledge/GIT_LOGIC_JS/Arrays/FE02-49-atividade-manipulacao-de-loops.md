# FE02-49 — Atividade: Manipulação de Loops

## Objetivo da Atividade

Trabalhar com filtragem, inversão de listas e construção de novos arrays transformados a partir de laços de repetição.

---

## Enunciado do Desafio

Construa as seguintes funções de manipulação de vetores:

1. `filtrarNumerosPares(lista)`:
   - Recebe um array de inteiros e retorna um **novo array** contendo exclusivamente os números pares.
2. `inverterArray(lista)`:
   - Recebe um array e retorna um novo array com os elementos em ordem reversa (sem utilizar o método nativo `.reverse()`).
3. `multiplicarVetor(lista, multiplicador)`:
   - Retorna um novo array onde cada número foi multiplicado pelo fator informado.

---

## Solução de Referência

```javascript
// 1. Filtrar números pares em um novo array
function filtrarNumerosPares(lista) {
  const pares = [];

  for (const numero of lista) {
    if (numero % 2 === 0) {
      pares.push(numero);
    }
  }

  return pares;
}

// 2. Inverter array manualmente com laço for regressivo
function inverterArray(lista) {
  const invertido = [];

  for (let i = lista.length - 1; i >= 0; i--) {
    invertido.push(lista[i]);
  }

  return invertido;
}

// 3. Multiplicação elemento a elemento
function multiplicarVetor(lista, multiplicador) {
  const transformado = [];

  for (const item of lista) {
    transformado.push(item * multiplicador);
  }

  return transformado;
}

// Testes:
const dadosOriginais = [1, 2, 3, 4, 5, 6];

console.log("Apenas Pares:", filtrarNumerosPares(dadosOriginais)); // [2, 4, 6]
console.log("Invertido:", inverterArray(dadosOriginais));         // [6, 5, 4, 3, 2, 1]
console.log("Dobrados (x2):", multiplicarVetor(dadosOriginais, 2)); // [2, 4, 6, 8, 10, 12]
```
