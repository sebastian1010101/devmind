# FE03-49 — Escopo de Bloco

## O Fim dos Problemas do `var` com `let` e `const`

Antes do ES6, o JavaScript possuía apenas dois níveis de escopo: **Global** e **Escopo de Função**. O conceito de escopo de bloco não existia para variáveis declaradas com `var`.

---

## O que é Escopo de Bloco?

Um bloco é qualquer seção de código delimitada por um par de chaves `{}`:
- O corpo de uma estrutura `if` ou `else`.
- O corpo de um laço `for` ou `while`.
- Um bloco de código avulso `{ ... }`.

Variáveis declaradas com **`let`** e **`const`** possuem **Escopo de Bloco**: elas nascem no momento da declaração e são destruídas assim que a execução atinge a chave de fechamento `}` do bloco.

```javascript
if (true) {
  const mensagem = "Segredo interno do bloco";
  let contador = 42;
}

console.log(mensagem); // ReferenceError: mensagem is not defined!
console.log(contador); // ReferenceError: contador is not defined!
```

---

## O Problema Clássico do `var` em Laços `for`

Com `var`, a variável do contador vaza para fora do loop e compartilha a mesma referência de memória em todas as voltas, gerando bugs graves em temporizadores assíncronos:

```javascript
// BUG HISTÓRICO COM VAR:
for (var i = 1; i <= 3; i++) {
  setTimeout(() => {
    console.log("Com var:", i); // Imprime: 4, 4, 4!
  }, 100);
}

// RESOLUÇÃO PERFEITA COM LET NO ES6:
for (let j = 1; j <= 3; j++) {
  setTimeout(() => {
    console.log("Com let:", j); // Imprime corretamente: 1, 2, 3!
  }, 100);
}
```

- Com `let`, o JavaScript cria uma **nova ligação de escopo isolada a cada iteração** do loop, preservando o valor correto para closures e funções assíncronas.
