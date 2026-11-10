# FE03-39 — Atividade: Criando Menu Responsivo

## Objetivo da Atividade

Construir do início ao fim um menu de navegação responsivo completo utilizando Mobile-First, Flexbox, media queries e um script leve em JavaScript para alternar a exibição da lista e os atributos de acessibilidade.

---

## Enunciado do Desafio

Crie os arquivos `menu.html`, `menu.css` e `menu.js` cumprindo os critérios:

1. **Visão Mobile (Padrão inicial):**
   - A lista de navegação fica recolhida acima ou fora da tela (`display: none` ou translação).
   - O botão hambúrguer fica visível no canto direito do cabeçalho.
   - Ao clicar no botão hambúrguer, o menu recebe a classe `.header__nav--ativo` e se abre como gaveta suspensa.
2. **Visão Desktop (`@media (min-width: 768px)`):**
   - O botão hambúrguer fica permanentemente oculto (`display: none`).
   - A lista de links é exibida horizontalmente lado a lado com `display: flex`.

---

## Solução de Referência

### `menu.css` (Mobile-First)

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: system-ui, -apple-system, sans-serif;
}

.header {
  background-color: #0f172a;
  color: #ffffff;
  padding: 1rem;
}

.header__container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.header__logo {
  color: #ffffff;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.25rem;
}

/* Botão no Mobile */
.header__btn-menu {
  background: none;
  border: none;
  color: #ffffff;
  font-size: 1.75rem;
  cursor: pointer;
  display: block;
}

/* Menu recolhido no Mobile */
.header__nav {
  display: none;
  position: absolute;
  top: 65px;
  left: 0;
  width: 100%;
  background-color: #1e293b;
  padding: 1rem 0;
}

.header__nav--ativo {
  display: block; /* Fica visível ao clicar */
}

.header__menu-lista {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0 1.5rem;
}

.header__menu-lista a {
  color: #cbd5e1;
  text-decoration: none;
  font-size: 1rem;
}

/* ==========================================
   DESKTOP: a partir de 768px
   ========================================== */
@media (min-width: 768px) {
  .header__btn-menu {
    display: none; /* Esconde o botão hambúrguer no PC */
  }

  .header__nav {
    display: block;
    position: static;
    width: auto;
    background: none;
    padding: 0;
  }

  .header__menu-lista {
    flex-direction: row;
    gap: 1.5rem;
  }
}
```

### `menu.js`

```javascript
const btnMenu = document.querySelector(".header__btn-menu");
const navContainer = document.querySelector(".header__nav");

if (btnMenu && navContainer) {
  btnMenu.addEventListener("click", () => {
    // Alterna a classe visual de abertura
    navContainer.classList.toggle("header__nav--ativo");

    // Alterna a propriedade de acessibilidade
    const estaAberto = navContainer.classList.contains("header__nav--ativo");
    btnMenu.setAttribute("aria-expanded", estaAberto);
  });
}
```
