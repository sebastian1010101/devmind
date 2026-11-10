# FE02-55 — Métodos de um Objeto

## O que é um Método?

Quando uma função é declarada como uma propriedade interna de um objeto, ela é chamada de **método**. Métodos representam as **ações e comportamentos** que aquela entidade é capaz de realizar sobre seus próprios dados.

---

## A Palavra-Chave `this`

Dentro de um método tradicional de um objeto, a palavra-chave especial `this` faz referência ao **próprio objeto que está executando o método**.

```javascript
const contaBancaria = {
  titular: "Sebastián Gomez",
  saldo: 1500.00,

  // Método tradicional:
  depositar(valor) {
    this.saldo += valor;
    console.log(`Depósito de R$ ${valor} concluído. Novo saldo: R$ ${this.saldo}`);
  },

  sacar(valor) {
    if (valor > this.saldo) {
      console.log("Operação recusada: saldo insuficiente.");
      return;
    }
    this.saldo -= valor;
    console.log(`Saque de R$ ${valor} efetuado. Saldo restante: R$ ${this.saldo}`);
  },

  exibirExtrato() {
    return `Conta de ${this.titular} — Saldo Disponível: R$ ${this.saldo.toFixed(2)}`;
  }
};

// Invocação dos métodos:
contaBancaria.depositar(500); // Saldo: 2000
contaBancaria.sacar(300);     // Saldo: 1700
console.log(contaBancaria.exibirExtrato());
```

---

## Cuidado com Arrow Functions como Métodos!

**Arrow functions NÃO possuem seu próprio `this`**. Elas herdam o `this` do escopo exterior onde foram criadas (geralmente o objeto global `window` no navegador ou módulo vazio no Node).

```javascript
const pessoa = {
  nome: "Ana",

  // PERIGO: 'this.nome' será undefined!
  saudarIncorreto: () => {
    console.log(`Olá, meu nome é ${this.nome}`);
  },

  // CORRETO: sintaxe de método nativo
  saudarCorreto() {
    console.log(`Olá, meu nome é ${this.nome}`);
  }
};

pessoa.saudarCorreto(); // "Olá, meu nome é Ana"
```
