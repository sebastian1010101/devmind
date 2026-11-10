# FE03-82 — Animation, Keyframes e Transition

## @keyframes — os fotogramas

`@keyframes` define as etapas de uma animação — os estados em cada ponto percentual do ciclo:

```css
@keyframes slide-in {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
```

`from`/`to` são atalhos para `0%`/`100%`. Para mais controle, use percentuais:

```css
@keyframes bounce {
  0%   { transform: translateY(0); }
  30%  { transform: translateY(-30px); }
  50%  { transform: translateY(0); }
  70%  { transform: translateY(-15px); }
  100% { transform: translateY(0); }
}
```

## animation — a propriedade

Aplica o `@keyframes` a um elemento e controla sua execução:

```css
.modal {
  animation: slide-in 0.4s ease-out;
}
```

### Todas as subpropriedades

```css
animation:
  slide-in        /* name — qual @keyframes */
  0.4s            /* duration — quanto dura */
  ease-out        /* timing-function — ritmo */
  0.1s            /* delay — espera antes de começar */
  1               /* iteration-count — quantas vezes */
  normal          /* direction — direção do ciclo */
  forwards        /* fill-mode — estado antes/depois */
  running;        /* play-state — pausado ou rodando */
```

### Propriedades individuais

```css
.animado {
  animation-name: bounce;
  animation-duration: 1s;
  animation-timing-function: ease-in-out;
  animation-delay: 0.2s;
  animation-iteration-count: infinite;
  animation-direction: alternate;
  animation-fill-mode: forwards;
  animation-play-state: running;
}
```

### fill-mode — o detalhe crucial

Controla o estado do elemento **antes e depois** da animação:

| Valor | Efeito |
| --- | --- |
| `none` (padrão) | Volta ao estado original ao terminar |
| `forwards` | **Fica no último fotograma** após terminar |
| `backwards` | Assume o primeiro fotograma durante o delay |
| `both` | forwards + backwards |

```css
/* Sem forwards, o elemento "pula" de volta ao estado inicial */
.modal {
  animation: slide-in 0.4s ease-out forwards;
}
```

### iteration-count e direction

```css
animation: pulsar 1s infinite;          /* loop eterno */
animation: pulsar 1s 3;                 /* 3 repetições */
animation: pulsar 1s infinite alternate; /* ida e volta */
animation: pulsar 1s reverse;            /* ao contrário */
```

## transition — transição entre estados

Dispara quando uma propriedade **muda de valor** (por `:hover`, classe, etc.):

```css
.card {
  background: white;
  transform: scale(1);
  transition: all 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}
```

### Subpropriedades

```css
.card {
  transition-property: transform, box-shadow; /* só essas animam */
  transition-duration: 0.3s;
  transition-timing-function: ease-out;
  transition-delay: 0s;
}
```

### ⚠️ Evite `transition: all`

```css
/* ❌ Anima TUDO que mudar — até o que você não esperava */
transition: all 0.3s;

/* ✅ Liste só o que deve animar */
transition: transform 0.3s, box-shadow 0.3s;
```

`all` também anima `font-size`, `padding` e propriedades inesperadas — e custa mais caro.

## Timing functions — o ritmo

| Valor | Comportamento |
| --- | --- |
| `linear` | Velocidade constante — robótico, raramente natural |
| `ease` (padrão) | Acelera e desacelera — o mais natural |
| `ease-in` | Começa lento, acelera |
| `ease-out` | Começa rápido, desacelera — ideal para entradas |
| `ease-in-out` | Lento → rápido → lento |
| `cubic-bezier(...)` | Curva customizada |
| `steps(n)` | Animação em saltos discretos |

```css
/* Curva customizada — salto com overshoot */
transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);

/* Passos — contador, máquina de escrever */
animation: piscar 1s steps(2) infinite;
```

## Múltiplas animações

Várias animações no mesmo elemento, separadas por vírgula:

```css
.card {
  animation:
    slide-in 0.4s ease-out forwards,
    pulsar 2s ease-in-out 0.4s infinite;
}
```

## Pausando com hover

```css
.spinner {
  animation: girar 2s linear infinite;
}

.spinner:hover {
  animation-play-state: paused;
}
```

## transition vs animation — quando usar cada

| Situação | Ferramenta |
| --- | --- |
| Hover/focus | `transition` |
| Entrada de elemento/modal | `animation` com `forwards` |
| Loading, spinner | `animation` com `infinite` |
| Mudança de estado controlada por JS | `transition` + troca de classe |
| Efeito complexo com etapas | `@keyframes` |

## JavaScript e animações

### Disparar adicionando classe

```javascript
elemento.classList.add("animado"); // transition faz o resto
```

### Esperar o fim da animação

```javascript
elemento.addEventListener("animationend", () => {
  elemento.classList.remove("animado");
});

elemento.addEventListener("transitionend", () => {
  // transição terminou
});
```

### O truque de reiniciar

Para re-disparar uma animação já rodada, force um reflow:

```javascript
elemento.classList.remove("animado");
void elemento.offsetWidth; // força reflow — "reseta" a animação
elemento.classList.add("animado");
```
