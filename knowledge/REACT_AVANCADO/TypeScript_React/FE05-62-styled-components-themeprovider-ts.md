# FE05-62 — TypeScript no React: Styled Components — ThemeProvider

## O tema tipado completo

```typescript
// theme.ts
export interface Tema {
  cores: {
    primaria: string;
    secundaria: string;
    fundo: string;
    fundoCard: string;
    texto: string;
    textoSecundario: string;
    borda: string;
    perigo: string;
  };
  fontes: {
    corpo: string;
    titulo: string;
  };
  espacamento: {
    xs: string;
    sm: string;
    md: string;
    lg: string;
  };
  raio: string;
  sombra: string;
}

export const temaClaro: Tema = {
  cores: {
    primaria: "#7159c1",
    secundaria: "#ab59c1",
    fundo: "#f8f9fa",
    fundoCard: "#ffffff",
    texto: "#1a1a1a",
    textoSecundario: "#666",
    borda: "#e0e0e0",
    perigo: "#e74c3c"
  },
  fontes: { corpo: "Inter, sans-serif", titulo: "Poppins, sans-serif" },
  espacamento: { xs: "4px", sm: "8px", md: "16px", lg: "24px" },
  raio: "8px",
  sombra: "0 2px 8px rgba(0,0,0,0.1)"
};

export const temaEscuro: Tema = {
  cores: {
    primaria: "#9b7ede",
    secundaria: "#c78bde",
    fundo: "#121212",
    fundoCard: "#1e1e1e",
    texto: "#eeeeee",
    textoSecundario: "#aaa",
    borda: "#333",
    perigo: "#ff6b6b"
  },
  fontes: { corpo: "Inter, sans-serif", titulo: "Poppins, sans-serif" },
  espacamento: { xs: "4px", sm: "8px", md: "16px", lg: "24px" },
  raio: "8px",
  sombra: "0 2px 8px rgba(0,0,0,0.4)"
};
```

## O DefaultTheme — o contrato

```typescript
// styled.d.ts
import "styled-components";
import type { Tema } from "./theme";

declare module "styled-components" {
  export interface DefaultTheme extends Tema {}
}
```

Todo `theme.cores.primaria` agora tem autocomplete e type-check.

## O ThemeProvider com estado

```tsx
// contexts/TemaProvider.tsx
import { ThemeProvider as StyledThemeProvider } from "styled-components";
import { temaClaro, temaEscuro, Tema } from "../theme";

interface TemaContextType {
  tema: "claro" | "escuro";
  alternar: () => void;
}

const TemaContext = createContext<TemaContextType | null>(null);

export function TemaProvider({ children }: { children: ReactNode }) {
  const [tema, setTema] = useState<"claro" | "escuro">("claro");

  const alternar = () =>
    setTema(t => t === "claro" ? "escuro" : "claro");

  const temaAtual = tema === "claro" ? temaClaro : temaEscuro;

  return (
    <TemaContext.Provider value={{ tema, alternar }}>
      <StyledThemeProvider theme={temaAtual}>
        {children}
      </StyledThemeProvider>
    </TemaContext.Provider>
  );
}
```

## GlobalStyle com tema

```tsx
const GlobalStyle = createGlobalStyle`
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: ${({ theme }) => theme.fontes.corpo};
    background: ${({ theme }) => theme.cores.fundo};
    color: ${({ theme }) => theme.cores.texto};
    transition: background 0.3s, color 0.3s;
  }
`;

// uso
<TemaProvider>
  <GlobalStyle />
  <App />
</TemaProvider>
```

## Componente usando o tema

```tsx
const Card = styled.div`
  background: ${({ theme }) => theme.cores.fundoCard};
  border: 1px solid ${({ theme }) => theme.cores.borda};
  border-radius: ${({ theme }) => theme.raio};
  padding: ${({ theme }) => theme.espacamento.md};
  box-shadow: ${({ theme }) => theme.sombra};

  h3 {
    font-family: ${({ theme }) => theme.fontes.titulo};
    color: ${({ theme }) => theme.cores.texto};
  }

  p {
    color: ${({ theme }) => theme.cores.textoSecundario};
  }
`;
```

## O toggle

```tsx
function ToggleTema() {
  const { tema, alternar } = useTema();

  return (
    <button onClick={alternar} aria-label="Alternar tema">
      {tema === "claro" ? "🌙" : "☀️"}
    </button>
  );
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `DefaultTheme` vazio | `extends Tema` — tipagem completa |
| Tema sem `styled.d.ts` | `theme` é `any` — sem autocomplete |
| GlobalStyle sem theme | `createGlobalStyle` recebe `theme` automaticamente |
| Tema mutado | `temaClaro`/`temaEscuro` são objetos imutáveis |

## Resumo

- `Tema` interface define o contrato; `DefaultTheme extends Tema` tipa tudo
- `ThemeProvider` do styled-components injeta `theme` nas props
- `createGlobalStyle` acessa o `theme` para estilos globais
- `temaClaro`/`temaEscuro` como objetos separados — troca limpa
