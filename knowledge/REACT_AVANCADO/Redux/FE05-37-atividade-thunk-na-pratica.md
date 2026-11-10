# FE05-37 — Atividade: Redux Thunk na Prática

## Objetivo

Buscar dados de API com Redux Thunk — a thunk despacha `carregando` → `sucesso`/`erro`, e o componente só lê.

## Os tipos

```jsx
// store/actionTypes.js
export const USUARIOS = {
  CARREGANDO: "usuarios/carregando",
  SUCESSO: "usuarios/sucesso",
  ERRO: "usuarios/erro"
};
```

## A thunk

```jsx
// store/usuariosThunks.js
import { api } from "../services/api";
import { USUARIOS } from "./actionTypes";

export function buscarUsuarios() {
  return async (dispatch) => {
    dispatch({ type: USUARIOS.CARREGANDO });

    try {
      const res = await api.get("/users");
      dispatch({ type: USUARIOS.SUCESSO, payload: res.data });
    } catch (e) {
      dispatch({
        type: USUARIOS.ERRO,
        payload: e.response?.data?.message || "Erro ao buscar"
      });
    }
  };
}
```

## O reducer

```jsx
// store/usuariosReducer.js
import { USUARIOS } from "./actionTypes";

const inicial = { lista: [], carregando: false, erro: null };

export function usuariosReducer(state = inicial, action) {
  switch (action.type) {
    case USUARIOS.CARREGANDO:
      return { ...state, carregando: true, erro: null };

    case USUARIOS.SUCESSO:
      return { ...state, carregando: false, lista: action.payload };

    case USUARIOS.ERRO:
      return { ...state, carregando: false, erro: action.payload };

    default:
      return state;
  }
}
```

## O componente

```jsx
function ListaUsuarios() {
  const { lista, carregando, erro } = useSelector(s => s.usuarios);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(buscarUsuarios());
  }, [dispatch]);

  if (carregando) return <p>Carregando usuários...</p>;
  if (erro) return <p>Erro: {erro}</p>;
  if (lista.length === 0) return <p>Nenhum usuário.</p>;

  return (
    <ul>
      {lista.map(u => (
        <li key={u.id}>
          <strong>{u.name}</strong> — {u.email}
        </li>
      ))}
    </ul>
  );
}
```

## Botão de refresh — re-executa a thunk

```jsx
<button onClick={() => dispatch(buscarUsuarios())}>
  Atualizar
</button>
```

## Thunk com parâmetros

```jsx
export function buscarUsuario(id) {
  return async (dispatch) => {
    dispatch({ type: USUARIOS.CARREGANDO });
    try {
      const res = await api.get(`/users/${id}`);
      dispatch({ type: USUARIOS.SUCESSO, payload: res.data });
    } catch (e) {
      dispatch({ type: USUARIOS.ERRO, payload: e.message });
    }
  };
}

// componente
dispatch(buscarUsuario(3));
```

## Deletando — thunk com atualização

```jsx
export function removerUsuario(id) {
  return async (dispatch) => {
    try {
      await api.delete(`/users/${id}`);
      dispatch({ type: USUARIOS.REMOVIDO, payload: id });
    } catch (e) {
      dispatch({ type: USUARIOS.ERRO, payload: e.message });
    }
  };
}
```

```jsx
case USUARIOS.REMOVIDO:
  return {
    ...state,
    lista: state.lista.filter(u => u.id !== action.payload)
  };
```

## O fluxo visual

```text
Montagem
  → dispatch(buscarUsuarios())
    → dispatch(CARREGANDO)    → loading: true
    → api.get("/users")
    → dispatch(SUCESSO, data) → lista: [...], loading: false
  → componente lê useSelector → renderiza
```

## Critérios de verificação

- Três actions por operação: `carregando`, `sucesso`, `erro`
- Thunk com `try/catch` — erro de rede tratado
- `useSelector` lê `s.usuarios` — o domínio
- `dispatch(thunk())` — função, não objeto
- Loading sempre desliga (sucesso ou erro)

## Erros comuns

| Erro | Correção |
| --- | --- |
| `dispatch` de objeto Promise | Thunk — função que recebe dispatch |
| `erro` não reseta no sucesso | `CARREGANDO` limpa `erro` |
| Thunk sem `try/catch` | Envolva o `await` |
| `loading` dependente só do sucesso | `ERRO` também desliga o loading |
