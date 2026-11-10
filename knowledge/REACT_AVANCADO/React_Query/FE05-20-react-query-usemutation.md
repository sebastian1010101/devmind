# FE05-20 — React Query: useMutation

## O que é useMutation

O hook para **escrever dados** — POST, PUT, PATCH, DELETE. Diferente do `useQuery` (leitura automática), `useMutation` só executa quando chamado.

```jsx
const mutation = useMutation({
  mutationFn: (novaNota) => api.post("/notas", novaNota)
});

mutation.mutate({ titulo: "...", conteudo: "..." });
```

## O básico — criar

```jsx
function FormNota() {
  const queryClient = useQueryClient();

  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: (dados) => api.post("/notas", dados).then(r => r.data),

    onSuccess: (novaNota) => {
      // invalida o cache — lista refetch automático
      queryClient.invalidateQueries({ queryKey: ["notas"] });
    },

    onError: (erro) => {
      alert("Erro ao criar: " + erro.message);
    }
  });

  function handleSubmit(e) {
    e.preventDefault();
    mutate({ titulo, conteudo });
  }
}
```

## Os callbacks do ciclo de vida

```jsx
useMutation({
  mutationFn: criarNota,

  onMutate: async (novaNota) => {
    // antes de enviar — retorna contexto pra rollback
    await queryClient.cancelQueries(["notas"]);
    const anterior = queryClient.getQueryData(["notas"]);
    queryClient.setQueryData(["notas"], velho => [...velho, novaNota]);
    return { anterior };
  },

  onError: (erro, novaNota, contexto) => {
    // rollback otimista
    queryClient.setQueryData(["notas"], contexto.anterior);
  },

  onSettled: () => {
    // sempre — revalida
    queryClient.invalidateQueries({ queryKey: ["notas"] });
  }
});
```

## Atualizar cache diretamente — setQueryData

```jsx
onSuccess: (novaNota) => {
  // adiciona sem refetch — atualização otimista do cache
  queryClient.setQueryData(["notas"], (velhas = []) => [
    novaNota,
    ...velhas
  ]);
}
```

## Delete com useMutation

```jsx
const deletar = useMutation({
  mutationFn: (id) => api.delete(`/notas/${id}`),
  onSuccess: (_, idRemovido) => {
    queryClient.setQueryData(["notas"], (velhas) =>
      velhas.filter(n => n.id !== idRemovido)
    );
  }
});

<button onClick={() => deletar.mutate(nota.id)}>Excluir</button>
```

## Update

```jsx
const atualizar = useMutation({
  mutationFn: ({ id, dados }) =>
    api.put(`/notas/${id}`, dados).then(r => r.data),

  onSuccess: (notaAtualizada) => {
    queryClient.setQueryData(["notas"], (velhas) =>
      velhas.map(n => n.id === notaAtualizada.id ? notaAtualizada : n)
    );
  }
});

atualizar.mutate({ id: nota.id, dados: { titulo: "Novo" } });
```

## Estados da mutation

```jsx
const {
  mutate,      // dispara
  mutateAsync, // dispara e retorna Promise (await)
  isPending,   // em andamento
  isError,
  error,
  isSuccess,
  data,        // resposta da API
  reset        // limpa o estado
} = useMutation({ ... });
```

## mutate vs mutateAsync

```jsx
// mutate — fire and forget, callbacks no objeto
mutate(dados, {
  onSuccess: () => navigate("/notas")
});

// mutateAsync — await no fluxo
try {
  const nota = await mutateAsync(dados);
  navigate(`/notas/${nota.id}`);
} catch (e) {
  // trata
}
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| Mutation sem invalidar cache | `invalidateQueries` no `onSuccess` |
| `isLoading` (useQuery) em mutation | `isPending` — nome diferente |
| `mutate` sem esperar | `mutateAsync` + `await` se precisa do resultado |
| Cache velho após delete | `setQueryData` ou `invalidateQueries` |

## Resumo

- `useMutation` para escrita — executa só no `mutate`
- `onSuccess`/`onError`/`onSettled` para efeitos pós-mutação
- `invalidateQueries` rebusca; `setQueryData` atualiza direto
- `isPending` indica em andamento — desabilite o botão
