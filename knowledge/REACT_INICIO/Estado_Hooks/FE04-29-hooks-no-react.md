# FE04-29 — Hooks no React

## O que são Hooks

**Hooks** são funções especiais que permitem a componentes de função usar recursos do React — estado, ciclo de vida, contexto, refs. Introduzidos no React 16.8, eliminaram a necessidade de componentes de classe.

```jsx
import { useState } from "react";

function Contador() {
  const [contagem, setContagem] = useState(0); // ← hook
  return <button onClick={() => setContagem(c => c + 1)}>{contagem}</button>;
}
```

## Os hooks essenciais

| Hook | O que faz |
| --- | --- |
| `useState` | Estado local do componente |
| `useEffect` | Efeitos colaterais (fetch, timers, subscriptions) |
| `useRef` | Referência mutável / acesso ao DOM |
| `useContext` | Consome contexto global |
| `useMemo` | Memoriza cálculos custosos |
| `useCallback` | Memoriza funções |
| `useReducer` | Estado complexo com reducer |

## As regras dos Hooks

Regras invioláveis — o React depende da ordem de chamada:

### 1. Só no topo do componente

```jsx
// ❌ Nunca dentro de condicional, loop ou função aninhada
function App() {
  if (condicao) {
    const [x, setX] = useState(0); // PROIBIDO
  }
}

// ✅ Sempre no nível superior, incondicionalmente
function App() {
  const [x, setX] = useState(0);

  if (condicao) { /* pode usar x aqui */ }
}
```

### 2. Só em componentes React ou hooks customizados

```jsx
// ✅ Em componente
function App() { const [x, setX] = useState(0); }

// ✅ Em hook customizado (função que começa com "use")
function useMeuHook() { const [x, setX] = useState(0); }

// ❌ Em função comum — proibido
function util() { const [x, setX] = useState(0); }
```

### Por que essas regras existem

O React rastreia hooks **pela ordem de chamada** — cada `useState` é "o primeiro", "o segundo", etc. Se a ordem muda entre renders (hook dentro de `if`), o React associa o estado errado.

## Nomeação: o prefixo `use`

Hooks customizados **devem** começar com `use` — é como o ESLint sabe que é um hook e aplica as regras:

```jsx
// ✅ Convenção obrigatória
function useLocalStorage() { }
function useFetch() { }
function useToggle() { }

// ❌ Não é reconhecido como hook
function localStorageHelper() { }
```

## Os padrões principais

### Estado

```jsx
const [valor, setValor] = useState(inicial);
```

### Efeito colateral

```jsx
useEffect(() => {
  // roda depois da renderização
  return () => { /* limpeza */ };
}, [dependencias]);
```

### Referência ao DOM

```jsx
const inputRef = useRef(null);
<input ref={inputRef} />
```

## Hooks vs funções comuns

| | Hook | Função comum |
| --- | --- | --- |
| Prefixo | `use` | Qualquer |
| Onde roda | Só em componente/hook | Qualquer lugar |
| Tem estado próprio | Sim | Não |
| Re-renderiza ao mudar | Sim (se useState/useReducer) | Não |

## Resumo

- Hooks = funções `use*` que dão superpoderes a componentes de função
- Regras: só no topo, só em componente ou hook customizado
- `useState` (estado), `useEffect` (efeitos) e `useRef` (refs) são os três essenciais
- A ordem de chamada dos hooks é o mecanismo de rastreamento do React
