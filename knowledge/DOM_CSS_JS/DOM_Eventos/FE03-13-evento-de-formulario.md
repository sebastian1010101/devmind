# FE03-13 — Evento de Formulário

## Capturando e Validando Formulários com JavaScript

A submissão de formulários é um dos fluxos de interação mais importantes no front-end. O JavaScript moderno intercepta o evento, valida os campos e gera feedback sem recarregar a tela.

---

## O Ciclo Completo do Evento `submit`

1. Selecionar a tag `<form>`.
2. Escutar o evento `"submit"`.
3. Invocar imediatamente `event.preventDefault()`.
4. Capturar os valores dos inputs.
5. Validar os dados e apresentar o resultado.

---

## Exemplo Completo de Implementação

```javascript
const formLogin = document.querySelector("#form-login");
const inputEmail = document.querySelector("#campo-email");
const inputSenha = document.querySelector("#campo-senha");
const mensagemAviso = document.querySelector("#mensagem-status");

formLogin.addEventListener("submit", (event) => {
  // 1. Evita o recarregamento automático da página
  event.preventDefault();

  // 2. Extrai e limpa os valores digitados
  const email = inputEmail.value.trim();
  const senha = inputSenha.value.trim();

  // 3. Validação local dos dados
  if (!email || !senha) {
    mensagemAviso.innerText = "Por favor, preencha todos os campos obrigatórios!";
    mensagemAviso.style.color = "red";
    return;
  }

  if (senha.length < 6) {
    mensagemAviso.innerText = "A senha deve conter no mínimo 6 caracteres.";
    mensagemAviso.style.color = "red";
    return;
  }

  // 4. Sucesso na validação
  mensagemAviso.innerText = "Autenticação em andamento...";
  mensagemAviso.style.color = "green";
  console.log("Dados prontos para envio:", { email, senha });

  // 5. Limpa os campos do formulário
  formLogin.reset();
});
```

---

## Eventos Complementares: `input` e `change`

- **Evento `input`:** dispara instantaneamente a cada tecla ou colagem de texto dentro de um campo. Ideal para buscas em tempo real e medidores de força de senha.
- **Evento `change`:** dispara apenas quando o campo perde o foco (*blur*) após o valor ter sido alterado. Ideal para seletores `<select>` e caixas `<input type="checkbox">`.
