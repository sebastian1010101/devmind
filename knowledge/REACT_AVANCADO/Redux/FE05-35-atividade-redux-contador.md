# FE05-35 — Atividade: Redux — Contador

## Objetivo

Consolidar o fluxo Redux completo — constantes, action creators, reducer, dispatch e seletores — num contador com passo customizável.

## Os actionTypes

```jsx
// store/actionTypes.js
export const CONTADOR = {
  INCREMENTAR: "contador/incrementar",
  DECREMENTAR: "contador/decrementar",
  INCREMENTAR_POR: "contador/incrementarPor",
  SET_PASSO: "contador/setPasso",
  RESETAR: "contador/resetar"
};
```

## Os action creators

```jsx
// store/contadorActions.js
import { CONTADOR } from "./actionTypes";

export const incrementar = () => ({ type: CONTADOR.INCREMENTAR });
export const decrementar = () => ({ type: CONTADOR.DECREMENTAR });
export const resetar = () => ({ type: CONTADOR.RESETAR });

export const incrementarPor = (valor) => ({
  type: CONTADOR.INCREMENTAR_POR,
  payload: valor
});

export const setPasso = (passo) => ({
  type: CONTADOR.SET_PASSO,
  payload: passo
});
```

## O reducer

```jsx
// store/contadorReducer.js
import { CONTADOR } from "./actionTypes";

const inicial = { valor: 0, passo: 1 };

export function contadorReducer(state = inicial, action) {
  switch (action.type) {
    case CONTADOR.INCREMENTAR:
      return { ...state, valor: state.valor + state.passo };

    case CONTADOR.DECREMENTAR:
      return { ...state, valor: state.valor - state.passo };

    case CONTADOR.INCREMENTAR_POR:
      return { ...state, valor: state.valor + action.payload };

    case CONTADOR.SET_PASSO:
      return { ...state, passo: action.payload };

    case CONTADOR.RESETAR:
      return inicial;

    default:
      return state;
  }
}
```

## O componente

```jsx
import { useSelector, useDispatch } from "react-redux";
import { incrementar, decrementar, resetar, setPasso } from "./store/contadorActions";

function Contador() {
  const valor = useSelector(s => s.contador.valor);
  const passo = useSelector(s => s.contador.passo);
  const dispatch = useDispatch();

  return (
    <div>
      <h1>{valor}</h1>

      <label>
        Passo:
        <input
          type="number"
          value={passo}
          onChange={e => dispatch(setPasso(Number(e.target.value)))}
        />
      </label>

      <button onClick={() => dispatch(decrementar())}>−{passo}</button>
      <button onClick={() => dispatch(incrementar())}>+{passo}</button>
      <button onClick={() => dispatch(resetar())}>Reset</button>
    </div>
  );
}
```

## Seletores derivados

```jsx
const dobro = useSelector(s => s.contador.valor * 2);
const ePositivo = useSelector(s => s.contador.valor > 0);
const historico = useSelector(s => s.contador.historico || []);
```

## Desafios extras

### Desafio A — histórico de valores

```jsx
case CONTADOR.INCREMENTAR:
  return {
    ...state,
    valor: state.valor + state.passo,
    historico: [...state.historico, state.valor + state.passo]
  };
```

### Desafio B — limites

```jsx
case CONTADOR.INCREMENTAR:
  const novo = state.valor + state.passo;
  return {
    ...state,
    valor: Math.min(novo, state.max || 100)
  };
```

### Desafio C — desfazer

```jsx
case CONTADOR.DESFAZER:
  const ultimo = state.historico[state.historico.length - 1];
  return {
    ...state,
    valor: ultimo ?? 0,
    historico: state.historico.slice(0, -1)
  };
```

## Critérios de verificação

- `actionTypes.js` com constantes namespaced
- Action creators em arquivo separado
- Reducer retorna novo objeto — `{...state}`
- `useSelector` com caminho completo (`s.contador.valor`)
- Payload para valores variáveis (passo, incrementarPor)

## Erros comuns

| Erro | Correção |
| --- | --- |
| `state.valor += 1` | Retorne `{...state, valor: ...}` |
| `dispatch({ type: "x" })` sem creator | `incrementar()` — centralizado |
| `passo` hardcoded | `SET_PASSO` action — configurável |
| `useSelector(s => s)` | Selecione `s.contador` — não a store toda |
