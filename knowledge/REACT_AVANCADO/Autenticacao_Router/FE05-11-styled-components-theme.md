# FE05-11 — Aula Extra: Styled Components — Theme

## ThemeProvider — tema centralizado

`styled-components` tem `ThemeProvider` próprio — injeta um objeto de tema em **todos os styled components** da árvore via props.

```jsx
import { ThemeProvider } from "styled-components";

const tema = {
  cores: {
    primaria: "#7159c1",
    fundo: "#f5f5f5",
    texto: "#222"
  },
  espacamento: { sm: "8px", md: "16px", lg: "24px" },
  raio: "8px"
};

<ThemeProvider theme={tema}>
  <App />
</ThemeProvider>
```

## Consumindo o tema

Todo styled component recebe `props.theme` automaticamente:

```jsx
const Botao = styled.button`
  background: ${props => props.theme.cores.primaria};
  color: ${props => props.theme.cores.fundo};
  padding: ${props => props.theme.espacamento.md};
  border-radius: ${props => props.theme.raio};
`;
```

Com desestruturação:

```jsx
const Botao = styled.button`
  background: ${({ theme }) => theme.cores.primaria};
`;
```

## Alternância de temas — claro/escuro

```jsx
const temas = {
  claro: {
    fundo: "#fff",
    texto: "#222",
    card: "#f5f5f5"
  },
  escuro: {
    fundo: "#1a1a1a",
    texto: "#eee",
    card: "#2d2d2d"
  }
};

function App() {
  const [tema, setTema] = useState("claro");

  return (
    <ThemeProvider theme={temas[tema]}>
      <GlobalStyle />
      <button onClick={() => setTema(t => t === "claro" ? "escuro" : "claro")}>
        Alternar
      </button>
      {/* styled components usam theme.* */}
    </ThemeProvider>
  );
}
```

Mudou o tema → `ThemeProvider` passa novo objeto → styled components recalculam.

## Tipando o tema (TypeScript)

```typescript
// styled.d.ts
import "styled-components";

declare module "styled-components" {
  export interface DefaultTheme {
    cores: {
      primaria: string;
      fundo: string;
      texto: string;
    };
    espacamento: {
      sm: string;
      md: string;
      lg: string;
    };
  }
}
```

Agora `theme.cores.primaria` tem autocomplete e type-check.

## Estilos globais com tema

```jsx
const GlobalStyle = createGlobalStyle`
  body {
    background: ${({ theme }) => theme.cores.fundo};
    color: ${({ theme }) => theme.cores.texto};
    font-family: sans-serif;
  }
`;

<ThemeProvider theme={temas[tema]}>
  <GlobalStyle /> {/* herda o theme automaticamente */}
  <App />
</ThemeProvider>
```

## Combinando com props normais

```jsx
const Botao = styled.button`
  background: ${({ theme, $perigo }) =>
    $perigo ? theme.cores.perigo : theme.cores.primaria};
`;
```

`$perigo` é transient prop (não vaza pro DOM) + `theme` do Provider.

## Funções auxiliares de tema

```jsx
// helpers dentro do tema
const tema = {
  cores: { primaria: "#7159c1" },
  botao: (variante) => {
    const estilos = {
      primario: "background: #7159c1; color: #fff;",
      outline: "border: 2px solid #7159c1; color: #7159c1;"
    };
    return estilos[variante];
  }
};

const Btn = styled.button`
  ${({ theme, $v }) => theme.botao($v)}
`;
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Theme fora do Provider | `props.theme` undefined — envolva a árvore |
| `theme` como prop normal | Use transient `$` para props de estilo |
| Tipagem ausente | `styled.d.ts` com `DefaultTheme` |
| Tema mutado direto | Novo objeto `temas[tema]` — imutável |

## Resumo

- `ThemeProvider` injeta `theme` em todo styled component
- `props.theme.cores.primaria` (ou desestruturado `{ theme }`)
- Alternância = trocar o objeto do `theme` no Provider
- `styled.d.ts` tipa o `DefaultTheme` no TypeScript
