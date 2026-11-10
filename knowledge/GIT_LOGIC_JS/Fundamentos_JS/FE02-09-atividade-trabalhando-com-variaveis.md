# FE02-09 — Atividade: Trabalhando com Variáveis

## Objetivo da Atividade

Praticar a declaração de variáveis com `const` e `let`, atribuição de diferentes tipos de dados primitivos (`string`, `number`, `boolean`) e exibição de dados combinados no console do navegador através de `console.log()`.

---

## Enunciado do Desafio

Crie um arquivo chamado `variaveis.js` para gerenciar a ficha cadastral de um produto em um sistema de comércio eletrônico, cumprindo as seguintes etapas:

1. Crie uma constante para o **nome do produto** (`"Teclado Mecânico RGB"`).
2. Crie uma constante para a **categoria** do produto (`"Periféricos"`).
3. Crie uma variável `let` para o **preço unitário** do produto (`250.00`).
4. Crie uma variável `let` para o **estoque disponível** (`15`).
5. Crie uma constante booleana indicando se o produto está **ativo para venda** (`true`).
6. Imprima no console uma mensagem de apresentação inicial da ficha técnica do produto.
7. Simule uma venda de 2 unidades: atualize o estoque e dê um desconto de 10% no preço unitário.
8. Imprima no console o novo estado dos dados atualizados.

---

## Solução de Referência

```javascript
// 1. Declaração dos dados iniciais do produto
const nomeProduto = "Teclado Mecânico RGB";
const categoria = "Periféricos";
let precoUnitario = 250.00;
let quantidadeEstoque = 15;
const emEstoque = true;

// 2. Exibição da ficha inicial
console.log("=== FICHA TÉCNICA DO PRODUTO ===");
console.log("Produto:", nomeProduto);
console.log("Categoria:", categoria);
console.log("Preço Inicial: R$", precoUnitario);
console.log("Estoque Atual:", quantidadeEstoque);
console.log("Disponível para venda?", emEstoque);

// 3. Simulação de atualização de dados (venda e desconto)
quantidadeEstoque = quantidadeEstoque - 2; // Venda de 2 unidades
precoUnitario = precoUnitario * 0.90;      // 10% de desconto aplicado

// 4. Exibição dos dados pós-atualização
console.log("\n=== ATUALIZAÇÃO APÓS PROMOÇÃO E VENDA ===");
console.log("Novo Estoque:", quantidadeEstoque);
console.log("Novo Preço Promocional: R$", precoUnitario);
```
