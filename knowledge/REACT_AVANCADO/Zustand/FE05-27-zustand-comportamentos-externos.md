# FE05-27 — Zustand: Comportamentos Externos

## Acessando a store fora do React

A store existe independente do React — útil em interceptors, services, arquivos utilitários.

```jsx
import { useAuthStore } from "../store/useAuthStore";

// Em um interceptor de axios — fora do componente
api.interceptors.request.use(config => {
  const { token } = useAuthStore.getState(); // lê sem hook
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  res => res,
  erro => {
    if (erro.response?.status === 401) {
      useAuthStore.getState().logout(); // chama action fora do React
    }
    return Promise.reject(erro);
  }
);
```

## Os métodos da store

```jsx
useStore.getState()          // lê estado atual — fora de componente
useStore.setState({...})     // atualiza direto — cuidado
useStore.subscribe(fn)       // reage a cada mudança
useStore.subscribeWithSelector // seletor específico
```

## subscribe — reagindo a mudanças

```jsx
// Analytics — rastreia mudança de usuário
useAuthStore.subscribe((estado, anterior) => {
  if (estado.usuario?.id !== anterior.usuario?.id) {
    analytics.identify(estado.usuario?.id);
  }
});

// Sync entre abas — localStorage
useTemaStore.subscribe(estado => {
  localStorage.setItem("tema", estado.tema);
});
```

## subscribeWithSelector — ouvindo só um pedaço

```jsx
import { subscribeWithSelector } from "zustand/middleware";

export const useStore = create(
  subscribeWithSelector((set) => ({ ... }))
);

// só quando 'usuario' muda
useStore.subscribe(
  s => s.usuario,              // seletor
  (usuario, anterior) => {     // callback com o pedaço
    console.log("usuário mudou", usuario);
  }
);
```

## Middlewares — a stack do Zustand

```jsx
import { create } from "zustand";
import { devtools, persist, subscribeWithSelector } from "zustand/middleware";

export const useStore = create(
  devtools(           // Redux DevTools
    persist(          // localStorage
      subscribeWithSelector(  // subscribe com seletor
        (set, get) => ({ ... })
      ),
      { name: "app" }
    )
  )
);
```

Ordem importa — `devtools` por último envolve tudo.

## persist — detalhes avançados

```jsx
persist(
  (set) => ({ ... }),
  {
    name: "app-storage",                    // chave no localStorage
    partialize: (s) => ({                   // só persiste o essencial
      usuario: s.usuario,
      carrinho: s.carrinho
    }),
    version: 2,                              // migração
    migrate: (persisted, versao) => {
      if (versao === 1) {
        // transforma o formato antigo
      }
      return persisted;
    }
  }
)
```

## devtools — debugando

```jsx
devtools(
  (set) => ({
    incrementar: () =>
      set(s => ({ contador: s.contador + 1 }),
        false,
        "incrementar" // nome da action no DevTools
      )
  }),
  { name: "MeuApp" }
)
```

No Redux DevTools aparece `incrementar` — fácil rastrear.

## temporal — undo/redo (middleware de comunidade)

```jsx
import { temporal } from "zundo";

export const useStore = create(
  temporal(
    (set) => ({
      texto: "",
      setTexto: (t) => set({ texto: t })
    })
  )
);

// undo/redo automático
useStore.temporal.getState().undo();
useStore.temporal.getState().redo();
```

## Slices — organizando stores grandes

```jsx
// slices/usuarioSlice.js
export const criarUsuarioSlice = (set, get) => ({
  usuario: null,
  login: async (email, senha) => { ... }
});

// slices/carrinhoSlice.js
export const criarCarrinhoSlice = (set, get) => ({
  itens: [],
  adicionar: (p) => { ... }
});

// store/index.js — junta tudo
export const useStore = create(
  devtools(
    persist(
      (set, get) => ({
        ...criarUsuarioSlice(set, get),
        ...criarCarrinhoSlice(set, get)
      }),
      { name: "app" }
    )
  )
);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useStore` como hook fora de componente | `useStore.getState()` |
| Middlewares na ordem errada | `devtools(persist(...))` — devtools por fora |
| Persistindo tudo | `partialize` — só o essencial |
| `subscribe` sem cleanup | Guarde o retorno e chame para desinscrever |

## Resumo

- `getState`/`setState`/`subscribe` — acesso fora do React
- `subscribeWithSelector` — reage só a um pedaço do estado
- `persist` com `partialize` e `version` — storage inteligente
- Slices dividem stores grandes por domínio
