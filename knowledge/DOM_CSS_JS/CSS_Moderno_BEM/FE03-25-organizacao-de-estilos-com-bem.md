# FE03-25 — Organização de Estilos com BEM

## Boas Práticas e Regras de Ouro do BEM

A metodologia BEM não serve apenas para dar nomes bonitos às classes; ela cria um código limpo e previsível quando combinada com a estrutura modular de arquivos:

---

## 1. Mantenha a Especificidade Plana (Evite Aninhamentos Excessivos)

No BEM, **cada classe já carrega seu próprio contexto**. Portanto, você quase nunca precisa aninhar seletores no CSS:

```css
/* RUIM: Especificidade alta e acoplada ao HTML */
.card .card__corpo h2.card__titulo {
  color: #0f172a;
}

/* EXCELENTE (Padrão BEM): Especificidade simples e rápida */
.card__titulo {
  color: #0f172a;
}
```

---

## 2. Não Crie Elementos de Elementos (`__elemento__subelemento`)

Um dos erros mais comuns de iniciantes é criar cadeias infinitas de underscores. Elementos devem pertencer **sempre diretamente ao Bloco**:

```html
<!-- ERRADO: encadeamento excessivo -->
<div class="menu">
  <ul class="menu__lista">
    <li class="menu__lista__item">
      <a class="menu__lista__item__link">Link</a>
    </li>
  </ul>
</div>

<!-- CORRETO: todos são elementos diretos do bloco menu -->
<nav class="menu">
  <ul class="menu__lista">
    <li class="menu__item">
      <a class="menu__link">Link</a>
    </li>
  </ul>
</nav>
```

---

## 3. Modularização de Arquivos por Bloco BEM

Em projetos profissionais, cada grande bloco BEM ganha seu próprio arquivo CSS dentro da pasta de componentes:

```text
src/styles/components/
├── _card.css        /* Apenas regras .card, .card__* e .card--* */
├── _header.css      /* Apenas regras .header e .header__* */
└── _buttons.css     /* Apenas regras .btn e .btn--* */
```

Isso garante que um desenvolvedor consiga editar o estilo de um componente sem o menor risco de quebrar o visual de outros blocos do sistema.
