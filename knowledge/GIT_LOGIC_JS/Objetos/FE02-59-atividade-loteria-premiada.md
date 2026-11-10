# FE02-59 — Atividade: Loteria Premiada

## Objetivo da Atividade

Praticar algoritmos de conferência cruzada entre dados de bilhetes de loteria (arrays de números) e regras de premiação em dinheiro armazenadas em objetos.

---

## Enunciado do Desafio

Crie uma função `conferirAposta(bilheteApostador, resultadoSorteio)` que:

1. O `bilheteApostador` é um objeto contendo o nome do apostador e sua lista de 6 dezenas escolhidas (ex: `{ apostador: "Carlos", dezenas: [4, 12, 18, 25, 33, 42] }`).
2. O `resultadoSorteio` é um array com as 6 dezenas sorteadas oficialmente (ex: `[4, 12, 18, 25, 33, 50]`).
3. Conte quantos acertos o apostador conseguiu.
4. Aplique a tabela de premiação:
   - 6 acertos: **Sena** &rarr; Prêmio: R$ 5.000.000,00
   - 5 acertos: **Quina** &rarr; Prêmio: R$ 40.000,00
   - 4 acertos: **Quadra** &rarr; Prêmio: R$ 1.000,00
   - Menos de 4 acertos: Não premiado &rarr; R$ 0,00
5. Retorne um relatório com nome, total de acertos e o valor do prêmio conquistado.

---

## Solução de Referência

```javascript
function conferirAposta(bilheteApostador, resultadoSorteio) {
  let acertos = 0;
  const dezenasSorteadas = [];

  // Conferência cruzada:
  for (const dezena of bilheteApostador.dezenas) {
    if (resultadoSorteio.includes(dezena)) {
      acertos++;
      dezenasSorteadas.push(dezena);
    }
  }

  let faixaPremio = "Não premiado";
  let valorPremio = 0;

  switch (acertos) {
    case 6:
      faixaPremio = "Sena (Prêmio Máximo)";
      valorPremio = 5000000.00;
      break;
    case 5:
      faixaPremio = "Quina";
      valorPremio = 40000.00;
      break;
    case 4:
      faixaPremio = "Quadra";
      valorPremio = 1000.00;
      break;
    default:
      faixaPremio = "Infelizmente não foi desta vez";
      valorPremio = 0;
  }

  return {
    apostador: bilheteApostador.apostador,
    totalAcertos: acertos,
    numerosAcertados: dezenasSorteadas,
    faixa: faixaPremio,
    premioRecebido: valorPremio
  };
}

// Teste de aposta com 5 acertos (Quina):
const meuBilhete = {
  apostador: "Sebastián Gomez",
  dezenas: [7, 14, 21, 35, 42, 56]
};

const dezenasOficiais = [7, 14, 21, 35, 42, 60];

const resultadoConferencia = conferirAposta(meuBilhete, dezenasOficiais);
console.log("=== RESULTADO DA LOTERIA ===");
console.log(`Apostador       : ${resultadoConferencia.apostador}`);
console.log(`Total de Acertos: ${resultadoConferencia.totalAcertos}`);
console.log(`Números Acertados: [${resultadoConferencia.numerosAcertados.join(", ")}]`);
console.log(`Faixa de Prêmio : ${resultadoConferencia.faixa}`);
console.log(`Valor a Receber : R$ ${resultadoConferencia.premioRecebido.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}`);
```
