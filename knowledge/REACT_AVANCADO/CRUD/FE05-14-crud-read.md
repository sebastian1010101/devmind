# FE05-14 — CRUD: Read (Leitura)

## O fluxo de leitura

```text
Montagem → GET → resposta com array → setState → renderização da lista
```

## Read básico — lista completa

```jsx
function ListaNotas() {
  const [notas, setNotas] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);

  useEffect(() => {
    async function carregar() {
      try {
        const res = await api.get("/notas");
        setNotas(res.data);
      } catch (e) {
        setErro("Erro ao carregar");
      } finally {
        setCarregando(false);
      }
    }
    carregar();
  }, []);

  if (carregando) return <p>Carregando...</p>;
  if (erro) return <p>{erro}</p>;
  if (notas.length === 0) return <p>Nenhuma nota ainda.</p>;

  return (
    <ul>
      {notas.map(n => <ItemNota key={n.id} nota={n} />)}
    </ul>
  );
}
```

## Read de um item — detalhe

```jsx
function DetalheNota({ id }) {
  const [nota, setNota] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregar() {
      setCarregando(true);
      const res = await api.get(`/notas/${id}`);
      setNota(res.data);
      setCarregando(false);
    }
    carregar();
  }, [id]); // recarrega quando id muda

  if (carregando) return <p>Carregando...</p>;
  if (!nota) return <p>Nota não encontrada</p>;

  return (
    <article>
      <h2>{nota.titulo}</h2>
      <p>{nota.conteudo}</p>
      <small>{new Date(nota.criadaEm).toLocaleDateString("pt-BR")}</small>
    </article>
  );
}
```

## Read com filtros — query params

```jsx
const [filtro, setFiltro] = useState("");

const { dados: notas } = useFetch(
  filtro ? `/notas?busca=${filtro}` : "/notas"
);
```

Ou com objeto params do axios:

```jsx
const res = await api.get("/notas", {
  params: { busca: filtro, categoria: cat }
});
```

## Read com paginação

```jsx
const [pagina, setPagina] = useState(1);
const [temMais, setTemMais] = useState(true);

useEffect(() => {
  async function carregar() {
    const res = await api.get("/notas", {
      params: { _page: pagina, _limit: 10 }
    });
    setNotas(atual => [...atual, ...res.data]);
    setTemMais(res.data.length === 10);
  }
  carregar();
}, [pagina]);

<button
  onClick={() => setPagina(p => p + 1)}
  disabled={!temMais}
>
  Carregar mais
</button>
```

## Estados de leitura — o que mostrar

```jsx
if (carregando) return <Skeleton />;
if (erro) return <Erro mensagem={erro} tentar={recarregar} />;
if (notas.length === 0) return <ListaVazia criar={...} />;
return <Lista notas={notas} />;
```

Quatro estados: carregando, erro, vazio, dados.

## Refresh manual — re-executar o fetch

```jsx
const [atualizar, setAtualizar] = useState(0);

useEffect(() => {
  carregar();
}, [atualizar]); // muda → re-executa

<button onClick={() => setAtualizar(a => a + 1)}>Atualizar</button>
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `res.data` sem verificar array | `Array.isArray(res.data)` ou fallback `[]` |
| Fetch sem `[]` | Loop infinito |
| Lista sem `key` | `key={n.id}` — estável e única |
| Id na URL sem conversão | `useParams` retorna string |
| Sem estado vazio | Lista `[]` renderiza nada — mostre mensagem |

## Resumo

- Read = `useEffect` + `GET` + `setItens(res.data)`
- Item único: `GET /notas/${id}` com `[id]` como dep
- Filtros via `params` do axios ou query string
- Quatro estados: carregando, erro, vazio, dados
