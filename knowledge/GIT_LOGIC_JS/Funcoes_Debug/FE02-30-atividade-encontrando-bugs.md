# FE02-30 — Atividade: Encontrando Bugs

## Objetivo da Atividade

Desenvolver o olhar crítico para identificar, diagnosticar e corrigir **erros de sintaxe, escopo, coerção de tipos e ausência de retornos** em códigos JavaScript propostos.

---

## Enunciado do Desafio

Analise os três trechos de código com falhas abaixo, identifique a causa de cada bug e escreva a versão corrigida:

---

## Bug 1: A Concatenação Acidental de Números

```javascript
// Código com Erro:
function somarValores(a, b) {
  return a + b;
}

const n1 = "20";
const n2 = 10;
console.log(somarValores(n1, n2)); // Imprime "2010" em vez de 30!
```

### Diagnóstico e Solução 1

O argumento `n1` é uma String. No JavaScript, o operador `+` com uma string realiza concatenação textual em vez de soma aritmética.

```javascript
// Código Corrigido:
function somarValores(a, b) {
  return Number(a) + Number(b);
}
console.log(somarValores(n1, n2)); // 30
```

---

## Bug 2: A Variável Inacessível por Escopo

```javascript
// Código com Erro:
function calcularDesconto(preco) {
  if (preco > 100) {
    const desconto = preco * 0.10;
  }
  return preco - desconto; // ReferenceError: desconto is not defined!
}
```

### Diagnóstico e Solução 2

A constante `desconto` foi declarada dentro do bloco `{}` do `if`. Por ter escopo de bloco, ela é destruída ao sair do `if` e não pode ser lida na linha do `return`.

```javascript
// Código Corrigido:
function calcularDesconto(preco) {
  let desconto = 0; // Declarada no escopo da função
  if (preco > 100) {
    desconto = preco * 0.10;
  }
  return preco - desconto;
}
```

---

## Bug 3: A Função que "Esqueceu" de Devolver o Resultado

```javascript
// Código com Erro:
function gerarMensagem(usuario) {
  const mensagem = `Bem-vindo, ${usuario}!`;
}

const resultado = gerarMensagem("Carlos");
console.log(resultado); // undefined!
```

### Diagnóstico e Solução 3

A função calcula a string, mas não possui a palavra-chave `return`. Sem ela, qualquer função devolve `undefined`.

```javascript
// Código Corrigido:
function gerarMensagem(usuario) {
  return `Bem-vindo, ${usuario}!`;
}
```
