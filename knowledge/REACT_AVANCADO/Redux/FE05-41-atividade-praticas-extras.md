# FE05-41 — Atividade: Redux — Práticas Extras

## Objetivo

Consolidar tudo — Redux Toolkit moderno, seletores derivados, persistência, e quando usar cada ferramenta.

## O contador com Redux Toolkit

```jsx
// store/contadorSlice.js
import { createSlice } from "@reduxjs/toolkit";

const contadorSlice = createSlice({
  name: "contador",
  initialState: { valor: 0, passo: 1, historico: [] },
  reducers: {
    incrementar: (s) => {
      s.valor += s.passo;
      s.historico.push(s.valor);
    },
    decrementar: (s) => {
      s.valor -= s.passo;
    },
    setPasso: (s, a) => {
      s.passo = a.payload;
    },
    resetar: (s) => {
      s.valor = 0;
      s.historico = [];
    }
  }
});

export const { incrementar, decrementar, setPasso, resetar } =
  contadorSlice.actions;
export default contadorSlice.reducer;
```

O `createSlice` usa **Immer** — "mutar" `s.valor` é seguro, ele gera imutável.

## A store com RTK

```jsx
// store/index.js
import { configureStore } from "@reduxjs/toolkit";
import contadorReducer from "./contadorSlice";
import authReducer from "./authSlice";

export const store = configureStore({
  reducer: {
    contador: contadorReducer,
    auth: authReducer
  }
});
```

## Async com createAsyncThunk

```jsx
import { createAsyncThunk } from "@reduxjs/toolkit";

export const buscarProdutos = createAsyncThunk(
  "produtos/buscar",
  async (_, { rejectWithValue }) => {
    try {
      const res = await api.get("/produtos");
      return res.data;
    } catch (e) {
      return rejectWithValue(e.response?.data?.message);
    }
  }
);
```

```jsx
// no slice
extraReducers: (builder) => {
  builder
    .addCase(buscarProdutos.pending, (s) => { s.loading = true })
    .addCase(buscarProdutos.fulfilled, (s, a) => {
      s.loading = false;
      s.itens = a.payload;
    })
    .addCase(buscarProdutos.rejected, (s, a) => {
      s.loading = false;
      s.erro = a.payload;
    });
}
```

## Seletores memoizados — createSelector

```jsx
import { createSelector } from "@reduxjs/toolkit";

const selectCarrinho = s => s.carrinho.itens;

export const selectTotal = createSelector(
  selectCarrinho,
  itens => itens.reduce((sum, i) => sum + i.preco * i.qtd, 0)
);

export const selectQtd = createSelector(
  selectCarrinho,
  itens => itens.reduce((sum, i) => sum + i.qtd, 0)
);

// componente
const total = useSelector(selectTotal);
```

Memoiza — só recalcula quando `itens` muda.

## Persistência — redux-persist

```bash
npm install redux-persist
```

```jsx
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";

const persistConfig = {
  key: "root",
  storage,
  whitelist: ["auth", "carrinho"] // só esses persistem
};

const persistedReducer = persistReducer(persistConfig, rootReducer);
export const store = configureStore({ reducer: persistedReducer });
export const persistor = persistStore(store);
```

```jsx
import { PersistGate } from "redux-persist/integration/react";

<PersistGate loading={null} persistor={persistor}>
  <App />
</PersistGate>
```

## Quando usar cada ferramenta

| Cenário | Ferramenta |
| --- | --- |
| Estado de um componente | `useState` |
| Tema/auth simples | Context |
| Dados de API | React Query |
| UI global (carrinho, filtros) | Zustand |
| Estado complexo, devtools, time travel | Redux Toolkit |
| App grande, time grande | Redux Toolkit |

## Desafios extras

### Desafio A — undo com Redux

```jsx
historico: (s) => { s.passado.push(s.presente) },
desfazer: (s) => {
  s.presente = s.passado.pop() ?? s.presente;
}
```

### Desafio B — normalização

```jsx
// store produtos como { id: produto } — acesso O(1)
produtos: {
  byId: {},
  allIds: []
}
```

### Desafio C — RTK Query

```jsx
// RTK Query — data fetching dentro do Redux
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const api = createApi({
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  endpoints: (b) => ({
    produtos: b.query({ query: () => "/produtos" })
  })
});
```

## Critérios de verificação

- `createSlice` com Immer — "mutável" seguro
- `createAsyncThunk` para async — pending/fulfilled/rejected automáticos
- `createSelector` para valores derivados
- `redux-persist` para o essencial — `whitelist`
- Context para o que muda pouco; Query para dados de servidor
