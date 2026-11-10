# FE02-62 — Atividade: Loops, Funções e Arrays

## Objetivo da Atividade

Integrar funções puras, laços de repetição e vetores para solucionar um problema de agregação e contagem de votos em uma eleição corporativa.

---

## Enunciado do Desafio

Crie uma função chamada `apurarEleicao(votos)` que:

1. Recebe um array contendo os nomes dos candidatos votados em cada cédula:
   ```javascript
   const urnaEletronica = ["Ana", "Carlos", "Ana", "Beatriz", "Carlos", "Ana", "Beatriz", "Ana"];
   ```
2. Percorre a lista e totaliza os votos recebidos por cada candidato dinamicamente.
3. Determina quem é o candidato vencedor (aquele com a maior contagem de votos).
4. Retorna um objeto consolidado contendo a tabela de apuração e o nome do candidato vencedor.

---

## Solução de Referência

```javascript
function apurarEleicao(votos) {
  const contagem = {};

  // 1. Contagem acumulativa de votos
  for (const candidato of votos) {
    if (contagem[candidato]) {
      contagem[candidato]++;
    } else {
      contagem[candidato] = 1;
    }
  }

  // 2. Determinação do vencedor
  let vencedor = "";
  let maiorVotacao = 0;

  for (const candidato in contagem) {
    if (contagem[candidato] > maiorVotacao) {
      maiorVotacao = contagem[candidato];
      vencedor = candidato;
    }
  }

  return {
    apuracaoGeral: contagem,
    candidatoEleito: vencedor,
    votosDoVencedor: maiorVotacao
  };
}

// Teste de apuração da urna:
const votosUrna = ["Ana", "Carlos", "Ana", "Beatriz", "Carlos", "Ana", "Beatriz", "Ana"];
const resultadoFinal = apurarEleicao(votosUrna);

console.log("=== APURAÇÃO FINAL DA ELEIÇÃO ===");
console.log("Distribuição de Votos:", resultadoFinal.apuracaoGeral);
console.log(`Candidato Vencedor   : ${resultadoFinal.candidatoEleito}`);
console.log(`Total de Votos       : ${resultadoFinal.votosDoVencedor}`);
```
