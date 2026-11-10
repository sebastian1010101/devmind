# FE02-39 — Atividade: Loops for II

## Objetivo da Atividade

Evoluir o uso de laços `for` integrando acumuladores de valores e filtros condicionais (`if`) dentro do corpo da repetição.

---

## Enunciado do Desafio

Crie um módulo com as seguintes soluções algorítmicas:

1. `somarAte(limite)`:
   - Utiliza uma variável acumuladora para somar todos os números inteiros de 1 até `limite` (ex: se `limite` for 5, calcula: `1 + 2 + 3 + 4 + 5 = 15`).
   - Retorna o total somado.
2. `filtrarPares(inicio, fim)`:
   - Percorre o intervalo e imprime no console apenas os números que forem estritamente pares (`numero % 2 === 0`).
3. `contarMultiplos(inicio, fim, divisor)`:
   - Conta e retorna quantos números dentro do intervalo são múltiplos exatos de `divisor`.

---

## Solução de Referência

```javascript
// 1. Acumulador de soma sequencial
function somarAte(limite) {
  let somaTotal = 0; // Variável acumuladora

  for (let i = 1; i <= limite; i++) {
    somaTotal += i;
  }

  return somaTotal;
}

// 2. Filtro de números pares com operador módulo
function filtrarPares(inicio, fim) {
  console.log(`Pares entre ${inicio} e ${fim}:`);
  for (let i = inicio; i <= fim; i++) {
    if (i % 2 === 0) {
      console.log(`Par encontrado: ${i}`);
    }
  }
}

// 3. Contador de múltiplos
function contarMultiplos(inicio, fim, divisor) {
  let quantidade = 0;

  for (let i = inicio; i <= fim; i++) {
    if (i % divisor === 0) {
      quantidade++;
    }
  }

  return quantidade;
}

// Testes:
console.log("Soma de 1 a 100:", somarAte(100)); // 5050
filtrarPares(10, 18);
console.log("Quantidade de múltiplos de 3 entre 1 e 30:", contarMultiplos(1, 30, 3)); // 10
```
