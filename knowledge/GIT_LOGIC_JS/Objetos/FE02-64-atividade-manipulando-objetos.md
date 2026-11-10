# FE02-64 — Atividade: Manipulando Objetos

## Objetivo da Atividade

Dominar métodos utilitários estáticos nativos do JavaScript para inspeção e manipulação avançada de objetos: `Object.keys()`, `Object.values()` e `Object.entries()`.

---

## Os Três Métodos Estáticos de `Object`

| Método | O que Retorna? | Exemplo Prático |
| --- | --- | --- |
| `Object.keys(obj)` | Array com os nomes de todas as chaves | `["nome", "preco", "estoque"]` |
| `Object.values(obj)` | Array com todos os valores armazenados | `["Monitor", 1200, 5]` |
| `Object.entries(obj)` | Array de arrays com pares `[chave, valor]` | `[["nome", "Monitor"], ["preco", 1200]]` |

---

## Enunciado do Desafio

Dado o objeto de vendas de uma filial no primeiro trimestre:

```javascript
const faturamentoTrimestre = {
  janeiro: 45000,
  fevereiro: 38000,
  marco: 52000
};
```

1. Obtenha a lista dos meses faturados utilizando `Object.keys()`.
2. Calcule o faturamento total acumulado do trimestre somando os valores retornados por `Object.values()`.
3. Utilize `Object.entries()` e um laço `for...of` com desestruturação para imprimir um relatório linha a linha formatando cada mês com seu respectivo valor em moeda brasileira.

---

## Solução de Referência

```javascript
const faturamentoTrimestre = {
  janeiro: 45000,
  fevereiro: 38000,
  marco: 52000
};

// 1. Extração das chaves (meses)
const meses = Object.keys(faturamentoTrimestre);
console.log("Meses apurados:", meses); // ["janeiro", "fevereiro", "marco"]

// 2. Extração dos valores e cálculo do total
const faturamentos = Object.values(faturamentoTrimestre);
let faturamentoTotal = 0;

for (const valor of faturamentos) {
  faturamentoTotal += valor;
}

console.log(`Faturamento total acumulado: R$ ${faturamentoTotal.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}`);

// 3. Relatório linha a linha com Object.entries()
console.log("\n=== DEMONSTRATIVO DETALHADO POR MÊS ===");
for (const [mes, valor] of Object.entries(faturamentoTrimestre)) {
  const mesFormatado = mes[0].toUpperCase() + mes.slice(1);
  console.log(`${mesFormatado.padEnd(12)}: R$ ${valor.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}`);
}
```
