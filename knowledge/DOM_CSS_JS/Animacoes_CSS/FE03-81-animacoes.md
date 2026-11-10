# FE03-81 — Animações

## Por que animar

Animações em CSS transformam interfaces estáticas em experiências vivas. Bem usadas, elas:

- **Guiam a atenção** — mostram o que mudou e para onde olhar
- **Dão feedback** — confirmam que um clique foi registrado
- **Suavizam transições** — mudanças abruptas assustam; animadas, orientam
- **Comunicam estado** — loading, sucesso, erro, espera

Mal usadas, fazem o oposto: distraem, irritam e prejudicam a acessibilidade. A regra: **animação é comunicação, não decoração**.

## As duas ferramentas

CSS oferece dois sistemas de animação:

| | `transition` | `@keyframes` + `animation` |
| --- | --- | --- |
| Disparo | Mudança de estado (hover, classe, foco) | Automático ou por classe |
| Complexidade | Um estado → outro (A → B) | Múltiplos passos (0% → 50% → 100%) |
| Loop | Não repete | `infinite`, `alternate`, `forwards` |
| Uso típico | Hover, toggle, modal | Spinner, bounce, entrada |

```css
/* Transition — o elemento muda suavemente quando algo muda nele */
.botao {
  background: blue;
  transition: background 0.3s;
}
.botao:hover {
  background: darkblue; /* transição suave */
}
```

```css
/* Keyframes — animação autônoma com etapas */
@keyframes pulsar {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.1); }
  100% { transform: scale(1); }
}

.icone {
  animation: pulsar 1s infinite;
}
```

## O que pode ser animado

Nem toda propriedade anima suavemente. As que **interpolam** (transição gradual):

| Animável | Não animável |
| --- | --- |
| `opacity` | `display` (none → block) |
| `transform` | `position` |
| `color`, `background` | `font-family` |
| `width`, `height`, `margin` | `z-index` (muda, mas sem transição) |
| `filter`, `box-shadow` | `visibility` |

## Performance: as propriedades baratas

O navegador renderiza em etapas — algumas propriedades forçam recálculos caros de layout (*reflow*) e pintura (*repaint*). Outras são processadas direto na GPU:

```text
Layout (caro)    → Paint (médio)    → Composite (barato, GPU)
width, height    color, background   transform, opacity
margin, padding  box-shadow          filter (com cuidado)
```

### A regra de ouro

Para animações fluidas a 60fps, prefira `transform` e `opacity` — são "baratas" porque não alteram o layout:

```css
/* ❌ Caro — mexe no layout a cada frame */
.caixa:hover {
  width: 300px;
  margin-left: 100px;
}

/* ✅ Barato — a GPU cuida, sem reflow */
.caixa:hover {
  transform: scale(1.2) translateX(100px);
}
```

### Transformações essenciais

```css
transform: translateX(50px);   /* desloca horizontalmente */
transform: translateY(-20px);  /* desloca verticalmente */
transform: scale(1.5);         /* escala uniforme */
transform: rotate(45deg);      /* gira */
transform: skewX(10deg);       /* inclina */

/* Combinadas */
transform: translateX(50px) scale(1.1) rotate(5deg);
```

## O problema do `display: none`

`display` não anima — um elemento com `none` some instantaneamente. A técnica para "sumir animando":

```css
/* ✅ Opacity + visibility — fade suave */
.card {
  opacity: 1;
  visibility: visible;
  transition: opacity 0.3s, visibility 0.3s;
}

.card.escondido {
  opacity: 0;
  visibility: hidden; /* some depois da transição */
}
```

`visibility: hidden` espera a transição de `opacity` terminar — o efeito é um fade-out limpo, sem tirar o elemento do fluxo antes da hora.

## `will-change` — aviso à GPU

Para animações complexas, avise o navegador com antecedência:

```css
.animado {
  will-change: transform, opacity;
}
```

Use com parcimônia — cada `will-change` aloca memória de GPU. Só em animações que realmente precisam de otimização.

## Resumo

- `transition` para mudanças de estado simples (hover, toggle)
- `@keyframes` + `animation` para movimentos com etapas e loops
- Anime `transform` e `opacity` — são as propriedades baratas
- `display: none` não anima — use `opacity` + `visibility`
- Animação boa é invisível — serve à experiência, não chama atenção para si
