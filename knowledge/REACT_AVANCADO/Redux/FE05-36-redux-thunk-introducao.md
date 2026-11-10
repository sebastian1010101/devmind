# FE05-36 — Redux: Introdução ao Redux Thunk

## O problema — Redux é síncrono

```jsx
// ❌ dispatch só aceita objetos — não async
dispatch({ type: "buscar" }); // mas e o fetch?

// Precisa esperar a resposta para despachar o resultado
// mas Redux não sabe esperar
```

**Redux Thunk** permite dispatch de **funções** — que podem ser async e despachar outras actions depois.

## Como funciona

```jsx
// thunk = função que recebe dispatch e getState
function buscarProdutos() {
  return async (dispatch, getState) => {
    dispatch({ type: "produtos/carregando" }); // loading liga

    try {
      const res = await api.get("/produtos");
      dispatch({ type: "produtos/sucesso", payload: res.data });
    } catch (e) {
      dispatch({ type: "produtos/erro", payload: e.message });
    }
  };
}

// dispatch aceita a função — thunk a executa
dispatch(buscarProdutos());
```

## O fluxo completo

```text
dispatch(buscarProdutos())          ← thunk, não objeto
  → thunk executa a função
  → dispatch({ type: "carregando" }) ← síncrono, dentro do thunk
  → await api.get(...)
  → dispatch({ type: "sucesso" })    ← síncrono, depois do await
```

## Configurando o Thunk

```bash
npm install redux-thunk
```

```jsx
// Redux clássico
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";

const store = createStore(reducer, applyMiddleware(thunk));
```

```jsx
// Redux Toolkit — thunk já vem embutido
import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({ reducer: {...} });
// thunk incluso por padrão
```

## As três actions do padrão async

```jsx
export const PRODUTOS = {
  CARREGANDO: "produtos/carregando",
  SUCESSO: "produtos/sucesso",
  ERRO: "produtos/erro"
};
```

```jsx
function produtosReducer(state = { itens: [], loading: false, erro: null }, action) {
  switch (action.type) {
    case PRODUTOS.CARREGANDO:
      return { ...state, loading: true, erro: null };
    case PRODUTOS.SUCESSO:
      return { ...state, loading: false, itens: action.payload };
    case PRODUTOS.ERRO:
      return { ...state, loading: false, erro: action.payload };
    default:
      return state;
  }
}
```

## A thunk completa

```jsx
// actions/produtosThunks.js
export function buscarProdutos() {
  return async (dispatch) => {
    dispatch({ type: PRODUTOS.CARREGANDO });

    try {
      const res = await api.get("/produtos");
      dispatch({ type: PRODUTOS.SUCESSO, payload: res.data });
    } catch (e) {
      dispatch({ type: PRODUTOS.ERRO, payload: e.message });
    }
  };
}
```

## Usando no componente

```jsx
function Produtos() {
  const { itens, loading, erro } = useSelector(s => s.produtos);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(buscarProdutos()); // dispatch da função thunk
  }, [dispatch]);

  if (loading) return <p>Carregando...</p>;
  if (erro) return <p>{erro}</p>;
  return <ul>{itens.map(...)}</ul>;
}
```

## getState — lendo o estado dentro da thunk

```jsx
function adicionarProduto(produto) {
  return async (dispatch, getState) => {
    const { usuario } = getState().auth; // lê sem hook

    const res = await api.post("/produtos", {
      ...produto,
      usuarioId: usuario.id
    });
    dispatch({ type: PRODUTOS.ADICIONAR, payload: res.data });
  };
}
```

## Redux Toolkit — createAsyncThunk (a forma moderna)

```jsx
import { createAsyncThunk } from "@reduxjs/toolkit";

export const buscarProdutos = createAsyncThunk(
  "produtos/buscar",
  async () => {
    const res = await api.get("/produtos");
    return res.data;
  }
);

// gera automaticamente: pending, fulfilled, rejected
```

```jsx
const slice = createSlice({
  name: "produtos",
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(buscarProdutos.pending, (s) => { s.loading = true })
      .addCase(buscarProdutos.fulfilled, (s, a) => {
        s.loading = false;
        s.itens = a.payload;
      })
      .addCase(buscarProdutos.rejected, (s, a) => {
        s.loading = false;
        s.erro = a.error.message;
      });
  }
});
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `dispatch` de objeto async | Thunk — dispatch de função |
| Thunk sem `try/catch` | Erro de rede silencioso |
| `loading` sem reset | `finally` ou action de sucesso/erro |
| Redux clássico sem `applyMiddleware` | `createStore(reducer, applyMiddleware(thunk))` |

## Resumo

- Thunk = dispatch de função — permite async antes de despachar actions
- Padrão `carregando`/`sucesso`/`erro` — três actions por operação
- `getState()` lê o estado dentro da thunk
- Redux Toolkit tem `createAsyncThunk` — automático e limpo
