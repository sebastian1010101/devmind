# FE02-21 — Sintaxe e Declaração de Funções

## Formas de Declarar Funções no JavaScript

Existem três maneiras principais de escrever funções na linguagem:

---

## 1. Declaração Tradicional (Function Declaration)

A forma clássica e mais comum:

```javascript
function somarValores(a, b) {
  return a + b;
}
```

### O Comportamento do Hoisting (Içamento)

Funções declaradas dessa forma sofrem **hoisting**: o motor do JavaScript move a declaração para o topo do arquivo em tempo de compilação. Isso significa que você pode invocar a função **antes** da linha em que ela foi escrita no código:

```javascript
// Funciona perfeitamente graças ao hoisting!
console.log(calcularDobro(4)); // 8

function calcularDobro(numero) {
  return numero * 2;
}
```

---

## 2. Expressão de Função (Function Expression)

A função é criada como uma função anônima e armazenada dentro de uma variável `const`:

```javascript
const multiplicar = function(x, y) {
  return x * y;
};

// Chamada normal:
console.log(multiplicar(3, 4)); // 12
```

- **Sem Hoisting:** a função não pode ser chamada antes da linha da sua atribuição.

---

## 3. Funções de Seta (Arrow Functions — ES6+)

A sintaxe moderna e enxuta introduzida no ECMAScript 2015, utilizando o operador `=>`:

```javascript
// Sintaxe completa com corpo de bloco:
const dividir = (a, b) => {
  return a / b;
};

// Sintaxe reduzida com retorno implícito (uma única expressão):
const calcularTriplo = n => n * 3;

console.log(calcularTriplo(5)); // 15
```
