# FE03-09 — Introdução a Eventos

## O que são Eventos no Navegador?

Um **evento** é um sinal emitido pelo navegador indicando que **algo relevante aconteceu** na página (uma ação do usuário ou uma alteração de estado do sistema).

Exemplos de eventos:
- O usuário clicou em um botão (`click`).
- O usuário digitou um caractere no teclado (`keydown` / `keyup`).
- O usuário moveu o mouse sobre uma área (`mouseenter` / `mouseleave`).
- A página terminou de carregar completamente (`DOMContentLoaded`).
- A janela foi redimensionada (`resize`) ou rolada (`scroll`).

---

## O Método Universal: `addEventListener()`

A forma padrão, moderna e profissional de escutar eventos em qualquer elemento do DOM é através do método `addEventListener`:

```javascript
elemento.addEventListener("tipoDoEvento", funcaoCallback);
```

### Exemplo Básico de Clique:

```javascript
const botaoEnviar = document.querySelector("#btn-enviar");

botaoEnviar.addEventListener("click", () => {
  console.log("O botão de envio foi clicado com sucesso!");
});
```

---

## Principais Tipos de Eventos do Cotidiano

| Categoria | Evento | Momento do Disparo |
| --- | --- | --- |
| **Mouse** | `click` | Clique completo do botão principal |
| **Mouse** | `dblclick` | Duplo clique rápido |
| **Mouse** | `mouseenter` | Cursor entra na área do elemento |
| **Teclado** | `keydown` | Uma tecla física é pressionada |
| **Teclado** | `keyup` | Uma tecla física é solta |
| **Formulário** | `submit` | O formulário é enviado |
| **Formulário** | `input` | O valor de um campo muda em tempo real |
| **Formulário** | `change` | O valor muda e o campo perde o foco |

---

## Por que Evitar Eventos Inline no HTML?

Você ainda pode encontrar em tutoriais legados o uso de atributos como `<button onclick="executar()">`. Essa prática é desencorajada porque:
- Polui a estrutura HTML com lógica de execução.
- Permite registrar apenas uma única função por evento (enquanto `addEventListener` permite adicionar múltiplos ouvintes independentes ao mesmo elemento).
