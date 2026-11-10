# FE05-39 — Redux: Autenticação com Redux e Thunk — Parte 1

## A estrutura de auth no Redux

```text
store/
├── authReducer.js    → { usuario, token, carregando, erro }
├── authActions.js    → loginRequest, loginSucesso, loginErro, logout
├── authThunks.js     → login(email, senha), verificarSessao()
└── actionTypes.js    → AUTH.LOGIN_REQUEST, ...
```

## Os tipos

```jsx
export const AUTH = {
  LOGIN_REQUEST: "auth/loginRequest",
  LOGIN_SUCESSO: "auth/loginSucesso",
  LOGIN_ERRO: "auth/loginErro",
  LOGOUT: "auth/logout",
  SESSAO_RESTAURADA: "auth/sessaoRestaurada"
};
```

## O reducer de auth

```jsx
import { AUTH } from "./actionTypes";

const inicial = {
  usuario: null,
  token: localStorage.getItem("token"), // restaura do storage
  carregando: false,
  erro: null
};

export function authReducer(state = inicial, action) {
  switch (action.type) {
    case AUTH.LOGIN_REQUEST:
      return { ...state, carregando: true, erro: null };

    case AUTH.LOGIN_SUCESSO:
      return {
        ...state,
        carregando: false,
        usuario: action.payload.usuario,
        token: action.payload.token
      };

    case AUTH.LOGIN_ERRO:
      return { ...state, carregando: false, erro: action.payload };

    case AUTH.LOGOUT:
      return { ...inicial, token: null }; // limpa tudo

    case AUTH.SESSAO_RESTAURADA:
      return { ...state, usuario: action.payload };

    default:
      return state;
  }
}
```

## A thunk de login

```jsx
// store/authThunks.js
import { api } from "../services/api";
import { AUTH } from "./actionTypes";

export function login(email, senha) {
  return async (dispatch) => {
    dispatch({ type: AUTH.LOGIN_REQUEST });

    try {
      const res = await api.post("/login", { email, senha });
      const { token, usuario } = res.data;

      localStorage.setItem("token", token);
      localStorage.setItem("usuario", JSON.stringify(usuario));

      dispatch({ type: AUTH.LOGIN_SUCESSO, payload: { usuario, token } });
      return true; // sucesso — para o componente navegar
    } catch (e) {
      const msg = e.response?.data?.message || "Credenciais inválidas";
      dispatch({ type: AUTH.LOGIN_ERRO, payload: msg });
      return false;
    }
  };
}
```

## O logout

```jsx
export function logout() {
  return (dispatch) => {
    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    dispatch({ type: AUTH.LOGOUT });
  };
}
```

## Restaurando sessão — thunk de verificação

```jsx
export function verificarSessao() {
  return async (dispatch) => {
    const token = localStorage.getItem("token");
    if (!token) return;

    try {
      const res = await api.get("/me"); // valida o token
      dispatch({ type: AUTH.SESSAO_RESTAURADA, payload: res.data });
    } catch {
      dispatch(logout()); // token inválido — limpa
    }
  };
}
```

```jsx
// App.jsx — na montagem
function App() {
  const dispatch = useDispatch();
  useEffect(() => {
    dispatch(verificarSessao());
  }, [dispatch]);
}
```

## O interceptor com Redux

```jsx
// services/api.js — injeta o token do store
import { store } from "../store";

api.interceptors.request.use(config => {
  const { token } = store.getState().auth;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Token no reducer sem storage | `localStorage` persiste; reducer lê inicial |
| Login sem `return` | `return true/false` — o componente decide navegar |
| Logout sem limpar storage | Remova token E usuário |
| Sessão sem verificação | `/me` valida se o token ainda serve |

## Resumo

- Auth no Redux = `{ usuario, token, carregando, erro }`
- `login` thunk: request → sucesso/erro → salva storage
- `logout` limpa storage e state
- `verificarSessao` restaura ao montar o app
