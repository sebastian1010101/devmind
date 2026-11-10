# FE05-26 — Atividade: Consumindo uma API com Zustand

## Objetivo

Loja com catálogo de produtos vindos de API — Zustand gerencia os dados, o carrinho e o loading, sem Context nem props.

## A store da loja

```jsx
// store/useLojaStore.js
import { create } from "zustand";
import { api } from "../services/api";

export const useLojaStore = create((set, get) => ({
  // catálogo
  produtos: [],
  carregando: false,
  erro: null,

  // carrinho
  carrinho: [],
  carrinhoAberto: false,

  // — ações de catálogo —
  buscarProdutos: async () => {
    set({ carregando: true, erro: null });
    try {
      const res = await api.get("/products");
      set({ produtos: res.data });
    } catch (e) {
      set({ erro: "Erro ao carregar produtos" });
    } finally {
      set({ carregando: false });
    }
  },

  // — ações do carrinho —
  adicionar: (produto) => {
    const { carrinho } = get();
    const existente = carrinho.find(i => i.id === produto.id);

    set(s => ({
      carrinho: existente
        ? s.carrinho.map(i =>
            i.id === produto.id ? { ...i, qtd: i.qtd + 1 } : i
          )
        : [...s.carrinho, { ...produto, qtd: 1 }]
    }));
  },

  remover: (id) =>
    set(s => ({ carrinho: s.carrinho.filter(i => i.id !== id) })),

  abrirCarrinho: () => set({ carrinhoAberto: true }),
  fecharCarrinho: () => set({ carrinhoAberto: false }),

  // — derivados —
  totalCarrinho: () =>
    get().carrinho.reduce((s, i) => s + i.price * i.qtd, 0)
}));
```

## Os componentes

### Catálogo — Read

```jsx
function Catalogo() {
  const { produtos, carregando, erro } = useLojaStore();
  const buscar = useLojaStore(s => s.buscarProdutos);
  const adicionar = useLojaStore(s => s.adicionar);

  useEffect(() => {
    buscar();
  }, [buscar]);

  if (carregando) return <p>Carregando produtos...</p>;
  if (erro) return <p>{erro}</p>;

  return (
    <div className="grid">
      {produtos.map(p => (
        <div key={p.id} className="produto">
          <img src={p.image} alt={p.title} />
          <h3>{p.title}</h3>
          <p>R$ {p.price.toFixed(2)}</p>
          <button onClick={() => adicionar(p)}>+ Carrinho</button>
        </div>
      ))}
    </div>
  );
}
```

### Carrinho — Drawer

```jsx
function Carrinho() {
  const { carrinho, carrinhoAberto, fecharCarrinho, remover } =
    useLojaStore();
  const total = useLojaStore(s =>
    s.carrinho.reduce((sum, i) => sum + i.price * i.qtd, 0)
  );

  if (!carrinhoAberto) return null;

  return (
    <aside className="carrinho">
      <button onClick={fecharCarrinho}>×</button>
      {carrinho.map(i => (
        <div key={i.id}>
          <span>{i.title}</span>
          <span>{i.qtd}x R$ {i.price.toFixed(2)}</span>
          <button onClick={() => remover(i.id)}>Remover</button>
        </div>
      ))}
      <p>Total: R$ {total.toFixed(2)}</p>
    </aside>
  );
}
```

### Ícone — Header

```jsx
function IconeCarrinho() {
  const qtd = useLojaStore(s =>
    s.carrinho.reduce((sum, i) => sum + i.qtd, 0)
  );
  const abrir = useLojaStore(s => s.abrirCarrinho);

  return (
    <button onClick={abrir}>
      🛒 {qtd > 0 && <span className="badge">{qtd}</span>}
    </button>
  );
}
```

## Por que Zustand aqui

- `IconeCarrinho` no Header precisa do carrinho — ramo diferente
- `Catalogo` precisa de `adicionar` — sem props
- `Carrinho` é um drawer — fora da árvore visual
- Sem Provider — store global acessível

## Desafios extras

### Desafio A — filtro por categoria

```jsx
// store
categoria: null,
setCategoria: (c) => set({ categoria: c }),

// componente — filtra na hora de ler
const produtos = useLojaStore(s =>
  s.categoria
    ? s.produtos.filter(p => p.category === s.categoria)
    : s.produtos
);
```

### Desafio B — persistir carrinho

```jsx
import { persist } from "zustand/middleware";

persist(
  (set, get) => ({ /* store */ }),
  {
    name: "loja",
    partialize: (s) => ({ carrinho: s.carrinho }) // só o carrinho
  }
)
```

### Desafio C — busca

```jsx
const [busca, setBusca] = useState("");
const filtrados = produtos.filter(p =>
  p.title.toLowerCase().includes(busca.toLowerCase())
);
```

## Critérios de verificação

- Store separa domínios: catálogo vs carrinho
- `buscarProdutos` tem try/catch/finally
- Seletores derivam `total` e `qtd` — sem duplicar estado
- `persist` com `partialize` salva só o necessário
- Sem props drilling entre Header, Catálogo e Carrinho

## Erros comuns

| Erro | Correção |
| --- | --- |
| `total` em estado separado | Derive no seletor — sem dessincronia |
| `carrinho` sem `get()` | `get().carrinho` lê o atual na action |
| `partialize` faltando | Persiste tudo — inclusive dados temporários |
| Fetch no componente | Action na store — `buscarProdutos()` |
