# FE02-48 — Atividade: Funções com Arrays

## Objetivo da Atividade

Desenvolver funções reutilizáveis que recebem arrays como parâmetros e realizam operações de transformação, agregação e estatística matemática.

---

## Enunciado do Desafio

Crie três funções utilitárias para processamento de listas numéricas:

1. `somarElementos(numeros)`:
   - Recebe um array de números e retorna a soma aritmética de todos os elementos.
2. `calcularMedia(numeros)`:
   - Reutiliza a função de soma para calcular e retornar a média aritmética dos valores do array.
3. `encontrarMaiorNumero(numeros)`:
   - Percorre o array e retorna o maior valor numérico encontrado (sem utilizar bibliotecas externas).

---

## Solução de Referência

```javascript
// 1. Função de soma de elementos de um array
function somarElementos(numeros) {
  let soma = 0;
  for (const n of numeros) {
    soma += n;
  }
  return soma;
}

// 2. Função de cálculo de média reaproveitando a soma
function calcularMedia(numeros) {
  if (numeros.length === 0) {
    return 0;
  }
  const total = somarElementos(numeros);
  return total / numeros.length;
}

// 3. Função para encontrar o maior número manualmente
function encontrarMaiorNumero(numeros) {
  if (numeros.length === 0) {
    return null;
  }

  // Define o primeiro elemento como referência inicial:
  let maior = numeros[0];

  for (let i = 1; i < numeros.length; i++) {
    if (numeros[i] > maior) {
      maior = numeros[i];
    }
  }

  return maior;
}

// Testes práticos:
const listaValores = [14, 28, 45, 9, 72, 33];

console.log("Valores da lista:", listaValores);
console.log("Soma total:", somarElementos(listaValores));      // 201
console.log("Média aritmética:", calcularMedia(listaValores)); // 33.5
console.log("Maior valor:", encontrarMaiorNumero(listaValores)); // 72
```
