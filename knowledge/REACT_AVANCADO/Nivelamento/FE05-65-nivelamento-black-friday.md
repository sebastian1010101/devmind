# FE05-65 — Nivelamento: Exercício Black Friday

## Objetivo

Página de Black Friday — produtos com desconto, countdown até o fim, filtros por categoria e carrinho com desconto aplicado.

## A estrutura

```tsx
interface Produto {
  id: number;
  nome: string;
  precoOriginal: number;
  desconto: number; // 0-100
  categoria: string;
  estoque: number;
  imagem: string;
}
```

## A store

```tsx
interface LojaStore {
  produtos: Produto[];
  carrinho: { id: number; qtd: number }[];
  carregando: boolean;
  buscar: () => Promise<void>;
  adicionar: (id: number) => void;
  remover: (id: number) => void;
}

export const useLojaStore = create<LojaStore>()((set, get) => ({
  produtos: [],
  carrinho: [],
  carregando: false,

  buscar: async () => {
    set({ carregando: true });
    try {
      const res = await api.get<Produto[]>("/produtos");
      set({ produtos: res.data });
    } finally {
      set({ carregando: false });
    }
  },

  adicionar: (id) =>
    set(s => {
      const existe = s.carrinho.find(i => i.id === id);
      return {
        carrinho: existe
          ? s.carrinho.map(i => i.id === id ? { ...i, qtd: i.qtd + 1 } : i)
          : [...s.carrinho, { id, qtd: 1 }]
      };
    }),

  remover: (id) =>
    set(s => ({ carrinho: s.carrinho.filter(i => i.id !== id) }))
}));
```

## O preço com desconto — derivado

```tsx
// seletor ou função utilitária
function precoComDesconto(p: Produto): number {
  return p.precoOriginal * (1 - p.desconto / 100);
}
```

## Countdown — hook customizado

```tsx
function useCountdown(fim: Date) {
  const [restante, setRestante] = useState("");

  useEffect(() => {
    const calcular = () => {
      const diff = fim.getTime() - Date.now();
      if (diff <= 0) return "Encerrado";
      const h = Math.floor(diff / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      const s = Math.floor((diff % 60000) / 1000);
      return `${h}h ${m}m ${s}s`;
    };

    setRestante(calcular());
    const id = setInterval(() => setRestante(calcular()), 1000);
    return () => clearInterval(id);
  }, [fim]);

  return restante;
}
```

## O card de produto

```tsx
function CardProduto({ produto }: { produto: Produto }) {
  const adicionar = useLojaStore(s => s.adicionar);
  const precoFinal = precoComDesconto(produto);

  return (
    <div className="card">
      <span className="badge">{produto.desconto}% OFF</span>
      <img src={produto.imagem} alt={produto.nome} />
      <h3>{produto.nome}</h3>
      <p className="preco-antigo">R$ {produto.precoOriginal.toFixed(2)}</p>
      <p className="preco-novo">R$ {precoFinal.toFixed(2)}</p>
      <button onClick={() => adicionar(produto.id)}>
        Adicionar
      </button>
    </div>
  );
}
```

## Critérios de nivelamento

- `precoComDesconto` calculado — sem estado duplicado
- `useCountdown` com `setInterval` + cleanup
- Carrinho só com `id`/`qtd` — dados vêm do catálogo
- Badge de desconto visível
- `estoque` verificado antes de adicionar

## Desafios extras

- Ordenação por desconto/preço
- Filtro por categoria
- Timer real até meia-noite
- Animação de entrada nos cards
