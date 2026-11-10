# FE05-30 — Redux: Introdução

## O que é o Redux

Biblioteca de **estado global previsível** — uma única store central, mudanças só através de "actions" descritas, e funções puras (reducers) que calculam o novo estado.

## Os três princípios

### 1. Single Source of Truth — uma única store

```jsx
// TODO o estado do app vive num objeto único
{
  usuario: { nome: "Ana", logado: true },
  carrinho: { itens: [...] },
  tema: "escuro"
}
```

### 2. State é read-only — só actions mudam

```jsx
// ❌ proibido
state.contador = 5;

// ✅ você despacha uma action descrevendo o que aconteceu
dispatch({ type: "contador/incrementar" });
```

### 3. Mudanças via funções puras — reducers

```jsx
// reducer = (estadoAtual, action) => novoEstado
function contadorReducer(state = 0, action) {
  if (action.type === "incrementar") return state + 1;
  return state;
}
```

## O fluxo Redux

```text
UI clica botão
  → dispatch(action)              { type: "incrementar" }
  → reducer(state, action)         calcula novo estado
  → store atualiza
  → componentes com useSelector    re-renderizam
```

## As peças

| Peça | O que é | Exemplo |
| --- | --- | --- |
| **Store** | O estado global | `createStore(reducer)` |
| **Action** | Objeto descrevendo o evento | `{ type: "add", payload: {...} }` |
| **Reducer** | Função pura que calcula novo estado | `(state, action) => newState` |
| **Dispatch** | Envia a action para a store | `dispatch(action)` |
| **Selector** | Lê um pedaço do estado | `useSelector(s => s.contador)` |

## Instalação

```bash
npm install redux react-redux
```

## Setup mínimo

```jsx
// store.js
import { createStore } from "redux";

function contadorReducer(state = { valor: 0 }, action) {
  switch (action.type) {
    case "incrementar":
      return { valor: state.valor + 1 };
    case "decrementar":
      return { valor: state.valor - 1 };
    default:
      return state;
  }
}

export const store = createStore(contadorReducer);
```

```jsx
// main.jsx
import { Provider } from "react-redux";
import { store } from "./store";

<Provider store={store}>
  <App />
</Provider>
```

```jsx
// componente
import { useSelector, useDispatch } from "react-redux";

function Contador() {
  const valor = useSelector(s => s.valor);
  const dispatch = useDispatch();

  return (
    <button onClick={() => dispatch({ type: "incrementar" })}>
      {valor}
    </button>
  );
}
```

## Redux vs Context vs Zustand

| | Redux | Context | Zustand |
| --- | --- | --- | --- |
| Boilerplate | Alto | Baixo | Baixo |
| DevTools | Excelente (time travel) | Nenhum | Bom (middleware) |
| Estrutura | Rígida, previsível | Livre | Flexível |
| Re-renders | Otimizado (selectors) | Todos os consumidores | Seletores finos |
| Curva | Alta | Baixa | Baixa |
| Ideal para | Apps grandes, times grandes | Auth/tema | Apps médias/grandes |

## Redux Toolkit — a forma moderna

O Redux "clássico" é verboso. **Redux Toolkit (RTK)** é a forma oficial moderna:

```bash
npm install @reduxjs/toolkit react-redux
```

```jsx
import { createSlice, configureStore } from "@reduxjs/toolkit";

const contadorSlice = createSlice({
  name: "contador",
  initialState: { valor: 0 },
  reducers: {
    incrementar: (state) => { state.valor += 1 } // "mutável" (Immer por dentro)
  }
});

const store = configureStore({
  reducer: { contador: contadorSlice.reducer }
});
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Mutar state no reducer | Retorne novo objeto — `{...state, campo: novo}` |
| Action sem `type` | Toda action precisa de `type` |
| `useSelector` retornando objeto novo | `shallowEqual` ou seletores separados |
| Redux pra estado local | `useState` — Redux é pra estado global compartilhado |

## Resumo

- Redux = store única + actions descritivas + reducers puros
- `dispatch(action)` → `reducer` calcula → `useSelector` lê
- Redux Toolkit (`createSlice`) é a forma moderna — menos boilerplate
- Para apps grandes e times; para apps menores, Zustand é mais leve
