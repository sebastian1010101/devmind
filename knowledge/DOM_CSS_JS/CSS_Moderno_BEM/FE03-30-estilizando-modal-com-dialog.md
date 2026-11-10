# FE03-30 — Estilizando Modal com Dialog

## Estilizando o Elemento `<dialog>`

Por padrão, os navegadores atribuem ao elemento `<dialog>` bordas pretas simples e centralização automática na tela. Podemos customizá-lo com CSS moderno:

```css
dialog {
  border: none;
  border-radius: 12px;
  padding: 32px;
  background-color: #ffffff;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  max-width: 500px;
  width: 90%;
}
```

---

## O Pseudo-Elemento `::backdrop`

Quando o modal é aberto através de `showModal()`, o navegador cria automaticamente um pseudo-elemento virtual em tela cheia localizado imediatamente atrás do diálogo, chamado `::backdrop`.

Podemos estilizá-lo com cores translúcidas ou efeitos de desfoque de fundo (*Glassmorphism*):

```css
dialog::backdrop {
  /* Fundo escuro semitransparente */
  background-color: rgba(15, 23, 42, 0.75);

  /* Efeito moderno de desfoque da página atrás */
  backdrop-filter: blur(4px);
}
```

---

## Fechando o Modal ao Clicar Fora (no Backdrop)

Uma funcionalidade muito desejada pelos usuários é fechar o diálogo ao clicar no fundo escuro. Com a tag `<dialog>`, podemos calcular as coordenadas do clique:

```javascript
const modal = document.querySelector("dialog");

modal.addEventListener("click", (event) => {
  const rect = modal.getBoundingClientRect();
  const clicouNoBackdrop = (
    event.clientX < rect.left ||
    event.clientX > rect.right ||
    event.clientY < rect.top ||
    event.clientY > rect.bottom
  );

  if (clicouNoBackdrop) {
    modal.close();
  }
});
```
