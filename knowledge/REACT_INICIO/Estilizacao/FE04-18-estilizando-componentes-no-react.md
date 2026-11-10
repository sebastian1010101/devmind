# FE04-18 — Estilizando Componentes no React

## As opções de estilização

React não impõe uma forma de estilizar — existem várias abordagens, cada uma com trade-offs:

| Abordagem | Escopo | Quando usar |
| --- | --- | --- |
| CSS global | Global | Reset, variáveis, base |
| CSS arquivo por componente | Global (mas organizado) | Projetos pequenos |
| CSS Modules | Local ao componente | Padrão recomendado |
| Inline `style={{}}` | Elemento | Valores dinâmicos |
| Styled Components | Local + tema | Design systems |
| Tailwind | Utility classes | Prototipagem rápida |

## CSS global — index.css

Para estilos que afetam tudo: reset, variáveis, tipografia base:

```css
/* src/index.css — importado no main.jsx */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --cor-primaria: #3498db;
  --cor-texto: #222;
}

body {
  font-family: system-ui, sans-serif;
  color: var(--cor-texto);
}
```

```jsx
// main.jsx — já vem no template do Vite
import "./index.css";
```

## CSS por componente — arquivo comum

```jsx
// Button.jsx
import "./Button.css";

function Button() {
  return <button className="botao">Clique</button>;
}
```

```css
/* Button.css */
.botao {
  background: var(--cor-primaria);
  padding: 0.5rem 1rem;
}
```

⚠️ O CSS importado é **global** — `.botao` vaza para qualquer componente que use a mesma classe. Em projetos maiores, prefira CSS Modules.

## Inline style — objeto JavaScript

Para valores que dependem de estado/props:

```jsx
function Barra({ progresso }) {
  return (
    <div style={{
      width: `${progresso}%`,
      background: progresso > 80 ? "green" : "orange",
      height: "8px"
    }} />
  );
}
```

Regras: camelCase nas propriedades, valores numéricos viram `px` automático, objeto — não string.

## className dinâmico

Alternando classes por estado:

```jsx
function Botao({ ativo }) {
  return (
    <button className={ativo ? "botao botao--ativo" : "botao"}>
      Clique
    </button>
  );
}
```

Ou com array + `filter`/`join` para várias classes:

```jsx
const classes = [
  "botao",
  ativo && "botao--ativo",
  grande && "botao--grande"
].filter(Boolean).join(" ");

<button className={classes}>Clique</button>
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `class=` em vez de `className` | JSX usa `className` |
| `style="color: red"` | `style={{ color: "red" }}` — objeto |
| CSS global com nomes genéricos | `.card` vaza — use BEM ou Modules |
| Estilizar `body` em CSS de componente | `body` é global — pertence ao `index.css` |

## Resumo

- `index.css` para reset, variáveis e base global
- CSS por componente funciona, mas é global — cuidado com colisões
- `style={{}}` para valores dinâmicos
- `className` dinâmico com ternário ou array
- CSS Modules (próximo tópico) resolve o escopo de verdade
