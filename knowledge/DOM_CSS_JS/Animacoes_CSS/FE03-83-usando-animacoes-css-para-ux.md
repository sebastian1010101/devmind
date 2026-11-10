# FE03-83 — Usando animações CSS para UX

## Animação como comunicação

A melhor animação é a que o usuário **não percebe** — ela simplesmente torna a interface mais clara. Cada animação deve responder: *"o que isso comunica?"*

## Feedback imediato

### Clique de botão — confirmação física

```css
.botao {
  transition: transform 0.1s;
}

.botao:active {
  transform: scale(0.95); /* "afunda" — feedback tátil */
}
```

O `:active` + `scale` simula a sensação física de pressionar — o usuário *sente* o clique.

### Sucesso/erro em formulários

```css
.input.valido {
  border-color: #22c55e;
  animation: check-pop 0.3s;
}

.input.invalido {
  border-color: #ef4444;
  animation: shake 0.4s;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25%      { transform: translateX(-6px); }
  75%      { transform: translateX(6px); }
}
```

O *shake* comunica erro sem palavras — um gesto universal de "não".

## Orientação de atenção

### Entrada de elementos — o que chegou novo

```css
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card {
  animation: fade-in-up 0.4s ease-out;
}
```

Elementos que "sobem" sinalizam conteúdo novo — direcionam o olhar naturalmente.

### Skeleton loading — a espera perceptível

```css
.skeleton {
  background: linear-gradient(90deg, #eee 25%, #f5f5f5 50%, #eee 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  from { background-position: 200% 0; }
  to   { background-position: -200% 0; }
}
```

O *shimmer* diz "está carregando" melhor que um spinner — mostra a estrutura do que vem.

### Indicador de scroll

```css
.seta-baixo {
  animation: bounce-down 2s infinite;
}

@keyframes bounce-down {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(8px); }
}
```

## Transições de estado

### Modal que entra e sai

```css
.modal-overlay {
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}

.modal-overlay.aberto {
  opacity: 1;
  visibility: visible;
}

.modal {
  transform: scale(0.9);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-overlay.aberto .modal {
  transform: scale(1); /* "cresce" ao abrir */
}
```

### Menu dropdown

```css
.menu {
  opacity: 0;
  transform: translateY(-10px);
  pointer-events: none; /* evita cliques quando escondido */
  transition: opacity 0.2s, transform 0.2s;
}

.menu.aberto {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
```

## Acessibilidade — prefers-reduced-motion

Usuários com sensibilidade a movimento (vestibular, TDAH) precisam de uma saída. A media query `prefers-reduced-motion` respeita a configuração do sistema:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Isso desativa animações para quem pediu. Inclua sempre — é o padrão de mercado.

## Regras práticas de UX

| Regra | Razão |
| --- | --- |
| Duração 150–400ms | Rápido o suficiente para não atrapalhar, visível o suficiente para notar |
| `ease-out` para entradas | Rápido no início, suave no fim — parece "atencioso" |
| `ease-in` para saídas | Começa a sair devagar — o usuário entende o que está sumindo |
| Anime `transform`/`opacity` | Performance — o resto força reflow |
| Uma coisa animada por vez | Animações simultâneas viram circo |
| Animação ≤ 500ms no total | Mais que isso o usuário espera — e esperar irrita |
| `prefers-reduced-motion` | Acessibilidade não é opcional |

## Anti-padrões a evitar

```css
/* ❌ Muito lento — o usuário espera a animação terminar */
transition: all 2s;

/* ❌ Anima o layout — caro e instável */
transition: width 0.3s, top 0.3s;

/* ❌ Animação que bloqueia interação */
.overlay {
  animation: abrir 1s; /* cliques ignorados por 1s */
}

/* ❌ Loop em conteúdo importante — distrai e irrita */
.aviso {
  animation: pulsar 1s infinite;
}
```

## Resumo executivo

- Animação serve à comunicação: feedback, orientação, estado
- `transform` + `opacity` = suave e barato
- Feedback tátil (`:active` + `scale`) faz interfaces parecerem vivas
- Skeleton > spinner quando a estrutura é conhecida
- `prefers-reduced-motion` sempre — acessibilidade primeiro
- Se a animação não comunica nada, remova
