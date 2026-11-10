# FE03-08 — Atividade: Criando uma Callback para uma Função

## Objetivo da Atividade

Desenvolver uma função de ordem superior (*Higher-Order Function*) que recebe dados e uma função de callback para aplicar diferentes operações matemáticas personalizadas sobre dois números.

---

## Enunciado do Desafio

Construa uma calculadora genérica baseada em callbacks:

1. Crie a função principal `calcular(num1, num2, operacaoCallback)`.
2. Implemente quatro funções de operação independentes:
   - `somar(a, b)`
   - `subtrair(a, b)`
   - `multiplicar(a, b)`
   - `dividir(a, b)` (com validação para divisão por zero).
3. Execute testes demonstrando a flexibilidade da arquitetura ao passar tanto as funções nomeadas quanto callbacks anônimas em Arrow Function.

---

## Solução de Referência

```javascript
// 1. Função de Ordem Superior
function calcular(num1, num2, operacaoCallback) {
  console.log(`[LOG] Executando cálculo com os valores: ${num1} e ${num2}`);
  return operacaoCallback(num1, num2);
}

// 2. Funções de Callback Especializadas
function somar(a, b) {
  return a + b;
}

function subtrair(a, b) {
  return a - b;
}

function multiplicar(a, b) {
  return a * b;
}

function dividir(a, b) {
  if (b === 0) {
    return "Erro: divisão por zero não permitida.";
  }
  return a / b;
}

// 3. Testes práticos com callbacks nomeadas
console.log("Soma         :", calcular(10, 5, somar));       // 15
console.log("Subtração    :", calcular(10, 5, subtrair));    // 5
console.log("Multiplicação:", calcular(10, 5, multiplicar)); // 50
console.log("Divisão      :", calcular(10, 5, dividir));     // 2

// 4. Teste com Arrow Function inline personalizada (Média):
const media = calcular(10, 20, (x, y) => (x + y) / 2);
console.log("Média inline :", media); // 15
```
