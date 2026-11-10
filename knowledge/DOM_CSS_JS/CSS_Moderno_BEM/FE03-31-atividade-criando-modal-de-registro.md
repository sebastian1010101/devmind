# FE03-31 — Atividade: Criando Modal de Registro

## Objetivo da Atividade

Integrar a tag semântica `<dialog>`, metodologia de classes BEM, variáveis CSS de design e manipulação de eventos de abertura, fechamento e submissão de formulário no modal.

---

## Enunciado do Desafio

Construa um componente modal de cadastro de novo usuário:

1. Um botão principal na página com a classe `.btn .btn--primario` para abrir o modal.
2. Uma tag `<dialog>` estruturada com classes BEM:
   - Bloco: `.modal`
   - Elementos: `.modal__cabecalho`, `.modal__titulo`, `.modal__btn-fechar`, `.modal__formulario`
3. Abertura do modal via `modal.showModal()` no clique do botão.
4. Fechamento do modal ao clicar no botão de fechar (`X`) ou ao submeter o formulário de cadastro com sucesso.
5. Estilização do `::backdrop` com fundo preto translúcido e desfoque suave.

---

## Solução de Referência

### `index.html`

```html
<button id="btn-abrir-cadastro" class="btn btn--primario">Novo Cadastro</button>

<dialog id="modal-cadastro" class="modal">
  <div class="modal__cabecalho">
    <h2 class="modal__titulo">Criar Nova Conta</h2>
    <button id="btn-fechar-modal" class="modal__btn-fechar" aria-label="Fechar modal">&times;</button>
  </div>

  <form id="form-cadastro" class="modal__formulario">
    <div class="campo">
      <label for="nome-usuario">Nome Completo:</label>
      <input type="text" id="nome-usuario" name="nome" required>
    </div>

    <div class="campo">
      <label for="email-usuario">E-mail:</label>
      <input type="email" id="email-usuario" name="email" required>
    </div>

    <button type="submit" class="btn btn--sucesso">Finalizar Registro</button>
  </form>
</dialog>
```

### `style.css`

```css
:root {
  --color-primary: #2563eb;
  --color-success: #16a34a;
  --color-text: #0f172a;
}

.modal {
  border: none;
  border-radius: 12px;
  padding: 24px;
  max-width: 440px;
  width: 90%;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal::backdrop {
  background-color: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
}

.modal__cabecalho {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal__btn-fechar {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #64748b;
}

.modal__btn-fechar:hover {
  color: #0f172a;
}
```

### `script.js`

```javascript
const modalCadastro = document.querySelector("#modal-cadastro");
const btnAbrirModal = document.querySelector("#btn-abrir-cadastro");
const btnFecharModal = document.querySelector("#btn-fechar-modal");
const formCadastro = document.querySelector("#form-cadastro");

btnAbrirModal.addEventListener("click", () => {
  modalCadastro.showModal();
});

btnFecharModal.addEventListener("click", () => {
  modalCadastro.close();
});

formCadastro.addEventListener("submit", (e) => {
  e.preventDefault();
  console.log("Usuário cadastrado com sucesso!");
  modalCadastro.close();
  formCadastro.reset();
});
```
