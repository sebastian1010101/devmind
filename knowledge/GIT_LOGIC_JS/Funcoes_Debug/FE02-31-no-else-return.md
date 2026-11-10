# FE02-31 — no-else-return

## O Conceito de `no-else-return`

O padrão **`no-else-return`** (frequentemente aplicado por linters como o ESLint) é uma regra de estilo e refatoração de código que estabelece:

> Se um bloco `if` contém uma instrução `return`, o bloco `else` ou `else if` seguinte torna-se **completamente desnecessário e redundante**.

---

## Por que o `else` é Redundante?

Como a palavra-chave `return` encerra e sai da função imediatamente, o código localizado abaixo do `if` só será alcançado se a condição do `if` for falsa. Portanto, envolver o restante do código dentro de um `else` apenas adiciona aninhamento e poluição visual desnecessários.

---

## Comparação Prática

### 1. Código com `else` Redundante (Evitar)

```javascript
function verificarParidade(numero) {
  if (numero % 2 === 0) {
    return "Par";
  } else {
    return "Ímpar"; // O 'else' é inútil aqui!
  }
}
```

### 2. Código Refatorado com `no-else-return` (Limpo e Idiomático)

```javascript
function verificarParidade(numero) {
  if (numero % 2 === 0) {
    return "Par";
  }

  return "Ímpar";
}
```

---

## O Padrão Guard Clauses (Cláusulas de Guarda)

Essa técnica permite tratar casos de erro, entradas inválidas ou exceções logo no início da função, "guardando" a lógica principal sem aninhamentos profundos (*Arrow Anti-Pattern*):

```javascript
// Função com Cláusulas de Guarda limpas
function processarTransferencia(saldo, valor, contaAtiva) {
  if (!contaAtiva) {
    return "Erro: a conta de origem está inativa.";
  }

  if (valor <= 0) {
    return "Erro: o valor a transferir deve ser positivo.";
  }

  if (saldo < valor) {
    return "Erro: saldo insuficiente para a operação.";
  }

  // Caminho feliz principal executado sem nenhum if/else aninhado:
  const novoSaldo = saldo - valor;
  return `Transferência de R$ ${valor} realizada com sucesso. Novo saldo: R$ ${novoSaldo}`;
}
```
