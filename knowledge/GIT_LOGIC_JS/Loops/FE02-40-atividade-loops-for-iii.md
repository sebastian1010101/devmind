# FE02-40 — Atividade: Loops for III

## Objetivo da Atividade

Resolver problemas matemáticos clássicos de lógica: cálculo de fatorial e identificação de números primos com laços `for` e interrupção controlada via `break`.

---

## Enunciado do Desafio

Implemente as seguintes funções:

1. `calcularFatorial(n)`:
   - O fatorial de um número natural é a multiplicação cumulativa de todos os inteiros positivos menores ou iguais a ele (ex: `5! = 5 * 4 * 3 * 2 * 1 = 120`).
   - Por definição matemática, `0! = 1` e `1! = 1`.
2. `ehPrimo(numero)`:
   - Um número primo é aquele maior que 1 divisível exclusivamente por 1 e por ele mesmo.
   - Retorne `true` se for primo e `false` se não for, otimizando o laço para interromper com `break` assim que encontrar qualquer divisor exato.

---

## Solução de Referência

```javascript
// 1. Cálculo de Fatorial
function calcularFatorial(n) {
  if (n < 0) {
    return "Erro: fatorial não definido para números negativos.";
  }

  let resultado = 1;
  for (let i = n; i >= 2; i--) {
    resultado *= i;
  }

  return resultado;
}

// 2. Verificação de Número Primo
function ehPrimo(numero) {
  if (numero <= 1) {
    return false; // Números menores ou iguais a 1 não são primos
  }

  let primo = true;

  // Testa divisores a partir de 2 até a raiz quadrada ou metade do número
  for (let divisor = 2; divisor < numero; divisor++) {
    if (numero % divisor === 0) {
      primo = false;
      break; // Encontrou um divisor exato: não é primo, interrompe imediatamente!
    }
  }

  return primo;
}

// Testes:
console.log("5! =", calcularFatorial(5)); // 120
console.log("0! =", calcularFatorial(0)); // 1
console.log("7 é primo?", ehPrimo(7));   // true
console.log("12 é primo?", ehPrimo(12)); // false
console.log("23 é primo?", ehPrimo(23)); // true
```
