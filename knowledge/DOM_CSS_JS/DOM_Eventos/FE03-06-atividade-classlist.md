# FE03-06 — Atividade: classList

## Objetivo da Atividade

Praticar o uso de `classList.add()`, `classList.remove()`, `classList.toggle()` e `classList.contains()` para criar um alternador de Tema Claro / Tema Escuro (*Dark Mode Toggle*) e destacar itens selecionados em uma interface.

---

## Enunciado do Desafio

Construa as funções de manipulação de classes para uma aplicação web:

1. `alternarModoEscuro()`:
   - Seleciona o elemento `<body>`.
   - Utiliza `classList.toggle("dark-mode")` para alternar o tema.
   - Se o modo escuro estiver ativo, altera o texto do botão para `"Mudar para Tema Claro"`; caso contrário, define como `"Mudar para Tema Escuro"`.
2. `selecionarCard(cardClicado)`:
   - Dado um conjunto de cards (`.card-opcao`), quando um card for selecionado:
     - Remove a classe `.selecionado` de todos os outros cards da tela.
     - Adiciona a classe `.selecionado` exclusivamente ao card que recebeu o clique.

---

## Solução de Referência

```javascript
// 1. Função de alternância de tema
function alternarModoEscuro() {
  const corpo = document.body;
  const botaoTema = document.querySelector("#btn-tema");

  corpo.classList.toggle("dark-mode");

  const estaEmModoEscuro = corpo.classList.contains("dark-mode");

  if (botaoTema) {
    botaoTema.innerText = estaEmModoEscuro ? "Mudar para Tema Claro" : "Mudar para Tema Escuro";
  }

  console.log(`Tema escuro ativo: ${estaEmModoEscuro}`);
}

// 2. Função de seleção exclusiva de card
function selecionarCard(cardClicado) {
  // Remove o destaque de todos os cards
  const todosOsCards = document.querySelectorAll(".card-opcao");
  todosOsCards.forEach(card => card.classList.remove("selecionado"));

  // Adiciona apenas ao elemento clicado
  cardClicado.classList.add("selecionado");
  console.log("Card selecionado:", cardClicado.dataset.id || cardClicado.innerText);
}
```
