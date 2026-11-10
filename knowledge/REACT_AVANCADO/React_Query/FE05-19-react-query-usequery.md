# FE05-19 — React Query: useQuery

## O básico

```jsx
import { useQuery } from "@tanstack/react-query";

function Produtos() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["produtos"],          // chave do cache
    queryFn: () => api.get("/produtos").then(r => r.data)
  });

  if (isLoading) return <p>Carregando...</p>;
  if (error) return <p>Erro: {error.message}</p>;

  return <ul>{data.map(p => <li key={p.id}>{p.nome}</li>)}</ul>;
}
```

## queryKey — o identificador do cache

```jsx
// Estática — mesma lista sempre
queryKey: ["produtos"]

// Dinâmica — muda → refetch automático
queryKey: ["produto", id]
queryKey: ["produtos", { categoria, pagina }]
queryKey: ["usuario", usuarioId, "posts"]
```

A chave funciona como "endereço" do cache — mesma chave, mesmo dado.

## Os estados do useQuery

```jsx
const {
  data,           // dados do cache/resposta
  isLoading,      // primeira carga
  isFetching,     // qualquer refetch (incluindo de fundo)
  isError,
  error,          // objeto do erro
  refetch,        // função manual
  isStale         // cache expirado
} = useQuery({ ... });
```

## queryFn — a função de busca

Deve retornar uma **Promise** que resolve nos dados:

```jsx
// Com axios
queryFn: () => api.get("/produtos").then(r => r.data)

// Com fetch
queryFn: () =>
  fetch("/api/produtos").then(r => {
    if (!r.ok) throw new Error("Erro");
    return r.json();
  })

// Com contexto — params da queryKey
queryFn: ({ queryKey }) => {
  const [, id] = queryKey;
  return api.get(`/produtos/${id}`).then(r => r.data);
}
```

## Configurações essenciais

```jsx
useQuery({
  queryKey: ["produtos"],
  queryFn: buscar,

  staleTime: 1000 * 60 * 5,    // 5min "fresco" — sem refetch
  cacheTime: 1000 * 60 * 30,   // 30min no cache depois de inativo
  refetchOnWindowFocus: false, // não refaz ao focar a aba
  retry: 1,                     // tenta 1x só em erro
  enabled: !!id,                // só roda quando id existe
  refetchInterval: 30000        // polling a cada 30s
});
```

## Dependências — busca condicional

```jsx
// Só busca quando o usuário está logado
useQuery({
  queryKey: ["perfil"],
  queryFn: buscarPerfil,
  enabled: !!usuario // espera o login
});

// Depende de um id que pode mudar
useQuery({
  queryKey: ["produto", produtoId],
  queryFn: () => api.get(`/produtos/${produtoId}`),
  enabled: produtoId > 0
});
```

## Cache em ação — o comportamento padrão

```text
1ª montagem de "produtos":
  sem cache → isLoading → fetch → data

2ª montagem (outro componente, mesma chave):
  cache existe → mostra cache → refetch em fundo se stale
```

## refetch — atualização manual

```jsx
const { refetch } = useQuery({ ... });

<button onClick={() => refetch()}>Atualizar</button>
```

## Paginação — keepPreviousData

```jsx
const { data, isFetching } = useQuery({
  queryKey: ["produtos", pagina],
  queryFn: () => api.get(`/produtos?page=${pagina}`).then(r => r.data),
  keepPreviousData: true // mantém página anterior ao trocar
});
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `queryKey` com objeto novo a cada render | String/primitivos — ou objeto memoizado |
| `queryFn` que retorna `res` | Retorne `res.data` — dados, não Response |
| `isLoading` vs `isFetching` | `isLoading` = primeira carga; `isFetching` = qualquer refetch |
| Fetch mesmo com cache | `staleTime` define por quanto tempo é "fresco" |

## Resumo

- `useQuery({ queryKey, queryFn })` — leitura com cache automático
- `queryKey` identifica o dado — mudou → refetch
- `enabled` controla quando busca; `staleTime` controla o cache
- `isLoading` (1ª vez) vs `isFetching` (sempre que busca)
