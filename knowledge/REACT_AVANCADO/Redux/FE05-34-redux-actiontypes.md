# FE05-34 — Redux: Utilizando actionTypes

## O problema — strings soltas

```jsx
// espalhadas pelo código — typo silencioso
dispatch({ type: "incrementar" });
dispatch({ type: "increment" });   // ← typo: action desconhecida, silencioso
```

Sem constantes, um erro de digitação cria uma action que nenhum reducer trata — **falha silenciosa**.

## A solução — constantes centralizadas

```jsx
// store/actionTypes.js
export const CONTADOR = {
  INCREMENTAR: "contador/incrementar",
  DECREMENTAR: "contador/decrementar",
  RESETAR: "contador/resetar"
};

export const CARRINHO = {
  ADICIONAR: "carrinho/adicionar",
  REMOVER: "carrinho/remover",
  LIMPAR: "carrinho/limpar"
};
```

```jsx
// uso — autocomplete e erro de referência se não existir
import { CONTADOR } from "./actionTypes";

dispatch({ type: CONTADOR.INCREMENTAR });
```

## O reducer usando as constantes

```jsx
import { CONTADOR } from "./actionTypes";

function contadorReducer(state = { valor: 0 }, action) {
  switch (action.type) {
    case CONTADOR.INCREMENTAR:
      return { ...state, valor: state.valor + 1 };
    case CONTADOR.DECREMENTAR:
      return { ...state, valor: state.valor - 1 };
    default:
      return state;
  }
}
```

Typo em `CONTADOR.INCREMENTAR` → erro de referência **imediatamente**, não silencioso.

## Convenção de nomes

```text
dominio/verbo — "carrinho/adicionar", "auth/loginSucesso"

Tipos comuns por domínio:
  dominio/VERBO          → ação do usuário
  dominio/VERBO_SUCESSO  → resposta OK do servidor
  dominio/VERBO_ERRO     → resposta de erro
```

```jsx
export const AUTH = {
  LOGIN_REQUEST: "auth/loginRequest",
  LOGIN_SUCESSO: "auth/loginSucesso",
  LOGIN_ERRO: "auth/loginErro",
  LOGOUT: "auth/logout"
};
```

## Com action creators tipados

```jsx
// actions/authActions.js
import { AUTH } from "../actionTypes";

export const loginRequest = () => ({ type: AUTH.LOGIN_REQUEST });
export const loginSucesso = (usuario) => ({
  type: AUTH.LOGIN_SUCESSO,
  payload: usuario
});
export const loginErro = (erro) => ({
  type: AUTH.LOGIN_ERRO,
  payload: erro
});
```

## Redux Toolkit elimina a necessidade

```jsx
// createSlice gera os types automaticamente
const slice = createSlice({
  name: "contador",
  reducers: {
    incrementar: (s) => { s.valor += 1 }
  }
});
// type gerado: "contador/incrementar"
```

Com RTK, os tipos são implícitos — actionTypes manuais são do Redux clássico.

## Erros comuns

| Erro | Correção |
| --- | --- |
| String solta no dispatch | Constantes de `actionTypes.js` |
| Tipo sem namespace | `"contador/incrementar"` — evita colisão |
| Constantes espalhadas | Arquivo único `actionTypes.js` |
| Typo silencioso | Constantes — erro de referência imediato |

## Resumo

- Strings soltas → typos silenciosos; constantes → erro imediato
- Arquivo `actionTypes.js` centraliza todos os tipos
- Convenção `dominio/verbo` evita colisões
- Redux Toolkit (`createSlice`) gera os tipos automaticamente
