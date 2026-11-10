# FE03-37 — Clamp

## Tipografia e Dimensões Fluidas com `clamp()`

Tradicionalmente, para fazer uma fonte encolher no celular e crescer no computador, escreviam-se múltiplas media queries para cada breakpoint.

A função moderna **`clamp()`** do CSS permite criar **valores fluidos e responsivos contínuos** em uma única linha de código, sem precisar de nenhuma media query:

```css
propriedade: clamp(minimo, valor-ideal-fluido, maximo);
```

---

## Os Três Parâmetros do `clamp()`

1. **Valor Mínimo:** o menor tamanho que a propriedade pode atingir (mesmo em telas microscópicas).
2. **Valor Ideal / Preferido:** um cálculo que combina unidades de viewport (`vw`) com unidades relativas (`rem`), permitindo que o valor cresça suavemente com a largura da tela.
3. **Valor Máximo:** o teto limite que a propriedade nunca ultrapassará (mesmo em monitores gigantes de 4K).

---

## Exemplo 1: Título Fluido Responsivo

```css
h1 {
  /* Tamanho mínimo: 24px (1.5rem)
     Ideal: 4% da largura da tela + 1rem
     Tamanho máximo: 48px (3rem) */
  font-size: clamp(1.5rem, 4vw + 1rem, 3rem);
}
```

- Em uma tela de celular de 360px, o título terá exatamente `1.5rem` (confortável).
- Conforme o usuário redimensiona a janela, o título cresce gradativamente.
- Em um monitor grande de 1920px, ele estaciona suavemente em `3rem` sem explodir de tamanho.

---

## Exemplo 2: Espaçamentos Internos e Containers Fluidos

O `clamp()` também pode ser aplicado a margens, preenchimentos e larguras de elementos:

```css
.hero-banner {
  /* Preenchimento vertical entre 32px e 96px */
  padding-top: clamp(2rem, 5vw + 1rem, 6rem);
  padding-bottom: clamp(2rem, 5vw + 1rem, 6rem);
}
```
