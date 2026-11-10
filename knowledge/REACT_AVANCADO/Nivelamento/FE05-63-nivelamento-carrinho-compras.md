# FE05-63 — Nivelamento: Carrinho de Compras

## Objetivo

Carrinho de compras completo integrando tudo do módulo: Context ou Zustand, CRUD de itens, total derivado e persistência.

## A store Zustand

```tsx
// store/useCarrinhoStore.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface Item {
  id: number;
  nome: string;
  preco: number;
  qtd: number;
}

interface CarrinhoStore {
  itens: Item[];
  adicionar: (produto: Omit<Item, "qtd">) => void;
  remover: (id: number) => void;
  alterarQtd: (id: number, delta: number) => void;
  limpar: () => void;
}

export const useCarrinhoStore = create<CarrinhoStore>()(
  persist(
    (set) => ({
      itens: [],

      adicionar: (produto) =>
        set(s => {
          const existe = s.itens.find(i => i.id === produto.id);
          return {
            itens: existe
              ? s.itens.map(i =>
                  i.id === produto.id ? { ...i, qtd: i.qtd + 1 } : i
                )
              : [...s.itens, { ...produto, qtd: 1 }]
          };
        }),

      remover: (id) =>
        set(s => ({ itens: s.itens.filter(i => i.id !== id) })),

      alterarQtd: (id, delta) =>
        set(s => ({
          itens: s.itens
            .map(i => i.id === id ? { ...i, qtd: i.qtd + delta } : i)
            .filter(i => i.qtd > 0)
        })),

      limpar: () => set({ itens: [] })
    }),
    { name: "carrinho" }
  )
);
```

## Os seletores derivados

```tsx
const total = useCarrinhoStore(s =>
  s.itens.reduce((acc, i) => acc + i.preco * i.qtd, 0)
);

const qtdTotal = useCarrinhoStore(s =>
  s.itens.reduce((acc, i) => acc + i.qtd, 0)
);
```

## Componentes

### Catálogo

```tsx
function Catalogo({ produtos }: { produtos: Produto[] }) {
  const adicionar = useCarrinhoStore(s => s.adicionar);
  const noCarrinho = useCarrinhoStore(s =>
    new Set(s.itens.map(i => i.id))
  );

  return (
    <div className="grid">
      {produtos.map(p => (
        <div key={p.id} className="produto">
          <h3>{p.nome}</h3>
          <p>R$ {p.preco.toFixed(2)}</p>
          <button
            onClick={() => adicionar(p)}
            disabled={noCarrinho.has(p.id)}
          >
            {noCarrinho.has(p.id) ? "No carrinho" : "Adicionar"}
          </button>
        </div>
      ))}
    </div>
  );
}
```

### Carrinho

```tsx
function Carrinho() {
  const { itens, remover, alterarQtd, limpar } = useCarrinhoStore();
  const total = useCarrinhoStore(s =>
    s.itens.reduce((acc, i) => acc + i.preco * i.qtd, 0)
  );

  if (itens.length === 0) return <p>Carrinho vazio</p>;

  return (
    <div>
      {itens.map(i => (
        <div key={i.id} className="item">
          <span>{i.nome}</span>
          <button onClick={() => alterarQtd(i.id, -1)}>-</button>
          <span>{i.qtd}</span>
          <button onClick={() => alterarQtd(i.id, 1)}>+</button>
          <span>R$ {(i.preco * i.qtd).toFixed(2)}</span>
          <button onClick={() => remover(i.id)}>×</button>
        </div>
      ))}
      <p>Total: R$ {total.toFixed(2)}</p>
      <button onClick={limpar}>Limpar</button>
    </div>
  );
}
```

## Critérios de nivelamento

- Store Zustand com `persist` — carrinho sobrevive ao reload
- `total` derivado com `reduce` — sem estado duplicado
- `alterarQtd` com filtro de zero — remove automaticamente
- `noCarrinho` com `Set` — lookup O(1)
- Actions encapsuladas na store — lógica centralizada

## Desafios extras

- Cupom de desconto (`cupom: string`, `aplicarCupom`)
- Limite de estoque por produto
- Frete calculado por faixa de CEP
- Checkout com resumo do pedido
