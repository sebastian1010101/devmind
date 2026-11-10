# FE02-29 — Atividade: Reutilizando Funções

## Objetivo da Atividade

Praticar a decomposição de um sistema de folha de pagamento em funções modulares independentes, reaproveitando funções menores de cálculo percentual dentro de uma função orquestradora central.

---

## Enunciado do Desafio

Crie um módulo `folhaPagamento.js` que implemente as seguintes funções:

1. `calcularDescontoINSS(salarioBruto)`:
   - Se o salário for até R$ 2.000: desconta 7.5%.
   - Se for acima de R$ 2.000 até R$ 4.000: desconta 9%.
   - Se for acima de R$ 4.000: desconta 12%.
2. `calcularValeTransporte(salarioBruto)`:
   - Desconto padrão legal de 6% sobre o salário bruto.
3. `calcularSalarioLiquido(salarioBruto, bonusExtra)`:
   - Reutiliza as funções de INSS e Vale Transporte.
   - Adiciona o bônus financeiro ao total.
   - Retorna uma mensagem detalhada com o demonstrativo salarial final.

---

## Solução de Referência

```javascript
// 1. Função isolada para o INSS
function calcularDescontoINSS(salarioBruto) {
  if (salarioBruto <= 2000) {
    return salarioBruto * 0.075;
  } else if (salarioBruto <= 4000) {
    return salarioBruto * 0.09;
  } else {
    return salarioBruto * 0.12;
  }
}

// 2. Função isolada para o Vale Transporte
function calcularValeTransporte(salarioBruto) {
  return salarioBruto * 0.06;
}

// 3. Função orquestradora
function calcularSalarioLiquido(salarioBruto, bonusExtra = 0) {
  const descontoINSS = calcularDescontoINSS(salarioBruto);
  const descontoVT = calcularValeTransporte(salarioBruto);
  const totalDescontos = descontoINSS + descontoVT;

  const salarioLiquido = (salarioBruto - totalDescontos) + bonusExtra;

  return `
=== DEMONSTRATIVO DE PAGAMENTO ===
Salário Bruto   : R$ ${salarioBruto.toFixed(2)}
Bônus Recebido  : R$ ${bonusExtra.toFixed(2)}
(-) Desconto INSS: R$ ${descontoINSS.toFixed(2)}
(-) Desconto VT  : R$ ${descontoVT.toFixed(2)}
----------------------------------
Total Líquido   : R$ ${salarioLiquido.toFixed(2)}
==================================`;
}

// Teste do demonstrativo com salário de R$ 3.500 e bônus de R$ 300:
console.log(calcularSalarioLiquido(3500, 300));
```
