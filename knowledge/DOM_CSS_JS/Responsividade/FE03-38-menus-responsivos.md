# FE03-38 — Menus Responsivos

## O Padrão do Menu Hambúrguer (*Hamburger Menu*)

Em computadores, cabeçalhos possuem espaço horizontal abundante para exibir listas completas de links lado a lado. Em smartphones, esse espaço é escasso, tornando essencial o padrão do **menu recolhível**:

- Em telas menores, a lista de links fica oculta por padrão e surge um botão de acionamento (geralmente com o ícone de três linhas paralelas &equiv;).
- Ao tocar no botão, o menu desliza suavemente sobre a tela ou empurra o conteúdo (*Off-Canvas Drawer*).
- Em telas maiores (`@media (min-width: 768px)`), o botão hambúrguer é ocultado e a barra de links volta à sua exibição horizontal contínua.

---

## Acessibilidade em Menus Móveis

Para garantir que pessoas com leitores de tela entendam o funcionamento do menu móvel:
- O botão deve possuir o atributo `aria-label="Abrir menu de navegação"`.
- O atributo `aria-expanded="false"` deve ser alternado via JavaScript para `"true"` quando o menu for aberto.
- O botão deve ser uma tag real `<button>`, permitindo foco via teclado.

---

## Estrutura HTML do Padrão Responsivo

```html
<header class="header">
  <div class="header__container">
    <a href="#" class="header__logo">Kenzie<span>Academy</span></a>

    <!-- Botão Hambúrguer visível apenas no mobile -->
    <button class="header__btn-menu" aria-label="Abrir menu" aria-expanded="false">
      <span class="hamburguer"></span>
    </button>

    <!-- Navegação que se transforma entre mobile e desktop -->
    <nav class="header__nav">
      <ul class="header__menu-lista">
        <li><a href="#cursos" class="header__link">Cursos</a></li>
        <li><a href="#metodologia" class="header__link">Metodologia</a></li>
        <li><a href="#contato" class="header__link">Contato</a></li>
      </ul>
    </nav>
  </div>
</header>
```
