# FE05-01 — Context: Introdução

## O que é o Context API

Mecanismo nativo do React para **compartilhar dados em profundidade** sem prop drilling — o componente "consumidor" puxa o dado direto, não importa onde esteja na árvore.

```jsx
// criar o contexto
const TemaContext = createContext("claro");

// prover (lá em cima)
<TemaContext.Provider value="escuro">
  <App />
</TemaContext.Provider>

// consumir (lá embaixo, qualquer nível)
const tema = useContext(TemaContext);
```

## As três peças

### 1. createContext — criar o contexto

```jsx
import { createContext } from "react";

export const TemaContext = createContext("claro"); // valor padrão
```

O valor padrão só é usado quando **não há Provider** acima.

### 2. Provider — fornecer o valor

```jsx
<TemaContext.Provider value={tema}>
  {/* toda a árvore dentro enxerga `tema` */}
</TemaContext.Provider>
```

Qualquer componente dentro do Provider — em qualquer profundidade — pode consumir.

### 3. useContext — consumir o valor

```jsx
import { useContext } from "react";

function Botao() {
  const tema = useContext(TemaContext);
  return <button className={tema}>...</button>;
}
```

## O contexto guarda qualquer coisa

```jsx
// String
<ThemeContext.Provider value="escuro">

// Objeto
<UsuarioContext.Provider value={{ nome: "Ana", admin: true }}>

// Estado + setter (o mais comum)
<UsuarioContext.Provider value={{ usuario, setUsuario }}>

// Múltiplos contextos
<AuthContext.Provider value={auth}>
  <ThemeContext.Provider value={tema}>
    <App />
  </ThemeContext.Provider>
</AuthContext.Provider>
```

## Onde vive o Context — a pasta contexts

```text
src/
├── contexts/
│   ├── UsuarioContext.jsx
│   ├── TemaContext.jsx
│   └── CarrinhoContext.jsx
├── components/
└── App.jsx
```

## Estrutura típica de um contexto

```jsx
// contexts/UsuarioContext.jsx
import { createContext, useState, useContext } from "react";

export const UsuarioContext = createContext(null);

export function UsuarioProvider({ children }) {
  const [usuario, setUsuario] = useState(null);

  return (
    <UsuarioContext.Provider value={{ usuario, setUsuario }}>
      {children}
    </UsuarioContext.Provider>
  );
}

// Hook customizado — consome mais limpo
export function useUsuario() {
  return useContext(UsuarioContext);
}
```

```jsx
// App.jsx
import { UsuarioProvider } from "./contexts/UsuarioContext";

function App() {
  return (
    <UsuarioProvider>
      <Rotas />
    </UsuarioProvider>
  );
}
```

```jsx
// qualquer componente
import { useUsuario } from "../contexts/UsuarioContext";

function Header() {
  const { usuario } = useUsuario();
  return <p>Olá, {usuario?.nome}</p>;
}
```

## Re-render — a armadilha

Quando o `value` do Provider muda, **todos os consumidores re-renderizam** — mesmo os que usam só um pedaço:

```jsx
// ❌ objeto novo a cada render — todos re-renderizam
<Provider value={{ usuario, setUsuario }}>

// ✅ memoizado — só re-renderiza se usuario mudar
const valor = useMemo(() => ({ usuario, setUsuario }), [usuario]);
<Provider value={valor}>
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useContext` sem Provider | Valor padrão ou `null` — sempre providencie |
| Objeto no `value` sem `useMemo` | Re-render de todos os consumidores |
| Um contexto gigante | Divida: Auth, Tema, Carrinho — contextos separados |
| Context para estado local | Context é global — useState local é mais leve |

## Resumo

- Context = dados compartilhados em profundidade sem drilling
- `createContext` → `Provider` (value) → `useContext` (consumo)
- Pasta `contexts/` + Provider customizado + hook `useX` = padrão
- `useMemo` no `value` evita re-renders desnecessários
