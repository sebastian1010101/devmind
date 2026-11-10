# FE04-19 — Atividade: Criando Reset CSS

## Objetivo

Criar o CSS de base do projeto React — reset, variáveis e estilos globais que toda aplicação precisa antes de estilizar componentes.

## O arquivo de reset

```css
/* src/index.css */

/* ============ RESET ============ */
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

img,
picture,
video,
canvas {
  display: block;
  max-width: 100%;
}

input,
button,
textarea,
select {
  font: inherit;
}

p,
h1, h2, h3, h4, h5, h6 {
  overflow-wrap: break-word;
}

/* ============ VARIÁVEIS ============ */
:root {
  --cor-primaria: #3498db;
  --cor-primaria-hover: #2980b9;
  --cor-fundo: #ffffff;
  --cor-texto: #222222;
  --cor-texto-suave: #666666;
  --cor-borda: #e0e0e0;
  --cor-erro: #e74c3c;
  --cor-sucesso: #22c55e;

  --fonte-base: 16px;
  --raio-borda: 8px;
  --espaco: 1rem;

  --transicao: 0.2s ease;
}

/* ============ BASE ============ */
html {
  font-size: var(--fonte-base);
}

body {
  font-family: system-ui, -apple-system, sans-serif;
  background: var(--cor-fundo);
  color: var(--cor-texto);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

#root {
  min-height: 100vh;
}

/* ============ UTILITÁRIOS ============ */
button {
  cursor: pointer;
  border: none;
  background: none;
  transition: var(--transicao);
}

a {
  color: var(--cor-primaria);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

ul, ol {
  list-style: none;
}
```

## Importando no projeto

```jsx
// src/main.jsx — já vem no template do Vite
import "./index.css";
```

O `index.css` é carregado globalmente — tudo que está nele afeta toda a aplicação.

## Testando o reset

```jsx
// src/App.jsx
function App() {
  return (
    <div>
      <h1>Reset CSS</h1>
      <p>Parágrafos sem margem padrão do navegador.</p>
      <button>Botão sem estilo nativo</button>
      <ul>
        <li>Lista sem bullets</li>
        <li>Item dois</li>
      </ul>
    </div>
  );
}
```

Sem o reset, cada navegador aplicaria estilos diferentes — margens de `<h1>` diferentes, bullets diferentes, fonte de `<button>` diferente.

## Desafio — modo escuro com variáveis

```css
:root[data-tema="escuro"] {
  --cor-fundo: #1a1a2e;
  --cor-texto: #eeeeee;
  --cor-borda: #333355;
}
```

```jsx
// Toggle de tema
document.documentElement.dataset.tema = "escuro";
```

## Critérios de verificação

- Reset com `box-sizing: border-box` universal
- Imagens com `max-width: 100%` (responsivas)
- Variáveis CSS no `:root` para cores/tipografia
- `font: inherit` em inputs e buttons
- `#root` com `min-height: 100vh` para layouts de página inteira
- Semântica: variáveis nomeadas por função (`--cor-primaria`), não por cor (`--azul`)

## Por que esse reset específico

| Regra | Problema que resolve |
| --- | --- |
| `box-sizing: border-box` | Padding não estoura `width` |
| `img { max-width: 100% }` | Imagem não vaza do container |
| `font: inherit` em inputs | Input herda a fonte — não fica com a do sistema |
| `button { border: none }` | Remove borda padrão do navegador |
| `ul { list-style: none }` | Remove bullets — listas de nav/cards limpas |
