# FE01-31 — Altura e Largura

## Controlando Dimensões: `width` e `height`

As propriedades `width` (largura) e `height` (altura) definem o tamanho das caixas no CSS.

```css
.card {
  width: 300px;
  height: 200px;
}
```

---

## Dimensões Mínimas e Máximas

Para criar layouts flexíveis e responsivos que se adaptam a diferentes tamanhos de monitores e celulares, utiliza-se limites mínimos e máximos:

### 1. `max-width` (Largura Máxima)
Impede que o elemento cresça além de um determinado limite, permitindo que ele encolha quando a tela for menor:

```css
.container {
  width: 100%;
  max-width: 1200px; /* Não ultrapassa 1200px em telas largas */
  margin: 0 auto;    /* Centraliza na tela */
}
```

### 2. `min-width` (Largura Mínima)
Garante que o elemento nunca fique menor do que uma medida essencial, evitando que o conteúdo fique espremido e ilegível:

```css
.sidebar {
  min-width: 240px;
}
```

### 3. `max-height` e `min-height`
Controlam os limites verticais. Uma prática muito comum é garantir que a página ou seção ocupe pelo menos a altura inteira da tela:

```css
.hero-section {
  min-height: 100vh; /* Ocupa no mínimo 100% da altura da viewport */
}
```

---

## Dimensões Automáticas e Imagens Responsivas

Evite definir `height` fixo em caixas que contêm texto dinâmico; deixe a altura como `auto` para que a caixa se expanda naturalmente de acordo com a quantidade de conteúdo.

Para imagens responsivas que nunca ultrapassam seu container pai:

```css
img {
  max-width: 100%;
  height: auto; /* Mantém a proporção de aspecto original sem distorcer */
  display: block;
}
```
