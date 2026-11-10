# FE05-18 — React Query: Introdução e Instalação

## O que é React Query (TanStack Query)

Biblioteca de **gerenciamento de dados de servidor** — elimina o boilerplate de `useState` + `useEffect` + `fetch` para ler/escrever dados de API.

```jsx
// Sem React Query — ~20 linhas
const [dados, setDados] = useState([]);
const [carregando, setCarregando] = useState(true);
const [erro, setErro] = useState(null);
useEffect(() => { /* fetch, try/catch, finally */ }, []);

// Com React Query — 1 linha
const { data, isLoading, error } = useQuery({
  queryKey: ["produtos"],
  queryFn: () => api.get("/produtos").then(r => r.data)
});
```

## O que o React Query resolve

| Problema manual | React Query |
| --- | --- |
| Loading/error em todo fetch | `isLoading`, `error` automáticos |
| Cache — refetch a cada montagem | Cache inteligente por `queryKey` |
| Refetch manual | `refetch()` e invalidação automática |
| Retry manual | Retry embutido (3x padrão) |
| Dados velhos na tela | `staleTime`/`refetchOnWindowFocus` |
| Paginação/scroll infinito | `useInfiniteQuery` |

## Instalação e setup

```bash
npm install @tanstack/react-query
```

```jsx
// main.jsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")).render(
  <QueryClientProvider client={queryClient}>
    <App />
  </QueryClientProvider>
);
```

## A mentalidade — dados de servidor ≠ estado local

```text
Estado local (useState):     Dados de servidor (React Query):
- modal aberto               - lista de produtos
- input de formulário        - perfil do usuário
- tema claro/escuro          - carrinho da API
```

React Query gerencia **dados que vêm do servidor** — não substitui `useState` para UI.

## O DevTools

```bash
npm install @tanstack/react-query-devtools
```

```jsx
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

<QueryClientProvider client={queryClient}>
  <App />
  <ReactQueryDevtools initialIsOpen={false} />
</QueryClientProvider>
```

Painel para inspecionar queries, cache, mutations em tempo real.

## Erros comuns

| Erro | Correção |
| --- | --- |
| React Query pra estado local | `useState` — Query é só pra dados de servidor |
| `queryFn` que não retorna Promise | Deve retornar Promise ou valor |
| `queryKey` dinâmica fora do hook | `[ "produto", id ]` — muda → refetch automático |
| Provider faltando | `QueryClientProvider` no topo |

## Resumo

- React Query elimina boilerplate de fetch — cache, retry, loading automáticos
- `useQuery` para leitura; `useMutation` para escrita
- `queryKey` identifica e cacheia cada requisição
- Provider no `main.jsx` + DevTools para debug
