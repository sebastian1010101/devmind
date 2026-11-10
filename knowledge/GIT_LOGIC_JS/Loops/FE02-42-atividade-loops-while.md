# FE02-42 — Atividade: Loops while

## Objetivo da Atividade

Praticar a aplicação de laços `while` em problemas onde o encerramento da repetição depende de condições dinâmicas e acumulativas.

---

## Enunciado do Desafio 1: Jogo da Adivinhação de Números

Crie uma função `simularAdivinhacao(numeroSecreto)` que simula uma sequência de palpites gerados aleatoriamente pelo computador até acertar o `numeroSecreto` (entre 1 e 20).

- O loop deve continuar rodando enquanto o palpite for diferente do número secreto.
- A cada tentativa incorreta, incremente um contador de tentativas.
- Ao acertar, encerre o laço e exiba quantas tentativas foram necessárias.

---

## Enunciado do Desafio 2: Meta de Poupança Financeira

Crie uma função `calcularMesesParaMeta(metaFinanceira, depositoMensal, rendimentoMensal)` que:

- Inicia com saldo de R$ 0,00.
- A cada mês (iteração), adiciona o rendimento sobre o saldo existente e soma o novo depósito mensal.
- Repete enquanto o saldo acumulado for estritamente menor que a meta financeira estabelecida.
- Retorna quantos meses foram necessários e o saldo final atingido.

---

## Solução de Referência

```javascript
// 1. Simulação de Jogo da Adivinhação
function simularAdivinhacao(numeroSecreto) {
  let palpite = 0;
  let tentativas = 0;

  console.log(`[JOGO] Procurando o número secreto: ${numeroSecreto}...`);

  while (palpite !== numeroSecreto) {
    tentativas++;
    // Gera um número inteiro pseudo-aleatório entre 1 e 20:
    palpite = Math.floor(Math.random() * 20) + 1;
  }

  console.log(`[SUCESSO] O número ${numeroSecreto} foi encontrado após ${tentativas} tentativa(s)!`);
}

// 2. Cálculo de Meta Financeira
function calcularMesesParaMeta(metaFinanceira, depositoMensal, taxaRendimentoMensal = 0.008) {
  let saldoAtual = 0;
  let meses = 0;

  while (saldoAtual < metaFinanceira) {
    meses++;
    saldoAtual += (saldoAtual * taxaRendimentoMensal); // Aplica juros compostos mensais
    saldoAtual += depositoMensal;                       // Adiciona o novo aporte
  }

  return {
    mesesNecessarios: meses,
    saldoFinal: Number(saldoAtual.toFixed(2))
  };
}

// Testes práticos:
simularAdivinhacao(14);

const resultadoMeta = calcularMesesParaMeta(10000, 500); // Guardando R$ 500/mês para juntar R$ 10.000
console.log(`Meta de R$ 10.000 atingida em ${resultadoMeta.mesesNecessarios} meses com saldo final de R$ ${resultadoMeta.saldoFinal}.`);
```
