# FE05-32 — Redux: Alterando o State Global com Actions e useDispatch

## useDispatch — o emissor de actions

```jsx
import { useDispatch } from "react-redux";

function Botao() {
  const dispatch = useDispatch();

  return (
    <button onClick={() => dispatch({ type: "incrementar" })}>
      +1
    </button>
  );
}
```

`dispatch` envia a action para a store → o reducer calcula → os componentes com `useSelector` re-renderizam.

## Action — o objeto descritivo

```jsx
// forma mínima
{ type: "incrementar" }

// com dados — payload
{ type: "adicionarProduto", payload: { id: 1, nome: "Mouse" } }

// com metadados
{ type: "removerItem", payload: { id: 5 }, meta: { usuario: "ana" } }
```

## Action creators — funções que criam actions

```jsx
// actions/contadorActions.js
export function incrementar() {
  return { type: "incrementar" };
}

export function adicionarProduto(produto) {
  return {
    type: "adicionarProduto",
    payload: produto
  };
}
```

```jsx
// componente
import { incrementar, adicionarProduto } from "./actions";

dispatch(incrementar());
dispatch(adicionarProduto({ id: 1, nome: "Mouse" }));
```

Vantagens: o `type` fica centralizado, autocomplete funciona, mudança de nome é segura.

## O reducer recebendo a action

```jsx
function carrinhoReducer(state = { itens: [] }, action) {
  switch (action.type) {
    case "adicionarProduto":
      return {
        ...state,
        itens: [...state.itens, action.payload] // payload é o produto
      };
    case "removerItem":
      return {
        ...state,
        itens: state.itens.filter(i => i.id !== action.payload.id)
      };
    default:
      return state;
  }
}
```

## Exemplo completo — carrinho

```jsx
function Produto({ produto }) {
  const dispatch = useDispatch();

  return (
    <button onClick={() =>
      dispatch(adicionarProduto(produto))
    }>
      + Carrinho
    </button>
  );
}
```

```jsx
function ItemCarrinho({ item }) {
  const dispatch = useDispatch();

  return (
    <button onClick={() =>
      dispatch({ type: "removerItem", payload: { id: item.id } })
    }>
      Remover
    </button>
  );
}
```

## Dispatch de múltiplas actions

```jsx
function finalizarCompra() {
  dispatch({ type: "finalizarPedido" });
  dispatch({ type: "limparCarrinho" });
  dispatch({ type: "mostrarNotificacao", payload: "Pedido feito!" });
}
```

## Dispatch condicional — com dados do estado

```jsx
function BotaoAdicionar({ produto }) {
  const dispatch = useDispatch();
  const noCarrinho = useSelector(s =>
    s.carrinho.itens.some(i => i.id === produto.id)
  );

  return (
    <button
      onClick={() => dispatch(adicionarProduto(produto))}
      disabled={noCarrinho}
    >
      {noCarrinho ? "No carrinho" : "+ Carrinho"}
    </button>
  );
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `dispatch` sem `type` | `{ type: "..." }` — obrigatório |
| Payload mutado | `payload` é dado — o reducer decide como usar |
| `dispatch` com função async | Redux clássico não aceita — Thunk resolve |
| Vários dispatches seguidos | Ok — cada um gera um novo estado |

## Resumo

- `useDispatch` retorna a função `dispatch` — emite actions
- Action = `{ type, payload? }` — descreve o que aconteceu
- Action creators encapsulam a criação
- Reducer recebe `(state, action)` e calcula o novo estado
