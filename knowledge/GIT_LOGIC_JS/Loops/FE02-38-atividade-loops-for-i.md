# FE02-38 — Atividade: Loops for I

## Objetivo da Atividade

Praticar a sintaxe fundamental do laço `for` com contagens progressivas, regressivas e cálculos de tabuada básica.

---

## Enunciado do Desafio

Crie três funções independentes utilizando loops `for`:

1. `imprimirIntervalo(inicio, fim)`:
   - Recebe dois números inteiros e imprime todos os valores no intervalo inclusivo, um por linha.
2. `fazerContagemRegressiva(numeroInicial)`:
   - Imprime os números de `numeroInicial` até 0 no console e encerra com a mensagem `"Fim da contagem!"`.
3. `gerarTabuada(numero)`:
   - Recebe um número inteiro e imprime a tabuada completa de 1 a 10 no formato: `numero x i = resultado`.

---

## Solução de Referência

```javascript
// 1. Função de intervalo numérico
function imprimirIntervalo(inicio, fim) {
  console.log(`=== INTERVALO DE ${inicio} ATÉ ${fim} ===`);
  for (let i = inicio; i <= fim; i++) {
    console.log(i);
  }
}

// 2. Função de contagem regressiva
function fazerContagemRegressiva(numeroInicial) {
  console.log(`\n=== CONTAGEM REGRESSIVA A PARTIR DE ${numeroInicial} ===`);
  for (let i = numeroInicial; i >= 0; i--) {
    console.log(i);
  }
  console.log("Fim da contagem!");
}

// 3. Função de tabuada
function gerarTabuada(numero) {
  console.log(`\n=== TABUADA DO ${numero} ===`);
  for (let i = 1; i <= 10; i++) {
    const resultado = numero * i;
    console.log(`${numero} x ${i} = ${resultado}`);
  }
}

// Testes:
imprimirIntervalo(5, 9);
fazerContagemRegressiva(3);
gerarTabuada(7);
```
