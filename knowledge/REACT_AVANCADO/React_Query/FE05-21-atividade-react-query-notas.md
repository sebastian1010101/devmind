# FE05-21 — Atividade: Refatorando Lista de Notas com React Query

## Objetivo

Pegar o CRUD de notas (FE05-17) — Context + useState + useEffect — e refatorar com React Query, eliminando o boilerplate de fetch.

## Antes — Context com fetch manual

```jsx
// ~50 linhas de estado + efeitos + actions
const [notas, setNotas] = useState([]);
const [carregando, setCarregando] = useState(true);
const [erro, setErro] = useState(null);

useEffect(() => { /* fetch, try/catch, finally */ }, []);
```

## Depois — React Query

```jsx
// Lista
function ListaNotas() {
  const { data: notas, isLoading, error } = useQuery({
    queryKey: ["notas"],
    queryFn: () => api.get("/notas").then(r => r.data)
  });

  if (isLoading) return <p>Carregando...</p>;
  if (error) return <p>Erro: {error.message}</p>;

  return (
    <ul>
      {notas.map(n => <ItemNota key={n.id} nota={n} />)}
    </ul>
  );
}
```

## A camada de serviço — separada

```jsx
// services/notas.js
export const notasApi = {
  listar: () => api.get("/notas").then(r => r.data),
  criar: (dados) => api.post("/notas", dados).then(r => r.data),
  atualizar: ({ id, dados }) => api.put(`/notas/${id}`, dados).then(r => r.data),
  remover: (id) => api.delete(`/notas/${id}`)
};
```

## Create com mutation

```jsx
function FormNota() {
  const queryClient = useQueryClient();
  const [titulo, setTitulo] = useState("");
  const [conteudo, setConteudo] = useState("");

  const criar = useMutation({
    mutationFn: notasApi.criar,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notas"] });
      setTitulo("");
      setConteudo("");
    }
  });

  function handleSubmit(e) {
    e.preventDefault();
    criar.mutate({ titulo, conteudo });
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={titulo} onChange={e => setTitulo(e.target.value)} />
      <textarea value={conteudo} onChange={e => setConteudo(e.target.value)} />
      <button disabled={criar.isPending}>
        {criar.isPending ? "Salvando..." : "Adicionar"}
      </button>
    </form>
  );
}
```

## Update com mutation

```jsx
function ItemNota({ nota }) {
  const queryClient = useQueryClient();
  const [editando, setEditando] = useState(false);
  const [titulo, setTitulo] = useState(nota.titulo);

  const atualizar = useMutation({
    mutationFn: notasApi.atualizar,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["notas"] });
      setEditando(false);
    }
  });

  const remover = useMutation({
    mutationFn: notasApi.remover,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["notas"] })
  });

  if (editando) {
    return (
      <div>
        <input value={titulo} onChange={e => setTitulo(e.target.value)} />
        <button onClick={() => atualizar.mutate({ id: nota.id, dados: { titulo } })}>
          Salvar
        </button>
        <button onClick={() => setEditando(false)}>Cancelar</button>
      </div>
    );
  }

  return (
    <li>
      <h3>{nota.titulo}</h3>
      <button onClick={() => setEditando(true)}>Editar</button>
      <button
        onClick={() => remover.mutate(nota.id)}
        disabled={remover.isPending}
      >
        Excluir
      </button>
    </li>
  );
}
```

## Hook customizado — useNotas

```jsx
// hooks/useNotas.js
export function useNotas() {
  const queryClient = useQueryClient();

  const notas = useQuery({
    queryKey: ["notas"],
    queryFn: notasApi.listar
  });

  const criar = useMutation({
    mutationFn: notasApi.criar,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["notas"] })
  });

  const atualizar = useMutation({
    mutationFn: notasApi.atualizar,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["notas"] })
  });

  const remover = useMutation({
    mutationFn: notasApi.remover,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["notas"] })
  });

  return { notas, criar, atualizar, remover };
}
```

```jsx
// componente — super limpo
function ListaNotas() {
  const { notas, remover } = useNotas();
  const { data, isLoading } = notas;

  if (isLoading) return <p>Carregando...</p>;
  return <ul>{data.map(n => ...)}</ul>;
}
```

## Comparação — antes vs depois

| Manual (Context) | React Query |
| --- | --- |
| `useState` para dados/loading/erro | `useQuery` retorna os três |
| `useEffect` com fetch | `queryFn` automático |
| Actions com setState | `useMutation` + invalidate |
| ~60 linhas de boilerplate | ~20 linhas |
| Cache inexistente | Cache automático por chave |

## Critérios de verificação

- `QueryClientProvider` no `main.jsx`
- `queryKey` consistente (`["notas"]` em tudo)
- Mutations invalidando o cache
- `isPending` desabilitando botões
- Serviço separado em `services/`

## Erros comuns

| Erro | Correção |
| --- | --- |
| Context + React Query duplicados | Query substitui o Context — remova |
| `invalidateQueries` com chave errada | `queryKey` idêntica à do `useQuery` |
| `mutationFn` sem retorno | Retorne `res.data` — fica no `data` da mutation |
| `useEffect` ainda no fetch | Delete — `useQuery` substitui |
