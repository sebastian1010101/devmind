# FE04-44 — Styled Components: Estilos Globais vs Estilos Pontuais

## Os dois níveis

Styled Components cobre dois escopos:

- **Global** — reset, variáveis, tipografia base (uma vez, para toda a app)
- **Pontual** — estilos de um componente específico

## createGlobalStyle — o reset global

```jsx
// src/styles/GlobalStyle.js
import { createGlobalStyle } from "styled-components";

const GlobalStyle = createGlobalStyle`
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
    background: var(--cor-fundo);
    color: var(--cor-texto);
    -webkit-font-smoothing: antialiased;
  }

  button {
    cursor: pointer;
    font: inherit;
    border: none;
  }
`;

export default GlobalStyle;
```

```jsx
// src/main.jsx ou App.jsx — monta uma vez no topo
import GlobalStyle from "./styles/GlobalStyle";

function App() {
  return (
    <>
      <GlobalStyle />
      <Header />
      <Main />
    </>
  );
}
```

`<GlobalStyle />` é um componente que injeta CSS global — renderiza uma vez e afeta tudo.

## Estilos pontuais — por componente

```jsx
// src/components/Card/Card.jsx
import styled from "styled-components";

const Container = styled.article`
  border: 1px solid var(--cor-borda);
  border-radius: 8px;
  padding: 1rem;
`;

const Titulo = styled.h3`
  font-size: 1.25rem;
  color: var(--cor-texto);
`;

function Card({ titulo, children }) {
  return (
    <Container>
      <Titulo>{titulo}</Titulo>
      {children}
    </Container>
  );
}
```

Cada styled component é local — `Container` e `Titulo` só existem para o `Card`.

## A divisão de responsabilidade

| Vai no global | Vai no componente |
| --- | --- |
| Reset (`*`, `body`) | Estilo do componente |
| Variáveis CSS (`:root`) | Variações locais |
| Tipografia base | Fonte específica se diferente |
| `button`, `a` base | Botão estilizado |
| Layout da página (`#root`) | Grid interno do componente |

## Theming — o caso forte do global

`ThemeProvider` + `createGlobalStyle` = tema dinâmico real:

```jsx
import { ThemeProvider } from "styled-components";

const temaClaro = {
  fundo: "#fff",
  texto: "#222",
  primaria: "#3498db"
};

const temaEscuro = {
  fundo: "#1a1a2e",
  texto: "#eee",
  primaria: "#5dade2"
};
```

```jsx
// GlobalStyle usa o tema
const GlobalStyle = createGlobalStyle`
  body {
    background: ${props => props.theme.fundo};
    color: ${props => props.theme.texto};
  }
`;

// Componentes também
const Botao = styled.button`
  background: ${props => props.theme.primaria};
`;
```

```jsx
function App() {
  const [escuro, setEscuro] = useState(false);

  return (
    <ThemeProvider theme={escuro ? temaEscuro : temaClaro}>
      <GlobalStyle />
      <button onClick={() => setEscuro(e => !e)}>Alternar tema</button>
      <Resto />
    </ThemeProvider>
  );
}
```

Cada componente styled acessa `props.theme` — troca de tema atualiza tudo.

## Erros comuns

| Erro | Correção |
| --- | --- |
| `<GlobalStyle />` dentro de componente | Monte uma vez no topo (`App`/`main`) |
| Reset dentro de styled pontual | Reset é global — vai no `createGlobalStyle` |
| `theme` undefined | Falta `ThemeProvider` envolvendo a árvore |
| Estilos globais e pontuais misturados | Global = base/tema; pontual = o componente em si |

## Resumo

- `createGlobalStyle` — reset, variáveis e base global (monta uma vez)
- `styled.tag` — estilos locais do componente
- `ThemeProvider` + `props.theme` — theming real que propaga por toda a árvore
- Divisão: global para base/tema, pontual para o componente
