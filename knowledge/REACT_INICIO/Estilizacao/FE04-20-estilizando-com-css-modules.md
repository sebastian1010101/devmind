# FE04-20 — Estilizando com CSS Modules

## O problema do CSS global

Todo CSS importado é global — duas classes com o mesmo nome colidem:

```css
/* Header.css */
.title { color: blue; }

/* Footer.css */
.title { color: red; }  /* ⚠️ sobrescreve a do Header! */
```

**CSS Modules** resolve com escopo local: cada classe é transformada num nome único (`Card_title__x7k2m`), impossível de colidir.

## Como funciona

Arquivo com sufixo `.module.css` + import como objeto:

```css
/* src/components/Card/Card.module.css */
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
}

.titulo {
  font-size: 1.25rem;
  color: var(--cor-primaria);
}
```

```jsx
// src/components/Card/Card.jsx
import styles from "./Card.module.css";

function Card() {
  return (
    <div className={styles.card}>
      <h2 className={styles.titulo}>Título</h2>
    </div>
  );
}
```

O que chega ao navegador:

```html
<div class="Card_card__a8f3k">
  <h2 class="Card_titulo__x2m9p">Título</h2>
</div>
```

Classes com hash único — colisão impossível por construção.

## Sintaxe avançada

### Múltiplas classes

```jsx
// template string
<div className={`${styles.card} ${styles.destaque}`}>

// array + join
<div className={[styles.card, styles.destaque].join(" ")}>
```

### Classes condicionais

```jsx
function Botao({ ativo }) {
  return (
    <button
      className={`${styles.botao} ${ativo ? styles.ativo : ""}`}
    >
      Clique
    </button>
  );
}
```

### Estilos compostos com `composes`

```css
.base {
  padding: 0.5rem 1rem;
  border-radius: 6px;
}

.primario {
  composes: base;         /* herda .base */
  background: blue;
  color: white;
}
```

## Variáveis CSS com Modules

Variáveis continuam globais — defina no `:root` do `index.css` e use normalmente:

```css
/* Card.module.css usa variáveis globais */
.card {
  background: var(--cor-primaria);
}
```

## O que o Modules NÃO cobre

| Escopo | Onde |
| --- | --- |
| Reset, variáveis, tipografia | `index.css` (global) |
| Estilos do componente | `*.module.css` (local) |
| Valores dinâmicos | `style={{}}` inline |

## Convenção de estrutura

```text
src/components/Card/
├── Card.jsx
├── Card.module.css    ← mesmo nome do componente
└── index.js
```

```jsx
import styles from "./Card.module.css";
```

## Modules vs alternativas

| | CSS Modules | CSS global | Styled Components |
| --- | --- | --- | --- |
| Escopo | Local (hash) | Global | Local (runtime) |
| Sintaxe | CSS puro | CSS puro | CSS-in-JS |
| Build | Vite processa | Nenhum | Biblioteca extra |
| Variáveis CSS | Sim | Sim | Sim |

## Erros comuns

| Erro | Sintoma |
| --- | --- |
| `Card.css` sem `.module` | CSS vira global — pode colidir |
| `styles["minha-classe"]` vs `styles.minhaClasse` | Modules converte `kebab-case` → use camelCase ou colchetes |
| Classe de outro componente | `styles` só tem classes do próprio arquivo |
| Tentar estilizar `body` no module | Module é local — `body` vai em `index.css` |

## Resumo

- `*.module.css` = CSS com escopo automático por arquivo
- `import styles from "./X.module.css"` — objeto com as classes
- `styles.nome` gera classe única `X_nome__hash`
- O padrão recomendado para estilos de componente em React
