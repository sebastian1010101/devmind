# FE05-52 — Atividade: Tipando Estados no React

## Objetivo

Tipar os estados de um formulário e de uma lista de produtos — `useState` com tipo explícito, union com `null`, e estados derivados.

## O exercício — formulário de cadastro

```tsx
interface FormularioData {
  nome: string;
  email: string;
  idade: number | "";  // input pode ser vazio
}

function FormCadastro() {
  const [form, setForm] = useState<FormularioData>({
    nome: "",
    email: "",
    idade: ""
  });
  const [enviando, setEnviando] = useState(false);
  const [sucesso, setSucesso] = useState(false);

  function atualizar(campo: keyof FormularioData, valor: string) {
    setForm(f => ({
      ...f,
      [campo]: campo === "idade" ? (valor === "" ? "" : Number(valor)) : valor
    }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setEnviando(true);
    await api.post("/usuarios", form);
    setSucesso(true);
    setEnviando(false);
  }
}
```

## Estado de lista — array tipado

```tsx
interface Produto {
  id: number;
  nome: string;
  preco: number;
}

function ListaProdutos() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    async function carregar() {
      try {
        const res = await api.get<Produto[]>("/produtos");
        setProdutos(res.data);
      } catch {
        setErro("Falha ao carregar");
      } finally {
        setCarregando(false);
      }
    }
    carregar();
  }, []);
}
```

## Estado derivado — sem duplicar

```tsx
// ❌ estado separado — pode dessincronizar
const [total, setTotal] = useState(0);

// ✅ derivado — calcula sempre
const total = produtos.reduce((s, p) => s + p.preco, 0);
const emEstoque = produtos.filter(p => p.preco > 0);
```

## O union `T | null` — fetch inicial

```tsx
interface Detalhe {
  id: number;
  titulo: string;
}

const [detalhe, setDetalhe] = useState<Detalhe | null>(null);

// efeito
const res = await api.get<Detalhe>(`/detalhes/${id}`);
setDetalhe(res.data); // Detalhe | null

// render
if (!detalhe) return <p>Carregando...</p>;
// aqui detalhe é Detalhe — TS sabe
return <h1>{detalhe.titulo}</h1>;
```

## Estado de enum — status tipado

```tsx
type Status = "idle" | "carregando" | "sucesso" | "erro";

const [status, setStatus] = useState<Status>("idle");

setStatus("carregando");
setStatus("sucesso");
setStatus("banana"); // ❌ erro — não é Status
```

## Desafios extras

### Desafio A — estado de favoritos tipado

```tsx
const [favoritos, setFavoritos] = useState<Set<number>>(new Set());
// ou array
const [favoritos, setFavoritos] = useState<number[]>([]);
```

### Desafio B — formulário com validação

```tsx
interface Erros {
  nome?: string;
  email?: string;
}

const [erros, setErros] = useState<Erros>({});
```

### Desafio C — generic para lista

```tsx
function useLista<T>(inicial: T[]) {
  const [itens, setItens] = useState<T[]>(inicial);
  return { itens, setItens };
}
```

## Critérios de verificação

- `useState<Tipo>` explícito para objetos/arrays
- `T | null` para dados que começam vazios
- Union para status (`"idle" | "loading" | ...`)
- Estado derivado sem `useState` duplicado
- `keyof` para atualizar campos genéricos

## Erros comuns

| Erro | Correção |
| --- | --- |
| `useState([])` sem tipo | `useState<Produto[]>([])` |
| `idade: number` com input vazio | `number \| ""` ou `number \| null` |
| Estado duplicado de derivado | Calcule — não duplique |
| `FormEvent` sem tipo | `FormEvent` do React |
