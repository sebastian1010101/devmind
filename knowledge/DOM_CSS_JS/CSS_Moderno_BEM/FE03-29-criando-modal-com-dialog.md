# FE03-29 — Criando Modal com Dialog

## A Tag Nativa `<dialog>` do HTML5

Antes da introdução da tag `<dialog>`, a criação de janelas modais em páginas web dependia de estruturas pesadas feitas com `<div>`, controle manual de foco e dezenas de linhas de JavaScript para impedir cliques na página de fundo (*backdrop*).

A tag semântica `<dialog>` resolve esses problemas de forma nativa e acessível:

```html
<dialog id="meu-modal">
  <h2>Título do Modal</h2>
  <p>Conteúdo da janela flutuante.</p>
  <button id="btn-fechar">Fechar</button>
</dialog>
```

---

## Os Dois Métodos Nativos de Abertura

O elemento `<dialog>` no DOM possui métodos nativos integrados no JavaScript:

### 1. `modal.showModal()` — Recomendado
Abre o diálogo como um **modal real**:
- Ativa automaticamente a camada de fundo escurecida (*Backdrop*).
- **Bloqueia a interação** com o restante da página (*foco modal*).
- Permite que o usuário feche a janela automaticamente ao pressionar a tecla `Escape`.

```javascript
const modal = document.querySelector("#meu-modal");
const btnAbrir = document.querySelector("#btn-abrir");

btnAbrir.addEventListener("click", () => {
  modal.showModal(); // Abre como modal real e acessível
});
```

### 2. `modal.show()`
Abre o diálogo como uma caixa de diálogo não-modal flutuante, permitindo que o usuário continue clicando em outros botões da página ao redor.

---

## Fechando o Modal: `modal.close()`

```javascript
const btnFechar = document.querySelector("#btn-fechar");

btnFechar.addEventListener("click", () => {
  modal.close(); // Fecha o diálogo
});
```

Também é possível fechar o modal utilizando formulários HTML nativos com o método especial:
```html
<form method="dialog">
  <button type="submit">Fechar Janela</button>
</form>
```
