# FE05-02 — Context: Primeiro Exemplo Prático

## O cenário — tema claro/escuro

App onde vários componentes precisam saber o tema atual — e um botão que alterna.

## Passo 1 — criar o contexto

```jsx
// contexts/TemaContext.jsx
import { createContext, useState, useContext } from "react";

export const TemaContext = createContext(null);
```

## Passo 2 — criar o Provider

```jsx
export function TemaProvider({ children }) {
  const [tema, setTema] = useState("claro");

  function alternarTema() {
    setTema(t => t === "claro" ? "escuro" : "claro");
  }

  return (
    <TemaContext.Provider value={{ tema, alternarTema }}>
      {children}
    </TemaContext.Provider>
  );
}
```

## Passo 3 — envolver a aplicação

```jsx
// App.jsx ou main.jsx
import { TemaProvider } from "./contexts/TemaContext";

function App() {
  return (
    <TemaProvider>
      <Header />
      <Conteudo />
    </TemaProvider>
  );
}
```

## Passo 4 — consumir nos componentes

```jsx
import { useContext } from "react";
import { TemaContext } from "../contexts/TemaContext";

function Header() {
  const { tema, alternarTema } = useContext(TemaContext);

  return (
    <header className={`header ${tema}`}>
      <h1>Meu App</h1>
      <button onClick={alternarTema}>
        {tema === "claro" ? "🌙" : "☀️"}
      </button>
    </header>
  );
}
```

```jsx
function Card() {
  const { tema } = useContext(TemaContext);
  return <div className={`card ${tema}`}>...</div>;
}
```

## Versão limpa — hook customizado

```jsx
// dentro do TemaContext.jsx
export function useTema() {
  const contexto = useContext(TemaContext);

  if (!contexto) {
    throw new Error("useTema deve estar dentro de TemaProvider");
  }

  return contexto;
}
```

```jsx
// nos componentes — mais limpo e seguro
import { useTema } from "../contexts/TemaContext";

function Header() {
  const { tema, alternarTema } = useTema();
  // ...
}
```

O `throw` dentro do hook **detecta o erro cedo** — em vez de quebrar com `undefined`.

## Otimização — useMemo no value

```jsx
export function TemaProvider({ children }) {
  const [tema, setTema] = useState("claro");

  const alternarTema = useCallback(() => {
    setTema(t => t === "claro" ? "escuro" : "claro");
  }, []);

  const valor = useMemo(
    () => ({ tema, alternarTema }),
    [tema, alternarTema]
  );

  return (
    <TemaContext.Provider value={valor}>
      {children}
    </TemaContext.Provider>
  );
}
```

Sem `useMemo`: toda renderização do Provider cria um objeto novo → todos os consumidores re-renderizam.

## Aplicando o tema no CSS

```css
.card.claro {
  background: #fff;
  color: #222;
}

.card.escuro {
  background: #1e1e1e;
  color: #eee;
}
```

Ou com variáveis CSS:

```jsx
useEffect(() => {
  document.documentElement.dataset.tema = tema;
}, [tema]);
```

```css
:root[data-tema="escuro"] {
  --fundo: #1e1e1e;
  --texto: #eee;
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useContext` fora do Provider | `undefined` ou erro — cheque a árvore |
| `value={{ ... }}` sem useMemo | Re-renders desnecessários |
| Esquecer o `children` no Provider | O Provider precisa renderizar os filhos |
| Contexto em arquivo JSX de componente | Pasta `contexts/` separada |

## Resumo

- `createContext` + Provider + `useContext` = a trinca
- Hook `useX` customizado encapsula o consumo e valida o Provider
- `useMemo`/`useCallback` no `value` evita re-renders
- Tema é o caso clássico — mas serve pra auth, idioma, carrinho
