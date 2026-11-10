# FE05-59 — Atividade: Lista de Frutas com TypeScript

## Objetivo

Refazer a lista de frutas com TypeScript — tipos de item, estado tipado, props tipadas e formulário validado.

## Os tipos

```typescript
// types/fruta.ts
interface Fruta {
  id: number;
  nome: string;
  emoji: string;
  calorias: number;
}

type FormFruta = Omit<Fruta, "id">; // sem id — o backend gera
```

## O estado

```tsx
function ListaFrutas() {
  const [frutas, setFrutas] = useState<Fruta[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    api.get<Fruta[]>("/frutas")
      .then(res => setFrutas(res.data))
      .catch(() => setErro("Erro ao carregar"))
      .finally(() => setCarregando(false));
  }, []);
}
```

## O formulário tipado

```tsx
function FormFruta({ onAdicionar }: { onAdicionar: (f: FormFruta) => void }) {
  const [form, setForm] = useState<FormFruta>({
    nome: "",
    emoji: "🍎",
    calorias: 0
  });

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    onAdicionar(form);
    setForm({ nome: "", emoji: "🍎", calorias: 0 });
  }
}
```

## O item tipado

```tsx
interface ItemFrutaProps {
  fruta: Fruta;
  onRemover: (id: number) => void;
  onEditar: (fruta: Fruta) => void;
}

function ItemFruta({ fruta, onRemover, onEditar }: ItemFrutaProps) {
  return (
    <li>
      <span>{fruta.emoji} {fruta.nome}</span>
      <small>{fruta.calorias} kcal</small>
      <button onClick={() => onEditar(fruta)}>Editar</button>
      <button onClick={() => onRemover(fruta.id)}>×</button>
    </li>
  );
}
```

## A lista com operações

```tsx
function ListaFrutas() {
  // ...

  async function remover(id: number) {
    await api.delete(`/frutas/${id}`);
    setFrutas(f => f.filter(fr => fr.id !== id));
  }

  async function adicionar(dados: FormFruta) {
    const res = await api.post<Fruta>("/frutas", dados);
    setFrutas(f => [...f, res.data]);
  }

  async function editar(fruta: Fruta) {
    const res = await api.put<Fruta>(`/frutas/${fruta.id}`, fruta);
    setFrutas(f => f.map(fr => fr.id === fruta.id ? res.data : fr));
  }
}
```

## O estado de edição

```tsx
const [editando, setEditando] = useState<Fruta | null>(null);

// abre o form com os dados
{editando && (
  <FormEdicao
    fruta={editando}
    fechar={() => setEditando(null)}
    onSalvar={editar}
  />
)}
```

## Filtro tipado

```tsx
const [busca, setBusca] = useState("");

const filtradas = frutas.filter(f =>
  f.nome.toLowerCase().includes(busca.toLowerCase())
);

// ou com tipo mais rigoroso
type FiltroFruta = "todas" | "comEmoji" | "semEmoji";

const [filtro, setFiltro] = useState<FiltroFruta>("todas");

const filtradas = frutas.filter(f => {
  if (filtro === "comEmoji") return f.emoji !== "";
  if (filtro === "semEmoji") return f.emoji === "";
  return true;
});
```

## Critérios de verificação

- `Fruta` e `FormFruta` como interfaces/tipos separados
- `useState<Fruta[]>` explícito
- `Omit<Fruta, "id">` para o form — sem id
- `keyof` para campos genéricos quando útil
- `FormEvent<HTMLFormElement>` no submit
- Edição com `Fruta | null` — controla qual está aberta

## Erros comuns

| Erro | Correção |
| --- | --- |
| `setFrutas` mutando | `setFrutas(f => [...f, nova])` |
| `form` sem tipo | `useState<FormFruta>` |
| `editando` sem tipo | `useState<Fruta \| null>(null)` |
| Evento sem tipo | `FormEvent`, `ChangeEvent` do React |
