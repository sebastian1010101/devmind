# FE05-38 — Atividade: Utilizando Redux para Requisições com APIs

## Objetivo

CRUD completo via Redux Thunk — lista de posts com criar, editar, remover — tudo passando pelas actions async.

## Os tipos

```jsx
// store/actionTypes.js
export const POSTS = {
  CARREGANDO: "posts/carregando",
  SUCESSO: "posts/sucesso",
  ERRO: "posts/erro",
  ADICIONADO: "posts/adicionado",
  ATUALIZADO: "posts/atualizado",
  REMOVIDO: "posts/removido"
};
```

## As thunks

```jsx
// store/postsThunks.js
import { api } from "../services/api";
import { POSTS } from "./actionTypes";

export function buscarPosts() {
  return async (dispatch) => {
    dispatch({ type: POSTS.CARREGANDO });
    try {
      const res = await api.get("/posts");
      dispatch({ type: POSTS.SUCESSO, payload: res.data });
    } catch (e) {
      dispatch({ type: POSTS.ERRO, payload: e.message });
    }
  };
}

export function criarPost(dados) {
  return async (dispatch) => {
    try {
      const res = await api.post("/posts", dados);
      dispatch({ type: POSTS.ADICIONADO, payload: res.data });
    } catch (e) {
      dispatch({ type: POSTS.ERRO, payload: e.message });
    }
  };
}

export function atualizarPost(id, dados) {
  return async (dispatch) => {
    try {
      const res = await api.put(`/posts/${id}`, dados);
      dispatch({ type: POSTS.ATUALIZADO, payload: res.data });
    } catch (e) {
      dispatch({ type: POSTS.ERRO, payload: e.message });
    }
  };
}

export function removerPost(id) {
  return async (dispatch) => {
    try {
      await api.delete(`/posts/${id}`);
      dispatch({ type: POSTS.REMOVIDO, payload: id });
    } catch (e) {
      dispatch({ type: POSTS.ERRO, payload: e.message });
    }
  };
}
```

## O reducer

```jsx
// store/postsReducer.js
import { POSTS } from "./actionTypes";

const inicial = { lista: [], carregando: false, erro: null };

export function postsReducer(state = inicial, action) {
  switch (action.type) {
    case POSTS.CARREGANDO:
      return { ...state, carregando: true, erro: null };

    case POSTS.SUCESSO:
      return { ...state, carregando: false, lista: action.payload };

    case POSTS.ADICIONADO:
      return { ...state, lista: [action.payload, ...state.lista] };

    case POSTS.ATUALIZADO:
      return {
        ...state,
        lista: state.lista.map(p =>
          p.id === action.payload.id ? action.payload : p
        )
      };

    case POSTS.REMOVIDO:
      return {
        ...state,
        lista: state.lista.filter(p => p.id !== action.payload)
      };

    case POSTS.ERRO:
      return { ...state, carregando: false, erro: action.payload };

    default:
      return state;
  }
}
```

## Os componentes

```jsx
function ListaPosts() {
  const { lista, carregando, erro } = useSelector(s => s.posts);
  const dispatch = useDispatch();

  useEffect(() => { dispatch(buscarPosts()) }, [dispatch]);

  if (carregando) return <p>Carregando...</p>;
  if (erro) return <p>{erro}</p>;

  return (
    <ul>
      {lista.map(p => (
        <li key={p.id}>
          {p.title}
          <button onClick={() => dispatch(removerPost(p.id))}>×</button>
        </li>
      ))}
    </ul>
  );
}
```

```jsx
function FormPost() {
  const [titulo, setTitulo] = useState("");
  const dispatch = useDispatch();

  async function handleSubmit(e) {
    e.preventDefault();
    dispatch(criarPost({ title: titulo, body: "", userId: 1 }));
    setTitulo("");
  }
}
```

## Loading por operação — granular

```jsx
// reducer — controle por operação
const inicial = {
  lista: [],
  carregando: { buscar: false, criar: false, remover: {} }
};

case POSTS.CARREGANDO:
  return { ...state, carregando: { ...state.carregando, buscar: true } };
```

```jsx
// componente
const removendo = useSelector(s => s.posts.carregando.remover[id]);
<button disabled={removendo}>
  {removendo ? "Removendo..." : "Excluir"}
</button>
```

## O fluxo

```text
Criar:
  FormPost → dispatch(criarPost(dados))
    → api.post
    → dispatch(ADICIONADO, res.data)
    → reducer: [novo, ...lista]
    → ListaPosts re-renderiza

Remover:
  ItemPost → dispatch(removerPost(id))
    → api.delete
    → dispatch(REMOVIDO, id)
    → reducer: lista.filter(...)
```

## Critérios de verificação

- Cada operação: thunk async + action de resultado
- Reducer cobre todos os tipos — inclusive erro
- `dispatch` no `useEffect` para o fetch inicial
- Loading global e por operação quando necessário

## Erros comuns

| Erro | Correção |
| --- | --- |
| Action sem tipo de resultado | `ADICIONADO`/`ATUALIZADO`/`REMOVIDO` |
| `map`/`filter` mutando | Sempre retorne novo array |
| Componente atualizando estado local | Deixe o reducer — dispatch a action |
| `dispatch` sem thunk | `dispatch(buscarPosts())` — função |
