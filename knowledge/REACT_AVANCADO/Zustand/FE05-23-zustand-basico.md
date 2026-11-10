# FE05-23 — Zustand: Utilização Básica

## O que é o Zustand

Biblioteca de estado global minimalista — store como hook, sem Provider, sem boilerplate.

```bash
npm install zustand
```

## Criando a store

```jsx
// store/useStore.js
import { create } from "zustand";

export const useStore = create((set) => ({
  // estado
  contador: 0,
  usuario: null,

  // ações
  incrementar: () => set(s => ({ contador: s.contador + 1 })),
  decrementar: () => set(s => ({ contador: s.contador - 1 })),
  setUsuario: (u) => set({ usuario: u }),
  reset: () => set({ contador: 0 })
}));
```

## Consumindo — o seletor

```jsx
import { useStore } from "./store/useStore";

function Contador() {
  // seleciona SÓ o que precisa — re-render só se isso mudar
  const contador = useStore(s => s.contador);
  const incrementar = useStore(s => s.incrementar);

  return (
    <div>
      <p>{contador}</p>
      <button onClick={incrementar}>+</button>
    </div>
  );
}
```

## O seletor — a peça chave

```jsx
// ❌ Re-renderiza em qualquer mudança da store
const store = useStore();

// ✅ Só re-renderiza se 'contador' mudar
const contador = useStore(s => s.contador);

// ✅ Múltiplos — mas cria objeto novo (use shallow)
const { contador, usuario } = useStore(
  s => ({ contador: s.contador, usuario: s.usuario })
);
// ou melhor — seletores separados
const contador = useStore(s => s.contador);
const usuario = useStore(s => s.usuario);
```

## Ações dentro da store — a boa prática

```jsx
export const useStore = create((set, get) => ({
  itens: [],

  // ação com lógica encapsulada
  adicionar: (item) =>
    set(s => ({ itens: [...s.itens, item] })),

  remover: (id) =>
    set(s => ({ itens: s.itens.filter(i => i.id !== id) })),

  // get acessa o estado atual
  total: () => get().itens.reduce((s, i) => s + i.preco, 0)
}));
```

## Estado derivado — computados

```jsx
export const useStore = create((set) => ({
  itens: [],

  // função derivada — chamada no componente
  getTotal: () => {
    const { itens } = useStore.getState();
    return itens.reduce((s, i) => s + i.preco * i.qtd, 0);
  }
}));

// ou melhor — calcule no seletor
const total = useStore(s =>
  s.itens.reduce((acc, i) => acc + i.preco * i.qtd, 0)
);
```

## Múltiplas stores — por domínio

```text
store/
├── useUsuarioStore.js   → auth, perfil
├── useCarrinhoStore.js  → itens, total
├── useTemaStore.js      → tema, preferências
└── useUiStore.js        → modais, loading
```

Cada store independente — consome só o que precisa.

## Fora do React — acesso direto

```jsx
// fora de componente — interceptor, service
useStore.getState().usuario;
useStore.setState({ usuario: novo });
useStore.subscribe(state => console.log("mudou"));
```

## Middlewares — persist e devtools

```jsx
import { persist } from "zustand/middleware";

export const useStore = create(
  persist(
    (set) => ({ /* estado */ }),
    { name: "meu-app" } // chave no localStorage
  )
);
```

```jsx
import { devtools } from "zustand/middleware";

export const useStore = create(
  devtools((set) => ({ /* estado */ }))
); // Redux DevTools funciona!
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useStore()` sem seletor | Re-renderiza em tudo — selecione |
| Objeto no seletor sem shallow | Crie seletores separados |
| Estado derivado na store | `useMemo` ou calcule no seletor |
| Store gigante | Divida por domínio |

## Resumo

- `create((set) => ({...}))` — estado + ações num hook
- Seletor `useStore(s => s.campo)` — re-render cirúrgico
- Ações na store encapsulam lógica
- `persist` salva no localStorage; `devtools` conecta Redux DevTools
