# FE05-31 — Atividade: Redux — Primeiro Reducer + useSelector

## Objetivo

Criar a primeira store Redux — um contador simples — e ler o valor com `useSelector`.

## Passo 1 — o reducer

```jsx
// store/contadorReducer.js
const estadoInicial = { valor: 0 };

export function contadorReducer(state = estadoInicial, action) {
  switch (action.type) {
    case "incrementar":
      return { ...state, valor: state.valor + 1 };
    case "decrementar":
      return { ...state, valor: state.valor - 1 };
    case "resetar":
      return { ...state, valor: 0 };
    default:
      return state; // obrigatório — retorna o estado intacto
  }
}
```

## Passo 2 — a store

```jsx
// store/index.js
import { createStore } from "redux";
import { contadorReducer } from "./contadorReducer";

export const store = createStore(contadorReducer);
```

## Passo 3 — o Provider

```jsx
// main.jsx
import { Provider } from "react-redux";
import { store } from "./store";

<Provider store={store}>
  <App />
</Provider>
```

## Passo 4 — o componente

```jsx
import { useSelector, useDispatch } from "react-redux";

function Contador() {
  const valor = useSelector(state => state.valor);
  const dispatch = useDispatch();

  return (
    <div>
      <button onClick={() => dispatch({ type: "decrementar" })}>−</button>
      <span>{valor}</span>
      <button onClick={() => dispatch({ type: "incrementar" })}>+</button>
      <button onClick={() => dispatch({ type: "resetar" })}>Reset</button>
    </div>
  );
}
```

## useSelector — a seleção fina

```jsx
// lê só o que precisa — re-render cirúrgico
const valor = useSelector(s => s.valor);

// deriva no seletor
const dobro = useSelector(s => s.valor * 2);
const ePar = useSelector(s => s.valor % 2 === 0);
```

## O erro clássico — mutação no reducer

```jsx
// ❌ mutação — React não detecta a mudança
case "incrementar":
  state.valor += 1;
  return state;

// ✅ novo objeto — React compara referência
case "incrementar":
  return { ...state, valor: state.valor + 1 };
```

## Estado inicial — o default do reducer

```jsx
function contadorReducer(state = { valor: 0 }, action) { ... }
//                        ↑ este é o estado inicial
```

Quando a store é criada, o reducer roda uma vez com `state = undefined` → o default entra.

## Desafios extras

### Desafio A — incremento customizado

```jsx
case "incrementarPor":
  return { ...state, valor: state.valor + action.payload };

dispatch({ type: "incrementarPor", payload: 5 });
```

### Desafio B — histórico

```jsx
const estadoInicial = { valor: 0, historico: [] };

case "incrementar":
  return {
    valor: state.valor + 1,
    historico: [...state.historico, state.valor + 1]
  };
```

### Desafio C — mínimo/máximo

```jsx
case "incrementar":
  return {
    ...state,
    valor: Math.min(state.valor + 1, state.max) // limite superior
  };
```

## Critérios de verificação

- Reducer retorna novo objeto — nunca muta
- `default:` retorna `state` — obrigatório
- `useSelector(s => s.valor)` — seleção fina
- `dispatch({ type: "..." })` — action com type

## Erros comuns

| Erro | Correção |
| --- | --- |
| `state.valor++` | Mutou — retorne `{...state, valor: state.valor + 1}` |
| `default` sem return | Sempre retorne `state` no default |
| `useSelector()` sem seletor | Selecione o pedaço — `s => s.valor` |
| `dispatch` sem `type` | `{ type: "incrementar" }` — obrigatório |
