# FE02-28 — Reutilizando Funções

## Composição de Funções

Um dos princípios mais importantes da programação estruturada e funcional é a **composição**: criar funções pequenas, focadas em fazer uma única coisa muito bem (*Princípio da Responsabilidade Única*), e combiná-las para resolver tarefas maiores.

---

## O Problema das Funções Gigantes ("God Functions")

Quando uma única função tenta validar os dados do usuário, calcular descontos, aplicar impostos, gerar um PDF e enviar um e-mail tudo de uma vez:

- O código se torna confuso e frágil.
- Se o cálculo do imposto mudar, você é obrigado a alterar toda a função de checkout.
- Torna-se quase impossível criar testes automatizados isolados.

---

## Exemplo de Arquitetura Modular

Podemos dividir o fluxo de fechamento de carrinho de compras em três funções reutilizáveis:

```javascript
// 1. Função focada apenas em calcular porcentagem de desconto
function calcularDesconto(valor, cupom) {
  if (cupom === "KENZIE10") {
    return valor * 0.10;
  }
  if (cupom === "KENZIE20") {
    return valor * 0.20;
  }
  return 0;
}

// 2. Função focada apenas em calcular taxa de frete por região
function calcularFrete(estado) {
  if (estado === "PR" || estado === "SP") {
    return 15.00;
  }
  return 30.00;
}

// 3. Função orquestradora que reutiliza as anteriores
function processarPedido(valorProdutos, cupom, estadoDestino) {
  const desconto = calcularDesconto(valorProdutos, cupom);
  const valorComDesconto = valorProdutos - desconto;
  const frete = calcularFrete(estadoDestino);

  const totalPagar = valorComDesconto + frete;

  return {
    subtotal: valorProdutos,
    descontoAplicado: desconto,
    valorFrete: frete,
    totalFinal: totalPagar
  };
}

console.log(processarPedido(500, "KENZIE10", "PR"));
// Subtotal: 500, Desconto: 50, Frete: 15, Total: 465
```
