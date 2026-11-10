# FE03-84 — Atividade: Animando um elemento HTML

## Objetivo

Aplicar os conceitos de `transition`, `@keyframes` e `animation` num elemento HTML real — construindo um card que responde a hover com animações suaves e performáticas.

## O cenário

Um card de produto que:

1. **Entra** na tela com fade-in
2. **Reage** ao hover elevando-se e destacando a sombra
3. **Confirma** o clique com um pulso
4. Respeita `prefers-reduced-motion`

## HTML

```html
<div class="card">
  <img src="produto.jpg" alt="Produto" class="card__imagem">
  <div class="card__corpo">
    <h3 class="card__titulo">Headphones Wireless</h3>
    <p class="card__descricao">Cancelamento de ruído ativo</p>
    <span class="card__preco">R$ 299</span>
    <button class="card__botao">Adicionar</button>
  </div>
</div>
```

## CSS — camadas de animação

### 1. Entrada com @keyframes

```css
.card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);

  /* Entrada suave ao carregar */
  animation: card-enter 0.5s ease-out forwards;
  opacity: 0; /* estado inicial — será animado para 1 */
}

@keyframes card-enter {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 2. Hover — elevação com transition

```css
.card {
  /* Transição nas propriedades que mudam no hover */
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-8px);            /* "flutua" */
  box-shadow: 0 12px 24px rgba(0,0,0,0.15); /* sombra mais marcada */
}
```

`translateY` negativo + sombra maior = efeito físico de levantar. Barato: só `transform` e `box-shadow`.

### 3. Clique — feedback tátil

```css
.card__botao {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;

  transition: transform 0.1s, background 0.2s;
}

.card__botao:hover {
  background: #2980b9;
}

.card__botao:active {
  transform: scale(0.92); /* "afunda" ao clicar */
}
```

### 4. Imagem com zoom suave no hover

```css
.card__imagem {
  width: 100%;
  display: block;
  transition: transform 0.4s ease;
}

.card:hover .card__imagem {
  transform: scale(1.05); /* zoom sutil — atrai o olhar */
}
```

O `overflow: hidden` do card garante que a imagem ampliada não vaze das bordas.

### 5. Acessibilidade — reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  .card,
  .card__imagem,
  .card__botao {
    animation: none;
    transition: none;
    opacity: 1; /* card visível sem animação de entrada */
  }
}
```

## CSS completo consolidado

```css
.card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  opacity: 0;
  animation: card-enter 0.5s ease-out forwards;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}

.card__imagem {
  width: 100%;
  display: block;
  transition: transform 0.4s ease;
}

.card:hover .card__imagem {
  transform: scale(1.05);
}

.card__corpo {
  padding: 1.2rem;
}

.card__botao {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.1s, background 0.2s;
}

.card__botao:hover {
  background: #2980b9;
}

.card__botao:active {
  transform: scale(0.92);
}

@keyframes card-enter {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
  .card, .card__imagem, .card__botao {
    animation: none;
    transition: none;
    opacity: 1;
  }
}
```

## Variações para explorar

### Variação A — entrada escalonada (stagger)

Cada card entra com um delay crescente — efeito cascata:

```css
.card:nth-child(1) { animation-delay: 0s; }
.card:nth-child(2) { animation-delay: 0.1s; }
.card:nth-child(3) { animation-delay: 0.2s; }
.card:nth-child(4) { animation-delay: 0.3s; }
```

### Variação B — badge pulsante de promoção

```css
.badge-promo {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #e74c3c;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  animation: pulsar 1.5s ease-in-out infinite;
}

@keyframes pulsar {
  0%, 100% { transform: scale(1); }
  50%      { transform: scale(1.08); }
}
```

### Variação C — reveal ao scroll (com JavaScript)

```javascript
const observer = new IntersectionObserver((entradas) => {
  entradas.forEach(entrada => {
    if (entrada.isIntersecting) {
      entrada.target.classList.add("visivel");
    }
  });
});

document.querySelectorAll(".card").forEach(card => observer.observe(card));
```

```css
.card {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.5s, transform 0.5s;
}

.card.visivel {
  opacity: 1;
  transform: translateY(0);
}
```

## Critérios de verificação

- Entrada usa `@keyframes` + `forwards` (elemento fica no estado final)
- Hover usa `transition` (mudança de estado, não animação autônoma)
- Apenas `transform`, `opacity` e `box-shadow` animados — nada de `width`/`top`
- `overflow: hidden` no card contém o zoom da imagem
- `prefers-reduced-motion` desativa tudo para usuários sensíveis
- Durações entre 0.1s (clique) e 0.5s (entrada) — dentro do ideal de UX

## Erros comuns a evitar

| Erro | Correção |
| --- | --- |
| `opacity: 0` sem `forwards` | Elemento volta a `opacity: 0` ao fim — use `animation-fill-mode: forwards` |
| `transition: all` | Liste as propriedades — `all` anima o que não deve |
| `width`/`height` animados | Força reflow — use `transform: scale()` |
| Animação longa (> 1s) | Entrada deve ser rápida — 400ms no máximo |
| Sem `prefers-reduced-motion` | Acessibilidade obrigatória — sempre inclua |
