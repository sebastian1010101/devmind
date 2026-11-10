# FE05-61 — TypeScript no React: Styled Components — Props

## O problema — props sem tipo no styled

```tsx
// ❌ sem tipos — qualquer prop aceita
const Botao = styled.button`
  background: ${props => props.cor}; // cor é any
`;

// ✅ com interface — props tipadas
interface BotaoProps {
  $variante: "primario" | "secundario" | "perigo";
  $tamanho?: "sm" | "md" | "lg";
}

const Botao = styled.button<BotaoProps>`
  background: ${({ $variante, theme }) =>
    $variante === "perigo" ? theme.cores.perigo : theme.cores.primaria};
  padding: ${({ $tamanho = "md" }) => `0.5rem ${$tamanho === "lg" ? "2rem" : "1rem"}`};
`;
```

## Transient props — o prefixo `$`

```tsx
// props com $ não vazam pro DOM — styled-components filtra
interface Props {
  $ativo: boolean;
  $cor?: string;
}

const Item = styled.li<Props>`
  background: ${({ $ativo }) => $ativo ? "#e0f2ff" : "transparent"};
`;

// <Item $ativo={true} /> — $ativo não chega no HTML
```

## Tipando o tema — DefaultTheme

```typescript
// styled.d.ts — tipa o theme globalmente
import "styled-components";

declare module "styled-components" {
  export interface DefaultTheme {
    cores: {
      primaria: string;
      secundaria: string;
      fundo: string;
      texto: string;
      perigo: string;
    };
    espacamento: {
      sm: string;
      md: string;
      lg: string;
    };
  }
}
```

```tsx
// agora theme.cores.primaria tem autocomplete
const Card = styled.div`
  background: ${({ theme }) => theme.cores.card};
  color: ${({ theme }) => theme.cores.texto};
`;
```

## Componente com props de estilo + tema

```tsx
interface AlertaProps {
  $tipo: "info" | "sucesso" | "aviso" | "erro";
}

const cores: Record<AlertaProps["$tipo"], string> = {
  info: "#2196F3",
  sucesso: "#4CAF50",
  aviso: "#FF9800",
  erro: "#F44336"
};

const Alerta = styled.div<AlertaProps>`
  background: ${({ $tipo }) => cores[$tipo]}20; // 20% opacidade
  border-left: 4px solid ${({ $tipo }) => cores[$tipo]};
  color: ${({ theme }) => theme.cores.texto};
  padding: ${({ theme }) => theme.espacamento.md};
`;
```

## Estendendo componente tipado

```tsx
// BotaoBase com props tipadas
const BotaoBase = styled.button<{ $perigo?: boolean }>`
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
`;

// extende mantendo os tipos
const BotaoPerigo = styled(BotaoBase)`
  background: red;
  color: white;
`;
```

## O as prop — mudando o elemento

```tsx
const Texto = styled.p`
  font-size: 1rem;
  color: ${({ theme }) => theme.cores.texto};
`;

// renderiza como h2 mantendo os estilos
<Texto as="h2">Título</Texto>
```

## Attrs — props com valor fixo

```tsx
const Icone = styled.span.attrs({
  role: "img",
  "aria-hidden": true
})`
  font-size: 1.2em;
`;
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Prop sem tipo no styled | `styled.div<Props>` — interface no generic |
| Prop vazando pro DOM | Prefixo `$` — transient prop |
| `theme` sem tipo | `styled.d.ts` com `DefaultTheme` |
| `props` sem desestruturação | `({ $variante }) => ...` — mais limpo |

## Resumo

- `styled.tag<Props>` tipa as props do componente
- `$` prefixo = transient prop — não vai pro DOM
- `DefaultTheme` em `styled.d.ts` tipa o `theme`
- `styled(Componente)` estende mantendo tipos
