# FE03-36 — Breakpoints

## O que é um Breakpoint (Ponto de Quebra)?

Um **breakpoint** é a largura de tela específica na qual o layout de uma página web precisa mudar significativamente para manter a legibilidade, o alinhamento e a facilidade de navegação do usuário.

Em vez de criar breakpoints arbitrários para cada modelo específico de smartphone lançado no mercado, a indústria adota **faixas padronizadas de corte**:

---

## Os Breakpoints Padrão do Mercado

| Categoria | Faixa de Largura | Breakpoint Típico | Dispositivos Representados |
| --- | --- | --- | --- |
| **Mobile Pequeno** | `< 480px` | Estilo Base (sem media query) | Smartphones em modo retrato |
| **Mobile Grande / Fablet** | `481px - 767px` | `@media (min-width: 480px)` | Celulares maiores e paisagem |
| **Tablet** | `768px - 1023px` | `@media (min-width: 768px)` | iPads, tablets em geral |
| **Desktop / Laptop** | `1024px - 1439px` | `@media (min-width: 1024px)` | Notebooks e monitores convencionais |
| **Telas Largas / 4K** | `>= 1440px` | `@media (min-width: 1440px)` | Monitores ultrawide de alta resolução |

---

## Organizando Breakpoints com Variáveis e Mobile-First

```css
/* ==========================================
   ESTILOS BASE: Celular (Mobile-First)
   ========================================== */
.card-usuario {
  width: 100%;
  padding: 1rem;
}

/* ==========================================
   TABLET: a partir de 768px
   ========================================== */
@media (min-width: 768px) {
  .card-usuario {
    width: calc(50% - 1rem); /* 2 colunas */
    padding: 1.5rem;
  }
}

/* ==========================================
   DESKTOP: a partir de 1024px
   ========================================== */
@media (min-width: 1024px) {
  .card-usuario {
    width: calc(33.333% - 1rem); /* 3 colunas */
    padding: 2rem;
  }
}
```

---

## A Regra de Ouro dos Breakpoints

> **Deixe o conteúdo ditar o breakpoint, não o aparelho.**
> Se o layout quebrou ou o texto ficou desconfortável em 900px, adicione um breakpoint em 900px, independentemente de haver ou não um aparelho famoso com essa medida exata.
