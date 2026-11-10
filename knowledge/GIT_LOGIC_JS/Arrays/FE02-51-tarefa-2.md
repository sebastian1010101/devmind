# FE02-51 — Tarefa 2

## Objetivo da Tarefa

Desenvolver um algoritmo de controle de fluxo de caixa e balanço contábil mensal a partir de um histórico de lançamentos financeiros representados em um array.

---

## Enunciado do Desafio

Crie uma função `calcularBalancoFinanceiro(lancamentos)` que receba uma lista de valores monetários:
- Números **positivos** representam receitas / entradas financeiras (ex: `+1500`, `+800`).
- Números **negativos** representam despesas / saídas financeiras (ex: `-250`, `-120`).

A função deve percorrer a lista uma única vez e retornar um relatório contendo:
1. Total acumulado de **Receitas**.
2. Total acumulado de **Despesas** (em valor absoluto positivo).
3. **Saldo Final Líquido** (`Receitas - Despesas`).
4. **Situação da Empresa:** `"Superávit (Lucro)"` se saldo > 0, `"Déficit (Prejuízo)"` se saldo < 0 ou `"Equilíbrio"` se for zero.

---

## Solução de Referência

```javascript
function calcularBalancoFinanceiro(lancamentos) {
  let totalReceitas = 0;
  let totalDespesas = 0;

  for (const valor of lancamentos) {
    if (valor > 0) {
      totalReceitas += valor;
    } else {
      // Converte o valor negativo para positivo na soma das despesas:
      totalDespesas += Math.abs(valor);
    }
  }

  const saldoLiquido = totalReceitas - totalDespesas;
  let statusEmpresa = "Equilíbrio";

  if (saldoLiquido > 0) {
    statusEmpresa = "Superávit (Lucro)";
  } else if (saldoLiquido < 0) {
    statusEmpresa = "Déficit (Prejuízo)";
  }

  return {
    receitas: Number(totalReceitas.toFixed(2)),
    despesas: Number(totalDespesas.toFixed(2)),
    saldo: Number(saldoLiquido.toFixed(2)),
    status: statusEmpresa
  };
}

// Teste com movimentação bancária:
const extratoMes = [5000, -1200, -450, 800, -2100, -350];
const relatorio = calcularBalancoFinanceiro(extratoMes);

console.log("=== RELATÓRIO FINANCEIRO CONSOLIDADO ===");
console.log(`(+) Total de Entradas: R$ ${relatorio.receitas}`);
console.log(`(-) Total de Saídas  : R$ ${relatorio.despesas}`);
console.log(`(=) Saldo Líquido    : R$ ${relatorio.saldo}`);
console.log(`Situação Contábil    : ${relatorio.status}`);
```
