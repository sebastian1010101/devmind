# FE01-48 — Pseudo Classe (hover)

## O Estado `:hover`

A pseudo-classe `:hover` é aplicada a um elemento quando o usuário interage com ele através de um dispositivo apontador (como o cursor do mouse), sem necessariamente ativá-lo ou clicar nele.

É o mecanismo fundamental para criar **micro-interações e feedback visual imediato**, informando ao usuário que aquele elemento é clicável e interativo.

---

## Casos de Uso Mais Frequentes

### 1. Botões com Transição Suave de Cor

```css
.btn-acao {
  background-color: #2563eb;
  color: #ffffff;
  padding: 12px 24px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  /* Transição suave evita mudanças visuais bruscas */
  transition: background-color 0.2s ease, transform 0.1s ease;
}

.btn-acao:hover {
  background-color: #1d4ed8; /* Escurece sutilmente no hover */
  transform: translateY(-2px); /* Efeito sutil de elevação */
}
```

### 2. Efeito de Elevação em Cards

```css
.card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 24px;
  transition: box-shadow 0.3s ease, border-color 0.3s ease;
}

.card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```

### 3. Sublinhado Dinâmico em Links de Navegação

```css
.nav-link {
  color: #334155;
  text-decoration: none;
  position: relative;
}

.nav-link:hover {
  color: #2563eb;
  text-decoration: underline;
}
```

---

## Considerações para Dispositivos Móveis (Touchscreens)

Em celulares e tablets, não existe o conceito de passar o cursor do mouse antes de tocar na tela. O `:hover` em telas de toque só dispara quando o usuário toca fisicamente no elemento, podendo às vezes manter o estado "preso" até o próximo toque.

Boas práticas:
- Nunca esconda informações essenciais ou botões críticos que só fiquem visíveis exclusivamente no `:hover`.
- No CSS moderno, pode-se isolar estilos de hover apenas para aparelhos com cursor real através de media queries:

```css
@media (hover: hover) {
  .btn:hover {
    background-color: #1d4ed8;
  }
}
```
