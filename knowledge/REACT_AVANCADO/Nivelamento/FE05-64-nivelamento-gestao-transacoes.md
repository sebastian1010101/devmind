# FE05-64 — Nivelamento: Gestão de Transações

## Objetivo

App financeiro pessoal — transações de entrada/saída, saldo calculado, filtros por tipo e período.

## O tipo Transação

```typescript
interface Transacao {
  id: string;
  descricao: string;
  valor: number;
  tipo: "entrada" | "saida";
  categoria: string;
  data: string; // ISO
  criadaEm: number;
}
```

## A store

```tsx
interface TransacaoStore {
  transacoes: Transacao[];
  adicionar: (t: Omit<Transacao, "id" | "criadaEm">) => void;
  remover: (id: string) => void;
}

export const useTransacaoStore = create<TransacaoStore>()(
  persist(
    (set) => ({
      transacoes: [],
      adicionar: (dados) =>
        set(s => ({
          transacoes: [{
            ...dados,
            id: crypto.randomUUID(),
            criadaEm: Date.now()
          }, ...s.transacoes]
        })),
      remover: (id) =>
        set(s => ({ transacoes: s.transacoes.filter(t => t.id !== id) }))
    }),
    { name: "financas" }
  )
);
```

## Os cálculos derivados

```tsx
const resumo = useTransacaoStore(s => {
  const entradas = s.transacoes
    .filter(t => t.tipo === "entrada")
    .reduce((acc, t) => acc + t.valor, 0);
  const saidas = s.transacoes
    .filter(t => t.tipo === "saida")
    .reduce((acc, t) => acc + t.valor, 0);
  return { entradas, saidas, saldo: entradas - saidas };
});
```

## O formulário

```tsx
const schema = z.object({
  descricao: z.string().min(3),
  valor: z.number().positive("Valor deve ser positivo"),
  tipo: z.enum(["entrada", "saida"]),
  categoria: z.string().min(1)
});

type FormData = z.infer<typeof schema>;

function FormTransacao() {
  const adicionar = useTransacaoStore(s => s.adicionar);
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema)
  });

  function onSubmit(dados: FormData) {
    adicionar({ ...dados, data: new Date().toISOString() });
  }
}
```

## A lista com filtro

```tsx
function ListaTransacoes() {
  const transacoes = useTransacaoStore(s => s.transacoes);
  const remover = useTransacaoStore(s => s.remover);
  const [filtro, setFiltro] = useState<"todas" | "entrada" | "saida">("todas");

  const filtradas = transacoes.filter(t =>
    filtro === "todas" ? true : t.tipo === filtro
  );

  return (
    <ul>
      {filtradas.map(t => (
        <li key={t.id} className={t.tipo}>
          <span>{t.descricao}</span>
          <span>{t.categoria}</span>
          <strong className={t.tipo}>
            {t.tipo === "saida" ? "-" : "+"} R$ {t.valor.toFixed(2)}
          </strong>
          <button onClick={() => remover(t.id)}>×</button>
        </li>
      ))}
    </ul>
  );
}
```

## Critérios de nivelamento

- `Transacao` tipada com `tipo` literal union
- `resumo` derivado com `reduce` — sem estado duplicado
- Zod validando valor positivo e categoria
- `persist` no Zustand — dados sobrevivem
- Filtro é estado local — não na store

## Desafios extras

- Filtro por mês (`data.slice(0, 7)`)
- Categorias com cores
- Meta de gastos por categoria
- Exportar CSV
