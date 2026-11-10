# FE05-25 — Zustand: Avançando com Estados, Actions e Requisições

## Actions assíncronas — fetch na store

```jsx
export const useProdutosStore = create((set) => ({
  produtos: [],
  carregando: false,
  erro: null,

  buscar: async () => {
    set({ carregando: true, erro: null });
    try {
      const res = await api.get("/produtos");
      set({ produtos: res.data, carregando: false });
    } catch (e) {
      set({ erro: e.message, carregando: false });
    }
  }
}));
```

```jsx
// componente — chama a action, a store gerencia o estado
function Produtos() {
  const { produtos, carregando, erro } = useProdutosStore();
  const buscar = useProdutosStore(s => s.buscar);

  useEffect(() => { buscar() }, [buscar]);
}
```

## O padrão async completo

```jsx
buscar: async () => {
  set({ carregando: true, erro: null });   // loading liga
  try {
    const res = await api.get("/produtos");
    set({ produtos: res.data });            // dados
  } catch (e) {
    set({ erro: traduzirErro(e) });          // erro
  } finally {
    set({ carregando: false });             // loading desliga
  }
}
```

## get — acessando estado dentro de actions

```jsx
adicionarAoCarrinho: (produto) => {
  const { carrinho } = get(); // lê o estado atual

  const existente = carrinho.find(i => i.id === produto.id);
  if (existente) {
    set(s => ({
      carrinho: s.carrinho.map(i =>
        i.id === produto.id ? { ...i, qtd: i.qtd + 1 } : i
      )
    }));
  } else {
    set(s => ({ carrinho: [...s.carrinho, { ...produto, qtd: 1 }] }));
  }
}
```

## Actions que chamam actions

```jsx
login: async (email, senha) => {
  set({ carregando: true });
  try {
    const res = await api.post("/login", { email, senha });
    set({ usuario: res.data.usuario, token: res.data.token });
    get().buscarDados(); // chama outra action da mesma store
  } catch (e) {
    set({ erro: e.message });
  } finally {
    set({ carregando: false });
  }
},

buscarDados: async () => {
  const res = await api.get("/me/dados");
  set({ dados: res.data });
}
```

## Combine — estado normalizado

```jsx
// ❌ Array de objetos — difícil atualizar
produtos: [{ id: 1, nome: "A" }, { id: 2, nome: "B" }]

// ✅ Normalizado — acesso direto por id
produtos: { 1: { id: 1, nome: "A" }, 2: { id: 2, nome: "B" } },
produtoIds: [1, 2],

adicionar: (produto) =>
  set(s => ({
    produtos: { ...s.produtos, [produto.id]: produto },
    produtoIds: [...s.produtoIds, produto.id]
  })),

remover: (id) =>
  set(s => {
    const { [id]: _, ...resto } = s.produtos;
    return {
      produtos: resto,
      produtoIds: s.produtoIds.filter(i => i !== id)
    };
  })
```

## subscribe — reagir a mudanças

```jsx
// fora de componente — log, analytics, sync
useStore.subscribe(
  (estado, anterior) => {
    if (estado.usuario !== anterior.usuario) {
      analytics.identify(estado.usuario?.id);
    }
  }
);
```

## Shallow — comparando objetos

```jsx
import { useShallow } from "zustand/react/shallow";

// sem shallow — objeto novo a cada render → re-render infinito
const { nome, email } = useStore(s => ({ nome: s.nome, email: s.email }));

// com shallow — só re-renderiza se os valores mudarem
const { nome, email } = useStore(
  useShallow(s => ({ nome: s.nome, email: s.email }))
);
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Fetch na store sem loading/erro | Sempre os três estados |
| `get()` desnecessário | `set(s => ...)` já tem o estado |
| Action não async | `async` no início da action |
| Estado derivado na store | Calcule no seletor |

## Resumo

- Actions assíncronas na store — loading/erro/dados gerenciados juntos
- `get()` lê o estado atual dentro de actions
- `useShallow` para múltiplos seletores sem re-render infinito
- Normalização por id para listas grandes
