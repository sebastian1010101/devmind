# BE02-45 — Prisma: Find com Relacionamento

## O default: relações NÃO vêm

```ts
const livro = await prisma.livro.findUnique({ where: { id: 1 } });
// livro.autor → undefined — só vem autorId (a FK)
```

É proposital: carregar relação = JOIN — o Prisma só faz quando você pede.

## include — trazendo relações

```ts
const autor = await prisma.autor.findUnique({
  where: { id: 1 },
  include: { livros: true },
});
// autor.livros → Livro[]

// múltiplas relações
include: { livros: true, perfil: true }
```

## include com opções — aninhado

```ts
const autor = await prisma.autor.findUnique({
  where: { id: 1 },
  include: {
    livros: {
      where: { anoPublicacao: { lt: 1900 } },
      orderBy: { titulo: "asc" },
      take: 5,
    },
  },
});
```

`include` aceita `where`, `orderBy`, `take`/`skip`, e `include`/`select` próprios.

## Include multinível

```ts
const curso = await prisma.curso.findUnique({
  where: { id: 1 },
  include: {
    matriculas: {
      include: { estudante: true },   // N-N explícito: junção → lado B
    },
  },
});
// curso.matriculas[].estudante.nome
```

## select — whitelist de campos

```ts
const autor = await prisma.autor.findUnique({
  where: { id: 1 },
  select: {
    nome: true,
    livros: {
      select: { titulo: true },      // só o título dos livros
    },
  },
});
// → { nome, livros: [{ titulo }] }
```

`select` aceita o mesmo aninhamento — e coexiste com relações (diferente de `include`, não pode misturar com `select` no mesmo nível).

| `include` | `select` |
| --- | --- |
| Todos os campos + as relações pedidas | Só o que você listou |
| Mais rápido de escrever | Mais preciso — ideal p/ API |

## count + include

```ts
const autores = await prisma.autor.findMany({
  include: {
    _count: { select: { livros: true } },
  },
});
// autores[0]._count.livros → 3
```

## O custo — N+1 não existe, mas JOIN existe

O Prisma resolve `include` com queries otimizadas (não é N+1 ingênuo). Mas cada `include` é tráfego e memória:

```ts
// ❌ traz tudo sempre
include: { livros: { include: { avaliacoes: { include: { usuario: true } } } } }

// ✅ traga só o que a rota precisa
select: { titulo: true, _count: { select: { avaliacoes: true } } }
```

## Erros comuns

| Erro | Correção |
| --- | --- |
| `autor.livros` undefined | Falta `include` ou `select` |
| `include` + `select` no mesmo nível | Inválido — ou um ou outro |
| N-N explícito esperando lado direto | Atravesse a junção: `include: { matriculas: { include: { estudante } } }` |
| Include profundo demais | Avalie select enxuto ou queries separadas |

## Resumo

- Relações não vêm por padrão — `include` ou `select` pedem explicitamente
- `include` traz tudo + relação; `select` traz só o listado (melhor para API)
- Aninhamento infinito: `include: { a: { include: { b: true } } }`
- `_count` conta filhos sem carregar objetos
