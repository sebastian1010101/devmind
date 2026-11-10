# FE03-35 — Media Query

## O que é uma Media Query?

Uma **Media Query** é uma diretiva condicional do CSS (`@media`) que permite aplicar blocos específicos de estilos somente quando determinadas características do dispositivo ou da tela forem atendidas (como largura mínima, orientação ou tipo de mídia).

---

## Sintaxe Fundamental

```css
/* Sintaxe Tradicional */
@media (min-width: 768px) {
  /* Regras aplicadas apenas em telas com largura de 768px ou mais */
  .container {
    max-width: 720px;
  }
}
```

---

## Tipos e Recursos de Mídia Comuns

### 1. `min-width` (Estratégia Mobile-First)
As regras entram em vigor **a partir daquela largura para cima**:
```css
/* Celular: padrão 1 coluna */
.grade-produtos {
  display: flex;
  flex-direction: column;
}

/* Tablet e Desktop: transforma em 3 colunas */
@media (min-width: 768px) {
  .grade-produtos {
    flex-direction: row;
    flex-wrap: wrap;
  }
}
```

### 2. `max-width` (Estratégia Desktop-First)
As regras aplicam-se **até atingir aquela largura máxima**:
```css
@media (max-width: 480px) {
  .sidebar {
    display: none; /* Oculta a barra lateral apenas em smartphones */
  }
}
```

### 3. Media Queries de Preferência do Usuário

O CSS moderno permite detectar preferências do sistema operacional do visitante:

```css
/* Detecta se o usuário ativou o Modo Escuro no Windows/macOS/Android */
@media (prefers-color-scheme: dark) {
  body {
    background-color: #0f172a;
    color: #f8fafc;
  }
}

/* Detecta se o usuário reduziu animações por sensibilidade vestibular */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
