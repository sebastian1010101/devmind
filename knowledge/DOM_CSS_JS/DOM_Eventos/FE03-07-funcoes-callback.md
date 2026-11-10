# FE03-07 — Funções Callback

## O que é uma Função Callback?

Uma **função callback** é uma função que é **passada como argumento para outra função**, para ser invocada (*chamada de volta*) em um momento posterior, após a ocorrência de determinado evento ou conclusão de uma rotina assíncrona.

No JavaScript, funções são "cidadãos de primeira classe" (*First-Class Citizens*), o que significa que podem ser tratadas como qualquer outro valor (armazenadas em variáveis, passadas como parâmetros e retornadas por outras funções).

---

## Estrutura Básica de uma Callback

```javascript
// 1. Função que recebe outra função como parâmetro
function processarUsuario(nome, callback) {
  console.log(`Processando cadastro de ${nome}...`);
  // Chama a função passada:
  callback(nome);
}

// 2. Função de callback
function notificarSucesso(nome) {
  console.log(`Notificação: ${nome} cadastrado com sucesso!`);
}

// 3. Passando a função sem parênteses (como referência):
processarUsuario("Sebastián", notificarSucesso);
```

> **Atenção:** Ao passar uma callback, nunca coloque parênteses `()` no nome da função (ex: `notificarSucesso`, e não `notificarSucesso()`), caso contrário ela será executada imediatamente em vez de esperar o momento certo.

---

## Callbacks com Funções Anônimas e Arrow Functions

É extremamente comum passar a função diretamente no próprio local da chamada:

```javascript
processarUsuario("Mariana", (nome) => {
  console.log(`E-mail de boas-vindas enviado para ${nome}.`);
});
```

---

## Onde Callbacks são Essenciais?

1. **Manipuladores de Eventos:** `botao.addEventListener("click", callback)`.
2. **Temporizadores:** `setTimeout(callback, 2000)` e `setInterval(callback, 1000)`.
3. **Métodos de Iteração de Arrays:** `.forEach()`, `.map()`, `.filter()`, `.reduce()`.
