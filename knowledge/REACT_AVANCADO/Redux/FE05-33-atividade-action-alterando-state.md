# FE05-33 — Atividade: Redux — Usando Action + Alterando State

## Objetivo

Praticar o fluxo completo — dispatch com payload, reducer que atualiza, `useSelector` que lê — numa lista de favoritos.

## O reducer de favoritos

```jsx
// store/favoritosReducer.js
const estadoInicial = { ids: [] };

export function favoritosReducer(state = estadoInicial, action) {
  switch (action.type) {
    case "favoritos/adicionar":
      if (state.ids.includes(action.payload)) return state; // evita duplicata
      return { ids: [...state.ids, action.payload] };

    case "favoritos/remover":
      return { ids: state.ids.filter(id => id !== action.payload) };

    case "favoritos/limpar":
      return { ids: [] };

    default:
      return state;
  }
}
```

## A store combinada

```jsx
// store/index.js
import { createStore, combineReducers } from "redux";
import { contadorReducer } from "./contadorReducer";
import { favoritosReducer } from "./favoritosReducer";

export const store = createStore(
  combineReducers({
    contador: contadorReducer,
    favoritos: favoritosReducer
  })
);
```

`combineReducers` divide a store por domínio — `state.contador`, `state.favoritos`.

## Os componentes

### Card de produto

```jsx
function CardProduto({ produto }) {
  const dispatch = useDispatch();
  const eFavorito = useSelector(s =>
    s.favoritos.ids.includes(produto.id)
  );

  return (
    <div className={eFavorito ? "card favorito" : "card"}>
      <h3>{produto.nome}</h3>
      <button
        onClick={() => dispatch({
          type: eFavorito
            ? "favoritos/remover"
            : "favoritos/adicionar",
          payload: produto.id
        })}
      >
        {eFavorito ? "★" : "☆"}
      </button>
    </div>
  );
}
```

### Badge de favoritos

```jsx
function BadgeFavoritos() {
  const total = useSelector(s => s.favoritos.ids.length);
  return <span>❤️ {total}</span>;
}
```

### Botão limpar

```jsx
function LimparFavoritos() {
  const dispatch = useDispatch();
  const temFavoritos = useSelector(s => s.favoritos.ids.length > 0);

  return (
    <button
      onClick={() => dispatch({ type: "favoritos/limpar" })}
      disabled={!temFavoritos}
    >
      Limpar favoritos
    </button>
  );
}
```

## O fluxo

```text
Clique em ☆
  → dispatch({ type: "favoritos/adicionar", payload: 3 })
  → reducer: { ids: [...ids, 3] }
  → CardProduto re-renderiza (useSelector mudou)
  → BadgeFavoritos re-renderiza (count mudou)
```

## Desafios extras

### Desafio A — toggle em uma action

```jsx
case "favoritos/toggle":
  return {
    ids: state.ids.includes(action.payload)
      ? state.ids.filter(id => id !== action.payload)
      : [...state.ids, action.payload]
  };
```

### Desafio B — favoritos com dados completos

```jsx
case "favoritos/adicionar":
  return {
    itens: [...state.itens, action.payload] // objeto completo
  };
```

### Desafio C — persistir no localStorage

```jsx
// store/index.js
const store = createStore(reducers);

store.subscribe(() => {
  localStorage.setItem(
    "favoritos",
    JSON.stringify(store.getState().favoritos)
  );
});
```

## Critérios de verificação

- `combineReducers` separando domínios
- `useSelector(s => s.favoritos.ids)` — caminho completo
- Action com `payload` — o id do produto
- `eFavorito` derivado no seletor — sem estado duplicado

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useSelector(s => s.favoritos)` — objeto inteiro | Selecione `s.favoritos.ids` — mais fino |
| `payload` como objeto ` {id}` | `payload: produto.id` — só o necessário |
| `includes` com referência | `includes(produto.id)` — compara primitivo |
| Duplicata no array | Cheque antes de adicionar |
