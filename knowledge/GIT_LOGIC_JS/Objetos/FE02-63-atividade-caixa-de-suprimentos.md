# FE02-63 — Atividade: Caixa de Suprimentos

## Objetivo da Atividade

Gerenciar o inventário e consumo de insumos de um escritório, aplicando objetos como dicionários de mapeamento e arrays para rastrear itens com estoque crítico.

---

## Enunciado do Desafio

Crie um sistema para uma `caixaDeSuprimentos` com as seguintes funcionalidades:

1. O estoque é armazenado em um objeto onde cada chave é o nome do suprimento e o valor é a quantidade em unidades:
   ```javascript
   const estoque = { papelA4: 12, canetas: 25, clips: 50, cafe: 4 };
   ```
2. Crie uma função `consumirItem(item, quantidade)`:
   - Se o item não existir na caixa, informe que o produto não é gerenciado.
   - Se a quantidade solicitada for maior que o estoque disponível, recuse a operação por insuficiência de material.
   - Caso contrário, deduza do estoque e retorne a nova quantidade restante.
3. Crie uma função `verificarItensCriticos(limiteMinimo)`:
   - Percorre todos os itens e retorna um array com o nome dos suprimentos que estão abaixo do limite mínimo recomendado.

---

## Solução de Referência

```javascript
const caixaDeSuprimentos = {
  papelA4: 12,
  canetas: 25,
  clips: 50,
  cafe: 4,

  consumirItem(item, quantidade) {
    if (!(item in this)) {
      return `Erro: o item "${item}" não existe no almoxarifado.`;
    }

    if (this[item] < quantidade) {
      return `Estoque insuficiente de "${item}". Disponível: ${this[item]}, Solicitado: ${quantidade}.`;
    }

    this[item] -= quantidade;
    return `Retirada de ${quantidade} unidade(s) de "${item}" efetuada. Restam: ${this[item]}.`;
  },

  verificarItensCriticos(limiteMinimo = 10) {
    const reposicaoUrgente = [];

    for (const item in this) {
      // Ignora métodos internos do objeto:
      if (typeof this[item] === "number" && this[item] < limiteMinimo) {
        reposicaoUrgente.push({ item, quantidadeAtual: this[item] });
      }
    }

    return reposicaoUrgente;
  }
};

// Testes de consumo e estoque:
console.log(caixaDeSuprimentos.consumirItem("cafe", 2));
console.log(caixaDeSuprimentos.consumirItem("canetas", 30)); // Insuficiente
console.log(caixaDeSuprimentos.consumirItem("canetas", 20)); // Restam 5
console.log("\nItens com estoque crítico abaixo de 10 unidades:", caixaDeSuprimentos.verificarItensCriticos(10));
```
